"""Regression test for using instructor as both cluster and fixed effect."""

import numpy as np
import pandas as pd

from cmat_analysis.ppa import clustered_academic_context_uptake_models


def test_professor_can_be_cluster_and_fixed_effect() -> None:
    rng = np.random.default_rng(73)
    rows = []
    for professor_index in range(12):
        professor = f"P{professor_index}"
        context = rng.normal()
        for period_index in range(4):
            for _ in range(15):
                rows.append({
                    "outcome": rng.binomial(1, 0.2),
                    "context": context + 0.1 * period_index,
                    "period": f"T{period_index}",
                    "major": "LAT" if professor_index % 2 == 0 else "OTHER",
                    "professor": professor,
                })
    d = pd.DataFrame(rows)
    out = clustered_academic_context_uptake_models(
        d,
        outcome_col="outcome",
        context_cols=["context"],
        period_col="period",
        cluster_col="professor",
        major_col="major",
        professor_col="professor",
        min_major_n=30,
    )
    assert len(out) == 2
    assert set(out["clusters"]) == {12}
    assert out["se_cluster"].notna().all()
