# Paper 4 — longitudinal engagement-related adaptation in university mathematics

**Working title:** *From Assigned to Chosen Academic Contexts: Longitudinal Traces of Student Engagement and Adaptation in First-Year University Mathematics*

Canonical portfolio: `../../docs/PUBLICATION_PORTFOLIO.md`.

This directory is the **single canonical home** for Paper 4. Paper-specific manuscript material, literature notes, results and submission files belong here; shared source PDFs remain in `../../literature/library/`. Reusable cohort definitions, historical-instructor measures, choice-set rankings, repeated-attempt transitions and confirmatory robustness helpers live in `../../cmat_analysis/`; branch-local recipes only compose those shared functions into Paper 4 analyses.

## Conceptual framing

Paper 4 uses Kahu's student-engagement framework as a theoretical organizer without claiming that administrative records directly measure the full psychosocial state of engagement. Kahu separates sociocultural context, structural and psychosocial influences, engagement, and proximal/distal consequences, while defining engagement itself as multidimensional across affect, cognition and behaviour. Our administrative data observe only part of that system, most clearly institutional context, academic outcomes and behavioural traces.

The proposed contribution is therefore a **Kahu-aligned quantitative trace layer** for studying longitudinal academic adaptation. The paper distinguishes structural/disciplinary context, experienced academic performance, formal support response, later context-selection adaptation and longitudinal transitions. CMAT use is treated as a formal help-seeking/behavioural trace, not as engagement itself; instructor-context movement is treated as an observable adaptation trace, not as a measure of intrinsic professor ease or unconstrained student preference.

A temporal distinction is essential. First-MU experience states combine realized classroom-relative performance and realized leave-one-out classroom pass-rate context, so their association with CMAT use during the same MU period is **contemporaneous and descriptive**. By contrast, first-MU experience precedes later Calculus enrolment, and a failed MU attempt precedes the next MU attempt, so those transition analyses have explicit temporal ordering even though they remain observational.

## Institutional transition that motivates the design

The MU-to-Calculus transition contains a useful change in institutional choice structure:

- **MU:** students are assigned to sections/professors by the university, with grouping strongly connected to degree programme. Professor identity is therefore primarily an assigned structural context.
- **Calculus I:** students subsequently enrol with a professor from the sections offered in that period. Individual schedules, section capacity and registration restrictions are not observed, so the observed period-wide set of instructors is only a proxy for the feasible choice set.

For instructor-context analyses, an instructor is never labeled intrinsically “easy” or “hard.” Strictly-prior pass-rate and mean-grade histories use only academic periods before the focal enrolment, and within-period percentiles rank those historical outcomes among instructors observed teaching the course that period. Higher percentiles therefore mean historically higher observed academic outcomes, not causal teaching quality, grading leniency or a deliberate student choice of an “easier” professor.

## Research questions

1. Can first-MU experiences be summarized into interpretable quantitative states that preserve the distinction between individual performance and academic context?
2. How does formal support use differ across those experience states, and is that pattern robust to alternative definitions of academic strain?
3. Does prior MU experience predict the historical academic-outcome context of the instructor with whom the student subsequently enrols in Calculus I?
4. After a failed MU attempt, how do students adapt before the next attempt through professor switching, movement in historical instructor-outcome context and changes in CMAT use?
5. Do degree programmes contribute systematic heterogeneity in formal support use and context-selection traces, and does the response to academic strain vary across programmes?

## Core populations

The September 2026 controlled-data rerun contains:

- **6,627** students whose first real MU attempt falls in a CMAT-coverage period;
- **8,979** real MU attempt rows across their observed histories;
- **4,151** students with a first later Calculus attempt in a CMAT-coverage period after an observed MU pass;
- **3,224** later Calculus enrolments for which the chosen instructor can be ranked from strictly prior instructor outcomes;
- **1,007** transitions from a failed/adverse MU attempt to a subsequent MU attempt where both periods have CMAT coverage.

## Primary first-MU experience states

The confirmatory primary classification is recomputed **within the covered analytic cohort**, using classroom-relative performance `Z <= -0.5` as individual strain and the bottom quartile of leave-one-out classroom pass rate as high contextual difficulty. This supersedes the earlier exploratory state counts in table `208`, whose contextual cut was inherited from the broader trajectory builder before the CMAT-coverage restriction. Table `232` is therefore the canonical main-analysis state summary.

- **lower strain:** `N=3,679`; first-period CMAT use 18.8%, eventual MU pass 99.8%, observed later Calculus 77.5%, later Calculus CMAT use 23.6%;
- **contextual challenge:** `N=1,012`; first-period CMAT use 28.6%, eventual MU pass 97.7%, observed later Calculus 76.3%, later Calculus CMAT use 30.6%;
- **individual strain:** `N=673`; first-period CMAT use 9.5%, eventual MU pass 58.5%, observed later Calculus 42.2%, later Calculus CMAT use 13.7%;
- **compounded strain:** `N=162`; first-period CMAT use 8.0%, eventual MU pass 30.9%, observed later Calculus 16.0%, later Calculus CMAT use 15.4%;
- **adverse/non-numeric:** `N=1,101`; first-period CMAT use 16.2%, eventual MU pass 44.2%, observed later Calculus 19.7%, later Calculus CMAT use 15.2%.

The measurement audit (`233`) shows that 16.6% of covered first-MU students lack a classroom-relative `Z`, and every such case lacks a numeric grade; no numeric-grade student is silently classified as adverse/non-numeric because of a missing `Z`, and classroom pass-rate context is complete for the analytic cohort.

## Confirmatory design closure

### 1. Robustness of the academic-strain taxonomy

Tables `220`–`222` test nine pre-specified definitions formed by performance cutoffs `-0.25`, `-0.50`, `-0.75` crossed with contextual-difficulty quantiles `0.20`, `0.25`, `1/3`. Across **all nine specifications**, contextual-challenge students have the highest first-period CMAT-use rate among the four numeric states. Relative to lower strain, the contextual-challenge CMAT-use difference ranges from **+8.4 to +10.0 percentage points**; relative to individual strain, from **+15.7 to +20.1 points**; and relative to compounded strain, from **+14.5 to +21.8 points**.

The continuous model (`222`) gives the same qualitative pattern without thresholds. Conditional on degree programme and period, a +1 SD increase in classroom-relative performance is associated with +5.0 percentage points in same-period CMAT use (`p<1e-30`), while a +1 SD increase in classroom pass-rate context is associated with -4.7 points (`p<1e-7`); the interaction is -1.8 points (`p<1e-5`). Because performance, classroom outcomes and CMAT use are realized within the same period, these are contemporaneous associations rather than causal effects of academic difficulty on help-seeking.

### 2. Formalized post-failure adaptation

The repeated-attempt models (`223`, `231`) separate three subsequent responses: movement toward a historically higher-outcome instructor context, next-period CMAT use and increased CMAT use. Attempt number itself does not jointly explain these responses after controls, while prior CMAT use predicts later CMAT use in the full transition sample (+11.3 percentage points, `p=0.00035`) but does not predict an increase in visits.

The descriptive movement toward historically higher-outcome instructors is robust to how instructor context is measured (`224`). After the **first failed MU attempt**, 62.3% of rankable transitions move upward in the within-period historical-outcome percentile, 67.5% move to a professor with a higher strictly-prior pass rate and 66.9% move to one with a higher strictly-prior mean grade. The same direction persists after the second and third failures, although samples become small thereafter. The absolute-history checks are important because they show that the pattern is not created solely by a changing within-period percentile denominator.

Among numeric failures with a classroom-relative `Z` (`231`), failure severity does not show evidence that a more severe failure causes greater upward professor-context movement or more CMAT use: the coefficient of prior `Z` on upward professor-context movement is +5.3 percentage points per SD (`p=0.056`), while its associations with next-period CMAT use and increased CMAT use are small and non-significant. These models remain observational and should not be interpreted as causal effects of switching professors or using CMAT.

### 3. Degree-programme heterogeneity without twenty separate subanalyses

The confirmatory programme analysis uses omnibus tests (`225`) rather than one regression per degree. Degree programme adds explanatory information beyond experience state and period for first-MU CMAT use (`ΔR²=0.0154`, joint `p=3.6e-7`), later Calculus CMAT use (`ΔR²=0.0250`, `p=3.0e-12`) and the historical instructor-outcome rank observed in Calculus (`ΔR²=0.0143`, `p=5.8e-6`). These are statistically clear but modest incremental contributions.

The original unrestricted programme×experience-state interaction in `225` is retained only as a diagnostic because 116 interaction restrictions with 190 classroom clusters are too highly parameterized for the primary inferential claim. Table `230` is the canonical interaction sensitivity: after increasingly aggressive pre-specified pooling of smaller programmes, the interaction remains detectable at thresholds of 100, 150 and 200 students per retained programme, while incremental fit declines from `ΔR²=0.0112` to `0.0060`. The interpretation is therefore that disciplinary context modifies behavioural response patterns, but the additional explanatory magnitude is modest rather than dominant.

### 4. Audit of the instructor-choice proxy

The Calculus choice-set audit (`226`) shows 5–25 instructors observed teaching the course per period (median 13.5), with 2–18 instructors rankable from strictly-prior history (median 11.5). The chosen instructor is historically rankable for **77.7%** of the 4,151 later Calculus enrolments, and average history coverage is about 0.78 at the student level.

The administrative audit (`228`) finds no usable fields for an individual section identifier, schedule time, capacity or room, so the analysis cannot reconstruct each student's feasible instructor set. The correct language is therefore **“students subsequently enrolled with instructors associated with historically higher/lower observed academic outcomes”**, not “students deliberately chose easier/harder professors.”

Choice-set sensitivity (`227`) does not rescue the simple avoidance hypothesis. The individual-strain coefficient remains about **-4.4 percentile points** when requiring at least 2, 3, 4 or 5 rankable instructors (`p≈0.024`), and becomes -6.0 points (`p=0.005`) when additionally requiring at least 75% historical coverage. Under that stricter sample contextual challenge is also associated with a lower historical-outcome rank (-3.4 points, `p=0.019`). Thus the data do not support a general pattern in which a difficult MU experience is followed by enrolment with historically higher-outcome Calculus instructors.

For post-failure MU transitions (`229`), all observed next-attempt periods have at least four rankable instructors, but only 47.2% of first-failure transitions have comparable historical percentiles for both the prior and next professor because early-period historical coverage is incomplete. Absolute prior pass-rate and mean-grade comparisons in `224` therefore remain essential robustness checks.

## Interpretation rules

- Do **not** equate CMAT non-use with disengagement; students may use other resources or need no formal support.
- Do **not** interpret same-period MU state → CMAT comparisons causally; performance, classroom outcomes and visits are contemporaneous.
- Do **not** label a professor intrinsically easy/hard. Use “historically higher/lower observed academic outcomes,” “historical instructor-outcome percentile,” or “observed academic context.”
- Do **not** describe Calculus professor enrolment as unconstrained preference or deliberate selection; schedules, capacity and registration restrictions are not observed.
- Do **not** treat movement to a historically higher-outcome professor or increased CMAT use as a treatment whose effect is identified by the descriptive next-attempt pass rates.
- Keep structural context, academic outcomes/feedback, behavioural traces and subsequent outcomes conceptually distinct in the Kahu-aligned interpretation.
- Degree-programme heterogeneity should be presented through omnibus and pooled interaction tests, not through a catalogue of isolated programme-specific significance tests.

## Reproducibility boundary

The shared trajectory, instructor-history, confirmatory sensitivity, post-failure and choice-set audit methods are implemented and tested under `main/cmat_analysis/src/cmat_analysis/ppa/`. Paper 4 uses three thin recipes: `code/run_engagement.py`, `code/run_confirmatory.py` and `code/run_confirmatory_extra.py`; controlled execution is handled by `.github/workflows/paper4-ci.yml`.

Reviewed aggregate outputs retained under `results/tables/` include the original engagement/adaptation tables `200`–`210` and the confirmatory closure tables `220`–`233`. Tables `232`–`233` define and audit the canonical primary state classification; `220`–`222` cover taxonomy robustness; `223`–`224` and `231` formalize post-failure adaptation; `225` and `230` cover degree-programme heterogeneity; and `226`–`229` audit the instructor-choice proxy and its support.

## Status

**Empirical design closure candidate.** The four planned pre-draft analyses have been completed and versioned. The manuscript has not been modified. The next decision is whether these robustness results are sufficient to freeze the empirical design; if frozen, subsequent work should focus on literature integration, Kahu-to-administrative-trace mapping, presentation/figures and manuscript drafting rather than adding unconstrained exploratory specifications.
