"""Per-orientation toolpath generation (Week 3 — stub).

TODO:
- Slice mesh in deposition plane for each OrientationStep
- Generate perimeters + infill (NEPath or custom)
- Attach Toolpath objects to OrientationStep.toolpaths
"""

from __future__ import annotations

import trimesh

from orient_print.models.orientation import OrientationStep


def generate_toolpaths_for_step(
    mesh: trimesh.Trimesh,
    step: OrientationStep,
    layer_height_mm: float,
    line_width_mm: float,
) -> OrientationStep:
    """Placeholder — returns step unchanged until Week 3."""
    _ = (mesh, layer_height_mm, line_width_mm)
    return step
