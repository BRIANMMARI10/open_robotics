"""Week 2: orientation planning."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from orient_print.config import load_config, make_run_dir
from orient_print.io.export import export_orientation_sequence
from orient_print.models.geometry import load_mesh, mesh_info
from orient_print.phase1_baseline.analysis import analyze_baseline
from orient_print.phase1_planning.orientation_planner import plan_orientation_sequence
from orient_print.phase1_simulation.visualizer import (
    plot_deposition_candidates,
    plot_orientation_sequence,
)


def run_orientation_plan(
    stl: Path | None = None,
    config: Path | None = None,
    project_root: Path | None = None,
) -> Path:
    root = project_root or Path.cwd()
    cfg = load_config(config_path=config, project_root=root, stl_override=stl)
    stl_path = stl or cfg.stl_path

    run_name = f"orientation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = make_run_dir(cfg, run_name)

    print(f"=== orient-print orientation plan ===")
    print(f"STL: {stl_path}")
    print(f"Output: {run_dir}\n")

    mesh = load_mesh(stl_path)
    info = mesh_info(mesh, stl_path)
    part_name = stl_path.stem

    baseline = analyze_baseline(mesh, cfg.analysis)
    print("Baseline (conventional +Z):")
    for line in baseline.summary_lines():
        print(f"  {line}")
    print()

    sequence, candidates = plan_orientation_sequence(
        mesh,
        cfg.analysis,
        cfg.planning,
        part_name=part_name,
    )

    print(f"Planned {len(sequence.steps)} orientation step(s), "
          f"{sequence.num_reorientations} reorientation(s):\n")
    for step in sequence.steps:
        d = step.deposition_direction
        print(
            f"  Step {step.index}: direction=[{d[0]:+.2f}, {d[1]:+.2f}, {d[2]:+.2f}]  "
            f"faces={len(step.printable_face_indices)}  {step.notes}"
        )
    print()

    export_orientation_sequence(sequence, candidates, run_dir / "orientation_plan.json")
    plot_deposition_candidates(
        mesh,
        candidates,
        top_n=6,
        output_path=run_dir / "deposition_candidates.png",
        show=cfg.viz.get("show_interactive", False),
    )
    plot_orientation_sequence(
        mesh,
        sequence,
        output_path=run_dir / "orientation_sequence.png",
        show=cfg.viz.get("show_interactive", False),
    )

    print(f"Part extents [mm]: {info.extents_mm}")
    print(f"\nDone. Artifacts in {run_dir}")
    return run_dir
