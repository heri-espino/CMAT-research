# Paper 2 literature index — MU performance

This index prioritizes literature directly relevant to mathematics-support use and academic performance in first-attempt MU. Use `../../library/CATALOG.md` to locate preferred source records and exact source-material paths.

## Core mathematics-support evidence

### `mullen_2024_mathematics-statistics-support-review`
- Priority: **core**.
- Role: broad current review of mathematics/statistics support impact/evaluation; principal field anchor.

### `lawson_2019_mathematics-support-literature-review`
- Priority: **core**.
- Role: field review and institutional context.

### `mac-an-bhaird_2009_mathematics-support-centre-grades`
- Priority: **core**.
- Role: direct support-centre attendance/grade comparator.

### `jacob_2018_mathematics-support-impact-irish-university`
- Priority: **core**.
- Role: longitudinal mathematics-support/outcome evidence.

### `berry_2015_mathematics-learning-support-at-risk-students`
- Priority: **core**.
- Role: use/performance among at-risk students; relevant for selection and heterogeneous need.

### `matthews_2013_evaluation-mathematics-support-centres`
- Priority: **core**.
- Role: evaluation approaches for mathematics-support centres.

### `pell_2008_mathematics-support-for-all`
- Priority: **core**.
- Role: participation/outcome context.

### `navarra-madsen_2010_mathematics-tutoring-student-success`
- Priority: supporting/core comparator.
- Role: mathematics tutoring and student success.

### Additional support-setting sources

- `mac-an-bhaird_2013_non-engagement-mathematics-support` — non-engagement/barriers to support use.
- `ni-fhloinn_2016_gender-engagement-mathematics-support` — heterogeneity in mathematics-support engagement.
- `johns_2026_performance-assessment-mathematics-tutoring-centres` — recent tutoring-centre assessment/evaluation context.
- `tinsley_2018_math-help-centers-student-perceptions` — student perceptions/help-centre context.

## Academic help-seeking / selection context

### `fong_2023_academic-help-seeking-achievement`
- Priority: **core**.
- Role: meta-analytic anchor linking academic help-seeking and achievement.
- Limitation: help-seeking is endogenous; attendance is not randomized treatment.

### Supporting help-seeking theory/evidence

- `karabenick_1991_academic-help-seeking-learning-strategies` — help-seeking and learning strategies.
- `karabenick_2001_help-large-college-classes` — heterogeneity in who seeks help and from whom.
- `karabenick_2011_self-regulated-help-seeking` — formal/self-regulated help-seeking framework.
- `kahu_2013_student-engagement-framework` — broader engagement framing; secondary in Paper 2.

## Encouragement / intervention comparators

- `pugatch_2018_nudging-peer-tutoring-higher-education` — encouragement toward peer tutoring; useful for uptake/outcome contrast.
- `paloyo_2016_supplemental-instruction-academic-performance` — randomized encouragement design; useful causal contrast to observational CMAT use.

These comparators help distinguish what stronger identification can estimate; their causal estimates should not be mapped onto CMAT.

## Selection / observational methods

### `austin_2011_propensity-score-confounding`
- Priority: **methods**.
- Role: practical propensity-score/confounding guidance for observational sensitivity analyses.

### `rosenbaum_1983_propensity-score-causal-effects`
- Priority: **methods**.
- Role: foundational propensity-score methodology.

These sources support adjustment/sensitivity language. They do **not** turn the primary CMAT design into a causal estimate because important pre-treatment variables, including baseline mathematics proficiency, are incomplete in the current administrative data.

## Measurement and classroom heterogeneity

Paper 2 uses classroom-relative performance:

`Z = (grade - classroom mean) / classroom sample SD`

with classroom defined as professor × subject × period and a minimum valid classroom size.

- `kjaergaard_2024_gradeless-learning-academic-performance` — secondary assessment/performance context.

Literature directly motivating this exact standardisation remains a targeted gap. Statistical references for heteroskedastic inference, clustered uncertainty and multiple comparisons belong in the manuscript methods bibliography rather than being treated as substantive mathematics-support evidence.

## Current empirical interpretation to protect

The exact visit-group analysis distinguishes two questions:

1. **use vs non-use** — robust separation between zero visits and positive use;
2. **dose among users** — no robust monotone ordering among 1, 2, 3 and 4+ after multiplicity-aware comparisons.

Paper 2 should distinguish:

- complete first-MU cohort (`N=6,627` in the current documented snapshot) for contemporaneous MU performance;
- later-Calculus progressor subset (`N=4,211`) as a selected future-conditioned sensitivity/population, not a replacement estimand.

Do not describe the observational pattern as a causal dose-response without stronger identification.
