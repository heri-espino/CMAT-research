# Paper 1 results

This directory contains generated or deliberately selected **publication-level aggregate outputs** for Paper 1. The canonical scientific recipe is `../code/run_paper.py`; reusable calculations remain in the shared `cmat_analysis` library, while `../code/figures.py` converts reviewed aggregate tables into paper-specific visual presentation.

The retained persistence bridge remains tables `101`–`107`, while the controlled instructor/familiarity extension is stored in tables `120`–`132`. No instructor identifiers, student identifiers, row-level joined cohorts or local input paths are retained in these publication outputs.

The instructor/familiarity tables are:

- `120_mu_professor_visit_group_distribution_summary.csv`: privacy-reviewed quantiles of instructor-specific shares in `0 / 1–2 / 3 / 4+`, restricted to instructors with at least 30 eligible MU students.
- `121_mu_professor_visit_group_multinomial_increment.csv`: joint four-group period/career model versus the same model plus MU instructor fixed effects.
- `122_mu_professor_any_use_increment.csv`: binary MU any-use instructor increment.
- `123_calc_professor_any_use_increment.csv`: binary Calculus any-use instructor increment.
- `124_familiarization_with_calc_professor_models.csv`: prior MU group contrasts for later use, culminating in a model with current Calculus instructor fixed effects.
- `125`–`127`: primary-cohort prior-familiarity × leave-period-out current-instructor uptake model and diagnostics.
- `128_professor_propensity_by_prior_familiarity.csv`: descriptive later-use rates by prior-use group and quartile of current-instructor leave-period-out uptake.
- `129`–`132`: all-subsequent-Calculus sensitivity versions of the familiarity and interaction models.

`results/run_summary.json` records the controlled cohort sizes and generated-output inventory. The current controlled rerun has an MU baseline of `N=4,906`, a strict next-regular-term persistence cohort of `N=3,241`, and an all-subsequent sensitivity cohort of `N=3,389`.

Tables `101`–`107` remain the primary reproducibility bridge to the retained longitudinal snapshot cited by the first manuscript draft. `python code/run_paper.py --compare-retained ...` checks them against `brainstorm/shared/historical_outputs/study/tables/` and fails rather than silently changing retained numbers.

The four manuscript figures remain generated artifacts rather than hand-edited source material. A direct `python paper/build.py` regenerates them from the retained aggregate snapshot, while `code/run_paper.py --compile` regenerates them from the aggregate tables produced by that empirical run.

Do not hand-edit numerical outputs. Administrative row-level data, student identifiers, raw joined cohorts and local input files must never be committed here. Aggregate CSVs or figures should only be committed after privacy and provenance review.
