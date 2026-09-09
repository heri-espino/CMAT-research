# CMAT Research

Canonical private monorepo for the research and publication programme based on the **Centro de Aprendizaje de Matemáticas (CMAT)** at UDLAP.

## Repository philosophy

`main` is the source of truth. The project is organized by scientific function, while Git branches are short-lived workspaces for concrete changes. Historical working copies should live in Git history rather than as versioned folders inside the active tree.

The scientific flow is:

`controlled data -> canonical code -> canonical aggregate outputs -> reports / manuscripts`.

Future AI sessions should start with `AI_HANDOFF.md` and `AGENTS.md`.

## Structure

```text
CMAT-research/
├── README.md
├── AGENTS.md
├── AI_HANDOFF.md
├── code/                     # active canonical Python pipeline only
├── analysis/                 # retained aggregate empirical record
│   └── historical_outputs/   # previously committed pipeline outputs awaiting canonical freeze
├── reports/
│   ├── methodology_report/   # methodology/statistical review report
│   └── research_compendium/  # cumulative historical research record
├── papers/
│   ├── paper1_ppa_persistence/
│   ├── paper2_mu_performance/
│   ├── paper3_grading_heterogeneity/
│   ├── paper4_degree_help_seeking/
│   └── paper5_longitudinal_trajectories/
├── literature/
│   ├── library/              # shared physical corpus/source layer
│   ├── general/              # cross-project literature view
│   └── papers/               # five paper-specific literature views
├── docs/                     # portfolio, protocol, roadmap, workflow, privacy, provenance
└── data/                     # documentation only; no administrative microdata
```

Each major folder contains or should contain a local README describing scope, inputs, outputs and canonical status.

## AI / agent entry points

1. Read `AI_HANDOFF.md` for current scientific/project state.
2. Read `AGENTS.md` for operating rules.
3. For literature work, read `literature/AGENTS.md` and `literature/AI_HANDOFF.md` before opening article files.

## Five-paper publication programme

Canonical plan: `docs/PUBLICATION_PORTFOLIO.md`.

1. **Paper 1 — incentive-linked persistence**  
   *Beyond the Incentive Threshold: Academic Support Use and Persistence After a First-Year Participation Incentive*  
   Current route: *Studies in Higher Education* first/ambitious; IJMEST, TEAMAT and *Journal of Further and Higher Education* as alternatives.

2. **Paper 2 — CMAT use and MU performance**  
   *Mathematics Support Use and Classroom-Relative Academic Performance in First-Year University Mathematics*  
   Current route: TEAMAT first; IJMEST second; IJRUME ambitious.

3. **Paper 3 — grading heterogeneity**  
   *When the Same Grade Does Not Mean the Same Performance: Instructor-by-Term Heterogeneity in Undergraduate Mathematics Assessment*  
   Current route: *Assessment & Evaluation in Higher Education* first; *Studies in Educational Evaluation* second; IJRUME ambitious. Requires dedicated re-analysis before drafting.

4. **Paper 4 — disciplinary help-seeking heterogeneity**  
   *Who Keeps Seeking Mathematics Help? Disciplinary Heterogeneity in University Mathematics Support Use*  
   Current route: IJMEST first; *Journal of Further and Higher Education* second; HERD ambitious.

5. **Paper 5 — full-degree trajectories**  
   *Longitudinal Trajectories of Mathematics Support Use Across the Undergraduate Degree*  
   Future route depends on final design: TEAMAT/IJMEST for substantive mathematics-support work, *Journal of Learning Analytics* for a genuine trace/sequence-analysis contribution, and *International Journal of STEM Education* as an ambitious STEM-progression option.

The master analysis and methodology report retain all validated discoveries; manuscripts select defensible subsets only after the empirical record is stable.

## Historical scientific provenance

Historical package labels such as `v8`, `methodology_v5`, and `v2` identify imported scientific states; they are not active folder names. The reports are purpose-based:

- `reports/methodology_report/` — later methodology-focused statistical report;
- `reports/research_compendium/` — cumulative report containing the earlier performance work and refined longitudinal/PPA chapter.

The duplicate historical code snapshot that had lived under `code/snapshots/` was removed from the active tree once its restoration was verified. Git remains the provenance layer: the complete pre-cleanup working tree is available at commit `20a993d92e8cc197a9060180d8cb6a6caf2607a7`, with additional restoration details under `docs/snapshots/` and `docs/HEAVY_SNAPSHOT.md`.

Removing that duplicate directory does **not** mean the active pipeline has already reconciled every later methodology correction with the refined longitudinal work. Before changing scientific code or relying on a historical result, read `docs/MIGRATION_STATUS.md`, current protocol files, tests, and the implementation itself.

## Literature

Literature is organized by scientific use, not upload batch. The physical corpus is shared under `literature/library/`; general and Papers 1–5 maintain curated views over that corpus without duplicating sources solely for manuscript relevance.

See `literature/README.md`, `literature/AGENTS.md`, and `literature/AI_HANDOFF.md`.

## Privacy

Administrative microdata are not committed. Do not commit:

- student IDs or direct identifiers;
- raw CMAT Forms exports;
- official row-level grade spreadsheets;
- HMAC keys, salts, credentials or tokens;
- unreviewed row-level pseudonymised longitudinal data;
- identifying free-text fields.

Heavy literature PDFs/assets are preserved only because this repository is private and the owner requested internal archival continuity; they are not automatically redistributable.

## Reproducibility

Scientific source fingerprints and controlled-source checksums document version identity and provenance. SHA-256 establishes integrity; it does not anonymise data.

Generated local outputs under `code/outputs/` are ignored by Git. Aggregate outputs selected for retention belong under `analysis/` with their scientific provenance.

## Git workflow

See `docs/BRANCH_STRATEGY.md` and `docs/GIT_WORKFLOW.md`.

In short: create a branch only for a concrete task when useful, review the diff/tests, merge into `main`, then delete the branch. ZIP snapshots and duplicate source folders are not project history; Git is.
