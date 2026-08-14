"""Synthetic pallet lineage and missing zone-exit scan."""
from dataclasses import asdict
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from event_engine import EventEngine, ExpectedEvent, CoverageInterval

engine = EventEngine()
engine.register_expectation(ExpectedEvent(
    expectation_id="scan-zone-B-exit", entity_id="pallet-8491", relation_id="epcis-zone-exit",
    due_start=120.0, due_end=135.0, predicate_version="warehouse-routing-3.2",
    authority={"basis": "work order WO-441"}
))
engine.add_coverage("pallet-8491", CoverageInterval("reader-B7", 120.0, 135.0, True))
print(json.dumps(asdict(engine.close_expectation("scan-zone-B-exit", 136.0)), indent=2))
