from __future__ import annotations

import json
from dataclasses import asdict

from equation_world_zero import (
    CompatibilityPolicy,
    Entity,
    LineRelation,
    SupportSector,
    Trajectory2D,
    TransitionRule,
    World,
    lineage_address,
)


def main() -> None:
    address = lineage_address("seed-alpha", ["spawn", "move-right"], [])
    entity = Entity(
        entity_id="e-alpha",
        trajectory=Trajectory2D(x0=-2.0, y0=0.25, vx=1.0, vy=0.0, phase0=0.0),
        sheet=0,
        address=address,
        invariant_tags=("mass-class-A",),
    )

    relation = LineRelation(
        relation_id="B0",
        nx=1.0,
        ny=0.0,
        c=0.0,
        support=SupportSector(origin=(0.0, 0.0), r_min=0.0, r_max=1.0),
        policy=CompatibilityPolicy(allowed_sheets=(0,), target_phase=0.0, phase_tolerance=0.01),
    )
    transition = TransitionRule(
        transition_id="route-A-to-B",
        target_sheet=1,
        toggle_parity=True,
        create_branch=True,
        state_updates={"route": "B"},
    )
    world = World(
        relations=[relation],
        transitions={transition.transition_id: transition},
        relation_to_transition={relation.relation_id: transition.transition_id},
    )

    before = world.state_at(entity, 0.0)
    event = world.next_event(entity, 0.0)
    if event is None:
        raise RuntimeError("Expected an admitted event")
    updated = world.apply_transition(entity, event)
    after = world.state_at(updated, event.time)

    print(json.dumps({
        "before": asdict(before),
        "event": asdict(world.event_log[-1]),
        "after": asdict(after),
    }, indent=2))


if __name__ == "__main__":
    main()
