#!/usr/bin/env python3
"""Generate Paper 2 publication figures from retained or freshly generated tables."""

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
RETAINED_TABLES_DIR = (
    REPO_ROOT / "brainstorm" / "shared" / "historical_outputs" / "study" / "tables"
)
GENERATED_TABLES_DIR = REPO_ROOT / "results" / "tables"
DEFAULT_FIGURES_DIR = REPO_ROOT / "results" / "figures"

GROUP_ORDER = ["0", "1-2", "3", "4+"]
GROUP_LABELS = ["0", "1–2", "3", "4+"]


def _distribution_filename(source: str) -> str:
    return (
        "02_visit_distribution_mu_vs_calculus.csv"
        if source == "retained"
        else "02_mu_visit_distribution.csv"
    )


def validate_figure_inputs(table_dir: Path, *, source: str) -> None:
    """Validate the aggregate tables required for the four Paper 2 figures."""
    required = [
        _distribution_filename(source),
        "10_primary_outcome_by_visit_group.csv",
        "11_primary_robust_gt3_vs_le3.csv",
        "13_primary_dose_group_model.csv",
        "14_continuous_outcome_sensitivity.csv",
    ]
    missing = [name for name in required if not (table_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(
            "Missing Paper 2 figure inputs: " + ", ".join(sorted(missing))
        )

    summary = pd.read_csv(table_dir / "10_primary_outcome_by_visit_group.csv")
    groups = set(summary["group"].astype(str))
    if not set(GROUP_ORDER).issubset(groups):
        raise ValueError(
            "Performance summary does not contain the expected 0/1-2/3/4+ groups."
        )


def _save_pdf(fig: plt.Figure, output_dir: Path, filename: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def _mu_distribution(table_dir: Path, source: str) -> pd.DataFrame:
    d = pd.read_csv(table_dir / _distribution_filename(source)).copy()
    if "course" in d.columns:
        d = d.loc[d["course"] == "Matemáticas Universitarias"].copy()
    return d


def plot_mu_visit_distribution(table_dir: Path, output_dir: Path, source: str) -> Path:
    """Plot same-term CMAT visit intensity in the first-MU analytical cohort."""
    d = _mu_distribution(table_dir, source)
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
    ax.axvline(2.5, linestyle="--", linewidth=1.1, label="PPA threshold = 3 visits")
    ax.set_xlabel("CMAT registrations during the same MU term")
    ax.set_ylabel("Students")
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.set_ylim(0, max(values) * 1.12)
    ax.legend(frameon=False)
    return _save_pdf(fig, output_dir, "fig01_mu_visit_distribution.pdf")


def plot_performance_by_visit_group(table_dir: Path, output_dir: Path) -> Path:
    """Plot classroom-relative mean performance and 95% intervals by visit group."""
    d = pd.read_csv(table_dir / "10_primary_outcome_by_visit_group.csv")
    d["group"] = pd.Categorical(d["group"], GROUP_ORDER, ordered=True)
    d = d.sort_values("group")
    x = np.arange(len(d))
    means = d["mean"].to_numpy(float)
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
    ax.set_xlabel("Same-term CMAT registrations in MU")
    ax.set_ylabel("Mean classroom-relative performance (Z), 95% CI")
    for xpos, row in zip(x, d.itertuples(index=False)):
        ax.annotate(
            f"n={int(row.n):,}",
            (xpos, float(row.mean)),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=8,
        )
    return _save_pdf(fig, output_dir, "fig02_mu_performance_by_visit_group.pdf")


def plot_adjusted_dose_coefficients(table_dir: Path, output_dir: Path) -> Path:
    """Plot classroom fixed-effect visit-group contrasts relative to zero visits."""
    d = pd.read_csv(table_dir / "13_primary_dose_group_model.csv").copy()
    label_map = {
        "T.1-2": "1–2 visits",
        "T.3]": "3 visits",
        "T.4+": "4+ visits",
    }
    rows: list[dict[str, object]] = []
    for row in d.itertuples(index=False):
        term = str(row.term)
        label = next((v for k, v in label_map.items() if k in term), term)
        rows.append(
            {
                "label": label,
                "estimate": float(row.estimate),
                "low": float(row.ci95_low),
                "high": float(row.ci95_high),
            }
        )
    order = {"1–2 visits": 0, "3 visits": 1, "4+ visits": 2}
    rows.sort(key=lambda r: order.get(str(r["label"]), 99))
    y = np.arange(len(rows))
    est = np.array([float(r["estimate"]) for r in rows])
    low = np.array([float(r["low"]) for r in rows])
    high = np.array([float(r["high"]) for r in rows])

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.errorbar(
        est,
        y,
        xerr=np.vstack([est - low, high - est]),
        fmt="o",
        capsize=4,
        linewidth=1.3,
    )
    ax.axvline(0, linestyle="--", linewidth=1.0)
    ax.set_yticks(y, [str(r["label"]) for r in rows])
    ax.set_xlabel("Difference in classroom-relative performance versus 0 visits (Z)")
    ax.set_ylabel("MU visit group")
    ax.invert_yaxis()
    return _save_pdf(fig, output_dir, "fig03_adjusted_dose_coefficients.pdf")


def plot_outcome_sensitivity(table_dir: Path, output_dir: Path) -> Path:
    """Plot threshold-contrast estimates under alternative outcome constructions."""
    primary = pd.read_csv(table_dir / "11_primary_robust_gt3_vs_le3.csv").iloc[0]
    sensitivity = pd.read_csv(table_dir / "14_continuous_outcome_sensitivity.csv")
    entries = [
        (
            "Primary adverse-outcome imputation",
            float(primary["mean_diff"]),
            float(primary["mean_diff_ci95_low"]),
            float(primary["mean_diff_ci95_high"]),
        )
    ]
    names = {
        "Z_GRADE_UNIFORM_SENS": "Uniform adverse-outcome imputation",
        "Z_GRADE_COMPLETE_CASE": "Complete cases",
    }
    for row in sensitivity.itertuples(index=False):
        entries.append(
            (
                names.get(str(row.outcome), str(row.outcome)),
                float(row.mean_diff),
                float(row.mean_diff_ci95_low),
                float(row.mean_diff_ci95_high),
            )
        )

    y = np.arange(len(entries))
    est = np.array([x[1] for x in entries])
    low = np.array([x[2] for x in entries])
    high = np.array([x[3] for x in entries])
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax.errorbar(
        est,
        y,
        xerr=np.vstack([est - low, high - est]),
        fmt="o",
        capsize=4,
        linewidth=1.3,
    )
    ax.axvline(0, linestyle="--", linewidth=1.0)
    ax.set_yticks(y, [x[0] for x in entries])
    ax.set_xlabel("Mean difference: >3 versus ≤3 CMAT visits (Z), 95% CI")
    ax.invert_yaxis()
    return _save_pdf(fig, output_dir, "fig04_outcome_sensitivity.pdf")


def generate_paper_figures(
    table_dir: Path,
    output_dir: Path = DEFAULT_FIGURES_DIR,
    *,
    source: str,
) -> list[Path]:
    """Generate all Paper 2 figures as vector PDFs."""
    validate_figure_inputs(table_dir, source=source)
    set_style()
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    return [
        plot_mu_visit_distribution(table_dir, output_dir, source),
        plot_performance_by_visit_group(table_dir, output_dir),
        plot_adjusted_dose_coefficients(table_dir, output_dir),
        plot_outcome_sensitivity(table_dir, output_dir),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Paper 2 vector PDF figures.")
    parser.add_argument(
        "--source",
        choices=("retained", "generated"),
        default="retained",
        help="Use the retained aggregate snapshot or freshly regenerated Paper 2 tables.",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_FIGURES_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    table_dir = RETAINED_TABLES_DIR if args.source == "retained" else GENERATED_TABLES_DIR
    paths = generate_paper_figures(
        table_dir,
        args.output_dir.resolve(),
        source=args.source,
    )
    for path in paths:
        print(path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
