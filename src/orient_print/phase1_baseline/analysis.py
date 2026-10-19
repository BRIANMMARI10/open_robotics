"""Conventional FDM baseline analysis (overhangs, printable area)."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import trimesh

from orient_print.models.geometry import gravity_vector


@dataclass
class BaselineReport:
    """Results from baseline geometry analysis."""

    overhang_angle_threshold_deg: float
    total_faces: int
    overhang_face_count: int
    overhang_area_mm2: float
    total_area_mm2: float
    overhang_face_indices: list[int] = field(default_factory=list)
    face_normals: np.ndarray = field(default_factory=lambda: np.empty((0, 3)))

    @property
    def overhang_area_fraction(self) -> float:
        if self.total_area_mm2 <= 0:
            return 0.0
        return self.overhang_area_mm2 / self.total_area_mm2

    @property
    def support_burden_estimate(self) -> str:
        frac = self.overhang_area_fraction
        if frac < 0.05:
            return "low"
        if frac < 0.20:
            return "moderate"
        return "high"

    def summary_lines(self) -> list[str]:
        return [
            f"Faces: {self.total_faces}",
            f"Overhang faces (>{self.overhang_angle_threshold_deg:.0f}°): "
            f"{self.overhang_face_count} ({100 * self.overhang_area_fraction:.1f}% area)",
            f"Estimated support burden: {self.support_burden_estimate}",
        ]


def analyze_baseline(mesh: trimesh.Trimesh, analysis_cfg: dict) -> BaselineReport:
    """
    Estimate which faces would need support in conventional +Z printing.

    A face normal pointing downward (against gravity) beyond the threshold
    is treated as an overhang requiring support.
    """
    gravity = gravity_vector(analysis_cfg)
    up = -gravity  # deposition comes from above relative to gravity

    threshold_deg = float(analysis_cfg.get("overhang_angle_deg", 45.0))
    min_area = float(analysis_cfg.get("min_face_area_mm2", 1.0))
    cos_limit = np.cos(np.radians(threshold_deg))

    normals = mesh.face_normals.copy()
    areas = mesh.area_faces.copy()
    total_area = float(areas.sum())

    # Angle between face normal and up direction; overhang if normal tilts away from up
    cos_to_up = normals @ up
    is_overhang = cos_to_up < cos_limit
    is_significant = areas >= min_area
    overhang_mask = is_overhang & is_significant

    overhang_indices = np.where(overhang_mask)[0].tolist()
    overhang_area = float(areas[overhang_mask].sum())

    return BaselineReport(
        overhang_angle_threshold_deg=threshold_deg,
        total_faces=len(mesh.faces),
        overhang_face_count=int(overhang_mask.sum()),
        overhang_area_mm2=overhang_area,
        total_area_mm2=total_area,
        overhang_face_indices=overhang_indices,
        face_normals=normals,
    )
