# Paper 1 — incentive-linked support use and persistence

**Working title:** *Beyond the Incentive Threshold: Academic Support Use and Persistence After a First-Year Participation Incentive*

Canonical portfolio: `../../docs/PUBLICATION_PORTFOLIO.md`.

This branch is the canonical publication workspace for Paper 1. Reusable cohort definitions and estimators live in `cmat_analysis`; paper-local code is a thin recipe that imports the shared library and writes only aggregate publication outputs.

## Current empirical framing

Paper 1 studies whether formal mathematics-support use persists across contexts and whether several observational channels are associated with CMAT uptake: prior familiarity/use history, instructor-linked support context, observed classroom outcome context, historical instructor academic context, and degree programme. MU-period registrations are classified as `0 / 1–2 / exactly 3 / 4+`; exactly three remains institutionally salient because it corresponds to the historical PPA participation threshold, while `4+` distinguishes use beyond that threshold.

Instructors routinely recommend CMAT as a tutoring resource, but the administrative data do not observe recommendation intensity. The empirical professor variables therefore measure instructor-linked uptake/implementation rather than a randomized recommendation treatment. Likewise, classroom mean grade and pass rate are treated as observed academic-outcome context rather than literal causal measures of professor difficulty, because they also reflect student composition and potentially students' use of support.

None of these channels is randomized. Prior use can reflect stable help-seeking propensity, perceived difficulty, motivation and other student selection, while instructor assignment, degree programme, grading outcomes and instructor-linked uptake can reflect student composition, scheduling, pedagogy and other instructor-associated factors. The analysis estimates persistence and contextual associations, not causal encouragement effects.

## Research questions

The current controlled-data analysis asks:

1. How strongly does the distribution of initial MU-period CMAT use (`0 / 1–2 / 3 / 4+`) vary across instructors after accounting for academic period and degree programme?
2. Does prior MU-period use predict any CMAT use in the subsequent eligible Calculus period after controlling for prior MU performance, degree programme, academic period and the current Calculus instructor?
3. Is later CMAT use also associated with the current instructor's historical uptake context, estimated from the same instructor's students in other academic periods?
4. Do prior familiarity and instructor-linked uptake appear to substitute for or complement one another descriptively?
5. Is initial CMAT use associated with the observed mean grade and pass rate of the student's MU classroom, using leave-one-out classroom measures so the focal student's own outcome does not mechanically determine the predictor?
6. Do instructors whose students historically have lower mean grades or pass rates also have higher historical CMAT uptake, and how much additional heterogeneity is associated with the student's degree programme after professor and period are controlled?

## Outcomes and exposures

The primary later outcome is any CMAT use during the strict next-regular-term eligible Calculus I period. The primary familiarity exposure is MU-period visit group: `0 / 1–2 / exactly 3 / 4+`.

For instructor-linked implementation, the primary descriptive measures are instructor fixed effects and a leave-period-out instructor uptake rate. The latter excludes the focal academic period, requires at least 30 students from other periods, and is standardized across the included student sample.

For academic context, classroom mean grade and pass/fail rates are reconstructed from all real MU attempt candidates, including adverse nonnumeric outcomes in the pass-rate denominator. Student-level models use leave-one-out classroom mean and pass rate. Historical instructor academic context uses the same instructor's outcomes in all other academic periods, thereby excluding the focal period while remaining potentially confounded by historical student composition.

## Core populations

The current controlled rerun uses three related populations:

- **Initial MU uptake baseline:** `N=4,906`, 53 MU instructors. This cohort is constructed before conditioning on later Calculus progression, so the instructor-to-initial-uptake and degree-programme analyses do not select only students who later progress.
- **Primary persistence cohort:** `N=3,241`, 48 Calculus instructors, linking MU to the subsequent eligible next-regular-term Calculus attempt.
- **All-subsequent sensitivity cohort:** `N=3,389`, retaining later eligible Calculus attempts beyond the strict next-regular-term definition.

The classroom-context reconstruction contains 227 MU professor-period classrooms and is built from all real attempt candidates rather than only the passing students retained in the Paper 1 uptake baseline. The historical `N=4,211` broad progressor snapshot remains provenance rather than the canonical current controlled rerun and should not be mixed with the current estimates.

## Controlled-data results added in September 2026

Instructor identity is strongly associated with the complete initial MU visit-group distribution. In the `N=4,906` baseline, adding 53 instructor fixed effects to period and degree-programme controls raises McFadden's pseudo-R² from 0.0617 to 0.1237; the joint multinomial likelihood-ratio test is approximately `LR=427.15`, `df=156`, `p=4.49e-27`. For the simpler outcome of any MU-period use, adding instructor fixed effects raises R² from 0.0649 to 0.1216 (`partial R²=0.0606`, joint `p=4.31e-37`).

The instructor distribution is substantively heterogeneous. Among the 42 MU instructors with at least 30 eligible students, the median share in the zero-use group is 80.4%, while the 10th and 90th percentiles are 65.3% and 89.5%. For exact-three use, the corresponding shares are 0.6%, 2.5% and 6.1%; for `4+`, they are 1.0%, 4.4% and 9.4%.

Degree programme is independently associated with initial uptake, although its incremental explanatory contribution is smaller than that of instructor identity. After period and professor fixed effects, adding 28 degree-programme categories raises R² from 0.1086 to 0.1216 (`delta R²=0.0131`, `partial R²=0.0147`, joint `p=7.02e-6`). In the four-group multinomial model, adding degree programme raises McFadden's pseudo-R² from 0.1065 to 0.1237 (`LR=118.70`, `df=81`, `p=0.0041`). Among programmes with at least 30 students, Actuaría (`LAT`) has the highest baseline any-use rate at 33.8% (`N=290`), with 20.3% in `1–2`, 5.5% in exactly `3`, and 7.9% in `4+`; the lowest retained any-use rate is 8.9% for `LAR`.

Observed classroom outcomes are related to CMAT uptake in the direction consistent with greater perceived academic difficulty. Across 227 MU classrooms, the median pass rate is 75.0% and the median numeric mean grade is 8.26. After academic-period and degree-programme adjustment, a one-standard-deviation higher leave-one-out classroom mean grade is associated with 3.49 percentage points less CMAT use (`p=3.15e-8`), while a one-standard-deviation higher leave-one-out pass rate is associated with 6.00 points less use (`p=4.37e-20`). After adding professor fixed effects, the mean-grade association shrinks to -1.15 points and is not statistically distinguishable from zero (`p=0.179`), whereas the pass-rate association remains -3.46 points (`p=8.87e-5`). This pattern suggests that much of the mean-grade relationship is between professors, while variation in classroom pass rates remains associated with uptake even within professor identity.

Historical professor context shows the same between-professor pattern. Net of period and degree programme, a one-standard-deviation higher leave-period-out historical mean grade is associated with 4.96 percentage points less initial CMAT use (`p=2.17e-16`), and a one-standard-deviation higher historical pass rate is associated with 4.07 points less use (`p=1.59e-11`). Across 168 professor-period cells with sufficient historical support, the professor's leave-period-out CMAT uptake rate correlates negatively with historical mean grade (`Pearson r=-0.464`, `Spearman rho=-0.476`) and historical pass rate (`Pearson r=-0.557`, `Spearman rho=-0.553`), all with very small p-values. These correlations are compatible with students using CMAT more in historically lower-performing or more demanding instructor contexts, but they do not establish causal professor severity because historical student composition may generate part of the same pattern.

Current Calculus instructor context is also associated with later CMAT use. In the primary persistence cohort, adding Calculus instructor fixed effects to period and degree-programme controls raises R² from 0.0674 to 0.1211 (`partial R²=0.0575`, joint `p=7.38e-19`).

Prior use remains strongly associated with later use after controlling for the current Calculus instructor. Relative to students with zero MU-period visits, the fully adjusted risk differences are +23.7 percentage points for `1–2`, +32.5 points for exactly `3`, and +47.8 points for `4+`; the joint prior-group test has `p=4.69e-113`. The all-subsequent sensitivity gives similar estimates of +22.9, +31.9 and +46.8 points.

The joint descriptive model uses the current Calculus instructor's leave-period-out uptake propensity and is estimated on 2,447 primary-cohort students across 30 instructors. A one-standard-deviation higher instructor propensity is associated with +3.34 percentage points of later use among students with no prior MU use, compared with +8.85 points after `1–2` MU visits, +9.93 after exactly `3`, and +9.52 after `4+`; the interaction terms are jointly significant (`p=7.68e-6`). The all-subsequent sensitivity shows the same pattern. This is consistent with complementarity between prior familiarity and an instructor-linked support context, but it must not be interpreted as a causal interaction because both components are observational.

## Contribution

The current contribution is broader than a threshold-only persistence comparison: formal help-seeking is strongly patterned by prior exposure, instructional context, degree programme and the academic-outcome environment, while prior CMAT use continues to predict later use within the same current-instructor context. The new classroom and historical-professor results provide a plausible demand-side pathway—students use support more in lower-performing academic contexts—while the independent programme and instructor associations show that neither disciplinary composition nor observed grading outcomes alone account for CMAT uptake heterogeneity.

## Interpretation rule

This remains an observational study. The analysis does **not** identify a causal PPA effect, a causal professor recommendation effect, a causal professor-difficulty effect, a tutoring treatment effect, motivation, or habit formation. Instructor identity, degree programme, classroom outcomes and historical instructor uptake are not valid instruments by themselves. In particular, lower professor-level mean grades or pass rates should be described as lower historical academic outcomes or greater observed grading severity/context, not as proof that an instructor is intrinsically more difficult.

## Reproducibility boundary

Reusable scientific functions are implemented, tested and documented under `main/cmat_analysis/src/cmat_analysis/ppa/`. Paper 1 imports those functions through thin recipes under `code/`; it does not maintain divergent estimators. Aggregate tables `120`–`132` contain the reviewed controlled-data instructor/familiarity extension, while tables `140`–`146` contain the reviewed degree-programme and academic-context extension. Cross-paper interpretation is documented in `brainstorm/shared/INSTRUCTOR_FAMILIARITY_HANDOFF.md`.
