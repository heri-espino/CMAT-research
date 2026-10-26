"""Synthetic PPA grouping tests: only 0 / 1–3 / 4+; no institutional records."""
from __future__ import annotations
from pathlib import Path
from itertools import combinations
import sys

import numpy as np
import pandas as pd
import pytest
from statsmodels.stats.multitest import multipletests

sys.path.insert(0, str(Path(__file__).parent))
from ppa_groups import SPECS, assign_visit_groups, ppa_family_size, verify_partition
from run_ppa_groups import _focus, run


def test_primary_boundary_and_historical_comparator():
    visits = pd.Series([0, 1, 2, 3, 4, 5, 6, 7, 8, 99])
    assert len(SPECS) == 2
    assert assign_visit_groups(visits, SPECS[0]).astype(str).tolist() == [
        "0", "1-3", "1-3", "1-3", "4+", "4+", "4+", "4+", "4+", "4+"
    ]
    assert assign_visit_groups(visits, SPECS[1]).astype(str).tolist() == [
        "0", "1", "2", "3", "4", "5", "6", "7+", "7+", "7+"
    ]


@pytest.mark.parametrize("values", [[-1, 0], [1.2, 2], [None, 3],
                                    [float("inf"), 2], ["unknown", 2]])
def test_invalid_visit_count_rejected(values):
    with pytest.raises((TypeError, ValueError)):
        assign_visit_groups(pd.Series(values), SPECS[0])


def test_partition_identity_with_exact_frequency_reference():
    frame = pd.DataFrame({"VISITS_CMAT_PERIOD": [0]*10 + [1]*3 + [2]*4 +
                          [3]*5 + [4]*6 + [5]*7 + [7]*8})
    counts = verify_partition(frame)
    assert counts[f"{SPECS[0].name}:0"] == 10
    assert counts[f"{SPECS[0].name}:1-3"] == 12
    assert counts[f"{SPECS[0].name}:4+"] == 21


def test_holm_primary_three_pairs_per_outcome():
    assert ppa_family_size() == 3
    raw_z = np.array([.001, .03, .7])
    raw_pass = np.array([.004, .045, .9])
    hz = multipletests(raw_z, alpha=.05, method="holm")[1]
    hp = multipletests(raw_pass, alpha=.05, method="holm")[1]
    assert len(hz) == len(hp) == 3
    assert hz[0] == pytest.approx(.003)
    assert hp[0] == pytest.approx(.012)


def test_focused_sign_and_percentage_point_conversion():
    rows = []
    spec = SPECS[0]
    for outcome in ("PASS", "Z_GRADE_PRIMARY"):
        for a, b in combinations(spec.labels, 2):
            rows.append(dict(specification=spec.name, outcome=outcome,
                group1=a, group2=b,
                adjusted_group1_minus_group2=-.04, ci_low=-.06, ci_high=-.02,
                p_raw=.03, p_holm_ppa_family=.09, ppa_family_m=3,
                n=60, n_clusters=8))
    focus = _focus(pd.DataFrame(rows))
    row = focus.loc[(focus.outcome == "PASS") &
                    (focus.baseline == "1-3") & (focus.target == "4+")].iloc[0]
    assert row.adjusted_target_minus_baseline == pytest.approx(4.)
    assert (row.ci95_low, row.ci95_high) == pytest.approx((2., 6.))
    assert row.units == "percentage_points"
    assert (focus.ppa_family_m == 3).all()


def test_data_free_check_and_removed_unrequested_option(capsys):
    assert run(["--check"]) == 0
    assert "3-pair" in capsys.readouterr().out.lower()
    with pytest.raises(SystemExit):
        run(["--check", "--include-secondary"])
