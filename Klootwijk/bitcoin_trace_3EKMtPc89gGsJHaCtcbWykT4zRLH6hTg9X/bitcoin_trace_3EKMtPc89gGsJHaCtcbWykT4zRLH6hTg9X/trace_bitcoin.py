#!/usr/bin/env python3
"""Reproducible Bitcoin UTXO follow-the-money tracer.

Public-chain analysis only. It follows UTXO spends from a target address and
uses proportional attribution only after tracked value is commingled with
untracked inputs. Current address balances are whole-address balances, not an
assertion of ownership or provenance.
"""
from __future__ import annotations

import argparse, csv, datetime as dt, hashlib, json, math, os, sys, time, textwrap
from collections import deque, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import requests
except Exception as e:
    raise SystemExit("Missing dependency 'requests'. Run: pip install -r requirements.txt") from e

SAT = 100_000_000
DEFAULT_BASE = "https://mempool.space/api"


def btc(sats: float | int | None) -> float | None:
    return None if sats is None else float(sats) / SAT


def iso(ts: int | None) -> str:
    if not ts:
        return ""
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).isoformat().replace("+00:00", "Z")


def short(s: str, n: int = 10) -> str:
    if len(s) <= n * 2 + 3:
        return s
    return s[:n] + "..." + s[-n:]


class Esplora:
    def __init__(self, base: str, raw_dir: Path, delay: float = 0.08, timeout: int = 30):
        self.base = base.rstrip("/")
        self.raw_dir = raw_dir
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.delay = delay
        self.timeout = timeout
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "bitcoin-utxo-trace-report/1.0"})
        self.cache: Dict[str, Any] = {}

    def get(self, path: str, cache_name: str | None = None) -> Any:
        if path in self.cache:
            return self.cache[path]
        url = self.base + path
        last_err = None
        for attempt in range(5):
            try:
                r = self.s.get(url, timeout=self.timeout)
                if r.status_code == 429:
                    time.sleep(min(2 ** attempt, 12))
                    continue
                r.raise_for_status()
                obj = r.json()
                self.cache[path] = obj
                if cache_name:
                    (self.raw_dir / cache_name).write_text(json.dumps(obj, indent=2), encoding="utf-8")
                time.sleep(self.delay)
                return obj
            except Exception as e:
                last_err = e
                time.sleep(min(2 ** attempt, 8))
        raise RuntimeError(f"GET {url} failed after retries: {last_err}")

    def address(self, address: str) -> Dict[str, Any]:
        return self.get(f"/address/{address}", f"address_{address}.json")

    def address_txs(self, address: str) -> List[Dict[str, Any]]:
        all_txs: List[Dict[str, Any]] = []
        first = self.get(f"/address/{address}/txs", f"address_{address}_txs_page0.json")
        all_txs.extend(first)
        confirmed = [t for t in first if t.get("status", {}).get("confirmed")]
        last = confirmed[-1]["txid"] if confirmed else None
        page = 1
        seen = {t["txid"] for t in all_txs}
        while last:
            batch = self.get(f"/address/{address}/txs/chain/{last}", f"address_{address}_txs_page{page}.json")
            if not batch:
                break
            new = [t for t in batch if t["txid"] not in seen]
            if not new:
                break
            all_txs.extend(new)
            seen.update(t["txid"] for t in new)
            last = new[-1]["txid"]
            page += 1
        return all_txs

    def tx(self, txid: str) -> Dict[str, Any]:
        safe = txid[:16]
        return self.get(f"/tx/{txid}", f"tx_{safe}.json")

    def outspends(self, txid: str) -> List[Dict[str, Any]]:
        safe = txid[:16]
        return self.get(f"/tx/{txid}/outspends", f"outspends_{safe}.json")


def outpoint(txid: str, vout: int) -> str:
    return f"{txid}:{vout}"


def prevout_address(vin: Dict[str, Any]) -> str:
    p = vin.get("prevout") or {}
    return p.get("scriptpubkey_address") or ("script:" + (p.get("scriptpubkey") or "unknown")[:24])


def vout_address(vo: Dict[str, Any]) -> str:
    return vo.get("scriptpubkey_address") or ("script:" + (vo.get("scriptpubkey") or "unknown")[:24])


def tx_time(tx: Dict[str, Any]) -> int | None:
    return tx.get("status", {}).get("block_time")


def starting_utxos_during_period(api: Esplora, address: str, start_ts: int, end_ts: int):
    txs = api.address_txs(address)
    candidates = []
    for tx in txs:
        fund_ts = tx_time(tx)
        if not fund_ts or fund_ts > end_ts:
            continue
        outs = api.outspends(tx["txid"])
        for idx, vo in enumerate(tx.get("vout", [])):
            if vo.get("scriptpubkey_address") != address:
                continue
            sp = outs[idx] if idx < len(outs) else {"spent": False}
            spend_tx = api.tx(sp["txid"]) if sp.get("spent") and sp.get("txid") else None
            spend_ts = tx_time(spend_tx) if spend_tx else None
            # UTXO existed at some point during requested interval.
            if spend_ts is None or spend_ts >= start_ts:
                candidates.append({
                    "outpoint": outpoint(tx["txid"], idx),
                    "funding_txid": tx["txid"], "vout": idx,
                    "value_sats": int(vo.get("value", 0)),
                    "funded_at": fund_ts, "spent": bool(sp.get("spent")),
                    "spend_txid": sp.get("txid"), "spent_at": spend_ts,
                })
    return txs, sorted(candidates, key=lambda x: (x["funded_at"], x["outpoint"]))


def trace(api: Esplora, address: str, roots: List[Dict[str, Any]], max_hops: int,
          min_attrib_sats: int, max_fanout: int):
    attrib: Dict[str, float] = {}
    depth: Dict[str, int] = {}
    origin_addr: Dict[str, str] = {}
    q = deque()
    for r in roots:
        attrib[r["outpoint"]] = float(r["value_sats"])
        depth[r["outpoint"]] = 0
        origin_addr[r["outpoint"]] = address
        q.append(r["outpoint"])

    processed_spends = set()
    edges: List[Dict[str, Any]] = []
    txrows: List[Dict[str, Any]] = []
    terminals: List[Dict[str, Any]] = []
    address_set = {address}

    while q:
        op = q.popleft()
        txid, n_s = op.split(":")
        n = int(n_s)
        d = depth[op]
        if d >= max_hops:
            terminals.append({"outpoint": op, "address": origin_addr.get(op, ""), "depth": d,
                              "attributed_sats": attrib[op], "reason": "max_hops"})
            continue
        osps = api.outspends(txid)
        sp = osps[n] if n < len(osps) else {"spent": False}
        if not sp.get("spent") or not sp.get("txid"):
            terminals.append({"outpoint": op, "address": origin_addr.get(op, ""), "depth": d,
                              "attributed_sats": attrib[op], "reason": "unspent"})
            continue
        spend_txid = sp["txid"]
        if spend_txid in processed_spends:
            continue
        tx = api.tx(spend_txid)

        total_in = sum(int((vin.get("prevout") or {}).get("value", 0)) for vin in tx.get("vin", []))
        total_out = sum(int(vo.get("value", 0)) for vo in tx.get("vout", []))
        tracked_in = 0.0
        tracked_inputs = []
        for vin in tx.get("vin", []):
            iop = outpoint(vin.get("txid", ""), int(vin.get("vout", 0)))
            if iop in attrib:
                tracked_in += attrib[iop]
                tracked_inputs.append((iop, attrib[iop], prevout_address(vin)))
        if total_in <= 0 or tracked_in <= 0:
            processed_spends.add(spend_txid)
            continue
        ratio = min(1.0, tracked_in / total_in)
        method = "fully_tracked" if math.isclose(ratio, 1.0, rel_tol=0, abs_tol=1e-12) else "proportional_after_commingling"
        fanout_stop = len(tx.get("vout", [])) > max_fanout
        txrows.append({
            "txid": spend_txid, "block_time": iso(tx_time(tx)), "block_height": tx.get("status", {}).get("block_height", ""),
            "input_sats": total_in, "output_sats": total_out, "fee_sats": int(tx.get("fee", total_in-total_out)),
            "tracked_input_sats": round(tracked_in, 8), "tracked_ratio": ratio, "method": method,
            "output_count": len(tx.get("vout", [])), "fanout_stop": fanout_stop,
        })
        for iop, ia, ia_addr in tracked_inputs:
            address_set.add(ia_addr)
            edges.append({
                "edge_type": "input_to_tx", "from": ia_addr, "to": "tx:" + spend_txid,
                "from_outpoint": iop, "to_outpoint": "", "spend_txid": spend_txid,
                "value_sats": "", "attributed_sats": round(ia, 8), "method": method,
                "depth": min(depth.get(iop, d), d),
            })
        for idx, vo in enumerate(tx.get("vout", [])):
            val = int(vo.get("value", 0))
            a = val * ratio
            dest = vout_address(vo)
            address_set.add(dest)
            new_op = outpoint(spend_txid, idx)
            edges.append({
                "edge_type": "tx_to_output", "from": "tx:" + spend_txid, "to": dest,
                "from_outpoint": "", "to_outpoint": new_op, "spend_txid": spend_txid,
                "value_sats": val, "attributed_sats": round(a, 8), "method": method,
                "depth": d + 1,
            })
            if a < min_attrib_sats:
                terminals.append({"outpoint": new_op, "address": dest, "depth": d+1,
                                  "attributed_sats": a, "reason": "below_threshold"})
                continue
            if fanout_stop:
                terminals.append({"outpoint": new_op, "address": dest, "depth": d+1,
                                  "attributed_sats": a, "reason": "high_fanout_stop"})
                continue
            # Keep the greatest attribution if paths reconverge at the same outpoint.
            if a > attrib.get(new_op, -1):
                attrib[new_op] = a
                depth[new_op] = d + 1
                origin_addr[new_op] = dest
                q.append(new_op)
        processed_spends.add(spend_txid)
    return edges, txrows, terminals, sorted(address_set)


def fetch_balances(api: Esplora, addresses: List[str], max_lookups: int):
    rows = []
    real = [a for a in addresses if not a.startswith("script:")]
    for i, a in enumerate(real):
        if i >= max_lookups:
            rows.append({"address": a, "balance_status": "lookup_cap_reached"})
            continue
        try:
            x = api.address(a)
            c = x.get("chain_stats", {}); m = x.get("mempool_stats", {})
            conf = int(c.get("funded_txo_sum", 0)) - int(c.get("spent_txo_sum", 0))
            mp = int(m.get("funded_txo_sum", 0)) - int(m.get("spent_txo_sum", 0))
            rows.append({
                "address": a, "confirmed_balance_sats": conf, "confirmed_balance_btc": btc(conf),
                "mempool_delta_sats": mp, "balance_including_mempool_sats": conf + mp,
                "balance_including_mempool_btc": btc(conf + mp),
                "chain_tx_count": c.get("tx_count", ""), "balance_status": "retrieved",
            })
        except Exception as e:
            rows.append({"address": a, "balance_status": "error", "error": str(e)})
    return rows


def write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str] | None = None):
    if fieldnames is None:
        keys = []
        for r in rows:
            for k in r:
                if k not in keys: keys.append(k)
        fieldnames = keys or ["status"]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def make_graph(outdir: Path, address: str, edges: List[Dict[str, Any]], max_nodes: int = 70):
    try:
        import matplotlib.pyplot as plt
        import networkx as nx
    except Exception as e:
        (outdir / "GRAPH_NOT_GENERATED.txt").write_text(f"Install matplotlib and networkx: {e}\n", encoding="utf-8")
        return None, None
    G = nx.DiGraph()
    for e in edges:
        a, b = e["from"], e["to"]
        G.add_node(a, kind="transaction" if a.startswith("tx:") else "address")
        G.add_node(b, kind="transaction" if b.startswith("tx:") else "address")
        G.add_edge(a, b, attributed_sats=float(e.get("attributed_sats") or 0), method=e.get("method", ""))
    nx.write_graphml(G, outdir / "trace_graph.graphml")
    if not G.nodes:
        G.add_node(address, kind="address")
    # Keep root plus highest-value nearby nodes for a readable static image.
    if len(G) > max_nodes:
        scores = defaultdict(float)
        for u, v, d in G.edges(data=True):
            scores[u] += d.get("attributed_sats", 0); scores[v] += d.get("attributed_sats", 0)
        keep = {address} | {n for n, _ in sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:max_nodes-1]}
        H = G.subgraph(keep).copy()
    else:
        H = G
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(H, seed=7, k=max(0.35, 2.0 / math.sqrt(max(len(H), 1))))
    labels = {n: ("TX\n" + short(n[3:], 6) if n.startswith("tx:") else short(n, 7)) for n in H}
    sizes = [1500 if n == address else (800 if n.startswith("tx:") else 950) for n in H]
    nx.draw_networkx_nodes(H, pos, node_size=sizes)
    nx.draw_networkx_edges(H, pos, arrows=True, width=1.0, alpha=0.6)
    nx.draw_networkx_labels(H, pos, labels=labels, font_size=6)
    plt.title("Bitcoin UTXO trace (static view; full graph in GraphML)")
    plt.axis("off"); plt.tight_layout()
    p = outdir / "trace_graph.png"; plt.savefig(p, dpi=180); plt.close()
    return p, outdir / "trace_graph.graphml"


def make_pdf(outdir: Path, address: str, period: str, summary: Dict[str, Any], roots, edges, txrows, balances, graph_path: Path | None):
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_LEFT
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
    except Exception as e:
        (outdir / "PDF_NOT_GENERATED.txt").write_text(f"Install reportlab: {e}\n", encoding="utf-8")
        return None
    pdf = outdir / "bitcoin_follow_the_money_report.pdf"
    doc = SimpleDocTemplate(str(pdf), pagesize=A4, rightMargin=14*mm, leftMargin=14*mm, topMargin=15*mm, bottomMargin=15*mm)
    st = getSampleStyleSheet()
    st.add(ParagraphStyle(name="Small", parent=st["BodyText"], fontSize=8, leading=10))
    st.add(ParagraphStyle(name="Tiny", parent=st["BodyText"], fontSize=6.7, leading=8))
    story = [Paragraph("Bitcoin Follow-the-Money Trace", st["Title"]),
             Paragraph(f"Target address: <font name='Courier'>{address}</font>", st["BodyText"]),
             Paragraph(f"Scope: UTXOs that existed at any point during {period}", st["BodyText"]),
             Paragraph(f"Generated: {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", st["BodyText"]), Spacer(1, 8)]
    story += [Paragraph("Executive summary", st["Heading2"]),
              Paragraph(f"Relevant starting UTXOs: {len(roots)}. Starting value in those UTXOs: {btc(sum(r['value_sats'] for r in roots)) or 0:.8f} BTC. Traced transaction nodes: {len(txrows)}. Recorded flow edges: {len(edges)}. Addresses/scripts encountered: {len(balances)}.", st["BodyText"]),
              Spacer(1, 5),
              Paragraph("Interpretation warning: Bitcoin tracks unspent transaction outputs (UTXOs), not tagged coins. Before commingling, an outpoint spend is an exact transaction fact. Once a spending transaction combines tracked and untracked inputs, this report uses proportional attribution only as a visualization heuristic. It is not proof that a specific later output, address, wallet, person, or service received the original coins.", st["Small"]),
              Spacer(1, 8)]
    if graph_path and graph_path.exists():
        story += [Paragraph("Flow graph", st["Heading2"]), Image(str(graph_path), width=180*mm, height=120*mm),
                  Paragraph("Static graph is intentionally capped for readability; trace_graph.graphml contains the full graph.", st["Small"]), PageBreak()]
    story += [Paragraph("Starting address profile", st["Heading2"])]
    prof = [["Metric", "Value"],
            ["Confirmed current balance", f"{summary.get('confirmed_balance_btc','')} BTC"],
            ["Balance incl. mempool", f"{summary.get('balance_including_mempool_btc','')} BTC"],
            ["Confirmed tx count", str(summary.get('chain_tx_count',''))],
            ["Address type", summary.get('address_type','')]]
    t=Table(prof, colWidths=[60*mm, 110*mm]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('GRID',(0,0),(-1,-1),0.25,colors.grey),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),('VALIGN',(0,0),(-1,-1),'TOP')]))
    story += [t, Spacer(1, 10), Paragraph("UTXOs present during the requested period", st["Heading2"])]
    root_data=[["Funding tx", "vout", "Funded", "Value BTC", "Spend tx", "Spent"]]
    for r in roots[:80]:
        root_data.append([short(r['funding_txid'],8), str(r['vout']), iso(r['funded_at'])[:10], f"{btc(r['value_sats']):.8f}", short(r.get('spend_txid') or 'unspent',8), iso(r.get('spent_at'))[:10]])
    rt=Table(root_data, repeatRows=1, colWidths=[34*mm,10*mm,24*mm,25*mm,34*mm,24*mm]); rt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('GRID',(0,0),(-1,-1),0.2,colors.grey),('FONTSIZE',(0,0),(-1,-1),6.5)]))
    story += [rt, PageBreak(), Paragraph("Encountered addresses and current balances", st["Heading2"]),
              Paragraph("Balances below are whole-address balances at retrieval time. They are not the amount attributable to the starting address and do not establish ownership.", st["Small"])]
    bal_data=[["Address", "Confirmed BTC", "Incl. mempool BTC", "Status"]]
    for r in balances[:160]:
        bal_data.append([short(r.get('address',''),12), str(r.get('confirmed_balance_btc','')), str(r.get('balance_including_mempool_btc','')), r.get('balance_status','')])
    bt=Table(bal_data, repeatRows=1, colWidths=[72*mm,35*mm,38*mm,30*mm]); bt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('GRID',(0,0),(-1,-1),0.2,colors.grey),('FONTSIZE',(0,0),(-1,-1),6.3)]))
    story += [bt, PageBreak(), Paragraph("Methodology and evidence levels", st["Heading2"]),
              Paragraph("1. Select outputs paid to the target address that existed at any point during the requested period. 2. Follow each selected outpoint to its exact spending transaction using the Esplora outspend endpoint. 3. If all input value of a downstream transaction is fully tracked, output values remain fully tracked (less the transaction fee). 4. If tracked value is mixed with outside inputs, allocate each output a proportional share equal to tracked input / total input. 5. Stop at unspent outputs, the hop limit, a small-value threshold, or high fan-out transactions.", st["BodyText"]),
              Spacer(1,5), Paragraph("Evidence levels: 'fully_tracked' means the transaction's input value is completely within the tracked lineage. 'proportional_after_commingling' is a heuristic, not a factual assignment of particular satoshis. Service/wallet identity is not inferred from address reuse or transaction shape alone.", st["Small"]),
              Spacer(1,10), Paragraph("Data sources", st["Heading2"]),
              Paragraph("Primary chain data: Mempool.space public Esplora-compatible REST API, with raw JSON snapshots saved in the raw/ folder. API base can be replaced with another compatible Esplora endpoint such as Blockstream's public API.", st["Small"]),
              Paragraph("This report deliberately excludes personal identifiers supplied outside the blockchain because they are not needed for the chain analysis.", st["Small"])]
    doc.build(story)
    return pdf


def main():
    ap=argparse.ArgumentParser(description="Trace Bitcoin UTXOs from an address and generate CSV/graph/PDF evidence files.")
    ap.add_argument("--address", required=True)
    ap.add_argument("--from-date", default="2020-01-01")
    ap.add_argument("--to-date", default="2020-12-31")
    ap.add_argument("--max-hops", type=int, default=4)
    ap.add_argument("--min-attributed-btc", type=float, default=0.00001)
    ap.add_argument("--max-fanout", type=int, default=30)
    ap.add_argument("--max-address-balance-lookups", type=int, default=250)
    ap.add_argument("--api-base", default=DEFAULT_BASE)
    ap.add_argument("--out", default="trace_output")
    args=ap.parse_args()
    outdir=Path(args.out); raw=outdir/"raw"; outdir.mkdir(parents=True, exist_ok=True)
    api=Esplora(args.api_base, raw)
    start_dt=dt.datetime.fromisoformat(args.from_date).replace(tzinfo=dt.timezone.utc)
    end_dt=dt.datetime.fromisoformat(args.to_date).replace(tzinfo=dt.timezone.utc)+dt.timedelta(days=1)-dt.timedelta(seconds=1)
    start_ts=int(start_dt.timestamp()); end_ts=int(end_dt.timestamp())

    addr_sum=api.address(args.address)
    c=addr_sum.get('chain_stats',{}); m=addr_sum.get('mempool_stats',{})
    conf=int(c.get('funded_txo_sum',0))-int(c.get('spent_txo_sum',0)); mp=int(m.get('funded_txo_sum',0))-int(m.get('spent_txo_sum',0))
    summary={"address":args.address,"confirmed_balance_sats":conf,"confirmed_balance_btc":btc(conf),"mempool_delta_sats":mp,"balance_including_mempool_sats":conf+mp,"balance_including_mempool_btc":btc(conf+mp),"chain_tx_count":c.get('tx_count',''),"address_type":"P2SH if the supplied address begins with 3 (validated separately in package metadata)"}
    txhist, roots=starting_utxos_during_period(api,args.address,start_ts,end_ts)
    edges, txrows, terminals, addresses=trace(api,args.address,roots,args.max_hops,int(args.min_attributed_btc*SAT),args.max_fanout)
    balances=fetch_balances(api,addresses,args.max_address_balance_lookups)
    write_csv(outdir/"starting_utxos.csv", roots)
    write_csv(outdir/"transactions.csv", txrows)
    write_csv(outdir/"flow_edges.csv", edges)
    write_csv(outdir/"terminal_outputs.csv", terminals)
    write_csv(outdir/"addresses.csv", balances)
    (outdir/"summary.json").write_text(json.dumps({"summary":summary,"period":{"from":args.from_date,"to":args.to_date},"counts":{"roots":len(roots),"transactions":len(txrows),"edges":len(edges),"addresses":len(addresses)}},indent=2),encoding="utf-8")
    graph_path,_=make_graph(outdir,args.address,edges)
    pdf=make_pdf(outdir,args.address,f"{args.from_date} through {args.to_date}",summary,roots,edges,txrows,balances,graph_path)
    print(json.dumps({"output":str(outdir.resolve()),"pdf":str(pdf) if pdf else None,"roots":len(roots),"transactions":len(txrows),"addresses":len(addresses)},indent=2))

if __name__ == "__main__":
    main()
