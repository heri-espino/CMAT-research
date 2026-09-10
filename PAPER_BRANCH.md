# Paper 1 — PPA persistence branch

This branch is the canonical publication workspace for Paper 1. It inherits shared infrastructure from `main` and owns only publication-specific selection and production.

- `literature_selected/`: selected literature, reading notes and annotated source Markdown;
- `code/`: paper-specific orchestration importing the installed `cmat_analysis` library;
- `results/`: generated/selected aggregate paper outputs;
- `paper/`: manuscript and build material;
- `submission/`: journal-specific material.

## Canonical Paper 1 runner

Install the shared library once from the repository root:

```bash
python -m pip install -e './cmat_analysis[dev]'
```

Validate the branch without private data:

```bash
python code/run_paper.py --check
```

Reproduce the current PPA-persistence specification with controlled local inputs:

```bash
python code/run_paper.py \
  --materias '/path/to/Materias.xlsx' \
  --asesorias '/path/to/Asesorias.xlsx' \
  --compare-retained
```

Use `--compile` to delegate to `paper/build.py` after a successful scientific run. The runner writes only aggregate publication outputs under `results/`; raw/row-level administrative data must never be committed.

## Coordination contract

This branch may be developed by a paper-specific research/writing chat, but repository-wide governance belongs to the designated repo-admin / integrator / upstream-maintainer workflow. The user retains final scientific authority.

Chats cannot communicate directly with one another. Durable decisions, requested upstream changes, methodological caveats, and handoffs must therefore be written into repository documentation rather than assumed to exist in another chat's context.

Do **not** open or merge a pull request that brings this entire paper branch into `main`. This branch is intentionally ahead of `main` because it owns publication-specific material.

If Paper 1 work discovers reusable scientific logic, do not maintain a divergent implementation here. Escalate the reusable capability for upstream review, implement and validate it under `main/cmat_analysis/src/cmat_analysis/`, and then bring the updated `main` back into this branch. Cross-paper empirical or methodological knowledge should similarly move through shared `brainstorm/` when appropriate rather than being copied manually between paper branches.

When `main` is synchronized into this branch, follow `docs/REPO_GOVERNANCE.md` and the root `AI_HANDOFF.md` as the canonical repository-wide contract.
