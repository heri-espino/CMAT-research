"""Reusable scientific analysis library for the CMAT research programme.

The root namespace is intentionally small. Scientific capabilities are exposed
through responsibility-based subpackages such as :mod:`cmat_analysis.cohorts`,
:mod:`cmat_analysis.measures`, :mod:`cmat_analysis.statistics`,
:mod:`cmat_analysis.longitudinal`, and :mod:`cmat_analysis.ppa`. Historical
report-orchestration namespaces remain importable only for reproducibility and
are not part of the root public API.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("cmat-analysis")
except PackageNotFoundError:  # source-tree imports before installation
    __version__ = "0+unknown"

__all__ = ["__version__"]
