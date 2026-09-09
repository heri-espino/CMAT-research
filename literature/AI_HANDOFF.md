# AI handoff — literature subsystem

Compact routing guide for CMAT literature work. Detailed paper scope belongs in `papers/<paper_id>/README.md`; this file should not duplicate the publication portfolio.

## 1. Canonical ownership

Shared physical corpus:

```text
literature/library/
├── CATALOG.md
├── articles/
├── pdf/
├── references/
└── PROVENANCE.md
```

Cross-project interpretation:

`literature/general/`

Paper-specific interpretation:

`papers/<paper_id>/literature/`

There is intentionally no `literature/papers/` hierarchy.

### Core rule

**One scholarly source/version has one physical library record.** A source can be referenced by general notes and several papers without copying its PDF/Markdown into those folders.

Do not recreate `Bib`, `Bib2`, upload-batch folders, extracted asset trees, or paper-specific physical source copies.

## 2. Retrieval order

For a paper-specific literature task:

1. read `papers/<paper_id>/README.md`;
2. read `papers/<paper_id>/literature/INDEX.md`;
3. use `READING_GUIDE.md` / `reading_notes/` when present;
4. resolve source IDs in `literature/library/CATALOG.md`;
5. read targeted `literature/library/articles/*.md` sections;
6. use `literature/library/references/` only for citation chaining/bibliography verification;
7. inspect the source PDF when exact wording, table/figure values, page anchors, or extraction ambiguity matters.

For cross-project questions, start from `literature/general/INDEX.md` instead.

Do not load the whole corpus when targeted retrieval is sufficient.

## 3. Source reliability

- Extracted Markdown is the efficient reading layer.
- Source PDF is the final exact/visual verification layer.
- Separated references are secondary metadata/citation-chaining material.
- Never infer an important number from visibly corrupted extraction.
- Never invent coefficients, p-values, confidence intervals, effect sizes, sample sizes, or methods that a source does not report.
- Preserve null findings.

If a statistic is calculated by us rather than printed by the source, label it as derived and record the quantities used.

## 4. Adding a source

1. choose a stable ID such as `author_year_short-topic`;
2. add canonical Markdown once to `literature/library/articles/`;
3. add the source PDF once to `literature/library/pdf/` when available/appropriate;
4. add separated references when useful;
5. update `literature/library/CATALOG.md`;
6. update every relevant view: `literature/general/` and/or `papers/<paper_id>/literature/`;
7. update relevant `MISSING_LITERATURE.md` files;
8. create/update a technical reading note when the source materially supports an active manuscript;
9. update this handoff only if routing/library architecture materially changes.

## 5. Paper-specific literature roles

Use concise role tags where helpful:

- `core`
- `supporting`
- `methods`
- `context`
- `contrast`

Also record `used_in` and `do_not_claim` when those boundaries prevent overinterpretation.

Paper-specific scientific/editorial details should remain in the paper's own README and literature files, not here.

## 6. Paper 1 technical reading layer

Paper 1 currently has the most developed evidence-card system:

- `papers/paper1_ppa_persistence/literature/READING_GUIDE.md`
- `papers/paper1_ppa_persistence/literature/reading_notes/README.md`
- `papers/paper1_ppa_persistence/literature/reading_notes/general/`
- `papers/paper1_ppa_persistence/literature/reading_notes/incentives/`

Reading-note folders are organized by **scientific function**, never upload batch, provider, extraction method, file type, or arbitrary date.

Keep one canonical technical note per source. Cross-reference rather than duplicating a note when a source serves several conceptual roles.

Only create another reading-note category when it has a distinct manuscript-relevant purpose, several substantive sources or a committed review stream, a stable inclusion rule, and clear retrieval value.

## 7. Scientific interpretation guardrails

Across the literature subsystem:

- distinguish randomized offer/exposure from voluntary uptake/intensity;
- do not transfer causal estimates from experimental comparators onto observational CMAT attendance;
- do not infer motivation, habit, need, or psychological state solely from visit patterns;
- classroom-relative `Z` is contextual relative position, not latent mathematical proficiency;
- programme-level patterns are ecological and do not establish individual mechanisms;
- PPA is not an exogenous treatment in the current CMAT data.

Paper-specific claim boundaries belong in each paper's literature index/notes.

## 8. Publication/library separation

Paper-specific `.bib`, manuscript text, cover letters, and submission files belong under `papers/<paper_id>/`, not in `literature/`.

The literature subsystem owns source records and retrieval infrastructure; paper folders own manuscript-specific interpretation and writing.

## 9. Privacy/copyright boundary

This is a private research repository. Source PDFs are internal research materials and are not automatically redistributable in a public release.

Administrative student data must never be added to the literature subsystem.

## 10. Maintenance rule

Keep this handoff compact. When a paper title, question, target journal, empirical result, or status changes, update the owning paper/portfolio file instead of copying the change here.

Use:

- `docs/PUBLICATION_PORTFOLIO.md` — cross-paper strategy;
- `papers/<paper_id>/README.md` — detailed paper source of truth;
- `papers/<paper_id>/literature/` — paper-specific evidence view;
- `literature/library/CATALOG.md` — physical-source catalogue.
