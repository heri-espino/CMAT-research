# CMAT branch strategy

`main` is the stable, reviewable source of truth. Scientific or manuscript work should not be developed directly on `main`; it should enter through a focused branch and a pull request once its scope is complete.

## Working branches

| Branch | Purpose | What ChatGPT is doing there | Merge condition |
|---|---|---|---|
| `method/reconcile-v8-v5` | Reconcile the historical v8 longitudinal pipeline with the later methodology-v5 corrections | Compare both code paths function by function; preserve PPA longitudinal logic; port corrected KDE imputation, all-pair 0/1/2/3/4+ contrasts, 4,211-progressor sensitivity, population-specific periodicity, and degree-programme analyses; update tests and fingerprint | One canonical pipeline, all tests passing, no lost v8 functionality, new function index/protocol/handoff/fingerprint |
| `analysis/all-discoveries` | Master empirical analysis independent of publication framing | Preserve **all** validated discoveries, tables, figures, sensitivities, cohort definitions, null results and caveats; avoid organizing findings around Paper 1 or Paper 2 | Every retained result is reproducible from the canonical pipeline and its provenance is documented |
| `report/technical-methodology` | Continuous technical report for statistical review | Rewrite the report as one methodological/results narrative with detailed mathematics, assumptions, formulas, estimands and diagnostics; the paper split appears only at the end | Report compiles cleanly, every numerical claim maps to an output, no causal overstatement, methodology fully specified |
| `paper1/ppa-persistence` | Paper 1 manuscript | Develop the PPA1 / formal-help-seeking persistence manuscript after the canonical pipeline is stable; later integrate survey and pre-MU mathematics measures if obtained | RQs, estimands and tables are frozen; literature gap closed; results reproduced from canonical outputs; submission checks completed |
| `paper2/mu-performance` | Paper 2 manuscript | Develop the CMAT-use / classroom-relative MU performance manuscript, TEAMAT-first, using the final contemporaneous analysis | Canonical MU analysis frozen; exact visit-group and sensitivity results finalized; journal framing and supplement plan complete |
| `literature/heavy-batch2` | Preserve second heavy bibliography batch | Import the 29-PDF / 322-asset second Docling batch into `literature/Bib2/` with checksum/provenance, then update indices/cards as needed | Binary transfer complete, counts/checksums verified, no administrative microdata introduced |
| `privacy/release-controls` | Privacy, governance and release rules | Audit tracked files, define what can be public/private, distinguish hashing/pseudonymization/anonymization, document journal data-sharing constraints and safe release procedure | No raw identifiers or administrative microdata tracked; release checklist and data-availability language ready |
| `integration/reproducible-pipeline` | Final integration/staging branch | Merge tested methodology, analysis, report, privacy and manuscript-ready outputs in dependency order before promotion to `main` | CI/tests/LaTeX builds pass; fingerprints and manifests updated; branch diffs reviewed |

## Dependency order

The intended dependency chain is:

`method/reconcile-v8-v5`
→ `analysis/all-discoveries`
→ `report/technical-methodology`
→ `paper1/ppa-persistence` and `paper2/mu-performance`
→ `integration/reproducible-pipeline`
→ `main`.

`privacy/release-controls` applies across every stage. `literature/heavy-batch2` can proceed independently, but literature indices used by a manuscript should be refreshed before that manuscript is frozen.

## Important separation

The **master analysis must not be pruned to fit the papers**. All validated discoveries remain in `analysis/all-discoveries` and the technical report. Paper branches select a defensible subset only after the empirical record is complete.

Likewise, a manuscript branch must not silently change scientific methodology. If a paper exposes a methodological problem, the correction returns first to `method/reconcile-v8-v5` (or a new method branch), is tested, and only then flows back into the paper.

## Privacy boundary

No branch may add administrative Excel files, row-level student/advising microdata, direct identifiers, HMAC keys, credentials, or unreviewed free-text fields. Heavy literature PDFs/Docling assets are allowed only because this repository is private and the owner explicitly requested archival preservation.

## Pull-request rule

Each substantive branch should eventually open a PR documenting:

1. what changed;
2. which estimand/result/document is affected;
3. tests/builds run;
4. source fingerprint before/after if scientific code changed;
5. privacy implications;
6. unresolved questions.
