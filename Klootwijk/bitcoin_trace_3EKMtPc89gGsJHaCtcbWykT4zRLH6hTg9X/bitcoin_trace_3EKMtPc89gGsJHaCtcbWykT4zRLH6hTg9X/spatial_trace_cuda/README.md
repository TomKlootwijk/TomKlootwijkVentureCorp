# Bitcoin Spatial Trace CUDA

This application turns the evidence files in `live_trace/` into one consistent set of outputs:

- a self-contained interactive dashboard;
- a UGTS sparse temporal graph (`.npy` arrays plus hashes);
- CUDA-computed flow metrics and a measured CPU/GPU comparison;
- a plain-language PDF report;
- provenance and validation manifests.

The target is `3EKMtPc89gGsJHaCtcbWykT4zRLH6hTg9X`, and the requested observation window begins on 2020-06-05. The map is topological, not geographic. Bitcoin has no location field.

## Critical evidence boundary

The exact facts are the target output, the transaction that spent it, the later transaction inputs/outputs, block times, and current address state returned by the explorer. After a transaction mixes a tracked output with unrelated inputs, Bitcoin does not mark which later output contains the earlier satoshis. The supplied tracer therefore uses proportional (haircut) attribution. This is a transparent model, not proof of ownership, identity, service, criminality, or geographic location.

"Everything" can only mean every record captured inside the configured trace policy. The upstream evidence bundle used four downstream hops, a 1,000 satoshi attribution cutoff, a 30-output fan-out stop, and a 250-address balance lookup cap. Those limits are shown in every generated artifact. Re-run the upstream tracer with different limits to expand the evidence set.

## Build all outputs

From this directory:

```powershell
python -m pip install -e .
python -m spatial_trace build `
  --trace-dir ..\live_trace `
  --ugts-source "C:\Users\Tom\Documents\TomKlootwijkVentureCorp\Klootwijk\Spatial trace block chain\ugts_spatial_distill_v0.1.0" `
  --out .\output `
  --from-date 2020-06-05 `
  --to-date 2026-08-18 `
  --device cuda `
  --verify-live
```

Or run `build_all.ps1` with the defaults already configured for these folders.

Open `output/dashboard/index.html` directly in a browser. It has no server or external JavaScript dependency. Run the validation again with:

```powershell
python -m spatial_trace validate --output .\output
```

## Refresh the blockchain evidence

The application never silently changes the source evidence. To refresh, run the original reproducible tracer into a new folder, inspect its limits, and then point this builder at that folder:

```powershell
python ..\trace_bitcoin.py `
  --address 3EKMtPc89gGsJHaCtcbWykT4zRLH6hTg9X `
  --from-date 2020-06-05 `
  --to-date 2026-08-18 `
  --max-hops 4 `
  --min-attributed-btc 0.00001 `
  --max-fanout 30 `
  --max-address-balance-lookups 250 `
  --out ..\live_trace_refresh
```

Use a self-hosted Esplora server for repeated or larger traces. Public APIs can rate-limit bulk traversal.

## Output map

```text
output/
  dashboard/       editable HTML/CSS/JS explorer and data payload
  figures/         report charts
  pdf/             ELI5 report
  tables/          ranked nodes and terminal outputs
  ugts_graph/      UGTS sparse temporal arrays, ontology, manifest
  cuda_metrics.json
  dataset_summary.json
  provenance.json
  validation.json
```

## CUDA behavior

The analytics engine uses PyTorch tensor scatter operations and weighted PageRank on CUDA when available. It records the actual device, CUDA version, timing, and numerical agreement with the CPU result. For a graph this small, GPU startup and transfer overhead may make CUDA slower; the report does not hide that outcome.

## Sources

- Bitcoin transaction and UTXO model: https://developer.bitcoin.org/devguide/transactions.html
- Blockstream Esplora API contract: https://github.com/Blockstream/esplora/blob/master/API.md
- Live data endpoint used by the upstream bundle: https://mempool.space/api
