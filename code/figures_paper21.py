#!/usr/bin/env python3
"""Generate Paper 2.1 publication figures from aggregate analysis outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
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
        "10d_zero_inclusive_exact_administrative_composition.csv",
        "10l_zero_inclusive_observed_numeric_grade_density.csv",
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

def plot_distribution_and_composition() -> Path:
    """Plot the observed, pre-imputation outcome composition by visit group.

    Administrative outcomes are shown as shares of the full attendance group.
    The ridgelines use only observed numeric grades on their original 0--10
    scale; no numeric value is assigned to BV, RT, or BA.
    """
    density = pd.read_csv(
        TABLES_DIR / "10l_zero_inclusive_observed_numeric_grade_density.csv"
    )
    composition = pd.read_csv(
        TABLES_DIR / "10d_zero_inclusive_exact_administrative_composition.csv"
    )
    density["group"] = density["group"].astype(str)
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
        1,
        2,
        figsize=(10.2, 6.2),
        sharey=True,
        gridspec_kw={"width_ratios": [1.7, 4.8], "wspace": 0.06},
    )
    ridge_height = 0.78
    positions = np.arange(len(GROUPS), dtype=float)

    def group_share(group: str, state: str) -> float:
        key = (group, state)
        return float(share.loc[key]) if key in share.index else 0.0

    admin_totals = [
        100.0 * sum(group_share(group, state) for state in ["BV", "RT", "BA"])
        for group in GROUPS
    ]
    admin_limit = max(20.0, 5.0 * np.ceil((max(admin_totals) + 3.0) / 5.0))

    for position, group in zip(positions, GROUPS):
        left = 0.0
        for state in ["BV", "RT", "BA"]:
            width = 100.0 * group_share(group, state)
            ax_admin.barh(
                position,
                width,
                left=left,
                height=0.38,
                color=component_colors[state],
                edgecolor="white",
                linewidth=0.45,
            )
            if width >= 1.15:
                ax_admin.text(
                    left + width / 2.0,
                    position,
                    f"{width:.1f}%",
                    ha="center",
                    va="center",
                    fontsize=6.4,
                )
            elif width > 0:
                ax_admin.text(
                    left + width / 2.0,
                    position + 0.29,
                    f"{width:.1f}%",
                    ha="center",
                    va="bottom",
                    fontsize=5.8,
                )
            left += width
        ax_admin.text(
            min(left + 0.45, admin_limit - 0.25),
            position,
            f"{left:.1f}% total",
            ha="left" if left + 0.45 < admin_limit - 0.25 else "right",
            va="center",
            fontsize=6.5,
            color="0.25",
        )

        observed = (
            density.loc[density["group"].eq(group)]
            .drop_duplicates("x")
            .sort_values("x")
        )
        if observed.empty:
            continue
        x = observed["x"].to_numpy(float)
        y = observed["density_total"].to_numpy(float)
        scale = float(np.nanmax(y))
        if not np.isfinite(scale) or scale <= 0:
            continue
        ridge = position + ridge_height * y / scale

        ax_grade.fill_between(
            x,
            position,
            ridge,
            where=x < 7.5,
            interpolate=True,
            color=component_colors["numeric_nonpass"],
            alpha=0.88,
        )
        ax_grade.fill_between(
            x,
            position,
            ridge,
            where=x >= 7.5,
            interpolate=True,
            color=component_colors["pass"],
            alpha=0.94,
        )
        ax_grade.plot(x, ridge, linewidth=0.95, color="0.20")
        ax_grade.hlines(position, 0.0, 10.0, linewidth=0.55, color="0.35")

        fail_share = 100.0 * group_share(group, "numeric_grade_below_7.5")
        pass_share = 100.0 * group_share(group, "pass")
        ax_grade.text(
            5.6,
            position + 0.11,
            f"{fail_share:.1f}% total",
            ha="right",
            va="bottom",
            fontsize=6.5,
            color=component_colors["numeric_nonpass"],
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.72, "pad": 0.8},
        )
        ax_grade.text(
            9.72,
            position + 0.11,
            f"{pass_share:.1f}% total",
            ha="right",
            va="bottom",
            fontsize=6.5,
            color=component_colors["pass"],
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.72, "pad": 0.8},
        )

    ax_admin.set_xlim(0.0, admin_limit)
    ax_admin.set_xticks(np.arange(0.0, admin_limit + 0.1, 5.0))
    ax_admin.set_xlabel("Non-numeric outcomes (% of full group)")
    ax_admin.set_ylabel("CMAT visits during the MU academic period")
    ax_admin.set_yticks(positions, GROUPS)
    ax_admin.set_title("Observed non-numeric records", fontsize=9.5)
    ax_admin.grid(axis="y", visible=False)

    ax_grade.axvline(7.5, linestyle="--", linewidth=0.9, color="0.35", alpha=0.85)
    ax_grade.text(
        7.5,
        len(GROUPS) - 0.05,
        "pass mark 7.5",
        rotation=90,
        ha="right",
        va="top",
        fontsize=7,
        color="0.35",
    )
    ax_grade.set_xlim(0.0, 10.0)
    ax_grade.set_xlabel("Observed numeric MU final grade")
    ax_grade.set_title("Empirical numeric-grade distribution", fontsize=9.5)
    ax_grade.grid(axis="y", visible=False)
    ax_grade.tick_params(axis="y", left=False, labelleft=False)

    fig.legend(
        handles=[
            Patch(
                facecolor=component_colors[component],
                label=component_labels[component],
            )
            for component in ["pass", "numeric_nonpass", "BV", "RT", "BA"]
        ],
        frameon=False,
        ncol=5,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.01),
    )
    fig.subplots_adjust(top=0.88)
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
        plot_distribution_and_composition(),
        plot_z_heatmap(),
        plot_pass_heatmap(),
        plot_zero_inclusive_z_heatmap(),
        plot_zero_inclusive_pass_heatmap(),
        plot_complete_case_gmm_ridgeline(),
        plot_lower_component_weight(),
    ]:
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
