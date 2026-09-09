# Code

Canonical scientific-analysis code for the CMAT project.

## Role

`code/` contains the **active executable pipeline only** plus the documentation required to understand and run it. Historical copies, notebooks, reports, and generated artifacts do not belong here; Git history is the provenance layer for those states.

## Current layout

```text
code/
├── .ai_handoff.md              # reproducibility/function/runner contract
├── README.md
├── FUNCTION_INDEX.md           # searchable AST inventory of Python symbols
├── README_STUDY.md
├── STUDY_PROTOCOL.md
├── ADMINISTRATIVE_QUESTIONS.md
├── config/
├── experiments/                # stable thin runners for specific questions/papers
├── src/                        # reusable scientific library + current broad runners
├── scripts/                    # maintenance/documentation utilities
├── tests/
├── pyproject.toml
├── requirements.txt
├── environment.yml
├── run_analysis.bat
├── run_study.bat
└── run_study.sh
```

## Reproducibility architecture

Read `code/.ai_handoff.md` before modifying Python. The core rule is:

```text
reusable scientific function
    code/src/visitas_analysis/...
        ↓ imported by
stable experiment/pipeline runner
    code/experiments/<experiment_id>.py
    or an existing canonical runner
        ↓
controlled configuration + controlled data
        ↓
regenerated outputs
```

When the institutional data are updated, the normal operation is to **rerun the same stable script**, not rewrite the analysis or create a new `*_v2.py` file. Git is the version-history layer.

`code/experiments/README.md` defines the contract for future paper/question-specific runners. Reusable cohort logic, statistics, models, transformations, and plotting logic must remain in the importable package rather than being duplicated inside those runners.

## Function index — read before adding code

`FUNCTION_INDEX.md` is the canonical low-cost search layer for the active Python tree. It is generated from the Python AST and indexes functions, classes, methods, nested helpers, signatures, line numbers, docstring summaries, and search tags. Test symbols are included separately so existing coverage can be found without treating tests as production utilities.

**Required workflow before creating a new function:**

1. read `.ai_handoff.md`;
2. search `FUNCTION_INDEX.md` by capability, keyword, or likely symbol name;
3. inspect the most relevant existing implementation and nearby helpers;
4. reuse or extend existing code where scientifically appropriate;
5. create a new symbol only when existing functionality does not cover the need;
6. give new reusable functions/classes a useful docstring and tests;
7. import the function into the stable runner that reproduces the relevant experiment/question.

The index is regenerated with:

```bash
python scripts/generate_function_index.py
```

GitHub also regenerates it automatically after changes to Python files under `code/`. Do not hand-edit the generated symbol tables; improve docstrings or `scripts/generate_function_index.py` instead.

## Current canonical runners

- `src/run_study.py` — broad publication-oriented study runner; imports `visitas_analysis.study.run_study_pipeline`.
- `src/run_analysis.py` — general/report pipeline runner; imports `visitas_analysis.pipeline.main_pipeline.run_visitas_pipeline`.

These remain canonical until a deliberate, tested refactor. New paper-specific runners should be thin importers under `experiments/`, not copies of these pipelines.

## What was intentionally removed from the working tree

The repository previously mixed active code with `snapshots/`, `legacy/`, `manual/`, `reporte/`, `LITERATURE_STARTER.md`, and committed generated outputs. These were removed from `code/` because they duplicate project history or belong to other subsystems.

- historical source states remain recoverable through Git;
- methodology-restoration provenance remains documented under `docs/` and `reports/methodology_report/`;
- legacy notebooks/manual reports remain available in Git history if ever needed;
- the previously committed aggregate outputs now live under `analysis/historical_outputs/`.

The complete pre-cleanup working tree is preserved by Git at commit `20a993d92e8cc197a9060180d8cb6a6caf2607a7`.

## Scientific caution

The active pipeline still needs a deliberate reconciliation between the refined longitudinal/PPA work and later methodology corrections documented in project provenance. Removing duplicate snapshots from the working tree does **not** imply that this reconciliation is complete.

Before changing scientific logic, inspect `.ai_handoff.md`, `FUNCTION_INDEX.md`, the implementation, tests, `STUDY_PROTOCOL.md`, `ADMINISTRATIVE_QUESTIONS.md`, `docs/MIGRATION_STATUS.md`, and the methodology report/provenance.

## Scientific rules

- Classroom = `instructor × course × academic period` unless a reviewed methodological change explicitly replaces it.
- Student-selected CMAT use is observational; do not use causal language without an identification design that supports it.
- Paper-specific code should not diverge from this canonical pipeline.
- Scientific code changes require tests and corresponding methodology/protocol documentation.
- Search `FUNCTION_INDEX.md` before introducing new scientific helpers; avoid parallel implementations of the same estimand or transformation.
- Stable experiment runners must import reusable functions rather than reimplement them.
- A new data vintage is not a reason to create a new function, runner, or version-suffixed file.

## Data boundary

Raw administrative data and row-level linked student records remain outside GitHub. Paths/configuration may refer to controlled local inputs, but those inputs must not be committed.

## Outputs

Local executions may generate `code/outputs/`; that directory is ignored by Git. Privacy-reviewed aggregate artifacts intended to be retained belong under `analysis/`.
