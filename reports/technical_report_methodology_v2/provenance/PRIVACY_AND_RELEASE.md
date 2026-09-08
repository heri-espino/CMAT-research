# Privacy, pseudonymization, anonymization, and release plan

## Concepts that must remain distinct

- **SHA-256 file hash:** integrity/provenance. It demonstrates that the bytes have not changed; it does not hide identities.
- **HMAC-SHA256 pseudonym:** deterministic linkage under a secret key. It removes the obvious identifier but remains linkable and may be re-identifiable when combined with rare attributes.
- **Anonymization:** a risk state in which identification is not reasonably possible under the relevant threat model. Rich longitudinal education data make absolute guarantees inappropriate.

## Strongest practical public-release strategy

For these CMAT administrative data, the most privacy-preserving reproducibility strategy is **not to release row-level historical microdata publicly**. Instead:

1. Release source code, environment specification, analysis protocol, and aggregate tables/figures.
2. Release a synthetic dataset with the same schema for running the pipeline.
3. Do not release persistent student or professor pseudonyms in public files.
4. Generalize or suppress rare degree-program × term × outcome combinations.
5. Coarsen dates to the minimum temporal resolution scientifically necessary.
6. Remove free text and any adviser/professor names not required for reproducibility.
7. Top-code or bin rare extreme visit counts where row-level outputs are ever released.
8. Apply formal statistical disclosure-control review before any microdata release; k-anonymity/l-diversity/t-closeness can be diagnostics but are not absolute privacy guarantees.
9. For released aggregate statistics, differential privacy could be considered only if a formal public-data product is required and a privacy budget can be justified.
10. Prefer controlled-access review environments over public microdata when the institution authorizes reviewer/researcher access.

## What is in this report package

Only aggregate CSVs, figures, LaTeX source, documentation, hashes, and methodological notes. The two original Excel files are intentionally excluded.
