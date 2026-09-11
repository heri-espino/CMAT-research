# Paper 3 — grading comparability and instructor-by-term heterogeneity

**Working title:** *Are Course Grades Comparable Across Classrooms? Instructor-by-Term Heterogeneity in Undergraduate Mathematics Assessment*

Canonical portfolio: `../docs/PUBLICATION_PORTFOLIO.md` from the repository root.

This branch is the single canonical publication workspace for Paper 3. Shared scientific code remains in `cmat_analysis/`; the historical `proyecto_visitas` workspace remains on branch `brainstorm/proyecto-visitas` and is treated as provenance rather than as a frozen publication analysis.

## Research problem

University course grades are routinely pooled across instructors, sections and academic periods as though the same numerical scale were automatically commensurable. Paper 3 studies whether that exchangeability assumption is empirically defensible in undergraduate mathematics, where a nominally common 0–10 grade scale is produced within local instructor, course and period assessment contexts.

The paper does **not** ask which instructors are "hard" or "easy" graders, because observed grade distributions jointly reflect assessment practice, assessment design, student composition and realized student performance. Its measurement question is narrower and more defensible: how much contextual variation remains after comparisons are restricted to nominally similar academic settings, how stable are instructor-course grade distributions across periods, and what changes when educational analyses use raw grades rather than classroom-relative outcomes?

## Primary research questions

1. How much do classroom grade distributions vary within the same course and academic period?
2. How stable are the location, spread and shape of an instructor-course grade distribution across periods?
3. How much student ranking or classification changes when raw grades are replaced by classroom-relative standardization?
4. How sensitive are conclusions about grade comparability to classroom-size restrictions and to the treatment of nonnumeric adverse outcomes?

## Classroom definition

A classroom is `instructor × course × academic period`, independent of section when the same instructor teaches the same course in the same period. The period remains part of the definition because the historical analysis already showed that the same instructor's grade distribution can shift across time.

## Outcome boundary

The primary grading-distribution analysis uses **observed numeric awarded grades**. `BV`, `RT` and `BA` are substantively adverse academic outcomes, but they are not numeric grades assigned by an instructor; therefore Paper 3 describes their classroom composition separately and uses the project's adverse-outcome imputation only as a sensitivity analysis. This differs deliberately from Paper 2, where an augmented academic-performance outcome retains adverse states in the primary construction.

Passing remains 7.5 whenever pass/fail summaries are reported.

## Planned analytical layers

- classroom summaries of location, dispersion, pass rate and adverse-outcome composition;
- within-course-period variation across classrooms;
- pairwise distribution distances within comparable course-period strata;
- descriptive variance decomposition with course-period context and repeated-student structure where supported by the controlled data;
- instructor-course temporal stability across repeated periods;
- raw-grade versus classroom-relative ranking/reclassification diagnostics;
- sensitivity to minimum classroom size and adverse-outcome construction.

Classroom-standardized `Z` is a contextual relative-position measure, not a universal measure of latent mathematical proficiency and not a claim that grading differences are error.

## Historical evidence available before the dedicated rerun

The retained `proyecto_visitas` report documents 26,140 student-classroom observations, 77 instructors and 769 classrooms over 2019–2025, with a median classroom size of 30. It also documents substantial visual differences in professor grade distributions, an exploratory KS-distance/K-Medoids solution whose maximum Silhouette Score occurred at `k=3`, and visible period-to-period changes for the same instructor. These quantities are development evidence only; Paper 3 will not present the historical clustering as a confirmatory taxonomy.

The historical report also records 3,217 nonnumeric final-grade observations (12.3%). Its aggregate passing share changes from 90.57% among observed numeric grades to 79.67% after the historical adverse-outcome imputation, which is precisely why the final paper must separate the construct "awarded numeric grade distribution" from the broader construct "academic outcome" rather than mixing them silently.

## Journal strategy

1. *Assessment & Evaluation in Higher Education* — primary target.
2. *Studies in Educational Evaluation* — second choice.
3. *International Journal of Research in Undergraduate Mathematics Education* — ambitious mathematics-education route.

## Current status

A formal first manuscript draft is now being developed from the historical evidence and a pre-specified reanalysis plan. Numerical claims that depend on the historical broad report are labelled as exploratory/provisional until the controlled institutional inputs are rerun under the Paper 3 specification.

## Scientific boundary with Paper 2

Paper 2 owns the student-level association between contemporaneous CMAT use and performance. Paper 3 owns the measurement problem created by heterogeneous grading contexts. CMAT attendance is therefore not an explanatory variable in Paper 3, except where Paper 2 is mentioned to illustrate why classroom-relative outcomes became necessary in the wider project.