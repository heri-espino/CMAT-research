# Paper 2 — Beyond First Attendance

**Status (2026-10-26): architecture/migration established; no unified manuscript, validated new analysis, integrated PDF, or Marp deck is claimed.** This is the namespace for one proposed observational publication, not a fusion of formerly separate scientific conclusions.

## Publication entry points

- **Current readable historical PDF:** [Paper 2.1 working PDF](https://github.com/heri-espino/CMAT-research/blob/1546c594bfb6867ad52064594469061ec7fd7fc6/paper/paper.pdf), preserved on the original branch (native Git blob, 301,630 bytes). This remains the published/viewable working draft until a new PDF has been built and scientifically approved.
- **Historical editable manuscript:** [Paper 2.1 TeX sources](https://github.com/heri-espino/CMAT-research/tree/1546c594bfb6867ad52064594469061ec7fd7fc6/paper/sections) and [references](https://github.com/heri-espino/CMAT-research/blob/1546c594bfb6867ad52064594469061ec7fd7fc6/paper/references.bib).
- **Integrated manuscript:** `manuscript/` (awaiting manuscript agent; **no** `paper.pdf` is present in this namespace).
- **Marp presentation:** `presentation/marp/` (awaiting presentation agent; **no** compiled deck is present).
- **Provenance and decisions:** [migration map](docs/migration-map.md), [full source register](docs/source-register.md), [decision log](docs/migration-decisions.md), [agent handoff](docs/agent-handoff.md).

## Architecture

```text
papers/paper2-beyond-first-attendance/
  README.md
  manuscript/              # integrated English TeX, bibliography, approved PDF (future)
  analysis/
    holm/                   # historical Wald/Holm anchor
    ppa-groups/             # prospective explicit coarse-group study (post hoc)
    first-visit-curves/     # two-part/functional-shape exploratory sensitivities
    fused/                  # ordered fusion: experimental evidence
    mixture/                # inherited historical GMM; new modality validation pending
    shapley/                # predictive-skill attribution, not causality
  results/
    tables/                 # approved publication-safe aggregate exports (future)
    figures/                # approved figures (future)
    provenance/             # manifests, source checks, disclosure review
  supplement/              # technical details; not assembled yet
  presentation/marp/        # Marp source, referenced figures and built PDF (future)
  docs/                     # source ledger, method conflicts, handoff
```

The inventory [TSV](docs/source-register.tsv) maps **every one of 1,086 source-branch file differences against the creation-time main commit** among the five frozen source branches; unchanged shared-main files are intentionally not recatalogued. Historical assets remain at SHA-pinned URLs, with one 441-byte JSON grouping specification selectively reused by identical Git blob. No entire branch trees or historical output collections were copied.

## Scientific contract

Study subject: first eligible Matemáticas Universitarias (MU) attempts, recorded CMAT attendance during the same academic period, and distinct performance outcomes. **6,627 attempts, 190 instructor-period groups, 1,234 attendees** are the historical cohort numbers—not a freshly revalidated pooled estimate. This is observational; visits are not randomly assigned, PPA1 eligibility/credit is not observed, and ordered association is not causal dose response.

Use original 15/21/28-pair Holm families as labeled. The **only requested new PPA-threshold grouping** is `0 | 1–3 | 4+` (historical counts: 5,393 / 932 / 302). It is exploratory and not interchangeable with historical Holm comparisons. The previously suggested `0 | 1–3 | 4 | 5+` is **not** a required analysis. BA/BV/RT must remain distinguishable from numeric marks and numeric-only complete cases.

See the [consolidation charter](https://github.com/heri-espino/CMAT-research/blob/d6b1670553e9a838339c4c0bebb397667ba3a392/docs/PAPER2_CONSOLIDATION_PLAN.md) before creating downstream branches. Agents branch from `paper/paper2-beyond-first-attendance` and send PRs **to this branch**, not directly to `main`. Upstream shared `cmat_analysis/`, workflows, root README and branch-retirement decisions remain admin-controlled.
