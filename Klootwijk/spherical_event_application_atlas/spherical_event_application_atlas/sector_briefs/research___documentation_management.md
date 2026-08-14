# Research & documentation management

8 application records.

| ID | Application | Boundary | Maturity |
|---|---|---|---|
| RES-01 | Claim-evidence-provenance graph | Addition beneath document systems. | Implementable pilot |
| RES-02 | Negative-result and non-observation registry | Addition. | Implementable design pattern |
| RES-03 | Electronic lab notebook as event-sourced experiment | Addition/partial replacement of page-centric ELN history. | Implementable pilot |
| RES-04 | Living systematic review and evidence map | Addition. | Near-term software pilot |
| RES-05 | Regulatory and quality-management evidence bundle | Addition. | Implementable integration |
| RES-06 | Software and computational-environment lineage | Addition. | Implementable pilot |
| RES-07 | Research portfolio and funding lineage | Addition. | Near-term information-system pilot |
| RES-08 | Knowledge transfer and institutional memory substrate | Addition. | Near-term pilot |

## Application notes

### RES-01 - Claim-evidence-provenance graph

Represent claims, evidence, analyses, authorship, review and revision as a provenance graph; documents become materialized views.

**Current baseline:** Reports and papers flatten claims, sources, methods and revisions into documents.

**Event guard:** Claim created, supported, challenged, revised or withdrawn with source and method lineage.

**Auditable absence:** Expected evidence, review or replication absent is explicit.

**Pilot:** One technical report or evidence review.

**Metrics:** Traceability; review time; unsupported claims; reproducibility.

**Risks:** Metadata burden; disagreement semantics; access rights.

**References:** C0; R28; R29

### RES-02 - Negative-result and non-observation registry

Use ExpectedEvent/AbsenceEvent with protocol, detection support, power, deadline and reason to record meaningful non-observation.

**Current baseline:** Research records positive observations more reliably than non-events or failed attempts.

**Event guard:** A pre-registered expected observation expires under adequate detection support without a compatible event.

**Auditable absence:** This is the core absence use case.

**Pilot:** One lab or benchmark suite.

**Metrics:** Publication bias; repeat failures; power/coverage quality; reuse.

**Risks:** Misclassified nulls; poor power; reputational incentives.

**References:** C0; R29

### RES-03 - Electronic lab notebook as event-sourced experiment

Record protocol, material, instrument, operator, environment, observation and transformation events with lineage.

**Current baseline:** ELNs store entries and attachments but may not reconstruct instrument, sample and analysis state.

**Event guard:** Experiment transition emits before/after state, instrument calibration, sample lineage and confidence.

**Auditable absence:** Expected run, calibration or sample event absent.

**Pilot:** One instrument workflow.

**Metrics:** Reproducibility; audit time; missing metadata; onboarding.

**Risks:** Instrumentation integration; user burden; IP security.

**References:** C0; R28; R29

### RES-04 - Living systematic review and evidence map

Maintain study, population, intervention, outcome, bias and claim events; materialize current reviews by query.

**Current baseline:** Reviews are periodic documents and rapidly become stale.

**Event guard:** Study or result changes the support for a claim under a versioned inclusion predicate.

**Auditable absence:** Expected registry result or follow-up publication absent is tracked as pending/unknown.

**Pilot:** One narrow research question.

**Metrics:** Update latency; citation coverage; reproducibility; conflict visibility.

**Risks:** Automated screening errors; paywalls; publication bias.

**References:** C0; R28; R29

### RES-05 - Regulatory and quality-management evidence bundle

Use event lineage and compatibility to generate auditable, version-specific evidence bundles.

**Current baseline:** Submissions assemble requirements, tests, risks, changes and approvals from many repositories.

**Event guard:** Requirement, design, test, deviation, risk control and approval events link to a release.

**Auditable absence:** Expected verification or approval absent blocks release.

**Pilot:** One product change or submission section.

**Metrics:** Audit prep time; trace gaps; change impact; defect escape.

**Risks:** Tool qualification; legal interpretation; access control.

**References:** C0; R28

### RES-06 - Software and computational-environment lineage

Treat environment and execution as lineage events; reconstruct exact branch and artifacts for each result.

**Current baseline:** Results depend on code, packages, containers, hardware and runtime parameters.

**Event guard:** Run event links code commit, dependencies, data, hardware, parameters and outputs.

**Auditable absence:** Expected artifact or checksum absent.

**Pilot:** One analysis pipeline.

**Metrics:** Reproduction success; build time; provenance completeness.

**Risks:** External services; nondeterminism; storage.

**References:** C0; R28; R29

### RES-07 - Research portfolio and funding lineage

Build lineage from question and funding to experiments, assets, outputs, reuse and societal outcomes without collapsing evaluation into one score.

**Current baseline:** Projects, grants, datasets, outputs and impacts are stored in separate systems.

**Event guard:** Funding, milestone, dataset, publication, reuse and outcome events preserve attribution.

**Auditable absence:** Expected deliverable or data release absent with documented reason.

**Pilot:** One program portfolio.

**Metrics:** Duplication; reuse; time to evidence; administrative burden.

**Risks:** Metric gaming; attribution complexity; privacy.

**References:** C0; R28; R29

### RES-08 - Knowledge transfer and institutional memory substrate

Store decisions, assumptions, predicates, evidence and outcomes as lineage-aware events; documents and dashboards are generated views.

**Current baseline:** Organizations lose rationale when staff, files and tools change.

**Event guard:** Decision or rule change records context, authority, evidence, alternatives and consequences.

**Auditable absence:** Expected review or retirement event absent.

**Pilot:** One engineering program or municipal department.

**Metrics:** Onboarding time; repeated mistakes; decision traceability; stale rules.

**Risks:** Over-documentation; sensitive reasoning; cultural adoption.

**References:** C0; R28
