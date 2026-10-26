# Paper 2 — Marp presentation (scientific review draft)

**Version:** 0.2.0-review2; **date:** 2026-10-26; **22 main slides + 8 technical appendix slides**. Source is editable `slides.md`; local vector assets are in `figures/`; speaker notes are also extracted in `speaker_notes.md`.

## Scientific status

The source is a **provisional evidence synthesis**. The methodological claims matrix (PR #97) and manuscript draft (PR #99) now exist for review; neither is merged scientific approval. Validated PPA adjusted contrasts remain unavailable. All PPA diagram panels are conceptual and have no invented estimates. The deck makes no causal CMAT-effect claims. Raw, adjusted, fitted, model-selected and predictive quantities are explicitly distinguished.

## Evidence tip commits

- Paper 2.1 Holm: `1546c594bfb6867ad52064594469061ec7fd7fc6`.
- Fused: `29810a86aef4c13a0327760955fae674ac349981`.
- Mixtures: `b1cace126fd73b74e8353c8a6170dc40af2243c2`.
- Shapley/curves: `5915976ff5a7e3c4eededd0c1e39290b8b4d402c`.
- Integration branch base from main `d61739ff89eca96be5113a1cb47ea8be496891dd`.

Figures are regenerated programmatically from *aggregate values extracted from committed CSV files* named in each slide's footer; figure SVGs are editable. The original source files and manifests remain on their cited historical branches. SVG encoding is plain UTF-8, not externally linked.

## Reproduce with the official Marp renderer

```bash
npx @marp-team/marp-cli@latest --allow-local-files slides.md -o deck.pdf
```

The exported PDF requires an authoritative Marp CLI rebuild and review after the integrated methods audit is accepted. The preliminary PDF provided separately with the handoff was exported and visually checked using the available offline CSS renderer because network package installation was unavailable. Do not claim publication readiness. Preserve professor-period cluster and Holm caveats. This contribution does not change the manuscript, root README, pipelines or shared workflows.

## Second pass and confidentiality gate (2026-10-26)

- Reconciled claims with methods-agent matrix PR #97, manuscript provenance PR #99, PPA methodology PR #98 and independent QA PR #96.
- The original primary users-only six-group analysis has **15** Holm pairwise comparisons per outcome. The supplementary full-cohort five-group analysis has **10**, positive-only seven-group sensitivity **21**, and full eight-group sensitivity **28**. Adjacent-step and two-part exploratory families have **7** and **2** within-outcome tests respectively.
- New PPA group adjusted estimates were unavailable. PR #98 proposes **18 Holm tests in total across both outcomes** across primary and secondary categorical models and two outcomes. Historical counts are only arithmetic references, not model outputs.
- **Critical: PR #96 reports controlled student-level rows publicly accessible through the repository tree. Treat as an active privacy incident requiring institutional and administrator review, including history. Do not release this draft presentation as an approved institutional scientific product.**
- Historical PASS-logit files mark undefined inferential results as rejected; do not use those flags. PASS-LPM is a distinct estimable specification.
- `deck.pdf` is an **offline vector review preview**. An authoritative Marp CLI PDF export and visual inspection have not been completed in this connected GitHub environment; the locally recreated second-pass CSS deck is validated separately and has a richer PNG figure set.
