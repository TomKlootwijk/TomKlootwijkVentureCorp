# Smart cities & municipal governance

10 application records.

| ID | Application | Boundary | Maturity |
|---|---|---|---|
| CIV-01 | Municipal service obligation and 311 event graph | Addition beneath CRM/asset systems. | Implementable pilot |
| CIV-02 | Transit arrival and missed-service ledger | Addition. | Near-term pilot |
| CIV-03 | Traffic, curb and intersection event control | Addition. | Research pilot |
| CIV-04 | Water, sewer, waste and street-asset lifecycle | Addition. | Near-term integration |
| CIV-05 | Emergency response common event substrate | Addition. | Research/operations pilot |
| CIV-06 | Permitting, licensing and inspection event pipeline | Addition/partial replacement of opaque workflow tracking. | Implementable pilot |
| CIV-07 | Budget, procurement and contract lineage | Addition. | Implementable information-system pilot |
| CIV-08 | Policy simulation with isolated counterfactual branches | Addition. | Near-term planning pilot |
| CIV-09 | Rights-preserving municipal data spaces | Addition and governance foundation. | Implementable architecture pilot |
| CIV-10 | Community well-being and service-outcome atlas | Addition. | Near-term analytics pilot |

## Application notes

### CIV-01 - Municipal service obligation and 311 event graph

Link requests, assets, departments, contractors, SLAs, inspections and resident communications through events and auditable absences.

**Current baseline:** 311 systems record requests but often separate promises, work orders, assets and outcomes.

**Event guard:** Request, dispatch, work, inspection and closure are typed events with reason and evidence.

**Auditable absence:** Expected response, visit or resolution absent after its service window.

**Pilot:** Pothole or streetlight service.

**Metrics:** Resolution time; reopen rate; equity; evidence completeness; resident trust.

**Risks:** Gaming closure; surveillance; uneven digital access; contractor data.

**References:** C0; R21; R23; R25

### CIV-02 - Transit arrival and missed-service ledger

Represent scheduled/expected service, vehicle lineage, stop support and observed arrivals; emit absence only with coverage.

**Current baseline:** Passenger systems emphasize predictions and vehicle positions; missed trips may be poorly distinguished from missing telemetry.

**Event guard:** Arrival/departure crosses stop/time support under a vehicle/run identity.

**Auditable absence:** Scheduled trip absent when AVL and operational coverage are verified; otherwise unknown/data gap.

**Pilot:** One bus corridor.

**Metrics:** On-time performance; ghost-trip classification; passenger delay; data coverage.

**Risks:** GPS outages; schedule changes; privacy; public misinterpretation.

**References:** C0; R21; R22; R24

### CIV-03 - Traffic, curb and intersection event control

Use local spatial supports, vehicle/pedestrian compatibility and next-conflict events; preserve policy versions and human override.

**Current baseline:** Controllers operate with loops, phases and local sensors; planning and enforcement data are separate.

**Event guard:** Conflict, queue, pedestrian call, emergency preemption or curb-occupancy guard crossing.

**Auditable absence:** Expected detector or phase acknowledgment absent.

**Pilot:** One simulated or controlled intersection.

**Metrics:** Delay; safety surrogate; emissions; false calls; accessibility.

**Risks:** Safety; sensor bias; priority fairness; cyber.

**References:** C0; R21; R24; R33

### CIV-04 - Water, sewer, waste and street-asset lifecycle

Give each asset lineage, condition events, local support and maintenance guards; connect physical and budget records.

**Current baseline:** Asset management is split across GIS, work orders, inspections and finance.

**Event guard:** Inspection, fault, maintenance, replacement and service events update asset state.

**Auditable absence:** Expected inspection, collection or repair absent under a service obligation.

**Pilot:** One asset class.

**Metrics:** Failure rate; backlog; lifecycle cost; service equity; auditability.

**Risks:** Legacy IDs; contractor boundaries; data quality.

**References:** C0; R21; R22; R24; R28

### CIV-05 - Emergency response common event substrate

Use a common incident lineage, local support, compatibility and event guards while preserving agency-specific sectors and permissions.

**Current baseline:** Calls, sensors, dispatch, hospitals and utilities exchange partial information.

**Event guard:** Incident, dispatch, arrival, hazard, capacity and handoff events are admitted under role and jurisdiction predicates.

**Auditable absence:** Expected unit acknowledgment or arrival absent within an explicit response window.

**Pilot:** Tabletop exercise and one low-risk event type.

**Metrics:** Response time; duplicate dispatch; handoff quality; privacy incidents.

**Risks:** Authority conflict; false data; surveillance; cyber.

**References:** C0; R21; R24; R35

### CIV-06 - Permitting, licensing and inspection event pipeline

Model application, evidence, review, inspection, decision, appeal and policy version as events with explicit compatibility and reason codes.

**Current baseline:** Applicants face document-centric workflows with opaque state and missing-action delays.

**Event guard:** Decision transition admitted only when required evidence, authority, policy version and procedural rights are satisfied.

**Auditable absence:** Expected review or applicant response absent after due interval, with waiver/extension states.

**Pilot:** One permit type.

**Metrics:** Cycle time; rework; appeals; missing documents; transparency.

**Risks:** Automating discretion; unequal access; policy complexity.

**References:** C0; R28

### CIV-07 - Budget, procurement and contract lineage

Create lineage from policy goal to appropriation, tender, bid, award, change order, invoice, delivery and outcome.

**Current baseline:** Budgets and contracts are document-heavy and decisions are hard to reconstruct.

**Event guard:** Financial or contractual transition carries authority, policy, evidence and before/after state.

**Auditable absence:** Expected deliverable, report or payment evidence absent.

**Pilot:** One capital project.

**Metrics:** Audit time; change-order visibility; duplicate spend; outcome linkage.

**Risks:** Commercial confidentiality; political misuse; data burden.

**References:** C0; R28; R29

### CIV-08 - Policy simulation with isolated counterfactual branches

Use branch-isolated policy worlds sharing base data; compare next events, service KPIs and distributional impacts without overwriting live state.

**Current baseline:** Municipal scenarios often live in separate spreadsheets/models and can contaminate operational assumptions.

**Event guard:** Policy-specific service, cost, risk or equity guard crossing.

**Auditable absence:** Missing evidence is shown as uncertainty, not zero impact.

**Pilot:** Transport, housing or energy policy case.

**Metrics:** Scenario reproducibility; runtime; KPI coverage; distributional impact; explainability.

**Risks:** False precision; biased models; branch explosion; political capture.

**References:** C0; R22; R25

### CIV-09 - Rights-preserving municipal data spaces

Use relational exclusion, purpose/time/role compatibility, provenance and public reason codes; co-location in a platform never implies join permission.

**Current baseline:** Smart-city systems can centralize surveillance and blur purposes.

**Event guard:** Data join admitted only for declared purpose, authority, minimization, retention and consent/legal basis.

**Auditable absence:** Expected deletion, review or access-log event absent triggers governance action.

**Pilot:** One cross-department data-sharing use case with privacy review.

**Metrics:** Unauthorized joins; purpose violations; access audit; resident redress.

**Risks:** Function creep; power imbalance; re-identification; opaque predicates.

**References:** C0; R21; R35

### CIV-10 - Community well-being and service-outcome atlas

Map technology events through infrastructure services to community benefits, with lineage and neighborhood support rather than one global score.

**Current baseline:** City dashboards emphasize technology and operational metrics.

**Event guard:** Service outcome or disparity crosses a declared community guard.

**Auditable absence:** Expected service result absent, with data coverage and denominator explicit.

**Pilot:** One service portfolio across neighborhoods.

**Metrics:** Service access; quality of life; equity; resilience; data completeness.

**Risks:** Metric gaming; ecological fallacy; missing populations; privacy.

**References:** C0; R22; R25
