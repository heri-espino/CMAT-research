# Source register — frozen branch inventory

**Inventory dated:** 2026-10-26. **Upstream comparator:** `main` commit `d61739ff89eca96be5113a1cb47ea8be496891dd` (tree `ceb238596490b0c30cfdf832976f476803615649`). **Scope:** all *file blobs differing in path or content* from this comparator in each source branch, including code, manuscripts, figures, result tables, tests, protocol notes, CI/workflow changes and transient QA material. Historical branches are not modified.

The machine-readable, **file-by-file and SHA-complete** register is [`source-register.tsv`](source-register.tsv). Each record provides source branch, original path, frozen **commit SHA**, file **blob SHA**, byte size, asset classification, branch-level completion label, disposition, proposed canonical namespace, immutable source hyperlink and dependency note. A proposed slot is not a claim that the file was copied; `copied-frozen` is the only imported-file disposition. Repeated paths are intentionally listed for each distinct frozen branch head, allowing identical inherited hashes to be compared rather than silently choosing a latest variant.

| Branch | Head SHA | Changed file blobs vs main | Branch-level disposition |
|---|---|---:|---|
| `paper/paper2-mu-performance` | `ac6f71208c503ab5a9e206f672746c57cb44a72e` | 93 | historical-draft |
| `paper/paper2.1-visit-frequency` | `1546c594bfb6867ad52064594469061ec7fd7fc6` | 221 | historical-holm-run |
| `paper/paper2.2.1-fused-frequency` | `29810a86aef4c13a0327760955fae674ac349981` | 287 | bootstrap-100-complete-extra-sensitivities-pending |
| `paper/paper2.2.2-distributional-heterogeneity` | `b1cace126fd73b74e8353c8a6170dc40af2243c2` | 234 | inherited-gmm-only-new-modality-pending |
| `research/paper21-shapley-predictive-importance` | `5915976ff5a7e3c4eededd0c1e39290b8b4d402c` | 251 | shapley-followup-curves-aggregates-present |

**Total**: 1086 branch/path rows, including 21 PDF-sized (≤200 byte) Git LFS pointers across frozen source trees; these pointers are **not** readable PDF bytes. The established Paper 2.1 `paper/paper.pdf` is an independently present ~302 KB Git blob and is kept at its original permalink. Source files identical to upstream `main` are not listed because they remain in the shared upstream and are not branch-specific migration work. This is a *comparison inventory*, not a full list of every tracked common upstream path or a statement that every changed file is scientifically relevant.

## Conflict and status ledger

- MU: original paper and `0/1/2/3/4+`; working draft and runnable historical recipe; entrance-exam baseline, ethics wording, robustness review still open.
- Paper 2.1: Holm/Wald outcome models and manuscript/aggregate files exist; distinguish `1/2/3/4/5/6+` from `0/1/2/3/4/5/6/7+` and 15/21/28 pair families; draft not submission-ready.
- Fused: 100/100 bootstrap fits documented for each of four specifications in the 2026-10-08 run; its branch-level earlier `PAPER_BRANCH.md` claims pending, superseded for **that experiment only** by dated notes and `run_manifest.json`. Further CV/selection-rule robustness remains open.
- Mixture: inherited Paper 2.1 GMM/skew-normal studies exist; novel Paper 2.2.2 modality-validation runner/results do **not** exist at this head. There is no demonstrated multimodal or identifiable student-type result.
- Shapley: grouped-Shapley CSVs, four follow-up CSVs, five attendance-curve CSVs and four PNG curve figures present at head; dated publication ledger's earlier missing-output section is superseded by its 2026-10-26 verification. Cross-model scientific synthesis remains open.

## Method-level primary original sources

- [Original MU paper status](https://github.com/heri-espino/CMAT-research/blob/ac6f71208c503ab5a9e206f672746c57cb44a72e/paper/STATUS_AND_ROADMAP.md).
- [Paper 2.1 grouping rationale](https://github.com/heri-espino/CMAT-research/blob/1546c594bfb6867ad52064594469061ec7fd7fc6/paper/docs/analysis/VISIT_GROUPING_DECISION.md).
- [Completed fused-lasso bootstrap note](https://github.com/heri-espino/CMAT-research/blob/29810a86aef4c13a0327760955fae674ac349981/notes/2026-10-07_fused_lasso_100_bootstrap_results.md) and [manifest](https://github.com/heri-espino/CMAT-research/blob/29810a86aef4c13a0327760955fae674ac349981/results/paper221/run_manifest.json).
- [Novel modality branch contract](https://github.com/heri-espino/CMAT-research/blob/b1cace126fd73b74e8353c8a6170dc40af2243c2/PAPER_BRANCH.md) and [inherited mixture results](https://github.com/heri-espino/CMAT-research/blob/b1cace126fd73b74e8353c8a6170dc40af2243c2/paper/docs/results/MIXTURE_ANALYSIS_RESULTS.md).
- [Shapley, follow-up, and curve tracker](https://github.com/heri-espino/CMAT-research/blob/5915976ff5a7e3c4eededd0c1e39290b8b4d402c/notes/20_RESEARCH_TRACKER.md), [curve results](https://github.com/heri-espino/CMAT-research/blob/5915976ff5a7e3c4eededd0c1e39290b8b4d402c/notes/24_ATTENDANCE_CURVE_RESULTS.md).

Inventory is **existence and provenance verification**, not execution of synthetic tests, statistical inference, privacy audit of each CSV, LaTeX build, or a conclusion that results across branches agree.
