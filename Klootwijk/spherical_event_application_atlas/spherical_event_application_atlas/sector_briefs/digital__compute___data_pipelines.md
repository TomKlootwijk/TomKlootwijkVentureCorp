# Digital, compute & data pipelines

15 application records.

| ID | Application | Boundary | Maturity |
|---|---|---|---|
| DIG-01 | Equation-world simulation kernel | Partial replacement of the authoritative simulation layer in bounded domains. | Research prototype |
| DIG-02 | Raymarching/rasterization bypass for state and collision | Partial replacement of state/collision pipeline; rendering remains optional. | Research prototype |
| DIG-03 | Dense linear-algebra avoidance planner | Addition/partial workload replacement, not elimination of linear algebra. | Research architecture |
| DIG-04 | Event-driven analog-to-digital conversion layer | Addition/partial replacement in sparse sensing. | Near-term hardware research |
| DIG-05 | Event-camera perception substrate | Addition/partial replacement for motion-centric tasks. | Implementable research pilot |
| DIG-06 | Photonic/mixed-signal query accelerator | Addition. | Frontier prototype |
| DIG-07 | Novelty-proportional state storage | Partial replacement of snapshot-heavy history for closed dynamics. | Near-term software pilot |
| DIG-08 | Auditable absence and negative-event ledger | Addition to any event system. | Implementable design pattern |
| DIG-09 | Data-pipeline state and lineage engine | Addition/partial replacement of dashboard-centric orchestration. | Implementable integration |
| DIG-10 | Cybersecurity trust-zone and policy event system | Addition. | Near-term architecture pilot |
| DIG-11 | Distributed-system reconstruction and branch debugging | Addition. | Near-term software pilot |
| DIG-12 | AI memory and retrieval with provenance and support | Addition. | Near-term pilot |
| DIG-13 | Model monitoring and deployment event graph | Addition. | Implementable integration |
| DIG-14 | Network and telecom event-native monitoring | Addition. | Near-term pilot |
| DIG-15 | AR/VR and simulation foveated query substrate | Addition/partial state-pipeline replacement. | Research prototype |

## Application notes

### DIG-01 - Equation-world simulation kernel

Implement direct state_at, next_event, support, coupling, routing and lineage queries for a bounded relation family; render only on demand.

**Current baseline:** Conventional engines advance frames and materialize scene state for broad classes of objects.

**Event guard:** Earliest admitted relation crossing with certified root/interval.

**Auditable absence:** Expected event absent only with complete relation/support coverage.

**Pilot:** Equation World Zero benchmark versus frame stepping and event queue.

**Metrics:** Query cost; event ordering; memory/novelty; correctness; expression growth.

**Risks:** Event/branch explosion; numerical conditioning; limited relation family.

**References:** C0

### DIG-02 - Raymarching/rasterization bypass for state and collision

Move authority to relations/events and use ray/raster methods only as materialized views; collision and causality use direct queries.

**Current baseline:** Graphics pipelines often become de facto world stores.

**Event guard:** Visibility, contact or transition query solved from relations rather than image sampling.

**Auditable absence:** No pixel or sample is never evidence that an entity is absent from state.

**Pilot:** Procedural 2D/3D scene with headless test suite and optional renderer.

**Metrics:** State query time; collision correctness; render independence; memory; view consistency.

**Risks:** Hard implicit geometry; projection mismatch; renderer feedback.

**References:** C0; R33

### DIG-03 - Dense linear-algebra avoidance planner

Use support pruning, typed relations, sparse/structured solvers and task routing; use dense linear algebra only where it is the correct local kernel.

**Current baseline:** Many systems turn all state into large dense matrices and repeat global tensor operations.

**Event guard:** Choose the smallest valid solver/kernel whose support and precision satisfy the query.

**Auditable absence:** A solver result is unavailable when support or conditioning is insufficient.

**Pilot:** Benchmark a fixed set of structured queries against dense tensor baselines.

**Metrics:** FLOPs avoided; data movement; J/query; accuracy; fallback rate.

**Risks:** Planner overhead; hidden dense transforms; small-batch inefficiency.

**References:** C0; R32

### DIG-04 - Event-driven analog-to-digital conversion layer

Use level-crossing, change-triggered or feature-triggered conversion for sparse signals, with conventional sampling as fallback and calibration reference.

**Current baseline:** Uniform ADC samples at a clock even when signals change little.

**Event guard:** Analog signal crosses a calibrated level or derivative guard.

**Auditable absence:** No event means no threshold crossing only if sensor health, coverage and threshold configuration are known.

**Pilot:** ECG, vibration or environmental signal with simultaneous conventional ADC.

**Metrics:** Samples/signal; energy; reconstruction error; latency; missed crossings.

**Risks:** Low-amplitude drift; noise chatter; reconstruction; calibration.

**References:** C0; R31

### DIG-05 - Event-camera perception substrate

Use asynchronous change events as input support, then compatibility and lineage to form object/interaction events; images remain optional.

**Current baseline:** Frame cameras repeatedly read all pixels.

**Event guard:** Local contrast event joins a tracked entity/trajectory and crosses a task guard.

**Auditable absence:** No events imply no local contrast changes only within sensor support; not object absence.

**Pilot:** Robot or industrial inspection task with hybrid frame/event camera.

**Metrics:** Latency; bandwidth; events/J; tracking accuracy; low-motion failure.

**Risks:** Static scenes; noise events; calibration; algorithm maturity.

**References:** C0; R30

### DIG-06 - Photonic/mixed-signal query accelerator

Route stable, high-reuse linear transforms to photonic or analog kernels and keep compatibility, uncertainty, nonlinear decisions and lineage digital.

**Current baseline:** Electronic accelerators pay data-movement, conversion and memory costs.

**Event guard:** Hardware path admitted when precision, calibration, batch reuse and I/O energy satisfy a policy.

**Auditable absence:** Missing calibration/reference event forces digital fallback.

**Pilot:** One fixed transform with full system energy accounting.

**Metrics:** End-to-end J/query; throughput; accuracy; I/O share; recalibration.

**Risks:** ADC/DAC dominates; drift; limited precision; workload mismatch.

**References:** C0; R32

### DIG-07 - Novelty-proportional state storage

Store seed/grammar, exogenous events, lineage, branch policy and checkpoints; materialize views on demand.

**Current baseline:** Snapshot systems store repeated derived state and logs without a reconstruction contract.

**Event guard:** An exogenous intervention or irreversible observation is appended as novelty.

**Auditable absence:** Expected events can expire into absence events; missing coverage remains unknown.

**Pilot:** One simulator, workflow or operational twin with deterministic replay.

**Metrics:** Storage growth; rebuild time; auditability; branch cost; view freshness.

**Risks:** Nondeterminism; external entropy; schema evolution; replay latency.

**References:** C0; R28

### DIG-08 - Auditable absence and negative-event ledger

Add ExpectedEvent and AbsenceEvent objects requiring obligation, observation support, deadline, coverage and reason codes.

**Current baseline:** Most event logs record what happened but conflate no record, no observation and confirmed non-occurrence.

**Event guard:** At deadline, emit absence only if expectation exists, observation support was valid and no compatible event occurred.

**Auditable absence:** The pattern itself formalizes auditable absence.

**Pilot:** Hospital follow-up, shipment scan and municipal SLA examples.

**Metrics:** False absence; unknown-vs-absent classification; overdue time; coverage quality.

**Risks:** Over-surveillance; brittle obligations; clock errors; gaming.

**References:** C0; R6; R7; R24; R26

### DIG-09 - Data-pipeline state and lineage engine

Represent datasets, transformations, models, approvals and deployments as typed events with compatibility and provenance.

**Current baseline:** ETL/ML pipelines rely on job status, logs and snapshots across tools.

**Event guard:** Transformation or release admitted only when inputs, schema, tests, authority and policy are compatible.

**Auditable absence:** Expected artifact, test or approval absent after a due interval.

**Pilot:** One analytics pipeline with W3C PROV export.

**Metrics:** Reproducibility; failure diagnosis; stale-data incidents; audit time.

**Risks:** Metadata burden; cross-tool identifiers; access control.

**References:** C0; R28; R29

### DIG-10 - Cybersecurity trust-zone and policy event system

Use sheet/sector separation, versioned compatibility predicates, provenance and event guards; co-location never implies access.

**Current baseline:** Systems often equate network reachability with authorization and store security state in fragmented logs.

**Event guard:** Access or data join admitted only under identity, device, context, policy version and time predicates.

**Auditable absence:** Expected attestation or heartbeat absent triggers degraded trust, not automatic compromise.

**Pilot:** One zero-trust data-sharing workflow.

**Metrics:** Unauthorized joins; policy explainability; response time; false blocks.

**Risks:** Policy complexity; identity compromise; centralization; denial of service.

**References:** C0; R28; R35

### DIG-11 - Distributed-system reconstruction and branch debugging

Use explicit event lineage, branch context, compatibility and invariant reports to reconstruct what happened and why.

**Current baseline:** Distributed systems produce partial logs, retries, races and divergent replicas.

**Event guard:** State transition creates before/after hashes, predicate version, branch and invariant report.

**Auditable absence:** Expected acknowledgment absent can be distinguished from delayed, dropped or never-sent.

**Pilot:** One event-driven service or workflow engine.

**Metrics:** Mean time to resolution; replay fidelity; log volume; invariant violations.

**Risks:** Clock ordering; partial observability; privacy; schema drift.

**References:** C0; R28

### DIG-12 - AI memory and retrieval with provenance and support

Use local semantic support, compatibility, provenance and event-based updates; render summaries only from admitted evidence.

**Current baseline:** Retrieval systems return items based on embeddings but may lose source lineage, time and permission context.

**Event guard:** Evidence enters a response only when relevance, authority, time, permission and provenance predicates pass.

**Auditable absence:** Expected evidence absent is reported as a gap, not fabricated.

**Pilot:** Research-document assistant over a bounded corpus.

**Metrics:** Citation accuracy; retrieval precision; stale-source rate; permission violations.

**Risks:** Semantic underspecification; source conflicts; privacy.

**References:** C0; R28; R29

### DIG-13 - Model monitoring and deployment event graph

Track data, model, evaluation, approval, deployment and drift as a provenance graph with compatibility and rollback branches.

**Current baseline:** Models are deployed as versions with metrics, but lineage and context may be fragmented.

**Event guard:** Deployment admitted when dataset, model, evaluation, policy and environment are compatible.

**Auditable absence:** Expected monitoring metric absent triggers a hold, not assumed normality.

**Pilot:** One model lifecycle.

**Metrics:** Rollback time; drift detection; reproducibility; audit completeness.

**Risks:** Metric gaming; hidden data shifts; access control.

**References:** C0; R28; R29

### DIG-14 - Network and telecom event-native monitoring

Use local flow supports, compatibility and threshold events; retain raw data around exceptions and provenance.

**Current baseline:** Packet and telemetry systems generate high-rate data and periodic aggregates.

**Event guard:** Latency, loss, congestion, security or service relation crosses a guard.

**Auditable absence:** Expected heartbeat or route acknowledgment absent under verified coverage.

**Pilot:** One network segment with mirrored conventional telemetry.

**Metrics:** Data reduction; detection time; false alarms; root-cause time; energy.

**Risks:** Encrypted traffic; baseline drift; adversarial evasion.

**References:** C0

### DIG-15 - AR/VR and simulation foveated query substrate

Use gaze/agent-local spherical support for relevance and direct state/event queries; render only admitted views and preserve nonvisual state independently.

**Current baseline:** Immersive systems render broad scenes at high frame rates.

**Event guard:** View or interaction event within gaze, reach, causal or semantic support.

**Auditable absence:** No rendered object is not evidence of world absence.

**Pilot:** Procedural scene with event-native physics and conventional display.

**Metrics:** Frame cost; motion-to-photon latency; interaction correctness; energy.

**Risks:** Gaze error; view inconsistency; hidden-state bugs.

**References:** C0
