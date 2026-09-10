# AI handoff — CMAT research repository

Canonical entry point for future AI sessions working in `heri-espino/CMAT-research`.

This file is intentionally a **router**, not a duplicate project encyclopedia.

## 1. Repository production model

`main` is the source of truth. Git history is the version/provenance layer; do not create active `v2`, `final`, dated or ZIP-derived duplicates solely for version control.

The primary scientific-production chain is:

```text
controlled institutional data
        ↓
code/src/visitas_analysis/
        reusable scientific/computational functions
        ↓ imported by
reports/<report_id>/code/
        thin report-local runner
        ↓
reports/<report_id>/
        broad research synthesis / brainstorming / validated outputs
        ↓ selected into
papers/<paper_id>/
        publication manuscript and final paper-specific assets
```

`analysis/shared/` is auxiliary storage for aggregates with genuine cross-report/project-wide value, not a mandatory intermediate stage.

Literature remains separate:

```text
literature/library/              one physical source record
        ↓
literature/general/              cross-project interpretation
papers/<paper_id>/literature/    paper-specific interpretation
```

Ownership rules:

- **root `code/` owns reusable computation**;
- **each report is atomic** and may own a thin `code/` entry point plus its tables, figures, notes, provenance and LaTeX;
- report-local code must import root `code/`, never fork scientific functions;
- **papers are the publication-selection layer** and do not redefine scientific logic independently;
- **one paper = one home:** `papers/<paper_id>/`;
- **one physical literature source = one library record:** `literature/library/`;
- historical source states belong in Git history, with explicit provenance records where useful.

## 2. Mandatory startup by task

### Any repository change

1. `README.md`
2. `AGENTS.md`
3. this file
4. README/AGENTS for the subsystem being changed

### Code / numerical analysis

1. `code/.ai_handoff.md`
2. `code/FUNCTION_INDEX.md`
3. `code/STUDY_PROTOCOL.md`
4. `code/ADMINISTRATIVE_QUESTIONS.md`
5. owning report/paper README
6. relevant root-code implementation and local runner

Search the function index before creating any reusable function.

### Report work

Read `reports/README.md`, then `reports/<report_id>/README.md`. A report's local `code/` folder is orchestration only; new scientific functions still go to root `code/`.

### Specific paper

1. `docs/PUBLICATION_PORTFOLIO.md`
2. `papers/<paper_id>/README.md`
3. `papers/<paper_id>/literature/`
4. source report(s) from which the paper selects evidence
5. manuscript/results/submission files only as needed

### Literature

1. `literature/AI_HANDOFF.md`
2. `literature/AGENTS.md`
3. `literature/library/CATALOG.md`
4. relevant general or paper-local literature view

## 3. Stable paper IDs

- `paper1_ppa_persistence`
- `paper2_mu_performance`
- `paper3_grading_heterogeneity`
- `paper4_degree_help_seeking`
- `paper5_longitudinal_trajectories`

Cross-paper strategy: `docs/PUBLICATION_PORTFOLIO.md`. Detailed scope/status belongs in each paper README.

## 4. Code/reproducibility contract

Canonical code guidance: `code/.ai_handoff.md`.

Before writing Python:

1. search `code/FUNCTION_INDEX.md`;
2. reuse/extend an existing scientifically equivalent root-code function;
3. create new reusable logic only under `code/src/visitas_analysis/` when necessary;
4. add docstring/tests;
5. call it from the owning report/paper runner;
6. rerun the same runner when only the data vintage changes.

Current atomic methodology-report runner:

```bash
python reports/methodology_report/code/methodology_report.py --check
```

With controlled inputs:

```bash
python reports/methodology_report/code/methodology_report.py \
  --materias <academic-file> \
  --asesorias <visits-file>
```

The local runner imports the implementation from root `code/`; do not reconstruct the calculation sequence inside the report folder.

## 5. Reports → papers boundary

`reports/` is where broad empirical reasoning is developed and preserved. Reports may contain null findings, sensitivities, competing specifications, methodological discussion and results that are useful for more than one manuscript.

`papers/` is where validated report evidence is selected into publication-specific arguments. A paper may copy/retain the final aggregate assets it actually needs for submission, but must preserve provenance to the source report/root code and must not create a competing estimator or cohort definition.

## 6. Global scientific invariants

### Observational interpretation

CMAT attendance is student-selected. Do not claim CMAT, PPA, tutoring, visit frequency or threshold crossing causally changes grades, persistence, motivation or habit without an identification design supporting that claim.

### CMAT visit records

One Google Forms row is one recorded advisory visit. There is no duration measure. Multiple same-day visits can be legitimate because advisers/blocks can change; do not label same-day concentration as manipulation without evidence.

### PPA context

Operational study threshold: **3 CMAT visit records during the MU period**. Do not equate three visit records with three PPA points. The threshold is student-controlled; it is **not a regression-discontinuity design**.

### Academic outcomes

Passing grade: `7.5`.

- BV / RT / BA: adverse/non-passing academic states.
- EQV / REV / AC: administrative/non-comparable states.

Classroom = `professor × same course × same academic period` unless an explicitly reviewed methodological change replaces it.

### Academic-record duplication

An academic row is not automatically a new real attempt. Degree changes/revalidations can repeat previously passed courses. Preserve the canonical real-attempt/revalidation rules.

Official academic programme (`CLAVECARRERA`) is the primary programme field.

### Cohort discipline

Do not silently substitute one cohort for another. First-MU, later-Calculus progressor and stricter longitudinal/PPA populations answer different questions. Trace quoted sample sizes/results to their report/runner/output.

## 7. Current products and provenance

Active reports:

- `reports/methodology_report/`
- `reports/research_compendium/`

Retained shared historical aggregates:

`analysis/shared/historical_outputs/`

Historical restoration/import records:

- `docs/MIGRATION_STATUS.md`
- `docs/ARCHIVE_PROVENANCE.md`
- `docs/provenance/`

Do not recreate permanent snapshot source trees merely because an old implementation is needed; retrieve it from Git history.

## 8. Data/privacy boundary

Never commit administrative Excel/raw exports, row-level student/advisory microdata, direct identifiers, HMAC keys/salts, credentials/tokens, unreviewed identifying free text, or unreviewed row-level pseudonymised longitudinal datasets.

Aggregate outputs may be retained only after disclosure/privacy review.

## 9. Current unresolved scientific maintenance

The later methodology corrections and refined longitudinal/PPA work still require deliberate scientific reconciliation before claiming one fully unified canonical study pipeline. See `docs/MIGRATION_STATUS.md`.

That unresolved maintenance item must not block narrower reproduction tasks when an existing validated report recipe already defines the requested artifact.

## 10. Handoff maintenance

Keep this file routing-oriented.

- code architecture/reproducibility → `code/.ai_handoff.md`
- function inventory → `code/FUNCTION_INDEX.md`
- report-specific build/scientific context → `reports/<report_id>/README.md`
- paper detail → `papers/<paper_id>/README.md`
- portfolio boundary → `docs/PUBLICATION_PORTFOLIO.md`
- literature routing → `literature/AI_HANDOFF.md` / `literature/AGENTS.md`
- migration/provenance → `docs/MIGRATION_STATUS.md` / `docs/provenance/`

Do not duplicate full paper descriptions, long result tables or detailed literature inventories here.
