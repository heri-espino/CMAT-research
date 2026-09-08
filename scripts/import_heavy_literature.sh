#!/usr/bin/env bash
set -euo pipefail

cat >&2 <<'EOF'
DEPRECATED: this script belonged to the historical Bib/Bib2 ingestion workflow.

The active repository uses:
  literature/library/
  literature/general/
  literature/papers/

Do not recreate literature/Bib or literature/Bib2.
See literature/AGENTS.md and literature/library/PROVENANCE.md.

Historical archive checksums remain documented in docs/HEAVY_SNAPSHOT.md.
EOF
exit 1
