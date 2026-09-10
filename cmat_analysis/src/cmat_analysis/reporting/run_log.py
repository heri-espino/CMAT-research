from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def _file_info(path: Path) -> dict[str, object]:
    resolved = path.resolve()
    if not resolved.exists():
        return {
            "path": str(resolved),
            "exists": False,
        }
    stat = resolved.stat()
    return {
        "path": str(resolved),
        "exists": True,
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(
            stat.st_mtime,
            tz=ZoneInfo("America/Mexico_City"),
        ).isoformat(timespec="seconds"),
    }


def write_run_log(
    *,
    logs_dir: Path,
    materias_path: Path,
    asesorias_path: Path,
    mode: str,
    status: str,
    details: dict[str, object] | None = None,
) -> Path:
    logs_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(ZoneInfo("America/Mexico_City"))
    payload = {
        "run_started_at": now.isoformat(timespec="seconds"),
        "timezone": "America/Mexico_City",
        "mode": mode,
        "status": status,
        "input_files": {
            "materias": _file_info(materias_path),
            "asesorias": _file_info(asesorias_path),
        },
        "details": details or {},
    }
    latest_path = logs_dir / "latest_run.json"
    timestamped_path = logs_dir / f"run_{now.strftime('%Y%m%d_%H%M%S')}.json"
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    latest_path.write_text(text + "\n", encoding="utf-8")
    timestamped_path.write_text(text + "\n", encoding="utf-8")
    return latest_path
