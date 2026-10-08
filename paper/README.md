# Paper 2.2.1 — Ordered attendance regimes

**Initial experiment implementation and English manuscript draft; controlled-data execution pending.** This branch explores whether the eight ordered CMAT visit-frequency categories should be fused into a smaller number of stable adjacent blocks using **fused lasso**, cluster-aware validation and independent post-selection inference.

Start with `../PAPER_BRANCH.md`, `AI_HANDOFF.md`, and `docs/README.md`; the full scientific and statistical specification is in `docs/analysis/FUSED_LASSO_PROTOCOL.md` and `docs/analysis/VALIDATION_AND_INFERENCE_221.md`.

The entire Paper 2.1 implementation and draft were inherited as a provenance checkpoint. **Do not treat `sections/`, `notebook.ipynb`, `paper_build.py`, `results/paper21/` or any inherited plots as Paper 2.2.1 deliverables.** A new manuscript/build procedure will be planned only after results exist.

This is an observational analysis. Penalty-selected boundaries do not imply causal visit thresholds, equivalent student types, or a priori participation regimes.
## Current entry points

- `code/run_paper221_fused.py --check` preflight without institutional data.
- `code/run_paper221_fused.py` estimates partitions, clustered CV, bootstrap and locked Wald when controlled data are accessible.
- `code/figures_paper221.py` renders approved aggregate result figures.
- `paper/paper221/main.tex` holds the **separate 2.2.1 LaTeX working draft**; it is not a revision of inherited Paper 2.1 files.
- `notes/README.md` tracks chronological run results, interpretation decisions and unresolved issues.
- `.github/workflows/paper221-experiments.yml` is manual-only and exports aggregates and manuscript PDF as Actions artifacts.
