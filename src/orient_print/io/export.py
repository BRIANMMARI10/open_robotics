"""Export reports and intermediate results."""

from __future__ import annotations

import json
from pathlib import Path

from orient_print.models.orientation import OrientationSequence
from orient_print.phase1_baseline.analysis import BaselineReport
from orient_print.phase1_planning.deposition_analysis import DepositionCandidate


def _json_default(obj):
    if hasattr(obj, "tolist"):
        return obj.tolist()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def export_baseline_report(report: BaselineReport, path: Path) -> None:
    data = {
        "overhang_angle_threshold_deg": report.overhang_angle_threshold_deg,
        "total_faces": report.total_faces,
        "overhang_face_count": report.overhang_face_count,
        "overhang_area_mm2": report.overhang_area_mm2,
        "total_area_mm2": report.total_area_mm2,
        "overhang_area_fraction": report.overhang_area_fraction,
        "support_burden_estimate": report.support_burden_estimate,
        "overhang_face_indices": report.overhang_face_indices,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def export_orientation_sequence(
    sequence: OrientationSequence,
    candidates: list[DepositionCandidate],
    path: Path,
) -> None:
    steps_data = []
    for step in sequence.steps:
        steps_data.append(
            {
                "index": step.index,
                "deposition_direction": step.deposition_direction.tolist(),
                "object_pose_rotation": step.object_pose.rotation.tolist(),
                "object_pose_translation": step.object_pose.translation.tolist(),
                "printable_face_indices": step.printable_face_indices,
                "printable_face_count": len(step.printable_face_indices),
                "collision_ok": step.collision_ok,
                "notes": step.notes,
            }
        )

    cand_data = [
        {
            "direction": c.direction.tolist(),
            "printable_face_count": c.printable_face_count,
            "printable_area_mm2": c.printable_area_mm2,
            "score": c.score,
        }
        for c in candidates
    ]

    data = {
        "part_name": sequence.part_name,
        "num_steps": len(sequence.steps),
        "num_reorientations": sequence.num_reorientations,
        "steps": steps_data,
        "all_candidates": cand_data,
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=_json_default))
