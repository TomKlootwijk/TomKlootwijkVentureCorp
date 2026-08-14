# Warehousing, logistics & supply chains

10 application records.

| ID | Application | Boundary | Maturity |
|---|---|---|---|
| LOG-01 | Warehouse event twin and inventory truth | Addition beneath WMS/WES. | Implementable pilot |
| LOG-02 | AMR and forklift continuous routing | Addition. | Near-term pilot |
| LOG-03 | Pick-path and wave planning as event scheduling | Addition. | Near-term software pilot |
| LOG-04 | Cold-chain and condition lineage | Addition. | Implementable pilot |
| LOG-05 | Last-mile delivery event and promise engine | Addition. | Near-term pilot |
| LOG-06 | Port, terminal and yard coordination | Addition. | Research/operations pilot |
| LOG-07 | Food provenance and recall event graph | Addition. | Implementable integration |
| LOG-08 | Medical-device and medicine supply chain | Addition. | Implementable pilot |
| LOG-09 | Returns, repair and circular-economy lineage | Addition. | Near-term pilot |
| LOG-10 | Supply-chain risk and counterfactual branch planner | Addition. | Research pilot |

## Application notes

### LOG-01 - Warehouse event twin and inventory truth

Use EPCIS-like visibility events, lineage and auditable absence to reconstruct item, tote, pallet, location and task state.

**Current baseline:** WMS/WES systems maintain inventory snapshots and task queues; physical reality diverges through missed scans and exceptions.

**Event guard:** Receive, move, pick, pack, load, count and exception events update lineage.

**Auditable absence:** Expected scan or movement absent under verified reader/task coverage.

**Pilot:** One zone or SKU family.

**Metrics:** Inventory accuracy; search time; write-offs; reconciliation labor; event completeness.

**Risks:** Reader gaps; human bypass; identity duplication; privacy.

**References:** C0; R26; R27

### LOG-02 - AMR and forklift continuous routing

Use continuous trajectories, local supports, compatibility and next-conflict events across vehicles, humans and temporary zones.

**Current baseline:** Fleet systems replan using maps and fixed update cycles.

**Event guard:** Earliest predicted conflict, blockage or task-window crossing.

**Auditable absence:** Tracking absence blocks high-speed motion; no return is not free space.

**Pilot:** Simulation and one controlled warehouse aisle.

**Metrics:** Throughput; near misses; stops; travel distance; energy/order.

**Risks:** Occlusion; uncertain human motion; network latency.

**References:** C0; R33; R34

### LOG-03 - Pick-path and wave planning as event scheduling

Schedule next admissible pick/pack/ship events using local resource support, due-time guards and branch isolation.

**Current baseline:** Batch/wave planning uses forecasts and combinatorial optimization over snapshots.

**Event guard:** Task admitted when inventory, worker/robot, container, dock and promise constraints match.

**Auditable absence:** Expected inventory or resource event absent.

**Pilot:** One shift using historical replay.

**Metrics:** Orders/hour; lateness; walking/drive distance; replans; fairness.

**Risks:** Objective conflicts; branch explosion; worker impacts.

**References:** C0

### LOG-04 - Cold-chain and condition lineage

Bind sensor observations, packaging, custody and product lineage; trigger excursion and missing-coverage events.

**Current baseline:** Temperature records, custody and product identity are often separated.

**Event guard:** Temperature/humidity/time relation exits product support during a custody interval.

**Auditable absence:** Expected logger data absent under a known custody and power window.

**Pilot:** One lane or product class.

**Metrics:** Excursion detection; spoilage; false holds; audit time.

**Risks:** Sensor placement; clock drift; liability; data-sharing.

**References:** C0; R24; R26; R27

### LOG-05 - Last-mile delivery event and promise engine

Use continuous vehicle/package state, local traffic support, compatibility and delivery-promise guards with explicit non-delivery reasons.

**Current baseline:** Routing systems optimize estimated travel times and update customer status.

**Event guard:** Delivery becomes admissible when parcel, recipient/location, vehicle, access and time conditions match.

**Auditable absence:** Expected arrival, handoff or proof event absent with verified route/coverage.

**Pilot:** One route cluster.

**Metrics:** On-time rate; miles/order; failed deliveries; customer contacts; emissions.

**Risks:** Privacy; dynamic traffic; inaccessible premises; worker pressure.

**References:** C0; R26; R27

### LOG-06 - Port, terminal and yard coordination

Create compatibility-gated events and lineage across berth, yard, crane, customs and onward transport.

**Current baseline:** Ports coordinate vessels, cranes, vehicles, containers and customs through multiple systems.

**Event guard:** Move admitted when asset, slot, clearance, equipment and safety states match.

**Auditable absence:** Expected clearance, equipment or handoff event absent.

**Pilot:** One terminal flow in simulation/shadow mode.

**Metrics:** Dwell time; crane productivity; truck queues; misroutes; energy.

**Risks:** Institutional boundaries; cyber; weather; labor impacts.

**References:** C0; R26; R27

### LOG-07 - Food provenance and recall event graph

Use critical tracking events, split/merge lineage, condition data and compatibility to localize affected product.

**Current baseline:** Traceability is often batch-based and reconciliation-heavy.

**Event guard:** Transformation, aggregation, shipment, receipt and recall events preserve parent/child lineage.

**Auditable absence:** Expected custody or transformation record absent.

**Pilot:** One product chain.

**Metrics:** Recall scope; trace time; waste; coverage; false inclusion/exclusion.

**Risks:** Supplier adoption; identifier granularity; data quality.

**References:** C0; R26; R27

### LOG-08 - Medical-device and medicine supply chain

Combine GS1 traceability with hospital compatibility and patient/procedure context.

**Current baseline:** Healthcare supplies require identity, condition, custody and regulatory records.

**Event guard:** Device/drug use admitted when product, lot, expiry, storage, order and patient/procedure predicates pass.

**Auditable absence:** Expected receipt, scan, temperature or recall acknowledgment absent.

**Pilot:** One implant or high-risk medicine.

**Metrics:** Expired/incorrect use; recall time; stockouts; auditability.

**Risks:** Workflow burden; identifier mismatch; privacy.

**References:** C0; R6; R26; R27

### LOG-09 - Returns, repair and circular-economy lineage

Preserve component lineage, condition events, repair branches and material provenance to route reuse, refurbishment or recycling.

**Current baseline:** Returned products lose history and are triaged through coarse categories.

**Event guard:** Disposition admitted when identity, condition, warranty, safety and material predicates pass.

**Auditable absence:** Expected inspection or test result absent.

**Pilot:** One electronics product family.

**Metrics:** Recovered value; waste avoided; turnaround; traceability.

**Risks:** Hidden damage; data ownership; reverse-logistics cost.

**References:** C0; R26; R28

### LOG-10 - Supply-chain risk and counterfactual branch planner

Use isolated branches sharing a base lineage to ask next disruption, substitute compatibility and downstream impact.

**Current baseline:** Risk tools aggregate supplier and logistics data into dashboards and scenarios.

**Event guard:** Supplier, lane, inventory or regulatory relation crosses a disruption guard.

**Auditable absence:** Expected shipment or supplier confirmation absent under a known reporting contract.

**Pilot:** One multi-tier component chain.

**Metrics:** Time to detect; recovery time; substitution success; scenario explainability.

**Risks:** Supplier opacity; false rumors; branch explosion; strategic misuse.

**References:** C0; R26; R27
