# AI handoff — reports as reproducible research workspaces

This file is the canonical operating guide for future AI sessions working inside `reports/`.

## Core mental model

Treat root `code/` as the project's internal scientific library, analogous in architectural role to a package such as scikit-learn: it owns reusable computational behavior. Treat `reports/` as reproducible research workspaces that import that library to test questions, compare specifications, preserve diagnostics, and build scientific arguments. Treat `papers/` as the downstream publication layer that selects validated evidence from those reports.

```text
code/
= reusable scientific library

reports/
= experiments + diagnostics + robustness + brainstorming + broad synthesis

papers/
= curated publication argument
```

The analogy does not mean root code must be generic to all researchers. CMAT-specific functions belong in root code whenever they define a calculation that should have one canonical implementation.

## Non-negotiable boundary

A report may own a `code/` folder, but that folder is **orchestration only**.

Allowed in `reports/<report_id>/code/`:

- imports from `code/src/visitas_analysis/`;
- report-specific CLI arguments;
- controlled input-path resolution;
- configuration selection;
- execution order;
- report-specific staging/build decisions;
- calls to LaTeX/report compilation helpers.

Not allowed there:

- a new cohort implementation;
- a copied estimator;
- a report-specific version of an existing statistical test;
- duplicated imputation or transformation logic;
- a reusable plotting implementation;
- scientific constants that should be shared/configured centrally;
- hidden calculations producing manuscript numbers.

If the local runner starts accumulating reusable functions, move those functions upstream into root `code/` and test them there.

## Mandatory startup for report work

Before changing an existing report:

1. read root `AI_HANDOFF.md`;
2. read `docs/RESEARCH_WORKFLOW.md`;
3. read this file;
4. read `code/.ai_handoff.md`;
5. search `code/FUNCTION_INDEX.md` for the needed capability;
6. read `reports/<report_id>/README.md`;
7. inspect only the relevant root-code functions and report-local runner;
8. inspect retained tables/figures/provenance before quoting old numerical results.

For a purely editorial change to report prose, root-code inspection may be unnecessary unless the edit changes or interprets numerical/scientific claims.

## Workflow for a new analysis inside a report

### 1. Define the question before coding

Record the research question, why it matters, the intended population/outcome/exposure, and important assumptions or uncertainties in the report README or `notes/`.

A report is allowed to contain unresolved ideas. Do not force every exploratory question directly into a paper.

### 2. Search root code

Search `code/FUNCTION_INDEX.md` before creating any implementation.

If the required calculation already exists, import it. If a function almost matches but differs scientifically, inspect the definition and decide whether the specification should be generalized or whether a genuinely distinct function is warranted.

### 3. Add missing reusable functions upstream

When new reusable computation is required:

1. implement it under `code/src/visitas_analysis/`;
2. document inputs, outputs, estimand/meaning, and caveats;
3. add or update tests under `code/tests/`;
4. update `code/STUDY_PROTOCOL.md` or relevant methodological documentation when the scientific specification changes;
5. regenerate `code/FUNCTION_INDEX.md`.

Only after that should the report-local runner call it.

### 4. Keep the runner readable as a recipe

A report-local runner should make it easy to answer:

- what data/configuration are used;
- what analyses run;
- in what order;
- where generated outputs go;
- which outputs are staged/retained;
- what external/historical dependencies remain.

The runner should not require reading local helper implementations to understand the scientific sequence because the calculations themselves live in root code.

### 5. Preserve the broad empirical record

Reports should retain scientifically useful information even when it will not appear in a paper, including:

- null results;
- failed/unsupported hypotheses;
- alternate specifications;
- sensitivity analyses;
- diagnostics;
- data-quality concerns;
- assumptions;
- discrepancies between cohorts;
- unresolved questions;
- interpretation boundaries.

This broad record is one of the main reasons reports exist separately from papers.

### 6. Separate generated build files from retained evidence

Prefer:

```text
reports/<report_id>/build/
= disposable/reproducible working outputs

reports/<report_id>/tables/
reports/<report_id>/figures/
= reviewed retained aggregate evidence
```

Never place raw institutional microdata inside the report for convenience.

### 7. Document each important result

For a material result, preserve enough context to recover:

- population/cohort;
- exposure/predictor;
- outcome;
- model/test;
- relevant assumptions;
- uncertainty measure;
- source output/table/figure;
- whether the result is descriptive, associational, sensitivity, or identified causally;
- whether it is currently considered suitable for a paper.

Do not rely on memory or manuscript prose as the only record of why a result was accepted.

## When an idea becomes a paper result

Promotion runs downstream only:

```text
root-code calculation
        ↓
report experiment/result
        ↓ scientific review
paper selection
```

A paper may select a subset of a report's evidence, but it should not silently modify the method or number after selection. If a paper requires a different specification, return upstream to root code + the relevant report and evaluate it there first.

A paper can have multiple source reports. One report can feed multiple papers.

## Data-update procedure

When new institutional data arrive but methodology has not changed:

1. keep the same root functions;
2. keep the same report-local runner;
3. update only controlled input paths/configuration as needed;
4. run root-code tests;
5. rerun the report;
6. compare cohort counts, diagnostics, tables and figures with the prior retained state;
7. investigate material differences;
8. accept/stage new retained outputs only after review;
9. propagate accepted changes to downstream paper(s).

A new data vintage is not a reason to create a version-suffixed script or report folder.

## Scientific-change procedure

If a cohort definition, transformation, estimand, imputation rule, model, test, standard error, threshold, confidence interval, or other result-generating rule changes:

```text
root code change
    ↓
tests + protocol + function index
    ↓
affected report runner(s)
    ↓
compare/review new evidence
    ↓
affected paper(s)
```

Never implement a methodology change only inside a report-local runner.

## Atomic report structure

Use only folders that contain real material, but the preferred structure is:

```text
reports/<report_id>/
├── README.md
├── AI_HANDOFF.md       # optional for complex report-specific state
├── code/               # thin local entry point(s)
├── notes/              # questions, reasoning, interpretation
├── tables/             # retained aggregate evidence
├── figures/            # retained aggregate evidence
├── provenance/         # report-specific history/fingerprints/protocol snapshots
├── build/              # disposable, ignored
├── <report_id>.tex
└── <report_id>.pdf
```

Do not add empty folders merely for symmetry.

## Current canonical example

`reports/methodology_report/` demonstrates the intended boundary.

Local entry point:

```bash
python reports/methodology_report/code/methodology_report.py --check
```

That file contains only path/bootstrap logic and invokes root-code build orchestration. The actual scientific implementation remains in `code/src/visitas_analysis/`.

## Creating a new report

Create a new report when an analysis direction is substantive enough to need its own persistent research record, not simply because one more function or figure is needed.

Use a purpose-based stable name, for example:

- `grading_heterogeneity_report/`
- `degree_help_seeking_report/`

Avoid:

- `report_v2/`;
- `report_new/`;
- `final_report/`;
- date-stamped active copies.

Git is the version-history layer.

A minimal new report can begin with only:

```text
reports/<report_id>/
├── README.md
├── notes/
└── code/<report_id>.py
```

provided each component contains real content. Add tables, figures, provenance, or LaTeX only as they become necessary.

## Relationship to `analysis/shared/`

Do not route every result through `analysis/shared/`. Use that directory only for aggregate objects with genuine project-wide or cross-report ownership, or for retained historical comparison/provenance.

The normal report-owned result should remain with its report.

## Relationship to literature

Reports can cite or discuss literature, but do not create duplicate physical article libraries inside reports. The physical source corpus remains in `literature/library/`. Paper-specific reading interpretation remains under each paper's `literature/` directory.

If report-level thematic literature notes become necessary, link to the shared sources rather than copying PDFs.

## Anti-pattern checklist

Before finishing report work, verify that you did **not**:

- create a reusable function inside the report;
- copy root-code logic into the report runner;
- introduce a second definition of a cohort or estimand;
- hard-code a reported result that should come from generated output;
- create a version-suffixed active report/script;
- move exploratory uncertainty directly into paper prose without preserving it in the report;
- delete null/sensitivity evidence merely because the paper does not need it;
- commit raw institutional data;
- create a new report when the work clearly belongs to an existing report.

## Handoff maintenance

Keep this file focused on report-layer workflow. Put detailed scientific state in the owning report README/notes, reusable-code rules in `code/.ai_handoff.md`, overall architecture in `docs/RESEARCH_WORKFLOW.md`, and paper-specific publication state in each paper README.

When future work reveals a better general report-development rule, update this file rather than relying on conversation memory.
