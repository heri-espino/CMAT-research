# Git workflow

`main` is the shared upstream research branch. The long-lived publication branches are `paper/paper1-ppa-persistence`, `paper/paper2-mu-performance`, `paper/paper3-grading-heterogeneity`, `paper/paper4-degree-help-seeking`, and `paper/paper5-longitudinal-trajectories`.

Shared library, data-contract, literature, brainstorm and programme-documentation changes should land on `main`, then be merged/rebased into active paper branches. Paper-specific `literature_selected/`, `code/`, `results/`, `paper/` and `submission/` changes remain on that paper branch.

Do not merge a paper branch wholesale back into `main`, because that would reintroduce publication-specific trees. Promote genuinely shared changes upstream as focused commits or cherry-picks.
