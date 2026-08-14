"""Synthetic solar inverter voltage guard with bounded compatibility."""
from dataclasses import asdict, replace
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from event_engine import EventEngine, State, linear_threshold_relation

engine = EventEngine()
engine.register_model("inverter-3", lambda t: State(
    entity_id="inverter-3", t=t, position=(4.1, 52.0), sheet="distribution-feeder",
    lineage_address="DER/site-22/inverter-3", branch="live", parity=0,
    attributes={"voltage_pu": 1.00 + 0.005*t}
))
relation = linear_threshold_relation(
    relation_id="overvoltage-support", transition_id="apply-volt-var",
    value_at_zero=1.00, slope=0.005, threshold=1.05,
    transition=lambda s,ctx: replace(s, parity=1, attributes={**s.attributes, "command": "volt-var"}),
    support=lambda s,t,c: (c.get("feeder_support", False), ["IN_DECLARED_FEEDER_SUPPORT"]),
    compatibility=lambda s,t,c: (c.get("ieee1547_mode", False) and c.get("operator_permission", False), ["GRID_SUPPORT_MODE_ALLOWED"]),
)
event = engine.next_event("inverter-3", relation, 0.0, {"feeder_support": True, "ieee1547_mode": True, "operator_permission": True})
print(json.dumps(asdict(event), indent=2))
