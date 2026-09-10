# Analysis

Canonical empirical-analysis layer for the CMAT project.

## What belongs here

- privacy-reviewed aggregate tables and figures;
- master analysis outputs and discovery summaries;
- definitions of cohorts and estimands;
- validated null results and sensitivity analyses;
- provenance notes linking retained outputs to code states/fingerprints.

## Canonical rule

The analysis layer preserves the full validated empirical record. Manuscripts select subsets from it; they do not recompute independent scientific versions.

## Inputs

- `../code/` canonical scientific pipeline;
- controlled administrative data outside GitHub;
- optional approved pre-MU covariates when available.

## Organization

- `shared/` — retained aggregate outputs or empirical objects that support the project globally or more than one paper.
- paper-specific reviewed outputs may later be promoted into `../papers/<paper_id>/results/` when they have a clear single manuscript owner; they must still originate from canonical code/runners.
- exploratory analysis folders should be created only when real exploratory work exists; do not add empty scaffolding.

## Current retained outputs

`brainstorm/shared/historical_outputs/` contains aggregate outputs that were previously committed under `code/outputs/`. They are shared provenance/comparison artifacts, not paper-specific ownership.

These files remain historical until the active pipeline is fully reconciled and a new canonical output set is explicitly frozen. `historical_outputs` does not mean the results are known to be wrong; it means the generating scientific state must be identified before reuse.

## Output policy

Local pipeline runs may write to `code/outputs/`, which is ignored by Git. Only outputs selected for the empirical record, reviewed for disclosure/privacy, should be promoted into `brainstorm/shared/` or a paper-local `results/` directory with provenance documentation.
