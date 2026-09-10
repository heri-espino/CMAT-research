# cmat_analysis migration map

This map records the architectural move from report-history namespaces to responsibility-based namespaces. `shim` means the old path contains imports only and delegates to the single canonical implementation.

| Previous path | Scientific responsibility | Canonical path | Status |
|---|---|---|---|
| `analysis/cleaning.py` | input cleaning | `preprocessing/cleaning.py` | moved; old path is shim |
| `analysis/parametric_tests.py` | parametric diagnostics | `statistics/parametric.py` | moved; old path is shim; legacy API not root-exported |
| `analysis/nonparametric_tests.py` | non-parametric diagnostics | `statistics/nonparametric.py` | moved; old path is shim; legacy API not root-exported |
| `analysis/grade_analysis.py` | grade figures | `visualization/grade_distributions.py` | moved; old path is shim; legacy API not root-exported |
| `study/cohort.py` | attempts/cohorts/exposure attachment | `cohorts/attempts.py` | moved; old path is shim |
| `study/outcomes.py` | grade/pass measures | `measures/grades.py` | moved; old path is shim |
| `study/statistics.py` | descriptive/inferential statistics | `statistics/inference.py` | moved; old path is shim |
| `study/selection.py` | propensity ATT sensitivity | `statistics/selection.py` | moved; old path is shim |
| `study/extended_analysis.py` | robust/group/career comparisons | `statistics/group_comparisons.py` | moved; old path is shim |
| `study/extended_methodology.py` | reusable visit-dose methodology diagnostics | `statistics/methodology.py` | moved; old path is shim |
| `study/methodology_plots.py` | methodology figures | `visualization/methodology.py` | moved; old path is shim |
| `study/temporal.py` | timing/regularity/periodicity | `longitudinal/temporal.py` | moved; old path is shim |
| `study/ppa_progression.py` | PPA progression/persistence | `ppa/progression.py` | moved; old path is shim |
| `study/plots.py` | study figures | `visualization/study.py` | moved; old path is shim |
| `study/ppa_plots.py` | PPA figures | `visualization/ppa.py` | moved; old path is shim |
| `study/extended_plots.py` | exploratory figures | `visualization/exploratory.py` | moved; old path is shim |
| `reporting/run_log.py` | run provenance | `reporting/provenance.py` | moved; old path is shim |

## Deliberately retained compatibility/orchestration

`analysis/raw_report_figures.py`, `analysis/report_compatible/`, `pipeline/`, `study/pipeline.py`, `study/methodology_pipeline.py`, `reporting/methodology_build.py`, and `reporting/methodology_report.py` remain outside the public API because they orchestrate or reproduce specific historical reports. They should be extracted to a brainstorm workspace only with an end-to-end reproduction check; no new reusable functionality should be added to them.

## Consumer rule

New and actively edited code should use canonical imports. Existing compatibility imports are tolerated only to preserve historical runners until those consumers are touched for substantive work.
