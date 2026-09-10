# CMAT research

`main` is the shared upstream research branch. It contains the scientific library, controlled-data contracts, shared literature, broad research brainstorming and programme documentation; publication-specific work and large historical workspaces live on dedicated long-lived branches.

```text
CMAT-research/
├── cmat_analysis/   # installable reusable scientific library
├── data/            # controlled-data contracts; no raw microdata in Git
├── literature/      # shared physical/source literature library
├── brainstorm/      # broad analyses, diagnostics, nulls, sensitivities, ideas
└── docs/            # programme-wide documentation and provenance
```

Install the shared library with `python -m pip install -e ./cmat_analysis`. Reusable scientific logic belongs in `cmat_analysis/src/cmat_analysis/`; brainstorm and paper runners import it.

## Publication branches

- `paper/paper1-ppa-persistence`
- `paper/paper2-mu-performance`
- `paper/paper3-grading-heterogeneity`
- `paper/paper4-degree-help-seeking`
- `paper/paper5-longitudinal-trajectories`

Each paper branch adds `literature_selected/`, `code/`, `results/`, `paper/`, `submission/`, and `PAPER_BRANCH.md`. Branch-local `code/` chooses what to run for that publication; it must not duplicate reusable estimators or cohort logic from `cmat_analysis`.

## Historical brainstorm branches

- `brainstorm/proyecto-visitas` — sanitized preservation of **only** the historical `proyecto visitas/` subtree from `heri-espino/CMAT`. Its legacy code, notebooks, outputs and LaTeX report are research-development/provenance material, not a sixth paper and not a replacement for the modern `cmat_analysis` library.

Historical brainstorm branches inherit shared upstream from `main` but keep large or legacy workspaces isolated. Do not merge them wholesale into `main`; selectively promote reusable capabilities to `cmat_analysis` or programme-level findings to the canonical shared `brainstorm/` layer after review.

Repository-wide integration is governed through a designated repo-admin / integrator / upstream-maintainer workflow, while branch-specific chats act as research, reconstruction or writing agents for their assigned branch. Because chats cannot communicate directly with one another, durable decisions and cross-branch instructions must be recorded in the repository. See `docs/REPO_GOVERNANCE.md` and `AI_HANDOFF.md` before making structural or upstream changes.

Do not merge an entire `paper/*` or long-lived historical `brainstorm/*` branch into `main`; these branches are intentionally ahead of the shared upstream. Reusable improvements discovered while working on a branch should be integrated into `main` first and then propagated back to the relevant branches.

Heavy research binaries remain in Git LFS. Install once with `git lfs install`; use `git lfs pull` when assets are still pointers.
