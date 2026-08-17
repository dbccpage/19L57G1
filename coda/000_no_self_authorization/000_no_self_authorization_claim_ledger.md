# NSA-000 — Claim ledger

**Paper:** `000_no_self_authorization.md` (v0.1 draft)
**AuthorityEffect:** None.

The residual monoid and `coda/figures.md` are authoritative for
counts. This ledger is a human-readable projection. Python
evidence is illustration / replay, not a universal proof.

| ID | Claim | Type | Support | Mechanization | Open |
| --- | --- | --- | --- | --- | --- |
| A1 | A comparison is four independent declarations: carrier, measure, evaluation, authorization. | DEFINITION | §1 | None | None |
| A2 | Collapsing the four into one reported verdict is the failure under study. | DEFINITION | §1 | None | None |
| A3 | AuthorityEffect of this paper is None. | POLICY | front matter | None | None |
| B1 | Under the item-count measure, min cost is exactly 2 items, both readings. | IMPORTED BOUNDED THEOREM | `FIG-MIN-COST` | sealed derivation | None |
| B2 | 3 tied non-isomorphic minima under reading L, declared bounds. | IMPORTED BOUNDED THEOREM | `FIG-TIED-L` | sealed derivation | None |
| B3 | 5 tied non-isomorphic minima under reading F, declared bounds. | IMPORTED BOUNDED THEOREM | `FIG-TIED-F` | sealed derivation | None |
| B4 | Countably infinite tie family indexed by arity. | IMPORTED THEOREM | `FIG-TIED-ARITY` | sealed Lean | None |
| B5 | Refined measure: 1 isomorphism class. | IMPORTED BOUNDED THEOREM | `FIG-MU2-CLASSES` | sealed derivation | None |
| B6 | That class still contains 2 concrete responses (stated identification of the two retained orientations). | IMPORTED / IDENTIFICATION | `FIG-MU2-CONCRETE` | sealed Lean + stated reading | None |
| C1 | Two positive measures can assign opposite orderings. | IMPORTED EXTERNAL | `FIG-GAUGE-ORDER` | not machine-checked here | None |
| C2 | Zero verdict is invariant under every positive measure. | IMPORTED EXTERNAL | `FIG-GAUGE-ORDER` scope | not machine-checked here | None |
| D1 | Reporting a singleton from a tie is an unauthorized selection unless declared. | DEFINITION / ILLUSTRATION | §4; `nsa000.selection` | Python finite | None |
| D2 | Capability does not close a gap that sits between stages. | ARGUMENT | §4 | None | lift to all systems OPEN |
| D3 | §4 transcript: five unauthorized selections, each caught externally; self-check twice not three. | COMPUTATION / RECORD | §4 | None | not a frequency |
| E1 | Legitimate closure is declaration, not detection. | CONSTRUCTION | §5 | None | None |
| E2 | Declaring a symmetry relocates freedom; it does not remove it. | ARGUMENT | §5 | None | None |
| F1 | Optional Hilbert lift reproduces Born-from-weights; uniqueness is imported. | IMPORTED / ILLUSTRATION | §6; `nsa000.born_lift` | Python finite | QM not derived |
| F2 | This paper stops at the Hilbert lift. | SCOPE FENCE | §6 | None | more is a later programme |
| G1 | Lift from counted ties to every meta-presentation still choosing is OPEN. | OPEN | Non-claims | None | G1 |
| G2 | No impossibility theorem about evaluation and authority is proved here. | REFUSED | Non-claims | None | None |
| G3 | `nsa000` does not replay FIG-TIED-L. | SCOPE FENCE | `src/nsa000/ties.py` | tests | None |
| G4 | The slogan is near-definitional; the contribution is `FIG-*`. | SCOPE FENCE | Non-claims; `attack_list.md` #2 | None | None |
| G5 | Source of handed authority, and whether FDA is more than a stop, is unanswered. | OPEN | `attack_list.md` #3 | None | G5 |
| G6 | Relation to known work is unanswered. Comparison belongs in `situating.md` and has not been written. | OPEN | `attack_list.md` #1; `situating.md` | None | G6 |
