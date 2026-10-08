# Git workflow

`main` is the shared upstream research branch. Current publication/research-paper branches are indexed in `docs/PUBLICATION_PORTFOLIO.md`, including the newer Paper 2.1 branch and the prospective Paper 2.2.1 (fused frequency) and 2.2.2 (distributional modality) design-only branches.

Shared library, data-contract, literature, brainstorm and programme-documentation changes should land on `main`, then be merged/rebased into active paper branches. Paper-specific `literature_selected/`, `code/`, `results/`, `paper/` and `submission/` changes remain on that paper branch.

Do not merge a paper branch wholesale back into `main`, because that would reintroduce publication-specific trees. Promote genuinely shared changes upstream as focused commits or cherry-picks.
