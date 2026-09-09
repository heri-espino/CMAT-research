# CMAT technical methodology report — v2

This package is the continuous technical report requested for statistical review. It presents **all current discoveries first** and discusses the proposed publication split only near the end.

## Main files

- `informe_cmat.pdf` — compiled 40-page report.
- `informe_cmat.tex` — LaTeX source.
- `referencias.bib` — report bibliography.
- `figures/` — 24 aggregate figures.
- `tables/` — 50 aggregate CSV outputs plus LaTeX table snippets.
- `notes/paper2_future_plan.md` — user-provided future plan retained as supporting context.
- `provenance/STUDY_PROTOCOL_methodology_v5.md` — current statistical protocol.
- `provenance/METHODOLOGY_CHANGELOG.md` — code/method changes made for this revision.
- `provenance/JOURNAL_DATA_POLICY.md` — current policy check for TEAMAT and Taylor & Francis / Studies in Higher Education.
- `provenance/PRIVACY_AND_RELEASE.md` — privacy/release distinctions and recommendations.

## Major methodological changes in this version

1. Official degree programme is taken from the academic record linked by student ID.
2. BV/RT/BA primary continuous imputation is within-classroom KDE below 7.5 using SciPy default Scott bandwidth; uniform is only the empty-pool fallback.
3. Performance is analysed across exact groups 0/1/2/3/4+, with all 10 Games–Howell pairs and all 10 adjusted FE+Holm pairs.
4. Exact counts 0–12 are shown; the sparse 8–12 tail is explicitly diagnosed.
5. Peak/periodicity analysis is run for all CMAT records and separately for first-MU students during MU.
6. Career summaries and use-vs-performance scatterplots are produced for three distinct populations.
7. The N=4,211 future-Calculus cohort is analysed as a selected progressor sensitivity rather than silently replacing the full N=6,627 first-MU cohort.
8. The report explicitly explains longitudinal analysis, ecological inference limits, cluster-robust inference, multiplicity, and propensity-score limitations.

## Scientific provenance

Scientific source fingerprint (`config/src/tests`):

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

Tests at freeze: **9 passed**.

The refined longitudinal N=3,241 result is preserved as an aggregate snapshot from a later pipeline stage and is explicitly identified in the report as not yet covered by this v5 source fingerprint. Before journal submission, that logic should be reintegrated into one frozen pipeline.

## Privacy

This ZIP must not be described as proof of absolute anonymity. It intentionally excludes the original administrative Excel workbooks and contains only aggregate research products/documentation. See `provenance/PRIVACY_AND_RELEASE.md`.
