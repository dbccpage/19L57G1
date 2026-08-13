# The Primitive Difference map: derivation, obstruction, growth

Run: PR #12 (contact and passage).  This paper is the synthesis: how
the primitive difference is derived, why the first obstruction is
forced to self-resolve or create structure, how the first graph and
the first 0-, 1-, 2-, 3-simplices grow out of that forcing, which
process created each piece of structure, and which invariants the run
discovered and named.  Every claim cites a theorem or a
countermodel; the post-hoc realization table at the end is
comparison, not derivation, and nothing in the formal development
depends on it.

## 1. The derivation of Primitive Difference

The provenance chain (sealed in PR #5, sharpened here):

1. **Supply is not difference.**  A supplied inscription is an
   occurrence, not a distinction; repetition creates occurrences,
   never identities (`PrimDiff.repetition_new_occurrence`).
2. **Bare assertion is not difference.**  A positive difference
   assertion with no laws is consistent with a one-point carrier
   asserting difference from itself (`selfdiff_consistent`).  Bare
   witness does not separate (`nimp_w_d`), and its
   indistinguishability is not even reflexive
   (`Apartness.bare_breaks_refl`).
3. **The first law that earns anything is irreflexivity.**  With it,
   the witnessed pair forces endpoint distinctness (`imp_a_d`) and a
   two-element carrier (`no_witness_on_subsingleton`).  **PD-A — the
   pointed witnessed irreflexive relation — is the weakest candidate
   that genuinely differentiates.**  The full 72-cell matrix
   (`primitive_implication_matrix.json`) places every other reading:
   symmetry, cotransitivity, locatedness, protection, retention, and
   operation-irreducibility are each separately priced additions,
   none derivable from the others (51 compiled countermodels; 4
   located cells OPEN with exact metatheoretic scope).
4. **The universal status is genuine.**  The oriented two-element
   realization is initial among ALL pointed witnessed relations
   (`PrimitiveCats.d2_initial`) — a true universal property, not a
   probe battery; unique up to isomorphism only
   (`two_initials_not_identical`), distinct from minimum cardinality
   (`larger_not_initial`).  The orientation fork is retained whole:
   the symmetric object is initial exactly in the symmetric
   subcategory and not weakly initial outside it.
5. **Indistinguishability is earned, not assumed.**  Under the three
   positive apartness laws it is an equivalence
   (`Apartness.indist_equivalence`), with each law spent at exactly
   one clause and each omission refuted by a minimal finite
   countermodel (carriers 1, 2, 3 — the last minimal because
   cotransitivity is automatic on two points,
   `cotrans_auto_on_two`).

## 2. The first obstruction, and why it must resolve or create

Difference alone obstructs nothing.  The passage
(`PrimitivePassage`) prices every further ingredient:

- retention (`admitWit`) — else the witness evaporates
  (`retention_not_free`);
- protection (`protect`) — else collapse is unobstructed
  (`no_protection_no_obstruction`; fidelity is a demand, never a
  fact: `witness_no_protection`);
- a **declared** observation (`declareObs`) — else there is no zero
  relation at all (`obst_requires_observation`; pre-observational
  states obstruct nothing, as a theorem);
- observer-zero on the pair — the declared observation is blind to
  the protected retained difference.

**The first obstruction is the first moment all four conditions
coexist** (`obstP`; every maximal proper subset refuted,
`obst_conditions_independent`).  It is a normative conflict: the
state retains and protects a difference its own declared observation
cannot see.

**The two-rule theorem** (`two_rule`) is the forcing: at an active
obstruction the response universe never runs dry —

> same-level repair family nonempty, **or** same-level exhaustion
> certified and the extension-proposal family provably nonempty
> (`extension_always_available`: the singleton column on the first
> endpoint is fresh *because* the observation is blind to the pair —
> the obstruction manufactures its own way out).

Refusal (an inert record) and terminalization (absorbing) are
separately typed; proposal is not execution (license and budget
gate it); and the executed response provably kills the obstruction
on remeasurement (`extension_resolves`).  So the first obstruction
is **forced to self-resolve (repair) or create structure
(extension)** — under exactly the declared hypotheses, nothing
stronger claimed.

## 3. The growth of the first graph

The growth driver iterates that forcing (`HigherStructure`):

    round k+2:  admitOcc (k+2); admitWit (k+1,k+2); protect;
                setBudget 1;  ← obstruction active here (round_obstruction)
                addCol [k+1]  ← the structural response (round_resolution)

- `graphAt_spec` (induction): the grown state at stage `k+1` is
  exactly the **path graph** on `k+2` occurrences — vertices = admitted
  occurrences (0-cells), edges = retained witnessed pairs (1-cells) —
  with one observation column per resolved obstruction.
- The **creation record** of every column is the round's obstruction
  and its accepted response (`round_creation_record`: the last event
  of every round is the `addCol`; the artifact's growth log carries
  the per-round obstruction → response → resolution triple).
- Quiescence is restored after every round (`graphAt_quiescent`),
  and the growth is unbounded (`graph_growth`).

A witnessed binary relation **is** a directed graph presentation —
carrier plus binary store, identity rather than force.  What is
*not* forced is everything above dimension one.

## 4. The 0-, 1-, 2-, 3-simplices and the process that creates them

The declared cell calculus (`CEvent`, `cstep`) admits a `k+1`-cell
exactly over a complete, unfilled boundary of `k`-cells — the horn
guards are load-bearing (`horn_guard_load_bearing`) and the horn
does not fill itself (`filling_not_forced`).  The four-occurrence
demonstration (`k4_builds`) grows, in replayable creation order:

| dim | cells | created by | count |
|---|---|---|---|
| 0 | occurrences 0–3 | `addV` (passage: `admitOcc`) | 4 |
| 1 | the six witnessed edges | `addE` (passage: `admitWit`, `k4_skeleton_agrees`) | 6 |
| 2 | the four triangles | `addT` over complete edge boundaries | 4 |
| 3 | the solid cell | `addQ` over the complete face boundary | 1 |

**The process responsible for structure creation is the same at
every dimension** — an unfilled parallel boundary (the dimension-`k`
obstruction shape) resolved by creating the filling `k+1`-cell
(`ladder_dim2`, `ladder_dim3`).  This recurrence is the run's
central structural discovery, named below.

## 5. Named invariants

1. **The ladder invariant** — the two-rule shape recurs one
   dimension up, indefinitely: boundary-complete-and-unfilled is the
   dimension-`k` obstruction; the `k+1`-cell is its structural
   response (`two_rule`; `ladder_dim2`; `ladder_dim3`).
2. **The connectivity residue** — occurrences minus witnessed edges
   equals 1 at every growth stage
   (`path_connectivity_residue`): the growth never disconnects and
   never closes a loop.
3. **The occurrence alternation number** (`altNum`) — the
   alternating sum of cell counts; along the demonstration: 4
   (vertices), −2 (edges), 2 (closed shell), 1 (solid)
   (`altNum_stages`).
4. **The cut census** — the number of faithful two-block
   observations separating the designated pair: 1, 2, 4, 8 on
   carriers 2, 3, 4, 5 (`cut_census_growth`); the count of observer
   branches, 2^(n−2) as a finite computation.
5. **The orientation residue** — the strictly finer data retention
   carries above the apartness layer: both orientations generate the
   same apartness and the same indistinguishability while remaining
   distinct as data (`orientations_same_apartness`,
   `orientations_differ`); its preserver monoid is trivial
   (`oriented_preserver_unique`), while the apartness preservers
   form the two-element swap pair (`apart_preserver_pair`).
6. **The budget trichotomy** — every descriptor, every event: budget
   unchanged, saturating decrement, or explicit set
   (`Horizon.interp_budget_bound`) — the exact cross-language
   invariant.

## 6. What is forced, admitted, or unsupported (Phase IX verdicts)

- Graph: **identity** (a witnessed relation is a graph
  presentation); nothing to force.
- 2-cells from repair diamonds: **admitted, not forced** — the
  passage state carries no 2-cell data; the horn is present and the
  filler absent until declared (`filling_not_forced`).
- Chains/boundaries/d²=0: **declaration-relative** — with declared
  integer coefficients and boundary maps the composite vanishes on
  every demonstration cell (`d2_zero_triangles`, `d2_zero_tet`), and
  two distinct conventions both work (`boundary_not_forced`), so the
  convention carries real declared content; no vanishing statement
  exists without the declarations.
- Metric/amplitude realizations: **unsupported** — nothing in the
  run supplies inner products, amplitudes, or state spaces; no such
  realization is claimed.

Terminal for this phase: **HIGHER_STRUCTURE_OPTIONAL_NOT_FORCED**.

## 7. Post-hoc realization table (comparison only — nothing above
depends on this section)

Recorded per the run directive to name mathematical objects
identical to known mathematics.  Identity claims are keyed to the
laws actually proved, not to resemblance.

| Native object (proved laws) | Known mathematics |
|---|---|
| D2, the oriented two-point witnessed irreflexive relation | the one-edge directed graph; the standard 1-simplex Δ¹ as a directed edge; the "walking arrow" |
| `d2_initial` (unique edge-preserving pointed map to any witnessed pair) | initiality of the free/representing object on one arrow |
| S2, the symmetric two-point apartness | the complete graph K₂; the two-point set with its unique apartness |
| `IsApart` (irreflexive + symmetric + cotransitive) and `Indist` an equivalence | apartness relation in constructive mathematics; the negation-equivalence is the standard apartness-to-equality passage |
| the located axis (`Located`, OPEN cells) | decidability of the apartness; its independence mirrors the constructive/classical divide |
| ZeroRel = agreement on all declared columns, an equivalence | the kernel of an observation map; observational/bisimulation equivalence |
| observer cut, `no_terminal_pres`, cut census 2^(n−2) | bipartitions separating two marked points; failure of a terminal object in the poset of faithful quotients above three points |
| the growth's path graph, connectivity residue 1 | the path graph Pₙ; \|V\| − \|E\| = 1 characterizing trees (Euler formula, tree case) |
| cell calculus with horn guards; ladder invariant | simplicial complexes built by cell attachment; horn filling (the boundary-complete-and-unfilled condition is an outer-horn shape) |
| `altNum` values 4, −2, 2, 1; shell value 2; solid value 1 | Euler characteristic; χ(∂Δ³) = χ(S²) = 2; χ(Δ³) = 1 |
| `bd1/bd2/bd3` with `d²=0`; `boundary_not_forced` | the simplicial boundary operator over ℤ; orientation-convention freedom |
| two-rule at an obstruction | completion/attachment step: resolve within the presentation or attach a cell |
| interpreter diagonalization (Phase VIII paper) | finite diagonal argument (Cantor-style) against a universal in-class evaluator |
| description/interpretation non-identification (Phase VIII paper) | the use–mention distinction; stratified metalanguage hierarchies |

Non-identifications, recorded deliberately: the passage's obstruction
is *not* a homotopical obstruction class (no coefficient system is
derived, only declared); the controller category's simulations are
transition-system simulations, and no claim links them to any
enriched or higher-categorical structure; nothing here derives a
metric, measure, or amplitude.

## 8. Terminals, adversarial record, and receipt

The run ends with ten terminal codes, each mapped to theorem or
countermodel evidence, five open obligations, the twenty-attack
adversarial record (every attack with its disposition), and the two
withdrawn-or-repaired claims — all machine-readable in
`artifacts/primitive_completion_receipt.json`.  Controller
universality: refuted, with the reachable-orbit salvage
(`paper/primitive_controller_universality.md`).  Interpreter
boundary: tower persists; the boundary is a Primitive Difference
(`paper/primitive_interpreter_boundary.md`).  The strongest
defensible terminal statement of the whole run:

> The weakest object deserving the name Primitive Difference is the
> pointed witnessed irreflexive relation, initial in its category;
> every further capacity — symmetry, cotransitivity, locatedness,
> retention, protection, observation — is a separately priced
> admission; the first obstruction exists only when a declared
> observation collapses a protected retained difference, and it is
> then forced to a response: same-level repair or structure
> creation; iterating that forcing grows the first graph, and the
> same forcing shape, one dimension up, grows the simplices; no
> controller realizing this is categorically unique; and the
> boundary between describing this system and running it is itself
> the next Primitive Difference.

