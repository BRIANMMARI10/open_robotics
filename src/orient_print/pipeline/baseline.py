"""Week 1: baseline geometry analysis."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from orient_print.config import load_config, make_run_dir
from orient_print.io.export import export_baseline_report
from orient_print.models.geometry import load_mesh, mesh_info
from orient_print.phase1_baseline.analysis import analyze_baseline
from orient_print.phase1_baseline.slicer import export_slice_preview_mesh
from orient_print.phase1_simulation.visualizer import plot_baseline_overhangs


def run_baseline(
    stl: Path | None = None,
    config: Path | None = None,
    project_root: Path | None = None,
) -> Path:
    root = project_root or Path.cwd()
    cfg = load_config(config_path=config, project_root=root, stl_override=stl)
    stl_path = stl or cfg.stl_path

    run_name = f"baseline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = make_run_dir(cfg, run_name)

    print(f"=== orient-print baseline ===")
    print(f"STL: {stl_path}")
    print(f"Output: {run_dir}\n")

    mesh = load_mesh(stl_path)
    info = mesh_info(mesh, stl_path)

    print("Mesh info:")
    print(f"  Vertices: {info.vertex_count:,}")
    print(f"  Faces: {info.face_count:,}")
    print(f"  Extents [mm]: {info.extents_mm}")
    print(f"  Watertight: {info.is_watertight}")
    if info.volume_mm3 is not None:
        print(f"  Volume [mm³]: {info.volume_mm3:.1f}")
    print()

    report = analyze_baseline(mesh, cfg.analysis)
    for line in report.summary_lines():
        print(line)
    print()

    export_baseline_report(report, run_dir / "baseline_report.json")
    plot_baseline_overhangs(
        mesh,
        report,
        output_path=run_dir / "baseline_overhangs.png",
        show=cfg.viz.get("show_interactive", False),
    )

    layer_h = float(cfg.printer.get("layer_height_mm", 0.2))
    zs = export_slice_preview_mesh(
        mesh,
        layer_height_mm=layer_h,
        output_path=run_dir / "slice_preview.obj",
        max_layers=20,
    )
    print(f"Slice preview: {len(zs)} layers saved to {run_dir / 'slice_preview.obj'}")

    print(f"\nDone. Artifacts in {run_dir}")
    return run_dir
