# Paper 2 — MU performance branch

This branch is the canonical publication workspace for Paper 2. It inherits shared infrastructure from `main` and owns only publication-specific selection and production.

- `literature_selected/`: selected literature and reading notes;
- `code/`: paper-specific orchestration importing `cmat_analysis`;
- `results/`: generated/selected paper outputs;
- `paper/`: manuscript and build material;
- `submission/`: journal-specific material.

## Scientific scope

Paper 2 studies the association between same-period CMAT use and classroom-relative academic performance in the first eligible attempt at Matemáticas Universitarias. Its main empirical distinction is use versus non-use, while positive-use dose categories are examined without assuming a causal monotone dose-response.

The historical `proyecto_visitas` work is decomposed rather than copied. `paper/DECOMPOSITION_FROM_PROYECTO_VISITAS.md` is the binding scope map: student support use/performance belongs here; professor grade distributions, grading-profile clusters, and grading-regime stability belong to Paper 3; general service-load material remains brainstorm/provenance.

## Coordination contract

This branch may be developed by a paper-specific research/writing chat, but repository-wide governance belongs to the designated repo-admin / integrator / upstream-maintainer workflow. The user retains final scientific authority.

Chats cannot communicate directly with one another. Durable decisions, requested upstream changes, methodological caveats, and handoffs must therefore be written into repository documentation rather than assumed to exist in another chat's context.

Do **not** open or merge a pull request that brings this entire paper branch into `main`. This branch is intentionally ahead of `main` because it owns publication-specific material.

If Paper 2 work discovers reusable scientific logic, do not maintain a divergent implementation here. Escalate the reusable capability for upstream review, implement and validate it under `main/cmat_analysis/src/cmat_analysis/`, and then bring the updated `main` back into this branch. Cross-paper empirical or methodological knowledge should similarly move through shared `brainstorm/` when appropriate rather than being copied manually between paper branches.

When `main` is synchronized into this branch, follow `docs/REPO_GOVERNANCE.md` and the root `AI_HANDOFF.md` as the canonical repository-wide contract.
