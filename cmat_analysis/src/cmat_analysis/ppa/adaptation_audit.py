"""Audit helpers for observed instructor sets and repeated-attempt context changes."""

from __future__ import annotations

import numpy as np
import pandas as pd

from cmat_analysis.cohorts import normalize_text

from ._progression import classify_revalidation_records


def augment_repeat_transition_context(
    transitions: pd.DataFrame,
    mu_attempts: pd.DataFrame,
) -> pd.DataFrame:
    """Attach absolute strictly-prior instructor outcomes to repeat transitions.

    Parameters
    ----------
    transitions : pandas.DataFrame
        Repeat-transition table from the longitudinal adaptation builder.
    mu_attempts : pandas.DataFrame
        Attempt-level MU table from the same builder, containing strictly-prior
        instructor pass-rate and mean-grade context.

    Returns
    -------
    pandas.DataFrame
        Transition table with previous/next historical pass rates and mean grades plus
        their differences. These absolute differences complement percentile changes
        whose reference set can vary across academic periods.
    """
    required_t = {"STUDENT_ID", "FAILED_ATTEMPT_NUMBER", "NEXT_ATTEMPT_NUMBER"}
    required_m = {
        "STUDENT_ID",
        "MU_ATTEMPT_NUMBER",
        "MU_PROF_PRIOR_PASS_RATE",
        "MU_PROF_PRIOR_MEAN_GRADE",
    }
    missing_t = required_t.difference(transitions.columns)
    missing_m = required_m.difference(mu_attempts.columns)
    if missing_t:
        raise KeyError(f"Missing transition columns: {sorted(missing_t)}")
    if missing_m:
        raise KeyError(f"Missing MU-attempt columns: {sorted(missing_m)}")

    context = mu_attempts[[
        "STUDENT_ID",
        "MU_ATTEMPT_NUMBER",
        "MU_PROF_PRIOR_PASS_RATE",
        "MU_PROF_PRIOR_MEAN_GRADE",
    ]].drop_duplicates(["STUDENT_ID", "MU_ATTEMPT_NUMBER"])
    previous = context.rename(columns={
        "MU_ATTEMPT_NUMBER": "FAILED_ATTEMPT_NUMBER",
        "MU_PROF_PRIOR_PASS_RATE": "PREV_PROF_PRIOR_PASS_RATE",
        "MU_PROF_PRIOR_MEAN_GRADE": "PREV_PROF_PRIOR_MEAN_GRADE",
    })
    nxt = context.rename(columns={
        "MU_ATTEMPT_NUMBER": "NEXT_ATTEMPT_NUMBER",
        "MU_PROF_PRIOR_PASS_RATE": "NEXT_PROF_PRIOR_PASS_RATE",
        "MU_PROF_PRIOR_MEAN_GRADE": "NEXT_PROF_PRIOR_MEAN_GRADE",
    })
    out = transitions.merge(
        previous,
        on=["STUDENT_ID", "FAILED_ATTEMPT_NUMBER"],
        how="left",
        validate="many_to_one",
    ).merge(
        nxt,
        on=["STUDENT_ID", "NEXT_ATTEMPT_NUMBER"],
        how="left",
        validate="many_to_one",
    )
    out["DELTA_PROF_PRIOR_PASS_RATE"] = (
        pd.to_numeric(out["NEXT_PROF_PRIOR_PASS_RATE"], errors="coerce")
        - pd.to_numeric(out["PREV_PROF_PRIOR_PASS_RATE"], errors="coerce")
    )
    out["DELTA_PROF_PRIOR_MEAN_GRADE"] = (
        pd.to_numeric(out["NEXT_PROF_PRIOR_MEAN_GRADE"], errors="coerce")
        - pd.to_numeric(out["PREV_PROF_PRIOR_MEAN_GRADE"], errors="coerce")
    )
    return out


def observed_course_instructor_counts(
    academics: pd.DataFrame,
    *,
    passing_grade: float,
    subject_code: str,
    subject_name: str,
    period_col: str = "PERIOD_INDEX",
    instructor_col: str = "CLAVEPROFESOR",
) -> pd.DataFrame:
    """Count instructors observed teaching a course in each academic period.

    Parameters
    ----------
    academics : pandas.DataFrame
        Cleaned academic-attempt table before course filtering.
    passing_grade : float
        Passing-grade threshold required by the revalidation classifier used to retain
        real academic attempts.
    subject_code : str
        Institutional subject code for the course of interest.
    subject_name : str
        Normalized or raw subject name used as a fallback identifier.
    period_col : str, default="PERIOD_INDEX"
        Academic-period index column.
    instructor_col : str, default="CLAVEPROFESOR"
        Instructor identifier column.

    Returns
    -------
    pandas.DataFrame
        One row per observed academic period with the number of distinct instructors
        represented in real attempts. The count is a period-wide observed set, not an
        individual student's feasible set.
    """
    history = classify_revalidation_records(academics, passing_grade=passing_grade)
    real = history.loc[history["ACADEMIC_EVENT_TYPE"].eq("real_attempt_candidate")].copy()
    mask = real["SUBJECT_CODE"].astype(str).str.upper().eq(str(subject_code).upper()) | real[
        "SUBJECT"
    ].eq(normalize_text(subject_name))
    course = real.loc[mask].dropna(subset=[period_col, instructor_col]).copy()
    if course.empty:
        return pd.DataFrame(columns=[period_col, "OBSERVED_INSTRUCTOR_N"])
    return (
        course.groupby(period_col, dropna=False)[instructor_col]
        .nunique()
        .rename("OBSERVED_INSTRUCTOR_N")
        .reset_index()
        .sort_values(period_col)
        .reset_index(drop=True)
    )


def attach_observed_choice_set_size(
    choices: pd.DataFrame,
    period_counts: pd.DataFrame,
    *,
    choice_period_col: str = "CALC_FIRST_PERIOD_INDEX",
    count_period_col: str = "PERIOD_INDEX",
    output_col: str = "CALC_CHOICE_SET_OBSERVED_N",
) -> pd.DataFrame:
    """Attach period-wide observed instructor counts to student choices.

    Parameters
    ----------
    choices : pandas.DataFrame
        Student-level instructor-choice table.
    period_counts : pandas.DataFrame
        Output from :func:`observed_course_instructor_counts`.
    choice_period_col : str, default="CALC_FIRST_PERIOD_INDEX"
        Period column in the student-level choices.
    count_period_col : str, default="PERIOD_INDEX"
        Period column in the counts table.
    output_col : str, default="CALC_CHOICE_SET_OBSERVED_N"
        Name assigned to the attached count.

    Returns
    -------
    pandas.DataFrame
        Copy of ``choices`` with the observed period-wide instructor count attached.
    """
    required_choices = {choice_period_col}
    required_counts = {count_period_col, "OBSERVED_INSTRUCTOR_N"}
    missing_choices = required_choices.difference(choices.columns)
    missing_counts = required_counts.difference(period_counts.columns)
    if missing_choices:
        raise KeyError(f"Missing choice columns: {sorted(missing_choices)}")
    if missing_counts:
        raise KeyError(f"Missing count columns: {sorted(missing_counts)}")
    counts = period_counts.rename(columns={
        count_period_col: choice_period_col,
        "OBSERVED_INSTRUCTOR_N": output_col,
    })[[choice_period_col, output_col]].drop_duplicates(choice_period_col)
    out = choices.merge(counts, on=choice_period_col, how="left", validate="many_to_one")
    out[output_col] = pd.to_numeric(out[output_col], errors="coerce")
    return out
