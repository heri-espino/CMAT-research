# Paper 1 — incentive-linked support use and persistence

**Working title:** *Beyond the Incentive Threshold: Academic Support Use and Persistence After a First-Year Participation Incentive*

Canonical portfolio: `../../docs/PUBLICATION_PORTFOLIO.md`.

This directory is the **single canonical home** for Paper 1. Paper-specific manuscript material, literature interpretation, selected final results and submission files belong here; shared source PDFs remain in `../../literature/library/`.

## Production position

Paper 1 is a downstream publication selection, not an independent analysis branch:

```text
root/code reusable functions
        ↓
brainstorm/research_compendium + brainstorm/methodology_report
        broad longitudinal/methodological evidence
        ↓
papers/paper1_ppa_persistence
        selected publication argument
```

When a Paper 1 calculation needs to change or be added, implement/reuse it in root `../../code/`, regenerate the relevant report evidence, and only then update the manuscript.

## Current status

A first formal English manuscript draft exists at `manuscript/main.tex`, with `manuscript/references.bib` and traceability/build notes in `manuscript/README.md`.

This is a research draft rather than a submission-ready manuscript. The primary persistence result is developed enough for a complete narrative, while unresolved reproducibility/selection questions are marked explicitly instead of being filled with unsupported assumptions.

## Research question

Does formal academic-support use observed in an incentive-linked first-year MU context persist into later Calculus use after that specific PPA1-linked incentive is treated as generally no longer applying?

## Primary outcome

Any CMAT use during the subsequent eligible Calculus period.

## Primary predictor

MU-period visit group: `0 / 1–2 / exactly 3 / 4+`.

## Core populations

- broad linked MU→Calculus cohort (`N=4,211` in the current methodological snapshot);
- stricter next-regular-term PPA snapshot (`N=3,241`) used by the current first manuscript draft and still requiring full reintegration into the canonical executable pipeline.

## Source reports

Paper 1 currently draws its empirical development from two report-level records:

- `../../brainstorm/research_compendium/` — contains the refined PPA1→Calculus longitudinal development, including the N=3,241 stage;
- `../../brainstorm/methodology_report/` — contains the later methodology/statistical review, broad N=4,211 progressor sensitivity, and the preserved N=3,241 comparison snapshot.

These reports are intentionally broader than Paper 1. The manuscript should select only the results needed for its argument while keeping traceability to the report/root-code source.

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

- `literature/` — paper-specific literature index, reading guides, annotations, gaps and reading notes; no duplicate source PDFs.
- `manuscript/` — current LaTeX manuscript draft and paper-local bibliography.
- `results/` — final reviewed tables/figures selected for Paper 1 when retained.
- `code/` — optional future thin packaging/build entry point only; no reusable scientific functions.
- `submission/` — journal-specific submission material when needed.

Create folders only when they contain real files; do not add empty scaffolding solely for symmetry.

## Dependencies and reproducibility boundary

Reusable longitudinal/statistical logic belongs in `../../code/`. Report-level empirical development belongs in `../../brainstorm/`. The strict N=3,241 longitudinal result currently remains a later-stage retained snapshot documented in the two source reports and must be regenerated from the canonical executable root-code pipeline before submission.

Paper-specific literature is in `literature/`; physical source records remain in `../../literature/library/`.
