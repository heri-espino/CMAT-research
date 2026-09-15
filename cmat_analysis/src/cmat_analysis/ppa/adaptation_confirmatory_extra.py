"""Additional confirmatory models for Paper 4 longitudinal adaptation.

This module keeps high-dimensional degree-programme interactions separate from the
lower-dimensional primary models and adds a numeric-failure severity analysis. All
estimands are observational associations.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from .adaptation_confirmatory import _collapse_rare, _joint_wald, _standardize, classify_experience_state


def career_heterogeneity_reduced_interactions(
    mu_students: pd.DataFrame,
    *,
    min_career_ns: tuple[int, ...] = (100, 150, 200),
) -> pd.DataFrame:
    """Test degree-programme by experience-state heterogeneity with controlled dimension.

    Parameters
    ----------
    mu_students : pandas.DataFrame
        Student-level first-MU table containing CMAT use, first-MU experience measures,
        degree programme, period and classroom identifier.
    min_career_ns : tuple of int, default=(100, 150, 200)
        Minimum programme sizes retained separately in successive interaction models;
        smaller programmes are pooled into ``OTHER``. Reporting several pre-specified
        thresholds guards against conclusions driven by a single dimensionality choice.

    Returns
    -------
    pandas.DataFrame
        Cluster-robust joint interaction tests and incremental R-squared measures for
        each pooling threshold.
    """
    required = {
        "MU_FIRST_CMAT_VISITS",
        "MU_FIRST_Z",
        "MU_FIRST_LOO_PASS_RATE",
        "MU_FIRST_CAREER",
        "MU_FIRST_PERIOD_LABEL",
        "MU_FIRST_CLASSROOM_ID",
    }
    missing = required.difference(mu_students.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")

    d = mu_students.copy()
    d["_STATE"] = classify_experience_state(d)
    d = d.loc[d["_STATE"].ne("unknown_context")].copy()
    d["_ANY_CMAT"] = (d["MU_FIRST_CMAT_VISITS"] > 0).astype(int)
    rows: list[dict[str, object]] = []
    for min_n in min_career_ns:
        work = d.copy()
        work["_CAREER_INT"] = _collapse_rare(work["MU_FIRST_CAREER"], int(min_n))
        work = work.dropna(subset=["MU_FIRST_CLASSROOM_ID", "_CAREER_INT"]).copy()
        base = smf.ols(
            "_ANY_CMAT ~ C(_STATE) + C(_CAREER_INT) + C(MU_FIRST_PERIOD_LABEL)",
            data=work,
        ).fit(cov_type="cluster", cov_kwds={"groups": work["MU_FIRST_CLASSROOM_ID"]})
        full = smf.ols(
            "_ANY_CMAT ~ C(_STATE) * C(_CAREER_INT) + C(MU_FIRST_PERIOD_LABEL)",
            data=work,
        ).fit(cov_type="cluster", cov_kwds={"groups": work["MU_FIRST_CLASSROOM_ID"]})
        stat, df_num, p_value = _joint_wald(full, contains=":C(_CAREER_INT)")
        delta = float(full.rsquared - base.rsquared)
        partial = delta / (1.0 - float(base.rsquared)) if base.rsquared < 1 else np.nan
        clusters = int(work["MU_FIRST_CLASSROOM_ID"].nunique())
        rows.append({
            "min_career_n": int(min_n),
            "n": int(full.nobs),
            "clusters": clusters,
            "career_levels": int(work["_CAREER_INT"].nunique()),
            "interaction_df": int(df_num),
            "interaction_df_per_cluster": float(df_num / clusters) if clusters else np.nan,
            "r2_base": float(base.rsquared),
            "r2_full": float(full.rsquared),
            "delta_r2": delta,
            "partial_r2": partial,
            "wald_stat": stat,
            "p_value": p_value,
        })
    return pd.DataFrame(rows)


def post_failure_numeric_severity_models(
    transitions: pd.DataFrame,
    *,
    min_career_n: int = 30,
) -> pd.DataFrame:
    """Relate numeric failure severity to subsequent adaptation responses.

    Parameters
    ----------
    transitions : pandas.DataFrame
        Covered post-failure MU transitions. ``PREV_Z`` must be available for the
        numeric-failure subset; professor-context movement additionally requires the
        previous historical instructor rank and a comparable next rank.
    min_career_n : int, default=30
        Minimum transition count before a degree programme is retained separately.

    Returns
    -------
    pandas.DataFrame
        Cluster-robust linear-probability coefficients for standardized prior relative
        performance in models of movement toward a historically higher-outcome professor,
        next-period CMAT use and increased CMAT use. More negative prior Z indicates a
        more severe classroom-relative numeric failure.
    """
    required = {
        "STUDENT_ID",
        "FAILED_ATTEMPT_NUMBER",
        "PREV_PERIOD_INDEX",
        "CAREER",
        "PREV_Z",
        "PREV_ANY_CMAT",
        "NEXT_ANY_CMAT",
        "PREV_CMAT_VISITS",
        "NEXT_CMAT_VISITS",
        "PREV_PROF_EASINESS_PERCENTILE",
        "DELTA_PROF_EASINESS_PERCENTILE",
    }
    missing = required.difference(transitions.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")

    d = transitions.copy()
    d["_PREV_Z"] = _standardize(d["PREV_Z"])
    d["_CAREER"] = _collapse_rare(d["CAREER"], min_career_n)
    d["_ATTEMPT_BAND"] = np.select(
        [d["FAILED_ATTEMPT_NUMBER"].eq(1), d["FAILED_ATTEMPT_NUMBER"].eq(2)],
        ["1", "2"],
        default="3+",
    )
    d["_INCREASED_CMAT"] = d["NEXT_CMAT_VISITS"].gt(d["PREV_CMAT_VISITS"]).astype(int)
    d["_PREV_RANK_10PP"] = pd.to_numeric(d["PREV_PROF_EASINESS_PERCENTILE"], errors="coerce") * 10

    specs = [
        (
            "higher_outcome_percentile",
            "_MOVE_HIGHER",
            "_PREV_Z + _PREV_RANK_10PP + PREV_ANY_CMAT + C(_ATTEMPT_BAND) + C(PREV_PERIOD_INDEX) + C(_CAREER)",
            True,
        ),
        (
            "next_cmat_use",
            "NEXT_ANY_CMAT",
            "_PREV_Z + PREV_ANY_CMAT + C(_ATTEMPT_BAND) + C(PREV_PERIOD_INDEX) + C(_CAREER)",
            False,
        ),
        (
            "increased_cmat",
            "_INCREASED_CMAT",
            "_PREV_Z + PREV_ANY_CMAT + C(_ATTEMPT_BAND) + C(PREV_PERIOD_INDEX) + C(_CAREER)",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for model_name, outcome, rhs, requires_rank in specs:
        model_data = d.dropna(subset=["_PREV_Z"]).copy()
        if requires_rank:
            delta = pd.to_numeric(model_data["DELTA_PROF_EASINESS_PERCENTILE"], errors="coerce")
            model_data = model_data.loc[delta.notna() & model_data["_PREV_RANK_10PP"].notna()].copy()
            model_data[outcome] = pd.to_numeric(
                model_data["DELTA_PROF_EASINESS_PERCENTILE"], errors="coerce"
            ).gt(0).astype(int)
        if len(model_data) < 20 or model_data[outcome].nunique() < 2:
            continue
        fit = smf.ols(f"{outcome} ~ {rhs}", data=model_data).fit(
            cov_type="cluster", cov_kwds={"groups": model_data["STUDENT_ID"]}
        )
        for term in ("_PREV_Z", "PREV_ANY_CMAT", "_PREV_RANK_10PP"):
            if term not in fit.params.index:
                continue
            rows.append({
                "model": model_name,
                "term": term,
                "n": int(fit.nobs),
                "student_clusters": int(model_data["STUDENT_ID"].nunique()),
                "estimate": float(fit.params[term]),
                "se_cluster": float(fit.bse[term]),
                "p_value": float(fit.pvalues[term]),
                "r2": float(fit.rsquared),
            })
    return pd.DataFrame(rows)
