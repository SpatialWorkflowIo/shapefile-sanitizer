from __future__ import annotations

from pathlib import Path

from shapefile_sanitizer.models import StageResult

WGS84_WKT = (
    'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],'
    'PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
)


def _projection_text(default_crs: str) -> str:
    normalized = default_crs.strip().upper()
    if normalized in {"EPSG:4326", "WGS84", "WGS 84"}:
        return WGS84_WKT
    return f"# CRS: {default_crs.strip()}"


def ensure_projection(shapefile_path: Path, default_crs: str = "EPSG:4326") -> StageResult:
    """Ensure a .prj file exists and has non-empty content."""

    prj_path = shapefile_path.with_suffix(".prj")
    projection_text = _projection_text(default_crs)

    if prj_path.exists() and prj_path.read_text(encoding="utf-8").strip():
        return StageResult(
            name="projection",
            changed=False,
            message=f"{prj_path.name} already present",
        )

    prj_path.write_text(f"{projection_text}\n", encoding="utf-8")
    return StageResult(
        name="projection",
        changed=True,
        message=f"wrote default CRS {default_crs} to {prj_path.name}",
    )

