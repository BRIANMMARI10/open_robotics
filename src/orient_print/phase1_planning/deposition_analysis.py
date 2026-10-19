"""Find candidate deposition directions for a mesh."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import trimesh

from orient_print.models.geometry import gravity_vector


@dataclass
class DepositionCandidate:
    """A candidate deposition direction and how much area it can print."""

    direction: np.ndarray  # unit vector: material extruded along this axis (build frame)
    printable_face_count: int
    printable_area_mm2: float
    printable_face_indices: list[int]
    score: float  # higher = better single-step coverage

    def __post_init__(self) -> None:
        d = np.asarray(self.direction, dtype=float)
        n = np.linalg.norm(d)
        self.direction = d / n if n > 0 else np.array([0.0, 0.0, 1.0])


def _normalize(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def analyze_deposition_candidates(
    mesh: trimesh.Trimesh,
    analysis_cfg: dict,
    planning_cfg: dict,
) -> list[DepositionCandidate]:
    """
    Score seed deposition directions by how much surface area is printable.

    A face is printable from direction d if its normal aligns with d
    (you can deposit onto the outward-facing side).
    """
    gravity = gravity_vector(analysis_cfg)
    min_area = float(analysis_cfg.get("min_face_area_mm2", 1.0))
    overhang_threshold = float(analysis_cfg.get("overhang_angle_deg", 45.0))
    cos_limit = np.cos(np.radians(overhang_threshold))

    seed_dirs = planning_cfg.get(
        "candidate_directions",
        [[0, 0, 1], [0, 0, -1], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]],
    )

    normals = mesh.face_normals
    areas = mesh.area_faces
    significant = areas >= min_area

    candidates: list[DepositionCandidate] = []

    for raw_dir in seed_dirs:
        d = _normalize(np.array(raw_dir, dtype=float))
        # Face printable if normal points roughly same way as deposition (top surface)
        cos_nd = normals @ d
        printable_mask = (cos_nd >= cos_limit) & significant
        indices = np.where(printable_mask)[0].tolist()
        printable_area = float(areas[printable_mask].sum())

        # Penalize directions that fight gravity (deposition against gravity)
        gravity_penalty = max(0.0, -float(d @ gravity))  # 0 if d points up
        score = printable_area * (1.0 - 0.5 * gravity_penalty)

        candidates.append(
            DepositionCandidate(
                direction=d,
                printable_face_count=len(indices),
                printable_area_mm2=printable_area,
                printable_face_indices=indices,
                score=score,
            )
        )

    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates
