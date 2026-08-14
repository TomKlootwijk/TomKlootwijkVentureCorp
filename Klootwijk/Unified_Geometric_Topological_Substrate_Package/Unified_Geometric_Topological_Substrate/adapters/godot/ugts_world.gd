class_name UGTSWorld
extends Node

# Minimal Godot adapter: authoritative state and events stay typed; drawing is optional.

static func state_at(p0: Vector2, v0: Vector2, t0: float, t: float, sheet: int, orientation: int, branch: StringName) -> Dictionary:
    return {
        "position": p0 + v0 * (t - t0),
        "velocity": v0,
        "time": t,
        "phase": 0.0,
        "sheet": sheet,
        "orientation": orientation,
        "branch": branch,
    }

static func next_line_crossing(p0: Vector2, v0: Vector2, t0: float, normal: Vector2, offset: float, after: float, before: float) -> Variant:
    var denominator := normal.dot(v0)
    if abs(denominator) < 1e-9:
        return null
    var dt := (offset - normal.dot(p0)) / denominator
    var event_time := t0 + dt
    if event_time > after and event_time <= before:
        return event_time
    return null

static func compatible(a: Dictionary, b: Dictionary, phase_tolerance: float = 0.001) -> bool:
    return a.sheet == b.sheet \
        and a.orientation == b.orientation \
        and abs(wrapf(a.phase - b.phase, -PI, PI)) <= phase_tolerance
