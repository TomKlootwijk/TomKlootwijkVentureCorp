#!/usr/bin/env python3
"""Build data tables, analysis notes, figures, and small reproducible prototypes.

This script is intentionally self-contained. It does not download anything and can be
re-run from the unpacked research package.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import random
import shutil
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "02_Data"
FIG = ROOT / "03_Figures"
ANALYSIS = ROOT / "04_Analysis"
PROTO = ROOT / "05_Prototype"
REFS = ROOT / "06_References"
BUILD = ROOT / "07_Build"

for d in (DATA, FIG, ANALYSIS, PROTO, REFS, BUILD):
    d.mkdir(parents=True, exist_ok=True)

# Report palette (chosen for print legibility and deuteranopia-aware contrast).
NAVY = "#0B2A3D"
TEAL = "#148C9B"
GOLD = "#D7A51F"
CORAL = "#C8665A"
GREEN = "#3B8D70"
PURPLE = "#695C9C"
LIGHT = "#EAF2F4"
MID = "#B6C8CF"
DARK = "#243640"
GREY = "#6E7C84"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.labelsize": 10,
    "figure.dpi": 160,
    "savefig.dpi": 220,
})


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def write_text(path: Path, text: str) -> None:
    path.write_text(text.strip() + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Core comparison data
# ---------------------------------------------------------------------------
comparison_rows = [
    {
        "Dimension": "Primary object",
        "Arie_1959_technique": "A population of difunctional molecules and growing polymer chains",
        "Tom_current_technique": "A finite grammar over directly queryable states, relations, phases, sheets, addresses, and branches",
        "Genuine_overlap": "Both replace an inventory-first description with rules that generate connectivity",
        "Critical_difference": "Molecular reactions are stochastic, irreversible, and thermodynamically constrained; the corpus is a symbolic architecture",
        "Present_day_opportunity": "Typed graph rewriting linked to measured chemistry and digital lineage",
        "Evidence_Arie": "Issued patent plus working examples",
        "Evidence_Tom": "Conceptual synthesis and prototype specifications",
    },
    {
        "Dimension": "Topology controlled",
        "Arie_1959_technique": "Molecular graph topology: nearly linear chains, low branching, controlled end groups",
        "Tom_current_technique": "Operational topology: supports, compatibility sectors, transition surfaces, routing, and lineage",
        "Genuine_overlap": "Connectivity changes only through admissible local operations",
        "Critical_difference": "One concerns covalent bonds; the other concerns information and state coupling",
        "Present_day_opportunity": "Multiscale models linking molecular, pore, interface, and information topology",
        "Evidence_Arie": "Directly embodied in chemistry",
        "Evidence_Tom": "Formally promising but not yet materially validated",
    },
    {
        "Dimension": "Matching condition",
        "Arie_1959_technique": "Near-equimolar complementary functionality with effective salt accounting",
        "Tom_current_technique": "Compatibility predicate chi over phase, sheet, address, mode, policy, or support",
        "Genuine_overlap": "High-value interactions are gated by type and balance rather than mere co-location",
        "Critical_difference": "Stoichiometric equivalence is a quantitative global conservation constraint, not a Boolean geometry metaphor",
        "Present_day_opportunity": "Use explicit conservation laws inside compatibility predicates",
        "Evidence_Arie": "Quantitative process window",
        "Evidence_Tom": "Explicit logical abstraction",
    },
    {
        "Dimension": "Local event",
        "Arie_1959_technique": "Phenoxide attack and epoxide ring opening form an ether bond and secondary alcohol",
        "Tom_current_technique": "A relation reaches an event surface under support and compatibility constraints",
        "Genuine_overlap": "A localized event changes connectivity and state",
        "Critical_difference": "Chemical event rates depend on kinetics, diffusion, activation, and concentrations",
        "Present_day_opportunity": "Reaction-aware hybrid automata and event-sourced chemistry models",
        "Evidence_Arie": "Known chemical mechanism",
        "Evidence_Tom": "Architecture-level event semantics",
    },
    {
        "Dimension": "Operator or catalyst",
        "Arie_1959_technique": "Alkaline phenoxide catalysis; the phenolic salt also affects functionality bookkeeping",
        "Tom_current_technique": "Transition operator T_j with context and routing state",
        "Genuine_overlap": "The operator changes what transitions are reachable without being the final product state",
        "Critical_difference": "Catalysis changes reaction rates and sometimes composition; symbolic operators need not consume material",
        "Present_day_opportunity": "Stateful catalytic models with mass-balance-aware event logs",
        "Evidence_Arie": "Specified catalyst ranges and examples",
        "Evidence_Tom": "General transition formalism",
    },
    {
        "Dimension": "Accessibility or support",
        "Arie_1959_technique": "Solvent keeps monomers and product mutually accessible; crystallization removes reactive chains",
        "Tom_current_technique": "Cone/hourglass/local spherical support limits relevant relations",
        "Genuine_overlap": "An entity can be present yet operationally unavailable",
        "Critical_difference": "Solubility and phase separation are physical fields, not just query pruning",
        "Present_day_opportunity": "Support predicates parameterized by transport, concentration, and phase state",
        "Evidence_Arie": "Central patent claim",
        "Evidence_Tom": "Mature corpus correction",
    },
    {
        "Dimension": "Boundary",
        "Arie_1959_technique": "Phase boundary, precipitation, glass/crystal transition, and reaction endpoint",
        "Tom_current_technique": "SDF = 0 or B = 0 as an explicit transition surface",
        "Genuine_overlap": "Boundary crossing is treated as an event rather than only a location",
        "Critical_difference": "A signed distance field is a representation; a chemical phase boundary follows thermodynamics and kinetics",
        "Present_day_opportunity": "Measured guards tied to physical observables and uncertainty",
        "Evidence_Arie": "Observed crystallization/viscosity/thermal behavior",
        "Evidence_Tom": "Explicit event-surface semantics",
    },
    {
        "Dimension": "One-bit role",
        "Arie_1959_technique": "No literal one-bit state; practical binary distinctions include reacted/unreacted or soluble/precipitated",
        "Tom_current_technique": "Parity, route, validity, freshness, or compatible/incompatible flag",
        "Genuine_overlap": "Binary flags can summarize a transition outcome",
        "Critical_difference": "A bit cannot carry concentration, uncertainty, chain length, or morphology",
        "Present_day_opportunity": "Keep one-bit control narrow and retain continuous state alongside it",
        "Evidence_Arie": "Not claimed",
        "Evidence_Tom": "Explicitly narrowed in Spherical Throughput",
    },
    {
        "Dimension": "Identity and lineage",
        "Arie_1959_technique": "Batch, monomer lot, chain population, and reaction history determine material state",
        "Tom_current_technique": "Generative address plus invariant/event history preserves identity",
        "Genuine_overlap": "History matters to present function",
        "Critical_difference": "Individual polymer chains are statistical and not naturally persistent UUID-bearing objects",
        "Present_day_opportunity": "Digital material passports and batch-to-device lineage",
        "Evidence_Arie": "Implicit through process history",
        "Evidence_Tom": "Explicit design principle",
    },
    {
        "Dimension": "Termination and closure",
        "Arie_1959_technique": "Controlled stoichiometric excess, chain stopper, precipitation, or cooling ends growth",
        "Tom_current_technique": "Transition, branch resolution, log append, and invariant update close an event",
        "Genuine_overlap": "The system needs explicit closure to prevent uncontrolled continuation",
        "Critical_difference": "Chemical termination changes molecular composition and distributions",
        "Present_day_opportunity": "End-state schemas that include material and computational closure",
        "Evidence_Arie": "Example 4 chain stopping",
        "Evidence_Tom": "Transition/log architecture",
    },
    {
        "Dimension": "Uncertainty",
        "Arie_1959_technique": "Impurities, conversion, side reactions, measurement variance, and molecular-weight distributions",
        "Tom_current_technique": "Set-valued answers, confidence, certified root solving, and event uncertainty in mature documents",
        "Genuine_overlap": "Useful operation requires bounded uncertainty",
        "Critical_difference": "Early corpus rhetoric sometimes treated analytic form as automatic exactness",
        "Present_day_opportunity": "Probabilistic or interval-valued guards tied to calibration data",
        "Evidence_Arie": "Experimental but historically limited characterization",
        "Evidence_Tom": "Explicitly recognized as a requirement",
    },
    {
        "Dimension": "Scaling claim",
        "Arie_1959_technique": "Scale depends on mixing, heat removal, solution viscosity, phase stability, and purification",
        "Tom_current_technique": "Potential horizon-independent state queries for fixed closed expressions",
        "Genuine_overlap": "Avoiding premature materialization can reduce cost",
        "Critical_difference": "Universal O(1), zero memory, or no broad phase is unsupported; combinatorics and exogenous novelty remain",
        "Present_day_opportunity": "Benchmark restricted relation families against frame-stepped and indexed baselines",
        "Evidence_Arie": "Process-engineering constraints",
        "Evidence_Tom": "Hypothesis with stated bottlenecks",
    },
    {
        "Dimension": "Outputs",
        "Arie_1959_technique": "Thermoplastic films, fibres, mouldings, coatings, and reactive hydroxyl-rich material",
        "Tom_current_technique": "State-at-time, next-event, reachable-relation, identity, sensing, and verified B.C.E. outputs",
        "Genuine_overlap": "Both create a platform whose value lies in downstream interfaces",
        "Critical_difference": "One output is matter; the other is a query/decision architecture",
        "Present_day_opportunity": "Smart interfaces whose material state and digital state are co-designed",
        "Evidence_Arie": "Demonstrated specimens and properties",
        "Evidence_Tom": "Prototype-level architecture",
    },
    {
        "Dimension": "Biomedical relevance",
        "Arie_1959_technique": "Pendant hydroxyls offer derivatization handles; sulfone raises polarity and thermal stability",
        "Tom_current_technique": "Compatibility-gated sensing, event logging, topology descriptors, and digital twins",
        "Genuine_overlap": "Interface function can be encoded chemically and monitored operationally",
        "Critical_difference": "The patent does not establish biocompatibility, membrane selectivity, or biological mechanism",
        "Present_day_opportunity": "Chemically addressable membrane/biointerface plus event-sourced digital twin",
        "Evidence_Arie": "Material-platform inference",
        "Evidence_Tom": "Architecture opportunity",
    },
]
write_csv(DATA / "comparison_matrix.csv", list(comparison_rows[0].keys()), comparison_rows)


topology_rows = [
    {
        "Layer": "1. Molecular graph topology",
        "Meaning": "Atoms, bonds, functionality, chain branching, cycles, and end groups",
        "Arie": "Directly controlled through difunctionality, stoichiometry, solvent, purity, and catalysis",
        "Tom": "Best treated as an external physical layer, not replaced by phase or routing metaphors",
        "Useful_methods": "Reaction-network graphs, graph rewriting, molecular simulation, spectroscopy, chromatography",
        "Failure_if_confused": "Calling operational sheets or SDF signs a molecular mechanism",
    },
    {
        "Layer": "2. Morphology and phase topology",
        "Meaning": "Crystals, amorphous domains, pores, connected phases, percolation, and interfaces",
        "Arie": "Crystallization can prematurely stop polymerization; solid-state morphology controls properties",
        "Tom": "Phase sheets and double-vacuum language can model uncoupled domains if physically typed",
        "Useful_methods": "Microscopy, scattering, DSC, tomography, percolation, persistent homology",
        "Failure_if_confused": "Treating a phase label as proof of physical separation or transport isolation",
    },
    {
        "Layer": "3. Interface and transport topology",
        "Meaning": "Which surfaces, pores, modes, analytes, cells, or channels can exchange mass, charge, energy, or information",
        "Arie": "Pendant OH groups and polar sulfone motifs create chemical handles and interfacial affinity",
        "Tom": "Local support and compatibility predicates are strongest here",
        "Useful_methods": "Transport PDEs, adsorption kinetics, surface chemistry, coupled-mode theory, microfluidics",
        "Failure_if_confused": "Assuming co-location guarantees coupling or that coupling is cost-free",
    },
    {
        "Layer": "4. Operational and information topology",
        "Meaning": "Queries, guards, events, routing, lineage, provenance, and consistency among local views",
        "Arie": "Only implicit through process recipes, batch history, and endpoint measurements",
        "Tom": "Primary strength: relation algebra, B.C.E. guards, event logs, lineage, and query-first architecture",
        "Useful_methods": "Hybrid automata, sheaves, event sourcing, temporal databases, formal verification",
        "Failure_if_confused": "Claiming that an elegant event model eliminates physical uncertainty or computation",
    },
]
write_csv(DATA / "topology_layers.csv", list(topology_rows[0].keys()), topology_rows)

application_rows = [
    {
        "Application": "Reactive membrane coating or tie layer",
        "Arie_contribution": "Hydroxyl-rich thermoplastic with polar sulfone backbone and post-functionalization potential",
        "Tom_contribution": "Compatibility-gated operational model, lineage, fouling/threshold event detection",
        "Near_term_readiness_1_to_5": 4,
        "Evidence_status": "Material plausible; application requires formulation and transport testing",
        "First_experiment": "Coat a commercial support, quantify adhesion, flux, selectivity, swelling, extractables, and cleaning stability",
    },
    {
        "Application": "Hemocompatible or antifouling biointerface",
        "Arie_contribution": "Pendant OH sites for grafting PEG, zwitterions, polysaccharides, peptides, or anticoagulant motifs",
        "Tom_contribution": "Event-based monitoring of adhesion/aggregation plus topology descriptors and traceable surface history",
        "Near_term_readiness_1_to_5": 3,
        "Evidence_status": "Requires full biological safety and surface-function validation",
        "First_experiment": "Compare unmodified, hydroxyl-rich, and derivatized coupons for protein adsorption, platelet adhesion, complement, and cytotoxicity",
    },
    {
        "Application": "Affinity membrane or biosensor",
        "Arie_contribution": "OH handles support immobilization chemistry",
        "Tom_contribution": "Typed analyte-receptor compatibility and bounded guard events",
        "Near_term_readiness_1_to_5": 4,
        "Evidence_status": "Strong conceptual fit; device-specific chemistry needed",
        "First_experiment": "Immobilize a model ligand, measure binding kinetics and false/missed event rate under flow",
    },
    {
        "Application": "Membrane digital twin",
        "Arie_contribution": "Defines a candidate reactive material and process history",
        "Tom_contribution": "State-at-time, next-event, uncertainty, guard crossings, and lineage",
        "Near_term_readiness_1_to_5": 5,
        "Evidence_status": "Existing digital-twin precedent; corpus contributes an event-centric formulation",
        "First_experiment": "Cross-flow cell with pressure, flux, conductivity, optical fouling, and cleaning events compared against fixed-rate logging",
    },
    {
        "Application": "Pore/morphology topology analytics",
        "Arie_contribution": "Material chemistry can generate evolving porous or phase-separated structures",
        "Tom_contribution": "Topology-first representation and query semantics",
        "Near_term_readiness_1_to_5": 4,
        "Evidence_status": "Persistent homology and scalar-field topology are established analysis tools",
        "First_experiment": "Micro-CT or confocal time series; correlate persistence descriptors with flux, modulus, or fouling onset",
    },
    {
        "Application": "Event-based microfluidics and cytometry",
        "Arie_contribution": "Potential substrate/coating for optical or biological channels",
        "Tom_contribution": "Sparse asynchronous events rather than mandatory global frames",
        "Near_term_readiness_1_to_5": 5,
        "Evidence_status": "Event-camera precedents exist; integration with the specific material is unproven",
        "First_experiment": "Track fluorescent or bright-field particles/cells and benchmark bandwidth, latency, missed events, and classification",
    },
    {
        "Application": "Optofluidic compatibility gate",
        "Arie_contribution": "Reactive polymer coatings or waveguide packaging interfaces",
        "Tom_contribution": "Local spherical support -> mode compatibility -> measured B.C.E.",
        "Near_term_readiness_1_to_5": 3,
        "Evidence_status": "Component classes are established; integrated system claim remains frontier",
        "First_experiment": "Hollowlens-0: liquid coupler, 2x2 interferometer, balanced detector, digital sidecar",
    },
    {
        "Application": "Composite and adhesive interphase",
        "Arie_contribution": "Thermoplastic processing plus reactive OH groups and hydrogen bonding",
        "Tom_contribution": "Interface lineage, damage-event guards, local support queries",
        "Near_term_readiness_1_to_5": 4,
        "Evidence_status": "Chemically plausible and aligned with phenoxy-resin uses",
        "First_experiment": "Interlaminar fracture, lap-shear, aging, and acoustic-event correlation",
    },
    {
        "Application": "Restricted equation-world physics / computer graphics",
        "Arie_contribution": "Provides a literal example of local graph transformation under constraints",
        "Tom_contribution": "Direct state/event queries, implicit relations, local supports, and hybrid projection",
        "Near_term_readiness_1_to_5": 3,
        "Evidence_status": "Prototype-worthy for restricted relation families; universal replacement claims unsupported",
        "First_experiment": "Equation World Zero with exact/conservative event solver and benchmark against frame stepping/BVH",
    },
    {
        "Application": "Digital material passport and process provenance",
        "Arie_contribution": "Material properties depend strongly on ratios, impurities, temperature, solvent, and reaction history",
        "Tom_contribution": "Generative address, lineage, invariant history, and append-only events",
        "Near_term_readiness_1_to_5": 5,
        "Evidence_status": "Software-ready; requires schema and sensor integration rather than new chemistry",
        "First_experiment": "Batch-to-coupon provenance graph linking raw materials, reaction events, QC, functionalization, sterilization, and tests",
    },
]
write_csv(DATA / "application_matrix.csv", list(application_rows[0].keys()), application_rows)

roadmap_rows = [
    {
        "Phase": "0 - Formal separation",
        "Duration": "2-4 weeks",
        "Objective": "Separate metaphor, mathematical abstraction, and physical claim",
        "Deliverables": "Typed ontology; units; state variables; guards; uncertainty model; source/evidence tags",
        "Success_metric": "Every symbol has a domain, unit or discrete schema; no physical claim depends on analogy alone",
        "Kill_or_pivot_criterion": "Key operators cannot be expressed without circular definitions",
    },
    {
        "Phase": "1 - Equation World Zero",
        "Duration": "1-2 months",
        "Objective": "Validate direct state-at-time and next-event queries for one bounded relation family",
        "Deliverables": "Reference implementation; test vectors; exact/conservative solver; baseline comparison",
        "Success_metric": "Correct event order, bounded error, and cost advantage for declared workloads",
        "Kill_or_pivot_criterion": "Expression/branch growth erases advantage over indexed stepping",
    },
    {
        "Phase": "2 - Membrane World Zero",
        "Duration": "2-4 months",
        "Objective": "Apply event/lineage model to a real cross-flow membrane cell",
        "Deliverables": "Sensor stack; event schema; digital twin; calibrated guards; benchmark dataset",
        "Success_metric": "Earlier or cheaper fouling/cleaning decisions at equal false/missed-event limits",
        "Kill_or_pivot_criterion": "Fixed-rate logging and conventional control are cheaper, faster, and equally informative",
    },
    {
        "Phase": "3 - Reactive surface demonstrator",
        "Duration": "3-6 months",
        "Objective": "Test a hydroxyl-rich phenoxy/PHES-like coating or analogue on a known membrane support",
        "Deliverables": "Coating recipe; chemistry/QC; adhesion; transport; aging; extractables profile",
        "Success_metric": "Reproducible surface-function gain without unacceptable flux, swelling, or leachables penalty",
        "Kill_or_pivot_criterion": "Residuals, delamination, instability, or performance loss exceed predefined limits",
    },
    {
        "Phase": "4 - Biointerface World Zero",
        "Duration": "4-9 months",
        "Objective": "Couple derivatized surfaces to event-based biological readout",
        "Deliverables": "In-vitro chip; event camera/reference imaging; TDA pipeline; biological safety screen",
        "Success_metric": "Event/topology descriptors predict predefined adhesion, fouling, or detachment outcomes",
        "Kill_or_pivot_criterion": "Surface chemistry dominates variability or event readout adds no decision value",
    },
    {
        "Phase": "5 - Integrated platform",
        "Duration": "9-18 months",
        "Objective": "Co-design material, sensing, digital twin, and lineage",
        "Deliverables": "Closed-loop prototype; energy/error budget; reproducibility package; IP claim chart",
        "Success_metric": "System-level advantage over matched material-only and software-only baselines",
        "Kill_or_pivot_criterion": "Integration overhead exceeds measured benefit",
    },
]
write_csv(DATA / "research_roadmap.csv", list(roadmap_rows[0].keys()), roadmap_rows)

ledger_rows = [
    {
        "Claim_or_theme": "The patent targets an almost exclusively linear high-molecular-weight thermoplastic",
        "Basis": "SE 301 717 B description and claims",
        "Classification": "Source-derived",
        "Confidence": "High",
        "Caution": "Historical molecular-weight evidence is mainly intrinsic viscosity and mechanical properties",
    },
    {
        "Claim_or_theme": "Near-equimolarity is a molecular-weight control mechanism",
        "Basis": "Patent ratio window plus ideal step-growth theory",
        "Classification": "Source plus established theory",
        "Confidence": "High",
        "Caution": "Real systems deviate through branching, cycles, impurities, and incomplete conversion",
    },
    {
        "Claim_or_theme": "SO2 is the neutral covalent diaryl-sulfone bridge, not sulfur-dioxide release",
        "Basis": "Chemical structures and patent-family terminology",
        "Classification": "Source-derived interpretation",
        "Confidence": "High",
        "Caution": "Do not conflate sulfone with sulfonate or sulfur dioxide",
    },
    {
        "Claim_or_theme": "The mature corpus is a query-first event calculus rather than a renderer",
        "Basis": "Chronological Synthesis and Spherical Throughput",
        "Classification": "Source-derived",
        "Confidence": "High",
        "Caution": "Earlier Hollowland pages contain overclaims later demoted by the corpus itself",
    },
    {
        "Claim_or_theme": "Arie and Tom share a support -> compatibility -> event -> transition -> lineage grammar",
        "Basis": "Comparative synthesis",
        "Classification": "Author inference",
        "Confidence": "Medium-high",
        "Caution": "The mapping is structural, not evidence of shared hidden intent or identical mechanisms",
    },
    {
        "Claim_or_theme": "The polymer is a candidate membrane coating/biointerface platform",
        "Basis": "Pendant hydroxyl chemistry, sulfone polarity, later PHES/phenoxy literature",
        "Classification": "Application inference",
        "Confidence": "Medium",
        "Caution": "The patent itself does not demonstrate membrane separation or biocompatibility",
    },
    {
        "Claim_or_theme": "Universal O(1), zero-memory, bypassed-sieve, and solved-CCD claims are established",
        "Basis": "Early corpus rhetoric only",
        "Classification": "Rejected/unsupported",
        "Confidence": "High",
        "Caution": "At most, fixed closed expressions may avoid cost proportional to skipped time steps",
    },
    {
        "Claim_or_theme": "Event-based sensing, membrane digital twins, persistent homology, and sheaf fusion are credible adjacent techniques",
        "Basis": "Peer-reviewed primary literature",
        "Classification": "Externally supported",
        "Confidence": "High",
        "Caution": "Their combination with the patented material remains a research program",
    },
    {
        "Claim_or_theme": "Biomedical deployment requires extractables/leachables and biological-risk evaluation",
        "Basis": "ISO 10993/FDA framework and BPS hazard concerns",
        "Classification": "Externally supported safety requirement",
        "Confidence": "High",
        "Caution": "Polymerized material is not automatically equivalent to free BPS; residuals and degradation products must be measured",
    },
]
write_csv(DATA / "evidence_ledger.csv", list(ledger_rows[0].keys()), ledger_rows)

glossary_rows = [
    {"Term": "BPS", "Definition": "Bisphenol S, 4,4'-sulfonyldiphenol; a difunctional phenol containing a neutral diaryl-sulfone bridge."},
    {"Term": "DGE-BPS", "Definition": "Diglycidyl ether of bisphenol S; a difunctional epoxide monomer."},
    {"Term": "PHES", "Definition": "Poly(hydroxyether sulfone), a later name for closely related hydroxyl-rich sulfone-containing polyethers."},
    {"Term": "Sulfone", "Definition": "A covalent R-S(=O)2-R group; distinct from sulfonate ions and from sulfur dioxide gas."},
    {"Term": "Step-growth polymerization", "Definition": "Polymer growth through reactions between functional groups on monomers/oligomers; high molecular weight requires high conversion and close stoichiometric balance."},
    {"Term": "SDF = 0", "Definition": "In the mature corpus, an implicit relation or event surface at which transition semantics are invoked; not necessarily a ray-marching loop."},
    {"Term": "B.C.E.", "Definition": "Bounded Compatibility Event: a transition declared only when support, compatibility, guard, and confidence conditions are satisfied."},
    {"Term": "Double vacuum", "Definition": "Operational metaphor for co-located but uncoupled sectors, modes, sheets, or channels; not a literal second physical vacuum."},
    {"Term": "Local spherical support", "Definition": "A radial-angular local chart for relevance, field of view, coupling, or uncertainty; not a mandatory global spherical world model."},
    {"Term": "Lineage", "Definition": "Identity and provenance preserved through event history and invariants rather than only instantaneous coordinates."},
    {"Term": "Persistent homology", "Definition": "A topological data-analysis method that tracks connected components, loops, and voids across a filtration scale."},
    {"Term": "Sheaf", "Definition": "A mathematical structure that organizes compatible local data and tests whether local observations can be consistently combined globally."},
    {"Term": "Hybrid automaton", "Definition": "A formal model combining continuous state evolution with discrete guards and transitions."},
    {"Term": "Event sourcing", "Definition": "A software pattern in which state changes are stored as an append-only sequence of events, allowing reconstruction and audit."},
]
write_csv(DATA / "glossary.csv", list(glossary_rows[0].keys()), glossary_rows)

# ---------------------------------------------------------------------------
# External references
# ---------------------------------------------------------------------------
references = [
    {
        "ID": "R01", "Type": "Patent", "Citation": "Kreps, R. W.; Klootwijk, A.; Goppel, J. M. Method for producing thermoplastics from a dihydroxy compound and a diepoxy compound containing an SO2 group. SE 301717 B; priority 15 June 1959.",
        "DOI_or_URL": "https://patents.google.com/patent/US3364178A/en", "Role": "Primary historical invention and patent-family terminology"
    },
    {
        "ID": "R02", "Type": "Journal article", "Citation": "Lu, H.; Zheng, S.; Tian, G. Poly(hydroxyether sulfone) and its blends with poly(ethylene oxide): miscibility, phase behavior and hydrogen bonding interactions. Polymer 45 (2004) 2897-2909.",
        "DOI_or_URL": "https://doi.org/10.1016/j.polymer.2004.02.050", "Role": "Later PHES terminology and material context"
    },
    {
        "ID": "R03", "Type": "Book", "Citation": "Flory, P. J. Principles of Polymer Chemistry. Cornell University Press, 1953.",
        "DOI_or_URL": "", "Role": "Step-growth polymerization and molecular-weight distributions"
    },
    {
        "ID": "R04", "Type": "Journal article", "Citation": "Robinson, M. Sheaves are the canonical data structure for sensor integration. Information Fusion 36 (2017) 208-224.",
        "DOI_or_URL": "https://doi.org/10.1016/j.inffus.2016.12.002", "Role": "Local-to-global data consistency and sensor fusion"
    },
    {
        "ID": "R05", "Type": "Journal article", "Citation": "Jiang, F.; Tsuji, T.; Shirai, T. Pore Geometry Characterization by Persistent Homology Theory. Water Resources Research 54 (2018) 4150-4163.",
        "DOI_or_URL": "https://doi.org/10.1029/2017WR021864", "Role": "Persistent homology for pore geometry"
    },
    {
        "ID": "R06", "Type": "Journal article", "Citation": "Yan, L.; Masood, T. B.; Sridharamurthy, R.; et al. Scalar Field Comparison with Topological Descriptors: Properties and Applications for Scientific Visualization. Computer Graphics Forum 40 (2021) 599-633.",
        "DOI_or_URL": "https://doi.org/10.1111/cgf.14331", "Role": "Topological descriptors for scientific visualization"
    },
    {
        "ID": "R07", "Type": "Journal article", "Citation": "Moller, J. K.; Goranovic, G.; Brath, P.; Madsen, H. A data-driven digital twin for water ultrafiltration. Communications Engineering 1, 23 (2022).",
        "DOI_or_URL": "https://doi.org/10.1038/s44172-022-00023-6", "Role": "Membrane digital-twin precedent with uncertainty and control"
    },
    {
        "ID": "R08", "Type": "Journal article", "Citation": "Howell, J.; Hammarton, T. C.; Altmann, Y.; Jimenez, M. High-speed particle detection and tracking in microfluidic devices using event-based sensing. Lab on a Chip 20 (2020) 3024-3035.",
        "DOI_or_URL": "https://doi.org/10.1039/D0LC00556H", "Role": "Event-based microfluidic sensing"
    },
    {
        "ID": "R09", "Type": "Journal article", "Citation": "Tsilikas, I.; Tsirigotis, A.; Sarantoglou, G.; et al. Photonic neuromorphic accelerators for event-based imaging flow cytometry. Scientific Reports 14, 24179 (2024).",
        "DOI_or_URL": "https://doi.org/10.1038/s41598-024-75667-9", "Role": "Event-based bioimaging/flow-cytometry precedent"
    },
    {
        "ID": "R10", "Type": "Journal article", "Citation": "Kuiper, S.; Hendriks, B. H. W. Variable-focus liquid lens for miniature cameras. Applied Physics Letters 85 (2004) 1128-1130.",
        "DOI_or_URL": "https://doi.org/10.1063/1.1779954", "Role": "Liquid-lens component precedent"
    },
    {
        "ID": "R11", "Type": "Journal article", "Citation": "Crespi, A.; Gu, Y.; Ngamsom, B.; et al. Three-dimensional Mach-Zehnder interferometer in a microfluidic chip for spatially-resolved label-free detection. Lab on a Chip 10 (2010) 1167-1173.",
        "DOI_or_URL": "https://doi.org/10.1039/B920062B", "Role": "Optofluidic interferometric readout"
    },
    {
        "ID": "R12", "Type": "Journal article", "Citation": "Tu, M.-M.; Xu, J.-J.; Qiu, Y.-R. Surface hemocompatible modification of polysulfone membrane via covalently grafting acrylic acid and sulfonated hydroxypropyl chitosan. RSC Advances 9 (2019) 6254-6266.",
        "DOI_or_URL": "https://doi.org/10.1039/C8RA10573A", "Role": "Hemocompatible surface-modification precedent on a sulfone polymer membrane"
    },
    {
        "ID": "R13", "Type": "Journal article", "Citation": "Yan, S.; Qiu, Y. Improving hemocompatibility of polysulfone membrane by UV-assisted grafting of sulfonated chitosan. Polymers 16 (2024) 1555.",
        "DOI_or_URL": "https://doi.org/10.3390/polym16111555", "Role": "Recent membrane hemocompatibility example"
    },
    {
        "ID": "R14", "Type": "Standard", "Citation": "ISO 10993-18:2020. Biological evaluation of medical devices - Part 18: Chemical characterization of medical device materials within a risk management process; Amendment 1:2022.",
        "DOI_or_URL": "https://www.iso.org/standard/64750.html", "Role": "Chemical characterization and extractables/leachables framework"
    },
    {
        "ID": "R15", "Type": "Standard", "Citation": "ISO 10993-17:2023. Biological evaluation of medical devices - Part 17: Toxicological risk assessment of medical device constituents; Amendment 1:2025.",
        "DOI_or_URL": "https://www.iso.org/standard/75323.html", "Role": "Toxicological risk assessment"
    },
    {
        "ID": "R16", "Type": "Guidance", "Citation": "U.S. Food and Drug Administration. Use of International Standard ISO 10993-1, Biological evaluation of medical devices - Part 1: Evaluation and testing within a risk management process. Final guidance, 8 September 2023.",
        "DOI_or_URL": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-international-standard-iso-10993-1-biological-evaluation-medical-devices-part-1-evaluation-and", "Role": "Regulatory biological-evaluation framework"
    },
    {
        "ID": "R17", "Type": "Official hazard listing", "Citation": "California OEHHA. Bisphenol S (BPS) Proposition 65 reproductive-toxicity listing: female, male, and developmental endpoints (2023-2025).",
        "DOI_or_URL": "https://oehha.ca.gov/proposition-65/chemicals/bisphenol-s-bps", "Role": "Reason to prioritize residual BPS and degradation-product analysis"
    },
    {
        "ID": "R18", "Type": "Journal article", "Citation": "Andersen, J. L.; Flamm, C.; Merkle, D.; Stadler, P. F. Inferring chemical reaction patterns using rule composition in graph grammars. Journal of Systems Chemistry 4, 4 (2013).",
        "DOI_or_URL": "https://doi.org/10.1186/1759-2208-4-4", "Role": "Chemical graph rewriting and reaction-pattern composition"
    },
    {
        "ID": "R19", "Type": "Technical report", "Citation": "Lee, E. A.; Zheng, H. Operational semantics of hybrid systems. University of California, Berkeley, 2005.",
        "DOI_or_URL": "https://ptolemy.berkeley.edu/publications/papers/05/OperationalSemantics/LeeZheng_HybridSystems.pdf", "Role": "Guards and discrete transitions coupled to continuous dynamics"
    },
    {
        "ID": "R20", "Type": "Web technical note", "Citation": "Fowler, M. Event Sourcing. 2005.",
        "DOI_or_URL": "https://martinfowler.com/eaaDev/EventSourcing.html", "Role": "Append-only event history and state reconstruction"
    },
]
write_csv(REFS / "external_references.csv", list(references[0].keys()), references)

bib = r"""
@patent{KrepsKlootwijkGoppel1959,
  author = {Kreps, R. W. and Klootwijk, Arie and Goppel, J. M.},
  title = {Thermoplastic poly(hydroxyalkyl diphenyl sulfone) ethers},
  number = {US3364178A},
  year = {1968},
  note = {Priority 15 June 1959; Swedish publication SE301717B}
}
@article{Lu2004PHES,
  author = {Lu, Han and Zheng, Sixun and Tian, Guohua},
  title = {Poly(hydroxyether sulfone) and its blends with poly(ethylene oxide): miscibility, phase behavior and hydrogen bonding interactions},
  journal = {Polymer},
  volume = {45},
  pages = {2897--2909},
  year = {2004},
  doi = {10.1016/j.polymer.2004.02.050}
}
@book{Flory1953,
  author = {Flory, Paul J.},
  title = {Principles of Polymer Chemistry},
  publisher = {Cornell University Press},
  year = {1953}
}
@article{Robinson2017,
  author = {Robinson, Michael},
  title = {Sheaves are the canonical data structure for sensor integration},
  journal = {Information Fusion},
  volume = {36},
  pages = {208--224},
  year = {2017},
  doi = {10.1016/j.inffus.2016.12.002}
}
@article{Jiang2018,
  author = {Jiang, Fei and Tsuji, Takeshi and Shirai, Tomoyuki},
  title = {Pore Geometry Characterization by Persistent Homology Theory},
  journal = {Water Resources Research},
  volume = {54},
  pages = {4150--4163},
  year = {2018},
  doi = {10.1029/2017WR021864}
}
@article{Yan2021Topology,
  author = {Yan, Lin and Masood, Talha Bin and Sridharamurthy, Raghavendra and Rasheed, Farhan and Natarajan, Vijay and Hotz, Ingrid and Wang, Bei},
  title = {Scalar Field Comparison with Topological Descriptors: Properties and Applications for Scientific Visualization},
  journal = {Computer Graphics Forum},
  volume = {40},
  pages = {599--633},
  year = {2021},
  doi = {10.1111/cgf.14331}
}
@article{Moller2022,
  author = {Moller, Jan Kloppenborg and Goranovic, Goran and Brath, Per and Madsen, Henrik},
  title = {A data-driven digital twin for water ultrafiltration},
  journal = {Communications Engineering},
  volume = {1},
  pages = {23},
  year = {2022},
  doi = {10.1038/s44172-022-00023-6}
}
@article{Howell2020,
  author = {Howell, Jessie and Hammarton, Tansy C. and Altmann, Yoann and Jimenez, Melanie},
  title = {High-speed particle detection and tracking in microfluidic devices using event-based sensing},
  journal = {Lab on a Chip},
  volume = {20},
  pages = {3024--3035},
  year = {2020},
  doi = {10.1039/D0LC00556H}
}
@article{Tsilikas2024,
  author = {Tsilikas, Ioannis and Tsirigotis, Aris and Sarantoglou, George and Deligiannidis, Stavros and Bogris, Adonis and Posch, Christoph and Van den Branden, Gerd and Mesaritakis, Charis},
  title = {Photonic neuromorphic accelerators for event-based imaging flow cytometry},
  journal = {Scientific Reports},
  volume = {14},
  pages = {24179},
  year = {2024},
  doi = {10.1038/s41598-024-75667-9}
}
@article{Tu2019,
  author = {Tu, Ming-Ming and Xu, Jing-Jie and Qiu, Yun-Ren},
  title = {Surface hemocompatible modification of polysulfone membrane via covalently grafting acrylic acid and sulfonated hydroxypropyl chitosan},
  journal = {RSC Advances},
  volume = {9},
  pages = {6254--6266},
  year = {2019},
  doi = {10.1039/C8RA10573A}
}
@article{Andersen2013,
  author = {Andersen, Jakob L. and Flamm, Christoph and Merkle, Daniel and Stadler, Peter F.},
  title = {Inferring chemical reaction patterns using rule composition in graph grammars},
  journal = {Journal of Systems Chemistry},
  volume = {4},
  pages = {4},
  year = {2013},
  doi = {10.1186/1759-2208-4-4}
}
"""
write_text(REFS / "bibliography.bib", bib)

# ---------------------------------------------------------------------------
# Analysis notes
# ---------------------------------------------------------------------------
write_text(ANALYSIS / "source_assessment.md", r"""
# Source assessment and evidence tiers

## Source set

The comparison rests on two very different classes of source:

1. **Arie Klootwijk's issued patent family and historical working examples.** These documents define reagents, ratios, solvents, catalyst handling, temperature, isolation, intrinsic viscosity, mechanical properties, and claims. They are strong evidence for what was proposed and historically demonstrated, but they do not meet modern characterization or biomedical-validation standards.
2. **Tom Klootwijk's spherical-substrate corpus.** The corpus is a design record that moves from exploratory metaphors to a disciplined query-first event calculus. The strongest source is the chronological synthesis, which explicitly demotes universal O(1), zero-memory, and totalizing renderer claims. The practical waveguide report further requires measured support, compatibility, guards, uncertainty, energy, error, and calibration.

## Evidence tiers used throughout

- **Tier A - source fact:** directly stated or measured in the patent/corpus.
- **Tier B - established external principle:** standard chemistry, polymer physics, topology, control, or biomedical guidance.
- **Tier C - comparative inference:** a structural mapping proposed in this review.
- **Tier D - research hypothesis:** plausible application that requires experiment.
- **Tier X - rejected overclaim:** contradicted by the mature corpus or unsupported by physical/computational evidence.

The central discipline is to avoid promoting a Tier C analogy into a Tier A mechanism. The fact that two systems share the pattern "compatibility -> event -> connectivity update" does not mean that one secretly encoded the other, nor that symbolic topology replaces kinetics, thermodynamics, transport, or experimental validation.
""")

write_text(ANALYSIS / "fundamental_crosswalk.md", r"""
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
""")

write_text(ANALYSIS / "where_tom_is_ahead_and_where_not.md", r"""
# Where Tom's work is ahead today - and where it is not

## Present-day strengths

Tom's mature line is stronger than the 1959 patent in the **operational information layer**. It explicitly asks what state holds at a time, what event occurs next, which sectors can interact, how local views are reconciled, and how identity persists through changes. That creates natural interfaces to hybrid systems, event-based sensing, digital twins, topological data analysis, provenance, and formal verification.

The most valuable innovations are not the universal claims from the exploratory dialogue. They are the disciplined corrections:

- local spherical/radial-angular support rather than a spherical replacement for all geometry;
- compatibility as a first-class predicate, so co-location does not imply coupling;
- explicit event surfaces and transition semantics;
- one-bit parity as a narrow route/validity tag, not complete state;
- lineage and an irreducible event log for exogenous novelty;
- uncertainty, calibration, error budgets, and matched baselines;
- headless, query-based prototypes before renderer or hardware spectacle.

## Where Arie's work remains stronger

Arie's work is stronger in **physical closure and evidence**. It names matter, quantities, impurities, solvents, temperatures, catalyst ranges, isolation steps, and failure mechanisms. It makes specimens and reports measurable properties. It also confronts scale-dependent realities: viscosity, crystallization, water exclusion, heat, purification, and process termination.

No amount of topological elegance replaces those constraints. A present-day program is credible only when it can state:

- the physical state variables and units;
- the governing conservation laws and kinetics;
- the measurement model and calibration;
- the uncertainty and false/missed-event limits;
- the material and biological safety boundary;
- the benchmark against a conventional baseline.

## Claims to retire or sharply narrow

The following should not be carried forward as established facts: universal O(1), zero memory, zero heat, zero latency, solved general CCD, elimination of all broad-phase indexing, automatic AI/world identity, exact long-horizon prediction of arbitrary systems, and physical proof from Klein-bottle or double-vacuum imagery. The mature corpus already provides the correct narrowing: a fixed closed expression may answer a state-at-time query without replaying skipped frames, while event-solving, compatibility, branch growth, numerical conditioning, and exogenous novelty still cost time and memory.
""")

write_text(ANALYSIS / "membranes_and_biointerfaces.md", r"""
# Membranes and biointerfaces

## What Arie's chemistry can credibly contribute

The preferred product is a linear sulfone-containing poly(hydroxy ether), closely related to later PHES/phenoxy terminology. Each epoxide-opening event introduces a secondary hydroxyl. Those hydroxyls provide hydrogen bonding and chemical handles for post-functionalization, while the aromatic sulfone contributes polarity, stiffness, and thermal resistance.

That combination is relevant to membrane and interface engineering in four roles:

1. **Reactive coating or tie layer** on a mechanically robust porous support.
2. **Blend modifier** that changes adhesion, toughness, water uptake, and interphase compatibility.
3. **Functionalization scaffold** for PEG, zwitterions, polysaccharides, peptides, affinity ligands, or crosslinkers.
4. **Patternable interface** in microfluidic, optical, or sensor devices.

The material is not intrinsically an ion-exchange membrane merely because it contains SO2. The sulfone is neutral. Ionic transport would require separate ionizable or permanently charged groups. Nor does the patent demonstrate pore morphology, selectivity, blood compatibility, cell response, sterilization stability, or long-term extractables.

## What Tom's architecture can add

A membrane or biointerface can be represented as a coupled material/digital system:

- local support defines which pore, surface patch, angular sector, analyte, cell, or optical mode is relevant;
- compatibility encodes size, charge, ligand/receptor, phase, wavelength, polarization, time window, or policy;
- guards represent breakthrough, fouling onset, pore blockage, binding, adhesion, detachment, delamination, threshold crossing, or loss of calibration;
- transitions update resistance, occupancy, surface state, route, cleaning mode, or confidence;
- lineage links raw material, synthesis batch, coating, sterilization, use cycles, and observed events.

Persistent homology can track connected pores, loops, and voids across imaging scales. Sheaf-based methods can test whether local sensors and models are globally consistent. Hybrid automata can combine continuous flux, pressure, adsorption, and cell motion with discrete cleaning, alarm, adhesion, or routing events. Event cameras can reduce data volume when biological or microfluidic information is concentrated in changes rather than static frames.

## Combined concept: a chemically addressable interface with an event-sourced twin

The strongest joint platform is not a mystical topological membrane. It is a **chemically addressable membrane or biointerface whose physical state is monitored by a bounded, event-sourced digital twin**.

A credible state vector might include flux, transmembrane pressure, temperature, conductivity, optical intensity, inferred fouling resistance, ligand occupancy, pore-topology descriptors, surface chemistry lot, calibration state, and uncertainty. A B.C.E. is emitted only when support, compatibility, a measured guard, and confidence are all satisfied.

## Biomedical safety boundary

Any biomedical route must begin with chemical characterization and risk assessment of the final processed device, not merely the nominal repeat unit. Priority analytes include residual BPS, DGE-BPS, low-molecular-weight oligomers, hydrolyzable chloride, catalyst residues, solvent residues, functionalization reagents, sterilization products, and aged/degraded extractables. Free BPS has current reproductive/developmental hazard listings, which makes residual and degradation analysis especially important. This does not prove that a purified high-molecular-weight polymer has the same hazard profile; it means exposure must be measured rather than assumed away.
""")

write_text(ANALYSIS / "research_and_ip_program.md", r"""
# Research and IP program

## Claim architecture

A useful patent or publication strategy should separate four claim families:

1. **Material composition and processing:** specific hydroxyl-rich sulfone polyether formulations, crosslinking, grafts, coating methods, residual limits, and morphology.
2. **Interface architecture:** layer stack, porous support, ligand pattern, optical/electrical readout, microfluidic geometry, and regeneration method.
3. **Operational method:** local-support admission, compatibility predicate, guard definition, event transition, uncertainty, and lineage update.
4. **System benchmark:** verified events or decisions per second and per joule at declared false/missed-event, calibration, and material-safety boundaries.

Avoid trying to claim a universal topology metaphor. Patentable value is more likely in a specific coupling: a material surface with a defined functionalization and a bounded event-control architecture that produces a measurable advantage.

## Minimum evidence before broad claims

- material identity by NMR/FTIR and molecular-weight distribution by SEC or an appropriate absolute method;
- residual monomer/oligomer/solvent/catalyst analysis;
- water uptake, swelling, Tg/thermal stability, mechanical properties, adhesion, and aging;
- membrane flux/selectivity/fouling/cleaning data or biointerface adsorption/cell/blood data;
- calibrated event timing, uncertainty, false/missed-event rates, and energy accounting;
- conventional material-only and software-only baselines;
- reproducible process and batch lineage.

## High-value cross-domain publications

- a formal paper defining the support-compatibility-event-transition-lineage calculus with hybrid-system semantics;
- a benchmark paper for Equation World Zero on restricted relation families;
- a membrane digital-twin paper using event guards and persistent topology descriptors;
- a materials paper on a hydroxyl-rich sulfone polyether coating with controlled functionalization;
- an integrated biointerface paper coupling event-based imaging to surface lineage and topology analytics.
""")

write_text(ANALYSIS / "evidence_boundaries.md", r"""
# Evidence boundaries and falsification rules

## Claims supported by the sources

- Arie's patent deliberately controls linear step-growth polymerization through near-equimolarity, solvent choice, purity, dryness, and catalyst handling.
- The patent identifies premature crystallization and reactive solvent as causes of low molecular weight.
- The mature spherical-substrate corpus prioritizes directly queryable relations, event solving, compatibility, lineage, and restricted prototypes rather than rasterization or ray marching as the substrate.
- Spherical Throughput converts one-bit, double-vacuum, and waveguide motifs into bounded engineering roles with measured errors, loss, energy, calibration, and failure criteria.

## Comparative inferences, not historical facts

- The patent can be interpreted as a physical graph-rewriting system.
- Solubility can be compared to support/accessibility, and crystallization to deactivation from the active relation set.
- Pendant hydroxyls can be interpreted as typed material interface ports.
- The two bodies of work can be combined as a chemically addressable interface plus event-sourced digital twin.

## Falsification rules

A proposed overlap should be rejected or rewritten if:

- it cannot identify the physical observable corresponding to the abstract state;
- it violates mass, charge, energy, or stoichiometric balance;
- it treats a binary flag as sufficient material state;
- it hides numerical iteration or candidate search while claiming O(1);
- its compatibility or event-solving cost exceeds the materialization it claims to avoid;
- a matched conventional baseline is better at equal accuracy, error, energy, and calibration burden;
- the final material fails extractables, aging, biological, or transport criteria.
""")

# ---------------------------------------------------------------------------
# Prototypes and schemas
# ---------------------------------------------------------------------------
membrane_spec = r"""
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
"""
write_text(PROTO / "Membrane_World_Zero_Specification.md", membrane_spec)

bio_spec = r"""
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
"""
write_text(PROTO / "Biointerface_World_Zero_Specification.md", bio_spec)

config = {
    "prototype": "Membrane World Zero",
    "version": "0.1",
    "sampling_reference_hz": 10,
    "support": {"active_module": "M0", "time_window_s": [0, 3600], "calibration_max_age_s": 900},
    "compatibility": {"require_sensor_valid": True, "require_material_lineage": True, "require_calibration": True},
    "guards": {
        "flux_drop_fraction": 0.12,
        "tmp_rise_fraction": 0.15,
        "breakthrough_conductivity": 1.5,
        "drift_zscore": 4.0,
        "min_confidence": 0.95,
    },
    "reporting": {"record_raw_window_before_s": 5, "record_raw_window_after_s": 10, "store_rejected_candidates": True},
}
write_text(PROTO / "membrane_world_zero_config.json", json.dumps(config, indent=2))

event_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Bounded Compatibility Event",
    "type": "object",
    "required": ["event_id", "event_type", "time_interval", "support", "compatibility", "guard", "confidence", "lineage", "pre_state", "post_state"],
    "properties": {
        "event_id": {"type": "string"},
        "event_type": {"type": "string"},
        "time_interval": {"type": "array", "prefixItems": [{"type": "number"}, {"type": "number"}], "minItems": 2, "maxItems": 2},
        "support": {"type": "object"},
        "compatibility": {"type": "object"},
        "guard": {"type": "object"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "lineage": {"type": "object"},
        "pre_state": {"type": "object"},
        "post_state": {"type": "object"},
        "action": {"type": ["string", "null"]},
        "raw_data_refs": {"type": "array", "items": {"type": "string"}},
    },
}
write_text(PROTO / "bounded_compatibility_event.schema.json", json.dumps(event_schema, indent=2))

material_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Material and biointerface lineage record",
    "type": "object",
    "required": ["material_id", "batch_id", "process_events", "qc_results"],
    "properties": {
        "material_id": {"type": "string"},
        "batch_id": {"type": "string"},
        "raw_material_lots": {"type": "array", "items": {"type": "object"}},
        "process_events": {"type": "array", "items": {"type": "object"}},
        "functionalization": {"type": "array", "items": {"type": "object"}},
        "sterilization_or_aging": {"type": "array", "items": {"type": "object"}},
        "qc_results": {"type": "array", "items": {"type": "object"}},
        "extractables_profile": {"type": ["object", "null"]},
        "parent_material_ids": {"type": "array", "items": {"type": "string"}},
    },
}
write_text(PROTO / "material_lineage.schema.json", json.dumps(material_schema, indent=2))

# Step-growth simulation script
poly_script = r'''#!/usr/bin/env python3
"""Monte Carlo illustration of AA+BB step-growth polymerization.

The model is deliberately idealized: bifunctional units, no rings, no branching, and
random reaction of complementary chain ends. It demonstrates how a small stoichiometric
imbalance caps the number-average chain length. It is not a molecular simulation of
SE301717B.
"""
from __future__ import annotations
import csv
import math
import random
from pathlib import Path

import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent


def theoretical_xn(r: float, p: float) -> float:
    return (1 + r) / (1 + r - 2 * r * p)


def simulate(n_limiting: int, r: float, conversion: float, seed: int = 7):
    """Graph-free chain-merging model using counts of A- and B-terminated chains."""
    rng = random.Random(seed)
    n_a = n_limiting
    n_b = max(1, round(n_limiting / r)) if r < 1 else n_limiting
    chains = [[1, "A", "A"] for _ in range(n_a)] + [[1, "B", "B"] for _ in range(n_b)]
    target = int(round(2 * n_a * conversion))
    reactions = 0
    while reactions < target:
        a_idx = [i for i, c in enumerate(chains) if c[1] == "A" or c[2] == "A"]
        b_idx = [i for i, c in enumerate(chains) if c[1] == "B" or c[2] == "B"]
        if not a_idx or not b_idx:
            break
        i = rng.choice(a_idx)
        j = rng.choice(b_idx)
        if i == j:
            continue
        c1, c2 = chains[i], chains[j]
        # consume one complementary end and join chains; retain the two unconsumed ends
        ends1 = [c1[1], c1[2]]
        ends2 = [c2[1], c2[2]]
        try:
            ends1.remove("A")
            ends2.remove("B")
        except ValueError:
            continue
        new = [c1[0] + c2[0], ends1[0], ends2[0]]
        for k in sorted((i, j), reverse=True):
            chains.pop(k)
        chains.append(new)
        reactions += 1
    lengths = [c[0] for c in chains]
    return lengths, reactions


def main():
    rows = []
    ratios = [1.0, 0.99, 0.98, 0.97]
    conversions = [0.95, 0.98, 0.99, 0.995]
    for r in ratios:
        for p in conversions:
            lengths, rx = simulate(2500, r, p, seed=int(r*10000+p*1000))
            xn_sim = sum(lengths) / len(lengths)
            rows.append({"r": r, "conversion": p, "theoretical_Xn": theoretical_xn(r, p), "simulated_mean_chain_units": xn_sim, "reactions": rx})
    with (OUT / "polymer_step_growth_results.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for r in ratios:
        xs = [p for p in conversions]
        ys = [next(z["theoretical_Xn"] for z in rows if z["r"] == r and z["conversion"] == p) for p in xs]
        ax.plot(xs, ys, marker="o", label=f"r={r:.2f}")
    ax.set_xlabel("Limiting-function conversion p")
    ax.set_ylabel("Ideal number-average degree Xn")
    ax.set_title("Conversion and stoichiometric balance jointly control chain length")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "polymer_step_growth_results.png", dpi=200)

if __name__ == "__main__":
    main()
'''
write_text(PROTO / "polymer_step_growth_demo.py", poly_script)
os.chmod(PROTO / "polymer_step_growth_demo.py", 0o755)

mem_sim_script = r'''#!/usr/bin/env python3
"""Synthetic Membrane World Zero event-log demonstration.

Generates a noisy flux/TMP process, applies support/compatibility/guard logic, and writes
an append-only event log. This is a software example, not validation of a real membrane.
"""
from __future__ import annotations
import csv
import json
import math
import random
import uuid
from pathlib import Path

import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent


def main():
    rng = random.Random(19)
    dt = 1.0
    n = 1800
    flux0 = 100.0
    tmp0 = 1.0
    rows = []
    events = []
    previous_flags = {"fouling": False, "pressure": False, "breakthrough": False}

    for i in range(n):
        t = i * dt
        cake = 0.0008 * t + 0.25 * (1 - math.exp(-t/250))
        clean = 0.45 if 1100 <= t < 1160 else 0.0
        effective = max(0, cake - clean)
        flux = flux0 / (1 + effective) + rng.gauss(0, 0.65)
        tmp = tmp0 * (1 + 0.42 * effective) + rng.gauss(0, 0.008)
        conductivity = 0.2 + (1.8 / (1 + math.exp(-(t-1450)/20))) + rng.gauss(0, 0.015)
        supported = 20 <= t <= 1770
        compatible = supported and (i % 127 != 0)  # synthetic calibration dropout
        confidence = 0.98 if compatible else 0.4
        flags = {
            "fouling": compatible and confidence >= 0.95 and flux < 82.0,
            "pressure": compatible and confidence >= 0.95 and tmp > 1.14,
            "breakthrough": compatible and confidence >= 0.95 and conductivity > 1.5,
        }
        for name, flag in flags.items():
            if flag and not previous_flags[name]:
                events.append({
                    "event_id": str(uuid.uuid4()),
                    "event_type": name,
                    "time_interval": [t-dt, t],
                    "support": {"active": supported, "module": "M0"},
                    "compatibility": {"value": compatible, "schema": "sensor+calibration+lineage"},
                    "guard": {"name": name, "crossed": True},
                    "confidence": confidence,
                    "lineage": {"material_id": "baseline_demo", "calibration": "cal-001"},
                    "pre_state": rows[-1] if rows else {},
                    "post_state": {"time_s": t, "flux": flux, "tmp": tmp, "conductivity": conductivity},
                    "action": "inspect_or_control",
                    "raw_data_refs": [f"membrane_timeseries.csv#row={i+2}"],
                })
            previous_flags[name] = flag
        rows.append({"time_s": t, "flux": flux, "tmp": tmp, "conductivity": conductivity, "supported": int(supported), "compatible": int(compatible), "confidence": confidence})

    with (OUT / "membrane_timeseries.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    with (OUT / "membrane_event_log.jsonl").open("w") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    ax.plot([r["time_s"] for r in rows], [r["flux"] for r in rows], label="Flux")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Synthetic flux")
    ax.set_title("Synthetic membrane process with guard-crossing events")
    for e in events:
        ax.axvline(e["time_interval"][1], alpha=0.35)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUT / "membrane_event_demo.png", dpi=200)
    print(f"Generated {len(rows)} samples and {len(events)} events")

if __name__ == "__main__":
    main()
'''
write_text(PROTO / "membrane_event_sim.py", mem_sim_script)
os.chmod(PROTO / "membrane_event_sim.py", 0o755)

# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def savefig(fig, name: str):
    fig.savefig(FIG / name, bbox_inches="tight", facecolor="white")
    plt.close(fig)

# Figure 1: topology layers
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.axis("off")
labels = [
    ("Molecular graph", "bonds, functionality, chains", CORAL),
    ("Morphology / phase", "crystals, pores, domains", GOLD),
    ("Interface / transport", "coupling, adsorption, flux", TEAL),
    ("Operational information", "support, guards, events, lineage", NAVY),
]
for i, (title, subtitle, color) in enumerate(labels):
    y = 0.77 - i * 0.19
    ax.add_patch(plt.Rectangle((0.08+i*0.045, y), 0.76-i*0.09, 0.13, color=color, alpha=0.92, transform=ax.transAxes))
    ax.text(0.11+i*0.045, y+0.081, title, color="white", weight="bold", fontsize=13, transform=ax.transAxes)
    ax.text(0.11+i*0.045, y+0.035, subtitle, color="white", fontsize=10.5, transform=ax.transAxes)
ax.text(0.5, 0.96, "Four distinct meanings of topology in the comparison", ha="center", va="top", fontsize=16, weight="bold", color=NAVY, transform=ax.transAxes)
ax.text(0.5, 0.04, "Arie is strongest at the molecular layer; Tom is strongest at the operational layer.\nThe research opportunity is to connect the layers without collapsing them.", ha="center", va="bottom", fontsize=11, color=DARK, transform=ax.transAxes)
savefig(fig, "figure_01_four_topology_layers.png")

# Figure 2: shared grammar
fig, ax = plt.subplots(figsize=(11.6, 6.2))
ax.axis("off")
ax.text(0.5, 0.97, "The strongest genuine overlap: a constrained event grammar", ha="center", va="top", fontsize=16, weight="bold", color=NAVY, transform=ax.transAxes)
stages = ["SUPPORT /\nACCESS", "COMPATIBILITY /\nBALANCE", "LOCAL EVENT /\nGUARD", "TRANSITION /\nREWRITE", "LINEAGE /\nCLOSURE"]
colors = [TEAL, PURPLE, CORAL, GOLD, GREEN]
arie_labels = ["solubility +\nmobility", "functional-group\nequivalence", "epoxide\nring opening", "new bond +\nsecondary OH", "chain ends +\nbatch history"]
tom_labels = ["local spherical\nsupport", "phase / sheet /\naddress predicate", "R(q)=0 or\nmeasured guard", "routing +\nstate update", "invariants +\nevent log"]
xs = [0.07 + i*0.185 for i in range(5)]
for lane_y, labels, lane_name, lane_color in [(0.72, arie_labels, "ARIE - PHYSICAL CHEMISTRY", CORAL), (0.14, tom_labels, "TOM - OPERATIONAL INFORMATION", TEAL)]:
    ax.text(0.02, lane_y+0.09, lane_name, rotation=90, va="center", ha="center", fontsize=9.5, weight="bold", color=lane_color, transform=ax.transAxes)
    for i,(x,label) in enumerate(zip(xs,labels)):
        ax.add_patch(FancyBboxPatch((x,lane_y),0.15,0.18,boxstyle="round,pad=0.015",fc=LIGHT,ec=lane_color,lw=1.8,transform=ax.transAxes))
        ax.text(x+0.075,lane_y+0.09,label,ha="center",va="center",fontsize=9.5,color=DARK,transform=ax.transAxes)
        if i<4:
            ax.annotate("",xy=(x+0.18,lane_y+0.09),xytext=(x+0.153,lane_y+0.09),arrowprops=dict(arrowstyle="->",lw=1.5,color=lane_color),xycoords=ax.transAxes)
for i,(s,c,x) in enumerate(zip(stages,colors,xs)):
    ax.add_patch(FancyBboxPatch((x,0.43),0.15,0.18,boxstyle="round,pad=0.018",fc=c,ec="none",transform=ax.transAxes))
    ax.text(x+0.075,0.52,s,ha="center",va="center",color="white",weight="bold",fontsize=10.5,transform=ax.transAxes)
    if i<4:
        ax.annotate("",xy=(x+0.18,0.52),xytext=(x+0.153,0.52),arrowprops=dict(arrowstyle="->",lw=2,color=NAVY),xycoords=ax.transAxes)
ax.text(0.5,0.035,"The mapping is structural. It does not make symbolic events chemically identical to reactions.",ha="center",va="bottom",fontsize=10.5,color=DARK,transform=ax.transAxes)
savefig(fig, "figure_02_event_grammar_crosswalk.png")

# Figure 3: stoichiometry curves
fig, ax = plt.subplots(figsize=(8.6, 5.2))
p = np.linspace(0.90, 0.999, 260)
for r, c in [(1.0, NAVY), (0.99, TEAL), (0.98, GOLD), (0.97, CORAL)]:
    xn = (1+r)/(1+r-2*r*p)
    ax.plot(p, xn, label=f"r = {r:.2f}", lw=2.2, color=c)
ax.set_yscale("log")
ax.set_xlabel("Conversion of limiting functional groups, p")
ax.set_ylabel("Ideal number-average degree of polymerization, Xn")
ax.set_title("Equimolarity is a quantitative invariant, not a visual metaphor", color=NAVY, weight="bold")
ax.grid(alpha=0.25, which="both")
ax.legend(title="Functional-group ratio")
ax.text(0.905, 320, "At high conversion,\na 1-3% imbalance imposes\na hard chain-length ceiling.", fontsize=10, bbox=dict(boxstyle="round,pad=0.4", fc=LIGHT, ec=TEAL))
savefig(fig, "figure_03_stoichiometry_as_invariant.png")

# Figure 4: evidence readiness
fig, ax = plt.subplots(figsize=(9.2, 5.5))
dim = ["Physical recipe", "Quantitative process window", "Measured specimens", "Formal query semantics", "Lineage/provenance", "Biomedical validation"]
arie = [5, 5, 4, 1, 2, 0.5]
tom = [0.5, 1.5, 0.5, 4.5, 4.5, 1.0]
y = np.arange(len(dim))
h = 0.34
ax.barh(y+h/2, arie, h, label="Arie patent", color=CORAL)
ax.barh(y-h/2, tom, h, label="Tom mature corpus", color=TEAL)
ax.set_yticks(y, dim)
ax.set_xlim(0, 5)
ax.set_xlabel("Relative evidence/readiness score (qualitative, 0-5)")
ax.set_title("Complementary strengths, not a single ranking", color=NAVY, weight="bold")
ax.grid(axis="x", alpha=0.2)
ax.legend()
ax.invert_yaxis()
savefig(fig, "figure_04_evidence_readiness.png")

# Figure 5: Membrane World Zero architecture
fig, ax = plt.subplots(figsize=(11.5, 5.6))
ax.axis("off")
boxes = [
    (0.02, 0.52, 0.14, 0.23, "MATERIAL\nmembrane + coating\nchemistry lineage", CORAL),
    (0.20, 0.52, 0.14, 0.23, "PHYSICAL CELL\nflow, pressure, solute,\nfouling, cleaning", GOLD),
    (0.38, 0.52, 0.14, 0.23, "SENSORS\nflux, TMP, optics,\nconductivity, temp", TEAL),
    (0.56, 0.52, 0.14, 0.23, "STATE ESTIMATOR\ncontinuous variables\n+ uncertainty", PURPLE),
    (0.74, 0.52, 0.12, 0.23, "B.C.E.\nsupport + chi\n+ guard", NAVY),
    (0.89, 0.52, 0.09, 0.23, "ACTION\nlog, alarm,\nclean", GREEN),
]
for x,y0,w,h0,txt,c in boxes:
    ax.add_patch(FancyBboxPatch((x,y0), w,h0, boxstyle="round,pad=0.015", fc=c, ec="none", transform=ax.transAxes))
    ax.text(x+w/2, y0+h0/2, txt, ha="center", va="center", color="white", weight="bold", fontsize=9.5, transform=ax.transAxes)
for i in range(len(boxes)-1):
    x1 = boxes[i][0]+boxes[i][2]
    x2 = boxes[i+1][0]
    ax.annotate("", xy=(x2-0.006,0.635), xytext=(x1+0.006,0.635), arrowprops=dict(arrowstyle="->", color=NAVY, lw=2), xycoords=ax.transAxes)
ax.add_patch(FancyBboxPatch((0.25,0.13),0.50,0.18,boxstyle="round,pad=0.02",fc=LIGHT,ec=TEAL,lw=2,transform=ax.transAxes))
ax.text(0.50,0.22,"APPEND-ONLY EVENT + MATERIAL LINEAGE STORE\nreplay, audit, calibration, batch, functionalization, aging",ha="center",va="center",color=NAVY,weight="bold",fontsize=11,transform=ax.transAxes)
ax.annotate("", xy=(0.79,0.51), xytext=(0.69,0.31), arrowprops=dict(arrowstyle="->", color=TEAL, lw=2), xycoords=ax.transAxes)
ax.annotate("", xy=(0.57,0.51), xytext=(0.50,0.31), arrowprops=dict(arrowstyle="->", color=TEAL, lw=2), xycoords=ax.transAxes)
ax.annotate("", xy=(0.34,0.51), xytext=(0.34,0.31), arrowprops=dict(arrowstyle="->", color=TEAL, lw=2), xycoords=ax.transAxes)
ax.text(0.5,0.95,"Membrane World Zero: material state and operational state stay distinct but coupled",ha="center",va="top",fontsize=16,weight="bold",color=NAVY,transform=ax.transAxes)
savefig(fig, "figure_05_membrane_world_zero.png")

svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="580" viewBox="0 0 1200 580">
<rect width="1200" height="580" fill="white"/>
<text x="600" y="42" text-anchor="middle" font-family="Inter,Arial" font-size="28" font-weight="700" fill="#0B2A3D">Membrane World Zero</text>
<g font-family="Inter,Arial" font-size="15" font-weight="700" fill="white" text-anchor="middle">
<rect x="25" y="135" width="155" height="145" rx="16" fill="#C8665A"/><text x="102" y="175"><tspan x="102">MATERIAL</tspan><tspan x="102" dy="28">membrane + coating</tspan><tspan x="102" dy="24">chemistry lineage</tspan></text>
<rect x="220" y="135" width="155" height="145" rx="16" fill="#D7A51F"/><text x="297" y="175"><tspan x="297">PHYSICAL CELL</tspan><tspan x="297" dy="28">flow / pressure</tspan><tspan x="297" dy="24">fouling / cleaning</tspan></text>
<rect x="415" y="135" width="155" height="145" rx="16" fill="#148C9B"/><text x="492" y="175"><tspan x="492">SENSORS</tspan><tspan x="492" dy="28">flux / TMP / optics</tspan><tspan x="492" dy="24">conductivity / temp</tspan></text>
<rect x="610" y="135" width="155" height="145" rx="16" fill="#695C9C"/><text x="687" y="175"><tspan x="687">STATE ESTIMATOR</tspan><tspan x="687" dy="28">continuous variables</tspan><tspan x="687" dy="24">+ uncertainty</tspan></text>
<rect x="805" y="135" width="135" height="145" rx="16" fill="#0B2A3D"/><text x="872" y="175"><tspan x="872">B.C.E.</tspan><tspan x="872" dy="28">support + chi</tspan><tspan x="872" dy="24">+ measured guard</tspan></text>
<rect x="980" y="135" width="135" height="145" rx="16" fill="#3B8D70"/><text x="1047" y="175"><tspan x="1047">ACTION</tspan><tspan x="1047" dy="28">log / alarm</tspan><tspan x="1047" dy="24">clean / route</tspan></text>
</g>
<g stroke="#0B2A3D" stroke-width="4" fill="none" marker-end="url(#a)"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#0B2A3D"/></marker></defs><path d="M180 207 H215"/><path d="M375 207 H410"/><path d="M570 207 H605"/><path d="M765 207 H800"/><path d="M940 207 H975"/></g>
<rect x="300" y="385" width="600" height="110" rx="20" fill="#EAF2F4" stroke="#148C9B" stroke-width="4"/><text x="600" y="430" text-anchor="middle" font-family="Inter,Arial" font-size="20" font-weight="700" fill="#0B2A3D">APPEND-ONLY EVENT + MATERIAL LINEAGE STORE</text><text x="600" y="463" text-anchor="middle" font-family="Inter,Arial" font-size="17" fill="#243640">replay / audit / calibration / batch / functionalization / aging</text>
</svg>'''
write_text(FIG / "figure_05_membrane_world_zero.svg", svg)

# Figure 6: Biointerface World Zero
fig, ax = plt.subplots(figsize=(10.8, 5.7))
ax.axis("off")
ax.text(0.5, 0.95, "Biointerface World Zero: chemistry -> interaction -> sparse events -> topology -> decision", ha="center", va="top", fontsize=15.5, weight="bold", color=NAVY, transform=ax.transAxes)
# surface
ax.add_patch(plt.Rectangle((0.08, 0.34), 0.84, 0.10, color=CORAL, transform=ax.transAxes))
for x in np.linspace(0.12,0.88,11):
    ax.plot([x,x],[0.44,0.52],color=TEAL,lw=3,transform=ax.transAxes)
    ax.scatter([x],[0.54],s=80,color=GOLD,transform=ax.transAxes,zorder=5)
# cells/objects
rng = np.random.default_rng(4)
for x,y0,sz in zip(rng.uniform(0.13,0.87,10), rng.uniform(0.58,0.78,10), rng.uniform(120,300,10)):
    ax.scatter([x],[y0],s=sz,color=PURPLE,alpha=0.75,edgecolor=NAVY,linewidth=1,transform=ax.transAxes)
# event rays and topology
for x in [0.21,0.39,0.62,0.80]:
    ax.annotate("event", xy=(x,0.61), xytext=(x,0.86), ha="center", color=TEAL, fontsize=9, arrowprops=dict(arrowstyle="->", color=TEAL), xycoords=ax.transAxes)
ax.add_patch(FancyBboxPatch((0.10,0.08),0.24,0.13,boxstyle="round,pad=0.02",fc=LIGHT,ec=TEAL,lw=2,transform=ax.transAxes))
ax.text(0.22,0.145,"Surface lineage\nchemistry / sterilization / aging",ha="center",va="center",fontsize=10,weight="bold",color=NAVY,transform=ax.transAxes)
ax.add_patch(FancyBboxPatch((0.38,0.08),0.24,0.13,boxstyle="round,pad=0.02",fc=LIGHT,ec=PURPLE,lw=2,transform=ax.transAxes))
ax.text(0.50,0.145,"Topology descriptors\nclusters / loops / voids",ha="center",va="center",fontsize=10,weight="bold",color=NAVY,transform=ax.transAxes)
ax.add_patch(FancyBboxPatch((0.66,0.08),0.24,0.13,boxstyle="round,pad=0.02",fc=LIGHT,ec=GREEN,lw=2,transform=ax.transAxes))
ax.text(0.78,0.145,"B.C.E. decision\nconfidence / action / replay",ha="center",va="center",fontsize=10,weight="bold",color=NAVY,transform=ax.transAxes)
savefig(fig, "figure_06_biointerface_world_zero.png")

# Figure 7: application portfolio bubble chart
fig = plt.figure(figsize=(12.0, 6.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 0.85], wspace=0.24)
ax = fig.add_subplot(gs[0,0])
ax_leg = fig.add_subplot(gs[0,1])
apps = [r["Application"] for r in application_rows]
readiness = np.array([r["Near_term_readiness_1_to_5"] for r in application_rows], dtype=float)
material = np.array([4.5,4,4,2,3,2,2,5,1,2.5])
info = np.array([3.5,4.5,4.5,5,4.5,5,4.5,3.5,5,5])
size = 170 + readiness*100
sc = ax.scatter(material, info, s=size, c=readiness, cmap="viridis", alpha=0.80, edgecolor=NAVY, linewidth=0.9)
for idx,(x,y0) in enumerate(zip(material,info), start=1):
    ax.text(x,y0,str(idx),ha="center",va="center",fontsize=9,weight="bold",color="white")
ax.set_xlim(0,5.5); ax.set_ylim(0,5.5)
ax.set_xlabel("Material contribution from Arie's platform (qualitative)")
ax.set_ylabel("Information/operational contribution from Tom's corpus (qualitative)")
ax.set_title("Application portfolio", color=NAVY, weight="bold", loc="left")
ax.grid(alpha=0.2)
cb=fig.colorbar(sc,ax=ax,fraction=0.046,pad=0.04)
cb.set_label("Near-term readiness")
ax_leg.axis("off")
ax_leg.text(0.0,0.97,"Numbered opportunities",ha="left",va="top",fontsize=13,weight="bold",color=NAVY,transform=ax_leg.transAxes)
for i,(name,r) in enumerate(zip(apps,readiness),start=1):
    y0=0.91-(i-1)*0.087
    ax_leg.text(0.00,y0,f"{i}",ha="left",va="top",fontsize=10,weight="bold",color=TEAL,transform=ax_leg.transAxes)
    ax_leg.text(0.07,y0,f"{name}\nreadiness {r:g}/5",ha="left",va="top",fontsize=9.3,color=DARK,transform=ax_leg.transAxes)
fig.suptitle("Best opportunities combine strong material and strong operational contributions",fontsize=16,weight="bold",color=NAVY,y=0.99)
savefig(fig, "figure_07_application_portfolio.png")

# Figure 8: translation ladder
fig, ax = plt.subplots(figsize=(10.2, 6.2))
ax.axis("off")
ax.text(0.5, 0.96, "Translation ladder: keep the abstraction typed", ha="center", va="top", fontsize=16, weight="bold", color=NAVY, transform=ax.transAxes)
steps = [
    ("1. PHYSICAL SYSTEM", "molecules / membrane / cells / photons", CORAL),
    ("2. GOVERNING MODEL", "reaction kinetics / transport / Maxwell / mechanics", GOLD),
    ("3. OBSERVABLES", "spectra / flux / pressure / images / impedance", TEAL),
    ("4. BOUNDED GUARDS", "support + compatibility + measured crossing + confidence", PURPLE),
    ("5. TRANSITIONS", "bond / route / clean / bind / detach / alarm", NAVY),
    ("6. LINEAGE + DECISION", "event log / batch / calibration / action / replay", GREEN),
]
for i,(title,sub,c) in enumerate(steps):
    y = 0.82 - i*0.125
    w = 0.70 - i*0.045
    x = (1-w)/2
    ax.add_patch(FancyBboxPatch((x,y),w,0.085,boxstyle="round,pad=0.015",fc=c,ec="none",transform=ax.transAxes))
    ax.text(0.5,y+0.055,title,ha="center",va="center",color="white",weight="bold",fontsize=11,transform=ax.transAxes)
    ax.text(0.5,y+0.022,sub,ha="center",va="center",color="white",fontsize=9.5,transform=ax.transAxes)
    if i < len(steps)-1:
        ax.annotate("",xy=(0.5,y-0.025),xytext=(0.5,y-0.002),arrowprops=dict(arrowstyle="->",color=NAVY,lw=1.8),xycoords=ax.transAxes)
ax.text(0.5,0.035,"A topological or event metaphor is useful only after its physical variables, units, measurements,\nuncertainty, and transition semantics have been specified.",ha="center",va="bottom",color=DARK,fontsize=11,transform=ax.transAxes)
savefig(fig, "figure_08_translation_ladder.png")

# Figure 9: application readiness bars
fig, ax = plt.subplots(figsize=(9.4, 5.8))
ordered = sorted(application_rows, key=lambda r: r["Near_term_readiness_1_to_5"])
names = [r["Application"] for r in ordered]
vals = [r["Near_term_readiness_1_to_5"] for r in ordered]
bar_colors = [CORAL if v <= 2.5 else GOLD if v < 4 else TEAL for v in vals]
y = np.arange(len(names))
ax.barh(y, vals, color=bar_colors)
ax.set_yticks(y, names)
ax.set_xlim(0,5)
ax.set_xlabel("Near-term readiness (qualitative 1-5)")
ax.set_title("Application readiness: software/measurement paths lead material-biomedical deployment", color=NAVY, weight="bold")
ax.grid(axis="x", alpha=0.2)
for yi,v in zip(y,vals):
    ax.text(v+0.06, yi, f"{v:g}", va="center", fontsize=9)
savefig(fig, "figure_09_application_readiness.png")

# Run the included prototypes to create reproducible sample outputs.
import subprocess
for script in (PROTO / "polymer_step_growth_demo.py", PROTO / "membrane_event_sim.py"):
    subprocess.run(["python", str(script)], check=True)

# Small machine-readable summary.
summary = {
    "package": "Klootwijk Generational Topology Comparison",
    "generated_files": {
        "data_tables": len(list(DATA.glob("*.csv"))),
        "figures": len(list(FIG.glob("*"))),
        "analysis_notes": len(list(ANALYSIS.glob("*.md"))),
        "prototype_files": len(list(PROTO.glob("*"))),
        "references": len(references),
    },
    "central_finding": "Arie directly controlled molecular graph topology and phase accessibility; Tom's mature corpus primarily controls operational topology through support, compatibility, guards, transitions, uncertainty, and lineage.",
    "recommended_joint_direction": "A chemically addressable membrane or biointerface coupled to a bounded, event-sourced digital twin.",
}
write_text(DATA / "package_summary.json", json.dumps(summary, indent=2))

print(json.dumps(summary, indent=2))
