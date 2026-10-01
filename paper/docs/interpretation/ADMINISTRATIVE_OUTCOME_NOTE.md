# Paper 2.1 — administrative-outcome attendance note

This is an internal interpretation note for the PASS/non-PASS analysis. It is not intended to become a standalone manuscript subsection.

## Canonical descriptive evidence

Using the canonical Paper 2 controlled-data run at commit `c1034a6d06911b23a8a4c2fa424914a28130a866`, table `49_withdrawal_share_by_visit_group.csv` contained **1,101** BA/BV/RT outcomes.

Of those 1,101 administrative withdrawals:

- 923 had 0 recorded CMAT visits (83.8%);
- 83 had 1 visit (7.5%);
- 36 had 2 visits (3.3%);
- 26 had 3 visits (2.4%);
- 33 had 4 or more visits (3.0%).

The corresponding withdrawal shares within the attendance groups were:

- 0 visits: 17.1%;
- 1 visit: 16.1%;
- 2 visits: 14.7%;
- 3 visits: 15.3%;
- 4+ visits: 10.9%.

## Interpretation

The fact that most BA/BV/RT cases are in the zero-visit group is **not by itself a strong finding**, because 81.4% of the entire Paper 2 cohort also had zero recorded visits. The concentration of administrative withdrawals at zero visits is therefore only modestly greater than the cohort's overall concentration at zero.

It may still be useful as a short descriptive observation, especially when explaining why PASS/non-PASS and the continuous imputed outcome are analysed in parallel. It should not be turned into a narrative that students withdrew because they did not attend CMAT, nor that they would otherwise have attended or passed.

## Recommended manuscript treatment

Keep the timing point to one sentence when defining the non-passing outcome, for example in substance:

> Administrative withdrawals may occur before the end of the academic period and therefore can provide less opportunity to accumulate CMAT visits.

If the descriptive distribution is mentioned, keep it similarly compact and contextualize it against the overall zero-visit prevalence. Do not state simply that “most withdrawals never attended” without that denominator, because the same is true of most students in the study sample.

## Future Paper 2.1 diagnostic

When the Paper 2.1 dual-outcome runner is implemented, regenerate this diagnostic under the frozen `1/2/3/4/5/6+` grouping and, if useful, separately by BA/BV/RT. Treat it as descriptive only.
