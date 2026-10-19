"""Tests for baseline and orientation planning."""

from __future__ import annotations

import trimesh

from orient_print.phase1_baseline.analysis import analyze_baseline
from orient_print.phase1_planning.orientation_planner import plan_orientation_sequence


def test_baseline_box_top_face_not_overhang(box_mesh: trimesh.Trimesh) -> None:
    """Top (+Z) face should be printable; bottom and vertical walls are overhangs."""
    report = analyze_baseline(box_mesh, {"overhang_angle_deg": 45.0, "min_face_area_mm2": 0.1})
    overhang_set = set(report.overhang_face_indices)
    top_faces = {i for i, n in enumerate(report.face_normals) if n[2] > 0.9}
    assert top_faces.isdisjoint(overhang_set)
    assert report.overhang_face_count > 0


def test_orientation_plan_covers_box(box_mesh: trimesh.Trimesh) -> None:
    analysis_cfg = {"overhang_angle_deg": 45.0, "min_face_area_mm2": 0.1, "gravity_direction": [0, 0, -1]}
    planning_cfg = {
        "max_orientations": 6,
        "candidate_directions": [[0, 0, 1], [0, 0, -1], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]],
    }
    sequence, candidates = plan_orientation_sequence(box_mesh, analysis_cfg, planning_cfg)
    assert len(candidates) == 6
    assert len(sequence.steps) >= 1
