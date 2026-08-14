# UGTS-0 package manifest

Version: 1.0.0  
Prepared: 2026-08-14  
Source basis: nine user-supplied PDFs, treated as design records. The original PDFs are not redistributed.

## Canonical technical core

UGTS-0 is a bounded, query-first geometric-topological substrate:

```text
finite grammar + typed state
        |
        v
local support -> compatibility -> event solve -> transition
        |                                  |
        +---------- lineage + log ---------+
                                            |
                  optional game / graphics / hardware adapters
```

The authoritative state separates position, continuous time, phase, sheet, orientation, branch, lineage and uncertainty. A one-bit value is only a schema-bound route, admission, parity or freshness flag. It is never the complete state.

## Delivered artifacts

- `report/Unified_Geometric_Topological_Substrate.pdf` - 45-page unified report.
- `report/main.tex` and generated table sources - reproducible report source.
- `specs/concept_inventory.csv` - 69 extracted concepts with source expression, normalized operator, disposition, source IDs and page ranges.
- `specs/claims_ledger.csv` - 18 corrected, demoted or rejected claims.
- `specs/architecture.json` - canonical layer and query model.
- `specs/world_schema.json` and `specs/example_world.json` - machine-readable world definition.
- `src/ugts/` - dependency-free Python reference implementation.
- `tests/test_ugts.py` - 17 executable tests.
- `examples/` - state/event, topology, graphics, fractal and B.C.E. demonstrations.
- `shaders/ugts_preview.frag` - optional GLSL preview adapter.
- `adapters/` - minimal Unity C# and Godot GDScript bridges.
- `diagrams/` - report figures plus the generation script.
- `source_notes/` - per-source extraction and evidence-boundary notes.

## Verification

Run from the extracted package root:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python examples/equation_world_zero.py
PYTHONPATH=src python examples/topology_demo.py
PYTHONPATH=src python examples/graphics_preview.py
PYTHONPATH=src python examples/fractal_preview.py
PYTHONPATH=src python examples/bce_demo.py
```

Expected unit-test result: `Ran 17 tests ... OK`.

## Rebuild the report

A TeX installation with XeLaTeX, `latexmk`, DejaVu fonts and the packages imported by `report/main.tex` is required.

```bash
python report/generate_tables.py
cd report
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

## Evidence and safety boundary

The package retains implementable operators and rejects unsupported totalizing claims. In particular, it does not claim universal constant-time computation, zero memory, zero latency or power, physical Klein-bottle self-assembly, complete state in one bit, replacement of all conventional simulation/indexing, or replacement of general AI. The optofluidic endpoint is a prototype specification requiring measured guards, calibration, error, energy and a conventional baseline.
