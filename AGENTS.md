# CMAT AI handoff

## Branch policy — mandatory

The repository has only two kinds of long-lived branches: `main` and paper branches under `paper/*`. Do not create or preserve `admin/*`, `brainstorm/*`, `chore/*`, `data/*`, `docs/*`, `fix/*`, `feature/*`, `integrate/*`, or other auxiliary branches unless the user explicitly authorizes a temporary exception for a specific task.

`main` is the canonical upstream scientific branch and owns all shared work: reusable `cmat_analysis/` code, data contracts and controlled data, literature infrastructure, `brainstorm/` exploratory work, documentation, repository configuration, CI, plotting style, fixes, migrations, and reusable outputs. Work of those kinds should be committed directly to `main`, not parked on a separate branch.

Paper branches exist only to hold paper-specific deltas: manuscript prose, paper-local analysis recipes, selected literature, paper results, submission material, and other artifacts whose meaning belongs to one paper. Current paper branches are `paper/paper1-ppa-persistence`, `paper/paper2-mu-performance`, `paper/paper3-grading-heterogeneity`, `paper/paper4-degree-help-seeking`, and `paper/paper5-longitudinal-trajectories`.

The synchronization direction is `main -> paper/*`. When a reusable method, data transformation, plotting convention, documentation rule, or shared fix is needed while working on a paper, implement and validate it on `main` first, then bring `main` into the relevant paper branch. Never use a whole paper branch as the source of truth for shared infrastructure, and never merge a complete paper branch back into `main` merely to recover reusable code.

Before creating any branch, first ask whether the work is genuinely a new paper. If not, use `main`. A new permanent branch is acceptable only for a new paper and should use the `paper/<paper-id>-<short-slug>` naming pattern. If a temporary branch is ever explicitly authorized, integrate its durable work into `main` during the same task and delete the temporary branch before finishing.

## Scientific architecture

`cmat_analysis/` is an installable internal scientific library analogous to a project-specific scikit-learn. Install it with `python -m pip install -e ./cmat_analysis`; search `cmat_analysis/FUNCTION_INDEX.md` before adding functions. Reusable cohort definitions, transformations, estimators, tests, models, uncertainty calculations, imputation logic and plotting functions belong in `cmat_analysis/src/cmat_analysis/`.

`brainstorm/` lives on `main` and preserves broad research development: exploratory questions, diagnostics, nulls, robustness checks, methodological reasoning, historical analyses and retained aggregate outputs. Brainstorm-local code is orchestration only and should import `cmat_analysis` when the capability is reusable.

A paper branch may add `literature_selected/`, branch-local `code/`, `results/`, `paper/`, and `submission/`. Shared improvements discovered during paper work must still be promoted to `main` first and then synchronized back down.

The physical literature corpus stays under `literature/library/`; branch-specific source selection and annotations live under `literature_selected/`. Raw institutional microdata, direct identifiers, credentials and secrets must never be committed. Heavy PDFs/images remain in Git LFS.

Read `.ai_handoff`, `docs/RESEARCH_WORKFLOW.md`, `cmat_analysis/AI_HANDOFF.md`, `brainstorm/AI_HANDOFF.md`, and `PAPER_BRANCH.md` when present.
