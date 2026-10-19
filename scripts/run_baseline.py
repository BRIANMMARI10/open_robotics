#!/usr/bin/env python3
"""Week 1: baseline geometry + overhang analysis."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from orient_print.pipeline.baseline import run_baseline  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run baseline overhang analysis")
    parser.add_argument("--stl", type=Path, help="Path to input STL")
    parser.add_argument("--config", type=Path, help="Config YAML (default: config/default.yaml)")
    args = parser.parse_args()

    run_baseline(stl=args.stl, config=args.config, project_root=ROOT)


if __name__ == "__main__":
    main()
