# AI handoff — CMAT research repository

Canonical entry point for future AI sessions working in `heri-espino/CMAT-research`.

This file is intentionally a **router, not a duplicate project encyclopedia**. Detailed scientific/editorial information belongs in the subsystem that owns it.

## 1. Repository model

`main` is the source of truth. Git history is the version/provenance layer; do not create active `v2`, `final`, dated, or ZIP-derived duplicates solely for version control.

Scientific flow:

```text
controlled institutional data
        ↓
code/src/visitas_analysis/       reusable scientific logic
        ↓
code/experiments/                stable reproducible recipes
        ↓
code/outputs/                    local generated outputs; ignored by Git
        ↓ review/privacy check
analysis/shared/ or papers/*/results/
        ↓
reports/ and papers/
```

Literature flow:

```text
literature/library/              one physical source record
        ↓
literature/general/              cross-project interpretation
papers/<paper_id>/literature/    paper-specific interpretation
        ↓
papers/<paper_id>/manuscript/
```

Ownership rules:

- **one paper = one home:** `papers/<paper_id>/`;
- do not recreate `literature/papers/`;
- **one physical literature source = one library record:** `literature/library/`;
- reusable scientific functions belong in `code/src/visitas_analysis/`;
- runners define execution recipes and import reusable functions;
- reports are project-level products; papers are manuscript-level products;
- historical source states belong in Git history; detailed restoration records may live under `docs/provenance/`.

## 2. Mandatory startup by task

### Any repository change

1. `README.md`
2. `AGENTS.md`
3. this file
4. README/AGENTS for the subsystem being changed

### Reproduction / execution

Read `REPRODUCING.md` first.

### Code / numerical analysis

1. `code/.ai_handoff.md`
2. `code/FUNCTION_INDEX.md` — search before creating any function
3. `code/STUDY_PROTOCOL.md`
4. `code/ADMINISTRATIVE_QUESTIONS.md`
5. only then open the relevant module/runner

For an existing report/analysis reproduction task, follow the runner-first rule: use the existing implementation/reference, reuse functions, create/edit one thin runner, verify reproduction, and do not broaden scope unnecessarily.

### Specific paper

1. `docs/PUBLICATION_PORTFOLIO.md` for cross-paper boundaries
2. `papers/<paper_id>/README.md` for the detailed paper source of truth
3. `papers/<paper_id>/literature/` for that paper's evidence map
4. relevant runner/results/manuscript files only as needed

### Literature

1. `literature/AI_HANDOFF.md`
2. `literature/AGENTS.md`
3. `literature/library/CATALOG.md`
4. relevant `literature/general/` or `papers/<paper_id>/literature/` index

## 3. Stable paper IDs

- `paper1_ppa_persistence`
- `paper2_mu_performance`
- `paper3_grading_heterogeneity`
- `paper4_degree_help_seeking`
- `paper5_longitudinal_trajectories`

Cross-paper strategy: `docs/PUBLICATION_PORTFOLIO.md`. Detailed scope/status: each `papers/<paper_id>/README.md`.

Do not duplicate full paper descriptions here.

## 4. Code/reproducibility contract

Canonical code guidance: `code/.ai_handoff.md`.

Before writing Python:

1. search `code/FUNCTION_INDEX.md`;
2. reuse/extend an existing scientifically equivalent function;
3. create new reusable logic only when needed;
4. add docstring/tests for new reusable logic;
5. import it into the stable experiment/report runner;
6. rerun the same runner when only the data vintage changes.

Current report-specific canonical runner:

```bash
python code/experiments/methodology_report.py
```

Do not recreate the methodology calculation sequence manually when the runner/reference implementation already exists.

## 5. Global scientific invariants

### Observational interpretation

CMAT attendance is student-selected. Do not claim CMAT, PPA, tutoring, visit frequency, or threshold crossing causally changes grades, persistence, motivation, or habit without an identification design that supports that claim.

### CMAT visit records

One Google Forms row is one recorded advisory visit. There is no duration measure. Multiple same-day visits can be legitimate because advisers/blocks can change; do not label same-day concentration as manipulation without evidence.

### PPA context

Operational study threshold: **3 CMAT visit records during the MU period**. Do not equate three visit records with three PPA points. The threshold is student-controlled; it is **not a regression-discontinuity design**.

### Academic outcomes

Passing grade: `7.5`.

- BV / RT / BA: adverse/non-passing academic states.
- EQV / REV / AC: administrative/non-comparable states.

Classroom for classroom-relative performance is `professor × same course × same academic period` unless an explicitly reviewed methodological change replaces it.

### Academic-record duplication

An academic row is not automatically a new real attempt. Degree changes/revalidations can repeat previously passed courses. Preserve the real-attempt/revalidation rules in canonical code.

Official academic programme (`CLAVECARRERA`) is the primary programme field.

### Cohort discipline

Do not silently substitute one cohort for another. First-MU, later-Calculus progressor, and stricter longitudinal/PPA populations answer different questions. Trace quoted sample sizes/results to their runner/output/report.

## 6. Reports, retained outputs and provenance

Active reports:

- `reports/methodology_report/`
- `reports/research_compendium/`

Retained shared historical aggregates:

`analysis/shared/historical_outputs/`

Historical restoration/import records:

- `docs/MIGRATION_STATUS.md`
- `docs/ARCHIVE_PROVENANCE.md`
- `docs/provenance/`

Detailed methodology-restoration record:

`docs/provenance/methodology_restoration_2026-09-07/README.md`

Do not re-create permanent snapshot source trees merely because an old implementation is needed; retrieve it from Git history.

## 7. Data/privacy boundary

Never commit administrative Excel/raw exports, row-level student/advisory microdata, direct identifiers, HMAC keys/salts, credentials/tokens, unreviewed identifying free text, or unreviewed row-level pseudonymised longitudinal datasets.

Aggregate outputs may be retained only after disclosure/privacy review.

## 8. Current unresolved scientific maintenance

The later methodology corrections and the refined longitudinal/PPA work still require deliberate scientific reconciliation before claiming one fully unified canonical study pipeline. See `docs/MIGRATION_STATUS.md`.

That unresolved maintenance item must **not** block narrower reproduction tasks when an existing validated implementation/runner already defines the requested artifact.

## 9. Handoff maintenance rule

Keep this file short and routing-oriented.

- paper detail -> `papers/<paper_id>/README.md`
- portfolio boundary/priority -> `docs/PUBLICATION_PORTFOLIO.md`
- code architecture/reproducibility -> `code/.ai_handoff.md`
- function inventory -> regenerate `code/FUNCTION_INDEX.md`
- literature routing/library state -> `literature/AI_HANDOFF.md` / `literature/AGENTS.md`
- migration/current provenance -> `docs/MIGRATION_STATUS.md` / `docs/provenance/`
- root handoff -> only project-wide routing/invariants

Do not paste paper-specific result tables, long literature lists, or detailed journal strategies into this file; link to their canonical homes instead.
