"""Regression test: exactly 7.5 passes; numeric failure is strictly below 7.5."""

import pandas as pd

from cmat_analysis.config.study_config import CMATStudyConfig
from cmat_analysis.measures.grades import add_primary_outcomes


def test_numeric_7_5_is_passing_and_administrative_records_have_no_numeric_grade():
    cohort = pd.DataFrame(
        {
            "CLASSROOM_ID": ["c1"] * 6,
            "SOURCE_ROW": list(range(6)),
            "GRADE_CLASS": ["numeric", "numeric", "numeric", "numeric", "adverse", "adverse"],
            "GRADE_TOKEN": ["7.49", "7.5", "8.0", "5.0", "BV", "RT"],
            "GRADE_NUMERIC": [7.49, 7.5, 8.0, 5.0, float("nan"), float("nan")],
        }
    )
    config = CMATStudyConfig(random_seed=221, min_classroom_n_for_z=2)
    result = add_primary_outcomes(cohort, config)
    assert result["PASS"].astype(int).tolist() == [0, 1, 1, 0, 0, 0]
    assert result.loc[1, "GRADE_PRIMARY"] == 7.5
    assert result.loc[0, "GRADE_PRIMARY"] == 7.49
    assert result.loc[4:5, "GRADE_NUMERIC"].isna().all()
    assert (result.loc[4:5, "GRADE_PRIMARY"] < 7.5).all()
