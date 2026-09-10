# Paper 4 — degree help-seeking branch

This branch is the canonical publication workspace for Paper 4. It inherits shared infrastructure from `main` and owns only publication-specific selection and production.

- `literature_selected/`: selected literature and reading notes;
- `code/`: paper-specific orchestration importing `cmat_analysis`;
- `results/`: generated/selected paper outputs;
- `paper/`: manuscript and build material;
- `submission/`: journal-specific material.

Reusable scientific logic must be implemented and tested on `main` under `cmat_analysis/src/cmat_analysis/`, then brought into this branch.
