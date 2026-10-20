"""Synthetic tests for Paper 2.1 standardized-Z control sensitivity."""
from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

import run_paper21_zscore_controls_experiment as experiment
from run_paper21_model_controls_experiment import GROUPS, PAIR_COUNT, prepare_cohort


def _fixture() -> pd.DataFrame:
    rng = np.random.default_rng(626)
    rows = []
    for classroom in range(20):
        for group in range(8):
            for student in range(4):
                career = f"K{student % 2}"
                rows.append({
                    "CLASSROOM_ID": f"C{classroom:02d}",
                    "CLAVECARRERA": career,
                    "VISITS_CMAT_PERIOD": 8 if group == 7 else group,
                    "Z_GRADE_PRIMARY": (
                        .14 * group + .25 * (career == "K1")
                        + .06 * (classroom % 4) + rng.normal(0, .6)
                    ),
                    "PASS": 1 if (student + group) % 3 else 0,
                })
    return pd.DataFrame(rows)


def test_four_z_ols_models_use_same_sample_and_holm_families():
    d = _fixture()
    pairs, models, sample = experiment.estimate_four_z(d)
    assert len(sample) == len(d)
    assert len(models) == 4
    assert set(models["model"]) == {"A", "B", "C", "D"}
    assert set(models["method"]) == {"Z_OLS"}
    assert models["n"].eq(len(d)).all()
    assert models["clusters"].eq(20).all()
    assert len(pairs) == 4 * PAIR_COUNT
    assert pairs["effect_scale"].eq("standardized Z difference").all()
    assert models["r_squared_in_sample"].between(0, 1).all()
    assert np.isfinite(models["rmse_in_sample"]).all()
    for (_,), family in pairs.groupby(["model"]):
        assert len(family) == PAIR_COUNT
        if family["inferential_status"].eq("valid").all():
            assert family["p_holm"].between(0, 1).all()
            assert family["holm_reject"].notna().all()
        else:
            assert family["holm_reject"].isna().all()
            assert family["p_holm"].isna().all()

    note = experiment.interpretive_note(pairs, models, sample, "TEST")
    assert "Z-score" in note
    assert "A frente a D" in note
    assert "predicciones evaluadas en estudiantes nuevos" in note


def test_d_z_model_reproduces_a_canonical_reference(tmp_path, monkeypatch):
    pairs, models, sample = experiment.estimate_four_z(_fixture())
    reference = (
        pairs.loc[pairs["model"].eq("D"), ["group_low", "group_high", "estimate"]]
        .rename(columns={"group_low": "group1", "group_high": "group2"})
        .copy()
    )
    reference["adjusted_difference_group1_minus_group2"] = -reference["estimate"]
    reference_file = tmp_path / "reference.csv"
    reference.to_csv(reference_file, index=False)
    monkeypatch.setattr(experiment, "REFERENCE", reference_file)
    assert "all 28" in experiment.audit_full_adjustment(pairs)
    reference.loc[reference.index[0], "adjusted_difference_group1_minus_group2"] += .02
    reference.to_csv(reference_file, index=False)
    with pytest.raises(RuntimeError, match="does not reproduce"):
        experiment.audit_full_adjustment(pairs)


def test_z_only_preparation_rejects_nonfinite_input():
    sample = prepare_cohort(_fixture(), outcome_col="Z_GRADE_PRIMARY")
    assert sample["VISIT_GROUP"].cat.categories.tolist() == list(GROUPS)
    invalid = _fixture()
    invalid.loc[invalid.index[0], "Z_GRADE_PRIMARY"] = np.inf
    with pytest.raises(ValueError, match="finite"):
        prepare_cohort(invalid, outcome_col="Z_GRADE_PRIMARY")
