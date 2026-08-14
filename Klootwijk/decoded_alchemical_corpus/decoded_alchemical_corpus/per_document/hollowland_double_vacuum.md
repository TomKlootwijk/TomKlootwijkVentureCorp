# Hollowland Double Vacuum

## Role in the corpus

This document is the generative vocabulary source. It begins with ordinary and quantum-vacuum language, moves through Klein bottles and sphere eversion, then assembles log-polar coordinates, SDFs, phase, one-bit routing, eigenvectors and an hourglass into a speculative “closed-form state engine.”

## Actual mathematical and physical knowledge

### Vacuum

A physical vacuum is a region of pressure below a reference level or, in quantum-field language, a lowest-energy state rather than literal philosophical nothingness. “Double vacuum” has no standard physical meaning. The later corpus resolves the phrase as **absence of coupling**, not stronger emptiness.

### Klein bottle

A Klein bottle is a closed non-orientable surface. A common 3D visualization self-intersects; a true embedding requires four spatial dimensions. It has no boundary as a mathematical surface, but this does not give a physical container that can hold a “vacuum inside a vacuum.” For engineering, the useful part is an orientation-reversing gluing rule.

### Sphere eversion

Sphere eversion is a regular homotopy that turns an immersed sphere inside out while permitting self-intersections. It is valid topology but not a literal deformation of an ordinary rigid shell.

### Log-polar coordinates

The useful transform is `ρ = ln r`, `θ = atan2(y,x)`. Radial scaling becomes translation in `ρ`. This can support multiscale/foveated indexing, but it has an origin singularity, sampling issues and metric distortion.

### Signed distance fields

An SDF is defined on both sides of a surface; zero is the boundary. On a non-orientable manifold a global sign requires an orientation cover or local-chart convention. The document’s proposed bit flip is therefore a routing convention, not an automatic theorem.

### Eigenvectors and eigenvalues

`Av=λv` is used as an “on-course” metaphor. The actual content is that an eigenvector’s direction is preserved by a linear map. Rank loss or a zero eigenvalue can mark a degenerate transition, but it does not automatically erase physical entities or noise.

## Useful architectural synthesis

The most productive decoding is:

1. log-polar or spherical support selects a local candidate domain;
2. an implicit relation/SDF defines a potential crossing;
3. a compatibility predicate filters phase/sheet/mode;
4. a root solver finds the event time;
5. an hourglass/transition table routes the state;
6. parity and lineage are updated.

## Unsupported claims

The document repeatedly asserts constant-time infinite-horizon solving, zero memory, exact collision prediction, automatic AI compression and universal physical simulation. Those claims are not derived. General nonlinear systems may have dense events, multiple roots, chaos, singularities and expression growth.

The document also treats the golden ratio as a phase governor with automatic anti-recurrence properties. Irrational rotations can reduce exact recurrence in ideal arithmetic, but finite precision and dynamical instability remain.

## Files in this package

- `structures/geometry/klein_bottle_immersion.obj`
- `structures/geometry/klein_bottle_immersion_preview.png`
- `structures/geometry/mobius_strip.obj`
- `structures/geometry/double_cone_hourglass.obj`
- `structures/geometry/log_polar_grid.svg`
- `structures/geometry/sdf_event_surface.svg`

## Page anchors

Vacuum and Klein bottle: pp. 1-11. Log-polar/Klein/SDF synthesis: pp. 12-19. Eigenvectors and hourglass: pp. 20-25. Kinematics, grammar, GPU and AI extensions: pp. 26-36.
