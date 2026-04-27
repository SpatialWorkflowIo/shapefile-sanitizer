from __future__ import annotations

import argparse
from pathlib import Path

from shapefile_sanitizer.pipeline import sanitize


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shapefile-sanitizer",
        description="Fix common shapefile issues (encoding, projection, geometry).",
    )
    parser.add_argument("input_shp", type=Path, help="Path to input .shp file")
    parser.add_argument("output_shp", type=Path, help="Path to output .shp file")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacing output files if they already exist",
    )
    parser.add_argument(
        "--default-encoding",
        default="UTF-8",
        help="Encoding written into .cpg when missing or mismatched",
    )
    parser.add_argument(
        "--default-crs",
        default="EPSG:4326",
        help="CRS to write into .prj when it is missing",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        copied, results = sanitize(
            args.input_shp,
            args.output_shp,
            overwrite=args.overwrite,
            default_encoding=args.default_encoding,
            default_crs=args.default_crs,
        )
    except (ValueError, FileNotFoundError, FileExistsError) as exc:
        print(f"Error: {exc}")
        return 1

    print(f"Copied: {', '.join(copied)}")
    for result in results:
        status = "changed" if result.changed else "unchanged"
        print(f"[{result.name}] {status} - {result.message}")
        for warning in result.warnings:
            print(f"  warning: {warning}")

    print("Completed.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

