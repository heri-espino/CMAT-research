# Archive provenance

This document records identity/checksums for historical literature and methodology packages imported during repository canonicalisation. Git history is the primary record for historical source states; duplicate versioned source folders are not retained in the active tree once verification is complete.

## Historical literature source set with visual assets

Original source archive: `Bib.zip`

- SHA-256: `84ef1c01a85db38ef6b5413621480eba1332f800dddc2523f098209e0745a237`;
- original expanded size: approximately 42 MB;
- 20 source PDFs;
- 20 Docling Markdown article extractions;
- 136 Docling visual assets;
- separated reference files and technical index files.

Current consolidated path: `literature/library/`.

## Historical PDF/Markdown source set

Original source archive: `339dc703-470e-407c-bb54-97ab069e4ce7.zip`

- SHA-256: `cfa14830138c970027a9bf730eab2e62b5bf84fe072ddb3c82c206a5c242478c`;
- original expanded size: approximately 99 MB;
- original archive included 29 source PDFs and hundreds of Docling visual assets.

The curated representation is consolidated under `literature/library/`. Omitted Docling visual assets were largely redundant with retained source PDFs; the source PDF remains the visual verification layer.

## Scientific literature interface

Start retrieval from:

- `literature/library/CATALOG.md`;
- `literature/general/INDEX.md` for cross-project questions;
- `papers/paper1_ppa_persistence/literature/INDEX.md`;
- `papers/paper2_mu_performance/literature/INDEX.md`;
- `papers/paper3_grading_heterogeneity/literature/INDEX.md`;
- `papers/paper4_degree_help_seeking/literature/INDEX.md`;
- `papers/paper5_longitudinal_trajectories/literature/INDEX.md`.

The former `literature/papers/` mirror and old upload-batch names remain only in Git/archive provenance.

## Historical methodology restoration

Historical scientific-source fingerprint:

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

Original local archive hashes recorded before browser re-packaging:

- sanitised methodology code ZIP: `d86a301278b37bcf7300fac3b12eaa200c948e4fbaa0016d049a734fba23d0b7`;
- technical methodology report ZIP: `68a872de5cd348e0304945c66adb581bb95192ea2547fd3aaebcb258584941be`;
- combined methodology bundle ZIP: `364c0b4de9b87aa9e635ba145977bfcdecfa99bfa812725e3ac66b082e18f5e8`.

Detailed restoration validation is consolidated at:

`docs/provenance/methodology_restoration_2026-09-07/README.md`

The duplicate methodology source tree once retained under `code/snapshots/` was removed after verification. The complete pre-cleanup tree remains recoverable at commit:

`20a993d92e8cc197a9060180d8cb6a6caf2607a7`

Verified report artifact:

- `reports/methodology_report/methodology_report.pdf` — 40 pages;
- SHA-256: `1e52d36809924df4bc84db65f6cb6669fe33d1f402076e8930b3a173f550595f`.

Historical validation recorded 9/9 methodology helper tests passed and a 320-symbol historical Python function index.

Removing duplicate historical storage does not imply scientific reconciliation of the later methodology corrections and refined longitudinal/PPA work.

## Data/privacy boundary

The repository must not include original administrative Excel workbooks, row-level student/advising microdata, direct identifiers, HMAC keys/salts, credentials/tokens, or unreviewed identifying free text.

## Rights / release boundary

Literature PDFs and retained extraction artifacts are stored for internal research continuity in this private repository. Their presence here does not imply permission for redistribution in a public data/code release.
