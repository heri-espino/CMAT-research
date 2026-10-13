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
BANDS = (("0", 0.0), ("1–3 (PPA1 option)", 2.0), ("4–6", 5.0), ("7+", 7.0))


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
             "Eligible first-semester students can complete a PPA1 activity on visit 3; separators are descriptive.",
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
             "PPA1 offers eligible first-semester students a 3-visit option; Holm applies to all 28 pairs.",
             ha="center", fontsize=8, color="0.3")
    return save(fig, filename)



def plot_cohort_outcome_attendance_overview() -> Path:
    """Display final-outcome type, overlaid standardised grades and attendance.

    PASS and numeric non-PASS use observed grade boundaries: >=7.5 and <7.5.
    BV, RT and BA are administrative outcomes with no numeric final grade.
    All graphical proportions use full attendance-group denominators.
    """
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    from matplotlib.ticker import PercentFormatter

    summary = pd.read_csv(TABLES / "10n_zero_inclusive_7plus_descriptives.csv")
    summary["group"] = summary["group"].astype(str)
    summary = summary.set_index("group").reindex(GROUPS)
    z_columns = ["n_outcome", "mean_z", "sd_z", "z_ci95_low", "z_ci95_high"]
    if summary[["n", "pass_rate", *z_columns]].isna().any().any():
        raise ValueError("Missing group-level descriptive Z statistics")
    if not np.array_equal(
        summary["n_outcome"].to_numpy(dtype=int),
        summary["n"].to_numpy(dtype=int),
    ):
        raise ValueError("Full-sample Z summaries and attendance groups differ")
    if not np.all(
        (summary["z_ci95_low"] <= summary["mean_z"])
        & (summary["mean_z"] <= summary["z_ci95_high"])
        & (summary["sd_z"] >= 0)
    ):
        raise ValueError("Invalid unadjusted mean, SD or CI bounds")

    composition = pd.read_csv(
        TABLES / "10o_zero_inclusive_7plus_exact_administrative_composition.csv"
    )
    composition["group"] = composition["group"].astype(str)
    categories = ["pass", "numeric_grade_below_7.5", "BV", "RT", "BA"]
    states = composition.pivot_table(
        index="group", columns="outcome_state", values="n",
        aggfunc="sum", fill_value=0
    ).reindex(index=GROUPS, columns=categories, fill_value=0)
    if states.isna().any().any():
        raise ValueError("Missing outcome states")
    n = summary["n"].to_numpy(dtype=int)
    if int(n.sum()) != 6627:
        raise ValueError("Unexpected cohort size")
    if not np.array_equal(states.sum(axis=1).to_numpy(dtype=int), n):
        raise ValueError("Outcome composition does not sum to visit-group sizes")
    if not np.allclose(
        states["pass"].to_numpy(dtype=float) / n,
        summary["pass_rate"].to_numpy(dtype=float), rtol=0, atol=1e-10
    ):
        raise ValueError("PASS fractions conflict with outcome composition")

    histogram = pd.read_csv(
        TABLES / "10s_zero_inclusive_7plus_imputed_z_histogram.csv"
    )
    histogram["group"] = histogram["group"].astype(str)
    if not set(["pass", "numeric_nonpass", "BV", "RT", "BA"]).issubset(
        histogram["component"].unique()
    ):
        raise ValueError("Incomplete imputed Z histogram components")

    colors = {
        "pass": "#367CA8",
        "numeric": "#E67630",
        "admin": "#DFB02D",
    }
    p = 100.0 * states["pass"].to_numpy(dtype=float) / n
    f = 100.0 * states["numeric_grade_below_7.5"].to_numpy(dtype=float) / n
    a = 100.0 * states[["BV", "RT", "BA"]].sum(axis=1).to_numpy(dtype=float) / n
    ypos = np.arange(len(GROUPS), dtype=float)

    fig, (ax_rate, ax_z, ax_count) = plt.subplots(
        1, 3, figsize=(14.0, 6.0), sharey=True,
        gridspec_kw={"width_ratios": [2.1, 5.1, 1.9], "wspace": 0.14},
    )
    for heights, left, color in (
        (p, np.zeros_like(p), colors["pass"]),
        (f, p, colors["numeric"]),
        (a, p + f, colors["admin"]),
    ):
        ax_rate.barh(ypos, heights, left=left, height=.58,
                     color=color, alpha=.86, edgecolor="white", linewidth=.25)
    for y, pi, fi, ai in zip(ypos, p, f, a):
        ax_rate.text(pi / 2, y, f"{pi:.1f}%", color="white",
                     ha="center", va="center", fontsize=7.2, weight="bold")
        if fi >= 5.3:
            ax_rate.text(pi + fi / 2, y, f"{fi:.1f}%",
                         ha="center", va="center", fontsize=6.5)
        if ai >= 5.3:
            ax_rate.text(pi + fi + ai / 2, y, f"{ai:.1f}%",
                         ha="center", va="center", fontsize=6.7)
    ax_rate.set_xlim(0, 100)
    ax_rate.xaxis.set_major_formatter(PercentFormatter(xmax=100))
    ax_rate.set_xlabel("Share within visit group")
    ax_rate.set_ylabel("Recorded CMAT visits")
    ax_rate.set_title("Final outcome composition", fontsize=10, pad=10)
    ax_rate.set_yticks(ypos, GROUPS)

    prepared = {}
    median_bins = {}
    peak = 0.0
    for group, size in zip(GROUPS, n):
        frame = histogram.loc[histogram["group"].eq(group)]
        if frame.empty:
            raise ValueError(f"Missing Z histogram for visits={group}")
        bins = frame.pivot_table(
            index="bin_center", columns="component",
            values="count", aggfunc="sum", fill_value=0
        ).sort_index()
        required = ["pass", "numeric_nonpass", "BV", "RT", "BA"]
        if not set(required).issubset(bins.columns):
            raise ValueError(f"Missing Z components for visits={group}")
        centers = bins.index.to_numpy(dtype=float)
        pass_h = bins["pass"].to_numpy(dtype=float) * 100 / size
        fail_h = bins["numeric_nonpass"].to_numpy(dtype=float) * 100 / size
        admin_h = bins[["BV", "RT", "BA"]].sum(axis=1).to_numpy(dtype=float) * 100 / size
        if sum(h.sum() for h in (pass_h, fail_h, admin_h)) > 100.0001:
            raise ValueError(f"Histogram total exceeds N for visits={group}")
        prepared[group] = (centers, pass_h, fail_h, admin_h)
        # Each Z bin is stacked, so the common scaling is determined by
        # its TOTAL percentage, not by the largest individual component.
        peak = max(peak, float((pass_h + fail_h + admin_h).max()))

        # Exact individual medians were NOT exported. The counts cover only
        # [-2, 2] in 0.1-Z bins. With n full-sample outcomes and k displayed
        # observations, m=n-k cases lie outside this plotting window.
        # Extremal allocations of those m cases to the two tails identify
        # a conservative interval containing the full-sample median.
        bins_for_median = (
            frame.groupby(["bin_left", "bin_right"], observed=True)["count"]
            .sum().reset_index().sort_values("bin_left")
        )
        counts = bins_for_median["count"].to_numpy(dtype=int)
        observed_n = int(counts.sum())
        omitted_n = int(size) - observed_n
        if omitted_n < 0 or observed_n < int(size) // 2 + 1:
            raise ValueError(f"Cannot bound full-group median from Z bins: {group}")
        low_rank = ((int(size) + 1) // 2) - omitted_n
        high_rank = (int(size) // 2) + 1
        cumulative = np.cumsum(counts)
        lower_idx = int(np.searchsorted(cumulative, max(1, low_rank), side="left"))
        upper_idx = int(np.searchsorted(cumulative, high_rank, side="left"))
        lower = float(bins_for_median.iloc[lower_idx]["bin_left"])
        upper = float(bins_for_median.iloc[upper_idx]["bin_right"])
        if lower > upper:
            raise ValueError(f"Invalid binned median bounds for group {group}")
        median_bins[group] = (lower, upper)

    # Keep the total ridge below the median and mean/CI annotations
    # (at y-.63 and y-.76); all rows share the same scale.
    common_scale = .50 / max(peak, 1e-9)
    for y, group in zip(ypos, GROUPS):
        x, pass_h, fail_h, admin_h = prepared[group]
        stacked_height = np.zeros_like(x, dtype=float)
        for h, color, order in (
            (pass_h, colors["pass"], 2),
            (fail_h, colors["numeric"], 3),
            (admin_h, colors["admin"], 4),
        ):
            height = h * common_scale
            # The shared y-axis is inverted. Stack each component above
            # the previous one so the three segments add to the bin total
            # and the histogram grows visually upward from y.
            ax_z.bar(x, height, width=.095,
                     bottom=y - stacked_height - height,
                     color=color, alpha=.92, align="center",
                     linewidth=0, zorder=order)
            stacked_height += height
        ax_z.hlines(y, -2, 2, color="0.50", linewidth=.4, zorder=1)

        # Draw the unadjusted, full-group mean and its existing 95% CI.
        # They come directly from 10n, not from the clipped histogram or
        # fixed-effects models; the SD is likewise a within-visit-group SD.
        row = summary.loc[group]
        avg, low, high = (
            float(row["mean_z"]), float(row["z_ci95_low"]),
            float(row["z_ci95_high"])
        )
        ci_y = y - .76
        ax_z.plot([low, high], [ci_y, ci_y], color="#202D3A",
                  linewidth=1.5, zorder=8, clip_on=False)
        ax_z.plot([low, low], [ci_y - .047, ci_y + .047],
                  color="#202D3A", linewidth=.9, zorder=8, clip_on=False)
        ax_z.plot([high, high], [ci_y - .047, ci_y + .047],
                  color="#202D3A", linewidth=.9, zorder=8, clip_on=False)
        ax_z.plot(avg, ci_y, marker="o", markersize=4.0, color="#202D3A",
                  markeredgecolor="white", markeredgewidth=.45,
                  zorder=9, clip_on=False)

        # The purple bar is a CONSERVATIVE MEDIAN LOCATION BOUND derived
        # from binned counts and unshown tails; it is NOT a confidence
        # interval. A diamond marks its midpoint, only as an approximation.
        med_low, med_high = median_bins[group]
        median_y = y - .63
        ax_z.plot([med_low, med_high], [median_y, median_y],
                  color="#8D52A1", linewidth=2.6, solid_capstyle="round",
                  zorder=8, clip_on=False)
        ax_z.plot((med_low + med_high) / 2, median_y,
                  marker="D", markersize=3.6, color="#8D52A1",
                  markeredgecolor="white", markeredgewidth=.4,
                  zorder=9, clip_on=False)

        # All eight SDs, means and approximate medians remain readable
        # without adding another full-width numerical table to the paper.
        ax_z.text(-1.98, y - .22,
                  f"mean {avg:+.2f} · median≈{(med_low+med_high)/2:+.2f}"
                  f" · SD {float(row['sd_z']):.2f}",
                  fontsize=6.9, ha="left", va="center", color="#283442",
                  zorder=11, clip_on=False,
                  bbox={"facecolor": "white", "edgecolor": "none",
                        "alpha": .74, "pad": .35})
    ax_z.set_xlim(-2.02, 2.02)
    ax_z.set_xlabel("Instructor–period standardised final outcome (Z)")
    ax_z.set_title("Stacked Z histograms; mean, median and uncertainty",
                   fontsize=10, pad=10)
    ax_z.tick_params(axis="y", left=False, labelleft=False)
    ax_z.text(
        .015, .025,
        f"Common scale: peak total {peak:.1f}% of group per 0.1-Z bin",
        transform=ax_z.transAxes, ha="left", va="bottom",
        fontsize=7, color="0.3",
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": .75, "pad": 1},
    )

    # A logarithmic count scale keeps the high-frequency small cells visible.
    ax_count.barh(ypos, n - 1, left=1, height=.58,
                  color="0.50", alpha=.75, linewidth=.3, edgecolor="white")
    ax_count.set_xscale("log")
    ax_count.set_xlim(1, float(n.max()) * 2.2)
    ax_count.set_xlabel("Students (log scale)")
    ax_count.set_title("Attendance counts", fontsize=10, pad=10)
    ax_count.tick_params(axis="y", left=False, labelleft=False)
    for y, size in zip(ypos, n):
        ax_count.text(size * 1.12, y, f"{size:,}", va="center", fontsize=7.4)

    for axis in (ax_rate, ax_z, ax_count):
        for boundary in (.5, 3.5, 6.5):
            axis.axhline(boundary, linestyle="--", color="0.38",
                         linewidth=.75, alpha=.6)
        axis.grid(axis="y", visible=False)
        # Space above the first ridge is needed for the CI and median marks.
        axis.set_ylim(len(GROUPS) - .35, -1.0)

    fig.legend(
        handles=[
            Patch(facecolor=colors["pass"], alpha=.86,
                  label="PASS: numeric grade ≥7.5"),
            Patch(facecolor=colors["numeric"], alpha=.86,
                  label="Numeric non-PASS: grade <7.5"),
            Patch(facecolor=colors["admin"], alpha=.86,
                  label="No numeric grade: BV / RT / BA"),
            Line2D([0], [0], color="#202D3A", linewidth=1.5,
                   marker="o", markersize=4,
                   label="Descriptive mean and 95% CI"),
            Line2D([0], [0], color="#8D52A1", linewidth=2.5,
                   marker="D", markersize=4,
                   label="Approximate median (binned bounds)"),
        ],
        loc="upper center", bbox_to_anchor=(.5, 1.018),
        ncol=5, frameon=False, fontsize=7.3,
    )
    fig.suptitle("Final outcomes and CMAT use by visit frequency",
                 fontsize=12, y=1.08)
    fig.text(
        .5, -.025,
        "Descriptive bands: 0 | 1–3 (PPA1 option at visit 3) | 4–6 | 7+. "
        "Only −2 ≤ Z ≤ 2 is plotted; mean, SD and CI use all Z outcomes. "
        "Median bounds use 0.1-Z bins and unshown-tail counts.",
        ha="center", fontsize=8, color="0.35",
    )
    fig.subplots_adjust(left=.08, right=.965, top=.87, bottom=.16)
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
