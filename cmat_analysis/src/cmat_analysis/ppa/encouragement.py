"""Instructor-linked uptake and prior-familiarization analyses for PPA studies.

The functions in this module quantify observational variation in formal CMAT
help-seeking associated with instructors and with prior service exposure. They
do not treat instructor identity, historical instructor uptake, or the PPA
threshold as randomized assignment or causal instruments.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf


DEFAULT_VISIT_GROUP_ORDER = ("0", "1-2", "3", "4+")


def _collapse_rare_categories(series: pd.Series, min_n: int) -> pd.Series:
    s = series.fillna("MISSING").astype(str)
    counts = s.value_counts()
    keep = set(counts[counts >= min_n].index)
    return s.where(s.isin(keep), "OTHER")


def professor_visit_group_distribution(
    df: pd.DataFrame,
    *,
    professor_col: str,
    group_col: str,
    min_professor_n: int = 30,
    group_order: Sequence[str] = DEFAULT_VISIT_GROUP_ORDER,
) -> pd.DataFrame:
    """Summarize 0/1-2/3/4+ service-use composition by instructor.

    Parameters
    ----------
    df : pandas.DataFrame
        Student-level analytical data.
    professor_col : str
        Column identifying the instructor attached to each student observation.
    group_col : str
        Column containing mutually exclusive visit-count groups.
    min_professor_n : int, default=30
        Minimum number of student observations required for an instructor to be
        retained in the returned summary.
    group_order : sequence of str, default=("0", "1-2", "3", "4+")
        Ordered visit-group labels to summarize.

    Returns
    -------
    pandas.DataFrame
        One row per retained instructor with total sample size, group counts and
        group shares. Instructor identifiers are retained for controlled
        analysis; publication outputs should aggregate or pseudonymize further.
    """
    required = {professor_col, group_col}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    groups = tuple(str(g) for g in group_order)
    d = df[[professor_col, group_col]].dropna().copy()
    d[group_col] = d[group_col].astype(str)
    d = d.loc[d[group_col].isin(groups)].copy()

    totals = d.groupby(professor_col).size().rename("n").to_frame()
    counts = (
        d.groupby([professor_col, group_col], observed=False)
        .size()
        .unstack(fill_value=0)
        .reindex(columns=groups, fill_value=0)
    )
    out = totals.join(counts, how="left").reset_index()
    out = out.loc[out["n"] >= int(min_professor_n)].copy()
    for group in groups:
        safe = group.replace("+", "plus").replace("-", "_")
        out[f"count_{safe}"] = out.pop(group).astype(int)
        out[f"share_{safe}"] = out[f"count_{safe}"] / out["n"]
    return out.sort_values(["n", professor_col], ascending=[False, True], kind="stable").reset_index(drop=True)


def leave_period_out_professor_propensity(
    df: pd.DataFrame,
    *,
    professor_col: str,
    period_col: str,
    outcome_col: str,
    min_other_n: int = 30,
    prefix: str = "PROF",
) -> pd.DataFrame:
    """Attach an instructor uptake rate estimated from other academic periods.

    For every instructor-period cell, the propensity uses observations for the
    same instructor from all *other* periods. This prevents the focal student's
    own period from contributing to the predictor and is therefore preferable
    to a contemporaneous instructor mean for descriptive encouragement analyses.

    Parameters
    ----------
    df : pandas.DataFrame
        Student-level analytical data with one binary uptake outcome per row.
    professor_col : str
        Instructor identifier.
    period_col : str
        Academic-period identifier.
    outcome_col : str
        Binary outcome whose instructor propensity is to be estimated.
    min_other_n : int, default=30
        Minimum number of observations from other periods required to define
        the instructor propensity.
    prefix : str, default="PROF"
        Prefix used for generated column names.

    Returns
    -------
    pandas.DataFrame
        Copy of ``df`` with leave-period-out instructor rate, supporting sample
        size, and a student-weighted z-standardized rate.
    """
    required = {professor_col, period_col, outcome_col}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")

    out = df.copy()
    work = out[[professor_col, period_col, outcome_col]].dropna().copy()
    values = pd.to_numeric(work[outcome_col], errors="coerce")
    if values.isna().any() or not set(values.unique()).issubset({0, 1}):
        raise ValueError(f"{outcome_col} must contain only binary 0/1 values on non-missing rows.")
    work[outcome_col] = values.astype(float)

    prof = (
        work.groupby(professor_col, dropna=False)[outcome_col]
        .agg(["sum", "count"])
        .rename(columns={"sum": "_prof_sum", "count": "_prof_n"})
        .reset_index()
    )
    cell = (
        work.groupby([professor_col, period_col], dropna=False)[outcome_col]
        .agg(["sum", "count"])
        .rename(columns={"sum": "_cell_sum", "count": "_cell_n"})
        .reset_index()
    )
    cell = cell.merge(prof, on=professor_col, how="left")
    cell["_other_sum"] = cell["_prof_sum"] - cell["_cell_sum"]
    cell["_other_n"] = cell["_prof_n"] - cell["_cell_n"]
    rate_col = f"{prefix}_LEAVE_PERIOD_OUT_RATE"
    n_col = f"{prefix}_LEAVE_PERIOD_OUT_N"
    z_col = f"{prefix}_LEAVE_PERIOD_OUT_Z"
    cell[n_col] = cell["_other_n"].astype(int)
    cell[rate_col] = np.where(
        cell["_other_n"] >= int(min_other_n),
        cell["_other_sum"] / cell["_other_n"],
        np.nan,
    )
    attach = cell[[professor_col, period_col, rate_col, n_col]]
    out = out.merge(attach, on=[professor_col, period_col], how="left")

    eligible = out[rate_col].dropna()
    sd = float(eligible.std(ddof=0)) if len(eligible) else np.nan
    mean = float(eligible.mean()) if len(eligible) else np.nan
    if np.isfinite(sd) and sd > 0:
        out[z_col] = (out[rate_col] - mean) / sd
    else:
        out[z_col] = np.nan
    return out


def professor_uptake_increment(
    df: pd.DataFrame,
    *,
    outcome_col: str,
    professor_col: str,
    period_col: str,
    career_col: str | None = None,
    min_career_n: int = 30,
) -> pd.DataFrame:
    """Quantify added descriptive fit from instructor fixed effects.

    Parameters
    ----------
    df : pandas.DataFrame
        Student-level analytical data with a binary uptake outcome.
    outcome_col : str
        Binary 0/1 service-use outcome.
    professor_col : str
        Instructor identifier.
    period_col : str
        Academic-period identifier included in both nested models.
    career_col : str or None, optional
        Optional degree-programme variable included in both nested models.
    min_career_n : int, default=30
        Minimum sample size for a programme to retain its own fixed-effect
        category; smaller categories are pooled as ``OTHER``.

    Returns
    -------
    pandas.DataFrame
        One-row nested linear-probability-model comparison containing base and
        instructor-augmented R-squared, partial R-squared, and the classical
        nested-model F test. The result is descriptive, not causal.
    """
    required = {outcome_col, professor_col, period_col}
    if career_col is not None:
        required.add(career_col)
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    d = df[list(required)].dropna(subset=[outcome_col, professor_col, period_col]).copy()
    d[outcome_col] = pd.to_numeric(d[outcome_col], errors="coerce")
    d = d.dropna(subset=[outcome_col]).copy()
    if not set(d[outcome_col].unique()).issubset({0, 1}):
        raise ValueError(f"{outcome_col} must be binary 0/1.")

    rhs = [f"C({period_col})"]
    if career_col is not None:
        model_career = "_MODEL_CAREER"
        d[model_career] = _collapse_rare_categories(d[career_col], min_career_n)
        rhs.append(f"C({model_career})")
    base_formula = f"{outcome_col} ~ " + " + ".join(rhs)
    full_formula = base_formula + f" + C({professor_col})"
    base = smf.ols(base_formula, data=d).fit()
    full = smf.ols(full_formula, data=d).fit()

    df_num = int(round(base.df_resid - full.df_resid))
    ss_gain = float(np.sum(base.resid**2) - np.sum(full.resid**2))
    mse_full = float(np.sum(full.resid**2) / full.df_resid)
    f_stat = float((ss_gain / df_num) / mse_full) if df_num > 0 and mse_full > 0 else np.nan
    p_value = float(stats.f.sf(f_stat, df_num, full.df_resid)) if np.isfinite(f_stat) else np.nan
    partial_r2 = (
        float((base.ssr - full.ssr) / base.ssr)
        if float(base.ssr) > 0
        else np.nan
    )
    return pd.DataFrame([{
        "outcome": outcome_col,
        "n": int(full.nobs),
        "professors": int(d[professor_col].nunique()),
        "periods": int(d[period_col].nunique()),
        "r2_base": float(base.rsquared),
        "r2_plus_professor": float(full.rsquared),
        "delta_r2_professor": float(full.rsquared - base.rsquared),
        "partial_r2_professor": partial_r2,
        "joint_f_professor": f_stat,
        "joint_df_num": df_num,
        "joint_df_den": float(full.df_resid),
        "joint_p_professor": p_value,
        "note": "descriptive nested linear-probability models; instructor identity is not randomized",
    }])


def professor_visit_group_multinomial_increment(
    df: pd.DataFrame,
    *,
    group_col: str,
    professor_col: str,
    period_col: str,
    career_col: str | None = None,
    min_career_n: int = 30,
    group_order: Sequence[str] = DEFAULT_VISIT_GROUP_ORDER,
) -> pd.DataFrame:
    """Test whether instructor identity adds fit for 0/1-2/3/4+ uptake groups.

    Parameters
    ----------
    df : pandas.DataFrame
        Student-level analytical data.
    group_col : str
        Mutually exclusive service-use group.
    professor_col : str
        Instructor identifier.
    period_col : str
        Academic-period identifier.
    career_col : str or None, optional
        Optional degree-programme control.
    min_career_n : int, default=30
        Minimum programme sample size before pooling smaller programmes.
    group_order : sequence of str, default=("0", "1-2", "3", "4+")
        Visit-group order used to encode the multinomial outcome.

    Returns
    -------
    pandas.DataFrame
        One-row likelihood-ratio comparison between period/career controls and
        the same model plus instructor fixed effects, including McFadden
        pseudo-R-squared values.
    """
    required = {group_col, professor_col, period_col}
    if career_col is not None:
        required.add(career_col)
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    groups = tuple(str(g) for g in group_order)
    d = df[list(required)].dropna(subset=[group_col, professor_col, period_col]).copy()
    d[group_col] = d[group_col].astype(str)
    d = d.loc[d[group_col].isin(groups)].copy()
    d["_GROUP_CODE"] = d[group_col].map({g: i for i, g in enumerate(groups)}).astype(int)
    rhs = [f"C({period_col})"]
    if career_col is not None:
        d["_MODEL_CAREER"] = _collapse_rare_categories(d[career_col], min_career_n)
        rhs.append("C(_MODEL_CAREER)")
    base_formula = "_GROUP_CODE ~ " + " + ".join(rhs)
    full_formula = base_formula + f" + C({professor_col})"
    base = smf.mnlogit(base_formula, data=d).fit(method="newton", maxiter=200, disp=False)
    full = smf.mnlogit(full_formula, data=d).fit(method="newton", maxiter=200, disp=False)
    lr = float(2 * (full.llf - base.llf))
    df_diff = int(round(full.df_model - base.df_model))
    p_value = float(stats.chi2.sf(lr, df_diff))
    ll_null = float(full.llnull)
    base_pr2 = float(1 - base.llf / ll_null)
    full_pr2 = float(1 - full.llf / ll_null)
    return pd.DataFrame([{
        "outcome": group_col,
        "n": int(full.nobs),
        "groups": "|".join(groups),
        "professors": int(d[professor_col].nunique()),
        "periods": int(d[period_col].nunique()),
        "mcfadden_r2_base": base_pr2,
        "mcfadden_r2_plus_professor": full_pr2,
        "delta_mcfadden_r2_professor": float(full_pr2 - base_pr2),
        "lr_stat_professor": lr,
        "lr_df": df_diff,
        "lr_p_professor": p_value,
        "base_converged": bool(base.mle_retvals.get("converged", True)),
        "full_converged": bool(full.mle_retvals.get("converged", True)),
        "note": "descriptive multinomial association; group 3 is retained as an institutionally salient category",
    }])


def familiarization_professor_persistence_models(
    df: pd.DataFrame,
    *,
    outcome_col: str = "CALC_ANY_VISIT",
    prior_group_col: str = "MU_VISIT_GROUP",
    prior_performance_col: str = "Z_MU",
    professor_col: str = "CALC_PROFESSOR",
    period_col: str = "CALC_PERIOD_LABEL",
    career_col: str = "CALC_CAREER_OFFICIAL",
    min_career_n: int = 30,
) -> pd.DataFrame:
    """Estimate prior-familiarization contrasts before and after instructor effects.

    The models use later Calculus-period CMAT use as the outcome and preserve the
    four prior MU exposure groups ``0 / 1-2 / 3 / 4+``. The final specification
    adds Calculus instructor fixed effects so that prior-familiarization
    contrasts are identified among students exposed to the same instructor,
    period controls, and observed covariates.

    Parameters
    ----------
    df : pandas.DataFrame
        Paired MU-to-Calculus progression cohort.
    outcome_col : str, default="CALC_ANY_VISIT"
        Later binary CMAT-use outcome.
    prior_group_col : str, default="MU_VISIT_GROUP"
        Prior MU visit group.
    prior_performance_col : str, default="Z_MU"
        Pretreatment classroom-relative MU performance.
    professor_col : str, default="CALC_PROFESSOR"
        Instructor in the later Calculus course.
    period_col : str, default="CALC_PERIOD_LABEL"
        Later academic-period label.
    career_col : str, default="CALC_CAREER_OFFICIAL"
        Later official degree programme.
    min_career_n : int, default=30
        Minimum programme size before smaller programmes are pooled.

    Returns
    -------
    pandas.DataFrame
        Focal linear-probability coefficients for prior MU visit groups across
        nested models, with standard errors clustered by Calculus instructor.
    """
    required = {
        outcome_col, prior_group_col, prior_performance_col, professor_col,
        period_col, career_col,
    }
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    d = df[list(required)].dropna(
        subset=[outcome_col, prior_group_col, prior_performance_col, professor_col, period_col]
    ).copy()
    d[outcome_col] = pd.to_numeric(d[outcome_col], errors="coerce")
    d = d.dropna(subset=[outcome_col]).copy()
    if not set(d[outcome_col].unique()).issubset({0, 1}):
        raise ValueError(f"{outcome_col} must be binary 0/1.")
    d["_MODEL_CAREER"] = _collapse_rare_categories(d[career_col], min_career_n)

    group_term = f"C({prior_group_col}, Treatment(reference='0'))"
    formulas = [
        ("familiarization_only", f"{outcome_col} ~ {group_term}"),
        (
            "adjusted_prior_performance_career_period",
            f"{outcome_col} ~ {group_term} + {prior_performance_col} + C(_MODEL_CAREER) + C({period_col})",
        ),
        (
            "plus_calc_professor_fixed_effects",
            f"{outcome_col} ~ {group_term} + {prior_performance_col} + C(_MODEL_CAREER) + C({period_col}) + C({professor_col})",
        ),
    ]
    rows: list[dict[str, object]] = []
    for model_name, formula in formulas:
        fit = smf.ols(formula, data=d).fit(
            cov_type="cluster", cov_kwds={"groups": d[professor_col]}
        )
        focal_terms = [
            term for term in fit.params.index
            if term.startswith(f"C({prior_group_col}, Treatment(reference='0'))")
        ]
        if focal_terms:
            restriction = np.zeros((len(focal_terms), len(fit.params)))
            for i, term in enumerate(focal_terms):
                restriction[i, fit.params.index.get_loc(term)] = 1.0
            joint = fit.wald_test(restriction, scalar=True)
            joint_stat = float(np.asarray(joint.statistic))
            joint_p = float(joint.pvalue)
        else:
            joint_stat = np.nan
            joint_p = np.nan
        for term in focal_terms:
            ci = fit.conf_int().loc[term]
            rows.append({
                "model": model_name,
                "term": term,
                "risk_difference": float(fit.params[term]),
                "cluster_se": float(fit.bse[term]),
                "p_value": float(fit.pvalues[term]),
                "ci95_low": float(ci.iloc[0]),
                "ci95_high": float(ci.iloc[1]),
                "n": int(fit.nobs),
                "professors": int(d[professor_col].nunique()),
                "r2": float(fit.rsquared),
                "joint_mu_group_stat": joint_stat,
                "joint_mu_group_p": joint_p,
                "covariance": f"cluster-robust by {professor_col}",
                "note": "risk-difference association; prior familiarity is observational, not randomized",
            })
    return pd.DataFrame(rows)


def professor_familiarization_interaction_model(
    df: pd.DataFrame,
    *,
    outcome_col: str = "CALC_ANY_VISIT",
    prior_group_col: str = "MU_VISIT_GROUP",
    prior_performance_col: str = "Z_MU",
    professor_col: str = "CALC_PROFESSOR",
    period_col: str = "CALC_PERIOD_LABEL",
    career_col: str = "CALC_CAREER_OFFICIAL",
    min_career_n: int = 30,
    min_other_n: int = 30,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Model joint associations of prior familiarity and instructor-linked uptake.

    Instructor-linked uptake is represented by the instructor's CMAT-use rate
    in *other* academic periods, standardized across the included student sample.
    The interaction therefore asks whether the association between current
    instructor-linked uptake and Calculus CMAT use differs across prior MU
    familiarity groups.

    Parameters
    ----------
    df : pandas.DataFrame
        Paired MU-to-Calculus progression cohort.
    outcome_col : str, default="CALC_ANY_VISIT"
        Later binary CMAT-use outcome.
    prior_group_col : str, default="MU_VISIT_GROUP"
        Prior MU visit group with 0 as the substantive reference.
    prior_performance_col : str, default="Z_MU"
        Pretreatment MU relative performance.
    professor_col : str, default="CALC_PROFESSOR"
        Later-course instructor identifier.
    period_col : str, default="CALC_PERIOD_LABEL"
        Later academic-period identifier.
    career_col : str, default="CALC_CAREER_OFFICIAL"
        Later official degree programme.
    min_career_n : int, default=30
        Minimum programme size before pooling smaller programmes.
    min_other_n : int, default=30
        Minimum number of other-period students needed to define an instructor
        propensity.

    Returns
    -------
    tuple of pandas.DataFrame
        ``(coefficients, group_specific_professor_slopes, diagnostics)``. The
        first table contains focal model terms, the second gives the estimated
        risk-difference slope for a one-standard-deviation instructor propensity
        increase within each prior-use group, and the third contains model and
        coverage diagnostics.
    """
    required = {
        outcome_col, prior_group_col, prior_performance_col, professor_col,
        period_col, career_col,
    }
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    base = df[list(required)].copy()
    augmented = leave_period_out_professor_propensity(
        base,
        professor_col=professor_col,
        period_col=period_col,
        outcome_col=outcome_col,
        min_other_n=min_other_n,
        prefix="_CALC_PROF",
    )
    rate_col = "_CALC_PROF_LEAVE_PERIOD_OUT_RATE"
    z_col = "_CALC_PROF_LEAVE_PERIOD_OUT_Z"
    n_col = "_CALC_PROF_LEAVE_PERIOD_OUT_N"
    d = augmented.dropna(
        subset=[outcome_col, prior_group_col, prior_performance_col, professor_col, period_col, z_col]
    ).copy()
    d[outcome_col] = pd.to_numeric(d[outcome_col], errors="coerce")
    d = d.dropna(subset=[outcome_col]).copy()
    d["_MODEL_CAREER"] = _collapse_rare_categories(d[career_col], min_career_n)

    group_term = f"C({prior_group_col}, Treatment(reference='0'))"
    formula = (
        f"{outcome_col} ~ {group_term} * {z_col} + {prior_performance_col} "
        f"+ C(_MODEL_CAREER) + C({period_col})"
    )
    fit = smf.ols(formula, data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d[professor_col]}
    )

    focal_terms = [
        term for term in fit.params.index
        if term == z_col
        or term.startswith(f"C({prior_group_col}, Treatment(reference='0'))")
    ]
    coefficients: list[dict[str, object]] = []
    for term in focal_terms:
        ci = fit.conf_int().loc[term]
        coefficients.append({
            "term": term,
            "risk_difference": float(fit.params[term]),
            "cluster_se": float(fit.bse[term]),
            "p_value": float(fit.pvalues[term]),
            "ci95_low": float(ci.iloc[0]),
            "ci95_high": float(ci.iloc[1]),
            "n": int(fit.nobs),
            "professors": int(d[professor_col].nunique()),
            "covariance": f"cluster-robust by {professor_col}",
        })

    groups = [str(g) for g in DEFAULT_VISIT_GROUP_ORDER if str(g) in set(d[prior_group_col].astype(str))]
    slope_rows: list[dict[str, object]] = []
    cov = fit.cov_params()
    params = fit.params
    base_idx = params.index.get_loc(z_col)
    for group in groups:
        weight = np.zeros(len(params))
        weight[base_idx] = 1.0
        interaction_term = None
        if group != "0":
            candidates = [
                term for term in params.index
                if z_col in term
                and ":" in term
                and f"[T.{group}]" in term
                and term.startswith(f"C({prior_group_col}, Treatment(reference='0'))")
            ]
            if len(candidates) == 1:
                interaction_term = candidates[0]
                weight[params.index.get_loc(interaction_term)] = 1.0
        estimate = float(weight @ params.to_numpy())
        variance = float(weight @ cov.to_numpy() @ weight)
        se = float(np.sqrt(max(variance, 0.0)))
        zcrit = stats.norm.ppf(0.975)
        p = float(2 * stats.norm.sf(abs(estimate / se))) if se > 0 else np.nan
        slope_rows.append({
            "mu_visit_group": group,
            "risk_difference_per_1sd_professor_propensity": estimate,
            "cluster_se": se,
            "p_value": p,
            "ci95_low": estimate - zcrit * se,
            "ci95_high": estimate + zcrit * se,
            "interaction_term": interaction_term or "",
        })

    interaction_terms = [
        term for term in params.index
        if ":" in term
        and z_col in term
        and term.startswith(f"C({prior_group_col}, Treatment(reference='0'))")
    ]
    if interaction_terms:
        restriction = np.zeros((len(interaction_terms), len(params)))
        for i, term in enumerate(interaction_terms):
            restriction[i, params.index.get_loc(term)] = 1.0
        joint_int = fit.wald_test(restriction, scalar=True)
        joint_int_stat = float(np.asarray(joint_int.statistic))
        joint_int_p = float(joint_int.pvalue)
    else:
        joint_int_stat = np.nan
        joint_int_p = np.nan

    diagnostics = pd.DataFrame([{
        "n_input": int(len(df)),
        "n_with_leave_period_out_propensity": int(augmented[z_col].notna().sum()),
        "n_model": int(fit.nobs),
        "professors_model": int(d[professor_col].nunique()),
        "periods_model": int(d[period_col].nunique()),
        "min_other_n": int(min_other_n),
        "leave_period_out_rate_mean": float(d[rate_col].mean()),
        "leave_period_out_rate_sd_student_weighted": float(d[rate_col].std(ddof=0)),
        "leave_period_out_support_min": int(d[n_col].min()),
        "leave_period_out_support_median": float(d[n_col].median()),
        "r2": float(fit.rsquared),
        "joint_interaction_stat": joint_int_stat,
        "joint_interaction_p": joint_int_p,
        "note": (
            "historical instructor uptake is an observational proxy for implementation/encouragement; "
            "it is not an instrument and may reflect student composition or other instructor-linked factors"
        ),
    }])
    return pd.DataFrame(coefficients), pd.DataFrame(slope_rows), diagnostics
