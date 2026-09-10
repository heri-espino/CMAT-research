# cmat_analysis

`cmat_analysis` is the reusable scientific Python library for the CMAT research programme. It owns data-cleaning primitives, cohort construction, derived measures, statistical estimators, longitudinal diagnostics, PPA analyses, visualization primitives, and generic reporting/provenance utilities that are shared across analyses. Report orchestration belongs in `brainstorm/<analysis>/code/`, while publication orchestration belongs in the corresponding paper branch.

## Installation

From the repository root:

```bash
python -m pip install -e "./cmat_analysis[dev,docs]"
```

The physical `src/` layout is intentional. After installation the package is imported directly as `cmat_analysis`.

## Namespace map

- `cmat_analysis.io` — source readers and input validation.
- `cmat_analysis.preprocessing` — reusable cleaning and normalization before cohort construction.
- `cmat_analysis.cohorts` — academic attempts, revalidations, period ordering, visit attachment, and study cohorts.
- `cmat_analysis.measures` — derived grade/pass outcomes and classroom-relative measures.
- `cmat_analysis.statistics` — descriptive/inferential statistics, fixed-effect models, robust comparisons, and observed-covariate selection adjustment.
- `cmat_analysis.longitudinal` — visit timing, regularity, periodicity, and repeated-use transitions.
- `cmat_analysis.ppa` — PPA exposure-threshold, persistence, and MU-to-Calculus progression analyses.
- `cmat_analysis.visualization` — styles and reusable scientific figure builders.
- `cmat_analysis.reporting` — generic formatting/provenance utilities; report-specific builders are compatibility code, not public API.
- `cmat_analysis.privacy` — pseudonymisation and privacy helpers.

The historical `analysis`, `study`, and `pipeline` namespaces are not public API. Compatibility shims preserve retained workflows while consumers migrate to the responsibility-based namespaces.

## Imports

```python
from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
from cmat_analysis.measures import add_primary_outcomes
from cmat_analysis.statistics import robust_two_group_tests, propensity_att_sensitivity
from cmat_analysis.longitudinal import student_temporal_regularity
from cmat_analysis.ppa import build_ppa_progression_cohort
```

## Minimal use

```python
from cmat_analysis.config.study_config import get_study_config
from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
from cmat_analysis.measures import add_primary_outcomes

config = get_study_config()
data = load_and_clean_inputs(config)
cohorts = build_study_cohorts(data, config)
mu = add_primary_outcomes(cohorts["mu_primary"], config)
```

These calls use the existing CMAT scientific definitions; the architecture refactor does not change passing thresholds, cohort rules, exposure definitions, imputation, standardization, or estimands.

## Tests

```bash
python -m pip install -e "./cmat_analysis[dev]"
python -c "import cmat_analysis"
pytest cmat_analysis/tests/
```

## Documentation

```bash
python -m pip install -e "./cmat_analysis[docs]"
sphinx-build -W -b html cmat_analysis/docs cmat_analysis/docs/_build/html
```

The Sphinx API reference is user/developer documentation generated from module and function docstrings. `FUNCTION_INDEX.md` is a separate generated inventory intended for development and AI-assisted code discovery.

## What belongs here

A function belongs in `cmat_analysis` when its scientific responsibility is reusable across analyses or papers and its behavior can be tested independently of a particular report. Code that selects which figures/tables to generate for one brainstorm or publication belongs in that workspace and should import the library rather than duplicate it.
