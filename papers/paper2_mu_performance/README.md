# Paper 2 — CMAT use and classroom-relative MU performance

**Working title:** *Mathematics Support Use and Classroom-Relative Academic Performance in First-Year University Mathematics*

Canonical portfolio: `../../docs/PUBLICATION_PORTFOLIO.md`.

This directory is the **single canonical home** for Paper 2. Paper-specific manuscript material, literature notes, results and submission files belong here; shared source PDFs remain in `../../literature/library/`.

## Research question

How is contemporaneous CMAT use associated with classroom-relative academic performance in first-attempt MU?

## Primary outcome

Classroom-standardised final performance `Z_MU`, with classroom defined as `professor × subject × academic period`.

## Primary population

First observed eligible MU attempts with CMAT coverage (`N=6,627` in the current methodological snapshot). The `N=4,211` future-Calculus cohort is a sensitivity, not the primary estimand.

## Main exposure

CMAT use during the same MU period: primary groups `0 / 1 / 2 / 3 / 4+`, with exact-count and historical binary sensitivities.

## Current interpretation

The strongest reproducible separation appears to be between `0 visits` and `any positive use`, rather than a clean monotone dose-response across positive-use groups after multiplicity correction.

## Journal strategy

1. *Teaching Mathematics and its Applications* (TEAMAT) — primary target.
2. *International Journal of Mathematical Education in Science and Technology* (IJMEST) — second choice.
3. *International Journal of Research in Undergraduate Mathematics Education* (IJRUME) — ambitious option if the theoretical mathematics-education contribution is sufficiently strong.

## Interpretation rule

Observational association only; do not present CMAT attendance as a randomized tutoring treatment.

## Paper-local structure

- `literature/` — paper-specific literature index and targeted gaps; no duplicate source PDFs.
- `manuscript/` — LaTeX/manuscript source when present.
- `results/` — paper-specific reviewed tables/figures when retained.
- `submission/` — journal-specific submission material when needed.

Create the latter three directories only when they contain real files; do not add empty scaffolding solely for symmetry.

## Dependencies

Uses canonical MU outputs from `../../analysis/` and reusable scientific logic from `../../code/`; it does not maintain a separate scientific pipeline. Paper-specific literature is in `literature/`; physical source records remain in `../../literature/library/`.
