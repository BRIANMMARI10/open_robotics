"""CLI entry point (optional: `orient-print` after pip install -e .)."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="orient-print PoC CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    base = sub.add_parser("baseline", help="Run Week 1 baseline analysis")
    base.add_argument("--stl", type=Path, help="Path to input STL")
    base.add_argument("--config", type=Path, help="Config YAML path")

    plan = sub.add_parser("plan", help="Run Week 2 orientation planning")
    plan.add_argument("--stl", type=Path, help="Path to input STL")
    plan.add_argument("--config", type=Path, help="Config YAML path")

    sim = sub.add_parser("simulate", help="Run full PoC pipeline")
    sim.add_argument("--stl", type=Path, help="Path to input STL")
    sim.add_argument("--config", type=Path, help="Config YAML path")

    args = parser.parse_args()
    root = Path.cwd()

    if args.command == "baseline":
        from orient_print.pipeline.baseline import run_baseline

        run_baseline(stl=args.stl, config=args.config, project_root=root)
    elif args.command == "plan":
        from orient_print.pipeline.orientation import run_orientation_plan

        run_orientation_plan(stl=args.stl, config=args.config, project_root=root)
    elif args.command == "simulate":
        from orient_print.pipeline.simulation import run_simulation

        run_simulation(stl=args.stl, config=args.config, project_root=root)
