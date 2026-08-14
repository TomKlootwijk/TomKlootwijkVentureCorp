import pathlib, sys, unittest
from dataclasses import replace
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from event_engine import (
    AbsenceEvent, CoverageInterval, EventEngine, ExpectedEvent, State,
    UnknownOutcome, linear_threshold_relation
)

class EngineTests(unittest.TestCase):
    def test_state_at_and_closed_form_event(self):
        engine = EventEngine()
        engine.register_model("e", lambda t: State("e", t, position=(t,), lineage_address="seed/e"))
        relation = linear_threshold_relation(
            "x5", "toggle", 0.0, 1.0, 5.0,
            lambda s,c: replace(s, parity=1-s.parity),
        )
        event = engine.next_event("e", relation, 0.0)
        self.assertAlmostEqual(event.t_star, 5.0)
        self.assertEqual(event.parity_after, 1)

    def test_compatibility_rejects_candidate(self):
        engine = EventEngine()
        engine.register_model("e", lambda t: State("e", t, lineage_address="seed/e"))
        relation = linear_threshold_relation(
            "r", "t", 0.0, 1.0, 1.0, lambda s,c:s,
            compatibility=lambda s,t,c: (False, ["DENIED"]),
        )
        self.assertIsNone(engine.next_event("e", relation, 0.0))

    def test_absence_requires_complete_coverage(self):
        engine = EventEngine()
        engine.register_expectation(ExpectedEvent("x","e","followup",0,10,"1",{"basis":"test"}))
        engine.add_coverage("e", CoverageInterval("sensor",0,4,True))
        outcome = engine.close_expectation("x",11)
        self.assertIsInstance(outcome, UnknownOutcome)

    def test_absence_emitted_with_coverage(self):
        engine = EventEngine()
        engine.register_expectation(ExpectedEvent("x","e","followup",0,10,"1",{"basis":"test"}))
        engine.add_coverage("e", CoverageInterval("sensor-a",0,5,True))
        engine.add_coverage("e", CoverageInterval("sensor-b",5,10,True))
        outcome = engine.close_expectation("x",11)
        self.assertIsInstance(outcome, AbsenceEvent)
        self.assertEqual(outcome.matching_event_count, 0)

    def test_exception_blocks_absence(self):
        engine = EventEngine()
        engine.register_expectation(ExpectedEvent("x","e","followup",0,10,"1",{"basis":"test"}))
        engine.add_coverage("e", CoverageInterval("sensor",0,10,True))
        engine.set_exception("x", "OPT_OUT")
        outcome = engine.close_expectation("x",11)
        self.assertIsInstance(outcome, UnknownOutcome)

if __name__ == '__main__':
    unittest.main()
