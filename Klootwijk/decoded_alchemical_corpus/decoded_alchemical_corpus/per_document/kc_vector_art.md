# KC Vector Graphical Art System

## Role in the corpus

This document returns the ideas to display and print output. It combines log-polar addressing, SDF geometry, one-bit masks, phase/amplitude language, temporal LED modulation, chromatic offsets and stochastic prepress screening.

## Established components

### Log-polar transform

`ρ=ln(√(x²+y²))`, `θ=atan2(y,x)`. Multiplicative radial scale becomes additive shift in `ρ`. This can simplify scale-like transforms around a chosen origin.

### Signed distance fields and CSG

A scalar field defines a zero boundary. The document gives standard min/max operations for union, intersection and subtraction. These operations define the correct implicit set but the result is not necessarily an exact Euclidean distance everywhere.

### One-bit temporal modulation

Pulse-density or delta-sigma modulation can represent average brightness using a high-rate bitstream. The panel, eye/camera integration and filtering determine the perceived or measured level.

### Dithering and prepress

Blue-noise thresholding, anisotropic screening, CMYK separation and dot-gain compensation are real print/imaging concepts. A log-polar, radius-dependent screen is a plausible design experiment, not a standard validated workflow.

## Unvalidated terminology

“Feynman vectors” are not formally defined. The closest established objects are complex phasors or wave amplitudes. A valid implementation would need:

- a state space and units;
- phase and magnitude definitions;
- path or sampling measure;
- accumulation rule;
- threshold/output rule;
- error and convergence analysis.

Calling the accumulator “Feynman” does not make the display quantum mechanical.

## Chromatic-aberration claim

A constant offset in log radius can approximate pure wavelength-dependent magnification. It cannot correct arbitrary longitudinal/lateral chromatic aberration, field curvature or wavelength-dependent point-spread functions. It also requires calibration and computation, so “zero cost” is not literal.

## Rasterization boundary

Even if geometry is represented analytically, a conventional screen or printing plate is a discrete output device. The system may improve how analytic geometry is sampled, but final LEDs/ink dots remain rasterized. This is consistent with the mature corpus: projection can be downstream without defining the substrate.

## Page anchors

Log-polar/SDF/Feynman vector pipeline: pp. 1-3. LED PDM/delta-sigma: pp. 4-6. Chromatic handling: pp. 7-8. One-bit prepress screening and dot gain: pp. 8-10.
