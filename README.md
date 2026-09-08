# CMAT Research

Canonical **private** repository for the research and publication work based on the Centro de Aprendizaje de Matemáticas (CMAT) at UDLAP.

## Purpose

This repository consolidates the statistical-analysis code, reproducibility documentation, technical reports, publication drafts, aggregated outputs, and the private research literature corpus that were previously distributed across several snapshots and ZIP archives.

The current empirical programme includes two main publication lines:

1. **Paper 1 — first-year participation incentive and persistence of formal academic help-seeking**: longitudinal transition from Matemáticas Universitarias (MU) to Calculus I.
2. **Paper 2 — CMAT use and classroom-relative academic performance**: contemporaneous CMAT exposure in MU, continuous classroom-standardised outcomes, heteroskedasticity-robust inference, exact visit-count analyses, and programme heterogeneity.

Other exploratory analyses are retained for reproducibility but are not automatically part of either manuscript.

## Canonical structure

```text
CMAT-research/
├── README.md
├── AGENTS.md
├── .gitignore
├── code/                    # scientific Python snapshot, config, scripts, tests, legacy notebooks
├── docs/                    # protocol, migration status, privacy/reproducibility documentation
├── reports/                 # technical LaTeX report snapshots and aggregated figures/tables
├── papers/                  # manuscript-specific projects as they are consolidated
├── literature/
│   ├── Bib/                 # heavy Batch 1: PDFs + Markdown + references + Docling PNG assets
│   └── Bib2/                # target archival path for heavy Batch 2 (pending binary transfer)
├── outputs/                 # aggregated/releasable outputs when promoted from code snapshots
└── data/
    └── README.md            # no administrative microdata in Git
```

## Heavy private literature corpus

The repository owner explicitly requested preservation of the **heavy** literature version in this private repository.

### Batch 1 — present in GitHub

`literature/Bib/` currently contains the complete first heavy corpus imported from the historical `CMAT2` repository:

- 20 source PDFs;
- 20 Docling Markdown article extractions;
- 136 Docling PNG/table/figure assets;
- separated reference files;
- technical retrieval/index files.

### Batch 2 — source inventoried, binary transfer pending

The second archive is tracked in `docs/HEAVY_SNAPSHOT.md` by SHA-256 and contains:

- 29 PDFs;
- 29 Markdown extractions;
- 322 Docling visual assets;
- separated references/index files.

It was supplied directly during the research session and never existed in `CMAT2`, so the automated GitHub import could not recover it. The canonical target path is `literature/Bib2/` until the two archival batches are intentionally consolidated.

Because these literature files may have different redistribution rights, **their presence in this private repository must not be interpreted as permission to make them public**.

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

The current methodological work defines classroom as:

`instructor × course × academic period`

and treats causal claims conservatively because CMAT use is student-selected.

The historical v8 scientific/report snapshot is already present in `code/` and `reports/technical_report_v8/`. A later methodology overlay contains additional corrections and analyses and still needs to be reconciled with that historical snapshot before `code/` can be treated as one final canonical executable pipeline. See `docs/MIGRATION_STATUS.md`.

## Workflow

This GitHub repository is now the source of truth. Changes should be made as descriptive commits rather than delivered as a sequence of ZIP snapshots.

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

## Migration status

Heavy Batch 1, the historical v8 scientific snapshot, legacy notebooks, aggregated v8 outputs, and the v8 LaTeX report are already in GitHub. Heavy Batch 2 and reconciliation with the latest methodology snapshot remain explicit pending tasks; they are documented rather than silently omitted.
