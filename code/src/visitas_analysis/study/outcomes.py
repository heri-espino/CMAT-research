from __future__ import annotations

import numpy as np
import pandas as pd


def _silverman_bandwidth(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return 0.1
    sd = np.std(x, ddof=1)
    q75, q25 = np.percentile(x, [75, 25])
    iqr = q75 - q25
    scale = min(sd, iqr / 1.34) if iqr > 0 else sd
    h = 0.9 * scale * n ** (-1 / 5)
    return max(float(h), 1e-3)


def _kde_draws(obs: np.ndarray, size: int, low: float, high: float, rng) -> np.ndarray:
    obs = np.asarray(obs, dtype=float)
    h = _silverman_bandwidth(obs)
    out = np.empty(size, dtype=float)
    k = 0
    while k < size:
        batch = max(size - k, 32)
        idx = rng.integers(0, len(obs), size=batch)
        cand = obs[idx] + rng.normal(0.0, h, size=batch)
        cand = cand[(cand >= low) & (cand <= high)]
        take = min(len(cand), size - k)
        if take:
            out[k:k + take] = cand[:take]
            k += take
    return out


def _uniform_quantiles(size: int, low: float, high: float) -> np.ndarray:
    if size <= 0:
        return np.array([], dtype=float)
    k = np.arange(1, size + 1, dtype=float)
    return low + (k / (size + 1.0)) * (high - low)


def add_primary_outcomes(df: pd.DataFrame, config) -> pd.DataFrame:
    """Create the primary continuous outcome and the secondary pass outcome.

    Primary: adverse outcomes (BV/RT/BA) are imputed below the passing threshold
    within professor x period, then standardized within that same context.
    Numeric grades are never changed. Complete-case and uniform-imputation
    variants are retained as sensitivity outcomes.
    """
    out = df.copy()
    rng = np.random.default_rng(config.random_seed)
    upper = float(config.imputation_upper_bound)

    out["GRADE_PRIMARY"] = out["GRADE_NUMERIC"].astype(float)
    out["GRADE_UNIFORM_SENS"] = out["GRADE_NUMERIC"].astype(float)
    out["PASS"] = np.nan
    numeric = out["GRADE_CLASS"] == "numeric"
    adverse = out["GRADE_CLASS"] == "adverse"
    out.loc[numeric, "PASS"] = (out.loc[numeric, "GRADE_NUMERIC"] >= config.passing_grade).astype(int)
    out.loc[adverse, "PASS"] = 0

    imputation_rows: list[dict[str, object]] = []
    grouped = out.groupby("CLASSROOM_ID", sort=False).groups
    # Iterate classrooms by their earliest source row, not by the literal
    # professor identifier. This makes results invariant to HMAC renaming.
    group_items = sorted(
        grouped.items(),
        key=lambda item: int(out.loc[list(item[1]), "SOURCE_ROW"].min()) if "SOURCE_ROW" in out.columns else 0,
    )
    for classroom_id, idx in group_items:
        idx = list(idx)
        g = out.loc[idx]
        need_mask = g["GRADE_CLASS"] == "adverse"
        if "SOURCE_ROW" in g.columns:
            need_idx = g.loc[need_mask].sort_values("SOURCE_ROW").index.to_numpy()
        else:
            need_idx = g.index[need_mask].to_numpy()
        n_need = len(need_idx)
        if n_need == 0:
            continue
        pool = np.sort(g.loc[
            (g["GRADE_CLASS"] == "numeric") & (g["GRADE_NUMERIC"] <= upper),
            "GRADE_NUMERIC",
        ].dropna().to_numpy(float))
        if len(pool) >= config.imputation_min_kde_n:
            draws = _kde_draws(pool, n_need, 0.0, upper, rng)
            method = "within_classroom_kde"
        elif len(pool) > 0:
            draws = rng.choice(pool, size=n_need, replace=True)
            method = "within_classroom_empirical"
        else:
            draws = _uniform_quantiles(n_need, 0.0, upper)
            method = "uniform_fallback_no_subpass_pool"
        out.loc[need_idx, "GRADE_PRIMARY"] = np.clip(draws, 0.0, upper)
        out.loc[need_idx, "GRADE_UNIFORM_SENS"] = _uniform_quantiles(n_need, 0.0, upper)
        imputation_rows.append({
            "CLASSROOM_ID": classroom_id,
            "n_adverse_imputed": n_need,
            "n_numeric_below_pass_pool": int(len(pool)),
            "method": method,
        })

    # Standardize inside the professor x period context. Tiny/constant groups
    # are marked missing rather than assigned an artificial zero effect.
    def zscore(series: pd.Series) -> pd.Series:
        if series.notna().sum() < config.min_classroom_n_for_z:
            return pd.Series(np.nan, index=series.index)
        sd = series.std(ddof=1)
        if pd.isna(sd) or sd == 0:
            return pd.Series(np.nan, index=series.index)
        return (series - series.mean()) / sd

    out["Z_GRADE_PRIMARY"] = out.groupby("CLASSROOM_ID", group_keys=False)["GRADE_PRIMARY"].apply(zscore)
    out["Z_GRADE_UNIFORM_SENS"] = out.groupby("CLASSROOM_ID", group_keys=False)["GRADE_UNIFORM_SENS"].apply(zscore)

    # Complete-case standardization: useful only as a sensitivity analysis,
    # because adverse academic outcomes are intentionally absent here.
    out["GRADE_COMPLETE_CASE"] = out["GRADE_NUMERIC"].where(out["GRADE_CLASS"] == "numeric")
    out["Z_GRADE_COMPLETE_CASE"] = out.groupby("CLASSROOM_ID", group_keys=False)["GRADE_COMPLETE_CASE"].apply(zscore)

    out.attrs["imputation_summary"] = pd.DataFrame(imputation_rows)
    return out
