# CMAT Research

Canonical private monorepo / research compendium for the research and publication programme based on the **Centro de Aprendizaje de Matemáticas (CMAT)** at UDLAP.

## Repository philosophy

`main` is the source of truth. The project is organized by scientific ownership and function, while Git branches are short-lived workspaces for concrete changes. Historical working copies live in Git history rather than as versioned folders inside the active tree.

The scientific flow is:

`controlled data -> reusable code -> stable runners -> aggregate outputs -> reports / papers`.

Two ownership rules organize the repository:

1. **one paper = one home** — everything specific to a manuscript belongs under `papers/<paper_id>/`;
2. **one physical literature source = one library record** — PDFs/Markdown/reference records live once under `literature/library/` and may be annotated by several papers.

Execution/reproduction instructions: `REPRODUCING.md`.

Future AI sessions should start with `AI_HANDOFF.md` and `AGENTS.md`.

## Structure

```text
CMAT-research/
├── README.md
├── REPRODUCING.md
├── AGENTS.md
├── AI_HANDOFF.md
│
├── code/                         # active canonical Python pipeline
│   ├── .ai_handoff.md
│   ├── FUNCTION_INDEX.md
│   ├── config/
│   ├── experiments/              # stable report/paper runners
│   ├── src/                      # reusable scientific functions
│   ├── scripts/                  # code maintenance utilities
│   └── tests/
│
├── analysis/
│   └── shared/
│       └── historical_outputs/   # retained shared aggregates awaiting canonical freeze
│
├── reports/
│   ├── methodology_report/       # methodology/statistical review report
│   └── research_compendium/      # cumulative historical research record
│
├── papers/
│   ├── paper1_ppa_persistence/
│   │   ├── README.md             # detailed Paper 1 source of truth
│   │   └── literature/           # Paper 1 literature interpretation/notes
│   ├── paper2_mu_performance/
│   │   ├── README.md
│   │   └── literature/
│   ├── paper3_grading_heterogeneity/
│   ├── paper4_degree_help_seeking/
│   └── paper5_longitudinal_trajectories/
│
├── literature/
│   ├── library/                  # shared physical corpus/source layer
│   └── general/                  # cross-project literature view
│
├── docs/                         # portfolio, workflow, privacy, migration/provenance
└── data/                         # documentation only; no administrative microdata
```

Within a paper, create `manuscript/`, `results/`, and `submission/` only when they contain real files. Do not add empty scaffolding merely for symmetry.

## Ownership map

### Code

Reusable estimators, cleaning, cohort construction, statistical tests and plotting logic belong in `code/src/visitas_analysis/`. Before writing a function, read `code/.ai_handoff.md` and search `code/FUNCTION_INDEX.md`.

A reproducible scientific/report recipe belongs in `code/experiments/` and imports the reusable functions. A new data extract normally means rerunning the same stable runner, not creating `*_v2.py`.

### Analysis outputs

`analysis/shared/` contains retained aggregate empirical objects with project-wide or multi-paper relevance. The current historical aggregate set is under `analysis/shared/historical_outputs/`.

If a reviewed output eventually has a clear single-paper owner, it may be retained under `papers/<paper_id>/results/`, but it must still originate from the canonical code/runners. Avoid duplicate retained copies without a documented reason.

### Papers

Each paper has exactly one canonical directory under `papers/<paper_id>/`. Its `README.md` is the detailed source of truth for that paper's question, estimand, contribution, journal route, status and interpretation boundaries.

Paper-specific literature indices, reading guides, gap trackers and evidence notes live under `papers/<paper_id>/literature/`. There is intentionally no `literature/papers/` mirror.

### Literature

`literature/library/` is the canonical shared physical corpus: extracted article Markdown, source PDFs, separated references and the catalogue/provenance layer. `literature/general/` contains cross-project thematic views.

A source used by several papers is stored once in the library and can be referenced/annotated by several paper-local literature views.

### Reports

`reports/methodology_report/` and `reports/research_compendium/` are project-level products rather than manuscript homes. Report names describe scientific purpose, not version.

## AI / agent entry points

1. `AI_HANDOFF.md` — current scientific/project state and routing.
2. `AGENTS.md` — repository operating rules.
3. `REPRODUCING.md` — environment, tests and canonical execution commands.
4. `code/.ai_handoff.md` + `code/FUNCTION_INDEX.md` — mandatory before code changes.
5. `docs/PUBLICATION_PORTFOLIO.md` — cross-paper boundaries/priorities.
6. `papers/<paper_id>/README.md` — detailed paper-specific source of truth.
7. `literature/AGENTS.md` and `literature/AI_HANDOFF.md` — shared-library/retrieval rules.

## Five-paper publication programme

Canonical cross-paper plan: `docs/PUBLICATION_PORTFOLIO.md`.

1. **Paper 1 — incentive-linked persistence**  
   *Beyond the Incentive Threshold: Academic Support Use and Persistence After a First-Year Participation Incentive*.

2. **Paper 2 — CMAT use and MU performance**  
   *Mathematics Support Use and Classroom-Relative Academic Performance in First-Year University Mathematics*.

3. **Paper 3 — grading heterogeneity**  
   *When the Same Grade Does Not Mean the Same Performance: Instructor-by-Term Heterogeneity in Undergraduate Mathematics Assessment*.

4. **Paper 4 — disciplinary help-seeking heterogeneity**  
   *Who Keeps Seeking Mathematics Help? Disciplinary Heterogeneity in University Mathematics Support Use*.

5. **Paper 5 — full-degree trajectories**  
   *Longitudinal Trajectories of Mathematics Support Use Across the Undergraduate Degree*.

The portfolio document provides cross-paper strategy; detailed manuscript information should be maintained in each paper rather than repeatedly copied into unrelated subsystem documentation.

## Historical scientific provenance

Historical package labels such as `v8`, `methodology_v5`, and `v2` identify imported scientific states; they are not active folder names. Duplicate historical code/import scripts are removed from the active tree once their provenance is recorded because Git is the history layer.

The complete pre-code-cleanup working tree remains available at commit `20a993d92e8cc197a9060180d8cb6a6caf2607a7`. Additional restoration details live under `docs/snapshots/`, `docs/MIGRATION_STATUS.md`, and `docs/HEAVY_SNAPSHOT.md`.

Removing duplicate historical directories does **not** imply that every historical methodological branch has been scientifically reconciled. Read `docs/MIGRATION_STATUS.md`, the current protocol, tests and implementation before making that claim.

## Privacy

Administrative microdata are not committed. Do not commit:

- student IDs or direct identifiers;
- raw CMAT Forms exports;
- official row-level grade spreadsheets;
- HMAC keys, salts, credentials or tokens;
- unreviewed row-level pseudonymised longitudinal data;
- identifying free-text fields.

Heavy literature PDFs/assets are preserved only because this repository is private and the owner requested internal research continuity; they are not automatically redistributable.

## Reproducibility

See `REPRODUCING.md` for installation, tests, controlled-input handling and exact runner commands.

Generated local outputs under `code/outputs/` are ignored by Git. Retained aggregate outputs must be privacy-reviewed and traceable to code/configuration.

The central reproducibility rule is simple: **functions define calculations; runners define reproducible scientific recipes; reports and papers present the resulting outputs.**

## Git workflow

See `docs/BRANCH_STRATEGY.md` and `docs/GIT_WORKFLOW.md`.

Use Git for history. Do not create permanent `v2`, `final`, dated, or ZIP-derived copies of active code/reports/papers solely for version control.
