# Literature retrieval policy for Bib2

Bib2 is intentionally optimized for text-first retrieval with the source PDF as the final visual/source-of-truth fallback. This batch does **not** contain Docling PNG/table/figure assets.

1. Start with `INDEX.md` and identify only the record(s) relevant to the current question.
2. Read/search only the targeted `extracted/*.md` files; do not load the whole corpus into context.
3. Search `references/*.references.md` only for citation chaining, bibliography verification, or related-work discovery.
4. If an exact table value, graph, formula, coefficient, p-value, confidence interval, sample size, or effect size is unclear or corrupted in Markdown, inspect the corresponding source PDF directly.
5. Do not infer exact numerical information from a corrupted extraction.
6. Generic extraction imperfections such as ligature spacing can be interpreted normally, but material ambiguity should trigger PDF verification.
7. `kahu_2018_student-engagement-educational-interface` is a documented exception: Bib2 contains a Markdown source copy rather than a source PDF. For exact bibliographic verification, use the original publication/source when available.

Retrieval chain for this batch:

`INDEX.md -> extracted Markdown -> separated references when needed -> source PDF`
