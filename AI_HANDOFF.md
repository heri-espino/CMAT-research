# AI handoff — CMAT research repository

Canonical entry point for future AI sessions working in `heri-espino/CMAT-research`.

This file is intentionally a **router, not a duplicate project encyclopedia**. Detailed scientific/editorial information belongs in the subsystem that owns it. Follow the links below instead of expanding this handoff with copied paper content or result tables.

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

### Ownership rules

- **One paper = one home:** `papers/<paper_id>/`.
- Do not recreate `literature/papers/`.
- **One physical literature source = one library record:** `literature/library/`.
- Reusable scientific functions belong in `code/src/visitas_analysis/`, not in paper/report folders.
- A runner defines an execution recipe; it does not reimplement estimators.
- Reports are project-level products; papers are manuscript-level products.

## 2. Mandatory startup by task

### Any repository change

1. `README.md`
2. `AGENTS.md`
3. this file
4. README/AGENTS for the subsystem being changed

### Code / numerical analysis

1. `code/.ai_handoff.md`
2. `code/FUNCTION_INDEX.md` — search before creating any function
3. `code/STUDY_PROTOCOL.md`
4. `code/ADMINISTRATIVE_QUESTIONS.md`
5. only then open the relevant module/runner

For an existing report/analysis reproduction task, follow the runner-first rule in `code/.ai_handoff.md`: use the existing implementation/reference, reuse functions, create or edit one thin runner, verify reproduction, and do not broaden scope unnecessarily.

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

Do not create alternate directories for these manuscripts:

- `paper1_ppa_persistence`
- `paper2_mu_performance`
- `paper3_grading_heterogeneity`
- `paper4_degree_help_seeking`
- `paper5_longitudinal_trajectories`

Cross-paper strategy: `docs/PUBLICATION_PORTFOLIO.md`.

Detailed scope/status: each `papers/<paper_id>/README.md`.

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

Use `--check` for a structure/import check without loading controlled data. Do not recreate the methodology report calculation sequence manually when the runner/reference implementation already exists.

## 5. Global scientific invariants

These are project-wide and belong here because violating them can affect several papers/reports.

### Observational interpretation

CMAT attendance is student-selected. Do not claim CMAT, PPA, tutoring, visit frequency, or threshold crossing causally changes grades, persistence, motivation, or habit without an identification design that supports that claim.

Use language such as `association`, `predictive association`, `behavioural persistence`, `formal academic help-seeking`, `institutional participation incentive`, and `pattern consistent with`.

### CMAT visit records

One Google Forms row is one recorded advisory visit. There is no duration measure. Multiple same-day visits can be legitimate because advisers/blocks can change; do not label same-day concentration as manipulation without evidence.

### PPA context

Operational study threshold: **3 CMAT visit records during the MU period**. Do not equate three visit records with three PPA points.

The current PPA interpretation treats MU as the first-year incentive-linked context and later Calculus as generally outside that same PPA1-linked CMAT incentive. Individual PPA1 completion timing is not directly observed.

The threshold is student-controlled; it is **not a regression-discontinuity design**.

### Academic outcomes

Passing grade: `7.5`.

- BV / RT / BA: adverse/non-passing academic states.
- EQV / REV / AC: administrative/non-comparable states.

Classroom for classroom-relative performance is `professor × same course × same academic period` unless an explicitly reviewed methodological change replaces it.

### Academic-record duplication

An academic row is not automatically a new real attempt. Degree changes/revalidations can repeat previously passed courses. Preserve the real-attempt/revalidation rules in canonical code.

Official academic programme (`CLAVECARRERA`) is the primary programme field. The CMAT-form self-reported programme cannot be used as a baseline covariate for non-users.

### Cohort discipline

Do not silently substitute one cohort for another. First-MU, later-Calculus progressor, and stricter longitudinal/PPA populations answer different questions. Before quoting a sample size or result, trace it to the current runner/output/report and state the population.

## 6. Reports and retained outputs

Active reports:

- `reports/methodology_report/`
- `reports/research_compendium/`

Purpose-based names are canonical. Historical `v*` labels may remain only in provenance objects.

Retained shared historical aggregates currently live under:

`analysis/shared/historical_outputs/`

They are provenance/comparison artifacts until a reconciled canonical output set is explicitly frozen. Do not infer that `historical` means invalid; identify the generating code state before reuse.

Historical restoration/provenance details:

- `docs/MIGRATION_STATUS.md`
- `docs/HEAVY_SNAPSHOT.md`
- `docs/snapshots/`

Do not re-create permanent snapshot source trees merely because an old implementation is needed; retrieve it from Git history.

## 7. Literature ownership and retrieval

Physical/shared corpus:

`literature/library/`

Cross-project view:

`literature/general/`

Paper-specific views:

`papers/<paper_id>/literature/`

A source may support multiple papers without physical duplication. PDFs in this private repository are internal research materials and are not automatically redistributable.

For exact numerical/visual claims from a source, verify against the source PDF when extracted Markdown is insufficient or ambiguous.

## 8. Data/privacy boundary

Never commit:

- administrative Excel/raw exports;
- row-level student/advisory microdata;
- direct identifiers;
- HMAC keys/salts;
- credentials/tokens;
- unreviewed identifying free text;
- unreviewed row-level pseudonymised longitudinal datasets.

Aggregate outputs may be retained only after disclosure/privacy review.

## 9. Current unresolved scientific maintenance

The later methodology corrections and the refined longitudinal/PPA work still require deliberate scientific reconciliation before claiming one fully unified canonical study pipeline. This is documented in `docs/MIGRATION_STATUS.md`.

That unresolved maintenance item must **not** block narrower reproduction tasks when an existing validated implementation/runner already defines the requested artifact.

## 10. Handoff maintenance rule

Keep this file short and routing-oriented.

When something changes:

- paper detail -> update `papers/<paper_id>/README.md`;
- portfolio boundary/priority -> update `docs/PUBLICATION_PORTFOLIO.md`;
- code architecture/reproducibility -> update `code/.ai_handoff.md`;
- function inventory -> regenerate `code/FUNCTION_INDEX.md`;
- literature routing/library state -> update `literature/AI_HANDOFF.md` / `literature/AGENTS.md`;
- migration/provenance -> update `docs/MIGRATION_STATUS.md`;
- only update this root handoff when the change affects project-wide routing or invariants.

Do not paste paper-specific result tables, long literature lists, or detailed journal strategies into this file; link to their canonical homes instead.
