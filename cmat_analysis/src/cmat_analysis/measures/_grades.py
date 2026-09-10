from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde


def _scipy_default_kde_draws(
    obs: np.ndarray,
    size: int,
    low: float,
    high: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, float | None, str]:
    """Draw from scipy.stats.gaussian_kde using SciPy's default bandwidth.

    Parameters
    ----------
    obs:
        Observed numeric grades strictly below the passing threshold in the
        same classroom.
    size:
        Number of adverse non-numeric outcomes to impute.
    low, high:
        Truncation interval [low, high). For this study high is 7.5, the
        passing threshold; draws at/above high are rejected.
    rng:
        NumPy Generator used as the seed source for deterministic resampling.

    Notes
    -----
    ``gaussian_kde(..., bw_method=None)`` is SciPy's default. In one dimension
    it uses Scott's factor n**(-1/5) multiplying the sample covariance scale.
    A Gaussian kernel is used. Truncation is implemented by rejection sampling
    so imputed adverse outcomes cannot cross the passing threshold.

    If the observed pool is degenerate (fewer than two observations or zero
    variance), a KDE covariance matrix cannot be estimated. In that narrow
    case the empirical sub-pass distribution is resampled instead. A uniform
    fallback is reserved for classrooms with *no* observed numeric grade below
    the threshold.
    """
    obs = np.asarray(obs, dtype=float)
    obs = obs[np.isfinite(obs)]
    if size <= 0:
        return np.array([], dtype=float), None, "none"
    if len(obs) == 0:
        raise ValueError("KDE requested with an empty observed pool")

    if len(obs) < 2 or float(np.std(obs, ddof=1)) == 0.0:
        draws = rng.choice(obs, size=size, replace=True).astype(float)
        return np.clip(draws, low, np.nextafter(high, low)), None, "within_classroom_empirical_degenerate_kde"

    kde = gaussian_kde(obs, bw_method=None)
    factor = float(kde.factor)
    out = np.empty(size, dtype=float)
    k = 0
    while k < size:
        batch = max(64, 3 * (size - k))
        cand = np.asarray(kde.resample(batch, seed=rng)).reshape(-1)
        cand = cand[(cand >= low) & (cand < high)]
        take = min(len(cand), size - k)
        if take:
            out[k:k + take] = cand[:take]
            k += take
    return out, factor, "within_classroom_scipy_gaussian_kde_default_scott"


def _uniform_draws(size: int, low: float, high: float, rng: np.random.Generator) -> np.ndarray:
    """Random U(low, high) draws; high is exclusive for NumPy's Generator."""
    if size <= 0:
        return np.array([], dtype=float)
    return rng.uniform(low, high, size=size)


def _uniform_quantiles(size: int, low: float, high: float) -> np.ndarray:
    """Deterministic interior points from a uniform distribution.

    Retained only as a sensitivity outcome so that repeated runs are exactly
    comparable independently of the random generator state.
    """
    if size <= 0:
        return np.array([], dtype=float)
    k = np.arange(1, size + 1, dtype=float)
    return low + (k / (size + 1.0)) * (high - low)


def add_primary_outcomes(df: pd.DataFrame, config) -> pd.DataFrame:
    """Create continuous classroom-relative performance and pass/fail outcomes.
    
    Primary continuous outcome
    --------------------------
    1. Numeric final grades are never changed.
    2. BV/RT/BA are treated as adverse academic outcomes. Within each
       ``CLASSROOM_ID``, collect observed numeric grades strictly below 7.5.
    3. For a non-degenerate pool, fit
       ``scipy.stats.gaussian_kde(pool, bw_method=None)`` (Scott default), draw
       from it, and reject draws outside [0, 7.5).
    4. A non-empty but degenerate pool uses empirical resampling.
    5. A classroom with no observed numeric sub-pass grade uses U(0, 7.5).
    6. The completed grade distribution is standardized within classroom.
    
    ``Z_GRADE_UNIFORM_SENS`` and ``Z_GRADE_COMPLETE_CASE`` are retained as
    sensitivity outcomes. ``PASS`` never assigns an artificial numeric grade.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input analytical table containing the columns named by the other arguments.
    config : object
        Configuration object supplying the existing study or peak-detection parameters required by the function.
    
    Returns
    -------
    pd.DataFrame
        Copy of the cohort table with primary/sensitivity grade measures, pass indicator, classroom-standardized outcomes, and an imputation-audit DataFrame stored in ``attrs``.
    """
    out = df.copy()
    rng = np.random.default_rng(config.random_seed)
    low = 0.0
    high = float(config.passing_grade)
    high_interior = np.nextafter(high, low)

    out["GRADE_PRIMARY"] = out["GRADE_NUMERIC"].astype(float)
    out["GRADE_UNIFORM_SENS"] = out["GRADE_NUMERIC"].astype(float)
    out["PASS"] = np.nan
    numeric = out["GRADE_CLASS"] == "numeric"
    adverse = out["GRADE_CLASS"] == "adverse"
    out.loc[numeric, "PASS"] = (out.loc[numeric, "GRADE_NUMERIC"] >= config.passing_grade).astype(int)
    out.loc[adverse, "PASS"] = 0

    imputation_rows: list[dict[str, object]] = []
    grouped = out.groupby("CLASSROOM_ID", sort=False).groups
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

        pool = np.sort(
            g.loc[
                (g["GRADE_CLASS"] == "numeric") & (g["GRADE_NUMERIC"] < high),
                "GRADE_NUMERIC",
            ].dropna().to_numpy(float)
        )

        kde_factor: float | None = None
        if len(pool) > 0:
            draws, kde_factor, method = _scipy_default_kde_draws(pool, n_need, low, high, rng)
        else:
            draws = _uniform_draws(n_need, low, high, rng)
            method = "uniform_fallback_no_observed_subpass_grade"

        out.loc[need_idx, "GRADE_PRIMARY"] = np.clip(draws, low, high_interior)
        out.loc[need_idx, "GRADE_UNIFORM_SENS"] = _uniform_quantiles(n_need, low, high)
        imputation_rows.append({
            "CLASSROOM_ID": classroom_id,
            "n_adverse_imputed": n_need,
            "n_numeric_below_pass_pool": int(len(pool)),
            "n_unique_numeric_below_pass_pool": int(len(np.unique(pool))),
            "method": method,
            "kde_library": "scipy.stats.gaussian_kde" if "kde" in method else None,
            "kde_bw_method": "None (SciPy default; Scott factor)" if "scipy_gaussian_kde" in method else None,
            "kde_factor": kde_factor,
            "support_low": low,
            "support_high_exclusive": high,
            "seed": int(config.random_seed),
        })

    def zscore(series: pd.Series) -> pd.Series:
        if series.notna().sum() < config.min_classroom_n_for_z:
            return pd.Series(np.nan, index=series.index)
        sd = series.std(ddof=1)
        if pd.isna(sd) or sd == 0:
            return pd.Series(np.nan, index=series.index)
        return (series - series.mean()) / sd

    out["Z_GRADE_PRIMARY"] = out.groupby("CLASSROOM_ID", group_keys=False)["GRADE_PRIMARY"].apply(zscore)
    out["Z_GRADE_UNIFORM_SENS"] = out.groupby("CLASSROOM_ID", group_keys=False)["GRADE_UNIFORM_SENS"].apply(zscore)
    out["GRADE_COMPLETE_CASE"] = out["GRADE_NUMERIC"].where(out["GRADE_CLASS"] == "numeric")
    out["Z_GRADE_COMPLETE_CASE"] = out.groupby("CLASSROOM_ID", group_keys=False)["GRADE_COMPLETE_CASE"].apply(zscore)

    out.attrs["imputation_summary"] = pd.DataFrame(imputation_rows)
    return out
