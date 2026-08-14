#!/usr/bin/env python3
"""Synthetic Membrane World Zero event-log demonstration.

Generates a noisy flux/TMP process, applies support/compatibility/guard logic, and writes
an append-only event log. This is a software example, not validation of a real membrane.
"""
from __future__ import annotations
import csv
import json
import math
import random
import uuid
from pathlib import Path

import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent


def main():
    rng = random.Random(19)
    dt = 1.0
    n = 1800
    flux0 = 100.0
    tmp0 = 1.0
    rows = []
    events = []
    previous_flags = {"fouling": False, "pressure": False, "breakthrough": False}

    for i in range(n):
        t = i * dt
        cake = 0.0008 * t + 0.25 * (1 - math.exp(-t/250))
        clean = 0.45 if 1100 <= t < 1160 else 0.0
        effective = max(0, cake - clean)
        flux = flux0 / (1 + effective) + rng.gauss(0, 0.65)
        tmp = tmp0 * (1 + 0.42 * effective) + rng.gauss(0, 0.008)
        conductivity = 0.2 + (1.8 / (1 + math.exp(-(t-1450)/20))) + rng.gauss(0, 0.015)
        supported = 20 <= t <= 1770
        compatible = supported and (i % 127 != 0)  # synthetic calibration dropout
        confidence = 0.98 if compatible else 0.4
        flags = {
            "fouling": compatible and confidence >= 0.95 and flux < 82.0,
            "pressure": compatible and confidence >= 0.95 and tmp > 1.14,
            "breakthrough": compatible and confidence >= 0.95 and conductivity > 1.5,
        }
        for name, flag in flags.items():
            if flag and not previous_flags[name]:
                events.append({
                    "event_id": str(uuid.uuid4()),
                    "event_type": name,
                    "time_interval": [t-dt, t],
                    "support": {"active": supported, "module": "M0"},
                    "compatibility": {"value": compatible, "schema": "sensor+calibration+lineage"},
                    "guard": {"name": name, "crossed": True},
                    "confidence": confidence,
                    "lineage": {"material_id": "baseline_demo", "calibration": "cal-001"},
                    "pre_state": rows[-1] if rows else {},
                    "post_state": {"time_s": t, "flux": flux, "tmp": tmp, "conductivity": conductivity},
                    "action": "inspect_or_control",
                    "raw_data_refs": [f"membrane_timeseries.csv#row={i+2}"],
                })
            previous_flags[name] = flag
        rows.append({"time_s": t, "flux": flux, "tmp": tmp, "conductivity": conductivity, "supported": int(supported), "compatible": int(compatible), "confidence": confidence})

    with (OUT / "membrane_timeseries.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    with (OUT / "membrane_event_log.jsonl").open("w") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    ax.plot([r["time_s"] for r in rows], [r["flux"] for r in rows], label="Flux")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Synthetic flux")
    ax.set_title("Synthetic membrane process with guard-crossing events")
    for e in events:
        ax.axvline(e["time_interval"][1], alpha=0.35)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUT / "membrane_event_demo.png", dpi=200)
    print(f"Generated {len(rows)} samples and {len(events)} events")

if __name__ == "__main__":
    main()
