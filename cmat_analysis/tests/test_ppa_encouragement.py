"""Tests for reusable instructor-linked uptake and familiarity helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd

from cmat_analysis.ppa import (
    familiarization_professor_persistence_models,
    leave_period_out_professor_propensity,
    professor_familiarization_interaction_model,
    professor_uptake_increment,
    professor_visit_group_distribution,
    professor_visit_group_multinomial_increment,
)


def _synthetic_progression(seed: int = 2026, n: int = 1600) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    professors = np.array([f"P{i:02d}" for i in range(12)])
    periods = np.array([f"T{i}" for i in range(6)])
    groups = np.array(["0", "1-2", "3", "4+"])
    d = pd.DataFrame({
        "CALC_PROFESSOR": rng.choice(professors, size=n),
        "CALC_PERIOD_LABEL": rng.choice(periods, size=n),
        "CALC_CAREER_OFFICIAL": rng.choice(["A", "B", "C", "D"], size=n),
        "Z_MU": rng.normal(size=n),
        "MU_VISIT_GROUP": rng.choice(groups, size=n, p=[0.60, 0.20, 0.10, 0.10]),
    })
    professor_shift = d["CALC_PROFESSOR"].map(
        {p: i * 0.006 for i, p in enumerate(professors)}
    ).to_numpy()
    familiarity_shift = d["MU_VISIT_GROUP"].map(
        {"0": 0.00, "1-2": 0.05, "3": 0.09, "4+": 0.12}
    ).to_numpy()
    prob = np.clip(0.08 + professor_shift + familiarity_shift, 0.01, 0.70)
    d["CALC_ANY_VISIT"] = (rng.random(n) < prob).astype(int)
    return d


def test_professor_visit_group_distribution_preserves_four_groups() -> None:
    d = _synthetic_progression()
    out = professor_visit_group_distribution(
        d,
        professor_col="CALC_PROFESSOR",
        group_col="MU_VISIT_GROUP",
        min_professor_n=30,
    )
    assert len(out) == 12
    assert {"share_0", "share_1_2", "share_3", "share_4plus"}.issubset(out.columns)
    shares = out[["share_0", "share_1_2", "share_3", "share_4plus"]].sum(axis=1)
    assert np.allclose(shares, 1.0)


def test_leave_period_out_propensity_excludes_current_period() -> None:
    d = pd.DataFrame({
        "prof": ["A", "A", "A", "A", "A", "A"],
        "period": ["T1", "T1", "T2", "T2", "T3", "T3"],
        "use": [1, 1, 0, 0, 1, 0],
    })
    out = leave_period_out_professor_propensity(
        d,
        professor_col="prof",
        period_col="period",
        outcome_col="use",
        min_other_n=1,
        prefix="X",
    )
    assert np.allclose(
        out.loc[out["period"].eq("T1"), "X_LEAVE_PERIOD_OUT_RATE"],
        0.25,
    )
    assert (out.loc[out["period"].eq("T1"), "X_LEAVE_PERIOD_OUT_N"] == 4).all()


def test_professor_increment_and_multinomial_return_joint_tests() -> None:
    d = _synthetic_progression()
    binary = professor_uptake_increment(
        d,
        outcome_col="CALC_ANY_VISIT",
        professor_col="CALC_PROFESSOR",
        period_col="CALC_PERIOD_LABEL",
        career_col="CALC_CAREER_OFFICIAL",
    )
    assert binary.loc[0, "delta_r2_professor"] >= 0
    assert 0 <= binary.loc[0, "joint_p_professor"] <= 1

    multi = professor_visit_group_multinomial_increment(
        d,
        group_col="MU_VISIT_GROUP",
        professor_col="CALC_PROFESSOR",
        period_col="CALC_PERIOD_LABEL",
        career_col="CALC_CAREER_OFFICIAL",
    )
    assert multi.loc[0, "lr_df"] > 0
    assert 0 <= multi.loc[0, "lr_p_professor"] <= 1


def test_familiarization_effects_survive_professor_fixed_effect_specification() -> None:
    d = _synthetic_progression()
    out = familiarization_professor_persistence_models(d)
    assert set(out["model"]) == {
        "familiarization_only",
        "adjusted_prior_performance_career_period",
        "plus_calc_professor_fixed_effects",
    }
    final = out.loc[out["model"].eq("plus_calc_professor_fixed_effects")]
    assert len(final) == 3
    assert final["term"].str.contains(r"\[T\.(1-2|3|4\+)\]", regex=True).all()


def test_joint_professor_familiarization_model_returns_group_specific_slopes() -> None:
    d = _synthetic_progression()
    coef, slopes, diagnostics = professor_familiarization_interaction_model(
        d,
        min_other_n=30,
    )
    assert not coef.empty
    assert slopes["mu_visit_group"].tolist() == ["0", "1-2", "3", "4+"]
    assert diagnostics.loc[0, "n_model"] > 0
    assert diagnostics.loc[0, "professors_model"] >= 2
