"""Tests for reusable univariate Gaussian-mixture analysis."""

from __future__ import annotations

import numpy as np
from scipy.stats import skewnorm

from cmat_analysis.statistics import (
    compare_univariate_shape_models,
    cross_validated_skew_normal_vs_gmm,
    gaussian_mixture_component_summary,
    gaussian_mixture_model_selection,
    gaussian_mixture_responsibilities,
    parametric_bootstrap_gmm_lrt,
    parametric_bootstrap_skew_normal_vs_gmm,
    soft_component_composition,
    skew_normal_fit_summary,
)


def _bimodal_sample() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(2026)
    low = rng.normal(-1.1, 0.22, size=120)
    high = rng.normal(0.55, 0.28, size=280)
    values = np.concatenate([low, high])
    states = np.array(["numeric_nonpass"] * len(low) + ["pass"] * len(high))
    return values, states


def test_two_component_model_recovers_ordered_bimodal_structure():
    values, _ = _bimodal_sample()
    selection, models = gaussian_mixture_model_selection(
        values,
        component_counts=(1, 2, 3),
        random_state=42,
        n_init=10,
        two_component_mean_starts=((-1.1, 0.5),),
    )
    bic = selection.set_index("n_components")["bic"]
    assert bic.loc[2] < bic.loc[1]

    summary = gaussian_mixture_component_summary(models[2])
    assert summary["component"].tolist() == [
        "lower_performance",
        "higher_performance",
    ]
    assert summary.loc[0, "mean"] < -0.8
    assert summary.loc[1, "mean"] > 0.3
    assert summary.loc[0, "ashman_d_two_component_model"] > 2.0


def test_responsibilities_and_soft_composition_are_probabilistic():
    values, states = _bimodal_sample()
    _, models = gaussian_mixture_model_selection(
        values,
        component_counts=(2,),
        random_state=42,
        n_init=8,
        two_component_mean_starts=((-1.1, 0.5),),
    )
    responsibilities = gaussian_mixture_responsibilities(models[2], values)
    cols = [
        "responsibility_lower_performance",
        "responsibility_higher_performance",
    ]
    assert np.allclose(responsibilities[cols].sum(axis=1), 1.0)

    composition = soft_component_composition(
        states,
        responsibilities,
        state_order=["numeric_nonpass", "pass"],
    )
    shares = composition.groupby("component")["share_within_component"].sum()
    assert np.allclose(shares.to_numpy(), 1.0)


def test_parametric_bootstrap_gmm_lrt_returns_valid_empirical_p_value():
    values, _ = _bimodal_sample()
    result = parametric_bootstrap_gmm_lrt(
        values,
        n_bootstrap=19,
        random_state=42,
        n_init=6,
        two_component_mean_starts=((-1.1, 0.5),),
    )
    assert result.loc[0, "likelihood_ratio"] > 0
    assert 0 < result.loc[0, "bootstrap_p_value"] <= 1


def test_single_skew_normal_beats_single_gaussian_for_skewed_unimodal_data():
    """A flexible one-component shape should absorb ordinary unimodal skew."""
    rng = np.random.default_rng(2027)
    values = skewnorm.rvs(8.0, loc=-0.7, scale=1.0, size=900, random_state=rng)
    skew = skew_normal_fit_summary(values).iloc[0]
    gaussian, _ = gaussian_mixture_model_selection(
        values, component_counts=(1,), random_state=42, n_init=8
    )
    assert skew["scale"] > 0
    assert skew["bic"] < gaussian.loc[0, "bic"]


def test_two_gaussians_can_beat_single_skew_normal_for_clear_bimodality():
    """A single skewed density should not erase clear two-mode structure."""
    rng = np.random.default_rng(2028)
    values = np.concatenate([
        rng.normal(-1.5, 0.20, size=250),
        rng.normal(0.65, 0.25, size=500),
    ])
    skew = skew_normal_fit_summary(values).iloc[0]
    gaussian, _ = gaussian_mixture_model_selection(
        values,
        component_counts=(1, 2),
        random_state=42,
        n_init=10,
        two_component_mean_starts=((-1.5, 0.65),),
    )
    bic2 = float(gaussian.loc[gaussian["n_components"].eq(2), "bic"].iloc[0])
    assert bic2 < skew["bic"]


def test_shape_model_comparison_prefers_two_gaussians_for_clear_bimodality():
    """The reusable comparator should identify a clearly bimodal density."""
    rng = np.random.default_rng(2029)
    values = np.concatenate([
        rng.normal(-1.6, 0.18, size=260),
        rng.normal(0.70, 0.24, size=520),
    ])
    result = compare_univariate_shape_models(
        values,
        random_state=42,
        n_init=10,
        two_component_mean_starts=((-1.6, 0.70),),
    ).iloc[0]
    assert result["bic_preferred_model"] == "gaussian_mixture_k2"
    assert result["bic_advantage_gmm_k2_over_skew_normal"] > 0
    assert result["n"] == len(values)



def test_skew_normal_null_bootstrap_returns_valid_tail_probability():
    """The skew-normal bootstrap should return a finite empirical reference."""
    rng = np.random.default_rng(2030)
    values = skewnorm.rvs(-5.0, loc=0.8, scale=1.1, size=400, random_state=rng)
    result = parametric_bootstrap_skew_normal_vs_gmm(
        values,
        n_bootstrap=19,
        random_state=42,
        n_init=6,
        two_component_mean_starts=((-1.1, 0.5),),
    ).iloc[0]
    assert np.isfinite(result["observed_bic_advantage_gmm_k2_over_skew_normal"])
    assert 0 < result["bootstrap_p_value"] <= 1
    assert result["bootstrap_replicates"] == 19


def test_cross_validated_shape_comparison_prefers_gmm_for_clear_bimodality():
    """Held-out density should favour a two-Gaussian fit for clear bimodality."""
    rng = np.random.default_rng(2031)
    values = np.concatenate([
        rng.normal(-1.5, 0.20, size=180),
        rng.normal(0.65, 0.24, size=360),
    ])
    result = cross_validated_skew_normal_vs_gmm(
        values,
        n_splits=5,
        n_repeats=3,
        random_state=42,
        n_init=6,
        two_component_mean_starts=((-1.5, 0.65),),
    ).iloc[0]
    assert result["mean_log_predictive_density_difference_gmm_minus_skew"] > 0
    assert result["gmm_fold_win_share"] > 0.5
    assert result["held_out_predictions"] == len(values) * 3
