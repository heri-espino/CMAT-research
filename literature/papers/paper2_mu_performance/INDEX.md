# Paper 2 literature index — MU performance

This index prioritizes literature directly relevant to mathematics-support use and academic performance in first-year MU.

## Core mathematics-support literature

### `mullen_2024_mathematics-statistics-support-review`
- Priority: **core**
- Role: broad evidence review of mathematics/statistics support.
- Used in: Introduction, literature review, limitations.

### `lawson_2019_mathematics-support-literature-review`
- Priority: **core**
- Role: field review; useful for positioning CMAT relative to mathematics-support scholarship.

### `matthews_2013_evaluation-mathematics-support-centres`
- Priority: **core**
- Role: evaluation of mathematics-support centres and common assessment approaches.

### `pell_2008_mathematics-support-for-all`
- Priority: **core**
- Role: mathematics-support participation and outcomes.

### `berry_2015_mathematics-learning-support-at-risk-students`
- Priority: **core**
- Role: direct relationship between mathematics-support usage and performance among at-risk students.
- Use carefully: compare design/population before drawing parallels to CMAT.

### `jacob_2018_mathematics-support-impact-irish-university`
- Priority: **core**
- Role: mathematics-support impact evidence in university context.

### `mac-an-bhaird_2009_mathematics-support-centre-grades`
- Priority: **core**
- Role: centre use and grades; useful comparator for CMAT’s performance analysis.

### `johns_2026_performance-assessment-mathematics-tutoring-centres`
- Priority: supporting
- Role: contemporary tutoring-centre performance assessment framework.

### `ni-fhloinn_2016_gender-engagement-mathematics-support`
- Priority: supporting
- Role: heterogeneity in engagement with mathematics support.

## Academic help-seeking

### `fong_2023_academic-help-seeking-achievement`
- Priority: **core**
- Role: meta-analytic anchor linking academic help-seeking and achievement.
- Important limitation: help-seeking is endogenous; the CMAT analysis must not interpret attendance as randomized treatment.

### `karabenick_1991_academic-help-seeking-learning-strategies`
### `karabenick_2001_help-large-college-classes`
### `karabenick_2011_self-regulated-help-seeking`
- Priority: supporting
- Role: theory and empirical background on who seeks help, why, and how help-seeking relates to learning strategies.

## Selection / observational methods

### `austin_2011_propensity-score-confounding`
- Priority: **methods**
- Role: propensity-score/confounding guidance for observational sensitivity analyses.

### `rosenbaum_1983_propensity-score-causal-effects`
- Priority: **methods**
- Role: foundational propensity-score methodology.

These sources support adjustment/sensitivity language. They do **not** turn the primary CMAT design into a causal estimate because important pre-treatment variables, including baseline mathematics proficiency, are currently incomplete.

## Measurement and classroom heterogeneity

The paper’s distinctive measurement choice is classroom-relative performance:

`Z = (grade - classroom mean) / classroom sample SD`

with classroom defined by professor × subject × period and a minimum valid classroom size. Literature directly motivating this exact standardisation remains a targeted gap; statistical references for heteroskedastic inference and clustered uncertainty belong in the manuscript methods bibliography rather than being treated as substantive mathematics-support literature.

## Main empirical contrast to prior work

CMAT’s exact visit-group analysis should be used to distinguish two empirical patterns:

1. **use vs non-use**: robust separation between zero visits and positive use;
2. **dose among users**: no robust monotone ordering among 1, 2, 3 and 4+ after multiplicity correction.

Literature should be reviewed for whether prior mathematics-support studies explicitly separate these two questions. Do not describe CMAT’s observational pattern as a dose-response effect without stronger identification.
# Paper 2 literature index

All IDs resolve to `../../library/articles/<id>.md`.

## Core mathematics-support evidence

| Literature ID | Role in Paper 2 |
|---|---|
| `mullen_2024_mathematics-statistics-support-review` | Broad current review of MSS impact and evaluation; principal field anchor. |
| `lawson_2019_mathematics-support-literature-review` | Mathematics-support literature synthesis and institutional context. |
| `mac-an-bhaird_2009_mathematics-support-centre-grades` | Direct support-centre attendance/grade comparator. |
| `jacob_2018_mathematics-support-impact-irish-university` | Longitudinal support/outcome evidence. |
| `berry_2015_mathematics-learning-support-at-risk-students` | Use/performance among at-risk students; relevant for selection and heterogeneous need. |
| `matthews_2013_evaluation-mathematics-support-centres` | Evaluation of mathematics-support centres. |
| `pell_2008_mathematics-support-for-all` | Participation/outcome context. |
| `navarra-madsen_2010_mathematics-tutoring-student-success` | Mathematics tutoring and student success. |
| `mac-an-bhaird_2013_non-engagement-mathematics-support` | Non-engagement and barriers to support use. |
| `ni-fhloinn_2016_gender-engagement-mathematics-support` | Heterogeneity in mathematics-support engagement. |
| `johns_2026_performance-assessment-mathematics-tutoring-centres` | Recent evaluation/assessment framework for tutoring centres. |
| `tinsley_2018_math-help-centers-student-perceptions` | Student perceptions and help-centre context. |

## Help-seeking / selection context

- `fong_2023_academic-help-seeking-achievement` — meta-analytic anchor; useful for discussing why support users are a selected group.
- `karabenick_1991_academic-help-seeking-learning-strategies` — help-seeking and learning strategies.
- `karabenick_2001_help-large-college-classes` — heterogeneity in who seeks help and from whom.
- `karabenick_2011_self-regulated-help-seeking` — formal help-seeking framework.
- `kahu_2013_student-engagement-framework` — broader engagement framing; secondary in Paper 2.

## Encouragement/intervention comparators

- `pugatch_2018_nudging-peer-tutoring-higher-education` — encouragement toward peer tutoring; important comparator for support uptake and outcomes.
- `paloyo_2016_supplemental-instruction-academic-performance` — randomized encouragement design; useful causal contrast to the observational CMAT design.

## Statistical / design references

- `rosenbaum_1983_propensity-score-causal-effects` — propensity-score foundation if propensity-based sensitivity/adjustment is retained.
- `austin_2011_propensity-score-confounding` — practical propensity-score guidance.

These references support methodology, not a claim that the current CMAT estimates are causal.

## Assessment/performance context

- `kjaergaard_2024_gradeless-learning-academic-performance` — assessment/performance context; secondary.

## Current empirical interpretation to protect

The strongest reproducible separation in the current work is approximately `0 visits` versus `any positive use`; the evidence does not support describing 1, 2, 3, and 4+ visits as a clean monotone causal dose-response.

Paper 2 should distinguish:

- complete first-MU cohort (`N=6,627` in the current documented snapshot) for contemporaneous MU performance;
- the later-Calculus progressor subset (`N=4,211`) as a selected future-conditioned sensitivity/population, not a replacement estimand.
