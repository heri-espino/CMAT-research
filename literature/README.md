# Literature

The active literature architecture is organized by scientific use, not by ingestion batch.

```text
literature/
├── library/          # one physical canonical copy of each work/version
├── general/          # cross-project thematic map
└── papers/
    ├── paper1_ppa_persistence/
    └── paper2_mu_performance/
```

Historical folders named `Bib`, `Bib2`, and `Bib2-2` are migration artifacts preserved in Git history only. Future work must not recreate them.

## Key principle

**Store once, index many times.** A paper relevant to both manuscripts stays once in `library/` and is referenced from both paper-specific indices.

## Retrieval

1. Start with `general/INDEX.md` for a broad project question, or a paper-specific `papers/.../INDEX.md` for manuscript work.
2. Resolve the stable literature ID in `library/articles/`.
3. Use separated references only for citation chaining/metadata verification.
4. Use a targeted archived asset if it exists and materially helps; otherwise consult the PDF for exact/visual verification.
5. Do not load the whole corpus into context.

See `AGENTS.md` and `AI_HANDOFF.md` before restructuring or adding literature.
