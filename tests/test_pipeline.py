from __future__ import annotations

from pathlib import Path

import pytest

from shapefile_sanitizer.pipeline import copy_shapefile_set, sanitize


def _write_minimal_set(base: Path) -> None:
    base.parent.mkdir(parents=True, exist_ok=True)
    base.write_bytes(b"fake-shp")
    base.with_suffix(".dbf").write_bytes(b"fake-dbf")


def test_copy_shapefile_set_copies_known_files(tmp_path: Path) -> None:
    input_base = tmp_path / "in" / "roads.shp"
    output_base = tmp_path / "out" / "roads_clean.shp"
    _write_minimal_set(input_base)
    input_base.with_suffix(".shx").write_bytes(b"fake-shx")

    copied = copy_shapefile_set(input_base, output_base)

    assert copied == ["roads_clean.shp", "roads_clean.shx", "roads_clean.dbf"]
    assert output_base.read_bytes() == b"fake-shp"
    assert output_base.with_suffix(".dbf").read_bytes() == b"fake-dbf"


def test_copy_shapefile_set_rejects_non_shp_input(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        copy_shapefile_set(tmp_path / "in.geojson", tmp_path / "out.shp")


def test_copy_shapefile_set_rejects_non_shp_output(tmp_path: Path) -> None:
    input_base = tmp_path / "in.shp"
    _write_minimal_set(input_base)

    with pytest.raises(ValueError):
        copy_shapefile_set(input_base, tmp_path / "out.geojson")


def test_copy_shapefile_set_rejects_missing_required_component(tmp_path: Path) -> None:
    input_base = tmp_path / "in.shp"
    input_base.write_bytes(b"fake-shp")

    with pytest.raises(FileNotFoundError):
        copy_shapefile_set(input_base, tmp_path / "out.shp")


def test_copy_shapefile_set_rejects_existing_output_without_overwrite(tmp_path: Path) -> None:
    input_base = tmp_path / "in.shp"
    output_base = tmp_path / "out.shp"
    _write_minimal_set(input_base)
    _write_minimal_set(output_base)

    with pytest.raises(FileExistsError):
        copy_shapefile_set(input_base, output_base)


def test_sanitize_creates_prj_and_cpg(tmp_path: Path) -> None:
    input_base = tmp_path / "in.shp"
    output_base = tmp_path / "out.shp"
    _write_minimal_set(input_base)

    copied, results = sanitize(input_base, output_base, default_crs="EPSG:4326")

    assert copied == ["out.shp", "out.dbf"]
    assert output_base.with_suffix(".cpg").read_text(encoding="utf-8").strip() == "UTF-8"
    assert "WGS 84" in output_base.with_suffix(".prj").read_text(encoding="utf-8")
    assert [result.name for result in results] == ["encoding", "projection", "geometry"]

