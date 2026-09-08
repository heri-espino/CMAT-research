from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


SESSION_MAP = {
    "P": "PRIMAVERA",
    "PRIMAVERA": "PRIMAVERA",
    "V": "VERANO",
    "VERANO": "VERANO",
    "SUMMER": "VERANO",
    "O": "OTONO",
    "OTONO": "OTONO",
    "OTOÑO": "OTONO",
}

SESSION_OFFSET = {"PRIMAVERA": 0, "VERANO": 1, "OTONO": 2}


def normalize_text(value: object) -> str | None:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    text = str(value).strip().upper()
    text = "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"\s+", " ", text)


def normalize_session(value: object) -> str | None:
    key = normalize_text(value)
    return SESSION_MAP.get(key, key)


def period_index(year: int | float, session: object) -> int:
    session_n = normalize_session(session)
    if session_n not in SESSION_OFFSET:
        raise ValueError(f"Unknown academic session: {session!r}")
    return int(year) * 3 + SESSION_OFFSET[session_n]


def period_label(year: int | float, session: object) -> str:
    return f"{int(year)}-{normalize_session(session)}"


def visit_group(visits: int | float, threshold: int = 3) -> str:
    v = int(visits)
    if v <= 0:
        return "0"
    if v < threshold:
        return f"1-{threshold - 1}"
    if v == threshold:
        return str(threshold)
    return f"{threshold + 1}+"


@dataclass
class StudyData:
    academics: pd.DataFrame
    advisories: pd.DataFrame
    data_quality: dict[str, object]
    # Normalized academic extract before rows with missing professor are removed.
    # It is used only for administrative auditing (e.g. revalidation/multiple-career
    # patterns), never as the main classroom-level analytical table.
    academic_audit: pd.DataFrame | None = None


def normalize_identifier(value: object) -> str | None:
    """Normalize numeric or pseudonymized identifiers without requiring numbers."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (float, np.floating)) and float(value).is_integer():
        return str(int(value))
    text = str(value).strip()
    return text or None


def _read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError(f"Unsupported input format: {path}")


def _classify_grade(value: object, adverse: set[str], non_attempt: set[str]) -> str:
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.notna(numeric):
        return "numeric"
    token = normalize_text(value)
    if token in adverse:
        return "adverse"
    if token in non_attempt:
        return "administrative_non_attempt"
    return "unknown_non_numeric"


def load_and_clean_inputs(config) -> StudyData:
    materias = _read_table(Path(config.materias_path))
    asesorias = _read_table(Path(config.asesorias_path))
    raw_academic_n = len(materias)

    adverse = set(config.adverse_grade_tokens)
    non_attempt = set(config.administrative_non_attempt_tokens)

    # Academic records: retain chronology. The legacy pipeline deduplicated on
    # student-course-grade across all years; here duplicates are only collapsed
    # inside the same student x course x period, so genuine repeats survive.
    materias = materias.copy()
    # Preserve source row order so stochastic sensitivity/imputation steps are
    # reproducible under identifier pseudonymization or dataframe reordering.
    materias["SOURCE_ROW"] = np.arange(len(materias), dtype=int)
    materias["STUDENT_ID"] = materias["CLAVEALUMNO"].map(normalize_identifier)
    materias["YEAR"] = pd.to_numeric(materias["anio"], errors="coerce").astype("Int64")
    materias["SESSION"] = materias["CLAVESESION"].map(normalize_session)
    materias["SUBJECT"] = materias["DESCRIBEMATERIA"].map(normalize_text)
    materias["SUBJECT_CODE"] = materias["CLAVEVARIANTEMATERIA"].astype(str).str.strip().str.upper()
    materias["GRADE_TOKEN"] = materias["CALIFICACION"].map(normalize_text)
    materias["GRADE_NUMERIC"] = pd.to_numeric(materias["CALIFICACION"], errors="coerce")
    materias["GRADE_CLASS"] = materias["CALIFICACION"].map(
        lambda x: _classify_grade(x, adverse, non_attempt)
    )
    materias["CLAVEPROFESOR"] = materias["CLAVEPROFESOR"].map(normalize_identifier)
    materias["PERIOD_INDEX"] = [
        period_index(y, s) if pd.notna(y) and s is not None else np.nan
        for y, s in zip(materias["YEAR"], materias["SESSION"])
    ]
    materias["PERIOD_LABEL"] = [
        period_label(y, s) if pd.notna(y) and s is not None else None
        for y, s in zip(materias["YEAR"], materias["SESSION"])
    ]

    # Preserve a pre-exclusion audit copy. Revalidated credits in the official
    # extract frequently have a numeric grade but no professor because no new
    # classroom was actually observed. Those rows are unsuitable for the
    # classroom Z-score but are informative for auditing administrative duplication.
    academic_audit = materias.copy()
    missing_prof_before = int(materias["CLAVEPROFESOR"].isna().sum())
    materias = materias.dropna(subset=["STUDENT_ID", "YEAR", "SESSION", "CLAVEPROFESOR"]).copy()

    dedup_keys = ["STUDENT_ID", "SUBJECT_CODE", "YEAR", "SESSION"]
    dup_mask = materias.duplicated(dedup_keys, keep=False)
    dup_groups = materias.loc[dup_mask].copy()
    conflict_groups = 0
    if not dup_groups.empty:
        for _, g in dup_groups.groupby(dedup_keys, dropna=False):
            if g["GRADE_TOKEN"].nunique(dropna=False) > 1 or g["CLAVEPROFESOR"].nunique(dropna=False) > 1:
                conflict_groups += 1
    # Exact duplicate course-period records are section-level duplication in
    # the supplied data. If a conflict appears, keep the first deterministically
    # but expose the count in data-quality outputs instead of silently hiding it.
    materias = materias.sort_values(dedup_keys + ["NUMORDEN"], kind="stable")
    materias = materias.drop_duplicates(dedup_keys, keep="first").reset_index(drop=True)

    # Advisory records. Each row is treated as one advisory event, matching the
    # legacy report. Exact duplicate rows are removed; same-day multiple visits
    # remain distinct because timestamps differ in the current data.
    asesorias = asesorias.copy()
    asesorias["VISIT_DATETIME"] = pd.to_datetime(asesorias["fecha"], errors="coerce")
    # Preserve calendar-day information for temporal attendance analyses while
    # keeping exact time only internally to order multiple visits within a day.
    asesorias["VISIT_DATE"] = asesorias["VISIT_DATETIME"].dt.normalize()
    asesorias["VISIT_WEEKDAY"] = asesorias["VISIT_DATE"].dt.day_name()
    asesorias["VISIT_DAY_OF_MONTH"] = asesorias["VISIT_DATE"].dt.day
    asesorias["VISIT_MONTH"] = asesorias["VISIT_DATE"].dt.month
    asesorias["STUDENT_ID"] = asesorias["id"].map(normalize_identifier)
    asesorias["YEAR"] = asesorias["VISIT_DATETIME"].dt.year.astype("Int64")
    asesorias["SESSION"] = asesorias["periodo"].map(normalize_session)
    asesorias["SUBJECT"] = asesorias["materia"].map(normalize_text)
    asesorias["PERIOD_LABEL"] = [
        period_label(y, s) if pd.notna(y) and s is not None else None
        for y, s in zip(asesorias["YEAR"], asesorias["SESSION"])
    ]
    exact_before = len(asesorias)
    asesorias = asesorias.drop_duplicates().reset_index(drop=True)
    exact_removed = exact_before - len(asesorias)
    asesorias = asesorias.dropna(subset=["STUDENT_ID", "VISIT_DATETIME", "YEAR", "SESSION"]).copy()

    coverage = (
        asesorias.groupby(["YEAR", "SESSION"], dropna=False)
        .agg(
            first_visit=("VISIT_DATETIME", "min"),
            last_visit=("VISIT_DATETIME", "max"),
            advisory_rows=("STUDENT_ID", "size"),
            advisory_students=("STUDENT_ID", "nunique"),
        )
        .reset_index()
        .sort_values(["YEAR", "SESSION"])
    )

    unknown_tokens = (
        materias.loc[materias["GRADE_CLASS"] == "unknown_non_numeric", "GRADE_TOKEN"]
        .value_counts(dropna=False)
        .to_dict()
    )

    quality = {
        "raw_academic_rows": int(raw_academic_n),
        "clean_academic_rows": int(len(materias)),
        "academic_rows_missing_professor_removed": missing_prof_before,
        "same_student_course_period_duplicate_rows": int(dup_mask.sum()),
        "same_student_course_period_conflict_groups": int(conflict_groups),
        "raw_advisory_rows": int(exact_before),
        "exact_duplicate_advisory_rows_removed": int(exact_removed),
        "unknown_non_numeric_grade_tokens": unknown_tokens,
        "coverage": coverage,
    }
    return StudyData(materias, asesorias, quality, academic_audit=academic_audit)


def _subject_mask(df: pd.DataFrame, code: str, name: str) -> pd.Series:
    return (df["SUBJECT_CODE"] == code.upper()) | (df["SUBJECT"] == normalize_text(name))


def _eligible_attempts(df: pd.DataFrame, code: str, name: str) -> pd.DataFrame:
    out = df.loc[_subject_mask(df, code, name)].copy()
    out = out.loc[out["GRADE_CLASS"].isin(["numeric", "adverse"])].copy()
    return out


def first_attempts(df: pd.DataFrame, code: str, name: str) -> pd.DataFrame:
    attempts = _eligible_attempts(df, code, name)
    attempts = attempts.sort_values(["STUDENT_ID", "PERIOD_INDEX"], kind="stable")
    return attempts.drop_duplicates(["STUDENT_ID"], keep="first").reset_index(drop=True)


def _visit_counts(advisories: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    by_course = (
        advisories.groupby(["STUDENT_ID", "YEAR", "SESSION", "SUBJECT"], dropna=False)
        .size()
        .rename("VISITS_COURSE")
        .reset_index()
    )
    by_period = (
        advisories.groupby(["STUDENT_ID", "YEAR", "SESSION"], dropna=False)
        .size()
        .rename("VISITS_CMAT_PERIOD")
        .reset_index()
    )
    return by_course, by_period


def attach_visits(attempts: pd.DataFrame, advisories: pd.DataFrame, *, threshold: int) -> pd.DataFrame:
    by_course, by_period = _visit_counts(advisories)
    out = attempts.merge(
        by_course,
        on=["STUDENT_ID", "YEAR", "SESSION", "SUBJECT"],
        how="left",
    )
    out = out.merge(by_period, on=["STUDENT_ID", "YEAR", "SESSION"], how="left")
    out["VISITS_COURSE"] = out["VISITS_COURSE"].fillna(0).astype(int)
    out["VISITS_CMAT_PERIOD"] = out["VISITS_CMAT_PERIOD"].fillna(0).astype(int)
    out["VISIT_GROUP_COURSE"] = out["VISITS_COURSE"].map(lambda x: visit_group(x, threshold))
    out["VISIT_GROUP_PERIOD"] = out["VISITS_CMAT_PERIOD"].map(lambda x: visit_group(x, threshold))
    out["PPA_REACHED_COURSE"] = (out["VISITS_COURSE"] >= threshold).astype(int)
    out["PPA_REACHED_PERIOD"] = (out["VISITS_CMAT_PERIOD"] >= threshold).astype(int)
    out["PERSISTENT_GT3_COURSE"] = (out["VISITS_COURSE"] > threshold).astype(int)
    out["PERSISTENT_GT3_PERIOD"] = (out["VISITS_CMAT_PERIOD"] > threshold).astype(int)
    out["CLASSROOM_ID"] = (
        out["CLAVEPROFESOR"].astype(str)
        + "|" + out["YEAR"].astype(str)
        + "|" + out["SESSION"].astype(str)
    )
    return out


def build_study_cohorts(data: StudyData, config) -> dict[str, pd.DataFrame]:
    academics, advisories = data.academics, data.advisories
    coverage = set(
        zip(
            data.data_quality["coverage"]["YEAR"].astype(int),
            data.data_quality["coverage"]["SESSION"],
        )
    )

    mu_all = first_attempts(
        academics, config.primary_subject_code, config.primary_subject_name
    )
    mu_all = attach_visits(mu_all, advisories, threshold=config.ppa_threshold)
    mu_all["VISIT_COVERAGE"] = [
        (int(y), s) in coverage for y, s in zip(mu_all["YEAR"], mu_all["SESSION"])
    ]
    mu_primary = mu_all.loc[mu_all["VISIT_COVERAGE"]].copy().reset_index(drop=True)

    calc_first = first_attempts(
        academics, config.followup_subject_code, config.followup_subject_name
    )
    calc_first = attach_visits(calc_first, advisories, threshold=config.ppa_threshold)
    calc_first["VISIT_COVERAGE"] = [
        (int(y), s) in coverage for y, s in zip(calc_first["YEAR"], calc_first["SESSION"])
    ]
    calc_comparator = calc_first.loc[calc_first["VISIT_COVERAGE"]].copy().reset_index(drop=True)

    # First Calculus I attempt strictly after the student's first MU attempt.
    calc_attempts = _eligible_attempts(
        academics, config.followup_subject_code, config.followup_subject_name
    ).sort_values(["STUDENT_ID", "PERIOD_INDEX"], kind="stable")
    mu_key = mu_all[["STUDENT_ID", "PERIOD_INDEX"]].rename(columns={"PERIOD_INDEX": "MU_PERIOD_INDEX"})
    candidate = calc_attempts.merge(mu_key, on="STUDENT_ID", how="inner")
    candidate = candidate.loc[candidate["PERIOD_INDEX"] > candidate["MU_PERIOD_INDEX"]].copy()
    first_follow = (
        candidate.sort_values(["STUDENT_ID", "PERIOD_INDEX"], kind="stable")
        .drop_duplicates(["STUDENT_ID"], keep="first")
        .drop(columns=["MU_PERIOD_INDEX"])
    )
    first_follow = attach_visits(first_follow, advisories, threshold=config.ppa_threshold)
    first_follow["CALC_VISIT_COVERAGE"] = [
        (int(y), s) in coverage for y, s in zip(first_follow["YEAR"], first_follow["SESSION"])
    ]

    mu_follow_cols = [
        "STUDENT_ID", "YEAR", "SESSION", "PERIOD_INDEX", "PERIOD_LABEL",
        "VISITS_COURSE", "VISITS_CMAT_PERIOD", "VISIT_GROUP_COURSE",
        "VISIT_GROUP_PERIOD", "PPA_REACHED_COURSE", "PPA_REACHED_PERIOD",
        "PERSISTENT_GT3_COURSE", "PERSISTENT_GT3_PERIOD", "VISIT_COVERAGE",
    ]
    mu_follow = mu_all[mu_follow_cols].rename(columns={
        "YEAR": "MU_YEAR",
        "SESSION": "MU_SESSION",
        "PERIOD_INDEX": "MU_PERIOD_INDEX",
        "PERIOD_LABEL": "MU_PERIOD_LABEL",
        "VISITS_COURSE": "MU_VISITS_COURSE",
        "VISITS_CMAT_PERIOD": "MU_VISITS_CMAT_PERIOD",
        "VISIT_GROUP_COURSE": "MU_VISIT_GROUP_COURSE",
        "VISIT_GROUP_PERIOD": "MU_VISIT_GROUP_PERIOD",
        "PPA_REACHED_COURSE": "MU_PPA_REACHED_COURSE",
        "PPA_REACHED_PERIOD": "MU_PPA_REACHED_PERIOD",
        "PERSISTENT_GT3_COURSE": "MU_PERSISTENT_GT3_COURSE",
        "PERSISTENT_GT3_PERIOD": "MU_PERSISTENT_GT3_PERIOD",
        "VISIT_COVERAGE": "MU_VISIT_COVERAGE",
    })
    longitudinal = first_follow.merge(mu_follow, on="STUDENT_ID", how="inner")
    longitudinal["CALC_ANY_VISIT_COURSE"] = (longitudinal["VISITS_COURSE"] > 0).astype(int)
    longitudinal["CALC_ANY_VISIT_PERIOD"] = (longitudinal["VISITS_CMAT_PERIOD"] > 0).astype(int)
    longitudinal["ACADEMIC_TERM_LAG"] = longitudinal["PERIOD_INDEX"] - longitudinal["MU_PERIOD_INDEX"]
    # Backward-compatible alias; one index step = one of Primavera/Verano/Otoño.
    longitudinal["SEMESTER_LAG"] = longitudinal["ACADEMIC_TERM_LAG"]

    progressed_ids = set(first_follow["STUDENT_ID"].astype(str))
    mu_all["PROGRESSED_TO_CALC"] = mu_all["STUDENT_ID"].astype(str).isin(progressed_ids).astype(int)
    mu_primary["PROGRESSED_TO_CALC"] = mu_primary["STUDENT_ID"].astype(str).isin(progressed_ids).astype(int)

    return {
        "mu_all_first_attempts": mu_all,
        "mu_primary": mu_primary,
        "calc_comparator": calc_comparator,
        "longitudinal": longitudinal,
    }
