# Paper 2 — status and roadmap

**Canonical branch:** `paper/paper2-mu-performance`  
**Primary target:** *Teaching Mathematics and its Applications* (TEAMAT), Section A research article  
**Status updated:** 2026-09-19

This file is the operational source of truth for **where Paper 2 stands, what is already decided, what remains to be done, and what the next agent should do**. Scientific and stylistic rules remain in `paper/AI_HANDOFF.md`; background and scope remain in `paper/PROJECT_CONTEXT.md`.

## Current state

The manuscript is a functioning research draft, not a submission-ready final.

- The official and commented manuscripts compile successfully in GitHub Actions.
- The controlled Paper 2 recipe runs successfully in CI.
- Current study sample: **N = 6,627** first eligible MU attempts in periods with CMAT attendance coverage.
- Primary attendance presentation: **0 / 1 / 2 / 3 / 4+ same-period CMAT visits**.
- Primary continuous outcome: final MU performance standardised within the existing **instructor × academic-period grading group** (`CLASSROOM_ID` in the analysis code).
- Primary inferential model: exact attendance-group indicators with instructor--period fixed effects, degree-programme indicators, cluster-robust standard errors at the instructor--period level, and Holm adjustment across the ten pairwise comparisons.
- Welch ANOVA and Games--Howell comparisons are secondary/unadjusted.
- The paper is explicitly observational. Do not convert the reported associations into causal effects.
- The user **requested university entrance-exam results on 2026-09-19**. Those data have not yet been received or audited.
- Exact institutional ethics/data-use wording and any approval/authorization identifier are still required before submission.

The most recent manuscript interpretation is that students with recorded CMAT attendance have higher standardised grades than students with no recorded attendance, while differences among the positive attendance-frequency groups do not show a stable ordering across analyses.

## Read order for a new agent

Before changing Paper 2, read these files in order:

1. `PAPER_BRANCH.md` — branch ownership and governance.
2. `paper/STATUS_AND_ROADMAP.md` — current status, milestones, dependencies, and next actions.
3. `paper/PROJECT_CONTEXT.md` — research question, population, exposure, outcome, and journal strategy.
4. `paper/AI_HANDOFF.md` — binding scientific, terminology, literature, and TEAMAT rules.
5. `paper/ENTRANCE_EXAM_PLAN.md` — protocol for the requested baseline-admission data.
6. `paper/SUBMISSION_METADATA.md` and `submission/README.md` — submission-specific metadata and blockers.
7. `code/run_paper.py` and `paper/build.py` — canonical analysis/build entry points.

Do not treat chat history as a source of truth when it conflicts with these files.

## Decisions that are closed unless the user reopens them

These are not pending methodological choices.

- **Attendance exposure is period-wide CMAT use.** Count all visits in the MU academic period irrespective of the subject label attached to an individual visit. Do not restrict the primary exposure to MU-tagged visits.
- **Use the exact attendance groups 0, 1, 2, 3, 4+.** Do not pool 1 and 2 in the main analysis.
- **The three-visit PPA requirement is context, not the estimand.** Do not turn Paper 2 into a threshold or encouragement-design paper.
- **Standardise grades within the existing instructor × academic-period grading group.** This is substantive because instructors set and grade their own assessments and grading difficulty may differ across groups.
- **Keep causal language out of the paper.** Fixed effects, clustering, baseline controls, propensity scores, or the requested entrance exam do not by themselves identify a causal effect.
- **Do not use the optional DMU diagnostic exam as a Paper 2 baseline covariate.** Its participation is incomplete/selective.
- **Do not merge the whole paper branch into `main`.** Reusable scientific capabilities must go through the upstream-maintainer workflow described in repository governance.

## Milestones

### M0 — Reproducible baseline manuscript — COMPLETE

- [x] Paper 2 branch and scope established.
- [x] Controlled-data analysis recipe exists.
- [x] Exact attendance groups 0/1/2/3/4+ are the primary presentation.
- [x] Instructor--period grade standardisation is implemented.
- [x] Main fixed-effect pairwise model and multiplicity adjustment are implemented.
- [x] Main figures and manuscript are reproducible from aggregate tables.
- [x] TEAMAT/IMA LaTeX build works in GitHub Actions.
- [x] Literature framing distinguishes usage records, help-seeking constructs, observational associations, and identification-oriented evidence.
- [x] Current CI checks pass.

### M1 — Scientific-referee robustness pass — IN PROGRESS

The recipe already contains referee-oriented sensitivities, but they still need to be reviewed as a coherent scientific package and incorporated into the manuscript only where they materially affect interpretation.

Already implemented in `code/run_paper.py`:

- [x] adjusted fixed-effect models for uniform-imputation and numeric-complete-case outcomes → table 39;
- [x] attendance-group pass-rate summary → table 40;
- [x] adjusted fixed-effect model for binary PASS → tables 41–42;
- [x] withdrawal share by attendance group → table 49;
- [x] leave-one-period-out fixed-effect estimates → table 50.

Still required:

- [ ] inspect tables 39–42 and 49–50 from a canonical controlled-data run and document whether they change the substantive interpretation;
- [ ] implement and inspect an **instructor-level clustering sensitivity**, because instructors recur across academic periods;
- [ ] decide which robustness results belong in the main paper and which belong in supplementary/submission material;
- [ ] update Results/Limitations only after the canonical outputs have been reviewed;
- [ ] perform a final scientific-referee read focused on selection, temporal ordering, withdrawal opportunity, inference, and interpretation rather than prose style.

**Do not add provisional audit numbers to the manuscript.** Manuscript values must come from the reproducible Paper 2 recipe or another explicitly versioned canonical analysis.

### M2 — University entrance-exam baseline — WAITING ON EXTERNAL DATA

The user requested the entrance-exam results on **2026-09-19**. This is currently the most important external scientific dependency because prior mathematical/academic preparation is the clearest remaining confounding concern.

- [x] data requested;
- [ ] data received;
- [ ] data dictionary / score meaning received;
- [ ] privacy and pseudonymisation route confirmed;
- [ ] join key confirmed;
- [ ] coverage and missingness audited;
- [ ] scale/version comparability across admission cohorts audited;
- [ ] relevant quantitative/mathematics component identified, if one exists;
- [ ] baseline-adjusted sensitivity model specified;
- [ ] sensitivity model run and compared with current estimates;
- [ ] manuscript updated only if the new analysis is interpretable.

Follow `paper/ENTRANCE_EXAM_PLAN.md` exactly. Do not simply add the score to the main regression on receipt.

### M3 — Submission blockers and manuscript freeze — BLOCKED / NOT STARTED

- [ ] obtain the exact UDLAP ethics/IRB approval, exemption, or institutional data-use authorization wording;
- [ ] obtain any required approval/reference/permit identifier;
- [ ] resolve every visible `\draftnote{}` before submission;
- [ ] decide the final role of the entrance-exam sensitivity after M2;
- [ ] complete the robustness decisions from M1;
- [ ] perform a final citation/reference audit;
- [ ] perform a final numbers-to-generated-output audit;
- [ ] perform a final figure/table/caption audit;
- [ ] confirm all author metadata required by TEAMAT; Daniela Cortés-Toto's ORCID is currently not provided and must not be invented;
- [ ] rebuild clean and commented PDFs from the frozen analysis outputs and require green CI.

Scientific freeze means no unresolved analysis question capable of changing the headline interpretation, all manuscript numbers trace to canonical outputs, and all external ethics requirements are documented.

### M4 — TEAMAT submission package — NOT STARTED

- [ ] prepare final clean manuscript source and PDF;
- [ ] prepare any anonymised manuscript variant if required by the current TEAMAT submission system;
- [ ] prepare cover letter;
- [ ] prepare data-availability and code-availability wording;
- [ ] prepare submission checklist and final author metadata;
- [ ] preserve the exact submission commit/tag or release identifier;
- [ ] archive the final compiled artifact and non-disclosive aggregate replication outputs.

Submission material belongs under `submission/`; scientific results remain sourced from `results/`.

### M5 — Review/revision cycle — FUTURE

- [ ] save reviewer/editor comments in a durable submission record;
- [ ] create a point-by-point response document;
- [ ] distinguish requests that affect scientific estimands from presentation-only requests;
- [ ] rerun analyses rather than editing reported numbers manually;
- [ ] preserve pre-revision and revised manuscript checkpoints;
- [ ] update this roadmap after each editorial decision.

## Priority queue

**P0 — external blockers:** receive/audit entrance-exam data; obtain exact institutional ethics/data-use wording and identifier.

**P1 — scientific work that can proceed now:** review canonical outputs 39–42 and 49–50; add instructor-level clustering sensitivity; decide main-text versus supplementary placement; rerun the scientific-referee pass.

**P2 — submission preparation:** resolve manuscript TODOs; freeze numbers/figures/tables; complete cover letter/checklist/submission package.

Do not expand the bibliography, redesign figures, or add modelling machinery merely to make the paper look more sophisticated unless a concrete scientific or journal requirement justifies it.

## Canonical commands

```bash
python -m pip install -e './cmat_analysis[dev]'
python code/run_paper.py --check
```

```bash
python code/run_paper.py \
  --materias data/controlled/Materias_pseudonymized.csv \
  --asesorias data/controlled/Asesorias_pseudonymized.csv
```

```bash
python paper/build.py
```

Or:

```bash
python code/run_paper.py \
  --materias data/controlled/Materias_pseudonymized.csv \
  --asesorias data/controlled/Asesorias_pseudonymized.csv \
  --compile
```

## Handoff protocol

At the end of any substantial future work session:

1. update the relevant milestone/checklist in this file;
2. record any new closed scientific decision in `paper/AI_HANDOFF.md`;
3. update `paper/PROJECT_CONTEXT.md` only when the study definition or high-level project state changes;
4. update `submission/README.md` only for submission-stage requirements;
5. ensure generated manuscript claims trace to reproducible outputs;
6. run or inspect CI;
7. commit with a message that states what scientific/project state changed.

A future agent should be able to determine the next task from this repository without needing the previous chat.
