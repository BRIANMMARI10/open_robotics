# Input models

Place your test STL here:

```
data/input/test_part.stl
```

Or pass any path via CLI:

```bash
python scripts/run_baseline.py --stl /path/to/your/model.stl
```

**Suggested test parts** (pick one that's hard for conventional FDM):

- Bracket with 45°+ overhangs
- Curved shell / dome
- Part with internal features visible only from certain angles
- Something you already know requires heavy supports in Cura/PrusaSlicer

STL files are gitignored by default (often large). Commit only if small.
