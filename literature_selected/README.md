# Paper 1 literature — PPA persistence

Paper-specific literature workspace for `paper1_ppa_persistence`.

The canonical paper scope, research question, outcomes, journal strategy and status live in `../README.md`. This directory contains only the literature-specific layer: source priorities, reading guidance, evidence notes, gaps and claim boundaries.

The physical source corpus remains shared in `../../../literature/library/`; do not duplicate PDFs here.

## Literature logic

The literature should support four distinct parts of the argument:

1. institutional incentives and intervention context;
2. formal academic help-seeking / engagement;
3. persistence after incentives or encouragement change;
4. mathematics support as the empirical setting.

Do not let mathematics-support literature dominate the broader higher-education contribution.

## Literature families

- incentives and incentive removal;
- behavioural persistence/familiarization without claiming habit is observed;
- academic help-seeking;
- student engagement and first-year transition;
- mathematics-support context;
- observational selection and alternative explanations.

## How to read this folder

1. `INDEX.md` — which sources matter and their role in the manuscript.
2. `READING_GUIDE.md` — rapid technical guide with the most important methods/results to remember.
3. `reading_notes/` — article-level evidence cards with sample, methods, coefficients/tests, uncertainty, quotations, claim boundaries and local verification anchors.
4. `notes_on_papers/` — generated **full-text annotated Markdown reading copies**. Important source passages are marked in place as: **1. main idea**, **2. numerical result**, or **3. methodology/statistical test/assumption**. These are derived reading aids; the canonical source remains under `../../../literature/library/`.
5. `MISSING_LITERATURE.md` — targeted gaps still requiring search/acquisition.

### Annotated full-text copies

`notes_on_papers/` uses GitHub-native Markdown alerts so the annotations are visually distinct without relying on custom CSS:

- `IMPORTANT` → **Idea principal**;
- `TIP` → **Resultado numérico**;
- `NOTE` → **Metodología / prueba estadística / supuesto**.

Relevant prose is additionally underlined with HTML `<u>...</u>`. Tables are kept intact rather than underlined when underlining would break Markdown rendering.

The initial annotated set is restricted to articles that already have technical evidence cards in `reading_notes/`, so every highlight is traceable to an existing note. The annotated copies are generated reproducibly by `notes_on_papers/_generate.py`; do not treat them as a second physical literature library.

## Interpretation boundary

PPA is not an exogenous treatment in the current data. Do not claim PPA causally created CMAT use, persistence, habit or motivation. The manuscript studies observational persistence across a change in incentive context.
