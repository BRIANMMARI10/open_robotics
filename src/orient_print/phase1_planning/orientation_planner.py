"""Greedy orientation sequence planner (Phase 1 heuristic)."""

from __future__ import annotations

import numpy as np
import trimesh

from orient_print.models.orientation import OrientationSequence, OrientationStep, Pose
from orient_print.phase1_planning.deposition_analysis import (
    DepositionCandidate,
    analyze_deposition_candidates,
)


def _pose_for_deposition_direction(direction: np.ndarray) -> Pose:
    """
    Compute object pose that aligns deposition with build +Z.

    We rotate the part so that `direction` (in part frame) maps to +Z in build frame.
    """
    d = direction / np.linalg.norm(direction)
    target = np.array([0.0, 0.0, 1.0])

    if np.allclose(d, target):
        return Pose.identity()
    if np.allclose(d, -target):
        return Pose.from_euler_xyz_deg(180, 0, 0)

    axis = np.cross(d, target)
    axis_norm = np.linalg.norm(axis)
    if axis_norm < 1e-9:
        return Pose.identity()

    axis = axis / axis_norm
    angle = np.arccos(np.clip(float(d @ target), -1.0, 1.0))
    # Rodrigues rotation
    kx, ky, kz = axis
    k = np.array([[0, -kz, ky], [kz, 0, -kx], [-ky, kx, 0]])
    r = np.eye(3) + np.sin(angle) * k + (1 - np.cos(angle)) * (k @ k)
    return Pose(rotation=r)


def plan_orientation_sequence(
    mesh: trimesh.Trimesh,
    analysis_cfg: dict,
    planning_cfg: dict,
    part_name: str = "part",
) -> tuple[OrientationSequence, list[DepositionCandidate]]:
    """
    Greedy planner: pick best deposition direction, mark faces covered, repeat.

    This is a starting heuristic — replace with smarter graph search later.
    """
    candidates = analyze_deposition_candidates(mesh, analysis_cfg, planning_cfg)
    max_steps = int(planning_cfg.get("max_orientations", 6))
    overhang_threshold = float(analysis_cfg.get("overhang_angle_deg", 45.0))
    cos_limit = np.cos(np.radians(overhang_threshold))
    min_area = float(analysis_cfg.get("min_face_area_mm2", 1.0))

    normals = mesh.face_normals
    areas = mesh.area_faces
    significant = areas >= min_area
    total_significant_area = float(areas[significant].sum())

    covered = np.zeros(len(mesh.faces), dtype=bool)
    steps: list[OrientationStep] = []
    used_directions: list[np.ndarray] = []

    for step_idx in range(max_steps):
        best: DepositionCandidate | None = None
        best_new_area = 0.0

        for cand in candidates:
            if any(np.allclose(cand.direction, u) for u in used_directions):
                continue

            d = cand.direction
            cos_nd = normals @ d
            printable = (cos_nd >= cos_limit) & significant & ~covered
            new_area = float(areas[printable].sum())

            if new_area > best_new_area:
                best_new_area = new_area
                best = DepositionCandidate(
                    direction=d,
                    printable_face_count=int(printable.sum()),
                    printable_area_mm2=new_area,
                    printable_face_indices=np.where(printable)[0].tolist(),
                    score=new_area,
                )

        if best is None or best_new_area <= 0:
            break

        covered[best.printable_face_indices] = True
        used_directions.append(best.direction.copy())

        pose = _pose_for_deposition_direction(best.direction)
        steps.append(
            OrientationStep(
                index=step_idx,
                object_pose=pose,
                deposition_direction=best.direction.copy(),
                printable_face_indices=best.printable_face_indices,
                notes=f"covers {best.printable_area_mm2:.1f} mm²",
            )
        )

    covered_area = float(areas[covered & significant].sum())
    coverage = covered_area / total_significant_area if total_significant_area > 0 else 0.0

    seq = OrientationSequence(steps=steps, part_name=part_name)
    if steps:
        steps[-1].notes += f" | total coverage {100 * coverage:.0f}%"

    return seq, candidates
