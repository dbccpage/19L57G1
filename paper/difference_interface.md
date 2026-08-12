# The Native Primitive-Difference Interface

**Mission.**  Externally imposed challenge (caller request,
2026-08-12): extend the metatheory with a self-contained,
adapter-independent theorem package exposing the pipeline

```text
reflection certificate → retained/protected zero-pair
  → active obstruction → map-saturated closure step
  or separately represented extension proposal
```

built around a typed difference operation.  The caller will map the
native definitions into their own types afterward; that independent
adapter is part of *their* evidence and is assumed nowhere here.  The
package (`lean4/Derivation/DiffInterface.lean`) imports core Lean only
— it does not depend on any other module of this development — and its
concrete realization and countermodels are mirrored deterministically
in `code/derivation/diff_interface.py` with artifact
`artifacts/diff_interface.json`.

## DELIVERED

Every requested component, with its evidence class:

| requirement | delivery | class |
|---|---|---|
| `δ : X → X → R`, `Zero : R → Prop`, `ZeroRel x y := Zero (δ x y)` | `DiffObs`, `ZeroRel` | definition |
| ZeroRel is an equivalence, **before any quotient** | `zeroRel_equivalence`; the quotient (`ObsQuotient`) is constructible only downstream, because it needs the `Setoid` built from that proof — the ordering is enforced by the dependency itself | theorem |
| three predicates kept separate | `Stage.retained` / `ZeroRel S.obs` / `Stage.guarded` (protection), independent fields with no coherence assumptions; separations witnessed by `no_guard_no_obstruction`, `unretained_not_active`, `distinguished_not_active` | definition + theorems |
| active obstruction = the conjunction | `ActiveObstruction` | definition |
| bare reflection, factored | `BareReflection`: embedding + retraction (`retract_embed`), a point outside the old live image (`fresh_from_live_image`), declared parent, preservation of old structure (`zero_preserved` — an iff on the old live region — with `retained_embed`, `guarded_embed`), retained + protected parent/new pair, pre-closure zero (`pair_zero`) | definition |
| reflection certificate contains an active obstruction | `bare_reflection_certifies_active_obstruction` packages a distinct pair with the retained, observer-zero, and protected fields already required by `BareReflection`; freshness alone does not imply the conclusion | theorem |
| closure over map-saturated demands, no preferred pair | abstract demands are predicates `D : X → X → Prop`; `MapSaturated` requires closure under exchange and each declared relation-preserving map (`StageMaps`), without claiming inverses or composition; concrete finite evidence may enumerate the predicate | definition |
| same-carrier steps preserve old distinctions | `refines_preserves_distinctions`, `closure_preserves_old_distinctions` | theorem |
| strict decrease of a declared finite measure | abstractly: demanded pairs are off-diagonal by the `ClosureStep.demand_offdiag` invariant, `closure_kills_demanded` discharges all of them, and `closure_adds_no_obstruction` pulls later activity back; concretely: `measureC`, `closed_measure_zero`, `preclose_measure_pos`, `towerNext_decrease` | theorem |
| extension = proposal, not authorized transition | `ExtensionProposal` is data (kind + demanded set); `ClosureOutcome.propose` carries it; nothing in the package constructs a stage from a proposal | definition (discipline) |
| finite fuel ⇒ termination | `drive_terminates` is conditional on strict measure decrease and is instantiated by `tower_fuel_terminates`; separately, the concrete demand predicate has a two-element enumerator (`tower_demand_bound`, `tower_demand_characterized`) | theorem |
| uniform successor-step family | `tower_successor_step`: at every `n` a bare-reflection certificate and map-saturated closure step are available, and application is the next closed stage definitionally (`tower_step_composes`); this is pointwise and does not formalize a trace object or finite-prefix induction | theorem |
| countermodels | freshness / tagging / edge / hash / repetition, below | countermodels |

## The concrete realization (non-vacuity)

Carrier `Nat`, result type `Nat × Nat`, observers = kernels of the
horizon-capped rank view `min · h` (every concrete observer is a
kernel observer, so its equivalence laws are inherited from
`kernelObs`, proved once).  A closed stage at size `s` carries horizon
`s − 1`: all live ranks distinct, measure zero (`tower_closed`,
`closed_measure_zero`).  The tower reflection certificate adds a point
outside the old live image while retaining the *stale* observer.  Its
declared parent/new pair collides (`tower_obstruction`) because the
certificate explicitly includes retention, protection, and the zero
fact.  The demand predicate is saturated under exchange and the
declared identity/top-swap maps, which preserve liveness, retention,
protection, and live zero-pairs.  One horizon re-synchronization
discharges the full predicate, and application is the next closed stage
by `rfl`.

The Lean package proves this successor-step shape uniformly for every
`n`.  It does not package the steps into an explicit infinite trace or
prove a separate theorem about every finite prefix.  With fuel, `drive`
reaches `closed` whenever fuel exceeds the declared measure
(`drive_terminates`); the Python mirror checks 15 rounds and
byte-reproduces.  The two-element demand bound is a separate concrete
fact, not the premise used by the termination theorem.

## A grammar with no closed view

Three protected points under the Boolean-view grammar: whatever view
is chosen — including any replacement view drawn from the same grammar
— two points collide (`bool_view_pigeonhole`,
`bool_grammar_obstruction`, `no_bool_view_is_closed`; checked
exhaustively over all eight views in Python).  Thus no view in the
grammar closes the stage.  `boolProposal` separately constructs
`ExtensionProposal { kind := observerStructure, demanded := … }` as
available request data, authorizing nothing.  No decision function or
theorem here says that a pipeline must select that proposal.

## Countermodels

Each names a feature that does **not** by itself produce
observer-visible difference, and — with protection absent — does not
produce an active obstruction either.  All are concrete finite
instances (`cm_freshness`, `cm_tagging`, `cm_edge`, `cm_hash`,
`cm_repetition`):

* **freshness** — a point outside the old live image is observer-zero
  with its parent under the stale horizon; unguarded, it obstructs
  nothing;
* **tagging** — a presence tag carried by both points leaves their
  kernel views equal (the presence-grade vacuity of the F5 run, in
  interface form);
* **an edge** — under a symmetric incidence view, both endpoints of
  the single admitted relation instance look identical: an edge alone
  neither separates nor orients;
* **a new hash** — a metatheoretically injective label the observer
  does not read changes nothing observable: receipts and hashes are
  metatheory until admitted into the observer;
* **repetition** — two occurrence indices presenting one token
  collapse under the token view: multiplicity is invisible to
  presence-grade observation.

Each Lean countermodel now includes its unprotected stage and proves
the displayed pair inactive.  The three blocking lemmas independently
show that removing any conjunct rules out activity.  The finite examples
do not claim to realize every proper subset of the three conditions.

## Boundary statements

* The package assumes nothing about any downstream consumer, imports
  no other module of this development, and names no external theory.
  The caller's adapter is external evidence, out of scope by design.
* `Stage.guarded` is the protection predicate ("must eventually be
  distinguished"); the field is named `guarded` only because
  `protected` is a reserved word.
* All 35 exported theorems report axioms within {propext, Quot.sound}
  (`Quot.sound` enters only through the optional quotient realization
  and standard list lemmas; the toolchain's `omega`-on-compound-goals
  and `List.eq_nil_iff_forall_not_mem` choice leaks were avoided —
  change log §11).
* Known limits, stated: `zero_preserved` and `zero_pres` are scoped to
  the live region (outside it the concrete top-swap is not
  view-preserving, and no claim is made); the interface's termination
  theorem is conditional on the declared measure decrease, which is
  proved for the concrete family and required as a field elsewhere.

## Open extensions (not obligations of this package)

* A proposal-*processing* discipline: admitting an
  `ExtensionProposal` as a new stage via a separately defined
  admission event, with its own replay rule — the interface
  deliberately stops at the proposal boundary.
* Quantitative fuel from the demand bound alone (fuel ≈ demand count),
  sharpening `drive_terminates`'s measure-based budget.
* A decision rule connecting a failed same-grammar closure search to an
  extension proposal.
* The class-general capacity theorem behind the Boolean-grammar
  obstruction (conjecture G1 of the F5 run).
