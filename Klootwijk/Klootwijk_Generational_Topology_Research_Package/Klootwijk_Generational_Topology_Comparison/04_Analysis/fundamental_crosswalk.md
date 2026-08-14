# Fundamental crosswalk: chemistry as constrained graph transformation

## The strongest common grammar

The most defensible overlap is a five-stage grammar:

1. **Support/accessibility:** the potential reactants or relations must be reachable in the active domain.
2. **Compatibility:** complementary types, functional groups, modes, phases, or policies must match.
3. **Event:** a guard or chemical condition is crossed.
4. **Transition:** connectivity and state are updated.
5. **Lineage/closure:** the resulting state is recorded, stabilized, or terminated.

In Arie's process, solvent quality keeps phenolic and epoxide functions accessible; near-equimolarity and difunctionality provide matching; ring opening is the local event; a new covalent edge and hydroxyl are created; and stoichiometric excess, chain stopper, precipitation, or cooling closes growth. In Tom's mature corpus, local spherical support and compatibility predicates admit a relation; a root or measured guard is reached; a transition operator routes the state; and lineage/invariants plus an event log preserve history.

## Why the overlap is real but limited

Chemistry is already a form of graph transformation: molecular graphs are rewritten through local bond-breaking and bond-forming rules. Yet the physical implementation is not a clean symbolic interpreter. It is a stochastic many-body process with distributions, activation barriers, mass transport, solvent effects, side reactions, and thermal history. A software event can be atomic by definition; a reaction event is embedded in a population and may be reversible or competing.

The corpus is therefore strongest when used as a **control and representation layer around chemistry**, not as a replacement for chemistry. A useful formal stack is:

- reaction graph and material balances;
- transport and phase-state model;
- measured observables;
- bounded compatibility/guard logic;
- event and lineage store;
- query and decision layer.

## Key non-equivalences

- Equimolarity is not a hidden geometric symmetry. It is a global functional-group balance that determines the attainable degree of polymerization.
- The sulfone bridge is not a communication bit. It is a polar covalent group that changes chain rigidity, dipole moment, packing, solubility, thermal behavior, and interfacial interactions.
- SDF = 0 is not a reaction mechanism. It can be a useful representation of a measured boundary or event surface.
- A one-bit route flag is not the material state. Conversion, composition, chain-length distribution, morphology, temperature, uncertainty, and residuals remain continuous or high-dimensional.
- A chain end is not automatically an ontological UUID. Polymer populations need statistical identity plus batch/process lineage.
