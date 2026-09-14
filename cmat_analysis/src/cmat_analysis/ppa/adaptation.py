"""Longitudinal academic-adaptation traces from MU to Calculus I.

The functions in this module operationalize observable administrative traces related
to academic engagement without treating them as direct measurements of the latent
engagement construct. They distinguish prior performance, classroom outcome context,
CMAT response, instructor context, later instructor selection, and repeated MU
attempts. All resulting quantities are observational.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from cmat_analysis.cohorts import attach_visits, normalize_text, visit_group

from ._progression import _numeric_classroom_reference_z, classify_revalidation_records
from .context import build_mu_classroom_outcome_context
from .encouragement import _collapse_rare_categories


@dataclass(frozen=True)
class EngagementTrajectoryData:
    """Container for MU experience, Calculus choice, and repeat-attempt traces.

    Parameters
    ----------
    mu_attempts : pandas.DataFrame
        Attempt-level real MU history with classroom, CMAT, and prior-instructor context.
    mu_students : pandas.DataFrame
        One row per student summarizing the first MU experience and attempts to first pass.
    calc_choices : pandas.DataFrame
        First observed Calculus attempt after the first MU pass, with historical choice-set ranks.
    repeat_transitions : pandas.DataFrame
        Consecutive MU transitions following a failed/adverse attempt.

    Notes
    -----
    These tables contain observable administrative traces. They do not identify a
    psychological engagement state, causal professor difficulty, or causal instructor choice.
    """

    mu_attempts: pd.DataFrame
    mu_students: pd.DataFrame
    calc_choices: pd.DataFrame
    repeat_transitions: pd.DataFrame


def strict_prior_instructor_context(
    df: pd.DataFrame,
    *,
    instructor_col: str,
    period_index_col: str,
    grade_col: str,
    pass_col: str,
    min_history_n: int = 20,
    prefix: str = "PRIOR_INSTRUCTOR",
) -> pd.DataFrame:
    """Attach instructor outcomes based only on strictly earlier academic periods.

    Parameters
    ----------
    df : pandas.DataFrame
        Attempt-level table containing instructor, period index, numeric grade, and pass flag.
    instructor_col : str
        Instructor identifier column.
    period_index_col : str
        Ordered academic-period index.
    grade_col : str
        Numeric grade column; nonnumeric outcomes should be missing.
    pass_col : str
        Binary pass indicator defined for all real attempt rows.
    min_history_n : int, default=20
        Minimum number of prior attempts required before pass-rate context is reported;
        the same minimum is applied to prior numeric grades for the mean-grade context.
    prefix : str, default="PRIOR_INSTRUCTOR"
        Prefix for generated historical-context columns.

    Returns
    -------
    pandas.DataFrame
        Copy of ``df`` with strictly-prior attempt counts, pass rate, mean numeric grade,
        and standardized versions of the two academic-context measures.
    """
    required = {instructor_col, period_index_col, grade_col, pass_col}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")

    out = df.copy()
    work = out[[instructor_col, period_index_col, grade_col, pass_col]].dropna(
        subset=[instructor_col, period_index_col, pass_col]
    ).copy()
    work[pass_col] = pd.to_numeric(work[pass_col], errors="coerce")
    work[grade_col] = pd.to_numeric(work[grade_col], errors="coerce")
    if work[pass_col].isna().any() or not set(work[pass_col].unique()).issubset({0, 1}):
        raise ValueError(f"{pass_col} must contain only binary 0/1 values.")
    work["_GRADE_PRESENT"] = work[grade_col].notna().astype(int)
    work["_GRADE_VALUE"] = work[grade_col].fillna(0.0)

    cells = (
        work.groupby([instructor_col, period_index_col], dropna=False)
        .agg(
            _pass_sum=(pass_col, "sum"),
            _attempt_n=(pass_col, "size"),
            _grade_sum=("_GRADE_VALUE", "sum"),
            _grade_n=("_GRADE_PRESENT", "sum"),
        )
        .reset_index()
        .sort_values([instructor_col, period_index_col], kind="stable")
    )
    for source, target in (
        ("_pass_sum", "_prior_pass_sum"),
        ("_attempt_n", "_prior_attempt_n"),
        ("_grade_sum", "_prior_grade_sum"),
        ("_grade_n", "_prior_grade_n"),
    ):
        cells[target] = cells.groupby(instructor_col, dropna=False)[source].cumsum() - cells[source]

    attempt_n_col = f"{prefix}_ATTEMPT_N"
    grade_n_col = f"{prefix}_GRADE_N"
    pass_rate_col = f"{prefix}_PASS_RATE"
    mean_grade_col = f"{prefix}_MEAN_GRADE"
    pass_z_col = f"{prefix}_PASS_Z"
    grade_z_col = f"{prefix}_GRADE_Z"
    cells[attempt_n_col] = cells["_prior_attempt_n"].astype(int)
    cells[grade_n_col] = cells["_prior_grade_n"].astype(int)
    cells[pass_rate_col] = np.where(
        cells["_prior_attempt_n"] >= int(min_history_n),
        cells["_prior_pass_sum"] / cells["_prior_attempt_n"],
        np.nan,
    )
    cells[mean_grade_col] = np.where(
        cells["_prior_grade_n"] >= int(min_history_n),
        cells["_prior_grade_sum"] / cells["_prior_grade_n"],
        np.nan,
    )
    attach = cells[[
        instructor_col,
        period_index_col,
        attempt_n_col,
        grade_n_col,
        pass_rate_col,
        mean_grade_col,
    ]]
    out = out.merge(attach, on=[instructor_col, period_index_col], how="left")
    for source, target in ((pass_rate_col, pass_z_col), (mean_grade_col, grade_z_col)):
        values = pd.to_numeric(out[source], errors="coerce")
        mean = float(values.mean()) if values.notna().any() else np.nan
        sd = float(values.std(ddof=0)) if values.notna().any() else np.nan
        out[target] = (values - mean) / sd if np.isfinite(sd) and sd > 0 else np.nan
    return out


def instructor_choice_percentiles(
    df: pd.DataFrame,
    *,
    instructor_col: str,
    period_index_col: str,
    pass_rate_col: str,
    mean_grade_col: str,
    prefix: str = "CHOICE",
) -> pd.DataFrame:
    """Rank historically observed instructor outcomes within each offered-period choice set.

    Parameters
    ----------
    df : pandas.DataFrame
        Attempt-level course table in which observed instructors define the set offered
        in each academic period and historical context has already been attached.
    instructor_col : str
        Instructor identifier column.
    period_index_col : str
        Academic-period index.
    pass_rate_col : str
        Strictly-prior instructor pass-rate column; higher values indicate historically
        higher observed pass rates.
    mean_grade_col : str
        Strictly-prior instructor mean-grade column; higher values indicate historically
        higher observed mean grades.
    prefix : str, default="CHOICE"
        Prefix for generated rank and choice-set columns.

    Returns
    -------
    pandas.DataFrame
        Copy of ``df`` with within-period pass-rate and mean-grade percentiles, their
        transparent equal-weight composite, and the number of historically rankable
        instructors in the observed period.
    """
    required = {instructor_col, period_index_col, pass_rate_col, mean_grade_col}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    out = df.copy()
    offers = out[[instructor_col, period_index_col, pass_rate_col, mean_grade_col]].drop_duplicates(
        [instructor_col, period_index_col]
    )
    pass_rank_col = f"{prefix}_PASS_PERCENTILE"
    grade_rank_col = f"{prefix}_GRADE_PERCENTILE"
    composite_col = f"{prefix}_EASINESS_PERCENTILE"
    eligible_col = f"{prefix}_ELIGIBLE_INSTRUCTORS"
    offers[pass_rank_col] = offers.groupby(period_index_col)[pass_rate_col].rank(
        method="average", pct=True
    )
    offers[grade_rank_col] = offers.groupby(period_index_col)[mean_grade_col].rank(
        method="average", pct=True
    )
    offers[composite_col] = offers[[pass_rank_col, grade_rank_col]].mean(axis=1, skipna=False)
    offers[eligible_col] = offers.groupby(period_index_col)[composite_col].transform("count").astype(int)
    offers.loc[offers[eligible_col].lt(2), [pass_rank_col, grade_rank_col, composite_col]] = np.nan
    return out.merge(
        offers[[
            instructor_col,
            period_index_col,
            pass_rank_col,
            grade_rank_col,
            composite_col,
            eligible_col,
        ]],
        on=[instructor_col, period_index_col],
        how="left",
    )


def _performance_band(z: float) -> str:
    if pd.isna(z):
        return "nonnumeric_or_unstandardized"
    if float(z) <= -0.5:
        return "low_relative"
    if float(z) >= 0.5:
        return "high_relative"
    return "middle_relative"


def _difficulty_band(pass_rate: float, low_cut: float, high_cut: float) -> str:
    if pd.isna(pass_rate):
        return "unknown_context"
    if float(pass_rate) <= low_cut:
        return "high_difficulty_context"
    if float(pass_rate) >= high_cut:
        return "low_difficulty_context"
    return "middle_difficulty_context"


def build_engagement_trajectory_data(
    data,
    config,
    *,
    min_history_n: int = 20,
) -> EngagementTrajectoryData:
    """Build MU experience, repeat-attempt, and later Calculus instructor-choice traces.

    Parameters
    ----------
    data : object
        Normalized ``StudyData`` containing academic attempts and CMAT advisory events.
    config : object
        Study configuration supplying MU/Calculus subject definitions, passing grade,
        PPA visit threshold, and minimum classroom size.
    min_history_n : int, default=20
        Minimum strictly-prior attempt count before an instructor historical outcome is
        used to construct within-period instructor-choice percentiles.

    Returns
    -------
    EngagementTrajectoryData
        Attempt-level MU history, student-level MU summaries, first later-Calculus
        choices after first MU pass, and consecutive transitions following MU failure.

    Notes
    -----
    The observed set of instructors teaching a course in a period is only an
    approximation to each student's feasible choice set; schedules, capacity, and
    registration restrictions are not observed. Higher choice percentiles mean higher
    historical pass rates/mean grades, not intrinsic instructor easiness.
    """
    history = classify_revalidation_records(data.academics, passing_grade=config.passing_grade)
    real = history.loc[history["ACADEMIC_EVENT_TYPE"].eq("real_attempt_candidate")].copy()

    def subject_mask(frame: pd.DataFrame, code: str, name: str) -> pd.Series:
        return frame["SUBJECT_CODE"].astype(str).str.upper().eq(str(code).upper()) | frame[
            "SUBJECT"
        ].eq(normalize_text(name))

    mu = real.loc[subject_mask(real, config.primary_subject_code, config.primary_subject_name)].copy()
    mu = mu.sort_values(["STUDENT_ID", "PERIOD_INDEX", "SOURCE_ROW"], kind="stable")
    mu["MU_ATTEMPT_NUMBER"] = mu.groupby("STUDENT_ID").cumcount() + 1
    mu["MU_ATTEMPT_PASS"] = (
        mu["GRADE_CLASS"].eq("numeric") & mu["GRADE_NUMERIC"].ge(float(config.passing_grade))
    ).astype(int)
    mu = attach_visits(mu, data.advisories, threshold=config.ppa_threshold)
    mu_context = build_mu_classroom_outcome_context(data, config)
    context_cols = [
        "SOURCE_ROW",
        "MU_CONTEXT_CLASSROOM_ID",
        "MU_CLASSROOM_ATTEMPT_N",
        "MU_CLASSROOM_MEAN_GRADE",
        "MU_CLASSROOM_PASS_RATE",
        "MU_LOO_CLASSROOM_MEAN_GRADE",
        "MU_LOO_CLASSROOM_PASS_RATE",
    ]
    mu = mu.merge(mu_context[context_cols], on="SOURCE_ROW", how="left", validate="one_to_one")
    mu_z = _numeric_classroom_reference_z(
        history,
        code=config.primary_subject_code,
        name=config.primary_subject_name,
        min_classroom_n=config.min_classroom_n_for_z,
    ).rename(columns={"Z_CLASSROOM_NUMERIC": "MU_ATTEMPT_Z"})
    mu = mu.merge(mu_z[["SOURCE_ROW", "MU_ATTEMPT_Z"]], on="SOURCE_ROW", how="left")
    mu = strict_prior_instructor_context(
        mu,
        instructor_col="CLAVEPROFESOR",
        period_index_col="PERIOD_INDEX",
        grade_col="GRADE_NUMERIC",
        pass_col="MU_ATTEMPT_PASS",
        min_history_n=min_history_n,
        prefix="MU_PROF_PRIOR",
    )
    mu = instructor_choice_percentiles(
        mu,
        instructor_col="CLAVEPROFESOR",
        period_index_col="PERIOD_INDEX",
        pass_rate_col="MU_PROF_PRIOR_PASS_RATE",
        mean_grade_col="MU_PROF_PRIOR_MEAN_GRADE",
        prefix="MU_OFFER",
    )

    first = mu.drop_duplicates("STUDENT_ID", keep="first").copy()
    pass_rows = mu.loc[mu["MU_ATTEMPT_PASS"].eq(1)].drop_duplicates("STUDENT_ID", keep="first").copy()
    first_pass_n = pass_rows.set_index("STUDENT_ID")["MU_ATTEMPT_NUMBER"]
    mu["FIRST_PASS_ATTEMPT_NUMBER"] = mu["STUDENT_ID"].map(first_pass_n)
    mu["THROUGH_FIRST_PASS"] = mu["FIRST_PASS_ATTEMPT_NUMBER"].isna() | mu["MU_ATTEMPT_NUMBER"].le(
        mu["FIRST_PASS_ATTEMPT_NUMBER"]
    )
    active = mu.loc[mu["THROUGH_FIRST_PASS"]].copy()
    aggregate = active.groupby("STUDENT_ID").agg(
        MU_ATTEMPTS_OBSERVED=("MU_ATTEMPT_NUMBER", "max"),
        MU_CUMULATIVE_CMAT_VISITS=("VISITS_CMAT_PERIOD", "sum"),
        MU_ATTEMPT_PERIODS_WITH_CMAT=("VISITS_CMAT_PERIOD", lambda s: int((s > 0).sum())),
        MU_DISTINCT_PROFESSORS=("CLAVEPROFESOR", "nunique"),
    )
    first = first.set_index("STUDENT_ID").join(aggregate).reset_index()
    first["MU_FIRST_PASS_ATTEMPT"] = first["STUDENT_ID"].map(first_pass_n)
    first["MU_EVER_PASSED"] = first["MU_FIRST_PASS_ATTEMPT"].notna().astype(int)
    first["MU_ATTEMPT_OUTCOME_PROFILE"] = np.select(
        [
            first["MU_FIRST_PASS_ATTEMPT"].eq(1),
            first["MU_FIRST_PASS_ATTEMPT"].eq(2),
            first["MU_FIRST_PASS_ATTEMPT"].ge(3),
        ],
        ["pass_first", "pass_second", "pass_third_or_later"],
        default="no_observed_pass",
    )
    first["MU_FIRST_VISIT_GROUP"] = first["VISITS_CMAT_PERIOD"].map(
        lambda value: visit_group(value, config.ppa_threshold)
    )
    first["MU_FIRST_PERFORMANCE_BAND"] = first["MU_ATTEMPT_Z"].map(_performance_band)
    valid_pass_rates = pd.to_numeric(first["MU_LOO_CLASSROOM_PASS_RATE"], errors="coerce").dropna()
    low_cut = float(valid_pass_rates.quantile(0.25)) if len(valid_pass_rates) else np.nan
    high_cut = float(valid_pass_rates.quantile(0.75)) if len(valid_pass_rates) else np.nan
    first["MU_FIRST_DIFFICULTY_BAND"] = [
        _difficulty_band(value, low_cut, high_cut)
        if np.isfinite(low_cut) and np.isfinite(high_cut)
        else "unknown_context"
        for value in first["MU_LOO_CLASSROOM_PASS_RATE"]
    ]
    first["MU_EXPERIENCE_PROFILE"] = (
        first["MU_FIRST_PERFORMANCE_BAND"].astype(str)
        + " | "
        + first["MU_FIRST_DIFFICULTY_BAND"].astype(str)
        + " | CMAT "
        + first["MU_FIRST_VISIT_GROUP"].astype(str)
    )
    first = first.rename(columns={
        "SOURCE_ROW": "MU_FIRST_SOURCE_ROW",
        "PERIOD_INDEX": "MU_FIRST_PERIOD_INDEX",
        "PERIOD_LABEL": "MU_FIRST_PERIOD_LABEL",
        "OFFICIAL_CAREER": "MU_FIRST_CAREER",
        "CLAVEPROFESOR": "MU_FIRST_PROFESSOR",
        "GRADE_NUMERIC": "MU_FIRST_GRADE",
        "MU_ATTEMPT_Z": "MU_FIRST_Z",
        "MU_LOO_CLASSROOM_PASS_RATE": "MU_FIRST_LOO_PASS_RATE",
        "MU_LOO_CLASSROOM_MEAN_GRADE": "MU_FIRST_LOO_MEAN_GRADE",
        "MU_CONTEXT_CLASSROOM_ID": "MU_FIRST_CLASSROOM_ID",
        "VISITS_CMAT_PERIOD": "MU_FIRST_CMAT_VISITS",
        "MU_OFFER_EASINESS_PERCENTILE": "MU_FIRST_PROFESSOR_EASINESS_PERCENTILE",
    })

    calc = real.loc[subject_mask(real, config.followup_subject_code, config.followup_subject_name)].copy()
    calc = calc.sort_values(["STUDENT_ID", "PERIOD_INDEX", "SOURCE_ROW"], kind="stable")
    calc["CALC_ATTEMPT_PASS"] = (
        calc["GRADE_CLASS"].eq("numeric") & calc["GRADE_NUMERIC"].ge(float(config.passing_grade))
    ).astype(int)
    calc = attach_visits(calc, data.advisories, threshold=config.ppa_threshold)
    calc = strict_prior_instructor_context(
        calc,
        instructor_col="CLAVEPROFESOR",
        period_index_col="PERIOD_INDEX",
        grade_col="GRADE_NUMERIC",
        pass_col="CALC_ATTEMPT_PASS",
        min_history_n=min_history_n,
        prefix="CALC_PROF_PRIOR",
    )
    calc = instructor_choice_percentiles(
        calc,
        instructor_col="CLAVEPROFESOR",
        period_index_col="PERIOD_INDEX",
        pass_rate_col="CALC_PROF_PRIOR_PASS_RATE",
        mean_grade_col="CALC_PROF_PRIOR_MEAN_GRADE",
        prefix="CALC_CHOICE",
    )
    pass_key = pass_rows[["STUDENT_ID", "PERIOD_INDEX"]].rename(
        columns={"PERIOD_INDEX": "MU_PASS_PERIOD_INDEX"}
    )
    calc_after = calc.merge(pass_key, on="STUDENT_ID", how="inner")
    calc_after = calc_after.loc[calc_after["PERIOD_INDEX"].gt(calc_after["MU_PASS_PERIOD_INDEX"])].copy()
    calc_first = calc_after.drop_duplicates("STUDENT_ID", keep="first").copy()
    calc_first = calc_first.rename(columns={
        "SOURCE_ROW": "CALC_FIRST_SOURCE_ROW",
        "PERIOD_INDEX": "CALC_FIRST_PERIOD_INDEX",
        "PERIOD_LABEL": "CALC_FIRST_PERIOD_LABEL",
        "CLAVEPROFESOR": "CALC_FIRST_PROFESSOR",
        "GRADE_NUMERIC": "CALC_FIRST_GRADE",
        "VISITS_CMAT_PERIOD": "CALC_FIRST_CMAT_VISITS",
        "CALC_CHOICE_EASINESS_PERCENTILE": "CALC_CHOSEN_EASINESS_PERCENTILE",
        "CALC_CHOICE_PASS_PERCENTILE": "CALC_CHOSEN_PASS_PERCENTILE",
        "CALC_CHOICE_GRADE_PERCENTILE": "CALC_CHOSEN_GRADE_PERCENTILE",
        "CALC_CHOICE_ELIGIBLE_INSTRUCTORS": "CALC_CHOICE_SET_RANKABLE_N",
    })
    calc_first["CALC_FIRST_ANY_CMAT"] = (calc_first["CALC_FIRST_CMAT_VISITS"] > 0).astype(int)
    student_cols = [
        "STUDENT_ID",
        "MU_FIRST_PERIOD_INDEX",
        "MU_FIRST_PERIOD_LABEL",
        "MU_FIRST_CAREER",
        "MU_FIRST_PROFESSOR",
        "MU_FIRST_CLASSROOM_ID",
        "MU_FIRST_GRADE",
        "MU_FIRST_Z",
        "MU_FIRST_LOO_PASS_RATE",
        "MU_FIRST_LOO_MEAN_GRADE",
        "MU_FIRST_CMAT_VISITS",
        "MU_FIRST_VISIT_GROUP",
        "MU_FIRST_PERFORMANCE_BAND",
        "MU_FIRST_DIFFICULTY_BAND",
        "MU_EXPERIENCE_PROFILE",
        "MU_FIRST_PASS_ATTEMPT",
        "MU_ATTEMPT_OUTCOME_PROFILE",
        "MU_CUMULATIVE_CMAT_VISITS",
        "MU_ATTEMPT_PERIODS_WITH_CMAT",
    ]
    calc_first = calc_first.merge(first[student_cols], on="STUDENT_ID", how="left", validate="one_to_one")

    transition_rows: list[dict[str, object]] = []
    for _, student_attempts in mu.groupby("STUDENT_ID", sort=False):
        student_attempts = student_attempts.sort_values(["MU_ATTEMPT_NUMBER", "PERIOD_INDEX"], kind="stable")
        records = student_attempts.to_dict("records")
        for previous, nxt in zip(records[:-1], records[1:]):
            if int(previous["MU_ATTEMPT_PASS"]) == 1:
                break
            transition_rows.append({
                "STUDENT_ID": previous["STUDENT_ID"],
                "FAILED_ATTEMPT_NUMBER": int(previous["MU_ATTEMPT_NUMBER"]),
                "NEXT_ATTEMPT_NUMBER": int(nxt["MU_ATTEMPT_NUMBER"]),
                "PREV_PERIOD_INDEX": previous["PERIOD_INDEX"],
                "NEXT_PERIOD_INDEX": nxt["PERIOD_INDEX"],
                "PREV_PROFESSOR": previous["CLAVEPROFESOR"],
                "NEXT_PROFESSOR": nxt["CLAVEPROFESOR"],
                "CHANGED_PROFESSOR": int(previous["CLAVEPROFESOR"] != nxt["CLAVEPROFESOR"]),
                "PREV_GRADE": previous["GRADE_NUMERIC"],
                "NEXT_GRADE": nxt["GRADE_NUMERIC"],
                "PREV_Z": previous["MU_ATTEMPT_Z"],
                "NEXT_Z": nxt["MU_ATTEMPT_Z"],
                "PREV_CMAT_VISITS": int(previous["VISITS_CMAT_PERIOD"]),
                "NEXT_CMAT_VISITS": int(nxt["VISITS_CMAT_PERIOD"]),
                "DELTA_CMAT_VISITS": int(nxt["VISITS_CMAT_PERIOD"] - previous["VISITS_CMAT_PERIOD"]),
                "PREV_ANY_CMAT": int(previous["VISITS_CMAT_PERIOD"] > 0),
                "NEXT_ANY_CMAT": int(nxt["VISITS_CMAT_PERIOD"] > 0),
                "NEXT_ATTEMPT_PASS": int(nxt["MU_ATTEMPT_PASS"]),
                "PREV_PROF_EASINESS_PERCENTILE": previous.get("MU_OFFER_EASINESS_PERCENTILE", np.nan),
                "NEXT_PROF_EASINESS_PERCENTILE": nxt.get("MU_OFFER_EASINESS_PERCENTILE", np.nan),
                "DELTA_PROF_EASINESS_PERCENTILE": (
                    nxt.get("MU_OFFER_EASINESS_PERCENTILE", np.nan)
                    - previous.get("MU_OFFER_EASINESS_PERCENTILE", np.nan)
                ),
                "CAREER": previous["OFFICIAL_CAREER"],
            })
    repeat_transitions = pd.DataFrame(transition_rows)
    return EngagementTrajectoryData(
        mu_attempts=mu.reset_index(drop=True),
        mu_students=first.reset_index(drop=True),
        calc_choices=calc_first.reset_index(drop=True),
        repeat_transitions=repeat_transitions.reset_index(drop=True),
    )


def experience_profile_summary(
    df: pd.DataFrame,
    *,
    profile_col: str = "MU_EXPERIENCE_PROFILE",
    min_n: int = 20,
) -> pd.DataFrame:
    """Summarize parsimonious first-MU experience profiles and later adaptation traces.

    Parameters
    ----------
    df : pandas.DataFrame
        Student-level table, preferably the Calculus-choice table returned by
        :func:`build_engagement_trajectory_data`, containing an MU experience profile.
    profile_col : str, default="MU_EXPERIENCE_PROFILE"
        Column identifying the performance × difficulty-context × CMAT-response profile.
    min_n : int, default=20
        Minimum profile size retained in the aggregate output.

    Returns
    -------
    pandas.DataFrame
        Profile sizes and, when present, later CMAT-use and chosen-instructor-easiness summaries.
    """
    if profile_col not in df.columns:
        raise KeyError(f"Missing required column: {profile_col}")
    rows: list[dict[str, object]] = []
    for profile, sub in df.groupby(profile_col, dropna=False):
        if len(sub) < int(min_n):
            continue
        row: dict[str, object] = {"profile": profile, "n": int(len(sub))}
        for column in (
            "MU_FIRST_Z",
            "MU_FIRST_LOO_PASS_RATE",
            "MU_FIRST_CMAT_VISITS",
            "CALC_CHOSEN_EASINESS_PERCENTILE",
            "CALC_FIRST_ANY_CMAT",
        ):
            if column in sub.columns:
                row[f"mean_{column.lower()}"] = float(pd.to_numeric(sub[column], errors="coerce").mean())
        if "MU_FIRST_CAREER" in sub.columns:
            mode = sub["MU_FIRST_CAREER"].dropna().mode()
            row["modal_career"] = mode.iloc[0] if len(mode) else np.nan
        rows.append(row)
    return pd.DataFrame(rows).sort_values("n", ascending=False).reset_index(drop=True)


def calc_choice_association_models(
    df: pd.DataFrame,
    *,
    outcome_col: str = "CALC_CHOSEN_EASINESS_PERCENTILE",
    career_col: str = "MU_FIRST_CAREER",
    calc_period_col: str = "CALC_FIRST_PERIOD_LABEL",
    cluster_col: str = "MU_FIRST_CLASSROOM_ID",
    min_career_n: int = 30,
) -> pd.DataFrame:
    """Estimate how prior MU experience is associated with later instructor-context choice.

    Parameters
    ----------
    df : pandas.DataFrame
        Calculus-choice table from :func:`build_engagement_trajectory_data`.
    outcome_col : str, default="CALC_CHOSEN_EASINESS_PERCENTILE"
        Within-period historical-outcome percentile of the chosen Calculus instructor.
    career_col : str, default="MU_FIRST_CAREER"
        Degree-programme control.
    calc_period_col : str, default="CALC_FIRST_PERIOD_LABEL"
        Calculus-period control.
    cluster_col : str, default="MU_FIRST_CLASSROOM_ID"
        Cluster used for robust covariance, typically the assigned first-MU classroom.
    min_career_n : int, default=30
        Minimum degree-programme size before smaller programmes are pooled.

    Returns
    -------
    pandas.DataFrame
        Coefficients for pre-specified prior-experience predictors from separate and
        joint linear models with period and degree-programme adjustment.

    Notes
    -----
    The outcome describes the historical academic outcomes of the chosen instructor
    relative to instructors observed teaching that period. It is not a causal measure
    of intrinsic instructor ease, and the observed instructor set may overstate the
    student's feasible schedule-compatible choice set.
    """
    required = {
        outcome_col,
        career_col,
        calc_period_col,
        cluster_col,
        "MU_FIRST_Z",
        "MU_FIRST_LOO_PASS_RATE",
        "MU_FIRST_VISIT_GROUP",
        "MU_ATTEMPT_OUTCOME_PROFILE",
    }
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    d = df[list(required)].dropna(subset=[outcome_col, career_col, calc_period_col, cluster_col]).copy()
    d[career_col] = _collapse_rare_categories(d[career_col], min_career_n)
    for source, target in (("MU_FIRST_Z", "_MU_Z"), ("MU_FIRST_LOO_PASS_RATE", "_MU_PASS_CONTEXT")):
        values = pd.to_numeric(d[source], errors="coerce")
        sd = float(values.std(ddof=0))
        d[target] = (values - values.mean()) / sd if np.isfinite(sd) and sd > 0 else np.nan
    base = f"C({calc_period_col}) + C({career_col})"
    specs = {
        "performance": f"_MU_Z + {base}",
        "classroom_context": f"_MU_PASS_CONTEXT + {base}",
        "cmat_response": f"C(MU_FIRST_VISIT_GROUP) + {base}",
        "attempt_history": f"C(MU_ATTEMPT_OUTCOME_PROFILE) + {base}",
        "joint": (
            f"_MU_Z + _MU_PASS_CONTEXT + C(MU_FIRST_VISIT_GROUP) + "
            f"C(MU_ATTEMPT_OUTCOME_PROFILE) + {base}"
        ),
    }
    rows: list[dict[str, object]] = []
    for specification, rhs in specs.items():
        model_data = d.dropna(subset=["_MU_Z", "_MU_PASS_CONTEXT"]) if specification == "joint" else d
        fit = smf.ols(f"{outcome_col} ~ {rhs}", data=model_data).fit(
            cov_type="cluster", cov_kwds={"groups": model_data[cluster_col]}
        )
        for term, estimate in fit.params.items():
            if term == "Intercept" or term.startswith(f"C({calc_period_col})") or term.startswith(f"C({career_col})"):
                continue
            rows.append({
                "specification": specification,
                "term": term,
                "n": int(fit.nobs),
                "clusters": int(model_data[cluster_col].nunique()),
                "estimate": float(estimate),
                "se_cluster": float(fit.bse[term]),
                "p_value": float(fit.pvalues[term]),
                "r2": float(fit.rsquared),
            })
    return pd.DataFrame(rows)


def repeat_attempt_summary(
    transitions: pd.DataFrame,
) -> pd.DataFrame:
    """Summarize behavioral and instructor-context changes after failed MU attempts.

    Parameters
    ----------
    transitions : pandas.DataFrame
        Repeat-transition table returned by :func:`build_engagement_trajectory_data`.

    Returns
    -------
    pandas.DataFrame
        Aggregate transition statistics by failed-attempt number, including professor
        switching, CMAT change, next-attempt pass rate, and historical-context shift.
    """
    required = {
        "FAILED_ATTEMPT_NUMBER",
        "CHANGED_PROFESSOR",
        "PREV_ANY_CMAT",
        "NEXT_ANY_CMAT",
        "DELTA_CMAT_VISITS",
        "NEXT_ATTEMPT_PASS",
        "DELTA_PROF_EASINESS_PERCENTILE",
    }
    missing = required.difference(transitions.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")
    rows: list[dict[str, object]] = []
    for attempt, sub in transitions.groupby("FAILED_ATTEMPT_NUMBER"):
        delta = pd.to_numeric(sub["DELTA_PROF_EASINESS_PERCENTILE"], errors="coerce")
        rows.append({
            "failed_attempt_number": int(attempt),
            "n_transitions": int(len(sub)),
            "professor_change_rate": float(sub["CHANGED_PROFESSOR"].mean()),
            "prev_cmat_use_rate": float(sub["PREV_ANY_CMAT"].mean()),
            "next_cmat_use_rate": float(sub["NEXT_ANY_CMAT"].mean()),
            "mean_delta_cmat_visits": float(sub["DELTA_CMAT_VISITS"].mean()),
            "next_attempt_pass_rate": float(sub["NEXT_ATTEMPT_PASS"].mean()),
            "n_with_easiness_delta": int(delta.notna().sum()),
            "mean_delta_prof_easiness_percentile": float(delta.mean()),
            "share_switching_to_higher_easiness_percentile": float((delta > 0).mean()) if delta.notna().any() else np.nan,
        })
    return pd.DataFrame(rows).sort_values("failed_attempt_number").reset_index(drop=True)
