# CMAT research compendium

This directory preserves the cumulative LaTeX research record built during the exploratory and manuscript-development stages of the CMAT project.

It is intentionally broader than any single paper and should be read as a research compendium rather than as the current methodological authority.

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
- the additive 1–2 visit pooling/equivalence work;
- Welch ANOVA, Games–Howell and classroom-clustered robustness;
- degree-programme use/performance analyses;
- the refined PPA1 → MU → Calculus longitudinal analysis, including the N=3,241 primary progression cohort and the 3-versus-4+ persistence contrast.

A classroom is professor × same course × same academic period. In the MU cohort the course is fixed, so operationally this is professor × period.

## Historical provenance

This material originated from the development line formerly labelled `v8`. That label is useful only when tracing provenance and should not be used as the active report name now that Git provides version history.

The later methodology-focused corrections and extensions are documented separately in `../methodology_report/`. The two historical development lines still require scientific reconciliation in the active canonical pipeline before journal submission.

## Compilation

```bash
pdflatex research_compendium.tex
pdflatex research_compendium.tex
```

For routine QA, compilation/log validation is sufficient unless a layout problem or explicit visual-review request requires page inspection.
