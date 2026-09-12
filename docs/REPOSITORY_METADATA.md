# Repository metadata and environment conventions

CMAT Research uses repository-level metadata to make the project easier to clone, cite, validate, and reproduce without duplicating the package definition in `cmat_analysis/`.

## Canonical files

| File | Purpose |
| --- | --- |
| `pyproject.toml` | Repository-level tooling configuration only. |
| `cmat_analysis/pyproject.toml` | Canonical installable-package metadata and Python dependencies. |
| `environment.yml` | Conda environment entry point, delegating Python package installation to `cmat_analysis`. |
| `CITATION.cff` | GitHub-native citation metadata. |
| `CITATION.bib` | Convenience BibTeX record for the research compendium. |
| `codemeta.json` | Machine-readable CodeMeta metadata. |
| `REPRODUCING.md` | Reproduction and environment instructions. |
| `CONTRIBUTING.md` | Contribution and branch-governance expectations. |
| `SECURITY.md` | Private reporting guidance for vulnerabilities and sensitive-data exposures. |
| `.pre-commit-config.yaml` | Lightweight repository hygiene checks. |
| `.editorconfig` | Cross-editor whitespace and encoding conventions. |
| `.github/CODEOWNERS` | Default review ownership. |

The root `pyproject.toml` intentionally does not define a second installable distribution because `cmat_analysis/pyproject.toml` is already the canonical package definition. Duplicating dependencies or package versions at the repository root would create two sources of truth.

## Environment policy

The supported Python line is 3.14. Pip users install the editable package from `cmat_analysis`; Conda users create `environment.yml`, which installs Python, Git LFS, and the same editable package with development and documentation extras. Scientific dependency pins remain in `cmat_analysis/pyproject.toml` so both setup paths resolve through the same package metadata.

A platform-specific Conda lock file is not committed until lock generation is automated for the supported operating systems, because a manually maintained lock would otherwise imply portability that has not been tested.

## Citation and archival policy

Repository citation metadata describes the research compendium and its maintainer; it does not determine authorship of future papers. Paper-specific author lists, acknowledgements, journal metadata, and final citations belong on the relevant publication branch and should be updated when a manuscript receives a persistent identifier.

No DOI or Zenodo deposition metadata is asserted before an actual archival release. When such a release is made, update `CITATION.cff`, `codemeta.json`, and the paper-specific metadata together rather than inventing a placeholder DOI.

## Rights and data boundary

Repository visibility does not grant a blanket license to third-party scholarly PDFs, controlled institutional data, or other materials for which the repository owner does not hold redistribution rights. The root `LICENSE` defines the current repository-wide default, while separate future licenses may cover explicitly identified code, documentation, data releases, or publications.
