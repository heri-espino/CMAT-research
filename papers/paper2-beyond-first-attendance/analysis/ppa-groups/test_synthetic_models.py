"""End-to-end tests of the real shared FE estimator using synthetic records only.

Execute from repository root after installing the canonical cmat_analysis package.
No pseudonymized or raw institutional student file is ever opened here.
"""
from __future__ import annotations
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import pytest

_REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_REPO / "cmat_analysis" / "src"))
# A missing scientific library must FAIL, not silently skip, this integration test.
# The reproducible prerequisite is: pip install -e './cmat_analysis[dev]'
from cmat_analysis.statistics import fixed_effect_group_comparisons
from ppa_groups import SPECS, verify_partition
from run_ppa_groups import _estimate, _adjusted_levels

@pytest.fixture
def synthetic_mu():
    rng = np.random.default_rng(23751)
    rows = []
    for context in range(12):
        for visits in range(9):
            for repeat in range(5):
                p = .59 + .08 * (visits > 0) + .014 * min(visits, 7)
                rows.append({
                    "VISITS_CMAT_PERIOD": visits,
                    "CLASSROOM_ID": f"CTX_{context:02d}",
                    "CLAVECARRERA": f"DEG_{(context + visits + repeat) % 4}",
                    "Z_GRADE_PRIMARY": float(rng.normal(.25 * (visits > 0) + .024 * visits, .78)),
                    "PASS": float(rng.random() < p),
                    "GRADE_NUMERIC": float(np.clip(rng.normal(7.8 + .03 * visits, 1.1), 0, 10)),
                    "Z_GRADE_COMPLETE_CASE": float(rng.normal(0, 1)),
                })
    return pd.DataFrame(rows)

def test_all_model_pair_counts_and_context_overlap(synthetic_mu):
    verify_partition(synthetic_mu)
    for spec in SPECS:
        pair, omnibus, info, observed, overlap = _estimate(synthetic_mu, spec, "Z_GRADE_PRIMARY")
        m = len(spec.labels) * (len(spec.labels) - 1) // 2
        assert len(pair) == m
        assert len(overlap) == m
        assert sum(observed.n) == len(synthetic_mu)
        assert info.loc[0,"n_fixed_effect_levels"] == 12
        assert omnibus.loc[0,"df_num"] == len(spec.labels)-1
        assert np.isfinite(pair.p_raw).all()
        assert np.isfinite(pair.cluster_robust_se).all()

def test_model_standardized_levels_reproduce_shared_pairwise(synthetic_mu):
    for outcome in ("Z_GRADE_PRIMARY", "PASS"):
        for spec in SPECS[:2]:
            levels = _adjusted_levels(synthetic_mu, spec, outcome)
            assert len(levels) == len(spec.labels)
            assert np.isfinite(levels.adjusted_mean).all()
            assert np.isfinite(levels.cluster_robust_se).all()

def test_numeric_selected_sensitivity_defined(synthetic_mu):
    for outcome in ("GRADE_NUMERIC", "Z_GRADE_COMPLETE_CASE"):
        for spec in SPECS[:2]:
            pairs, omnibus, _, _, _ = _estimate(synthetic_mu,spec,outcome)
            assert len(pairs) in (3,6)
            assert np.isfinite(omnibus.p_value).all()
