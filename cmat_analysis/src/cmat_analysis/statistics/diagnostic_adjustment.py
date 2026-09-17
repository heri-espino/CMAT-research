"""Observed baseline-diagnostic adjustment for exact CMAT visit groups.

These helpers are designed for sensitivity analyses in observational CMAT
studies. They align one same-student/same-term diagnostic score to a focal
course attempt and compare exact visit-group associations on the same
complete-case sample before and after adjustment for the observed diagnostic.
They do not identify a causal tutoring effect and they do not resolve
unmeasured confounding.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from .methodology import EXACT_GROUP_ORDER, add_exact_visit_group


def attach_same_term_diagnostic(
    df: pd.DataFrame,
    diagnostics: pd.DataFrame,
    *,
    student_col: str = "STUDENT_ID",
    year_col: str = "YEAR",
    session_col: str = "SESSION",
    diagnostic_student_col: str = "student_id",
    diagnostic_year_col: str = "year",
    diagnostic_session_col: str = "period",
    diagnostic_score_col: str = "percentage",
    diagnostic_type_col: str = "exam_type",
    diagnostic_type: str | None = "DMU",
) -> pd.DataFrame:
    """Attach an unambiguous same-student/same-term diagnostic score.

    Diagnostic rows are matched on student, academic year, and session/period.
    If multiple non-missing diagnostic values exist for the same key and those
    values disagree, the score is treated as ambiguous and is left missing
    rather than resolved arbitrarily.
    """
    required_left = {student_col, year_col, session_col}
    required_right = {
        diagnostic_student_col,
        diagnostic_year_col,
        diagnostic_session_col,
        diagnostic_score_col,
    }
    missing_left = sorted(required_left.difference(df.columns))
    missing_right = sorted(required_right.difference(diagnostics.columns))
    if missing_left:
        raise KeyError(f"Missing focal-cohort columns: {missing_left}")
    if missing_right:
        raise KeyError(f"Missing diagnostic columns: {missing_right}")

    left = df.copy()
    right = diagnostics.copy()
    if diagnostic_type is not None and diagnostic_type_col in right.columns:
        right = right.loc[
            right[diagnostic_type_col].astype(str).str.strip().eq(str(diagnostic_type))
        ].copy()

    left["_DIAG_STUDENT_KEY"] = left[student_col].astype(str)
    left["_DIAG_YEAR_KEY"] = pd.to_numeric(left[year_col], errors="coerce").astype("Int64")
    left["_DIAG_SESSION_KEY"] = left[session_col].astype(str).str.strip()

    right["_DIAG_STUDENT_KEY"] = right[diagnostic_student_col].astype(str)
    right["_DIAG_YEAR_KEY"] = pd.to_numeric(
        right[diagnostic_year_col], errors="coerce"
    ).astype("Int64")
    right["_DIAG_SESSION_KEY"] = right[diagnostic_session_col].astype(str).str.strip()
    right["_DIAG_SCORE"] = pd.to_numeric(right[diagnostic_score_col], errors="coerce")

    keys = ["_DIAG_STUDENT_KEY", "_DIAG_YEAR_KEY", "_DIAG_SESSION_KEY"]

    def _summarize(group: pd.DataFrame) -> pd.Series:
        scores = group["_DIAG_SCORE"].dropna()
        unique = scores.drop_duplicates()
        return pd.Series(
            {
                "DIAGNOSTIC_ROWS": int(len(group)),
                "DIAGNOSTIC_NONMISSING_SCORES": int(len(scores)),
                "DIAGNOSTIC_DISTINCT_SCORES": int(len(unique)),
                "DIAGNOSTIC_PERCENTAGE": (
                    float(unique.iloc[0]) if len(unique) == 1 else np.nan
                ),
            }
        )

    summary = right.groupby(keys, dropna=False, observed=True).apply(
        _summarize, include_groups=False
    ).reset_index()

    out = left.merge(summary, on=keys, how="left", validate="many_to_one")
    out["DIAGNOSTIC_MATCHED"] = out["DIAGNOSTIC_PERCENTAGE"].notna()
    return out.drop(columns=keys)


def diagnostic_adjusted_exact_visit_models(
    df: pd.DataFrame,
    *,
    visits_col: str = "VISITS_CMAT_PERIOD",
    outcome_col: str = "Z_GRADE_PRIMARY",
    diagnostic_col: str = "DIAGNOSTIC_PERCENTAGE",
    classroom_col: str = "CLASSROOM_ID",
    career_col: str = "CLAVECARRERA",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compare exact visit-group associations before/after diagnostic adjustment."""
    required = {visits_col, outcome_col, diagnostic_col, classroom_col, career_col}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise KeyError(f"Missing analytical columns: {missing}")

    grouped = add_exact_visit_group(df, visits_col)
    grouped[diagnostic_col] = pd.to_numeric(grouped[diagnostic_col], errors="coerce")

    coverage_rows: list[dict[str, object]] = []
    for group in EXACT_GROUP_ORDER:
        g = grouped.loc[grouped["EXACT_VISIT_GROUP_0_1_2_3_4P"] == group].copy()
        observed = g[diagnostic_col].notna()
        coverage_rows.append(
            {
                "group": group,
                "n_total": int(len(g)),
                "n_diagnostic": int(observed.sum()),
                "diagnostic_coverage": float(observed.mean()) if len(g) else np.nan,
                "mean_diagnostic_percentage": (
                    float(g.loc[observed, diagnostic_col].mean()) if observed.any() else np.nan
                ),
            }
        )
    coverage = pd.DataFrame(coverage_rows)

    d = grouped.dropna(
        subset=[outcome_col, diagnostic_col, classroom_col, career_col, "EXACT_VISIT_GROUP_0_1_2_3_4P"]
    ).copy()
    if d.empty:
        return coverage, pd.DataFrame()

    diag_sd = float(d[diagnostic_col].std(ddof=0))
    if not np.isfinite(diag_sd) or diag_sd <= 0:
        raise ValueError("Diagnostic score has zero or undefined variance in complete cases.")
    d["DIAGNOSTIC_Z"] = (d[diagnostic_col] - float(d[diagnostic_col].mean())) / diag_sd

    group_term = "C(EXACT_VISIT_GROUP_0_1_2_3_4P, Treatment(reference='0'))"
    base_formula = f"{outcome_col} ~ {group_term} + C({classroom_col}) + C({career_col})"
    models = {
        "same_sample_without_diagnostic": smf.ols(base_formula, data=d).fit(
            cov_type="cluster", cov_kwds={"groups": d[classroom_col]}
        ),
        "plus_diagnostic": smf.ols(base_formula + " + DIAGNOSTIC_Z", data=d).fit(
            cov_type="cluster", cov_kwds={"groups": d[classroom_col]}
        ),
    }

    rows: list[dict[str, object]] = []
    for model_name, model in models.items():
        for group in EXACT_GROUP_ORDER[1:]:
            parameter = f"{group_term}[T.{group}]"
            if parameter not in model.params.index:
                continue
            ci = model.conf_int().loc[parameter]
            rows.append(
                {
                    "model": model_name,
                    "group": group,
                    "reference_group": "0",
                    "estimate_z": float(model.params[parameter]),
                    "cluster_robust_se": float(model.bse[parameter]),
                    "ci95_low": float(ci.iloc[0]),
                    "ci95_high": float(ci.iloc[1]),
                    "p_value": float(model.pvalues[parameter]),
                    "n": int(model.nobs),
                    "n_classrooms": int(d[classroom_col].nunique()),
                    "n_careers": int(d[career_col].nunique()),
                    "diagnostic_mean": float(d[diagnostic_col].mean()),
                    "diagnostic_sd": diag_sd,
                }
            )
    return coverage, pd.DataFrame(rows)
