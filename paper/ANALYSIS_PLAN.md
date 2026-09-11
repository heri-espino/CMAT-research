# Paper 3 analysis plan

This document freezes the intended Paper 3 estimands before the dedicated controlled-data rerun. It does not change the shared scientific definitions in `cmat_analysis` and it does not promote exploratory `proyecto_visitas` results to confirmatory findings.

## 1. Target construct

Paper 3 studies the **contextual comparability of recorded undergraduate mathematics grades**. The primary empirical object is the distribution of numeric final grades awarded within an instructor × course × academic-period classroom. The paper does not identify a latent "true" mathematics score, nor does it interpret classroom differences as pure instructor severity, because student composition and assessment design can also contribute to the observed distributions.

## 2. Analytical records

The controlled academic file will be cleaned with the canonical attempt/administrative-status rules already maintained in `cmat_analysis`. Equivalencies, revalidations and other administrative non-attempt records must not be treated as newly awarded grades. Duplicate student-course records require the existing attempt/revalidation logic rather than arbitrary row deletion.

For the primary distribution analysis:

- retain observations with an awarded numeric final grade;
- define `PASS = 1` when grade ≥ 7.5 and `0` otherwise;
- retain `BV`, `RT` and `BA` in a parallel adverse-outcome table rather than assigning them a numeric value in the primary grading-distribution outcome;
- define classroom as instructor × course × academic period, pooling sections only when instructor, course and period are identical.

The primary minimum classroom size for distributional comparisons will be **20 numeric grades**, with sensitivity analyses at 10 and 30. This threshold is a stability rule for empirical distributions, not a claim that smaller classrooms are substantively unimportant.

## 3. Descriptive classroom heterogeneity

For each eligible classroom, report at least:

- number of numeric grades;
- mean and standard deviation;
- median and interquartile range;
- pass rate among numeric grades;
- adverse-outcome count/share using the parallel status table;
- course and academic period.

Distributions of these classroom-level summaries will be presented overall and, more importantly, within course × period strata so that differences between distinct courses or calendar periods do not masquerade as instructor-context heterogeneity.

## 4. Within-course-period distributional distances

For every course × period stratum containing at least two eligible classrooms, compare classroom empirical grade distributions pairwise. The historical analysis used the two-sample Kolmogorov–Smirnov distance; the confirmatory rerun will retain KS as a shape-sensitive summary and add the first Wasserstein distance as a scale-sensitive companion.

Primary summaries are the median, interquartile range and upper-tail quantiles of pairwise distance within course-period strata. The paper may display a clustered heat map for selected high-coverage strata, but unsupervised clusters will remain descriptive and will not be labelled as "strict" or "lenient" grading types.

## 5. Context variance decomposition

A multilevel/cross-classified model will quantify contextual variation while avoiding the claim that the classroom component is a causal instructor effect. The preferred model begins from numeric final grade and includes course × period fixed effects, with random intercepts for repeated students and for classroom or instructor context as supported by the observed nesting structure.

The exact random-effects parameterization must be chosen after inspecting overlap and identifiability in the controlled data. Report variance components and variance-partition quantities with uncertainty, but describe the classroom/instructor component as **context-associated variation**, because allocation of students to instructors is not randomized.

If the cross-classified model is unstable or poorly identified, the fallback is a course-period fixed-effect model with classroom-level residual summaries and cluster-robust uncertainty; do not force a multilevel model merely because it is planned here.

## 6. Temporal stability

For instructor-course combinations observed in at least three eligible academic periods, estimate the stability of classroom distribution summaries across periods. At minimum evaluate:

- correlation/stability of classroom mean grade;
- stability of within-classroom standard deviation;
- stability of pass rate;
- within-instructor-course range across periods;
- pairwise KS/Wasserstein distance across periods.

This analysis formalizes the historical visual observation that the same instructor can exhibit different grade distributions across periods. A stable instructor-specific component and a period-specific component should be distinguished whenever the data support that decomposition.

## 7. Consequence for grade-based comparison

For each eligible student-grade observation, define the classroom-relative score

`Z = (grade - classroom mean) / classroom SD`

using numeric grades in the primary specification. This score changes the estimand from absolute recorded grade to position within the local classroom distribution; it is not an estimate of latent proficiency.

Quantify the consequences of using raw versus contextualized outcomes through:

- Spearman association between raw grade and classroom-relative `Z`;
- movement in pooled percentile rank;
- decile/quintile reclassification rates;
- examples of observations for which a similar raw grade corresponds to materially different relative positions;
- sensitivity to classroom-size thresholds.

The paper should emphasize reclassification and rank movement rather than claiming that one scale is universally "correct".

## 8. Nonnumeric adverse outcomes

The historical `proyecto_visitas` report imputed adverse states into the lower grade range and showed that aggregate pass/fail composition is sensitive to that construction. Paper 3 therefore treats the following as separate analytical questions:

1. How heterogeneous are **awarded numeric grades** across classrooms?
2. How heterogeneous is the **composition of adverse nonnumeric outcomes** across classrooms?
3. If the project's preserved adverse-outcome imputation is applied as a sensitivity analysis, how much do conclusions about distributional heterogeneity change?

The imputed outcome must never be described as an observed instructor-assigned grade.

## 9. Historical cluster analysis

The exploratory report used professor-level KS distances and K-Medoids and found its maximum Silhouette Score at `k=3`. Paper 3 may mention this as evidence that the old analysis detected non-random-looking structure, but the final paper will rerun clustering only after conditioning on course/period comparability and minimum cell size. The number of clusters is not pre-specified as three.

## 10. Required sensitivity analyses

At minimum rerun key heterogeneity summaries under:

- minimum classroom numeric `N` = 10, 20 and 30;
- classroom = instructor × course × period versus section-retaining definitions when section identifiers permit;
- observed numeric grades only versus augmented adverse-outcome sensitivity;
- high-coverage core courses versus the broader mathematics-course population;
- periods before/after major coverage changes if diagnostics show discontinuities.

## 11. Claim boundary

Permitted claims concern observed grade-distribution heterogeneity, contextual comparability, temporal stability and the consequences of alternative measurement scales. The paper must not claim that:

- an instructor causes higher or lower student achievement;
- a distributional cluster identifies instructor quality;
- classroom `Z` is a universal mathematics proficiency score;
- standardization makes grades causally comparable;
- observed distribution differences are entirely due to grading severity.

## 12. Development gate before submission

Before numerical results are frozen, the Paper 3 runner must reproduce the controlled-data cohort, generate all publication tables/figures from the current shared library, record the exact library/repository commit, and reconcile any discrepancy with the retained historical report. Development notes in `paper/main.tex` should then be replaced by final estimates rather than silently removed.