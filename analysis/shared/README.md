# Shared analysis outputs

This directory contains retained aggregate empirical artifacts that are project-wide or support more than one paper.

## Current contents

- `historical_outputs/` — aggregate outputs preserved from an earlier canonical pipeline state for provenance and comparison.

## Rule

Do not place raw/row-level institutional data here. Outputs must be aggregate/privacy-reviewed and traceable to code/configuration. When an output has a clear single-paper owner and is intentionally retained for that manuscript, it may be promoted to `papers/<paper_id>/results/`; do not duplicate the same retained artifact in both places without a documented reason.
