#!/usr/bin/env python3
"""Exploratory attendance curves: first-visit jump, linear vs diminishing trends.

All estimators describe associations in the historical Paper 2.1 cohort.
Only aggregate tables, figures and a generated report are exported. Never
commit institutional microdata, model design matrices or individual predictions.
"""
from __future__ import annotations

import argparse
import math
from dataclasses import replace
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import norm
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from statsmodels.stats.multitest import multipletests

from run_paper21_model_controls_experiment import ROOT, GROUPS

TABLES = ROOT / "results/paper21/tables/attendance_curves"
FIGURES = ROOT / "results/paper21/figures/attendance_curves"
NOTE = ROOT / "notes/24_ATTENDANCE_CURVE_RESULTS.md"
# Imputed Z is comparable with the preceding Holm/Shapley studies.
# Numeric-only outcomes are separate conditional-on-numeric-grade sensitivities.
OUTCOMES = (
    ("Z_GRADE_PRIMARY", "imputed_z"),
    ("PASS", "pass_lpm"),
    ("Z_GRADE_COMPLETE_CASE", "numeric_only_z"),
    ("GRADE_NUMERIC", "observed_numeric_grade"),
)
SHAPES = ("linear", "log", "sqrt", "categories")
FEATURE = {"linear": "EXTRA_LINEAR", "log": "EXTRA_LOG",
           "sqrt": "EXTRA_SQRT"}


def curve_values(visits: np.ndarray) -> dict[str, np.ndarray]:
    """Zero vs any + capped positive-frequency increments; 7 means 7+."""
    visits = np.asarray(visits, dtype=float)
    if not np.isfinite(visits).all() or (visits < 0).any() or (
        visits != np.floor(visits)
    ).any():
        raise ValueError("Visits must be finite nonnegative integers")
    capped = np.minimum(visits, 7)
    positive = np.maximum(capped, 1)
    return {
        "ANY_VISIT": (capped > 0).astype(float),
        "EXTRA_LINEAR": np.maximum(capped - 1, 0),
        "EXTRA_LOG": np.log(positive),
        "EXTRA_SQRT": np.sqrt(positive) - 1,
    }


def make_design(frame: pd.DataFrame, outcome: str) -> pd.DataFrame:
    if outcome not in dict(OUTCOMES):
        raise ValueError("Unexpected outcome")
    required = [outcome, "CLASSROOM_ID", "CLAVECARRERA", "VISITS_CMAT_PERIOD"]
    missing = set(required).difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    d = frame.dropna(subset=required).copy()
    d.attrs.clear()  # upstream pandas .attrs contains a nested audit DataFrame
    if not np.isfinite(d[outcome].to_numpy(dtype=float)).all():
        raise ValueError(f"Nonfinite values in {outcome}")
    if outcome == "PASS" and not d[outcome].isin((0, 1)).all():
        raise ValueError("PASS is not binary")
    visits = d["VISITS_CMAT_PERIOD"].to_numpy(dtype=float)
    for name, values in curve_values(visits).items():
        d[name] = values
    capped = np.minimum(visits, 7).astype(int)
    labels = np.where(capped == 7, "7+", capped.astype(str))
    d["VISIT_GROUP"] = pd.Categorical(labels, categories=GROUPS, ordered=True)
    if set(d["VISIT_GROUP"].dropna().astype(str)) != set(GROUPS):
        raise ValueError("All eight visit-frequency categories must be present")
    return d


def exposure_terms(shape: str) -> str:
    if shape == "categories":
        return "C(VISIT_GROUP, Treatment(reference='0'))"
    if shape not in FEATURE:
        raise ValueError(f"Unknown curve shape: {shape}")
    return f"ANY_VISIT + {FEATURE[shape]}"


def basis(shape: str, k: int, names: list[str]) -> np.ndarray:
    """Coefficient-space contrast for category k vs zero attendance."""
    if k not in range(8):
        raise ValueError("k must be an integer from 0 through 7 (=7+)")
    vec = np.zeros(len(names))
    if k == 0:
        return vec
    if shape == "categories":
        label = "7+" if k == 7 else str(k)
        term = f"C(VISIT_GROUP, Treatment(reference='0'))[T.{label}]"
        vec[names.index(term)] = 1.0
    else:
        values = curve_values(np.array([k]))
        vec[names.index("ANY_VISIT")] = 1.0
        vec[names.index(FEATURE[shape])] = float(values[FEATURE[shape]][0])
    return vec


def estimate_contrast(fit, left: np.ndarray, right: np.ndarray) -> dict:
    """Cluster-robust contrast using fitted coefficient covariance."""
    vec = right - left
    beta = fit.params.to_numpy(dtype=float)
    cov = fit.cov_params().to_numpy(dtype=float)
    effect = float(vec @ beta)
    variance = float(vec @ cov @ vec)
    if variance < 0 and abs(variance) < 1e-12:
        variance = 0
    se = math.sqrt(variance) if variance >= 0 else float("nan")
    if not (np.isfinite(effect) and np.isfinite(se)):
        raise RuntimeError("Nonfinite cluster-robust contrast")
    p = float(2*norm.sf(abs(effect/se))) if se > 0 else float("nan")
    return dict(estimate=effect, se_clustered=se,
                ci95_low=effect-1.95996398454*se,
                ci95_high=effect+1.95996398454*se, p_raw=p)


def fit_shape(d: pd.DataFrame, outcome: str, shape: str):
    formula = (f"{outcome} ~ {exposure_terms(shape)}"
               " + C(CLASSROOM_ID) + C(CLAVECARRERA)")
    fit = smf.ols(formula, data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d["CLASSROOM_ID"]}
    )
    if not np.isfinite(fit.params.to_numpy()).all():
        raise RuntimeError("Invalid coefficient vector")
    return fit, formula


def observed_means(d: pd.DataFrame, outcome: str) -> pd.DataFrame:
    # Clustered group means (unadjusted), not independent-student SEs.
    fit = smf.ols(f"{outcome} ~ 0 + C(VISIT_GROUP)", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d["CLASSROOM_ID"]}
    )
    counts = d.groupby("VISIT_GROUP", observed=True).size()
    contexts = d.groupby("VISIT_GROUP", observed=True)["CLASSROOM_ID"].nunique()
    rows = []
    for k, label in enumerate(GROUPS):
        term = f"C(VISIT_GROUP)[{label}]"
        mu = float(fit.params[term])
        se = float(fit.bse[term])
        rows.append(dict(outcome=outcome, visits=label, k=k,
                         n=int(counts.loc[label]), clusters=int(contexts.loc[label]),
                         unadjusted_mean=mu, se_clustered=se,
                         ci95_low=mu-1.95996398454*se,
                         ci95_high=mu+1.95996398454*se))
    return pd.DataFrame(rows)


def fitted_shapes(d: pd.DataFrame, outcome: str):
    """Fit nested-free working shapes on identical complete cases per outcome."""
    means = observed_means(d, outcome)
    allfits, curves, adjacent = [], [], []
    for shape in SHAPES:
        fit, formula = fit_shape(d, outcome, shape)
        allfits.append(dict(
            outcome=outcome, shape=shape, n=len(d),
            clusters=int(d["CLASSROOM_ID"].nunique()), aic=float(fit.aic),
            bic=float(fit.bic), r2_in_sample=float(fit.rsquared),
            adjusted_r2_in_sample=float(fit.rsquared_adj),
            df_model=float(fit.df_model), formula=formula
        ))
        names = list(fit.params.index)
        for k, label in enumerate(GROUPS):
            contrast = estimate_contrast(
                fit, basis(shape, 0, names), basis(shape, k, names)
            )
            curves.append(dict(outcome=outcome, shape=shape,
                               visits=label, k=k, **contrast))
        if shape == "categories":
            for k in range(1, 8):
                contrast = estimate_contrast(
                    fit, basis(shape, k-1, names), basis(shape, k, names)
                )
                adjacent.append(dict(
                    outcome=outcome, comparison=f"{GROUPS[k-1]}->{GROUPS[k]}",
                    k_from=k-1, k_to=k, **contrast
                ))
    adjacent_table = pd.DataFrame(adjacent)
    # Explicitly different from the old 15/21/28 Holm families.
    pvals = adjacent_table["p_raw"].to_numpy(dtype=float)
    adjacent_table["p_holm_7_adjacent"] = (
        multipletests(pvals, method="holm")[1]
        if np.isfinite(pvals).all() else np.nan
    )
    return means, pd.DataFrame(allfits), pd.DataFrame(curves), adjacent_table


def grouped_cv(d: pd.DataFrame, outcome: str, folds: int = 5) -> pd.DataFrame:
    """Prospective-classroom holdout for *shape comparison only*.

    Omits classroom FE because test classrooms are unseen. Degree one-hot
    coding is fitted inside each training fold. No student-level output.
    """
    groups = d["CLASSROOM_ID"].astype(str).to_numpy()
    if len(np.unique(groups)) < folds:
        raise ValueError("Insufficient professor-period groups")
    y = d[outcome].to_numpy(dtype=float)
    base_pred = np.zeros_like(y)
    splits = list(GroupKFold(n_splits=folds).split(y, y, groups))
    for train, test in splits:
        base_pred[test] = np.mean(y[train])
    baseline_error = float(np.mean((y-base_pred)**2))
    if baseline_error <= 0:
        raise RuntimeError("Degenerate grouped validation baseline")

    output = []
    for shape in SHAPES:
        # Convert to raw arrays before building a clean DataFrame to avoid
        # comparing nested DataFrames in pandas 3 inherited .attrs.
        base = {"degree": d["CLAVECARRERA"].to_numpy(dtype=str)}
        if shape == "categories":
            base["visits"] = d["VISIT_GROUP"].astype(str).to_numpy()
            categorical = ["degree", "visits"]
            numeric = []
        else:
            base["any"] = d["ANY_VISIT"].to_numpy(dtype=float)
            base["extra"] = d[FEATURE[shape]].to_numpy(dtype=float)
            categorical = ["degree"]
            numeric = ["any", "extra"]
        X = pd.DataFrame(base)
        predictions = np.zeros_like(y)
        for train, test in splits:
            transform = ColumnTransformer(
                [("cat", OneHotEncoder(handle_unknown="ignore"), categorical)]
                + ([("numeric", "passthrough", numeric)] if numeric else [])
            )
            model = make_pipeline(transform, LinearRegression())
            model.fit(X.iloc[train], y[train])
            predictions[test] = model.predict(X.iloc[test])
        # LPM is kept on the binary-outcome scale; probability predictions
        # are clipped only for the held-out Brier comparison.
        if outcome == "PASS":
            predictions = np.clip(predictions, 0, 1)
        error = float(np.mean((y-predictions)**2))
        output.append(dict(outcome=outcome, shape=shape,
                           folds=folds, n=len(d),
                           error_metric=("brier" if outcome == "PASS" else "mse"),
                           cv_error=error, cv_baseline=baseline_error,
                           cv_skill=1.0-error/baseline_error,
                           cv_rmse=float(np.sqrt(error)),
                           classroom_fe_in_cv=False))
    return pd.DataFrame(output)


def save_plot(outcome: str, means: pd.DataFrame,
              curves: pd.DataFrame, path: Path) -> None:
    """Two panels deliberately separate raw means from adjusted differences."""
    selection = curves.loc[curves["outcome"].eq(outcome)]
    raw = means.loc[means["outcome"].eq(outcome)].sort_values("k")
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 4.5))
    ax.errorbar(raw["k"], raw["unadjusted_mean"],
                yerr=1.95996398454*raw["se_clustered"], fmt="o-", capsize=3)
    ax.set_title(f"{outcome}: observed group means")
    ax.set_ylabel("Outcome (original units)")
    ax.set_xlabel("Recorded CMAT visits")
    for shape, style in (("categories", "o-"), ("linear", "--"),
                         ("log", "-"), ("sqrt", "-.")):
        g = selection.loc[selection["shape"].eq(shape)].sort_values("k")
        bx.plot(g["k"], g["estimate"], style, label=shape)
        if shape == "categories":
            bx.errorbar(g["k"], g["estimate"],
                        yerr=1.95996398454*g["se_clustered"],
                        fmt="none", capsize=3)
        if shape == "log":
            bx.fill_between(g["k"].to_numpy(dtype=float),
                            g["ci95_low"].to_numpy(dtype=float),
                            g["ci95_high"].to_numpy(dtype=float), alpha=.12)
    bx.axhline(0, linestyle=":", linewidth=.8)
    bx.set_title("Adjusted difference vs zero visits")
    bx.set_ylabel("OLS contrast (SD / grade points / probability)")
    bx.set_xlabel("Recorded CMAT visits")
    bx.legend(fontsize=8)
    for axis in (ax, bx):
        axis.set_xticks(range(8), GROUPS)
    fig.suptitle("Exploratory: 7+ is top-coded; clustered 95% intervals")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    plt.close(fig)


def report(means: pd.DataFrame, fits: pd.DataFrame, curves: pd.DataFrame,
           adjacent: pd.DataFrame, cv: pd.DataFrame) -> str:
    lines = [
        "# 24 — Attendance curve comparison (exploratory; generated)",
        "",
        "Four outcomes: imputed professor-period Z, PASS LPM, numeric-only Z",
        "and observed numeric final grade (last two condition on numeric results).",
        "No CMAT causal effects are estimated. All confidence intervals use",
        "professor-period clustered sandwich covariance.",
        "",
        "## Model comparison",
        "",
        "All in-sample shapes use degree and professor-period fixed effects.",
        "Five-fold grouped CV **excludes** professor-period fixed effects because",
        "test contexts were not observed in training; it includes degree, and",
        "compares shape generalization using squared error or binary Brier.",
        "In-sample AIC/BIC and out-of-context CV score are not the same estimand.",
        "",
        "| Outcome | Shape | R² in sample | AIC | Held-out skill | CV error |",
        "|---|---|---:|---:|---:|---:|",
    ]
    full = fits.merge(cv, on=["outcome", "shape"], validate="one_to_one")
    for r in full.itertuples():
        lines.append(f"| {r.outcome} | {r.shape} | {r.r2_in_sample:.4f} | "
                     f"{r.aic:.1f} | {r.cv_skill:.4f} | {r.cv_error:.4f} |")
    lines += [
        "",
        "## Raw attendance-frequency means (unadjusted)",
        "",
        "| Outcome | Visits | N | Clusters | Mean | 95% clustered CI |",
        "|---|---|---:|---:|---:|---|",
    ]
    for r in means.itertuples():
        lines.append(f"| {r.outcome} | {r.visits} | {r.n} | {r.clusters} | "
                     f"{r.unadjusted_mean:.3f} | [{r.ci95_low:.3f}, "
                     f"{r.ci95_high:.3f}] |")
    lines += [
        "",
        "## Adjusted category contrasts and their uncertainty",
        "",
        "The unrestricted eight-category model does NOT assume a monotone trend.",
        "Its 5→6 interval is the relevant check for the observed late dip.",
        "Intervals are nominal unless explicitly labeled Holm.",
        "",
        "| Outcome | Visits versus zero | Difference | 95% clustered CI |",
        "|---|---|---:|---|",
    ]
    c = curves.loc[curves["shape"].eq("categories") & curves["k"].gt(0)]
    for r in c.itertuples():
        lines.append(f"| {r.outcome} | {r.visits} | {r.estimate:.3f} | "
                     f"[{r.ci95_low:.3f}, {r.ci95_high:.3f}] |")
    lines += [
        "",
        "## Unrestricted adjacent contrasts: 7-comparison Holm family / outcome",
        "",
        "| Outcome | Pair | Estimate | Nominal CI95 | Holm p |",
        "|---|---|---:|---|---:|",
    ]
    for r in adjacent.itertuples():
        lines.append(f"| {r.outcome} | {r.comparison} | {r.estimate:.3f} | "
                     f"[{r.ci95_low:.3f}, {r.ci95_high:.3f}] | "
                     f"{r.p_holm_7_adjacent:.4f} |")
    lines += [
        "",
        "## Interpretive boundaries",
        "",
        "- Log and square-root fits *impose* declining additional-visit increments.",
        "  A favorable CV score does not prove the underlying causal response is concave.",
        "- The log coefficient begins at visit 1: it cannot by itself identify",
        "  a treatment effect of an exogenously assigned first CMAT visit.",
        "- Group 7+ combines seven and more visits, not exact seven.",
        "- Original numeric final grades have an upper bound of 10 and",
        "  numeric-only subsets exclude BA/BV/RT, whereas primary Z imputes them.",
        "- Group-count and professor-period overlap are highly unequal; the",
        "  5→6 contrast may have much greater uncertainty than 0→1.",
        "- This exploratory family (seven adjacent contrasts per outcome)",
        "  does not replace earlier 15/21/28-comparison Holm inferences.",
        "- Recorded visits accumulate over the same term as outcomes; motivation,",
        "  prior preparation, persistence and administrative outcomes may confound",
        "  the association. No early-warning interpretation is justified.",
        "",
        "Figures are at results/paper21/figures/attendance_curves/*.png.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--materias", type=Path)
    parser.add_argument("--asesorias", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        v = curve_values(np.array([0, 1, 2, 5, 6, 7, 11]))
        assert v["EXTRA_LINEAR"].tolist() == [0, 0, 1, 4, 5, 6, 6]
        assert np.all(np.diff(curve_values(np.arange(1, 8))["EXTRA_LOG"], n=2) < 0)
        print("Curve basis and top-coding contract valid; no institutional inputs loaded.")
        return 0

    from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
    from cmat_analysis.measures import add_primary_outcomes

    cfg = get_study_config(ROOT)
    cfg = replace(cfg,
                  materias_path=(args.materias or cfg.materias_path).expanduser().resolve(),
                  asesorias_path=(args.asesorias or cfg.asesorias_path).expanduser().resolve())
    for path in (cfg.materias_path, cfg.asesorias_path):
        if not path.is_file():
            raise SystemExit(f"Missing authorized institutional input: {path}")
    cohort = add_primary_outcomes(build_study_cohorts(
        load_and_clean_inputs(cfg), cfg)["mu_primary"], cfg)
    if len(cohort) != 6627 or cohort["CLASSROOM_ID"].nunique() != 190:
        raise RuntimeError("Study cohort differs from validated Paper 2.1 contract")

    allmeans, allfits, allcurves, alladjacent, allcv = [], [], [], [], []
    for outcome, label in OUTCOMES:
        d = make_design(cohort, outcome)
        print(f"Curve fitting: {outcome} / n={len(d)}", flush=True)
        means, fits, curves, adjacent = fitted_shapes(d, outcome)
        print(f"Group-heldout CV: {outcome}", flush=True)
        cv = grouped_cv(d, outcome)
        allmeans.append(means); allfits.append(fits)
        allcurves.append(curves); alladjacent.append(adjacent); allcv.append(cv)
        save_plot(outcome, means, curves, FIGURES / f"{label}_attendance_curve.png")

    means = pd.concat(allmeans, ignore_index=True)
    fits = pd.concat(allfits, ignore_index=True)
    curves = pd.concat(allcurves, ignore_index=True)
    adjacent = pd.concat(alladjacent, ignore_index=True)
    cv = pd.concat(allcv, ignore_index=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    for file, frame in (
        ("unadjusted_means_cluster_ci.csv", means),
        ("model_comparison_in_sample.csv", fits),
        ("adjusted_curves_cluster_ci.csv", curves),
        ("adjacent_differences_holm.csv", adjacent),
        ("group_heldout_shape_cv.csv", cv),
    ):
        frame.to_csv(TABLES / file, index=False)
    NOTE.write_text(report(means, fits, curves, adjacent, cv), encoding="utf-8")
    print(f"Aggregate results: {TABLES}")
    print(f"Four figures: {FIGURES}")
    print(f"Report: {NOTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
