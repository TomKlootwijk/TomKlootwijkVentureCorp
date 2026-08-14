# Computer-Graphics Projection Adapter

## Boundary rule

The relation/event substrate is authoritative. A screen image, vector page, print plate, mesh, or sampled volume is a materialized view produced for a particular query and display policy.

## Input

A projection adapter consumes:

- query result states and events;
- a camera or local support definition;
- display/print resolution and uncertainty policy;
- optional implicit geometry functions;
- a color, phase, or mode transfer function.

## Source-derived KC adapter

The KC Vector Graphical Art System can be normalized as this downstream pipeline:

```text
query result / implicit boundary
    -> local log-polar address (rho, theta)
    -> SDF/CSG evaluation
    -> phase-amplitude edge accumulation
    -> quantization policy
    -> screen PDM / spatial dither / prepress halftone
```

### SDF operators

- union: `min(f1, f2)`
- intersection: `max(f1, f2)`
- subtraction: `max(f1, -f2)`
- boundary: `f(p)=0`

### Terminology correction

The source calls the phase-amplitude samples "Feynman vectors," but it does not supply a path-integral derivation. The safe technical name in this package is **phase-amplitude edge accumulator**.

### Output modes

1. **Screen**: temporal 1-bit pulse-density modulation, optionally combined with anisotropic dithering.
2. **Vector/analytic**: retain implicit curves and event loci directly when the target supports them.
3. **Print**: CMYK conversion, log-polar blue-noise thresholding, SDF edge locking, and dot-gain compensation.

## Non-goals

- The adapter does not define world identity or event truth.
- A projection artifact must not mutate the authoritative state.
- Visual quality is not evidence that the query substrate is correct.
- The adapter does not eliminate physical pixel, refresh, color, or print constraints.

Source anchors: S1 pp. 9-10; S7 pp. 1-10.
