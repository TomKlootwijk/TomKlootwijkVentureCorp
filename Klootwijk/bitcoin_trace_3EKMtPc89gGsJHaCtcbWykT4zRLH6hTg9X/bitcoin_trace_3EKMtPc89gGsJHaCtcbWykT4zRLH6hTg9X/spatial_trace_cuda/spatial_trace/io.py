from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED_FILES = (
    "starting_utxos.csv",
    "transactions.csv",
    "flow_edges.csv",
    "terminal_outputs.csv",
    "addresses.csv",
    "summary.json",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def _int(value: str | None, default: int = 0) -> int:
    if value in (None, ""):
        return default
    return int(Decimal(value))


def _float(value: str | None, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    return float(Decimal(value))


def _bool(value: str | None) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


@dataclass
class TraceData:
    root: Path
    roots: list[dict[str, Any]]
    transactions: list[dict[str, Any]]
    edges: list[dict[str, Any]]
    terminals: list[dict[str, Any]]
    addresses: list[dict[str, Any]]
    upstream_summary: dict[str, Any]
    source_hashes: dict[str, str]
    raw_evidence: dict[str, Any]

    @property
    def target_address(self) -> str:
        return str(self.upstream_summary["summary"]["address"])

    @property
    def starting_sats(self) -> int:
        return sum(int(row["value_sats"]) for row in self.roots)


def load_trace(directory: str | Path) -> TraceData:
    root = Path(directory).resolve()
    missing = [name for name in REQUIRED_FILES if not (root / name).is_file()]
    if missing:
        raise FileNotFoundError(f"trace directory is missing: {', '.join(missing)}")

    roots = _rows(root / "starting_utxos.csv")
    transactions = _rows(root / "transactions.csv")
    edges = _rows(root / "flow_edges.csv")
    terminals = _rows(root / "terminal_outputs.csv")
    addresses = _rows(root / "addresses.csv")

    for row in roots:
        row.update(
            value_sats=_int(row.get("value_sats")),
            vout=_int(row.get("vout")),
            funded_at=_int(row.get("funded_at")),
            spent_at=_int(row.get("spent_at")),
            spent=_bool(row.get("spent")),
        )
    for row in transactions:
        row.update(
            block_height=_int(row.get("block_height")),
            input_sats=_int(row.get("input_sats")),
            output_sats=_int(row.get("output_sats")),
            fee_sats=_int(row.get("fee_sats")),
            tracked_input_sats=_float(row.get("tracked_input_sats")),
            tracked_ratio=_float(row.get("tracked_ratio")),
            output_count=_int(row.get("output_count")),
            fanout_stop=_bool(row.get("fanout_stop")),
        )
    for row in edges:
        row.update(
            value_sats=_int(row.get("value_sats")),
            attributed_sats=_float(row.get("attributed_sats")),
            depth=_int(row.get("depth")),
        )
    for row in terminals:
        row.update(
            depth=_int(row.get("depth")),
            attributed_sats=_float(row.get("attributed_sats")),
        )
    for row in addresses:
        row.update(
            confirmed_balance_sats=_int(row.get("confirmed_balance_sats")),
            mempool_delta_sats=_int(row.get("mempool_delta_sats")),
            balance_including_mempool_sats=_int(row.get("balance_including_mempool_sats")),
            chain_tx_count=_int(row.get("chain_tx_count")),
        )

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    source_hashes = {name: sha256_file(root / name) for name in REQUIRED_FILES}
    raw_dir = root / "raw"
    raw_files = sorted(raw_dir.glob("*.json")) if raw_dir.is_dir() else []
    raw_evidence = {
        "directory": str(raw_dir),
        "json_file_count": len(raw_files),
        "total_bytes": sum(path.stat().st_size for path in raw_files),
        "aggregate_sha256": _aggregate_hash(raw_files),
    }
    data = TraceData(root, roots, transactions, edges, terminals, addresses, summary, source_hashes, raw_evidence)
    validate_trace(data)
    return data


def _aggregate_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.name.encode("utf-8"))
        digest.update(bytes.fromhex(sha256_file(path)))
    return digest.hexdigest()


def validate_trace(data: TraceData) -> None:
    if not data.roots:
        raise ValueError("trace contains no starting UTXO")
    target = data.target_address
    if any(not row.get("outpoint") for row in data.roots):
        raise ValueError("a starting UTXO has no outpoint")
    if any(row["edge_type"] not in {"input_to_tx", "tx_to_output"} for row in data.edges):
        raise ValueError("unsupported edge type")
    txids = {row["txid"] for row in data.transactions}
    referenced = {row["spend_txid"] for row in data.edges if row.get("spend_txid")}
    if not referenced.issubset(txids):
        raise ValueError("flow edges reference a transaction missing from transactions.csv")
    target_rows = [row for row in data.addresses if row.get("address") == target]
    if len(target_rows) != 1:
        raise ValueError("addresses.csv must contain the target exactly once")
    root_total = data.starting_sats
    terminal_total = sum(row["attributed_sats"] for row in data.terminals)
    if terminal_total > root_total + 1.0:
        raise ValueError("terminal attribution exceeds the starting value")


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
