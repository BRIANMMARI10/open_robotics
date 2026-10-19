"""Shared test fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
import trimesh


@pytest.fixture
def box_mesh() -> trimesh.Trimesh:
    return trimesh.creation.box(extents=[20, 20, 10])


@pytest.fixture
def box_stl(tmp_path: Path, box_mesh: trimesh.Trimesh) -> Path:
    path = tmp_path / "box.stl"
    box_mesh.export(path)
    return path
