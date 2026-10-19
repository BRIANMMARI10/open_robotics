"""Basic collision checks (stubs — expand in Week 3)."""

from __future__ import annotations

import trimesh

from orient_print.models.orientation import OrientationStep


def check_step_collision(
    mesh: trimesh.Trimesh,
    step: OrientationStep,
    simulation_cfg: dict,
) -> bool:
    """
    Placeholder collision check.

    TODO Week 3:
    - Transform mesh by step.object_pose
    - Model nozzle geometry along deposition axis
    - Check interference with already-deposited volume
    """
    _ = (mesh, step, simulation_cfg)
    return True
