# Literature

Private literature corpus, technical indices and citation notes for the CMAT research project.

## Heavy corpus

- `Bib/`: Batch 1. Includes PDFs, Docling Markdown, separated references and retained PNG/table/figure assets.
- `Bib2/`: Batch 2. Includes 30 extracted Markdown records, 29 source PDFs and 24 separated reference files. **No visual assets are retained in Bib2 by design.**

## Retrieval rule

Always start with the batch `INDEX.md`, then read only targeted Markdown. Use separated references only for citation chaining or bibliographic checks. If an exact value, formula, graph or table is ambiguous, use the source PDF as the fallback.

The retrieval chains therefore differ slightly:

- `Bib/`: index -> Markdown -> targeted asset when useful -> PDF.
- `Bib2/`: index -> Markdown -> references when needed -> PDF.

Do not load either full corpus unnecessarily.

## Publication rule

This repository is private. Literature PDFs and any retained Docling assets are preserved for internal research continuity; they are not automatically redistributable in a public release.
