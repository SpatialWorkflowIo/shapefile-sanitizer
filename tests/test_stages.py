from __future__ import annotations

import sys
from pathlib import Path

from shapefile_sanitizer.stages.encoding import fix_encoding
from shapefile_sanitizer.stages.geometry import repair_geometry
from shapefile_sanitizer.stages.projection import _projection_text, ensure_projection


def test_fix_encoding_create_then_no_change_then_update(tmp_path: Path) -> None:
    shp = tmp_path / "roads.shp"
    shp.write_bytes(b"x")

    created = fix_encoding(shp)
    same = fix_encoding(shp)
    shp.with_suffix(".cpg").write_text("latin1\n", encoding="utf-8")
    updated = fix_encoding(shp)

    assert created.changed is True
    assert same.changed is False
    assert updated.changed is True
    assert "latin1" in updated.message


def test_projection_text_non_default() -> None:
    assert _projection_text("EPSG:3857") == "# CRS: EPSG:3857"


def test_ensure_projection_existing_nonempty_and_write_when_empty(tmp_path: Path) -> None:
    shp = tmp_path / "roads.shp"
    shp.write_bytes(b"x")

    written = ensure_projection(shp, default_crs="EPSG:3857")
    assert written.changed is True
    assert "EPSG:3857" in shp.with_suffix(".prj").read_text(encoding="utf-8")

    unchanged = ensure_projection(shp)
    assert unchanged.changed is False

    shp.with_suffix(".prj").write_text("\n", encoding="utf-8")
    rewritten = ensure_projection(shp)
    assert rewritten.changed is True


def test_repair_geometry_dependency_paths(tmp_path: Path, monkeypatch) -> None:
    shp = tmp_path / "roads.shp"
    shp.write_bytes(b"x")

    missing = repair_geometry(shp)
    assert missing.changed is False
    assert "missing" in missing.message

    monkeypatch.setitem(sys.modules, "shapefile", object())
    monkeypatch.setitem(sys.modules, "shapely", object())
    available = repair_geometry(shp)
    assert available.changed is False
    assert "backend available" in available.message

