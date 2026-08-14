"""Synthetic mental-health research observation with consent as compatibility.

Silence is never converted into a symptom. Missing diary data under incomplete coverage
returns UnknownOutcome, and no clinical conclusion is produced.
"""
from dataclasses import asdict
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from event_engine import EventEngine, ExpectedEvent, CoverageInterval

engine = EventEngine()
engine.register_expectation(ExpectedEvent(
    expectation_id="research-diary-window-12", entity_id="participant-pseudonym-88",
    relation_id="consented-diary-submission", due_start=12.0, due_end=13.0,
    predicate_version="consent-protocol-2.1", authority={"basis": "IRB-approved synthetic example"}
))
# Device sync failed for part of the interval: this must remain unknown.
engine.add_coverage("participant-pseudonym-88", CoverageInterval("study-app", 12.0, 12.3, True))
outcome = engine.close_expectation("research-diary-window-12", 14.0)
print(json.dumps(asdict(outcome), indent=2))
