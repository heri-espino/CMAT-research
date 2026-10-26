# CMAT research

## Consolidated Paper 2 — working integration

The merged methodology audit, corrected PPA three-group implementation, integrated
LaTeX draft, Marp slides, QA reports, and all reproducibility runners are in:

**[Paper 2: Beyond First Attendance — integrated project](https://github.com/heri-espino/CMAT-research/tree/paper/paper2-beyond-first-attendance/papers/paper2-beyond-first-attendance)**

The [full rerun instructions](https://github.com/heri-espino/CMAT-research/blob/paper/paper2-beyond-first-attendance/papers/paper2-beyond-first-attendance/README.md)
include one Windows command that regenerates the original Holm, EM/GMM,
fused, Shapley, piecewise, curve, and primary PPA analyses and publishes the
reviewed **aggregate** results to the consolidated branch. New adjusted PPA
results and a fully validated integrated paper/Marp export remain pending
the next authorized institutional-data run and manuscript/slide claim review.
The historically published Paper 2.1 PDF below remains available and is
**not** yet a representation of this new integrated article.

## Manuscript — direct PDF

**[Read Paper 2.1: CMAT attendance frequency and academic outcomes (PDF)](https://github.com/heri-espino/CMAT-research/blob/paper/paper2.1-visit-frequency/paper/paper.pdf)**

The linked file is the clean compiled **working draft** hosted directly in the paper branch, rather than a temporary GitHub Actions artifact. [Paper source, figures and reproducibility notes](https://github.com/heri-espino/CMAT-research/tree/paper/paper2.1-visit-frequency/paper). The manuscript is observational and remains subject to the documented editorial and data-use checks.

`main` is the shared upstream research branch. It contains the scientific library, controlled-data contracts, shared literature, broad research brainstorming and programme documentation; publication-specific work and large historical workspaces live on dedicated long-lived branches.

```text
CMAT-research/
├── cmat_analysis/   # installable reusable scientific library
├── data/            # controlled-data contracts; no raw microdata in Git
├── literature/      # shared physical/source literature library
├── brainstorm/      # broad analyses, diagnostics, nulls, sensitivities, ideas
└── docs/            # programme-wide documentation and provenance
```

## Environment

The canonical Python package metadata and scientific dependency pins live in `cmat_analysis/pyproject.toml`. For pip, install the shared library with:

```bash
python -m pip install -e './cmat_analysis[dev,docs]'
```

For Conda, create the repository environment with:

```bash
conda env create -f environment.yml
conda activate cmat-research
```

Reusable scientific logic belongs in `cmat_analysis/src/cmat_analysis/`; brainstorm and paper runners import it. See `REPRODUCING.md` and `docs/REPOSITORY_METADATA.md` for the reproducibility and metadata conventions.

## Publication branches

- `paper/paper1-ppa-persistence`
- `paper/paper2-mu-performance`
- `paper/paper2.1-visit-frequency` — observational attendance-frequency analysis
- `paper/paper2.2.1-fused-frequency` — **design stage**: ordered fused-lasso frequency regimes
- `paper/paper2.2.2-distributional-heterogeneity` — **design stage**: modality and mixture-model adequacy
- `paper/paper3-grading-heterogeneity`
- `paper/paper4-degree-help-seeking`
- `paper/paper5-longitudinal-trajectories`

Each paper branch adds `literature_selected/`, `code/`, `results/`, `paper/`, `submission/`, and `PAPER_BRANCH.md`. Branch-local `code/` chooses what to run for that publication; it must not duplicate reusable estimators or cohort logic from `cmat_analysis`.

## Historical brainstorm branches

- `brainstorm/proyecto-visitas` — sanitized preservation of **only** the historical `proyecto visitas/` subtree from `heri-espino/CMAT`. Its legacy code, notebooks, outputs and LaTeX report are research-development/provenance material, not a sixth paper and not a replacement for the modern `cmat_analysis` library.

Historical brainstorm branches inherit shared upstream from `main` but keep large or legacy workspaces isolated. Do not merge them wholesale into `main`; selectively promote reusable capabilities to `cmat_analysis` or programme-level findings to the canonical shared `brainstorm/` layer after review.

Repository-wide integration is governed through a designated repo-admin / integrator / upstream-maintainer workflow, while branch-specific chats act as research, reconstruction or writing agents for their assigned branch. Because chats cannot communicate directly with one another, durable decisions and cross-branch instructions must be recorded in the repository. See `docs/REPO_GOVERNANCE.md` and `AI_HANDOFF.md` before making structural or upstream changes.

Do not merge an entire `paper/*` or long-lived historical `brainstorm/*` branch into `main`; these branches are intentionally ahead of the shared upstream. Reusable improvements discovered while working on a branch should be integrated into `main` first and then propagated back to the relevant branches.

## Citation and repository metadata

GitHub citation metadata lives in `CITATION.cff`; a BibTeX convenience record is available in `CITATION.bib`, while `codemeta.json` provides machine-readable software metadata. These files describe the research compendium rather than determining authorship of individual manuscripts.

The repository-wide rights boundary is described in `LICENSE`, contribution expectations in `CONTRIBUTING.md`, and sensitive-data/security reporting in `SECURITY.md`.

Heavy research binaries remain in Git LFS. Install once with `git lfs install`; use `git lfs pull` when assets are still pointers.
