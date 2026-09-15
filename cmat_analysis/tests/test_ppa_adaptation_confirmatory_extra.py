"""Tests for reduced-dimensional confirmatory adaptation models."""

import numpy as np
import pandas as pd

from cmat_analysis.ppa.adaptation_confirmatory_extra import (
    career_heterogeneity_reduced_interactions,
    post_failure_numeric_severity_models,
)


def test_career_interaction_models_reduce_dimension_as_threshold_rises() -> None:
    rows = []
    careers = ["A", "B", "C", "D"]
    for i in range(240):
        career = careers[i % 4]
        rows.append({
            "MU_FIRST_CMAT_VISITS": int(i % 5 == 0),
            "MU_FIRST_Z": (-1.0 if i % 3 == 0 else 0.2) + (i % 7) / 100,
            "MU_FIRST_LOO_PASS_RATE": 0.45 if i % 4 == 0 else 0.8,
            "MU_FIRST_CAREER": career,
            "MU_FIRST_PERIOD_LABEL": f"P{i % 6}",
            "MU_FIRST_CLASSROOM_ID": f"C{i % 30}",
        })
    out = career_heterogeneity_reduced_interactions(
        pd.DataFrame(rows), min_career_ns=(20, 70)
    )
    assert out.shape[0] == 2
    assert out.loc[out["min_career_n"].eq(70), "career_levels"].iloc[0] <= out.loc[
        out["min_career_n"].eq(20), "career_levels"
    ].iloc[0]
    assert (out["interaction_df_per_cluster"] >= 0).all()


def test_numeric_failure_severity_models_report_prior_z() -> None:
    rows = []
    for i in range(120):
        z = -0.2 - (i % 10) / 10
        previous_rank = (i % 8 + 1) / 10
        delta = 0.15 if i % 3 else -0.10
        rows.append({
            "STUDENT_ID": f"S{i // 2}",
            "FAILED_ATTEMPT_NUMBER": 1 if i < 80 else 2,
            "PREV_PERIOD_INDEX": 1 + i % 3,
            "CAREER": "A" if i < 60 else "B",
            "PREV_Z": z,
            "PREV_ANY_CMAT": int(i % 4 == 0),
            "NEXT_ANY_CMAT": int(i % 4 == 0 or i % 7 == 0),
            "PREV_CMAT_VISITS": int(i % 4 == 0),
            "NEXT_CMAT_VISITS": int(i % 4 == 0) + int(i % 7 == 0),
            "PREV_PROF_EASINESS_PERCENTILE": previous_rank,
            "DELTA_PROF_EASINESS_PERCENTILE": delta,
        })
    out = post_failure_numeric_severity_models(pd.DataFrame(rows), min_career_n=10)
    assert set(out["model"]) == {
        "higher_outcome_percentile",
        "next_cmat_use",
        "increased_cmat",
    }
    assert (out.groupby("model")["term"].apply(lambda s: "_PREV_Z" in set(s))).all()
    assert np.isfinite(out.loc[out["term"].eq("_PREV_Z"), "estimate"]).all()
