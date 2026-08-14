# Topological Cross-Domain Corpus Package

## Purpose

This package supersedes the earlier chemistry-first decoding. It reads the seven supplied PDFs as a cross-domain design corpus centered on:

- a directly queryable state-and-event substrate;
- local spherical or radial-angular supports;
- relations, compatibility predicates, and explicit event surfaces;
- phase sheets, parity routing, gluing rules, and lineage identity;
- novelty-aware memory and an exogenous event log;
- computer-graphics, display, print, and photonic systems as downstream projections or optional embodiments.

The report preserves source terminology but distinguishes canonical architecture, normalized operators, decoder inference, bounded hypotheses, and rejected totalizing claims.

## Primary deliverables

- `Topological_Cross_Domain_Corpus_Report.pdf` - 63-page illustrated report.
- `Topological_Cross_Domain_Corpus_Report.html` - browser-readable report source.
- `Topological_Cross_Domain_Corpus_Report.md` - portable Markdown edition.
- `data/operator_lexicon.json` and `.csv` - 63 operator mappings.
- `data/claims_matrix.json` and `.csv` - 40 claims with evidence status and disposition.
- `data/corpus_ontology.jsonld` and `.graphml` - machine-readable corpus graph.
- `specs/` - state/event schemas, compatibility, projection, experiment plan, and query API.
- `prototype/` - restricted Equation World Zero reference implementation and tests.
- `source_maps/` - per-document technical maps and a key-page index.
- `source_extracts/` - page-separated parsed text from all seven documents.
- `source_documents/` - the original user-supplied PDFs.
- `diagrams/` - report diagrams in SVG and PNG.

## Correct reading rule

The authoritative object is not a framebuffer, a sequence of frames, a raymarch loop, or a global voxel inventory. The mature corpus treats those as optional projection mechanisms. Its core is a finite grammar and directly queryable state manifold in which:

```text
Q = P^n x R_time x S^1_phase x Z2_sheet x A_address x B_branch

Event = relation crossing
        AND local support admission
        AND compatibility

Transition = typed state update
             + invariant check
             + lineage update
```

The most important normalized operators are:

- `double vacuum` -> same coordinate, incompatible sector, no coupling;
- `SDF=0` or `B=0` -> event/transition guard;
- `one bit` -> narrow parity, route, validity, or admission flag;
- `quad hourglass` -> four-sector routing visualization around an event locus;
- `Klein bottle` -> explicit orientation/gluing abstraction, not automatic physical law;
- `sphere/cone/shell` -> local support and relevance operators, not a universal world remesh;
- `projection` -> materialized view derived from the authoritative state/query substrate.

## Source authority

- **S1** is the mature interpretive authority.
- **S2-S5** supply generative topology, optics, geometry, information, and hardware motifs, but include speculative and metaphorical passages.
- **S6** is the bounded engineering authority for the optional Hollowlens-0 physical bridge.
- **S7** is treated as a downstream graphics/display/print projection adapter.

Where early sources conflict with S1's later reading, S1 controls. Where physical metaphors need engineering discipline, S6 controls.

## Quick start

Read the report:

```text
Topological_Cross_Domain_Corpus_Report.pdf
```

Run the reference prototype:

```bash
cd prototype
python demo.py
python -m unittest -v test_equation_world_zero.py
```

Inspect machine-readable files:

```text
data/operator_lexicon.json
data/claims_matrix.json
data/query_matrix.json
data/corpus_ontology.jsonld
specs/query_api.yaml
specs/state_schema.json
specs/event_schema.json
```

## Prototype boundary

The Python prototype demonstrates:

- closed-form state-at-time evaluation for constant-velocity trajectories;
- analytic event roots for line and circle relations;
- local radial-angular support;
- sheet, phase, and invariant-tag compatibility;
- typed transitions, parity toggle, branch creation, lineage update, and event logging.

It is deliberately not:

- a renderer;
- a general physics or PDE engine;
- a topology proof;
- a universal constant-time solver;
- a medical or biological control mechanism;
- proof of optical or computational performance.

## Claims boundary

The package rejects or excludes universal O(1), zero memory, zero latency, zero heat, literal topological immunity, perfect determinism for arbitrary systems, direct medical control, and personal/political narratives as technical validation.

The package retains these as testable or bounded ideas only where explicitly stated:

- horizon-independent state evaluation for a fixed closed expression;
- next-event solving over a restricted relation family;
- memory proportional to seed, grammar, irreducible novelty, and necessary branch history;
- a bounded optofluidic demonstrator measured against a matched electronic baseline.

## Validation

See `validation/` for:

- PDF metadata and preflight output;
- text-overflow scan result;
- prototype unit-test output;
- package inventory summary.

The final PDF was rendered and visually inspected page by page. It contains no detected text blocks outside the A4 page bounds and no replacement-character or black-square glyph failures.

## Integrity

- `manifest.txt` lists every delivered file.
- `SHA256SUMS.txt` contains a SHA-256 hash for every file except itself.
- `data/source_manifest.json` records the original document hashes, sizes, and page counts.

## Evidence boundary

This is a source-grounded synthesis and implementation scaffold. It is not external scientific validation, patent analysis, safety certification, medical advice, or proof that the proposed architecture outperforms established systems.
