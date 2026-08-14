# Data files

- `application_atlas.csv/json` - 95 application records. Each record contains baseline, proposed role, boundary, maturity, evidence status, operators, event guard, auditable absence, metrics, pilot, risks and references.
- `evidence_registry.csv/json` - source ID, organization, year, URL and role.
- `application_evidence_links.csv` - exploded many-to-many application/reference links.
- `replacement_addition_matrix.csv` - layer-by-layer retain/add/replace/frontier decisions.
- `pilot_portfolio.csv` - 16 pilots, horizons and go/no-go gates.
- `metrics_dictionary.csv` - benchmark definitions.
- `negative_event_examples.csv` - domain examples of ExpectedEvent/AbsenceEvent semantics.
- `domain_operator_matrix.csv` - counts of normalized operators by domain.
- `maturity_summary.csv` - application count by maturity label.
- `operator_application_ontology.jsonld` - JSON-LD graph of applications, operators and evidence.
- `application_graph.graphml` - GraphML version for network tools.
