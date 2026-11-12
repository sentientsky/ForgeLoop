from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

MAX_READY_ITEMS = 100
MAX_OUTPUT_BYTES = 500_000
BEADS_TIMEOUT_SECONDS = 10


def beads_ready(root: Path, limit: int = 20) -> dict[str, Any]:
    """Read ready Beads tasks without claiming, installing, or syncing anything."""
    if not 1 <= limit <= MAX_READY_ITEMS:
        raise ValueError(f"Beads result limit must be between 1 and {MAX_READY_ITEMS}")
    executable = shutil.which("bd")
    if not executable:
        raise FileNotFoundError("Beads CLI 'bd' is not installed or not on PATH; ForgeLoop will not install it")
    try:
        result = subprocess.run(
            [executable, "ready", "--json", "--brief", "--limit", str(limit)],
            cwd=root.resolve(),
            capture_output=True,
            text=True,
            timeout=BEADS_TIMEOUT_SECONDS,
            check=False,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("Beads read-only query timed out") from exc
    if result.returncode:
        raise RuntimeError(f"Beads read-only query failed with exit code {result.returncode}")
    encoded = result.stdout.encode("utf-8")
    if len(encoded) > MAX_OUTPUT_BYTES:
        raise ValueError("Beads response exceeded the output-size limit")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("Beads returned invalid JSON") from exc
    if not isinstance(payload, (list, dict)):
        raise TypeError("Beads response must be a JSON object or array")
    return {"source": "beads", "mode": "read-only", "limit": limit, "items": payload}
