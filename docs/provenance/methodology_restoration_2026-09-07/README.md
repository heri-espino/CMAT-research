# Historical methodology restoration — 2026-09-07

This directory is a **provenance record**, not an active code path and not a retained source snapshot. It documents the historical methodology state previously identified as `methodology_v5` and the validation performed when that state was restored from project archives.

## Purpose

The historical source tree was temporarily retained during migration verification, then removed from the active working tree once Git became the canonical history layer. This document preserves the information needed to identify and audit that restored state without keeping duplicate code folders.

## Restoration validation

The restored state was validated before merge:

- every entry in `SOURCE_MANIFEST_SHA256.txt` passed SHA-256 verification;
- every entry in the methodology report `provenance/SHA256SUMS.txt` passed SHA-256 verification;
- methodology helper suite: **9/9 tests passed**;
- historical Python function index: **320 symbols**;
- `reports/methodology_report/methodology_report.pdf`: **40 pages** and SHA-256 `1e52d36809924df4bc84db65f6cb6669fe33d1f402076e8930b3a173f550595f`;
- no original Excel files or prohibited raw administrative microdata formats were present.

Historical scientific-source fingerprint:

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

## Archive/container identity

Original local archive hashes recorded before browser re-packaging:

- sanitised methodology code ZIP: `d86a301278b37bcf7300fac3b12eaa200c948e4fbaa0016d049a734fba23d0b7`;
- technical methodology report ZIP: `68a872de5cd348e0304945c66adb581bb95192ea2547fd3aaebcb258584941be`;
- combined methodology bundle ZIP: `364c0b4de9b87aa9e635ba145977bfcdecfa99bfa812725e3ac66b082e18f5e8`.

Hashes of the browser-uploaded containers used during restoration:

- code ZIP: `9db4bbb4ae4952ede3267cc23feb759cae0ad344bf395f56ab58e9b341194a71`;
- report ZIP: `59278ed2ef7a37d3d779920fab477f8fa5b3c55bcb6b52d7fb087cecc033d572`.

The uploaded code container omitted hidden `.ai_handoff.md`. The exact staged copy was restored only after its SHA-256 matched the embedded source manifest. Non-scientific packaging/cache files were excluded during validation.

## Scientific scope of this historical state

This fingerprint covers the later methodology work associated with:

- primary first-MU cohort `N=6,627`;
- future-Calculus progressor sensitivity `N=4,211`;
- SciPy Gaussian KDE / Scott imputation logic;
- complete `0 / 1 / 2 / 3 / 4+` comparisons;
- periodicity extensions;
- expanded degree-programme analyses.

The refined longitudinal/PPA `N=3,241` stage is **later work** and is not claimed to be covered by this historical fingerprint.

## Current repository location

The active methodology report is:

`reports/methodology_report/`

The duplicate restored code tree that once lived under `code/snapshots/` was intentionally removed. The full working tree immediately before that code cleanup remains recoverable from Git at commit:

`20a993d92e8cc197a9060180d8cb6a6caf2607a7`

If implementation details from this historical state are needed, retrieve them from Git history rather than recreating a permanent snapshot directory.

## Interpretation boundary

Removing duplicate historical storage does **not** mean the active scientific pipeline has fully reconciled the later methodology corrections with the refined longitudinal/PPA work. That is a separate scientific-maintenance question documented in `../../MIGRATION_STATUS.md`.

Historical labels such as `methodology_v5`, `v8`, or `v2` are retained here only when needed to identify provenance objects; active repository paths remain purpose-based and versionless.
