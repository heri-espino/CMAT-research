# Paper 1 — annotated source Markdown

This folder contains **generated, full-text reading copies** of the canonical extracted Markdown articles used most directly in Paper 1.

The canonical physical/source layer remains in `../../../../literature/library/`. These files are **derived annotations**, not new source records and not a replacement for the source PDF.

## Visual convention

GitHub-native alerts are used because they remain visible without custom CSS:

> [!IMPORTANT]
> **1 · IDEA PRINCIPAL** — the source passage carrying a main conceptual claim used in Paper 1.

> [!TIP]
> **2 · RESULTADO NUMÉRICO** — a source passage/table containing a result, effect size, test statistic, sample quantity or other numerical evidence.

> [!NOTE]
> **3 · METODOLOGÍA / PRUEBA / SUPUESTO** — design, statistical method, identification condition, measurement definition or explicit assumption.

Prose passages are additionally wrapped with `<u>...</u>`. Tables/code blocks are not underlined because doing so can break Markdown rendering.

## Scope

The initial collection is intentionally restricted to articles that already have technical evidence cards in `../reading_notes/`. This keeps every annotation traceable to an existing Paper 1 note.

`INDEX.md` lists the generated papers and annotation counts.

## Regeneration

Run from the repository root:

```bash
python literature_selected/notes_on_papers/_generate.py --write
```

Validation without writing:

```bash
python literature_selected/notes_on_papers/_generate.py --check
```

Do not hand-edit generated article copies. If an annotation is wrong or incomplete, edit `_generate.py` or the underlying technical reading note and regenerate.

## Citation rule

Use these copies for **reading/navigation**. For manuscript quotations, page-specific claims, tables, or final numerical verification, return to the canonical Markdown and source PDF.
