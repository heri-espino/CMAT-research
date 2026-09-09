# Merge notes — historical methodology restoration

This restoration was validated before merge.

## Validation

- `SOURCE_MANIFEST_SHA256.txt`: all listed files passed SHA-256 verification.
- `reports/methodology_report/provenance/SHA256SUMS.txt`: all listed files passed SHA-256 verification.
- Methodology helper suite: 9/9 tests passed.
- Historical Python function index: 320 symbols.
- `reports/methodology_report/methodology_report.pdf`: 40 pages and SHA-256 `1e52d36809924df4bc84db65f6cb6669fe33d1f402076e8930b3a173f550595f`.
- No original Excel files or prohibited raw microdata formats were included.
- Historical scientific-source fingerprint: `03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`.

## Packaging cleanup

The browser-uploaded ZIPs had been repackaged. The code upload omitted hidden `.ai_handoff.md`; the exact staged copy was restored only after its SHA-256 matched the source manifest. Non-scientific packaging/cache files were removed during validation.

## Scope

The restored methodology state represents the N=6,627 first-MU analysis and N=4,211 future-progressor sensitivity described in its handoff. The refined N=3,241 longitudinal stage is explicitly later work and is not claimed to be covered by this scientific-source fingerprint.

The historical labels remain in this documentation because it records a specific restoration event. Active report and code paths are purpose-based and versionless.

## Post-restoration repository cleanup

The restored source tree was initially kept under `code/snapshots/` for verification. Once Git became the canonical provenance mechanism, the duplicate snapshot directory was removed from the active tree. The full pre-cleanup state remains recoverable at commit `20a993d92e8cc197a9060180d8cb6a6caf2607a7`.

This cleanup did not reconcile scientific methodologies; it only removed duplicate historical storage from the working tree.
