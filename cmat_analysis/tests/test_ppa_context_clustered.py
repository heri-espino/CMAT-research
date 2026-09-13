"""Tests for cluster-robust PPA academic-context inference."""

import numpy as np
import pandas as pd

from cmat_analysis.ppa import clustered_academic_context_uptake_models


def test_clustered_context_models_report_cluster_counts() -> None:
    rng = np.random.default_rng(2026)
    rows = []
    for classroom in range(40):
        context = rng.normal()
        professor = f"P{classroom % 8}"
        period = f"T{classroom % 4}"
        major = "LAT" if classroom % 3 == 0 else "OTHER"
        for _ in range(20):
            probability = 1.0 / (1.0 + np.exp(-(-1.4 - 0.35 * context)))
            rows.append({
                "outcome": rng.binomial(1, probability),
                "context": context,
                "period": period,
                "major": major,
                "professor": professor,
                "classroom": f"C{classroom}",
            })
    d = pd.DataFrame(rows)
    out = clustered_academic_context_uptake_models(
        d,
        outcome_col="outcome",
        context_cols=["context"],
        period_col="period",
        cluster_col="classroom",
        major_col="major",
        professor_col="professor",
        min_major_n=30,
    )
    assert set(out["specification"]) == {
        "period_major",
        "period_major_professor_fe",
    }
    assert set(out["clusters"]) == {40}
    assert out["se_cluster"].gt(0).all()
    assert out["estimate_per_sd"].notna().all()
