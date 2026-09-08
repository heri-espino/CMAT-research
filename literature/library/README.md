# Canonical research library

`literature/library/` is the shared source layer for the CMAT literature system.

## Contents

- `CATALOG.md` — master scientific catalogue and preferred retrieval entry point.
- `source_material/visual_corpus/` — historical source set containing PDFs, extracted Markdown, separated references and Docling visual assets.
- `source_material/pdf_markdown_corpus/` — historical source set containing PDFs, extracted Markdown and separated references; visual assets are intentionally omitted.

The two source-material folders preserve provenance of the original imports. They are not separate scientific bibliographies.

## Canonical-use rule

Use `CATALOG.md` and the paper/general indices to decide which source matters. If the same scholarly work appears in more than one source-material location, treat one record as preferred/canonical in the catalogue and preserve the alternate copy only for provenance until a later deduplication pass confirms it is safe to remove.

Do not create a parallel `articles/`, `pdf/`, or `references/` hierarchy without an intentional documented migration. The current canonical physical paths are under `source_material/`.

## Retrieval order

1. start from `../general/INDEX.md` or a paper-specific index under `../papers/`;
2. use `CATALOG.md` to locate the preferred record and source-material path;
3. read only the relevant extracted Markdown sections;
4. use separated references only for citation chaining or bibliographic verification;
5. if an exact numerical value, table, figure, or wording is uncertain, consult the source PDF;
6. use visual assets only where available and necessary;
7. do not load the whole library into context.

## Identifiers and versions

File stems function as stable literature IDs such as `author_year_short-topic`. Keep genuinely distinct scholarly versions (for example working paper vs published article) separately when analytically useful, while recording which is preferred for citation.

## Publication boundary

The repository is private. Source PDFs and extraction artifacts are internal research materials and are not automatically cleared for redistribution. Public releases should normally expose manuscript bibliography/DOIs/metadata rather than this private PDF corpus.
