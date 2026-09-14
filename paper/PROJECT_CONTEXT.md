# Paper 4 — longitudinal engagement-related adaptation in university mathematics

**Working title:** *From Assigned to Chosen Academic Contexts: Longitudinal Traces of Student Engagement and Adaptation in First-Year University Mathematics*

Canonical portfolio: `../../docs/PUBLICATION_PORTFOLIO.md`.

This directory is the **single canonical home** for Paper 4. Paper-specific manuscript material, literature notes, results and submission files belong here; shared source PDFs remain in `../../literature/library/`. Reusable cohort definitions, historical-instructor measures, choice-set rankings and transition helpers live in `../../cmat_analysis/`; the branch-local recipe only composes those shared functions into Paper 4 analyses.

## Conceptual framing

Paper 4 uses Kahu's student-engagement framework as a theoretical organizer without claiming that administrative records directly measure the full psychosocial state of engagement. Kahu separates sociocultural context, structural and psychosocial influences, engagement, and proximal/distal consequences, while defining engagement itself as multidimensional across affect, cognition and behaviour. Our administrative data observe only part of that system, most clearly institutional context, academic outcomes and behavioral traces.

The proposed contribution is therefore a **Kahu-aligned quantitative trace layer** for studying longitudinal academic adaptation. The paper distinguishes:

1. **Structural/disciplinary context:** official degree programme, institutional assignment to the first MU professor, and the realized classroom academic environment.
2. **Experienced academic performance:** classroom-relative performance, pass/non-pass outcomes and attempt number. These are treated as academic outcomes/feedback, not engagement itself.
3. **Formal support response:** contemporaneous CMAT use and its intensity (`0 / 1–2 / exactly 3 / 4+`). This is an observable behavioural trace related to engagement/help-seeking, not a complete measure of engagement.
4. **Context-selection adaptation:** after contexts become selectable, whether the student moves toward instructors with historically higher observed pass rates and mean grades. This is an observable adaptation/choice trace and not a measure of intrinsic professor ease.
5. **Longitudinal transition:** repeated MU attempts, later Calculus progression, subsequent CMAT use and next-attempt outcomes.

This structure preserves Kahu's central warning that antecedents, engagement and consequences should not be collapsed into one construct. It also exploits the framework's emphasis on engagement as situational, responsive to the environment and potentially bidirectional with academic outcomes. Degree-programme comparisons are interpreted as possible disciplinary cultures of engagement rather than fixed student traits.

Recent learning-analytics reviews strengthen this positioning because they show that higher-education engagement analytics overwhelmingly rely on observable behavioural traces and often provide limited contextual information. Paper 4 differs by explicitly separating context, academic outcomes, behavioral support use and later adaptation rather than labeling every administrative trace as engagement.

## Institutional transition that motivates the design

The MU-to-Calculus transition contains a useful change in institutional choice structure:

- **MU:** students are assigned to sections/professors by the university, with grouping strongly connected to degree programme. Professor identity is therefore primarily an assigned structural context.
- **Calculus I:** students choose their professor subject to the offered sections, schedules, capacity and other constraints that are not fully observed in the administrative data. Professor choice can therefore be studied as a later behavioral/context-selection trace, although not as unconstrained preference.

For instructor-choice analyses, an instructor is never labeled intrinsically “easy” or “hard.” The shared library calculates strictly-prior pass-rate and mean-grade histories using only academic periods before the student's choice, then ranks historically observed instructor outcomes within the professors observed teaching the course in that period. Higher percentiles mean historically higher observed pass rates/grades, not causal teaching quality or leniency.

## Research questions

1. Can first-MU experiences be summarized into interpretable quantitative states that preserve the distinction between individual performance and academic context?
2. How does formal support use differ across those experience states and across degree programmes?
3. Does an adverse or difficult MU experience predict selecting a Calculus instructor with historically higher academic outcomes once professor choice becomes available?
4. After a failed MU attempt, how do students adapt before the next attempt through professor switching, movement in historical instructor-outcome context and changes in CMAT use?
5. How do these adaptation traces differ across degree programmes, and are they consistent with disciplinary cultures of engagement?

## Primary quantitative states

The detailed exploratory grid retains performance band × realized classroom-difficulty band × CMAT group, but the main analysis avoids presenting dozens of sparse combinations. First-MU experience is reduced to five interpretable states before studying behavioral responses:

- **lower strain:** middle/high relative performance outside the most difficult classroom quartile;
- **contextual challenge:** middle/high relative performance in the bottom quartile of leave-one-out classroom pass rate;
- **individual strain:** low relative performance outside the most difficult classroom quartile;
- **compounded strain:** low relative performance in the most difficult classroom quartile;
- **adverse/non-numeric:** first MU attempt recorded as an adverse or otherwise nonnumeric outcome.

The state itself is not an engagement category. CMAT use, later instructor choice and repeated-attempt changes are analyzed as responses/adaptation traces conditional on that experience.

## Core populations and current controlled rerun

The September 2026 controlled-data rerun contains:

- **6,627** students whose first real MU attempt falls in a CMAT-coverage period;
- **8,979** real MU attempt rows across their observed histories;
- **4,151** students with a first later Calculus attempt in a CMAT-coverage period after an observed MU pass;
- **3,224** later Calculus choices for which the chosen instructor can be ranked from strictly prior instructor outcomes;
- **1,007** transitions from a failed/adverse MU attempt to a subsequent MU attempt where both periods have CMAT coverage.

## Current empirical findings

### First-MU experience states

The five states sharply separate subsequent academic trajectories and support responses.

- **Lower strain:** `N=3,653`; 0.9% first-attempt non-pass, 99.8% eventual MU pass, 18.8% first-period CMAT use, 77.7% observed later Calculus progression and 23.6% later Calculus CMAT use.
- **Contextual challenge:** `N=1,038`; despite being in the lowest classroom-pass-rate quartile, only 5.1% have a first-attempt non-pass and 97.8% eventually pass MU. This group has the highest first-period CMAT use among the main states (28.0%; mean 1.04 visits) and 30.5% later Calculus CMAT use.
- **Individual strain:** `N=665`; 55.3% first-attempt non-pass, 58.9% eventual MU pass, only 9.5% first-period CMAT use, 42.4% observed later Calculus and 13.8% later Calculus CMAT use.
- **Compounded strain:** `N=170`; 97.1% first-attempt non-pass, 30.6% eventual MU pass, 8.2% first-period CMAT use and only 16.5% observed later Calculus.
- **Adverse/non-numeric:** `N=1,101`; 44.2% eventually pass MU and 19.7% are observed later in Calculus.

The contrast is substantively important: the students experiencing the greatest academic strain are not necessarily the students using the most formal support. The contextual-challenge group combines strong relative performance under a difficult classroom context with the highest CMAT uptake, whereas individual/compounded strain show lower support use despite much weaker academic trajectories. This should be investigated as a help-seeking/engagement-related selection pattern rather than interpreted causally.

### Does a difficult MU experience lead students to choose an easier Calculus professor?

The simple avoidance hypothesis is **not supported** by the current Calculus-choice analysis. In `N=3,224` rankable choices, with Calculus-period and degree-programme controls plus CMAT-response and attempt-history controls, the experience-state comparison uses lower strain as the reference:

- contextual challenge: −1.78 percentile points in chosen historical instructor outcome rank (`p=0.205`);
- compounded strain: −2.60 points (`p=0.655`);
- adverse/non-numeric: −0.51 points (`p=0.901`);
- individual strain: **−4.55 points** (`p=0.021`).

The continuous specification gives the same broad conclusion: higher MU classroom-relative performance is associated with a small shift toward historically higher-outcome Calculus instructors (+1.34 percentile points per SD in the joint model, `p=0.028`), while realized MU classroom pass-rate context is not independently associated with the later choice (`p=0.161`) and the performance × classroom-context interaction is not evident (`p=0.681`). Therefore the data do not support the narrative that students who do poorly in assigned MU systematically compensate by choosing historically easier/higher-outcome Calculus professors.

### Failed MU attempts are a distinct adaptation point

The strongest context-selection response occurs **immediately after MU failure**, not at the later Calculus transition.

Among 820 covered transitions following the first failed/adverse MU attempt, 97.0% move to a different professor. For the 387 transitions where both the prior and next professors can be ranked from historical outcomes, 62.3% move toward a professor with historically higher outcomes, with a mean shift of **+13.4 percentile points**. The same directional tendency appears after the second failure (60.0% of 85 rankable transitions; +6.1 points) and third failure (63.6% of 22; +8.6 points), although later-attempt samples are small.

Next-attempt pass rates decline with repeated failure: 64.6% after the first failed attempt, 54.5% after the second and 40.0% after the third. This makes the `n`th-attempt population a substantively distinct high-risk group rather than a nuisance to be discarded.

Among rankable first-failure transitions, the descriptive adaptation-strategy table shows:

- moving to a historically higher-outcome professor without increasing CMAT: `N=225`, next-attempt pass rate 73.3%;
- neither observed change: `N=138`, next-attempt pass rate 58.0%;
- moving to a historically higher-outcome professor **and** increasing CMAT: `N=16`, next-attempt pass rate 87.5%.

These are descriptive associations, not treatment effects. Professor movement may reflect availability, scheduling, institutional rules, student composition, grading practices or other unobserved selection, and the small joint-strategy group should not be overinterpreted.

CMAT use does not increase after the first failure in aggregate: any-use falls from 18.9% in the failed attempt period to 9.8% in the next attempt period, with a mean change of −0.23 visits. This decline must be interpreted together with the PPA participation incentive and changing institutional context, not as direct evidence of disengagement.

### Degree-programme heterogeneity

Degree programmes show substantial differences in first-MU failure, CMAT use, later Calculus support use and selected historical instructor context. Actuaría (`LAT`) remains an informative example: among `N=368` first-MU students, 30.4% use CMAT in the first MU period and 40.8% of the `N=287` later-Calculus students use CMAT there, while its mean chosen Calculus historical-outcome percentile is near the middle of the observed choice set (0.532). Thus high formal-support use in Actuaría is not simply accompanied by systematic selection of historically high-outcome Calculus professors.

Programme differences should remain part of the paper because Kahu's framework explicitly permits disciplinary structural context and different cultures of engagement, but programme-level descriptive differences must not be treated as individual mechanisms without adjustment.

## Contribution

The emerging contribution is no longer a catalogue of degree-programme support rates. Paper 4 can show how administrative data can provide a **quantitative longitudinal complement** to a multidimensional engagement framework by observing the sequence:

`assigned context → academic experience/outcome → support response → context-selection adaptation → subsequent outcome`.

The contribution is strongest when framed as an operational layer for observable engagement-related adaptation rather than a claim to measure latent engagement. In particular, the assigned-MU/chosen-Calculus transition and repeated-MU-attempt transitions create natural moments where changes in student behaviour can be studied after academic feedback.

## Interpretation rules

- Do **not** equate CMAT non-use with disengagement; students may use other resources or need no formal support.
- Do **not** label a professor intrinsically easy/hard. Use “historically higher/lower observed academic outcomes,” “historical instructor-outcome percentile,” or “observed academic context.”
- Do **not** treat instructor choice as unconstrained preference; individual schedules, capacity and registration restrictions are not fully observed.
- Do **not** treat a change to a historically higher-outcome professor as causal treatment.
- Keep performance outcomes, contextual antecedents and behavioral traces conceptually distinct in the Kahu-aligned interpretation.
- The `n`th-attempt analyses include adverse/nonnumeric failures and require CMAT coverage in both transition periods when CMAT changes are interpreted.
- Official academic degree `CLAVECARRERA` remains the primary programme variable; small programmes remain in the data but should be pooled/excluded from programme-level inference as appropriate.

## Journal strategy

The target should be reconsidered after the engagement framing is fully developed. The paper now potentially fits a broader higher-education/engagement audience better than a mathematics-support-only outlet. Candidate targets include *Higher Education Research & Development* if the Kahu-aligned theoretical contribution is made explicit, *Studies in Higher Education* as an ambitious option, and *International Journal of Mathematical Education in Science and Technology* if the manuscript remains primarily mathematics-education focused.

## Reproducibility boundary

The shared trajectory and instructor-history methods are implemented and tested under `main/cmat_analysis/src/cmat_analysis/ppa/`. The Paper 4 recipe is `code/run_engagement.py` and its controlled CI is `.github/workflows/paper4-ci.yml`.

Reviewed aggregate outputs retained under `results/tables/` include the attempt-history summary (`200`), Calculus-choice models (`203`–`204`), repeat-attempt summary (`205`), degree-programme adaptation summary (`207`), five-state experience summary (`208`), state-to-Calculus-choice model (`209`) and post-failure adaptation strategies (`210`). Detailed profile tables (`201`–`202`) and the repeat-by-career table (`206`) are reproducibly generated by the recipe and available through the CI artifact even when not retained as primary reviewed tables.

## Status

Active Paper 4 design. The empirical signal is now strong enough to justify targeted literature work and manuscript development, but the next methodological priority is to formalize the Kahu-to-administrative-trace mapping, test robustness of the historical instructor-choice measure, and distinguish descriptive adaptation from causal interpretation.
