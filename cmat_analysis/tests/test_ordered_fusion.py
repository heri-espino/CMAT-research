"""Synthetic, privacy-safe regression tests for ordered fusion."""
import numpy as np
import pandas as pd
import pytest

from cmat_analysis.statistics.ordered_fusion import (
    cluster_split, exhaustive_contiguous_partitions, fit_prepared, grouped_cv, heldout_within_classroom_mse,
    lambda_grid, prepare_fusion, resample_cluster_rows, selected_partition,
)


def synthetic(seed=17, n_classrooms=36, per_class=20):
    rng = np.random.default_rng(seed)
    n = n_classrooms * per_class
    cls = np.repeat(np.arange(n_classrooms), per_class).astype(str)
    visits = rng.integers(0, 8, size=n)
    deg = rng.integers(0, 3, size=n)
    true_levels = np.array([0, .3, .3, .3, .3, .5, .5, .8])
    y = (true_levels[visits] + .18 * deg
         + np.repeat(rng.normal(0, .5, n_classrooms), per_class)
         + rng.normal(0, .2, n))
    return pd.DataFrame({
        "GRADE": y, "PASS": (y > .2).astype(float),
        "GROUP": np.array(["0", "1", "2", "3", "4", "5", "6", "7+"])[visits],
        "CLASSROOM_ID": cls, "CLAVECARRERA": deg.astype(str),
    })


ORDER = ("0", "1", "2", "3", "4", "5", "6", "7+")


def test_zero_lambda_is_unpenalised_partial_regression():
    d = synthetic()
    prep = prepare_fusion(d["GRADE"], d["GROUP"], d["CLASSROOM_ID"],
                          d["CLAVECARRERA"], ORDER)
    zero = fit_prepared(prep, 0)
    direct = np.linalg.lstsq(prep.residual_steps, prep.residual_y, rcond=None)[0]
    np.testing.assert_allclose(zero["step_coefficients"], direct, atol=1e-5)
    assert zero["n_blocks"] <= 8
    assert np.linalg.matrix_rank(prep.residual_steps) == 7


def test_large_penalty_fuses_all_and_preserves_nuisance():
    d = synthetic()
    prep = prepare_fusion(d["GRADE"], d["GROUP"], d["CLASSROOM_ID"],
                          d["CLAVECARRERA"], ORDER)
    grid = lambda_grid(prep)
    fit = fit_prepared(prep, float(grid[-1]))
    assert fit["n_blocks"] == 1
    assert fit["boundaries"] == ()
    assert len(fit["degree_coefficients"]) == d["CLAVECARRERA"].nunique()


def test_partitions_and_grouped_folds():
    d = synthetic()
    first, hold = cluster_split(d, seed=41)
    assert not set(first["CLASSROOM_ID"]) & set(hold["CLASSROOM_ID"])
    summary, selected = grouped_cv(first, outcome="GRADE", group="GROUP",
                                   order=ORDER, folds=3, grid_size=5)
    assert np.isfinite(summary["cv_mse"]).all()
    assert selected in set(summary["lambda"])
    fit = fit_prepared(prepare_fusion(first["GRADE"], first["GROUP"],
                                      first["CLASSROOM_ID"],
                                      first["CLAVECARRERA"], ORDER), selected)
    score = heldout_within_classroom_mse(
        fit, hold["GRADE"], hold["GROUP"], hold["CLASSROOM_ID"],
        hold["CLAVECARRERA"], ORDER
    )
    assert np.isfinite(score)
    assert len(selected_partition(ORDER, fit["boundaries"])) == fit["n_blocks"]


def test_cluster_bootstrap_relabels_duplicate_draws():
    d = synthetic(n_classrooms=15)
    boot = resample_cluster_rows(d, seed=91)
    assert boot["CLASSROOM_ID"].nunique() == 15
    assert len(boot) == len(d)


def test_reject_unknown_validation_degree():
    d = synthetic()
    fit = fit_prepared(prepare_fusion(d["GRADE"], d["GROUP"],
                                      d["CLASSROOM_ID"],
                                      d["CLAVECARRERA"], ORDER), .01)
    with pytest.raises(ValueError, match="Unseen"):
        heldout_within_classroom_mse(fit, d["GRADE"], d["GROUP"],
                                     d["CLASSROOM_ID"],
                                     np.repeat("unknown", len(d)), ORDER)


def test_exhaustive_partition_bic_and_unrestricted_fit():
    d = synthetic()
    prep = prepare_fusion(d["GRADE"], d["GROUP"], d["CLASSROOM_ID"],
                          d["CLAVECARRERA"], ORDER)
    table = exhaustive_contiguous_partitions(prep)
    assert len(table) == 128
    assert set(table["rank_bic"]) == set(range(1, 129))
    assert np.isfinite(table["bic_relative"]).all()
    unrestricted = table.loc[table["n_blocks"].eq(8)].iloc[0]
    unpenalised = fit_prepared(prep, 0)
    assert np.isclose(unrestricted["sse"],
                      len(d) * unpenalised["training_loss_within_context"],
                      atol=1e-5)
