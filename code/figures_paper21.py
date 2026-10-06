#!/usr/bin/env python3
"""Generate Paper 2.1 publication figures from aggregate analysis outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm
from matplotlib.patches import Patch
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
ZERO_DISPLAY_GROUPS = ["0", "1", "2", "3", "4", "5", "6", "7+"]
USER_GROUPS = ["1", "2", "3", "4", "5", "6+"]
SENSITIVITY_GROUPS = ["1", "2", "3", "4", "5", "6", "7+"]
OUTCOME_STATES = ["pass", "numeric_nonpass", "BV", "RT", "BA"]

# Consistent publication colours for observed and imputed outcome-state displays.
OUTCOME_COLORS = {
    "pass": "#2563EB",              # blue
    "numeric_nonpass": "#DA70D6",  # orchid
    "BV": "#F472B6",               # pink
    "RT": "#F59E0B",               # orange
    "BA": "#FACC15",               # yellow
}

OBSOLETE_FIGURES = [
    "fig02_pairwise_z_heatmap.pdf",
    "fig03_pairwise_pass_heatmap.pdf",
    "fig04_complete_case_gmm_ridgeline.pdf",
    "fig05_lower_component_weight.pdf",
    "fig06_sensitivity_7plus_z_pvalue_dashboard.pdf",
    "fig07_sensitivity_7plus_pass_pvalue_dashboard.pdf",
    "fig08_sensitivity_6_7plus_complete_case_gmm_ridgeline.pdf",
    "fig09_sensitivity_6_7plus_lower_component_weight.pdf",
    "figS01_zero_inclusive_z_heatmap.pdf",
    "figS02_zero_inclusive_pass_heatmap.pdf",
]


def _save(fig: plt.Figure, name: str) -> Path:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / name
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def validate() -> None:
    required = [
        "10n_zero_inclusive_7plus_descriptives.csv",
        "10o_zero_inclusive_7plus_exact_administrative_composition.csv",
        "10p_zero_inclusive_7plus_stacked_ridgeline_density.csv",
        "10q_zero_inclusive_7plus_observed_numeric_grade_histogram.csv",
        "10r_zero_inclusive_7plus_imputed_z_short_kde_density.csv",
        "10s_zero_inclusive_7plus_imputed_z_histogram.csv",
        "26b_zero_inclusive_7plus_z_effect_matrix.csv",
        "26d_zero_inclusive_7plus_pass_odds_ratio_matrix.csv",
        "26e_zero_inclusive_7plus_z_p_raw_matrix.csv",
        "26f_zero_inclusive_7plus_z_p_holm_matrix.csv",
        "26g_zero_inclusive_7plus_pass_p_raw_matrix.csv",
        "26h_zero_inclusive_7plus_pass_p_holm_matrix.csv",
        "38_complete_case_gmm_two_component_parameters.csv",
        "42_imputed_gmm_two_component_parameters.csv",
        "46_complete_case_gmm_ridgeline_density.csv",
        "54_sensitivity_6_7plus_complete_case_gmm_two_component_parameters.csv",
        "58_sensitivity_6_7plus_imputed_gmm_two_component_parameters.csv",
        "62_sensitivity_6_7plus_complete_case_gmm_ridgeline_density.csv",
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
        if subset.empty:
            continue
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

def _plot_observed_histogram_structure(
    *,
    histogram_path: Path,
    composition_path: Path,
    group_order: list[str],
    filename: str,
    grade_title: str,
) -> Path:
    """Plot observed non-passing shares beside a full-group-normalised histogram."""
    histogram = pd.read_csv(histogram_path)
    composition = pd.read_csv(composition_path)
    histogram["group"] = histogram["group"].astype(str)
    composition["group"] = composition["group"].astype(str)

    share = (
        composition.set_index(["group", "outcome_state"])["share_within_group"]
        .astype(float)
    )

    component_labels = {
        "pass": "Numeric pass (>=7.5)",
        "numeric_nonpass": "Numeric <7.5",
        "BV": "BV",
        "RT": "RT",
        "BA": "BA",
    }
    component_colors = OUTCOME_COLORS.copy()

    fig, (ax_admin, ax_grade, ax_counts) = plt.subplots(
        1, 3, figsize=(12.6, 6.2), sharey=True,
        gridspec_kw={"width_ratios": [1.7, 4.8, 1.05], "wspace": 0.06},
    )
    hist_height = 0.78
    positions = np.arange(len(group_order), dtype=float)

    group_counts = (
        histogram.groupby("group", observed=True)["group_n"]
        .first()
        .reindex(group_order)
        .astype(float)
    )
    if group_counts.isna().any():
        missing_groups = group_counts.index[group_counts.isna()].tolist()
        raise ValueError(
            "Missing group_n values for count panel: "
            + ", ".join(str(group) for group in missing_groups)
        )

    def group_share(group: str, state: str) -> float:
        key = (group, state)
        return float(share.loc[key]) if key in share.index else 0.0

    nonpass_states = ["numeric_grade_below_7.5", "BV", "RT", "BA"]
    nonpass_totals = [
        100.0 * sum(group_share(group, state) for state in nonpass_states)
        for group in group_order
    ]
    nonpass_limit = max(20.0, 5.0 * np.ceil((max(nonpass_totals) + 3.0) / 5.0))
    max_bin_percent = float(histogram["percent_of_full_group"].max())
    hist_scale_percent = max(5.0, 5.0 * np.ceil(max_bin_percent / 5.0))

    for position, group in zip(positions, group_order):
        left = 0.0
        for state in nonpass_states:
            width = 100.0 * group_share(group, state)
            color_key = "numeric_nonpass" if state == "numeric_grade_below_7.5" else state
            ax_admin.barh(
                position, width, left=left, height=0.38,
                color=component_colors[color_key], edgecolor="white", linewidth=0.45,
            )
            if width >= 1.15:
                ax_admin.text(left + width / 2.0, position, f"{width:.1f}%",
                              ha="center", va="center", fontsize=6.4)
            elif width > 0:
                ax_admin.text(left + width / 2.0, position + 0.29, f"{width:.1f}%",
                              ha="center", va="bottom", fontsize=5.8)
            left += width
        ax_admin.text(
            min(left + 0.45, nonpass_limit - 0.25), position, f"{left:.1f}% total",
            ha="left" if left + 0.45 < nonpass_limit - 0.25 else "right",
            va="center", fontsize=6.5, color="0.25",
        )

        observed = histogram.loc[histogram["group"].eq(group)].sort_values("bin_center")
        if observed.empty:
            continue
        x = observed["bin_center"].to_numpy(float)
        percent = observed["percent_of_full_group"].to_numpy(float)
        heights = hist_height * percent / hist_scale_percent
        colors = [
            component_colors["numeric_nonpass"] if center < 7.5 else component_colors["pass"]
            for center in x
        ]
        ax_grade.bar(
            x, heights, width=0.088, bottom=position, align="center",
            color=colors, edgecolor="white", linewidth=0.12,
        )
        ax_grade.hlines(position, -0.05, 10.05, linewidth=0.55, color="0.35")

        fail_share = 100.0 * group_share(group, "numeric_grade_below_7.5")
        pass_share = 100.0 * group_share(group, "pass")
        ax_grade.text(
            5.6, position + 0.11, f"{fail_share:.1f}% total",
            ha="right", va="bottom", fontsize=6.5,
            color=component_colors["numeric_nonpass"],
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.78, "pad": 0.8},
        )
        ax_grade.text(
            9.72, position + 0.11, f"{pass_share:.1f}% total",
            ha="right", va="bottom", fontsize=6.5, color=component_colors["pass"],
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.78, "pad": 0.8},
        )

    ax_admin.set_xlim(0.0, nonpass_limit)
    ax_admin.set_xticks(np.arange(0.0, nonpass_limit + 0.1, 5.0))
    ax_admin.set_xlabel("Non-passing outcomes (% of full group)")
    ax_admin.set_ylabel("CMAT visits during the MU academic period")
    ax_admin.set_yticks(positions, group_order)
    ax_admin.set_title("Observed non-passing outcomes", fontsize=9.5)
    ax_admin.grid(axis="y", visible=False)

    ax_grade.axvline(7.5, linestyle="--", linewidth=0.9, color="0.35", alpha=0.85)
    ax_grade.text(
        7.5, len(group_order) - 0.05, "pass mark 7.5", rotation=90,
        ha="right", va="top", fontsize=7, color="0.35",
    )
    ax_grade.set_xlim(-0.05, 10.05)
    ax_grade.set_ylim(-0.35, len(group_order) - 1 + hist_height + 0.28)
    ax_grade.set_xlabel("Observed numeric MU final grade")
    ax_grade.set_title(grade_title, fontsize=9.5)
    ax_grade.grid(axis="y", visible=False)
    ax_grade.tick_params(axis="y", left=False, labelleft=False)
    ax_grade.text(
        0.01, 0.985,
        f"Common bar-height scale: 0–{hist_scale_percent:.0f}% of full group per bin",
        transform=ax_grade.transAxes, ha="left", va="top", fontsize=6.6, color="0.35",
    )

    # Far-right panel: attendance-group sample sizes.  This panel uses the
    # same y positions as the outcome panels so the loss of support in the
    # upper-frequency tail is visible directly in Figure 1.
    count_values = group_counts.to_numpy(float)
    max_count = float(np.nanmax(count_values))
    count_limit = max_count * 1.22
    ax_counts.barh(
        positions,
        count_values,
        height=0.42,
        color="0.62",
        edgecolor="white",
        linewidth=0.45,
    )
    for position, value in zip(positions, count_values):
        ax_counts.text(
            value + 0.025 * max_count,
            position,
            f"{int(value):,}",
            ha="left",
            va="center",
            fontsize=6.8,
            color="0.20",
        )
    ax_counts.set_xlim(0.0, count_limit)
    ax_counts.set_xlabel("Students (N)")
    ax_counts.set_title("Counts", fontsize=9.5)
    ax_counts.grid(axis="y", visible=False)
    ax_counts.grid(axis="x", linewidth=0.55, alpha=0.45)
    ax_counts.tick_params(axis="y", left=False, labelleft=False)

    fig.legend(
        handles=[Patch(facecolor=component_colors[c], label=component_labels[c])
                 for c in ["pass", "numeric_nonpass", "BV", "RT", "BA"]],
        frameon=False, ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.01),
    )
    fig.subplots_adjust(top=0.88)
    return _save(fig, filename)


def plot_observed_pre_imputation_structure() -> Path:
    """Observed zero-inclusive structure with exact 1--6 visits and a 7+ tail."""
    return _plot_observed_histogram_structure(
        histogram_path=TABLES_DIR / "10q_zero_inclusive_7plus_observed_numeric_grade_histogram.csv",
        composition_path=TABLES_DIR / "10o_zero_inclusive_7plus_exact_administrative_composition.csv",
        group_order=ZERO_DISPLAY_GROUPS,
        filename="fig01a_observed_pre_imputation_structure.pdf",
        grade_title="Observed numeric grades: 0, exact 1–6 visits, and 7+",
    )


def plot_distribution_and_composition() -> Path:
    density = pd.read_csv(
        TABLES_DIR / "10p_zero_inclusive_7plus_stacked_ridgeline_density.csv"
    )
    summary = pd.read_csv(TABLES_DIR / "10n_zero_inclusive_7plus_descriptives.csv")
    summary = summary.rename(
        columns={
            "mean_z": "outcome_mean",
            "z_ci95_low": "outcome_ci95_low",
            "z_ci95_high": "outcome_ci95_high",
        }
    )

    fig, ax = plt.subplots(figsize=(8.4, 6.0))
    component_labels = {
        "pass": "Pass",
        "numeric_nonpass": "Numeric <7.5",
        "BV": "BV",
        "RT": "RT",
        "BA": "BA",
    }
    component_colors = OUTCOME_COLORS.copy()
    plot_stacked_ridgeline(
        density,
        group_order=ZERO_DISPLAY_GROUPS,
        component_order=OUTCOME_STATES,
        summary=summary,
        colors=component_colors,
        component_labels=component_labels,
        ridge_height=0.82,
        ax=ax,
    )
    ax.axvline(0, linestyle="--", linewidth=0.9, alpha=0.65)
    ax.set_xlim(-2, 2)
    ax.set_xlabel("Instructor-period-standardised MU grade (Z)")
    ax.set_ylabel("CMAT visits during the MU academic period")
    ax.grid(axis="y", visible=False)
    ax.legend(
        handles=[
            Patch(
                facecolor=component_colors[component],
                label=component_labels[component],
            )
            for component in OUTCOME_STATES
        ],
        frameon=False,
        ncol=5,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
    )
    return _save(fig, "fig01_distribution_composition_ridgeline.pdf")

def plot_imputed_histogram_kde_overlay() -> Path:
    """Overlay a short-bandwidth KDE and histogram for the imputed Z outcome."""
    density = pd.read_csv(
        TABLES_DIR / "10r_zero_inclusive_7plus_imputed_z_short_kde_density.csv"
    )
    histogram = pd.read_csv(
        TABLES_DIR / "10s_zero_inclusive_7plus_imputed_z_histogram.csv"
    )
    density["group"] = density["group"].astype(str)
    density["component"] = density["component"].astype(str)
    histogram["group"] = histogram["group"].astype(str)
    histogram["component"] = histogram["component"].astype(str)

    component_labels = {
        "pass": "Pass",
        "numeric_nonpass": "Numeric <7.5",
        "BV": "BV",
        "RT": "RT",
        "BA": "BA",
    }
    ridge_height = 0.78
    fig, ax = plt.subplots(figsize=(8.8, 6.2))

    for y, group in enumerate(ZERO_DISPLAY_GROUPS):
        kde_group = density.loc[
            density["group"].eq(group)
            & density["x"].between(-2.0, 2.0)
        ].copy()
        hist_group = histogram.loc[histogram["group"].eq(group)].copy()
        if kde_group.empty or hist_group.empty:
            continue

        x_values = np.sort(kde_group["x"].unique().astype(float))
        total_kde = (
            kde_group.drop_duplicates("x")
            .set_index("x")
            .reindex(x_values)["density_total"]
            .fillna(0.0)
            .to_numpy(float)
        )

        bin_centers = np.sort(hist_group["bin_center"].unique().astype(float))
        hist_total = (
            hist_group.groupby("bin_center", observed=True)["density_of_full_group"]
            .sum()
            .reindex(bin_centers, fill_value=0.0)
            .to_numpy(float)
        )
        maximum = float(max(np.nanmax(total_kde), np.nanmax(hist_total)))
        scale = ridge_height / maximum if np.isfinite(maximum) and maximum > 0 else 1.0

        hist_cumulative = np.zeros_like(bin_centers, dtype=float)
        for component in OUTCOME_STATES:
            frame = (
                hist_group.loc[
                    hist_group["component"].eq(component),
                    ["bin_center", "bin_left", "bin_right", "density_of_full_group"],
                ]
                .set_index("bin_center")
                .reindex(bin_centers)
            )
            values = frame["density_of_full_group"].fillna(0.0).to_numpy(float)
            widths = (
                frame["bin_right"].fillna(pd.Series(bin_centers + 0.05, index=frame.index)).to_numpy(float)
                - frame["bin_left"].fillna(pd.Series(bin_centers - 0.05, index=frame.index)).to_numpy(float)
            )
            ax.bar(
                bin_centers,
                values * scale,
                width=widths * 0.90,
                bottom=y + hist_cumulative * scale,
                color=OUTCOME_COLORS[component],
                alpha=0.38,
                edgecolor="none",
                align="center",
                zorder=2,
            )
            hist_cumulative += values

        kde_cumulative = np.zeros_like(x_values, dtype=float)
        for component in OUTCOME_STATES:
            component_values = (
                kde_group.loc[
                    kde_group["component"].eq(component),
                    ["x", "density_component"],
                ]
                .set_index("x")
                .reindex(x_values)["density_component"]
                .fillna(0.0)
                .to_numpy(float)
            )
            lower = y + kde_cumulative * scale
            kde_cumulative += component_values
            upper = y + kde_cumulative * scale
            ax.fill_between(
                x_values,
                lower,
                upper,
                color=OUTCOME_COLORS[component],
                alpha=0.22,
                linewidth=0,
                zorder=3,
            )

        ax.plot(
            x_values,
            y + total_kde * scale,
            color="0.15",
            linewidth=0.9,
            alpha=0.80,
            zorder=4,
        )
        ax.hlines(y, -2.0, 2.0, color="0.72", linewidth=0.45, zorder=1)

    scale_values = pd.to_numeric(density.get("bandwidth_scale"), errors="coerce")
    bandwidth_scale = float(scale_values.dropna().iloc[0]) if scale_values.notna().any() else np.nan
    note = (
        f"KDE bandwidth = {bandwidth_scale:.2f} x baseline; histogram bins = 0.1 Z"
        if np.isfinite(bandwidth_scale)
        else "Short-bandwidth KDE; histogram bins = 0.1 Z"
    )
    ax.text(
        0.01, 0.985, note, transform=ax.transAxes,
        ha="left", va="top", fontsize=6.8, color="0.35"
    )
    ax.axvline(0.0, linestyle="--", linewidth=0.9, color="0.30", alpha=0.65)
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-0.35, len(ZERO_DISPLAY_GROUPS) - 1 + ridge_height + 0.25)
    ax.set_yticks(np.arange(len(ZERO_DISPLAY_GROUPS)), ZERO_DISPLAY_GROUPS)
    ax.set_xlabel("Instructor-period-standardised MU grade (Z)")
    ax.set_ylabel("CMAT visits during the MU academic period")
    ax.set_title("Imputed outcome: histogram and shorter-bandwidth KDE", fontsize=10)
    ax.grid(axis="y", visible=False)
    ax.legend(
        handles=[
            Patch(facecolor=OUTCOME_COLORS[c], label=component_labels[c], alpha=0.75)
            for c in OUTCOME_STATES
        ],
        frameon=False,
        ncol=5,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
    )
    return _save(fig, "fig02_imputed_histogram_kde_overlay.pdf")

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
    odds = _matrix_from_csv(
        TABLES_DIR / "26d_zero_inclusive_7plus_pass_odds_ratio_matrix.csv", groups
    )
    log_odds = np.log(odds)
    np.fill_diagonal(z, np.nan)
    np.fill_diagonal(log_odds, np.nan)

    zmax = float(np.nanmax(np.abs(z)))
    lomax = float(np.nanmax(np.abs(log_odds)))
    if not np.isfinite(zmax) or zmax <= 0:
        zmax = 1.0
    if not np.isfinite(lomax) or lomax <= 0:
        lomax = 1.0

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.5), sharex=True, sharey=True)
    threshold = groups.index("2") + 0.5

    left = axes[0].imshow(z, cmap="RdBu_r", vmin=-zmax, vmax=zmax)
    right = axes[1].imshow(log_odds, cmap="RdBu_r", vmin=-lomax, vmax=lomax)

    for ax, title in zip(
        axes,
        [
            "Adjusted standardised-grade difference",
            "Adjusted odds ratio for passing (point estimate)",
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
            if np.isfinite(log_odds[i, j]):
                value = odds[i, j]
                axes[1].text(
                    j, i, f"{value:.2f}",
                    ha="center", va="center", fontsize=7.2,
                )

    cbar_left = fig.colorbar(left, ax=axes[0], shrink=0.82, pad=0.03)
    cbar_left.set_label("Row minus column, SD")
    cbar_right = fig.colorbar(right, ax=axes[1], shrink=0.82, pad=0.03)
    ticks = cbar_right.get_ticks()
    cbar_right.set_ticklabels([f"{np.exp(value):.2f}" for value in ticks])
    cbar_right.set_label("Odds ratio for passing (row / column)")

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


def _gaussian_density(
    x: np.ndarray,
    *,
    mean: float,
    sd: float,
    weight: float = 1.0,
) -> np.ndarray:
    sd = max(float(sd), 1e-9)
    z = (x - float(mean)) / sd
    return float(weight) * np.exp(-0.5 * z**2) / (sd * np.sqrt(2.0 * np.pi))


def _full_7plus_gmm_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Assemble independently fitted 0--5 and exact-6/7+ EM outputs."""
    complete_primary = pd.read_csv(
        TABLES_DIR / "38_complete_case_gmm_two_component_parameters.csv"
    )
    imputed_primary = pd.read_csv(
        TABLES_DIR / "42_imputed_gmm_two_component_parameters.csv"
    )
    density_primary = pd.read_csv(
        TABLES_DIR / "46_complete_case_gmm_ridgeline_density.csv"
    )
    complete_tail = pd.read_csv(
        TABLES_DIR / "54_sensitivity_6_7plus_complete_case_gmm_two_component_parameters.csv"
    )
    imputed_tail = pd.read_csv(
        TABLES_DIR / "58_sensitivity_6_7plus_imputed_gmm_two_component_parameters.csv"
    )
    density_tail = pd.read_csv(
        TABLES_DIR / "62_sensitivity_6_7plus_complete_case_gmm_ridgeline_density.csv"
    )

    for frame in (
        complete_primary, imputed_primary, density_primary,
        complete_tail, imputed_tail, density_tail,
    ):
        frame["group"] = frame["group"].astype(str)

    keep_primary = ["0", "1", "2", "3", "4", "5"]
    complete = pd.concat(
        [
            complete_primary.loc[complete_primary["group"].isin(keep_primary)],
            complete_tail.loc[complete_tail["group"].isin(["6", "7+"])],
        ],
        ignore_index=True,
    )
    imputed = pd.concat(
        [
            imputed_primary.loc[imputed_primary["group"].isin(keep_primary)],
            imputed_tail.loc[imputed_tail["group"].isin(["6", "7+"])],
        ],
        ignore_index=True,
    )
    density = pd.concat(
        [
            density_primary.loc[density_primary["group"].isin(keep_primary)],
            density_tail.loc[density_tail["group"].isin(["6", "7+"])],
        ],
        ignore_index=True,
    )
    return complete, imputed, density


def plot_complete_case_gmm_ridgeline() -> Path:
    params, _, density = _full_7plus_gmm_tables()

    fig, ax = plt.subplots(figsize=(9.4, 6.8))
    ridge_height = 0.76
    available_groups = [
        group
        for group in ZERO_DISPLAY_GROUPS
        if group in set(density["group"]) and group in set(params["group"])
    ]

    for position, group in enumerate(available_groups):
        observed = (
            density.loc[density["group"].eq(group)]
            .drop_duplicates("x")
            .sort_values("x")
        )
        x = observed["x"].to_numpy(float)
        y = observed["density_total"].to_numpy(float)
        scale = float(np.nanmax(y))
        if not np.isfinite(scale) or scale <= 0:
            continue

        baseline = float(position)
        observed_scaled = baseline + ridge_height * y / scale
        ax.fill_between(x, baseline, observed_scaled, color="0.75", alpha=0.30)
        ax.plot(
            x, observed_scaled, linewidth=1.15, color="0.25",
            label="Observed complete-case KDE" if position == 0 else None,
        )

        group_params = params.loc[params["group"].eq(group)].copy()
        component_curves: dict[str, np.ndarray] = {}
        for component, linestyle, color in [
            ("lower_performance", "--", "C1"),
            ("higher_performance", "-.", "C2"),
        ]:
            row = group_params.loc[group_params["component"].eq(component)]
            if row.empty:
                continue
            row = row.iloc[0]
            curve = _gaussian_density(
                x,
                mean=float(row["mean"]),
                sd=float(row["sd"]),
                weight=float(row["weight"]),
            )
            component_curves[component] = curve
            ax.plot(
                x,
                baseline + ridge_height * curve / scale,
                linestyle=linestyle,
                color=color,
                linewidth=1.35,
                label=(
                    "Lower-performance Gaussian"
                    if position == 0 and component == "lower_performance"
                    else "Higher-performance Gaussian"
                    if position == 0 and component == "higher_performance"
                    else None
                ),
            )

        if len(component_curves) == 2:
            fitted = (
                component_curves["lower_performance"]
                + component_curves["higher_performance"]
            )
            ax.plot(
                x,
                baseline + ridge_height * fitted / scale,
                linewidth=0.9,
                color="C3",
                alpha=0.8,
                label="Two-component fitted density" if position == 0 else None,
            )

        lower = group_params.loc[group_params["component"].eq("lower_performance")]
        higher = group_params.loc[group_params["component"].eq("higher_performance")]
        if not lower.empty and not higher.empty:
            lo, hi = lower.iloc[0], higher.iloc[0]
            ax.text(
                0.995,
                (baseline + 0.08) / max(len(available_groups), 1),
                (
                    f"πL={float(lo['weight']):.0%}, μL={float(lo['mean']):.2f}; "
                    f"πH={float(hi['weight']):.0%}, μH={float(hi['mean']):.2f}"
                ),
                transform=ax.transAxes,
                ha="right",
                va="bottom",
                fontsize=7.2,
            )

    ax.axhline(2.5, linestyle="--", linewidth=0.8, color="0.55", alpha=0.7)
    ax.set_xlim(-2, 2)
    ax.set_yticks(np.arange(len(available_groups)), available_groups)
    ax.set_ylim(-0.15, max(len(available_groups) - 0.05, 0.85))
    ax.set_xlabel("Instructor-period-standardised numeric final grade (complete case)")
    ax.set_ylabel("CMAT visits during the MU academic period")
    ax.set_title("Complete-case Gaussian-mixture fits: 0, exact 1–6, and 7+")
    ax.grid(axis="y", visible=False)
    ax.legend(frameon=False, ncol=2, loc="lower center", bbox_to_anchor=(0.5, 1.01))
    return _save(fig, "fig07_complete_case_gmm_ridgeline.pdf")


def plot_lower_component_weight() -> Path:
    complete, imputed, _ = _full_7plus_gmm_tables()

    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    x = np.arange(len(ZERO_DISPLAY_GROUPS))
    for frame, label, linestyle in [
        (complete, "Numeric complete case", "-"),
        (imputed, "Imputed-outcome sensitivity", "--"),
    ]:
        lower = (
            frame.loc[frame["component"].eq("lower_performance"), ["group", "weight"]]
            .set_index("group")
            .reindex(ZERO_DISPLAY_GROUPS)
        )
        y = lower["weight"].to_numpy(float)
        ax.plot(x, y, marker="o", linestyle=linestyle, linewidth=1.4, label=label)

    ax.axvline(2.5, linestyle="--", linewidth=0.9, color="0.45", alpha=0.75)
    ax.text(2.5, 0.98, "PPA threshold", ha="center", va="top", fontsize=7, color="0.35")
    ax.set_xticks(x, ZERO_DISPLAY_GROUPS)
    ax.set_ylim(0, 1)
    ax.set_xlabel("CMAT visits during the MU academic period")
    ax.set_ylabel(r"Estimated lower-component weight $\hat{\pi}_{L,k}$")
    ax.set_title("Lower-component weight: 0, exact 1–6, and 7+ visits")
    ax.legend(frameon=False)
    ax.grid(axis="x", visible=False)
    return _save(fig, "fig08_lower_component_weight.pdf")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    validate()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    for obsolete in OBSOLETE_FIGURES:
        path = FIGURES_DIR / obsolete
        if path.exists():
            path.unlink()
    set_style()
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    for path in [
        plot_observed_pre_imputation_structure(),
        plot_distribution_and_composition(),
        plot_imputed_histogram_kde_overlay(),
        plot_pairwise_effect_dashboard(),
        plot_z_pvalue_dashboard(),
        plot_pass_pvalue_dashboard(),
        plot_complete_case_gmm_ridgeline(),
        plot_lower_component_weight(),
    ]:
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
