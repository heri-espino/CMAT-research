# Architecture handoff to analysis, methods, manuscript and presentation agents

**Integration branch:** `paper/paper2-beyond-first-attendance` (from `main` `d61739ff89eca96be5113a1cb47ea8be496891dd`). **Ownership:** architecture stage only. Read `README.md`, `docs/migration-map.md`, `docs/source-register.tsv`, `docs/migration-decisions.md` and `main/docs/PAPER2_CONSOLIDATION_PLAN.md` before starting.

Use exact source-commit permalinks from the register; do **not** treat proposed namespace slots as migrated files. Existing source branches and Paper 2.1 PDF have not been modified. Source tree assets overlapping across branches may share blob SHAs but are not independent replications.

## Assigned work

- **PPA group analysis agent:** branch `paper/paper2-ppa-groups-agent` from this branch; own `analysis/ppa-groups/` and approved tables/figures. Implement nonoverlapping `0 | 1–3 | 4+` and `0 | 1–3 | 4 | 5+`, with group counts, professor-period overlap, cluster-robust CI and transparent exploratory Holm family; synthetic fixtures, outcome definitions, no PPA-treatment mechanism.
- **Methods audit agent:** `paper/paper2-methods-audit-agent`; own `docs/claims-evidence-matrix.md`, reconciliation of cohort/outcomes/families and provenance manifests; explicitly adjudicate stale status and conflicts instead of substituting method-specific estimates.
- **Manuscript agent:** `paper/paper2-manuscript-agent`; own `manuscript/` and `supplement/`. Use original Wald/Holm evidence as inferential anchor; distinguish exploratory model-selection evidence; do not publish a replacement PDF/link without source-claim audit, build and review.
- **Marp presentation agent:** `paper/paper2-marp-agent`; own `presentation/marp/`, with figures drawn only from verified aggregate outputs. Produce editable Markdown and validate actual exported PDF bytes; not before statistical synthesis.

All downstream PRs target `paper/paper2-beyond-first-attendance`. Each should report its source SHAs, output paths, dependency versions, tests and build logs, observational caveats, missing controlled data, and any scientific conflicts. The administrator controls `main` promotions, root `README.md`, workflows and merges.

**Reusable-code review queue, without changes:** `cmat_analysis/src/cmat_analysis/statistics/{attendance_frequency,inference,ordered_fusion,mixtures}.py`; synthetic tests `test_{attendance_frequency,ordered_fusion,mixtures}.py` plus branch-only `test_paper21_{shapley_importance,attendance_curves,followup_questions}.py`. Check `cmat_analysis/FUNCTION_INDEX.md` before proposing generalized estimators, group-validation, cluster bootstrap, shape comparison or predictive decomposition helpers. Branch scripts remain publication orchestration until independently reviewed.

**Approval gates:** aligned input fingerprints, data disclosure assessment, compatible outcome/cohort labels, original multiplicity families, no causal language, run manifests for all reported estimates, independently tested PDF and Marp builds, and human scientific sign-off. New 2.2.2 modality tests remain pending. Do not silently fill scientific gaps or mark the integrated paper submission-ready.
