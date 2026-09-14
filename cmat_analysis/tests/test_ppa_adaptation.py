"""Tests for MU-to-Calculus adaptation helpers."""

import numpy as np
import pandas as pd

from cmat_analysis.ppa import (
    instructor_choice_percentiles,
    repeat_attempt_summary,
    strict_prior_instructor_context,
)


def test_strict_prior_instructor_context_excludes_current_and_future_periods() -> None:
    rows = []
    for period in range(1, 5):
        for i in range(10):
            rows.append({
                "professor": "P1",
                "period": period,
                "grade": 7.0 + period * 0.2,
                "passed": int(i < period + 4),
            })
    d = pd.DataFrame(rows)
    out = strict_prior_instructor_context(
        d,
        instructor_col="professor",
        period_index_col="period",
        grade_col="grade",
        pass_col="passed",
        min_history_n=10,
        prefix="HIST",
    )
    p1 = out.loc[out["period"].eq(1)].iloc[0]
    p2 = out.loc[out["period"].eq(2)].iloc[0]
    p4 = out.loc[out["period"].eq(4)].iloc[0]
    assert p1["HIST_ATTEMPT_N"] == 0
    assert np.isnan(p1["HIST_PASS_RATE"])
    assert p2["HIST_ATTEMPT_N"] == 10
    assert np.isclose(p2["HIST_PASS_RATE"], 0.5)
    assert p4["HIST_ATTEMPT_N"] == 30
    assert np.isclose(p4["HIST_PASS_RATE"], (5 + 6 + 7) / 30)


def test_instructor_choice_percentiles_rank_only_within_period() -> None:
    d = pd.DataFrame({
        "professor": ["A", "B", "C", "A", "B", "C"],
        "period": [1, 1, 1, 2, 2, 2],
        "pass_rate": [0.5, 0.7, 0.9, 0.9, 0.5, 0.7],
        "mean_grade": [7.0, 8.0, 9.0, 9.0, 7.0, 8.0],
    })
    out = instructor_choice_percentiles(
        d,
        instructor_col="professor",
        period_index_col="period",
        pass_rate_col="pass_rate",
        mean_grade_col="mean_grade",
        prefix="RANK",
    )
    p1 = out.loc[out["period"].eq(1)].set_index("professor")
    p2 = out.loc[out["period"].eq(2)].set_index("professor")
    assert np.isclose(p1.loc["C", "RANK_EASINESS_PERCENTILE"], 1.0)
    assert np.isclose(p1.loc["A", "RANK_EASINESS_PERCENTILE"], 1 / 3)
    assert np.isclose(p2.loc["A", "RANK_EASINESS_PERCENTILE"], 1.0)
    assert set(out["RANK_ELIGIBLE_INSTRUCTORS"]) == {3}


def test_repeat_attempt_summary_tracks_post_failure_changes() -> None:
    transitions = pd.DataFrame({
        "FAILED_ATTEMPT_NUMBER": [1, 1, 2],
        "CHANGED_PROFESSOR": [1, 0, 1],
        "PREV_ANY_CMAT": [0, 1, 1],
        "NEXT_ANY_CMAT": [1, 1, 1],
        "DELTA_CMAT_VISITS": [2, 1, 0],
        "NEXT_ATTEMPT_PASS": [1, 0, 1],
        "DELTA_PROF_EASINESS_PERCENTILE": [0.25, -0.10, 0.30],
    })
    out = repeat_attempt_summary(transitions)
    first = out.loc[out["failed_attempt_number"].eq(1)].iloc[0]
    assert first["n_transitions"] == 2
    assert np.isclose(first["professor_change_rate"], 0.5)
    assert np.isclose(first["prev_cmat_use_rate"], 0.5)
    assert np.isclose(first["next_cmat_use_rate"], 1.0)
    assert np.isclose(first["next_attempt_pass_rate"], 0.5)
