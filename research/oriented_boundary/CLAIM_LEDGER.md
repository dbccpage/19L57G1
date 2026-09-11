# Claim ledger — oriented_boundary (discharge of SF-OPEN-A)

`AuthorityEffect: None.` Open, analytic result; amends nothing sealed. Name
resolution is weaker than semantic certification. See `CLOSURE.md` for the
argument and `MECHANIZATION.md` for what is mechanized versus analytic.

| ID | Grade | Statement | Evidence | Falsifier / boundary |
| --- | --- | --- | --- | --- |
| OB-B-EMPTY | Derivation | On a two-element carrier, σ (the swap) ∈ Aut iff no admitted judgment distinguishes the pair; equivalently σ ∉ Aut forces an admitted distinguishing (mechanism-A) witness. Route (B) — withdraw σ with no witness — is empty. | lean/OrientedBoundary/Basic.lean `b_is_empty`, `not_in_aut_needs_witness` (axioms ⊆ {propext, Quot.sound}) | A Lean model where σ ∉ Aut with no distinguishing admitted judgment. |
| OB-B-EMPTY-EXHAUSTIVE | Representation | The lemma holds over every one of the 16 admitted sets on the four distinct judgments; σ∈Aut iff no (A) witness; the witnessless σ∉Aut is unrepresentable. | oriented_boundary.py; test_oriented_boundary.py | Any admitted set with σ∉Aut and no asymmetric admitted judgment. |
| OB-ONE-CAPABILITY | Derivation | The unoriented reading (only a symmetric judgment) has σ ∈ Aut; the oriented reading breaks it at exactly one asymmetric witness. | `s2u_swap_is_automorphism`, `s2o_swap_is_not_automorphism`, `s2o_breaks_at_one_witness`; oriented_boundary.py S2_U/S2_O | Orientation breaks σ at zero witnesses, or requires more than one. |
| OB-KIND | Representation | An order is a paid symmetry-breaking admitted witness (mechanism A), not a container: a boundary exists before its contents; an order exists only with its contents — different existence-conditions, different kinds. | CLOSURE.md §§2–3 (analytic, on the seed's existence conditions) | A construction giving an order the boundary's exists-before-contents condition. |
| OB-NOT-TIME | Representation | Even orientation (σ ∉ Aut) is static two-sidedness, not succession; time-as-succession-as-internal-object never entered the language. | CLOSURE.md §4; AUTHOR_READING.md AP5 | An admitted internal object ordering events (a clock/succession) inside `<>`,`<|>`,`<a|b>`. |
| OB-SF-OPEN-A | Representation | SF-OPEN-A ("is the admission order a container?", research/side_free/CLAIM_LEDGER.md) is DISCHARGED: its open clause — "does not decide what kind of thing an order is" — is decided by OB-KIND, with OB-B-EMPTY the load-bearing lemma. Analytic (not blind) + one independent clean-model confirmation (VERDICT T7). | CLOSURE.md; AUTHOR_READING.md (frozen predictions HIT) | The kind question re-opens: a route to σ∉Aut that is neither (A) nor from-nowhere. |
| OB-DEFERRED | Representation | The space/time reading of boundary/orientation is a deferred functor, refused here. This is an object-language result, not a physics claim. | AUTHOR_READING.md; CLOSURE.md provenance | Prose here asserting a claim about nature rather than the object language. |
