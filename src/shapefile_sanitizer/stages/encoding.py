from __future__ import annotations

from pathlib import Path

from shapefile_sanitizer.models import StageResult


def fix_encoding(shapefile_path: Path, encoding: str = "UTF-8") -> StageResult:
    """Ensure a .cpg file exists and contains the requested encoding."""

    cpg_path = shapefile_path.with_suffix(".cpg")
    if not cpg_path.exists():
        cpg_path.write_text(f"{encoding}\n", encoding="utf-8")
        return StageResult(
            name="encoding",
            changed=True,
            message=f"wrote {encoding} to {cpg_path.name}",
        )

    current_value = cpg_path.read_text(encoding="utf-8").strip()
    if current_value.upper() == encoding.upper():
        return StageResult(
            name="encoding",
            changed=False,
            message=f"{cpg_path.name} already set to {encoding}",
        )

    cpg_path.write_text(f"{encoding}\n", encoding="utf-8")
    return StageResult(
        name="encoding",
        changed=True,
        message=f"updated {cpg_path.name} from {current_value or 'empty'} to {encoding}",
    )

