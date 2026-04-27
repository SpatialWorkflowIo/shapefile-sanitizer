# shapefile-sanitizer

Fix common shapefile pain points with one command:
- missing encoding sidecar (`.cpg`)
- missing projection (`.prj`)
- invalid geometries (when optional geometry dependencies are installed)

This project is designed to be beginner-friendly and scriptable.

Author website: https://spatialworkflow.io/

## Quickstart

```bash
cd /home/martin/PycharmProjects/shapefile-sanitizer
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run on a shapefile:

```bash
shapefile-sanitizer /path/to/input/roads.shp /path/to/output/roads_clean.shp
```

If you also want geometry repair support:

```bash
pip install -e ".[dev,geometry]"
shapefile-sanitizer /path/to/input/roads.shp /path/to/output/roads_clean.shp
```

## What the CLI does

1. Copies the input shapefile set (`.shp`, `.shx`, `.dbf`, optional `.prj`, optional `.cpg`) to the output path.
2. Ensures an encoding file exists and defaults to `UTF-8`.
3. Ensures a projection file exists and defaults to `EPSG:4326` (WGS84).
4. Attempts geometry repair if optional geometry dependencies are installed.

## Example

```bash
shapefile-sanitizer ./examples/parcels.shp ./examples_out/parcels_fixed.shp --overwrite
```

Sample output:

```text
Copied: parcels_fixed.shp, parcels_fixed.dbf
[encoding] changed - wrote UTF-8 to parcels_fixed.cpg
[projection] changed - wrote default CRS EPSG:4326 to parcels_fixed.prj
[geometry] unchanged - optional dependencies missing (install extras: geometry)
Completed.
```

## Development

Run tests:

```bash
pytest
```

The test suite enforces 100% coverage for the current code in `src/shapefile_sanitizer/`.

