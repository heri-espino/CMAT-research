from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


GROUP_ORDER = ["0", "1-2", "3", "4+"]


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_visit_distribution(mu: pd.DataFrame, calc: pd.DataFrame, out: Path, visits_col: str) -> None:
    max_k = 10
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    width = 0.38
    x = np.arange(max_k + 1)
    mu_p = [(mu[visits_col].astype(int) == k).mean() for k in x]
    ca_p = [(calc[visits_col].astype(int) == k).mean() for k in x]
    ax.bar(x - width / 2, mu_p, width=width, label="Matemáticas Universitarias")
    ax.bar(x + width / 2, ca_p, width=width, label="Cálculo I")
    ax.axvline(3, linestyle="--", linewidth=1, label="Umbral PPA = 3")
    ax.set_xlabel("Visitas al CMAT durante el periodo académico")
    ax.set_ylabel("Proporción de estudiantes")
    ax.set_xticks(x)
    ax.legend()
    _save(fig, out / "01_visit_distribution_mu_vs_calculus.png")


def plot_continuation(curves: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    for course, g in curves.groupby("course"):
        ax.plot(g["k"], g["continuation_probability"], marker="o", label=course)
        ax.fill_between(g["k"], g["ci95_low"], g["ci95_high"], alpha=0.15)
    ax.axvline(3, linestyle="--", linewidth=1, label="Umbral PPA = 3")
    ax.set_xlabel("k visitas alcanzadas")
    ax.set_ylabel("P(V ≥ k+1 | V ≥ k)")
    ax.set_ylim(0, 1)
    ax.legend()
    _save(fig, out / "02_continuation_probability.png")


def plot_primary_group_means(summary: pd.DataFrame, out: Path) -> None:
    d = summary.set_index("group").reindex(GROUP_ORDER).dropna(subset=["mean"])
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    x = np.arange(len(d))
    yerr = np.vstack([d["mean"] - d["ci95_low"], d["ci95_high"] - d["mean"]])
    ax.errorbar(x, d["mean"], yerr=yerr, fmt="o", capsize=4)
    ax.axhline(0, linewidth=1, linestyle="--")
    ax.set_xticks(x, d.index)
    ax.set_xlabel("Visitas al CMAT durante el primer intento de MU")
    ax.set_ylabel("Desempeño estandarizado (Z), media e IC95%")
    _save(fig, out / "03_primary_outcome_by_visit_group.png")


def plot_longitudinal_persistence(summary: pd.DataFrame, out: Path) -> None:
    d = summary.set_index("mu_visit_group").reindex(GROUP_ORDER).dropna(subset=["any_calc_visit_proportion"])
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.bar(np.arange(len(d)), d["any_calc_visit_proportion"])
    ax.set_xticks(np.arange(len(d)), d.index)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Grupo de visitas en Matemáticas Universitarias")
    ax.set_ylabel("Proporción con ≥1 visita en Cálculo I")
    _save(fig, out / "04_longitudinal_persistence_to_calculus.png")


def plot_daily_cmat_timeline(daily: pd.DataFrame, out: Path) -> None:
    """Calendar-day service load with a 7-day rolling mean of unique students."""
    d = daily.copy().sort_values("VISIT_DATE")
    if d.empty:
        return
    all_days = pd.date_range(d["VISIT_DATE"].min(), d["VISIT_DATE"].max(), freq="D")
    x = d.set_index("VISIT_DATE")[["visits", "unique_students"]].reindex(all_days, fill_value=0)
    x["unique_students_rolling7_mean"] = x["unique_students"].rolling(7, center=True, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(11.5, 4.8))
    ax.plot(x.index, x["unique_students"], linewidth=0.7, alpha=0.35, label="Estudiantes únicos por día")
    ax.plot(x.index, x["unique_students_rolling7_mean"], linewidth=1.6, label="Media móvil 7 días")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Estudiantes únicos")
    ax.legend()
    _save(fig, out / "05_daily_cmat_timeline.png")


def plot_term_peak_profiles(profiles: pd.DataFrame, peaks: pd.DataFrame, out: Path) -> None:
    """Small multiples of smoothed within-period attendance with detected peaks."""
    if profiles.empty:
        return
    periods = (
        profiles[["YEAR", "SESSION"]].drop_duplicates().sort_values(["YEAR", "SESSION"]).itertuples(index=False, name=None)
    )
    periods = list(periods)
    n = len(periods)
    ncols = 3
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(12.2, 2.8 * nrows), squeeze=False)
    for ax, (year, session) in zip(axes.ravel(), periods):
        g = profiles.loc[(profiles["YEAR"] == year) & (profiles["SESSION"] == session)].copy()
        ax.plot(g["VISIT_DATE"], g["rolling_unique_student_days_7d"], linewidth=1.2)
        pg = peaks.loc[(peaks["YEAR"] == year) & (peaks["SESSION"] == session)]
        if not pg.empty:
            ax.scatter(pg["peak_date"], pg["rolling_unique_student_days_7d"], s=28, zorder=3)
        ax.set_title(f"{int(year)} {session.title()}")
        ax.tick_params(axis="x", rotation=35, labelsize=7)
        ax.tick_params(axis="y", labelsize=8)
    for ax in axes.ravel()[len(periods):]:
        ax.axis("off")
    fig.suptitle("Actividad diaria del CMAT por periodo: suma móvil de 7 días de estudiantes-día", y=1.01)
    fig.supxlabel("Fecha")
    fig.supylabel("Estudiantes-día en ventana de 7 días")
    _save(fig, out / "06_term_temporal_peaks.png")


def plot_same_day_ppa_behavior(maxdist: pd.DataFrame, out: Path) -> None:
    """Maximum number of same-day visits among students who reached the PPA threshold."""
    d = maxdist.loc[maxdist["PPA_REACHED"] == 1].copy()
    if d.empty:
        return
    order = ["1", "2", "3+"]
    d["MAX_DAILY_BUCKET"] = pd.Categorical(d["MAX_DAILY_BUCKET"], categories=order, ordered=True)
    d = d.sort_values("MAX_DAILY_BUCKET")
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.bar(d["MAX_DAILY_BUCKET"].astype(str), d["proportion"])
    ax.set_xlabel("Máximo de visitas del estudiante en un mismo día")
    ax.set_ylabel("Proporción entre quienes alcanzaron PPA")
    ax.set_ylim(0, max(0.05, float(d["proportion"].max()) * 1.12))
    _save(fig, out / "07_same_day_ppa_behavior.png")


def plot_peak_spacing(intervals: pd.DataFrame, summary: pd.DataFrame, out: Path) -> None:
    if intervals.empty:
        return
    d = intervals["gap_days"].dropna().astype(float)
    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    bins = np.arange(max(0, d.min() - 2), d.max() + 5, 4)
    ax.hist(d, bins=bins, edgecolor="white")
    median = float(d.median())
    ax.axvline(median, linestyle="--", linewidth=1.4, label=f"Mediana = {median:.0f} días")
    ax.axvspan(24, 38, alpha=0.12, label="Ventana mensual 24–38 días")
    ax.set_xlabel("Días entre picos detectados consecutivos")
    ax.set_ylabel("Número de intervalos")
    ax.legend()
    _save(fig, out / "08_peak_spacing_days.png")



def plot_monthly_periodicity_acf(acf: pd.DataFrame, out: Path) -> None:
    if acf.empty:
        return
    d = acf.loc[acf["SESSION"] == "POOLED"].dropna(subset=["autocorrelation"]).copy()
    if d.empty:
        return
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    ax.plot(d["lag_days"], d["autocorrelation"], marker="o", markersize=3, linewidth=1.2)
    ax.axvspan(24, 38, alpha=0.12, label="Ventana aproximadamente mensual (24–38 días)")
    best = d.loc[d["autocorrelation"].idxmax()]
    ax.axvline(best["lag_days"], linestyle="--", linewidth=1.2, label=f"Máximo ACF = {int(best['lag_days'])} días")
    ax.set_xlabel("Rezago (días)")
    ax.set_ylabel("Autocorrelación diaria, ajustada por día de semana")
    ax.legend()
    _save(fig, out / "09_monthly_periodicity_acf.png")


def plot_exact3_regularity_performance(summary: pd.DataFrame, out: Path) -> None:
    if summary.empty:
        return
    d = summary.copy().sort_values("active_calendar_months")
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    x = np.arange(len(d))
    yerr = np.vstack([d["mean_z"] - d["ci95_low"], d["ci95_high"] - d["mean_z"]])
    ax.errorbar(x, d["mean_z"], yerr=yerr, fmt="o", capsize=4)
    ax.axhline(0, linewidth=1, linestyle="--")
    ax.set_xticks(x, d["active_calendar_months"].astype(str))
    ax.set_xlabel("Meses calendario activos entre estudiantes con exactamente 3 visitas")
    ax.set_ylabel("Desempeño Z (solo calificaciones numéricas), media e IC95%")
    _save(fig, out / "10_exact3_regularity_vs_performance.png")
