# Repository governance and AI coordination

This document is the canonical coordination contract for the CMAT research repository.

## Authority and roles

The user/researcher retains final scientific and project authority. Architecture, methodological interpretation, publication strategy, and scientific claims remain subject to the user's approval.

A designated **repo-admin / integrator / upstream-maintainer chat** coordinates repository-wide work. Its responsibilities are to maintain Git and branch coherence, protect the shared scientific architecture, integrate reusable improvements into `main`, preserve provenance and methodological contracts, and coordinate the flow of work across the five paper branches.

Other chats may act as **paper-specific research and writing agents**. They may work deeply inside one publication branch, including literature selection, analysis orchestration, result production, manuscript drafting, robustness work, and submission preparation, but they should not independently redesign the repository-wide architecture or treat paper-specific requirements as shared infrastructure without upstream review.

## No direct inter-chat channel

Chats cannot send messages directly to one another as an inter-chat communication channel. Do not assume that another chat has seen a decision merely because it was discussed elsewhere.

The repository is therefore the persistent coordination layer. Decisions that must survive a chat session or be visible to another agent must be written into canonical repository documents such as:

- `AI_HANDOFF.md` for repository-wide operating rules;
- `docs/REPO_GOVERNANCE.md` for governance and cross-branch coordination;
- `cmat_analysis/AI_HANDOFF.md` for the shared scientific library;
- `brainstorm/AI_HANDOFF.md` for research-development work;
- `PAPER_BRANCH.md` for the contract of a specific publication branch;
- component READMEs and provenance records when a rule belongs to a narrower scope.

A proposal produced in another chat can also be brought to the repo-admin chat for review before it is integrated upstream.

## Branch responsibilities

`main` is the scientific upstream and owns shared infrastructure:

```text
cmat_analysis/
data/
literature/
brainstorm/
docs/
```

Each long-lived `paper/*` branch inherits `main` and adds publication-specific material such as:

```text
literature_selected/
code/
results/
paper/
submission/
PAPER_BRANCH.md
```

Paper branches are intentionally ahead of `main`. Do **not** open or merge a pull request that brings an entire paper branch back into `main`; doing so would reintroduce publication-specific material into the shared upstream.

## Upstream-change protocol

When paper-specific work discovers a capability that is genuinely reusable across papers, the reusable part belongs upstream. The expected flow is:

```text
paper-specific need
        ↓
identify reusable scientific capability
        ↓
review/integrate through repo-admin coordination
        ↓
main/cmat_analysis
        ↓
tests + documentation + provenance as appropriate
        ↓
bring updated main into the relevant paper branch(es)
```

The paper branch may retain orchestration that answers its own research question, but reusable cohort definitions, estimators, statistical tests, transformations, uncertainty calculations, imputation logic, and plotting functions should not remain as divergent paper-local implementations.

Likewise, if a paper discovers a broader empirical or methodological result that should inform several publications, preserve it in `brainstorm/` or another shared upstream record rather than copying it manually between paper branches.

## Repo-admin responsibilities

The repo-admin / integrator / upstream-maintainer role should:

1. maintain the conceptual boundary between shared upstream and publication-specific work;
2. review cross-branch changes before they become canonical shared infrastructure;
3. keep `cmat_analysis` installable, tested, documented, and reusable;
4. preserve scientific provenance, historical definitions, retained outputs, and data/privacy rules;
5. coordinate updates from `main` into paper branches without merging whole paper workspaces back upstream;
6. prevent duplicate or conflicting implementations across branches;
7. record durable decisions in the repository rather than relying on chat history;
8. review proposals produced by paper-specific chats when the user brings them back for integration.

Paper-specific agents should optimize their publication; the repo-admin should optimize coherence of the whole research programme.
