from __future__ import annotations

from pathlib import Path


def read_variation() -> dict[str, str]:
    config_path = Path("experiment/variation.env")
    values: dict[str, str] = {}

    if not config_path.exists():
        return values

    for raw_line in config_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()

    return values

