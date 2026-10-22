"""Synthetic, privacy-safe tests for the three follow-up questions."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from run_paper21_model_controls_experiment import prepare_cohort
from run_paper21_followup_questions import (
    _coarse_group,
    numeric_grade_distribution,
    overlap_diagnostics,
    render_report,
    two_part_attendance,
)


def synthetic() -> pd.DataFrame:
    rng = np.random.default_rng(2382)
    rows = []
    for classroom in range(12):
        for visit in range(8):
            for rep in range(5):
                degree = "MATH" if rep % 2 else "OTHER"
                z = (0.15 * (visit > 0) + 0.045 * max(min(visit, 7) - 1, 0)
                     + 0.12 * (degree == "MATH") + rng.normal(0, 0.7))
                prob = np.clip(.55 + .07*(visit > 0)
                               + .02*max(visit-1, 0)
                               + .03*(degree == "MATH"), .05, .95)
                adverse = bool(rng.random() < .13)
                grade = np.nan if adverse else float(
                    np.clip(7.5 + z * 1.4, 0, 10)
                )
                passed = 0 if adverse else int(grade >= 7.5)
                rows.append(dict(CLASSROOM_ID=f"GROUP-{classroom}",
                                 CLAVECARRERA=degree, VISITS_CMAT_PERIOD=visit,
                                 Z_GRADE_PRIMARY=z, PASS=passed,
                                 GRADE_NUMERIC=grade,
                                 GRADE_CLASS="adverse" if adverse else "numeric"))
    return pd.DataFrame(rows)


def test_coarse_groups_and_topcoding():
    got = _coarse_group(pd.Series([0, 1, 2, 6, 7, 15])).tolist()
    assert got == ["0", "1", "2-6", "2-6", "7+", "7+"]
    try:
        _coarse_group(pd.Series([-1]))
    except ValueError:
        pass
    else:
        raise AssertionError("Negative visits must be rejected")


def test_degree_overlap_within_mixed_professor_periods():
    frame = prepare_cohort(synthetic(), outcome_col="Z_GRADE_PRIMARY")
    frame.attrs["audit"] = pd.DataFrame({"nested": [1, 2]})
    result = overlap_diagnostics(frame).iloc[0]
    assert result.n_professor_period == 12
    assert result.n_mixed_professor_period == 12
    assert result.n_students_in_mixed_contexts == len(frame)
    assert result.status == "descriptive_fit_only"
    assert result.incremental_r2_degree_mixed >= -1e-10


def test_single_degree_context_does_not_claim_partial_identification():
    data = synthetic()
    data["CLAVECARRERA"] = data["CLASSROOM_ID"].map(
        lambda value: "DEG-" + str(value))
    cohort = prepare_cohort(data, outcome_col="Z_GRADE_PRIMARY")
    result = overlap_diagnostics(cohort).iloc[0]
    assert result.n_mixed_professor_period == 0
    assert result.status == "insufficient_mixed_contexts"
    assert pd.isna(result.incremental_r2_degree_mixed)


def test_attendance_hurdle_ols_with_clustered_inference():
    d = synthetic()
    d.attrs["imputation_summary"] = pd.DataFrame({"nested": [1, 2]})
    z = two_part_attendance(d, "Z_GRADE_PRIMARY")
    passed = two_part_attendance(d, "PASS")
    assert set(z.term) == {"ANY_VISIT", "EXTRA_VISITS_CAPPED_7"}
    assert set(passed.term) == set(z.term)
    for out in (z, passed):
        assert out["clusters"].eq(12).all()
        assert out["n"].eq(len(d)).all()
        assert out["p_holm_within_two_term_family"].between(0, 1).all()
        assert (out["ci95_low"] < out["ci95_high"]).all()


def test_numeric_grades_exclude_adverse_and_report_full_population():
    d = synthetic()
    d.attrs["imputation_summary"] = pd.DataFrame({"nested": [1, 2]})
    grade, composition = numeric_grade_distribution(d)
    assert grade["group"].tolist() == ["0", "1", "2-6", "7+"]
    assert int(composition["n_all_outcomes"].sum()) == len(d)
    assert int(composition["n_numeric"].sum()) == int(
        d["GRADE_CLASS"].eq("numeric").sum())
    assert int(composition["n_adverse"].sum()) == int(
        d["GRADE_CLASS"].eq("adverse").sum())
    assert ((grade["numeric_median"] >= grade["numeric_p10"])
            & (grade["numeric_median"] <= grade["numeric_p90"])).all()
    assert grade["numeric_share_within_half_point_of_7p5"].between(0, 1).all()


def test_generated_report_avoids_student_or_professor_identifiers():
    d = synthetic()
    mix = overlap_diagnostics(prepare_cohort(d, outcome_col="Z_GRADE_PRIMARY"))
    estimates = pd.concat([two_part_attendance(d, "PASS"),
                           two_part_attendance(d, "Z_GRADE_PRIMARY")])
    grade, composition = numeric_grade_distribution(d)
    note = render_report(mix, estimates, grade, composition)
    assert "ANY_VISIT" in note
    assert "numeric" in note.lower()
    assert "GROUP-" not in note
    assert "DEG-" not in note
