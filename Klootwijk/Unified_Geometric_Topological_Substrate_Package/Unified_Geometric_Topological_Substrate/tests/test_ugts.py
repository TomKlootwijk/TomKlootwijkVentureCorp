from __future__ import annotations

import json
import math
from pathlib import Path
import tempfile
import unittest

from ugts import (
    BCEController,
    BCEMeasurement,
    CircleSurface,
    CompatibilityRule,
    Entity,
    EventRule,
    HourglassRouter,
    KleinBottleQuotient,
    LinearTrajectory,
    LineSurface,
    LogPolarLUT,
    MobiusBand,
    PortalMap,
    RadialAngularSupport,
    TransitionRule,
    Vec2,
    World,
    from_log_polar,
    load_world,
    to_log_polar,
    write_event_log,
)
from ugts.geometry import BoxSDF, CircleSDF, DifferenceField, IntersectionField, UnionField, lens_area_equal_circles
from ugts.grammar import FiniteGrammar, GrammarError, Production
from ugts.glyphs import loop_to_r_morph
from ugts.numeric import (
    active_bit_positions,
    active_bits_triangle,
    hamming_weight,
    pascal_entry_is_odd,
    radix_digit_count,
    radix_thresholds,
    zero_based_ordinal,
)
from ugts.render import Bounds2D, posterize_1bit, rasterize_field, sigma_delta_bitstream


ROOT = Path(__file__).resolve().parents[1]


class NumericTests(unittest.TestCase):
    def test_radix_and_indexing(self) -> None:
        self.assertEqual(radix_digit_count(0, 2), 1)
        self.assertEqual(radix_digit_count(19, 2), 5)
        self.assertEqual(radix_thresholds(2, 20), [2, 4, 8, 16])
        self.assertEqual(zero_based_ordinal(35), 36)

    def test_active_bits_and_pascal(self) -> None:
        self.assertEqual(active_bit_positions(19), (4, 1, 0))
        self.assertEqual(hamming_weight(19), 3)
        tri = active_bits_triangle(19)
        self.assertEqual(tri.bit_positions, (4, 1, 0))
        # Row 7 (=2^3-1) is all odd; row 8 is not.
        self.assertTrue(all(pascal_entry_is_odd(7, k) for k in range(8)))
        self.assertFalse(all(pascal_entry_is_odd(8, k) for k in range(9)))


class GeometryTests(unittest.TestCase):
    def test_csg_signs(self) -> None:
        circle = CircleSDF(Vec2(0, 0), 1.0)
        box = BoxSDF(Vec2(0, 0), Vec2(0.5, 0.5))
        self.assertLess(UnionField(circle, box).value(Vec2(0, 0)), 0)
        self.assertLess(IntersectionField(circle, box).value(Vec2(0, 0)), 0)
        self.assertGreater(DifferenceField(circle, box).value(Vec2(0, 0)), 0)

    def test_overlap_lens_area(self) -> None:
        self.assertAlmostEqual(lens_area_equal_circles(1.0, 0.0), math.pi)
        self.assertEqual(lens_area_equal_circles(1.0, 2.0), 0.0)

    def test_glyph_morph_is_queryable(self) -> None:
        start = loop_to_r_morph(0.0)
        end = loop_to_r_morph(1.0)
        self.assertTrue(math.isfinite(start.value(Vec2(0.0, 0.0))))
        self.assertTrue(math.isfinite(end.value(Vec2(0.0, 0.0))))


class EventWorldTests(unittest.TestCase):
    def make_world(self) -> World:
        world = World()
        world.add_entity(Entity(
            'traveler',
            LinearTrajectory(Vec2(-2.0, 0.0), Vec2(1.0, 0.0)),
            phase0=0.0,
            sheet0=0,
            orientation0=1,
            tags0=frozenset({'player'}),
        ))
        world.add_rule(EventRule(
            'x_zero',
            LineSurface(Vec2(1.0, 0.0), 0.0),
            support=RadialAngularSupport(r_max=3.0),
            compatibility=CompatibilityRule(allowed_sheets=frozenset({0}), required_tags=frozenset({'player'})),
            transition=TransitionRule(toggle_sheet=True, flip_orientation=True, set_branch='B', phase_delta=math.pi / 2),
        ))
        return world

    def test_next_event_and_transition(self) -> None:
        world = self.make_world()
        candidate = world.next_event('traveler', 0.0, 5.0)
        self.assertIsNotNone(candidate)
        assert candidate is not None
        self.assertAlmostEqual(candidate.time, 2.0)
        record = world.process_next_event('traveler', 0.0, 5.0)
        self.assertIsNotNone(record)
        assert record is not None
        self.assertEqual(record.state_before.sheet, 0)
        self.assertEqual(record.state_after.sheet, 1)
        self.assertEqual(record.state_after.orientation, -1)
        self.assertEqual(record.state_after.branch, 'B')
        self.assertEqual(len(world.event_log), 1)

    def test_double_vacuum_same_coordinate_no_coupling(self) -> None:
        world = World()
        world.add_entity(Entity('a', LinearTrajectory(Vec2(0, 0), Vec2(0, 0)), sheet0=0, phase0=0.0))
        world.add_entity(Entity('b', LinearTrajectory(Vec2(0, 0), Vec2(0, 0)), sheet0=1, phase0=math.pi))
        result = world.can_couple('a', 'b', 0.0, max_distance=1e-9, phase_tolerance=0.1)
        self.assertFalse(result.accepted)
        self.assertIn('sheet_mismatch', result.reason_codes)
        self.assertIn('phase_mismatch', result.reason_codes)

    def test_circle_event(self) -> None:
        world = World()
        world.add_entity(Entity('e', LinearTrajectory(Vec2(-2, 0), Vec2(1, 0))))
        world.add_rule(EventRule('circle', CircleSurface(Vec2(0, 0), 1.0)))
        times = [c.time for c in world.solver.candidates(world.entities['e'], world.rules, 0, 5)]
        self.assertEqual(len(times), 2)
        self.assertAlmostEqual(times[0], 1.0)
        self.assertAlmostEqual(times[1], 3.0)


class TopologyTests(unittest.TestCase):
    def test_mobius_orientation_flip(self) -> None:
        band = MobiusBand(4.0, 2.0)
        mapped = band.map(Vec2(4.5, 0.25), orientation=1)
        self.assertAlmostEqual(mapped.point.x, 0.5)
        self.assertAlmostEqual(mapped.point.y, -0.25)
        self.assertEqual(mapped.orientation, -1)

    def test_klein_sheet_flip(self) -> None:
        kb = KleinBottleQuotient(4.0, 2.0)
        mapped = kb.map(Vec2(4.5, 0.25), orientation=1, sheet=0)
        self.assertEqual(mapped.orientation, -1)
        self.assertEqual(mapped.sheet, 1)

    def test_portal_and_hourglass(self) -> None:
        portal = PortalMap(translation=Vec2(1, 2), rotation=math.pi / 2, flip_orientation=True, sheet_delta=1)
        mapped = portal.apply(Vec2(1, 0), 1, 0)
        self.assertAlmostEqual(mapped.point.x, 1.0)
        self.assertAlmostEqual(mapped.point.y, 3.0)
        self.assertEqual(mapped.orientation, -1)
        self.assertEqual(mapped.sheet, 1)
        router = HourglassRouter()
        self.assertEqual(router.chamber(1, 1), 'A')
        self.assertEqual(router.route('A', 1), 'C')


class LogPolarAndRenderTests(unittest.TestCase):
    def test_roundtrip_and_core(self) -> None:
        p = Vec2(2.0, -1.0)
        lp = to_log_polar(p)
        q = from_log_polar(lp)
        self.assertAlmostEqual(p.x, q.x, places=8)
        self.assertAlmostEqual(p.y, q.y, places=8)
        self.assertTrue(to_log_polar(Vec2(0, 0)).is_core)

    def test_lut_storage_and_render(self) -> None:
        lut = LogPolarLUT(-5.0, 2.0, 32, 64)
        lut.fill(lambda lp: abs(lp.theta) < 0.5)
        self.assertGreater(lut.active_count(), 0)
        self.assertEqual(lut.storage_bytes, 256)
        image = rasterize_field(CircleSDF(Vec2(0, 0), 0.75), width=24, height=24, bounds=Bounds2D(-1, 1, -1, 1), samples=4)
        binary = posterize_1bit(image, seed=7)
        self.assertEqual(len(binary.pixels), 24 * 24)
        self.assertTrue(set(binary.pixels).issubset({0.0, 1.0}))

    def test_sigma_delta(self) -> None:
        bits = sigma_delta_bitstream(0.25, 100)
        self.assertLessEqual(abs(sum(bits) - 25), 1)


class GrammarTests(unittest.TestCase):
    def test_finite_expansion(self) -> None:
        grammar = FiniteGrammar.from_productions(('X',), [Production('X', ('X', '+', 'X'))], max_depth=3, max_symbols=100)
        self.assertEqual(len(grammar.expand(2)), 7)
        with self.assertRaises(GrammarError):
            grammar.expand(4)


class BCETests(unittest.TestCase):
    def test_guard_crossing_and_parity(self) -> None:
        controller = BCEController(threshold=1.0, minimum_confidence=0.8)
        first = controller.evaluate(BCEMeasurement(0.0, 0.5, True, True, True, confidence=0.9))
        self.assertFalse(first.accepted)
        second = controller.evaluate(BCEMeasurement(0.1, 1.2, True, True, True, confidence=0.9))
        self.assertTrue(second.accepted)
        self.assertEqual(second.parity, 1)
        rejected = controller.evaluate(BCEMeasurement(0.2, 1.3, False, True, True, confidence=0.9))
        self.assertFalse(rejected.accepted)
        self.assertIn('outside_support', rejected.reason_codes)


class IOTests(unittest.TestCase):
    def test_load_example_and_write_log(self) -> None:
        world = load_world(ROOT / 'specs' / 'example_world.json')
        self.assertEqual(set(world.entities), {'traveler_A', 'co_located_B'})
        record = world.process_next_event('traveler_A', 0.0, 5.0)
        self.assertIsNotNone(record)
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'events.json'
            write_event_log(world, path)
            payload = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(len(payload['events']), 1)
            self.assertEqual(payload['events'][0]['rule_id'], 'x_zero_hinge')


if __name__ == '__main__':
    unittest.main()
