# Canonical literature library

This directory is the single physical literature store for the CMAT research programme.

## Rule: one work, one canonical record

Do not create separate physical copies for Paper 1, Paper 2, or general literature. A work is stored once here and can be referenced by any number of thematic or manuscript-specific indices.

## Contents

- `articles/`: canonical Markdown/article extractions used for text-first retrieval.
- `pdf/`: source PDFs available for exact or visual verification. PDFs are internal research material in this private repository and are not automatically redistributable.
- `references/`: separated reference lists when available, used for citation chaining and bibliographic verification.
- `assets/`: Docling visual assets retained only for works for which they were already archived. The later literature expansion intentionally omitted redundant assets; absence of an asset is not an error when a source PDF is available.
- `INDEX.md`: complete canonical inventory.
- `PROVENANCE.md`: migration and version notes.

## Retrieval order

1. Start from `../general/INDEX.md` or a paper-specific index under `../papers/`.
2. Read only the relevant `articles/<id>.md` files.
3. Use `references/<id>.references.md` only when citation chaining or bibliographic verification is needed.
4. If an exact numerical value, table, figure, or wording is uncertain, use a targeted asset when it exists; otherwise consult the source PDF.
5. Do not load the whole library into context.

## Canonical identifiers

File stems are stable literature IDs of the form `author_year_short-topic`. Paper-specific indices should link to these IDs rather than inventing alternative names.
