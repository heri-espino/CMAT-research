# Heavy private snapshot provenance

This private repository preserves CMAT research code/report history and an internal literature corpus. Heavy binaries are configured for Git LFS where applicable.

## Historical literature source set with visual assets

Original source archive: `Bib.zip`

- SHA-256: `84ef1c01a85db38ef6b5413621480eba1332f800dddc2523f098209e0745a237`;
- original expanded size: approximately 42 MB;
- 20 source PDFs;
- 20 Docling Markdown article extractions;
- 136 Docling visual assets;
- separated reference files and technical index files.

Current repository path:

`literature/library/` (consolidated)

This source set is preserved with its visual assets.

## Historical PDF/Markdown source set

Original source archive: `339dc703-470e-407c-bb54-97ab069e4ce7.zip`

- SHA-256: `cfa14830138c970027a9bf730eab2e62b5bf84fe072ddb3c82c206a5c242478c`;
- original expanded size: approximately 99 MB;
- original archive included 29 source PDFs and hundreds of Docling visual assets.

Current repository path:

`literature/library/` (consolidated)

### Curated GitHub representation

The repository intentionally does **not** reproduce the full original visual-asset directory. The curated representation contains:

- 30 extracted Markdown records;
- 29 source PDFs;
- 24 separated reference files;
- 0 Docling PNG/table/figure assets.

The additional Markdown record reflects retained/versioned source material. `kahu_2018_student-engagement-educational-interface` has a Markdown source copy rather than a PDF in this source set.

The omitted visual assets were large and largely redundant with retained source PDFs. Exact table/figure verification therefore falls back to the PDF.

The original archive checksum above remains the provenance reference for the uncurated source package; the GitHub representation is a deliberate derivative and should not be expected to reproduce the original archive byte-for-byte.

## Scientific literature interface

The source-material paths above are provenance/storage layers. Scientific retrieval should start from:

- `literature/library/CATALOG.md`;
- `literature/general/INDEX.md`;
- `literature/papers/paper1_ppa_persistence/INDEX.md`;
- `literature/papers/paper2_mu_performance/INDEX.md`;
- `literature/papers/paper3_grading_heterogeneity/INDEX.md`;
- `literature/papers/paper4_degree_help_seeking/INDEX.md`;
- `literature/papers/paper5_longitudinal_trajectories/INDEX.md`.

The old upload-batch names are retained only in historical Git commits and archive/checksum descriptions, not as the current scientific organization.

## Methodology v5 / technical report v2 restoration

The exact historical methodology snapshot is preserved under:

`code/snapshots/methodology_v5_2026-09-07/`

The exact technical report v2 is preserved under:

`reports/technical_report_methodology_v2/`

Historical scientific-source fingerprint recorded by that snapshot:

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

Original local archive hashes recorded before browser re-packaging:

- sanitised methodology code ZIP: `d86a301278b37bcf7300fac3b12eaa200c948e4fbaa0016d049a734fba23d0b7`;
- technical methodology report ZIP: `68a872de5cd348e0304945c66adb581bb95192ea2547fd3aaebcb258584941be`;
- combined methodology bundle ZIP: `364c0b4de9b87aa9e635ba145977bfcdecfa99bfa812725e3ac66b082e18f5e8`.

The browser-uploaded ZIP containers used during restoration were repackaged; their restoration-time hashes are documented separately in `docs/snapshots/methodology_v5_2026-09-07/README.md`. File-level manifests, rather than outer ZIP identity, were used to verify scientific fidelity.

Verified report artifact:

- `informe_cmat.pdf` — 40 pages;
- SHA-256: `1e52d36809924df4bc84db65f6cb6669fe33d1f402076e8930b3a173f550595f`.

Verified methodology helper suite: **9/9 tests passed**. `PYTHON_FUNCTION_INDEX.md` declares **320 symbols**.

## Data/privacy boundary

The repository must **not** include:

- original administrative Excel workbooks;
- row-level student/advising microdata;
- direct identifiers;
- HMAC keys, salts, credentials or tokens;
- unreviewed identifying free text.

The restored methodology/report snapshot was audited as containing no original Excel/raw administrative microdata formats.

## Rights / release boundary

Literature PDFs and retained extraction artifacts are stored for internal research continuity in this private repository. Their presence here does not imply permission for redistribution in a public data/code release.


## Literature consolidation update — 2026-09-08

The active literature tree was simplified after verification that all historical Markdown/PDF/reference filenames were represented byte-for-byte in the flat canonical library. The historical `source_material/` hierarchy, duplicate Docling `assets/` tree, and the redundant former secondary inventory were removed. The single master inventory is now `literature/library/CATALOG.md`; original batch checksums and former layout remain documented in provenance and Git history.
