"""Observed-covariate selection adjustment and propensity-score diagnostics.

The current implementation estimates ATT weights from observed covariates only;
it does not remove bias from unmeasured motivation, need, or other confounders.
"""

from ._selection import *  # noqa: F401,F403
