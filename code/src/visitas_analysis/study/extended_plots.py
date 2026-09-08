from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from visitas_analysis.visualization.style import mpl_apply


def _finish(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_exact_visit_performance_index(index_df: pd.DataFrame, figures: Path) -> None:
    mpl_apply()
    plt.rcParams["axes.unicode_minus"] = False
    d = index_df.copy()
    d = d.loc[d["n"].fillna(0) > 0]
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    y = d["career_relative_index_student_weighted"].astype(float)
    lo = d["career_relative_ci95_low"].astype(float)
    hi = d["career_relative_ci95_high"].astype(float)
    ax.errorbar(d["visits"], y, yerr=[y-lo, hi-y], marker="o", capsize=3, linewidth=1.5)
    ax.axhline(0, linewidth=1, linestyle="--")
    for _, r in d.iterrows():
        ax.annotate(f"n={int(r['n'])}", (r["visits"], r["career_relative_index_student_weighted"]),
                    textcoords="offset points", xytext=(0, 8), ha="center", fontsize=7)
    ax.set_xlabel("Número exacto de visitas al CMAT durante el semestre")
    ax.set_ylabel("Índice de rendimiento relativo a la licenciatura (DE)")
    ax.set_title("Rendimiento relativo por número exacto de asesorías (1–12)")
    ax.set_xticks(range(1, 13))
    _finish(fig, figures / "11_exact_visit_career_relative_index.png")


def plot_career_performance(career_summary: pd.DataFrame, figures: Path, min_n: int = 30) -> None:
    mpl_apply()
    plt.rcParams["axes.unicode_minus"] = False
    d = career_summary.loc[career_summary["n"] >= min_n].copy().sort_values("mean_z")
    fig_h = max(5.5, 0.26 * len(d) + 1.5)
    fig, ax = plt.subplots(figsize=(9.4, fig_h))
    x = d["mean_z"].to_numpy(float)
    lo = d["ci95_low"].to_numpy(float)
    hi = d["ci95_high"].to_numpy(float)
    y = np.arange(len(d))
    ax.errorbar(x, y, xerr=[x-lo, hi-x], fmt="o", capsize=2.5)
    ax.axvline(0, linewidth=1, linestyle="--")
    ax.set_yticks(y)
    ax.set_yticklabels([f"{c} (n={n})" for c, n in zip(d["CLAVECARRERA"], d["n"])])
    ax.set_xlabel("Media de Z respecto al salón (DE)")
    ax.set_ylabel("Licenciatura")
    ax.set_title("Desempeño relativo al salón por licenciatura")
    _finish(fig, figures / "12_career_classroom_z_means.png")


def plot_longitudinal_any_visit_transition(combos: pd.DataFrame, stats_df: pd.DataFrame, figures: Path) -> None:
    mpl_apply()
    plt.rcParams["axes.unicode_minus"] = False
    # Conditional probabilities are more interpretable than a mosaic in a report.
    n11 = int(combos.loc[(combos.mu_any_visit == 1) & (combos.calc_any_visit == 1), "n"].iloc[0])
    n10 = int(combos.loc[(combos.mu_any_visit == 1) & (combos.calc_any_visit == 0), "n"].iloc[0])
    n01 = int(combos.loc[(combos.mu_any_visit == 0) & (combos.calc_any_visit == 1), "n"].iloc[0])
    n00 = int(combos.loc[(combos.mu_any_visit == 0) & (combos.calc_any_visit == 0), "n"].iloc[0])
    stat = stats_df.iloc[0]
    p0 = float(stat["p_calc_visit_given_no_mu_visit"])
    p1 = float(stat["p_calc_visit_given_mu_visit"])
    ns = [n00+n01, n10+n11]
    ps = [p0, p1]
    lows = [
        float(stat["p_calc_visit_given_no_mu_visit_ci95_low"]),
        float(stat["p_calc_visit_given_mu_visit_ci95_low"]),
    ]
    highs = [
        float(stat["p_calc_visit_given_no_mu_visit_ci95_high"]),
        float(stat["p_calc_visit_given_mu_visit_ci95_high"]),
    ]
    yerr = [[p-lo for p, lo in zip(ps, lows)], [hi-p for p, hi in zip(ps, highs)]]
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    ax.bar([0, 1], ps, yerr=yerr, capsize=4)
    ax.set_xticks([0, 1], ["No usó CMAT en MU", "Sí usó CMAT en MU"])
    ax.set_ylabel("P(al menos una visita en Cálculo I)")
    ax.set_ylim(0, min(1, max(ps) + 0.15))
    rr = float(stat["risk_ratio"])
    ax.set_title(f"Persistencia individual de uso: MU a Cálculo I (RR={rr:.2f})")
    for i,(p,n) in enumerate(zip(ps,ns)):
        ax.text(i, p+0.025, f"{100*p:.1f}%\nn={n}", ha="center", va="bottom", fontsize=9)
    _finish(fig, figures / "13_any_visit_mu_to_calculus_transition.png")


def plot_career_usage_rates(career_summary: pd.DataFrame, figures: Path, min_n: int = 30) -> None:
    mpl_apply()
    plt.rcParams["axes.unicode_minus"] = False
    d = career_summary.loc[career_summary["n"] >= min_n].copy().sort_values("any_visit_rate")
    fig_h = max(5.5, 0.26 * len(d) + 1.5)
    fig, ax = plt.subplots(figsize=(9.4, fig_h))
    y = np.arange(len(d))
    ax.plot(d["any_visit_rate"], y, "o")
    ax.set_yticks(y)
    ax.set_yticklabels([f"{c} (n={n})" for c,n in zip(d["CLAVECARRERA"], d["n"])])
    ax.set_xlabel("Proporción con al menos una visita al CMAT")
    ax.set_ylabel("Licenciatura")
    ax.set_title("Uso del CMAT por licenciatura")
    ax.set_xlim(left=0)
    _finish(fig, figures / "14_career_any_visit_rates.png")
