# Heavy private snapshot inventory

This repository is intended to preserve the full internal CMAT research snapshot. Heavy binaries are configured for Git LFS in `.gitattributes`.

## Literature corpus available for migration

Two local source archives were preserved during the research workflow:

### Batch 1 — `Bib.zip`

- SHA-256: `84ef1c01a85db38ef6b5413621480eba1332f800dddc2523f098209e0745a237`
- Expanded directory size: approximately 42 MB
- 20 source PDFs
- 20 Docling Markdown article extractions
- 136 Docling visual assets (PNG/table/figure files)
- separated reference files and technical index files

Target path in this repository: `literature/Bib/`

### Batch 2 — literature expansion

Source archive: `339dc703-470e-407c-bb54-97ab069e4ce7.zip`

- SHA-256: `cfa14830138c970027a9bf730eab2e62b5bf84fe072ddb3c82c206a5c242478c`
- Expanded directory size: approximately 99 MB
- 29 source PDFs
- 29 Docling Markdown article extractions
- 322 Docling visual assets
- separated reference files and technical index files

Target path in this repository: `literature/Bib2/` during raw archival preservation. A later consolidation may canonicalize duplicate papers into `literature/Bib/`, but the raw imported batches should remain traceable by checksum.

## Current methodology/report snapshots

- Sanitized scientific-code snapshot ZIP SHA-256: `d86a301278b37bcf7300fac3b12eaa200c948e4fbaa0016d049a734fba23d0b7`
- Technical methodology report ZIP SHA-256: `68a872de5cd348e0304945c66adb581bb95192ea2547fd3aaebcb258584941be`
- Combined methodology bundle ZIP SHA-256: `4a6e5400bef7574b375c9c03479d4353cf377129c536bc36feef704e5b33d69a`

## Privacy boundary

The heavy snapshot may include literature PDFs and Docling-generated visual assets because this GitHub repository is private and the owner explicitly requested preservation. It must **not** include:

- administrative Excel workbooks;
- row-level student/advising microdata;
- direct student or professor identifiers;
- HMAC/secret keys;
- credentials or tokens.

## Git LFS

`*.pdf`, literature `*.png`/images, report/paper binaries, and archive ZIPs are configured for Git LFS. This is deliberate: committing roughly 140 MB of already-compressed PDF/PNG material directly into ordinary Git history would make the repository unnecessarily difficult to clone and maintain.

## Important connector limitation

The ChatGPT GitHub connector can create/update GitHub files and individual Git objects, but it does not expose a local-directory `git push`/Git-LFS streaming operation. Therefore the repository can be prepared and maintained here, while the initial transfer of the ~140 MB binary corpus requires a Git/LFS client capable of streaming local files. Once those binaries exist in the repository, future text/code/document changes can continue through the connected GitHub workflow.
