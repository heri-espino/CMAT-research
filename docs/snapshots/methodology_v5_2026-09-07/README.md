# Historical methodology restoration record

This document records the restoration performed on 2026-09-08 from archives uploaded by the project owner.

The uploaded ZIP containers had been repackaged. The code ZIP omitted the hidden file `.ai_handoff.md`; that single file was restored from the already-staged exact copy after verifying its SHA-256 against the embedded source manifest.

Fidelity was verified at the file level before commit:

- every entry in `SOURCE_MANIFEST_SHA256.txt` passed SHA-256 verification;
- every entry in the report `provenance/SHA256SUMS.txt` passed SHA-256 verification;
- the methodology report matched SHA-256 `1e52d36809924df4bc84db65f6cb6669fe33d1f402076e8930b3a173f550595f` and has 40 pages;
- the methodology test suite passed 9/9 tests;
- the historical Python function index declared 320 symbols;
- no Excel or other prohibited raw microdata formats were present.

Uploaded container hashes at restoration:

- code ZIP: `9db4bbb4ae4952ede3267cc23feb759cae0ad344bf395f56ab58e9b341194a71`
- report ZIP: `59278ed2ef7a37d3d779920fab477f8fa5b3c55bcb6b52d7fb087cecc033d572`

Historical scientific-source fingerprint documented by the restored state:

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

Cohort interpretation remains unchanged: primary first-MU N=6,627; future-progressor sensitivity N=4,211. The refined longitudinal N=3,241 analysis is later work and is not claimed to be covered by this fingerprint.

## Current archive location

The restored code tree was temporarily retained under `code/snapshots/` during migration verification. After the repository moved to Git-native provenance, that duplicate directory was removed from the active working tree.

The full pre-cleanup repository state is recoverable at commit:

`20a993d92e8cc197a9060180d8cb6a6caf2607a7`.

The active statistical report remains at `reports/methodology_report/`.

This folder under `docs/snapshots/` is documentation of a historical restoration event, not an active scientific code path.
