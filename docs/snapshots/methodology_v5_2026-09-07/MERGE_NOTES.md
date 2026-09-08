# Merge notes — exact methodology v5 / technical report v2 restoration

This restoration was validated before opening the pull request.

## Validation

- `SOURCE_MANIFEST_SHA256.txt`: all listed files pass SHA-256 verification.
- `reports/technical_report_methodology_v2/provenance/SHA256SUMS.txt`: all listed files pass SHA-256 verification.
- Methodology helper suite: 9/9 tests pass.
- `PYTHON_FUNCTION_INDEX.md`: 320-symbol inventory present.
- `informe_cmat.pdf`: 40 pages and SHA-256 `1e52d36809924df4bc84db65f6cb6669fe33d1f402076e8930b3a173f550595f`.
- No original Excel files or prohibited raw microdata formats are included.
- Historical scientific-source fingerprint remains `03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`.

## Packaging cleanup

The browser-uploaded ZIPs had been repackaged. The code upload omitted hidden `.ai_handoff.md`; the exact staged copy was restored only after its SHA-256 matched the source manifest. Non-scientific `__MACOSX`, `.pytest_cache`, `.DS_Store`, and Python 3.12 bytecode generated during restoration validation were removed. Manifest-listed historical Python 3.13 bytecode remains because it is part of the preserved snapshot.

## Scope

The restored methodology-v5 snapshot represents the N=6,627 first-MU analysis and N=4,211 future-progressor sensitivity described in its handoff. The refined N=3,241 longitudinal stage remains explicitly later work and is not claimed to be covered by the v5 scientific-source fingerprint.

This PR also removes the temporary recovery workflow that had been accidentally merged into `main` during the earlier incomplete restoration attempt.
