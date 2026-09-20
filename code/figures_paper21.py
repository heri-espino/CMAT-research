#!/usr/bin/env python3
"""Generate Paper 2.1 publication figures from aggregate analysis tables."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
import pandas as pd

try:
    from cmat_analysis.visualization import set_style
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Paper 2.1 figures require the shared editable library. Run:\n"
        '  python -m pip install -e "./cmat_analysis[dev]"'
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = REPO_ROOT / "results" / "paper21" / "tables"
FIGURES_DIR = REPO_ROOT / "results" / "paper21" / "figures"
GROUPS = ["0", "1", "2", "3", "4", "5", "6+"]
USER_GROUPS = ["1", "2", "3", "4", "5", "6+"]


def _save(fig: plt.Figure, name: str) -> Path:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / name
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def validate() -> None:
    required = [
        "10b_zero_inclusive_descriptives.csv",
        "10d_zero_inclusive_exact_administrative_composition.csv",
        "18_primary_z_heatmap_matrix.csv",
        "19_primary_pass_heatmap_matrix.csv",
    ]
    missing = [f for f in required if not (TABLES_DIR / f).is_file()]
    if missing:
        raise FileNotFoundError("Missing Paper 2.1 figure inputs: " + ", ".join(missing))


def plot_outcomes_by_group() -> Path:
    d = pd.read_csv(TABLES_DIR / "10b_zero_inclusive_descriptives.csv").copy()
    d["group"] = pd.Categorical(d["group"].astype(str), GROUPS, ordered=True)
    d = d.sort_values("group")
    x = np.arange(len(d))

    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    means = d["mean_z"].to_numpy(float)
    lows = d["z_ci95_low"].to_numpy(float)
    highs = d["z_ci95_high"].to_numpy(float)
    ax.errorbar(
        x, means,
        yerr=np.vstack([means - lows, highs - means]),
        fmt="o", capsize=4, linewidth=1.2,
    )
    ax.axhline(0, linestyle="--", linewidth=1)
    ax.set_xticks(x, d["group"].astype(str))
    ax.set_xlabel("CMAT visits during the MU academic period")
    ax.set_ylabel("Mean instructor-period-standardised grade (Z), 95% CI")
    return _save(fig, "fig01_standardised_grade_by_frequency.pdf")


def _heatmap(path: Path, value_scale: float, label: str, filename: str) -> Path:
    d = pd.read_csv(path).copy()
    d["group"] = d["group"].astype(str)
    d = d.set_index("group")
    matrix = d[USER_GROUPS].loc[USER_GROUPS].astype(float).to_numpy() * value_scale
    vmax = float(np.nanmax(np.abs(matrix)))
    if not np.isfinite(vmax) or vmax == 0:
        vmax = 1.0

    fig, ax = plt.subplots(figsize=(6.7, 5.8))
    im = ax.imshow(matrix, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    ax.set_xticks(np.arange(len(USER_GROUPS)), USER_GROUPS)
    ax.set_yticks(np.arange(len(USER_GROUPS)), USER_GROUPS)
    ax.set_xlabel("Comparison group")
    ax.set_ylabel("Reference group")
    for i in range(len(USER_GROUPS)):
        for j in range(len(USER_GROUPS)):
            value = matrix[i, j]
            if np.isfinite(value):
                ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=8)
    cbar = fig.colorbar(im, ax=ax, shrink=0.84)
    cbar.set_label(label)
    return _save(fig, filename)


def plot_z_heatmap() -> Path:
    return _heatmap(
        TABLES_DIR / "18_primary_z_heatmap_matrix.csv",
        1.0,
        "Adjusted difference in standardised grade (row minus column)",
        "fig02_pairwise_z_heatmap.pdf",
    )


def plot_pass_heatmap() -> Path:
    return _heatmap(
        TABLES_DIR / "19_primary_pass_heatmap_matrix.csv",
        100.0,
        "Adjusted difference in pass probability, percentage points (row minus column)",
        "fig03_pairwise_pass_heatmap.pdf",
    )


def plot_outcome_composition() -> Path:
    d = pd.read_csv(TABLES_DIR / "10d_zero_inclusive_exact_administrative_composition.csv").copy()
    d["group"] = pd.Categorical(d["group"].astype(str), GROUPS, ordered=True)
    pivot = (
        d.pivot(index="group", columns="outcome_state", values="share_within_group")
        .reindex(GROUPS)
        .fillna(0.0)
    )
    states = ["pass", "numeric_grade_below_7.5", "BV", "RT", "BA"]
    labels = ["Pass", "Numeric <7.5", "BV", "RT", "BA"]
    x = np.arange(len(GROUPS))
    bottom = np.zeros(len(GROUPS))

    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    for state, label in zip(states, labels):
        values = pivot.get(state, pd.Series(0.0, index=pivot.index)).to_numpy(float)
        ax.bar(x, values, bottom=bottom, label=label)
        bottom += values
    ax.set_xticks(x, GROUPS)
    ax.set_xlabel("CMAT visits during the MU academic period")
    ax.set_ylabel("Share of students")
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.set_ylim(0, 1)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))
    return _save(fig, "fig04_outcome_composition.pdf")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    validate()
    set_style()
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    for path in [
        plot_outcomes_by_group(),
        plot_z_heatmap(),
        plot_pass_heatmap(),
        plot_outcome_composition(),
    ]:
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
