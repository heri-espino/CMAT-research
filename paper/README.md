# Paper 2.1 — visit-frequency structure

This branch develops a denser extension of Paper 2 focused on what happens **among students who attend CMAT**, rather than stopping at the difference between zero attendance and any attendance.

Read:

- `docs/README.md` for the internal-document map;

- `docs/project/PROJECT_CONTEXT.md` for the scientific question;
- `docs/analysis/ANALYSIS_PLAN.md` for the pre-outcome analysis contract;
- `docs/project/STATUS_AND_ROADMAP.md` for current milestones;
- `docs/analysis/OUTCOME_FRAMEWORK.md` for the performance and academic-management margins;
- `docs/interpretation/ACADEMIC_MANAGEMENT_HYPOTHESIS.md` for the mechanism hypothesis and its guardrails;
- `docs/results/PRELIMINARY_RESULTS.md` for verified intermediate results;
- `docs/analysis/MIXTURE_ANALYSIS_PLAN.md` for the pre-specified density-analysis hierarchy;
- `docs/results/MIXTURE_ANALYSIS_RESULTS.md` for the complete GMM/skew-normal results, code map, validation provenance, and interpretation guardrails;
- `../literature_selected/ACCESS_NOTES.md` for source-access limitations, including the abstract-only Gokhool & Lawson citation;
- `AI_HANDOFF.md` for binding branch-specific rules.

The primary frequency grouping is now frozen as `1 / 2 / 3 / 4 / 5 / 6+` from an outcome-blind support and pair-overlap audit. `1 / 2 / 3 / 4 / 5 / 6 / 7+` is exploratory sensitivity only. See `docs/analysis/VISIT_GROUPING_DECISION.md`.

The manuscript now analyses two performance outcomes—PASS/non-PASS and the continuous imputed instructor-period-standardised grade—together with the composition of adverse outcomes, including the BV-specific academic-management contrast.

`sections/01.tex`--`04.tex` now contain the full Paper 2.1 draft. The build regenerates Paper 2.1 aggregate results and vector figures before compiling the clean and commented TEAMAT/IMA PDFs.

The distributional extension now includes a one-component skew-normal specification check against the one-Gaussian and two-Gaussian candidates. Reusable estimators live in `main/cmat_analysis`; Paper 2.1 runners contain only publication-specific orchestration.

## Build workflow

The paper now uses a dependency-aware build entry point at `paper/paper_build.py`, with table/figure orchestration isolated in `paper/paper_build_figures.py`.

Common commands:

- `python paper/paper_build.py` — compile the clean and commented PDFs, automatically generating missing figures and, when needed, their missing table inputs;
- `python paper/paper_build.py --tables` — force regeneration of the canonical Paper 2.1 aggregate tables;
- `python paper/paper_build.py --figures` — force regeneration of all vector figures, automatically rebuilding tables only if required figure inputs are absent;
- `python paper/paper_build.py --paper` (or `--pdf`) — compile PDFs, resolving missing dependencies automatically;
- `python paper/paper_build.py --tables --figures --paper` — explicit full rebuild;
- `python paper/paper_build.py --all` — shorthand for the same full rebuild;
- `python paper/paper_build.py --check` — report missing tables, figure inputs, figures, manuscript sources, and PDFs without changing files;
- `python paper/paper_build.py --paper --no-auto` — compile only when all required figures already exist, failing instead of regenerating dependencies.

The legacy `python paper/build.py` command remains available as a compatibility wrapper and delegates to `paper_build.py`. Explicit stage flags mean “rebuild this stage”; automatic rebuilding is reserved for missing upstream dependencies, so an ordinary PDF compile does not rerun the expensive mixture analysis when its figures already exist.
