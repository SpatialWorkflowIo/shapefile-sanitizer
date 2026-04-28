# 🗺️ shapefile-sanitizer

> **Automatically fix broken shapefiles in seconds.** Repair encoding, projections, and geometry issues with a single command—no GIS experience required.

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Tests](https://img.shields.io/badge/tests-100%25%20coverage-brightgreen)](https://github.com/SpatialWorkflowIo/shapefile-sanitizer) [![PyPI](https://img.shields.io/badge/pypi-package-blueviolet)](https://pypi.org)

---

## 🎯 Why shapefile-sanitizer?

Shapefiles are ubiquitous in GIS workflows, but often arrive with common problems:

| Problem | Impact | Solution |
|---------|--------|----------|
| **Missing encoding metadata** (`.cpg`) | Character corruption, garbled text in non-ASCII regions | Auto-detect or set UTF-8 |
| **Missing projection** (`.prj`) | Data rendered in wrong location; analysis results invalid | Apply default WGS84 (EPSG:4326) or custom CRS |
| **Invalid geometries** | Processing fails in analysis tools; topology errors | Repair/validate with shapely + pyshp |

Instead of manually fixing each file in ArcGIS or QGIS, **run one command**:

```bash
shapefile-sanitizer broken.shp fixed.shp --overwrite
```

✅ **100% test coverage** | ✅ **Beginner-friendly** | ✅ **Scriptable for batch jobs** | ✅ **Open source**

---

## 📦 Installation

### Minimal (encoding + projection only)

```bash
pip install shapefile-sanitizer
```

### With geometry repair (recommended)

```bash
pip install shapefile-sanitizer[geometry]
```

### For development

```bash
git clone https://github.com/SpatialWorkflowIo/shapefile-sanitizer.git
cd shapefile-sanitizer
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

---

## 🚀 Quick Start

### Basic usage

```bash
shapefile-sanitizer input/roads.shp output/roads_clean.shp
```

### Overwrite existing files

```bash
shapefile-sanitizer roads.shp roads.shp --overwrite
```

### Batch process (with geometry repair)

```bash
for file in data/*.shp; do
  shapefile-sanitizer "$file" "output/$(basename $file)" --overwrite
done
```

---

## 📋 What It Does

The CLI performs these steps in order:

1. **📋 Validates input** — checks for required `.shp` + `.dbf`
2. **📁 Copies shapefile set** — transfers `.shp`, `.shx`, `.dbf`, `.prj`, `.cpg` to output
3. **🔤 Ensures encoding** — adds/normalizes `.cpg` (defaults to UTF-8)
4. **🧭 Ensures projection** — adds/normalizes `.prj` (defaults to EPSG:4326 / WGS84)
5. **✅ Repairs geometry** (optional) — validates and fixes invalid shapes (requires `[geometry]` extra)

### Example output

```bash
$ shapefile-sanitizer parcels.shp parcels_clean.shp --overwrite
Copied: parcels_clean.shp, parcels_clean.dbf
[encoding] changed - wrote UTF-8 to parcels_clean.cpg
[projection] changed - wrote default CRS EPSG:4326 to parcels_clean.prj
[geometry] skipped - optional dependencies missing (install: pip install shapefile-sanitizer[geometry])
Completed.
```

---

## 🔧 Use Cases

### 📊 Data Standardization Pipelines
Import shapefiles from multiple sources with inconsistent metadata into a unified GIS or data warehouse.

```bash
for source in vendor_*.shp; do
  shapefile-sanitizer "$source" "standardized/$(basename $source)" --overwrite
done
```

### 🌍 Publishing Open Data
Ensure public GIS datasets conform to best practices before release (UTF-8 encoding, explicit CRS).

### 🔬 Research Data Prep
Fix geometry and projection issues before running spatial analysis, reducing downstream errors.

### 🏗️ ETL Workflows
Integrate shapefile repair as a stage in data ingestion pipelines (Docker-friendly).

---

## 📖 Full Documentation

### Command-line Options

```bash
shapefile-sanitizer --help
```

```
usage: shapefile-sanitizer INPUT_SHP OUTPUT_SHP [--overwrite]

Fix common shapefile issues.

positional arguments:
  INPUT_SHP              Path to input .shp file
  OUTPUT_SHP             Path to output .shp file

optional arguments:
  --overwrite            Overwrite output if it already exists
  -h, --help             Show this help message and exit
```

### Environment & Requirements

- **Python**: 3.8+
- **Core dependencies**: pyshp (shapefile reading/writing)
- **Optional (geometry)**: shapely (geometry validation/repair)

---

## 🧪 Development

### Run tests

```bash
pytest
```

Enforces **100% code coverage** — all logic paths are tested.

### Add a new fix stage

1. Create `src/shapefile_sanitizer/stages/new_stage.py`
2. Implement `repair_new_thing(shapefile_path: str) -> StageResult`
3. Add to pipeline in `src/shapefile_sanitizer/pipeline.py`
4. Add tests to `tests/test_stages.py`
5. Update `README.md` docs

### Project structure

```
shapefile-sanitizer/
├── src/shapefile_sanitizer/
│   ├── cli.py              # CLI argument parsing + UX
│   ├── pipeline.py         # Stage orchestration
│   ├── models.py           # Shared contracts (StageResult, etc.)
│   └── stages/
│       ├── encoding.py     # .cpg handling
│       ├── projection.py   # .prj handling
│       └── geometry.py     # optional shape validation/repair
├── tests/                  # 100% coverage tests
├── README.md               # This file
└── pyproject.toml          # Package metadata
```

---

## 🐛 Troubleshooting

### "Required input file not found"

Ensure you're passing the full `.shp` file path, not just the stem. Required sidecars (`.shx`, `.dbf`) must also exist.

```bash
# ✅ Correct
shapefile-sanitizer data/roads.shp output/roads.shp

# ❌ Wrong
shapefile-sanitizer data/roads output/roads
```

### "Output file already exists"

Use `--overwrite` to replace:

```bash
shapefile-sanitizer roads.shp roads_fixed.shp --overwrite
```

### Geometry repair not working

Ensure `[geometry]` extras are installed:

```bash
pip install -e shapefile-sanitizer[geometry]
```

Verify with:

```bash
python -c "import shapely; print(shapely.__version__)"
```

---

## 🤝 Contributing

Found a bug or have a feature request? **Issues & PRs welcome!**

For major changes, please open an issue first to discuss proposed changes.

---

## 📄 License

This project is licensed under the **MIT License** — see `LICENSE` file for details.

---

## 🔗 Author & Resources

**Website**: [https://spatialworkflow.io/](https://spatialworkflow.io/)

**Repository**: [github.com/SpatialWorkflowIo/shapefile-sanitizer](https://github.com/SpatialWorkflowIo/shapefile-sanitizer)

Learn more about shapefiles:
- [ESRI Shapefile Technical Description](https://www.esri.com/content/dam/esrisites/sitecore/Home/Microsites/Product-Pages/shapefile/shapefile.pdf)
- [Unicode & Encoding in GIS](https://wikipedia.org/wiki/Character_encoding)
- [EPSG Registry - Coordinate Systems](https://epsg.io/)

