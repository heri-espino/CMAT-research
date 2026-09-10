# Paper 1 manuscript

This directory contains the first formal Paper 1 draft.

## Main files

- `main.tex` — English manuscript draft.
- `references.bib` — paper-local bibliography used by the draft.
- `build.py` — cross-platform build wrapper; packaging/orchestration only, with no scientific calculations.
- `FIGURE_INVENTORY.md` — audit, provenance and replacement map for manuscript figures.

## Current status

This is a **research draft, not a submission-ready manuscript**. The central contribution and main longitudinal results are sufficiently developed for a full paper structure, but several methodological/reproducibility items remain deliberately marked in bold as `Draft-development note` items inside the manuscript.

The current ambitious target remains *Studies in Higher Education*. The draft is framed around a broader higher-education question—persistence in formal academic help-seeking across a change in institutional incentive context—rather than as a local evaluation of a mathematics centre.

## Reproducible analysis

Paper-specific scientific orchestration lives in `../code/run_paper.py`. Paper-specific figure presentation lives in `../code/figures.py`. Reusable scientific functions remain in the shared `cmat_analysis` package.

From the repository root:

```bash
python -m pip install -e './cmat_analysis[dev]'
python code/run_paper.py --check
```

With controlled local inputs:

```bash
python code/run_paper.py \
  --materias '/path/to/Materias.xlsx' \
  --asesorias '/path/to/Asesorias.xlsx' \
  --compare-retained
```

The runner rebuilds the strict next-regular-term MU-to-Calculus cohort and aggregate tables 98--107 under `../results/`, generates the four English manuscript figures from those aggregate tables, then optionally compares tables 101--107 against the retained historical snapshot. A comparison failure must be reviewed before manuscript numbers are changed.

## Numerical traceability

The current draft was written from the retained refined longitudinal analysis under:

- `../brainstorm/shared/historical_outputs/study/tables/98_ppa_progression_cohort_flow.csv`
- `../brainstorm/shared/historical_outputs/study/tables/101_ppa_behavior_profiles.csv`
- `../brainstorm/shared/historical_outputs/study/tables/102_ppa_persistence_by_mu_group.csv`
- `../brainstorm/shared/historical_outputs/study/tables/103_ppa_persistence_omnibus.csv`
- `../brainstorm/shared/historical_outputs/study/tables/104_ppa_exact3_vs_4plus_persistence.csv`
- `../brainstorm/shared/historical_outputs/study/tables/105_ppa_persistence_logistic_models.csv`
- `../brainstorm/shared/historical_outputs/study/tables/106_ppa_piecewise_threshold_persistence.csv`
- `../brainstorm/shared/historical_outputs/study/tables/107_ppa_later_performance_models.csv`

The longitudinal cohort construction and interpretation are also documented in:

- `../brainstorm/research_compendium/ppa_progression_analysis.tex`
- `../brainstorm/methodology_report/README.md`

The pre-update manuscript used the retained historical figure:

- `../brainstorm/methodology_report/figures/refined_longitudinal_persistence_3241.png`

That binary remains preserved for provenance but is no longer used by `main.tex`. The manuscript now uses four paper-owned figures regenerated from reviewed aggregate tables:

- `../results/figures/figure_01_cohort_flow.png`
- `../results/figures/figure_02_main_persistence.png`
- `../results/figures/figure_03_threshold_piecewise.png`
- `../results/figures/figure_04_adjusted_persistence_or.png`

Direct manuscript builds regenerate those figures from the retained aggregate snapshot, so the draft can be compiled without private microdata and without relying on the historical Spanish-labelled PNG. A full empirical run generates the same figure set from the new aggregate tables; `--compare-retained` remains the numerical gate before manuscript numbers should be revised.

Do not manually alter manuscript numbers or figure values after a data update. Re-run `code/run_paper.py`, inspect `results/`, compare against retained outputs when appropriate, and then update prose/tables from reviewed generated outputs.

## Literature traceability

Paper-specific evidence selection and technical reading notes live in `../literature_selected/`. Physical source records remain in `../literature/library/`.

The draft intentionally uses several *Studies in Higher Education* anchors already present in the project corpus, including Kahu (2013), van Herpen et al. (2020), Bowden et al. (2021), Blondeel et al. (2024), Büchele and Schürmann (2024), and Felby et al. (2026).

## Build

The preferred local build is the cross-platform wrapper, which can be invoked from the repository root or from any other working directory:

```bash
python paper/build.py
```

`build.py` first calls `code/figures.py --source retained`, validates the four generated PNGs, and then compiles with `paper/` as the working directory so the bibliography and external figure paths resolve consistently. The generated figure files live under `results/figures/` and should not be hand-edited.

If a full empirical run invokes `code/run_paper.py --compile`, the runner sets the figure source to `generated`, so compilation uses the aggregate tables created by that same run rather than the retained snapshot.

You need a LaTeX distribution providing `latexmk` (recommended), or at minimum both `pdflatex` and `bibtex`. The wrapper uses `latexmk` when available and otherwise falls back to:

```text
pdflatex -> bibtex -> pdflatex -> pdflatex
```

### Direct LaTeX build

If you prefer to compile manually, first generate the figures and then compile from `paper/`:

```bash
python code/figures.py --source retained
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

or use the `pdflatex`/`bibtex` sequence after figure generation. Prefer `python paper/build.py` because it enforces the figure-generation step automatically.

## Must resolve before submission

1. Reproduce the strict `N=3,241` longitudinal analysis with `code/run_paper.py` and controlled current inputs, then inspect any divergence from the retained snapshot.
2. Re-run the broader `N=4,211` progressor sensitivity under harmonized definitions.
3. Add a dedicated selection/attrition analysis for entry into the MU-to-Calculus cohort.
4. Use direct PPA1 completion timing if it becomes available; otherwise retain the institutional-timing assumption as an explicit limitation.
5. Add stronger pre-exposure covariates if institutionally available (for example mathematics admission/diagnostic measures).
6. Consider direct mechanism evidence (survey/qualitative) before making claims about familiarity, motivation, or perceived usefulness.
7. Conduct a journal-specific format/word-count/anonymization pass only after the scientific pipeline is frozen.
