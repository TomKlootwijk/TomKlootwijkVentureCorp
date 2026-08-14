"""Synthetic pipeline event: solve a pressure guard and register valve-response obligation."""
from dataclasses import asdict, replace
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from event_engine import EventEngine, State, ExpectedEvent, CoverageInterval, linear_threshold_relation

engine = EventEngine()
engine.register_model("segment-17", lambda t: State(
    entity_id="segment-17", t=t, position=(12.5,), sheet="live",
    lineage_address="pipeline/segment-17", branch="operations", parity=0,
    attributes={"pressure_bar": 80.0 - 2.0*t}
))
relation = linear_threshold_relation(
    relation_id="low-pressure-guard", transition_id="declare-suspected-rupture",
    value_at_zero=80.0, slope=-2.0, threshold=60.0,
    transition=lambda s, ctx: replace(s, parity=1, branch="incident-branch", attributes={**s.attributes, "incident": True}),
    support=lambda s,t,c: (c.get("sensor_coverage", False), ["PRESSURE_SENSOR_HEALTHY"]),
    compatibility=lambda s,t,c: (c.get("authorized", False), ["CONTROL_AUTHORIZED"]),
)
event = engine.next_event("segment-17", relation, 0.0, {"sensor_coverage": True, "authorized": True})
engine.register_expectation(ExpectedEvent(
    expectation_id="valve-close-17", entity_id="segment-17", relation_id="valve-closed",
    due_start=event.t_star, due_end=event.t_star+2.0, predicate_version="mitigation-1.0",
    authority={"basis": "synthetic emergency rule"}
))
engine.add_coverage("segment-17", CoverageInterval("valve-position-feedback", event.t_star, event.t_star+2.0, True))
absence = engine.close_expectation("valve-close-17", event.t_star+2.1)
print(json.dumps({"guard_event": asdict(event), "mitigation_outcome": asdict(absence)}, indent=2))
