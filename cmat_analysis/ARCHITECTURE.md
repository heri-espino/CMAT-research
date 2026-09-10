# cmat_analysis architecture

## Design objective

`cmat_analysis` is organized by stable scientific responsibility rather than by the report or notebook that originally required a function. The physical `src/cmat_analysis/` package layout is retained because it cleanly separates repository files from importable Python code. The root package stays deliberately small; callers import capabilities from a named scientific namespace.

## Namespace responsibilities

**`io`** reads source files and validates input shape without making scientific treatment or outcome decisions. **`preprocessing`** performs reusable cleaning and normalization before population construction. **`cohorts`** owns academic-attempt classification, period ordering, visit attachment, revalidation handling used in cohort construction, and reusable population builders. **`measures`** derives analytical variables after cohort membership is known, including grade, pass/fail, and classroom-relative outcomes.

**`statistics`** owns descriptive estimators, robust comparisons, fixed-effect models, uncertainty calculations, threshold diagnostics, and observed-covariate selection adjustment. **`longitudinal`** owns time-indexed service-use diagnostics, regularity, periodicity, and transitions across academic periods. **`ppa`** contains PPA-specific exposure-threshold and MU-to-Calculus progression/persistence analyses because PPA is a stable programme concept rather than a report name; its threshold remains an operational exposure rule, not a randomized cutoff. **`visualization`** converts already-constructed analytical objects into scientific figures and must not silently redefine cohorts or estimands. **`reporting`** contains generic tables, formatting, and provenance; publication/report orchestration should live outside the library. **`privacy`** retains pseudonymisation and disclosure-control helpers.

## Compatibility layer

The former `analysis/` and `study/` namespaces mixed reusable scientific implementations with report history. During this refactor, modules that could be moved without changing their scientific code were relocated into private implementation modules beneath the canonical namespaces and their old locations were replaced by import-only compatibility shims. This means there is one implementation, while historical runners and retained outputs remain reproducible. New code must not depend on the compatibility paths.

Some report-specific orchestration (`study/pipeline.py`, `study/methodology_pipeline.py`, `reporting/methodology_build.py`, `reporting/methodology_report.py`, and the raw-report compatibility stack) remains temporarily in place because it is directly tied to retained historical outputs. It is deliberately excluded from the public API; extraction into the corresponding brainstorm workspace should occur only when its thin runner can be verified end-to-end, rather than deleting provenance during an architectural cleanup.

## Dependency direction

The intended dependency direction is approximately

```text
io / preprocessing
        |
      cohorts
        |
      measures
        |
 statistics ---- longitudinal ---- ppa
        |              |             |
        +------ visualization -------+
                       |
                   reporting
```

This is a design constraint rather than a claim that every existing compatibility module already satisfies the graph. Compatibility shims may point into the canonical layer, but canonical low-level modules must not import historical report builders.

## Public API policy

The package root exports only package metadata. Public scientific functions are selected in namespace `__init__.py` files; implementation modules beginning with `_` are not public API. Historical Spanish-named plotting/testing modules retained for reproduction are available by explicit module path but are not re-exported from canonical package roots. Deprecation shims must contain no scientific implementation and can be removed once repository consumers stop importing them.

## Scientific-change firewall

This refactor treats existing scientific behavior as invariant. Relocated implementation blobs are byte-identical wherever possible. No formula, threshold, cohort rule, imputation method, standardization rule, clustering definition, treatment of administrative attempts, or causal interpretation is changed merely to improve software structure. Potential scientific changes require a separate review and tests targeted at the estimand or cohort they affect.
