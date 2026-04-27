from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class StageResult:
    """Result returned by each pipeline stage."""

    name: str
    changed: bool
    message: str
    warnings: tuple[str, ...] = field(default_factory=tuple)

