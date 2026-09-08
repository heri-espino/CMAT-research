# Agnew, Kerr & Watt (2021) — *The Effect on Student Behaviour and Achievement of Removing Incentives to Complete Online Formative Assessments*

## Citation

Agnew, S., Kerr, J., & Watt, R. (2021). The effect on student behaviour and achievement of removing incentives to complete online formative assessments. *Australasian Journal of Educational Technology, 37*(4), 173–185. https://doi.org/10.14742/ajet.6203

## 60-second summary

This is the closest current source in the Paper 1 library to the idea of **observing behaviour after an incentive is removed**. In a first-year economics course, weekly quizzes were worth 1% each during Term 1; that incentive was removed in Term 2. Quiz completion collapsed, and students who continued participating also showed lower-intensity engagement. The paper then uses OLS and a historical-cohort comparison to examine achievement.

The study is highly relevant conceptually to PPA because it explicitly compares behaviour under an incentive with behaviour after removal. Its design, however, is not a randomized removal experiment, so causal language should remain cautious.

## Role in Paper 1

- **Priority:** core empirical comparator for incentive removal.
- **Used in:** literature review, rationale for later-use outcome, Discussion.
- **Main job:** show that removing a small participation incentive can strongly change behaviour and engagement quality.
- **CMAT connection:** supports treating post-incentive persistence as an empirical outcome rather than assuming behaviour continues unchanged.

## Design and sample

- **Setting:** first-year introductory economics course at a New Zealand university.
- **Course cohort:** `337` students reported at study design stage; the article later notes `331` students in the course when describing the ethical grade allocation.
- **Term 1:** five weekly quizzes, each worth `1%` of course grade; up to two attempts.
- **Term 2:** quiz incentive removed.
- **Behavioural outcomes:** quiz count, start timing, duration, number of attempts, mean quiz score.
- **Achievement outcomes:** term-test and final-exam percentage.
- **Methods:** within-course behavioural comparison, OLS regressions, historical-cohort difference-in-differences-style comparison using the same/similar assessments.

## Key results

### Behaviour after incentive removal

| Outcome | Term 1 | Term 2 |
|---|---:|---:|
| completed all 5 quizzes | `55%` | `6%` |
| completed 0 quizzes | `1%` | `51%` |
| average start day (Wed=1, Thu=2, Fri=3) | `2.24` | `2.33` |
| average duration | `14.95` | `11.63` |
| average attempts | `1.65` | `1.50` |

The paper summarizes the participation change as a fall from `99%` attempting at least one quiz under incentives to `49%` after removal.

### OLS models

For the term-test model:

- Term 1 quiz count: `B = 1.606`, `SE = 0.799`, marked `p < .05`.
- Term 1 average quiz duration: `B = -0.268`, `SE = 0.106`, `p < .05`.
- Final-exam percentage: `B = 0.691`, `SE = 0.041`, `p < .01`.
- Adjusted `R² = .595`.

For the final-exam model:

- Term 2 quiz count: `B = -0.740`, `SE = 0.704`, not significant.
- Term 1 average day quiz commenced: `B = -5.064`, `SE = 1.564`, `p < .01`.
- Term-test percentage: `B = 0.757`, `SE = 0.045`, `p < .01`.
- Adjusted `R² = .593`.

The important null for Paper 1 is that **none of the Term 2 quiz-behaviour variables significantly predicted final-exam percentage** in this model.

### Historical-cohort comparison

| Cohort | Term-test mean | Exam mean |
|---|---:|---:|
| historical/control year | `52%` | `52%` |
| 2018 removal year | `57%` | `50%` |

The paper reports a `7` percentage-point decline from term-test to exam mean in the removal cohort versus no mean decline in the historical cohort. Quartile-specific comparisons of the change in means are reported as `p < .001` for all four quartiles.

## What this paper lets us say

- Small grade incentives can strongly affect completion of optional/low-stakes academic activities.
- Behaviour after removal can differ sharply from behaviour while incentives are active.
- Binary participation alone may miss changes in engagement intensity/quality.
- Post-removal academic effects are harder to identify cleanly than the immediate behavioural change.

## What it does **not** let us say

- Removing PPA caused any later CMAT pattern.
- The historical control year fully eliminates cohort/instructor/content differences.
- Continued quiz completion without incentives measures intrinsic motivation.
- More quiz attempts after removal causally improve examination performance; the Term 2 OLS coefficients were null.

## Local verification

Markdown: `literature/library/articles/agnew_2021_removing-incentives-online-formative-assessments.md`

PDF: `literature/library/pdf/agnew_2021_removing-incentives-online-formative-assessments.pdf`

Key anchors: pp. 6–10; Tables 1–5.