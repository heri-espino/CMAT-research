"""Reusable figures for methodology and visit-dose diagnostics.

Plot functions consume already-computed analytical tables and do not define
cohorts, exposure rules, or statistical estimands.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_pairwise_exact_group_means(summary: pd.DataFrame, out: Path, filename: str, title: str) -> None:
    d = summary.copy()
    if d.empty:
        return
    order = ["0", "1", "2", "3", "4+"]
    d["group"] = pd.Categorical(d["group"], categories=order, ordered=True)
    d = d.sort_values("group")
    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    x = np.arange(len(d))
    yerr = np.vstack([d["mean_z"] - d["ci95_low"], d["ci95_high"] - d["mean_z"]])
    ax.errorbar(x, d["mean_z"], yerr=yerr, fmt="o", capsize=4)
    ax.axhline(0, linewidth=1, linestyle="--")
    ax.set_xticks(x, d["group"].astype(str))
    ax.set_xlabel("Número de visitas al CMAT durante el periodo de MU")
    ax.set_ylabel("Media de Z relativo al salón (IC 95%)")
    ax.set_title(title)
    _save(fig, out / filename)


def plot_career_mean_z(summary: pd.DataFrame, population: str, out: Path, filename: str) -> None:
    d = summary.loc[(summary["population"] == population) & summary["included_n_ge_min"]].copy()
    if d.empty:
        return
    d = d.sort_values("mean_z")
    fig, ax = plt.subplots(figsize=(9.4, max(5.2, 0.23 * len(d) + 1.8)))
    ax.barh(d["CLAVECARRERA"].astype(str), d["mean_z"])
    ax.axvline(0, linewidth=1, linestyle="--")
    ax.set_xlabel("Media de Z relativo al salón")
    ax.set_ylabel("Licenciatura oficial")
    ax.set_title(f"Desempeño relativo promedio por licenciatura: {population}")
    _save(fig, out / filename)


def plot_career_use_vs_z(summary: pd.DataFrame, population: str, out: Path, filename: str) -> None:
    d = summary.loc[(summary["population"] == population) & summary["included_n_ge_min"]].copy()
    if d.empty:
        return
    fig, ax = plt.subplots(figsize=(7.4, 5.6))
    sizes = 18 + 90 * (d["n"] / d["n"].max())
    ax.scatter(d["any_visit_rate"], d["mean_z"], s=sizes, alpha=0.75)
    for _, r in d.iterrows():
        ax.annotate(str(r["CLAVECARRERA"]), (r["any_visit_rate"], r["mean_z"]), xytext=(3, 3), textcoords="offset points", fontsize=7)
    ax.axhline(0, linewidth=1, linestyle="--")
    ax.set_xlabel("Proporción con al menos una visita al CMAT")
    ax.set_ylabel("Media de Z relativo al salón")
    ax.set_title(f"Uso del CMAT y desempeño agregado por licenciatura: {population}")
    _save(fig, out / filename)


def plot_periodicity_acf_by_population(acf: pd.DataFrame, out: Path, filename: str = "09_monthly_periodicity_acf_by_population.png") -> None:
    d = acf.loc[acf["SESSION"] == "POOLED"].dropna(subset=["autocorrelation"]).copy()
    if d.empty:
        return
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    for population, g in d.groupby("population", observed=True):
        g = g.sort_values("lag_days")
        ax.plot(g["lag_days"], g["autocorrelation"], marker="o", markersize=3, linewidth=1.1, label=population)
        best = g.loc[g["autocorrelation"].idxmax()]
        ax.axvline(float(best["lag_days"]), linestyle=":", linewidth=0.9)
    ax.axvspan(24, 38, alpha=0.10, label="Ventana 24–38 días")
    ax.set_xlabel("Rezago (días)")
    ax.set_ylabel("Autocorrelación de carga diaria ajustada")
    ax.set_title("Periodicidad aproximada por población")
    ax.legend(fontsize=8)
    _save(fig, out / filename)


def plot_peak_spacing_by_population(intervals: pd.DataFrame, out: Path, filename: str = "08_peak_spacing_by_population.png") -> None:
    if intervals.empty:
        return
    populations = list(intervals["population"].dropna().unique())
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    data = [intervals.loc[intervals["population"] == p, "gap_days"].dropna().to_numpy(float) for p in populations]
    ax.boxplot(data, tick_labels=populations, showmeans=True)
    ax.axhspan(24, 38, alpha=0.10, label="Ventana 24–38 días")
    ax.set_ylabel("Días entre picos consecutivos")
    ax.set_title("Separación entre picos detectados por población")
    ax.tick_params(axis="x", rotation=10)
    ax.legend(fontsize=8)
    _save(fig, out / filename)


def plot_exact_visit_count_curve(summary: pd.DataFrame, out: Path, filename: str = "13_exact_visit_counts_0_to_12.png") -> None:
    d = summary.copy().dropna(subset=["mean_z"])
    if d.empty:
        return
    d = d.sort_values("visits_exact")
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    yerr_low = (d["mean_z"] - d["ci95_low"]).clip(lower=0)
    yerr_high = (d["ci95_high"] - d["mean_z"]).clip(lower=0)
    ax.errorbar(d["visits_exact"], d["mean_z"], yerr=np.vstack([yerr_low, yerr_high]), marker="o", capsize=3, linewidth=1.1)
    for _, r in d.iterrows():
        ax.annotate(f"n={int(r['n'])}", (r["visits_exact"], r["mean_z"]), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=7)
    ax.axhline(0, linewidth=1, linestyle="--")
    ax.set_xticks(range(int(d["visits_exact"].min()), int(d["visits_exact"].max()) + 1))
    ax.set_xlabel("Número exacto de visitas al CMAT durante el periodo de MU")
    ax.set_ylabel("Media de Z relativo al salón (IC 95%)")
    ax.set_title("Desempeño relativo por número exacto de visitas (0–12)")
    _save(fig, out / filename)
