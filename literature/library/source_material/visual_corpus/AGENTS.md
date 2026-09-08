# Literature retrieval policy for Bib/

The files in this directory are optimized to minimize context usage while preserving a
high-fidelity fallback path.

1. Start with `Bib/INDEX.md` and identify only the papers relevant to the current question.
2. Search/read `Bib/extracted/*.md` as the primary literature corpus; do not load the full
   corpus into context at once.
3. `Bib/references/` is intentionally separated from the main corpus. Search it only for
   citation chaining, bibliography verification, or related-work discovery.
4. If an exact table value, graph, or visually encoded result is unclear in Markdown, inspect
   the specific PNG under `Bib/assets/<paper>/tables/` or `figures/` before opening the PDF.
5. Treat `Bib/pdf/*.pdf` as the source of truth and open it only when Markdown + targeted
   assets are insufficient or when a critical exact value needs final verification.
6. Do not infer a numerical coefficient, p-value, confidence interval, sample size, or effect
   size from a corrupted extraction. Verify it against a visual asset or the PDF.
7. Generic extraction imperfections such as ligature spacing can be interpreted normally,
   but material corruption should trigger the visual/PDF fallback path.
