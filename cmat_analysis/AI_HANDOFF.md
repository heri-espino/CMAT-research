# AI handoff: cmat_analysis

`cmat_analysis` is the reusable scientific library of the CMAT repository. Treat `brainstorm/**/code/` as research orchestration and paper-branch `code/` as publication orchestration; neither should duplicate reusable scientific implementations that belong here.

## Architecture contract

The package uses the standard `src` layout at `cmat_analysis/src/cmat_analysis/`. Do not remove or flatten that layout. Public imports should use responsibility-based namespaces: `io`, `preprocessing`, `cohorts`, `measures`, `statistics`, `longitudinal`, `ppa`, `visualization`, `reporting`, and `privacy`.

The historical `analysis/`, `study/`, and `pipeline/` paths are compatibility/orchestration surfaces, not destinations for new reusable code. Several former modules are now shims that delegate to canonical namespaces; do not reintroduce implementations into those shims.

The reviewed public API is defined by namespace `__all__` declarations and documented in `PUBLIC_API.md`. Before changing public names, exports, semantics, or compatibility aliases, also read `API_REVIEW_BACKLOG.md`; its entries are intentionally unresolved semantic/API questions and must not be changed opportunistically.

## Scientific invariants

Architecture work must not silently change cohort definitions, passing grade, treatment/exposure definitions, the PPA threshold, classroom construction, grade standardization, inclusion/exclusion logic, statistical estimands, confidence-interval formulas, clustering, administrative-attempt handling, same-day visit interpretation, or retained scientific results. If a potential scientific bug is discovered during software work, document it for explicit review instead of correcting it opportunistically.

## Adding code

1. Identify the scientific responsibility before choosing a module.
2. Search `FUNCTION_INDEX.md` and the Sphinx API before writing a parallel implementation.
3. Keep low-level preprocessing independent of higher-level statistics and reporting.
4. Put a NumPy-style module docstring on public modules and NumPy-style docstrings on public functions/classes, documenting units, scales, assumptions, and limitations when methodologically relevant.
5. Add type hints to public interfaces when they can be stated without changing behavior.
6. Add or update tests under `cmat_analysis/tests/` by scientific component.
7. Run editable installation, import tests, `pytest`, and the Sphinx `-W` build before declaring success.
8. Regenerate `FUNCTION_INDEX.md` with `python cmat_analysis/scripts/generate_function_index.py` (the main-branch workflow also enforces this).

## Dependency direction

Prefer dependencies that flow from input/cleaning to cohorts to measures to statistics/longitudinal/PPA and finally visualization/reporting. Avoid circular imports and avoid making basic data transformations depend on report builders.

See `ARCHITECTURE.md` for the namespace rationale, `MIGRATION_MAP.md` for the current-path-to-canonical-path mapping, `PUBLIC_API.md` for the stable documentation surface, and `API_REVIEW_BACKLOG.md` for deferred semantic/API decisions.
