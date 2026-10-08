# Paper 2.2.1 — Independent manuscript workspace

The inherited root `paper/main.tex`, `paper/sections/*`, `paper/notebook.ipynb` and Paper 2.1 build orchestration remain the older manuscript. This new workspace is intentionally separate.

- `main.tex` — substantive **English draft** with complete research motivation, data/outcome contracts, estimation, clustered selection, stability, honest inference, limitations and explicitly unfilled results/declarations.
- Support-centre literature is reused from inherited `paper/references.bib`. The separate `methods_references.bib` adds verified methodological references on fused lasso, generalised lasso, stability selection and post-selection inference. This preserves the inherited Paper 2.1 bibliography unchanged.
- Figures in `results/paper221/figures/` are included conditionally after the controlled-data experiment runs.
- Compile from this directory: `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`.
- GitHub Actions compiles on explicit manual request and exports the PDF in a short-lived artifact, **never** commits build PDFs.

A completed draft does not mean a completed experiment or a submission-ready article. All numerical claims require verified `results/paper221/` provenance.