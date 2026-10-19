# orient-print-poc

Proof of concept: **dynamic orientation during 3D printing** to enable geometries that are difficult or impossible with conventional fixed-bed FDM.

## Hypothesis

> Can we use a sequence of object orientations (via robot arm, rotating fixture, or multi-axis platform) to change deposition direction during fabrication, producing viable toolpaths where conventional layer-by-layer printing fails or requires heavy support?

**Build to discover** — not to prove a business model on day one.

## Phase 1 scope (30 days)

| Week | Focus | Script |
|------|-------|--------|
| 1 | Baseline: load STL, analyze geometry, conventional slice preview | `scripts/run_baseline.py` |
| 2 | Orientation planning: candidate deposition directions | `scripts/run_orientation_plan.py` |
| 3 | Toolpaths per orientation + collision checks | (extend planning module) |
| 4 | Full simulation + comparison vs baseline | `scripts/run_simulation.py` |

## Quick start

```bash
cd orient-print-poc
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Drop your test STL into `data/input/` (e.g. `data/input/test_part.stl`), then:

```bash
# Week 1: inspect mesh + baseline overhang analysis
python scripts/run_baseline.py --stl data/input/test_part.stl

# Week 2: find candidate deposition directions
python scripts/run_orientation_plan.py --stl data/input/test_part.stl

# Week 4: run full PoC pipeline (when implemented)
python scripts/run_simulation.py --stl data/input/test_part.stl
```

Outputs land in `data/output/<run_name>/`.

## Project layout

```
orient-print-poc/
├── config/default.yaml       # print + analysis parameters
├── data/
│   ├── input/                # your STL goes here
│   └── output/               # generated plots, JSON, G-code
├── docs/
│   ├── hypothesis.md         # technical hypothesis + success criteria
│   └── weekly_log.md         # discovery journal
├── scripts/                  # runnable entry points
├── src/orient_print/         # library code
│   ├── models/               # data structures (poses, toolpaths)
│   ├── phase1_baseline/      # conventional FDM comparison
│   ├── phase1_planning/      # orientation + toolpath planning
│   ├── phase1_simulation/    # collision + visualization
│   └── io/                   # export helpers
└── tests/
```

## Core data model

The PoC uses an intermediate representation — **not** G-code as the primary format:

```python
OrientationStep(
    object_pose=(R, t),           # part transform relative to build frame
    deposition_direction=[0,0,1], # gravity-aligned extrusion axis in build frame
    toolpaths=[...],              # 3D polylines to extrude in this step
    collision_ok=True,
)
```

G-code is generated later for baseline comparison or Phase 2 hardware.

## Configuration

Edit `config/default.yaml` for layer height, nozzle diameter, overhang threshold, etc.

## Tests

```bash
pytest
```

## License

Private PoC — add a license when/if you open-source.
