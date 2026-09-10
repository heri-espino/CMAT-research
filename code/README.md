# Code

Canonical reusable scientific/computational core for the CMAT project.

## Role

`code/` owns **functions and shared pipelines**, not report or paper ownership. Historical copies, report-local recipes, manuscripts and generated report assets do not belong here.

The production boundary is:

```text
controlled data
    ↓
root/code
    reusable scientific functions + shared pipelines
    ↓ imported by
reports/<report_id>/code/<runner>.py
    thin product-local orchestration
    ↓
report tables / figures / notes / LaTeX
    ↓ selected into
papers/<paper_id>/
```

A reusable calculation must have one implementation in root `code/`. Report- or paper-local code may **call** that implementation but must not fork it.

## Current layout

```text
code/
├── .ai_handoff.md
├── README.md
├── FUNCTION_INDEX.md
├── README_STUDY.md
├── STUDY_PROTOCOL.md
├── ADMINISTRATIVE_QUESTIONS.md
├── config/
├── src/                        # reusable scientific library + broad project runners
├── scripts/                    # code-maintenance/documentation utilities
├── tests/
├── pyproject.toml
├── requirements.txt
├── environment.yml
├── run_analysis.bat
├── run_study.bat
└── run_study.sh
```

There is intentionally **no `code/experiments/` layer**. Product-specific orchestration is co-located with the product that owns it.

## Reusable-code rule

Before creating a Python function:

1. read `.ai_handoff.md`;
2. search `FUNCTION_INDEX.md` by capability, likely name and tags;
3. inspect the most relevant implementation;
4. reuse or extend an existing scientifically equivalent function;
5. if a new reusable function is required, put it in the appropriate module under `src/visitas_analysis/`;
6. add a useful docstring and tests;
7. call it from the owning report/paper runner rather than implementing it locally;
8. regenerate `FUNCTION_INDEX.md`.

The index is generated with:

```bash
python scripts/generate_function_index.py
```

GitHub also refreshes it automatically after Python changes under `code/`.

## Product-local runner rule

A runner belongs with the product whose build recipe it defines.

Current canonical example:

```text
reports/methodology_report/
├── code/
│   └── methodology_report.py      # thin entry point
├── tables/
├── figures/
├── notes/
├── provenance/
├── methodology_report.tex
└── methodology_report.pdf
```

The entry point imports the actual implementation from root `code/`. It should not contain cohort construction, estimators, tests, transformations, model definitions or reusable plotting logic.

If another report becomes reproducible, use the same pattern under `reports/<report_id>/code/`. If a paper later needs a build/orchestration script, it may use `papers/<paper_id>/code/` under the same restriction.

## Current shared runners

These remain in root `code/` because they are broad project-level pipelines rather than one product's recipe:

- `src/run_study.py` — publication-oriented shared study runner;
- `src/run_analysis.py` — general/descriptive shared analysis runner;
- `src/generador_figuras_cli.py` — figure utility;
- `src/create_anonymized_release.py` — privacy/release utility;
- `src/prepare_release_latex.py` — release-preparation utility.

The methodology report itself is run from:

```bash
python ../reports/methodology_report/code/methodology_report.py --check
```

when the current working directory is `code/`, or from the repository root with:

```bash
python reports/methodology_report/code/methodology_report.py --check
```

## Report-build functions

Report-specific **reusable build helpers may still live in root `code/`**. For example, the methodology report uses:

- `src/visitas_analysis/study/methodology_pipeline.py` for the analysis sequence;
- `src/visitas_analysis/reporting/methodology_report.py` for LaTeX table rendering;
- `src/visitas_analysis/reporting/methodology_build.py` for report-build orchestration/validation.

The fact that a helper is report-specific does not make the report folder the right place for a reusable implementation. Root `code/` remains the computational authority.

## Data updates

When institutional data are updated, rerun the same product-local runner with the new controlled inputs. Do not create `*_v2.py`, duplicate the report folder, or copy calculations into a notebook.

A new data vintage is not a scientific change. If cohort rules, estimands, outcomes, imputation, statistical tests/models, standard errors or threshold logic change, update root `code/`, tests and protocol first, then rerun the affected reports and papers.

## Reports versus papers

`reports/` is the broad scientific-development/brainstorming layer. Reports may contain competing analyses, nulls, sensitivities and methodological discussion.

`papers/` is the publication-selection layer. Papers select validated evidence from the reports and canonical code outputs; they must not maintain independent scientific implementations.

## Historical cleanup

Older active copies such as `snapshots/`, `legacy/`, `manual/`, `reporte/` and committed `code/outputs/` were removed from the code tree because Git is the history layer and products belong outside `code/`.

The pre-cleanup working tree remains recoverable at commit `20a993d92e8cc197a9060180d8cb6a6caf2607a7`.

## Scientific cautions

- Classroom = `instructor × course × academic period` unless a reviewed methodological change explicitly replaces it.
- Student-selected CMAT use is observational; do not use causal language without an identification design that supports it.
- Do not infer motivation, habit or psychological mechanisms directly from administrative visit traces.
- Scientific-code changes require tests and corresponding methodology/protocol documentation.
- Search `FUNCTION_INDEX.md` before introducing new scientific helpers.
- Product-local runners import root functions; they do not redefine them.

## Data and output boundary

Raw administrative data and row-level linked records remain outside GitHub.

`code/outputs/` remains available for disposable outputs of broad shared pipelines. Product-specific disposable build files should live inside the owning product's ignored `build/` directory, for example `reports/methodology_report/build/`.
