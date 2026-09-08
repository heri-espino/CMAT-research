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
├── code/                     # canonical Python pipeline + preserved historical v8 outputs
├── analysis/                 # canonical aggregate empirical record
├── reports/                  # technical reports
├── papers/
│   ├── paper1_ppa_persistence/
│   └── paper2_mu_performance/
├── literature/               # heavy private Bib corpus + notes/indices
├── docs/                     # protocol, roadmap, changelog, branch policy, privacy
└── data/                     # documentation only; no administrative microdata
```

Each major folder contains or should contain a local README describing scope, inputs, outputs and what is canonical.

## Current scientific work

The immediate methodological task is to reconcile:

1. historical **v8**, which contains the refined longitudinal PPA progression pipeline; and
2. the later methodology snapshot that introduced corrected classroom-level KDE imputation, all-pair `0/1/2/3/4+` contrasts, the 4,211-progressor sensitivity, population-specific periodicity, and expanded degree-programme analyses.

This work should occur on the short-lived branch `method/reconcile-v8-v5`, then return to `main` after tests and review.

## Publication programme

Two publication lines are currently prioritized:

1. **Paper 1 — PPA1 and persistence of formal academic help-seeking**, targeted at *Studies in Higher Education*.
2. **Paper 2 — CMAT use and classroom-relative MU performance**, TEAMAT-first.

The master analysis and technical report retain all validated discoveries; manuscripts select defensible subsets only after the empirical record is stable.

## Privacy

Administrative microdata are not committed. Do not commit:

- student IDs or direct identifiers;
- raw CMAT Forms exports;
- official row-level grade spreadsheets;
- HMAC keys, salts, credentials or tokens;
- unreviewed row-level pseudonymised longitudinal data;
- identifying free-text fields.

Heavy literature PDFs and Docling assets are preserved only because this repository is private and the owner explicitly requested archival continuity.

## Reproducibility

Scientific source fingerprints and controlled-source checksums document version identity and provenance. SHA-256 establishes integrity; it does not anonymise data.

## Git workflow

See `docs/BRANCH_STRATEGY.md`.

In short: create a branch for a concrete task, review the diff/tests, merge into `main`, then delete the branch. ZIP snapshots are optional offline backups, not project history.