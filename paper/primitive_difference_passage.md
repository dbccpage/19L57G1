# The passage through Primitive Difference

Run: PR #12.  Sources: `lean4/Derivation/PrimitivePassage.lean`,
`lean4/Derivation/Apartness.lean`, `lean4/Derivation/HigherStructure.lean`
(growth side), Python mirrors `primitive_passage.py`, `apartness.py`,
artifact `primitive_passage.json`, `apartness.json`.

Each of the THIRTEEN arrows of the passage chain (fourteen stations)
has exactly one status — THEOREM,
DECLARATION (a separately priced admission event, with a countermodel
showing the arrow is false without it), or FALSE without extra
hypotheses — and executable evidence.

## The chain, arrow by arrow

| # | Arrow | Status | Evidence |
|---|---|---|---|
| 1 | PrimitiveDifference → RetainedDifference | DECLARATION (`assertWit` supplies; `admitWit` retains) | `assertion_not_retained`: an asserted difference is not yet retained; `retention_requires_assertion`; candidate A transports into the pre-retention state as a theorem (`assert_transport`, `kernel_enters_preretained`); once admitted, retention persists (`retention_persists`) |
| 2 | RetainedDifference → FaithfulPresentation | DECLARATION (demand) | `PrimDiff.const_presentation_unfaithful`; faithfulness is never a fact |
| 3 | FaithfulPresentation → DeclaredObservation | DECLARATION (`declareObs`) | `obs : Option …` — `none` is pre-observational, not "a blind observer" |
| 4 | DeclaredObservation → ZeroRel | THEOREM | `zero_refl`, `zero_symm`, `zero_trans`: the zero relation of any declared observation is an equivalence, proved before any quotient (P4) |
| 5 | ZeroRel → ProtectedCollapse | THEOREM (conditional on protection) | zero on a protected retained pair is exactly the collapse in force |
| 6 | ProtectedCollapse → ActiveObstruction | DEFINITION + THEOREM | `obstP` has three written factors (`obstP_strict_factors`); there are four gates in the proved factorization, and every maximal proper gate subset fails (P5) |
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
- `obst_policies_agree_when_declared` / `obst_policies_differ`: the
  policies agree on every declared state and differ at one named
  undeclared state.  A complete divergence characterization remains
  OPEN; the older `obst_diverges_when_undeclared` is only a historical
  witness and does not compare both predicates on one state.

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
- **P5** — the four-gate factorization and independence.  `obstP`
  itself has the three written factors recorded by
  `obstP_strict_factors`; there are four gates in the proved
  factorization (`obstP_factors`).  No gate follows from the other
  three, and no maximal proper subset entails obstruction — each a
  pair of `¬ ∀` statements over all states and pairs
  (`gate_zero_independent`, `gate_declared_independent`,
  `gate_protection_independent`, `gate_retention_independent`), with
  the five concrete witnesses in `obst_conditions_independent`.
  Scope: independence is non-entailment; the gates are NOT jointly
  free, since gates 3 and 4 both read `obs`
  (`obs_gates_not_both_false`).  Cite the factorization and the
  independence theorems together — the factorization alone is
  near-definitional.
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
  requires license.  Exact preservation statement: it preserves
  admitted occurrences, asserted and retained witnesses, protected
  demands, and every already-satisfied protected separation; it
  consumes one budget unit and strictly refines the prior
  observational equivalence classes (that refinement is its point).
  The `setBudget 1` in emitted blocks is a declared self-funding
  policy, not derived resource availability.
- Refusal changes no object field.  The terminal ends everything —
  the one arrow that loses the future, priced as such.

## Scope note (2026-08-13): the executed contact collision

Everything above is the PR #12 record, written while the declared
contact input was absent.  That input now exists and the collision has
been executed (`paper/primitive_difference_contact.md`).  Nothing in
this paper is withdrawn or restated: no arrow changed status, no
P-theorem was reopened, and the coverage map of the arriving
development (103 declaration rows,
`contact/analysis/contact_countermodels.json`) contains no declaration
bearing on retention, protection, budget, license, response families
or growth.  What the collision ADDS, all of it new material citing
this chain rather than revising it:

- **Arrow 4, placed exactly.**  What the arriving structure ADMITS as
  three equivalence-law fields, arrow 4 PROVES — but the asymmetry is
  at the INSTANCE level, not between the two signatures: native
  `DiffInterface.DiffObs` carries the same three laws as fields, and
  the arriving structure is field-for-field the same record.  The
  asymmetry is that every concrete observer of the SEALED CORPUS AT
  `a5caee2` is a KERNEL OBSERVER (`kernelObs` at a view), where the
  three laws are proved rather than admitted; at the declared
  observation stage that is a theorem
  (`ContactBridge.declared_zero_as_view`,
  `observation_stage_realizes_observer`), so the arriving stratum
  sits at the zero-relation station, not before it
  (`ContactBridge.kernelStage`, `kernel_stage_no_obstruction`).
  **Scope, not a universal claim about native observers**: the
  collision modules add observers that are not kernel observers —
  `ObsDescent.intDiffObs` (laws by linear arithmetic),
  `ObsDescent.collapseAllObs` (laws by `trivial`), and
  `ContactBridge.apartObs`, whose three law fields are discharged by
  the three ADMITTED `Apartness.IsApart` fields, spent one-for-one,
  so at that observer the three laws are exactly as admitted as on
  the arriving side.  The two placement theorems named above are
  scoped to the declared observation stage and are unaffected.
- **Arrows 1-3, licensed not shortened.**  The common replacement
  kernel enters at the same pre-retention station, reusing
  `kernel_enters_preretained` rather than re-proving it
  (`ContactKernel.kernel_licenses_entry`), where protection is empty,
  no observation is declared, and `obstP` is false
  (`entry_pre_observation`).  Of the three conjuncts of
  `kernel_licenses_entry` only the first mentions the kernel
  (endpoint distinctness); the other two are sealed constants about
  `preRetained` that hold with or without a kernel, and no map from
  an arbitrary kernel into the passage state is claimed.  Retention,
  protection and observation remain separately priced admission
  events.
- **Arrow 6, kept strictly finer.**  The arriving descent obstruction
  is collapse-collision at the quotient projection, proved in both
  directions (`ContactBridge.pair_blocked_is_collapse_collision`,
  `collapse_collision_is_pair_blocked`,
  `pair_blocked_iff_collapse_collision`); the four-condition `obstP`
  with `obst_conditions_independent` is strictly finer, and the two
  are not identified.

Ledger: CL-PD2-CONTACT-ENTRY, CL-PD2-CONTACT-BRIDGE.
