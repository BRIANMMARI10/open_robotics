"""Tests for mesh loading."""

from __future__ import annotations

from pathlib import Path

import pytest

from orient_print.models.geometry import load_mesh, mesh_info


def test_load_mesh(box_stl: Path) -> None:
    mesh = load_mesh(box_stl)
    assert len(mesh.vertices) > 0
    assert len(mesh.faces) > 0


def test_load_mesh_missing() -> None:
    with pytest.raises(FileNotFoundError, match="STL not found"):
        load_mesh(Path("/nonexistent/part.stl"))


def test_mesh_info(box_stl: Path) -> None:
    mesh = load_mesh(box_stl)
    info = mesh_info(mesh, box_stl)
    assert info.is_watertight
    assert info.volume_mm3 == pytest.approx(20 * 20 * 10, rel=0.01)
