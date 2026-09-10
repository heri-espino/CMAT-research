# Paper 2 results

This directory is the branch-local destination for validated aggregate outputs produced by `code/run_paper.py` and publication figures produced by `code/figures.py`.

Expected structure after a controlled-data run:

```text
results/
├── tables/
├── figures/
├── logs/
└── run_summary.json
```

Figures are generated as vector PDF files for LaTeX. Generated microdata or student-level analytical datasets must never be written here or committed.

The manuscript can also be compiled without private data by generating figures from the retained aggregate checkpoint at `brainstorm/shared/historical_outputs/study/tables/`. Retained tables are provenance and a reproducibility guard; before submission they should be checked against a fresh controlled-data run with:

```bash
python code/run_paper.py --materias ... --asesorias ... --compare-retained
```
