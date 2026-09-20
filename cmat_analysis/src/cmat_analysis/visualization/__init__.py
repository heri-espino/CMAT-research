"""Reusable visualization primitives and scientific figure builders.

Plotting is separated from cohort construction and statistical estimation.
"""

from .ridgeline import plot_stacked_ridgeline
from .style import mpl_apply, plotly_apply, set_style

__all__ = ["mpl_apply", "plot_stacked_ridgeline", "plotly_apply", "set_style"]
