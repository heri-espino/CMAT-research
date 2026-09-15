"""Tests for confirmatory engagement-adaptation helpers."""

import numpy as np
import pandas as pd

from cmat_analysis.ppa.adaptation_audit import (
    attach_observed_choice_set_size,
    augment_repeat_transition_context,
)
from cmat_analysis.ppa.adaptation_confirmatory import (
    administrative_choice_constraint_audit,
    choice_set_audit,
    classify_experience_state,
    experience_state_sensitivity,
    post_failure_response_models,
)


def test_classify_experience_state_separates_individual_and_contextual_strain() -> None:
    d = pd.DataFrame({
        "MU_FIRST_Z": [0.1, 0.2, -1.0, -1.0, np.nan],
        "MU_FIRST_LOO_PASS_RATE": [0.9, 0.4, 0.9, 0.4, 0.4],
    })
    state = classify_experience_state(d, performance_cut=-0.5, difficulty_quantile=0.4)
    assert state.tolist() == [
        "lower_strain",
        "contextual_challenge",
        "individual_strain",
        "compounded_strain",
        "adverse_or_nonnumeric",
    ]


def test_experience_state_sensitivity_returns_predefined_grid() -> None:
    d = pd.DataFrame({
        "STUDENT_ID": [f"S{i}" for i in range(12)],
        "MU_FIRST_Z": np.linspace(-1.5, 1.5, 12),
        "MU_FIRST_LOO_PASS_RATE": np.linspace(0.4, 0.95, 12),
        "MU_FIRST_CMAT_VISITS": [0, 1, 0, 2, 0, 0, 1, 0, 3, 0, 4, 0],
        "MU_EVER_PASSED": [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    })
    out = experience_state_sensitivity(
        d,
        later_calc_student_ids={"S5", "S6", "S7"},
        performance_cuts=(-0.5, -1.0),
        difficulty_quantiles=(0.25, 0.5),
    )
    assert out[["performance_cut", "difficulty_quantile"]].drop_duplicates().shape[0] == 4
    assert set(out["state"]).issubset({
        "lower_strain",
        "contextual_challenge",
        "individual_strain",
        "compounded_strain",
        "adverse_or_nonnumeric",
        "unknown_context",
    })


def test_choice_set_audit_uses_observed_and_rankable_counts() -> None:
    d = pd.DataFrame({
        "CALC_FIRST_PERIOD_LABEL": ["P1", "P1", "P2"],
        "CALC_CHOICE_SET_OBSERVED_N": [4, 4, 3],
        "CALC_CHOICE_SET_RANKABLE_N": [3, 3, 2],
        "CALC_CHOSEN_EASINESS_PERCENTILE": [0.2, 0.8, np.nan],
    })
    out = choice_set_audit(d)
    metric = out.set_index(["level", "metric"])["value"]
    assert np.isclose(metric.loc[("student", "chosen_instructor_rankable_share")], 2 / 3)
    assert metric.loc[("period", "observed_instructors_median")] == 3.5


def test_augment_repeat_transition_context_adds_absolute_history_changes() -> None:
    transitions = pd.DataFrame({
        "STUDENT_ID": ["S1"],
        "FAILED_ATTEMPT_NUMBER": [1],
        "NEXT_ATTEMPT_NUMBER": [2],
    })
    attempts = pd.DataFrame({
        "STUDENT_ID": ["S1", "S1"],
        "MU_ATTEMPT_NUMBER": [1, 2],
        "MU_PROF_PRIOR_PASS_RATE": [0.5, 0.7],
        "MU_PROF_PRIOR_MEAN_GRADE": [7.0, 8.0],
    })
    out = augment_repeat_transition_context(transitions, attempts).iloc[0]
    assert np.isclose(out["DELTA_PROF_PRIOR_PASS_RATE"], 0.2)
    assert np.isclose(out["DELTA_PROF_PRIOR_MEAN_GRADE"], 1.0)


def test_attach_observed_choice_set_size_is_many_to_one() -> None:
    choices = pd.DataFrame({"CALC_FIRST_PERIOD_INDEX": [1, 1, 2], "x": [1, 2, 3]})
    counts = pd.DataFrame({"PERIOD_INDEX": [1, 2], "OBSERVED_INSTRUCTOR_N": [4, 3]})
    out = attach_observed_choice_set_size(choices, counts)
    assert out["CALC_CHOICE_SET_OBSERVED_N"].tolist() == [4, 4, 3]


def test_administrative_choice_constraint_audit_finds_schedule_but_not_capacity() -> None:
    d = pd.DataFrame(columns=["STUDENT_ID", "SECTION", "START_TIME", "GRADE"])
    out = administrative_choice_constraint_audit(d).set_index("constraint_category")
    assert bool(out.loc["section_identifier", "field_available"])
    assert bool(out.loc["schedule_time", "field_available"])
    assert not bool(out.loc["capacity", "field_available"])


def test_post_failure_response_models_runs_clustered_lpm() -> None:
    rows = []
    for i in range(80):
        previous_rank = (i % 10 + 1) / 11
        delta = 0.15 if i % 3 else -0.10
        rows.append({
            "STUDENT_ID": f"S{i // 2}",
            "FAILED_ATTEMPT_NUMBER": 1 if i < 50 else 2,
            "PREV_PERIOD_INDEX": 1 if i % 2 else 2,
            "CAREER": "A" if i < 40 else "B",
            "PREV_ANY_CMAT": int(i % 4 == 0),
            "NEXT_ANY_CMAT": int(i % 5 == 0 or i % 4 == 0),
            "PREV_CMAT_VISITS": int(i % 4 == 0),
            "NEXT_CMAT_VISITS": int(i % 5 == 0) + int(i % 4 == 0),
            "PREV_PROF_EASINESS_PERCENTILE": previous_rank,
            "DELTA_PROF_EASINESS_PERCENTILE": delta,
            "PREV_PROF_PRIOR_PASS_RATE": 0.5 + previous_rank / 4,
            "DELTA_PROF_PRIOR_PASS_RATE": 0.05 if delta > 0 else -0.03,
            "PREV_PROF_PRIOR_MEAN_GRADE": 7.0 + previous_rank,
            "DELTA_PROF_PRIOR_MEAN_GRADE": 0.4 if delta > 0 else -0.2,
        })
    out = post_failure_response_models(pd.DataFrame(rows), min_career_n=10)
    assert {"higher_outcome_percentile", "next_cmat_use", "increased_cmat"}.issubset(set(out["model"]))
