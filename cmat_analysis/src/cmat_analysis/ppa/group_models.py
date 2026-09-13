"""Stable categorical uptake models for PPA participation analyses."""

from __future__ import annotations

from collections.abc import Sequence
import warnings

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

from .encouragement import DEFAULT_VISIT_GROUP_ORDER, _collapse_rare_categories


def _fit_finite_mnlogit(formula: str, data: pd.DataFrame):
    """Fit MNLogit with conservative optimizer fallbacks and finite-result checks."""
    attempts: list[str] = []
    for method in ("lbfgs", "bfgs", "newton"):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                fit = smf.mnlogit(formula, data=data).fit(
                    method=method,
                    maxiter=1000,
                    disp=False,
                )
            finite = bool(
                np.isfinite(float(fit.llf))
                and np.isfinite(np.asarray(fit.params, dtype=float)).all()
            )
            converged = bool(fit.mle_retvals.get("converged", False))
            if finite and converged:
                return fit, method
            attempts.append(
                f"{method}: converged={converged}, finite={finite}, llf={fit.llf}"
            )
        except Exception as exc:  # pragma: no cover - optimizer-dependent fallback
            attempts.append(f"{method}: {type(exc).__name__}: {exc}")
    raise RuntimeError(
        "Multinomial model failed to produce a finite converged solution; "
        + " | ".join(attempts)
    )


def professor_visit_group_multinomial_increment(
    df: pd.DataFrame,
    *,
    group_col: str,
    professor_col: str,
    period_col: str,
    career_col: str | None = None,
    min_career_n: int = 30,
    group_order: Sequence[str] = DEFAULT_VISIT_GROUP_ORDER,
) -> pd.DataFrame:
    """Test whether instructor identity adds fit for 0/1-2/3/4+ uptake groups.

    The estimator fits nested multinomial-logit models, first with academic
    period and optional degree-programme controls and then with instructor fixed
    effects added. Optimizer fallbacks are accepted only when both nested models
    converge to finite likelihoods, preventing silent propagation of NaN
    likelihood-ratio statistics under sparse exact-threshold cells.

    Parameters
    ----------
    df : pandas.DataFrame
        Student-level analytical data.
    group_col : str
        Mutually exclusive service-use group.
    professor_col : str
        Instructor identifier.
    period_col : str
        Academic-period identifier.
    career_col : str or None, optional
        Optional degree-programme control.
    min_career_n : int, default=30
        Minimum programme sample size before pooling smaller programmes.
    group_order : sequence of str, default=("0", "1-2", "3", "4+")
        Visit-group order used to encode the multinomial outcome.

    Returns
    -------
    pandas.DataFrame
        One-row likelihood-ratio comparison between period/career controls and
        the same model plus instructor fixed effects, including McFadden
        pseudo-R-squared values and the successful optimizers.
    """
    required = {group_col, professor_col, period_col}
    if career_col is not None:
        required.add(career_col)
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")

    groups = tuple(str(group) for group in group_order)
    d = df[list(required)].dropna(
        subset=[group_col, professor_col, period_col]
    ).copy()
    d[group_col] = d[group_col].astype(str)
    d = d.loc[d[group_col].isin(groups)].copy()
    observed_groups = tuple(group for group in groups if group in set(d[group_col]))
    if len(observed_groups) != len(groups):
        missing_groups = [group for group in groups if group not in observed_groups]
        raise ValueError(f"Requested visit groups absent from data: {missing_groups}")

    d["_GROUP_CODE"] = d[group_col].map(
        {group: i for i, group in enumerate(groups)}
    ).astype(int)
    rhs = [f"C({period_col})"]
    if career_col is not None:
        d["_MODEL_CAREER"] = _collapse_rare_categories(d[career_col], min_career_n)
        rhs.append("C(_MODEL_CAREER)")

    base_formula = "_GROUP_CODE ~ " + " + ".join(rhs)
    full_formula = base_formula + f" + C({professor_col})"
    base, base_method = _fit_finite_mnlogit(base_formula, d)
    full, full_method = _fit_finite_mnlogit(full_formula, d)

    lr = float(2.0 * (full.llf - base.llf))
    df_diff = int(round(full.df_model - base.df_model))
    if lr < -1e-8:
        raise RuntimeError(
            f"Nested multinomial fit produced a negative likelihood-ratio statistic: {lr}"
        )
    lr = max(lr, 0.0)
    p_value = float(stats.chi2.sf(lr, df_diff))
    ll_null = float(full.llnull)
    if not np.isfinite(ll_null) or ll_null == 0:
        raise RuntimeError("Multinomial null log-likelihood is not finite.")
    base_pr2 = float(1.0 - base.llf / ll_null)
    full_pr2 = float(1.0 - full.llf / ll_null)

    return pd.DataFrame([{
        "outcome": group_col,
        "n": int(full.nobs),
        "groups": "|".join(groups),
        "professors": int(d[professor_col].nunique()),
        "periods": int(d[period_col].nunique()),
        "mcfadden_r2_base": base_pr2,
        "mcfadden_r2_plus_professor": full_pr2,
        "delta_mcfadden_r2_professor": float(full_pr2 - base_pr2),
        "lr_stat_professor": lr,
        "lr_df": df_diff,
        "lr_p_professor": p_value,
        "base_optimizer": base_method,
        "full_optimizer": full_method,
        "base_converged": True,
        "full_converged": True,
        "note": (
            "descriptive multinomial association; exact group 3 is retained as "
            "an institutionally salient category; instructor identity is not randomized"
        ),
    }])
