# CMAT publication-oriented study outputs

Primary outcome: continuous standardized performance (`Z_GRADE_PRIMARY`).  
Secondary outcome: pass/adverse academic result (`PASS`).  
Primary exposure: **all CMAT visits during the same academic term** as the student's first attempt at Matemáticas Universitarias.  
Confirmed PPA rule: the point is reached at **≥3 visits**; `4+` is interpreted only as **use beyond the incentive threshold**, not as intrinsic motivation.

## Current cohort
- First standard attempt at Matemáticas Universitarias, all periods: 7,777
- Primary cohort with advisory-record coverage: 6,627
- Students in primary cohort with >3 course-period visits: 302
- Longitudinal MU→Cálculo pairs with visit coverage in Cálculo: 4,211

## Temporal attendance findings
- Calendar day of every advisory is preserved for analysis; exact clock time is used internally only to order repeated same-day visits.
- PPA achievers (≥3 visits): 472.
- PPA achievers with ≥3 visits on at least one single day: 24 (5.08%).
- PPA achievers whose first 3 visits all occurred on one calendar day: 7 (1.48%).
- Detected CMAT service-load peaks are separated by a median of 30.5 days (IQR 28.0–33.8); 73.7% of detected inter-peak gaps fall between 24 and 38 days. This is compatible with a roughly monthly academic cycle, but peaks must not be labeled as exams without professor-level exam calendars.
- ACF/periodogram diagnostics are exported as independent descriptive checks of the approximately monthly cycle.

## RQ2b — temporal regularity and performance
- Primary temporal-spread metric: `REGULARITY_MONTHLY_4 = min(active calendar months, 4) / min(total visits, 4)`.
- Primary RQ2b population: students with ≥3 visits and a numeric final grade, to avoid mechanically shortening the opportunity window for withdrawal cases.
- The model adjusts flexibly for visit intensity (3, 4, 5, 6, 7, 8+), professor×period fixed effects and career; it remains observational.
- Effective-number-of-weeks and adverse-outcome-imputed specifications are sensitivity analyses.

## Interpretation guardrails
1. The study is observational. Fixed effects and propensity weighting address observed structure, not unmeasured motivation/need.
2. The current academic file has no exact withdrawal date, so visits are linked by year/session rather than truncated on a student's withdrawal date.
3. `BV`, `RT`, and `BA` are treated as adverse academic outcomes below 7.5. `EQV`, `REV`, and `AC` are confirmed external/equivalent passing records and are excluded because the relevant instructor/classroom is not observed.
4. Every advisory row is one confirmed visit.
5. Cálculo I is a descriptive/no-PPA comparator and a longitudinal follow-up; it is not treated as a causal control for the PPA policy.

See `STUDY_PROTOCOL.md` and `ADMINISTRATIVE_QUESTIONS.md` at the project root before publication use.
