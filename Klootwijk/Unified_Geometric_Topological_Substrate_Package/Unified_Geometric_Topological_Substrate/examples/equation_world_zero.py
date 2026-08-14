from __future__ import annotations

import json
from pathlib import Path

from ugts import load_world, write_event_log


ROOT = Path(__file__).resolve().parents[1]
world = load_world(ROOT / 'specs' / 'example_world.json')

print('state_at(traveler_A, 1.25):')
print(world.state_at('traveler_A', 1.25))

candidate = world.next_event('traveler_A', 0.0, 5.0)
print('\nnext_event:', candidate)
record = world.process_next_event('traveler_A', 0.0, 5.0)
print('\nprocessed event:', record)

coupling = world.can_couple(
    'traveler_A', 'co_located_B', 2.0,
    max_distance=1e-9,
    phase_tolerance=0.2,
    require_same_sheet=True,
    require_same_orientation=True,
)
print('\nco-located coupling result:', coupling)

out = ROOT / 'examples' / 'generated' / 'event_log.json'
write_event_log(world, out)
print(f'\nwrote {out}')
