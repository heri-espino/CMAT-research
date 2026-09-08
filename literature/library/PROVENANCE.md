# Literature provenance

The active library is a verified consolidated derivative of two historical literature imports. Upload-batch structure is no longer preserved in the working tree because it duplicated the canonical flat library.

## Historical source sets

### Original visual corpus

- archive: `Bib.zip`;
- SHA-256: `84ef1c01a85db38ef6b5413621480eba1332f800dddc2523f098209e0745a237`;
- 20 source PDFs;
- 20 extracted Markdown records;
- separated references;
- 136 Docling figure/table assets in the original import.

### Original PDF/Markdown corpus

- archive: `339dc703-470e-407c-bb54-97ab069e4ce7.zip`;
- SHA-256: `cfa14830138c970027a9bf730eab2e62b5bf84fe072ddb3c82c206a5c242478c`;
- curated representation historically contained 30 extracted Markdown records, 29 PDFs and 24 separated reference files;
- visual assets were intentionally omitted from that curated import.

## Consolidation

On 2026-09-08, the historical source-batch folders were verified against the flat `articles/`, `pdf/`, and `references/` library before removal. For each historical filename, the flat canonical file matched at least one historical copy byte-for-byte. The duplicate top-level asset tree and the original visual-corpus asset tree also had the same Git tree hash before both were removed.

The active library therefore preserves the scholarly Markdown/PDF/reference content while dropping redundant migration structure and extracted PNG/table assets. Git history preserves the former folder layout and asset files if forensic provenance is ever required.

`kahu_2018_student-engagement-educational-interface` remains a Markdown-only library record in the historical corpus state.

## Rights boundary

Source PDFs are retained for internal research continuity in this private repository. Their presence does not imply permission for redistribution.
