# Paper 2 — Marp presentation (scientific review draft)

**Version:** 0.1.0; **date:** 2026-10-26; **22 main slides + 8 technical appendix slides**. Source is editable `slides.md`; local vector assets are in `figures/`; speaker notes are also extracted in `speaker_notes.md`.

## Scientific status

The source is a **provisional evidence synthesis**. The integrated manuscript, signed-off claims matrix and validated new PPA contrasts were unavailable when produced. All PPA diagram panels are conceptual and have no invented estimates. The deck makes no causal CMAT-effect claims. Raw, adjusted, fitted, model-selected and predictive quantities are explicitly distinguished.

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
