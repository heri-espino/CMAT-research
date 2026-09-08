# Agent instructions — canonical literature library

This is the physical source library, not a manuscript-specific bibliography.

## Required behavior

- Never duplicate an article simply because it is relevant to more than one paper.
- Resolve literature through the stable file stem/ID.
- Prefer Markdown first; open the PDF only for exact critical verification or when extraction is ambiguous.
- Search `references/` only for citation chaining, forward/backward bibliography work, or metadata checks.
- Assets are optional fallbacks. Do not assume every article has `assets/`.
- Preserve distinct bibliographic versions when scientifically meaningful (for example, a working paper and its published version). Do not silently collapse them.
- Do not infer missing coefficients, p-values, confidence intervals, sample sizes, effect sizes, or quotations from corrupted extraction text.
- When changing article IDs or paths, update `INDEX.md`, all thematic/paper indices, and the repository AI handoff in the same change.

## Relationship to manuscripts

The paper-specific literature folders contain indexes and editorial roles only. They must point back here. LaTeX `.bib` files belong with the manuscript under `papers/`, not inside this library.
