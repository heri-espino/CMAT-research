#!/usr/bin/env python3
"""Generate publication figures for Paper 1 from aggregate analysis tables.

The module contains presentation-only logic. It reads aggregate outputs already
produced by the shared scientific library and does not redefine cohorts,
thresholds, estimands, confidence intervals, or statistical models.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

from cmat_analysis.visualization import set_style


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_TABLES_DIR = REPO_ROOT / "results" / "tables"
RESULTS_FIGURES_DIR = REPO_ROOT / "results" / "figures"
RETAINED_TABLES_DIR = (
    REPO_ROOT / "brainstorm" / "shared" / "historical_outputs" / "study" / "tables"
)

FIGURE_FILES = (
    "figure_01_cohort_flow.png",
    "figure_02_main_persistence.png",
    "figure_03_threshold_piecewise.png",
    "figure_04_adjusted_persistence_or.png",
)

REQUIRED_COLUMNS: dict[str, set[str]] = {
    "98_ppa_progression_cohort_flow.csv": {"stage", "n"},
    "102_ppa_persistence_by_mu_group.csv": {
        "mu_visit_group",
        "n",
        "p_calc_any_visit",
        "ci95_low_wilson",
        "ci95_high_wilson",
    },
    "105_ppa_persistence_logistic_models.csv": {
        "model",
        "term",
        "odds_ratio",
        "or_ci95_low",
        "or_ci95_high",
    },
    "106_ppa_piecewise_threshold_persistence.csv": {
        "term",
        "odds_ratio_per_one_visit",
        "or_ci95_low",
        "or_ci95_high",
    },
}


def validate_figure_inputs(table_dir: Path) -> None:
    """Validate the aggregate tables required by the Paper 1 figures.

    Parameters
    ----------
    table_dir : pathlib.Path
        Directory containing Paper 1 aggregate CSV tables.

    Raises
    ------
    FileNotFoundError
        If one of the required aggregate tables is absent.
    ValueError
        If a required table does not contain the expected columns.
    """
    for filename, required in REQUIRED_COLUMNS.items():
        path = table_dir / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing Paper 1 figure input: {path}")
        columns = set(pd.read_csv(path, nrows=0).columns)
        missing = required.difference(columns)
        if missing:
            raise ValueError(
                f"{filename} is missing required columns: {', '.join(sorted(missing))}"
            )


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _plot_cohort_flow(flow: pd.DataFrame, path: Path) -> None:
    labels = {
        "first observed MU attempt (real-attempt candidate)": "First real observed MU attempt",
        "first MU attempt is numeric pass >= 7.5": "Numeric passing first MU attempt (grade ≥ 7.5)",
        "first later Calculus I real-attempt candidate exists": "Subsequent first Calculus I attempt observed",
        "later Calculus I has numeric final grade": "Calculus I attempt with numeric final grade",
        "paired MU/Calculus with CMAT coverage and classroom Z in both": "CMAT coverage and classroom-relative Z in both courses",
        "primary PPA progression cohort: next regular term": "Primary cohort: Calculus I in the next regular term",
    }
    d = flow.copy()
    d["display"] = d["stage"].map(labels).fillna(d["stage"].astype(str))

    set_style()
    fig, ax = plt.subplots(figsize=(7.2, 6.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    y_positions = np.linspace(0.91, 0.09, len(d))
    for i, (y, row) in enumerate(zip(y_positions, d.itertuples(index=False))):
        ax.text(
            0.5,
            y,
            f"{row.display}\nN = {int(row.n):,}",
            ha="center",
            va="center",
            fontsize=10,
            bbox={"boxstyle": "round,pad=0.45", "facecolor": "white", "edgecolor": "0.35"},
        )
        if i < len(y_positions) - 1:
            ax.annotate(
                "",
                xy=(0.5, y_positions[i + 1] + 0.055),
                xytext=(0.5, y - 0.055),
                arrowprops={"arrowstyle": "->", "linewidth": 1.0, "color": "0.35"},
            )
    _save(fig, path)


def _plot_main_persistence(summary: pd.DataFrame, path: Path) -> None:
    order = ["0", "1-2", "3", "4+"]
    labels = ["0", "1–2", "3", "4+"]
    d = summary.copy()
    d["mu_visit_group"] = d["mu_visit_group"].astype(str)
    d = d.set_index("mu_visit_group").reindex(order).reset_index()

    y = d["p_calc_any_visit"].to_numpy(float)
    lo = d["ci95_low_wilson"].to_numpy(float)
    hi = d["ci95_high_wilson"].to_numpy(float)
    x = np.arange(len(d))

    set_style()
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.errorbar(x, y, yerr=[y - lo, hi - y], marker="o", capsize=4, linewidth=1.5)
    ax.set_xticks(x, labels)
    ax.set_ylim(0, min(1.0, float(np.nanmax(hi)) + 0.12))
    ax.set_xlabel("CMAT visits during University Mathematics (MU)")
    ax.set_ylabel("Probability of any CMAT use in Calculus I")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(axis="y", alpha=0.2)
    for i, row in d.iterrows():
        ax.annotate(
            f"N={int(row['n']):,}",
            (i, float(row["p_calc_any_visit"])),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=8.5,
        )
    _save(fig, path)


def _plot_threshold_piecewise(piecewise: pd.DataFrame, path: Path) -> None:
    term_order = ["VISITS_TO_THRESHOLD", "VISITS_AFTER_THRESHOLD"]
    labels = {
        "VISITS_TO_THRESHOLD": "Through 3 visits",
        "VISITS_AFTER_THRESHOLD": "After 3 visits",
    }
    d = piecewise.set_index("term").reindex(term_order).reset_index()
    x = d["odds_ratio_per_one_visit"].to_numpy(float)
    lo = d["or_ci95_low"].to_numpy(float)
    hi = d["or_ci95_high"].to_numpy(float)
    y = np.arange(len(d))[::-1]

    set_style()
    fig, ax = plt.subplots(figsize=(7.2, 3.7))
    ax.errorbar(
        x,
        y,
        xerr=[x - lo, hi - x],
        fmt="o",
        capsize=4,
        linewidth=1.5,
    )
    ax.axvline(1.0, linestyle="--", linewidth=1.0)
    ax.set_yticks(y, [labels[t] for t in d["term"]])
    ax.set_xscale("log")
    ax.set_xlabel("Odds ratio per additional MU visit")
    ax.xaxis.set_major_formatter(mtick.ScalarFormatter())
    ax.grid(axis="x", alpha=0.2)
    _save(fig, path)


def _visit_group_label(term: str) -> str | None:
    if "[T.1-2]" in term:
        return "1–2 visits vs 0"
    if "[T.3]" in term:
        return "3 visits vs 0"
    if "[T.4+]" in term:
        return "4+ visits vs 0"
    return None


def _plot_adjusted_odds_ratios(models: pd.DataFrame, path: Path) -> None:
    d = models.loc[
        models["model"].eq("adjusted_prior_performance_major_term_logit")
        & models["term"].str.contains("MU_VISIT_GROUP", regex=False)
    ].copy()
    d["label"] = d["term"].map(_visit_group_label)
    d = d.dropna(subset=["label"])
    order = ["1–2 visits vs 0", "3 visits vs 0", "4+ visits vs 0"]
    d["label"] = pd.Categorical(d["label"], categories=order, ordered=True)
    d = d.sort_values("label")

    x = d["odds_ratio"].to_numpy(float)
    lo = d["or_ci95_low"].to_numpy(float)
    hi = d["or_ci95_high"].to_numpy(float)
    y = np.arange(len(d))[::-1]

    set_style()
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.errorbar(
        x,
        y,
        xerr=[x - lo, hi - x],
        fmt="o",
        capsize=4,
        linewidth=1.5,
    )
    ax.axvline(1.0, linestyle="--", linewidth=1.0)
    ax.set_yticks(y, d["label"].astype(str))
    ax.set_xscale("log")
    ax.set_xlabel("Adjusted odds ratio for any CMAT use in Calculus I")
    ax.xaxis.set_major_formatter(mtick.ScalarFormatter())
    ax.grid(axis="x", alpha=0.2)
    _save(fig, path)


def generate_paper_figures(table_dir: Path, figure_dir: Path = RESULTS_FIGURES_DIR) -> list[Path]:
    """Generate the four manuscript figures from Paper 1 aggregate tables.

    Parameters
    ----------
    table_dir : pathlib.Path
        Directory containing aggregate Paper 1 tables 98, 102, 105, and 106.
    figure_dir : pathlib.Path, optional
        Output directory for publication figures.

    Returns
    -------
    list[pathlib.Path]
        Paths of the four generated PNG figures in manuscript order.
    """
    validate_figure_inputs(table_dir)
    figure_dir.mkdir(parents=True, exist_ok=True)

    flow = pd.read_csv(table_dir / "98_ppa_progression_cohort_flow.csv")
    persistence = pd.read_csv(table_dir / "102_ppa_persistence_by_mu_group.csv")
    models = pd.read_csv(table_dir / "105_ppa_persistence_logistic_models.csv")
    piecewise = pd.read_csv(table_dir / "106_ppa_piecewise_threshold_persistence.csv")

    paths = [figure_dir / name for name in FIGURE_FILES]
    _plot_cohort_flow(flow, paths[0])
    _plot_main_persistence(persistence, paths[1])
    _plot_threshold_piecewise(piecewise, paths[2])
    _plot_adjusted_odds_ratios(models, paths[3])
    return paths


def _resolve_source(source: str) -> Path:
    if source == "retained":
        return RETAINED_TABLES_DIR
    if source == "generated":
        return RESULTS_TABLES_DIR
    if all((RESULTS_TABLES_DIR / filename).is_file() for filename in REQUIRED_COLUMNS):
        return RESULTS_TABLES_DIR
    return RETAINED_TABLES_DIR


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate English publication figures for Paper 1 from aggregate tables."
    )
    parser.add_argument(
        "--source",
        choices=("auto", "retained", "generated"),
        default="auto",
        help="Aggregate-table source. 'auto' prefers generated results when complete.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    table_dir = _resolve_source(args.source)
    paths = generate_paper_figures(table_dir)
    print(f"Paper 1 figure source: {table_dir.relative_to(REPO_ROOT)}")
    for path in paths:
        print(f"Generated: {path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
