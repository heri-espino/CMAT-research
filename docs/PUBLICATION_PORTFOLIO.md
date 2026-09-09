# CMAT publication portfolio

Canonical cross-paper planning document for the five-paper CMAT research programme.

Last journal-fit review: 2026-09-07. Journal targets are strategic rather than commitments; re-check aims, scope, data policies, and article types immediately before submission.

## Portfolio rule

All papers consume the same canonical scientific pipeline and aggregate outputs. Manuscripts must not maintain independent versions of cohorts, estimands, models, or numerical results. If a manuscript exposes a methodological problem, fix it in `code/`, regenerate canonical outputs, and only then update the manuscript.

Each paper has one canonical home under `papers/<paper_id>/`. This document summarizes cross-paper boundaries and priorities; detailed paper-specific scope lives in that paper's `README.md`, and paper-specific literature work lives in `papers/<paper_id>/literature/`.

## Paper 1 — incentive-linked support use and persistence

**Working title**  
*Beyond the Incentive Threshold: Academic Support Use and Persistence After a First-Year Participation Incentive*

**Priority**: highest / active.

**Core question**  
Does formal mathematics-support use observed during the incentive-linked first-year MU/PPA1 context persist into later Calculus use after that specific PPA1-linked incentive is treated as generally no longer applying?

**Primary outcome**  
Any later CMAT use during the first eligible later Calculus period.

**Main exposure**  
MU-period CMAT use, primarily `0 / 1–2 / exactly 3 / 4+`, with exact-count and course-specific sensitivities where useful.

**Core populations**
- broad linked MU→Calculus cohort with coverage (`N=4,211` in the current methodological snapshot);
- stricter next-regular-term PPA snapshot (`N=3,241`) once its logic is fully reintegrated into the canonical pipeline;
- delayed/alternative longitudinal sensitivity populations should remain explicitly labelled.

**Main contribution**  
Persistence of formal academic support-seeking across a change in incentive context, while separating persistent use from stable self-selection and avoiding causal claims that the observational data cannot identify.

**Current journal strategy**
1. **Studies in Higher Education** — ambitious primary target if the manuscript is framed as a general higher-education contribution about incentives, engagement, institutional support and persistence rather than a local mathematics-centre case.
2. **International Journal of Mathematical Education in Science and Technology (IJMEST)** — strong mathematics-education fallback.
3. **Teaching Mathematics and its Applications (TEAMAT)** — strong mathematics-support fallback.
4. **Journal of Further and Higher Education** — broader higher-education fallback.

**Interpretation boundaries**
- do not identify a causal PPA effect;
- do not call PPA a generic nudge without qualification;
- do not infer motivation or habit from visit counts;
- temporal precedence does not eliminate stable confounding.

## Paper 2 — CMAT use and classroom-relative MU performance

**Working title**  
*Mathematics Support Use and Classroom-Relative Academic Performance in First-Year University Mathematics*

**Priority**: high / active after the canonical methodology is frozen.

**Core question**  
How is contemporaneous CMAT use associated with classroom-relative academic performance in first-attempt MU?

**Primary outcome**  
`Z_MU`, standardized within `professor × subject × period` classrooms.

**Primary population**  
First observed eligible MU attempts with CMAT coverage (`N=6,627` in the current methodological snapshot). The `N=4,211` future-Calculus progressor cohort is a sensitivity, not a replacement estimand.

**Main exposure**  
Exact grouped use `0 / 1 / 2 / 3 / 4+`, plus exact count `0–12` and historical binary contrasts as sensitivities.

**Main contribution**  
A homogeneous-course analysis that distinguishes any-use versus non-use from dose/intensity among users, uses classroom-relative performance, robust heteroskedastic inference and multiplicity-adjusted pairwise comparisons.

**Current journal strategy**
1. **Teaching Mathematics and its Applications (TEAMAT)** — primary target.
2. **IJMEST** — second choice.
3. **International Journal of Research in Undergraduate Mathematics Education (IJRUME)** — ambitious option if the theoretical contribution to undergraduate mathematics education is sufficiently strong.

**Interpretation boundaries**
- observational association, not tutoring-treatment effect;
- current evidence mainly separates zero visits from positive use;
- no clean monotone dose-response among positive-use groups after multiplicity adjustment.

## Paper 3 — grading and instructor-by-term heterogeneity

**Working title**  
*When the Same Grade Does Not Mean the Same Performance: Instructor-by-Term Heterogeneity in Undergraduate Mathematics Assessment*

**Priority**: high, but requires a dedicated re-analysis before drafting.

**Core question**  
How much do grading distributions differ across instructors, courses and academic periods, and what do those differences imply for comparisons based on raw university grades?

**Core analytical objects**
- grade distributions by `professor × subject × period`;
- pass/adverse/administrative outcome composition;
- within-course and across-period variation;
- instructor-by-term dispersion and stability;
- consequences of raw-grade pooling versus classroom-relative standardization;
- sensitivity to classroom minimum size and handling of nonnumeric adverse outcomes.

**Main contribution**  
A measurement/assessment paper showing why identical raw grades can have different contextual meanings and documenting the empirical consequences of instructor-by-term heterogeneity in undergraduate mathematics.

**Current journal strategy**
1. **Assessment & Evaluation in Higher Education** — primary target because the paper is fundamentally about assessment comparability and grading practice in higher education.
2. **Studies in Educational Evaluation** — second choice.
3. **IJRUME** — ambitious mathematics-education route if the paper is framed around implications for undergraduate mathematics research and measurement.

**Status / requirements**
- do not draft from current descriptive plots alone;
- define a dedicated estimand and inferential plan first;
- quantify between-classroom and within-classroom variance formally;
- distinguish grading heterogeneity from differences in student composition;
- consider whether available data can support instructor/time variance components or only descriptive contextualization.

## Paper 4 — disciplinary heterogeneity in help-seeking

**Working title**  
*Who Keeps Seeking Mathematics Help? Disciplinary Heterogeneity in University Mathematics Support Use*

**Priority**: later, conditional on a stronger discipline-level design.

**Core question**  
How do mathematics-support use, persistence and possibly classroom-relative performance differ across official degree programmes?

**Candidate populations**
- broad observed mathematics-course attempts with CMAT coverage;
- first-MU cohort;
- linked later-Calculus risk set.

**Main analytical objects**
- degree-programme use rates;
- programme mean classroom-relative performance;
- programme differences in later support persistence;
- ecological versus individual-level relationships;
- sample-size thresholds and rare-programme handling;
- programme changes/revalidation audit where relevant.

**Main contribution**  
Disciplinary heterogeneity in formal academic help-seeking, with mathematics support treated as an institutional resource used differently across degree programmes rather than as a one-size-fits-all service.

**Current journal strategy**
1. **IJMEST** — primary mathematics-education target.
2. **Journal of Further and Higher Education** — broader higher-education alternative.
3. **Higher Education Research & Development (HERD)** — ambitious target only if the paper goes beyond a single-institution catalogue and makes a strong international higher-education contribution.

**Interpretation boundaries**
- career-level scatterplots are ecological and cannot establish individual-level relationships;
- official academic degree `CLAVECARRERA` is the primary programme variable;
- small programmes remain in the data even when excluded from programme-level inference.

## Paper 5 — full-degree longitudinal support trajectories

**Working title**  
*Longitudinal Trajectories of Mathematics Support Use Across the Undergraduate Degree*

**Priority**: future project.

**Core question**  
What recurring trajectories of mathematics-support use appear across students’ full undergraduate course sequences, beyond the MU→Calculus transition?

**Potential analytical direction**
- repeated course-level CMAT-use states across the degree;
- entry, persistence, re-entry and discontinuation of formal support use;
- sequence/trajectory clustering or state-transition models;
- relationship between trajectory types and academic progression;
- discipline-specific trajectory heterogeneity;
- explicit missingness/coverage and administrative-revalidation handling.

**Main contribution**  
Move from a two-time-point persistence design to a full longitudinal representation of formal mathematics-support engagement across the undergraduate degree.

**Current journal strategy**
- **TEAMAT or IJMEST** if the contribution remains primarily mathematics-support / mathematics-education substantive research;
- **Journal of Learning Analytics** if the final paper makes a genuine learning-analytics contribution using longitudinal educational traces, sequence/state modelling, and implications for learning environments;
- **International Journal of STEM Education** as an ambitious option if the trajectories are framed broadly around STEM progression and institutional support.

The target is intentionally not frozen because Paper 5 depends on the final data structure and analytical method.

## Current priority order

1. Paper 1 — PPA/incentive-context persistence.
2. Paper 2 — MU use and classroom-relative performance.
3. Paper 3 — grading/assessment heterogeneity after dedicated re-analysis.
4. Paper 4 — disciplinary heterogeneity after strengthening the programme-level design.
5. Paper 5 — future full-degree trajectory project.

## Literature architecture

The shared physical corpus lives in `literature/library/`. Cross-project literature lives in `literature/general/`. Manuscript-specific literature views live inside each paper:

- `papers/paper1_ppa_persistence/literature/`
- `papers/paper2_mu_performance/literature/`
- `papers/paper3_grading_heterogeneity/literature/`
- `papers/paper4_degree_help_seeking/literature/`
- `papers/paper5_longitudinal_trajectories/literature/`

A source may be indexed in several paper views without duplicating the underlying PDF/Markdown. Do not recreate a parallel `literature/papers/` hierarchy.

## Journal-fit sources reviewed

Official scope pages reviewed on 2026-09-07:

- Studies in Higher Education: https://www.tandfonline.com/journals/cshe20/about-this-journal
- TEAMAT: https://academic.oup.com/teamat/pages/Information_For_Authors
- IJMEST: https://www.tandfonline.com/journals/tmes20/about-this-journal
- Assessment & Evaluation in Higher Education: https://www.tandfonline.com/journals/caeh20/about-this-journal
- Journal of Further and Higher Education: https://www.tandfonline.com/journals/cjfh20/about-this-journal
- HERD: https://www.tandfonline.com/journals/cher20/about-this-journal
- Journal of Learning Analytics: https://learning-analytics.info/index.php/JLA/focusandscope

Before submission, verify current aims/scope, manuscript format, data-sharing policy and any fees directly from the journal website.
