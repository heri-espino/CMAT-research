from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from visitas_analysis.visualization.style import mpl_apply


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_ppa_persistence_by_mu_group(summary: pd.DataFrame, figures: Path) -> None:
    """Plot later Calculus-use probability by 0/1-2/3/4+ MU visits."""
    mpl_apply()
    plt.rcParams["axes.unicode_minus"] = False
    d = summary.copy()
    x = np.arange(len(d))
    p = d["p_calc_any_visit"].to_numpy(float)
    lo = d["ci95_low_wilson"].to_numpy(float)
    hi = d["ci95_high_wilson"].to_numpy(float)
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    ax.errorbar(x, p, yerr=[p - lo, hi - p], marker="o", capsize=4, linewidth=1.5)
    ax.set_xticks(x, d["mu_visit_group"].astype(str))
    ax.set_xlabel("Visitas al CMAT durante Matemáticas Universitarias")
    ax.set_ylabel("P(al menos una visita durante Cálculo I)")
    ax.set_ylim(0, min(1.0, float(np.nanmax(hi)) + 0.12))
    ax.set_title("Persistencia de uso después del contexto PPA1")
    for i, r in d.iterrows():
        ax.annotate(f"n={int(r['n'])}", (i, r["p_calc_any_visit"]), xytext=(0, 9),
                    textcoords="offset points", ha="center", fontsize=8)
    _save(fig, figures / "15_ppa_persistence_by_mu_group.png")


def plot_ppa_academic_trajectory_profiles(profiles: pd.DataFrame, figures: Path) -> None:
    """Plot mean Delta-Z for the eight observable MU-group x Calculus-use profiles."""
    mpl_apply()
    plt.rcParams["axes.unicode_minus"] = False
    d = profiles.loc[profiles["n"] > 0].copy()
    labels = d["profile"].str.replace("Calc use", "Calc sí", regex=False).str.replace("Calc no use", "Calc no", regex=False)
    y = np.arange(len(d))
    fig_h = max(5.0, 0.5 * len(d) + 1.5)
    fig, ax = plt.subplots(figsize=(9.0, fig_h))
    ax.plot(d["mean_delta_z"], y, "o")
    ax.axvline(0, linestyle="--", linewidth=1)
    ax.set_yticks(y, [f"{lab} (n={n})" for lab, n in zip(labels, d["n"])])
    ax.set_xlabel(r"Cambio medio en posición relativa: $Z_{Calc}-Z_{MU}$")
    ax.set_ylabel("Perfil observable")
    ax.set_title("Trayectoria académica relativa por patrón de uso")
    _save(fig, figures / "16_ppa_academic_trajectory_profiles.png")
