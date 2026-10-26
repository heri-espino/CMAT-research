"""Synthetic-only PPA partition and reporting tests; never load student records."""
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

def test_boundary_values():
    x = pd.Series([0,1,2,3,4,5,6,7,8,99])
    assert assign_visit_groups(x,SPECS[0]).astype(str).tolist() == [
        "0","1-3","1-3","1-3","4+","4+","4+","4+","4+","4+"]
    assert assign_visit_groups(x,SPECS[1]).astype(str).tolist() == [
        "0","1-3","1-3","1-3","4","5+","5+","5+","5+","5+"]
    assert assign_visit_groups(x,SPECS[2]).astype(str).tolist() == [
        "0","1","2","3","4","5","6","7+","7+","7+"]

@pytest.mark.parametrize("values", [[-1,0],[1.2,2],[None,3],[float("inf"),2],["unknown",2]])
def test_bad_count_rejected(values):
    with pytest.raises((ValueError,TypeError)):
        assign_visit_groups(pd.Series(values), SPECS[0])

def test_exhaustive_nonoverlap():
    x = pd.DataFrame({"VISITS_CMAT_PERIOD":[0]*10+[1]*3+[2]*4+[3]*5+[4]*6+[5]*7+[7]*8})
    c = verify_partition(x)
    assert c[f"{SPECS[0].name}:1-3"] == 12
    assert c[f"{SPECS[0].name}:4+"] == 21
    assert c[f"{SPECS[1].name}:4"] == 6
    assert c[f"{SPECS[1].name}:5+"] == 15

def test_holm_joint_18_not_nine_or_previous_families():
    assert ppa_family_size() == 18
    raw = np.array([.001,.02,.03,.08,.3,.7,.01,.2,.8,.003,.04,.15,.45,.9,.23,.07,.5,.6])
    rejects, adjusted, _, _ = multipletests(raw,alpha=.05,method="holm")
    order = np.argsort(raw)
    assert len(adjusted) == 18
    assert np.all(adjusted >= raw-1e-12)
    assert np.all(np.diff(adjusted[order]) >= -1e-12)
    assert bool(rejects[0]) and not bool(rejects[1])
    assert not np.array_equal(adjusted[:3],multipletests(raw[:3],method="holm")[1])

def test_focused_contrast_sign_and_pp_scale():
    rows = []
    for spec in SPECS[:2]:
        for outcome in ("PASS","Z_GRADE_PRIMARY"):
            for group1, group2 in combinations(spec.labels,2):
                rows.append(dict(specification=spec.name,outcome=outcome,
                    group1=group1,group2=group2,
                    adjusted_group1_minus_group2=-.04,ci_low=-.06,ci_high=-.02,
                    p_raw=.03,p_holm_ppa_family=.23,ppa_family_m=18,n=60,n_clusters=8))
    focus = _focus(pd.DataFrame(rows))
    row = focus.loc[(focus.outcome=="PASS")&(focus.baseline=="1-3")&(focus.target=="4+")].iloc[0]
    assert row.adjusted_target_minus_baseline == pytest.approx(4.)
    assert (row.ci95_low,row.ci95_high) == pytest.approx((2.,6.))
    assert row.units == "percentage_points"
    zz = focus.loc[(focus.outcome=="Z_GRADE_PRIMARY")&(focus.baseline=="4")&(focus.target=="5+")].iloc[0]
    assert zz.adjusted_target_minus_baseline == pytest.approx(.04)

def test_data_free_static_check(capsys):
    assert run(["--check"]) == 0
    assert "PASS" in capsys.readouterr().out


def test_primary_only_family_has_six_tests():
    """Only three primary group pairs per outcome when secondary is not retained."""
    primary = SPECS[0]
    assert len(list(combinations(primary.labels, 2))) * 2 == 6
    assert ppa_family_size() == 18
    raw = np.array([.001, .02, .03, .04, .05, .06])
    adjusted_primary = multipletests(raw, method="holm")[1]
    adjusted_joint = multipletests(np.r_[raw, np.linspace(.001, .9, 12)], method="holm")[1]
    assert not np.allclose(adjusted_primary, adjusted_joint[:6])
