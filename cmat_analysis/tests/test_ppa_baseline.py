"""Tests for the unselected PPA MU baseline cohort."""

from types import SimpleNamespace

import pandas as pd

from cmat_analysis.cohorts import StudyData, period_index
from cmat_analysis.ppa import build_ppa_mu_baseline_cohort


def test_ppa_mu_baseline_does_not_require_later_calculus_progression() -> None:
    academics = pd.DataFrame({
        "STUDENT_ID": ["a", "b", "c"],
        "CLAVECARRERA": ["A", "B", "C"],
        "SUBJECT_CODE": ["MAT1012"] * 3,
        "SUBJECT": ["MATEMATICAS UNIVERSITARIAS"] * 3,
        "YEAR": [2024] * 3,
        "SESSION": ["PRIMAVERA"] * 3,
        "PERIOD_INDEX": [period_index(2024, "PRIMAVERA")] * 3,
        "SOURCE_ROW": [0, 1, 2],
        "GRADE_CLASS": ["numeric", "numeric", "numeric"],
        "GRADE_NUMERIC": [8.5, 9.0, 7.0],
        "GRADE_TOKEN": ["8.5", "9", "7"],
        "CLAVEPROFESOR": ["P1", "P2", "P3"],
    })
    advisories = pd.DataFrame({
        "STUDENT_ID": ["a", "a", "a"],
        "YEAR": [2024, 2024, 2024],
        "SESSION": ["PRIMAVERA", "PRIMAVERA", "PRIMAVERA"],
        "SUBJECT": ["MATEMATICAS UNIVERSITARIAS"] * 3,
    })
    coverage = pd.DataFrame({
        "YEAR": [2024],
        "SESSION": ["PRIMAVERA"],
    })
    data = StudyData(
        academics=academics,
        advisories=advisories,
        data_quality={"coverage": coverage},
    )
    config = SimpleNamespace(
        passing_grade=7.5,
        primary_subject_code="MAT1012",
        primary_subject_name="MATEMATICAS UNIVERSITARIAS",
        ppa_threshold=3,
    )

    baseline = build_ppa_mu_baseline_cohort(data, config)

    assert baseline["STUDENT_ID"].tolist() == ["a", "b"]
    assert baseline.set_index("STUDENT_ID").loc["a", "MU_VISIT_GROUP"] == "3"
    assert baseline.set_index("STUDENT_ID").loc["b", "MU_VISIT_GROUP"] == "0"
    assert "MU_PROFESSOR" in baseline.columns
