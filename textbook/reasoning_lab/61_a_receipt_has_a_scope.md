# 61. A receipt has a scope

The Python guard can return a receipt containing the formula, observer
names, before/after values and a refusal label. It also stores a
**checksum**: a string calculated from those recorded fields.

| Operation on a receipt | Does its checksum check pass? |
|---|---|
| Keep fields and their calculated checksum | Yes |
| Change a verdict field but retain the old checksum | No |
| Change that field and calculate a new checksum | Yes |

<details><summary>Predict: does the last “yes” establish that the changed verdict is true?</summary>

No. It establishes agreement between the supplied fields and their
calculated checksum. It does not compare those fields with the model or
with a physical observation.

</details>

## Attach the right claim to the check

Checksum verification can detect a field change relative to an unchanged
stored checksum. A separately trusted earlier checksum can support a
comparison with that earlier record. The receipt's own checksum alone
does not identify its author or prove its assertions.

Even a refusal label needs interpretation. In Lesson 60, a true starting
claim becomes false after removing a fact. The guard's receipt labels
the result with a negative verdict. Keep the before value, changed
input and guard policy visible; do not translate that label into “the
starting claim was disproved.”

The Lean refusal receipt has different fields and no checksum field.
Its state-retention theorem concerns its defined execution rule. It is
not a proof of the Python checksum procedure, callback purity, or an
empirical truth claim.

Try the [changed practice](SEMANTICS_PRACTICE.md) before the
[separate answers](SEMANTICS_ANSWERS.md). Optional
[source details](SEMANTICS_SOURCES.md) name the exact implementations
and checks. Return to the [Reasoning hub](README.md) when finished.

AuthorityEffect: None. Receipt integrity within its declared field comparison.
