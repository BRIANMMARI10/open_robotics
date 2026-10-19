"""Intermediate toolpath representation (not G-code)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import numpy as np


class SegmentType(str, Enum):
    EXTRUDE = "extrude"
    TRAVEL = "travel"


@dataclass
class ToolpathSegment:
    """A polyline segment with extrusion flag."""

    points: np.ndarray  # shape (N, 3)
    segment_type: SegmentType = SegmentType.EXTRUDE

    def __post_init__(self) -> None:
        self.points = np.asarray(self.points, dtype=float)
        if self.points.ndim != 2 or self.points.shape[1] != 3:
            raise ValueError("points must have shape (N, 3)")


@dataclass
class Toolpath:
    """Collection of segments for one feature (perimeter, infill, etc.)."""

    name: str
    segments: list[ToolpathSegment] = field(default_factory=list)

    @property
    def total_length_mm(self) -> float:
        total = 0.0
        for seg in self.segments:
            if len(seg.points) < 2:
                continue
            diffs = np.diff(seg.points, axis=0)
            total += float(np.linalg.norm(diffs, axis=1).sum())
        return total
