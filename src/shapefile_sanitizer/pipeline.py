from __future__ import annotations

import shutil
from pathlib import Path

from shapefile_sanitizer.models import StageResult
from shapefile_sanitizer.stages.encoding import fix_encoding
from shapefile_sanitizer.stages.geometry import repair_geometry
from shapefile_sanitizer.stages.projection import ensure_projection

_REQUIRED_EXTENSIONS = (".shp", ".dbf")
_KNOWN_EXTENSIONS = (".shp", ".shx", ".dbf", ".prj", ".cpg")


def _validate_input(input_shp: Path) -> None:
    if input_shp.suffix.lower() != ".shp":
        raise ValueError(f"Input must be a .shp file, got: {input_shp}")
    if not input_shp.exists():
        raise FileNotFoundError(f"Input shapefile not found: {input_shp}")

    for extension in _REQUIRED_EXTENSIONS:
        if not input_shp.with_suffix(extension).exists():
            raise FileNotFoundError(
                f"Missing required shapefile component: {input_shp.with_suffix(extension)}"
            )


def _validate_output(output_shp: Path, overwrite: bool) -> None:
    if output_shp.suffix.lower() != ".shp":
        raise ValueError(f"Output must be a .shp file, got: {output_shp}")

    if output_shp.exists() and not overwrite:
        raise FileExistsError(
            f"Output exists: {output_shp}. Use --overwrite to replace it."
        )


def copy_shapefile_set(input_shp: Path, output_shp: Path, overwrite: bool = False) -> list[str]:
    """Copy known shapefile sidecars from input base name to output base name."""

    _validate_input(input_shp)
    _validate_output(output_shp, overwrite)

    output_shp.parent.mkdir(parents=True, exist_ok=True)

    copied_files: list[str] = []
    for extension in _KNOWN_EXTENSIONS:
        source = input_shp.with_suffix(extension)
        if not source.exists():
            continue
        target = output_shp.with_suffix(extension)
        shutil.copy2(source, target)
        copied_files.append(target.name)

    return copied_files


def sanitize(
    input_shp: Path,
    output_shp: Path,
    *,
    overwrite: bool = False,
    default_encoding: str = "UTF-8",
    default_crs: str = "EPSG:4326",
) -> tuple[list[str], list[StageResult]]:
    """Run the full pipeline against a copied output shapefile set."""

    copied = copy_shapefile_set(input_shp, output_shp, overwrite=overwrite)

    results = [
        fix_encoding(output_shp, encoding=default_encoding),
        ensure_projection(output_shp, default_crs=default_crs),
        repair_geometry(output_shp),
    ]
    return copied, results

