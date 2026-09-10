# CMAT research workflow

## Shared upstream

`main` contains `cmat_analysis/`, `data/`, `literature/`, `brainstorm/`, and `docs/`. `cmat_analysis` is the internal reusable library and should be installed editable with `python -m pip install -e ./cmat_analysis`. `brainstorm` is the broad empirical-development layer that retains exploratory work, nulls, diagnostics and sensitivities.

## Publication branches

Each paper has a long-lived branch inheriting `main` and adding:

```text
literature_selected/   paper-specific source selection and annotations
code/                  thin paper-specific analysis orchestration
results/               generated/selected paper outputs
paper/                 manuscript and build material
submission/            journal-specific material
PAPER_BRANCH.md         branch contract
```

Branch-local `code/` specifies which shared functions and specifications answer the paper's question; `cmat_analysis` defines how calculations work. If a paper exposes a missing reusable function, fix and test it on `main/cmat_analysis`, then merge/rebase `main` into the paper branch and rerun.

`literature/` is the shared physical/source corpus; `literature_selected/` exists only on paper branches and contains the working subset, reading notes and annotated Markdown derivatives.
