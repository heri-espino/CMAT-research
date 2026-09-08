# CMAT Research

Canonical private repository for the research and publication work based on the **Centro de Aprendizaje de Matemáticas (CMAT)** at UDLAP.

## Purpose

This repository consolidates the statistical-analysis code, reproducibility documentation, technical reports, publication drafts, aggregated outputs, and literature metadata that were previously distributed across several snapshots and ZIP archives.

The current empirical programme includes two publication-ready research lines:

1. **Paper 1 — first-year participation incentive and persistence of formal academic help-seeking**: longitudinal transition from Matemáticas Universitarias (MU) to Calculus I.
2. **Paper 2 — CMAT use and classroom-relative academic performance**: contemporaneous CMAT exposure in MU, continuous classroom-standardised outcomes, heteroskedasticity-robust inference, exact visit-count analyses, and programme heterogeneity.

Other exploratory analyses are retained for reproducibility but are not automatically part of either manuscript.

## Canonical structure

```text
CMAT-research/
├── README.md
├── AGENTS.md
├── .gitignore
├── code/                    # Python package, config, scripts and tests
├── docs/                    # protocol, handoff, function index, roadmap, changelog
├── reports/                 # technical LaTeX report and aggregated tables/figures
├── papers/                  # manuscript-specific LaTeX projects
│   ├── paper1_ppa_persistence/
│   └── paper2_cmat_performance/
├── literature/              # metadata, cards, indices and citation notes; no copyrighted PDFs
├── outputs/                 # aggregated/releasable analysis outputs only
├── tests/
└── data/
    └── README.md            # no administrative microdata in Git
```

## Privacy rule

**Administrative microdata are not committed to this repository.** In particular, do not commit:

- student IDs or direct identifiers;
- raw CMAT Google Forms exports;
- official grade spreadsheets containing student-level rows;
- HMAC keys, salts, passwords, tokens, or other secrets;
- row-level pseudonymised longitudinal data unless separately reviewed and approved;
- free-text fields that could identify students or advisers.

The repository may contain aggregated tables and figures, reproducibility code, hashes of controlled internal source files, and privacy/release documentation.

## Reproducibility

Scientific-source fingerprints are documented in the project handoff and methodology changelog. A SHA-256 fingerprint establishes file integrity/version identity; it does **not** anonymise data.

The current methodology snapshot uses classroom as:

`instructor × course × academic period`

and treats causal claims conservatively because CMAT use is student-selected.

## Workflow

From now on, this GitHub repository should be treated as the source of truth. Changes should be made as descriptive commits rather than delivered as a sequence of ZIP snapshots.

Suggested commit prefixes:

- `analysis:` statistical analysis or estimand changes
- `method:` methodology changes
- `report:` technical report updates
- `paper1:` Paper 1 manuscript changes
- `paper2:` Paper 2 manuscript changes
- `literature:` bibliography/index updates
- `docs:` protocol/handoff/documentation
- `privacy:` release/privacy controls
- `test:` test-suite changes
- `chore:` repository maintenance

## Current status

The repository is being migrated from the latest sanitised methodology snapshot. Raw administrative data remain outside GitHub.
