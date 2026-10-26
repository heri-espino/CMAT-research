# PPA-threshold analysis status — 2026-10-26

**Implementation ready for review; institutional PPA estimates PENDING.**
The approved categorization is exclusively `0 | 1–3 | 4+`.
Historical exact-frequency support remains an independent comparator.
The earlier proposed `0 | 1–3 | 4 | 5+` grouping was withdrawn by
the user and is not part of the run contract.

The runner fits professor-period-FE and degree-adjusted `Z_GRADE_PRIMARY`
and `PASS`, applies Holm to **three pairs independently per outcome**,
reports descriptive and adjusted means, clustered nominal CIs, and
numeric-only sensitivities. The historical count reference shows
5,393 / 932 / 302 for the original cohort; there are no new adjusted
model result CSVs here yet.

Use `run_ppa_groups.py --check` and the paired synthetic test modules.
The executable's default is suitable for updated datasets: it reports
actual cohort size and visit frequencies in a source-fingerprinted manifest;
the optional `--require-historical-cohort` reproduces the frozen cohort
validation. Confirm tests against the exact merged SHA and execute
on the authorized institutional inputs before reporting empirical findings.

Do not infer eligibility, motives, PPA credits, causal returns to visits,
or effect-size significance from the historical count-only reference.
