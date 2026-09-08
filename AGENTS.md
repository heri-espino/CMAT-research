# CMAT repository operating rules

## Canonical repository model

`main` is the source of truth. Organize the project by subfolder; use branches only as short-lived workspaces for concrete changes.

Read `docs/BRANCH_STRATEGY.md` before creating or reusing a branch.

## Scientific dependency rule

Maintain one scientific chain:

`controlled data -> code/ -> analysis/ -> reports/ and papers/`.

Do not create manuscript-specific scientific pipelines. If Paper 1 or Paper 2 needs a methodological change, implement and validate it in the canonical code first.

## Preservation rule

Historical snapshots may be retained for provenance, but must be clearly labeled as historical and must not silently overwrite the canonical path.

## Data/privacy boundary

Never commit:

- administrative Excel workbooks;
- row-level student/advising microdata;
- direct student or professor identifiers;
- HMAC/secret keys;
- credentials/tokens;
- unreviewed identifying free text.

Aggregated outputs may be committed after privacy review. Heavy literature PDFs and Docling assets are allowed in this private repository because the owner explicitly requested archival preservation; treat them as internal research material, not automatically redistributable content.

## Analysis/reporting rules

- Preserve all validated discoveries in the master analysis and technical report, including null results and sensitivity analyses.
- Keep causal language conservative for student-selected CMAT use.
- Classroom is `instructor × course × academic period` unless a later reviewed methodological change explicitly replaces it.
- Scientific-code changes require updated tests, documentation and source fingerprint.
- Paper-specific selections happen after canonical outputs are stable.

## Documentation

Major folders should have a README explaining scope, inputs, outputs, canonical status and dependencies. Update the project handoff/changelog whenever code or estimands change.
