from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

from cmat_analysis.reporting.methodology_build import methodology_report_cli
from cmat_analysis.statistics.methodology import add_exact_visit_group, games_howell_exact_groups
from cmat_analysis.measures import add_primary_outcomes


def test_methodology_primary_outcome_uses_scipy_kde_and_uniform_fallback():
    cfg = SimpleNamespace(passing_grade=7.5, random_seed=42, min_classroom_n_for_z=2)
    d = pd.DataFrame({
        "CLASSROOM_ID": ["A"] * 5 + ["B"] * 3,
        "GRADE_CLASS": ["numeric", "numeric", "numeric", "adverse", "adverse", "numeric", "adverse", "adverse"],
        "GRADE_NUMERIC": [5.0, 6.0, 9.0, np.nan, np.nan, 9.0, np.nan, np.nan],
        "SOURCE_ROW": list(range(8)),
    })
    out = add_primary_outcomes(d, cfg)
    audit = out.attrs["imputation_summary"].set_index("CLASSROOM_ID")
    assert audit.loc["A", "method"] == "within_classroom_scipy_gaussian_kde_default_scott"
    assert audit.loc["A", "kde_bw_method"] == "None (SciPy default; Scott factor)"
    assert np.isfinite(float(audit.loc["A", "kde_factor"]))
    assert audit.loc["B", "method"] == "uniform_fallback_no_observed_subpass_grade"
    imputed = out.loc[out["GRADE_CLASS"] == "adverse", "GRADE_PRIMARY"]
    assert (imputed >= 0).all()
    assert (imputed < 7.5).all()


def test_methodology_exact_visit_grouping_has_all_ten_pairwise_contrasts():
    rows = []
    for visits in [0, 1, 2, 3, 4]:
        for j in range(5):
            rows.append({"VISITS_CMAT_PERIOD": visits, "Z_GRADE_PRIMARY": float(visits) + j / 10})
    d = pd.DataFrame(rows)
    grouped = add_exact_visit_group(d)
    assert set(grouped["EXACT_VISIT_GROUP_0_1_2_3_4P"].astype(str)) == {"0", "1", "2", "3", "4+"}
    assert len(games_howell_exact_groups(d, population="test")) == 10


def test_methodology_report_atomic_runner_resolves_root_code_dependencies():
    repo_root = Path(__file__).resolve().parents[2]
    report_dir = repo_root / "brainstorm" / "methodology_report"
    assert methodology_report_cli(repo_root, report_dir, ["--check"]) == 0
