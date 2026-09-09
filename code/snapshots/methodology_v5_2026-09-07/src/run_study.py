from __future__ import annotations

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_ROOT.parent
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.study_config import get_study_config
from visitas_analysis.study import run_study_pipeline


def main() -> int:
    config = get_study_config(PROJECT_ROOT)
    result = run_study_pipeline(config)
    print("[OK] Publication-oriented CMAT study completed.")
    print(f"Outputs: {result['output_dir']}")
    print(f"Primary MU cohort: {result['primary_n']}")
    print(f"Longitudinal MU→Cálculo with visit coverage: {result['longitudinal_n']}")
    print(f"Summary: {result['summary_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
