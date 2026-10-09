#!/usr/bin/env python3
"""Paper 2.1 Holm-only pairwise figures from aggregate adjusted tables."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm
import numpy as np
import pandas as pd

from cmat_analysis.visualization import set_style

REPO_ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = REPO_ROOT / "results" / "paper21" / "tables"
FIGURES_DIR = REPO_ROOT / "results" / "paper21" / "figures"
ZERO_DISPLAY_GROUPS = ["0", "1", "2", "3", "4", "5", "6", "7+"]

def _save(fig: plt.Figure, name: str) -> Path:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / name
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path

def validate() -> None:
    """Require only adjusted Wald/Holm contrast matrices."""
    required = [
        "26b_zero_inclusive_7plus_z_effect_matrix.csv",
        "26d_zero_inclusive_7plus_pass_odds_ratio_matrix.csv",
        "26e_zero_inclusive_7plus_z_p_raw_matrix.csv",
        "26f_zero_inclusive_7plus_z_p_holm_matrix.csv",
        "26g_zero_inclusive_7plus_pass_p_raw_matrix.csv",
        "26h_zero_inclusive_7plus_pass_p_holm_matrix.csv",
    ]
    missing = [name for name in required if not (TABLES_DIR / name).is_file()]
    if missing:
        raise FileNotFoundError("Missing Paper 2.1 Holm matrices: " + ", ".join(missing))

def _matrix_from_csv(path: Path, group_order: list[str]) -> np.ndarray:
    frame = pd.read_csv(path).copy()
    frame["group"] = frame["group"].astype(str)
    return (
        frame.set_index("group")[group_order]
        .loc[group_order]
        .astype(float)
        .to_numpy(copy=True)
    )

def plot_pairwise_effect_dashboard() -> Path:
    """Main pairwise dashboard for the full 0,1,...,6,7+ paper grouping."""
    groups = ZERO_DISPLAY_GROUPS
    z = _matrix_from_csv(
        TABLES_DIR / "26b_zero_inclusive_7plus_z_effect_matrix.csv", groups
    )
    pass_pairs = pd.read_csv(TABLES_DIR / "26k_zero_inclusive_7plus_pairwise_pass_lpm.csv")
    passdiff = np.zeros((len(groups), len(groups)), dtype=float)
    positions = {name: i for i, name in enumerate(groups)}
    for row in pass_pairs.itertuples(index=False):
        left_group, right_group = str(row.group1), str(row.group2)
        i, j = positions[left_group], positions[right_group]
        delta = float(row.adjusted_difference_group1_minus_group2)
        passdiff[i, j], passdiff[j, i] = delta, -delta
    np.fill_diagonal(z, np.nan)
    np.fill_diagonal(passdiff, np.nan)

    zmax = float(np.nanmax(np.abs(z)))
    pmax = float(np.nanmax(np.abs(passdiff)))
    if not np.isfinite(zmax) or zmax <= 0:
        zmax = 1.0
    if not np.isfinite(pmax) or pmax <= 0:
        pmax = 1.0

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.5), sharex=True, sharey=True)
    threshold = groups.index("2") + 0.5

    left = axes[0].imshow(z, cmap="RdBu_r", vmin=-zmax, vmax=zmax)
    right = axes[1].imshow(passdiff, cmap="RdBu_r", vmin=-pmax, vmax=pmax)

    for ax, title in zip(
        axes,
        [
            "Adjusted standardised-grade difference",
            "Adjusted pass-probability difference (pp)",
        ],
    ):
        ax.set_xticks(np.arange(len(groups)), groups)
        ax.set_yticks(np.arange(len(groups)), groups)
        ax.set_xlabel("Comparison group")
        ax.set_title(title, fontsize=10)
        ax.grid(False)
        ax.axvline(threshold, linestyle="--", linewidth=1.0, color="0.25", alpha=0.75)
        ax.axhline(threshold, linestyle="--", linewidth=1.0, color="0.25", alpha=0.75)

    axes[0].set_ylabel("Reference group")

    for i in range(len(groups)):
        for j in range(len(groups)):
            if np.isfinite(z[i, j]):
                axes[0].text(
                    j, i, f"{z[i, j]:+.2f}",
                    ha="center", va="center", fontsize=7.2,
                )
            if np.isfinite(passdiff[i, j]):
                value = passdiff[i, j]
                axes[1].text(
                    j, i, f"{value*100:+.1f}",
                    ha="center", va="center", fontsize=7.2,
                )

    cbar_left = fig.colorbar(left, ax=axes[0], shrink=0.82, pad=0.03)
    cbar_left.set_label("Row minus column, SD")
    cbar_right = fig.colorbar(right, ax=axes[1], shrink=0.82, pad=0.03)
    cbar_right.set_label("Row minus column, pass probability")

    fig.suptitle(
        "Adjusted pairwise outcomes by CMAT attendance frequency: 0, exact 1–6, and 7+ visits",
        fontsize=11,
        y=0.995,
    )
    fig.text(
        0.5, 0.015,
        "Dashed lines mark the institutional three-visit PPA threshold between 2 and 3 visits.",
        ha="center", va="bottom", fontsize=7.2, color="0.30",
    )
    fig.subplots_adjust(top=0.88, bottom=0.12, wspace=0.16)
    return _save(fig, "fig03_04_pairwise_effect_dashboard.pdf")

def _format_pvalue(value: float) -> str:
    if not np.isfinite(value):
        return ""
    if value < 0.001:
        return "<.001"
    if value < 0.01:
        return f"{value:.3f}"
    return f"{value:.2f}"

def _pvalue_dashboard(
    *,
    raw_path: Path,
    holm_path: Path,
    filename: str,
    outcome_title: str,
    group_order: list[str],
) -> Path:
    """Plot raw and Holm-adjusted pairwise p-values side by side."""
    matrices = []
    for path in [raw_path, holm_path]:
        matrix = _matrix_from_csv(path, group_order)
        np.fill_diagonal(matrix, np.nan)
        matrices.append(matrix)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.4), sharex=True, sharey=True)
    norm = PowerNorm(gamma=0.35, vmin=0.0, vmax=1.0)
    threshold = group_order.index("2") + 0.5
    image = None

    for ax, matrix, panel_title in zip(
        axes, matrices, ["Raw pairwise p-values", "Holm-adjusted p-values"]
    ):
        image = ax.imshow(matrix, cmap="viridis_r", norm=norm)
        ax.set_xticks(np.arange(len(group_order)), group_order)
        ax.set_yticks(np.arange(len(group_order)), group_order)
        ax.set_xlabel("Comparison group")
        ax.set_title(panel_title, fontsize=10)
        ax.grid(False)
        ax.axvline(threshold, linestyle="--", linewidth=1.0, color="white", alpha=0.9)
        ax.axhline(threshold, linestyle="--", linewidth=1.0, color="white", alpha=0.9)
        for i in range(len(group_order)):
            for j in range(len(group_order)):
                value = matrix[i, j]
                if not np.isfinite(value):
                    continue
                ax.text(
                    j, i, _format_pvalue(value), ha="center", va="center",
                    fontsize=7.0, fontweight="bold" if value < 0.05 else "normal",
                    color="black" if value < 0.35 else "white",
                )

    axes[0].set_ylabel("Reference group")
    fig.suptitle(
        f"{outcome_title}: pairwise comparisons for 0, exact 1–6, and 7+ visits",
        fontsize=11, y=0.99,
    )
    fig.text(
        0.5, 0.015,
        "Dashed separator marks the institutional three-visit PPA threshold. "
        "Raw p-values locate local contrasts; Holm-adjusted values control family-wise multiplicity.",
        ha="center", va="bottom", fontsize=7.2, color="0.30",
    )
    if image is not None:
        cbar = fig.colorbar(image, ax=axes, shrink=0.82, pad=0.03)
        cbar.set_label("Pairwise p-value")
    fig.subplots_adjust(top=0.86, bottom=0.14, wspace=0.12)
    return _save(fig, filename)

def plot_z_pvalue_dashboard() -> Path:
    return _pvalue_dashboard(
        raw_path=TABLES_DIR / "26e_zero_inclusive_7plus_z_p_raw_matrix.csv",
        holm_path=TABLES_DIR / "26f_zero_inclusive_7plus_z_p_holm_matrix.csv",
        filename="fig05_pairwise_z_pvalue_dashboard.pdf",
        outcome_title="Adjusted standardised MU grade",
        group_order=ZERO_DISPLAY_GROUPS,
    )

def plot_pass_pvalue_dashboard() -> Path:
    return _pvalue_dashboard(
        raw_path=TABLES_DIR / "26g_zero_inclusive_7plus_pass_p_raw_matrix.csv",
        holm_path=TABLES_DIR / "26h_zero_inclusive_7plus_pass_p_holm_matrix.csv",
        filename="fig06_pairwise_pass_pvalue_dashboard.pdf",
        outcome_title="Adjusted pass probability (linear-probability inference)",
        group_order=ZERO_DISPLAY_GROUPS,
    )

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Paper 2.1 Wald/Holm pairwise figures only.")
    parser.parse_args()
    validate()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    set_style()
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    for path in [
        plot_pairwise_effect_dashboard(),
        plot_z_pvalue_dashboard(),
        plot_pass_pvalue_dashboard(),
    ]:
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

