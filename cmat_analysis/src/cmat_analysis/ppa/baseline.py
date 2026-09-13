"""Baseline MU cohorts used by PPA participation analyses."""

from __future__ import annotations

import pandas as pd

from cmat_analysis.cohorts import attach_visits, normalize_text, visit_group

from ._progression import classify_revalidation_records


GROUP_ORDER = ["0", "1-2", "3", "4+"]


def build_ppa_mu_baseline_cohort(data, config) -> pd.DataFrame:
    """Build the pre-progression MU cohort for PPA participation analyses.

    The cohort contains each student's first observed real-attempt candidate in
    Matemáticas Universitarias when that attempt has a numeric passing grade and
    occurs in an academic period with observable CMAT registration coverage.
    Unlike the MU-to-Calculus progression cohort, this baseline does not
    condition on subsequently reaching Calculus, which avoids selecting the
    sample on later academic progression when studying initial CMAT uptake.

    Parameters
    ----------
    data : object
        Normalized ``StudyData`` object containing academic and CMAT advisory
        records.
    config : object
        Study configuration supplying MU subject definitions, passing grade,
        PPA threshold, and coverage conventions.

    Returns
    -------
    pandas.DataFrame
        One row per eligible MU student with standardized MU professor, period,
        career, visit-count, and 0/1-2/3/4+ group fields.
    """
    history = classify_revalidation_records(
        data.academics, passing_grade=config.passing_grade
    )
    coverage = set(
        zip(
            data.data_quality["coverage"]["YEAR"].astype(int),
            data.data_quality["coverage"]["SESSION"],
        )
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
    mu = real.loc[subject].copy()
    mu = mu.sort_values(
        ["STUDENT_ID", "PERIOD_INDEX", "SOURCE_ROW"], kind="stable"
    )
    mu = mu.drop_duplicates("STUDENT_ID", keep="first").copy()
    mu = mu.loc[
        mu["GRADE_CLASS"].eq("numeric")
        & mu["GRADE_NUMERIC"].ge(config.passing_grade)
    ].copy()
    mu = attach_visits(mu, data.advisories, threshold=config.ppa_threshold)
    mu["VISIT_COVERAGE"] = [
        (int(year), session) in coverage
        for year, session in zip(mu["YEAR"], mu["SESSION"])
    ]
    mu = mu.loc[mu["VISIT_COVERAGE"]].copy().reset_index(drop=True)
    mu["MU_VISIT_GROUP"] = pd.Categorical(
        mu["VISITS_CMAT_PERIOD"].map(
            lambda value: visit_group(value, config.ppa_threshold)
        ),
        categories=GROUP_ORDER,
        ordered=True,
    )
    mu["MU_ANY_VISIT"] = (mu["VISITS_CMAT_PERIOD"] > 0).astype(int)
    return mu.rename(
        columns={
            "CLAVEPROFESOR": "MU_PROFESSOR",
            "PERIOD_LABEL": "MU_PERIOD_LABEL",
            "OFFICIAL_CAREER": "MU_CAREER_OFFICIAL",
            "VISITS_CMAT_PERIOD": "MU_VISITS_CMAT_PERIOD",
            "VISITS_COURSE": "MU_VISITS_COURSE",
            "PPA_REACHED_PERIOD": "MU_PPA_REACHED_PERIOD",
            "PERSISTENT_GT3_PERIOD": "MU_PERSISTENT_GT3_PERIOD",
        }
    )
