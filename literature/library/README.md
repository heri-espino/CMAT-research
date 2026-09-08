# Canonical research library

`literature/library/` is the single shared physical source layer for the CMAT literature system.

## Contents

- `CATALOG.md` — master inventory and preferred lookup entry point.
- `articles/` — extracted/searchable Markdown, one canonical record per literature ID/version.
- `pdf/` — retained source PDFs when available.
- `references/` — separated reference lists when available.
- `PROVENANCE.md` — history of the original literature imports and consolidation.
- `AGENTS.md` — maintenance rules for this library.

There are no paper-specific source copies. General and manuscript-specific folders under `literature/` are scientific views over this shared library.

## Retrieval order

1. start from `../general/INDEX.md` or a paper-specific index under `../papers/`;
2. use `CATALOG.md` to resolve the stable literature ID;
3. read `articles/<id>.md` for efficient targeted retrieval;
4. use `references/` for citation chaining or metadata checks;
5. use the PDF for exact numbers, tables, figures, quotations, page anchors, or extraction ambiguity.

The PDF is the authoritative visual source. Extracted Docling PNG/table assets are not retained in the active library.

## Versions

Preserve genuinely distinct scholarly versions when analytically useful. Prefer the published version for citation unless documented otherwise.

## Publication boundary

This is a private research repository. Source PDFs and extraction artifacts are internal research materials and are not automatically cleared for redistribution.
