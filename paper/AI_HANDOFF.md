# Paper 4 LaTeX AI handoff

This file defines the LaTeX conventions for Paper 4 so future AI-assisted edits do not reintroduce formatting or reproducibility problems.

## Source architecture

- `manuscript.tex` is the canonical manuscript aggregator; substantive prose is split by major section under `sections/` so edits remain manageable.
- `main.tex` is the **official clean version** and sets `\PaperCommented=0` before including `manuscript.tex`.
- `main_commented.tex` is the **development version** and sets `\PaperCommented=1`, making `\draftnote{...}` TODO annotations visible.
- Never maintain two independent official/commented copies of the manuscript prose. Edit the appropriate file under `sections/`; both outputs include the same section files.
- `references.bib` is the sole bibliography database for this paper.

## Page and typography conventions

- Use A4 paper at 11 pt.
- Keep the explicit 1.8 cm margins unless a target journal template later supersedes them.
- The manuscript uses Latin Modern/Computer Modern through LaTeX. Do not commit or distribute font files.
- Author name: `Heriberto Espino-Montelongo`.
- Affiliation: `Universidad de las Américas Puebla` unless journal anonymization rules require removal.

## Citations and cross-references

- References are numeric. Use `natbib` with `[numbers,sort&compress]` and `unsrtnat`; do not depend on `IEEEtranN.bst` unless the CI toolchain is explicitly extended to install it.
- Use `\citep{key}` for ordinary numbered citations. Avoid `\citeyearpar` in this numeric manuscript.
- Load `hyperref` before `cleveref`.
- Prefer `\cref{...}` or `\Cref{...}` for equations, tables, figures, sections, and appendices. Do not write `Table~\ref{...}`, `Figure~\ref{...}`, or `Equation~\ref{...}` manually.
- Use semantic labels: `eq:...`, `tab:...`, `fig:...`, `sec:...`, `app:...`.

## Mathematics

- Every standalone/displayed mathematical expression must be in a numbered, referenceable environment, normally `equation`; use `align` only when genuinely necessary for multiple aligned lines.
- Every displayed equation must have a `\label{eq:...}` and should be introduced or discussed using `\cref`/`\Cref` whenever a textual reference is useful.
- Do not use `\[ ... \]`, `$$ ... $$`, or unnumbered display environments for manuscript mathematics.
- Short mathematical notation that belongs grammatically inside prose (for example `$p<.001$`, `$R^2$`, `$Z$`, or `$N=6627$`) remains inline; do not turn routine inline statistics into separate display equations.

## Tables and appendices

- Wide descriptive tables belong in the appendix rather than being squeezed into the main text.
- Use `pdflscape` with a `landscape` environment for tables that would otherwise overrun the A4 text block; keep the table itself as a normal `table` float so the PDF page carries landscape orientation metadata.
- Main-text prose may cite appendix tables with `\Cref{tab:...}`; forward references are allowed.
- Do not shrink tables to illegible font sizes merely to avoid overfull boxes.

## TODO annotations

- Put manuscript-development tasks inside `\draftnote{...}` in the relevant file under `sections/`.
- TODOs are visible only in `main_commented.pdf`; the official `main.pdf` must remain annotation-free.
- Do not weaken the interpretation constraints in `DRAFT_NOTES.md`: CMAT use is a formal help-seeking trace, not latent engagement; non-use is not disengagement; historical instructor outcomes are not intrinsic instructor difficulty/quality; and the analyses are observational.

## Figures

- Shared Matplotlib/Seaborn styling lives in `cmat_analysis.visualization.style`.
- Prefer Seaborn `whitegrid` with `context="paper"`.
- Font resolution should prefer `CMU Serif`, then `Latin Modern Roman`, then the bundled `DejaVu Serif`; mathematics should use Matplotlib's Computer Modern mathtext (`mathtext.fontset="cm"`). This makes plots reproducible even when CMU is not installed on CI.
- Do not commit or share font files.
- Keep figure generation separate from scientific estimand construction; style code must never alter cohorts or calculations.

## Build and verification

- `python paper/build.py` must compile both `main.pdf` and `main_commented.pdf`.
- Before merging manuscript changes, check that BibTeX resolves all citations, cleveref resolves all labels, and the log has no material overfull boxes.
- Visually inspect both PDFs after any layout change, especially landscape appendix tables.
