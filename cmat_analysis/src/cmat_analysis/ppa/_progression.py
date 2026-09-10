from __future__ import annotations

"""PPA1-oriented longitudinal analyses for the MU -> Calculus progression cohort.

This module is intentionally additive.  It does not replace the earlier working-draft
cohorts or results.  It implements the newer administrative interpretation supplied
for the project:

* Matemáticas Universitarias (MU) is treated as a first-semester course.
* PPA1 is a first-semester institutional participation requirement.  The study uses
  the operational three-CMAT-registration threshold already present in the data design
  as an incentive-related threshold; it does not infer a student's psychological motive.
* Cálculo I is the subsequent course and CMAT visits during Cálculo do not satisfy the
  same PPA1 incentive under the study assumption.
* The primary PPA progression cohort contains students whose first observed MU attempt
  was passed with a numeric grade, who subsequently have a numeric Cálculo I grade,
  whose two periods have CMAT-record coverage, and who progress in the next regular
  Primavera/Otoño term.  A broader all-subsequent-Cálculo sensitivity cohort is retained.
* Later academic rows after an observed pass of the same subject are flagged as likely
  administrative revalidations/replications and are never silently deleted.

All analyses remain observational.  The threshold is not an assignment variable and
must not be described as a regression-discontinuity design.
"""

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
from statsmodels.stats.contingency_tables import Table2x2
from statsmodels.stats.proportion import confint_proportions_2indep, proportion_confint

from .cohort import attach_visits, normalize_text, visit_group


GROUP_ORDER = ["0", "1-2", "3", "4+"]


@dataclass(frozen=True)
class PPAProgressionCohorts:
    """Container for the reconstructed administrative history and paired cohorts."""

    academic_history: pd.DataFrame
    paired_all_subsequent: pd.DataFrame
    paired_primary_next_term: pd.DataFrame
    cohort_flow: pd.DataFrame
    revalidation_audit: pd.DataFrame
    career_count_distribution: pd.DataFrame


def _subject_mask(df: pd.DataFrame, code: str, name: str) -> pd.Series:
    return (df["SUBJECT_CODE"].astype(str).str.upper() == code.upper()) | (
        df["SUBJECT"] == normalize_text(name)
    )


def classify_revalidation_records(academics: pd.DataFrame, *, passing_grade: float = 7.5) -> pd.DataFrame:
    """Flag later rows after an observed pass as likely revalidation/replication.

    The official academic extract can contain the same student's passed course again
    under a different degree program when that credit is revalidated.  There is no
    explicit revalidation flag in the supplied extract.  We therefore apply a
    conservative, auditable rule: once a numeric passing result for a student-subject
    has been observed, any *later-period* row for that same subject is flagged as
    ``likely_post_pass_revalidation``.  Failed/adverse rows before the first pass remain
    genuine attempt candidates.  Administrative non-attempt tokens remain a separate
    category.  Nothing is removed here.
    """
    d = academics.copy()
    d["OFFICIAL_CAREER"] = d["CLAVECARRERA"].map(normalize_text)
    d = d.sort_values(["STUDENT_ID", "SUBJECT_CODE", "PERIOD_INDEX", "SOURCE_ROW"], kind="stable")
    d["IS_NUMERIC_PASS"] = (
        d["GRADE_CLASS"].eq("numeric") & d["GRADE_NUMERIC"].ge(float(passing_grade))
    )
    same_period_keys = ["STUDENT_ID", "SUBJECT_CODE", "YEAR", "SESSION"]
    d["SAME_PERIOD_ROW_COUNT"] = d.groupby(same_period_keys)["STUDENT_ID"].transform("size")
    d["SAME_PERIOD_CAREER_COUNT"] = d.groupby(same_period_keys)["OFFICIAL_CAREER"].transform("nunique")
    d["SAME_PERIOD_GRADE_COUNT"] = d.groupby(same_period_keys)["GRADE_TOKEN"].transform("nunique")
    d["LIKELY_SAME_PERIOD_CAREER_REPLICATION"] = (
        d["SAME_PERIOD_ROW_COUNT"].gt(1)
        & d["SAME_PERIOD_CAREER_COUNT"].gt(1)
        & d["SAME_PERIOD_GRADE_COUNT"].eq(1)
    )
    d["SAME_PERIOD_REPLICATION_RANK"] = d.groupby(same_period_keys).cumcount()

    first_pass = (
        d.loc[d["IS_NUMERIC_PASS"]]
        .groupby(["STUDENT_ID", "SUBJECT_CODE"], dropna=False)["PERIOD_INDEX"]
        .min()
        .rename("FIRST_PASS_PERIOD_INDEX")
    )
    d = d.join(first_pass, on=["STUDENT_ID", "SUBJECT_CODE"])
    d["LIKELY_POST_PASS_REVALIDATION"] = (
        d["FIRST_PASS_PERIOD_INDEX"].notna()
        & d["PERIOD_INDEX"].gt(d["FIRST_PASS_PERIOD_INDEX"])
    )
    d["SAME_GRADE_AS_FIRST_PASS"] = False

    pass_token = (
        d.loc[d["IS_NUMERIC_PASS"]]
        .sort_values(["STUDENT_ID", "SUBJECT_CODE", "PERIOD_INDEX", "SOURCE_ROW"], kind="stable")
        .drop_duplicates(["STUDENT_ID", "SUBJECT_CODE"], keep="first")
        .set_index(["STUDENT_ID", "SUBJECT_CODE"])["GRADE_TOKEN"]
        .rename("FIRST_PASS_GRADE_TOKEN")
    )
    d = d.join(pass_token, on=["STUDENT_ID", "SUBJECT_CODE"])
    d["SAME_GRADE_AS_FIRST_PASS"] = (
        d["LIKELY_POST_PASS_REVALIDATION"]
        & d["GRADE_TOKEN"].eq(d["FIRST_PASS_GRADE_TOKEN"])
    )

    d["ACADEMIC_EVENT_TYPE"] = "other_or_unknown"
    d.loc[d["GRADE_CLASS"].eq("administrative_non_attempt"), "ACADEMIC_EVENT_TYPE"] = "administrative_non_attempt"
    same_period_replica = d["LIKELY_SAME_PERIOD_CAREER_REPLICATION"] & d["SAME_PERIOD_REPLICATION_RANK"].gt(0)
    real = (
        d["GRADE_CLASS"].isin(["numeric", "adverse"])
        & ~d["LIKELY_POST_PASS_REVALIDATION"]
        & ~same_period_replica
    )
    d.loc[real, "ACADEMIC_EVENT_TYPE"] = "real_attempt_candidate"
    d.loc[same_period_replica, "ACADEMIC_EVENT_TYPE"] = "likely_same_period_career_replication"
    d.loc[d["LIKELY_POST_PASS_REVALIDATION"], "ACADEMIC_EVENT_TYPE"] = "likely_post_pass_revalidation"

    # Career history is useful for auditing dual/multiple-degree records.  It is not
    # used as evidence that a later post-pass row is a new course attempt.
    d["N_OFFICIAL_CAREERS_STUDENT"] = d.groupby("STUDENT_ID")["OFFICIAL_CAREER"].transform("nunique")
    d["N_OFFICIAL_CAREERS_STUDENT_SUBJECT"] = d.groupby(
        ["STUDENT_ID", "SUBJECT_CODE"]
    )["OFFICIAL_CAREER"].transform("nunique")
    return d


def _numeric_classroom_reference_z(
    history: pd.DataFrame,
    *,
    code: str,
    name: str,
    min_classroom_n: int = 5,
) -> pd.DataFrame:
    """Compute numeric-grade Z using the actual course classroom as reference.

    Classroom is defined as professor x same subject x same academic period.  The
    reference set contains every row classified as a real attempt candidate with a
    numeric grade, including genuine repeats before a first pass, and excludes likely
    post-pass revalidation rows.  This makes the Z-score a property of the student's
    observed classroom rather than of the later analytical subcohort.
    """
    d = history.loc[
        _subject_mask(history, code, name)
        & history["ACADEMIC_EVENT_TYPE"].eq("real_attempt_candidate")
        & history["GRADE_CLASS"].eq("numeric")
    ].copy()
    d["COURSE_CLASSROOM_ID"] = (
        d["SUBJECT_CODE"].astype(str)
        + "|" + d["CLAVEPROFESOR"].astype(str)
        + "|" + d["YEAR"].astype(str)
        + "|" + d["SESSION"].astype(str)
    )
    stats_df = d.groupby("COURSE_CLASSROOM_ID")["GRADE_NUMERIC"].agg(
        CLASSROOM_N="size", CLASSROOM_MEAN="mean", CLASSROOM_SD="std"
    )
    d = d.join(stats_df, on="COURSE_CLASSROOM_ID")
    valid = (d["CLASSROOM_N"] >= int(min_classroom_n)) & d["CLASSROOM_SD"].gt(0)
    d["Z_CLASSROOM_NUMERIC"] = np.where(
        valid,
        (d["GRADE_NUMERIC"] - d["CLASSROOM_MEAN"]) / d["CLASSROOM_SD"],
        np.nan,
    )
    return d[[
        "SOURCE_ROW", "COURSE_CLASSROOM_ID", "CLASSROOM_N", "CLASSROOM_MEAN",
        "CLASSROOM_SD", "Z_CLASSROOM_NUMERIC"
    ]].copy()


def _next_regular_term(year: int, session: str) -> tuple[int, str] | None:
    session = normalize_text(session)
    if session == "PRIMAVERA":
        return int(year), "OTONO"
    if session == "OTONO":
        return int(year) + 1, "PRIMAVERA"
    if session == "VERANO":
        return int(year), "OTONO"
    return None


def _period_form_career(advisories: pd.DataFrame) -> pd.DataFrame:
    """Most frequently recorded Google-Form career for each student-period.

    This field is descriptive only.  Non-users have no Google-Form career by
    construction, so it must not be used as a baseline adjustment variable in models
    comparing users with non-users.
    """
    a = advisories.copy()
    if "carrera" not in a.columns:
        return pd.DataFrame(columns=[
            "STUDENT_ID", "YEAR", "SESSION", "FORM_CAREER_MODE", "FORM_CAREER_NUNIQUE"
        ])
    a["FORM_CAREER"] = a["carrera"].map(normalize_text)
    a = a.dropna(subset=["FORM_CAREER"]).copy()
    counts = (
        a.groupby(["STUDENT_ID", "YEAR", "SESSION", "FORM_CAREER"], dropna=False)
        .size().rename("n").reset_index()
    )
    counts = counts.sort_values(
        ["STUDENT_ID", "YEAR", "SESSION", "n", "FORM_CAREER"],
        ascending=[True, True, True, False, True], kind="stable"
    )
    mode = counts.drop_duplicates(["STUDENT_ID", "YEAR", "SESSION"], keep="first").rename(
        columns={"FORM_CAREER": "FORM_CAREER_MODE"}
    )[["STUDENT_ID", "YEAR", "SESSION", "FORM_CAREER_MODE"]]
    nu = (
        a.groupby(["STUDENT_ID", "YEAR", "SESSION"])["FORM_CAREER"]
        .nunique().rename("FORM_CAREER_NUNIQUE").reset_index()
    )
    return mode.merge(nu, on=["STUDENT_ID", "YEAR", "SESSION"], how="left")


def build_ppa_progression_cohort(data, config) -> PPAProgressionCohorts:
    """Build strict MU -> Calculus cohorts under the PPA1 first-semester assumption."""
    history = classify_revalidation_records(data.academics, passing_grade=config.passing_grade)
    audit_source = data.academic_audit if getattr(data, "academic_audit", None) is not None else data.academics
    audit_history = classify_revalidation_records(audit_source, passing_grade=config.passing_grade)
    coverage = set(zip(
        data.data_quality["coverage"]["YEAR"].astype(int),
        data.data_quality["coverage"]["SESSION"],
    ))

    real = history.loc[history["ACADEMIC_EVENT_TYPE"].eq("real_attempt_candidate")].copy()
    mu_all = real.loc[_subject_mask(real, config.primary_subject_code, config.primary_subject_name)].copy()
    mu_all = mu_all.sort_values(["STUDENT_ID", "PERIOD_INDEX", "SOURCE_ROW"], kind="stable")
    mu_first = mu_all.drop_duplicates("STUDENT_ID", keep="first").copy()
    # PPA-focused cohort: first observed MU attempt must be a numeric pass.
    mu_pass = mu_first.loc[
        mu_first["GRADE_CLASS"].eq("numeric")
        & mu_first["GRADE_NUMERIC"].ge(config.passing_grade)
    ].copy()
    mu_pass = attach_visits(mu_pass, data.advisories, threshold=config.ppa_threshold)
    mu_pass["VISIT_COVERAGE"] = [
        (int(y), s) in coverage for y, s in zip(mu_pass["YEAR"], mu_pass["SESSION"])
    ]

    calc_all = real.loc[_subject_mask(real, config.followup_subject_code, config.followup_subject_name)].copy()
    calc_all = calc_all.sort_values(["STUDENT_ID", "PERIOD_INDEX", "SOURCE_ROW"], kind="stable")
    mu_key = mu_pass[["STUDENT_ID", "PERIOD_INDEX"]].rename(columns={"PERIOD_INDEX": "MU_PERIOD_INDEX_KEY"})
    calc_candidate = calc_all.merge(mu_key, on="STUDENT_ID", how="inner")
    calc_candidate = calc_candidate.loc[calc_candidate["PERIOD_INDEX"] > calc_candidate["MU_PERIOD_INDEX_KEY"]].copy()
    calc_first_after = (
        calc_candidate.sort_values(["STUDENT_ID", "PERIOD_INDEX", "SOURCE_ROW"], kind="stable")
        .drop_duplicates("STUDENT_ID", keep="first")
        .drop(columns="MU_PERIOD_INDEX_KEY")
    )
    # "Ya obtuvieron calificación" is operationalized as a numeric final grade.
    calc_numeric = calc_first_after.loc[calc_first_after["GRADE_CLASS"].eq("numeric")].copy()
    calc_numeric = attach_visits(calc_numeric, data.advisories, threshold=config.ppa_threshold)
    calc_numeric["VISIT_COVERAGE"] = [
        (int(y), s) in coverage for y, s in zip(calc_numeric["YEAR"], calc_numeric["SESSION"])
    ]

    mu_z = _numeric_classroom_reference_z(
        history, code=config.primary_subject_code, name=config.primary_subject_name,
        min_classroom_n=config.min_classroom_n_for_z,
    ).rename(columns={
        "COURSE_CLASSROOM_ID": "MU_CLASSROOM_ID",
        "CLASSROOM_N": "MU_CLASSROOM_N",
        "CLASSROOM_MEAN": "MU_CLASSROOM_MEAN",
        "CLASSROOM_SD": "MU_CLASSROOM_SD",
        "Z_CLASSROOM_NUMERIC": "Z_MU",
    })
    calc_z = _numeric_classroom_reference_z(
        history, code=config.followup_subject_code, name=config.followup_subject_name,
        min_classroom_n=config.min_classroom_n_for_z,
    ).rename(columns={
        "COURSE_CLASSROOM_ID": "CALC_CLASSROOM_ID",
        "CLASSROOM_N": "CALC_CLASSROOM_N",
        "CLASSROOM_MEAN": "CALC_CLASSROOM_MEAN",
        "CLASSROOM_SD": "CALC_CLASSROOM_SD",
        "Z_CLASSROOM_NUMERIC": "Z_CALC",
    })

    mu_pass = mu_pass.merge(mu_z, on="SOURCE_ROW", how="left")
    calc_numeric = calc_numeric.merge(calc_z, on="SOURCE_ROW", how="left")

    mu_cols = [
        "STUDENT_ID", "SOURCE_ROW", "YEAR", "SESSION", "PERIOD_INDEX", "PERIOD_LABEL",
        "OFFICIAL_CAREER", "CLAVEPROFESOR", "GRADE_NUMERIC", "VISITS_COURSE",
        "VISITS_CMAT_PERIOD", "VISIT_GROUP_COURSE", "VISIT_GROUP_PERIOD",
        "PPA_REACHED_PERIOD", "PERSISTENT_GT3_PERIOD", "VISIT_COVERAGE",
        "MU_CLASSROOM_ID", "MU_CLASSROOM_N", "MU_CLASSROOM_MEAN", "MU_CLASSROOM_SD", "Z_MU",
        "N_OFFICIAL_CAREERS_STUDENT",
    ]
    mu_pair = mu_pass[mu_cols].rename(columns={
        "SOURCE_ROW": "MU_SOURCE_ROW", "YEAR": "MU_YEAR", "SESSION": "MU_SESSION",
        "PERIOD_INDEX": "MU_PERIOD_INDEX", "PERIOD_LABEL": "MU_PERIOD_LABEL",
        "OFFICIAL_CAREER": "MU_CAREER_OFFICIAL", "CLAVEPROFESOR": "MU_PROFESSOR",
        "GRADE_NUMERIC": "MU_GRADE_NUMERIC", "VISITS_COURSE": "MU_VISITS_COURSE",
        "VISITS_CMAT_PERIOD": "MU_VISITS_CMAT_PERIOD", "VISIT_GROUP_COURSE": "MU_VISIT_GROUP_COURSE",
        "VISIT_GROUP_PERIOD": "MU_VISIT_GROUP_PERIOD", "PPA_REACHED_PERIOD": "MU_PPA_REACHED_PERIOD",
        "PERSISTENT_GT3_PERIOD": "MU_PERSISTENT_GT3_PERIOD", "VISIT_COVERAGE": "MU_VISIT_COVERAGE",
    })
    calc_cols = [
        "STUDENT_ID", "SOURCE_ROW", "YEAR", "SESSION", "PERIOD_INDEX", "PERIOD_LABEL",
        "OFFICIAL_CAREER", "CLAVEPROFESOR", "GRADE_NUMERIC", "VISITS_COURSE",
        "VISITS_CMAT_PERIOD", "VISIT_GROUP_COURSE", "VISIT_GROUP_PERIOD", "VISIT_COVERAGE",
        "CALC_CLASSROOM_ID", "CALC_CLASSROOM_N", "CALC_CLASSROOM_MEAN", "CALC_CLASSROOM_SD", "Z_CALC",
    ]
    calc_pair = calc_numeric[calc_cols].rename(columns={
        "SOURCE_ROW": "CALC_SOURCE_ROW", "YEAR": "CALC_YEAR", "SESSION": "CALC_SESSION",
        "PERIOD_INDEX": "CALC_PERIOD_INDEX", "PERIOD_LABEL": "CALC_PERIOD_LABEL",
        "OFFICIAL_CAREER": "CALC_CAREER_OFFICIAL", "CLAVEPROFESOR": "CALC_PROFESSOR",
        "GRADE_NUMERIC": "CALC_GRADE_NUMERIC", "VISITS_COURSE": "CALC_VISITS_COURSE",
        "VISITS_CMAT_PERIOD": "CALC_VISITS_CMAT_PERIOD", "VISIT_GROUP_COURSE": "CALC_VISIT_GROUP_COURSE",
        "VISIT_GROUP_PERIOD": "CALC_VISIT_GROUP_PERIOD", "VISIT_COVERAGE": "CALC_VISIT_COVERAGE",
    })

    paired = mu_pair.merge(calc_pair, on="STUDENT_ID", how="inner")
    paired["BOTH_VISIT_COVERAGE"] = paired["MU_VISIT_COVERAGE"] & paired["CALC_VISIT_COVERAGE"]
    paired["BOTH_Z_AVAILABLE"] = paired["Z_MU"].notna() & paired["Z_CALC"].notna()
    paired["IS_NEXT_REGULAR_TERM"] = [
        (int(cy), cs) == _next_regular_term(int(my), ms)
        for my, ms, cy, cs in zip(
            paired["MU_YEAR"], paired["MU_SESSION"], paired["CALC_YEAR"], paired["CALC_SESSION"]
        )
    ]
    paired["ACADEMIC_TERM_LAG"] = paired["CALC_PERIOD_INDEX"] - paired["MU_PERIOD_INDEX"]
    paired["MU_ANY_VISIT"] = (paired["MU_VISITS_CMAT_PERIOD"] > 0).astype(int)
    paired["CALC_ANY_VISIT"] = (paired["CALC_VISITS_CMAT_PERIOD"] > 0).astype(int)
    paired["MU_SPECIFIC_ANY_VISIT"] = (paired["MU_VISITS_COURSE"] > 0).astype(int)
    paired["CALC_SPECIFIC_ANY_VISIT"] = (paired["CALC_VISITS_COURSE"] > 0).astype(int)
    paired["DELTA_Z"] = paired["Z_CALC"] - paired["Z_MU"]
    paired["MU_VISIT_GROUP"] = pd.Categorical(
        paired["MU_VISITS_CMAT_PERIOD"].map(lambda v: visit_group(v, config.ppa_threshold)),
        categories=GROUP_ORDER, ordered=True,
    )
    paired["BEHAVIOR_PROFILE"] = (
        paired["MU_VISIT_GROUP"].astype(str)
        + " -> "
        + np.where(paired["CALC_ANY_VISIT"].eq(1), "Calc use", "Calc no use")
    )
    paired["OFFICIAL_CAREER_CHANGED"] = (
        paired["MU_CAREER_OFFICIAL"].fillna("__MISSING__")
        != paired["CALC_CAREER_OFFICIAL"].fillna("__MISSING__")
    ).astype(int)

    # Add contemporaneous career recorded by the Google Form, only descriptively.
    form_career = _period_form_career(data.advisories)
    if len(form_career):
        mu_fc = form_career.rename(columns={
            "YEAR": "MU_YEAR", "SESSION": "MU_SESSION",
            "FORM_CAREER_MODE": "MU_FORM_CAREER_MODE",
            "FORM_CAREER_NUNIQUE": "MU_FORM_CAREER_NUNIQUE",
        })
        calc_fc = form_career.rename(columns={
            "YEAR": "CALC_YEAR", "SESSION": "CALC_SESSION",
            "FORM_CAREER_MODE": "CALC_FORM_CAREER_MODE",
            "FORM_CAREER_NUNIQUE": "CALC_FORM_CAREER_NUNIQUE",
        })
        paired = paired.merge(mu_fc, on=["STUDENT_ID", "MU_YEAR", "MU_SESSION"], how="left")
        paired = paired.merge(calc_fc, on=["STUDENT_ID", "CALC_YEAR", "CALC_SESSION"], how="left")

    all_subseq = paired.loc[paired["BOTH_VISIT_COVERAGE"] & paired["BOTH_Z_AVAILABLE"]].copy().reset_index(drop=True)
    primary = all_subseq.loc[all_subseq["IS_NEXT_REGULAR_TERM"]].copy().reset_index(drop=True)

    flow = pd.DataFrame([
        {"stage": "first observed MU attempt (real-attempt candidate)", "n": int(len(mu_first))},
        {"stage": "first MU attempt is numeric pass >= 7.5", "n": int(len(mu_pass))},
        {"stage": "first later Calculus I real-attempt candidate exists", "n": int(len(calc_first_after))},
        {"stage": "later Calculus I has numeric final grade", "n": int(len(calc_numeric))},
        {"stage": "paired MU/Calculus with CMAT coverage and classroom Z in both", "n": int(len(all_subseq))},
        {"stage": "primary PPA progression cohort: next regular term", "n": int(len(primary))},
    ])

    reval_audit = (
        audit_history.groupby("ACADEMIC_EVENT_TYPE", dropna=False)
        .agg(rows=("STUDENT_ID", "size"), students=("STUDENT_ID", "nunique"))
        .reset_index()
    )
    reval_extra = pd.DataFrame([
        {
            "ACADEMIC_EVENT_TYPE": "likely_revalidation_same_grade_as_first_pass",
            "rows": int(audit_history["SAME_GRADE_AS_FIRST_PASS"].sum()),
            "students": int(audit_history.loc[audit_history["SAME_GRADE_AS_FIRST_PASS"], "STUDENT_ID"].nunique()),
        },
        {
            "ACADEMIC_EVENT_TYPE": "rows_with_missing_professor_in_raw_extract",
            "rows": int(audit_history["CLAVEPROFESOR"].isna().sum()),
            "students": int(audit_history.loc[audit_history["CLAVEPROFESOR"].isna(), "STUDENT_ID"].nunique()),
        },
    ])
    reval_audit = pd.concat([reval_audit, reval_extra], ignore_index=True)

    career_dist = (
        audit_history[["STUDENT_ID", "N_OFFICIAL_CAREERS_STUDENT"]]
        .drop_duplicates("STUDENT_ID")
        .groupby("N_OFFICIAL_CAREERS_STUDENT")
        .size().rename("students").reset_index()
        .sort_values("N_OFFICIAL_CAREERS_STUDENT")
    )
    return PPAProgressionCohorts(history, all_subseq, primary, flow, reval_audit, career_dist)


def ppa_behavior_profiles(df: pd.DataFrame) -> pd.DataFrame:
    """Eight observable MU-group x later-Calculus-use profiles."""
    d = df.copy()
    rows = []
    for g in GROUP_ORDER:
        for calc_use in [0, 1]:
            m = d["MU_VISIT_GROUP"].astype(str).eq(g) & d["CALC_ANY_VISIT"].eq(calc_use)
            sub = d.loc[m]
            rows.append({
                "mu_visit_group": g,
                "calc_any_visit": calc_use,
                "profile": f"{g} -> {'Calc use' if calc_use else 'Calc no use'}",
                "n": int(len(sub)),
                "proportion_total": float(len(sub) / len(d)) if len(d) else np.nan,
                "mean_z_mu": float(sub["Z_MU"].mean()) if len(sub) else np.nan,
                "mean_z_calc": float(sub["Z_CALC"].mean()) if len(sub) else np.nan,
                "mean_delta_z": float(sub["DELTA_Z"].mean()) if len(sub) else np.nan,
            })
    return pd.DataFrame(rows)


def persistence_by_mu_group(df: pd.DataFrame) -> pd.DataFrame:
    """P(Calculus CMAT use | MU visit group) with Wilson intervals."""
    rows = []
    for g in GROUP_ORDER:
        sub = df.loc[df["MU_VISIT_GROUP"].astype(str).eq(g)]
        n = len(sub)
        events = int(sub["CALC_ANY_VISIT"].sum())
        p = events / n if n else np.nan
        lo, hi = proportion_confint(events, n, alpha=0.05, method="wilson") if n else (np.nan, np.nan)
        rows.append({
            "mu_visit_group": g,
            "n": int(n),
            "calc_users": events,
            "p_calc_any_visit": float(p),
            "ci95_low_wilson": float(lo),
            "ci95_high_wilson": float(hi),
            "mean_mu_visits": float(sub["MU_VISITS_CMAT_PERIOD"].mean()) if n else np.nan,
            "mean_calc_visits": float(sub["CALC_VISITS_CMAT_PERIOD"].mean()) if n else np.nan,
        })
    return pd.DataFrame(rows)


def _two_group_risk_comparison(
    df: pd.DataFrame,
    *,
    group_col: str,
    event_col: str,
    exposed_value: str,
    reference_value: str,
    label: str,
) -> pd.DataFrame:
    d = df.loc[df[group_col].astype(str).isin([reference_value, exposed_value])].copy()
    exposed = d[group_col].astype(str).eq(exposed_value)
    a = int((exposed & d[event_col].eq(1)).sum())
    b = int((exposed & d[event_col].eq(0)).sum())
    c = int((~exposed & d[event_col].eq(1)).sum())
    e = int((~exposed & d[event_col].eq(0)).sum())
    table = np.array([[a, b], [c, e]], dtype=float)
    n1, n0 = a + b, c + e
    p1 = a / n1 if n1 else np.nan
    p0 = c / n0 if n0 else np.nan
    p1ci = proportion_confint(a, n1, method="wilson") if n1 else (np.nan, np.nan)
    p0ci = proportion_confint(c, n0, method="wilson") if n0 else (np.nan, np.nan)
    rdci = confint_proportions_2indep(a, n1, c, n0, compare="diff", method="newcomb", correction=True)
    t2 = Table2x2(table, shift_zeros=True)
    chi2, pchi, chi_df, expected = stats.chi2_contingency(table, correction=False)
    fisher_or, fisher_p = stats.fisher_exact(table, alternative="two-sided")
    return pd.DataFrame([{
        "comparison": label,
        "exposed_group": exposed_value,
        "reference_group": reference_value,
        "n_exposed": n1,
        "n_reference": n0,
        "p_exposed": p1,
        "p_exposed_ci95_low": float(p1ci[0]),
        "p_exposed_ci95_high": float(p1ci[1]),
        "p_reference": p0,
        "p_reference_ci95_low": float(p0ci[0]),
        "p_reference_ci95_high": float(p0ci[1]),
        "risk_difference": float(p1 - p0),
        "risk_difference_ci95_low": float(rdci[0]),
        "risk_difference_ci95_high": float(rdci[1]),
        "risk_ratio": float(t2.riskratio),
        "risk_ratio_ci95_low": float(t2.riskratio_confint()[0]),
        "risk_ratio_ci95_high": float(t2.riskratio_confint()[1]),
        "odds_ratio": float(t2.oddsratio),
        "odds_ratio_ci95_low": float(t2.oddsratio_confint()[0]),
        "odds_ratio_ci95_high": float(t2.oddsratio_confint()[1]),
        "pearson_chi_square": float(chi2),
        "pearson_p": float(pchi),
        "min_expected_cell": float(np.min(expected)),
        "fisher_exact_or": float(fisher_or),
        "fisher_exact_p": float(fisher_p),
        "interpretation": "observational risk comparison; not a causal PPA effect",
    }])


def ppa_persistence_association_tests(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Omnibus 4x2 association plus the pre-specified exact-3 vs 4+ contrast."""
    tab = pd.crosstab(df["MU_VISIT_GROUP"].astype(str), df["CALC_ANY_VISIT"]).reindex(GROUP_ORDER, fill_value=0)
    tab = tab.reindex(columns=[0, 1], fill_value=0)
    chi2, p, dof, expected = stats.chi2_contingency(tab.to_numpy(), correction=False)
    n = int(tab.to_numpy().sum())
    # For a 4x2 table, min(r-1,c-1)=1, so Cramer's V simplifies to sqrt(chi2/n).
    v = math.sqrt(chi2 / n) if n else np.nan
    omnibus = pd.DataFrame([{
        "test": "Pearson chi-square: MU 0/1-2/3/4+ x any Calculus use",
        "n": n,
        "chi_square": float(chi2),
        "df": int(dof),
        "p_value": float(p),
        "cramers_v": float(v),
        "min_expected_cell": float(np.min(expected)),
        "assumption_note": "Pearson asymptotic inference is adequate when expected cells are not sparse; unit is one student.",
    }])
    key = _two_group_risk_comparison(
        df, group_col="MU_VISIT_GROUP", event_col="CALC_ANY_VISIT",
        exposed_value="4+", reference_value="3",
        label="4+ MU visits vs exactly 3: later Calculus CMAT use",
    )
    return omnibus, key


def _collapse_rare(series: pd.Series, min_n: int = 30) -> pd.Series:
    s = series.fillna("MISSING").astype(str)
    counts = s.value_counts()
    keep = set(counts[counts >= min_n].index)
    return s.where(s.isin(keep), "OTHER")


def persistence_logistic_models(df: pd.DataFrame, *, min_career_n: int = 30) -> pd.DataFrame:
    """Cluster-robust logistic models for later CMAT use.

    Model 1 contains the four MU visit groups.  Model 2 additionally conditions on
    prior relative performance (Z_MU), contemporaneous official degree program at the
    actual MU attempt, and MU academic period.  Clustering is by MU classroom.  These
    models quantify predictive association; they do not identify a PPA treatment effect.
    """
    d = df.dropna(subset=["CALC_ANY_VISIT", "MU_VISIT_GROUP", "MU_CLASSROOM_ID", "Z_MU"]).copy()
    d["MU_CAREER_MODEL"] = _collapse_rare(d["MU_CAREER_OFFICIAL"], min_n=min_career_n)
    formulas = [
        ("unadjusted_group_logit", "CALC_ANY_VISIT ~ C(MU_VISIT_GROUP, Treatment(reference='0'))"),
        (
            "adjusted_prior_performance_major_term_logit",
            "CALC_ANY_VISIT ~ C(MU_VISIT_GROUP, Treatment(reference='0')) + Z_MU + C(MU_CAREER_MODEL) + C(MU_PERIOD_LABEL)",
        ),
    ]
    rows: list[dict[str, object]] = []
    for name, formula in formulas:
        fit = smf.logit(formula, data=d).fit(
            disp=False, cov_type="cluster", cov_kwds={"groups": d["MU_CLASSROOM_ID"]}
        )
        for term in fit.params.index:
            if term == "Intercept":
                continue
            ci = fit.conf_int().loc[term]
            rows.append({
                "model": name,
                "term": term,
                "log_odds_coef": float(fit.params[term]),
                "cluster_se": float(fit.bse[term]),
                "p_value": float(fit.pvalues[term]),
                "odds_ratio": float(np.exp(fit.params[term])),
                "or_ci95_low": float(np.exp(ci.iloc[0])),
                "or_ci95_high": float(np.exp(ci.iloc[1])),
                "n": int(fit.nobs),
                "mu_classrooms": int(d["MU_CLASSROOM_ID"].nunique()),
                "covariance": "cluster-robust by MU course classroom",
            })
    return pd.DataFrame(rows)


def piecewise_threshold_persistence_model(df: pd.DataFrame, *, cap_visits: int = 12) -> pd.DataFrame:
    """Descriptive piecewise logit around V=3; explicitly not an RD design."""
    d = df.dropna(subset=["CALC_ANY_VISIT", "MU_VISITS_CMAT_PERIOD", "MU_CLASSROOM_ID"]).copy()
    d["MU_VISITS_CAPPED"] = d["MU_VISITS_CMAT_PERIOD"].clip(upper=cap_visits).astype(float)
    d["VISITS_TO_THRESHOLD"] = np.minimum(d["MU_VISITS_CAPPED"], 3.0)
    d["VISITS_AFTER_THRESHOLD"] = np.maximum(d["MU_VISITS_CAPPED"] - 3.0, 0.0)
    fit = smf.logit(
        "CALC_ANY_VISIT ~ VISITS_TO_THRESHOLD + VISITS_AFTER_THRESHOLD", data=d
    ).fit(disp=False, cov_type="cluster", cov_kwds={"groups": d["MU_CLASSROOM_ID"]})
    rows = []
    for term in ["VISITS_TO_THRESHOLD", "VISITS_AFTER_THRESHOLD"]:
        ci = fit.conf_int().loc[term]
        rows.append({
            "term": term,
            "coef_log_odds": float(fit.params[term]),
            "cluster_se": float(fit.bse[term]),
            "p_value": float(fit.pvalues[term]),
            "odds_ratio_per_one_visit": float(np.exp(fit.params[term])),
            "or_ci95_low": float(np.exp(ci.iloc[0])),
            "or_ci95_high": float(np.exp(ci.iloc[1])),
            "n": int(fit.nobs),
            "cap_visits": int(cap_visits),
            "note": "piecewise descriptive association; V is student-controlled, so this is not regression discontinuity",
        })
    return pd.DataFrame(rows)


def later_performance_models(df: pd.DataFrame, *, min_career_n: int = 30) -> pd.DataFrame:
    """Predict later Calculus classroom-relative performance from prior MU information.

    The primary temporal specification uses Z_MU and MU visit group to predict Z_CALC.
    It deliberately does not include Cálculo-period CMAT use because that exposure is
    contemporaneous with the outcome and can respond to difficulty experienced during
    the course.  Standard errors are clustered by the Cálculo classroom.
    """
    d = df.dropna(subset=["Z_CALC", "Z_MU", "MU_VISIT_GROUP", "CALC_CLASSROOM_ID"]).copy()
    d["CALC_CAREER_MODEL"] = _collapse_rare(d["CALC_CAREER_OFFICIAL"], min_n=min_career_n)
    formulas = [
        (
            "prior_performance_plus_mu_use",
            "Z_CALC ~ Z_MU + C(MU_VISIT_GROUP, Treatment(reference='0'))",
        ),
        (
            "plus_calc_major_and_period",
            "Z_CALC ~ Z_MU + C(MU_VISIT_GROUP, Treatment(reference='0')) + C(CALC_CAREER_MODEL) + C(CALC_PERIOD_LABEL)",
        ),
    ]
    rows = []
    for name, formula in formulas:
        fit = smf.ols(formula, data=d).fit(
            cov_type="cluster", cov_kwds={"groups": d["CALC_CLASSROOM_ID"]}
        )
        for term in fit.params.index:
            if term == "Intercept":
                continue
            ci = fit.conf_int().loc[term]
            rows.append({
                "model": name,
                "term": term,
                "coef": float(fit.params[term]),
                "cluster_se": float(fit.bse[term]),
                "p_value": float(fit.pvalues[term]),
                "ci95_low": float(ci.iloc[0]),
                "ci95_high": float(ci.iloc[1]),
                "n": int(fit.nobs),
                "calc_classrooms": int(d["CALC_CLASSROOM_ID"].nunique()),
                "covariance": "cluster-robust by Calculus course classroom",
            })
    return pd.DataFrame(rows)


def major_persistence_summary(df: pd.DataFrame, *, min_n: int = 30) -> pd.DataFrame:
    """Descriptive adoption/persistence/academic trajectory by official MU major."""
    d = df.dropna(subset=["MU_CAREER_OFFICIAL"]).copy()
    rows = []
    for career, g in d.groupby("MU_CAREER_OFFICIAL"):
        if len(g) < min_n:
            continue
        mu_users = g.loc[g["MU_ANY_VISIT"].eq(1)]
        mu_non = g.loc[g["MU_ANY_VISIT"].eq(0)]
        rows.append({
            "MU_CAREER_OFFICIAL": career,
            "n": int(len(g)),
            "mu_any_visit_rate": float(g["MU_ANY_VISIT"].mean()),
            "calc_any_visit_rate": float(g["CALC_ANY_VISIT"].mean()),
            "persistence_given_mu_use": float(mu_users["CALC_ANY_VISIT"].mean()) if len(mu_users) else np.nan,
            "late_adoption_given_no_mu_use": float(mu_non["CALC_ANY_VISIT"].mean()) if len(mu_non) else np.nan,
            "mean_z_mu": float(g["Z_MU"].mean()),
            "mean_z_calc": float(g["Z_CALC"].mean()),
            "mean_delta_z": float(g["DELTA_Z"].mean()),
            "official_career_change_rate_to_calc": float(g["OFFICIAL_CAREER_CHANGED"].mean()),
        })
    return pd.DataFrame(rows).sort_values("n", ascending=False).reset_index(drop=True)


def course_specific_transition(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """2x2 transition using course-tagged MU and Calculus advisory records."""
    d = df.copy()
    n00 = int(((d.MU_SPECIFIC_ANY_VISIT == 0) & (d.CALC_SPECIFIC_ANY_VISIT == 0)).sum())
    n01 = int(((d.MU_SPECIFIC_ANY_VISIT == 0) & (d.CALC_SPECIFIC_ANY_VISIT == 1)).sum())
    n10 = int(((d.MU_SPECIFIC_ANY_VISIT == 1) & (d.CALC_SPECIFIC_ANY_VISIT == 0)).sum())
    n11 = int(((d.MU_SPECIFIC_ANY_VISIT == 1) & (d.CALC_SPECIFIC_ANY_VISIT == 1)).sum())
    n = n00 + n01 + n10 + n11
    combos = pd.DataFrame([
        {"mu_specific_any": 0, "calc_specific_any": 0, "n": n00},
        {"mu_specific_any": 0, "calc_specific_any": 1, "n": n01},
        {"mu_specific_any": 1, "calc_specific_any": 0, "n": n10},
        {"mu_specific_any": 1, "calc_specific_any": 1, "n": n11},
    ])
    combos["proportion"] = combos["n"] / n if n else np.nan
    tmp = d.rename(columns={"MU_SPECIFIC_ANY_VISIT": "G", "CALC_SPECIFIC_ANY_VISIT": "E"})
    stats_df = _two_group_risk_comparison(
        tmp.assign(G=tmp["G"].map({0: "0", 1: "1"})),
        group_col="G", event_col="E", exposed_value="1", reference_value="0",
        label="course-tagged MU support -> course-tagged Calculus support",
    )
    return combos, stats_df


def form_career_crosswalk(df: pd.DataFrame) -> pd.DataFrame:
    """Observed official-code x Google-Form-career pairs among users in the cohort."""
    pieces = []
    for prefix in ["MU", "CALC"]:
        fcol = f"{prefix}_FORM_CAREER_MODE"
        ocol = f"{prefix}_CAREER_OFFICIAL"
        if fcol not in df.columns:
            continue
        x = df.dropna(subset=[fcol, ocol]).groupby([ocol, fcol]).size().rename("n").reset_index()
        x.insert(0, "course_period", prefix)
        x = x.rename(columns={ocol: "OFFICIAL_CAREER", fcol: "FORM_CAREER"})
        pieces.append(x)
    if not pieces:
        return pd.DataFrame(columns=["course_period", "OFFICIAL_CAREER", "FORM_CAREER", "n"])
    return pd.concat(pieces, ignore_index=True).sort_values(
        ["course_period", "OFFICIAL_CAREER", "n"], ascending=[True, True, False]
    )


def major_persistence_joint_test(df: pd.DataFrame, *, min_career_n: int = 30) -> pd.DataFrame:
    """Joint Wald test for official MU degree program in the adjusted persistence logit."""
    d = df.dropna(subset=["CALC_ANY_VISIT", "MU_VISIT_GROUP", "Z_MU", "MU_CLASSROOM_ID"]).copy()
    d["MU_CAREER_MODEL"] = _collapse_rare(d["MU_CAREER_OFFICIAL"], min_n=min_career_n)
    fit = smf.logit(
        "CALC_ANY_VISIT ~ C(MU_VISIT_GROUP, Treatment(reference='0')) + Z_MU + C(MU_CAREER_MODEL) + C(MU_PERIOD_LABEL)",
        data=d,
    ).fit(disp=False, cov_type="cluster", cov_kwds={"groups": d["MU_CLASSROOM_ID"]})
    terms = [t for t in fit.params.index if t.startswith("C(MU_CAREER_MODEL)")]
    idx = [fit.params.index.get_loc(t) for t in terms]
    R = np.zeros((len(idx), len(fit.params)))
    for r, j in enumerate(idx):
        R[r, j] = 1.0
    wt = fit.wald_test(R, scalar=True)
    return pd.DataFrame([{
        "test": "joint official-major terms in adjusted Calculus-use logit",
        "n": int(fit.nobs),
        "career_terms": int(len(terms)),
        "wald_statistic": float(wt.statistic),
        "df_constraints": int(len(terms)),
        "p_value": float(wt.pvalue),
        "min_career_n_before_other": int(min_career_n),
        "covariance": "cluster-robust by MU course classroom",
        "interpretation": "tests whether later CMAT-use propensity differs by observed degree program conditional on MU-use group, Z_MU and period; observational",
    }])


def major_delta_z_welch(df: pd.DataFrame, *, min_n: int = 30) -> pd.DataFrame:
    """Welch ANOVA of classroom-relative academic change (Delta Z) across majors."""
    from statsmodels.stats.oneway import anova_oneway

    d = df.dropna(subset=["MU_CAREER_OFFICIAL", "DELTA_Z"]).copy()
    counts = d["MU_CAREER_OFFICIAL"].value_counts()
    keep = counts[counts >= min_n].index
    d = d.loc[d["MU_CAREER_OFFICIAL"].isin(keep)].copy()
    groups = [g["DELTA_Z"].to_numpy(float) for _, g in d.groupby("MU_CAREER_OFFICIAL") if len(g) >= 2]
    if len(groups) < 2:
        return pd.DataFrame([{"status": "insufficient_data"}])
    welch = anova_oneway(groups, use_var="unequal", welch_correction=True)
    bf_stat, bf_p = stats.levene(*groups, center="median")
    return pd.DataFrame([{
        "status": "ok",
        "test": "Welch ANOVA of Delta Z = Z_Calculus - Z_MU across official MU majors",
        "n": int(len(d)),
        "careers_included": int(d["MU_CAREER_OFFICIAL"].nunique()),
        "min_career_n": int(min_n),
        "welch_F": float(welch.statistic),
        "df_num": float(welch.df_num),
        "df_denom": float(welch.df_denom),
        "p_value": float(welch.pvalue),
        "brown_forsythe_stat": float(bf_stat),
        "brown_forsythe_p": float(bf_p),
        "interpretation": "Delta Z compares relative classroom position across two courses; it is not a raw-grade change and not a causal CMAT effect",
    }])
