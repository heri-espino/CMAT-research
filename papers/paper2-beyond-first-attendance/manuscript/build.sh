#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export TEXINPUTS=".:ima-authoring-template//:${TEXINPUTS:-}"
mkdir -p build
if command -v bibtex >/dev/null; then latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex; else latexmk -e '$bibtex = "bibtex8 %O %S";' -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex; fi
cp build/main.pdf paper.pdf
