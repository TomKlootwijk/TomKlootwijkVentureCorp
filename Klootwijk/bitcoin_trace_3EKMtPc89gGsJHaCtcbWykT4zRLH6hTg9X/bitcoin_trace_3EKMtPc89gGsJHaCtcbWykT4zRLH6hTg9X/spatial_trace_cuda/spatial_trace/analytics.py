from __future__ import annotations

from collections import defaultdict
import hashlib
import math
import statistics
import time
from typing import Any

import torch

from .io import TraceData


def select_device(requested: str) -> torch.device:
    requested = requested.lower()
    if requested == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but torch.cuda.is_available() is false")
    return torch.device(requested)


def _graph_arrays(data: TraceData) -> tuple[list[str], dict[str, int], list[int], list[int], list[float]]:
    names = {data.target_address}
    for edge in data.edges:
        names.add(str(edge["from"]))
        names.add(str(edge["to"]))
    ordered = [data.target_address] + sorted(n for n in names if n.startswith("tx:")) + sorted(
        n for n in names if n != data.target_address and not n.startswith("tx:")
    )
    index = {name: idx for idx, name in enumerate(ordered)}
    src = [index[str(edge["from"])] for edge in data.edges]
    dst = [index[str(edge["to"])] for edge in data.edges]
    weight = [max(float(edge["attributed_sats"]), 0.0) for edge in data.edges]
    return ordered, index, src, dst, weight


def _tensor_kernel(
    node_count: int,
    src_values: list[int],
    dst_values: list[int],
    weights: list[float],
    device: torch.device,
    iterations: int,
) -> dict[str, torch.Tensor]:
    src = torch.tensor(src_values, dtype=torch.long, device=device)
    dst = torch.tensor(dst_values, dtype=torch.long, device=device)
    weight = torch.tensor(weights, dtype=torch.float64, device=device)
    ones = torch.ones_like(weight)
    incoming = torch.zeros(node_count, dtype=torch.float64, device=device).scatter_add_(0, dst, weight)
    outgoing = torch.zeros(node_count, dtype=torch.float64, device=device).scatter_add_(0, src, weight)
    in_degree = torch.zeros(node_count, dtype=torch.float64, device=device).scatter_add_(0, dst, ones)
    out_degree = torch.zeros(node_count, dtype=torch.float64, device=device).scatter_add_(0, src, ones)

    rank = torch.full((node_count,), 1.0 / node_count, dtype=torch.float64, device=device)
    damping = 0.85
    transition = weight / outgoing[src].clamp_min(1e-30)
    dangling = outgoing <= 0
    for _ in range(iterations):
        contribution = rank[src] * transition
        next_rank = torch.zeros_like(rank).scatter_add_(0, dst, contribution)
        dangling_mass = rank[dangling].sum() / node_count
        rank = (1.0 - damping) / node_count + damping * (next_rank + dangling_mass)
    rank /= rank.sum().clamp_min(1e-30)
    return {
        "incoming_attributed_sats": incoming,
        "outgoing_attributed_sats": outgoing,
        "in_degree": in_degree,
        "out_degree": out_degree,
        "weighted_pagerank": rank,
    }


def _timed_kernel(
    node_count: int,
    src: list[int],
    dst: list[int],
    weights: list[float],
    device: torch.device,
    iterations: int,
    repeats: int = 12,
) -> tuple[dict[str, torch.Tensor], list[float]]:
    _tensor_kernel(node_count, src, dst, weights, device, iterations)
    if device.type == "cuda":
        torch.cuda.synchronize(device)
    timings: list[float] = []
    result: dict[str, torch.Tensor] | None = None
    for _ in range(repeats):
        start = time.perf_counter()
        result = _tensor_kernel(node_count, src, dst, weights, device, iterations)
        if device.type == "cuda":
            torch.cuda.synchronize(device)
        timings.append((time.perf_counter() - start) * 1000.0)
    assert result is not None
    return result, timings


def _stable_fraction(value: str) -> float:
    raw = hashlib.blake2s(value.encode("utf-8"), digest_size=8, person=b"UGTSMAP").digest()
    return int.from_bytes(raw, "little") / float(2**64 - 1)


def _node_depths(data: TraceData, names: list[str]) -> dict[str, float]:
    depth: dict[str, float] = {data.target_address: 0.0}
    for edge in data.edges:
        d = float(edge["depth"])
        if edge["edge_type"] == "input_to_tx":
            depth[str(edge["from"])] = min(depth.get(str(edge["from"]), d), d)
            tx_depth = d + 0.48
            depth[str(edge["to"])] = min(depth.get(str(edge["to"]), tx_depth), tx_depth)
        else:
            depth[str(edge["from"])] = min(depth.get(str(edge["from"]), max(d - 0.52, 0.0)), max(d - 0.52, 0.0))
            depth[str(edge["to"])] = min(depth.get(str(edge["to"]), d), d)
    return {name: depth.get(name, 0.0) for name in names}


def _layout(data: TraceData, names: list[str], metrics: dict[str, list[float]]) -> dict[str, tuple[float, float]]:
    depths = _node_depths(data, names)
    groups: dict[int, list[str]] = defaultdict(list)
    for name in names:
        groups[int(round(depths[name] * 2))].append(name)
    result: dict[str, tuple[float, float]] = {}
    for layer, group in sorted(groups.items()):
        group.sort(key=lambda n: (-metrics["weighted_pagerank"][names.index(n)], _stable_fraction(n)))
        count = len(group)
        for position, name in enumerate(group):
            if count == 1:
                y = 0.0
            else:
                y = -1.0 + 2.0 * position / (count - 1)
                y += (_stable_fraction(name) - 0.5) * min(0.08, 0.8 / count)
            result[name] = (depths[name], y)
    return result


def analyze(data: TraceData, requested_device: str = "auto", pagerank_iterations: int = 64) -> dict[str, Any]:
    names, index, src, dst, weights = _graph_arrays(data)
    device = select_device(requested_device)
    cpu_result, cpu_times = _timed_kernel(len(names), src, dst, weights, torch.device("cpu"), pagerank_iterations)
    device_result, device_times = _timed_kernel(len(names), src, dst, weights, device, pagerank_iterations)

    metrics: dict[str, list[float]] = {
        key: tensor.detach().cpu().tolist() for key, tensor in device_result.items()
    }
    layout = _layout(data, names, metrics)
    max_error = max(
        float(torch.max(torch.abs(cpu_result[key].cpu() - device_result[key].cpu())).item())
        for key in cpu_result
    )
    node_rows = []
    address_rows = {row["address"]: row for row in data.addresses}
    transaction_rows = {"tx:" + row["txid"]: row for row in data.transactions}
    terminal_reason: dict[str, str] = {}
    for row in data.terminals:
        terminal_reason.setdefault(str(row["address"]), str(row["reason"]))
    depth_map = _node_depths(data, names)
    for name in names:
        i = index[name]
        if name == data.target_address:
            kind = "target"
        elif name.startswith("tx:"):
            kind = "transaction"
        elif name.startswith("script:"):
            kind = "script"
        else:
            kind = "address"
        address = address_rows.get(name, {})
        tx = transaction_rows.get(name, {})
        node_rows.append(
            {
                "id": name,
                "kind": kind,
                "depth": depth_map[name],
                "x": layout[name][0],
                "y": layout[name][1],
                "incoming_attributed_sats": metrics["incoming_attributed_sats"][i],
                "outgoing_attributed_sats": metrics["outgoing_attributed_sats"][i],
                "in_degree": int(round(metrics["in_degree"][i])),
                "out_degree": int(round(metrics["out_degree"][i])),
                "weighted_pagerank": metrics["weighted_pagerank"][i],
                "confirmed_balance_sats": int(address.get("confirmed_balance_sats", 0)),
                "balance_status": str(address.get("balance_status", "not_applicable")),
                "chain_tx_count": int(address.get("chain_tx_count", 0)),
                "block_time": str(tx.get("block_time", "")),
                "terminal_reason": terminal_reason.get(name, ""),
            }
        )

    benchmark = {
        "requested_device": requested_device,
        "selected_device": str(device),
        "cuda_used": device.type == "cuda",
        "torch_version": torch.__version__,
        "torch_cuda_version": torch.version.cuda,
        "gpu_name": torch.cuda.get_device_name(device) if device.type == "cuda" else None,
        "node_count": len(names),
        "edge_count": len(src),
        "pagerank_iterations": pagerank_iterations,
        "repeats": len(device_times),
        "cpu_median_ms": statistics.median(cpu_times),
        "selected_device_median_ms": statistics.median(device_times),
        "selected_device_min_ms": min(device_times),
        "max_cpu_device_absolute_error": max_error,
        "timing_scope": "Tensor construction plus scatter/PageRank loop; Python import and CSV parsing excluded.",
    }
    return {"nodes": node_rows, "node_index": index, "benchmark": benchmark}
