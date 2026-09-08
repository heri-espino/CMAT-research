# Papers

Publication-specific manuscript projects for the five-paper CMAT research programme.

## Core rule

Papers consume the canonical scientific pipeline and aggregate outputs; they do **not** maintain independent versions of cohorts, estimands, models, or numerical results.

The canonical portfolio plan is `docs/PUBLICATION_PORTFOLIO.md`. Use that document as the source of truth for working titles, priority, target journals, and paper boundaries.

## Planned manuscripts

1. `paper1_ppa_persistence/` — persistence of formal mathematics-support use after the first-year incentive-linked context.
2. `paper2_mu_performance/` — contemporaneous CMAT use and classroom-relative MU performance.
3. `paper3_grading_heterogeneity/` — instructor-by-term grading heterogeneity and assessment comparability.
4. `paper4_degree_help_seeking/` — disciplinary/degree-programme heterogeneity in support use and persistence.
5. `paper5_longitudinal_trajectories/` — full-degree longitudinal trajectories of mathematics-support use.

## Expected contents of each paper folder

- `README.md` with scope, RQs, contribution, target journals, status and dependencies;
- LaTeX manuscript source when drafting begins;
- manuscript-specific `references.bib`;
- only the figures/tables needed for that manuscript, sourced from canonical aggregate outputs;
- no paper-specific copy of the scientific analysis pipeline.

## Scientific boundary

If a manuscript exposes a methodological problem, fix it first in `code/` through a short-lived feature branch, regenerate canonical outputs, verify changed numbers, and only then update the manuscript.

Paper-specific literature maps live separately under `literature/papers/`; the physical literature corpus remains shared under `literature/library/`.