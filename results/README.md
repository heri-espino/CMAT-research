# Paper 4 results

This directory contains generated or deliberately selected **publication-level aggregate outputs** for Paper 4. Reusable scientific calculations live in the shared `cmat_analysis` library; `../code/run_engagement.py` is a thin paper-specific recipe that composes those functions and writes only aggregate outputs.

The current controlled engagement/adaptation analysis is summarized in `engagement_run_summary.json`. The reviewed core tables are:

- `200_mu_attempt_outcome_summary.csv`: first-pass, second-pass, third-or-later-pass, and no-observed-pass groups, with aggregate CMAT and professor-history summaries.
- `203_calc_choice_association_models.csv`: associations between prior MU performance/context/CMAT history and the historical-outcome percentile of the chosen Calculus instructor.
- `204_calc_choice_performance_difficulty_interaction.csv`: continuous MU performance × classroom-context sensitivity for later Calculus instructor choice.
- `205_mu_repeat_attempt_summary.csv`: transitions after the first, second, and later failed MU attempts, including professor switching, CMAT change, next-attempt pass rate, and historical instructor-context shift.
- `207_career_adaptation_summary.csv`: degree-programme differences in first-MU outcomes, CMAT use, later Calculus support use, and chosen instructor historical-outcome context.
- `208_mu_experience_state_summary.csv`: five interpretable first-MU experience states—lower strain, contextual challenge, individual strain, compounded strain, and adverse/non-numeric—with subsequent support and progression outcomes.
- `209_calc_choice_by_mu_experience_state.csv`: adjusted differences in chosen Calculus instructor historical-outcome percentile across the five MU experience states.
- `210_post_failure_adaptation_strategy.csv`: descriptive next-attempt outcomes for combinations of movement toward historically higher-outcome professors and increased CMAT use after failure.

The recipe also generates detailed profile tables `201`–`202` and repeat-by-career table `206`; these are exploratory reproducibility outputs and need not be treated as primary manuscript tables until their role is justified.

The current controlled rerun contains 6,627 students whose first real MU attempt occurs during CMAT coverage, 4,151 students with a later observed Calculus attempt in CMAT coverage after an MU pass, 3,224 rankable Calculus instructor choices, and 1,007 covered transitions from a failed/adverse MU attempt to a subsequent MU attempt.

The historical instructor-choice variable uses only outcomes from academic periods strictly before the focal choice and ranks instructors within the professors observed teaching the course in that period. It is an observed academic-context measure, not a causal or intrinsic measure of professor difficulty/easiness. The observed instructor set also does not guarantee that every section was feasible for every student because schedules, capacity, and registration constraints are not fully observed.

Do not hand-edit numerical outputs. Administrative row-level data, student identifiers, instructor identifiers, row-level joined cohorts, or private local inputs must never be committed here. CMAT non-use must not be interpreted as disengagement, and descriptive post-failure adaptation patterns must not be interpreted as causal treatment effects.
