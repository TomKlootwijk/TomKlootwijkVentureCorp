from __future__ import annotations

import json
from pathlib import Path
import shutil
from typing import Any

from .io import TraceData


def build_dashboard(output: Path, data: TraceData, analysis: dict[str, Any], summary: dict[str, Any]) -> Path:
    root = output / "dashboard"
    root.mkdir(parents=True, exist_ok=True)
    tx_times = {row["txid"]: row["block_time"] for row in data.transactions}
    payload = {
        "summary": summary,
        "nodes": analysis["nodes"],
        "edges": [
            {
                "source": row["from"],
                "target": row["to"],
                "edge_type": row["edge_type"],
                "attributed_sats": row["attributed_sats"],
                "value_sats": row["value_sats"],
                "method": row["method"],
                "depth": row["depth"],
                "spend_txid": row["spend_txid"],
                "block_time": tx_times.get(row["spend_txid"], ""),
            }
            for row in data.edges
        ],
        "transactions": data.transactions,
        "starting_utxos": data.roots,
        "terminals": data.terminals,
    }
    (root / "trace_data.js").write_text(
        "window.TRACE_DATA = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    templates = Path(__file__).with_name("templates")
    for name in ("index.html", "styles.css", "app.js"):
        shutil.copyfile(templates / name, root / name)
    return root / "index.html"
