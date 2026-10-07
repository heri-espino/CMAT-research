#!/usr/bin/env python3
"""Paper 2.1 dual-outcome analysis using the shared cmat_analysis library.

Paper-specific code constructs the cohort, freezes the documented grouping, and
formats publication outputs. Reusable grouping, outcome-state construction,
clustered fixed-effect comparisons, distribution profiles, and effect matrices
live in cmat_analysis on main.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from itertools import combinations
from math import factorial
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

try:
    from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
    from cmat_analysis.measures import add_academic_outcome_states, add_primary_outcomes
    from cmat_analysis.statistics import (
        add_topcoded_visit_group,
        distribution_profile,
        fixed_effect_group_comparisons,
        fixed_effect_logistic_group_comparisons,
        group_outcome_summary,
        mixture_component_density,
        outcome_state_composition,
        pairwise_effect_matrix,
    )
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Paper 2.1 requires the shared editable library. From the repository root run:\n"
        '  python -m pip install -e "./cmat_analysis[dev]"\n'
        f"Original import error: {exc}"
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = REPO_ROOT / "results" / "paper21" / "tables"
GROUP_SPEC = REPO_ROOT / "paper" / "visit_grouping_spec.json"


def _save(frame: pd.DataFrame, name: str) -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    frame.to_csv(TABLES_DIR / name, index=False)


def _format_descriptives(
    frame: pd.DataFrame,
    *,
    specification: str,
) -> pd.DataFrame:
    out = frame.rename(
        columns={
            "outcome_mean": "mean_z",
            "outcome_sd": "sd_z",
            "outcome_ci95_low": "z_ci95_low",
            "outcome_ci95_high": "z_ci95_high",
            "binary_rate": "pass_rate",
            "binary_ci95_low": "pass_ci95_low",
            "binary_ci95_high": "pass_ci95_high",
        }
    ).copy()
    out.insert(0, "specification", specification)
    return out


def _format_pairwise(
    pairwise: pd.DataFrame,
    info: pd.DataFrame,
    *,
    outcome: str,
    specification: str,
) -> pd.DataFrame:
    out = pairwise.rename(
        columns={
            "estimate_group1_minus_group2": "adjusted_difference_group1_minus_group2",
            "ci_low": "ci95_low",
            "ci_high": "ci95_high",
            "p_adjusted": "p_holm",
            "reject_adjusted": "reject_holm_0_05",
        }
    ).copy()
    out.insert(0, "outcome", outcome)
    out.insert(0, "specification", specification)
    out["n_instructor_period_groups"] = int(info.loc[0, "n_fixed_effect_levels"])
    return out


def _format_omnibus(
    omnibus: pd.DataFrame,
    info: pd.DataFrame,
    *,
    outcome: str,
    specification: str,
) -> pd.DataFrame:
    out = omnibus.copy()
    out.insert(0, "outcome", outcome)
    out.insert(0, "specification", specification)
    out["n_instructor_period_groups"] = int(info.loc[0, "n_fixed_effect_levels"])
    out["covariance"] = f"cluster-robust by {info.loc[0, 'cluster_col']}"
    out["adjustment"] = "instructor-period fixed effects + degree-programme indicators"
    return out


def _fit(
    data: pd.DataFrame,
    *,
    group_col: str,
    group_order: list[str],
    outcome_col: str,
    outcome_label: str,
    specification: str,
    cluster_col: str = "CLASSROOM_ID",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    pairwise, omnibus, info = fixed_effect_group_comparisons(
        data,
        group_col=group_col,
        group_order=group_order,
        outcome_col=outcome_col,
        fixed_effect_col="CLASSROOM_ID",
        cluster_col=cluster_col,
        categorical_covariates=["CLAVECARRERA"],
        multiplicity_method="holm",
    )
    return (
        _format_pairwise(
            pairwise, info, outcome=outcome_label, specification=specification
        ),
        _format_omnibus(
            omnibus, info, outcome=outcome_label, specification=specification
        ),
    )


def _benchmark(
    data: pd.DataFrame,
    outcome_col: str,
    outcome_label: str,
    *,
    cluster_col: str = "CLASSROOM_ID",
) -> dict[str, object]:
    x = data.copy()
    x["ATTENDANCE_BINARY_GROUP"] = np.where(
        x["VISITS_CMAT_PERIOD"].gt(0), "1+", "0"
    )
    pairwise, _, info = fixed_effect_group_comparisons(
        x,
        group_col="ATTENDANCE_BINARY_GROUP",
        group_order=["0", "1+"],
        outcome_col=outcome_col,
        fixed_effect_col="CLASSROOM_ID",
        cluster_col=cluster_col,
        categorical_covariates=["CLAVECARRERA"],
    )
    row = pairwise.iloc[0]
    return {
        "outcome": outcome_label,
        "comparison": "1+ visits minus 0 visits",
        "adjusted_difference": -float(row["estimate_group1_minus_group2"]),
        "cluster_robust_se": float(row["cluster_robust_se"]),
        "ci95_low": -float(row["ci_high"]),
        "ci95_high": -float(row["ci_low"]),
        "p_value": float(row["p_raw"]),
        "n": int(row["n"]),
        "n_instructor_period_groups": int(info.loc[0, "n_fixed_effect_levels"]),
        "cluster_col": cluster_col,
        "n_clusters": int(info.loc[0, "n_clusters"]),
    }


def benchmark_model_diagnostics(
    data: pd.DataFrame,
    outcome_col: str,
    outcome_label: str,
    *,
    cluster_col: str = "CLASSROOM_ID",
) -> dict[str, pd.DataFrame]:
    """Audit the binary-attendance benchmark beyond its headline coefficient.

    The diagnostic keeps one common complete-case sample and treats three
    predictor blocks separately: attendance, degree programme, and
    instructor-period fixed effects. It returns the sequential R-squared path,
    all subset fits, an exact blockwise Shapley decomposition of R-squared,
    conditional/partial R-squared diagnostics, the complete cluster-robust
    coefficient table, and the strongest off-diagonal correlations in the
    cluster-robust coefficient covariance matrix.

    These quantities describe model fit and estimator geometry. They do not
    decompose causal effects and Shapley shares must not be interpreted as
    causal importance.
    """
    x = data.copy()
    x["ATTENDANCE_BINARY_GROUP"] = np.where(
        x["VISITS_CMAT_PERIOD"].gt(0), "1+", "0"
    )
    required = [
        outcome_col,
        "ATTENDANCE_BINARY_GROUP",
        "CLASSROOM_ID",
        "CLAVECARRERA",
        cluster_col,
    ]
    d = x.dropna(subset=required).copy()
    d["ATTENDANCE_BINARY_GROUP"] = pd.Categorical(
        d["ATTENDANCE_BINARY_GROUP"].astype(str),
        categories=["0", "1+"],
        ordered=True,
    )

    block_terms = {
        "attendance": "C(ATTENDANCE_BINARY_GROUP, Treatment(reference='0'))",
        "degree": "C(CLAVECARRERA)",
        "instructor_period": "C(CLASSROOM_ID)",
    }
    block_order = list(block_terms)

    def fit_blocks(included: tuple[str, ...]):
        rhs = " + ".join(block_terms[name] for name in included) if included else "1"
        formula = f"{outcome_col} ~ {rhs}"
        model = smf.ols(formula, data=d).fit(
            cov_type="cluster",
            cov_kwds={"groups": d[cluster_col]},
        )
        return model, formula

    # Fit every subset once. With three blocks this is only 2^3 = 8 models.
    subset_models: dict[frozenset[str], object] = {}
    subset_formulas: dict[frozenset[str], str] = {}
    subset_rows: list[dict[str, object]] = []
    for size in range(len(block_order) + 1):
        for subset_tuple in combinations(block_order, size):
            key = frozenset(subset_tuple)
            model, formula = fit_blocks(tuple(subset_tuple))
            subset_models[key] = model
            subset_formulas[key] = formula
            subset_rows.append(
                {
                    "outcome": outcome_label,
                    "included_blocks": (
                        "intercept_only" if not subset_tuple else " + ".join(subset_tuple)
                    ),
                    "n_blocks": int(size),
                    "r_squared": float(model.rsquared),
                    "adjusted_r_squared": float(model.rsquared_adj),
                    "sse": float(np.dot(model.resid, model.resid)),
                    "df_model": float(model.df_model),
                    "df_resid": float(model.df_resid),
                    "N": int(model.nobs),
                    "formula": formula,
                }
            )
    subset_table = pd.DataFrame(subset_rows)

    # Sequential path requested for interpretation: attendance -> degree -> classroom.
    attendance_term = f"{block_terms['attendance']}[T.1+]"
    path_rows: list[dict[str, object]] = []
    previous_r2 = float(subset_models[frozenset()].rsquared)
    previous_adj_r2 = float(subset_models[frozenset()].rsquared_adj)
    for step in range(1, len(block_order) + 1):
        included = tuple(block_order[:step])
        model = subset_models[frozenset(included)]
        ci = model.conf_int()
        path_rows.append(
            {
                "outcome": outcome_label,
                "step": step,
                "model": " + ".join(included),
                "added_block": included[-1],
                "r_squared": float(model.rsquared),
                "adjusted_r_squared": float(model.rsquared_adj),
                "delta_r_squared_from_previous": float(model.rsquared - previous_r2),
                "delta_adjusted_r_squared_from_previous": float(
                    model.rsquared_adj - previous_adj_r2
                ),
                "attendance_beta": (
                    float(model.params[attendance_term])
                    if attendance_term in model.params.index
                    else np.nan
                ),
                "attendance_cluster_robust_se": (
                    float(model.bse[attendance_term])
                    if attendance_term in model.params.index
                    else np.nan
                ),
                "attendance_ci95_low": (
                    float(ci.loc[attendance_term, 0])
                    if attendance_term in ci.index
                    else np.nan
                ),
                "attendance_ci95_high": (
                    float(ci.loc[attendance_term, 1])
                    if attendance_term in ci.index
                    else np.nan
                ),
                "attendance_p_value": (
                    float(model.pvalues[attendance_term])
                    if attendance_term in model.params.index
                    else np.nan
                ),
                "N": int(model.nobs),
                "n_clusters": int(d[cluster_col].nunique()),
            }
        )
        previous_r2 = float(model.rsquared)
        previous_adj_r2 = float(model.rsquared_adj)
    model_path = pd.DataFrame(path_rows)

    # Exact Shapley/LMG-style allocation of the full-model R^2 across blocks.
    m = len(block_order)
    full_key = frozenset(block_order)
    full_model = subset_models[full_key]
    full_r2 = float(full_model.rsquared)
    shapley_rows: list[dict[str, object]] = []
    for block in block_order:
        others = [name for name in block_order if name != block]
        contribution = 0.0
        for size in range(m):
            weight = factorial(size) * factorial(m - size - 1) / factorial(m)
            for subset_tuple in combinations(others, size):
                subset = frozenset(subset_tuple)
                with_block = subset | {block}
                contribution += weight * (
                    float(subset_models[with_block].rsquared)
                    - float(subset_models[subset].rsquared)
                )
        shapley_rows.append(
            {
                "outcome": outcome_label,
                "block": block,
                "shapley_r_squared": float(contribution),
                "share_of_full_r_squared": (
                    float(contribution / full_r2) if full_r2 > 0 else np.nan
                ),
                "full_model_r_squared": full_r2,
                "n_blocks": m,
                "n_orderings_averaged": factorial(m),
                "interpretation": (
                    "order-averaged allocation of OLS R-squared; descriptive, not causal"
                ),
            }
        )
    shapley = pd.DataFrame(shapley_rows)

    # Conditional contribution of each block when it is added last.
    full_sse = float(np.dot(full_model.resid, full_model.resid))
    partial_rows: list[dict[str, object]] = []
    for block in block_order:
        reduced_key = full_key - {block}
        reduced = subset_models[reduced_key]
        reduced_sse = float(np.dot(reduced.resid, reduced.resid))
        partial_rows.append(
            {
                "outcome": outcome_label,
                "block": block,
                "full_r_squared": full_r2,
                "r_squared_without_block": float(reduced.rsquared),
                "delta_r_squared_full_minus_without_block": float(
                    full_r2 - reduced.rsquared
                ),
                "partial_r_squared_conditional": (
                    float((reduced_sse - full_sse) / reduced_sse)
                    if reduced_sse > 0
                    else np.nan
                ),
                "interpretation": (
                    "incremental fit conditional on all other listed blocks"
                ),
            }
        )
    partial = pd.DataFrame(partial_rows)

    def classify_term(term: str) -> str:
        if term == "Intercept":
            return "intercept"
        if "ATTENDANCE_BINARY_GROUP" in term:
            return "attendance"
        if "C(CLAVECARRERA)" in term:
            return "degree"
        if "C(CLASSROOM_ID)" in term:
            return "instructor_period"
        return "other"

    ci = np.asarray(full_model.conf_int(), dtype=float)
    coefficients = pd.DataFrame(
        {
            "outcome": outcome_label,
            "term": full_model.params.index.astype(str),
            "estimate": np.asarray(full_model.params, dtype=float),
            "cluster_robust_se": np.asarray(full_model.bse, dtype=float),
            "statistic": np.asarray(full_model.tvalues, dtype=float),
            "p_value": np.asarray(full_model.pvalues, dtype=float),
            "ci95_low": ci[:, 0],
            "ci95_high": ci[:, 1],
        }
    )
    coefficients.insert(
        2,
        "block",
        coefficients["term"].map(classify_term),
    )
    coefficients["scale"] = (
        "probability (0-1)" if outcome_col == "PASS" else "standardized outcome (SD)"
    )
    if outcome_col == "PASS":
        coefficients["estimate_percentage_points"] = 100.0 * coefficients["estimate"]
        coefficients["ci95_low_percentage_points"] = 100.0 * coefficients["ci95_low"]
        coefficients["ci95_high_percentage_points"] = 100.0 * coefficients["ci95_high"]

    # The covariance matrix is chiefly useful through contrasts. For notebook
    # audit, retain the strongest estimator correlations rather than printing
    # the entire p x p matrix.
    covariance = np.asarray(full_model.cov_params(), dtype=float)
    standard_errors = np.sqrt(np.clip(np.diag(covariance), 0.0, None))
    denom = np.outer(standard_errors, standard_errors)
    corr = np.divide(
        covariance,
        denom,
        out=np.full_like(covariance, np.nan, dtype=float),
        where=denom > 0,
    )
    terms = list(full_model.params.index.astype(str))
    covariance_rows: list[dict[str, object]] = []
    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            if not np.isfinite(corr[i, j]):
                continue
            covariance_rows.append(
                {
                    "outcome": outcome_label,
                    "term_1": terms[i],
                    "block_1": classify_term(terms[i]),
                    "term_2": terms[j],
                    "block_2": classify_term(terms[j]),
                    "cluster_robust_covariance": float(covariance[i, j]),
                    "estimator_correlation": float(corr[i, j]),
                    "abs_estimator_correlation": float(abs(corr[i, j])),
                }
            )
    covariance_top = (
        pd.DataFrame(covariance_rows)
        .sort_values("abs_estimator_correlation", ascending=False)
        .head(50)
        .reset_index(drop=True)
    )

    return {
        "model_path": model_path,
        "subset_r2": subset_table,
        "shapley_r2": shapley,
        "partial_r2": partial,
        "coefficients": coefficients,
        "covariance_top": covariance_top,
    }


def _composition(
    data: pd.DataFrame,
    *,
    group_col: str,
    group_order: list[str],
    state_col: str,
    state_order: list[str],
    specification: str,
) -> pd.DataFrame:
    out = outcome_state_composition(
        data,
        group_col=group_col,
        group_order=group_order,
        state_col=state_col,
        state_order=state_order,
    ).rename(columns={"state": "outcome_state"})
    out["outcome_state"] = out["outcome_state"].replace(
        {"numeric_nonpass": "numeric_grade_below_7.5"}
    )
    out.insert(0, "specification", specification)
    return out


def _observed_numeric_histogram(
    data: pd.DataFrame,
    *,
    group_col: str,
    group_order: list[str],
    outcome_col: str = "GRADE_NUMERIC",
) -> pd.DataFrame:
    """Tabulate observed numeric grades in 101 bins centred on 0.0--10.0.

    Each 0.1-point bin is normalised by the size of the full attendance
    group, not by the number of numeric grades. Therefore the sum of
    share_of_full_group across the 101 bins equals the observed numeric
    share of that attendance group; BV, RT and BA occupy the remaining mass.
    """
    centers = np.round(np.arange(0.0, 10.0 + 0.1, 0.1), 1)
    edges = np.linspace(-0.05, 10.05, len(centers) + 1)
    labels = data[group_col].astype("string")
    rows: list[dict[str, object]] = []

    for group in group_order:
        subset = data.loc[labels.eq(group)].copy()
        group_n = int(len(subset))
        numeric = pd.to_numeric(subset[outcome_col], errors="coerce").dropna()
        numeric_values = numeric.to_numpy(float)

        if np.any((numeric_values < 0.0) | (numeric_values > 10.0)):
            bad = numeric_values[(numeric_values < 0.0) | (numeric_values > 10.0)]
            raise ValueError(
                f"Observed numeric MU grades outside 0--10 in group {group}: "
                + ", ".join(f"{value:g}" for value in bad[:10])
            )

        counts, _ = np.histogram(numeric_values, bins=edges)
        numeric_n = int(counts.sum())

        for center, count in zip(centers, counts):
            share = count / group_n if group_n else np.nan
            rows.append(
                {
                    "group": group,
                    "bin_center": float(center),
                    "bin_left": float(center - 0.05),
                    "bin_right": float(center + 0.05),
                    "count": int(count),
                    "group_n": group_n,
                    "numeric_n": numeric_n,
                    "share_of_full_group": share,
                    "percent_of_full_group": 100.0 * share if group_n else np.nan,
                    "numeric_state": (
                        "numeric_nonpass" if center < 7.5 else "pass"
                    ),
                }
            )

    return pd.DataFrame(rows)


def _continuous_state_histogram(
    data: pd.DataFrame,
    *,
    group_col: str,
    group_order: list[str],
    outcome_col: str,
    state_col: str,
    state_order: list[str],
    bin_min: float = -2.0,
    bin_max: float = 2.0,
    bin_width: float = 0.1,
) -> pd.DataFrame:
    """Tabulate a continuous outcome by state on a fixed display window.

    Bin heights are expressed as density contributions relative to the full
    attendance-group size, so stacked bars are directly comparable with the
    stacked KDE components. Values outside the display window are retained
    in group/component counts but do not contribute to plotted bins.
    """
    if bin_width <= 0 or bin_max <= bin_min:
        raise ValueError("Invalid histogram range or bin width")

    edges = np.arange(bin_min, bin_max + bin_width * 0.5, bin_width)
    if edges[-1] < bin_max:
        edges = np.append(edges, bin_max)
    centers = (edges[:-1] + edges[1:]) / 2.0

    labels = data[group_col].astype("string")
    states = data[state_col].astype("string")
    outcome = pd.to_numeric(data[outcome_col], errors="coerce")
    rows: list[dict[str, object]] = []

    for group in group_order:
        group_mask = labels.eq(group) & outcome.notna()
        group_n = int(group_mask.sum())
        for state in state_order:
            state_mask = group_mask & states.eq(state)
            values = outcome.loc[state_mask].to_numpy(float)
            counts, _ = np.histogram(values, bins=edges)
            component_n = int(len(values))

            for center, left, right, count in zip(
                centers, edges[:-1], edges[1:], counts
            ):
                share = count / group_n if group_n else np.nan
                density = (
                    share / float(right - left)
                    if group_n and right > left
                    else np.nan
                )
                rows.append(
                    {
                        "group": group,
                        "component": state,
                        "bin_center": float(center),
                        "bin_left": float(left),
                        "bin_right": float(right),
                        "count": int(count),
                        "group_n": group_n,
                        "component_n": component_n,
                        "share_of_full_group_bin": share,
                        "density_of_full_group": density,
                    }
                )

    return pd.DataFrame(rows)

def _profile(
    data: pd.DataFrame,
    *,
    group_col: str,
    group_order: list[str],
    outcome_col: str,
    outcome_label: str,
    specification: str,
) -> pd.DataFrame:
    out = distribution_profile(
        data,
        group_col=group_col,
        group_order=group_order,
        outcome_col=outcome_col,
        pass_col="PASS",
    )
    out = out.rename(
        columns={
            "q10": "z_q10",
            "q25": "z_q25",
            "q50": "z_median",
            "q75": "z_q75",
            "q90": "z_q90",
            "mean_outcome_among_pass": "mean_z_among_pass",
            "mean_outcome_among_nonpass": "mean_z_among_nonpass",
        }
    )
    out.insert(0, "outcome", outcome_label)
    out.insert(0, "specification", specification)
    out["interpretation"] = (
        "descriptive distribution profile; conditional means are not causal subgroup effects"
    )
    return out


def _matrix(
    pairwise: pd.DataFrame,
    *,
    group_order: list[str],
    outcome: str,
) -> pd.DataFrame:
    out = pairwise_effect_matrix(
        pairwise,
        group_order=group_order,
        estimate_col="adjusted_difference_group1_minus_group2",
    )
    out.insert(0, "outcome", outcome)
    return out


def _pairwise_pvalue_matrix(
    pairwise: pd.DataFrame,
    *,
    group_order: list[str],
    p_col: str,
    outcome: str,
    adjustment: str,
) -> pd.DataFrame:
    """Convert long pairwise p-values to a symmetric matrix.

    The diagonal is set to 1 because each group is identical to itself.
    Raw and Holm-adjusted matrices are exported separately so the distinction
    between exploratory pairwise evidence and multiplicity-aware inference is
    explicit in downstream figures.
    """
    required = {"group1", "group2", p_col}
    missing = required.difference(pairwise.columns)
    if missing:
        raise KeyError(f"Missing pairwise p-value columns: {sorted(missing)}")

    order = [str(group) for group in group_order]
    matrix = pd.DataFrame(np.nan, index=order, columns=order, dtype=float)
    for group in order:
        matrix.loc[group, group] = 1.0

    for _, row in pairwise.iterrows():
        group1 = str(row["group1"])
        group2 = str(row["group2"])
        if group1 not in order or group2 not in order:
            continue
        value = float(row[p_col])
        matrix.loc[group1, group2] = value
        matrix.loc[group2, group1] = value

    out = matrix.reset_index(names="group")
    out.insert(0, "adjustment", adjustment)
    out.insert(0, "outcome", outcome)
    return out


def _odds_ratio_matrix(
    pairwise: pd.DataFrame,
    *,
    group_order: list[str],
    outcome: str,
) -> pd.DataFrame:
    """Convert long pairwise odds ratios to a reciprocal matrix."""
    required = {"group1", "group2", "odds_ratio_group1_vs_group2"}
    missing = required.difference(pairwise.columns)
    if missing:
        raise KeyError(f"Missing odds-ratio columns: {sorted(missing)}")

    order = [str(group) for group in group_order]
    matrix = pd.DataFrame(np.nan, index=order, columns=order, dtype=float)
    for group in order:
        matrix.loc[group, group] = 1.0

    for _, row in pairwise.iterrows():
        group1 = str(row["group1"])
        group2 = str(row["group2"])
        if group1 not in order or group2 not in order:
            continue
        value = float(row["odds_ratio_group1_vs_group2"])
        matrix.loc[group1, group2] = value
        matrix.loc[group2, group1] = 1.0 / value if value > 0 else np.nan

    out = matrix.reset_index(names="group")
    out.insert(0, "outcome", outcome)
    return out


def _nonpass_management_summary(data: pd.DataFrame) -> pd.DataFrame:
    x = data.loc[data["PASS"].eq(0)].copy()
    x["attendance"] = np.where(x["VISITS_CMAT_PERIOD"].gt(0), "1+", "0")
    token = x["GRADE_TOKEN"].fillna("").astype(str).str.upper()
    rows = []
    for attendance in ["0", "1+"]:
        group = x.loc[x["attendance"].eq(attendance)]
        group_token = token.loc[group.index]
        numeric_n = int(group["GRADE_CLASS"].eq("numeric").sum())
        bv_n = int(group_token.eq("BV").sum())
        rt_n = int(group_token.eq("RT").sum())
        ba_n = int(group_token.eq("BA").sum())
        admin_n = bv_n + rt_n + ba_n
        n = int(len(group))
        rows.append(
            {
                "attendance": attendance,
                "nonpass_n": n,
                "numeric_below_7_5_n": numeric_n,
                "BV_n": bv_n,
                "RT_n": rt_n,
                "BA_n": ba_n,
                "administrative_n": admin_n,
                "administrative_share_among_nonpass": admin_n / n if n else np.nan,
                "BV_RT_share_among_numeric_or_BV_RT": (
                    (bv_n + rt_n) / (numeric_n + bv_n + rt_n)
                    if numeric_n + bv_n + rt_n
                    else np.nan
                ),
                "BV_share_among_numeric_or_BV": (
                    bv_n / (numeric_n + bv_n) if numeric_n + bv_n else np.nan
                ),
                "RT_share_among_numeric_or_RT": (
                    rt_n / (numeric_n + rt_n) if numeric_n + rt_n else np.nan
                ),
            }
        )
    return pd.DataFrame(rows)


def check_environment() -> int:
    required = [
        REPO_ROOT / "paper" / "docs" / "analysis" / "VISIT_GROUPING_DECISION.md",
        GROUP_SPEC,
        REPO_ROOT / "cmat_analysis" / "pyproject.toml",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.exists()]
    if missing:
        raise SystemExit("Missing Paper 2.1 outcome-analysis paths: " + ", ".join(missing))
    spec = json.loads(GROUP_SPEC.read_text(encoding="utf-8"))
    if spec["positive_user_primary_groups"] != ["1", "2", "3", "4", "5", "6+"]:
        raise SystemExit("Paper 2.1 primary visit grouping differs from frozen decision.")
    print("Paper 2.1 dual-outcome analysis check: OK")
    print("Reusable estimators: cmat_analysis 0.3 attendance-frequency API")
    print("Frozen primary groups: 1, 2, 3, 4, 5, 6+")
    return 0


def run(args: argparse.Namespace) -> int:
    base = get_study_config(REPO_ROOT)
    config = replace(
        base,
        materias_path=(args.materias or base.materias_path).expanduser().resolve(),
        asesorias_path=(args.asesorias or base.asesorias_path).expanduser().resolve(),
    )
    data = load_and_clean_inputs(config)
    mu = add_primary_outcomes(build_study_cohorts(data, config)["mu_primary"], config)
    mu["PASS"] = mu["PASS"].astype(float)
    mu = add_academic_outcome_states(mu)

    benchmark = pd.DataFrame(
        [
            _benchmark(mu, "Z_GRADE_PRIMARY", "continuous_standardised_grade"),
            _benchmark(mu, "PASS", "pass_probability"),
        ]
    )
    _save(benchmark, "10_benchmark_0_vs_1plus.csv")

    benchmark_diagnostics = [
        benchmark_model_diagnostics(
            mu, "Z_GRADE_PRIMARY", "continuous_standardised_grade"
        ),
        benchmark_model_diagnostics(mu, "PASS", "pass_probability"),
    ]
    for key, filename in [
        ("model_path", "10e_benchmark_model_fit_path.csv"),
        ("subset_r2", "10f_benchmark_r2_all_subsets.csv"),
        ("shapley_r2", "10g_benchmark_r2_shapley.csv"),
        ("partial_r2", "10h_benchmark_partial_r2.csv"),
        ("coefficients", "10i_benchmark_full_coefficients.csv"),
        ("covariance_top", "10j_benchmark_covariance_top_correlations.csv"),
    ]:
        _save(
            pd.concat([bundle[key] for bundle in benchmark_diagnostics], ignore_index=True),
            filename,
        )

    zero_order = ["0", "1", "2", "3", "4", "5", "6+"]
    zero_plus = add_topcoded_visit_group(
        mu,
        top_exact=5,
        include_zero=True,
        output_col="P21_GROUP_WITH_ZERO",
    )
    zero_desc = group_outcome_summary(
        zero_plus,
        group_col="P21_GROUP_WITH_ZERO",
        group_order=zero_order,
        outcome_col="Z_GRADE_PRIMARY",
        pass_col="PASS",
    )
    _save(
        _format_descriptives(
            zero_desc, specification="zero_inclusive_primary_0_1_2_3_4_5_6plus"
        ),
        "10b_zero_inclusive_descriptives.csv",
    )
    _save(
        _composition(
            zero_plus,
            group_col="P21_GROUP_WITH_ZERO",
            group_order=zero_order,
            state_col="ACADEMIC_OUTCOME_STATE_4",
            state_order=["pass", "numeric_nonpass", "BV_RT", "BA"],
            specification="zero_inclusive_primary_0_1_2_3_4_5_6plus",
        ),
        "10c_zero_inclusive_outcome_state_composition.csv",
    )
    _save(
        _composition(
            zero_plus,
            group_col="P21_GROUP_WITH_ZERO",
            group_order=zero_order,
            state_col="ACADEMIC_OUTCOME_STATE_5",
            state_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
            specification="zero_inclusive_primary_0_1_2_3_4_5_6plus",
        ),
        "10d_zero_inclusive_exact_administrative_composition.csv",
    )

    observed_numeric_density = mixture_component_density(
        zero_plus,
        group_col="P21_GROUP_WITH_ZERO",
        group_order=zero_order,
        outcome_col="GRADE_NUMERIC",
        component_col="ACADEMIC_OUTCOME_STATE_5",
        component_order=["numeric_nonpass", "pass"],
        grid_size=400,
        cut=0.0,
    )
    _save(
        observed_numeric_density,
        "10l_zero_inclusive_observed_numeric_grade_density.csv",
    )

    _save(
        _observed_numeric_histogram(
            zero_plus,
            group_col="P21_GROUP_WITH_ZERO",
            group_order=zero_order,
            outcome_col="GRADE_NUMERIC",
        ),
        "10m_zero_inclusive_observed_numeric_grade_histogram.csv",
    )

    ridge_density = mixture_component_density(
        zero_plus,
        group_col="P21_GROUP_WITH_ZERO",
        group_order=zero_order,
        outcome_col="Z_GRADE_PRIMARY",
        component_col="ACADEMIC_OUTCOME_STATE_5",
        component_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
        grid_size=400,
    )
    _save(ridge_density, "10g_zero_inclusive_stacked_ridgeline_density.csv")

    # Descriptive display sensitivity resolving exact six visits from the 7+ tail.
    # The pre-specified primary grouping remains 1/2/3/4/5/6+ for inference,
    # while Figures 1a and 1 use this higher-resolution zero-inclusive display.
    zero_7plus_order = ["0", "1", "2", "3", "4", "5", "6", "7+"]
    zero_7plus = add_topcoded_visit_group(
        mu,
        top_exact=6,
        include_zero=True,
        output_col="P21_GROUP_WITH_ZERO_7P",
    )
    zero_7plus_desc = group_outcome_summary(
        zero_7plus,
        group_col="P21_GROUP_WITH_ZERO_7P",
        group_order=zero_7plus_order,
        outcome_col="Z_GRADE_PRIMARY",
        pass_col="PASS",
    )
    _save(
        _format_descriptives(
            zero_7plus_desc,
            specification="zero_inclusive_display_0_1_2_3_4_5_6_7plus",
        ),
        "10n_zero_inclusive_7plus_descriptives.csv",
    )
    _save(
        _composition(
            zero_7plus,
            group_col="P21_GROUP_WITH_ZERO_7P",
            group_order=zero_7plus_order,
            state_col="ACADEMIC_OUTCOME_STATE_5",
            state_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
            specification="zero_inclusive_display_0_1_2_3_4_5_6_7plus",
        ),
        "10o_zero_inclusive_7plus_exact_administrative_composition.csv",
    )
    _save(
        mixture_component_density(
            zero_7plus,
            group_col="P21_GROUP_WITH_ZERO_7P",
            group_order=zero_7plus_order,
            outcome_col="Z_GRADE_PRIMARY",
            component_col="ACADEMIC_OUTCOME_STATE_5",
            component_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
            grid_size=400,
        ),
        "10p_zero_inclusive_7plus_stacked_ridgeline_density.csv",
    )
    _save(
        _observed_numeric_histogram(
            zero_7plus,
            group_col="P21_GROUP_WITH_ZERO_7P",
            group_order=zero_7plus_order,
            outcome_col="GRADE_NUMERIC",
        ),
        "10q_zero_inclusive_7plus_observed_numeric_grade_histogram.csv",
    )

    short_bandwidth_scale = 0.55
    short_density = mixture_component_density(
        zero_7plus,
        group_col="P21_GROUP_WITH_ZERO_7P",
        group_order=zero_7plus_order,
        outcome_col="Z_GRADE_PRIMARY",
        component_col="ACADEMIC_OUTCOME_STATE_5",
        component_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
        grid_size=800,
        cut=0.0,
        bandwidth_scale=short_bandwidth_scale,
    )
    short_density.insert(0, "bandwidth_scale", short_bandwidth_scale)
    _save(
        short_density,
        "10r_zero_inclusive_7plus_imputed_z_short_kde_density.csv",
    )
    _save(
        _continuous_state_histogram(
            zero_7plus,
            group_col="P21_GROUP_WITH_ZERO_7P",
            group_order=zero_7plus_order,
            outcome_col="Z_GRADE_PRIMARY",
            state_col="ACADEMIC_OUTCOME_STATE_5",
            state_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
            bin_min=-2.0,
            bin_max=2.0,
            bin_width=0.1,
        ),
        "10s_zero_inclusive_7plus_imputed_z_histogram.csv",
    )

    zero_z_pair, _ = _fit(
        zero_plus,
        group_col="P21_GROUP_WITH_ZERO",
        group_order=zero_order,
        outcome_col="Z_GRADE_PRIMARY",
        outcome_label="continuous_standardised_grade",
        specification="zero_inclusive_primary_0_1_2_3_4_5_6plus",
    )
    zero_p_pair, _ = _fit(
        zero_plus,
        group_col="P21_GROUP_WITH_ZERO",
        group_order=zero_order,
        outcome_col="PASS",
        outcome_label="pass_probability",
        specification="zero_inclusive_primary_0_1_2_3_4_5_6plus",
    )
    _save(zero_z_pair, "10h_zero_inclusive_pairwise_continuous.csv")
    _save(zero_p_pair, "10i_zero_inclusive_pairwise_pass.csv")
    _save(
        _matrix(
            zero_z_pair,
            group_order=zero_order,
            outcome="continuous_standardised_grade",
        ),
        "10j_zero_inclusive_z_heatmap_matrix.csv",
    )
    _save(
        _matrix(
            zero_p_pair,
            group_order=zero_order,
            outcome="pass_probability",
        ),
        "10k_zero_inclusive_pass_heatmap_matrix.csv",
    )

    nonpass = mu.loc[mu["PASS"].eq(0)].copy()
    management_benchmark = pd.DataFrame(
        [
            _benchmark(
                nonpass,
                "ADMINISTRATIVE_VS_NUMERIC_NONPASS",
                "administrative_outcome_vs_numeric_failure_among_nonpass",
            ),
            _benchmark(
                nonpass,
                "BVRT_VS_NUMERIC_NONPASS",
                "BV_RT_vs_numeric_failure_among_nonpass_excluding_BA",
            ),
            _benchmark(
                nonpass,
                "BV_VS_NUMERIC_NONPASS",
                "BV_vs_numeric_failure_among_nonpass_excluding_RT_BA",
            ),
            _benchmark(
                nonpass,
                "RT_VS_NUMERIC_NONPASS",
                "RT_vs_numeric_failure_among_nonpass_excluding_BV_BA",
            ),
        ]
    )
    _save(management_benchmark, "10e_nonpass_management_benchmark_0_vs_1plus.csv")
    _save(_nonpass_management_summary(mu), "10f_nonpass_management_descriptives_0_vs_1plus.csv")

    users = mu.loc[mu["VISITS_CMAT_PERIOD"].gt(0)].copy()
    primary_order = ["1", "2", "3", "4", "5", "6+"]
    users = add_topcoded_visit_group(
        users, top_exact=5, output_col="P21_GROUP"
    )
    primary_desc = group_outcome_summary(
        users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="Z_GRADE_PRIMARY",
        pass_col="PASS",
    )
    _save(
        _format_descriptives(primary_desc, specification="primary_1_2_3_4_5_6plus"),
        "11_primary_group_descriptives.csv",
    )

    z_pair, z_omni = _fit(
        users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="Z_GRADE_PRIMARY",
        outcome_label="continuous_standardised_grade",
        specification="primary_1_2_3_4_5_6plus",
    )
    p_pair, p_omni = _fit(
        users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="PASS",
        outcome_label="pass_probability",
        specification="primary_1_2_3_4_5_6plus",
    )
    _save(pd.concat([z_omni, p_omni], ignore_index=True), "12_primary_omnibus.csv")
    _save(z_pair, "13_primary_pairwise_continuous.csv")
    _save(p_pair, "14_primary_pairwise_pass.csv")

    _save(
        _composition(
            users,
            group_col="P21_GROUP",
            group_order=primary_order,
            state_col="ACADEMIC_OUTCOME_STATE_4",
            state_order=["pass", "numeric_nonpass", "BV_RT", "BA"],
            specification="primary_1_2_3_4_5_6plus",
        ),
        "15_primary_outcome_state_composition.csv",
    )
    _save(
        _composition(
            users,
            group_col="P21_GROUP",
            group_order=primary_order,
            state_col="ACADEMIC_OUTCOME_STATE_5",
            state_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
            specification="primary_1_2_3_4_5_6plus",
        ),
        "15a_primary_exact_administrative_composition.csv",
    )
    _save(
        _profile(
            users,
            group_col="P21_GROUP",
            group_order=primary_order,
            outcome_col="Z_GRADE_PRIMARY",
            outcome_label="continuous_standardised_grade",
            specification="primary_1_2_3_4_5_6plus",
        ),
        "15b_primary_distribution_profile.csv",
    )
    _save(
        _profile(
            users,
            group_col="P21_GROUP",
            group_order=primary_order,
            outcome_col="Z_GRADE_COMPLETE_CASE",
            outcome_label="numeric_complete_case_standardised_grade",
            specification="primary_1_2_3_4_5_6plus_complete_case",
        ),
        "15c_primary_complete_case_distribution_profile.csv",
    )

    nonpass_users = users.loc[users["PASS"].eq(0)].copy()
    admin_pair, admin_omni = _fit(
        nonpass_users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="ADMINISTRATIVE_VS_NUMERIC_NONPASS",
        outcome_label="administrative_outcome_vs_numeric_failure_among_nonpass",
        specification="primary_1_2_3_4_5_6plus_nonpass",
    )
    bvrt_pair, bvrt_omni = _fit(
        nonpass_users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="BVRT_VS_NUMERIC_NONPASS",
        outcome_label="BV_RT_vs_numeric_failure_among_nonpass_excluding_BA",
        specification="primary_1_2_3_4_5_6plus_nonpass",
    )
    bv_pair, bv_omni = _fit(
        nonpass_users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="BV_VS_NUMERIC_NONPASS",
        outcome_label="BV_vs_numeric_failure_among_nonpass_excluding_RT_BA",
        specification="primary_1_2_3_4_5_6plus_nonpass",
    )
    _save(
        pd.concat([admin_omni, bvrt_omni, bv_omni], ignore_index=True),
        "15d_nonpass_management_omnibus.csv",
    )
    _save(admin_pair, "15e_nonpass_administrative_pairwise.csv")
    _save(bvrt_pair, "15f_nonpass_BVRT_pairwise.csv")
    _save(bv_pair, "15g_nonpass_BV_pairwise.csv")

    cc_pair, cc_omni = _fit(
        users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="Z_GRADE_COMPLETE_CASE",
        outcome_label="numeric_complete_case_standardised_grade",
        specification="primary_1_2_3_4_5_6plus",
    )
    _save(cc_pair, "16_complete_case_pairwise_continuous.csv")
    _save(cc_omni, "17_complete_case_omnibus.csv")
    _save(
        _matrix(z_pair, group_order=primary_order, outcome="continuous_standardised_grade"),
        "18_primary_z_heatmap_matrix.csv",
    )
    _save(
        _matrix(p_pair, group_order=primary_order, outcome="pass_probability"),
        "19_primary_pass_heatmap_matrix.csv",
    )

    sensitivity_order = ["1", "2", "3", "4", "5", "6", "7+"]
    sensitivity = add_topcoded_visit_group(
        users.drop(columns=["P21_GROUP"]),
        top_exact=6,
        output_col="P21_GROUP_7P",
    )
    sensitivity_desc = group_outcome_summary(
        sensitivity,
        group_col="P21_GROUP_7P",
        group_order=sensitivity_order,
        outcome_col="Z_GRADE_PRIMARY",
        pass_col="PASS",
    )
    _save(
        _format_descriptives(
            sensitivity_desc, specification="sensitivity_1_to_6_7plus"
        ),
        "20_sensitivity_7plus_group_descriptives.csv",
    )
    sz_pair, sz_omni = _fit(
        sensitivity,
        group_col="P21_GROUP_7P",
        group_order=sensitivity_order,
        outcome_col="Z_GRADE_PRIMARY",
        outcome_label="continuous_standardised_grade",
        specification="sensitivity_1_to_6_7plus",
    )
    sp_pair, sp_omni = _fit(
        sensitivity,
        group_col="P21_GROUP_7P",
        group_order=sensitivity_order,
        outcome_col="PASS",
        outcome_label="pass_probability",
        specification="sensitivity_1_to_6_7plus",
    )
    _save(pd.concat([sz_omni, sp_omni], ignore_index=True), "21_sensitivity_7plus_omnibus.csv")
    _save(sz_pair, "22_sensitivity_7plus_pairwise_continuous.csv")
    _save(sp_pair, "23_sensitivity_7plus_pairwise_pass.csv")
    _save(
        _pairwise_pvalue_matrix(
            sz_pair,
            group_order=sensitivity_order,
            p_col="p_raw",
            outcome="continuous_standardised_grade",
            adjustment="raw",
        ),
        "22a_sensitivity_7plus_p_raw_continuous_matrix.csv",
    )
    _save(
        _pairwise_pvalue_matrix(
            sz_pair,
            group_order=sensitivity_order,
            p_col="p_holm",
            outcome="continuous_standardised_grade",
            adjustment="holm",
        ),
        "22b_sensitivity_7plus_p_holm_continuous_matrix.csv",
    )
    _save(
        _pairwise_pvalue_matrix(
            sp_pair,
            group_order=sensitivity_order,
            p_col="p_raw",
            outcome="pass_probability",
            adjustment="raw",
        ),
        "23a_sensitivity_7plus_p_raw_pass_matrix.csv",
    )
    _save(
        _pairwise_pvalue_matrix(
            sp_pair,
            group_order=sensitivity_order,
            p_col="p_holm",
            outcome="pass_probability",
            adjustment="holm",
        ),
        "23b_sensitivity_7plus_p_holm_pass_matrix.csv",
    )

    _save(
        _composition(
            sensitivity,
            group_col="P21_GROUP_7P",
            group_order=sensitivity_order,
            state_col="ACADEMIC_OUTCOME_STATE_4",
            state_order=["pass", "numeric_nonpass", "BV_RT", "BA"],
            specification="sensitivity_1_to_6_7plus",
        ),
        "24_sensitivity_7plus_outcome_state_composition.csv",
    )
    _save(
        _composition(
            sensitivity,
            group_col="P21_GROUP_7P",
            group_order=sensitivity_order,
            state_col="ACADEMIC_OUTCOME_STATE_5",
            state_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
            specification="sensitivity_1_to_6_7plus",
        ),
        "24a_sensitivity_7plus_exact_administrative_composition.csv",
    )
    _save(
        _observed_numeric_histogram(
            sensitivity,
            group_col="P21_GROUP_7P",
            group_order=sensitivity_order,
            outcome_col="GRADE_NUMERIC",
        ),
        "25a_sensitivity_7plus_observed_numeric_grade_histogram.csv",
    )
    _save(
        _profile(
            sensitivity,
            group_col="P21_GROUP_7P",
            group_order=sensitivity_order,
            outcome_col="Z_GRADE_PRIMARY",
            outcome_label="continuous_standardised_grade",
            specification="sensitivity_1_to_6_7plus",
        ),
        "25_sensitivity_7plus_distribution_profile.csv",
    )

    # Main-paper zero-inclusive pairwise family: 0, exact 1--6, and 7+.
    # Continuous performance retains the adjusted fixed-effect difference scale.
    # PASS is represented with a fixed-effect logistic model so the pairwise
    # dashboard can report odds ratios rather than percentage-point differences.
    paper_order = ["0", "1", "2", "3", "4", "5", "6", "7+"]
    full_z_pair, full_z_omni = _fit(
        zero_7plus,
        group_col="P21_GROUP_WITH_ZERO_7P",
        group_order=paper_order,
        outcome_col="Z_GRADE_PRIMARY",
        outcome_label="continuous_standardised_grade",
        specification="main_zero_inclusive_0_1_2_3_4_5_6_7plus",
    )
    _save(full_z_pair, "26a_zero_inclusive_7plus_pairwise_continuous.csv")
    _save(
        _matrix(
            full_z_pair,
            group_order=paper_order,
            outcome="continuous_standardised_grade",
        ),
        "26b_zero_inclusive_7plus_z_effect_matrix.csv",
    )
    _save(
        _pairwise_pvalue_matrix(
            full_z_pair,
            group_order=paper_order,
            p_col="p_raw",
            outcome="continuous_standardised_grade",
            adjustment="raw",
        ),
        "26e_zero_inclusive_7plus_z_p_raw_matrix.csv",
    )
    _save(
        _pairwise_pvalue_matrix(
            full_z_pair,
            group_order=paper_order,
            p_col="p_holm",
            outcome="continuous_standardised_grade",
            adjustment="holm",
        ),
        "26f_zero_inclusive_7plus_z_p_holm_matrix.csv",
    )

    # Use the stable fixed-effect linear-probability specification for
    # multiplicity-aware PASS inference. The logistic model is retained only
    # for interpretable odds-ratio point estimates because its cluster-robust
    # covariance can be rank-deficient when classroom fixed effects and
    # classroom clustering coincide.
    full_pass_pair, full_pass_omni = _fit(
        zero_7plus,
        group_col="P21_GROUP_WITH_ZERO_7P",
        group_order=paper_order,
        outcome_col="PASS",
        outcome_label="pass_probability",
        specification="main_zero_inclusive_0_1_2_3_4_5_6_7plus",
    )
    _save(full_pass_pair, "26k_zero_inclusive_7plus_pairwise_pass_lpm.csv")
    _save(full_pass_omni, "26l_zero_inclusive_7plus_pass_lpm_omnibus.csv")

    pass_logit_pair, pass_logit_omni, pass_logit_info = (
        fixed_effect_logistic_group_comparisons(
            zero_7plus,
            group_col="P21_GROUP_WITH_ZERO_7P",
            group_order=paper_order,
            outcome_col="PASS",
            fixed_effect_col="CLASSROOM_ID",
            cluster_col="CLASSROOM_ID",
            categorical_covariates=["CLAVECARRERA"],
            multiplicity_method="holm",
        )
    )
    pass_logit_pair.insert(
        0, "specification", "main_zero_inclusive_0_1_2_3_4_5_6_7plus"
    )
    pass_logit_omni.insert(
        0, "specification", "main_zero_inclusive_0_1_2_3_4_5_6_7plus"
    )
    pass_logit_info.insert(
        0, "specification", "main_zero_inclusive_0_1_2_3_4_5_6_7plus"
    )
    _save(pass_logit_pair, "26c_zero_inclusive_7plus_pass_logit_pairwise.csv")
    _save(
        _odds_ratio_matrix(
            pass_logit_pair,
            group_order=paper_order,
            outcome="pass_odds_ratio",
        ),
        "26d_zero_inclusive_7plus_pass_odds_ratio_matrix.csv",
    )
    _save(
        _pairwise_pvalue_matrix(
            full_pass_pair,
            group_order=paper_order,
            p_col="p_raw",
            outcome="pass_probability_linear_probability_model",
            adjustment="raw",
        ),
        "26g_zero_inclusive_7plus_pass_p_raw_matrix.csv",
    )
    _save(
        _pairwise_pvalue_matrix(
            full_pass_pair,
            group_order=paper_order,
            p_col="p_holm",
            outcome="pass_probability_linear_probability_model",
            adjustment="holm",
        ),
        "26h_zero_inclusive_7plus_pass_p_holm_matrix.csv",
    )
    full_z_omni.insert(0, "family", "continuous_standardised_grade")
    full_pass_omni.insert(0, "family", "pass_probability")
    _save(
        pd.concat([full_z_omni, full_pass_omni], ignore_index=True, sort=False),
        "26i_zero_inclusive_7plus_omnibus.csv",
    )
    _save(pass_logit_info, "26j_zero_inclusive_7plus_pass_logit_model_info.csv")

    z_prof_pair, z_prof_omni = _fit(
        users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="Z_GRADE_PRIMARY",
        outcome_label="continuous_standardised_grade",
        specification="primary_instructor_cluster_sensitivity",
        cluster_col="CLAVEPROFESOR",
    )
    p_prof_pair, p_prof_omni = _fit(
        users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="PASS",
        outcome_label="pass_probability",
        specification="primary_instructor_cluster_sensitivity",
        cluster_col="CLAVEPROFESOR",
    )
    _save(z_prof_pair, "26_instructor_cluster_pairwise_continuous.csv")
    _save(p_prof_pair, "27_instructor_cluster_pairwise_pass.csv")
    _save(
        pd.concat([z_prof_omni, p_prof_omni], ignore_index=True),
        "28_instructor_cluster_omnibus.csv",
    )
    _save(
        pd.DataFrame(
            [
                _benchmark(
                    mu,
                    "Z_GRADE_PRIMARY",
                    "continuous_standardised_grade",
                    cluster_col="CLAVEPROFESOR",
                ),
                _benchmark(
                    mu,
                    "PASS",
                    "pass_probability",
                    cluster_col="CLAVEPROFESOR",
                ),
            ]
        ),
        "29_instructor_cluster_benchmark_0_vs_1plus.csv",
    )

    print(f"Paper 2.1 study cohort: N={len(mu):,}")
    print(f"Positive-attendance analysis: N={len(users):,}")
    print("Main manuscript reporting groups: 0, 1, 2, 3, 4, 5, 6, 7+")
    print("Historical pooled-tail robustness groups: 1, 2, 3, 4, 5, 6+")
    print("Shared methods: cmat_analysis 0.3 public API")
    print(f"Outputs: {TABLES_DIR}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Paper 2.1 dual-outcome frequency analysis."
    )
    parser.add_argument("--materias", type=Path)
    parser.add_argument("--asesorias", type=Path)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return check_environment() if args.check else run(args)


if __name__ == "__main__":
    raise SystemExit(main())
