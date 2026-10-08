"""Ordered fused lasso with unpenalised contextual nuisance effects.

Research code: score outcomes in held-out classrooms by removing a held-out
classroom intercept. This is *conditional within-context* validation, not a
claim to predict a new instructor-period's intercept.

The lambda penalty applies only to adjacent attendance steps. A test sample
used for post-selection Wald inference must never enter tune_fusion().
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse.linalg import lsqr
from sklearn.linear_model import Lasso


@dataclass
class PreparedFusion:
    y: np.ndarray
    visit: np.ndarray
    cluster: np.ndarray
    degree: np.ndarray
    order: tuple[str, ...]
    steps: np.ndarray
    residual_y: np.ndarray
    residual_steps: np.ndarray
    nuisance: sparse.csr_matrix
    degree_levels: tuple[str, ...]
    n_classrooms: int


def _strings(values: object, name: str) -> np.ndarray:
    arr = np.asarray(values, dtype=object).reshape(-1)
    if any(pd.isna(value) for value in arr):
        raise ValueError(f"{name} has missing values")
    return np.asarray([str(value) for value in arr], dtype=str)


def prepare_fusion(
    y: object,
    visit: object,
    cluster: object,
    degree: object,
    order: tuple[str, ...],
) -> PreparedFusion:
    """Partial out classroom FE and degree indicators before L1 fusion."""
    if len(order) < 2 or len(set(order)) != len(order):
        raise ValueError("order must have distinct levels, at least two")
    y_arr = np.asarray(y, dtype=float).reshape(-1)
    group = _strings(visit, "visit")
    classrooms = _strings(cluster, "cluster")
    degrees = _strings(degree, "degree")
    n = len(y_arr)
    if not (len(group) == len(classrooms) == len(degrees) == n):
        raise ValueError("All arrays must have equal length")
    if n < 10 or not np.isfinite(y_arr).all():
        raise ValueError("Too few or nonfinite observations")
    index = {name: i for i, name in enumerate(order)}
    if not set(group).issubset(index):
        raise ValueError("Unknown attendance group")
    group_index = np.asarray([index[g] for g in group], dtype=int)
    cls_levels, cls_index = np.unique(classrooms, return_inverse=True)
    deg_levels, deg_index = np.unique(degrees, return_inverse=True)
    if len(cls_levels) < 3:
        raise ValueError("At least three classrooms required")
    cls_dummies = sparse.csr_matrix(
        (np.ones(n), (np.arange(n), cls_index)),
        shape=(n, len(cls_levels)),
    )
    # Classroom indicators absorb intercept; drop one degree reference level.
    degree_dummies = sparse.csr_matrix(
        (np.ones(int((deg_index > 0).sum())),
         (np.flatnonzero(deg_index > 0), deg_index[deg_index > 0] - 1)),
        shape=(n, len(deg_levels) - 1),
    )
    nuisance = sparse.hstack((cls_dummies, degree_dummies), format="csr")
    steps = (group_index[:, None] >=
             np.arange(1, len(order))[None, :]).astype(float)

    def resid(vector: np.ndarray) -> np.ndarray:
        weights = lsqr(nuisance, vector, atol=1e-11, btol=1e-11,
                       iter_lim=4000)[0]
        return vector - nuisance @ weights

    resid_y = resid(y_arr)
    resid_steps = np.column_stack([resid(steps[:, j])
                                   for j in range(steps.shape[1])])
    return PreparedFusion(
        y=y_arr, visit=group, cluster=classrooms, degree=degrees,
        order=tuple(order), steps=steps,
        residual_y=resid_y, residual_steps=resid_steps,
        nuisance=nuisance, degree_levels=tuple(deg_levels),
        n_classrooms=len(cls_levels),
    )


def lambda_grid(prepared: PreparedFusion, *, count: int = 12) -> np.ndarray:
    """Include OLS/no penalty and a value just above the all-fused threshold."""
    if count < 4:
        raise ValueError("count must be >=4")
    upper = float(np.max(np.abs(
        prepared.residual_steps.T @ prepared.residual_y / len(prepared.y)
    )))
    if upper < 1e-12:
        return np.array([0.0, 1e-9, 1e-8, 1e-7])
    return np.r_[0.0, np.geomspace(upper * 1e-3, upper * 1.10, count - 1)]


def fit_prepared(
    prepared: PreparedFusion,
    lam: float,
    *,
    zero_tol: float = 1e-6,
) -> dict[str, object]:
    """Estimate cumulative step differences and unpenalised nuisance effects."""
    if lam < 0 or not np.isfinite(lam):
        raise ValueError("lambda must be finite and nonnegative")
    x = prepared.residual_steps
    y = prepared.residual_y
    if lam == 0:
        coefficients = np.linalg.lstsq(x, y, rcond=None)[0]
    else:
        fit = Lasso(alpha=float(lam), fit_intercept=False,
                    max_iter=80000, tol=1e-8, selection="cyclic")
        fit.fit(x, y)
        if fit.dual_gap_ > max(1e-6, 1e-5 * np.mean(y ** 2)):
            raise RuntimeError("Fused lasso did not converge sufficiently")
        coefficients = fit.coef_.copy()
    coefficients[np.abs(coefficients) < zero_tol] = 0.0
    levels = np.r_[0.0, np.cumsum(coefficients)]
    boundaries = tuple(int(k) for k in np.flatnonzero(
        np.abs(coefficients) > 0.0) + 1)
    blocks = np.zeros(len(prepared.order), dtype=int)
    for boundary in boundaries:
        blocks[boundary:] += 1
    # Reestimate unpenalised nuisance coefficients for the penalised steps.
    nuisance_coef = lsqr(
        prepared.nuisance, prepared.y - prepared.steps @ coefficients,
        atol=1e-11, btol=1e-11, iter_lim=4000
    )[0]
    degree_coef = {
        key: (0.0 if i == 0 else float(
            nuisance_coef[prepared.n_classrooms + i - 1]))
        for i, key in enumerate(prepared.degree_levels)
    }
    return {
        "lambda": float(lam),
        "step_coefficients": coefficients,
        "adjusted_levels_relative_zero": levels,
        "boundaries": boundaries,
        "block_ids": blocks,
        "n_blocks": len(boundaries) + 1,
        "degree_coefficients": degree_coef,
        "training_loss_within_context": float(np.mean(
            (y - x @ coefficients) ** 2
        )),
    }


def heldout_within_classroom_mse(
    fitted: dict[str, object],
    y: object,
    visit: object,
    cluster: object,
    degree: object,
    order: tuple[str, ...],
    allow_unseen_degree: bool = False,
) -> float:
    """MSE after removing each held-out classroom's mean residual.

    Degree effects are trained. The default is to reject unseen degrees;
    grouped_cv explicitly allows zero-reference fallback and logs its count.
    Classroom effects are *never* transferred from a disjoint training set.
    """
    group = _strings(visit, "visit")
    cls = _strings(cluster, "cluster")
    deg = _strings(degree, "degree")
    outcome = np.asarray(y, dtype=float)
    if not (len(outcome) == len(group) == len(cls) == len(deg)):
        raise ValueError("Held-out arrays must have matching lengths")
    mapping = {key: i for i, key in enumerate(order)}
    degree_effect = fitted["degree_coefficients"]
    if not set(group).issubset(mapping):
        raise ValueError("Unseen visit level in held-out fold")
    missing_degree = set(deg).difference(degree_effect)
    if missing_degree and not allow_unseen_degree:
        raise ValueError("Unseen degree level in held-out fold")
    indices = np.asarray([mapping[value] for value in group])
    steps = (indices[:, None] >= np.arange(1, len(order))[None, :])
    prediction = (
        steps @ fitted["step_coefficients"] +
        np.asarray([degree_effect.get(value, 0.0) for value in deg])
    )
    residual = outcome - prediction
    centered = residual - pd.Series(residual).groupby(
        pd.Series(cls), sort=False
    ).transform("mean").to_numpy()
    return float(np.mean(centered ** 2))


def grouped_cv(
    frame: pd.DataFrame,
    *,
    outcome: str,
    group: str,
    order: tuple[str, ...],
    folds: int = 4,
    repeats: int = 1,
    seed: int = 221,
    grid_size: int = 12,
) -> tuple[pd.DataFrame, float]:
    """Select lambda by grouped conditional loss with a one-SE parsimony rule.

    Fold scores are for hyperparameter selection, not independently unbiased
    out-of-sample performance or iid draws for significance testing.
    """
    if folds < 2 or repeats < 1:
        raise ValueError("folds>=2 and repeats>=1 required")
    p = prepare_fusion(frame[outcome], frame[group],
                       frame["CLASSROOM_ID"], frame["CLAVECARRERA"], order)
    grid = lambda_grid(p, count=grid_size)
    clusters = np.unique(p.cluster)
    if len(clusters) < folds * 2:
        raise ValueError("Too few clusters for grouped CV")
    rows = []
    for repetition in range(repeats):
        shuffled = np.random.default_rng(seed + repetition).permutation(clusters)
        for fold, held in enumerate(np.array_split(shuffled, folds)):
            mask = np.isin(p.cluster, held)
            tr = frame.loc[~mask].copy()
            te = frame.loc[mask].copy()
            prepared = prepare_fusion(tr[outcome], tr[group],
                                      tr["CLASSROOM_ID"], tr["CLAVECARRERA"], order)
            for lam in grid:
                fitted = fit_prepared(prepared, float(lam))
                score = heldout_within_classroom_mse(
                    fitted, te[outcome], te[group],
                    te["CLASSROOM_ID"], te["CLAVECARRERA"], order,
                    allow_unseen_degree=True,
                )
                unseen_degree_rows = int((~te["CLAVECARRERA"].astype(str).isin(
                    prepared.degree_levels)).sum())
                rows.append({
                    "lambda": float(lam), "repeat": repetition,
                    "fold": fold, "heldout_clusters": len(held),
                    "heldout_students": int(len(te)),
                    "unseen_degree_rows": unseen_degree_rows,
                    "within_classroom_mse": score,
                    "n_blocks": fitted["n_blocks"],
                })
    details = pd.DataFrame(rows)
    # Scores across repeated folds are dependent; this SE is a selection
    # heuristic, not a valid inferential SE.
    summary = details.groupby("lambda", as_index=False).agg(
        cv_mse=("within_classroom_mse", "mean"),
        cv_sd=("within_classroom_mse", "std"),
        evaluations=("fold", "size"),
        mean_blocks=("n_blocks", "mean"),
    )
    summary["cv_se_heuristic"] = (
        summary["cv_sd"].fillna(0) / np.sqrt(summary["evaluations"]))
    best = summary.loc[summary["cv_mse"].idxmin()]
    candidates = summary.loc[
        summary["cv_mse"] <= best["cv_mse"] + best["cv_se_heuristic"] + 1e-12
    ]
    chosen = float(candidates["lambda"].max())
    summary["selected_lambda"] = summary["lambda"].eq(chosen)
    return summary.sort_values("lambda").reset_index(drop=True), chosen


def cluster_split(
    frame: pd.DataFrame,
    *,
    validation_fraction: float = 0.30,
    seed: int = 221,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Reserve entire instructor-periods for locked Wald validation."""
    if not 0.1 <= validation_fraction <= 0.5:
        raise ValueError("validation_fraction must be within [0.1, 0.5]")
    clusters = _strings(frame["CLASSROOM_ID"], "CLASSROOM_ID")
    unique = np.unique(clusters)
    if len(unique) < 30:
        raise ValueError("Too few clusters for honest splitting")
    shuffled = np.random.default_rng(seed).permutation(unique)
    count = max(1, int(round(len(unique) * validation_fraction)))
    validation = np.isin(clusters, shuffled[:count])
    return frame.loc[~validation].copy(), frame.loc[validation].copy()


def resample_cluster_rows(frame: pd.DataFrame, *, seed: int) -> pd.DataFrame:
    """Cluster bootstrap; clone labels make duplicated draws independent FE."""
    rng = np.random.default_rng(seed)
    labels = frame["CLASSROOM_ID"].astype(str)
    clusters = labels.drop_duplicates().to_numpy()
    drawn = rng.choice(clusters, size=len(clusters), replace=True)
    chunks = []
    for i, value in enumerate(drawn):
        part = frame.loc[labels.eq(value)].copy()
        # Pandas compares attrs during concat. Cohort attrs may include a
        # DataFrame, whose equality is not a scalar boolean; drop metadata
        # only on the bootstrap copy, never on the original cohort.
        part.attrs.clear()
        part["CLASSROOM_ID"] = f"resample_{i}"
        chunks.append(part)
    return pd.concat(chunks, ignore_index=True)


def selected_partition(order: tuple[str, ...], boundaries: tuple[int, ...]) -> list[dict]:
    """Human-readable contiguous regimes; boundary positions start at 1."""
    boundaries = tuple(sorted(set(int(k) for k in boundaries)))
    edges = (0,) + boundaries + (len(order),)
    if any(b <= 0 or b >= len(order) for b in boundaries):
        raise ValueError("Out-of-range boundary")
    return [
        {"block": f"B{i}", "first": order[a], "last": order[b-1],
         "members": "|".join(order[a:b]), "n_levels": b-a}
        for i, (a, b) in enumerate(zip(edges[:-1], edges[1:]))
    ]


def exhaustive_contiguous_partitions(prepared: PreparedFusion) -> pd.DataFrame:
    """Compare every contiguous partition using discovery-sample fit only.

    Reports a *relative* Gaussian BIC ranking with the same unpenalised FE and
    degree nuisance controls across partitions. This is model selection, not a
    null-hypothesis p-value or an independent prediction score.
    """
    x = prepared.residual_steps
    y = prepared.residual_y
    n = len(y)
    m = x.shape[1]
    rows: list[dict[str, object]] = []
    for mask in range(1 << m):
        chosen = tuple(j for j in range(m) if mask & (1 << j))
        if chosen:
            design = x[:, list(chosen)]
            coefficients = np.linalg.lstsq(design, y, rcond=None)[0]
            errors = y - design @ coefficients
        else:
            errors = y
        sse = float(errors @ errors)
        bic_relative = float(n * np.log(max(sse / n, 1e-15)) +
                             len(chosen) * np.log(n))
        rows.append({
            "partition_mask": mask,
            "boundaries": "|".join(
                f"{prepared.order[j]}|{prepared.order[j+1]}" for j in chosen
            ),
            "n_blocks": len(chosen) + 1,
            "sse": sse,
            "conditional_r2": 1.0 - sse / float(y @ y)
                if float(y @ y) > 0 else np.nan,
            "bic_relative": bic_relative,
        })
    result = pd.DataFrame(rows).sort_values(
        ["bic_relative", "n_blocks"]).reset_index(drop=True)
    result["bic_delta_best"] = result["bic_relative"] - result["bic_relative"].min()
    result["rank_bic"] = np.arange(1, len(result) + 1)
    return result
