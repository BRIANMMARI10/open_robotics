#!/usr/bin/env python3
"""Compare two run directories (baseline vs reorient plan)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare orient-print run outputs")
    parser.add_argument("baseline_run", type=Path, help="Run dir with baseline_report.json")
    parser.add_argument("orientation_run", type=Path, help="Run dir with orientation_plan.json")
    args = parser.parse_args()

    baseline = load_json(args.baseline_run / "baseline_report.json")
    plan = load_json(args.orientation_run / "orientation_plan.json")

    print("=== Comparison ===\n")
    print("Conventional baseline (+Z):")
    print(f"  Overhang area fraction: {100 * baseline['overhang_area_fraction']:.1f}%")
    print(f"  Support burden: {baseline['support_burden_estimate']}")
    print()
    print("Reorientation plan:")
    print(f"  Steps: {plan['num_steps']}")
    print(f"  Reorientations: {plan['num_reorientations']}")
    for step in plan["steps"]:
        print(f"    Step {step['index']}: {step['printable_face_count']} faces — {step['notes']}")


if __name__ == "__main__":
    main()
