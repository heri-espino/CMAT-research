# CMAT Research

Canonical private monorepo for the research and publication programme based on the **Centro de Aprendizaje de Matemáticas (CMAT)** at UDLAP.

## Repository philosophy

`main` is the source of truth. The project is organized by subfolder, while Git branches are short-lived workspaces for concrete changes. There should not be separate long-lived scientific realities for the report, Paper 1, Paper 2, or exploratory analysis.

The scientific flow is:

`controlled data -> canonical code -> canonical aggregate outputs -> technical report / manuscripts`.

## Structure

```text
CMAT-research/
├── README.md
├── AGENTS.md
├── .ai_handoff.md
├── code/                     # scientific Python pipeline + preserved historical outputs
├── analysis/                 # canonical aggregate empirical record
├── reports/                  # technical reports
├── papers/
│   ├── paper1_ppa_persistence/
│   └── paper2_mu_performance/
├── literature/
│   ├── library/              # one canonical physical copy of each literature work/version
│   ├── general/              # broad thematic literature map
│   └── papers/               # Paper 1 / Paper 2 literature roles; no duplicated articles
├── docs/                     # protocol, roadmap, changelog, branch policy, privacy
├── scripts/                  # repository maintenance only; never scientific analysis
└── data/                     # documentation only; no administrative microdata
```

Each major folder contains or should contain a local README describing scope, inputs, outputs and canonical status.

## AI / agent entry points

1. Read `AGENTS.md` for operating rules.
2. Read `.ai_handoff.md` for scientific state, definitions, known results and unresolved methodology work.
3. For literature work, read `literature/AGENTS.md` and the relevant thematic/paper index before opening article files.

## Current scientific work

The repository still preserves two scientifically important development lines that must ultimately become one validated pipeline:

1. historical **v8**, containing refined longitudinal PPA progression logic; and
2. the later methodology snapshot introducing corrected classroom-level KDE imputation, all-pair `0/1/2/3/4+` contrasts, the 4,211-progressor sensitivity, population-specific periodicity, and expanded degree-programme analyses.

Do not overwrite one line with the other. The next scientific-code reconciliation must preserve longitudinal functionality, integrate the newer methodology, pass tests, regenerate canonical aggregate outputs, and produce a new source fingerprint.

## Publication programme

Two publication lines are currently prioritized:

1. **Paper 1 — PPA1 and persistence of formal academic help-seeking**, targeted at *Studies in Higher Education*.
2. **Paper 2 — CMAT use and classroom-relative MU performance**, TEAMAT-first.

The master analysis and technical report retain all validated discoveries; manuscripts select defensible subsets only after the empirical record is stable.

## Literature philosophy

The literature corpus is no longer organized by upload batches. `literature/library/` stores each work/version once. `literature/general/` and `literature/papers/` are semantic index layers that can reference the same canonical record without duplicating it.

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

## Git workflow

See `docs/GIT_WORKFLOW.md` and `docs/BRANCH_STRATEGY.md`.

In short: create a branch for a concrete task, review the diff/tests, merge into `main`, then delete the branch. ZIP snapshots are optional offline backups, not project history.
