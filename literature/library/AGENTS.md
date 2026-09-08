# Agent instructions — canonical literature library

This is the physical source library, not a manuscript-specific bibliography.

## Required behavior

- Never duplicate an article because it is relevant to more than one paper.
- Resolve works through the stable file stem/ID and `CATALOG.md`.
- Prefer `articles/<id>.md` for efficient reading; open `pdf/<id>.pdf` for exact critical verification or extraction ambiguity.
- Use `references/` for citation chaining and bibliographic verification.
- Do not regenerate or archive extracted figure/table assets by default; the source PDF is the visual authority.
- Preserve distinct scholarly versions when scientifically meaningful.
- Never infer missing coefficients, p-values, confidence intervals, sample sizes, effect sizes, or quotations from corrupted extraction text.
- When changing IDs or canonical paths, update `CATALOG.md`, every affected thematic/paper view, reading-note anchors, and the literature AI handoff.

## Adding a work

Add the canonical Markdown record to `articles/`, the source PDF to `pdf/` when available/appropriate, and a separated reference list to `references/` when useful. Then update `CATALOG.md` and every relevant scientific view.

## Relationship to manuscripts

Paper-specific literature folders contain indices, gap tracking and technical reading notes only. LaTeX `.bib` files belong with manuscripts under root `papers/`.
