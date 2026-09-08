# Heavy private snapshot inventory

This private repository preserves the CMAT research code/report history and an internal literature corpus. Heavy binaries are configured for Git LFS where applicable.

## Historical literature source set with visual assets

Original source archive: `Bib.zip`

- SHA-256: `84ef1c01a85db38ef6b5413621480eba1332f800dddc2523f098209e0745a237`
- original expanded size: approximately 42 MB;
- 20 source PDFs;
- 20 Docling Markdown article extractions;
- 136 Docling visual assets;
- separated reference files and technical index files.

Current repository path:

`literature/library/source_material/visual_corpus/`

This source set is preserved with its visual assets.

## Historical PDF/Markdown source set

Original source archive: `339dc703-470e-407c-bb54-97ab069e4ce7.zip`

- SHA-256: `cfa14830138c970027a9bf730eab2e62b5bf84fe072ddb3c82c206a5c242478c`;
- original expanded size: approximately 99 MB;
- original archive included 29 source PDFs and hundreds of Docling visual assets.

Current repository path:

`literature/library/source_material/pdf_markdown_corpus/`

### Curated GitHub representation

The repository intentionally does **not** reproduce the full original visual-asset directory. The current checked-in representation contains:

- 30 extracted Markdown records;
- 29 source PDFs;
- 24 separated reference files;
- 0 Docling PNG/table/figure assets.

The additional Markdown record reflects retained/versioned source material in the curated corpus. `kahu_2018_student-engagement-educational-interface` has a Markdown source copy rather than a PDF in this source set.

The visual assets were intentionally omitted because they were large and largely redundant with the retained source PDFs. Exact table/figure verification therefore falls back directly to the PDF.

The original archive checksum above remains the provenance reference for the uncurated source package; the GitHub representation is a deliberate derivative and should not be expected to reproduce the original archive byte-for-byte.

## Scientific literature interface

The source-material paths above are provenance/storage layers. Scientific retrieval should start from:

- `literature/library/CATALOG.md`;
- `literature/general/INDEX.md`;
- `literature/papers/paper1_ppa_persistence/INDEX.md`;
- `literature/papers/paper2_mu_performance/INDEX.md`.

The old upload-batch names are retained only in historical Git commits and archive/checksum descriptions, not as the current scientific organization.

## Current methodology/report snapshots

- Sanitized scientific-code snapshot ZIP SHA-256: `d86a301278b37bcf7300fac3b12eaa200c948e4fbaa0016d049a734fba23d0b7`
- Technical methodology report ZIP SHA-256: `68a872de5cd348e0304945c66adb581bb95192ea2547fd3aaebcb258584941be`
- Combined methodology bundle ZIP SHA-256: `4a6e5400bef7574b375c9c03479d4353cf377129c536bc36feef704e5b33d69a`

## Privacy boundary

The repository must **not** include:

- administrative Excel workbooks;
- row-level student/advising microdata;
- direct student or professor identifiers;
- HMAC/secret keys;
- credentials or tokens.

## Rights / release boundary

Literature PDFs and retained extraction artifacts are stored for internal research continuity in this private repository. Their presence here does not imply permission for redistribution in a public data/code release.
