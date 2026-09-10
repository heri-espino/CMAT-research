# Brainstorm

`brainstorm/` is the shared research-development layer and replaces the former `reports/` concept. It is where questions are explored broadly, diagnostics and nulls are retained, sensitivities are compared, and methodological reasoning is documented before evidence is selected into a paper.

A brainstorm may have a thin local `code/` runner, notes, tables, figures and provenance, but reusable calculations remain in `cmat_analysis`. `shared/` preserves cross-topic historical aggregate outputs and provenance.

## Shared versus branch-specific brainstorms

Most programme-level brainstorms belong directly in `main/brainstorm/`. Exceptionally, a large historical or exploratory workspace may live on a dedicated long-lived `brainstorm/*` branch when importing it into `main` would mix substantial legacy code/assets with the shared upstream.

Registered branch-specific historical workspace:

- `brainstorm/proyecto-visitas` — sanitized import of only `proyecto visitas/` from the older `heri-espino/CMAT` repository. Its historical LaTeX report is brainstorm/provenance, not a paper manuscript; its old `visitas_analysis` package is preserved for reconstruction and must not override `cmat_analysis`.

See `docs/REPO_GOVERNANCE.md` for branch direction and promotion rules.
