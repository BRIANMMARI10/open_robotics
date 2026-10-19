"""Orientation sequence data structures."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from orient_print.models.toolpath import Toolpath


@dataclass
class Pose:
    """Rigid transform: rotation matrix R (3x3) + translation t (3,)."""

    rotation: np.ndarray
    translation: np.ndarray = field(default_factory=lambda: np.zeros(3))

    def __post_init__(self) -> None:
        self.rotation = np.asarray(self.rotation, dtype=float).reshape(3, 3)
        self.translation = np.asarray(self.translation, dtype=float).reshape(3)

    @classmethod
    def identity(cls) -> Pose:
        return cls(rotation=np.eye(3), translation=np.zeros(3))

    @classmethod
    def from_euler_xyz_deg(cls, rx: float, ry: float, rz: float, t: np.ndarray | None = None) -> Pose:
        """Build pose from extrinsic XYZ Euler angles in degrees."""
        rx_r, ry_r, rz_r = np.radians([rx, ry, rz])
        cx, sx = np.cos(rx_r), np.sin(rx_r)
        cy, sy = np.cos(ry_r), np.sin(ry_r)
        cz, sz = np.cos(rz_r), np.sin(rz_r)

        rx_m = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
        ry_m = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
        rz_m = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
        r = rz_m @ ry_m @ rx_m
        return cls(rotation=r, translation=t if t is not None else np.zeros(3))

    def as_matrix(self) -> np.ndarray:
        m = np.eye(4)
        m[:3, :3] = self.rotation
        m[:3, 3] = self.translation
        return m


@dataclass
class OrientationStep:
    """One fabrication step: part pose + deposition direction + toolpaths."""

    index: int
    object_pose: Pose
    deposition_direction: np.ndarray  # unit vector in build frame
    printable_face_indices: list[int] = field(default_factory=list)
    toolpaths: list[Toolpath] = field(default_factory=list)
    collision_ok: bool = True
    notes: str = ""

    def __post_init__(self) -> None:
        d = np.asarray(self.deposition_direction, dtype=float)
        n = np.linalg.norm(d)
        self.deposition_direction = d / n if n > 0 else np.array([0.0, 0.0, 1.0])


@dataclass
class OrientationSequence:
    """Ordered list of orientation steps for the full build."""

    steps: list[OrientationStep] = field(default_factory=list)
    part_name: str = ""

    @property
    def num_reorientations(self) -> int:
        return max(0, len(self.steps) - 1)
