# High-Impact Application Atlas package

This package translates the uploaded **Topological Cross-Domain Corpus Report** into a broad, source-grounded application program spanning physical instruments, biomedical systems, MRI, semiconductor manufacturing and ASML-adjacent workflows, energy grids, pipelines, solar, digital compute, analog-to-digital conversion, graphics, warehousing, delivery, smart cities, mental-health research, and documentation management.

## Start here

- `High_Impact_Application_Atlas.pdf` - 99-page illustrated report.
- `High_Impact_Application_Atlas.html` - searchable, link-rich report source.
- `High_Impact_Application_Atlas.md` - text-first companion.
- `data/application_atlas.csv` and `.json` - 95 structured application hypotheses.
- `data/pilot_portfolio.csv` - 16 bounded pilots with horizons and go/no-go gates.
- `data/replacement_addition_matrix.csv` - what to retain, add, partially replace, test, or reject.
- `data/metrics_dictionary.csv` - 38 benchmark measures, including verified events per joule.
- `schemas/` - state, event, expectation, absence, compatibility, lineage and application schemas.
- `prototype/` - tested reference code for direct state/event queries and auditable absence.
- `sector_briefs/` - one Markdown brief for each domain.
- `diagrams/` - 13 SVG/PNG architecture diagrams.
- `source/` - the uploaded report and selected evidence-page snapshots.

## Evidence discipline

The package uses six statuses:

1. corpus-canonical operator;
2. established external component or standard;
3. cross-domain inference;
4. bounded pilot;
5. frontier replacement hypothesis;
6. rejected totalizing claim.

The report does **not** claim clinical validation, MRI replacement, lithography replacement, zero power, zero latency, universal constant complexity, exact chaos, automatic medical control, or guaranteed fossil-fuel reduction. These applications are experiment definitions with matched baselines and kill criteria.

## Run the prototype

```bash
cd prototype
python -m unittest discover -s tests -v
python examples/hospital_journey.py
python examples/energy_pipeline.py
python examples/warehouse_delivery.py
python examples/solar_grid.py
python examples/mental_health_research.py
```

The examples are synthetic and are not medical, safety, regulatory, financial, or operational decision systems.

## Core rule

A verified event requires:

```text
relation/guard crossing AND support admission AND compatibility
```

An auditable absence requires:

```text
expectation AND complete declared coverage AND closed interval
AND no matching compatible event AND no valid exception
```

Missing telemetry remains `UNKNOWN` rather than becoming false negative evidence.
