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
USER_GROUPS = ["1", "2", "3", "4", "5", "6+"]
SENSITIVITY_GROUPS = ["1", "2", "3", "4", "5", "6", "7+"]
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
        "10g_zero_inclusive_stacked_ridgeline_density.csv",
        "10b_zero_inclusive_descriptives.csv",
        "10d_zero_inclusive_exact_administrative_composition.csv",
        "10m_zero_inclusive_observed_numeric_grade_histogram.csv",
        "24a_sensitivity_7plus_exact_administrative_composition.csv",
        "25a_sensitivity_7plus_observed_numeric_grade_histogram.csv",
        "22a_sensitivity_7plus_p_raw_continuous_matrix.csv",
        "22b_sensitivity_7plus_p_holm_continuous_matrix.csv",
        "23a_sensitivity_7plus_p_raw_pass_matrix.csv",
        "23b_sensitivity_7plus_p_holm_pass_matrix.csv",
        "18_primary_z_heatmap_matrix.csv",
        "19_primary_pass_heatmap_matrix.csv",
        "38_complete_case_gmm_two_component_parameters.csv",
        "42_imputed_gmm_two_component_parameters.csv",
        "46_complete_case_gmm_ridgeline_density.csv",
        "10j_zero_inclusive_z_heatmap_matrix.csv",
        "10k_zero_inclusive_pass_heatmap_matrix.csv",
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
    """Plot observed non-numeric shares beside a full-group-normalised histogram."""
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
    cycle = plt.rcParams["axes.prop_cycle"].by_key().get("color", [])
    if not cycle:
        cycle = [f"C{i}" for i in range(len(OUTCOME_STATES))]
    component_colors = {
        component: cycle[index % len(cycle)]
        for index, component in enumerate(OUTCOME_STATES)
    }

    fig, (ax_admin, ax_grade) = plt.subplots(
        1, 2, figsize=(10.2, 6.2), sharey=True,
        gridspec_kw={"width_ratios": [1.7, 4.8], "wspace": 0.06},
    )
    hist_height = 0.78
    positions = np.arange(len(group_order), dtype=float)

    def group_share(group: str, state: str) -> float:
        key = (group, state)
        return float(share.loc[key]) if key in share.index else 0.0

    admin_totals = [
        100.0 * sum(group_share(group, state) for state in ["BV", "RT", "BA"])
        for group in group_order
    ]
    admin_limit = max(20.0, 5.0 * np.ceil((max(admin_totals) + 3.0) / 5.0))
    max_bin_percent = float(histogram["percent_of_full_group"].max())
    hist_scale_percent = max(5.0, 5.0 * np.ceil(max_bin_percent / 5.0))

    for position, group in zip(positions, group_order):
        left = 0.0
        for state in ["BV", "RT", "BA"]:
            width = 100.0 * group_share(group, state)
            ax_admin.barh(
                position, width, left=left, height=0.38,
                color=component_colors[state], edgecolor="white", linewidth=0.45,
            )
            if width >= 1.15:
                ax_admin.text(left + width / 2.0, position, f"{width:.1f}%",
                              ha="center", va="center", fontsize=6.4)
            elif width > 0:
                ax_admin.text(left + width / 2.0, position + 0.29, f"{width:.1f}%",
                              ha="center", va="bottom", fontsize=5.8)
            left += width
        ax_admin.text(
            min(left + 0.45, admin_limit - 0.25), position, f"{left:.1f}% total",
            ha="left" if left + 0.45 < admin_limit - 0.25 else "right",
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

    ax_admin.set_xlim(0.0, admin_limit)
    ax_admin.set_xticks(np.arange(0.0, admin_limit + 0.1, 5.0))
    ax_admin.set_xlabel("Non-numeric outcomes (% of full group)")
    ax_admin.set_ylabel("CMAT visits during the MU academic period")
    ax_admin.set_yticks(positions, group_order)
    ax_admin.set_title("Observed non-numeric records", fontsize=9.5)
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

    fig.legend(
        handles=[Patch(facecolor=component_colors[c], label=component_labels[c])
                 for c in ["pass", "numeric_nonpass", "BV", "RT", "BA"]],
        frameon=False, ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.01),
    )
    fig.subplots_adjust(top=0.88)
    return _save(fig, filename)


def plot_observed_pre_imputation_structure() -> Path:
    return _plot_observed_histogram_structure(
        histogram_path=TABLES_DIR / "10m_zero_inclusive_observed_numeric_grade_histogram.csv",
        composition_path=TABLES_DIR / "10d_zero_inclusive_exact_administrative_composition.csv",
        group_order=GROUPS,
        filename="fig01a_observed_pre_imputation_structure.pdf",
        grade_title="Observed numeric grades (0.1-point bins)",
    )


def plot_observed_pre_imputation_7plus_structure() -> Path:
    """Exploratory user-only view resolving six visits from the 7+ tail."""
    return _plot_observed_histogram_structure(
        histogram_path=TABLES_DIR / "25a_sensitivity_7plus_observed_numeric_grade_histogram.csv",
        composition_path=TABLES_DIR / "24a_sensitivity_7plus_exact_administrative_composition.csv",
        group_order=SENSITIVITY_GROUPS,
        filename="fig01b_observed_pre_imputation_1to6_7plus.pdf",
        grade_title="Users only: exact 1–6 visits and 7+ (0.1-point bins)",
    )


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
    component_labels = {
        "pass": "Pass",
        "numeric_nonpass": "Numeric <7.5",
        "BV": "BV",
        "RT": "RT",
        "BA": "BA",
    }
    cycle = plt.rcParams["axes.prop_cycle"].by_key().get("color", [])
    if not cycle:
        cycle = [f"C{i}" for i in range(len(OUTCOME_STATES))]
    component_colors = {
        component: cycle[index % len(cycle)]
        for index, component in enumerate(OUTCOME_STATES)
    }
    plot_stacked_ridgeline(
        density,
        group_order=GROUPS,
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

def _heatmap(
    path: Path,
    value_scale: float,
    label: str,
    filename: str,
    *,
    group_order: list[str],
) -> Path:
    d = pd.read_csv(path).copy()
    d["group"] = d["group"].astype(str)
    d = d.set_index("group")
    matrix = d[group_order].loc[group_order].astype(float).to_numpy() * value_scale
    vmax = float(np.nanmax(np.abs(matrix)))
    if not np.isfinite(vmax) or vmax == 0:
        vmax = 1.0

    fig, ax = plt.subplots(figsize=(6.7, 5.8))
    im = ax.imshow(matrix, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    ax.set_xticks(np.arange(len(group_order)), group_order)
    ax.set_yticks(np.arange(len(group_order)), group_order)
    ax.set_xlabel("Comparison group")
    ax.set_ylabel("Reference group")
    ax.grid(False)
    for i in range(len(group_order)):
        for j in range(len(group_order)):
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
        group_order=USER_GROUPS,
    )


def plot_pass_heatmap() -> Path:
    return _heatmap(
        TABLES_DIR / "19_primary_pass_heatmap_matrix.csv",
        100.0,
        "Adjusted difference in pass probability, percentage points (row minus column)",
        "fig03_pairwise_pass_heatmap.pdf",
        group_order=USER_GROUPS,
    )


def plot_zero_inclusive_z_heatmap() -> Path:
    return _heatmap(
        TABLES_DIR / "10j_zero_inclusive_z_heatmap_matrix.csv",
        1.0,
        "Adjusted difference in standardised grade (row minus column)",
        "figS01_zero_inclusive_z_heatmap.pdf",
        group_order=GROUPS,
    )


def plot_zero_inclusive_pass_heatmap() -> Path:
    return _heatmap(
        TABLES_DIR / "10k_zero_inclusive_pass_heatmap_matrix.csv",
        100.0,
        "Adjusted difference in pass probability, percentage points (row minus column)",
        "figS02_zero_inclusive_pass_heatmap.pdf",
        group_order=GROUPS,
    )


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
) -> Path:
    """Plot raw and Holm-adjusted pairwise p-values side by side."""
    matrices = []
    for path in [raw_path, holm_path]:
        frame = pd.read_csv(path).copy()
        frame["group"] = frame["group"].astype(str)
        matrix = (
            frame.set_index("group")[SENSITIVITY_GROUPS]
            .loc[SENSITIVITY_GROUPS]
            .astype(float)
            .to_numpy(copy=True)
        )
        np.fill_diagonal(matrix, np.nan)
        matrices.append(matrix)

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.2), sharex=True, sharey=True)
    norm = PowerNorm(gamma=0.35, vmin=0.0, vmax=1.0)
    image = None
    for ax, matrix, panel_title in zip(
        axes, matrices, ["Raw pairwise p-values", "Holm-adjusted p-values"]
    ):
        image = ax.imshow(matrix, cmap="viridis_r", norm=norm)
        ax.set_xticks(np.arange(len(SENSITIVITY_GROUPS)), SENSITIVITY_GROUPS)
        ax.set_yticks(np.arange(len(SENSITIVITY_GROUPS)), SENSITIVITY_GROUPS)
        ax.set_xlabel("Comparison group")
        ax.set_title(panel_title, fontsize=10)
        ax.grid(False)
        ax.axvline(1.5, linestyle="--", linewidth=1.0, color="white", alpha=0.9)
        ax.axhline(1.5, linestyle="--", linewidth=1.0, color="white", alpha=0.9)
        for i in range(len(SENSITIVITY_GROUPS)):
            for j in range(len(SENSITIVITY_GROUPS)):
                value = matrix[i, j]
                if not np.isfinite(value):
                    continue
                ax.text(
                    j, i, _format_pvalue(value), ha="center", va="center",
                    fontsize=7.4, fontweight="bold" if value < 0.05 else "normal",
                    color="black" if value < 0.35 else "white",
                )
        ax.text(
            1.5, -0.72, "PPA threshold", ha="center", va="bottom", fontsize=7,
            color="0.25", clip_on=False,
        )

    axes[0].set_ylabel("Reference group")
    fig.suptitle(
        f"{outcome_title}: exploratory pairwise comparison of 1, 2, 3, 4, 5, 6 and 7+ visits",
        fontsize=11, y=0.99,
    )
    fig.text(
        0.5, 0.015,
        "Dashed separator marks the institutional 3-visit PPA threshold. "
        "Bold cells have p < 0.05; raw p-values are descriptive and Holm controls family-wise multiplicity.",
        ha="center", va="bottom", fontsize=7.2, color="0.30",
    )
    if image is not None:
        cbar = fig.colorbar(image, ax=axes, shrink=0.82, pad=0.03)
        cbar.set_label("Pairwise p-value")
    fig.subplots_adjust(top=0.86, bottom=0.14, wspace=0.12)
    return _save(fig, filename)


def plot_sensitivity_z_pvalue_dashboard() -> Path:
    return _pvalue_dashboard(
        raw_path=TABLES_DIR / "22a_sensitivity_7plus_p_raw_continuous_matrix.csv",
        holm_path=TABLES_DIR / "22b_sensitivity_7plus_p_holm_continuous_matrix.csv",
        filename="fig06_sensitivity_7plus_z_pvalue_dashboard.pdf",
        outcome_title="Adjusted standardised MU grade",
    )


def plot_sensitivity_pass_pvalue_dashboard() -> Path:
    return _pvalue_dashboard(
        raw_path=TABLES_DIR / "23a_sensitivity_7plus_p_raw_pass_matrix.csv",
        holm_path=TABLES_DIR / "23b_sensitivity_7plus_p_holm_pass_matrix.csv",
        filename="fig07_sensitivity_7plus_pass_pvalue_dashboard.pdf",
        outcome_title="Adjusted pass probability",
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


def plot_complete_case_gmm_ridgeline() -> Path:
    density = pd.read_csv(TABLES_DIR / "46_complete_case_gmm_ridgeline_density.csv")
    params = pd.read_csv(TABLES_DIR / "38_complete_case_gmm_two_component_parameters.csv")
    density["group"] = density["group"].astype(str)
    params["group"] = params["group"].astype(str)

    fig, ax = plt.subplots(figsize=(9.2, 6.2))
    ridge_height = 0.76
    available_groups = [
        group
        for group in GROUPS
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
            x,
            observed_scaled,
            linewidth=1.15,
            color="0.25",
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

        lower = group_params.loc[
            group_params["component"].eq("lower_performance")
        ]
        higher = group_params.loc[
            group_params["component"].eq("higher_performance")
        ]
        if not lower.empty and not higher.empty:
            lo = lower.iloc[0]
            hi = higher.iloc[0]
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
                fontsize=7.5,
            )

    ax.set_xlim(-2, 2)
    ax.set_yticks(np.arange(len(available_groups)), available_groups)
    ax.set_ylim(-0.15, max(len(available_groups) - 0.05, 0.85))
    ax.set_xlabel("Instructor-period-standardised numeric final grade (complete case)")
    ax.set_ylabel("CMAT visits during the MU academic period")
    ax.grid(axis="y", visible=False)
    ax.legend(frameon=False, ncol=2, loc="lower center", bbox_to_anchor=(0.5, 1.01))
    return _save(fig, "fig04_complete_case_gmm_ridgeline.pdf")


def plot_lower_component_weight() -> Path:
    complete = pd.read_csv(
        TABLES_DIR / "38_complete_case_gmm_two_component_parameters.csv"
    )
    imputed = pd.read_csv(
        TABLES_DIR / "42_imputed_gmm_two_component_parameters.csv"
    )
    for frame in (complete, imputed):
        frame["group"] = frame["group"].astype(str)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    x = np.arange(len(GROUPS))
    for frame, label, linestyle in [
        (complete, "Numeric complete case", "-"),
        (imputed, "Imputed-outcome sensitivity", "--"),
    ]:
        lower = (
            frame.loc[frame["component"].eq("lower_performance"), ["group", "weight"]]
            .set_index("group")
            .reindex(GROUPS)
        )
        y = lower["weight"].to_numpy(float)
        ax.plot(x, y, marker="o", linestyle=linestyle, linewidth=1.4, label=label)

    ax.set_xticks(x, GROUPS)
    ax.set_ylim(0, 1)
    ax.set_xlabel("CMAT visits during the MU academic period")
    ax.set_ylabel(r"Estimated lower-component weight $\hat{\pi}_{L,k}$")
    ax.legend(frameon=False)
    ax.grid(axis="x", visible=False)
    return _save(fig, "fig05_lower_component_weight.pdf")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    validate()
    set_style()
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    for path in [
        plot_observed_pre_imputation_structure(),
        plot_observed_pre_imputation_7plus_structure(),
        plot_distribution_and_composition(),
        plot_z_heatmap(),
        plot_pass_heatmap(),
        plot_zero_inclusive_z_heatmap(),
        plot_zero_inclusive_pass_heatmap(),
        plot_complete_case_gmm_ridgeline(),
        plot_lower_component_weight(),
        plot_sensitivity_z_pvalue_dashboard(),
        plot_sensitivity_pass_pvalue_dashboard(),
    ]:
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
