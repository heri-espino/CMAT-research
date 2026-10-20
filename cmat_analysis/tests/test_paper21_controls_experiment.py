"""Synthetic-only checks for the Paper 2.1 adjustment experiment."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from run_paper21_model_controls_experiment import (
    PAIR_COUNT,
    SPECS,
    _inference,
    group_formula,
    prepare_cohort,
    run_four_by_two,
)


def _balanced_fixture() -> pd.DataFrame:
    rng = np.random.default_rng(2194)
    rows = []
    for cluster in range(20):
        for group in range(8):
            for j in range(3):
                career = "K0" if j % 2 == 0 else "K1"
                log_odds = -.9 + group * .12 + .4 * (career == "K1") + .06 * (cluster % 5)
                chance = 1 / (1 + np.exp(-log_odds))
                rows.append({
                    "CLASSROOM_ID": f"C{cluster:02d}",
                    "CLAVECARRERA": career,
                    "VISITS_CMAT_PERIOD": group if group < 7 else 8,
                    "PASS": int(rng.random() < chance),
                })
    return pd.DataFrame(rows)


def test_four_by_two_methods_and_holm_families():
    assert len(SPECS) == 4
    d = _balanced_fixture()
    pairs, models, prepared = run_four_by_two(d)
    assert len(prepared) == len(d)
    assert len(models) == 8
    assert set(models["method"]) == {"LPM", "logit"}
    assert models.groupby("method")["model"].nunique().eq(4).all()
    assert set(models["n"]) == {len(d)}
    assert models["clusters"].eq(20).all()
    assert PAIR_COUNT == 28
    for (_, _), frame in pairs.groupby(["method", "model"]):
        assert len(frame) == 28
        valid = frame["inferential_status"].eq("valid").all()
        if valid:
            assert frame["p_holm"].between(0, 1).all()
            assert frame["holm_reject"].notna().all()
        else:
            assert frame["p_holm"].isna().all()
            assert frame["holm_reject"].isna().all()
    assert len(pairs) == 8 * 28


def test_invalid_covariance_cannot_pass_holm():
    class Dummy:
        pass
    model = Dummy()
    term = "C(VISIT_GROUP, Treatment(reference='0'))"
    names = ["Intercept"] + [f"{term}[T.{label}]" for label in ("1", "2", "3", "4", "5", "6", "7+")]
    model.params = pd.Series(np.ones(len(names)), index=names)
    covariance = np.eye(len(names))
    covariance[1, 1] = np.nan
    model.cov_params = lambda: covariance
    result, status = _inference(
        model, method="logit", code="X", n=100, n_clusters=8,
        has_fe=False, has_career=False, diagnostic=""
    )
    assert len(result) == 28
    assert status == "not_estimable"
    assert result["p_holm"].isna().all()
    assert result["holm_reject"].isna().all()
    assert result["inferential_status"].eq("not_estimable").all()


def test_reference_group_and_eligible_cohort_checks():
    assert group_formula(False, False).count(" + ") == 0
    assert "C(CLASSROOM_ID)" in group_formula(True, False)
    assert "C(CLAVECARRERA)" in group_formula(False, True)
    assert all(z in group_formula(True, True) for z in ("C(CLASSROOM_ID)", "C(CLAVECARRERA)"))
    frame = prepare_cohort(_balanced_fixture())
    assert frame["VISIT_GROUP"].cat.categories.tolist() == [
        "0", "1", "2", "3", "4", "5", "6", "7+"
    ]
    assert set(frame["PASS"]) == {0, 1}
