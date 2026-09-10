# Brainstorm branch — Proyecto Visitas historical workspace

Branch: `brainstorm/proyecto-visitas`

## Purpose

This branch preserves the historical `proyecto visitas/` work from the separate repository `heri-espino/CMAT` as a research-development workspace. It is **not** a sixth publication branch and it is **not** part of the public API of `cmat_analysis`.

The shared upstream remains `main` and owns:

- `cmat_analysis/`
- `data/`
- `literature/`
- `brainstorm/`
- `docs/`

This branch inherits that upstream and adds the historical project under:

```text
brainstorm/proyecto_visitas/
```

## Source provenance

Imported source:

- repository: `heri-espino/CMAT`
- source ref: `main`
- source subtree: `proyecto visitas/`
- source tree SHA at import planning: `06be56b28e2dacb8b7d53a490e55274fda34be70`

Only that subtree is imported; the rest of the old `CMAT` repository must not be copied into this branch.

## Scientific status

Everything under `brainstorm/proyecto_visitas/` is historical exploratory/research-development material. In particular, the LaTeX report under the imported `reportes/` tree is classified as **brainstorm/provenance**, not as a submission-ready paper.

The historical `src/visitas_analysis/` code is preserved for provenance and reproducibility. It must not silently replace or override the shared modern library in `cmat_analysis/`. If a historical function is still scientifically useful, review it against the modern implementation and migrate the reusable capability upstream through the repo-admin workflow rather than copying it directly.

## Privacy and import sanitation

The new repository has stricter privacy rules than the historical source. The import therefore preserves scientific code, aggregate outputs, figures, references, LaTeX and notebook source while excluding direct student-level exported tables. Notebook outputs are cleared during import so historical rendered outputs cannot reintroduce student identifiers.

At minimum, these historical row-level exports are excluded:

- `output_visitas/report_assets/tables/student_summary.csv`
- `output_visitas/report_assets/tables/top_students_by_visits.csv`
- `output_visitas/report_assets/tables/lorenz_visits.csv`

LaTeX auxiliary/build files such as `.aux`, `.log`, `.out`, `.toc`, `.synctex.gz` and Windows shortcut files are also excluded; the `.tex` source and compiled PDF are retained.

## Branch direction

Like paper branches, this branch should normally receive updates from `main`:

```text
main -> brainstorm/proyecto-visitas
```

Do **not** merge the whole branch back into `main`. Reusable scientific improvements should be reviewed and integrated selectively into `main/cmat_analysis/` or the canonical shared `brainstorm/` record.

## Coordination

Repository-wide architectural decisions remain under the repo-admin / integrator / upstream-maintainer workflow defined in `docs/REPO_GOVERNANCE.md`. A chat working specifically on this branch may inspect, reconstruct and interpret the historical Proyecto Visitas work, but should not redesign shared infrastructure independently.
