# Claims

AuthorityEffect: None.

Statuses as the research-tree contract admits them: PROVED_THEOREM (a Lean
declaration named in `TREE_CONTRACT.json`, axioms within
`{propext, Quot.sound}`); VERIFIED_FINITE (checked by `model.py` on the
bounds pinned in `input.json`, nothing beyond them); CONDITIONAL (holds under
the stated assumption, which is not proved here); OPEN; REFUTED.  A withdrawn
statement keeps its row with a dated note.

Bridge-table status (the plan's vocabulary, not the contract's) is given in
the Statement column as RECOVERED, NECESSARY or OPTIONAL, always relative to
the admissions named in `README.md`.

| Claim | Status | Statement | Evidence |
| --- | --- | --- | --- |
| QB-1 | PROVED_THEOREM | B1(i), RECOVERED. An interference challenge over weight presentations `Q₀` holds exactly when `Q₀` does not know the readout. | `ResearchQmBridge.Residual.challenge_iff_not_knows` |
| QB-2 | PROVED_THEOREM | B1(i). The challenge holds exactly when adding the readout changes Genesis information, and then information strictly rises. | `ResearchQmBridge.Residual.challenge_iff_information_ne`, `ResearchQmBridge.Residual.challenge_information_lt` |
| QB-3 | PROVED_THEOREM | B1(i). On every represented carrier either the weights know the readout or the challenge holds. | `ResearchQmBridge.Residual.challenge_or_knows` |
| QB-4 | PROVED_THEOREM | Under A_amp over `ℤ[i]`: the mixing readout is the two weights plus twice the cross term. | `ResearchQmBridge.Gauss.GI.polarization` |
| QB-5 | PROVED_THEOREM | B1(ii), NECESSARY. With the weights fixed, the mixing context separates two preparations exactly when their cross terms differ; two preparations meeting the challenge are two amplitude pairs on one weight fiber. | `ResearchQmBridge.Gauss.separates_iff_cross`, `ResearchQmBridge.Gauss.fiber_necessary` |
| QB-6 | PROVED_THEOREM | The sign group suffices for one pair: `(1,1)` and `(1,-1)` share weights, readouts 4 and 0.  Three readouts on one fiber are realized by the four units of `ℤ[i]`: readouts 4, 2, 0. | `ResearchQmBridge.Gauss.sign_pair`, `ResearchQmBridge.Gauss.mu4_triple` |
| QB-7 | PROVED_THEOREM | The unit readout on `μ₄ ⊂ ℤ[i]` is invariant under conjugation and takes the three values 4, 2, 0 on the class representatives: `Re` realizes the class readout at order four. | `ResearchQmBridge.Gauss.mu4_readout_invariant`, `ResearchQmBridge.Gauss.mu4_readout_values` |
| QB-8 | PROVED_THEOREM | B1(ii), NECESSARY. A conjugation-invariant readout on the order-`N` cyclic phase group separates at most `N / 2 + 1` phases. | `ResearchQmBridge.Multiplicity.readout_factors`, `ResearchQmBridge.Multiplicity.multiplicity_bound`, `ResearchQmBridge.Multiplicity.nodup_le` |
| QB-9 | PROVED_THEOREM | B1(ii). For `k ≥ 1`, `N ≥ 1`: some invariant readout separates `k` phases of order `N` exactly when `2k - 2 ≤ N`.  The sign group carries exactly two; three need order four. | `ResearchQmBridge.Multiplicity.rep_separates`, `ResearchQmBridge.Multiplicity.realizable_iff`, `ResearchQmBridge.Multiplicity.signs_iff`, `ResearchQmBridge.Multiplicity.three_needs_four` |
| QB-10 | PROVED_THEOREM | B1(iii), OPTIONAL. Every finite multiplicity is realized in a finite cyclic phase group: the circle is not needed for any finite interference challenge of this form. | `ResearchQmBridge.Multiplicity.finite_order_suffices` |
| QB-11 | CONDITIONAL | The real part itself realizes the bound at every order: `Re ζ_N^j` takes `N / 2 + 1` distinct values on the class representatives.  Assumption: injectivity of the cosine on `[0, π]`, a classical fact imported at a price and not proved here.  Proved for `N = 4` in QB-7. | `README.md`, Admissions |
| QB-12 | PROVED_THEOREM | The amplitude model meets the Genesis challenge: on the carrier `[0, 1, 2]` with amplitudes `(1,1)`, `(1,i)`, `(1,-1)`, the weights carry information 1, with the readout 3, and do not know the readout. | `ResearchQmBridge.Instance.instance_information`, `ResearchQmBridge.Instance.instance_not_knows`, `ResearchQmBridge.Instance.instance_challenge` |
| QB-13 | VERIFIED_FINITE | Independent model: polarization on the box of real and imaginary parts between -3 and 3; readout-versus-cross-term agreement on a sample of weight-equal pairs; the instance numbers of QB-12; orbit count `N / 2 + 1` for `N ≤ 40`; least order `2k - 2` for `2 ≤ k ≤ 21`; the `μ₄` readouts. | `tests/test_model.py` |
| QB-14 | VERIFIED_FINITE | Encoding audit, mechanical part: the challenge reads only presentations on the carrier; it is decided without any amplitude. | `tests/test_model.py::test_challenge_mentions_no_amplitude`; `README.md`, Encoding audit |
| QB-15o | OPEN | B1(iv): the holonomy class of a phase cochain on a finite report graph is its gauge-invariant content (plan, QM-207 Theorem 4.3; Lean goal `FQM-QM207-LEAN`). Milestone M4. | — |
| QB-16o | OPEN | B1(iv′): reducing an integer excess modulo `N` gives a native source of `μ_N` cochains. Milestone M4. | — |

Lean reach: only the declarations named in `TREE_CONTRACT.json`.  This is not
a census of every compiled constant.
