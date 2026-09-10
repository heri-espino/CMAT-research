# Paper 1 code

This directory owns only the **publication-specific recipe** for Paper 1. Reusable scientific logic belongs upstream in `main/cmat_analysis`; this branch imports that installed library and selects the cohort, estimators, output tables and figures required by the paper.

## Setup

From the repository root:

```bash
python -m pip install -e './cmat_analysis[dev]'
```

Validate the branch-local recipe without reading private data:

```bash
python code/run_paper.py --check
```

The check also validates that the retained aggregate inputs required to build the four manuscript figures are present and have the expected columns.

## Reproduce Paper 1

Administrative microdata are intentionally not stored in Git. Supply the controlled local files explicitly:

```bash
python code/run_paper.py \
  --materias '/path/to/Materias.xlsx' \
  --asesorias '/path/to/Asesorias.xlsx'
```

The runner reconstructs the strict next-regular-term MU -> Calculus progression cohort and writes aggregate outputs to:

```text
results/
├── tables/
│   ├── 98_ppa_progression_cohort_flow.csv
│   ├── 99_revalidation_audit.csv
│   ├── 100_student_official_career_count_distribution.csv
│   └── 101_... through 107_...
├── figures/
│   ├── figure_01_cohort_flow.png
│   ├── figure_02_main_persistence.png
│   ├── figure_03_threshold_piecewise.png
│   └── figure_04_adjusted_persistence_or.png
├── logs/
└── run_summary.json
```

For the current manuscript, tables `101`--`107` correspond to the retained refined longitudinal outputs used in the draft. To require numerical agreement with that retained snapshot:

```bash
python code/run_paper.py \
  --materias '/path/to/Materias.xlsx' \
  --asesorias '/path/to/Asesorias.xlsx' \
  --compare-retained
```

A mismatch is intentionally fatal: do not update manuscript numbers until it has been reviewed.

To run the analysis and then compile the LaTeX manuscript:

```bash
python code/run_paper.py \
  --materias '/path/to/Materias.xlsx' \
  --asesorias '/path/to/Asesorias.xlsx' \
  --compare-retained \
  --compile
```

`--compile` delegates to `paper/build.py`; it does not implement LaTeX logic inside the scientific runner. The runner generates the four paper figures from the newly generated aggregate tables before compilation.

## Figure-only generation

`code/figures.py` contains publication-specific presentation logic only; it never reconstructs cohorts or re-estimates models. It can regenerate the English manuscript figures from retained aggregate tables without private data:

```bash
python code/figures.py --source retained
```

or, after a successful empirical run, from `results/tables/`:

```bash
python code/figures.py --source generated
```

See `paper/FIGURE_INVENTORY.md` for the mapping from the old historical figure to the four current manuscript figures and for the decision not to add a separate academic-performance figure.

## Shared API used

The recipe imports the reviewed public surfaces in `cmat_analysis.cohorts`, `cmat_analysis.ppa`, `cmat_analysis.reporting`, and `cmat_analysis.visualization`. The configuration factory remains in `cmat_analysis.config.study_config`.

Do **not** implement reusable estimators, cohort definitions, confidence intervals, transformations, model primitives, or reusable plotting functions here. If Paper 1 needs a new reusable capability, escalate it to the repo-admin workflow and implement/test it upstream in `main/cmat_analysis` before synchronizing `main` back into this branch.
