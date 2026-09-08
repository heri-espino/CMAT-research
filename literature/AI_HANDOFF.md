# AI handoff — literature subsystem

This file is the starting point for future AI sessions working on CMAT literature.

## Purpose

The literature subsystem is organized by scientific use, not by upload batch. The repository exposes one research library plus lightweight scientific views for the overall project and each paper.

## Canonical layout

- `literature/library/`: source layer and master catalogue.
- `literature/library/source_material/visual_corpus/`: historical source set with PDFs, extracted Markdown, references and visual assets.
- `literature/library/source_material/pdf_markdown_corpus/`: historical source set with PDFs/Markdown/references and no visual assets by design.
- `literature/general/`: cross-project literature map and thematic notes.
- `literature/papers/paper1_ppa_persistence/`: literature view for the persistence-after-incentive paper.
- `literature/papers/paper2_mu_performance/`: literature view for the MU performance paper.

Do not recreate `Bib`, `Bib2`, `Bib3`, or other upload-batch folders as user-facing organization.

## Retrieval order

1. Read `literature/README.md`.
2. Read the relevant paper/general `INDEX.md`.
3. Use `literature/library/CATALOG.md` and source-material indices to locate the canonical record.
4. Read targeted extracted Markdown first.
5. Read separated references only for citation chaining or bibliography verification.
6. Open the source PDF when an exact table, figure, coefficient, wording, page, or extraction ambiguity matters.
7. Visual assets exist only for part of the historical corpus; never assume they exist for every paper.

## Scientific roles

### General literature

Use for concepts shared by the whole CMAT programme: mathematics support, academic help-seeking, engagement, observational inference, selection/confounding, institutional context, and measurement.

### Paper 1 — PPA persistence

Working question: whether support-seeking observed in an incentive-linked first-year context persists when the specific PPA1 incentive no longer applies. Relevant families include incentives, incentive removal, persistence, engagement, help-seeking, first-year transitions, and mathematics-support context. Do not describe PPA as an exogenous treatment and do not identify a causal PPA effect.

### Paper 2 — MU performance

Working question: association between CMAT use and classroom-relative academic performance in first Mathematics University (MU). Relevant families include mathematics/statistics support, tutoring/help-seeking, selection into support, usage intensity, academic performance, classroom adjustment, heteroskedastic inference, and observational sensitivity analysis.

## Important current interpretation rules

- One source may be indexed in general, Paper 1, and Paper 2 without duplicating the physical PDF/Markdown.
- Paper-specific folders are views/notes, not separate libraries.
- Keep published and working-paper versions separate when they are genuinely distinct scholarly versions.
- Prefer the most complete/high-fidelity extracted Markdown when true duplicates are discovered, but preserve provenance in the catalogue.
- Do not infer numerical results from corrupted extraction; verify against the PDF.
- Literature PDFs are internal research materials in this private repository and are not automatically redistributable in a public release.

## Maintenance

When adding a paper:

1. choose a stable ID such as `author_year_short-topic`;
2. place or register the source in the library source-material layer;
3. update `literature/library/CATALOG.md`;
4. add it to one or more scientific views (`general`, `paper1`, `paper2`) with a short role/priority note;
5. update the relevant `MISSING_LITERATURE.md` if the new paper fills a known gap;
6. avoid physical duplication solely because a paper supports multiple manuscripts.

When true duplicates are discovered, verify title/authors/year/DOI/content before collapsing them. Historical import provenance can remain documented in Git history and `docs/HEAVY_SNAPSHOT.md` even after duplicate working copies are removed.

When changing the literature architecture, update this handoff and `literature/AGENTS.md` in the same PR.
