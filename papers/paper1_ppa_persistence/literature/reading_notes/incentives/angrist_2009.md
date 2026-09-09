# Angrist, Lang & Oreopoulos (2009) — *Incentives and Services for College Achievement: Evidence from a Randomized Trial*

## Citation

Angrist, J., Lang, D., & Oreopoulos, P. (2009). Incentives and services for college achievement: Evidence from a randomized trial. *American Economic Journal: Applied Economics, 1*(1), 136–163. https://doi.org/10.1257/app.1.1.136

## 60-second summary

Project STAR randomly assigned first-year university students to academic services, financial incentives, both, or control. The combined intervention increased academic-service take-up and improved several academic outcomes for women, while effects for men were essentially null. Importantly for Paper 1, some female achievement differences persisted into second year even though the intervention was offered only in first year.

This is a strong comparator because it experimentally separates **offer of treatment** from actual service use and explicitly studies persistence after the intervention period. It also demonstrates substantial heterogeneity by gender.

## Role in Paper 1

- **Priority:** core randomized higher-education comparator.
- **Used in:** literature review, identification discussion, Discussion.
- **Main job:** show that an incentive can increase use of academic services and that some later academic differences can persist after the intervention ends.
- **CMAT connection:** particularly relevant to the question of whether support use/academic differences continue when the initial incentive context is gone.

## Design and sample

- **Setting:** first-year students at a satellite campus of a large Canadian university.
- **Eligibility:** first-year entrants except the top quartile of high-school GPA.
- **Randomized arms:**
  - SSP: academic support services (`n=250` offered);
  - SFP: financial reward for meeting GPA targets (`n=250` offered);
  - SFSP: services + incentives (`n=150` offered);
  - control (`n=1,006`).
- **Incentive magnitude:** up to `$5,000` CAD for meeting GPA targets, with lower `$1,000` targets and some intermediate awards.
- **Methods:** intention-to-treat regressions with robust SE; later 2SLS/IV adjustment using randomized offer as instrument for participation.

## Key results

### Incentives increased support-service use

From Table 3, full-control specifications:

| Offer | Received SSP services | Contacted advisor | Attended FSG |
|---|---:|---:|---:|
| SSP | `.255` (`SE=.029`)*** | `.217` (`.028`)*** | `.118` (`.021`)*** |
| SFSP | `.431` (`.044`)*** | `.397` (`.043`)*** | `.139` (`.031`)*** |

For women, service use was especially high in the combined arm:

- SSP services: `.287` (`SE=.040`) under SSP versus `.532` (`.058`) under SFSP.
- advisor contact: `.264` (`.040`) versus `.489` (`.058`).

This is direct experimental evidence that adding a fellowship opportunity increased take-up of academic support.

### First-year academic outcomes

From Table 5:

- **SFSP, all students, fall grade:** `+2.702` points, `SE=1.124`, `p<.05`.
- **SFSP, women, fall grade:** `+4.205` points, `SE=1.325`, `p<.01`.
- **SFSP, all students, first-year GPA:** `+0.210`, `SE=.092`, `p<.05`.
- **SFSP, women, first-year GPA:** `+0.267`, `SE=.117`, `p<.05`.
- Male academic effects were not statistically significant in the corresponding estimates.

The paper reports continued female outperformance in second year even though fellowships/services were offered only in first year; stacked first-/second-year models also produced a significant SFSP effect for women with smaller SEs.

## Identification detail worth remembering

The authors emphasize intention-to-treat effects because randomization assigns the **offer**, not actual participation. They then use the offer as an instrument for sign-up to estimate treatment effects among compliers/participants. This distinction is directly useful for CMAT: observed visits are uptake, while PPA context is not randomized in our data.

## What this paper lets us say

- Financial incentives can raise use of offered academic-support services.
- Treatment response can differ sharply by subgroup.
- Some intervention-associated academic differences can persist after the active intervention period.
- Random assignment of an offer and actual support use are analytically distinct.

## What it does **not** let us say

- PPA has the same causal effect as Project STAR.
- Persistence in later CMAT use must reflect improved study habits.
- The female-specific STAR result generalizes automatically to CMAT.
- Observed CMAT use can be interpreted as randomized treatment receipt.

## Local verification

Markdown: `literature/library/articles/angrist_2009_incentives-services-college-achievement.md`

PDF: `literature/library/pdf/angrist_2009_incentives-services-college-achievement.pdf`

Key anchors: study design around pp. 3–5; Table 3 for service take-up; pp. 12–13 / Table 5 for first-year outcomes; later tables for second-year/IV analyses.