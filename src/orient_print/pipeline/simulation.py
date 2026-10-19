"""Week 4: full PoC pipeline (baseline + planning + collision stubs)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from orient_print.config import load_config, make_run_dir
from orient_print.io.export import export_baseline_report, export_orientation_sequence
from orient_print.models.geometry import load_mesh
from orient_print.phase1_baseline.analysis import analyze_baseline
from orient_print.phase1_planning.orientation_planner import plan_orientation_sequence
from orient_print.phase1_simulation.collision import check_step_collision
from orient_print.phase1_simulation.visualizer import (
    plot_baseline_overhangs,
    plot_deposition_candidates,
    plot_orientation_sequence,
)


def run_simulation(
    stl: Path | None = None,
    config: Path | None = None,
    project_root: Path | None = None,
) -> Path:
    root = project_root or Path.cwd()
    cfg = load_config(config_path=config, project_root=root, stl_override=stl)
    stl_path = stl or cfg.stl_path

    run_name = f"simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = make_run_dir(cfg, run_name)

    print(f"=== orient-print simulation ===")
    print(f"STL: {stl_path}")
    print(f"Output: {run_dir}\n")

    mesh = load_mesh(stl_path)
    part_name = stl_path.stem

    baseline = analyze_baseline(mesh, cfg.analysis)
    sequence, candidates = plan_orientation_sequence(
        mesh, cfg.analysis, cfg.planning, part_name=part_name
    )

    for step in sequence.steps:
        step.collision_ok = check_step_collision(mesh, step, cfg.simulation)

    export_baseline_report(baseline, run_dir / "baseline_report.json")
    export_orientation_sequence(sequence, candidates, run_dir / "orientation_plan.json")

    plot_baseline_overhangs(mesh, baseline, run_dir / "baseline_overhangs.png")
    plot_deposition_candidates(mesh, candidates, top_n=6, output_path=run_dir / "deposition_candidates.png")
    plot_orientation_sequence(mesh, sequence, run_dir / "orientation_sequence.png")

    print("Baseline:")
    for line in baseline.summary_lines():
        print(f"  {line}")

    print(f"\nOrientation plan: {len(sequence.steps)} steps")
    all_collision_ok = all(s.collision_ok for s in sequence.steps)
    print(f"Collision check (stub): {'PASS' if all_collision_ok else 'FAIL'}")

    print(f"\nDone. Artifacts in {run_dir}")
    return run_dir
