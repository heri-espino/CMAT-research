"""Synthetic-only tests: grouped Shapley fit and professor-period holdout."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from run_paper21_model_controls_experiment import prepare_cohort
from run_paper21_shapley_importance import (
    CV_BLOCKS, MODEL_BLOCKS, coalitions, cross_validated_shapley,
    cross_validated_value, in_sample_shapley, in_sample_value, shapley,
)


def sample():
    rng = np.random.default_rng(528)
    rows = []
    for classroom in range(20):
        for visits in range(8):
            for rep in range(5):
                degree = "A" if rep % 2 else "B"
                score = (.11 * visits + .5 * (degree == "A")
                         + .02 * (classroom % 3) + rng.normal(0, .6))
                chance = 1 / (1 + np.exp(-(-1 + .2 * visits
                                          + .2 * (degree == "A"))))
                rows.append(dict(CLASSROOM_ID=f"C{classroom}",
                                 CLAVECARRERA=degree,
                                 VISITS_CMAT_PERIOD=visits,
                                 Z_GRADE_PRIMARY=score,
                                 PASS=int(rng.random() < chance)))
    return pd.DataFrame(rows)


def test_two_block_shapley_exact_values():
    values = {(): 0, ("attendance",): .10, ("degree",): .20,
              ("attendance", "degree"): .25}
    contrib = shapley(("attendance", "degree"), values)
    assert np.isclose(contrib["attendance"], .075)
    assert np.isclose(contrib["degree"], .175)
    assert np.isclose(sum(contrib.values()), .25)


def test_all_models_have_exact_additive_importance_without_expanding_categories():
    d = prepare_cohort(sample(), outcome_col="Z_GRADE_PRIMARY")
    imp, coal = in_sample_shapley(d, "Z_GRADE_PRIMARY", "Z_OLS",
                                   "r2_in_sample")
    assert len(imp) == sum(len(x) for x in MODEL_BLOCKS.values()) == 8
    assert len(coal) == 7
    assert imp["status"].eq("valid").all()
    for code, subset in MODEL_BLOCKS.items():
        frame = imp.loc[imp["model"].eq(code)]
        assert set(frame["block"]) == set(subset)
        assert np.isclose(frame["contribution"].sum(),
                          frame["model_score"].iloc[0], atol=1e-10)
        assert np.isclose(frame["share_of_model"].sum(), 1, atol=1e-10)


def test_logistic_importance_is_pseudo_r2_not_ols_r2():
    d = prepare_cohort(sample())
    v = in_sample_value(d, "PASS", "PASS_LOGIT", ("attendance",))
    assert 0 < v < 1


def test_group_holdout_is_additive_and_baseline_is_zero():
    d = prepare_cohort(sample(), outcome_col="Z_GRADE_PRIMARY")
    assert cross_validated_value(d, "Z_GRADE_PRIMARY", ()) == 0
    imp, scores = cross_validated_shapley(d, "Z_GRADE_PRIMARY")
    assert len(scores) == len(list(coalitions(CV_BLOCKS))) == 4
    assert len(imp) == 2
    assert np.isclose(imp["contribution"].sum(),
                      imp["model_score"].iloc[0], atol=1e-9)


def test_pass_prediction_uses_brier_skill_not_pseudo_r2():
    d = prepare_cohort(sample())
    imp, scores = cross_validated_shapley(d, "PASS")
    assert scores["metric"].eq("out_of_context_brier_skill").all()
    assert np.isclose(imp["contribution"].sum(),
                      imp["model_score"].iloc[0], atol=1e-9)


def test_group_holdout_with_dataframe_metadata_on_source():
    """Regression: pandas 3 cannot compare DataFrames stored in .attrs."""
    d = prepare_cohort(sample(), outcome_col="Z_GRADE_PRIMARY")
    d.attrs["upstream_source"] = pd.DataFrame({"extra": [1, 2]})
    # Earlier multi-column .astype(str) raised an ambiguous-truth-value
    # ValueError during internal Series concatenation.
    for players in ((), ("attendance",), ("degree",), CV_BLOCKS):
        score = cross_validated_value(d, "Z_GRADE_PRIMARY", players)
        assert np.isfinite(score)

def test_pass_group_holdout_with_dataframe_metadata_on_source():
    """PASS logistic predictions must also work with attached source metadata."""
    d = prepare_cohort(sample())
    d.attrs["upstream_source"] = pd.DataFrame({"extra": [1, 2]})
    importance, scores = cross_validated_shapley(d, "PASS")
    assert len(importance) == 2
    assert scores["score"].notna().all()
