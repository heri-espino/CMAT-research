# Paper 1 — incentive-linked support use and persistence

**Working title:** *Beyond the Incentive Threshold: Academic Support Use and Persistence After a First-Year Participation Incentive*

Canonical portfolio: `../../docs/PUBLICATION_PORTFOLIO.md`.

This directory is the **single canonical home** for Paper 1. Paper-specific manuscript material, literature notes, results and submission files belong here; shared source PDFs remain in `../../literature/library/`.

## Current status

A first formal English manuscript draft now exists at `manuscript/main.tex`, with a paper-local `manuscript/references.bib` and traceability/build notes in `manuscript/README.md`.

This is a research draft rather than a submission-ready manuscript. The primary persistence result is developed enough for a complete paper narrative, while unresolved reproducibility/selection questions are marked explicitly as draft-development notes rather than being hidden or filled with unsupported assumptions.

## Research question

Does formal academic-support use observed in an incentive-linked first-year MU context persist into later Calculus use after that specific PPA1-linked incentive is treated as generally no longer applying?

## Primary outcome

Any CMAT use during the subsequent eligible Calculus period.

## Primary predictor

MU-period visit group: `0 / 1–2 / exactly 3 / 4+`.

## Core populations

- broad linked MU→Calculus cohort (`N=4,211` in the current methodological snapshot);
- stricter next-regular-term PPA snapshot (`N=3,241`) used by the current first manuscript draft and still requiring full reintegration into the canonical executable pipeline.

## Contribution

Persistence of formal academic help-seeking across a change in incentive context, while keeping competing explanations visible: threshold-limited use, persistence/familiarization, and stable student selection.

## Journal strategy

1. *Studies in Higher Education* — ambitious primary target.
2. *International Journal of Mathematical Education in Science and Technology* (IJMEST).
3. *Teaching Mathematics and its Applications* (TEAMAT).
4. *Journal of Further and Higher Education*.

## Interpretation rule

This is observational. Visit counts are student-chosen. The analysis does **not** identify a causal PPA effect, a tutoring effect, motivation, or habit formation.

## Paper-local structure

- `literature/` — paper-specific literature index, reading guides, gaps and reading notes; no duplicate source PDFs.
- `manuscript/` — current LaTeX manuscript draft and paper-local bibliography.
- `results/` — paper-specific reviewed tables/figures when retained.
- `submission/` — journal-specific submission material when needed.

Create `results/` and `submission/` only when they contain real files; do not add empty scaffolding solely for symmetry.

## Dependencies

Uses the canonical longitudinal logic in `../../code/` and aggregate outputs from `../../analysis/`. The strict `N=3,241` longitudinal result currently remains a later-stage retained snapshot documented in the research compendium/methodology report and must be regenerated from the canonical executable pipeline before submission. Paper-specific literature is in `literature/`; physical source records remain in `../../literature/library/`.
