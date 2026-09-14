"""Aggregate summaries for longitudinal adaptation transitions."""

from __future__ import annotations

import numpy as np
import pandas as pd


def repeat_attempt_summary(transitions: pd.DataFrame) -> pd.DataFrame:
    """Summarize behavioral and instructor-context changes after failed MU attempts.

    Parameters
    ----------
    transitions : pandas.DataFrame
        Repeat-transition table produced by the engagement-trajectory builder. The
        caller should restrict this table to transitions whose periods have the data
        coverage required for the quantities being interpreted.

    Returns
    -------
    pandas.DataFrame
        Aggregate transition statistics by failed-attempt number. Percentages involving
        historical instructor-outcome shifts use only transitions with nonmissing ranks,
        rather than treating unavailable ranks as negative shifts.
    """
    required = {
        "FAILED_ATTEMPT_NUMBER",
        "CHANGED_PROFESSOR",
        "PREV_ANY_CMAT",
        "NEXT_ANY_CMAT",
        "DELTA_CMAT_VISITS",
        "NEXT_ATTEMPT_PASS",
        "DELTA_PROF_EASINESS_PERCENTILE",
    }
    missing = required.difference(transitions.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")

    rows: list[dict[str, object]] = []
    for attempt, sub in transitions.groupby("FAILED_ATTEMPT_NUMBER"):
        delta = pd.to_numeric(sub["DELTA_PROF_EASINESS_PERCENTILE"], errors="coerce")
        rankable = delta.dropna()
        rows.append({
            "failed_attempt_number": int(attempt),
            "n_transitions": int(len(sub)),
            "professor_change_rate": float(sub["CHANGED_PROFESSOR"].mean()),
            "prev_cmat_use_rate": float(sub["PREV_ANY_CMAT"].mean()),
            "next_cmat_use_rate": float(sub["NEXT_ANY_CMAT"].mean()),
            "mean_delta_cmat_visits": float(sub["DELTA_CMAT_VISITS"].mean()),
            "next_attempt_pass_rate": float(sub["NEXT_ATTEMPT_PASS"].mean()),
            "n_with_easiness_delta": int(rankable.size),
            "mean_delta_prof_easiness_percentile": float(rankable.mean()) if rankable.size else np.nan,
            "share_switching_to_higher_easiness_percentile": (
                float((rankable > 0).mean()) if rankable.size else np.nan
            ),
        })
    return pd.DataFrame(rows).sort_values("failed_attempt_number").reset_index(drop=True)
