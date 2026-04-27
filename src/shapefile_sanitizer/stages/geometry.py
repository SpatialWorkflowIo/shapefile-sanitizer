from __future__ import annotations

from pathlib import Path

from shapefile_sanitizer.models import StageResult


def repair_geometry(shapefile_path: Path) -> StageResult:
    """Attempt geometry repair if optional dependencies are installed.

    Current behavior is intentionally conservative: if optional dependencies are
    not installed, the stage reports a warning and leaves data unchanged.
    """

    del shapefile_path

    try:
        import shapefile  # noqa: F401
        import shapely  # noqa: F401
    except ImportError:
        return StageResult(
            name="geometry",
            changed=False,
            message="optional dependencies missing (install extras: geometry)",
            warnings=("geometry repair skipped",),
        )

    return StageResult(
        name="geometry",
        changed=False,
        message="geometry backend available; no automatic repairs applied",
        warnings=("manual review recommended for invalid geometry cases",),
    )

