#!/usr/bin/env python3
"""Generate Paper 2.1 publication figures from aggregate analysis outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from cmat_analysis.visualization import plot_stacked_ridgeline, set_style
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
OUTCOME_STATES = ["pass", "numeric_nonpass", "BV", "RT", "BA"]


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
        "10g_zero_inclusive_stacked_ridgeline_density.csv",
        "18_primary_z_heatmap_matrix.csv",
        "19_primary_pass_heatmap_matrix.csv",
    ]
    missing = [name for name in required if not (TABLES_DIR / name).is_file()]
    if missing:
        raise FileNotFoundError(
            "Missing Paper 2.1 figure inputs: " + ", ".join(missing)
        )



def _central_density_limits(
    density: pd.DataFrame,
    *,
    lower: float = 0.005,
    upper: float = 0.995,
) -> tuple[float, float]:
    limits = []
    for group in GROUPS:
        subset = (
            density.loc[density["group"].astype(str).eq(group)]
            .drop_duplicates("x")
            .sort_values("x")
        )
        x = subset["x"].to_numpy(float)
        y = subset["density_total"].to_numpy(float)
        increments = (y[:-1] + y[1:]) * 0.5 * np.diff(x)
        cumulative = np.concatenate([[0.0], np.cumsum(increments)])
        if cumulative[-1] <= 0:
            continue
        cumulative /= cumulative[-1]
        limits.append(
            (
                float(np.interp(lower, cumulative, x)),
                float(np.interp(upper, cumulative, x)),
            )
        )
    left = min(value[0] for value in limits)
    right = max(value[1] for value in limits)
    margin = 0.04 * (right - left)
    return left - margin, right + margin

def plot_distribution_and_composition() -> Path:
    density = pd.read_csv(
        TABLES_DIR / "10g_zero_inclusive_stacked_ridgeline_density.csv"
    )
    summary = pd.read_csv(TABLES_DIR / "10b_zero_inclusive_descriptives.csv")
    summary = summary.rename(
        columns={
            "mean_z": "outcome_mean",
            "z_ci95_low": "outcome_ci95_low",
            "z_ci95_high": "outcome_ci95_high",
        }
    )

    fig, ax = plt.subplots(figsize=(8.4, 6.0))
    plot_stacked_ridgeline(
        density,
        group_order=GROUPS,
        component_order=OUTCOME_STATES,
        summary=summary,
        component_labels={
            "pass": "Pass",
            "numeric_nonpass": "Numeric <7.5",
            "BV": "BV",
            "RT": "RT",
            "BA": "BA",
        },
        ridge_height=0.82,
        ax=ax,
    )
    ax.axvline(0, linestyle="--", linewidth=0.9, alpha=0.65)
    ax.set_xlim(*_central_density_limits(density))
    ax.set_xlabel("Instructor-period-standardised MU grade (Z)")
    ax.set_ylabel("CMAT visits during the MU academic period")
    ax.grid(axis="y", visible=False)
    ax.legend(
        frameon=False,
        ncol=5,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
    )
    return _save(fig, "fig01_distribution_composition_ridgeline.pdf")


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    validate()
    set_style()
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    for path in [
        plot_distribution_and_composition(),
        plot_z_heatmap(),
        plot_pass_heatmap(),
    ]:
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
