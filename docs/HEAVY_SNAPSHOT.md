# Heavy private snapshot provenance

This file records the historical source archives used to populate the internal literature corpus. The active repository architecture is now `literature/library/`; batch names below are provenance only.

## Historical Batch 1

Source archive: `Bib.zip`

- SHA-256: `84ef1c01a85db38ef6b5413621480eba1332f800dddc2523f098209e0745a237`
- approximately 42 MB expanded;
- 20 source PDFs;
- 20 Markdown article extractions;
- 136 Docling visual assets;
- separated reference files for a subset.

## Historical Batch 2

Source archive: `339dc703-470e-407c-bb54-97ab069e4ce7.zip`

- SHA-256: `cfa14830138c970027a9bf730eab2e62b5bf84fe072ddb3c82c206a5c242478c`
- original archive contained the later literature expansion and many Docling visual assets.

The repository owner subsequently chose the lighter curated representation for this second expansion: retain Markdown/source PDFs/references but **omit its redundant PNG assets**, because source PDFs remain available for exact/visual fallback.

## Active canonical representation

`literature/library/` consolidates the imported records independently of source batch:

- 50 Markdown article/version records;
- 49 PDFs;
- separated reference lists where available;
- assets only for the original archived subset.

`kahu_2018_student-engagement-educational-interface` currently has a Markdown source record but no source PDF in the consolidated library.

Meaningfully different versions are not silently collapsed. For example, alternate/published Damgaard records and working-paper/published Oreopoulos records remain separately traceable pending bibliographic consolidation decisions.

## Other preserved snapshot checksums

Historical sanitised scientific-code snapshot SHA-256:

`d86a301278b37bcf7300fac3b12eaa200c948e4fbaa0016d049a734fba23d0b7`

Historical technical methodology report ZIP SHA-256:

`68a872de5cd348e0304945c66adb581bb95192ea2547fd3aaebcb258584941be`

Historical combined methodology bundle ZIP SHA-256:

`4a6e5400bef7574b375c9c03479d4353cf377129c536bc36feef704e5b33d69a`

## Privacy and copyright boundary

Literature PDFs/assets may remain in this **private** repository for internal research continuity. They are not automatically approved for redistribution in a public replication package.

Never place administrative student microdata, direct identifiers, HMAC keys, credentials or secrets in heavy snapshot directories.
