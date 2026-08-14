# Energy, climate & infrastructure

18 application records.

| ID | Application | Boundary | Maturity |
|---|---|---|---|
| ENG-01 | Grid state and contingency query substrate | Addition beneath EMS/DERMS. | Research/utility pilot |
| ENG-02 | Distributed energy and microgrid compatibility router | Addition. | Near-term pilot |
| ENG-03 | Protection and disturbance event engine | Addition to analysis and coordination, not unvalidated relay replacement. | Near-term research pilot |
| ENG-04 | Solar PV string and module event twin | Addition. | Near-term pilot |
| ENG-05 | Solar inverter and MPPT event-native control | Addition; low-level control remains conventional unless certified. | Research pilot |
| ENG-06 | Battery state-of-health and thermal-runaway guard engine | Addition. | Near-term pilot |
| ENG-07 | EV charging and fleet energy routing | Addition. | Near-term pilot |
| ENG-08 | Gas, oil, hydrogen and CO2 pipeline leak/rupture event twin | Addition/upgrade to CPM and response coordination. | Near-term research pilot |
| ENG-09 | Water distribution leak and service-loss event system | Addition. | Near-term municipal pilot |
| ENG-10 | Industrial combustion, boilers and process heat next-event optimization | Addition. | Research pilot |
| ENG-11 | Fossil-fuel reduction through event-native operations | Cross-sector addition; not a substitute for clean-energy policy or physical transition. | Portfolio hypothesis |
| ENG-12 | Data-center and AI energy workload router | Addition. | Research prototype |
| ENG-13 | Building HVAC and indoor-environment event twin | Addition. | Near-term pilot |
| ENG-14 | Wind turbine and rotating-equipment next-fault engine | Addition. | Near-term pilot |
| ENG-15 | District heating, cooling and thermal-network routing | Addition. | Research pilot |
| ENG-16 | Carbon and energy provenance ledger | Addition. | Implementable information-system pilot |
| ENG-17 | Renewable curtailment and storage counterfactual planner | Addition. | Near-term planning pilot |
| ENG-18 | Environmental sensing with event/absence semantics | Addition. | Near-term pilot |

## Application notes

### ENG-01 - Grid state and contingency query substrate

Maintain a versioned grid state and solve local support, compatibility and next-limit events; use conventional power-flow solvers as typed physical services.

**Current baseline:** Grid operations combine estimators, SCADA/PMU streams, forecasts and periodic contingency studies.

**Event guard:** Earliest thermal, voltage, frequency, stability or protection guard crossing under a scenario branch.

**Auditable absence:** Expected telemetry or breaker state absent is classified separately from a normal zero.

**Pilot:** Offline replay and shadow control-room pilot for one region.

**Metrics:** Contingency solve time; missed events; false alarms; operator workload; events/J.

**Risks:** Model error; cyber risk; event explosion; operator trust.

**References:** C0; R15; R16

### ENG-02 - Distributed energy and microgrid compatibility router

Use compatibility predicates for device capability, grid state, market/policy and ownership; route only admitted events.

**Current baseline:** DERs, batteries, EVs and loads are coordinated through heterogeneous protocols and control layers.

**Event guard:** Dispatch or islanding transition admitted when electrical, contractual, cyber and timing predicates match.

**Auditable absence:** Expected device acknowledgment or telemetry absent after a verified communication window.

**Pilot:** Campus microgrid or simulated feeder.

**Metrics:** Dispatch success; interoperability failures; curtailment; resilience; cyber incidents.

**Risks:** Vendor heterogeneity; cyber attack; conflicting objectives.

**References:** C0; R15; R17

### ENG-03 - Protection and disturbance event engine

Represent disturbance supports, device compatibility, guard crossings and event lineage explicitly; keep certified relays authoritative.

**Current baseline:** Protection systems react to waveform thresholds with strict timing, while analytics may be separated.

**Event guard:** Fault or instability relation crosses a certified boundary in the protected zone.

**Auditable absence:** Expected breaker trip or relay acknowledgment absent within the mandated interval.

**Pilot:** Digital real-time simulator with relay-in-the-loop.

**Metrics:** Detection time; selectivity; false trips; coordination; event reconstruction.

**Risks:** Safety criticality; timing; model mismatch; cyber.

**References:** C0; R15

### ENG-04 - Solar PV string and module event twin

Use local array/string support, expected-yield relations, inverter compatibility and lineage to detect shading, soiling, mismatch, connector and degradation events.

**Current baseline:** PV monitoring aggregates power, irradiance and inverter data; faults may be discovered after energy loss.

**Event guard:** Measured/predicted energy balance exits a calibrated support or a component relation crosses a fault guard.

**Auditable absence:** Expected generation or telemetry absent only after irradiance, availability and sensor coverage are verified.

**Pilot:** One commercial array with parallel conventional monitoring.

**Metrics:** Energy recovered; detection delay; false alarms; O&M cost; events/J; curtailment avoided.

**Risks:** Weather-model error; sensor drift; maintenance burden.

**References:** C0; R17; R18

### ENG-05 - Solar inverter and MPPT event-native control

Add local event rules for mode changes, mismatch, voltage support and thermal limits; investigate level-crossing conversion for sparse supervisory signals.

**Current baseline:** Inverters continuously sample voltage/current and update control loops.

**Event guard:** Operating point, thermal, grid-support or protection relation crosses a guard.

**Auditable absence:** Expected inverter response absent under verified communications and power availability.

**Pilot:** Controller-in-the-loop PV emulator.

**Metrics:** Wh delivered per control joule; tracking efficiency; response time; thermal cycling.

**Risks:** Control stability; harmonics; standards compliance; converter noise.

**References:** C0; R17; R31

### ENG-06 - Battery state-of-health and thermal-runaway guard engine

Use continuous state relations, lineage of cells/modules and next-event guards for degradation, imbalance, venting and thermal risk.

**Current baseline:** BMSs estimate state using sampled electrical and thermal data and rule-based protections.

**Event guard:** Predicted temperature, voltage, pressure, impedance or imbalance crosses a certified threshold.

**Auditable absence:** Expected sensor/contactor response absent; never interpret missing telemetry as safe.

**Pilot:** Battery cycler and abuse-test dataset in shadow mode.

**Metrics:** Prediction horizon; false/late trips; cycle life; pack availability; compute energy.

**Risks:** Cell variability; rare-event data; safety certification.

**References:** C0

### ENG-07 - EV charging and fleet energy routing

Use vehicle/charger/grid compatibility, local feeder support and next-departure/constraint events with lineage-aware energy accounting.

**Current baseline:** Fleet charging is optimized using schedules, prices and charger availability.

**Event guard:** Charge/discharge transition admitted under connector, battery, departure, feeder and tariff constraints.

**Auditable absence:** Expected vehicle arrival, charger acknowledgment or departure readiness absent.

**Pilot:** Municipal or depot fleet.

**Metrics:** Peak demand; missed departures; energy cost; battery wear; charger utilization.

**Risks:** Data quality; user autonomy; tariff volatility; cyber.

**References:** C0; R15

### ENG-08 - Gas, oil, hydrogen and CO2 pipeline leak/rupture event twin

Express leak/rupture, negative-pressure-wave and valve-response events with support, compatibility, uncertainty and auditable negative events.

**Current baseline:** Computational pipeline monitoring compares pressure, flow, temperature and equipment states to models.

**Event guard:** Hydraulic/mass-balance or wave relation crosses a leak guard and is compatible with operating transients.

**Auditable absence:** Expected valve closure, pressure recovery or sensor report absent within a verified interval.

**Pilot:** Historical replay and controlled test loop.

**Metrics:** Leak size/time sensitivity; location error; false alarms; isolated volume; response time.

**Risks:** Small leaks; transient confusion; sensor failure; regulatory requirements.

**References:** C0; R19; R20

### ENG-09 - Water distribution leak and service-loss event system

Combine hydraulic relations, local geographic support, meter/sensor compatibility and 311 reports; explicitly model service absence.

**Current baseline:** Utilities use SCADA, district metering and customer reports.

**Event guard:** Pressure/flow imbalance or service complaint crosses a localized guard.

**Auditable absence:** Expected pressure, meter heartbeat or repair completion absent under coverage.

**Pilot:** One pressure district.

**Metrics:** Water loss; detection time; false alarms; repair time; equity by neighborhood.

**Risks:** Sparse sensors; demand uncertainty; privacy; false absence.

**References:** C0; R23; R24

### ENG-10 - Industrial combustion, boilers and process heat next-event optimization

Layer a query-first event twin over validated thermodynamic/control models to predict limit crossings, fouling and efficiency transitions.

**Current baseline:** Plants use control loops, historians and model predictive control.

**Event guard:** Efficiency, emissions, temperature or pressure relation crosses a guard under a candidate operating branch.

**Auditable absence:** Expected actuator or sensor response absent.

**Pilot:** One boiler or furnace subsystem in shadow mode.

**Metrics:** Fuel per output; emissions; downtime; false interventions; control energy.

**Risks:** Model mismatch; unsafe optimization; operator acceptance.

**References:** C0

### ENG-11 - Fossil-fuel reduction through event-native operations

Apply event-native sensing, direct queries, provenance and compatibility to reduce avoidable compute, leaks, curtailment, idling and overproduction.

**Current baseline:** Digital and physical systems waste energy on over-acquisition, unnecessary transport, leakage and poorly timed operation.

**Event guard:** Avoided-energy or avoided-emission action occurs only when a verified event justifies it.

**Auditable absence:** Missing data cannot be counted as avoided use or emissions.

**Pilot:** Bundle grid, PV, pipeline and logistics pilots with a common measurement protocol.

**Metrics:** Net J saved; kgCO2e avoided; rebound; capital cost; verification confidence.

**Risks:** Rebound; greenwashing; boundary manipulation; lifecycle omissions.

**References:** C0; R15; R18; R19

### ENG-12 - Data-center and AI energy workload router

Use local workload support, compatibility, event thresholds and hardware-specific energy models to choose electronic, analog or photonic paths.

**Current baseline:** Large workloads are scheduled by utilization and service objectives, often with dense telemetry and broad models.

**Event guard:** Route a task when accuracy, latency, energy, precision and hardware calibration predicates are satisfied.

**Auditable absence:** Expected accelerator result or calibration signal absent; fall back.

**Pilot:** One fixed inference or signal-processing workload across CPU/GPU/photonic emulator.

**Metrics:** J/query; throughput; accuracy; data movement; fallback rate.

**Risks:** I/O dominates; calibration; model portability; misleading component-only metrics.

**References:** C0; R32

### ENG-13 - Building HVAC and indoor-environment event twin

Use local zone supports, occupancy/privacy compatibility and next-comfort/air-quality/fault events; store exceptions and novelty rather than every derived view.

**Current baseline:** Building systems sample temperature, occupancy and equipment state at fixed intervals.

**Event guard:** Comfort, CO2, humidity, equipment or demand guard crossing.

**Auditable absence:** Expected occupancy or sensor signal absent only with coverage/consent known.

**Pilot:** One building zone with parallel BMS.

**Metrics:** kWh; comfort; indoor air quality; false occupancy; maintenance.

**Risks:** Privacy; occupancy inference; sensor drift; control oscillation.

**References:** C0; R21; R24

### ENG-14 - Wind turbine and rotating-equipment next-fault engine

Represent phase, rotational state, load and component lineage; solve bearing, imbalance and fatigue guard events.

**Current baseline:** Condition monitoring uses vibration, SCADA and periodic analysis.

**Event guard:** Vibration/temperature/load relation crosses a calibrated fault guard.

**Auditable absence:** Expected phase marker or sensor heartbeat absent.

**Pilot:** Historical replay and one instrumented turbine/test rig.

**Metrics:** Lead time; false alarms; downtime; maintenance cost; energy availability.

**Risks:** Nonstationary load; rare failures; sensor degradation.

**References:** C0

### ENG-15 - District heating, cooling and thermal-network routing

Use continuous transport relations, local branch support and compatibility to predict demand/temperature events and route heat.

**Current baseline:** Thermal networks have delays, storage and heterogeneous loads.

**Event guard:** Supply/return temperature, pressure or storage state crosses an operational guard.

**Auditable absence:** Expected demand or telemetry absent under verified coverage.

**Pilot:** Campus thermal network digital twin.

**Metrics:** Fuel/electricity; losses; comfort; peak reduction; event accuracy.

**Risks:** Long delays; uncertain demand; actuator limits.

**References:** C0

### ENG-16 - Carbon and energy provenance ledger

Use lineage, versioned factors, compatibility and explicit missingness to make every claim reconstructable and branch-aware.

**Current baseline:** Emissions and energy claims are assembled from heterogeneous activity data and factors.

**Event guard:** A carbon/energy claim is emitted only when source data, factor version, scope and ownership predicates are complete.

**Auditable absence:** Missing activity or factor data remains a declared gap, not a zero.

**Pilot:** One product or facility lifecycle.

**Metrics:** Coverage; audit time; recalculation reproducibility; uncertainty; double-count prevention.

**Risks:** Boundary gaming; factor uncertainty; supplier data gaps.

**References:** C0; R28; R29

### ENG-17 - Renewable curtailment and storage counterfactual planner

Use isolated branches over a shared state to ask which intervention prevents the next constraint while preserving provenance.

**Current baseline:** Planning tools compare scenarios using repeated simulations and spreadsheets.

**Event guard:** Branch-specific constraint or reliability event under a candidate storage, network or demand-response action.

**Auditable absence:** Expected asset availability absent in a branch is explicit.

**Pilot:** One feeder or region with locked baseline scenarios.

**Metrics:** Curtailment avoided; reliability; cost; model runtime; branch explainability.

**Risks:** Scenario explosion; uncertain futures; policy assumptions.

**References:** C0; R15; R16

### ENG-18 - Environmental sensing with event/absence semantics

Use local support, sensor provenance, coverage contracts and threshold events; distinguish non-detection from sensor silence.

**Current baseline:** Air, water and ecosystem monitoring often mixes missing data, normal values and true non-detection.

**Event guard:** Pollutant or ecological indicator crosses a calibrated guard under valid sensor support.

**Auditable absence:** Non-detection is emitted only when detection capability and sampling coverage are certified.

**Pilot:** One air-quality or water-quality network.

**Metrics:** Detection delay; false absence; sensor uptime; spatial coverage; energy.

**Risks:** Calibration; sparse coverage; community trust; interpretation.

**References:** C0; R24
