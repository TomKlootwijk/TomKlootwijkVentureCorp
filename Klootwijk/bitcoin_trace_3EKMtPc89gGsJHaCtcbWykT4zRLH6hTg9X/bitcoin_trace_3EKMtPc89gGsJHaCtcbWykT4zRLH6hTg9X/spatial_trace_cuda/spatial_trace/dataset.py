from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

import requests

from .io import TraceData, sha256_file, write_csv


SAT = 100_000_000


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def verify_live(address: str, api_base: str = "https://mempool.space/api") -> dict[str, Any]:
    session = requests.Session()
    session.headers["User-Agent"] = "bitcoin-spatial-trace-cuda/1.0"
    address_response = session.get(f"{api_base.rstrip('/')}/address/{address}", timeout=30)
    address_response.raise_for_status()
    tip_response = session.get(f"{api_base.rstrip('/')}/blocks/tip/height", timeout=30)
    tip_response.raise_for_status()
    body = address_response.json()
    chain = body.get("chain_stats", {})
    mempool = body.get("mempool_stats", {})
    confirmed = int(chain.get("funded_txo_sum", 0)) - int(chain.get("spent_txo_sum", 0))
    mempool_delta = int(mempool.get("funded_txo_sum", 0)) - int(mempool.get("spent_txo_sum", 0))
    return {
        "schema": "BITCOIN-SPATIAL-LIVE-VERIFICATION-1",
        "retrieved_utc": utc_now(),
        "api_base": api_base,
        "address": address,
        "tip_height": int(tip_response.text.strip()),
        "chain_stats": chain,
        "mempool_stats": mempool,
        "confirmed_balance_sats": confirmed,
        "balance_including_mempool_sats": confirmed + mempool_delta,
    }


def make_summary(
    data: TraceData,
    analysis: dict[str, Any],
    from_date: str,
    to_date: str,
    source_policy: dict[str, Any],
    live: dict[str, Any] | None,
) -> dict[str, Any]:
    reason_count = Counter(row["reason"] for row in data.terminals)
    reason_sats: dict[str, float] = defaultdict(float)
    for row in data.terminals:
        reason_sats[str(row["reason"])] += float(row["attributed_sats"])
    tx_times = sorted(row["block_time"] for row in data.transactions if row.get("block_time"))
    methods = Counter(row["method"] for row in data.transactions)
    target_source = next(row for row in data.addresses if row["address"] == data.target_address)
    root = data.roots[0]
    terminal_total = sum(float(row["attributed_sats"]) for row in data.terminals)
    fee_loss = max(float(data.starting_sats) - terminal_total, 0.0)
    return {
        "schema": "BITCOIN-SPATIAL-TRACE-SUMMARY-1",
        "generated_utc": utc_now(),
        "target_address": data.target_address,
        "requested_period": {"from": from_date, "to": to_date, "timezone": "UTC"},
        "source_observation_period": data.upstream_summary.get("period", {}),
        "target": {
            "starting_utxo_count": len(data.roots),
            "starting_sats": data.starting_sats,
            "starting_btc": data.starting_sats / SAT,
            "funding_txid": root["funding_txid"],
            "funded_at_unix": root["funded_at"],
            "spent": bool(root["spent"]),
            "spend_txid": root.get("spend_txid", ""),
            "spent_at_unix": root.get("spent_at", 0),
            "source_confirmed_balance_sats": int(target_source["confirmed_balance_sats"]),
            "live_confirmed_balance_sats": None if live is None else live["confirmed_balance_sats"],
        },
        "captured_graph": {
            "nodes": len(analysis["nodes"]),
            "transactions": len(data.transactions),
            "flow_edges": len(data.edges),
            "addresses_and_scripts": sum(1 for row in analysis["nodes"] if row["kind"] in {"target", "address", "script"}),
            "terminal_outputs": len(data.terminals),
            "first_traced_transaction_utc": tx_times[0] if tx_times else None,
            "last_traced_transaction_utc": tx_times[-1] if tx_times else None,
            "transaction_methods": dict(methods),
        },
        "terminal_coverage": {
            "count_by_reason": dict(reason_count),
            "attributed_sats_by_reason": dict(reason_sats),
            "terminal_attributed_sats": terminal_total,
            "terminal_attributed_btc": terminal_total / SAT,
            "difference_from_start_sats": fee_loss,
            "difference_note": "The small difference is primarily attributed transaction fees and floating-point rounding.",
        },
        "source_policy": source_policy,
        "evidence_boundary": {
            "exact": [
                "The target outpoint value and its spending transaction.",
                "Transaction inputs, outputs, fees, block heights, and block times captured from Esplora.",
                "The target address balance at the recorded retrieval time.",
            ],
            "modeled": [
                "The amount assigned to later outputs after tracked value is mixed with unrelated inputs.",
                "Weighted PageRank and the topological layout.",
            ],
            "not_claimed": [
                "Who controls an address or wallet.",
                "Whether an address belongs to a service or person.",
                "A physical or geographic location.",
                "That a particular later satoshi is the original satoshi.",
            ],
        },
        "live_verification": live,
        "cuda": analysis["benchmark"],
    }


def write_ranked_tables(output: Path, data: TraceData, analysis: dict[str, Any]) -> None:
    nodes = sorted(
        (row for row in analysis["nodes"] if row["kind"] != "transaction"),
        key=lambda row: (-float(row["incoming_attributed_sats"]), row["id"]),
    )
    write_csv(
        output / "tables" / "nodes_ranked_by_incoming_attribution.csv",
        nodes,
        [
            "id", "kind", "depth", "incoming_attributed_sats", "outgoing_attributed_sats",
            "weighted_pagerank", "confirmed_balance_sats", "balance_status", "terminal_reason",
        ],
    )
    terminals = sorted(data.terminals, key=lambda row: (-float(row["attributed_sats"]), row["outpoint"]))
    write_csv(
        output / "tables" / "terminal_outputs_ranked.csv",
        terminals,
        ["outpoint", "address", "depth", "attributed_sats", "reason"],
    )


def write_provenance(
    output: Path,
    data: TraceData,
    ugts_source: Path,
    source_policy: dict[str, Any],
    live: dict[str, Any] | None,
) -> dict[str, Any]:
    provenance = {
        "schema": "BITCOIN-SPATIAL-TRACE-PROVENANCE-1",
        "generated_utc": utc_now(),
        "source_trace_directory": str(data.root),
        "source_files": {
            name: {"sha256": digest, "bytes": (data.root / name).stat().st_size}
            for name, digest in data.source_hashes.items()
        },
        "raw_evidence": data.raw_evidence,
        "ugts_source_directory": str(ugts_source.resolve()),
        "ugts_build_info_sha256": sha256_file(ugts_source / "BUILD_INFO.json") if (ugts_source / "BUILD_INFO.json").is_file() else None,
        "source_policy": source_policy,
        "source_policy_recording_note": "The upstream summary did not serialize its CLI caps. Values are supplied to this build and checked against observed terminal reasons/depths.",
        "live_verification": live,
        "external_references": [
            {"title": "Bitcoin Developer Guide - Transactions", "url": "https://developer.bitcoin.org/devguide/transactions.html"},
            {"title": "Blockstream Esplora HTTP API", "url": "https://github.com/Blockstream/esplora/blob/master/API.md"},
            {"title": "mempool.space API", "url": "https://mempool.space/api"},
        ],
    }
    (output / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    return provenance
