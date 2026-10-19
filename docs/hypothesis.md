# Technical Hypothesis

## Question

Can we find a sequence of object poses `{R_i, t_i}` and deposition directions `{d_i}` such that the union of material deposited in each step forms the target geometry, with **better manufacturability** than a single fixed-orientation FDM slice?

## Success criteria (Phase 1 — simulation)

- [ ] Load test STL and report baseline overhang/support burden
- [ ] Identify ≥3 candidate deposition directions for the test part
- [ ] Produce an orientation sequence covering printable surface patches
- [ ] Generate toolpaths for at least one orientation step
- [ ] Pass basic nozzle-vs-part collision check
- [ ] Visualize full process: reorient → deposit → reorient → deposit
- [ ] Side-by-side comparison with conventional baseline

## Non-goals (Phase 1)

- Production-ready slicer
- Real robot integration
- Material adhesion / cooling physics
- Sub-millimeter registration accuracy

## Possible outcomes (all valuable)

1. **Success** — feasible orientation sequence demonstrated in simulation
2. **Limitation** — physics/geometry constraint identified; refine approach
3. **Pivot** — experiments reveal a different problem worth pursuing

## Open questions to answer during PoC

- Rotate workpiece vs move printhead vs robot arm — which is easiest?
- How many reorientations are needed for the test part?
- Does changing deposition direction actually reduce support material?
- Where does collision (nozzle vs printed geometry) kill feasibility?
