from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.signal import find_peaks


@dataclass(frozen=True)
class TemporalPeakConfig:
    """Configuration for descriptive temporal peak detection.
    
    Parameters
    ----------
    rolling_window_days : int, default=7
        Width of the centered rolling window used to smooth daily activity.
    min_peak_distance_days : int, default=21
        Minimum separation in days between detected rolling peaks.
    prominence_fraction : float, default=0.12
        Fraction of a period's maximum smoothed activity used in the adaptive
        prominence threshold.
    min_prominence : float, default=5.0
        Absolute lower bound for the peak-prominence threshold.
    monthly_interval_low_days : int, default=24
        Lower bound used to label a consecutive peak interval as approximately monthly.
    monthly_interval_high_days : int, default=38
        Upper bound used to label a consecutive peak interval as approximately monthly.
    
    Notes
    -----
    Peak detection is descriptive. The configuration does not encode an examination
    calendar and therefore cannot identify a peak as an exam-related event by itself.
    """
    rolling_window_days: int = 7
    min_peak_distance_days: int = 21
    prominence_fraction: float = 0.12
    min_prominence: float = 5.0
    monthly_interval_low_days: int = 24
    monthly_interval_high_days: int = 38


def primary_period_visit_events(mu: pd.DataFrame, advisories: pd.DataFrame) -> pd.DataFrame:
    """Return every CMAT visit made during each student's first-MU academic period.
    
    The PPA rule counts any CMAT visit in the term.  The academic file does not
    contain an exact withdrawal date, so the finest defensible temporal link is
    student x year x session.  VISIT_DATE is calendar-day resolution; the exact
    timestamp is retained internally only to order visits within a day.
    
    Parameters
    ----------
    mu : pd.DataFrame
        Primary MU cohort whose student-year-session keys define the periods to retain.
    advisories : pd.DataFrame
        CMAT advisory-event table with normalized student and academic-period identifiers.
    
    Returns
    -------
    pd.DataFrame
        Computed table or tables containing the quantities described above.
    """
    keys = mu[["STUDENT_ID", "YEAR", "SESSION"]].drop_duplicates()
    out = advisories.merge(keys, on=["STUDENT_ID", "YEAR", "SESSION"], how="inner")
    out = out.copy()
    out["VISIT_DATE"] = pd.to_datetime(out["VISIT_DATETIME"], errors="coerce").dt.normalize()
    out["VISIT_WEEKDAY"] = out["VISIT_DATE"].dt.day_name()
    out["VISIT_DAY_OF_MONTH"] = out["VISIT_DATE"].dt.day
    out["VISIT_MONTH"] = out["VISIT_DATE"].dt.month
    return out.sort_values(["STUDENT_ID", "VISIT_DATETIME"], kind="stable").reset_index(drop=True)


def daily_service_counts(events: pd.DataFrame, population: str) -> pd.DataFrame:
    """Aggregate visit events to daily service volume within academic periods.
    
    Parameters
    ----------
    events : pd.DataFrame
        CMAT visit-event table containing student, period, and timestamp information.
    population : str
        Label identifying the analyzed population in returned tables.
    
    Returns
    -------
    pd.DataFrame
        Computed table or tables containing the quantities described above.
    """
    d = events.copy()
    if "VISIT_DATE" not in d.columns:
        d["VISIT_DATE"] = pd.to_datetime(d["VISIT_DATETIME"], errors="coerce").dt.normalize()
    out = (
        d.groupby(["YEAR", "SESSION", "VISIT_DATE"], observed=True)
        .agg(
            visits=("STUDENT_ID", "size"),
            unique_students=("STUDENT_ID", "nunique"),
        )
        .reset_index()
        .sort_values(["YEAR", "SESSION", "VISIT_DATE"])
    )
    out.insert(0, "population", population)
    return out


def same_day_ppa_behavior(
    mu: pd.DataFrame,
    mu_events: pd.DataFrame,
    threshold: int = 3,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Characterize concentrated same-day attendance around the PPA threshold.
    
    
    Parameters
    ----------
    mu : pd.DataFrame
        Primary MU cohort table with one row per student attempt.
    mu_events : pd.DataFrame
        Visit-event table restricted to the relevant MU periods.
    threshold : int, default=3
        Visit count defining PPA completion for the same-day concentration diagnostics.
    Returns
    -------
    student_summary:
        One row per primary-cohort student with same-day behavior fields.
    aggregate_summary:
        Compact counts/rates for the manuscript and README.
    max_daily_distribution:
        Distribution of maximum visits made by a student on a single day.
    completion_dates:
        Aggregate dates on which students reached their threshold-th visit.
    
    No behavioral motive is inferred.  In particular, three visits in one day
    is described as concentrated attendance, not "gaming" the incentive.
    
    Notes
    -----
    Concentrated same-day attendance is described behaviorally without inferring strategic intent or “gaming.”
    """
    threshold = int(threshold)
    events = mu_events.sort_values(["STUDENT_ID", "VISIT_DATETIME"], kind="stable").copy()
    events["VISIT_ORDINAL"] = events.groupby("STUDENT_ID").cumcount() + 1

    daily = (
        events.groupby(["STUDENT_ID", "YEAR", "SESSION", "VISIT_DATE"], observed=True)
        .size()
        .rename("VISITS_SAME_DAY")
        .reset_index()
    )
    max_daily = (
        daily.groupby("STUDENT_ID", observed=True)["VISITS_SAME_DAY"]
        .max()
        .rename("MAX_VISITS_ONE_DAY")
    )

    first_n = events.loc[events["VISIT_ORDINAL"] <= threshold].copy()
    first_n_summary = (
        first_n.groupby("STUDENT_ID", observed=True)
        .agg(
            N_FIRST_THRESHOLD_ROWS=("VISIT_ORDINAL", "size"),
            N_DATES_FIRST_THRESHOLD=("VISIT_DATE", "nunique"),
            FIRST_VISIT_DATE=("VISIT_DATE", "min"),
        )
    )

    completion = events.loc[events["VISIT_ORDINAL"] == threshold, ["STUDENT_ID", "VISIT_DATE"]].copy()
    completion = completion.rename(columns={"VISIT_DATE": "PPA_COMPLETION_DATE"})
    completion = completion.merge(
        daily[["STUDENT_ID", "VISIT_DATE", "VISITS_SAME_DAY"]],
        left_on=["STUDENT_ID", "PPA_COMPLETION_DATE"],
        right_on=["STUDENT_ID", "VISIT_DATE"],
        how="left",
    ).drop(columns=["VISIT_DATE"])
    completion = completion.rename(columns={"VISITS_SAME_DAY": "VISITS_ON_PPA_COMPLETION_DATE"})

    student = mu[["STUDENT_ID", "YEAR", "SESSION", "VISITS_CMAT_PERIOD"]].copy()
    student = student.merge(max_daily, on="STUDENT_ID", how="left")
    student = student.merge(first_n_summary, on="STUDENT_ID", how="left")
    student = student.merge(completion, on="STUDENT_ID", how="left")
    student["MAX_VISITS_ONE_DAY"] = student["MAX_VISITS_ONE_DAY"].fillna(0).astype(int)
    student["PPA_REACHED"] = (student["VISITS_CMAT_PERIOD"] >= threshold).astype(int)
    student["ANY_2PLUS_SAME_DAY"] = (student["MAX_VISITS_ONE_DAY"] >= 2).astype(int)
    student["ANY_3PLUS_SAME_DAY"] = (student["MAX_VISITS_ONE_DAY"] >= threshold).astype(int)
    student["FIRST_3_VISITS_SAME_DAY"] = (
        (student["N_FIRST_THRESHOLD_ROWS"].fillna(0) >= threshold)
        & (student["N_DATES_FIRST_THRESHOLD"].fillna(np.inf) == 1)
    ).astype(int)
    student["PPA_COMPLETION_DAY_2PLUS"] = (
        student["VISITS_ON_PPA_COMPLETION_DATE"].fillna(0) >= 2
    ).astype(int)
    student["PPA_COMPLETION_DAY_3PLUS"] = (
        student["VISITS_ON_PPA_COMPLETION_DATE"].fillna(0) >= threshold
    ).astype(int)

    ppa = student.loc[student["PPA_REACHED"] == 1]
    visitors = student.loc[student["VISITS_CMAT_PERIOD"] > 0]

    rows = [
        ("primary_cohort_students", len(student), len(student)),
        ("students_with_any_visit", len(visitors), len(student)),
        ("students_reaching_ppa_ge3", len(ppa), len(student)),
        ("visitors_with_any_2plus_same_day", int(visitors["ANY_2PLUS_SAME_DAY"].sum()), len(visitors)),
        ("visitors_with_any_3plus_same_day", int(visitors["ANY_3PLUS_SAME_DAY"].sum()), len(visitors)),
        ("ppa_achievers_with_any_2plus_same_day", int(ppa["ANY_2PLUS_SAME_DAY"].sum()), len(ppa)),
        ("ppa_achievers_with_any_3plus_same_day", int(ppa["ANY_3PLUS_SAME_DAY"].sum()), len(ppa)),
        ("ppa_achievers_first_3_visits_same_day", int(ppa["FIRST_3_VISITS_SAME_DAY"].sum()), len(ppa)),
        ("ppa_achievers_completion_day_2plus", int(ppa["PPA_COMPLETION_DAY_2PLUS"].sum()), len(ppa)),
        ("ppa_achievers_completion_day_3plus", int(ppa["PPA_COMPLETION_DAY_3PLUS"].sum()), len(ppa)),
    ]
    aggregate = pd.DataFrame(rows, columns=["metric", "count", "denominator"])
    aggregate["proportion"] = np.where(
        aggregate["denominator"] > 0,
        aggregate["count"] / aggregate["denominator"],
        np.nan,
    )

    def _max_bucket(v: int) -> str:
        if v <= 0:
            return "0"
        if v == 1:
            return "1"
        if v == 2:
            return "2"
        return "3+"

    student["MAX_DAILY_BUCKET"] = student["MAX_VISITS_ONE_DAY"].map(_max_bucket)
    maxdist = (
        student.groupby(["PPA_REACHED", "MAX_DAILY_BUCKET"], observed=True)
        .size().rename("students").reset_index()
    )
    denom = student.groupby("PPA_REACHED").size().rename("denominator")
    maxdist = maxdist.merge(denom, on="PPA_REACHED", how="left")
    maxdist["proportion"] = maxdist["students"] / maxdist["denominator"]

    completion_dates = (
        ppa.dropna(subset=["PPA_COMPLETION_DATE"])
        .groupby(["YEAR", "SESSION", "PPA_COMPLETION_DATE"], observed=True)
        .agg(
            students_reaching_ppa=("STUDENT_ID", "nunique"),
            students_reaching_ppa_with_3plus_that_day=("PPA_COMPLETION_DAY_3PLUS", "sum"),
        )
        .reset_index()
        .sort_values(["YEAR", "SESSION", "PPA_COMPLETION_DATE"])
    )
    return student, aggregate, maxdist, completion_dates


def top_daily_dates(daily: pd.DataFrame, n: int = 25) -> pd.DataFrame:
    """Return the busiest observed service dates from an aggregated daily table.
    
    Parameters
    ----------
    daily : pd.DataFrame
        Daily service-count table, typically returned by ``daily_service_counts``.
    n : int, default=25
        Number of rows to retain.
    
    Returns
    -------
    pd.DataFrame
        Computed table or tables containing the quantities described above.
    """
    return (
        daily.sort_values(["unique_students", "visits"], ascending=False)
        .head(int(n))
        .reset_index(drop=True)
    )


def detect_period_peaks(
    events: pd.DataFrame,
    config: TemporalPeakConfig | None = None,
    population: str = "All CMAT",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Detect separated local peaks in daily CMAT activity.
    
    Detection is deliberately descriptive.  It uses a centered 7-day rolling
    sum of unique-student-days, minimum 21-day separation, and a prominence
    threshold equal to max(5, 12% of the period maximum).  Peaks are not labeled
    as exams unless an official exam calendar is supplied separately.
    
    Parameters
    ----------
    events : pd.DataFrame
        CMAT visit-event table containing student, period, and timestamp information.
    config : TemporalPeakConfig | None, default=None
        Optional temporal-peak configuration. ``None`` uses ``TemporalPeakConfig()``.
    population : str, default='All CMAT'
        Label identifying the analyzed population in returned tables.
    
    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
        Tuple containing detected peaks, complete daily period profiles, and consecutive peak intervals.
    """
    cfg = config or TemporalPeakConfig()
    d = events.copy()
    if "VISIT_DATE" not in d.columns:
        d["VISIT_DATE"] = pd.to_datetime(d["VISIT_DATETIME"], errors="coerce").dt.normalize()

    peak_rows: list[dict[str, object]] = []
    profile_rows: list[pd.DataFrame] = []
    interval_rows: list[dict[str, object]] = []

    for (year, session), g in d.groupby(["YEAR", "SESSION"], observed=True):
        by_day = (
            g.groupby("VISIT_DATE", observed=True)
            .agg(visits=("STUDENT_ID", "size"), unique_students=("STUDENT_ID", "nunique"))
            .sort_index()
        )
        if by_day.empty:
            continue
        idx = pd.date_range(by_day.index.min(), by_day.index.max(), freq="D")
        full = by_day.reindex(idx, fill_value=0)
        full.index.name = "VISIT_DATE"
        full["rolling_unique_student_days_7d"] = (
            full["unique_students"].rolling(cfg.rolling_window_days, center=True, min_periods=1).sum()
        )
        full["rolling_visits_7d"] = (
            full["visits"].rolling(cfg.rolling_window_days, center=True, min_periods=1).sum()
        )
        prominence = max(
            cfg.min_prominence,
            cfg.prominence_fraction * float(full["rolling_unique_student_days_7d"].max()),
        )
        peaks, props = find_peaks(
            full["rolling_unique_student_days_7d"].to_numpy(dtype=float),
            distance=cfg.min_peak_distance_days,
            prominence=prominence,
        )
        # The rolling maximum can fall on a weekend/zero-visit day because the
        # window is centered.  For a human-interpretable peak date, snap each
        # detected rolling center to the busiest actual calendar day within
        # +/-3 days, while retaining the rolling-center date for auditability.
        actual_peak_dates: list[pd.Timestamp] = []
        for order, p in enumerate(peaks, start=1):
            lo = max(0, p - 3)
            hi = min(len(full) - 1, p + 3)
            window = full.iloc[lo:hi + 1].copy()
            actual_date = (
                window.reset_index()
                .sort_values(["unique_students", "visits", "VISIT_DATE"], ascending=[False, False, True])
                .iloc[0]["VISIT_DATE"]
            )
            actual_pos = int(full.index.get_loc(actual_date))
            actual_peak_dates.append(pd.Timestamp(actual_date))
            peak_rows.append({
                "population": population,
                "YEAR": int(year),
                "SESSION": session,
                "peak_order": order,
                "peak_date": pd.Timestamp(actual_date),
                "rolling_peak_center_date": pd.Timestamp(idx[p]),
                "daily_visits": int(full.iloc[actual_pos]["visits"]),
                "daily_unique_students": int(full.iloc[actual_pos]["unique_students"]),
                "rolling_unique_student_days_7d": float(full.iloc[p]["rolling_unique_student_days_7d"]),
                "rolling_visits_7d": float(full.iloc[p]["rolling_visits_7d"]),
                "prominence": float(props["prominences"][order - 1]),
                "detection_prominence_threshold": float(prominence),
            })
        peak_dates = pd.DatetimeIndex(actual_peak_dates)
        if len(peak_dates) >= 2:
            gaps = np.diff(peak_dates.values).astype("timedelta64[D]").astype(int)
            for j, gap in enumerate(gaps, start=1):
                interval_rows.append({
                    "population": population,
                    "YEAR": int(year),
                    "SESSION": session,
                    "from_peak_order": j,
                    "to_peak_order": j + 1,
                    "from_peak_date": peak_dates[j - 1],
                    "to_peak_date": peak_dates[j],
                    "gap_days": int(gap),
                    "monthly_like_24_38_days": int(
                        cfg.monthly_interval_low_days <= int(gap) <= cfg.monthly_interval_high_days
                    ),
                })

        prof = full.reset_index()
        prof.insert(0, "population", population)
        prof.insert(1, "YEAR", int(year))
        prof.insert(2, "SESSION", session)
        prof["day_from_first_observed_visit"] = (
            prof["VISIT_DATE"] - prof["VISIT_DATE"].min()
        ).dt.days
        profile_rows.append(prof)

    peaks_df = pd.DataFrame(peak_rows)
    profiles_df = pd.concat(profile_rows, ignore_index=True) if profile_rows else pd.DataFrame()
    intervals_df = pd.DataFrame(interval_rows)
    return peaks_df, profiles_df, intervals_df


def peak_spacing_summary(
    peaks: pd.DataFrame,
    intervals: pd.DataFrame,
    config: TemporalPeakConfig | None = None,
) -> pd.DataFrame:
    """Summarize the number and spacing of detected service-use peaks.
    
    Parameters
    ----------
    peaks : pd.DataFrame
        Detected peak table returned by ``detect_period_peaks``.
    intervals : pd.DataFrame
        Peak-to-peak interval table returned by ``detect_period_peaks``.
    config : TemporalPeakConfig | None, default=None
        Optional temporal-peak configuration supplying the monthly-like gap bounds.
    
    Returns
    -------
    pd.DataFrame
        Computed table or tables containing the quantities described above.
    """
    cfg = config or TemporalPeakConfig()
    if peaks.empty:
        return pd.DataFrame()
    per_period = (
        peaks.groupby(["population", "YEAR", "SESSION"], observed=True)
        .size().rename("detected_peaks").reset_index()
    )
    rows: list[dict[str, object]] = []
    for population, g in per_period.groupby("population", observed=True):
        ints = intervals.loc[intervals["population"] == population, "gap_days"] if not intervals.empty else pd.Series(dtype=float)
        rows.append({
            "population": population,
            "periods_analyzed": int(len(g)),
            "median_detected_peaks_per_period": float(g["detected_peaks"].median()),
            "periods_with_3_peaks": int((g["detected_peaks"] == 3).sum()),
            "periods_with_4_peaks": int((g["detected_peaks"] == 4).sum()),
            "periods_with_5_peaks": int((g["detected_peaks"] == 5).sum()),
            "peak_intervals_n": int(len(ints)),
            "peak_gap_median_days": float(ints.median()) if len(ints) else np.nan,
            "peak_gap_q25_days": float(ints.quantile(0.25)) if len(ints) else np.nan,
            "peak_gap_q75_days": float(ints.quantile(0.75)) if len(ints) else np.nan,
            "monthly_like_gap_low_days": cfg.monthly_interval_low_days,
            "monthly_like_gap_high_days": cfg.monthly_interval_high_days,
            "monthly_like_intervals": int(
                ((ints >= cfg.monthly_interval_low_days) & (ints <= cfg.monthly_interval_high_days)).sum()
            ) if len(ints) else 0,
            "monthly_like_interval_proportion": float(
                ((ints >= cfg.monthly_interval_low_days) & (ints <= cfg.monthly_interval_high_days)).mean()
            ) if len(ints) else np.nan,
        })
    return pd.DataFrame(rows)



def student_temporal_regularity(
    mu: pd.DataFrame,
    mu_events: pd.DataFrame,
    *,
    visits_col: str = "VISITS_CMAT_PERIOD",
    assessment_cycles: int = 4,
) -> pd.DataFrame:
    """Construct student-level temporal-distribution measures for CMAT use.
    
    The university reports an approximately monthly assessment rhythm (about
    four assessments per standard term), but exact examination dates vary by
    instructor and are not observed.  Therefore the primary regularity metric
    uses *calendar-month spread* rather than labeling any visit as pre-exam.
    
    REGULARITY_MONTHLY_4 = min(active calendar months, 4) / min(total visits, 4)
    
    It is 1 when the student's observed visits are as distributed across
    calendar months as their visit count permits (up to four assessment-cycle
    months), and smaller when visits are temporally concentrated.  Additional
    day/week measures are retained as sensitivity/descriptive metrics.
    
    No causal or motivational interpretation is attached to these measures.
    
    Parameters
    ----------
    mu : pd.DataFrame
        Primary MU cohort table with one row per student attempt.
    mu_events : pd.DataFrame
        Visit-event table restricted to the relevant MU periods.
    visits_col : str, default='VISITS_CMAT_PERIOD'
        Column containing CMAT visit counts.
    assessment_cycles : int, default=4
        Number of assessment-cycle months used to cap the primary regularity measure.
    
    Returns
    -------
    pd.DataFrame
        Computed table or tables containing the quantities described above.
    """
    cycles = int(assessment_cycles)
    if cycles < 2:
        raise ValueError("assessment_cycles must be >= 2")

    base_cols = ["STUDENT_ID", "YEAR", "SESSION", visits_col]
    out = mu[base_cols].drop_duplicates("STUDENT_ID").copy()
    out = out.rename(columns={visits_col: "TOTAL_TERM_VISITS"})

    e = mu_events.copy()
    if "VISIT_DATE" not in e.columns:
        e["VISIT_DATE"] = pd.to_datetime(e["VISIT_DATETIME"], errors="coerce").dt.normalize()
    e = e.dropna(subset=["VISIT_DATE"]).copy()
    e["VISIT_MONTH_KEY"] = e["VISIT_DATE"].dt.to_period("M").astype(str)
    # Monday-anchored week key; exact ISO week numbering is not required.
    e["VISIT_WEEK_KEY"] = e["VISIT_DATE"].dt.to_period("W-SUN").astype(str)

    daily = (
        e.groupby(["STUDENT_ID", "VISIT_DATE"], observed=True)
        .size().rename("N_DAY").reset_index()
    )
    weekly = (
        e.groupby(["STUDENT_ID", "VISIT_WEEK_KEY"], observed=True)
        .size().rename("N_WEEK").reset_index()
    )

    agg = (
        e.groupby("STUDENT_ID", observed=True)
        .agg(
            ACTIVE_DAYS=("VISIT_DATE", "nunique"),
            ACTIVE_WEEKS=("VISIT_WEEK_KEY", "nunique"),
            ACTIVE_CALENDAR_MONTHS=("VISIT_MONTH_KEY", "nunique"),
            FIRST_VISIT_DATE=("VISIT_DATE", "min"),
            LAST_VISIT_DATE=("VISIT_DATE", "max"),
        )
        .reset_index()
    )
    maxday = daily.groupby("STUDENT_ID", observed=True)["N_DAY"].max().rename("MAX_VISITS_ONE_DAY").reset_index()

    # Shannon effective number of weeks: exp(H), where p_w is the share of
    # visits in week w.  The normalized variant is in (0,1] and equals one
    # when every visit occurs in a different week.
    week_rows = []
    for sid, g in weekly.groupby("STUDENT_ID", observed=True):
        counts = g["N_WEEK"].to_numpy(float)
        total = counts.sum()
        p_w = counts / total if total else counts
        h = float(-(p_w * np.log(p_w)).sum()) if total else np.nan
        eff = float(np.exp(h)) if np.isfinite(h) else np.nan
        week_rows.append({
            "STUDENT_ID": sid,
            "WEEK_ENTROPY": h,
            "EFFECTIVE_WEEKS": eff,
            "EFFECTIVE_WEEKS_PER_VISIT": eff / total if total else np.nan,
        })
    week_metrics = pd.DataFrame(week_rows)

    out = out.merge(agg, on="STUDENT_ID", how="left")
    out = out.merge(maxday, on="STUDENT_ID", how="left")
    if not week_metrics.empty:
        out = out.merge(week_metrics, on="STUDENT_ID", how="left")
    else:
        out["WEEK_ENTROPY"] = np.nan
        out["EFFECTIVE_WEEKS"] = np.nan
        out["EFFECTIVE_WEEKS_PER_VISIT"] = np.nan

    zero = out["TOTAL_TERM_VISITS"].fillna(0).astype(int) <= 0
    for c in ["ACTIVE_DAYS", "ACTIVE_WEEKS", "ACTIVE_CALENDAR_MONTHS", "MAX_VISITS_ONE_DAY"]:
        out[c] = out[c].fillna(0).astype(int)
    out["VISIT_SPAN_DAYS"] = (out["LAST_VISIT_DATE"] - out["FIRST_VISIT_DATE"]).dt.days
    out.loc[zero, "VISIT_SPAN_DAYS"] = np.nan
    out["MAX_SAME_DAY_SHARE"] = np.where(
        out["TOTAL_TERM_VISITS"] > 0,
        out["MAX_VISITS_ONE_DAY"] / out["TOTAL_TERM_VISITS"],
        np.nan,
    )
    out["ACTIVE_MONTHS_CAPPED4"] = out["ACTIVE_CALENDAR_MONTHS"].clip(upper=cycles)
    denom = np.minimum(out["TOTAL_TERM_VISITS"].astype(float), float(cycles))
    out["REGULARITY_MONTHLY_4"] = np.where(
        denom > 0,
        out["ACTIVE_MONTHS_CAPPED4"] / denom,
        np.nan,
    )
    out["VISITS_CAPPED_8"] = out["TOTAL_TERM_VISITS"].clip(upper=8).astype(int)
    return out


def monthly_periodicity_diagnostics(
    events: pd.DataFrame,
    *,
    lag_min: int = 14,
    lag_max: int = 45,
    candidate_period_low: int = 21,
    candidate_period_high: int = 42,
    population: str = "All CMAT",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Estimate descriptive monthly-cycle diagnostics from daily service load.
    
    For each academic period, daily unique-student counts are completed with
    zero days, day-of-week means are removed, and the remaining series is
    linearly detrended.  We report autocorrelation by lag and the strongest
    periodogram component within 21--42 days.  These are *cycle diagnostics*;
    they do not identify exam dates or establish that exams caused the peaks.
    
    Parameters
    ----------
    events : pd.DataFrame
        CMAT visit-event table containing student, period, and timestamp information.
    lag_min : int, default=14
        Smallest autocorrelation lag, in days, to evaluate.
    lag_max : int, default=45
        Largest autocorrelation lag, in days, to evaluate.
    candidate_period_low : int, default=21
        Lower bound, in days, of the periodogram search window.
    candidate_period_high : int, default=42
        Upper bound, in days, of the periodogram search window.
    population : str, default='All CMAT'
        Label identifying the analyzed population in returned tables.
    
    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        Tuple containing lagged autocorrelation diagnostics and per-period dominant periodogram components.
    
    Notes
    -----
    The detected cycle is a service-load diagnostic; without an official examination calendar it does not identify exam dates or establish an exam effect.
    """
    from scipy.signal import detrend, periodogram

    e = events.copy()
    if "VISIT_DATE" not in e.columns:
        e["VISIT_DATE"] = pd.to_datetime(e["VISIT_DATETIME"], errors="coerce").dt.normalize()
    acf_rows: list[dict[str, object]] = []
    period_rows: list[dict[str, object]] = []

    for (year, session), g in e.groupby(["YEAR", "SESSION"], observed=True):
        by_day = g.groupby("VISIT_DATE", observed=True)["STUDENT_ID"].nunique().sort_index()
        if len(by_day) < lag_max + 10:
            continue
        idx = pd.date_range(by_day.index.min(), by_day.index.max(), freq="D")
        y = by_day.reindex(idx, fill_value=0).astype(float)
        weekday = pd.Series(idx.dayofweek, index=idx)
        wd_means = y.groupby(weekday).mean()
        resid = y - weekday.map(wd_means).to_numpy()
        resid = pd.Series(detrend(resid.to_numpy(float), type="linear"), index=idx)

        for lag in range(int(lag_min), int(lag_max) + 1):
            a = resid.iloc[:-lag].to_numpy(float)
            b = resid.iloc[lag:].to_numpy(float)
            if len(a) < 10 or np.std(a) == 0 or np.std(b) == 0:
                r = np.nan
            else:
                r = float(np.corrcoef(a, b)[0, 1])
            acf_rows.append({
                "population": population,
                "YEAR": int(year),
                "SESSION": session,
                "lag_days": lag,
                "autocorrelation": r,
                "pairs": len(a),
            })

        freqs, power = periodogram(resid.to_numpy(float), fs=1.0, detrend=False)
        valid = freqs > 0
        periods = np.full(freqs.shape, np.nan, dtype=float)
        periods[valid] = 1.0 / freqs[valid]
        mask = valid & (periods >= candidate_period_low) & (periods <= candidate_period_high)
        if mask.any():
            inds = np.where(mask)[0]
            best = inds[np.argmax(power[inds])]
            best_period = float(periods[best])
            best_power = float(power[best])
        else:
            best_period = np.nan
            best_power = np.nan
        period_rows.append({
            "population": population,
            "YEAR": int(year),
            "SESSION": session,
            "n_calendar_days": int(len(resid)),
            "dominant_period_days_21_42": best_period,
            "dominant_period_power": best_power,
        })

    acf = pd.DataFrame(acf_rows)
    periods = pd.DataFrame(period_rows)
    if not acf.empty:
        # Pair-count weighted mean autocorrelation across terms.
        pooled = (
            acf.dropna(subset=["autocorrelation"])
            .assign(weighted=lambda x: x["autocorrelation"] * x["pairs"])
            .groupby("lag_days", observed=True)
            .agg(weighted_sum=("weighted", "sum"), total_pairs=("pairs", "sum"), periods=("YEAR", "size"))
            .reset_index()
        )
        pooled["pooled_autocorrelation"] = pooled["weighted_sum"] / pooled["total_pairs"]
        pooled.insert(0, "population", population)
        pooled["YEAR"] = np.nan
        pooled["SESSION"] = "POOLED"
        pooled["autocorrelation"] = pooled["pooled_autocorrelation"]
        pooled["pairs"] = pooled["total_pairs"]
        pooled = pooled[["population", "YEAR", "SESSION", "lag_days", "autocorrelation", "pairs", "periods"]]
        acf = pd.concat([acf.assign(periods=1), pooled], ignore_index=True)
    return acf, periods
