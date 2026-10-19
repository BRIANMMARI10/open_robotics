"""Load and merge YAML config with CLI overrides."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Config:
    """Runtime configuration for the PoC pipeline."""

    raw: dict[str, Any] = field(default_factory=dict)
    project_root: Path = field(default_factory=lambda: Path.cwd())

    @property
    def output_dir(self) -> Path:
        rel = self.raw.get("project", {}).get("output_dir", "data/output")
        return self.project_root / rel

    @property
    def stl_path(self) -> Path:
        raw = self.raw.get("input", {}).get("stl", "data/input/test_part.stl")
        path = Path(raw)
        return path if path.is_absolute() else self.project_root / path

    @property
    def printer(self) -> dict[str, Any]:
        return self.raw.get("printer", {})

    @property
    def analysis(self) -> dict[str, Any]:
        return self.raw.get("analysis", {})

    @property
    def planning(self) -> dict[str, Any]:
        return self.raw.get("planning", {})

    @property
    def simulation(self) -> dict[str, Any]:
        return self.raw.get("simulation", {})

    @property
    def viz(self) -> dict[str, Any]:
        return self.raw.get("viz", {})


def load_config(
    config_path: Path | None = None,
    project_root: Path | None = None,
    stl_override: Path | None = None,
) -> Config:
    root = project_root or Path.cwd()
    path = config_path or root / "config" / "default.yaml"

    with path.open() as f:
        raw = yaml.safe_load(f) or {}

    if stl_override is not None:
        raw.setdefault("input", {})["stl"] = str(stl_override)

    return Config(raw=raw, project_root=root)


def make_run_dir(config: Config, run_name: str) -> Path:
    run_dir = config.output_dir / run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir
