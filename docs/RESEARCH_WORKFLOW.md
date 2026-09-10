# CMAT research production workflow

This document is the canonical description of **how research moves through the repository**. It records the architecture and working method so future analysis does not drift back into duplicated scripts, parallel scientific implementations, or paper-specific code forks.

## Mental model

The simplest analogy is:

```text
code/    ≈ an internal scientific library (similar in role to scikit-learn)
reports/ ≈ reproducible research workspaces that use that library
papers/  ≈ publication products that select validated evidence from reports
```

The analogy is architectural, not about generality. Functions in `code/` may be very CMAT-specific; they belong there when they define a reusable calculation, cohort, transformation, statistical procedure, model, plot, or build helper that should have one canonical implementation.

The primary production chain is therefore:

```text
controlled institutional data
        ↓
code/src/visitas_analysis/
        reusable scientific/computational library
        ↓ imported by
reports/<report_id>/code/
        thin experiment/report recipe
        ↓
reports/<report_id>/
        broad research record: tests, sensitivities, figures, tables, notes
        ↓ selected into
papers/<paper_id>/
        final manuscript argument and submission assets
```

`analysis/shared/` is optional auxiliary storage for aggregate objects with genuine cross-report or project-wide value. It is not a mandatory stage in the production chain.

## 1. `code/` — computational authority

Root `code/` owns **how things are calculated**.

Examples that belong in `code/src/visitas_analysis/`:

- cohort construction and eligibility rules;
- cleaning and revalidation/real-attempt logic;
- visit-count transformations and group definitions;
- outcome construction and imputation;
- confidence intervals and effect-size calculations;
- statistical tests and model fitting;
- propensity/selection diagnostics;
- temporal analyses;
- reusable plotting functions;
- reusable rendering/build helpers.

Before creating a function, search `code/FUNCTION_INDEX.md`. If an equivalent function exists, reuse it. If a genuinely new function is needed, add it to the appropriate root-code module, document it, test it, regenerate the function index, and only then call it from a report.

Root code should not know that a particular function is being used only because Paper 1 happens to need it today. It should define the calculation cleanly; the report decides whether and how to use it.

## 2. `reports/` — research-development workspaces

A report owns **what we tried, in what order, why, and what we learned**.

Reports are the normal home for:

- research questions under active investigation;
- exploratory analyses;
- methodological checks;
- robustness and sensitivity analyses;
- competing specifications;
- null findings worth preserving;
- diagnostic figures/tables;
- interpretation notes;
- assumptions and limitations;
- decisions about which results appear strong enough to feed a paper.

Each report should be atomic as a research product while still importing all reusable computation from root `code/`.

Preferred layout when those components actually exist:

```text
reports/<report_id>/
├── README.md
├── AI_HANDOFF.md        # optional when the report becomes complex
├── code/
│   └── <report_id>.py   # thin runner / experiment recipe
├── notes/               # brainstorming, interpretation, open questions
├── tables/              # reviewed retained aggregate tables
├── figures/             # reviewed retained figures
├── provenance/          # report-specific methodological/history records
├── build/               # disposable generated workspace; ignored by Git
├── <report_id>.tex
└── <report_id>.pdf
```

A report-local runner may resolve paths, parse report-specific options, choose which canonical functions to call, and specify their execution order. It must not reimplement estimators, cohort builders, transformations, tests, models, confidence intervals, or reusable plotting logic.

## 3. `papers/` — publication-selection layer

A paper owns **the final publication argument**, not a competing scientific implementation.

A paper should select from validated report evidence:

- the research question and contribution that survive the broader exploration;
- the subset of results necessary for the manuscript;
- final tables/figures needed for submission;
- paper-specific literature interpretation;
- manuscript prose and journal-specific submission materials.

A paper may retain copies of approved report tables/figures for portability, but provenance back to the source report/root code must remain clear. Do not manually alter a copied numerical result inside the paper.

If manuscript writing reveals that a new analysis is required, go **back upstream**: implement/reuse the calculation in `code/`, execute it in the appropriate report, evaluate it there, and only then promote the validated result into the paper.

## 4. Workflow for a new research idea

Use this sequence by default.

### Step 1 — give the idea a report home

Decide which existing report owns the question. If the idea is substantively independent and likely to accumulate its own analyses, create a purpose-based report folder rather than a versioned copy such as `report_v2`.

Write the question, rationale, assumptions, and unresolved issues in the report README or `notes/` before the analysis becomes difficult to reconstruct from code alone.

### Step 2 — search the computational library

Read `code/.ai_handoff.md` and search `code/FUNCTION_INDEX.md` using the scientific concept, likely function name, and related terms.

Do not start by writing a new implementation inside the report.

### Step 3 — add missing reusable capability only in root `code/`

If the needed capability does not exist:

1. implement it in the scientifically appropriate module under `code/src/visitas_analysis/`;
2. give it a useful docstring;
3. add/update tests;
4. update the methodological protocol when the change affects the scientific specification;
5. regenerate `code/FUNCTION_INDEX.md`.

### Step 4 — call the capability from the report-local runner

The report-local script should read like an experimental recipe: imports, configuration, execution order, output destinations, and product-specific build/staging decisions.

It should be possible to understand **which analyses were run** from the runner without finding a second implementation of **how each analysis works** there.

### Step 5 — keep disposable and retained outputs distinct

Generate intermediate/rebuildable files under the report's ignored `build/` directory when practical. Promote aggregate tables/figures into the report's retained `tables/` and `figures/` only when they are scientifically useful and privacy-reviewed.

Never commit raw institutional microdata merely to make a report self-contained.

### Step 6 — record interpretation, not just numbers

Preserve in the report:

- what the result says;
- what it does not identify;
- assumptions required for interpretation;
- important nulls or contradictions;
- sensitivity to alternative specifications;
- open questions and next analyses.

This is why reports are broader than papers.

### Step 7 — promote evidence to a paper only after review

Once an analysis supports a coherent publication question, select the necessary evidence into `papers/<paper_id>/`.

The paper should be narrower than its source report(s). It should not delete or replace the broader research record that led to the selected result.

### Step 8 — when data are updated, rerun rather than rewrite

If only the institutional data vintage changes:

1. keep the same root functions;
2. keep the same report-local runner;
3. point it to the new controlled input files;
4. rerun tests;
5. regenerate the report outputs;
6. compare cohort counts and numerical results with the previous retained state;
7. investigate unexpected differences before updating paper prose.

Do not create `*_v2.py`, a dated report copy, or a second implementation merely because the data changed.

### Step 9 — when methodology changes, propagate downstream

For a genuine scientific change:

```text
change root code
    ↓
update tests + protocol + function index
    ↓
rerun affected report(s)
    ↓
review changed evidence
    ↓
update affected paper(s)
```

Never patch the final manuscript first and then try to make the code match it.

## 5. Placement decision table

| Object | Canonical location |
|---|---|
| Reusable cohort builder | `code/src/visitas_analysis/...` |
| Reusable statistical test/model helper | `code/src/visitas_analysis/...` |
| Reusable plot function | `code/src/visitas_analysis/...` |
| Unit/scientific regression test | `code/tests/` |
| Searchable function inventory | `code/FUNCTION_INDEX.md` |
| Experiment/report execution order | `reports/<report_id>/code/` |
| Exploratory interpretation or methodological brainstorming | `reports/<report_id>/notes/` |
| Reviewed report aggregate table/figure | `reports/<report_id>/tables/` or `figures/` |
| Cross-report retained aggregate | `analysis/shared/` |
| Paper-specific literature interpretation | `papers/<paper_id>/literature/` |
| Manuscript prose/LaTeX | `papers/<paper_id>/manuscript/` |
| Final paper-specific selected assets | `papers/<paper_id>/results/` |
| Journal submission materials | `papers/<paper_id>/submission/` |
| Shared physical literature source | `literature/library/` |

## 6. Anti-patterns to avoid

Do not:

- copy a statistical function into `reports/<report>/code/` because it is convenient;
- create slightly different cohort builders for different reports without a reviewed scientific reason;
- calculate a new reported number directly inside manuscript LaTeX or a one-off notebook;
- create `analysis_final.py`, `report_v2/`, `paper_final/`, or date-suffixed active variants for version control;
- treat `papers/` as an exploratory analysis workspace;
- discard null findings from reports merely because they are not selected into the paper;
- duplicate source PDFs across papers;
- allow a report-local runner to become a second package of reusable functions.

Git preserves versions; folder structure expresses current scientific responsibility.

## 7. Current example: methodology report

The canonical model is already implemented by:

```text
reports/methodology_report/code/methodology_report.py
        ↓ imports
code/src/visitas_analysis/reporting/methodology_build.py
        ↓ calls
code/src/visitas_analysis/study/methodology_pipeline.py
        + other canonical root-code functions
        ↓
reports/methodology_report/build/
        ↓ reviewed/staged
reports/methodology_report/tables/ + figures/
```

The product is atomic, while the computation remains centralized.

## 8. Current example: Paper 1

Paper 1 is not a standalone analysis codebase. Its current scientific story is selected primarily from the broader longitudinal evidence preserved in `reports/research_compendium/` together with methodological review/sensitivity evidence in `reports/methodology_report/`.

If Paper 1 needs an additional robustness analysis, that analysis should first be developed in the appropriate report using root-code functions; only the validated subset should enter the manuscript.

## 9. Documentation hierarchy

Use these documents without duplicating their roles:

- `README.md` — repository map and high-level architecture;
- `AI_HANDOFF.md` — short global router/invariants;
- `docs/RESEARCH_WORKFLOW.md` — this full production model;
- `code/.ai_handoff.md` — rules for reusable computation;
- `reports/AI_HANDOFF.md` — rules for experimental/report workspaces;
- `papers/README.md` — publication-layer rules;
- individual report/paper READMEs — product-specific scientific state;
- `REPRODUCING.md` — executable commands/environment.

When the architecture changes, update the owning canonical document and only add short links elsewhere rather than copying the full explanation into every handoff.
