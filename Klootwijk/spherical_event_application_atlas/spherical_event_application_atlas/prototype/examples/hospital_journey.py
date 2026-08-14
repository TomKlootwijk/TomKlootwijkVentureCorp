"""Synthetic cradle-to-life care journey: lineage, consent and auditable absence."""
from dataclasses import asdict
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from event_engine import EventEngine, ExpectedEvent, CoverageInterval

engine = EventEngine()
engine.register_expectation(ExpectedEvent(
    expectation_id="maternal-newborn-followup-001",
    entity_id="journey-person-001",
    relation_id="post-discharge-followup",
    due_start=7.0,
    due_end=14.0,
    predicate_version="care-pathway-1.0",
    authority={"basis": "synthetic care plan", "consent": "granted"},
))
engine.add_coverage("journey-person-001", CoverageInterval("patient-portal", 7.0, 14.0, True))
outcome = engine.close_expectation("maternal-newborn-followup-001", now=15.0)
print(json.dumps(asdict(outcome), indent=2))
