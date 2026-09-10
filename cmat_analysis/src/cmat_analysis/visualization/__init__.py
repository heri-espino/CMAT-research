"""Reusable visualization primitives and scientific figure builders.

Plotting is separated from cohort construction and statistical estimation.
The package root exposes style configuration only; specialized plots live in
named submodules to avoid an excessively broad plotting namespace.
"""

from .style import mpl_apply, plotly_apply, set_style

__all__ = ["mpl_apply", "plotly_apply", "set_style"]
