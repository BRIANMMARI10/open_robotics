#!/usr/bin/env python3
"""Week 2: deposition direction analysis + orientation sequence."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from orient_print.pipeline.orientation import run_orientation_plan  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Plan orientation sequence")
    parser.add_argument("--stl", type=Path, help="Path to input STL")
    parser.add_argument("--config", type=Path, help="Config YAML")
    args = parser.parse_args()

    run_orientation_plan(stl=args.stl, config=args.config, project_root=ROOT)


if __name__ == "__main__":
    main()
