#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

START_BRANCH="$(git branch --show-current)"
OUTPUT_DIR="$(dirname "$ROOT")/CMAT-compiled-papers"

branches=(
  "paper/paper1-ppa-persistence"
  "paper/paper2-mu-performance"
  "paper/paper3-grading-heterogeneity"
)

names=(
  "paper1-ppa-persistence"
  "paper2-mu-performance"
  "paper3-grading-heterogeneity"
)

# Do not switch branches over local modifications.
if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: working tree is not clean."
  echo
  git status --short
  echo
  echo "Commit/stash the changes, or discard them with:"
  echo "  git reset --hard HEAD"
  echo "  git clean -fd"
  exit 1
fi

# Verify the active Python environment.
echo "Python:"
python --version

python - <<'PY'
import sys
if sys.version_info[:2] != (3, 14):
    raise SystemExit(
        f"ERROR: Python 3.14 is required; current version is {sys.version.split()[0]}"
    )
PY

# Verify LaTeX.
if command -v latexmk >/dev/null 2>&1; then
  echo "LaTeX: $(command -v latexmk)"
elif command -v pdflatex >/dev/null 2>&1 && command -v bibtex >/dev/null 2>&1; then
  echo "LaTeX: pdflatex + bibtex"
else
  echo "ERROR: LaTeX is not installed."
  echo "Install MacTeX/BasicTeX first."
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

restore_branch() {
  echo
  echo "Returning to $START_BRANCH..."
  git switch "$START_BRANCH" >/dev/null 2>&1 || true
}
trap restore_branch EXIT

git fetch origin --tags

for i in "${!branches[@]}"; do
  branch="${branches[$i]}"
  name="${names[$i]}"

  echo
  echo "============================================================"
  echo "Compiling $name"
  echo "Branch: $branch"
  echo "============================================================"

  git switch "$branch"

  # Make the local branch exactly match GitHub.
  git reset --hard "origin/$branch"

  git lfs pull

  # Reinstall the branch's current shared analysis library.
  python -m pip install -e "./cmat_analysis[dev]"

  # Compile figures + manuscript according to each paper's own builder.
  python paper/build.py

  if [[ ! -f paper/main.pdf ]]; then
    echo "ERROR: $branch did not produce paper/main.pdf"
    exit 1
  fi

  cp paper/main.pdf "$OUTPUT_DIR/${name}.pdf"

  echo "Saved:"
  echo "  $OUTPUT_DIR/${name}.pdf"
done

echo
echo "============================================================"
echo "All papers compiled successfully"
echo "============================================================"
echo
echo "PDFs:"
for name in "${names[@]}"; do
  echo "  $OUTPUT_DIR/${name}.pdf"
done