"""Mesh loading and basic geometry utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import trimesh


@dataclass
class MeshInfo:
    """Summary stats for a loaded mesh."""

    path: Path
    vertex_count: int
    face_count: int
    bounds_min: np.ndarray
    bounds_max: np.ndarray
    volume_mm3: float | None
    is_watertight: bool

    @property
    def extents_mm(self) -> np.ndarray:
        return self.bounds_max - self.bounds_min

    @property
    def center_mm(self) -> np.ndarray:
        return (self.bounds_min + self.bounds_max) / 2.0


def load_mesh(stl_path: Path) -> trimesh.Trimesh:
    """Load an STL and return a single Trimesh instance."""
    if not stl_path.exists():
        raise FileNotFoundError(
            f"STL not found: {stl_path}\n"
            f"Drop your test file in data/input/ or pass --stl /path/to/file.stl"
        )

    mesh = trimesh.load_mesh(stl_path, force="mesh")
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(tuple(mesh.geometry.values()))

    if not isinstance(mesh, trimesh.Trimesh):
        raise TypeError(f"Expected Trimesh, got {type(mesh)}")

    return mesh


def mesh_info(mesh: trimesh.Trimesh, path: Path) -> MeshInfo:
    bounds = mesh.bounds
    volume = float(mesh.volume) if mesh.is_watertight else None
    return MeshInfo(
        path=path,
        vertex_count=len(mesh.vertices),
        face_count=len(mesh.faces),
        bounds_min=bounds[0].copy(),
        bounds_max=bounds[1].copy(),
        volume_mm3=volume,
        is_watertight=bool(mesh.is_watertight),
    )


def gravity_vector(analysis_cfg: dict) -> np.ndarray:
    g = np.array(analysis_cfg.get("gravity_direction", [0, 0, -1]), dtype=float)
    norm = np.linalg.norm(g)
    return g / norm if norm > 0 else np.array([0.0, 0.0, -1.0])
