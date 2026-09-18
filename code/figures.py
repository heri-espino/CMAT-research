#!/usr/bin/env python3
"""Generate Paper 2 publication figures from reviewed aggregate tables."""

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
        "Paper 2 figures require the shared editable library. Run:\n"
        '  python -m pip install -e "./cmat_analysis[dev]"'
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATED_TABLES_DIR = REPO_ROOT / "results" / "tables"
DEFAULT_FIGURES_DIR = REPO_ROOT / "results" / "figures"

GROUP_ORDER = ["0", "1", "2", "3", "4+"]
GROUP_LABELS = ["0", "1", "2", "3", "4+"]
OUTCOME_LABELS = {
    "primary_adverse_outcome_rule": "Primary",
    "uniform_adverse_imputation": "Uniform below-pass imputation",
    "numeric_complete_case": "Numeric grades only",
}


def validate_figure_inputs(table_dir: Path) -> None:
    """Validate aggregate tables required for the four primary figures."""
    required = [
        "02_mu_visit_distribution.csv",
        "30_exact_visit_groups_summary.csv",
        "33_exact_visit_groups_fe_pairwise.csv",
        "37_exact_visit_groups_outcome_sensitivity.csv",
    ]
    missing = [name for name in required if not (table_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(
            "Missing Paper 2 figure inputs: " + ", ".join(sorted(missing))
        )

    summary = pd.read_csv(table_dir / "30_exact_visit_groups_summary.csv")
    groups = set(summary["group"].astype(str))
    if not set(GROUP_ORDER).issubset(groups):
        raise ValueError(
            "Exact performance summary does not contain the expected 0/1/2/3/4+ groups."
        )


def _save_pdf(fig: plt.Figure, output_dir: Path, filename: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_mu_visit_distribution(table_dir: Path, output_dir: Path) -> Path:
    """Plot same-term CMAT visit intensity without emphasizing the PPA threshold."""
    d = pd.read_csv(table_dir / "02_mu_visit_distribution.csv").copy()
    exact: dict[int, float] = {}
    high = 0.0
    for row in d.itertuples(index=False):
        label = str(row.visits)
        prop = float(row.proportion)
        try:
            k = int(float(label))
        except ValueError:
            high += prop
            continue
        if k <= 5:
            exact[k] = exact.get(k, 0.0) + prop
        else:
            high += prop
    values = [exact.get(k, 0.0) for k in range(6)] + [high]
    labels = [str(k) for k in range(6)] + ["6+"]

    fig, ax = plt.subplots(figsize=(7.4, 4.7))
    x = np.arange(len(labels))
    ax.bar(x, values)
    ax.set_xticks(x, labels)
    ax.set_xlabel("CMAT visits during the MU academic period")
    ax.set_ylabel("Percentage of students")
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.set_ylim(0, max(values) * 1.12)
    return _save_pdf(fig, output_dir, "fig01_mu_visit_distribution.pdf")


def plot_performance_by_exact_visit_group(table_dir: Path, output_dir: Path) -> Path:
    """Plot mean classroom-relative performance for 0, 1, 2, 3, and 4+ visits."""
    d = pd.read_csv(table_dir / "30_exact_visit_groups_summary.csv").copy()
    d["group"] = pd.Categorical(d["group"].astype(str), GROUP_ORDER, ordered=True)
    d = d.sort_values("group")
    x = np.arange(len(d))
    means = d["mean_z"].to_numpy(float)
    lows = d["ci95_low"].to_numpy(float)
    highs = d["ci95_high"].to_numpy(float)

    fig, ax = plt.subplots(figsize=(7.4, 4.7))
    ax.errorbar(
        x,
        means,
        yerr=np.vstack([means - lows, highs - means]),
        fmt="o",
        capsize=4,
        linewidth=1.3,
    )
    ax.axhline(0, linestyle="--", linewidth=1.0)
    ax.set_xticks(x, GROUP_LABELS)
    ax.set_xlabel("CMAT visits during the MU academic period")
    ax.set_ylabel("Mean within-class standardised grade (Z), 95% CI")
    for xpos, row in zip(x, d.itertuples(index=False)):
        ax.annotate(
            f"n={int(row.n):,}",
            (xpos, float(row.mean_z)),
            xytext=(8, 14),
            textcoords="offset points",
            ha="left",
            va="bottom",
            fontsize=8,
            arrowprops={
                "arrowstyle": "-",
                "color": "0.35",
                "linewidth": 0.7,
                "shrinkA": 0,
                "shrinkB": 2,
            },
        )
    return _save_pdf(fig, output_dir, "fig02_mu_performance_by_visit_group.pdf")


def plot_exact_group_fe_contrasts(table_dir: Path, output_dir: Path) -> Path:
    """Plot adjusted exact-group contrasts relative to zero visits."""
    d = pd.read_csv(table_dir / "33_exact_visit_groups_fe_pairwise.csv").copy()
    d["group1"] = d["group1"].astype(str)
    d["group2"] = d["group2"].astype(str)
    d = d.loc[(d["group1"] == "0") & d["group2"].isin(GROUP_ORDER[1:])].copy()
    d["group2"] = pd.Categorical(d["group2"], GROUP_ORDER[1:], ordered=True)
    d = d.sort_values("group2")

    estimates = -d["adjusted_mean_difference_group1_minus_group2"].to_numpy(float)
    lows = -d["ci95_high"].to_numpy(float)
    highs = -d["ci95_low"].to_numpy(float)
    y = np.arange(len(d))

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.errorbar(
        estimates,
        y,
        xerr=np.vstack([estimates - lows, highs - estimates]),
        fmt="o",
        capsize=4,
        linewidth=1.3,
    )
    ax.axvline(0, linestyle="--", linewidth=1.0)
    ax.set_yticks(
        y,
        [f"{g} visit" if g == "1" else f"{g} visits" for g in d["group2"].astype(str)],
    )
    ax.set_xlabel("Adjusted difference in standardised grade versus 0 visits (Z)")
    ax.set_ylabel("CMAT visits during the MU academic period")
    ax.invert_yaxis()
    return _save_pdf(fig, output_dir, "fig03_adjusted_dose_coefficients.pdf")


def plot_outcome_sensitivity(table_dir: Path, output_dir: Path) -> Path:
    """Plot the exact-group pattern under three outcome constructions."""
    d = pd.read_csv(table_dir / "37_exact_visit_groups_outcome_sensitivity.csv").copy()
    d["group"] = pd.Categorical(d["group"].astype(str), GROUP_ORDER, ordered=True)
    x = np.arange(len(GROUP_ORDER), dtype=float)
    offsets = np.linspace(-0.12, 0.12, num=3)

    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    for offset, outcome in zip(offsets, OUTCOME_LABELS):
        sub = d.loc[d["outcome_definition"] == outcome].sort_values("group")
        means = sub["mean_z"].to_numpy(float)
        lows = sub["ci95_low"].to_numpy(float)
        highs = sub["ci95_high"].to_numpy(float)
        ax.errorbar(
            x + offset,
            means,
            yerr=np.vstack([means - lows, highs - means]),
            fmt="o",
            capsize=3,
            linewidth=1.0,
            markersize=4,
            label=OUTCOME_LABELS[outcome],
        )

    ax.axhline(0, linestyle="--", linewidth=1.0)
    ax.set_xticks(x, GROUP_LABELS)
    ax.set_xlabel("Same-term CMAT registrations in MU")
    ax.set_ylabel("Mean classroom-relative performance (Z), 95% CI")
    ax.legend(frameon=False)
    return _save_pdf(fig, output_dir, "fig04_outcome_sensitivity.pdf")


def generate_paper_figures(
    table_dir: Path = GENERATED_TABLES_DIR,
    output_dir: Path = DEFAULT_FIGURES_DIR,
) -> list[Path]:
    """Generate all four Paper 2 figures as vector PDFs."""
    validate_figure_inputs(table_dir)
    set_style()
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    return [
        plot_mu_visit_distribution(table_dir, output_dir),
        plot_performance_by_exact_visit_group(table_dir, output_dir),
        plot_exact_group_fe_contrasts(table_dir, output_dir),
        plot_outcome_sensitivity(table_dir, output_dir),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Paper 2 vector PDF figures.")
    parser.add_argument("--table-dir", type=Path, default=GENERATED_TABLES_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_FIGURES_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = generate_paper_figures(args.table_dir.resolve(), args.output_dir.resolve())
    for path in paths:
        print(path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
