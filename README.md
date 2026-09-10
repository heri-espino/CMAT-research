# CMAT Research

Canonical private research compendium for the research and publication programme based on the **Centro de Aprendizaje de Matemáticas (CMAT)** at UDLAP.

## Repository philosophy

`main` is the source of truth and Git is the version/provenance layer. Active folders are organized by **scientific responsibility and production stage**, not by historical version.

The production hierarchy is:

```text
controlled institutional data
        ↓
code/                         reusable scientific functions and shared pipelines
        ↓
reports/<report_id>/          atomic research/brainstorming products
        ↓
papers/<paper_id>/           publication manuscripts selecting validated report evidence
```

`analysis/` is an auxiliary cross-report archive for retained shared aggregates; it is not a required intermediate layer in the main production chain.

Three ownership rules organize the repository:

1. **root `code/` owns reusable computation** — cohort construction, transformations, estimators, tests, models, plots and reusable report-build helpers;
2. **each report is atomic** — a report may contain its own thin `code/` entry point, notes, tables, figures, provenance and LaTeX, but its local code must import reusable functions from root `code/` rather than reimplementing them;
3. **one paper = one home** — everything editorially specific to a manuscript belongs under `papers/<paper_id>/`; papers select and synthesize validated evidence rather than maintaining independent scientific pipelines.

A fourth rule applies to literature: **one physical literature source = one library record** under `literature/library/`; paper-specific interpretation lives with the paper.

Execution/reproduction instructions: `REPRODUCING.md`.

## Structure

```text
CMAT-research/
├── README.md
├── REPRODUCING.md
├── CITATION.cff
├── LICENSE
├── AGENTS.md
├── AI_HANDOFF.md
│
├── code/                         # canonical reusable scientific/computational core
│   ├── .ai_handoff.md
│   ├── FUNCTION_INDEX.md
│   ├── config/
│   ├── src/                      # reusable functions + broad shared pipelines
│   ├── scripts/                  # code-maintenance utilities
│   └── tests/
│
├── reports/                      # research development / brainstorming layer
│   ├── README.md
│   ├── methodology_report/
│   │   ├── code/                 # thin local runner only
│   │   ├── tables/
│   │   ├── figures/
│   │   ├── notes/
│   │   ├── provenance/
│   │   ├── methodology_report.tex
│   │   └── methodology_report.pdf
│   └── research_compendium/
│
├── papers/                       # publication layer
│   ├── paper1_ppa_persistence/
│   ├── paper2_mu_performance/
│   ├── paper3_grading_heterogeneity/
│   ├── paper4_degree_help_seeking/
│   └── paper5_longitudinal_trajectories/
│
├── analysis/
│   └── shared/
│       └── historical_outputs/   # cross-report retained aggregates/provenance
│
├── literature/
│   ├── library/                  # shared physical source corpus
│   └── general/                  # cross-project literature views
│
├── docs/
│   ├── PUBLICATION_PORTFOLIO.md
│   ├── GIT_WORKFLOW.md
│   ├── MIGRATION_STATUS.md
│   ├── ARCHIVE_PROVENANCE.md
│   └── provenance/
│
└── data/                         # documentation only; no administrative microdata
```

## Production model

### 1. Root `code/` — computational authority

Reusable estimators, cleaning, cohort construction, statistical tests, transformations, plotting functions and reusable build utilities belong in `code/src/visitas_analysis/`. Before writing a function, read `code/.ai_handoff.md` and search `code/FUNCTION_INDEX.md`.

A product folder must not become a second scientific codebase. If a report reveals that a new statistic, model, transformation or plotting function is needed, implement it in root `code/`, test it there, and then import it from the product-local entry point.

Broad shared runners such as `code/src/run_study.py` and `code/src/run_analysis.py` remain in root `code/` because they are project-wide pipelines rather than one report's build recipe.

### 2. `reports/` — atomic research-development products

Reports are the project's working scientific synthesis and brainstorming layer. A report may be broad, exploratory, methodological, or cumulative; it can retain null results, sensitivities and analyses that will never appear together in one publication.

Each report should be as self-contained as practical:

```text
reports/<report_id>/
├── README.md
├── code/             # thin entry point(s); imports root/code
├── notes/
├── tables/
├── figures/
├── provenance/
├── <report>.tex
└── <report>.pdf
```

The canonical methodology-report command is now:

```bash
python reports/methodology_report/code/methodology_report.py --check
```

and, with controlled data:

```bash
python reports/methodology_report/code/methodology_report.py \
  --materias <academic-file> \
  --asesorias <visits-file>
```

Its disposable working directory is `reports/methodology_report/build/`, which is ignored by Git. Reviewed report tables/figures remain inside the report itself.

### 3. `papers/` — publication selection layer

Each paper has exactly one canonical directory under `papers/<paper_id>/`. Papers select, interpret and present validated results developed in the reports; they do not redefine cohorts or estimands independently.

Paper-specific literature indices, reading guides and evidence notes live with the paper. Manuscript, reviewed final figures/tables and submission files should also live there when they exist.

If a paper needs a product-local script later, it may use `papers/<paper_id>/code/`, but that script must be a thin consumer/orchestrator of root `code/` and/or reviewed report outputs, never a parallel scientific implementation.

## Current reports

- `reports/methodology_report/` — current detailed methodology/statistical review workspace and atomic reproducible report.
- `reports/research_compendium/` — cumulative historical research record retained for scientific continuity and broader brainstorming context.

## Current papers

Canonical cross-paper plan: `docs/PUBLICATION_PORTFOLIO.md`.

1. `paper1_ppa_persistence`
2. `paper2_mu_performance`
3. `paper3_grading_heterogeneity`
4. `paper4_degree_help_seeking`
5. `paper5_longitudinal_trajectories`

Detailed scope/status belongs in each paper's own `README.md`, not repeated in the root documentation.

## Literature

`literature/library/` is the canonical shared physical corpus: extracted article Markdown, source PDFs, separated references and catalogue/provenance records. `literature/general/` contains cross-project thematic views; `papers/<paper_id>/literature/` contains paper-specific interpretation and notes.

Do not recreate a parallel `literature/papers/` hierarchy or duplicate PDFs inside paper folders.

## Analysis archive

`analysis/shared/` is reserved for aggregate empirical objects that genuinely have cross-report or project-wide value, including historical outputs used for reconciliation. Report-owned generated assets should normally stay with the report that interprets them.

## AI / agent entry points

1. `AI_HANDOFF.md` — global routing and invariants.
2. `AGENTS.md` — repository operating rules.
3. `REPRODUCING.md` — environment and execution commands.
4. `code/.ai_handoff.md` + `code/FUNCTION_INDEX.md` — mandatory before Python/scientific-code changes.
5. `reports/<report_id>/README.md` — report-specific scientific/build context.
6. `docs/PUBLICATION_PORTFOLIO.md` and `papers/<paper_id>/README.md` — publication context.
7. `literature/AGENTS.md` and `literature/AI_HANDOFF.md` — literature rules.

## Privacy and provenance

Administrative microdata are not committed. Do not commit student/direct identifiers, raw CMAT exports, official row-level grade spreadsheets, HMAC keys/salts, credentials/tokens, unreviewed row-level pseudonymised longitudinal data, or identifying free text.

Historical source states belong in Git history; detailed restoration records may live under `docs/provenance/` or a report's own `provenance/` directory. Active paths should not use `v2`, `final`, dated, or ZIP-derived names solely for version control.

Repository-level citation metadata is in `CITATION.cff`. `LICENSE` intentionally does not grant a blanket open license over the private repository or third-party literature/institutional materials.
