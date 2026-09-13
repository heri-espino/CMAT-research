"""Tests for PPA classroom-outcome and degree-programme context helpers."""

from types import SimpleNamespace

import numpy as np
import pandas as pd

from cmat_analysis.ppa import (
    academic_context_uptake_models,
    build_mu_classroom_outcome_context,
    leave_period_out_professor_academic_context,
    major_uptake_increment,
    major_visit_group_multinomial_increment,
    major_visit_group_summary,
)


def _academic_rows() -> pd.DataFrame:
    grades = [9.0, 8.0, 7.0, 6.0, np.nan, 10.0]
    classes = ["numeric", "numeric", "numeric", "numeric", "adverse", "numeric"]
    tokens = ["9", "8", "7", "6", "NP", "10"]
    return pd.DataFrame({
        "STUDENT_ID": [f"S{i}" for i in range(6)],
        "SUBJECT_CODE": ["MU"] * 6,
        "SUBJECT": ["MATEMATICAS UNIVERSITARIAS"] * 6,
        "PERIOD_INDEX": [1] * 6,
        "SOURCE_ROW": list(range(6)),
        "GRADE_CLASS": classes,
        "GRADE_NUMERIC": grades,
        "GRADE_TOKEN": tokens,
        "YEAR": [2025] * 6,
        "SESSION": ["OTONO"] * 6,
        "PERIOD_LABEL": ["2025-OTONO"] * 6,
        "CLAVEPROFESOR": ["P1"] * 6,
        "CLAVECARRERA": ["LAT", "LAT", "LAT", "LID", "LID", "LID"],
    })


def test_build_mu_classroom_context_counts_all_real_attempts() -> None:
    data = SimpleNamespace(academics=_academic_rows())
    config = SimpleNamespace(
        passing_grade=7.5,
        primary_subject_code="MU",
        primary_subject_name="MATEMATICAS UNIVERSITARIAS",
    )
    out = build_mu_classroom_outcome_context(data, config, min_classroom_n=2)
    first = out.loc[out["SOURCE_ROW"].eq(0)].iloc[0]
    assert int(first["MU_CLASSROOM_ATTEMPT_N"]) == 6
    assert int(first["MU_CLASSROOM_NUMERIC_N"]) == 5
    assert int(first["MU_CLASSROOM_ADVERSE_N"]) == 1
    assert np.isclose(first["MU_CLASSROOM_MEAN_GRADE"], 8.0)
    assert np.isclose(first["MU_CLASSROOM_PASS_RATE"], 0.5)
    assert np.isclose(first["MU_LOO_CLASSROOM_PASS_RATE"], 0.4)
    assert np.isclose(first["MU_LOO_CLASSROOM_MEAN_GRADE"], 7.75)


def test_leave_period_out_academic_context_excludes_current_period() -> None:
    d = pd.DataFrame({
        "prof": ["A"] * 6,
        "period": ["P1"] * 3 + ["P2"] * 3,
        "grade": [9.0, 8.0, 7.0, 6.0, 5.0, 4.0],
        "passed": [1, 1, 0, 0, 0, 0],
    })
    out = leave_period_out_professor_academic_context(
        d,
        professor_col="prof",
        period_col="period",
        grade_col="grade",
        pass_col="passed",
        min_other_n=2,
        prefix="HIST",
    )
    p1 = out.loc[out["period"].eq("P1")].iloc[0]
    p2 = out.loc[out["period"].eq("P2")].iloc[0]
    assert np.isclose(p1["HIST_LEAVE_PERIOD_OUT_PASS_RATE"], 0.0)
    assert np.isclose(p1["HIST_LEAVE_PERIOD_OUT_MEAN_GRADE"], 5.0)
    assert np.isclose(p2["HIST_LEAVE_PERIOD_OUT_PASS_RATE"], 2 / 3)
    assert np.isclose(p2["HIST_LEAVE_PERIOD_OUT_MEAN_GRADE"], 8.0)


def _major_data(seed: int = 17, n: int = 800) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    major = rng.choice(["LAT", "LID", "LAF"], size=n, p=[0.25, 0.40, 0.35])
    professor = rng.choice(["P1", "P2", "P3", "P4"], size=n)
    period = rng.choice(["T1", "T2", "T3"], size=n)
    p = np.where(major == "LAT", 0.42, np.where(major == "LID", 0.22, 0.15))
    any_use = rng.binomial(1, p)
    visit_group = []
    visits = []
    for used in any_use:
        if not used:
            visit_group.append("0")
            visits.append(0)
        else:
            g = rng.choice(["1-2", "3", "4+"], p=[0.55, 0.20, 0.25])
            visit_group.append(g)
            visits.append({"1-2": 1, "3": 3, "4+": 5}[g])
    context = rng.normal(size=n) + 0.25 * any_use
    return pd.DataFrame({
        "MU_CAREER_OFFICIAL": major,
        "MU_PROFESSOR": professor,
        "MU_PERIOD_LABEL": period,
        "MU_ANY_VISIT": any_use,
        "MU_VISIT_GROUP": visit_group,
        "MU_VISITS_CMAT_PERIOD": visits,
        "context": context,
    })


def test_major_summary_and_increment_detect_programme_heterogeneity() -> None:
    d = _major_data()
    summary = major_visit_group_summary(d, min_n=30)
    rates = summary.set_index("MU_CAREER_OFFICIAL")["any_use_rate"]
    assert rates["LAT"] > rates["LID"] > rates["LAF"]
    binary = major_uptake_increment(d, min_major_n=30)
    multinomial = major_visit_group_multinomial_increment(d, min_major_n=30)
    assert np.isfinite(binary.loc[0, "joint_f_major"])
    assert binary.loc[0, "joint_p_major"] < 0.05
    assert np.isfinite(multinomial.loc[0, "lr_stat_major"])


def test_academic_context_models_return_standardized_coefficients() -> None:
    d = _major_data()
    out = academic_context_uptake_models(
        d,
        outcome_col="MU_ANY_VISIT",
        context_cols=["context"],
        period_col="MU_PERIOD_LABEL",
        major_col="MU_CAREER_OFFICIAL",
        professor_col="MU_PROFESSOR",
        min_major_n=30,
    )
    assert set(out["specification"]) == {
        "period_major",
        "period_major_professor_fe",
    }
    assert out["estimate_per_sd"].notna().all()
