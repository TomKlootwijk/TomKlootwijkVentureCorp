# High-Impact Application Atlas for the Spherical-Support Event Calculus

**Physical, biomedical, digital, energy, logistics, civic and research systems**  

14 August 2026  

95 application hypotheses | 16 pilots | 38 metrics | 36 evidence anchors

> Status: application atlas and bounded research program; not performance, clinical, regulatory or system validation.

## Core thesis

The authoritative object is a typed state-and-event substrate. Images, grids, dashboards, matrices and documents become downstream views. A verified event requires relation/guard crossing, support admission and compatibility; transitions preserve lineage; external novelty remains logged.

```text
Finite grammar + external log -> state -> support -> compatibility -> guard/root -> event -> transition + lineage -> optional view
```

## Evidence labels
- Corpus canonical operator
- Established external component or standard
- Cross-domain inference
- Bounded pilot
- Frontier replacement hypothesis
- Rejected totalizing claim

## Auditable absence

```text
AbsenceEvent = ExpectedEvent AND CoverageComplete AND IntervalClosed AND no MatchingCompatibleEvent AND no ValidException
```
Missing telemetry remains unknown. Silence is not a diagnosis.

## Replacement strategy
Retain irreducible physical layers; add the query/event substrate; partially replace only bounded materialization stages; test frontier instruments with full system accounting; reject universal zero-cost claims.

## Biomedical & healthcare

### BIO-01 - MRI adaptive acquisition and sequence orchestration

- **Maturity:** Near-term research pilot
- **Boundary:** Addition to MRI acquisition and control; not a magnet replacement.
- **Proposed role:** Use local anatomical/physiological support, motion and safety compatibility, and quantitative guard conditions to adapt which measurements are acquired next.
- **Guard:** Acquire the next encoding block when predicted information gain or quantitative uncertainty crosses a declared threshold and safety constraints remain satisfied.
- **Auditable absence:** Expected calibration, physiological gating or coil data fail to arrive within the sequence window despite verified sensor coverage.
- **Metrics:** Diagnostic task performance; scan time; acquired samples; SAR and gradient limits; motion artifacts; events/J; false-adaptation rate.
- **Pilot:** Retrospective raw-data replay, then a phantom or volunteer study with a locked protocol and conventional reconstruction reference.
- **Risks:** Adaptive bias; missed pathology; instability; regulatory validation; patient safety.
- **References:** C0; R1; R2; R3; R5

### BIO-02 - MRI physics-constrained direct parameter query

- **Maturity:** Research prototype
- **Boundary:** Partial replacement of selected reconstruction stages for bounded tasks.
- **Proposed role:** Represent Bloch-model-compatible signal families as relations and query selected parameters or change events directly, optionally using images as a view.
- **Guard:** Parameter posterior or certified interval enters a clinically meaningful range under sufficient acquisition support.
- **Auditable absence:** A parameter cannot be certified because the required excitation/encoding support was never observed.
- **Metrics:** Parameter bias/variance; calibration; scan time; task AUC; reconstruction energy; uncertainty coverage.
- **Pilot:** Phantom study comparing direct parameter estimates, MRF-style matching and standard image-first workflow.
- **Risks:** Model mismatch; dictionary/expression growth; non-identifiability; clinical interpretability.
- **References:** C0; R3; R4

### BIO-03 - MRI narrow diagnostic instrument as an alternative to full imaging

- **Maturity:** Frontier concept
- **Boundary:** Alternative narrow instrument; full MRI replacement unsupported.
- **Proposed role:** Design a task-specific MR instrument that answers a bounded question such as relaxation change, flow threshold or lesion-presence probability without requiring a full diagnostic image.
- **Guard:** A task-specific signal relation crosses a validated threshold with confidence and safety conditions satisfied.
- **Auditable absence:** The expected signal support is absent, but only after coil, sequence and coverage integrity are verified.
- **Metrics:** Sensitivity/specificity; acquisition time; energy; footprint; cost; inconclusive rate; referral-to-full-MRI rate.
- **Pilot:** Start with a benchtop NMR/MR phantom and a single quantitative task.
- **Risks:** Loss of generality; hidden confounders; regulatory burden; false reassurance.
- **References:** C0; R1; R4; R5

### BIO-04 - MRI motion, respiratory and cardiac event gating

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Treat motion/physiology as continuous state and solve for compatible acquisition windows or correction events rather than replaying uniform frames.
- **Guard:** Predicted motion enters an admissible window and a sequence block is admitted; otherwise hold or redirect.
- **Auditable absence:** A required quiet-window event never occurs within the allowed interval.
- **Metrics:** Rejected acquisitions; reacquisition rate; image/parameter quality; latency; patient time.
- **Pilot:** Integrate an external motion sensor with retrospective MR sequence logs.
- **Risks:** Sensor drift; phase mismatch; prolonged scans; selection bias.
- **References:** C0; R1; R3

### BIO-05 - MRI safety and implant compatibility engine

- **Maturity:** Implementable integration
- **Boundary:** Addition to safety workflow.
- **Proposed role:** Model implant identity, field strength, sequence limits and patient state as a compatibility predicate with provenance and explicit reason codes.
- **Guard:** Scan becomes admissible only when all required device attributes and MR-conditional constraints are present and current.
- **Auditable absence:** Missing implant identity or condition is logged as a blocking absence, not silently treated as safe.
- **Metrics:** Screening completeness; prevented unsafe scans; delay time; override rate; auditability.
- **Pilot:** FHIR-compatible registry and rules engine in one MRI service line.
- **Risks:** Incorrect device metadata; stale labeling; workflow bypass; privacy.
- **References:** C0; R5; R6

### BIO-06 - Ultrasound echo-event acquisition and beam control

- **Maturity:** Research prototype
- **Boundary:** Addition or partial replacement of acquisition/reconstruction for narrow tasks.
- **Proposed role:** Use level-crossing or feature-triggered acquisition, local beam support and direct arrival-time/flow events to reduce irrelevant conversion and processing.
- **Guard:** Echo arrival, Doppler shift or tissue-boundary relation crosses a validated threshold within the beam support.
- **Auditable absence:** Expected echo absent only when transducer contact and acoustic coverage are verified.
- **Metrics:** Samples/event; energy; latency; sensitivity; localization error; image equivalence when a view is produced.
- **Pilot:** Phantom and flow-loop test with simultaneous conventional RF capture.
- **Risks:** Information loss; nonlinear propagation; aliasing; difficult certification.
- **References:** C0; R31

### BIO-07 - CT/PET task-specific sparse acquisition

- **Maturity:** Research concept
- **Boundary:** Addition/partial replacement in bounded tasks.
- **Proposed role:** Select measurement supports adaptively and solve for bounded findings or quantitative changes with explicit uncertainty, retaining full reconstruction as fallback.
- **Guard:** Task confidence reaches a preset boundary without violating dose/count constraints.
- **Auditable absence:** A required angular or count support is absent; result remains inconclusive rather than negative.
- **Metrics:** Dose or tracer counts; task performance; scan time; uncertainty; fallback rate.
- **Pilot:** Digital phantom and archived raw-data challenge.
- **Risks:** Dose-selection bias; hallucinated structure; regulatory validation.
- **References:** C0

### BIO-08 - Microscopy and cell-culture event microscope

- **Maturity:** Near-term research pilot
- **Boundary:** Addition and, for narrow assays, partial replacement of continuous imaging.
- **Proposed role:** Use local optical supports, event sensors or analog prefilters to emit only lineage-aware cell events such as division, migration, morphology change or fluorescence threshold crossing.
- **Guard:** A tracked cell lineage crosses a morphology, intensity or interaction guard with sufficient optical support.
- **Auditable absence:** Expected cell or marker observation absent only when field coverage and sensor health are known.
- **Metrics:** Events/J; bytes/experiment; missed/false events; lineage accuracy; phototoxic exposure.
- **Pilot:** Parallel conventional imaging and event extraction on a well-defined assay.
- **Risks:** Rare-event miss; lineage swaps; optical drift; loss of serendipitous observations.
- **References:** C0; R30

### BIO-09 - ICU and ward event-native patient monitoring

- **Maturity:** Near-term pilot
- **Boundary:** Addition to monitoring and clinical decision support.
- **Proposed role:** Maintain a continuous patient state, local physiological supports, compatibility with interventions and an auditable event record for threshold crossings and trends.
- **Guard:** A validated physiological relation crosses a severity guard and matches the patient context, sensor quality and treatment phase.
- **Auditable absence:** Expected vital, medication response or reassessment is absent despite confirmed observation coverage.
- **Metrics:** Alarm precision/recall; time to recognition; clinician workload; missed-data rate; intervention outcomes.
- **Pilot:** Silent-mode retrospective validation followed by prospective shadow deployment.
- **Risks:** Alarm overreach; sensor artifacts; automation bias; privacy; clinical liability.
- **References:** C0; R6; R7; R8; R10

### BIO-10 - Surgical navigation and tool-tissue time-of-contact

- **Maturity:** Research prototype
- **Boundary:** Addition.
- **Proposed role:** Represent tool and anatomy trajectories continuously; solve certified time-of-contact events within local support and surgical permissions.
- **Guard:** Earliest predicted tool/tissue contact or no-go-zone crossing under uncertainty.
- **Auditable absence:** Tracking signal absence blocks the action rather than implying clearance.
- **Metrics:** Contact-time error; missed crossings; latency; false stops; surgeon workload.
- **Pilot:** Simulation and benchtop phantom with a conventional navigation baseline.
- **Risks:** Deformable anatomy; tracking dropout; model error; safety certification.
- **References:** C0; R33; R34

### BIO-11 - Medication, infusion and closed-loop therapy guard engine

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Join medication identity, dose lineage, patient state, timing and device status through compatibility and event guards; keep clinicians in the loop.
- **Guard:** Dose or infusion transition is admitted only when patient, order, pump, drug, route and timing are compatible.
- **Auditable absence:** Expected reassessment, pump acknowledgment or lab result is missing after its due interval.
- **Metrics:** Medication errors; delayed doses; false blocks; response-monitoring completeness; audit time.
- **Pilot:** One high-risk infusion pathway in simulation and shadow mode.
- **Risks:** Rule brittleness; alert fatigue; override handling; governance.
- **References:** C0; R6; R7; R8

### BIO-12 - Cradle-to-life longitudinal patient journey substrate

- **Maturity:** Implementable architecture pilot
- **Boundary:** Addition beneath EHRs; not an autonomous medical authority.
- **Proposed role:** Use a stable person lineage with prenatal, birth, neonatal, childhood, adult and elder branches; represent encounters and documents as views over a consent- and provenance-aware event graph.
- **Guard:** Care transitions, referrals, procedures, consent changes and outcomes are typed events tied to the person lineage.
- **Auditable absence:** Expected follow-up, screening, handoff, result or support service is absent only under an explicit obligation and coverage rule.
- **Metrics:** Record-linkage errors; care-gap closure; duplicate testing; handoff failures; patient access; consent compliance.
- **Pilot:** One maternal-neonatal or chronic-care pathway across two organizations using FHIR events and PROV lineage.
- **Risks:** Identity matching; privacy; institutional power; data quality; patient autonomy.
- **References:** C0; R6; R7; R8; R28

### BIO-13 - Maternal, fetal, birth and neonatal journey coordination

- **Maturity:** Near-term information-system pilot
- **Boundary:** Addition.
- **Proposed role:** Model mother, fetus/newborn, samples, devices and care teams as related but distinct lineages, with consent and event transitions at birth.
- **Guard:** Birth, transfer, screening, feeding, medication and follow-up transitions preserve parent/child lineage and provenance.
- **Auditable absence:** Expected screening or post-discharge follow-up is absent with verified obligation and outreach coverage.
- **Metrics:** Missed screens; duplicate identity; handoff delay; maternal/newborn linkage accuracy.
- **Pilot:** Neonatal screening and follow-up pathway.
- **Risks:** Identity errors; consent complexity; sensitive data exposure.
- **References:** C0; R6; R8

### BIO-14 - Hospital flow, beds, theatres and discharge event twin

- **Maturity:** Near-term pilot
- **Boundary:** Addition/partial replacement of dashboard-centric coordination.
- **Proposed role:** Represent patient flow, rooms, staff, equipment and constraints as a compatibility-gated event system with next-event and counterfactual queries.
- **Guard:** A transfer or discharge becomes admissible when clinical, staffing, bed, transport and documentation conditions are satisfied.
- **Auditable absence:** Required consult, result, transport or discharge action has not occurred by the due interval.
- **Metrics:** Length of stay; boarding time; cancelled procedures; idle beds; false-ready rate; staff burden.
- **Pilot:** One ward-to-discharge process in shadow mode.
- **Risks:** Optimization against patient welfare; unstable priorities; data latency.
- **References:** C0; R6; R7; R10

### BIO-15 - Mental-health longitudinal care and research substrate

- **Maturity:** Research and governance pilot
- **Boundary:** Addition to records and research; not automated diagnosis or therapy.
- **Proposed role:** Maintain patient-authored goals, consent, context, development, environment, observations and interventions as lineage-aware events and dimensional trajectories.
- **Guard:** A care or research transition is admitted under explicit consent, role, time and safety predicates, with human review.
- **Auditable absence:** Expected check-in or follow-up may be logged as absent, but lack of digital activity is never equated with deterioration without corroboration.
- **Metrics:** Continuity; patient control; follow-up completion; bias; clinician burden; data access.
- **Pilot:** Patient-controlled longitudinal research registry with independent ethics review.
- **Risks:** Surveillance; stigma; coercion; false inference; crisis responsibility.
- **References:** C0; R8; R9; R10; R11

### BIO-16 - Clinical trial and observational study event graph

- **Maturity:** Implementable pilot
- **Boundary:** Addition/partial replacement of document-centric trial operations.
- **Proposed role:** Create a versioned event and provenance graph connecting protocol, consent, intervention, measurement, deviation, analysis and publication.
- **Guard:** Every trial action creates a typed event with protocol version, authority, subject, time and before/after state.
- **Auditable absence:** Expected visit, sample, outcome or adverse-event assessment is explicitly expired, waived or observed.
- **Metrics:** Protocol deviations; reconciliation time; missing data; audit readiness; reproducibility.
- **Pilot:** Single-site prospective study with export to standard regulatory documents.
- **Risks:** Operational complexity; privacy; legal admissibility; version drift.
- **References:** C0; R6; R28; R29

### BIO-17 - Biomedical sample and biobank lineage

- **Maturity:** Implementable integration
- **Boundary:** Addition.
- **Proposed role:** Use lineage addresses and split/merge rules for specimen, aliquot, derivative, assay and storage events.
- **Guard:** A sample transition is admitted only when identity, consent, chain of custody, storage and assay compatibility are satisfied.
- **Auditable absence:** Expected receipt, temperature record or assay result is missing after verified custody.
- **Metrics:** Misidentification; unusable samples; audit time; consent violations; freezer excursions.
- **Pilot:** One biobank workflow with barcode/EPCIS and PROV mapping.
- **Risks:** Legacy identifiers; merge ambiguity; privacy; operational adoption.
- **References:** C0; R26; R27; R28

### BIO-18 - Protein dynamics and molecular-event simulation

- **Maturity:** Research prototype
- **Boundary:** Hybrid addition; broad replacement unsupported.
- **Proposed role:** For selected relation families, solve binding, contact, conformational and threshold events directly, while retaining conventional simulation for unresolved regions.
- **Guard:** Earliest compatible contact, barrier crossing or conformational transition within a bounded model.
- **Auditable absence:** A predicted event is absent only when the modeled support and force field are valid; otherwise unknown.
- **Metrics:** Event-time error; energy conservation; missed states; compute/J; expression growth.
- **Pilot:** Small molecule or coarse-grained benchmark against MD trajectories.
- **Risks:** Chaotic dynamics; model inadequacy; event explosion; no general closed form.
- **References:** C0

### BIO-19 - CRISPR and gene-editing in-silico candidate pruning

- **Maturity:** Research concept
- **Boundary:** Addition to design; not physical gene control.
- **Proposed role:** Use local genomic/epigenetic support, compatibility predicates and lineage to rank candidate interventions and downstream event risks before laboratory testing.
- **Guard:** Candidate passes sequence, structure, cell-context, off-target and policy guards with uncertainty.
- **Auditable absence:** Missing cell-context evidence is a blocking absence, not proof of safety.
- **Metrics:** Off-target ranking; experimental hit rate; uncertainty calibration; provenance.
- **Pilot:** Benchmark on public datasets; no clinical use.
- **Risks:** Overconfidence; incomplete biology; dual use; ethical concerns.
- **References:** C0; R8; R9

### BIO-20 - Public-health event and service-absence observatory

- **Maturity:** Near-term data pilot
- **Boundary:** Addition.
- **Proposed role:** Use event notifications, local geographic supports, lineage and explicit expected-report contracts to distinguish true absence, delayed data and sensor failure.
- **Guard:** Case, lab, wastewater, capacity or intervention events cross a public-health guard.
- **Auditable absence:** Expected report absent only after source coverage, reporting obligation and deadline are verified.
- **Metrics:** Reporting delay; missingness classification; false alarms; privacy; action time.
- **Pilot:** One syndromic or wastewater surveillance program with transparent absence rules.
- **Risks:** Re-identification; political misuse; reporting bias; jurisdiction conflicts.
- **References:** C0; R6; R7; R8; R24

## Semiconductor & physical manufacturing

### PHY-01 - ASML/EUV event-native exposure and scanner control

- **Maturity:** Research/industry pilot
- **Boundary:** Addition to scanner control; physical exposure system remains.
- **Proposed role:** Add a query-first state/event layer for wafer-stage trajectories, dose, focus, overlay, contamination and subsystem readiness.
- **Guard:** Expose only when stage, source, reticle, wafer, focus, dose and safety states are compatible; latch deviations as events.
- **Auditable absence:** Expected metrology, droplet/source, stage or vacuum readiness event is absent within the control window.
- **Metrics:** Overlay; focus/dose error; wafers/hour; downtime; false aborts; control energy.
- **Pilot:** Offline replay of scanner logs and a hardware-in-the-loop subsystem test.
- **Risks:** Proprietary complexity; nanometre tolerances; latency; certification.
- **References:** C0; R12; R13; R14

### PHY-02 - Computational lithography hotspot query engine

- **Maturity:** Research prototype
- **Boundary:** Addition/partial replacement of selected optimization passes.
- **Proposed role:** Represent pattern constraints and process windows as local supports and guards; query hotspot events and compatible corrections instead of materializing every candidate globally.
- **Guard:** A local pattern/process relation exits the manufacturable window under a declared model.
- **Auditable absence:** No hotspot observation is valid only under verified model coverage; unmodeled pattern classes remain unknown.
- **Metrics:** Runtime; memory; hotspot recall; process-window improvement; correction complexity.
- **Pilot:** Public benchmark or synthetic mask set comparing local event solver with conventional simulation.
- **Risks:** Model closure; missed long-range effects; stochastic resist behavior; IP constraints.
- **References:** C0; R12

### PHY-03 - Reduced-order Maxwell/rigorous simulation query service

- **Maturity:** Research prototype
- **Boundary:** Addition.
- **Proposed role:** Compile bounded parameter families into reduced or surrogate relation models with certified validity regions and fall back to full solvers outside support.
- **Guard:** Parameter query is answered only within certified support and error tolerance.
- **Auditable absence:** A result is absent/inconclusive when the query lies outside the reduced model support.
- **Metrics:** Error bound; solver speed; fallback rate; memory; process-window coverage.
- **Pilot:** Reduced-basis study on a narrow mask family.
- **Risks:** Extrapolation; hidden coupling; certification overhead.
- **References:** C0; R12; R13

### PHY-04 - Reticle, wafer and process lineage graph

- **Maturity:** Implementable integration
- **Boundary:** Addition beneath MES/yield systems.
- **Proposed role:** Use immutable lineage, split/merge and event records across design, mask, exposure, etch, metrology and yield.
- **Guard:** Every custody, recipe, exposure, inspection and disposition creates a versioned event.
- **Auditable absence:** Expected metrology, hold release or lot movement is absent after a declared due interval.
- **Metrics:** Root-cause time; genealogy completeness; scrap containment; auditability.
- **Pilot:** One process module or product family.
- **Risks:** Identifier mismatch; data volume; supplier boundaries; confidentiality.
- **References:** C0; R26; R27; R28

### PHY-05 - Wafer-stage and robot continuous motion scheduling

- **Maturity:** Near-term research pilot
- **Boundary:** Addition.
- **Proposed role:** Use continuous trajectories, local supports and exact/conservative time-of-impact events rather than only fixed-rate checking.
- **Guard:** Earliest contact, clearance or timing-constraint crossing under bounded trajectory uncertainty.
- **Auditable absence:** Tracking absence blocks motion; it never implies free space.
- **Metrics:** Cycle time; missed collision probability; false stops; timing jitter.
- **Pilot:** Digital twin and hardware-in-the-loop stage/robot cell.
- **Risks:** Trajectory uncertainty; flexible structures; numerical degeneracy.
- **References:** C0; R33; R34

### PHY-06 - Fab chamber next-fault digital twin

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Represent pressure, temperature, flow, plasma, chemistry and equipment states continuously; solve next-fault and regime-change events with calibrated uncertainty.
- **Guard:** Earliest compatible threshold or regime transition under a validated physical model.
- **Auditable absence:** Expected sensor or actuator acknowledgment absent with coverage known.
- **Metrics:** Unplanned downtime; false alarms; yield; maintenance hours; model error.
- **Pilot:** One chamber subsystem in shadow mode.
- **Risks:** Model drift; rare faults; sensor bias; action latency.
- **References:** C0

### PHY-07 - Metrology optical prefilter and B.C.E. detector

- **Maturity:** Frontier lab prototype
- **Boundary:** Addition; narrow analog front end.
- **Proposed role:** Use calibrated waveguide/optofluidic transfer functions and compatibility gates to detect narrow optical events before full digitization.
- **Guard:** Selected wavelength/polarization/mode response crosses a calibrated guard.
- **Auditable absence:** Expected reference-channel event absent indicates drift or hardware fault, not sample absence.
- **Metrics:** Verified events/J; insertion loss; miss/false rate; calibration interval; throughput.
- **Pilot:** Hollowlens-style benchtop metrology proxy with electronic baseline.
- **Risks:** Optical loss; drift; liquid instability; ADC still needed; limited task range.
- **References:** C0

### PHY-08 - PCB routing, revision and signal-integrity event graph

- **Maturity:** Near-term software pilot
- **Boundary:** Addition/partial replacement of selected checks.
- **Proposed role:** Treat traces, vias, components and constraints as lineage-aware relations; use local support for clearance and compatibility for electrical/net semantics.
- **Guard:** Clearance, impedance, timing or net-compatibility relation crosses a guard.
- **Auditable absence:** Expected test or sign-off absent is explicit.
- **Metrics:** DRC runtime; missed violations; revision traceability; ECO turnaround.
- **Pilot:** One board design with conventional DRC reference.
- **Risks:** Nonlocal electromagnetic effects; rule explosion; tool integration.
- **References:** C0

### PHY-09 - Pick-and-place event-native cell

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Combine continuous motion, local supports, compatibility and lineage for part/nozzle/feeder events.
- **Guard:** Pick or placement is admitted when pose, part identity, nozzle, feeder, board and clearance states match.
- **Auditable absence:** Expected component present but not observed under verified camera/feeder coverage.
- **Metrics:** Cycle time; mispicks; placement error; stoppages; energy/placed part.
- **Pilot:** One SMT cell in shadow or simulation mode.
- **Risks:** Occlusion; calibration; part damage; false absence.
- **References:** C0; R26; R33; R34

### PHY-10 - Additive manufacturing melt-pool event control

- **Maturity:** Research prototype
- **Boundary:** Addition.
- **Proposed role:** Model melt-pool geometry, thermal state, feedstock and scan trajectory continuously; trigger corrective transitions at guard crossings.
- **Guard:** Melt-pool, porosity-risk or thermal-gradient relation exits process support.
- **Auditable absence:** Expected sensor or powder-delivery event absent blocks confidence.
- **Metrics:** Defect rate; scrap; energy/kg; latency; calibration.
- **Pilot:** Single material and geometry with high-speed sensing.
- **Risks:** Complex multiphysics; sensor occlusion; actuation limits.
- **References:** C0

### PHY-11 - CNC and tool-wear next-event control

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Represent tool state, workpiece lineage and continuous load/vibration relations; predict wear threshold and collision events.
- **Guard:** Predicted wear, chatter, overload or collision guard crossing.
- **Auditable absence:** Expected cut completion or sensor signature absent under verified coverage.
- **Metrics:** Tool life; scrap; downtime; false alarms; energy/part.
- **Pilot:** One machining process with historical data and shadow prediction.
- **Risks:** Model drift; varying materials; sensor noise.
- **References:** C0

### PHY-12 - Industrial optical spectroscopy classifier

- **Maturity:** Frontier lab pilot
- **Boundary:** Addition/alternative narrow instrument.
- **Proposed role:** Use tunable optical supports, mode compatibility and threshold events to detect selected chemical/physical signatures before or alongside full spectra.
- **Guard:** Spectral/mode response crosses a calibrated target guard.
- **Auditable absence:** Reference line absent indicates instrument fault; target absence requires full support coverage.
- **Metrics:** Events/J; limit of detection; false alarms; calibration; cost.
- **Pilot:** Known gas or liquid assay with simultaneous reference spectrometer.
- **Risks:** Cross-sensitivity; drift; environmental dependence.
- **References:** C0

### PHY-13 - Quality inspection as direct relation query

- **Maturity:** Near-term pilot
- **Boundary:** Addition/partial replacement for narrow inspections.
- **Proposed role:** Use local support and event-based or analog prefilters for specific geometry, surface or assembly relations; retain images only for exceptions.
- **Guard:** Feature deviation crosses tolerance under sufficient illumination and pose support.
- **Auditable absence:** Expected feature not observed under verified coverage; otherwise unknown.
- **Metrics:** Bytes/part; events/J; miss/false; inspection time; exception-image rate.
- **Pilot:** Single repetitive inspection task.
- **Risks:** Novel defects; lighting; model coverage; evidence retention.
- **References:** C0; R30

### PHY-14 - Photonic relation kernel for fixed industrial queries

- **Maturity:** Frontier prototype
- **Boundary:** Addition; domain-specific accelerator.
- **Proposed role:** Map stable linear transforms to calibrated interferometric hardware, while nonlinear logic, uncertainty, lineage and policy remain digital.
- **Guard:** Optical output crosses a calibrated guard and digital sidecar validates context.
- **Auditable absence:** Reference-channel absence or drift blocks result.
- **Metrics:** End-to-end events/J; accuracy; calibration; insertion loss; latency.
- **Pilot:** Small MZI mesh on one sensing or control task.
- **Risks:** I/O and ADC costs; drift; precision; programmability.
- **References:** C0; R32

## Energy, climate & infrastructure

### ENG-01 - Grid state and contingency query substrate

- **Maturity:** Research/utility pilot
- **Boundary:** Addition beneath EMS/DERMS.
- **Proposed role:** Maintain a versioned grid state and solve local support, compatibility and next-limit events; use conventional power-flow solvers as typed physical services.
- **Guard:** Earliest thermal, voltage, frequency, stability or protection guard crossing under a scenario branch.
- **Auditable absence:** Expected telemetry or breaker state absent is classified separately from a normal zero.
- **Metrics:** Contingency solve time; missed events; false alarms; operator workload; events/J.
- **Pilot:** Offline replay and shadow control-room pilot for one region.
- **Risks:** Model error; cyber risk; event explosion; operator trust.
- **References:** C0; R15; R16

### ENG-02 - Distributed energy and microgrid compatibility router

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Use compatibility predicates for device capability, grid state, market/policy and ownership; route only admitted events.
- **Guard:** Dispatch or islanding transition admitted when electrical, contractual, cyber and timing predicates match.
- **Auditable absence:** Expected device acknowledgment or telemetry absent after a verified communication window.
- **Metrics:** Dispatch success; interoperability failures; curtailment; resilience; cyber incidents.
- **Pilot:** Campus microgrid or simulated feeder.
- **Risks:** Vendor heterogeneity; cyber attack; conflicting objectives.
- **References:** C0; R15; R17

### ENG-03 - Protection and disturbance event engine

- **Maturity:** Near-term research pilot
- **Boundary:** Addition to analysis and coordination, not unvalidated relay replacement.
- **Proposed role:** Represent disturbance supports, device compatibility, guard crossings and event lineage explicitly; keep certified relays authoritative.
- **Guard:** Fault or instability relation crosses a certified boundary in the protected zone.
- **Auditable absence:** Expected breaker trip or relay acknowledgment absent within the mandated interval.
- **Metrics:** Detection time; selectivity; false trips; coordination; event reconstruction.
- **Pilot:** Digital real-time simulator with relay-in-the-loop.
- **Risks:** Safety criticality; timing; model mismatch; cyber.
- **References:** C0; R15

### ENG-04 - Solar PV string and module event twin

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Use local array/string support, expected-yield relations, inverter compatibility and lineage to detect shading, soiling, mismatch, connector and degradation events.
- **Guard:** Measured/predicted energy balance exits a calibrated support or a component relation crosses a fault guard.
- **Auditable absence:** Expected generation or telemetry absent only after irradiance, availability and sensor coverage are verified.
- **Metrics:** Energy recovered; detection delay; false alarms; O&M cost; events/J; curtailment avoided.
- **Pilot:** One commercial array with parallel conventional monitoring.
- **Risks:** Weather-model error; sensor drift; maintenance burden.
- **References:** C0; R17; R18

### ENG-05 - Solar inverter and MPPT event-native control

- **Maturity:** Research pilot
- **Boundary:** Addition; low-level control remains conventional unless certified.
- **Proposed role:** Add local event rules for mode changes, mismatch, voltage support and thermal limits; investigate level-crossing conversion for sparse supervisory signals.
- **Guard:** Operating point, thermal, grid-support or protection relation crosses a guard.
- **Auditable absence:** Expected inverter response absent under verified communications and power availability.
- **Metrics:** Wh delivered per control joule; tracking efficiency; response time; thermal cycling.
- **Pilot:** Controller-in-the-loop PV emulator.
- **Risks:** Control stability; harmonics; standards compliance; converter noise.
- **References:** C0; R17; R31

### ENG-06 - Battery state-of-health and thermal-runaway guard engine

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Use continuous state relations, lineage of cells/modules and next-event guards for degradation, imbalance, venting and thermal risk.
- **Guard:** Predicted temperature, voltage, pressure, impedance or imbalance crosses a certified threshold.
- **Auditable absence:** Expected sensor/contactor response absent; never interpret missing telemetry as safe.
- **Metrics:** Prediction horizon; false/late trips; cycle life; pack availability; compute energy.
- **Pilot:** Battery cycler and abuse-test dataset in shadow mode.
- **Risks:** Cell variability; rare-event data; safety certification.
- **References:** C0

### ENG-07 - EV charging and fleet energy routing

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Use vehicle/charger/grid compatibility, local feeder support and next-departure/constraint events with lineage-aware energy accounting.
- **Guard:** Charge/discharge transition admitted under connector, battery, departure, feeder and tariff constraints.
- **Auditable absence:** Expected vehicle arrival, charger acknowledgment or departure readiness absent.
- **Metrics:** Peak demand; missed departures; energy cost; battery wear; charger utilization.
- **Pilot:** Municipal or depot fleet.
- **Risks:** Data quality; user autonomy; tariff volatility; cyber.
- **References:** C0; R15

### ENG-08 - Gas, oil, hydrogen and CO2 pipeline leak/rupture event twin

- **Maturity:** Near-term research pilot
- **Boundary:** Addition/upgrade to CPM and response coordination.
- **Proposed role:** Express leak/rupture, negative-pressure-wave and valve-response events with support, compatibility, uncertainty and auditable negative events.
- **Guard:** Hydraulic/mass-balance or wave relation crosses a leak guard and is compatible with operating transients.
- **Auditable absence:** Expected valve closure, pressure recovery or sensor report absent within a verified interval.
- **Metrics:** Leak size/time sensitivity; location error; false alarms; isolated volume; response time.
- **Pilot:** Historical replay and controlled test loop.
- **Risks:** Small leaks; transient confusion; sensor failure; regulatory requirements.
- **References:** C0; R19; R20

### ENG-09 - Water distribution leak and service-loss event system

- **Maturity:** Near-term municipal pilot
- **Boundary:** Addition.
- **Proposed role:** Combine hydraulic relations, local geographic support, meter/sensor compatibility and 311 reports; explicitly model service absence.
- **Guard:** Pressure/flow imbalance or service complaint crosses a localized guard.
- **Auditable absence:** Expected pressure, meter heartbeat or repair completion absent under coverage.
- **Metrics:** Water loss; detection time; false alarms; repair time; equity by neighborhood.
- **Pilot:** One pressure district.
- **Risks:** Sparse sensors; demand uncertainty; privacy; false absence.
- **References:** C0; R23; R24

### ENG-10 - Industrial combustion, boilers and process heat next-event optimization

- **Maturity:** Research pilot
- **Boundary:** Addition.
- **Proposed role:** Layer a query-first event twin over validated thermodynamic/control models to predict limit crossings, fouling and efficiency transitions.
- **Guard:** Efficiency, emissions, temperature or pressure relation crosses a guard under a candidate operating branch.
- **Auditable absence:** Expected actuator or sensor response absent.
- **Metrics:** Fuel per output; emissions; downtime; false interventions; control energy.
- **Pilot:** One boiler or furnace subsystem in shadow mode.
- **Risks:** Model mismatch; unsafe optimization; operator acceptance.
- **References:** C0

### ENG-11 - Fossil-fuel reduction through event-native operations

- **Maturity:** Portfolio hypothesis
- **Boundary:** Cross-sector addition; not a substitute for clean-energy policy or physical transition.
- **Proposed role:** Apply event-native sensing, direct queries, provenance and compatibility to reduce avoidable compute, leaks, curtailment, idling and overproduction.
- **Guard:** Avoided-energy or avoided-emission action occurs only when a verified event justifies it.
- **Auditable absence:** Missing data cannot be counted as avoided use or emissions.
- **Metrics:** Net J saved; kgCO2e avoided; rebound; capital cost; verification confidence.
- **Pilot:** Bundle grid, PV, pipeline and logistics pilots with a common measurement protocol.
- **Risks:** Rebound; greenwashing; boundary manipulation; lifecycle omissions.
- **References:** C0; R15; R18; R19

### ENG-12 - Data-center and AI energy workload router

- **Maturity:** Research prototype
- **Boundary:** Addition.
- **Proposed role:** Use local workload support, compatibility, event thresholds and hardware-specific energy models to choose electronic, analog or photonic paths.
- **Guard:** Route a task when accuracy, latency, energy, precision and hardware calibration predicates are satisfied.
- **Auditable absence:** Expected accelerator result or calibration signal absent; fall back.
- **Metrics:** J/query; throughput; accuracy; data movement; fallback rate.
- **Pilot:** One fixed inference or signal-processing workload across CPU/GPU/photonic emulator.
- **Risks:** I/O dominates; calibration; model portability; misleading component-only metrics.
- **References:** C0; R32

### ENG-13 - Building HVAC and indoor-environment event twin

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Use local zone supports, occupancy/privacy compatibility and next-comfort/air-quality/fault events; store exceptions and novelty rather than every derived view.
- **Guard:** Comfort, CO2, humidity, equipment or demand guard crossing.
- **Auditable absence:** Expected occupancy or sensor signal absent only with coverage/consent known.
- **Metrics:** kWh; comfort; indoor air quality; false occupancy; maintenance.
- **Pilot:** One building zone with parallel BMS.
- **Risks:** Privacy; occupancy inference; sensor drift; control oscillation.
- **References:** C0; R21; R24

### ENG-14 - Wind turbine and rotating-equipment next-fault engine

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Represent phase, rotational state, load and component lineage; solve bearing, imbalance and fatigue guard events.
- **Guard:** Vibration/temperature/load relation crosses a calibrated fault guard.
- **Auditable absence:** Expected phase marker or sensor heartbeat absent.
- **Metrics:** Lead time; false alarms; downtime; maintenance cost; energy availability.
- **Pilot:** Historical replay and one instrumented turbine/test rig.
- **Risks:** Nonstationary load; rare failures; sensor degradation.
- **References:** C0

### ENG-15 - District heating, cooling and thermal-network routing

- **Maturity:** Research pilot
- **Boundary:** Addition.
- **Proposed role:** Use continuous transport relations, local branch support and compatibility to predict demand/temperature events and route heat.
- **Guard:** Supply/return temperature, pressure or storage state crosses an operational guard.
- **Auditable absence:** Expected demand or telemetry absent under verified coverage.
- **Metrics:** Fuel/electricity; losses; comfort; peak reduction; event accuracy.
- **Pilot:** Campus thermal network digital twin.
- **Risks:** Long delays; uncertain demand; actuator limits.
- **References:** C0

### ENG-16 - Carbon and energy provenance ledger

- **Maturity:** Implementable information-system pilot
- **Boundary:** Addition.
- **Proposed role:** Use lineage, versioned factors, compatibility and explicit missingness to make every claim reconstructable and branch-aware.
- **Guard:** A carbon/energy claim is emitted only when source data, factor version, scope and ownership predicates are complete.
- **Auditable absence:** Missing activity or factor data remains a declared gap, not a zero.
- **Metrics:** Coverage; audit time; recalculation reproducibility; uncertainty; double-count prevention.
- **Pilot:** One product or facility lifecycle.
- **Risks:** Boundary gaming; factor uncertainty; supplier data gaps.
- **References:** C0; R28; R29

### ENG-17 - Renewable curtailment and storage counterfactual planner

- **Maturity:** Near-term planning pilot
- **Boundary:** Addition.
- **Proposed role:** Use isolated branches over a shared state to ask which intervention prevents the next constraint while preserving provenance.
- **Guard:** Branch-specific constraint or reliability event under a candidate storage, network or demand-response action.
- **Auditable absence:** Expected asset availability absent in a branch is explicit.
- **Metrics:** Curtailment avoided; reliability; cost; model runtime; branch explainability.
- **Pilot:** One feeder or region with locked baseline scenarios.
- **Risks:** Scenario explosion; uncertain futures; policy assumptions.
- **References:** C0; R15; R16

### ENG-18 - Environmental sensing with event/absence semantics

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Use local support, sensor provenance, coverage contracts and threshold events; distinguish non-detection from sensor silence.
- **Guard:** Pollutant or ecological indicator crosses a calibrated guard under valid sensor support.
- **Auditable absence:** Non-detection is emitted only when detection capability and sampling coverage are certified.
- **Metrics:** Detection delay; false absence; sensor uptime; spatial coverage; energy.
- **Pilot:** One air-quality or water-quality network.
- **Risks:** Calibration; sparse coverage; community trust; interpretation.
- **References:** C0; R24

## Digital, compute & data pipelines

### DIG-01 - Equation-world simulation kernel

- **Maturity:** Research prototype
- **Boundary:** Partial replacement of the authoritative simulation layer in bounded domains.
- **Proposed role:** Implement direct state_at, next_event, support, coupling, routing and lineage queries for a bounded relation family; render only on demand.
- **Guard:** Earliest admitted relation crossing with certified root/interval.
- **Auditable absence:** Expected event absent only with complete relation/support coverage.
- **Metrics:** Query cost; event ordering; memory/novelty; correctness; expression growth.
- **Pilot:** Equation World Zero benchmark versus frame stepping and event queue.
- **Risks:** Event/branch explosion; numerical conditioning; limited relation family.
- **References:** C0

### DIG-02 - Raymarching/rasterization bypass for state and collision

- **Maturity:** Research prototype
- **Boundary:** Partial replacement of state/collision pipeline; rendering remains optional.
- **Proposed role:** Move authority to relations/events and use ray/raster methods only as materialized views; collision and causality use direct queries.
- **Guard:** Visibility, contact or transition query solved from relations rather than image sampling.
- **Auditable absence:** No pixel or sample is never evidence that an entity is absent from state.
- **Metrics:** State query time; collision correctness; render independence; memory; view consistency.
- **Pilot:** Procedural 2D/3D scene with headless test suite and optional renderer.
- **Risks:** Hard implicit geometry; projection mismatch; renderer feedback.
- **References:** C0; R33

### DIG-03 - Dense linear-algebra avoidance planner

- **Maturity:** Research architecture
- **Boundary:** Addition/partial workload replacement, not elimination of linear algebra.
- **Proposed role:** Use support pruning, typed relations, sparse/structured solvers and task routing; use dense linear algebra only where it is the correct local kernel.
- **Guard:** Choose the smallest valid solver/kernel whose support and precision satisfy the query.
- **Auditable absence:** A solver result is unavailable when support or conditioning is insufficient.
- **Metrics:** FLOPs avoided; data movement; J/query; accuracy; fallback rate.
- **Pilot:** Benchmark a fixed set of structured queries against dense tensor baselines.
- **Risks:** Planner overhead; hidden dense transforms; small-batch inefficiency.
- **References:** C0; R32

### DIG-04 - Event-driven analog-to-digital conversion layer

- **Maturity:** Near-term hardware research
- **Boundary:** Addition/partial replacement in sparse sensing.
- **Proposed role:** Use level-crossing, change-triggered or feature-triggered conversion for sparse signals, with conventional sampling as fallback and calibration reference.
- **Guard:** Analog signal crosses a calibrated level or derivative guard.
- **Auditable absence:** No event means no threshold crossing only if sensor health, coverage and threshold configuration are known.
- **Metrics:** Samples/signal; energy; reconstruction error; latency; missed crossings.
- **Pilot:** ECG, vibration or environmental signal with simultaneous conventional ADC.
- **Risks:** Low-amplitude drift; noise chatter; reconstruction; calibration.
- **References:** C0; R31

### DIG-05 - Event-camera perception substrate

- **Maturity:** Implementable research pilot
- **Boundary:** Addition/partial replacement for motion-centric tasks.
- **Proposed role:** Use asynchronous change events as input support, then compatibility and lineage to form object/interaction events; images remain optional.
- **Guard:** Local contrast event joins a tracked entity/trajectory and crosses a task guard.
- **Auditable absence:** No events imply no local contrast changes only within sensor support; not object absence.
- **Metrics:** Latency; bandwidth; events/J; tracking accuracy; low-motion failure.
- **Pilot:** Robot or industrial inspection task with hybrid frame/event camera.
- **Risks:** Static scenes; noise events; calibration; algorithm maturity.
- **References:** C0; R30

### DIG-06 - Photonic/mixed-signal query accelerator

- **Maturity:** Frontier prototype
- **Boundary:** Addition.
- **Proposed role:** Route stable, high-reuse linear transforms to photonic or analog kernels and keep compatibility, uncertainty, nonlinear decisions and lineage digital.
- **Guard:** Hardware path admitted when precision, calibration, batch reuse and I/O energy satisfy a policy.
- **Auditable absence:** Missing calibration/reference event forces digital fallback.
- **Metrics:** End-to-end J/query; throughput; accuracy; I/O share; recalibration.
- **Pilot:** One fixed transform with full system energy accounting.
- **Risks:** ADC/DAC dominates; drift; limited precision; workload mismatch.
- **References:** C0; R32

### DIG-07 - Novelty-proportional state storage

- **Maturity:** Near-term software pilot
- **Boundary:** Partial replacement of snapshot-heavy history for closed dynamics.
- **Proposed role:** Store seed/grammar, exogenous events, lineage, branch policy and checkpoints; materialize views on demand.
- **Guard:** An exogenous intervention or irreversible observation is appended as novelty.
- **Auditable absence:** Expected events can expire into absence events; missing coverage remains unknown.
- **Metrics:** Storage growth; rebuild time; auditability; branch cost; view freshness.
- **Pilot:** One simulator, workflow or operational twin with deterministic replay.
- **Risks:** Nondeterminism; external entropy; schema evolution; replay latency.
- **References:** C0; R28

### DIG-08 - Auditable absence and negative-event ledger

- **Maturity:** Implementable design pattern
- **Boundary:** Addition to any event system.
- **Proposed role:** Add ExpectedEvent and AbsenceEvent objects requiring obligation, observation support, deadline, coverage and reason codes.
- **Guard:** At deadline, emit absence only if expectation exists, observation support was valid and no compatible event occurred.
- **Auditable absence:** The pattern itself formalizes auditable absence.
- **Metrics:** False absence; unknown-vs-absent classification; overdue time; coverage quality.
- **Pilot:** Hospital follow-up, shipment scan and municipal SLA examples.
- **Risks:** Over-surveillance; brittle obligations; clock errors; gaming.
- **References:** C0; R6; R7; R24; R26

### DIG-09 - Data-pipeline state and lineage engine

- **Maturity:** Implementable integration
- **Boundary:** Addition/partial replacement of dashboard-centric orchestration.
- **Proposed role:** Represent datasets, transformations, models, approvals and deployments as typed events with compatibility and provenance.
- **Guard:** Transformation or release admitted only when inputs, schema, tests, authority and policy are compatible.
- **Auditable absence:** Expected artifact, test or approval absent after a due interval.
- **Metrics:** Reproducibility; failure diagnosis; stale-data incidents; audit time.
- **Pilot:** One analytics pipeline with W3C PROV export.
- **Risks:** Metadata burden; cross-tool identifiers; access control.
- **References:** C0; R28; R29

### DIG-10 - Cybersecurity trust-zone and policy event system

- **Maturity:** Near-term architecture pilot
- **Boundary:** Addition.
- **Proposed role:** Use sheet/sector separation, versioned compatibility predicates, provenance and event guards; co-location never implies access.
- **Guard:** Access or data join admitted only under identity, device, context, policy version and time predicates.
- **Auditable absence:** Expected attestation or heartbeat absent triggers degraded trust, not automatic compromise.
- **Metrics:** Unauthorized joins; policy explainability; response time; false blocks.
- **Pilot:** One zero-trust data-sharing workflow.
- **Risks:** Policy complexity; identity compromise; centralization; denial of service.
- **References:** C0; R28; R35

### DIG-11 - Distributed-system reconstruction and branch debugging

- **Maturity:** Near-term software pilot
- **Boundary:** Addition.
- **Proposed role:** Use explicit event lineage, branch context, compatibility and invariant reports to reconstruct what happened and why.
- **Guard:** State transition creates before/after hashes, predicate version, branch and invariant report.
- **Auditable absence:** Expected acknowledgment absent can be distinguished from delayed, dropped or never-sent.
- **Metrics:** Mean time to resolution; replay fidelity; log volume; invariant violations.
- **Pilot:** One event-driven service or workflow engine.
- **Risks:** Clock ordering; partial observability; privacy; schema drift.
- **References:** C0; R28

### DIG-12 - AI memory and retrieval with provenance and support

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Use local semantic support, compatibility, provenance and event-based updates; render summaries only from admitted evidence.
- **Guard:** Evidence enters a response only when relevance, authority, time, permission and provenance predicates pass.
- **Auditable absence:** Expected evidence absent is reported as a gap, not fabricated.
- **Metrics:** Citation accuracy; retrieval precision; stale-source rate; permission violations.
- **Pilot:** Research-document assistant over a bounded corpus.
- **Risks:** Semantic underspecification; source conflicts; privacy.
- **References:** C0; R28; R29

### DIG-13 - Model monitoring and deployment event graph

- **Maturity:** Implementable integration
- **Boundary:** Addition.
- **Proposed role:** Track data, model, evaluation, approval, deployment and drift as a provenance graph with compatibility and rollback branches.
- **Guard:** Deployment admitted when dataset, model, evaluation, policy and environment are compatible.
- **Auditable absence:** Expected monitoring metric absent triggers a hold, not assumed normality.
- **Metrics:** Rollback time; drift detection; reproducibility; audit completeness.
- **Pilot:** One model lifecycle.
- **Risks:** Metric gaming; hidden data shifts; access control.
- **References:** C0; R28; R29

### DIG-14 - Network and telecom event-native monitoring

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Use local flow supports, compatibility and threshold events; retain raw data around exceptions and provenance.
- **Guard:** Latency, loss, congestion, security or service relation crosses a guard.
- **Auditable absence:** Expected heartbeat or route acknowledgment absent under verified coverage.
- **Metrics:** Data reduction; detection time; false alarms; root-cause time; energy.
- **Pilot:** One network segment with mirrored conventional telemetry.
- **Risks:** Encrypted traffic; baseline drift; adversarial evasion.
- **References:** C0

### DIG-15 - AR/VR and simulation foveated query substrate

- **Maturity:** Research prototype
- **Boundary:** Addition/partial state-pipeline replacement.
- **Proposed role:** Use gaze/agent-local spherical support for relevance and direct state/event queries; render only admitted views and preserve nonvisual state independently.
- **Guard:** View or interaction event within gaze, reach, causal or semantic support.
- **Auditable absence:** No rendered object is not evidence of world absence.
- **Metrics:** Frame cost; motion-to-photon latency; interaction correctness; energy.
- **Pilot:** Procedural scene with event-native physics and conventional display.
- **Risks:** Gaze error; view inconsistency; hidden-state bugs.
- **References:** C0

## Warehousing, logistics & supply chains

### LOG-01 - Warehouse event twin and inventory truth

- **Maturity:** Implementable pilot
- **Boundary:** Addition beneath WMS/WES.
- **Proposed role:** Use EPCIS-like visibility events, lineage and auditable absence to reconstruct item, tote, pallet, location and task state.
- **Guard:** Receive, move, pick, pack, load, count and exception events update lineage.
- **Auditable absence:** Expected scan or movement absent under verified reader/task coverage.
- **Metrics:** Inventory accuracy; search time; write-offs; reconciliation labor; event completeness.
- **Pilot:** One zone or SKU family.
- **Risks:** Reader gaps; human bypass; identity duplication; privacy.
- **References:** C0; R26; R27

### LOG-02 - AMR and forklift continuous routing

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Use continuous trajectories, local supports, compatibility and next-conflict events across vehicles, humans and temporary zones.
- **Guard:** Earliest predicted conflict, blockage or task-window crossing.
- **Auditable absence:** Tracking absence blocks high-speed motion; no return is not free space.
- **Metrics:** Throughput; near misses; stops; travel distance; energy/order.
- **Pilot:** Simulation and one controlled warehouse aisle.
- **Risks:** Occlusion; uncertain human motion; network latency.
- **References:** C0; R33; R34

### LOG-03 - Pick-path and wave planning as event scheduling

- **Maturity:** Near-term software pilot
- **Boundary:** Addition.
- **Proposed role:** Schedule next admissible pick/pack/ship events using local resource support, due-time guards and branch isolation.
- **Guard:** Task admitted when inventory, worker/robot, container, dock and promise constraints match.
- **Auditable absence:** Expected inventory or resource event absent.
- **Metrics:** Orders/hour; lateness; walking/drive distance; replans; fairness.
- **Pilot:** One shift using historical replay.
- **Risks:** Objective conflicts; branch explosion; worker impacts.
- **References:** C0

### LOG-04 - Cold-chain and condition lineage

- **Maturity:** Implementable pilot
- **Boundary:** Addition.
- **Proposed role:** Bind sensor observations, packaging, custody and product lineage; trigger excursion and missing-coverage events.
- **Guard:** Temperature/humidity/time relation exits product support during a custody interval.
- **Auditable absence:** Expected logger data absent under a known custody and power window.
- **Metrics:** Excursion detection; spoilage; false holds; audit time.
- **Pilot:** One lane or product class.
- **Risks:** Sensor placement; clock drift; liability; data-sharing.
- **References:** C0; R24; R26; R27

### LOG-05 - Last-mile delivery event and promise engine

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Use continuous vehicle/package state, local traffic support, compatibility and delivery-promise guards with explicit non-delivery reasons.
- **Guard:** Delivery becomes admissible when parcel, recipient/location, vehicle, access and time conditions match.
- **Auditable absence:** Expected arrival, handoff or proof event absent with verified route/coverage.
- **Metrics:** On-time rate; miles/order; failed deliveries; customer contacts; emissions.
- **Pilot:** One route cluster.
- **Risks:** Privacy; dynamic traffic; inaccessible premises; worker pressure.
- **References:** C0; R26; R27

### LOG-06 - Port, terminal and yard coordination

- **Maturity:** Research/operations pilot
- **Boundary:** Addition.
- **Proposed role:** Create compatibility-gated events and lineage across berth, yard, crane, customs and onward transport.
- **Guard:** Move admitted when asset, slot, clearance, equipment and safety states match.
- **Auditable absence:** Expected clearance, equipment or handoff event absent.
- **Metrics:** Dwell time; crane productivity; truck queues; misroutes; energy.
- **Pilot:** One terminal flow in simulation/shadow mode.
- **Risks:** Institutional boundaries; cyber; weather; labor impacts.
- **References:** C0; R26; R27

### LOG-07 - Food provenance and recall event graph

- **Maturity:** Implementable integration
- **Boundary:** Addition.
- **Proposed role:** Use critical tracking events, split/merge lineage, condition data and compatibility to localize affected product.
- **Guard:** Transformation, aggregation, shipment, receipt and recall events preserve parent/child lineage.
- **Auditable absence:** Expected custody or transformation record absent.
- **Metrics:** Recall scope; trace time; waste; coverage; false inclusion/exclusion.
- **Pilot:** One product chain.
- **Risks:** Supplier adoption; identifier granularity; data quality.
- **References:** C0; R26; R27

### LOG-08 - Medical-device and medicine supply chain

- **Maturity:** Implementable pilot
- **Boundary:** Addition.
- **Proposed role:** Combine GS1 traceability with hospital compatibility and patient/procedure context.
- **Guard:** Device/drug use admitted when product, lot, expiry, storage, order and patient/procedure predicates pass.
- **Auditable absence:** Expected receipt, scan, temperature or recall acknowledgment absent.
- **Metrics:** Expired/incorrect use; recall time; stockouts; auditability.
- **Pilot:** One implant or high-risk medicine.
- **Risks:** Workflow burden; identifier mismatch; privacy.
- **References:** C0; R6; R26; R27

### LOG-09 - Returns, repair and circular-economy lineage

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Preserve component lineage, condition events, repair branches and material provenance to route reuse, refurbishment or recycling.
- **Guard:** Disposition admitted when identity, condition, warranty, safety and material predicates pass.
- **Auditable absence:** Expected inspection or test result absent.
- **Metrics:** Recovered value; waste avoided; turnaround; traceability.
- **Pilot:** One electronics product family.
- **Risks:** Hidden damage; data ownership; reverse-logistics cost.
- **References:** C0; R26; R28

### LOG-10 - Supply-chain risk and counterfactual branch planner

- **Maturity:** Research pilot
- **Boundary:** Addition.
- **Proposed role:** Use isolated branches sharing a base lineage to ask next disruption, substitute compatibility and downstream impact.
- **Guard:** Supplier, lane, inventory or regulatory relation crosses a disruption guard.
- **Auditable absence:** Expected shipment or supplier confirmation absent under a known reporting contract.
- **Metrics:** Time to detect; recovery time; substitution success; scenario explainability.
- **Pilot:** One multi-tier component chain.
- **Risks:** Supplier opacity; false rumors; branch explosion; strategic misuse.
- **References:** C0; R26; R27

## Smart cities & municipal governance

### CIV-01 - Municipal service obligation and 311 event graph

- **Maturity:** Implementable pilot
- **Boundary:** Addition beneath CRM/asset systems.
- **Proposed role:** Link requests, assets, departments, contractors, SLAs, inspections and resident communications through events and auditable absences.
- **Guard:** Request, dispatch, work, inspection and closure are typed events with reason and evidence.
- **Auditable absence:** Expected response, visit or resolution absent after its service window.
- **Metrics:** Resolution time; reopen rate; equity; evidence completeness; resident trust.
- **Pilot:** Pothole or streetlight service.
- **Risks:** Gaming closure; surveillance; uneven digital access; contractor data.
- **References:** C0; R21; R23; R25

### CIV-02 - Transit arrival and missed-service ledger

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Represent scheduled/expected service, vehicle lineage, stop support and observed arrivals; emit absence only with coverage.
- **Guard:** Arrival/departure crosses stop/time support under a vehicle/run identity.
- **Auditable absence:** Scheduled trip absent when AVL and operational coverage are verified; otherwise unknown/data gap.
- **Metrics:** On-time performance; ghost-trip classification; passenger delay; data coverage.
- **Pilot:** One bus corridor.
- **Risks:** GPS outages; schedule changes; privacy; public misinterpretation.
- **References:** C0; R21; R22; R24

### CIV-03 - Traffic, curb and intersection event control

- **Maturity:** Research pilot
- **Boundary:** Addition.
- **Proposed role:** Use local spatial supports, vehicle/pedestrian compatibility and next-conflict events; preserve policy versions and human override.
- **Guard:** Conflict, queue, pedestrian call, emergency preemption or curb-occupancy guard crossing.
- **Auditable absence:** Expected detector or phase acknowledgment absent.
- **Metrics:** Delay; safety surrogate; emissions; false calls; accessibility.
- **Pilot:** One simulated or controlled intersection.
- **Risks:** Safety; sensor bias; priority fairness; cyber.
- **References:** C0; R21; R24; R33

### CIV-04 - Water, sewer, waste and street-asset lifecycle

- **Maturity:** Near-term integration
- **Boundary:** Addition.
- **Proposed role:** Give each asset lineage, condition events, local support and maintenance guards; connect physical and budget records.
- **Guard:** Inspection, fault, maintenance, replacement and service events update asset state.
- **Auditable absence:** Expected inspection, collection or repair absent under a service obligation.
- **Metrics:** Failure rate; backlog; lifecycle cost; service equity; auditability.
- **Pilot:** One asset class.
- **Risks:** Legacy IDs; contractor boundaries; data quality.
- **References:** C0; R21; R22; R24; R28

### CIV-05 - Emergency response common event substrate

- **Maturity:** Research/operations pilot
- **Boundary:** Addition.
- **Proposed role:** Use a common incident lineage, local support, compatibility and event guards while preserving agency-specific sectors and permissions.
- **Guard:** Incident, dispatch, arrival, hazard, capacity and handoff events are admitted under role and jurisdiction predicates.
- **Auditable absence:** Expected unit acknowledgment or arrival absent within an explicit response window.
- **Metrics:** Response time; duplicate dispatch; handoff quality; privacy incidents.
- **Pilot:** Tabletop exercise and one low-risk event type.
- **Risks:** Authority conflict; false data; surveillance; cyber.
- **References:** C0; R21; R24; R35

### CIV-06 - Permitting, licensing and inspection event pipeline

- **Maturity:** Implementable pilot
- **Boundary:** Addition/partial replacement of opaque workflow tracking.
- **Proposed role:** Model application, evidence, review, inspection, decision, appeal and policy version as events with explicit compatibility and reason codes.
- **Guard:** Decision transition admitted only when required evidence, authority, policy version and procedural rights are satisfied.
- **Auditable absence:** Expected review or applicant response absent after due interval, with waiver/extension states.
- **Metrics:** Cycle time; rework; appeals; missing documents; transparency.
- **Pilot:** One permit type.
- **Risks:** Automating discretion; unequal access; policy complexity.
- **References:** C0; R28

### CIV-07 - Budget, procurement and contract lineage

- **Maturity:** Implementable information-system pilot
- **Boundary:** Addition.
- **Proposed role:** Create lineage from policy goal to appropriation, tender, bid, award, change order, invoice, delivery and outcome.
- **Guard:** Financial or contractual transition carries authority, policy, evidence and before/after state.
- **Auditable absence:** Expected deliverable, report or payment evidence absent.
- **Metrics:** Audit time; change-order visibility; duplicate spend; outcome linkage.
- **Pilot:** One capital project.
- **Risks:** Commercial confidentiality; political misuse; data burden.
- **References:** C0; R28; R29

### CIV-08 - Policy simulation with isolated counterfactual branches

- **Maturity:** Near-term planning pilot
- **Boundary:** Addition.
- **Proposed role:** Use branch-isolated policy worlds sharing base data; compare next events, service KPIs and distributional impacts without overwriting live state.
- **Guard:** Policy-specific service, cost, risk or equity guard crossing.
- **Auditable absence:** Missing evidence is shown as uncertainty, not zero impact.
- **Metrics:** Scenario reproducibility; runtime; KPI coverage; distributional impact; explainability.
- **Pilot:** Transport, housing or energy policy case.
- **Risks:** False precision; biased models; branch explosion; political capture.
- **References:** C0; R22; R25

### CIV-09 - Rights-preserving municipal data spaces

- **Maturity:** Implementable architecture pilot
- **Boundary:** Addition and governance foundation.
- **Proposed role:** Use relational exclusion, purpose/time/role compatibility, provenance and public reason codes; co-location in a platform never implies join permission.
- **Guard:** Data join admitted only for declared purpose, authority, minimization, retention and consent/legal basis.
- **Auditable absence:** Expected deletion, review or access-log event absent triggers governance action.
- **Metrics:** Unauthorized joins; purpose violations; access audit; resident redress.
- **Pilot:** One cross-department data-sharing use case with privacy review.
- **Risks:** Function creep; power imbalance; re-identification; opaque predicates.
- **References:** C0; R21; R35

### CIV-10 - Community well-being and service-outcome atlas

- **Maturity:** Near-term analytics pilot
- **Boundary:** Addition.
- **Proposed role:** Map technology events through infrastructure services to community benefits, with lineage and neighborhood support rather than one global score.
- **Guard:** Service outcome or disparity crosses a declared community guard.
- **Auditable absence:** Expected service result absent, with data coverage and denominator explicit.
- **Metrics:** Service access; quality of life; equity; resilience; data completeness.
- **Pilot:** One service portfolio across neighborhoods.
- **Risks:** Metric gaming; ecological fallacy; missing populations; privacy.
- **References:** C0; R22; R25

## Research & documentation management

### RES-01 - Claim-evidence-provenance graph

- **Maturity:** Implementable pilot
- **Boundary:** Addition beneath document systems.
- **Proposed role:** Represent claims, evidence, analyses, authorship, review and revision as a provenance graph; documents become materialized views.
- **Guard:** Claim created, supported, challenged, revised or withdrawn with source and method lineage.
- **Auditable absence:** Expected evidence, review or replication absent is explicit.
- **Metrics:** Traceability; review time; unsupported claims; reproducibility.
- **Pilot:** One technical report or evidence review.
- **Risks:** Metadata burden; disagreement semantics; access rights.
- **References:** C0; R28; R29

### RES-02 - Negative-result and non-observation registry

- **Maturity:** Implementable design pattern
- **Boundary:** Addition.
- **Proposed role:** Use ExpectedEvent/AbsenceEvent with protocol, detection support, power, deadline and reason to record meaningful non-observation.
- **Guard:** A pre-registered expected observation expires under adequate detection support without a compatible event.
- **Auditable absence:** This is the core absence use case.
- **Metrics:** Publication bias; repeat failures; power/coverage quality; reuse.
- **Pilot:** One lab or benchmark suite.
- **Risks:** Misclassified nulls; poor power; reputational incentives.
- **References:** C0; R29

### RES-03 - Electronic lab notebook as event-sourced experiment

- **Maturity:** Implementable pilot
- **Boundary:** Addition/partial replacement of page-centric ELN history.
- **Proposed role:** Record protocol, material, instrument, operator, environment, observation and transformation events with lineage.
- **Guard:** Experiment transition emits before/after state, instrument calibration, sample lineage and confidence.
- **Auditable absence:** Expected run, calibration or sample event absent.
- **Metrics:** Reproducibility; audit time; missing metadata; onboarding.
- **Pilot:** One instrument workflow.
- **Risks:** Instrumentation integration; user burden; IP security.
- **References:** C0; R28; R29

### RES-04 - Living systematic review and evidence map

- **Maturity:** Near-term software pilot
- **Boundary:** Addition.
- **Proposed role:** Maintain study, population, intervention, outcome, bias and claim events; materialize current reviews by query.
- **Guard:** Study or result changes the support for a claim under a versioned inclusion predicate.
- **Auditable absence:** Expected registry result or follow-up publication absent is tracked as pending/unknown.
- **Metrics:** Update latency; citation coverage; reproducibility; conflict visibility.
- **Pilot:** One narrow research question.
- **Risks:** Automated screening errors; paywalls; publication bias.
- **References:** C0; R28; R29

### RES-05 - Regulatory and quality-management evidence bundle

- **Maturity:** Implementable integration
- **Boundary:** Addition.
- **Proposed role:** Use event lineage and compatibility to generate auditable, version-specific evidence bundles.
- **Guard:** Requirement, design, test, deviation, risk control and approval events link to a release.
- **Auditable absence:** Expected verification or approval absent blocks release.
- **Metrics:** Audit prep time; trace gaps; change impact; defect escape.
- **Pilot:** One product change or submission section.
- **Risks:** Tool qualification; legal interpretation; access control.
- **References:** C0; R28

### RES-06 - Software and computational-environment lineage

- **Maturity:** Implementable pilot
- **Boundary:** Addition.
- **Proposed role:** Treat environment and execution as lineage events; reconstruct exact branch and artifacts for each result.
- **Guard:** Run event links code commit, dependencies, data, hardware, parameters and outputs.
- **Auditable absence:** Expected artifact or checksum absent.
- **Metrics:** Reproduction success; build time; provenance completeness.
- **Pilot:** One analysis pipeline.
- **Risks:** External services; nondeterminism; storage.
- **References:** C0; R28; R29

### RES-07 - Research portfolio and funding lineage

- **Maturity:** Near-term information-system pilot
- **Boundary:** Addition.
- **Proposed role:** Build lineage from question and funding to experiments, assets, outputs, reuse and societal outcomes without collapsing evaluation into one score.
- **Guard:** Funding, milestone, dataset, publication, reuse and outcome events preserve attribution.
- **Auditable absence:** Expected deliverable or data release absent with documented reason.
- **Metrics:** Duplication; reuse; time to evidence; administrative burden.
- **Pilot:** One program portfolio.
- **Risks:** Metric gaming; attribution complexity; privacy.
- **References:** C0; R28; R29

### RES-08 - Knowledge transfer and institutional memory substrate

- **Maturity:** Near-term pilot
- **Boundary:** Addition.
- **Proposed role:** Store decisions, assumptions, predicates, evidence and outcomes as lineage-aware events; documents and dashboards are generated views.
- **Guard:** Decision or rule change records context, authority, evidence, alternatives and consequences.
- **Auditable absence:** Expected review or retirement event absent.
- **Metrics:** Onboarding time; repeated mistakes; decision traceability; stale rules.
- **Pilot:** One engineering program or municipal department.
- **Risks:** Over-documentation; sensitive reasoning; cultural adoption.
- **References:** C0; R28

## Pilot portfolio

- **P01 Equation World Zero** (Digital core, 3-6 months): Implement six queries on one relation family and benchmark against frame stepping. Gate: Go if event solving + lineage is cheaper at equal correctness.

- **P02 Auditable absence ledger** (Cross-domain data, 3 months): Deploy ExpectedEvent/AbsenceEvent in hospital follow-up, shipment scan or municipal SLA. Gate: Go if unknown vs absent classification improves without excessive false absence.

- **P03 MRI adaptive raw-data replay** (Biomedical imaging, 6-12 months): Replay archived k-space/physiology data to test support- and guard-driven acquisition decisions. Gate: Go only with preserved task performance and uncertainty.

- **P04 Quantitative MR direct query phantom** (Biomedical imaging, 9-18 months): Compare direct parameter estimation, MRF-style approach and image-first baseline. Gate: Go if task accuracy/scan time improve under safety constraints.

- **P05 Cradle-to-life care journey** (Health information, 6-12 months): FHIR/PROV event graph for maternal-neonatal or chronic-care pathway. Gate: Go if identity, consent and care-gap auditability improve.

- **P06 Mental-health patient-controlled registry** (Mental health, 12 months): Longitudinal goals, context, consent and research measures with no automated diagnosis. Gate: Go only with independent ethics, patient control and low harm.

- **P07 Lithography hotspot event solver** (Semiconductor, 6-12 months): Local support and guard queries on a synthetic/public mask benchmark. Gate: Go if hotspot recall and runtime beat baseline without missed long-range effects.

- **P08 Fab next-fault shadow twin** (Manufacturing, 6-12 months): One chamber subsystem with continuous relations and event predictions. Gate: Go if false alarms and lead time meet preset thresholds.

- **P09 Hollowlens metrology proxy** (Physical/photonic, 12-24 months): Optofluidic or fixed photonic prefilter plus digital sidecar and matched electronic baseline. Gate: Go only on end-to-end verified events/J and stability.

- **P10 PV array event twin** (Solar, 6-12 months): String-level faults, absence semantics and O&M workflow. Gate: Go if energy recovery exceeds sensor/control burden.

- **P11 Pipeline leak replay and test loop** (Infrastructure, 9-18 months): Historical transients plus controlled leak/negative-pressure-wave tests. Gate: Go only with regulatory-grade sensitivity and false-alarm bounds.

- **P12 Warehouse event truth zone** (Logistics, 6 months): EPCIS lineage, expected scans and AMR time-of-conflict in one zone. Gate: Go if inventory accuracy and throughput improve.

- **P13 Municipal service obligation graph** (Civic, 6 months): Pothole, streetlight or waste service with Open311 and explicit SLA absence. Gate: Go if closure evidence and equity improve.

- **P14 Research claim-evidence graph** (Documentation, 3-6 months): Convert one report or systematic review to PROV/FAIR event graph. Gate: Go if review/update and audit time fall.

- **P15 Event ADC sensing benchmark** (Mixed signal, 6-12 months): Level-crossing plus reference sampling on vibration, ECG or environmental signal. Gate: Go if end-to-end energy falls at equal reconstruction/event performance.

- **P16 Photonic query-kernel benchmark** (Compute hardware, 12-24 months): Stable transform with full source, detector, ADC/DAC and calibration accounting. Gate: Go only if end-to-end J/query beats electronic reference.

## Evidence registry

- **C0 Topological Cross-Domain Synthesis of the Spherical Substrate Corpus** - User-supplied corpus reconstruction (2026), source/Topological_Cross_Domain_Corpus_Report_source.pdf

- **R1 Magnetic Resonance Imaging (MRI)** - U.S. FDA (2018), https://www.fda.gov/radiation-emitting-products/medical-imaging/mri-magnetic-resonance-imaging

- **R2 Magnetic resonance imaging (MRI) scans** - NIBIB/NIH (current), https://www.nibib.nih.gov/science-education/science-topics/magnetic-resonance-imaging-mri

- **R3 Sparse MRI: The application of compressed sensing for rapid MR imaging** - Lustig, Donoho and Pauly (2007), https://doi.org/10.1002/mrm.21391

- **R4 Magnetic resonance fingerprinting** - Ma et al. (2013), https://doi.org/10.1038/nature11971

- **R5 Testing and Labeling Medical Devices for Safety in the Magnetic Resonance Environment** - U.S. FDA (2023), https://www.fda.gov/regulatory-information/search-fda-guidance-documents/testing-and-labeling-medical-devices-safety-magnetic-resonance-mr-environment

- **R6 FHIR R5 Specification** - HL7 (2023), https://hl7.org/fhir/

- **R7 FHIR Subscription** - HL7 (2023), https://fhir.hl7.org/fhir/subscription.html

- **R8 Ethics and governance of artificial intelligence for health** - World Health Organization (2021), https://www.who.int/publications/i/item/9789240029200

- **R9 Ethics and governance of artificial intelligence for health: guidance on large multi-modal models** - World Health Organization (2025), https://www.who.int/publications/i/item/9789240084759

- **R10 WHO guideline: recommendations on digital interventions for health system strengthening** - World Health Organization (2019), https://www.who.int/publications/i/item/9789241550505

- **R11 Research Domain Criteria (RDoC) Initiative** - NIMH (current), https://www.nimh.nih.gov/research/research-funded-by-nimh/rdoc

- **R12 Computational lithography** - ASML (current), https://www.asml.com/products/computational-lithography

- **R13 EUV lithography systems** - ASML (current), https://www.asml.com/products/euv-lithography-systems

- **R14 ASML and imec open joint High NA EUV Lithography Lab** - ASML and imec (2024), https://www.asml.com/news/press-releases/2024/asml-imec-opening-high-na-euv-lithography-lab

- **R15 NIST Framework and Roadmap for Smart Grid Interoperability Standards, Release 4.0** - NIST (2021), https://doi.org/10.6028/NIST.SP.1108r4

- **R16 Digital Twin + AI: Control Room of the Future** - NREL (2024), https://docs.nrel.gov/docs/fy24osti/87050.pdf

- **R17 IEEE 1547-2018 Based Interoperable PV Inverter with Advanced Grid-Support Functions** - NREL (2019), https://www.nrel.gov/docs/fy19osti/73131.pdf

- **R18 Best Practices in Photovoltaic System Operations and Maintenance** - NREL (2017), https://www.nrel.gov/docs/fy17osti/68281.pdf

- **R19 Leak Detection Systems Fact Sheet** - PHMSA (2011), https://primis.phmsa.dot.gov/stakeholder-comms/factsheets/fsleakdetectionsystems/

- **R20 Pipeline Safety: Requirement of Valve Installation and Minimum Rupture Detection Standards** - PHMSA (2022), https://www.phmsa.dot.gov/sites/phmsa.dot.gov/files/2022-03/PHMSA%202137-AF06%20Valve%20Final%20Rule%20-%20March%202022.pdf

- **R21 NIST Smart Cities and Communities Framework Series** - NIST (current), https://www.nist.gov/ctl/smart-connected-systems-division/iot-devices-and-infrastructures-group/smart-americaglobal/nist

- **R22 Smart Cities and Communities: A Key Performance Indicators Framework** - NIST (2022), https://doi.org/10.6028/NIST.SP.1900-206

- **R23 GeoReport v2** - Open311 (current), https://wiki.open311.org/GeoReport_v2/

- **R24 OGC SensorThings API Standard** - Open Geospatial Consortium (current), https://www.ogc.org/standards/sensorthings/

- **R25 ISO 37120: Sustainable cities and communities - Indicators for city services and quality of life** - ISO (2018), https://www.iso.org/standard/68498.html

- **R26 EPCIS and Core Business Vocabulary** - GS1 (current), https://www.gs1.org/standards/epcis

- **R27 GS1 Global Traceability Standard** - GS1 (current), https://www.gs1.org/standards/traceability

- **R28 PROV-O: The PROV Ontology** - W3C (2013), https://www.w3.org/TR/prov-o/

- **R29 The FAIR Guiding Principles for scientific data management and stewardship** - Wilkinson et al. (2016), https://doi.org/10.1038/sdata.2016.18

- **R30 A 128x128 120 dB 15 us latency asynchronous temporal contrast vision sensor** - Lichtsteiner, Posch and Delbruck (2008), https://doi.org/10.1109/JSSC.2007.914337

- **R31 A 10.4-ENOB 0.92-5.38 uW Event-Driven Level-Crossing ADC** - Van Assche et al. (2022), https://lirias.kuleuven.be/retrieve/16f6ab16-2034-48a3-aab2-386c85bbaf9d

- **R32 Deep learning with coherent nanophotonic circuits** - Shen et al. (2017), https://doi.org/10.1038/nphoton.2017.93

- **R33 Time of Impact Dataset for Continuous Collision Detection and a Scalable Conservative Algorithm** - Belgrod et al. (2023), https://arxiv.org/abs/2112.06300

- **R34 A Generalized Continuous Collision Detection Framework of Polynomial Trajectory for Mobile Robots** - Zhang et al. (2022), https://arxiv.org/abs/2206.13175

- **R35 A Risk Management Approach to Smart City Cybersecurity and Privacy** - NIST GCTC (2019), https://pages.nist.gov/GCTC/uploads/blueprints/2019_GCTC-SC3_Cybersecurity_and_Privacy_Advisory_Committee_Guidebook_July_2019.pdf
