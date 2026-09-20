"""Reusable stacked ridgeline visualization for outcome distributions."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Patch
import numpy as np
import pandas as pd


def plot_stacked_ridgeline(
    density: pd.DataFrame,
    *,
    group_order: Sequence[str],
    component_order: Sequence[str],
    summary: pd.DataFrame | None = None,
    colors: Mapping[str, str] | None = None,
    component_labels: Mapping[str, str] | None = None,
    ridge_height: float = 0.82,
    ax: Axes | None = None,
) -> Axes:
    """Plot horizontally oriented stacked component densities by group.

    Parameters
    ----------
    density : pandas.DataFrame
        Long-format output from the mixture-component density helper.
    group_order : sequence of str
        Group labels in bottom-to-top order.
    component_order : sequence of str
        Component stacking order.
    summary : pandas.DataFrame or None, default=None
        Optional group-level table containing group, outcome_mean,
        outcome_ci95_low, and outcome_ci95_high.
    colors : mapping or None, default=None
        Optional component-to-color mapping. The active Matplotlib color cycle
        is used when omitted.
    component_labels : mapping or None, default=None
        Optional display labels for the legend.
    ridge_height : float, default=0.82
        Maximum normalized vertical height of each ridge.
    ax : matplotlib.axes.Axes or None, default=None
        Existing axes. A new axes is created when omitted.

    Returns
    -------
    matplotlib.axes.Axes
        Axes containing the stacked ridgeline plot.

    Notes
    -----
    Component areas encode observed group shares before the purely visual
    ridge-height normalization. Means and confidence intervals, when supplied,
    are horizontal because the continuous outcome is on the x-axis.
    """
    required = {"group", "component", "x", "density_component", "density_total"}
    missing = sorted(required.difference(density.columns))
    if missing:
        raise KeyError(f"Missing ridgeline density columns: {missing}")
    if ridge_height <= 0:
        raise ValueError("ridge_height must be positive")

    groups = [str(value) for value in group_order]
    components = [str(value) for value in component_order]
    if ax is None:
        _, ax = plt.subplots(figsize=(8.2, 5.8))

    if colors is None:
        cycle = plt.rcParams["axes.prop_cycle"].by_key().get("color", [])
        if not cycle:
            cycle = [f"C{i}" for i in range(len(components))]
        color_map = {
            component: cycle[index % len(cycle)]
            for index, component in enumerate(components)
        }
    else:
        color_map = {component: colors[component] for component in components}

    work = density.copy()
    work["group"] = work["group"].astype(str)
    work["component"] = work["component"].astype(str)

    for y, group in enumerate(groups):
        subset = work.loc[work["group"].eq(group)]
        if subset.empty:
            continue
        x_values = np.sort(subset["x"].unique().astype(float))
        total = (
            subset.drop_duplicates("x")
            .set_index("x")
            .reindex(x_values)["density_total"]
            .to_numpy(float)
        )
        maximum = float(np.nanmax(total))
        scale = ridge_height / maximum if np.isfinite(maximum) and maximum > 0 else 1.0
        cumulative = np.zeros_like(x_values)

        for component in components:
            frame = (
                subset.loc[
                    subset["component"].eq(component),
                    ["x", "density_component"],
                ]
                .set_index("x")
                .reindex(x_values)
            )
            values = frame["density_component"].fillna(0.0).to_numpy(float)
            lower = y + cumulative * scale
            cumulative = cumulative + values
            upper = y + cumulative * scale
            ax.fill_between(
                x_values,
                lower,
                upper,
                color=color_map[component],
                linewidth=0,
                alpha=0.96,
            )

        ax.plot(
            x_values,
            y + total * scale,
            color="0.18",
            linewidth=0.9,
            zorder=4,
        )
        ax.hlines(y, x_values.min(), x_values.max(), color="0.78", linewidth=0.45)

    if summary is not None:
        needed = {"group", "outcome_mean", "outcome_ci95_low", "outcome_ci95_high"}
        missing_summary = sorted(needed.difference(summary.columns))
        if missing_summary:
            raise KeyError(f"Missing ridgeline summary columns: {missing_summary}")
        summary_work = summary.copy()
        summary_work["group"] = summary_work["group"].astype(str)
        for y, group in enumerate(groups):
            row = summary_work.loc[summary_work["group"].eq(group)]
            if row.empty:
                continue
            mean = float(row.iloc[0]["outcome_mean"])
            low = float(row.iloc[0]["outcome_ci95_low"])
            high = float(row.iloc[0]["outcome_ci95_high"])
            marker_y = y + ridge_height * 0.14
            ax.errorbar(
                mean,
                marker_y,
                xerr=np.array([[mean - low], [high - mean]]),
                fmt="o",
                markersize=5.5,
                markerfacecolor="white",
                markeredgecolor="0.15",
                ecolor="0.15",
                elinewidth=1.15,
                capsize=3,
                zorder=7,
            )

    ax.set_yticks(np.arange(len(groups)), groups)
    handles = [
        Patch(
            facecolor=color_map[component],
            label=(component_labels or {}).get(component, component),
        )
        for component in components
    ]
    ax.legend(handles=handles, frameon=False, ncol=min(len(handles), 5))
    return ax
