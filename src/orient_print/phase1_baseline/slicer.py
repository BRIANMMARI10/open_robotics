"""Placeholder for conventional slice baseline (G-code export later).

For Week 1, we analyze geometry only. Future: integrate external slicer CLI
(PrusaSlicer, CuraEngine) or Python slicer for G-code baseline comparison.
"""

from __future__ import annotations

from pathlib import Path

import trimesh


def export_slice_preview_mesh(
    mesh: trimesh.Trimesh,
    layer_height_mm: float,
    output_path: Path,
    max_layers: int = 20,
) -> list[float]:
    """
    Slice mesh at regular Z intervals and save a combined preview mesh.

    Returns list of Z heights sliced. Useful for visual sanity check before
    full slicer integration.
    """
    z_min, z_max = mesh.bounds[:, 2]
    zs = []
    sections = []

    z = z_min + layer_height_mm / 2
    count = 0
    while z < z_max and count < max_layers:
        section = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        if section is not None:
            path_3d = section.to_3D()
            if path_3d is not None and len(path_3d.entities) > 0:
                sections.append(path_3d)
                zs.append(z)
        z += layer_height_mm
        count += 1

    if sections:
        combined = trimesh.util.concatenate(sections)
        combined.export(output_path)

    return zs
