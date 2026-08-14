# Membrane World Zero - prototype specification

## Question

Can a bounded event-and-lineage representation detect and act on membrane state changes with less data or earlier useful warning than fixed-rate logging, at equal false/missed-event limits?

## Physical setup

- Cross-flow or dead-end bench cell with a well-characterized commercial membrane.
- Pressure, flow, permeate mass/volume, conductivity, temperature, and optional optical imaging.
- Three surface conditions: unmodified baseline; hydroxyl-rich coating/analogue; derivatized coating.
- Conventional fixed-rate logger retained as the reference path.

## State vector

`q(t) = [J, TMP, Q_cross, conductivity, temperature, R_membrane, R_fouling, optical_features, topology_features, chemistry_lot, calibration_state, confidence]`

## Local support

A sensor reading is admitted only if its spatial/temporal channel, calibration interval, and membrane region are declared active. Optional radial-angular support is used only for optical or local probe geometry.

## Compatibility

`chi = sensor_valid AND channel_aligned AND chemistry_lot_known AND time_window_valid AND policy_allowed`

## Guards

- `g_flux`: statistically significant flux slope or level crossing.
- `g_pressure`: TMP rise beyond model-predicted uncertainty.
- `g_breakthrough`: conductivity or tracer crossing.
- `g_topology`: persistence-diagram distance or connected-pore descriptor crossing.
- `g_clean`: recovery after cleaning reaches/fails target.
- `g_drift`: calibration residual exceeds limit.

## Event record

Each event stores timestamp interval, guard, pre/post state, confidence, sensor provenance, material batch/functionalization, calibration version, action, and linked raw-data segment.

## Baselines

1. Fixed-rate time series with standard thresholding.
2. Conventional resistance-in-series or fitted fouling model.
3. Optional stochastic greybox digital twin.

## Success criteria

- equal or lower false/missed-event rates;
- earlier detection of fouling or breakthrough;
- lower stored/transmitted data per correct decision;
- stable lineage and replay;
- total energy and calibration overhead reported;
- no claim of advantage unless a matched baseline is beaten.

## Kill criteria

- event logic adds no decision value over fixed-rate data;
- calibration and synchronization dominate cost;
- surface coating causes unacceptable flux/selectivity loss, swelling, delamination, or extractables;
- topology descriptors are unstable or unrelated to operational outcomes.
