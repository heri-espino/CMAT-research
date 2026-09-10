# Paper 1 code

This directory owns only the **publication-specific recipe** for Paper 1. Reusable scientific logic belongs upstream in `main/cmat_analysis`; this branch imports that installed library and selects the cohort, estimators, output tables and figure required by the paper.

## Setup

From the repository root:

```bash
python -m pip install -e './cmat_analysis[dev]'
```

Validate the branch-local recipe without reading private data:

```bash
python code/run_paper.py --check
```

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
│   └── ppa_persistence_by_mu_group.png
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

`--compile` delegates to `paper/build.py`; it does not implement LaTeX logic inside the scientific runner.

## Shared API used

The recipe imports the reviewed public surfaces in `cmat_analysis.cohorts`, `cmat_analysis.ppa`, `cmat_analysis.reporting`, and `cmat_analysis.visualization`. The configuration factory remains in `cmat_analysis.config.study_config`.

Do **not** implement reusable estimators, cohort definitions, confidence intervals, transformations, model primitives, or reusable plotting functions here. If Paper 1 needs a new reusable capability, escalate it to the repo-admin workflow and implement/test it upstream in `main/cmat_analysis` before synchronizing `main` back into this branch.
