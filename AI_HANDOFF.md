# CMAT AI handoff

`main` is the upstream scientific branch and owns shared `cmat_analysis/`, `data/`, `literature/`, `brainstorm/`, and `docs/`. Publication-specific manuscript trees belong only on the five `paper/*` branches.

`cmat_analysis/` is an installable internal scientific library analogous to a project-specific scikit-learn. Install it with `python -m pip install -e ./cmat_analysis`; search `cmat_analysis/FUNCTION_INDEX.md` before adding functions. Reusable cohort definitions, transformations, estimators, tests, models, uncertainty calculations, imputation logic and plotting functions belong in `cmat_analysis/src/cmat_analysis/`.

`brainstorm/` preserves broad research development: exploratory questions, diagnostics, nulls, robustness checks, methodological reasoning and retained aggregate outputs. Brainstorm-local code is orchestration only and imports `cmat_analysis`.

A paper branch adds `literature_selected/`, branch-local `code/`, `results/`, `paper/`, and `submission/`. If paper work needs a reusable capability, implement and validate it on `main` in `cmat_analysis`, then bring `main` into the paper branch. Do not leave shared scientific improvements isolated in one publication branch.

The physical literature corpus stays under `literature/library/`; branch-specific source selection and annotations live under `literature_selected/`. Raw institutional microdata, identifiers, credentials and secrets must never be committed. Heavy PDFs/images remain in Git LFS.

Read `docs/RESEARCH_WORKFLOW.md`, `cmat_analysis/AI_HANDOFF.md`, `brainstorm/AI_HANDOFF.md`, and `PAPER_BRANCH.md` when present.
