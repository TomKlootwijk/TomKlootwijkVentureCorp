# Bitcoin UTXO follow-the-money package

Target: `3EKMtPc89gGsJHaCtcbWykT4zRLH6hTg9X`
Default period: 2020-01-01 through 2020-12-31 UTC.

## Important status

The ChatGPT execution environment that created this ZIP could verify the public explorer API specifications but could not retrieve the target address's live, non-indexed JSON endpoint. Therefore the included interim PDF and CSVs DO NOT invent downstream transactions or balances.

The included `trace_bitcoin.py` is the reproducible live tracer. Run it on any normal internet-connected machine to populate the trail directly from the public Bitcoin chain.

## Run it

### Windows

1. Install Python 3.10+.
2. Open Command Prompt in this folder.
3. Run:

```bat
python -m pip install -r requirements.txt
python trace_bitcoin.py --address 3EKMtPc89gGsJHaCtcbWykT4zRLH6hTg9X --from-date 2020-01-01 --to-date 2020-12-31 --out live_trace
```

### macOS / Linux

```bash
python3 -m pip install -r requirements.txt
python3 trace_bitcoin.py --address 3EKMtPc89gGsJHaCtcbWykT4zRLH6hTg9X --from-date 2020-01-01 --to-date 2020-12-31 --out live_trace
```

The `live_trace/` directory will contain:

- `bitcoin_follow_the_money_report.pdf`
- `trace_graph.png` and `trace_graph.graphml`
- `starting_utxos.csv`
- `transactions.csv`
- `flow_edges.csv`
- `terminal_outputs.csv`
- `addresses.csv` with current whole-address balances
- `summary.json`
- `raw/` JSON responses used as source evidence

## What 'money present in 2020' means

The tracer selects outputs paid to the target address that existed at any point between 2020-01-01 and 2020-12-31 UTC. That includes an output funded before 2020 if it was still unspent when 2020 began, and an output funded during 2020 if it existed for any part of the year.

## Evidence model

Bitcoin is UTXO-based. The spender of an outpoint is an exact on-chain fact. Once a tracked output is spent together with unrelated inputs, Bitcoin itself does not record which later output contains which original satoshis. The tracer therefore uses a proportional/haircut attribution after commingling and labels those edges `proportional_after_commingling`.

A downstream address's current balance is the balance of the entire address at retrieval time. It must not be read as the amount still attributable to the starting address, or as proof of who controls that address.

## Defaults and caps

- 4 downstream hops
- minimum attributed amount: 0.00001 BTC
- stops propagation through transactions with more than 30 outputs to avoid service/batch fan-out explosions
- up to 250 downstream address-balance lookups

All are configurable with command-line flags. Run `python trace_bitcoin.py --help` for options.

## Privacy

The report intentionally contains no date of birth, government/customer number, or other personal identifier. Those details are unnecessary for public-chain tracing.
