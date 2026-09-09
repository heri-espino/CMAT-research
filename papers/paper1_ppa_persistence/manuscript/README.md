# Paper 1 manuscript

This directory contains the first formal Paper 1 draft.

## Main file

- `main.tex` — English manuscript draft.
- `references.bib` — paper-local bibliography used by the draft.

## Current status

This is a **research draft, not a submission-ready manuscript**. The central contribution and main longitudinal results are sufficiently developed for a full paper structure, but several methodological/reproducibility items remain deliberately marked in bold as `Draft-development note` items inside the manuscript.

The current ambitious target remains *Studies in Higher Education*. The draft is therefore framed around a broader higher-education question—persistence in formal academic help-seeking across a change in institutional incentive context—rather than as a local evaluation of a mathematics centre.

## Numerical traceability

Primary Paper 1 estimates currently come from the retained refined longitudinal analysis under:

- `../../../analysis/shared/historical_outputs/study/tables/101_ppa_behavior_profiles.csv`
- `../../../analysis/shared/historical_outputs/study/tables/102_ppa_persistence_by_mu_group.csv`
- `../../../analysis/shared/historical_outputs/study/tables/103_ppa_persistence_omnibus.csv`
- `../../../analysis/shared/historical_outputs/study/tables/104_ppa_exact3_vs_4plus_persistence.csv`
- `../../../analysis/shared/historical_outputs/study/tables/105_ppa_persistence_logistic_models.csv`
- `../../../analysis/shared/historical_outputs/study/tables/106_ppa_piecewise_threshold_persistence.csv`
- `../../../analysis/shared/historical_outputs/study/tables/107_ppa_later_performance_models.csv`

The longitudinal cohort construction and interpretation are also documented in:

- `../../../reports/research_compendium/ppa_progression_analysis.tex`
- `../../../reports/methodology_report/README.md`

The figure currently used by `main.tex` is the retained refined longitudinal snapshot:

- `../../../reports/methodology_report/figures/refined_longitudinal_persistence_3241.png`

Do not manually alter manuscript numbers after a data update. Re-run the relevant longitudinal analysis once it is reintegrated into the canonical executable pipeline, compare generated outputs, and then update the prose from those outputs.

## Literature traceability

Paper-specific evidence selection and technical reading notes live in `../literature/`. Physical source records remain in `../../../literature/library/`.

The draft intentionally uses several *Studies in Higher Education* anchors already present in the project corpus, including Kahu (2013), van Herpen et al. (2020), Bowden et al. (2021), Blondeel et al. (2024), B\"uchele and Sch\"urmann (2024), and Felby et al. (2026).

## Build

From this directory, a normal BibTeX build is:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The external figure path assumes the repository layout remains intact.

## Must resolve before submission

1. Reintegrate and reproduce the strict `N=3,241` longitudinal analysis from the canonical code/runner.
2. Re-run the broader `N=4,211` progressor sensitivity under harmonized definitions.
3. Add a dedicated selection/attrition analysis for entry into the MU-to-Calculus cohort.
4. Use direct PPA1 completion timing if it becomes available; otherwise retain the institutional-timing assumption as an explicit limitation.
5. Add stronger pre-exposure covariates if institutionally available (for example mathematics admission/diagnostic measures).
6. Consider direct mechanism evidence (survey/qualitative) before making claims about familiarity, motivation, or perceived usefulness.
7. Conduct a journal-specific format/word-count/anonymization pass only after the scientific pipeline is frozen.
