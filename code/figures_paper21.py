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
    # Reserve a separate strip for the common colour bar; allowing
    # figure.colorbar(ax=axes) can overlay the second upper triangle.
    fig.subplots_adjust(wspace=.22, right=.88)
    colorbar_axis = fig.add_axes([.91, .19, .017, .60])
    cb = fig.colorbar(image, cax=colorbar_axis)
    cb.set_label("Two-sided pairwise p-value", fontsize=9)
    fig.suptitle(outcome + ": upper-triangle pairwise Wald tests", fontsize=11, y=1.035)
    fig.text(.5, -.005,
             "PPA1 completes at visit 3. Holm applies to all 28 pairs per outcome, not to proposed visit bands.",
             ha="center", fontsize=8, color="0.3")
    return save(fig, filename)



def plot_cohort_outcome_attendance_overview() -> Path:
    """Three aligned panels: PASS rate, Z histogram overlay, and visit counts.

    Only pre-aggregated CSV tables are used; no student-level records are read.
    Histograms display the pre-exported [-2, 2] Z window only.
    """
    from matplotlib.patches import Patch
    from matplotlib.ticker import PercentFormatter

    summaries = pd.read_csv(
        TABLES / "10n_zero_inclusive_7plus_descriptives.csv"
    )
    summaries["group"] = summaries["group"].astype(str)
    summaries = summaries.set_index("group").reindex(GROUPS)
    if summaries[["n", "pass_rate"]].isna().any().any():
        raise ValueError("Missing frequency groups in cohort overview table")

    histogram = pd.read_csv(
        TABLES / "10s_zero_inclusive_7plus_imputed_z_histogram.csv"
    )
    histogram["group"] = histogram["group"].astype(str)
    required = {"pass", "numeric_nonpass", "BV", "RT", "BA"}
    if not required.issubset(set(histogram["component"].unique())):
        raise ValueError("Imputed Z histogram lacks PASS/non-PASS components")

    palette = {"pass": "C0", "nonpass": "C1"}
    fig, (ax_rates, ax_z, ax_freq) = plt.subplots(
        1, 3, figsize=(14.0, 6.0), sharey=True,
        gridspec_kw={"width_ratios": [2.05, 5.1, 1.95], "wspace": 0.13},
    )
    xpos = np.arange(len(GROUPS), dtype=float)
    sample_size = summaries["n"].to_numpy(dtype=int)
    pass_pct = 100 * summaries["pass_rate"].to_numpy(dtype=float)
    nonpass_pct = 100 - pass_pct
    if int(sample_size.sum()) != 6627:
        raise ValueError("Unexpected cohort size in aggregate overview")
    if not np.isfinite(pass_pct).all() or ((pass_pct < 0) | (pass_pct > 100)).any():
        raise ValueError("PASS fractions are not valid probabilities")

    # Left: exact observed PASS and non-PASS shares, all percentages use
    # the full attendance-frequency group's denominator.
    ax_rates.barh(xpos, pass_pct, height=.58,
                  color=palette["pass"], alpha=.80, edgecolor="white", linewidth=.25)
    ax_rates.barh(xpos, nonpass_pct, left=pass_pct, height=.58,
                  color=palette["nonpass"], alpha=.80, edgecolor="white", linewidth=.25)
    for y, p, q in zip(xpos, pass_pct, nonpass_pct):
        ax_rates.text(p / 2, y, f"{p:.1f}%", ha="center",
                      va="center", fontsize=7.3, color="white", weight="bold")
        if q >= 8:
            ax_rates.text(p + q / 2, y, f"{q:.1f}%",
                          ha="center", va="center", fontsize=7.1, color="0.15")
    ax_rates.set_xlim(0, 100)
    ax_rates.xaxis.set_major_formatter(PercentFormatter(xmax=100))
    ax_rates.set_xlabel("Within-frequency share")
    ax_rates.set_ylabel("Recorded CMAT visits")
    ax_rates.set_title("PASS versus non-PASS", fontsize=10, pad=12)
    ax_rates.set_yticks(xpos, GROUPS)

    # Centre: from the archived 0.1-Z histogram, each component is divided
    # by the *entire group n*. PASS and non-PASS histograms overlap
    # translucently on the same row: they are not stacked or rescaled to
    # their separate PASS/non-PASS populations.
    by_group = {}
    max_bin_share = 0.0
    for group, n in zip(GROUPS, sample_size):
        subset = histogram.loc[histogram["group"].eq(group)]
        if subset.empty:
            raise ValueError(f"Missing Z histogram for {group} visits")
        bins = subset.pivot_table(
            index="bin_center", columns="component",
            values="count", aggfunc="sum", fill_value=0
        ).sort_index()
        passing = bins["pass"].to_numpy(dtype=float) * 100 / n
        failing = bins.drop(columns=["pass"]).sum(axis=1).to_numpy(dtype=float) * 100 / n
        if passing.sum() + failing.sum() > 100.001:
            raise ValueError(f"Z histogram exceeds group size for {group}")
        centers = bins.index.to_numpy(dtype=float)
        by_group[group] = (centers, passing, failing)
        max_bin_share = max(max_bin_share, passing.max(initial=0), failing.max(initial=0))

    row_height = .70
    scale = row_height / max(max_bin_share, 1e-6)
    for y, group in zip(xpos, GROUPS):
        centers, passing, failing = by_group[group]
        ax_z.bar(centers, failing * scale, width=.095,
                 bottom=y, color=palette["nonpass"], alpha=.50,
                 linewidth=0, align="center", zorder=2)
        ax_z.bar(centers, passing * scale, width=.095,
                 bottom=y, color=palette["pass"], alpha=.55,
                 linewidth=0, align="center", zorder=3)
        ax_z.hlines(y, -2.0, 2.0, color="0.55", linewidth=.4, zorder=1)
    ax_z.set_xlim(-2.03, 2.03)
    ax_z.set_xlabel("Instructor–period standardised final outcome (Z)")
    ax_z.set_title("Translucent Z-score histograms", fontsize=10, pad=12)
    ax_z.text(
        .02, .02, "Common scale: %.1f%% of full group per 0.1-Z bin" % max_bin_share,
        transform=ax_z.transAxes, fontsize=7, color="0.3",
        bbox=dict(facecolor="white", edgecolor="none", alpha=.75, pad=1)
    )
    ax_z.tick_params(axis="y", left=False, labelleft=False)

    # Right: complete attendance-frequency group counts, not the number
    # falling inside the histogram's restricted Z plotting window.
    # Start each bar at one for a well-defined logarithmic axis;
    # its right end still encodes the exact full-group count.
    ax_freq.barh(xpos, sample_size - 1, left=1, height=.58,
                 color="0.50", alpha=.75, edgecolor="white", linewidth=.3)
    ax_freq.set_xscale("log")
    ax_freq.set_xlim(1, int(sample_size.max()) * 2.2)
    ax_freq.set_xlabel("Students (log scale)")
    ax_freq.set_title("Attendance frequency", fontsize=10, pad=12)
    ax_freq.tick_params(axis="y", left=False, labelleft=False)
    for y, count in zip(xpos, sample_size):
        ax_freq.text(count * 1.12, y, f"{count:,}", fontsize=7.5, va="center")
    ax_freq.grid(axis="x", linewidth=.35, alpha=.25)

    # Row boundaries are *institutional interpretation bands*, not
    # regression blocks or Holm-established changepoints.
    for ax in (ax_rates, ax_z, ax_freq):
        for boundary in (.5, 3.5, 6.5):
            ax.axhline(boundary, color="0.35", linestyle="--",
                       linewidth=.75, alpha=.60)
        ax.set_ylim(len(GROUPS) - .38, -.62)
        ax.grid(axis="y", visible=False)

    fig.legend(handles=[
        Patch(facecolor=palette["pass"], alpha=.75,
              label="PASS (numeric grade ≥7.5)"),
        Patch(facecolor=palette["nonpass"], alpha=.65,
              label="non-PASS (numeric failure or BA/BV/RT)"),
    ], loc="upper center", bbox_to_anchor=(.5, 1.015),
       ncol=2, frameon=False, fontsize=9)
    fig.suptitle("Final outcomes and CMAT use by visit frequency",
                 fontsize=12, y=1.07)
    fig.text(.5, -.025,
             "Dashed lines: 0 | 1–3 (PPA1 completed at visit 3) | 4–6 | 7+. "
             "Histogram shows only −2 ≤ Z ≤ 2; percentages and N use all students.",
             ha="center", va="bottom", fontsize=8, color="0.35")
    fig.subplots_adjust(left=.075, right=.96, top=.87, bottom=.16)
    return save(fig, "fig01_cohort_outcome_attendance.pdf")

def main() -> int:
    argparse.ArgumentParser(
        description="Regenerate Paper 2.1 upper-triangular Wald/Holm heatmaps."
    ).parse_args()
    validate()
    set_style()
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    outputs = [
        plot_cohort_outcome_attendance_overview(),
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
