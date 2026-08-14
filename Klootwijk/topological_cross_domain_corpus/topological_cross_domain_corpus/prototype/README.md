# Equation World Zero Reference Prototype

This standard-library Python prototype implements a deliberately restricted subset of the corpus:

- closed-form constant-velocity state evaluation;
- analytic roots for line and circle guards;
- local radial-angular support;
- sheet/phase/tag compatibility;
- one-bit parity routing;
- lineage-address update and event logging.

Run:

```bash
python demo.py
python -m unittest -v test_equation_world_zero.py
```

The code is an executable interpretation, not source validation. It does not implement arbitrary SDFs, general topology, PDEs, rendering, AI, photonics, biology, or universal O(1) computation.
