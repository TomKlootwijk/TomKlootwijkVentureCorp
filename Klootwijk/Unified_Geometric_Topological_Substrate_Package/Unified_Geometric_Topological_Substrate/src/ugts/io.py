from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .compatibility import CompatibilityRule
from .events import CircleSurface, EventRule, LineSurface
from .math2d import Vec2
from .state import Entity, EntityState, EventRecord
from .support import RadialAngularSupport
from .trajectory import LinearTrajectory, QuadraticTrajectory
from .transition import TransitionRule
from .world import World


def _vec2(value: Any, name: str) -> Vec2:
    try:
        return Vec2.from_iterable(value)
    except Exception as exc:  # noqa: BLE001 - convert into schema-oriented message
        raise ValueError(f'{name} must be a two-number sequence') from exc


def world_from_dict(data: Mapping[str, Any]) -> World:
    schema_version = str(data.get('schema_version', '1.0.0'))
    world = World(schema_version=schema_version)
    for raw in data.get('entities', []):
        tr_raw = raw['trajectory']
        tr_type = tr_raw['type']
        common = dict(p0=_vec2(tr_raw['p0'], 'p0'), v0=_vec2(tr_raw['v0'], 'v0'), t0=float(tr_raw.get('t0', 0.0)))
        if tr_type == 'linear':
            trajectory = LinearTrajectory(**common)
        elif tr_type == 'quadratic':
            acceleration = _vec2(tr_raw.get('a', tr_raw.get('acceleration')), 'a')
            trajectory = QuadraticTrajectory(acceleration=acceleration, **common)
        else:
            raise ValueError(f'unsupported trajectory type: {tr_type!r}')
        world.add_entity(Entity(
            entity_id=str(raw['id']),
            trajectory=trajectory,
            phase0=float(raw.get('phase', 0.0)),
            phase_rate=float(raw.get('phase_rate', 0.0)),
            sheet0=int(raw.get('sheet', 0)),
            orientation0=int(raw.get('orientation', 1)),
            branch0=str(raw.get('branch', 'A')),
            tags0=frozenset(map(str, raw.get('tags', []))),
            uncertainty=float(raw.get('uncertainty', 0.0)),
            metadata=dict(raw.get('metadata', {})),
        ))

    for raw in data.get('relations', []):
        sraw = raw['surface']
        stype = sraw['type']
        if stype == 'line':
            surface = LineSurface(_vec2(sraw['normal'], 'normal'), float(sraw.get('offset', 0.0)), name=str(sraw.get('name', raw['id'])))
        elif stype == 'circle':
            surface = CircleSurface(_vec2(sraw.get('center', [0.0, 0.0]), 'center'), float(sraw['radius']), name=str(sraw.get('name', raw['id'])))
        else:
            raise ValueError(f'unsupported surface type: {stype!r}')

        support = None
        sup = raw.get('support')
        if sup is not None:
            if sup.get('type', 'radial_angular') != 'radial_angular':
                raise ValueError('only radial_angular support is implemented')
            support = RadialAngularSupport(
                origin=_vec2(sup.get('origin', [0.0, 0.0]), 'support.origin'),
                r_min=float(sup.get('r_min', 0.0)),
                r_max=float(sup.get('r_max', float('inf'))),
                theta_center=float(sup.get('theta_center', 0.0)),
                theta_half_width=float(sup.get('theta_half_width', 3.141592653589793)),
                time_min=float(sup.get('time_min', -float('inf'))),
                time_max=float(sup.get('time_max', float('inf'))),
            )

        comp = raw.get('compatibility', {})
        compatibility = CompatibilityRule(
            allowed_sheets=None if 'allowed_sheets' not in comp else frozenset(map(int, comp['allowed_sheets'])),
            allowed_orientations=None if 'allowed_orientations' not in comp else frozenset(map(int, comp['allowed_orientations'])),
            phase_center=None if 'phase_center' not in comp else float(comp['phase_center']),
            phase_tolerance=float(comp.get('phase_tolerance', 3.141592653589793)),
            allowed_branches=None if 'allowed_branches' not in comp else frozenset(map(str, comp['allowed_branches'])),
            required_tags=frozenset(map(str, comp.get('required_tags', []))),
            forbidden_tags=frozenset(map(str, comp.get('forbidden_tags', []))),
            lineage_prefix=None if 'lineage_prefix' not in comp else tuple(map(str, comp['lineage_prefix'])),
        )

        tr = raw.get('transition', {})
        transition = TransitionRule(
            toggle_sheet=bool(tr.get('toggle_sheet', False)),
            sheet_modulus=int(tr.get('sheet_modulus', 2)),
            set_sheet=None if tr.get('set_sheet') is None else int(tr['set_sheet']),
            flip_orientation=bool(tr.get('flip_orientation', False)),
            phase_delta=float(tr.get('phase_delta', 0.0)),
            set_branch=None if tr.get('set_branch') is None else str(tr['set_branch']),
            add_tags=frozenset(map(str, tr.get('add_tags', []))),
            remove_tags=frozenset(map(str, tr.get('remove_tags', []))),
            lineage_label=None if tr.get('lineage_label') is None else str(tr['lineage_label']),
        )
        world.add_rule(EventRule(
            rule_id=str(raw['id']),
            surface=surface,
            support=support,
            compatibility=compatibility,
            transition=transition,
            enabled=bool(raw.get('enabled', True)),
            confidence=float(raw.get('confidence', 1.0)),
            metadata=dict(raw.get('metadata', {})),
        ))
    return world


def load_world(path: str | Path) -> World:
    with Path(path).open('r', encoding='utf-8') as fh:
        return world_from_dict(json.load(fh))


def _state_dict(state: EntityState | None) -> dict[str, Any] | None:
    if state is None:
        return None
    return {
        'entity_id': state.entity_id,
        'time': state.time,
        'position': list(state.position.as_tuple()),
        'velocity': list(state.velocity.as_tuple()),
        'phase': state.phase,
        'sheet': state.sheet,
        'orientation': state.orientation,
        'branch': state.branch,
        'lineage': list(state.lineage),
        'tags': sorted(state.tags),
        'uncertainty': state.uncertainty,
        'metadata': dict(state.metadata),
    }


def event_record_dict(record: EventRecord) -> dict[str, Any]:
    return {
        'event_id': record.event_id,
        'entity_id': record.entity_id,
        'rule_id': record.rule_id,
        'time': record.time,
        'state_before': _state_dict(record.state_before),
        'state_after': _state_dict(record.state_after),
        'relation_value': record.relation_value,
        'crossing_direction': record.crossing_direction,
        'confidence': record.confidence,
        'solver': record.solver,
        'lineage': list(record.lineage),
        'reason_codes': list(record.reason_codes),
        'metadata': dict(record.metadata),
    }


def write_event_log(world: World, path: str | Path) -> None:
    payload = {
        'schema_version': world.schema_version,
        'events': [event_record_dict(record) for record in world.event_log],
    }
    Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n', encoding='utf-8')
