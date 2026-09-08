# Repository operating rules

This is the canonical CMAT research repository.

## Before changing code

1. Read `docs/AI_HANDOFF.md` and `docs/STUDY_PROTOCOL.md`.
2. Search `docs/PYTHON_FUNCTION_INDEX.md` before creating a new function.
3. Preserve observational/associational language unless a design explicitly identifies a causal estimand.
4. If scientific Python changes, update the function index, handoff, methodology changelog, tests, and source fingerprint in the same commit.

## Data/privacy

Never commit administrative microdata, student IDs, raw Google Forms exports, direct identifiers, HMAC keys, secrets, or row-level linked student records. Keep source data outside GitHub. Aggregated outputs must be reviewed for disclosure risk before commit.

SHA-256 is for integrity/version identity, not anonymisation. HMAC pseudonymisation is not anonymity.

## Current core definitions

- Classroom = instructor × course × academic period.
- Pass threshold = 7.5.
- Primary continuous outcome is classroom-relative performance.
- Non-numeric adverse outcomes BV/RT/BA are handled in the continuous analysis using within-classroom KDE based on observed numeric grades below 7.5; uniform fallback is used only when no sub-7.5 numeric grade exists in the classroom. Exact implementation details belong in the study protocol.
- CMAT visit count is student-selected. Threshold/piecewise analyses are descriptive, not regression discontinuity designs.
- Same-day multiple visits are administratively plausible and must not be labelled manipulation without evidence.

## Manuscript separation

Do not organise the technical discovery report around papers. The report should present all findings continuously, then propose publication splits at the end.

- Paper 1: first-year participation incentive / persistence of formal academic help-seeking.
- Paper 2: contemporaneous CMAT use / classroom-relative performance in MU.

## Git workflow

Prefer small descriptive commits. Use branches/PRs for substantive methodological changes when useful. Do not upload ZIP snapshots to GitHub as the primary source of truth.
