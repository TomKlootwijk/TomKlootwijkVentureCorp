from __future__ import annotations

from datetime import datetime
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np

from .io import TraceData


ONTOLOGY = {
    "schema": "UGTS-SPATIAL-ONTOLOGY-1",
    "description": "Bitcoin trace profile for the UGTS sparse temporal graph. Coordinates are topological display coordinates, not geography.",
    "node_types": [
        {"id": 0, "name": "address", "sheet": 0, "description": "Bitcoin address observed in a captured transaction output."},
        {"id": 1, "name": "transaction", "sheet": 1, "description": "Confirmed Bitcoin transaction."},
        {"id": 2, "name": "script", "sheet": 2, "description": "Output script without a decoded address in the source response."},
        {"id": 3, "name": "target_address", "sheet": 3, "description": "Requested starting address."},
    ],
    "relations": [
        {"id": 0, "name": "spends_into", "source_types": [0, 2, 3], "target_types": [1], "mode_bit": 0, "guard": "outpoint"},
        {"id": 1, "name": "creates_output", "source_types": [1], "target_types": [0, 2, 3], "mode_bit": 1, "guard": "transaction_output"},
    ],
}


def _node_type(kind: str) -> int:
    return {"address": 0, "transaction": 1, "script": 2, "target": 3}[kind]


def _timestamp(value: str) -> float:
    if not value:
        return 0.0
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def export_ugts(
    output_dir: Path,
    data: TraceData,
    analysis: dict[str, Any],
    ugts_source: Path,
    requested_period: dict[str, str],
) -> dict[str, Any]:
    source = str(ugts_source.resolve())
    if source not in sys.path:
        sys.path.insert(0, source)
    from ugts_spatial.graph import GraphBuilder, SparseTemporalGraph

    root = output_dir / "ugts_graph"
    root.mkdir(parents=True, exist_ok=True)
    (root / "bitcoin_trace_ontology.json").write_text(json.dumps(ONTOLOGY, indent=2) + "\n", encoding="utf-8")

    builder = GraphBuilder(feature_dim=16)
    builder.metadata = {
        "profile": "BITCOIN-UGTS-SPARSE-TEMPORAL-1",
        "target_address": data.target_address,
        "requested_period": requested_period,
        "coordinate_semantics": {
            "column_0": "topological hop depth",
            "column_1": "deterministic display order within the hop layer",
            "column_2": "reserved and zero",
            "warning": "These are not latitude, longitude, altitude, or evidence of physical location.",
        },
        "feature_columns": [
            "is_address", "is_transaction", "is_script", "is_target",
            "log_incoming_attribution", "log_outgoing_attribution", "normalized_depth", "weighted_pagerank",
            "normalized_in_degree", "normalized_out_degree", "log_confirmed_balance", "has_retrieved_balance",
            "is_terminal_below_threshold", "is_terminal_max_hops", "transaction_tracked_ratio", "transaction_output_count_normalized",
        ],
        "edge_weight_semantics": "attributed_sats divided by starting_sats",
        "attribution_warning": "After commingling, attributed_sats is a proportional model and not a tagged-coin fact.",
    }
    max_depth = max(float(row["depth"]) for row in analysis["nodes"]) or 1.0
    max_in_degree = max(int(row["in_degree"]) for row in analysis["nodes"]) or 1
    max_out_degree = max(int(row["out_degree"]) for row in analysis["nodes"]) or 1
    tx_map = {"tx:" + row["txid"]: row for row in data.transactions}
    node_indices: dict[str, int] = {}
    for row in analysis["nodes"]:
        kind = row["kind"]
        tx = tx_map.get(row["id"], {})
        features = np.asarray(
            [
                kind == "address", kind == "transaction", kind == "script", kind == "target",
                math.log1p(float(row["incoming_attributed_sats"])) / math.log1p(max(data.starting_sats, 1)),
                math.log1p(float(row["outgoing_attributed_sats"])) / math.log1p(max(data.starting_sats, 1)),
                float(row["depth"]) / max_depth,
                float(row["weighted_pagerank"]),
                int(row["in_degree"]) / max_in_degree,
                int(row["out_degree"]) / max_out_degree,
                math.log1p(max(int(row["confirmed_balance_sats"]), 0)) / math.log1p(max(data.starting_sats, 1)),
                row["balance_status"] == "retrieved",
                row["terminal_reason"] == "below_threshold",
                row["terminal_reason"] == "max_hops",
                float(tx.get("tracked_ratio", 0.0)),
                min(int(tx.get("output_count", 0)) / 30.0, 1.0),
            ],
            dtype=np.float32,
        )
        text = f"{kind}: {row['id']}"
        node_indices[row["id"]] = builder.add_node(
            "bitcoin-mainnet", row["id"], _node_type(kind),
            float(row["x"]), float(row["y"]), 0.0,
            features=features, text=text,
        )

    tx_times = {row["txid"]: _timestamp(row["block_time"]) for row in data.transactions}
    for edge in data.edges:
        relation = 0 if edge["edge_type"] == "input_to_tx" else 1
        builder.add_edge(
            node_indices[str(edge["from"])], node_indices[str(edge["to"])], relation,
            time=tx_times.get(str(edge["spend_txid"]), 0.0),
            weight=float(edge["attributed_sats"]) / max(data.starting_sats, 1),
            flags=1 if edge["method"] == "proportional_after_commingling" else 0,
        )
    for tx_id, tx in tx_map.items():
        builder.add_event(
            node_indices[tx_id], _timestamp(tx["block_time"]), 0,
            values=(
                tx["input_sats"] / 100_000_000,
                tx["output_sats"] / 100_000_000,
                tx["fee_sats"] / 100_000_000,
                tx["tracked_input_sats"] / 100_000_000,
            ),
            flags=1 if tx["method"] == "proportional_after_commingling" else 0,
        )
    graph = builder.build()
    graph.save(root)
    loaded = SparseTemporalGraph.load(root, mmap=True, verify_hashes=True)
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    manifest["verification"] = {
        "hashes_verified_after_write": True,
        "loaded_counts": {"nodes": loaded.num_nodes, "edges": loaded.num_edges, "events": loaded.num_events},
        "ontology_file": "bitcoin_trace_ontology.json",
    }
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest
