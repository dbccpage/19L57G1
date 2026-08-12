# The passage through Primitive Difference

Run: PR #12.  Sources: `lean4/Derivation/PrimitivePassage.lean`,
`lean4/Derivation/Apartness.lean`, `lean4/Derivation/HigherStructure.lean`
(growth side), Python mirrors `primitive_passage.py`, `apartness.py`,
artifact `primitive_passage.json`, `apartness.json`.

Every arrow of the passage chain has exactly one status — THEOREM,
DECLARATION (a separately priced admission event, with a countermodel
showing the arrow is false without it), or FALSE without extra
hypotheses — and executable evidence.

## The chain, arrow by arrow

| # | Arrow | Status | Evidence |
|---|---|---|---|
| 1 | PrimitiveDifference → RetainedDifference | DECLARATION (`admitWit`) | `retention_not_free`: occurrences alone retain nothing; once admitted, retention persists (`retention_persists`) |
| 2 | RetainedDifference → FaithfulPresentation | DECLARATION (demand) | `PrimDiff.const_presentation_unfaithful`; faithfulness is never a fact |
| 3 | FaithfulPresentation → DeclaredObservation | DECLARATION (`declareObs`) | `obs : Option …` — `none` is pre-observational, not "a blind observer" |
| 4 | DeclaredObservation → ZeroRel | THEOREM | `zero_refl`, `zero_symm`, `zero_trans`: the zero relation of any declared observation is an equivalence, proved before any quotient (P4) |
| 5 | ZeroRel → ProtectedCollapse | THEOREM (conditional on protection) | zero on a protected retained pair is exactly the collapse in force |
| 6 | ProtectedCollapse → ActiveObstruction | DEFINITION + THEOREM | `obstP`: the FOUR-condition conjunction; every maximal proper subset fails (`obst_conditions_independent`, P5) |
| 7 | ActiveObstruction → ExhaustiveSameLevelFamily | THEOREM | `menu_complete`: the response menu contains every declared column × in-bounds point |
| 8 | → RepairFamily \| ExtensionProposalFamily | THEOREM (P7, the two-rule) | `two_rule`: repair nonempty, or certified exhaustion + provably nonempty extension family (`extension_always_available`) |
| 9 | → AuthorizationAndBudget | DECLARATION (gates) | `proposal_not_execution`, `budget_gates_execution`: proposing is free, executing is licensed and funded |
| 10 | → Replay | THEOREM | `replay_deterministic`, `replay_append`: state is a function of represented history |
| 11 | → Remeasurement | THEOREM | `extension_resolves`: the executed response kills the obstruction on re-evaluation |
| 12 | → RefusalRecord \| Terminal | DEFINITION, separately typed | `refusal_object_inert` + `refusal_not_terminal` (record, non-absorbing) vs `terminal_absorbing` (absorbing) — never one word |
| 13 | → RepresentedNextFamily | THEOREM | `nextFamilyP_stop` (silence is a verdict), `nextFamilyP_nonempty`, `nextFamilyP_complete_repair/_ext`; iteration of the family remains metatheoretic, stated |

## The four-condition refinement

The sealed `Completion.obstC` reads "no separating view" as observer
zero, which makes an observerless state vacuously zero.  The passage
separates *no observation declared* from *observation declared and
blind*:

- `obst_requires_observation`: pre-observational states obstruct
  nothing — whatever is retained and protected (P1, half 2);
- `wit_independent_of_obs`: the witness store never depends on the
  observation field (P1, half 1 — Primitive Difference precedes
  observation, as a theorem);
- `obst_agrees_when_declared` / `obst_diverges_when_undeclared`: the
  exact agreement and the exact divergence with the three-condition
  reading.

## P-theorems

- **P1** — proved both halves (above).
- **P2** — fidelity separate: `witness_no_protection` (admitting a
  witness never creates protection), `no_protection_no_obstruction`
  (collapse without protection obstructs nothing).
- **P3** — the barrier: `quotient_no_recovery` — once a presentation
  identifies the endpoints, no function of the quotient alone
  separates their images; recovery data must be retained outside the
  quotient.  That is what retention is *for*.
- **P4** — ZeroRel laws proved pre-quotient (`zero_refl/symm/trans`).
  With the Apartness module: the zero relation is the
  indistinguishability of the declared observation's separation
  apartness, and the equivalence laws are earned exactly as
  `Apartness.indist_equivalence` earns them — reflexivity from
  irreflexivity, symmetry from symmetry, transitivity from
  cotransitivity (automatic here because separation-by-columns is
  cotransitive: `sepCol_trans` is its finite avatar).
- **P5** — the four-condition independence, all maximal proper
  subsets refuted concretely.
- **P6** — same-level completeness certified by construction
  (`menu_complete`), repair family = the exhaustive filter; the
  extension side is a *separate* family with its own gates, refusal
  is a record, the terminal absorbs.
- **P7** — **the two-rule theorem** (`two_rule`): at an active
  obstruction with an in-bounds protected pair, the response universe
  never runs dry: **remove the obstruction at the same level, or
  create structure**.  The exact hypotheses are: active obstruction
  (four conditions), endpoint distinctness and in-bounds (from
  well-formed protection), the declared same-level and extension
  universes.  Nothing else.  The extension family is *always*
  nonempty at an obstruction (`extension_always_available`) — the
  singleton column on the first endpoint is fresh precisely because
  the observation is blind to the pair.  The first obstruction is
  forced to a response: self-resolution or structure creation.
- **P8** — operational no-outside: `no_outside_operational`,
  `replay_deterministic`; the absolute form quantifies over
  unrepresented differences, is not formulable here, and is not
  claimed (matches the sealed scope).

## The passage feeding the growth

`HigherStructure.graphAt_spec` iterates the passage: every round is
admission → retention → protection → obstruction
(`round_obstruction`) → nonempty response family (`round_two_rule`)
→ executed structure creation landing exactly on the next
characterized state (`round_resolution`), with the creation event
recorded as the round's last event (`round_creation_record`) and
quiescence restored (`graphAt_quiescent`).  The passage is not a
diagram: it runs, at every horizon.

## Losses and preservations, stated exactly

- Retention preserves the witness store under every event
  (append-only; `retention_persists`).
- Observation declaration preserves everything (a new empty store).
- Same-level repair preserves protected separations by its
  acceptance law (the monotone clause of `refineOk`).
- Extension execution costs budget (exactly one unit, saturating —
  `Horizon.interp_budget_bound` pins the shared semantics) and
  requires license; it adds one column and loses nothing.
- Refusal changes no object field.  The terminal ends everything —
  the one arrow that loses the future, priced as such.
