#!/usr/bin/env python3
"""Aggregate repeated physical-GPU UGTS and LUT-cache benchmark runs."""
from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def median(values: list[float]) -> float:
    return float(statistics.median(values))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, action="append", default=[])
    parser.add_argument("--lut", type=Path, action="append", default=[])
    parser.add_argument("--l2-bytes", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    if not args.core or not args.lut:
        parser.error("at least one --core and one --lut run are required")

    core_docs = [load(path) for path in args.core]
    lut_docs = [load(path) for path in args.lut]
    device_names = {doc["device"]["name"] for doc in core_docs + lut_docs}
    if len(device_names) != 1:
        raise SystemExit(f"runs contain multiple devices: {sorted(device_names)}")

    core_groups: dict[tuple[str, str, int], list[dict[str, Any]]] = defaultdict(list)
    for doc in core_docs:
        for row in doc["benchmarks"]:
            core_groups[(row["profile"], row["mode"], row["candidates"])].append(row)

    core_rows: list[dict[str, Any]] = []
    for (profile, mode, candidates), rows in sorted(core_groups.items()):
        p50 = [row["device_dispatch_ms"]["p50"] for row in rows]
        rates = [row["candidate_rate_mps"] for row in rows]
        event_rates = [row["verified_event_rate_mps"] for row in rows]
        bandwidths = [row["effective_bandwidth_gbps"] for row in rows]
        working_set = rows[0]["total_buffer_bytes"]
        core_rows.append(
            {
                "profile": profile,
                "mode": mode,
                "candidates": candidates,
                "replicates": len(rows),
                "working_set_bytes": working_set,
                "working_set_l2_fraction": working_set / args.l2_bytes,
                "device_p50_ms_median": median(p50),
                "device_p50_ms_min": min(p50),
                "device_p50_ms_max": max(p50),
                "candidate_rate_mps_median": median(rates),
                "candidate_rate_mps_min": min(rates),
                "candidate_rate_mps_max": max(rates),
                "verified_event_rate_mps_median": median(event_rates),
                "logical_bandwidth_gbps_median": median(bandwidths),
                "gpu_counts": rows[0]["counts"],
                "oracle_counts": rows[0]["oracle_counts"],
                "boundary_divergent_outputs": rows[0]["boundary_divergent_outputs"],
                "all_outputs_validated": all(
                    row["validated_outputs"] == candidates and row["sample_validation"]
                    for row in rows
                ),
                "all_commit_counters_validated": all(row["counter_validation"] for row in rows),
            }
        )

    lut_groups: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for doc in lut_docs:
        for row in doc["results"]:
            lut_groups[(row["pattern"], row["table_bytes"])].append(row)

    lut_rows: list[dict[str, Any]] = []
    for (pattern, table_bytes), rows in sorted(lut_groups.items()):
        p50 = [row["device_ms"]["p50"] for row in rows]
        rates = [row["lookup_mps"] for row in rows]
        bandwidths = [row["logical_gbps"] for row in rows]
        lut_rows.append(
            {
                "pattern": pattern,
                "table_bytes": table_bytes,
                "l2_fraction": table_bytes / args.l2_bytes,
                "candidates": rows[0]["candidates"],
                "replicates": len(rows),
                "device_p50_ms_median": median(p50),
                "device_p50_ms_min": min(p50),
                "device_p50_ms_max": max(p50),
                "lookup_mps_median": median(rates),
                "lookup_mps_min": min(rates),
                "lookup_mps_max": max(rates),
                "logical_bandwidth_gbps_median": median(bandwidths),
                "all_outputs_validated": all(row["validation"] for row in rows),
            }
        )

    result = {
        "schema": "UGTS-WINDOWS-PHYSICAL-GPU-AGGREGATE-1.0",
        "device": next(iter(device_names)),
        "l2_bytes": args.l2_bytes,
        "core_sources": [str(path) for path in args.core],
        "lut_sources": [str(path) for path in args.lut],
        "core": core_rows,
        "lut": lut_rows,
        "notes": [
            "Medians aggregate independent process runs; min/max expose dynamic-clock and WDDM variability.",
            "Logical bandwidth counts declared input plus output record bytes, not external DRAM transactions.",
            "LUT results use R32_UINT uniform texel fetches containing two packed 16-bit log codes per word.",
            "L2 size came from the local CUDA device-properties query; direct performance counters were permission-blocked.",
        ],
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "aggregate_metrics.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )

    with (args.out_dir / "core_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        fieldnames = [key for key in core_rows[0] if key not in {"gpu_counts", "oracle_counts"}]
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for row in core_rows:
            writer.writerow({key: row[key] for key in fieldnames})

    with (args.out_dir / "lut_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=lut_rows[0].keys())
        writer.writeheader()
        writer.writerows(lut_rows)

    print(args.out_dir / "aggregate_metrics.json")


if __name__ == "__main__":
    main()
