# Validation record

## Report

- `High_Impact_Application_Atlas.pdf`: 99 A4 pages.
- Rendered successfully to 99 PNG pages with the PDF skill renderer.
- All pages were reviewed through five contact sheets; selected full-size pages were checked for table and bibliography legibility.
- Text extraction produced 99 form-feed page boundaries and no Unicode replacement characters or broken-square glyphs.

## Structured data

- 95 application records validate against `schemas/application_record.schema.json`.
- Evidence registry contains 36 source records: one corpus source and 35 external anchors.
- The atlas contains 16 pilot charters, 38 metrics and 10 auditable-absence examples.

## Prototype

Five unit tests pass:

1. closed-form `state_at` and `next_event`;
2. compatibility rejection;
3. incomplete coverage produces `UNKNOWN`;
4. complete coverage can produce `AbsenceEvent`;
5. an exception blocks absence emission.

The generated event examples validate against `event.schema.json`, and the hospital, warehouse and pipeline absence examples validate against `absence_event.schema.json`.

## Scope

Validation confirms package integrity, rendering, schema consistency and prototype behavior. It does not establish clinical, manufacturing, energy, safety, regulatory or societal performance.
