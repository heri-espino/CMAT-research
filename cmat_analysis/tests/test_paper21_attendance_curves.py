"""Synthetic checks for diminishing-return working curves; no student data."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from run_paper21_attendance_curves import (
    GROUPS, OUTCOMES, SHAPES, basis, curve_values, fitted_shapes,
    grouped_cv, make_design, report, save_plot,
)


def synthetic() -> pd.DataFrame:
    rng = np.random.default_rng(4096)
    rows = []
    for classroom in range(12):
        for k in range(8):
            for rep in range(7):
                degree = "A" if rep % 2 else "B"
                any_use = int(k > 0)
                z = (.37*any_use + .18*np.log(max(k, 1))
                     + .20*(degree == "A")
                     + .015*(classroom % 3) + rng.normal(0, .55))
                grade = float(np.clip(7.2 + 1.25*z, 0, 10))
                adverse = bool(rng.random() < .10)
                rows.append(dict(
                    CLASSROOM_ID=f"CTX-{classroom}",
                    CLAVECARRERA=degree,
                    VISITS_CMAT_PERIOD=k,
                    Z_GRADE_PRIMARY=z,
                    Z_GRADE_COMPLETE_CASE=(z if not adverse else np.nan),
                    GRADE_NUMERIC=(grade if not adverse else np.nan),
                    PASS=int((grade >= 7.5) and not adverse),
                ))
    d = pd.DataFrame(rows)
    # Reproduce the original institutional pandas 3 metadata trigger.
    d.attrs["imputation_summary"] = pd.DataFrame({"audit": [1, 2]})
    return d


def test_curve_features_have_discrete_first_jump_and_concave_shapes():
    v = curve_values(np.arange(0, 9))
    assert v["ANY_VISIT"].tolist() == [0, 1, 1, 1, 1, 1, 1, 1, 1]
    assert v["EXTRA_LINEAR"].tolist() == [0, 0, 1, 2, 3, 4, 5, 6, 6]
    assert v["EXTRA_LOG"][0] == v["EXTRA_LOG"][1] == 0
    assert v["EXTRA_SQRT"][0] == v["EXTRA_SQRT"][1] == 0
    for key in ("EXTRA_LOG", "EXTRA_SQRT"):
        assert np.all(np.diff(v[key][1:8]) > 0)
        assert np.all(np.diff(v[key][1:8], n=2) < 0)
    with pytest.raises(ValueError):
        curve_values(np.array([0, -1]))
    with pytest.raises(ValueError):
        curve_values(np.array([0, .5]))


def test_missing_numeric_outcomes_are_not_imputed():
    s = synthetic()
    full = make_design(s, "Z_GRADE_PRIMARY")
    numeric = make_design(s, "GRADE_NUMERIC")
    cc = make_design(s, "Z_GRADE_COMPLETE_CASE")
    assert len(full) == len(s)
    assert len(numeric) == int(s["GRADE_NUMERIC"].notna().sum())
    assert len(cc) == len(numeric)
    assert len(full) > len(numeric)
    assert full.attrs == {}
    assert set(numeric["VISIT_GROUP"].astype(str)) == set(GROUPS)


def test_flexible_curve_retains_six_visit_dip_and_clustered_intervals():
    d = make_design(synthetic(), "Z_GRADE_PRIMARY")
    means, fits, curves, adjacent = fitted_shapes(d, "Z_GRADE_PRIMARY")
    assert len(means) == 8
    assert len(fits) == len(SHAPES) == 4
    assert len(curves) == 8 * 4
    assert len(adjacent) == 7
    assert "5->6" in set(adjacent["comparison"])
    assert means["n"].sum() == len(d)
    assert means["clusters"].between(1, 12).all()
    assert adjacent["p_holm_7_adjacent"].between(0, 1).all()
    assert curves.loc[curves["k"].eq(0), "estimate"].eq(0).all()
    assert fits["r2_in_sample"].between(0, 1).all()
    categories = curves.loc[curves["shape"].eq("categories")]
    assert categories["visits"].tolist() == list(GROUPS)


def test_full_dummies_identify_5_and_6_separately():
    d = make_design(synthetic(), "Z_GRADE_PRIMARY")
    from run_paper21_attendance_curves import fit_shape
    fit, _ = fit_shape(d, "Z_GRADE_PRIMARY", "categories")
    names = list(fit.params.index)
    d5 = basis("categories", 5, names)
    d6 = basis("categories", 6, names)
    assert not np.array_equal(d5, d6)
    assert np.array_equal(basis("categories", 0, names), np.zeros(len(names)))


def test_holdout_prediction_score_uses_comparable_outcome_sample():
    d = make_design(synthetic(), "GRADE_NUMERIC")
    cv = grouped_cv(d, "GRADE_NUMERIC")
    assert cv["shape"].tolist() == list(SHAPES)
    assert cv["n"].eq(len(d)).all()
    assert cv["folds"].eq(5).all()
    assert cv["cv_error"].ge(0).all()
    assert np.isfinite(cv["cv_skill"].to_numpy()).all()
    assert cv["classroom_fe_in_cv"].eq(False).all()


def test_synthetic_report_and_graph_are_aggregate(tmp_path):
    d = make_design(synthetic(), "PASS")
    means, fits, curves, adjacent = fitted_shapes(d, "PASS")
    cv = grouped_cv(d, "PASS")
    name = tmp_path / "pass_curve.png"
    save_plot("PASS", means, curves, name)
    assert name.exists() and name.stat().st_size > 1000
    s = report(means, fits, curves, adjacent, cv)
    assert "5→6" in s
    assert "log" in s
    assert "CTX-" not in s


def test_outcomes_are_registered_separately():
    assert len(OUTCOMES) == 4
    assert "Z_GRADE_PRIMARY" in dict(OUTCOMES)
    assert "Z_GRADE_COMPLETE_CASE" in dict(OUTCOMES)
    assert "GRADE_NUMERIC" in dict(OUTCOMES)
    assert "PASS" in dict(OUTCOMES)
