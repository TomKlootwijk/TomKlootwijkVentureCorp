# Restricted reference prototype

This directory implements the smallest reusable software kernel behind the application atlas:

1. `state_at(entity, t)` evaluates a declared state function without a global frame loop.
2. `next_event(...)` asks a relation for candidate roots, then applies support, compatibility and guard checks.
3. transitions preserve identity/lineage invariants and emit auditable event records.
4. an `ExpectedEvent` can become an `AbsenceEvent` only after its interval closes under complete declared observation coverage.
5. missing telemetry produces `UnknownOutcome`, never false certainty.

The examples are synthetic. They do not make clinical, safety, regulatory, financial or operational decisions.
Run:

```bash
cd prototype
python -m unittest discover -s tests -v
python examples/hospital_journey.py
python examples/energy_pipeline.py
python examples/warehouse_delivery.py
python examples/solar_grid.py
python examples/mental_health_research.py
```
