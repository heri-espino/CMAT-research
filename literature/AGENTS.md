# Agent instructions — literature subsystem

## Architecture

`library/` is the only physical literature store. `general/` and `papers/` are semantic/editorial indexes. Never duplicate source Markdown/PDFs across those layers.

## Adding a new work

1. Choose a stable ID: `author_year_short-topic`.
2. Add the article Markdown to `library/articles/<id>.md`.
3. Add a source PDF to `library/pdf/<id>.pdf` when available/appropriate for this private repository.
4. Add `library/references/<id>.references.md` if a separated reference list is available.
5. Add assets only when they already exist or are genuinely needed; do not regenerate hundreds of images merely for archival completeness.
6. Update `library/INDEX.md`.
7. Classify the work in `general/INDEX.md`.
8. If relevant, add its editorial role to Paper 1 and/or Paper 2 index. Never make a paper-specific physical copy.
9. Update `AI_HANDOFF.md` if the new work materially changes the literature gap, target-journal fit, or manuscript logic.

## Reading order

Use `INDEX -> targeted Markdown -> separated references if needed -> targeted asset/PDF for exact verification`.

## Bibliographic versions

Keep genuinely distinct versions when scientifically useful (e.g. working paper vs published paper). Prefer the published version for manuscript citation unless there is a specific reason to cite the working paper. Document alternate copies rather than silently merging them.

## Claims

Do not make a claim stronger than the source supports. In particular, literature on incentives, nudges, tutoring, engagement, or support must not be used to convert the observational CMAT design into a causal one.

## Publication vs internal archive

The GitHub repository is private. Source PDFs are internal research material and are not automatically cleared for redistribution. A public release should normally publish manuscript bibliography/DOIs/metadata, not this private PDF library.
