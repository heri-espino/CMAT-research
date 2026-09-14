"""Regression test for rankable-only repeat-transition percentages."""

import numpy as np
import pandas as pd

from cmat_analysis.ppa import repeat_attempt_summary


def test_repeat_rank_shift_share_excludes_missing_ranks() -> None:
    transitions = pd.DataFrame({
        "FAILED_ATTEMPT_NUMBER": [1, 1, 1, 1],
        "CHANGED_PROFESSOR": [1, 1, 1, 1],
        "PREV_ANY_CMAT": [0, 0, 0, 0],
        "NEXT_ANY_CMAT": [0, 0, 0, 0],
        "DELTA_CMAT_VISITS": [0, 0, 0, 0],
        "NEXT_ATTEMPT_PASS": [1, 1, 0, 0],
        "DELTA_PROF_EASINESS_PERCENTILE": [0.2, -0.1, np.nan, np.nan],
    })
    out = repeat_attempt_summary(transitions).iloc[0]
    assert out["n_with_easiness_delta"] == 2
    assert np.isclose(out["share_switching_to_higher_easiness_percentile"], 0.5)
