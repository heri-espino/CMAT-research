# Paper 2.2.1 — Scientific decision register

| Decision | Current choice | Rationale | Review status |
|---|---|---|---|
| Primary frequency grid | 0,1,2,3,4,5,6,7+ | Inherited Paper 2.1 reporting resolution; no new grouping inferred yet | Frozen for first experimental run |
| Historical support sensitivity | pooled 6+ | Preserve Paper 2.1 pre-outcome decision | Planned optional run |
| Model | squared-loss adjacent fused lasso, only visit coefficients penalised | Respect ordered categories while adjusting classroom and degree | Implemented, synthetic tests awaiting execution |
| Outcomes | Z_GRADE_PRIMARY and PASS as separate families | Continuous standardised grade and LPM probability measure different quantities | Implemented |
| Split | 70% discovery / 30% validation by instructor-period, seed 221 | Holdout untouched by discovery and tuning | Working protocol; support to verify |
| Penalty | nonnegative grid including 0 and complete fusion; 1-SE-type heuristic | Parsimony; CV standard error **not** formal inferential uncertainty | Implemented; subject to method audit |
| Bootstrap | whole discovery classrooms with lambda reselected | Boundary stability | Default runner 30; first smoke may use 0 |
| Validation | unpenalised selected-block OLS/LPM, CR Wald, Holm within outcome | Avoid naive same-sample post-selection p-values; report adjacent pair classroom overlap | Implemented; controlled run pending |
| CV interpretation | within-held-out-classroom MSE | Unseen classroom intercepts cannot be predicted | Implemented, generalisation scope limited |
| Results | only actual aggregate exports | Protect controlled microdata and avoid invented results | None yet |
| Article | separate `paper/paper221/main.tex` draft | Preserve Paper 2.1 manuscript | First draft, no empirical results |

If analysis exposes weak overlap, unseen degree levels, rank deficiency, solver instability, computation limits or changing result interpretation, create a dated notes entry before modifying the protocol. Report exploratory changes explicitly rather than retroactively claiming preregistration.
| Exhaustive benchmark | Enumerate 128 contiguous partitions by discovery-sample SSE and relative BIC | Test if the selected fused solution is plausible; not a null test | Implemented; controlled run pending |
