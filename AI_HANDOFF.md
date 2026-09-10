# CMAT AI handoff

`main` is the upstream scientific branch and owns shared `cmat_analysis/`, `data/`, `literature/`, `brainstorm/`, and `docs/`. Publication-specific manuscript trees belong only on the five `paper/*` branches.

## Governance and cross-chat coordination

The user retains final scientific and project authority. A designated **repo-admin / integrator / upstream-maintainer chat** coordinates repository-wide architecture, Git state, shared methodology, provenance, and movement of reusable work between `main` and the five paper branches. Other chats may act as **paper-specific research and writing agents** and should optimize the publication they own without independently redesigning shared infrastructure.

Chats cannot send messages directly to one another as an inter-chat channel. Consequently, any decision that must persist or be visible to another chat must be written into the repository. Use `AI_HANDOFF.md`, `docs/REPO_GOVERNANCE.md`, `cmat_analysis/AI_HANDOFF.md`, `brainstorm/AI_HANDOFF.md`, `PAPER_BRANCH.md`, component READMEs, and provenance records as the persistent communication layer. A proposal from another chat can be brought to the repo-admin chat for review before integration.

Do not merge an entire paper branch back into `main`. Paper branches are intentionally ahead of `main` because they own publication-specific `literature_selected/`, `code/`, `results/`, `paper/`, and `submission/`. If paper work discovers reusable scientific logic, integrate that capability into `main/cmat_analysis`, validate it there, and then bring the updated `main` into the relevant paper branch(es).

`cmat_analysis/` is an installable internal scientific library analogous to a project-specific scikit-learn. Install it with `python -m pip install -e ./cmat_analysis`; search `cmat_analysis/FUNCTION_INDEX.md` before adding functions. Reusable cohort definitions, transformations, estimators, tests, models, uncertainty calculations, imputation logic and plotting functions belong in `cmat_analysis/src/cmat_analysis/`.

`brainstorm/` preserves broad research development: exploratory questions, diagnostics, nulls, robustness checks, methodological reasoning and retained aggregate outputs. Brainstorm-local code is orchestration only and imports `cmat_analysis`.

A paper branch adds `literature_selected/`, branch-local `code/`, `results/`, `paper/`, and `submission/`. If paper work needs a reusable capability, implement and validate it on `main` in `cmat_analysis`, then bring `main` into the paper branch. Do not leave shared scientific improvements isolated in one publication branch.

The physical literature corpus stays under `literature/library/`; branch-specific source selection and annotations live under `literature_selected/`. Raw institutional microdata, identifiers, credentials and secrets must never be committed. Heavy PDFs/images remain in Git LFS.

Read `docs/REPO_GOVERNANCE.md`, `docs/RESEARCH_WORKFLOW.md`, `cmat_analysis/AI_HANDOFF.md`, `brainstorm/AI_HANDOFF.md`, and `PAPER_BRANCH.md` when present.
