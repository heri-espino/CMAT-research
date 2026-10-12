#!/usr/bin/env python3
"""Paper 2.1 upper-triangular Wald/Holm figures from observed aggregate tables.

The group bands 0 | 1–3 | 4–6 | 7+ are institutional/descriptive hypotheses,
not partitions established by the multiple-comparison procedure.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm
import numpy as np
import pandas as pd

from cmat_analysis.visualization import set_style


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "paper21" / "tables"
FIGURES = ROOT / "results" / "paper21" / "figures"
GROUPS = ["0", "1", "2", "3", "4", "5", "6", "7+"]
# These are boundaries after 0, after 3 (PPA1), and after 6 visits.
BAND_EDGES = (0.5, 3.5, 6.5)
BANDS = (("0", 0.0), ("1–3 (PPA1)", 2.0), ("4–6", 5.0), ("7+", 7.0))


def validate() -> None:
    required = (
        "26b_zero_inclusive_7plus_z_effect_matrix.csv",
        "26e_zero_inclusive_7plus_z_p_raw_matrix.csv",
        "26f_zero_inclusive_7plus_z_p_holm_matrix.csv",
        "26g_zero_inclusive_7plus_pass_p_raw_matrix.csv",
        "26h_zero_inclusive_7plus_pass_p_holm_matrix.csv",
        "26k_zero_inclusive_7plus_pairwise_pass_lpm.csv",
    )
    absent = [x for x in required if not (TABLES / x).is_file()]
    if absent:
        raise FileNotFoundError("Missing adjusted Wald/Holm inputs: " + ", ".join(absent))


def matrix(name: str) -> np.ndarray:
    frame = pd.read_csv(TABLES / name).copy()
    frame["group"] = frame["group"].astype(str)
    return (
        frame.set_index("group")[GROUPS].loc[GROUPS]
        .astype(float).to_numpy(copy=True)
    )


def higher_minus_lower(matrix_row_minus_col: np.ndarray) -> np.ndarray:
    """Return only i<j: higher-frequency column minus lower-frequency row."""
    original = np.asarray(matrix_row_minus_col, dtype=float)
    return np.where(np.triu(np.ones(original.shape, dtype=bool), k=1), -original, np.nan)


def upper_pvalues(square: np.ndarray) -> np.ndarray:
    """Raw/Holm two-sided p-values are symmetric; keep only the upper half."""
    return np.where(np.triu(np.ones(square.shape, dtype=bool), k=1), square, np.nan)


def setup_axis(ax: plt.Axes) -> None:
    ax.set_xticks(np.arange(len(GROUPS)), GROUPS)
    ax.set_yticks(np.arange(len(GROUPS)), GROUPS)
    ax.xaxis.tick_bottom()
    ax.set_xlabel("Higher visit frequency (column)", fontsize=9)
    ax.set_ylabel("Lower visit frequency (row)", fontsize=9)
    ax.set_xlim(-0.5, len(GROUPS) - 0.5)
    ax.set_ylim(len(GROUPS) - 0.5, -0.5)
    ax.grid(False)
    ax.tick_params(axis="both", length=0)
    for border in ax.spines.values():
        border.set_visible(False)
    for edge in BAND_EDGES:
        ax.axvline(edge, color="0.45", linewidth=0.8, linestyle="--", alpha=0.6)
        ax.axhline(edge, color="0.45", linewidth=0.8, linestyle="--", alpha=0.6)
    for label, xpos in BANDS:
        ax.text(xpos, 1.035, label, transform=ax.get_xaxis_transform(),
                ha="center", va="bottom", fontsize=7.5, color="0.25",
                clip_on=False)


def save(fig: plt.Figure, name: str) -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / name
    fig.savefig(path, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    return path


def pass_probability_matrix() -> np.ndarray:
    pairs = pd.read_csv(TABLES / "26k_zero_inclusive_7plus_pairwise_pass_lpm.csv")
    positions = {name: i for i, name in enumerate(GROUPS)}
    values = np.zeros((len(GROUPS), len(GROUPS)), dtype=float)
    for pair in pairs.itertuples(index=False):
        i, j = positions[str(pair.group1)], positions[str(pair.group2)]
        delta_pp = 100.0 * float(pair.adjusted_difference_group1_minus_group2)
        values[i, j], values[j, i] = delta_pp, -delta_pp
    return values


def draw_effects() -> Path:
    z = higher_minus_lower(matrix("26b_zero_inclusive_7plus_z_effect_matrix.csv"))
    passing = higher_minus_lower(pass_probability_matrix())
    fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.8))
    for ax, values, title, units, digits in (
        (axes[0], z, "Final grade (adjusted Z)", "Standard deviations", 2),
        (axes[1], passing, "Pass probability (LPM)", "Percentage points", 1),
    ):
        bound = max(float(np.nanmax(np.abs(values))), 1e-6)
        cmap = plt.get_cmap("RdBu_r").copy()
        cmap.set_bad("white")
        image = ax.imshow(np.ma.masked_invalid(values), cmap=cmap,
                          vmin=-bound, vmax=bound, interpolation="nearest")
        setup_axis(ax)
        ax.set_title(title, fontsize=10, pad=27)
        for i in range(len(GROUPS)):
            for j in range(i + 1, len(GROUPS)):
                value = values[i, j]
                if np.isfinite(value):
                    ax.text(j, i, f"{value:+.{digits}f}", ha="center",
                            va="center", fontsize=7.5,
                            color="white" if abs(value) / bound > .72 else "0.10")
        cb = fig.colorbar(image, ax=ax, shrink=.77, pad=.025)
        cb.set_label(units, fontsize=9)
    fig.suptitle("CMAT visits: adjusted contrasts (later group minus earlier group)",
                 fontsize=11, y=1.035)
    fig.text(.5, -.005,
             "PPA1 is completed on visit 3; separators after 0, 3 and 6 are descriptive, not Holm-derived.",
             ha="center", fontsize=8, color="0.3")
    fig.subplots_adjust(wspace=.27)
    return save(fig, "fig03_04_pairwise_effect_dashboard.pdf")


def fmt_p(p: float) -> str:
    if p < .001:
        return "<.001"
    return f"{p:.3f}" if p < .01 else f"{p:.2f}"


def draw_pvalues(outcome: str, raw_file: str, holm_file: str, filename: str) -> Path:
    raw = upper_pvalues(matrix(raw_file))
    adjusted = upper_pvalues(matrix(holm_file))
    cmap = plt.get_cmap("viridis_r").copy()
    cmap.set_bad("white")
    norm = PowerNorm(gamma=.35, vmin=0, vmax=1)
    fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.8))
    for ax, values, title in zip(
        axes, (raw, adjusted), ("Unadjusted Wald p-value", "Holm-adjusted p-value")
    ):
        image = ax.imshow(np.ma.masked_invalid(values), cmap=cmap, norm=norm,
                          interpolation="nearest")
        setup_axis(ax)
        ax.set_title(title, fontsize=10, pad=27)
        for i in range(len(GROUPS)):
            for j in range(i + 1, len(GROUPS)):
                p = values[i, j]
                if np.isfinite(p):
                    ax.text(j, i, fmt_p(p), ha="center", va="center",
                            fontsize=7.5, weight="bold" if p < .05 else "normal",
                            color="0.10" if p < .3 else "white")
    cb = fig.colorbar(image, ax=axes, shrink=.77, pad=.025)
    cb.set_label("Two-sided pairwise p-value", fontsize=9)
    fig.suptitle(outcome + ": upper-triangle pairwise Wald tests", fontsize=11, y=1.035)
    fig.text(.5, -.005,
             "PPA1 completes at visit 3. Holm applies to all 28 pairs per outcome, not to proposed visit bands.",
             ha="center", fontsize=8, color="0.3")
    fig.subplots_adjust(wspace=.25)
    return save(fig, filename)


def main() -> int:
    argparse.ArgumentParser(
        description="Regenerate Paper 2.1 upper-triangular Wald/Holm heatmaps."
    ).parse_args()
    validate()
    set_style()
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    outputs = [
        draw_effects(),
        draw_pvalues(
            "Adjusted standardised grade (Z)",
            "26e_zero_inclusive_7plus_z_p_raw_matrix.csv",
            "26f_zero_inclusive_7plus_z_p_holm_matrix.csv",
            "fig05_pairwise_z_pvalue_dashboard.pdf",
        ),
        draw_pvalues(
            "Adjusted PASS probability (LPM)",
            "26g_zero_inclusive_7plus_pass_p_raw_matrix.csv",
            "26h_zero_inclusive_7plus_pass_p_holm_matrix.csv",
            "fig06_pairwise_pass_pvalue_dashboard.pdf",
        ),
    ]
    for path in outputs:
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
