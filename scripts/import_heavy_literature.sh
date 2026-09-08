#!/usr/bin/env bash
set -euo pipefail

# Import the two private literature batches into the canonical CMAT repository.
# Usage:
#   ./scripts/import_heavy_literature.sh /path/to/Bib.zip /path/to/339dc703-470e-407c-bb54-97ab069e4ce7.zip
#
# Requirements:
#   git, git-lfs, unzip, sha256sum
#
# This script intentionally refuses to proceed if the source archives do not
# match the checksums recorded during the research workflow.

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 /path/to/Bib.zip /path/to/second-literature.zip" >&2
  exit 2
fi

BIB1="$1"
BIB2="$2"
EXPECTED1="84ef1c01a85db38ef6b5413621480eba1332f800dddc2523f098209e0745a237"
EXPECTED2="cfa14830138c970027a9bf730eab2e62b5bf84fe072ddb3c82c206a5c242478c"

actual1="$(sha256sum "$BIB1" | awk '{print $1}')"
actual2="$(sha256sum "$BIB2" | awk '{print $1}')"

if [[ "$actual1" != "$EXPECTED1" ]]; then
  echo "ERROR: Bib.zip checksum mismatch" >&2
  echo "expected: $EXPECTED1" >&2
  echo "actual:   $actual1" >&2
  exit 1
fi

if [[ "$actual2" != "$EXPECTED2" ]]; then
  echo "ERROR: second literature archive checksum mismatch" >&2
  echo "expected: $EXPECTED2" >&2
  echo "actual:   $actual2" >&2
  exit 1
fi

git lfs install
mkdir -p literature
rm -rf literature/Bib literature/Bib2
unzip -q "$BIB1" -d literature
unzip -q "$BIB2" -d literature

# Verify the expected imported directory names.
[[ -d literature/Bib ]] || { echo "ERROR: literature/Bib was not created" >&2; exit 1; }
[[ -d literature/Bib2 ]] || { echo "ERROR: literature/Bib2 was not created" >&2; exit 1; }

printf 'Bib1 PDFs: '; find literature/Bib/pdf -type f -name '*.pdf' | wc -l
printf 'Bib1 Markdown: '; find literature/Bib/extracted -type f -name '*.md' | wc -l
printf 'Bib1 assets: '; find literature/Bib/assets -type f | wc -l
printf 'Bib2 PDFs: '; find literature/Bib2/pdf -type f -name '*.pdf' | wc -l
printf 'Bib2 Markdown: '; find literature/Bib2/extracted -type f -name '*.md' | wc -l
printf 'Bib2 assets: '; find literature/Bib2/assets -type f | wc -l

git add .gitattributes literature/Bib literature/Bib2 docs/HEAVY_SNAPSHOT.md

echo
echo "Heavy literature staged successfully. Review with:"
echo "  git status"
echo "  git lfs ls-files"
echo
echo "Then commit/push, for example:"
echo "  git commit -m 'literature: import full private Docling corpus with LFS'"
echo "  git push origin main"
