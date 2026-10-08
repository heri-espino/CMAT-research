#!/usr/bin/env python3
"""Generate vector figures from Paper 2.2.1 exported aggregate tables."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "paper221" / "tables"
FIGURES = ROOT / "results" / "paper221" / "figures"


def render(prefix: str) -> None:
    cv = pd.read_csv(TABLES / f"{prefix}_cv.csv")
    levels = pd.read_csv(TABLES / f"{prefix}_fusion_levels.csv")
    stability = pd.read_csv(TABLES / f"{prefix}_boundary_stability.csv")
    FIGURES.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    ax.plot(np.arange(len(cv)), cv["cv_mse"], marker="o")
    idx = int(np.flatnonzero(cv["selected_lambda"].astype(bool))[0])
    ax.axvline(idx, linestyle="--", linewidth=1, color="gray")
    ax.set_xticks(np.arange(len(cv))[::max(1, len(cv)//6)])
    ax.set_xticklabels([f"{cv.iloc[j]['lambda']:.2g}"
                        for j in np.arange(len(cv))[::max(1, len(cv)//6)]])
    ax.set_xlabel("Fusion penalty lambda")
    ax.set_ylabel("Held-out within-classroom MSE")
    ax.set_title(f"Penalty selection: {prefix}")
    fig.tight_layout()
    fig.savefig(FIGURES / f"{prefix}_cv.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    ax.step(np.arange(len(levels)),
            levels["adjusted_level_relative_zero_shrunken"], where="mid")
    ax.scatter(np.arange(len(levels)),
               levels["adjusted_level_relative_zero_shrunken"])
    ax.set_xticks(np.arange(len(levels)))
    ax.set_xticklabels(levels["group"].astype(str))
    ax.set_ylabel("Penalised relative level (not an inferential CI)")
    ax.set_xlabel("Number of CMAT visits (7+ is pooled)")
    ax.set_title(f"Discovery fusion: {prefix}")
    fig.tight_layout()
    fig.savefig(FIGURES / f"{prefix}_fused_levels.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    frequency = stability["selection_frequency"].to_numpy(float)
    ax.bar(np.arange(len(stability)), frequency)
    ax.set_xticks(np.arange(len(stability)))
    ax.set_xticklabels(stability["boundary"].astype(str))
    ax.set_ylim(0, 1)
    ax.set_ylabel("Cluster bootstrap selection frequency")
    ax.set_title(f"Boundary stability: {prefix}")
    fig.tight_layout()
    fig.savefig(FIGURES / f"{prefix}_boundary_stability.pdf")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if args.check:
        print("Paper 2.2.1 figure runner import/layout: OK; no outputs checked")
        return
    paths = sorted(TABLES.glob("*_fusion_levels.csv"))
    if not paths:
        raise SystemExit("No Paper 2.2.1 aggregate tables; run code/run_paper221_fused.py first")
    for path in paths:
        prefix = path.name.removesuffix("_fusion_levels.csv")
        render(prefix)
        print("Created vector figures for", prefix)


if __name__ == "__main__":
    main()
