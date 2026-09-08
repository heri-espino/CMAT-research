# Canonical research library

`literature/library/` is the source layer for the CMAT literature system.

## Contents

- `CATALOG.md`: master scientific catalogue and preferred retrieval entry point.
- `source_material/visual_corpus/`: historical source set containing PDFs, extracted Markdown, separated references and Docling visual assets.
- `source_material/pdf_markdown_corpus/`: historical source set containing PDFs, extracted Markdown and separated references; visual assets are intentionally omitted.

The two source-material folders preserve provenance of the original imports. They are not separate scientific bibliographies.

## Canonical-use rule

Use `CATALOG.md` and the paper/general indices to decide which source matters. If the same scholarly work appears in more than one source-material location, treat one record as canonical in the catalogue and preserve the alternate copy only for provenance until a later deduplication pass confirms it is safe to remove.

## Retrieval

Prefer extracted Markdown for normal reading. Use source PDFs for exact verification. Use visual assets only where available and necessary.
