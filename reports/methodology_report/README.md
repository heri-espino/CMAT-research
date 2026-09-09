# CMAT methodology report

This directory contains the methodology-focused technical report used for statistical review. It presents the complete current empirical and methodological record first and discusses the proposed publication split only near the end.

## Main files

- `methodology_report.pdf` — compiled 40-page report.
- `methodology_report.tex` — LaTeX source.
- `referencias.bib` — report bibliography.
- `figures/` — 24 aggregate figures.
- `tables/` — 50 aggregate CSV outputs plus LaTeX table snippets.
- `notes/paper2_future_plan.md` — user-provided future plan retained as supporting context.
- `provenance/STUDY_PROTOCOL_methodology_v5.md` — statistical protocol preserved from the historical methodology snapshot.
- `provenance/METHODOLOGY_CHANGELOG.md` — code/method changes recorded for that snapshot.
- `provenance/JOURNAL_DATA_POLICY.md` — policy check for TEAMAT and Taylor & Francis / Studies in Higher Education.
- `provenance/PRIVACY_AND_RELEASE.md` — privacy/release distinctions and recommendations.

## Methodological content

The report documents the later methodology corrections and extensions, including:

1. official degree programme from the academic record linked by student ID;
2. BV/RT/BA primary continuous imputation using within-classroom KDE below 7.5 with SciPy default Scott bandwidth, with uniform only as the empty-pool fallback;
3. exact performance groups `0/1/2/3/4+`, all 10 Games–Howell pairs and all 10 adjusted FE+Holm pairs;
4. exact counts 0–12 with explicit diagnosis of the sparse 8–12 tail;
5. peak/periodicity analysis for all CMAT records and separately for first-MU students during MU;
6. degree-programme summaries and use-vs-performance scatterplots for three distinct populations;
7. the N=4,211 future-Calculus cohort treated as a selected progressor sensitivity rather than replacing the full N=6,627 first-MU cohort;
8. explicit discussion of longitudinal analysis, ecological inference limits, cluster-robust inference, multiplicity and propensity-score limitations.

## Scientific provenance

Historical scientific-source fingerprint associated with this methodology snapshot (`config/src/tests`):

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

Tests at freeze: **9 passed**.

The refined longitudinal N=3,241 result is preserved as an aggregate snapshot from a later pipeline stage and is explicitly identified in the report as not yet covered by this historical source fingerprint. Before journal submission, that logic should be reintegrated into one frozen canonical pipeline.

Version labels such as `methodology_v5` are retained only where they identify historical provenance files or fingerprints. The active report name is purpose-based and versionless because Git now provides project history.

## Privacy

This report directory must not be described as proof of absolute anonymity. It intentionally excludes the original administrative Excel workbooks and contains only aggregate research products/documentation. See `provenance/PRIVACY_AND_RELEASE.md`.
