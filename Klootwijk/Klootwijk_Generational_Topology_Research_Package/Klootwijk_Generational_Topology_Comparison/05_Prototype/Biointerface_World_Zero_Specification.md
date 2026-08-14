# Biointerface World Zero - prototype specification

## Question

Can a chemically addressable surface plus event-based and topological readout distinguish biologically meaningful adhesion, spreading, aggregation, or detachment events with lower bandwidth and traceable material history?

## Surface set

- inert/control substrate;
- hydroxyl-rich sulfone polyether or close safe analogue;
- one antifouling derivatization;
- one affinity/cell-adhesive derivatization.

## Assays

Begin with non-clinical in-vitro screens: protein adsorption, model cells or platelets as appropriate, viability/cytotoxicity, adhesion force/detachment, and sterilization/aging effects. Selection depends on intended contact category.

## Sensing

- event camera or sparse optical-change detector for fast changes;
- periodic conventional images as the ground truth/reference;
- optional impedance, fluorescence, or force readout;
- surface/batch/sterilization lineage attached to every sample.

## State and topology

`q(t) = [object_count, velocity, adhesion_area, shape_features, cluster_graph, persistence_descriptors, fluorescence/impedance, surface_state, uncertainty]`

Persistent homology or related descriptors track connected clusters, loops, and voids in cell/biofilm morphology. Sheaf-style consistency checks can reconcile local optical, electrical, and chemical measurements.

## Example guards

- first stable attachment;
- spreading area exceeds threshold for a declared duration;
- aggregate merges/splits;
- detachment impulse;
- biofilm/pore topology changes class;
- sensor disagreement or drift invalidates an event.

## Success criteria

- event-derived phenotype agrees with reference imaging/assay;
- lower bandwidth or latency at equal classification error;
- surface chemistry effects are reproducible across batches;
- extractables/leachables and cytotoxicity are within the intended research boundary;
- all decisions are replayable from the event and provenance log.

## Kill criteria

- event camera misses slow or low-contrast biology without a dense reference;
- topology descriptors do not add predictive value;
- biological variability exceeds surface or event-model effect;
- final processed surface fails chemical or biological safety screens.
