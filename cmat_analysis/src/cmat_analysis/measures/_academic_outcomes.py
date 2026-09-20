"""Academic-result state construction for educational outcome analyses.

These derived measures preserve the type of adverse final record. They are
descriptive and must not be interpreted as direct measures of motivation,
engagement, institutional knowledge, or causal response to support.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def add_academic_outcome_states(
    df: pd.DataFrame,
    *,
    pass_col: str = "PASS",
    grade_class_col: str = "GRADE_CLASS",
    grade_token_col: str = "GRADE_TOKEN",
    numeric_class: str = "numeric",
    adverse_class: str = "adverse",
) -> pd.DataFrame:
    """Add exact/compact result states and conditional non-pass contrasts.

    Parameters
    ----------
    df : pandas.DataFrame
        Table containing pass status, grade class, and original grade token.
    pass_col : str, default='PASS'
        Column coded 1 for pass and 0 for non-pass.
    grade_class_col : str, default='GRADE_CLASS'
        Column distinguishing numeric and adverse records.
    grade_token_col : str, default='GRADE_TOKEN'
        Column containing original tokens such as BV, RT, and BA.
    numeric_class : str, default='numeric'
        Value identifying numeric final grades.
    adverse_class : str, default='adverse'
        Value identifying adverse administrative records.

    Returns
    -------
    pandas.DataFrame
        Copy with exact five-state and compact four-state outcomes plus binary
        administrative, BV/RT, BV, and RT versus numeric-nonpass contrasts.

    Notes
    -----
    Rows outside a binary contrast are NaN. The function never infers why an
    administrative outcome occurred.
    """
    required = {pass_col, grade_class_col, grade_token_col}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise KeyError(f"Missing required academic-outcome columns: {missing}")

    out = df.copy()
    passed = pd.to_numeric(out[pass_col], errors="coerce")
    grade_class = out[grade_class_col].astype("string")
    token = out[grade_token_col].fillna("").astype(str).str.strip().str.upper()
    is_pass = passed.eq(1)
    is_nonpass = passed.eq(0)
    numeric_nonpass = is_nonpass & grade_class.eq(numeric_class)
    adverse_nonpass = is_nonpass & grade_class.eq(adverse_class)

    out["ACADEMIC_OUTCOME_STATE_5"] = np.select(
        [is_pass, numeric_nonpass, token.eq("BV"), token.eq("RT"), token.eq("BA")],
        ["pass", "numeric_nonpass", "BV", "RT", "BA"],
        default="other",
    )
    out["ACADEMIC_OUTCOME_STATE_4"] = np.select(
        [is_pass, numeric_nonpass, token.isin(["BV", "RT"]), token.eq("BA")],
        ["pass", "numeric_nonpass", "BV_RT", "BA"],
        default="other",
    )

    def contrast(positive: pd.Series) -> pd.Series:
        values = pd.Series(np.nan, index=out.index, dtype=float)
        values.loc[numeric_nonpass] = 0.0
        values.loc[positive & adverse_nonpass] = 1.0
        return values

    out["ADMINISTRATIVE_VS_NUMERIC_NONPASS"] = contrast(
        token.isin(["BV", "RT", "BA"])
    )
    out["BVRT_VS_NUMERIC_NONPASS"] = contrast(token.isin(["BV", "RT"]))
    out["BV_VS_NUMERIC_NONPASS"] = contrast(token.eq("BV"))
    out["RT_VS_NUMERIC_NONPASS"] = contrast(token.eq("RT"))
    return out
