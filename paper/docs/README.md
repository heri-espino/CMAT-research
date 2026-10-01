# Paper 2.1 internal documentation

The manuscript source remains directly under `paper/`; research-development documents are grouped here by purpose so that the manuscript directory stays readable.

## Project

- `project/PROJECT_CONTEXT.md` — scientific question, scope, population and framing.
- `project/STATUS_AND_ROADMAP.md` — current state, completed milestones and remaining blockers.
- `project/DECOMPOSITION_FROM_PROYECTO_VISITAS.md` — provenance from the historical project and portfolio boundary.

## Analysis

- `analysis/ANALYSIS_PLAN.md` — pre-outcome analysis contract.
- `analysis/OUTCOME_FRAMEWORK.md` — performance and academic-management outcome hierarchy.
- `analysis/VISIT_GROUPING_DECISION.md` — frozen outcome-blind visit grouping.
- `analysis/MIXTURE_ANALYSIS_PLAN.md` — numeric-failure, GMM and skew-normal analysis specification.
- `analysis/ENTRANCE_EXAM_PLAN.md` — planned prior-preparation sensitivity if entrance-exam data become available.

## Results

- `results/PRELIMINARY_RESULTS.md` — verified controlled-data results used during manuscript development.
- `results/MIXTURE_ANALYSIS_RESULTS.md` — detailed mixture/shape results and validation provenance.

## Interpretation

- `interpretation/ACADEMIC_MANAGEMENT_HYPOTHESIS.md` — mechanism hypothesis and causal guardrails.
- `interpretation/ADMINISTRATIVE_OUTCOME_NOTE.md` — internal note on administrative outcome composition.

Literature-specific access notes live in `literature_selected/ACCESS_NOTES.md`, while submission-system metadata lives in `submission/METADATA.md`. Branch-level navigation starts at `PAPER_BRANCH.md`, and manuscript/build instructions remain in `paper/README.md`.

## Observation audit

- `observations/README.md` — local-only observation-level audit workflow.
- `observations/group5_observation_audit.tex` — standalone companion source motivated by the five-visit numeric-failure feature.
- `observations/build_observation_audit.py` — generates de-identified observation profiles and classroom-distribution figures into an ignored local directory.
