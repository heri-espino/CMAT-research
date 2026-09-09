# Analysis

Canonical empirical-analysis layer for the CMAT project.

## What belongs here

- privacy-reviewed aggregate tables and figures;
- master analysis outputs and discovery summaries;
- definitions of cohorts and estimands;
- validated null results and sensitivity analyses;
- provenance notes linking retained outputs to code states/fingerprints.

## Canonical rule

The analysis layer is **not organized around Paper 1 or Paper 2**. It preserves the full validated empirical record. Manuscripts select subsets from here; they do not recompute independent scientific versions.

## Inputs

- `code/` canonical scientific pipeline;
- controlled administrative data outside GitHub;
- optional approved pre-MU covariates when available.

## Current layout

`analysis/historical_outputs/` contains the aggregate outputs that were previously committed under `code/outputs/`. They were moved here because generated results are not source code.

These files remain historical until the active pipeline is fully reconciled and a new canonical output set is explicitly frozen. Do not silently treat the directory name `historical_outputs` as evidence that the results are wrong; it means their generating scientific state must be identified before reuse.

## Output policy

Local pipeline runs may write to `code/outputs/`, which is ignored by Git. Only outputs selected for the shared empirical record, reviewed for disclosure/privacy, should be copied or promoted into `analysis/` with provenance documentation.
