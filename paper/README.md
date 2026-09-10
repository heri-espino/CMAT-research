# Paper 1 manuscript

This directory contains the first formal Paper 1 draft.

## Main files

- `main.tex` — English manuscript draft.
- `references.bib` — paper-local bibliography used by the draft.
- `build.py` — cross-platform build wrapper; packaging/orchestration only, with no scientific calculations.

## Current status

This is a **research draft, not a submission-ready manuscript**. The central contribution and main longitudinal results are sufficiently developed for a full paper structure, but several methodological/reproducibility items remain deliberately marked in bold as `Draft-development note` items inside the manuscript.

The current ambitious target remains *Studies in Higher Education*. The draft is therefore framed around a broader higher-education question—persistence in formal academic help-seeking across a change in institutional incentive context—rather than as a local evaluation of a mathematics centre.

## Numerical traceability

Primary Paper 1 estimates currently come from the retained refined longitudinal analysis under:

- `../../../brainstorm/shared/historical_outputs/study/tables/101_ppa_behavior_profiles.csv`
- `../../../brainstorm/shared/historical_outputs/study/tables/102_ppa_persistence_by_mu_group.csv`
- `../../../brainstorm/shared/historical_outputs/study/tables/103_ppa_persistence_omnibus.csv`
- `../../../brainstorm/shared/historical_outputs/study/tables/104_ppa_exact3_vs_4plus_persistence.csv`
- `../../../brainstorm/shared/historical_outputs/study/tables/105_ppa_persistence_logistic_models.csv`
- `../../../brainstorm/shared/historical_outputs/study/tables/106_ppa_piecewise_threshold_persistence.csv`
- `../../../brainstorm/shared/historical_outputs/study/tables/107_ppa_later_performance_models.csv`

The longitudinal cohort construction and interpretation are also documented in:

- `../../../brainstorm/research_compendium/ppa_progression_analysis.tex`
- `../../../brainstorm/methodology_report/README.md`

The figure currently used by `main.tex` is the retained refined longitudinal snapshot:

- `../../../brainstorm/methodology_report/figures/refined_longitudinal_persistence_3241.png`

Do not manually alter manuscript numbers after a data update. Re-run the relevant longitudinal analysis once it is reintegrated into the canonical executable pipeline, compare generated outputs, and then update the prose from those outputs.

## Literature traceability

Paper-specific evidence selection and technical reading notes live in `../literature/`. Physical source records remain in `../../../literature/library/`.

The draft intentionally uses several *Studies in Higher Education* anchors already present in the project corpus, including Kahu (2013), van Herpen et al. (2020), Bowden et al. (2021), Blondeel et al. (2024), B\"uchele and Sch\"urmann (2024), and Felby et al. (2026).

## Build

The manuscript is validated in GitHub Actions on a clean TeX Live installation with Git LFS assets materialized. The preferred local build is the cross-platform wrapper, which can be invoked from the repository root or from any other working directory:

```bash
python paper/build.py
```

The wrapper always compiles with `manuscript/` as the working directory, so the bibliography and external figure paths resolve consistently. It first checks that the required figure is a real PNG rather than a Git LFS pointer.

### First-time local setup

Because report figures are stored with Git LFS, install/initialize LFS and materialize the binary assets before compiling:

```bash
git lfs install
git lfs pull
```

If `build.py` reports that `refined_longitudinal_persistence_3241.png` is still an LFS pointer, rerun `git lfs pull` from the repository root.

You also need a LaTeX distribution providing `latexmk` (recommended), or at minimum both `pdflatex` and `bibtex`. The wrapper uses `latexmk` when available and otherwise falls back to:

```text
pdflatex -> bibtex -> pdflatex -> pdflatex
```

### Direct LaTeX build

If you prefer to compile manually, run the commands **from this manuscript directory**:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

or:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Do not run plain `pdflatex paper/main.tex` from the repository root without changing directories, because the manuscript currently uses report-relative figure paths and a paper-local bibliography. Use `build.py`, `latexmk -cd`, or `cd papers/paper1_ppa_persistence/manuscript` first.

## Continuous compilation check

`.github/workflows/compile-paper1.yml` checks out Git LFS assets and compiles Paper 1 whenever the manuscript or its retained persistence figure changes. A passing workflow therefore verifies that the repository version of the manuscript is compilable independently of a local machine configuration.

## Must resolve before submission

1. Reintegrate and reproduce the strict `N=3,241` longitudinal analysis from the canonical code/runner.
2. Re-run the broader `N=4,211` progressor sensitivity under harmonized definitions.
3. Add a dedicated selection/attrition analysis for entry into the MU-to-Calculus cohort.
4. Use direct PPA1 completion timing if it becomes available; otherwise retain the institutional-timing assumption as an explicit limitation.
5. Add stronger pre-exposure covariates if institutionally available (for example mathematics admission/diagnostic measures).
6. Consider direct mechanism evidence (survey/qualitative) before making claims about familiarity, motivation, or perceived usefulness.
7. Conduct a journal-specific format/word-count/anonymization pass only after the scientific pipeline is frozen.
