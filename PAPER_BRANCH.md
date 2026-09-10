# Paper 3 — grading heterogeneity branch

This branch is the canonical publication workspace for Paper 3. It inherits shared infrastructure from `main` and owns only publication-specific selection and production.

- `literature_selected/`: selected literature and reading notes;
- `code/`: paper-specific orchestration importing `cmat_analysis`;
- `results/`: generated/selected paper outputs;
- `paper/`: manuscript and build material;
- `submission/`: journal-specific material.

## Coordination contract

This branch may be developed by a paper-specific research/writing chat, but repository-wide governance belongs to the designated repo-admin / integrator / upstream-maintainer workflow. The user retains final scientific authority.

Chats cannot communicate directly with one another. Durable decisions, requested upstream changes, methodological caveats, and handoffs must therefore be written into repository documentation rather than assumed to exist in another chat's context.

Do **not** open or merge a pull request that brings this entire paper branch into `main`. This branch is intentionally ahead of `main` because it owns publication-specific material.

If Paper 3 work discovers reusable scientific logic, do not maintain a divergent implementation here. Escalate the reusable capability for upstream review, implement and validate it under `main/cmat_analysis/src/cmat_analysis/`, and then bring the updated `main` back into this branch. Cross-paper empirical or methodological knowledge should similarly move through shared `brainstorm/` when appropriate rather than being copied manually between paper branches.

When `main` is synchronized into this branch, follow `docs/REPO_GOVERNANCE.md` and the root `AI_HANDOFF.md` as the canonical repository-wide contract.
