# Reproducing CMAT research

CMAT Research supports Python 3.14. The installable scientific package is defined by `cmat_analysis/pyproject.toml`; the root `pyproject.toml` contains repository-level tooling configuration only.

## Pip setup

From the repository root:

```bash
python -m pip install -e './cmat_analysis[dev,docs]'
```

Verify the shared library with:

```bash
(cd cmat_analysis && pytest -q)
python cmat_analysis/scripts/generate_function_index.py
```

## Conda setup

From the repository root:

```bash
conda env create -f environment.yml
conda activate cmat-research
git lfs install
git lfs pull
```

The Conda environment delegates Python package installation to the same editable `cmat_analysis` package used by the pip workflow, so scientific dependency pins remain centralized in `cmat_analysis/pyproject.toml`.

## Data inputs

Raw administrative workbooks remain local even while the repository is private. Place them under:

```text
data/raw/
├── Materias estudiantes-profesores 2019-2025 P y O.xlsx
├── Asesorias2024.xlsx
└── pre_treatment_covariates.xlsx   # optional
```

`data/raw/` is ignored by Git except for its README. The shared configuration discovers the canonical workbooks automatically, and the shorter aliases `Materias.xlsx` and `Asesorias.xlsx` are also accepted.

The private repository may additionally contain the controlled pseudonymized research release:

```text
data/controlled/
├── Materias_pseudonymized.csv
├── Asesorias_pseudonymized.csv
├── PSEUDONYMIZATION_MANIFEST.json
├── SHA256SUMS.txt
└── PRIVACY_README.md
```

Raw local workbooks have priority when present; otherwise `get_study_config()` and the shared visit-analysis settings fall back automatically to the controlled pseudonymized CSVs. This permits the paper branches to reproduce analyses without committing direct institutional identifiers.

To regenerate the controlled release from authorized local source workbooks, use the same secret HMAC key stored outside the repository:

```bash
python cmat_analysis/src/create_anonymized_release.py \
  --key-file /secure/path/to/CMAT_PSEUDONYM_KEY.txt \
  --install-controlled
```

The generator preserves all substantive advisory research fields, including the exact timestamp, while replacing student identifiers and professor identifiers with deterministic HMAC-SHA256 pseudonyms. It never writes the secret key into the release. Advisory professor names currently use a separate `advisor_*` namespace because no verified crosswalk to numeric `CLAVEPROFESOR` is available.

The row-level controlled release is pseudonymized rather than anonymous and may remain in Git only while the repository is private and access-restricted. If repository visibility is ever changed to public, purge the controlled release from the full Git/LFS history, releases, caches, and workflow artifacts before changing visibility. See `docs/DATA_PRIVACY.md` and `docs/PSEUDONYMIZED_RELEASE.md`.

A temporary compatibility fallback still recognizes historical data locations directly under `data/`; new setups should use `data/raw/` or the documented controlled release.

## Git LFS and controlled data

Heavy research binaries use Git LFS; run `git lfs install` once and `git lfs pull` after cloning when assets are still pointers. Raw administrative workbooks, direct identifiers, credentials, secrets, and HMAC keys must never be committed. The only row-level data intended for repository versioning are the specifically documented pseudonymized files under `data/controlled/` while the repository remains private.

## Research runners

Brainstorm-local runners import the installed library, for example:

```bash
python brainstorm/methodology_report/code/methodology_report.py --check
```

On a `paper/*` branch, follow `PAPER_BRANCH.md`; paper-specific `code/` may orchestrate `cmat_analysis`, but reusable calculations must be validated upstream in the library first. Buildable paper branches use `python paper/build.py`, and the shared GitHub Actions paper workflow compiles manuscripts and exports source artifacts automatically.
