# Changelog

This file tracks repository-level infrastructure and research-compendium changes. The installable `cmat_analysis` package has its own version metadata in `cmat_analysis/pyproject.toml` and should not be assumed to share repository-level release numbering.

## Unreleased

### Added

- `cmat_analysis.statistics.skew_normal_fit_summary` as a reusable one-component skew-normal specification check for mixture analyses, with synthetic tests and Sphinx documentation.
- `cmat_analysis.statistics.compare_univariate_shape_models` as the canonical same-sample Gaussian K=1 versus skew-normal K=1 versus Gaussian-mixture K=2 comparison, returning likelihood/AIC/BIC diagnostics and criterion preferences.
- A dedicated mixture-model user guide covering Gaussian-mixture selection, posterior responsibilities, bootstrap component testing, and Gaussian-versus-skew-normal interpretation.

- Repository-level `pyproject.toml` for shared tooling configuration.
- Conda environment definition in `environment.yml`.
- Citation metadata in `CITATION.cff`, `CITATION.bib`, and `codemeta.json`.
- Contribution, conduct, security, editor, pre-commit, CODEOWNERS, and issue-template infrastructure.
- Metadata validation workflow for long-lived branches.

### Changed

- Reproduction and README guidance now document both pip and Conda setup paths.
