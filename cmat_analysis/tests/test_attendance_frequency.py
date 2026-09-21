"""Tests for reusable attendance-frequency and outcome-composition tools."""

from __future__ import annotations

import numpy as np
import pandas as pd

from cmat_analysis.measures import add_academic_outcome_states
from cmat_analysis.statistics import (
    add_topcoded_visit_group,
    distribution_profile,
    fixed_effect_group_comparisons,
    fixed_effect_logistic_group_comparisons,
    fixed_effect_logistic_adjusted_probabilities,
    mixture_component_density,
    outcome_state_composition,
    pairwise_effect_matrix,
    visit_frequency_cut_frontier,
    visit_frequency_support_audit,
    visit_group_pair_overlap,
)


def _fixture() -> pd.DataFrame:
    rng = np.random.default_rng(2026)
    rows = []
    for cluster in range(12):
        for label, visits in [("1", 1), ("2", 2), ("3+", 3)]:
            for j in range(4):
                rows.append({
                    "CLASSROOM_ID": f"C{cluster}",
                    "PROFESSOR_ID": f"P{cluster // 2}",
                    "CAREER": f"K{j % 2}",
                    "VISITS_CMAT_PERIOD": visits,
                    "GROUP": label,
                    "Y": visits * 0.2 + rng.normal(0, 0.2),
                    "PASS": int(rng.random() < 0.65 + 0.08 * visits),
                })
        rows.append({
            "CLASSROOM_ID": f"C{cluster}",
            "PROFESSOR_ID": f"P{cluster // 2}",
            "CAREER": "K0",
            "VISITS_CMAT_PERIOD": 0,
            "GROUP": "0",
            "Y": rng.normal(-0.2, 0.2),
            "PASS": 0,
        })
    return pd.DataFrame(rows)


def test_academic_outcome_states_preserve_exact_administrative_codes():
    d = pd.DataFrame({
        "PASS": [1, 0, 0, 0, 0],
        "GRADE_CLASS": ["numeric", "numeric", "adverse", "adverse", "adverse"],
        "GRADE_TOKEN": ["9.1", "6.0", "BV", "RT", "BA"],
    })
    out = add_academic_outcome_states(d)
    assert out["ACADEMIC_OUTCOME_STATE_5"].tolist() == [
        "pass", "numeric_nonpass", "BV", "RT", "BA"
    ]
    assert out["BV_VS_NUMERIC_NONPASS"].iloc[1] == 0
    assert out["BV_VS_NUMERIC_NONPASS"].iloc[2] == 1
    assert np.isnan(out["BV_VS_NUMERIC_NONPASS"].iloc[3])
    assert out["ADMINISTRATIVE_VS_NUMERIC_NONPASS"].iloc[4] == 1


def test_grouping_support_and_cut_frontier_use_exposure_only():
    d = _fixture()
    grouped = add_topcoded_visit_group(
        d, top_exact=2, include_zero=True, output_col="FREQ"
    )
    assert list(grouped["FREQ"].cat.categories) == ["0", "1", "2", "3+"]
    support = visit_frequency_support_audit(
        d, cluster_col="CLASSROOM_ID", instructor_col="PROFESSOR_ID"
    )
    assert set(support["visits_exact"]) == {1, 2, 3}
    assert support.loc[
        support["visits_exact"].eq(1), "clusters_with_zero_visit_students"
    ].iloc[0] == 12
    frontier = visit_frequency_cut_frontier(
        d, cluster_col="CLASSROOM_ID", min_top_exact=1, max_top_exact=2
    )
    assert frontier["top_exact_visit_count"].tolist() == [1, 2]
    assert (frontier["minimum_adjacent_pair_overlap_clusters"] == 12).all()


def test_clustered_fe_pairwise_family_and_overlap_are_complete():
    d = _fixture().loc[lambda x: x["VISITS_CMAT_PERIOD"].gt(0)].copy()
    overlap = visit_group_pair_overlap(
        d, group_col="GROUP", group_order=["1", "2", "3+"]
    )
    assert len(overlap) == 3
    assert overlap["clusters_with_both"].min() == 12
    pairwise, omnibus, info = fixed_effect_group_comparisons(
        d,
        group_col="GROUP",
        group_order=["1", "2", "3+"],
        outcome_col="Y",
        fixed_effect_col="CLASSROOM_ID",
        cluster_col="CLASSROOM_ID",
        categorical_covariates=["CAREER"],
    )
    assert len(pairwise) == 3
    assert pairwise["p_adjusted"].between(0, 1).all()
    assert pairwise["adjacent_groups"].sum() == 2
    assert omnibus.loc[0, "df_num"] == 2
    assert info.loc[0, "n_clusters"] == 12


def test_composition_distribution_and_matrix_outputs_are_consistent():
    d = _fixture().loc[lambda x: x["VISITS_CMAT_PERIOD"].gt(0)].copy()
    d["STATE"] = np.where(d["PASS"].eq(1), "pass", "numeric_nonpass")
    composition = outcome_state_composition(
        d,
        group_col="GROUP",
        group_order=["1", "2", "3+"],
        state_col="STATE",
        state_order=["pass", "numeric_nonpass"],
    )
    assert np.allclose(
        composition.groupby("group")["share_within_group"].sum().to_numpy(), 1.0
    )
    profile = distribution_profile(
        d,
        group_col="GROUP",
        group_order=["1", "2", "3+"],
        outcome_col="Y",
        pass_col="PASS",
    )
    assert {"q10", "q25", "q50", "q75", "q90"}.issubset(profile.columns)
    pairwise, _, _ = fixed_effect_group_comparisons(
        d,
        group_col="GROUP",
        group_order=["1", "2", "3+"],
        outcome_col="Y",
        fixed_effect_col="CLASSROOM_ID",
        cluster_col="CLASSROOM_ID",
    )
    matrix = pairwise_effect_matrix(pairwise, group_order=["1", "2", "3+"])
    wide = matrix.set_index("group")
    assert np.allclose(np.diag(wide.to_numpy()), 0.0)
    assert np.isclose(wide.loc["1", "2"], -wide.loc["2", "1"])



def test_mixture_component_density_areas_recover_component_shares():
    d = _fixture().copy()
    d["STATE"] = np.where(d["PASS"].eq(1), "pass", "nonpass")
    density = mixture_component_density(
        d,
        group_col="GROUP",
        group_order=["0", "1", "2", "3+"],
        outcome_col="Y",
        component_col="STATE",
        component_order=["pass", "nonpass"],
        grid_size=512,
    )
    for group in ["0", "1", "2", "3+"]:
        g = density.loc[density["group"].eq(group)]
        x = g["x"].drop_duplicates().to_numpy(float)
        total = (
            g.drop_duplicates("x")
            .sort_values("x")["density_total"]
            .to_numpy(float)
        )
        assert np.isclose(np.trapezoid(total, x), 1.0, atol=0.02)
        for component in ["pass", "nonpass"]:
            c = g.loc[g["component"].eq(component)].sort_values("x")
            area = np.trapezoid(c["density_component"].to_numpy(float), c["x"].to_numpy(float))
            share = float(c["component_share"].iloc[0])
            assert np.isclose(area, share, atol=0.02)



def test_clustered_fixed_effect_logit_returns_odds_ratios():
    d = _fixture().loc[lambda x: x["VISITS_CMAT_PERIOD"].gt(0)].copy()
    pairwise, omnibus, info = fixed_effect_logistic_group_comparisons(
        d,
        group_col="GROUP",
        group_order=["1", "2", "3+"],
        outcome_col="PASS",
        fixed_effect_col="CLASSROOM_ID",
        cluster_col="CLASSROOM_ID",
        categorical_covariates=["CAREER"],
    )
    assert len(pairwise) == 3
    assert pairwise["odds_ratio_group1_vs_group2"].gt(0).all()
    assert pairwise["p_adjusted"].between(0, 1).all()
    assert omnibus.loc[0, "df_num"] == 2
    assert info.loc[0, "converged"]


def test_clustered_fixed_effect_logit_returns_adjusted_probabilities():
    d = _fixture().loc[lambda x: x["VISITS_CMAT_PERIOD"].gt(0)].copy()
    adjusted = fixed_effect_logistic_adjusted_probabilities(
        d,
        group_col="GROUP",
        group_order=["1", "2", "3+"],
        outcome_col="PASS",
        fixed_effect_col="CLASSROOM_ID",
        cluster_col="CLASSROOM_ID",
        categorical_covariates=["CAREER"],
    )
    assert adjusted["group"].tolist() == ["1", "2", "3+"]
    assert adjusted["adjusted_probability"].between(0, 1).all()
    assert adjusted["adjusted_probability_se"].ge(0).all()
    assert adjusted["adjusted_ci95_low"].between(0, 1).all()
    assert adjusted["adjusted_ci95_high"].between(0, 1).all()
    assert (adjusted["adjusted_ci95_low"] <= adjusted["adjusted_probability"]).all()
    assert (adjusted["adjusted_probability"] <= adjusted["adjusted_ci95_high"]).all()
    assert adjusted["observed_probability"].between(0, 1).all()
    assert adjusted["n_standardization_sample"].nunique() == 1
    assert adjusted["converged"].all()
