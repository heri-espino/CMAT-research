# Paper 2.2.1 — Independent manuscript workspace

The inherited root `paper/main.tex`, `paper/sections/*`, `paper/notebook.ipynb` and Paper 2.1 build orchestration remain the older manuscript. This new workspace is intentionally separate.

- `main.tex` — substantive **English draft** with research motivation, outcomes, estimation, clustered selection, internal validation and limitations. It now includes the data-derived `results_221.tex` section; several sensitivity analyses and declarations remain pending.
- Support-centre literature is reused from inherited `paper/references.bib`. The separate `methods_references.bib` adds verified methodological references on fused lasso, generalised lasso, stability selection and post-selection inference. This preserves the inherited Paper 2.1 bibliography unchanged.
- Figures in `results/paper221/figures/` are included conditionally after the controlled-data experiment runs.
- Compile from this directory: `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`.
- GitHub Actions compiles on explicit manual request and exports the PDF in a short-lived artifact, **never** commits build PDFs.

The initial 100-replicate full computational run is available in `results/paper221/` and summarised in `notes/2026-10-07_fused_lasso_100_bootstrap_results.md`. The draft is **not submission ready**: complete-case and alternative tuning/cluster sensitivities, data governance language, and a literature/methodological review remain pending.