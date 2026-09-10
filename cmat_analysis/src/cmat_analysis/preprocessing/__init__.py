"""Input cleaning and reusable preprocessing operations.

This namespace contains transformations applied before cohort construction.
Functions here may clean or normalize source tables, but they must not encode
paper-specific inclusion rules or alter scientific estimands.
"""

from .cleaning import clean_materias_df, get_salones_with_imputations

__all__ = ["clean_materias_df", "get_salones_with_imputations"]
