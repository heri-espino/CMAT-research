"""Classroom outcome, instructor severity, and degree-programme context for PPA studies.

These helpers separate contemporaneous classroom outcomes from historical instructor
patterns and degree-programme composition. They are descriptive observational tools;
classroom averages, pass rates, instructor identity, and degree programme are not
randomized treatments and must not be interpreted as causal measures of difficulty or
encouragement.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

from cmat_analysis.cohorts import normalize_text

from ._progression import classify_revalidation_records
from .encouragement import _collapse_rare_categories
from .group_models import _fit_finite_mnlogit


DEFAULT_VISIT_GROUP_ORDER = ("0", "1-2", "3", "4+")


def build_mu_classroom_outcome_context(
    data,
    config,
    *,
    min_classroom_n: int = 5,
) -> pd.DataFrame:
    """Build MU classroom outcome context from all real attempt candidates.

    The classroom reference contains numeric and adverse MU attempts, rather than
    only students who later enter the Paper 1 baseline. Numeric grades define the
    classroom mean, while pass/fail rates use every real attempt candidate and count
    adverse outcomes as non-passes. Leave-one-out versions remove the focal row before
    computing its classroom context.

    Parameters
    ----------
    data : object
        Normalized ``StudyData`` object containing academic records.
    config : object
        Study configuration supplying MU subject definitions and passing grade.
    min_classroom_n : int, default=5
        Minimum number of other observations required for leave-one-out rates and
        minimum number of other numeric grades required for the leave-one-out mean.

    Returns
    -------
    pandas.DataFrame
        One row per real MU attempt with classroom size, numeric-grade mean, pass/fail
        rates, and leave-one-out counterparts.
    """
    history = classify_revalidation_records(
        data.academics, passing_grade=config.passing_grade
    )
    real = history.loc[
        history["ACADEMIC_EVENT_TYPE"].eq("real_attempt_candidate")
    ].copy()
    subject = (
        real["SUBJECT_CODE"].astype(str).str.upper().eq(
            str(config.primary_subject_code).upper()
        )
        | real["SUBJECT"].eq(normalize_text(config.primary_subject_name))
    )
    d = real.loc[subject].copy()
    d["MU_CONTEXT_CLASSROOM_ID"] = (
        d["SUBJECT_CODE"].astype(str)
        + "|"
        + d["CLAVEPROFESOR"].astype(str)
        + "|"
        + d["YEAR"].astype(str)
        + "|"
        + d["SESSION"].astype(str)
    )
    numeric = d["GRADE_CLASS"].eq("numeric") & d["GRADE_NUMERIC"].notna()
    d["_NUMERIC"] = numeric.astype(int)
    d["_NUMERIC_GRADE"] = np.where(numeric, d["GRADE_NUMERIC"], np.nan)
    d["_PASS"] = np.where(
        numeric & d["GRADE_NUMERIC"].ge(float(config.passing_grade)), 1.0, 0.0
    )
    d["_ADVERSE"] = d["GRADE_CLASS"].eq("adverse").astype(int)

    grouped = d.groupby("MU_CONTEXT_CLASSROOM_ID", dropna=False)
    d["MU_CLASSROOM_ATTEMPT_N"] = grouped["SOURCE_ROW"].transform("size")
    d["MU_CLASSROOM_NUMERIC_N"] = grouped["_NUMERIC"].transform("sum")
    d["MU_CLASSROOM_ADVERSE_N"] = grouped["_ADVERSE"].transform("sum")
    d["_PASS_SUM"] = grouped["_PASS"].transform("sum")
    d["_GRADE_SUM"] = grouped["_NUMERIC_GRADE"].transform("sum")
    d["MU_CLASSROOM_MEAN_GRADE"] = grouped["_NUMERIC_GRADE"].transform("mean")
    d["MU_CLASSROOM_MEDIAN_GRADE"] = grouped["_NUMERIC_GRADE"].transform("median")
    d["MU_CLASSROOM_SD_GRADE"] = grouped["_NUMERIC_GRADE"].transform("std")
    d["MU_CLASSROOM_PASS_RATE"] = d["_PASS_SUM"] / d["MU_CLASSROOM_ATTEMPT_N"]
    d["MU_CLASSROOM_FAIL_RATE"] = 1.0 - d["MU_CLASSROOM_PASS_RATE"]

    other_n = d["MU_CLASSROOM_ATTEMPT_N"] - 1
    other_pass = d["_PASS_SUM"] - d["_PASS"]
    d["MU_LOO_CLASSROOM_PASS_RATE"] = np.where(
        other_n >= int(min_classroom_n), other_pass / other_n, np.nan
    )
    d["MU_LOO_CLASSROOM_FAIL_RATE"] = 1.0 - d["MU_LOO_CLASSROOM_PASS_RATE"]

    other_numeric_n = d["MU_CLASSROOM_NUMERIC_N"] - d["_NUMERIC"]
    focal_grade = np.where(numeric, d["GRADE_NUMERIC"], 0.0)
    other_grade_sum = d["_GRADE_SUM"] - focal_grade
    d["MU_LOO_CLASSROOM_MEAN_GRADE"] = np.where(
        other_numeric_n >= int(min_classroom_n),
        other_grade_sum / other_numeric_n,
        np.nan,
    )

    return d[[
        "SOURCE_ROW",
        "STUDENT_ID",
        "CLAVEPROFESOR",
        "PERIOD_LABEL",
        "OFFICIAL_CAREER",
        "MU_CONTEXT_CLASSROOM_ID",
        "MU_CLASSROOM_ATTEMPT_N",
        "MU_CLASSROOM_NUMERIC_N",
        "MU_CLASSROOM_ADVERSE_N",
        "MU_CLASSROOM_MEAN_GRADE",
        "MU_CLASSROOM_MEDIAN_GRADE",
        "MU_CLASSROOM_SD_GRADE",
        "MU_CLASSROOM_PASS_RATE",
        "MU_CLASSROOM_FAIL_RATE",
        "MU_LOO_CLASSROOM_MEAN_GRADE",
        "MU_LOO_CLASSROOM_PASS_RATE",
        "MU_LOO_CLASSROOM_FAIL_RATE",
        "GRADE_NUMERIC",
        "GRADE_CLASS",
        "_PASS",
    ]].rename(columns={"_PASS": "MU_ATTEMPT_PASS"})


def leave_period_out_professor_academic_context(
    df: pd.DataFrame,
    *,
    professor_col: str,
    period_col: str,
    grade_col: str,
    pass_col: str,
    min_other_n: int = 30,
    prefix: str = "PROF_ACAD",
) -> pd.DataFrame:
    """Attach historical instructor grading context estimated from other periods.

    For each instructor-period cell, pass rate and numeric mean grade are computed
    from the same instructor's observations in all other periods. This prevents the
    focal period from contributing to the historical context, although the resulting
    measures can still reflect student composition and other unobserved differences.

    Parameters
    ----------
    df : pandas.DataFrame
        Attempt-level data containing instructor, period, numeric grade, and pass flag.
    professor_col : str
        Instructor identifier.
    period_col : str
        Academic-period identifier.
    grade_col : str
        Numeric grade column; nonnumeric outcomes should be missing.
    pass_col : str
        Binary pass indicator defined for all real attempt candidates.
    min_other_n : int, default=30
        Minimum other-period attempt count for pass rate and minimum other-period
        numeric-grade count for mean grade.
    prefix : str, default="PROF_ACAD"
        Prefix for generated columns.

    Returns
    -------
    pandas.DataFrame
        Copy of ``df`` with leave-period-out pass rate, fail rate, numeric mean grade,
        supporting counts, and student-weighted z-standardized versions.
    """
    required = {professor_col, period_col, grade_col, pass_col}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")

    out = df.copy()
    work = out[[professor_col, period_col, grade_col, pass_col]].dropna(
        subset=[professor_col, period_col, pass_col]
    ).copy()
    work[pass_col] = pd.to_numeric(work[pass_col], errors="coerce")
    if work[pass_col].isna().any() or not set(work[pass_col].unique()).issubset({0, 1}):
        raise ValueError(f"{pass_col} must contain only binary 0/1 values.")
    work[grade_col] = pd.to_numeric(work[grade_col], errors="coerce")
    work["_GRADE_PRESENT"] = work[grade_col].notna().astype(int)
    work["_GRADE_VALUE"] = work[grade_col].fillna(0.0)

    prof = work.groupby(professor_col, dropna=False).agg(
        _prof_pass_sum=(pass_col, "sum"),
        _prof_attempt_n=(pass_col, "size"),
        _prof_grade_sum=("_GRADE_VALUE", "sum"),
        _prof_grade_n=("_GRADE_PRESENT", "sum"),
    ).reset_index()
    cell = work.groupby([professor_col, period_col], dropna=False).agg(
        _cell_pass_sum=(pass_col, "sum"),
        _cell_attempt_n=(pass_col, "size"),
        _cell_grade_sum=("_GRADE_VALUE", "sum"),
        _cell_grade_n=("_GRADE_PRESENT", "sum"),
    ).reset_index()
    cell = cell.merge(prof, on=professor_col, how="left")
    cell["_other_pass_sum"] = cell["_prof_pass_sum"] - cell["_cell_pass_sum"]
    cell["_other_attempt_n"] = cell["_prof_attempt_n"] - cell["_cell_attempt_n"]
    cell["_other_grade_sum"] = cell["_prof_grade_sum"] - cell["_cell_grade_sum"]
    cell["_other_grade_n"] = cell["_prof_grade_n"] - cell["_cell_grade_n"]

    pass_rate_col = f"{prefix}_LEAVE_PERIOD_OUT_PASS_RATE"
    fail_rate_col = f"{prefix}_LEAVE_PERIOD_OUT_FAIL_RATE"
    mean_grade_col = f"{prefix}_LEAVE_PERIOD_OUT_MEAN_GRADE"
    attempt_n_col = f"{prefix}_LEAVE_PERIOD_OUT_ATTEMPT_N"
    grade_n_col = f"{prefix}_LEAVE_PERIOD_OUT_GRADE_N"
    pass_z_col = f"{prefix}_LEAVE_PERIOD_OUT_PASS_Z"
    grade_z_col = f"{prefix}_LEAVE_PERIOD_OUT_GRADE_Z"

    cell[attempt_n_col] = cell["_other_attempt_n"].astype(int)
    cell[grade_n_col] = cell["_other_grade_n"].astype(int)
    cell[pass_rate_col] = np.where(
        cell["_other_attempt_n"] >= int(min_other_n),
        cell["_other_pass_sum"] / cell["_other_attempt_n"],
        np.nan,
    )
    cell[fail_rate_col] = 1.0 - cell[pass_rate_col]
    cell[mean_grade_col] = np.where(
        cell["_other_grade_n"] >= int(min_other_n),
        cell["_other_grade_sum"] / cell["_other_grade_n"],
        np.nan,
    )

    attach = cell[[
        professor_col,
        period_col,
        pass_rate_col,
        fail_rate_col,
        mean_grade_col,
        attempt_n_col,
        grade_n_col,
    ]]
    out = out.merge(attach, on=[professor_col, period_col], how="left")

    for source_col, z_col in ((pass_rate_col, pass_z_col), (mean_grade_col, grade_z_col)):
        values = out[source_col].dropna()
        sd = float(values.std(ddof=0)) if len(values) else np.nan
        mean = float(values.mean()) if len(values) else np.nan
        out[z_col] = (out[source_col] - mean) / sd if np.isfinite(sd) and sd > 0 else np.nan
    return out


def major_visit_group_summary(
    df: pd.DataFrame,
    *,
    major_col: str = "MU_CAREER_OFFICIAL",
    group_col: str = "MU_VISIT_GROUP",
    visit_col: str = "MU_VISITS_CMAT_PERIOD",
    min_n: int = 30,
    group_order: Sequence[str] = DEFAULT_VISIT_GROUP_ORDER,
) -> pd.DataFrame:
    """Summarize initial CMAT use by official degree programme.

    Parameters
    ----------
    df : pandas.DataFrame
        Student-level MU baseline.
    major_col : str, default="MU_CAREER_OFFICIAL"
        Official degree-programme column.
    group_col : str, default="MU_VISIT_GROUP"
        0/1-2/3/4+ visit group.
    visit_col : str, default="MU_VISITS_CMAT_PERIOD"
        Same-period visit count.
    min_n : int, default=30
        Minimum programme sample size retained in the summary.
    group_order : sequence of str, default=("0", "1-2", "3", "4+")
        Ordered visit groups to summarize.

    Returns
    -------
    pandas.DataFrame
        One row per retained degree programme with sample size, mean visits, any-use
        rate, and shares in each visit group.
    """
    required = {major_col, group_col, visit_col}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    groups = tuple(str(group) for group in group_order)
    d = df[list(required)].dropna(subset=[major_col, group_col]).copy()
    d[group_col] = d[group_col].astype(str)
    d = d.loc[d[group_col].isin(groups)].copy()
    d[visit_col] = pd.to_numeric(d[visit_col], errors="coerce").fillna(0.0)

    base = d.groupby(major_col).agg(
        n=(group_col, "size"),
        mean_visits=(visit_col, "mean"),
        any_use_rate=(visit_col, lambda s: float((s > 0).mean())),
    )
    counts = (
        d.groupby([major_col, group_col], observed=False)
        .size()
        .unstack(fill_value=0)
        .reindex(columns=groups, fill_value=0)
    )
    out = base.join(counts).reset_index()
    out = out.loc[out["n"] >= int(min_n)].copy()
    for group in groups:
        safe = group.replace("+", "plus").replace("-", "_")
        out[f"count_{safe}"] = out.pop(group).astype(int)
        out[f"share_{safe}"] = out[f"count_{safe}"] / out["n"]
    return out.sort_values(["any_use_rate", "n"], ascending=[False, False]).reset_index(drop=True)


def major_uptake_increment(
    df: pd.DataFrame,
    *,
    outcome_col: str = "MU_ANY_VISIT",
    major_col: str = "MU_CAREER_OFFICIAL",
    professor_col: str = "MU_PROFESSOR",
    period_col: str = "MU_PERIOD_LABEL",
    min_major_n: int = 30,
) -> pd.DataFrame:
    """Quantify added descriptive fit from degree programme beyond professor and period.

    Parameters
    ----------
    df : pandas.DataFrame
        Student-level MU baseline.
    outcome_col : str, default="MU_ANY_VISIT"
        Binary CMAT-use outcome.
    major_col : str, default="MU_CAREER_OFFICIAL"
        Official degree programme.
    professor_col : str, default="MU_PROFESSOR"
        MU instructor identifier.
    period_col : str, default="MU_PERIOD_LABEL"
        Academic period.
    min_major_n : int, default=30
        Minimum sample size before smaller programmes are pooled as ``OTHER``.

    Returns
    -------
    pandas.DataFrame
        Nested linear-probability-model comparison for adding degree-programme fixed
        effects to period and professor fixed effects.
    """
    required = {outcome_col, major_col, professor_col, period_col}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    d = df[list(required)].dropna().copy()
    d[outcome_col] = pd.to_numeric(d[outcome_col], errors="coerce")
    d = d.dropna(subset=[outcome_col])
    if not set(d[outcome_col].unique()).issubset({0, 1}):
        raise ValueError(f"{outcome_col} must be binary 0/1.")
    d["_MODEL_MAJOR"] = _collapse_rare_categories(d[major_col], min_major_n)
    base = smf.ols(
        f"{outcome_col} ~ C({period_col}) + C({professor_col})", data=d
    ).fit()
    full = smf.ols(
        f"{outcome_col} ~ C({period_col}) + C({professor_col}) + C(_MODEL_MAJOR)",
        data=d,
    ).fit()
    df_num = int(round(base.df_resid - full.df_resid))
    ss_gain = float(base.ssr - full.ssr)
    mse_full = float(full.ssr / full.df_resid)
    f_stat = float((ss_gain / df_num) / mse_full) if df_num > 0 and mse_full > 0 else np.nan
    p_value = float(stats.f.sf(f_stat, df_num, full.df_resid)) if np.isfinite(f_stat) else np.nan
    partial_r2 = float((base.ssr - full.ssr) / base.ssr) if float(base.ssr) > 0 else np.nan
    return pd.DataFrame([{
        "outcome": outcome_col,
        "n": int(full.nobs),
        "majors": int(d["_MODEL_MAJOR"].nunique()),
        "professors": int(d[professor_col].nunique()),
        "periods": int(d[period_col].nunique()),
        "r2_base_period_professor": float(base.rsquared),
        "r2_plus_major": float(full.rsquared),
        "delta_r2_major": float(full.rsquared - base.rsquared),
        "partial_r2_major": partial_r2,
        "joint_f_major": f_stat,
        "joint_df_num": df_num,
        "joint_df_den": float(full.df_resid),
        "joint_p_major": p_value,
        "note": "descriptive association; degree programme is not randomized",
    }])


def major_visit_group_multinomial_increment(
    df: pd.DataFrame,
    *,
    group_col: str = "MU_VISIT_GROUP",
    major_col: str = "MU_CAREER_OFFICIAL",
    professor_col: str = "MU_PROFESSOR",
    period_col: str = "MU_PERIOD_LABEL",
    min_major_n: int = 30,
    group_order: Sequence[str] = DEFAULT_VISIT_GROUP_ORDER,
) -> pd.DataFrame:
    """Test whether degree programme adds fit for 0/1-2/3/4+ use beyond professor.

    Parameters
    ----------
    df : pandas.DataFrame
        Student-level MU baseline.
    group_col : str, default="MU_VISIT_GROUP"
        Multinomial CMAT-use group.
    major_col : str, default="MU_CAREER_OFFICIAL"
        Official degree programme.
    professor_col : str, default="MU_PROFESSOR"
        MU instructor identifier.
    period_col : str, default="MU_PERIOD_LABEL"
        Academic period.
    min_major_n : int, default=30
        Minimum sample size before smaller programmes are pooled as ``OTHER``.
    group_order : sequence of str, default=("0", "1-2", "3", "4+")
        Visit-group order.

    Returns
    -------
    pandas.DataFrame
        Likelihood-ratio comparison between period+professor controls and the same
        multinomial model plus degree-programme fixed effects.
    """
    required = {group_col, major_col, professor_col, period_col}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    groups = tuple(str(group) for group in group_order)
    d = df[list(required)].dropna().copy()
    d[group_col] = d[group_col].astype(str)
    d = d.loc[d[group_col].isin(groups)].copy()
    if set(d[group_col].unique()) != set(groups):
        absent = sorted(set(groups).difference(d[group_col].unique()))
        raise ValueError(f"Requested visit groups absent from data: {absent}")
    d["_GROUP_CODE"] = d[group_col].map({group: i for i, group in enumerate(groups)}).astype(int)
    d["_MODEL_MAJOR"] = _collapse_rare_categories(d[major_col], min_major_n)
    base_formula = f"_GROUP_CODE ~ C({period_col}) + C({professor_col})"
    full_formula = base_formula + " + C(_MODEL_MAJOR)"
    base, base_method = _fit_finite_mnlogit(base_formula, d)
    full, full_method = _fit_finite_mnlogit(full_formula, d)
    lr = max(float(2.0 * (full.llf - base.llf)), 0.0)
    df_diff = int(round(full.df_model - base.df_model))
    p_value = float(stats.chi2.sf(lr, df_diff))
    ll_null = float(full.llnull)
    return pd.DataFrame([{
        "outcome": group_col,
        "n": int(full.nobs),
        "groups": "|".join(groups),
        "majors": int(d["_MODEL_MAJOR"].nunique()),
        "professors": int(d[professor_col].nunique()),
        "periods": int(d[period_col].nunique()),
        "mcfadden_r2_base_period_professor": float(1.0 - base.llf / ll_null),
        "mcfadden_r2_plus_major": float(1.0 - full.llf / ll_null),
        "delta_mcfadden_r2_major": float((base.llf - full.llf) / ll_null),
        "lr_stat_major": lr,
        "lr_df": df_diff,
        "lr_p_major": p_value,
        "base_optimizer": base_method,
        "full_optimizer": full_method,
        "note": "descriptive multinomial association; degree programme is not randomized",
    }])


def academic_context_uptake_models(
    df: pd.DataFrame,
    *,
    outcome_col: str,
    context_cols: Sequence[str],
    period_col: str,
    major_col: str | None = None,
    professor_col: str | None = None,
    min_major_n: int = 30,
) -> pd.DataFrame:
    """Estimate separate standardized associations between academic context and CMAT use.

    Each context measure is entered in its own linear probability model to avoid
    treating highly collinear classroom mean-grade and pass-rate measures as distinct
    causal mechanisms. Models always adjust for period, optionally adjust for degree
    programme, and optionally add professor fixed effects as a second specification.

    Parameters
    ----------
    df : pandas.DataFrame
        Student-level analytical data with binary CMAT use and context measures.
    outcome_col : str
        Binary CMAT-use outcome.
    context_cols : sequence of str
        Continuous context measures to standardize and test separately.
    period_col : str
        Academic-period control.
    major_col : str or None, optional
        Optional degree-programme control.
    professor_col : str or None, optional
        Optional instructor fixed effect for a second specification.
    min_major_n : int, default=30
        Minimum degree-programme sample size before pooling smaller groups.

    Returns
    -------
    pandas.DataFrame
        Coefficients, robust standard errors, confidence intervals, p-values, and R2
        for each context measure and specification; coefficients are probability-point
        changes associated with one sample standard deviation of the context measure.
    """
    required = {outcome_col, period_col, *context_cols}
    if major_col is not None:
        required.add(major_col)
    if professor_col is not None:
        required.add(professor_col)
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")

    rows: list[dict[str, object]] = []
    for context_col in context_cols:
        subset = [outcome_col, period_col, context_col]
        if major_col is not None:
            subset.append(major_col)
        if professor_col is not None:
            subset.append(professor_col)
        d = df[subset].dropna().copy()
        d[outcome_col] = pd.to_numeric(d[outcome_col], errors="coerce")
        d[context_col] = pd.to_numeric(d[context_col], errors="coerce")
        d = d.dropna(subset=[outcome_col, context_col])
        if d.empty or d[context_col].std(ddof=0) <= 0:
            continue
        if not set(d[outcome_col].unique()).issubset({0, 1}):
            raise ValueError(f"{outcome_col} must be binary 0/1.")
        d["_CONTEXT_Z"] = (d[context_col] - d[context_col].mean()) / d[context_col].std(ddof=0)
        rhs = ["_CONTEXT_Z", f"C({period_col})"]
        if major_col is not None:
            d["_MODEL_MAJOR"] = _collapse_rare_categories(d[major_col], min_major_n)
            rhs.append("C(_MODEL_MAJOR)")
        specifications = [("period_major", rhs.copy())]
        if professor_col is not None:
            specifications.append(("period_major_professor_fe", rhs + [f"C({professor_col})"]))
        for specification, terms in specifications:
            fit = smf.ols(f"{outcome_col} ~ " + " + ".join(terms), data=d).fit(cov_type="HC1")
            estimate = float(fit.params["_CONTEXT_Z"])
            se = float(fit.bse["_CONTEXT_Z"])
            rows.append({
                "context_measure": context_col,
                "specification": specification,
                "n": int(fit.nobs),
                "estimate_per_sd": estimate,
                "se_hc1": se,
                "ci_low": estimate - 1.96 * se,
                "ci_high": estimate + 1.96 * se,
                "p_value": float(fit.pvalues["_CONTEXT_Z"]),
                "r2": float(fit.rsquared),
                "note": "descriptive linear probability model; context is not a causal difficulty measure",
            })
    return pd.DataFrame(rows)


def professor_period_context_correlations(
    df: pd.DataFrame,
    *,
    professor_col: str,
    period_col: str,
    uptake_col: str,
    academic_cols: Sequence[str],
) -> pd.DataFrame:
    """Correlate historical instructor uptake propensity with academic context.

    Parameters
    ----------
    df : pandas.DataFrame
        Data containing one repeated value per instructor-period cell for the historical
        CMAT-uptake propensity and academic-context measures.
    professor_col : str
        Instructor identifier.
    period_col : str
        Academic-period identifier.
    uptake_col : str
        Leave-period-out instructor CMAT-use propensity.
    academic_cols : sequence of str
        Historical instructor mean-grade or pass-rate measures.

    Returns
    -------
    pandas.DataFrame
        Pearson and Spearman correlations across distinct instructor-period cells.
    """
    required = {professor_col, period_col, uptake_col, *academic_cols}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    cells = df[list(required)].drop_duplicates([professor_col, period_col]).copy()
    rows: list[dict[str, object]] = []
    for academic_col in academic_cols:
        d = cells[[uptake_col, academic_col]].dropna()
        if len(d) < 3 or d[uptake_col].nunique() < 2 or d[academic_col].nunique() < 2:
            continue
        pearson_r, pearson_p = stats.pearsonr(d[academic_col], d[uptake_col])
        spearman_r, spearman_p = stats.spearmanr(d[academic_col], d[uptake_col])
        rows.append({
            "academic_context": academic_col,
            "uptake_context": uptake_col,
            "professor_period_cells": int(len(d)),
            "pearson_r": float(pearson_r),
            "pearson_p": float(pearson_p),
            "spearman_rho": float(spearman_r),
            "spearman_p": float(spearman_p),
            "note": "cell-level descriptive correlation; neither measure is a randomized instructor trait",
        })
    return pd.DataFrame(rows)
