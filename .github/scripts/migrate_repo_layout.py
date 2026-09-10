from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path.cwd()
BASE_SHA = os.environ["GITHUB_SHA"]


def run(*args: str, cwd: Path | None = None) -> None:
    print("+", " ".join(args))
    subprocess.run(args, cwd=cwd or ROOT, check=True)


def write(path: str | Path, text: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")


def replace_text(root: Path, replacements: list[tuple[str, str]]) -> None:
    skip = {".pdf", ".png", ".jpg", ".jpeg", ".zip", ".xlsx", ".xls", ".pyc"}
    for p in root.rglob("*"):
        if not p.is_file() or ".git" in p.parts or p.suffix.lower() in skip:
            continue
        try:
            old = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new = old
        for a, b in replacements:
            new = new.replace(a, b)
        if new != old:
            p.write_text(new, encoding="utf-8")


def migrate_main() -> None:
    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")

    run("git", "mv", "code", "cmat_analysis")
    run("git", "mv", "cmat_analysis/src/visitas_analysis", "cmat_analysis/src/cmat_analysis")
    run("git", "mv", "cmat_analysis/.ai_handoff.md", "cmat_analysis/AI_HANDOFF.md")

    cfg = ROOT / "cmat_analysis/src/cmat_analysis/config"
    cfg.mkdir(parents=True, exist_ok=True)
    for name in ("__init__.py", "settings.py", "study_config.py"):
        run("git", "mv", f"cmat_analysis/config/{name}", f"cmat_analysis/src/cmat_analysis/config/{name}")
    (ROOT / "cmat_analysis/config").rmdir()

    run("git", "mv", "reports", "brainstorm")
    run("git", "mv", "analysis/shared", "brainstorm/shared")
    run("git", "mv", "analysis/README.md", "brainstorm/SHARED_OUTPUTS.md")
    (ROOT / "analysis").rmdir()

    run("git", "rm", "-r", "papers")
    for p in (
        ".github/workflows/compile-paper1.yml",
        ".github/workflows/generate-paper1-annotated-sources.yml",
    ):
        if Path(p).exists():
            run("git", "rm", "-f", p)

    replace_text(
        ROOT,
        [
            ("visitas_analysis", "cmat_analysis"),
            ("from config.", "from cmat_analysis.config."),
            ("import config.", "import cmat_analysis.config."),
            ("code/src/", "cmat_analysis/src/"),
            ("code/FUNCTION_INDEX.md", "cmat_analysis/FUNCTION_INDEX.md"),
            ("code/.ai_handoff.md", "cmat_analysis/AI_HANDOFF.md"),
            ("code/pyproject.toml", "cmat_analysis/pyproject.toml"),
            ("code/environment.yml", "cmat_analysis/environment.yml"),
            ("code/requirements.txt", "cmat_analysis/requirements.txt"),
            ("code/scripts/", "cmat_analysis/scripts/"),
            ("code/tests/", "cmat_analysis/tests/"),
            ("reports/", "brainstorm/"),
            ("analysis/shared/", "brainstorm/shared/"),
            (' / "reports"', ' / "brainstorm"'),
            (' / "code"', ' / "cmat_analysis"'),
        ],
    )

    write(
        "cmat_analysis/pyproject.toml",
        '''
[project]
name = "cmat-analysis"
version = "0.1.0"
description = "Reusable scientific analysis library for the CMAT research programme."
requires-python = ">=3.14,<3.15"
dependencies = [
    "pandas==3.0.3",
    "numpy==2.4.6",
    "matplotlib==3.10.9",
    "seaborn==0.13.2",
    "scipy==1.17.1",
    "scikit-learn==1.8.0",
    "statsmodels==0.14.6",
    "openpyxl==3.1.5",
]

[project.optional-dependencies]
dev = ["build", "pytest"]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
include = ["cmat_analysis*"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
''',
    )

    write(
        ".gitattributes",
        '''
# Heavy binary research assets use Git LFS.
literature/**/*.pdf filter=lfs diff=lfs merge=lfs -text
literature/**/*.png filter=lfs diff=lfs merge=lfs -text
literature/**/*.jpg filter=lfs diff=lfs merge=lfs -text
literature/**/*.jpeg filter=lfs diff=lfs merge=lfs -text
brainstorm/**/*.pdf filter=lfs diff=lfs merge=lfs -text
brainstorm/**/*.png filter=lfs diff=lfs merge=lfs -text
brainstorm/**/*.jpg filter=lfs diff=lfs merge=lfs -text
paper/**/*.pdf filter=lfs diff=lfs merge=lfs -text
paper/**/*.png filter=lfs diff=lfs merge=lfs -text
literature_selected/**/*.pdf filter=lfs diff=lfs merge=lfs -text
literature_selected/**/*.png filter=lfs diff=lfs merge=lfs -text
**/*.zip filter=lfs diff=lfs merge=lfs -text
''',
    )

    write(
        "README.md",
        '''
# CMAT research

`main` is the shared upstream research branch. It contains the scientific library, controlled-data contracts, shared literature, broad research brainstorming and programme documentation; publication-specific work lives on one long-lived branch per paper.

```text
CMAT-research/
├── cmat_analysis/   # installable reusable scientific library
├── data/            # controlled-data contracts; no raw microdata in Git
├── literature/      # shared physical/source literature library
├── brainstorm/      # broad analyses, diagnostics, nulls, sensitivities, ideas
└── docs/            # programme-wide documentation and provenance
```

Install the shared library with `python -m pip install -e ./cmat_analysis`. Reusable scientific logic belongs in `cmat_analysis/src/cmat_analysis/`; brainstorm and paper runners import it.

Publication branches:

- `paper/paper1-ppa-persistence`
- `paper/paper2-mu-performance`
- `paper/paper3-grading-heterogeneity`
- `paper/paper4-degree-help-seeking`
- `paper/paper5-longitudinal-trajectories`

Each paper branch adds `literature_selected/`, `code/`, `results/`, `paper/`, `submission/`, and `PAPER_BRANCH.md`. Branch-local `code/` chooses what to run for that publication; it must not duplicate reusable estimators or cohort logic from `cmat_analysis`.

Heavy research binaries remain in Git LFS. Install once with `git lfs install`; use `git lfs pull` when assets are still pointers.
''',
    )

    handoff = '''
# CMAT AI handoff

`main` is the upstream scientific branch and owns shared `cmat_analysis/`, `data/`, `literature/`, `brainstorm/`, and `docs/`. Publication-specific manuscript trees belong only on the five `paper/*` branches.

`cmat_analysis/` is an installable internal scientific library analogous to a project-specific scikit-learn. Install it with `python -m pip install -e ./cmat_analysis`; search `cmat_analysis/FUNCTION_INDEX.md` before adding functions. Reusable cohort definitions, transformations, estimators, tests, models, uncertainty calculations, imputation logic and plotting functions belong in `cmat_analysis/src/cmat_analysis/`.

`brainstorm/` preserves broad research development: exploratory questions, diagnostics, nulls, robustness checks, methodological reasoning and retained aggregate outputs. Brainstorm-local code is orchestration only and imports `cmat_analysis`.

A paper branch adds `literature_selected/`, branch-local `code/`, `results/`, `paper/`, and `submission/`. If paper work needs a reusable capability, implement and validate it on `main` in `cmat_analysis`, then bring `main` into the paper branch. Do not leave shared scientific improvements isolated in one publication branch.

The physical literature corpus stays under `literature/library/`; branch-specific source selection and annotations live under `literature_selected/`. Raw institutional microdata, identifiers, credentials and secrets must never be committed. Heavy PDFs/images remain in Git LFS.

Read `docs/RESEARCH_WORKFLOW.md`, `cmat_analysis/AI_HANDOFF.md`, `brainstorm/AI_HANDOFF.md`, and `PAPER_BRANCH.md` when present.
'''
    write("AI_HANDOFF.md", handoff)
    write("AGENTS.md", handoff)

    write(
        "cmat_analysis/README.md",
        '''
# cmat_analysis

`cmat_analysis` is the reusable scientific Python library for CMAT research, shared by `main` and every paper branch.

From the repository root:

```bash
python -m pip install -e ./cmat_analysis
```

Use normal imports such as `import cmat_analysis`. Source lives in `src/cmat_analysis/`, tests in `tests/`, and `FUNCTION_INDEX.md` is the searchable inventory that must be checked before implementing a new reusable function.
''',
    )
    write(
        "cmat_analysis/AI_HANDOFF.md",
        '''
# cmat_analysis AI handoff

This directory is the shared scientific library. Before writing reusable code, search `FUNCTION_INDEX.md` and inspect the nearest implementation. New cohort logic, outcomes, estimators, tests, models, confidence intervals, imputation rules and reusable plotting functions belong under `src/cmat_analysis/`, with tests and concise docstrings.

The package must remain installable with `python -m pip install -e ./cmat_analysis`; consumers should use normal `cmat_analysis...` imports rather than injecting repository paths into `sys.path`. Paper-specific execution order/specifications belong in the current paper branch's root `code/`; broad exploratory orchestration belongs in `brainstorm/<topic>/code/`.
''',
    )
    write(
        "brainstorm/README.md",
        '''
# Brainstorm

`brainstorm/` is the shared research-development layer and replaces the former `reports/` concept. It is where questions are explored broadly, diagnostics and nulls are retained, sensitivities are compared, and methodological reasoning is documented before evidence is selected into a paper.

A brainstorm may have a thin local `code/` runner, notes, tables, figures and provenance, but reusable calculations remain in `cmat_analysis`. `shared/` preserves cross-topic historical aggregate outputs and provenance.
''',
    )
    write(
        "brainstorm/AI_HANDOFF.md",
        '''
# Brainstorm AI handoff

Use brainstorms to test questions broadly and preserve nulls, diagnostics, alternative definitions and sensitivities. Workflow: record the question -> search `cmat_analysis/FUNCTION_INDEX.md` -> add missing reusable capability to `cmat_analysis` with tests -> call it from the brainstorm -> inspect evidence -> select validated results into a paper branch.

A brainstorm-local runner may choose inputs/configuration and execution order, but it must not implement a second scientific library.
''',
    )

    write(
        "docs/RESEARCH_WORKFLOW.md",
        '''
# CMAT research workflow

## Shared upstream

`main` contains `cmat_analysis/`, `data/`, `literature/`, `brainstorm/`, and `docs/`. `cmat_analysis` is the internal reusable library and should be installed editable with `python -m pip install -e ./cmat_analysis`. `brainstorm` is the broad empirical-development layer that retains exploratory work, nulls, diagnostics and sensitivities.

## Publication branches

Each paper has a long-lived branch inheriting `main` and adding:

```text
literature_selected/   paper-specific source selection and annotations
code/                  thin paper-specific analysis orchestration
results/               generated/selected paper outputs
paper/                 manuscript and build material
submission/            journal-specific material
PAPER_BRANCH.md         branch contract
```

Branch-local `code/` specifies which shared functions and specifications answer the paper's question; `cmat_analysis` defines how calculations work. If a paper exposes a missing reusable function, fix and test it on `main/cmat_analysis`, then merge/rebase `main` into the paper branch and rerun.

`literature/` is the shared physical/source corpus; `literature_selected/` exists only on paper branches and contains the working subset, reading notes and annotated Markdown derivatives.
''',
    )
    write(
        "docs/GIT_WORKFLOW.md",
        '''
# Git workflow

`main` is the shared upstream research branch. The long-lived publication branches are `paper/paper1-ppa-persistence`, `paper/paper2-mu-performance`, `paper/paper3-grading-heterogeneity`, `paper/paper4-degree-help-seeking`, and `paper/paper5-longitudinal-trajectories`.

Shared library, data-contract, literature, brainstorm and programme-documentation changes should land on `main`, then be merged/rebased into active paper branches. Paper-specific `literature_selected/`, `code/`, `results/`, `paper/` and `submission/` changes remain on that paper branch.

Do not merge a paper branch wholesale back into `main`, because that would reintroduce publication-specific trees. Promote genuinely shared changes upstream as focused commits or cherry-picks.
''',
    )
    write(
        "docs/PUBLICATION_PORTFOLIO.md",
        '''
# Publication portfolio

| Paper | Branch | Primary focus |
|---|---|---|
| Paper 1 | `paper/paper1-ppa-persistence` | PPA-linked CMAT use and later help-seeking persistence |
| Paper 2 | `paper/paper2-mu-performance` | MU support use and classroom-relative performance |
| Paper 3 | `paper/paper3-grading-heterogeneity` | grading/classroom heterogeneity and standardisation |
| Paper 4 | `paper/paper4-degree-help-seeking` | degree programme and formal help-seeking |
| Paper 5 | `paper/paper5-longitudinal-trajectories` | longer-run support-use and academic trajectories |

Shared computation belongs to `main/cmat_analysis`; broad evidence development belongs to `main/brainstorm`; each publication branch owns its selected literature, paper-specific recipe, results and manuscript.
''',
    )
    write(
        "REPRODUCING.md",
        '''
# Reproducing CMAT research

Use Python 3.14 and install the shared library from the repository root:

```bash
python -m pip install -e './cmat_analysis[dev]'
```

Verify it with `(cd cmat_analysis && pytest -q)` and regenerate the function inventory with `python cmat_analysis/scripts/generate_function_index.py`.

Heavy binaries use Git LFS: run `git lfs install` once and `git lfs pull` after cloning when necessary.

Brainstorm-local runners import the installed library, for example `python brainstorm/methodology_report/code/methodology_report.py --check`. On a `paper/*` branch, follow `PAPER_BRANCH.md`; paper-specific `code/` may orchestrate `cmat_analysis`, but reusable calculations must be validated upstream in the library first.
''',
    )

    write(
        "brainstorm/methodology_report/code/methodology_report.py",
        '''
"""Thin entry point for the methodology brainstorm."""
from pathlib import Path
from cmat_analysis.reporting.methodology_build import methodology_report_cli

REPORT_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]

if __name__ == "__main__":
    raise SystemExit(methodology_report_cli(REPO_ROOT, REPORT_DIR))
''',
    )

    gen = ROOT / "cmat_analysis/scripts/generate_function_index.py"
    gen.write_text(
        gen.read_text(encoding="utf-8")
        .replace("src/visitas_analysis/", "src/cmat_analysis/")
        .replace("Canonical search index for `code/`", "Canonical search index for `cmat_analysis/`"),
        encoding="utf-8",
    )

    # Remove one-shot migration infrastructure from the resulting canonical tree.
    for p in (
        ".github/workflows/migrate-to-paper-branches.yml",
        ".github/workflows/migrate-to-paper-branches-v2.yml",
        ".github/scripts/migrate_repo_layout.py",
    ):
        Path(p).unlink(missing_ok=True)


def validate_main() -> None:
    run("python", "-m", "pip", "install", "--upgrade", "pip")
    run("python", "-m", "pip", "install", "-e", "./cmat_analysis[dev]")
    run("python", "-c", "import cmat_analysis; from cmat_analysis.config.study_config import get_study_config; print('editable import OK')")
    run("pytest", "-q", cwd=ROOT / "cmat_analysis")
    run("python", "cmat_analysis/scripts/generate_function_index.py")
    run("python", "brainstorm/methodology_report/code/methodology_report.py", "--check")
    run("git", "diff", "--check")


def branch_replace(old_slug: str) -> None:
    replace_text(
        ROOT / "literature_selected",
        [
            ("reports/", "brainstorm/"),
            ("analysis/shared/", "brainstorm/shared/"),
            (f"papers/{old_slug}/literature/", "literature_selected/"),
            ("../../../literature/library/", "../literature/library/"),
            ("../../literature/library/", "../literature/library/"),
        ],
    )
    replace_text(
        ROOT / "paper",
        [
            ("reports/", "brainstorm/"),
            ("analysis/shared/", "brainstorm/shared/"),
            (f"papers/{old_slug}/literature/", "literature_selected/"),
            (f"papers/{old_slug}/manuscript/", "paper/"),
        ],
    )


def make_branch(branch: str, old_slug: str, label: str, main_sha: str) -> None:
    run("git", "checkout", "-B", branch, main_sha)
    run("git", "checkout", BASE_SHA, "--", f"papers/{old_slug}")

    for d in ("literature_selected", "code", "results", "paper", "submission"):
        Path(d).mkdir(exist_ok=True)

    old = ROOT / "papers" / old_slug
    if (old / "literature").exists():
        shutil.rmtree(ROOT / "literature_selected")
        run("git", "mv", f"papers/{old_slug}/literature", "literature_selected")
    if (old / "manuscript").exists():
        shutil.rmtree(ROOT / "paper")
        run("git", "mv", f"papers/{old_slug}/manuscript", "paper")
    if (old / "README.md").exists():
        run("git", "mv", f"papers/{old_slug}/README.md", "paper/PROJECT_CONTEXT.md")
    shutil.rmtree(old, ignore_errors=True)
    shutil.rmtree(ROOT / "papers", ignore_errors=True)

    branch_replace(old_slug)

    write(
        "PAPER_BRANCH.md",
        f'''
# {label} branch

This is the canonical publication workspace for {label}. It inherits shared infrastructure from `main` and owns only publication-specific selection and production.

- `literature_selected/`: selected literature, reading notes and annotated source Markdown;
- `code/`: paper-specific orchestration importing `cmat_analysis`;
- `results/`: generated/selected paper outputs;
- `paper/`: manuscript/build material;
- `submission/`: journal-specific material.

Reusable scientific logic must be implemented and tested on `main` under `cmat_analysis/src/cmat_analysis/`, then brought into this branch. Do not maintain a divergent copy of shared functions here.
''',
    )
    write(
        "code/README.md",
        '''
# Paper-specific code

This directory owns only the recipe for this publication: specification choices, execution order, paper-specific outputs and calls into the installed `cmat_analysis` library. Do not implement reusable estimators, cohorts, tests, transformations or plotting primitives here.
''',
    )
    write(
        "results/README.md",
        '''
# Paper results

Generated or deliberately selected outputs used by this publication belong here. Preserve provenance to the branch-local recipe and shared `cmat_analysis` functions; do not hand-edit numerical results.
''',
    )
    if not (ROOT / "paper/README.md").exists():
        write("paper/README.md", "# Paper\n\nPublication manuscript and build assets belong here. `PROJECT_CONTEXT.md`, when present, preserves the pre-branch planning record.")
    write(
        "submission/README.md",
        "# Submission\n\nJournal-specific cover letters, anonymised variants, checklists and submission exports belong here when created.",
    )

    if old_slug == "paper1_ppa_persistence":
        main = ROOT / "paper/main.tex"
        text = main.read_text(encoding="utf-8")
        text = text.replace("../../../reports/methodology_report/", "../brainstorm/methodology_report/")
        text = text.replace("../../../brainstorm/methodology_report/", "../brainstorm/methodology_report/")
        main.write_text(text, encoding="utf-8")

        build = ROOT / "paper/build.py"
        if build.exists():
            text = build.read_text(encoding="utf-8")
            text = text.replace("REPO_ROOT = MANUSCRIPT_DIR.parents[2]", "REPO_ROOT = MANUSCRIPT_DIR.parent")
            text = text.replace('/ "reports"', '/ "brainstorm"')
            build.write_text(text, encoding="utf-8")

        gen = ROOT / "literature_selected/notes_on_papers/_generate.py"
        if gen.exists():
            text = gen.read_text(encoding="utf-8")
            text = text.replace("ROOT = Path(__file__).resolve().parents[4]", "ROOT = Path(__file__).resolve().parents[2]")
            text = text.replace('ROOT / "papers" / "paper1_ppa_persistence" / "literature" / "reading_notes"', 'ROOT / "literature_selected" / "reading_notes"')
            gen.write_text(text, encoding="utf-8")

        write(
            ".github/workflows/compile-paper.yml",
            '''
name: Compile Paper 1
on:
  push:
    branches: ['paper/paper1-ppa-persistence']
    paths: ['paper/**', 'brainstorm/methodology_report/figures/refined_longitudinal_persistence_3241.png', '.github/workflows/compile-paper.yml']
  workflow_dispatch:
permissions:
  contents: read
jobs:
  compile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true
      - name: Install LaTeX
        run: |
          sudo apt-get update
          sudo apt-get install -y latexmk texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended
      - name: Compile
        working-directory: paper
        run: latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
''',
        )

    run("git", "add", "-A")
    run("git", "diff", "--cached", "--check")
    run("git", "commit", "-m", f"refactor: establish {label} publication workspace")
    run("git", "push", "-u", "origin", branch)


def main() -> None:
    migrate_main()
    validate_main()
    run("git", "add", "-A")
    run("git", "commit", "-m", "refactor: establish shared cmat_analysis and brainstorm main")
    run("git", "push", "origin", "HEAD:main")
    main_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()

    specs = [
        ("paper/paper1-ppa-persistence", "paper1_ppa_persistence", "Paper 1 — PPA persistence"),
        ("paper/paper2-mu-performance", "paper2_mu_performance", "Paper 2 — MU performance"),
        ("paper/paper3-grading-heterogeneity", "paper3_grading_heterogeneity", "Paper 3 — grading heterogeneity"),
        ("paper/paper4-degree-help-seeking", "paper4_degree_help_seeking", "Paper 4 — degree help-seeking"),
        ("paper/paper5-longitudinal-trajectories", "paper5_longitudinal_trajectories", "Paper 5 — longitudinal trajectories"),
    ]
    for spec in specs:
        make_branch(*spec, main_sha)
    run("git", "checkout", "main")


if __name__ == "__main__":
    main()
