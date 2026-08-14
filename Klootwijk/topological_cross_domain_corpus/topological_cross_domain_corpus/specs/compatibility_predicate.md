# Compatibility Predicate Normal Form

The corpus's "double vacuum" becomes technically meaningful only through an explicit compatibility predicate. The normalized form is:

```text
chi(entity, relation, context) =
    sheet_ok
    AND phase_ok
    AND type_or_mode_ok
    AND time_ok
    AND provenance_ok
    AND policy_ok
```

## Required outputs

A compatibility evaluation returns:

```json
{
  "compatible": false,
  "reason_codes": ["SHEET_MISMATCH", "PHASE_OUTSIDE_TOLERANCE"],
  "predicate_version": "chi-v0.1",
  "evaluated_at": 12.5
}
```

## Semantics

- **Double vacuum**: same spatial coordinate, incompatible predicate, therefore no coupling.
- **Phase sheet**: a finite sector label or namespace, not a literal second physical vacuum.
- **One-bit parity**: a route or orientation bit interpreted under a declared schema.
- **Question gate**: the Boolean compatibility decision, not a replacement for uncertainty, amplitude, lineage, or state.

## Design constraints

1. The predicate must be deterministic for the same inputs and version.
2. Every rejection must have a machine-readable reason.
3. Predicate versions must be recorded in the event log.
4. Compatibility filtering must be measured; it cannot be assumed to remove all candidates cheaply.
5. Policy and permission checks must remain separate from geometry and physics types.

Source anchors: S1 p. 6; S5 pp. 32-33; S6 p. 7.
