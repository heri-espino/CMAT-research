"""Confirmatory robustness and inference for longitudinal academic adaptation.

These helpers support pre-specified robustness checks for experience-state definitions,
post-failure behavioral responses, degree-programme heterogeneity, and the observed
instructor choice-set proxy. They remain observational and do not identify latent
engagement, intrinsic instructor difficulty, or unconstrained student preference.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


def _collapse_rare(series: pd.Series, min_n: int) -> pd.Series:
    counts = series.value_counts(dropna=False)
    keep = set(counts[counts >= int(min_n)].index)
    return series.where(series.isin(keep), "OTHER")


def _standardize(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    sd = float(values.std(ddof=0))
    if not np.isfinite(sd) or sd <= 0:
        return pd.Series(np.nan, index=series.index, dtype=float)
    return (values - float(values.mean())) / sd


def _joint_wald(fit, *, contains: str) -> tuple[float, int, float]:
    names = list(fit.params.index)
    indices = [i for i, name in enumerate(names) if contains in name]
    if not indices:
        return np.nan, 0, np.nan
    restriction = np.zeros((len(indices), len(names)), dtype=float)
    for row, index in enumerate(indices):
        restriction[row, index] = 1.0
    try:
        test = fit.wald_test(restriction, scalar=True)
        return float(test.statistic), int(len(indices)), float(test.pvalue)
    except Exception:
        return np.nan, int(len(indices)), np.nan


def classify_experience_state(
    df: pd.DataFrame,
    *,
    z_col: str = "MU_FIRST_Z",
    pass_rate_col: str = "MU_FIRST_LOO_PASS_RATE",
    performance_cut: float = -0.5,
    difficulty_quantile: float = 0.25,
) -> pd.Series:
    """Classify first-MU experience into five parsimonious academic-strain states.

    Parameters
    ----------
    df : pandas.DataFrame
        Student-level first-MU table.
    z_col : str, default="MU_FIRST_Z"
        Classroom-relative performance measure; lower values indicate weaker relative
        performance.
    pass_rate_col : str, default="MU_FIRST_LOO_PASS_RATE"
        Leave-one-out classroom pass-rate context; lower values indicate a classroom
        with lower observed pass rates.
    performance_cut : float, default=-0.5
        Threshold at or below which relative performance is classified as individual
        strain.
    difficulty_quantile : float, default=0.25
        Quantile of the observed leave-one-out classroom pass-rate distribution used
        to define the high-difficulty contextual tail.

    Returns
    -------
    pandas.Series
        One state per row: ``lower_strain``, ``contextual_challenge``,
        ``individual_strain``, ``compounded_strain``, or
        ``adverse_or_nonnumeric``/``unknown_context`` when the required measures are
        unavailable.
    """
    required = {z_col, pass_rate_col}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    if not 0 < float(difficulty_quantile) < 1:
        raise ValueError("difficulty_quantile must lie strictly between 0 and 1")

    z = pd.to_numeric(df[z_col], errors="coerce")
    pass_rate = pd.to_numeric(df[pass_rate_col], errors="coerce")
    valid_context = pass_rate.dropna()
    difficulty_cut = (
        float(valid_context.quantile(float(difficulty_quantile)))
        if len(valid_context)
        else np.nan
    )
    state = pd.Series("lower_strain", index=df.index, dtype="object")
    state.loc[z.isna()] = "adverse_or_nonnumeric"
    state.loc[z.notna() & pass_rate.isna()] = "unknown_context"
    if np.isfinite(difficulty_cut):
        low = z.le(float(performance_cut))
        hard = pass_rate.le(difficulty_cut)
        numeric_context = z.notna() & pass_rate.notna()
        state.loc[numeric_context & ~low & hard] = "contextual_challenge"
        state.loc[numeric_context & low & ~hard] = "individual_strain"
        state.loc[numeric_context & low & hard] = "compounded_strain"
    return state


def experience_state_sensitivity(
    mu_students: pd.DataFrame,
    *,
    later_calc_student_ids: Iterable[object] | None = None,
    performance_cuts: tuple[float, ...] = (-0.25, -0.5, -0.75),
    difficulty_quantiles: tuple[float, ...] = (0.20, 0.25, 1 / 3),
) -> pd.DataFrame:
    """Summarize experience states across a pre-specified threshold grid.

    Parameters
    ----------
    mu_students : pandas.DataFrame
        Student-level first-MU table containing performance, classroom context, CMAT
        use, and eventual MU progression fields.
    later_calc_student_ids : iterable, optional
        Student identifiers observed later in Calculus; when supplied, the function
        also reports later-Calculus observation rates.
    performance_cuts : tuple of float
        Relative-performance thresholds evaluated in the sensitivity grid.
    difficulty_quantiles : tuple of float
        Classroom pass-rate quantiles evaluated as the high-difficulty tail.

    Returns
    -------
    pandas.DataFrame
        State sizes and principal support/progression rates for every threshold
        specification.
    """
    required = {
        "STUDENT_ID",
        "MU_FIRST_Z",
        "MU_FIRST_LOO_PASS_RATE",
        "MU_FIRST_CMAT_VISITS",
        "MU_EVER_PASSED",
    }
    missing = required.difference(mu_students.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")

    later_ids = set(map(str, later_calc_student_ids)) if later_calc_student_ids is not None else None
    rows: list[dict[str, object]] = []
    context = pd.to_numeric(mu_students["MU_FIRST_LOO_PASS_RATE"], errors="coerce").dropna()
    for performance_cut in performance_cuts:
        for difficulty_quantile in difficulty_quantiles:
            difficulty_cut = (
                float(context.quantile(float(difficulty_quantile))) if len(context) else np.nan
            )
            state = classify_experience_state(
                mu_students,
                performance_cut=float(performance_cut),
                difficulty_quantile=float(difficulty_quantile),
            )
            work = mu_students.copy()
            work["_STATE"] = state
            if later_ids is not None:
                work["_LATER_CALC"] = work["STUDENT_ID"].astype(str).isin(later_ids).astype(int)
            for label, sub in work.groupby("_STATE", dropna=False):
                row: dict[str, object] = {
                    "performance_cut": float(performance_cut),
                    "difficulty_quantile": float(difficulty_quantile),
                    "difficulty_pass_rate_cut": difficulty_cut,
                    "state": label,
                    "n": int(len(sub)),
                    "first_cmat_use_rate": float((sub["MU_FIRST_CMAT_VISITS"] > 0).mean()),
                    "mean_first_cmat_visits": float(sub["MU_FIRST_CMAT_VISITS"].mean()),
                    "eventual_mu_pass_rate": float(sub["MU_EVER_PASSED"].mean()),
                }
                if later_ids is not None:
                    row["observed_later_calc_rate"] = float(sub["_LATER_CALC"].mean())
                rows.append(row)
    return pd.DataFrame(rows).sort_values(
        ["performance_cut", "difficulty_quantile", "state"]
    ).reset_index(drop=True)


def continuous_challenge_response_model(
    mu_students: pd.DataFrame,
    *,
    min_career_n: int = 30,
) -> pd.DataFrame:
    """Model first-MU CMAT use continuously as performance and context vary.

    Parameters
    ----------
    mu_students : pandas.DataFrame
        Student-level first-MU table.
    min_career_n : int, default=30
        Minimum degree-programme size retained before rarer programmes are pooled.

    Returns
    -------
    pandas.DataFrame
        Cluster-robust linear-probability coefficients for standardized relative
        performance, standardized leave-one-out classroom pass rate, and their
        interaction, with period and degree-programme adjustment.
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
    d = mu_students[list(required)].copy()
    d["_ANY_CMAT"] = (d["MU_FIRST_CMAT_VISITS"] > 0).astype(int)
    d["_Z"] = _standardize(d["MU_FIRST_Z"])
    d["_PASS_CONTEXT"] = _standardize(d["MU_FIRST_LOO_PASS_RATE"])
    d = d.dropna(subset=["_Z", "_PASS_CONTEXT", "MU_FIRST_CLASSROOM_ID"]).copy()
    d["_CAREER"] = _collapse_rare(d["MU_FIRST_CAREER"], min_career_n)
    fit = smf.ols(
        "_ANY_CMAT ~ _Z * _PASS_CONTEXT + C(MU_FIRST_PERIOD_LABEL) + C(_CAREER)",
        data=d,
    ).fit(cov_type="cluster", cov_kwds={"groups": d["MU_FIRST_CLASSROOM_ID"]})
    rows = []
    for term in ("_Z", "_PASS_CONTEXT", "_Z:_PASS_CONTEXT"):
        rows.append({
            "term": term,
            "n": int(fit.nobs),
            "clusters": int(d["MU_FIRST_CLASSROOM_ID"].nunique()),
            "estimate": float(fit.params[term]),
            "se_cluster": float(fit.bse[term]),
            "p_value": float(fit.pvalues[term]),
            "r2": float(fit.rsquared),
        })
    return pd.DataFrame(rows)


def post_failure_response_models(
    transitions: pd.DataFrame,
    *,
    min_career_n: int = 30,
) -> pd.DataFrame:
    """Estimate formal response models after a failed or adverse MU attempt.

    Parameters
    ----------
    transitions : pandas.DataFrame
        Consecutive post-failure MU transitions, preferably restricted by the caller to
        periods with valid CMAT coverage when support-use outcomes are interpreted.
    min_career_n : int, default=30
        Minimum transition count before a degree programme is retained separately.

    Returns
    -------
    pandas.DataFrame
        Cluster-robust linear-probability coefficients for movement toward historically
        higher-outcome instructors and subsequent CMAT use. Instructor-response models
        include the prior instructor rank to account for ceiling/regression-to-the-mean
        opportunities; all models adjust for attempt number, period and degree programme.
    """
    required = {
        "STUDENT_ID",
        "FAILED_ATTEMPT_NUMBER",
        "PREV_PERIOD_INDEX",
        "CAREER",
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
    d["_CAREER"] = _collapse_rare(d["CAREER"], min_career_n)
    d["_ATTEMPT_BAND"] = np.select(
        [d["FAILED_ATTEMPT_NUMBER"].eq(1), d["FAILED_ATTEMPT_NUMBER"].eq(2)],
        ["1", "2"],
        default="3+",
    )
    d["_INCREASED_CMAT"] = d["NEXT_CMAT_VISITS"].gt(d["PREV_CMAT_VISITS"]).astype(int)
    d["_PREV_RANK_10PP"] = pd.to_numeric(
        d["PREV_PROF_EASINESS_PERCENTILE"], errors="coerce"
    ) * 10.0

    model_specs: list[tuple[str, str, str, str | None]] = [
        (
            "higher_outcome_percentile",
            "_MOVE_HIGHER_PERCENTILE",
            "_PREV_RANK_10PP + PREV_ANY_CMAT + C(_ATTEMPT_BAND) + C(PREV_PERIOD_INDEX) + C(_CAREER)",
            "DELTA_PROF_EASINESS_PERCENTILE",
        ),
        (
            "next_cmat_use",
            "NEXT_ANY_CMAT",
            "PREV_ANY_CMAT + C(_ATTEMPT_BAND) + C(PREV_PERIOD_INDEX) + C(_CAREER)",
            None,
        ),
        (
            "increased_cmat",
            "_INCREASED_CMAT",
            "PREV_ANY_CMAT + C(_ATTEMPT_BAND) + C(PREV_PERIOD_INDEX) + C(_CAREER)",
            None,
        ),
    ]
    if {"DELTA_PROF_PRIOR_PASS_RATE", "PREV_PROF_PRIOR_PASS_RATE"}.issubset(d.columns):
        d["_PREV_PASS_10PP"] = pd.to_numeric(d["PREV_PROF_PRIOR_PASS_RATE"], errors="coerce") * 10.0
        model_specs.append((
            "higher_prior_pass_rate",
            "_MOVE_HIGHER_PASS",
            "_PREV_PASS_10PP + PREV_ANY_CMAT + C(_ATTEMPT_BAND) + C(PREV_PERIOD_INDEX) + C(_CAREER)",
            "DELTA_PROF_PRIOR_PASS_RATE",
        ))
    if {"DELTA_PROF_PRIOR_MEAN_GRADE", "PREV_PROF_PRIOR_MEAN_GRADE"}.issubset(d.columns):
        d["_PREV_MEAN_GRADE"] = pd.to_numeric(d["PREV_PROF_PRIOR_MEAN_GRADE"], errors="coerce")
        model_specs.append((
            "higher_prior_mean_grade",
            "_MOVE_HIGHER_GRADE",
            "_PREV_MEAN_GRADE + PREV_ANY_CMAT + C(_ATTEMPT_BAND) + C(PREV_PERIOD_INDEX) + C(_CAREER)",
            "DELTA_PROF_PRIOR_MEAN_GRADE",
        ))

    rows: list[dict[str, object]] = []
    for model_name, outcome, rhs, delta_col in model_specs:
        model_data = d.copy()
        if delta_col is not None:
            delta = pd.to_numeric(model_data[delta_col], errors="coerce")
            model_data = model_data.loc[delta.notna()].copy()
            if outcome == "_MOVE_HIGHER_PERCENTILE":
                model_data[outcome] = pd.to_numeric(
                    model_data["DELTA_PROF_EASINESS_PERCENTILE"], errors="coerce"
                ).gt(0).astype(int)
            elif outcome == "_MOVE_HIGHER_PASS":
                model_data[outcome] = pd.to_numeric(
                    model_data["DELTA_PROF_PRIOR_PASS_RATE"], errors="coerce"
                ).gt(0).astype(int)
            elif outcome == "_MOVE_HIGHER_GRADE":
                model_data[outcome] = pd.to_numeric(
                    model_data["DELTA_PROF_PRIOR_MEAN_GRADE"], errors="coerce"
                ).gt(0).astype(int)
        needed = [outcome, "STUDENT_ID"]
        if "_PREV_RANK_10PP" in rhs:
            needed.append("_PREV_RANK_10PP")
        if "_PREV_PASS_10PP" in rhs:
            needed.append("_PREV_PASS_10PP")
        if "_PREV_MEAN_GRADE" in rhs:
            needed.append("_PREV_MEAN_GRADE")
        model_data = model_data.dropna(subset=needed).copy()
        if len(model_data) < 20 or model_data[outcome].nunique() < 2:
            continue
        fit = smf.ols(f"{outcome} ~ {rhs}", data=model_data).fit(
            cov_type="cluster", cov_kwds={"groups": model_data["STUDENT_ID"]}
        )
        focal_terms = [
            name for name in fit.params.index
            if name in {"PREV_ANY_CMAT", "_PREV_RANK_10PP", "_PREV_PASS_10PP", "_PREV_MEAN_GRADE"}
            or name.startswith("C(_ATTEMPT_BAND)")
        ]
        for term in focal_terms:
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
        stat, df_num, p_value = _joint_wald(fit, contains="C(_ATTEMPT_BAND)")
        rows.append({
            "model": model_name,
            "term": "attempt_band_joint",
            "n": int(fit.nobs),
            "student_clusters": int(model_data["STUDENT_ID"].nunique()),
            "estimate": stat,
            "se_cluster": np.nan,
            "p_value": p_value,
            "r2": float(fit.rsquared),
            "joint_df": df_num,
        })
    return pd.DataFrame(rows)


def career_heterogeneity_tests(
    mu_students: pd.DataFrame,
    calc_choices: pd.DataFrame,
    *,
    min_career_n: int = 30,
) -> pd.DataFrame:
    """Test whether degree programme adds joint explanatory information to key responses.

    Parameters
    ----------
    mu_students : pandas.DataFrame
        Student-level first-MU table.
    calc_choices : pandas.DataFrame
        First later-Calculus table from the longitudinal trajectory builder.
    min_career_n : int, default=30
        Minimum programme size before rarer programmes are pooled into ``OTHER``.

    Returns
    -------
    pandas.DataFrame
        Cluster-robust omnibus tests and incremental R-squared measures for degree
        programme in first-MU CMAT use, later-Calculus CMAT use, and selected historical
        instructor-outcome rank, plus one global programme-by-experience-state test for
        first-MU support use.
    """
    rows: list[dict[str, object]] = []

    mu = mu_students.copy()
    mu["_STATE"] = classify_experience_state(mu)
    mu = mu.loc[mu["_STATE"].ne("unknown_context")].copy()
    mu["_ANY_CMAT"] = (mu["MU_FIRST_CMAT_VISITS"] > 0).astype(int)
    mu["_CAREER"] = _collapse_rare(mu["MU_FIRST_CAREER"], min_career_n)

    calc = calc_choices.copy()
    calc["_STATE"] = classify_experience_state(calc)
    calc = calc.loc[calc["_STATE"].ne("unknown_context")].copy()
    calc["_CAREER"] = _collapse_rare(calc["MU_FIRST_CAREER"], min_career_n)

    specifications: list[tuple[str, pd.DataFrame, str, str, str, str]] = [
        (
            "first_mu_cmat",
            mu,
            "_ANY_CMAT",
            "C(_STATE) + C(MU_FIRST_PERIOD_LABEL)",
            "MU_FIRST_CLASSROOM_ID",
            "C(_CAREER)",
        ),
        (
            "calc_cmat",
            calc,
            "CALC_FIRST_ANY_CMAT",
            "C(_STATE) + C(MU_FIRST_VISIT_GROUP) + C(CALC_FIRST_PERIOD_LABEL)",
            "MU_FIRST_CLASSROOM_ID",
            "C(_CAREER)",
        ),
        (
            "calc_choice_rank",
            calc.dropna(subset=["CALC_CHOSEN_EASINESS_PERCENTILE"]).copy(),
            "CALC_CHOSEN_EASINESS_PERCENTILE",
            "C(_STATE) + C(MU_FIRST_VISIT_GROUP) + C(CALC_FIRST_PERIOD_LABEL)",
            "MU_FIRST_CLASSROOM_ID",
            "C(_CAREER)",
        ),
    ]
    for analysis, data, outcome, base_rhs, cluster_col, career_term in specifications:
        data = data.dropna(subset=[outcome, cluster_col, "_CAREER"]).copy()
        if len(data) < 20:
            continue
        base = smf.ols(f"{outcome} ~ {base_rhs}", data=data).fit(
            cov_type="cluster", cov_kwds={"groups": data[cluster_col]}
        )
        full = smf.ols(f"{outcome} ~ {base_rhs} + {career_term}", data=data).fit(
            cov_type="cluster", cov_kwds={"groups": data[cluster_col]}
        )
        stat, df_num, p_value = _joint_wald(full, contains="C(_CAREER)")
        delta = float(full.rsquared - base.rsquared)
        partial = delta / (1.0 - float(base.rsquared)) if base.rsquared < 1 else np.nan
        rows.append({
            "analysis": analysis,
            "test": "career_main_effect",
            "n": int(full.nobs),
            "clusters": int(data[cluster_col].nunique()),
            "career_levels": int(data["_CAREER"].nunique()),
            "r2_base": float(base.rsquared),
            "r2_full": float(full.rsquared),
            "delta_r2": delta,
            "partial_r2": partial,
            "wald_stat": stat,
            "wald_df": df_num,
            "p_value": p_value,
        })

    mu_interaction = mu.dropna(subset=["_ANY_CMAT", "MU_FIRST_CLASSROOM_ID", "_CAREER"]).copy()
    if len(mu_interaction) >= 20:
        base = smf.ols(
            "_ANY_CMAT ~ C(_STATE) + C(_CAREER) + C(MU_FIRST_PERIOD_LABEL)",
            data=mu_interaction,
        ).fit(cov_type="cluster", cov_kwds={"groups": mu_interaction["MU_FIRST_CLASSROOM_ID"]})
        full = smf.ols(
            "_ANY_CMAT ~ C(_STATE) * C(_CAREER) + C(MU_FIRST_PERIOD_LABEL)",
            data=mu_interaction,
        ).fit(cov_type="cluster", cov_kwds={"groups": mu_interaction["MU_FIRST_CLASSROOM_ID"]})
        stat, df_num, p_value = _joint_wald(full, contains=":C(_CAREER)")
        delta = float(full.rsquared - base.rsquared)
        partial = delta / (1.0 - float(base.rsquared)) if base.rsquared < 1 else np.nan
        rows.append({
            "analysis": "first_mu_cmat",
            "test": "career_by_experience_state",
            "n": int(full.nobs),
            "clusters": int(mu_interaction["MU_FIRST_CLASSROOM_ID"].nunique()),
            "career_levels": int(mu_interaction["_CAREER"].nunique()),
            "r2_base": float(base.rsquared),
            "r2_full": float(full.rsquared),
            "delta_r2": delta,
            "partial_r2": partial,
            "wald_stat": stat,
            "wald_df": df_num,
            "p_value": p_value,
        })
    return pd.DataFrame(rows)


def choice_set_audit(
    calc_choices: pd.DataFrame,
    *,
    observed_col: str = "CALC_CHOICE_SET_OBSERVED_N",
    rankable_col: str = "CALC_CHOICE_SET_RANKABLE_N",
    period_col: str = "CALC_FIRST_PERIOD_LABEL",
) -> pd.DataFrame:
    """Audit the observed-period instructor set used as a choice-set proxy.

    Parameters
    ----------
    calc_choices : pandas.DataFrame
        First later-Calculus choices with observed and historically rankable instructor
        counts attached.
    observed_col : str, default="CALC_CHOICE_SET_OBSERVED_N"
        Number of distinct instructors observed teaching the course in the period.
    rankable_col : str, default="CALC_CHOICE_SET_RANKABLE_N"
        Number of those instructors with sufficient strictly-prior outcome history.
    period_col : str, default="CALC_FIRST_PERIOD_LABEL"
        Academic-period label.

    Returns
    -------
    pandas.DataFrame
        Compact audit metrics for set size, historical-rank coverage and rankability.
        These metrics do not establish schedule compatibility, capacity or individual
        feasibility.
    """
    required = {observed_col, rankable_col, period_col, "CALC_CHOSEN_EASINESS_PERCENTILE"}
    missing = required.difference(calc_choices.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    d = calc_choices.copy()
    observed = pd.to_numeric(d[observed_col], errors="coerce")
    rankable = pd.to_numeric(d[rankable_col], errors="coerce")
    d["_HISTORY_COVERAGE"] = rankable / observed.replace(0, np.nan)
    period = d[[period_col, observed_col, rankable_col]].drop_duplicates(period_col).copy()
    period["_HISTORY_COVERAGE"] = (
        pd.to_numeric(period[rankable_col], errors="coerce")
        / pd.to_numeric(period[observed_col], errors="coerce").replace(0, np.nan)
    )
    rows: list[dict[str, object]] = []

    def add(metric: str, value: float | int, level: str) -> None:
        rows.append({"level": level, "metric": metric, "value": value})

    add("n_student_choices", int(len(d)), "student")
    add("chosen_instructor_rankable_share", float(d["CALC_CHOSEN_EASINESS_PERCENTILE"].notna().mean()), "student")
    for threshold in (2, 3, 4, 5):
        add(f"share_with_rankable_instructors_ge_{threshold}", float(rankable.ge(threshold).mean()), "student")
    add("mean_history_coverage", float(d["_HISTORY_COVERAGE"].mean()), "student")

    add("n_periods", int(len(period)), "period")
    for col, label in ((observed_col, "observed_instructors"), (rankable_col, "rankable_instructors")):
        values = pd.to_numeric(period[col], errors="coerce").dropna()
        if len(values):
            add(f"{label}_min", float(values.min()), "period")
            add(f"{label}_p25", float(values.quantile(0.25)), "period")
            add(f"{label}_median", float(values.median()), "period")
            add(f"{label}_p75", float(values.quantile(0.75)), "period")
            add(f"{label}_max", float(values.max()), "period")
    add("mean_history_coverage", float(period["_HISTORY_COVERAGE"].mean()), "period")
    return pd.DataFrame(rows)


def choice_set_sensitivity_models(
    calc_choices: pd.DataFrame,
    *,
    min_career_n: int = 30,
    rankable_thresholds: tuple[int, ...] = (2, 3, 4, 5),
    min_history_coverage: float = 0.75,
) -> pd.DataFrame:
    """Re-estimate experience-state choice associations under stricter set support.

    Parameters
    ----------
    calc_choices : pandas.DataFrame
        First later-Calculus choices with choice-set counts and first-MU experience
        variables.
    min_career_n : int, default=30
        Minimum programme size before rarer programmes are pooled.
    rankable_thresholds : tuple of int, default=(2, 3, 4, 5)
        Minimum number of historically rankable instructors required in successive
        robustness samples.
    min_history_coverage : float, default=0.75
        Additional robustness restriction requiring the historically rankable set to
        cover at least this share of instructors observed teaching in the period.

    Returns
    -------
    pandas.DataFrame
        Cluster-robust experience-state coefficients across choice-set restrictions.
    """
    required = {
        "CALC_CHOSEN_EASINESS_PERCENTILE",
        "CALC_CHOICE_SET_RANKABLE_N",
        "CALC_CHOICE_SET_OBSERVED_N",
        "MU_FIRST_Z",
        "MU_FIRST_LOO_PASS_RATE",
        "MU_FIRST_VISIT_GROUP",
        "MU_FIRST_CAREER",
        "CALC_FIRST_PERIOD_LABEL",
        "MU_FIRST_CLASSROOM_ID",
    }
    missing = required.difference(calc_choices.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    d = calc_choices.copy()
    d["_STATE"] = classify_experience_state(d)
    d = d.loc[d["_STATE"].ne("unknown_context")].copy()
    d["_CAREER"] = _collapse_rare(d["MU_FIRST_CAREER"], min_career_n)
    observed = pd.to_numeric(d["CALC_CHOICE_SET_OBSERVED_N"], errors="coerce")
    rankable = pd.to_numeric(d["CALC_CHOICE_SET_RANKABLE_N"], errors="coerce")
    d["_HISTORY_COVERAGE"] = rankable / observed.replace(0, np.nan)

    specs: list[tuple[str, pd.Series]] = []
    for threshold in rankable_thresholds:
        specs.append((f"rankable_ge_{int(threshold)}", rankable.ge(int(threshold))))
    specs.append((
        f"rankable_ge_2_history_coverage_ge_{min_history_coverage:.2f}",
        rankable.ge(2) & d["_HISTORY_COVERAGE"].ge(float(min_history_coverage)),
    ))

    rows: list[dict[str, object]] = []
    for specification, mask in specs:
        sub = d.loc[mask & d["CALC_CHOSEN_EASINESS_PERCENTILE"].notna()].copy()
        if len(sub) < 50:
            continue
        formula = (
            "CALC_CHOSEN_EASINESS_PERCENTILE ~ "
            "C(_STATE, Treatment(reference='lower_strain')) + "
            "C(MU_FIRST_VISIT_GROUP) + C(_CAREER) + C(CALC_FIRST_PERIOD_LABEL)"
        )
        fit = smf.ols(formula, data=sub).fit(
            cov_type="cluster", cov_kwds={"groups": sub["MU_FIRST_CLASSROOM_ID"]}
        )
        prefix = "C(_STATE, Treatment(reference='lower_strain'))"
        for term in fit.params.index:
            if not term.startswith(prefix):
                continue
            rows.append({
                "specification": specification,
                "term": term,
                "n": int(fit.nobs),
                "clusters": int(sub["MU_FIRST_CLASSROOM_ID"].nunique()),
                "periods": int(sub["CALC_FIRST_PERIOD_LABEL"].nunique()),
                "estimate": float(fit.params[term]),
                "se_cluster": float(fit.bse[term]),
                "p_value": float(fit.pvalues[term]),
                "r2": float(fit.rsquared),
            })
    return pd.DataFrame(rows)


def administrative_choice_constraint_audit(
    academic_df: pd.DataFrame,
    *,
    additional_groups: Mapping[str, tuple[str, ...]] | None = None,
) -> pd.DataFrame:
    """Audit whether administrative fields can refine individual instructor choice sets.

    Parameters
    ----------
    academic_df : pandas.DataFrame
        Cleaned academic-attempt table used by the study pipeline.
    additional_groups : mapping, optional
        Extra audit categories mapping a category name to case-insensitive substrings
        searched in column names.

    Returns
    -------
    pandas.DataFrame
        Schema-only audit showing whether section, schedule, capacity or room fields are
        available to constrain the observed instructor set. Absence means the period-wide
        observed set must be interpreted as a proxy rather than an individual feasible set.
    """
    groups: dict[str, tuple[str, ...]] = {
        "section_identifier": ("NRC", "CRN", "SECTION", "SECCION"),
        "schedule_time": ("HORARIO", "START_TIME", "END_TIME", "MEETING_TIME", "HORA"),
        "capacity": ("CAPACITY", "CUPO", "ENROLLMENT_CAP"),
        "room": ("SALON", "ROOM", "AULA"),
    }
    if additional_groups:
        groups.update({key: tuple(value) for key, value in additional_groups.items()})
    columns = [str(column) for column in academic_df.columns]
    upper = {column: column.upper() for column in columns}
    rows = []
    for category, tokens in groups.items():
        matches = [
            original
            for original, normalized in upper.items()
            if any(token.upper() in normalized for token in tokens)
        ]
        rows.append({
            "constraint_category": category,
            "field_available": bool(matches),
            "matched_fields": ";".join(matches),
        })
    return pd.DataFrame(rows)
