"""Exclusive PPA-threshold group definitions; do not infer student motives."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass(frozen=True)
class GroupSpecification:
    name: str
    labels: tuple[str, ...]
    exploratory_ppa: bool

SPECS = (
    GroupSpecification("primary_0_1to3_4plus", ("0", "1-3", "4+"), True),
    GroupSpecification("historical_exact_0to6_7plus", ("0", "1", "2", "3", "4", "5", "6", "7+"), False),
)

def assign_visit_groups(visits: pd.Series, spec: GroupSpecification) -> pd.Series:
    """Partition nonnegative integer same-period visit counts, failing closed."""
    numeric = pd.to_numeric(visits, errors="raise")
    if numeric.isna().any() or not np.isfinite(numeric.to_numpy(dtype=float)).all():
        raise ValueError("Attendance count contains missing or non-finite entries")
    if (numeric < 0).any() or (numeric != np.floor(numeric)).any():
        raise ValueError("Attendance count must be a nonnegative integer")
    v = numeric.to_numpy(dtype=np.int64)
    if spec.name == SPECS[0].name:
        labels = np.select([v == 0, v <= 3], ["0", "1-3"], default="4+")
    elif spec.name == SPECS[2].name:
        labels = np.where(v >= 7, "7+", v.astype(str))
    else:
        raise ValueError(f"Unknown specification: {spec.name}")
    return pd.Series(pd.Categorical(labels, categories=spec.labels, ordered=True), index=visits.index)

def verify_partition(df: pd.DataFrame, *, visit_col: str = "VISITS_CMAT_PERIOD") -> dict[str, int]:
    """Check exhaustive mutually exclusive partitions and cross-model identities."""
    if visit_col not in df:
        raise KeyError(visit_col)
    n = len(df)
    counts = {}
    for spec in SPECS:
        g = assign_visit_groups(df[visit_col], spec)
        if g.isna().any() or sum(int((g == label).sum()) for label in spec.labels) != n:
            raise AssertionError(f"Non-exhaustive partition: {spec.name}")
        for label in spec.labels:
            counts[f"{spec.name}:{label}"] = int((g == label).sum())
    primary, exact = SPECS
    assert counts[f"{primary.name}:0"] == counts[f"{exact.name}:0"]
    assert counts[f"{primary.name}:1-3"] == sum(counts[f"{exact.name}:{x}"] for x in ("1", "2", "3"))
    assert counts[f"{primary.name}:4+"] == sum(counts[f"{exact.name}:{x}"] for x in ("4", "5", "6", "7+"))
    assert sum(counts[f"{primary.name}:{x}"] for x in primary.labels) == n
    return counts

def ppa_family_size() -> int:
    """Three pairwise contrasts in EACH of two separately corrected outcome families."""
    return len(SPECS[0].labels) * (len(SPECS[0].labels) - 1) // 2

assert ppa_family_size() == 3
