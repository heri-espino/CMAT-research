# Publication portfolio

The branch list below distinguishes existing manuscript programmes from **prospective design-only studies**. Creating a `paper/*` branch does not imply that a stand-alone journal article, new statistical result or approved interpretation already exists.

| Workstream | Branch | Research question / role | Current status |
|---|---|---|---|
| Paper 1 | `paper/paper1-ppa-persistence` | PPA-linked CMAT use and later help-seeking persistence | Paper-specific research branch |
| Paper 2 | `paper/paper2-mu-performance` | MU support use and classroom-relative performance | Paper-specific research branch |
| Paper 2.1 | `paper/paper2.1-visit-frequency` | Observational visit-frequency structure, final outcomes and mixture sensitivities | Inherited empirical baseline/manuscript for 2.2.x |
| **Paper 2.2.1 (proposed)** | `paper/paper2.2.1-fused-frequency` | Discover stable contiguous attendance regimes with ordered fused lasso and cluster-held-out validation | **Documentation/design only; no new analysis** |
| **Paper 2.2.2 (proposed)** | `paper/paper2.2.2-distributional-heterogeneity` | Distinguish GMM component count from modes and latent subpopulations; test unimodality under grade heaping/cluster sensitivity | **Documentation/design only; no new analysis** |
| Paper 3 | `paper/paper3-grading-heterogeneity` | Grading/classroom heterogeneity and standardisation | Paper-specific research branch |
| Paper 4 | `paper/paper4-degree-help-seeking` | Degree programme and formal help-seeking | Paper-specific research branch |
| Paper 5 | `paper/paper5-longitudinal-trajectories` | Longer-run support-use and academic trajectories | Paper-specific research branch |

## Provenance and handoff

Both 2.2.x branches were forked on 2026-10-07 from Paper 2.1 commit `0e39a875343c03ca3bb5c793f1f9e7c2bcba6173`. For each, read its `PAPER_BRANCH.md`, `paper/AI_HANDOFF.md` and `paper/docs/README.md` before implementing. Its inherited Paper 2.1 manuscript, code, tables and figures remain **historical baseline**, not 2.2.x results.

The root `code/` on a paper branch orchestrates publication-specific scripts. Reusable estimators belong to `main/cmat_analysis/src/cmat_analysis/`, with tests and function index updates upstream first. Shared `docs/` and portfolio governance belong to `main`. Never merge a complete paper branch into `main`; selectively propagate reusable code and methods. No raw institutional microdata or personal identifiers may be committed.

**Research boundaries:** 2.2.1 tests the resolution of *ordered attendance categories*; 2.2.2 tests *distributional shape and modality*. Neither paper may claim causal visit effects. Two fitted Gaussian components never automatically imply two modes or two natural types of students.
