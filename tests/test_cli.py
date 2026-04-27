from __future__ import annotations

from pathlib import Path

from shapefile_sanitizer.cli import build_parser, main


def _write_minimal_set(base: Path) -> None:
    base.parent.mkdir(parents=True, exist_ok=True)
    base.write_bytes(b"fake-shp")
    base.with_suffix(".dbf").write_bytes(b"fake-dbf")


def test_build_parser_defaults() -> None:
    parser = build_parser()
    args = parser.parse_args(["in.shp", "out.shp"])
    assert args.default_encoding == "UTF-8"
    assert args.default_crs == "EPSG:4326"


def test_main_success(tmp_path: Path, capsys) -> None:
    input_base = tmp_path / "in.shp"
    output_base = tmp_path / "out.shp"
    _write_minimal_set(input_base)

    exit_code = main([str(input_base), str(output_base)])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Copied:" in output
    assert "[encoding]" in output
    assert "Completed." in output


def test_main_error_branch(capsys) -> None:
    exit_code = main(["does-not-exist.shp", "out.shp"])
    output = capsys.readouterr().out

    assert exit_code == 1
    assert output.startswith("Error:")

