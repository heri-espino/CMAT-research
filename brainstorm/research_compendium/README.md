# CMAT research compendium

This directory preserves the cumulative LaTeX research record built during exploratory and manuscript-development stages of the CMAT project.

Within the current repository architecture, it is a **report-layer research/brainstorming product**: broader than any single paper and upstream of publication-specific selection, but not the current methodological authority.

## Production role

```text
root/code reusable functions
        ↓
brainstorm/research_compendium
        cumulative empirical reasoning / exploratory extensions
        ↓
papers/
        selected publication arguments
```

The compendium should preserve useful scientific reasoning even when only a subset eventually enters Paper 1, Paper 2 or another manuscript.

## Main files

- `research_compendium.tex` — main LaTeX source.
- `research_compendium.pdf` — compiled cumulative report.
- `referencias.bib` — working bibliography retained for reuse.
- `figures/` — figures inherited from the corresponding historical analysis outputs.
- `new_section.tex` — additive analyses on visit-group pooling, robust comparisons and degree-programme heterogeneity.
- `ppa_progression_analysis.tex` — additive longitudinal PPA1 → Calculus chapter.

## Scientific role

The compendium preserves important historical results and reasoning, including:

- the original RQ structure for CMAT use and academic performance;
- additive 1–2 visit pooling/equivalence work;
- Welch ANOVA, Games–Howell and classroom-clustered robustness;
- degree-programme use/performance analyses;
- refined PPA1 → MU → Calculus longitudinal analysis, including the N=3,241 primary progression cohort and 3-versus-4+ persistence contrast.

A classroom is professor × same course × same academic period. In the MU cohort the course is fixed, so operationally this is professor × period.

## Code boundary

This report does not yet have an atomic computational runner. When one is added, use:

```text
brainstorm/research_compendium/code/
```

for the **thin entry point only**. Reusable scientific functions must remain under `../../cmat_analysis/src/cmat_analysis/`; do not reconstruct or copy estimators into this report folder merely to make it self-contained.

## Historical provenance

This material originated from the development line formerly labelled `v8`. That label is useful only when tracing provenance and should not be used as the active report name now that Git provides version history.

The later methodology-focused corrections and extensions are documented separately in `../methodology_report/`. The two historical development lines still require scientific reconciliation in root code before journal submission.

## Compilation

At present, compilation remains a presentation-only operation:

```bash
cd brainstorm/research_compendium
pdflatex research_compendium.tex
pdflatex research_compendium.tex
```

Do not interpret this LaTeX compilation command as a reproducible scientific runner; the report has not yet been wired end-to-end to root code.
