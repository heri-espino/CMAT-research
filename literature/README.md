# Literature

This subsystem contains the shared physical literature library and cross-project literature maps. Paper-specific literature work is co-located with each paper under `../papers/<paper_id>/literature/`.

## Structure

- `library/` — canonical Markdown/PDF/reference library and master catalogue.
- `general/` — cross-project conceptual literature map.
- `AI_HANDOFF.md` — literature continuity for future sessions.
- `AGENTS.md` — maintenance/retrieval rules.
- `../papers/<paper_id>/literature/` — manuscript-specific literature indices, gap trackers, reading guides and technical reading notes.

There is intentionally **no `literature/papers/` hierarchy**. One paper has one canonical home under `papers/`.

Canonical publication strategy: `../docs/PUBLICATION_PORTFOLIO.md`.

## Core rule

One scholarly source/version has one physical library record. It may be referenced by `general/` and several paper-local literature views without duplication.

The physical corpus stays here:

```text
literature/library/
├── articles/
├── pdf/
├── references/
└── CATALOG.md
```

Paper-specific interpretation stays with the paper:

```text
papers/<paper_id>/literature/
```

Do not copy source PDFs into paper folders solely because a paper cites them.

## Retrieval order

1. If the question is paper-specific, start from `../papers/<paper_id>/literature/INDEX.md` (and a `READING_GUIDE.md` when present).
2. If the question is cross-project, start from `general/INDEX.md`.
3. Resolve source IDs through `library/CATALOG.md`.
4. Read targeted Markdown in `library/articles/`.
5. Use `library/references/` for citation chaining.
6. Consult the source PDF for exact or visual verification.

Extracted figure/table assets are intentionally not retained in the active library; the PDF is the visual authority.

## Publication boundary

The repository is private. Source PDFs and extraction artifacts are internal research materials and are not automatically redistributable in a public release.
