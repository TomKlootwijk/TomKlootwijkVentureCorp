from __future__ import annotations

import unittest

from equation_world_zero import (
    CircleRelation,
    CompatibilityPolicy,
    Entity,
    LineRelation,
    SupportSector,
    Trajectory2D,
    TransitionRule,
    World,
    lineage_address,
)


class EquationWorldZeroTests(unittest.TestCase):
    def make_entity(self, *, sheet: int = 0, phase0: float = 0.0) -> Entity:
        return Entity(
            entity_id="e",
            trajectory=Trajectory2D(-2.0, 0.0, 1.0, 0.0, phase0=phase0),
            sheet=sheet,
            address=lineage_address("seed", ["move"], []),
            invariant_tags=("stable",),
        )

    def test_state_at_is_closed_form(self) -> None:
        world = World([], {}, {})
        entity = self.make_entity()
        self.assertEqual(world.state_at(entity, 1_000_000.0).position, (999_998.0, 0.0))

    def test_double_vacuum_rejects_co_location(self) -> None:
        relation = LineRelation(
            "B0", 1.0, 0.0, 0.0,
            policy=CompatibilityPolicy(allowed_sheets=(1,)),
        )
        rule = TransitionRule("route")
        world = World([relation], {"route": rule}, {"B0": "route"})
        self.assertIsNone(world.next_event(self.make_entity(sheet=0), 0.0))

    def test_line_event_routes_and_toggles(self) -> None:
        relation = LineRelation(
            "B0", 1.0, 0.0, 0.0,
            support=SupportSector(r_max=0.1),
            policy=CompatibilityPolicy(allowed_sheets=(0,)),
        )
        rule = TransitionRule("route", target_sheet=1, toggle_parity=True)
        world = World([relation], {"route": rule}, {"B0": "route"})
        entity = self.make_entity(sheet=0)
        event = world.next_event(entity, 0.0)
        self.assertIsNotNone(event)
        assert event is not None
        self.assertAlmostEqual(event.time, 2.0)
        updated = world.apply_transition(entity, event)
        self.assertEqual(updated.sheet, 1)
        self.assertEqual(updated.parity, 1)
        self.assertEqual(len(world.event_log), 1)

    def test_circle_roots_are_analytic(self) -> None:
        relation = CircleRelation(
            "circle", 0.0, 0.0, 1.0,
            policy=CompatibilityPolicy(allowed_sheets=(0,)),
        )
        rule = TransitionRule("touch")
        world = World([relation], {"touch": rule}, {"circle": "touch"})
        event = world.next_event(self.make_entity(), 0.0)
        self.assertIsNotNone(event)
        assert event is not None
        self.assertAlmostEqual(event.time, 1.0)


if __name__ == "__main__":
    unittest.main()
