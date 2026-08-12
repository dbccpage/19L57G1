# The Native Primitive-Difference Interface

**Mission.**  Externally imposed challenge (caller request,
2026-08-12): extend the metatheory with a self-contained,
adapter-independent theorem package exposing the pipeline

```text
reflection → retained/protected zero-pair → active obstruction
           → orbit closure or extension proposal
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
| bare reflection, factored | `BareReflection`: embedding + retraction (`retract_embed`), genuinely fresh point (`fresh_genuine`, live-scoped), declared parent, preservation of old structure (`zero_preserved` — an iff on the old live region — with `retained_embed`, `guarded_embed`), retained + protected parent/new pair, pre-closure zero (`pair_zero`) | definition |
| reflection produces an active obstruction | `bare_reflection_active_obstruction` — on a pair that is metatheoretically distinct yet observer-zero, retained, protected | theorem |
| closure over complete symmetry orbits, no least representative | demands are a *predicate* `D : X → X → Prop` (there is no ordering and no representative anywhere in the interface); `OrbitComplete` requires closure under exchange and under every declared symmetry (`StageSym`); `ClosureStep` discharges such a set by same-carrier, same-result-type refinement | definition |
| same-carrier steps preserve old distinctions | `refines_preserves_distinctions`, `closure_preserves_old_distinctions` | theorem |
| strict decrease of a declared finite measure | abstractly: `closure_kills_demanded` + `closure_adds_no_obstruction`; concretely: `measureC` (the count of retained, protected, observer-zero ordered pairs), `closed_measure_zero`, `preclose_measure_pos`, `towerNext_decrease` | theorem |
| extension = proposal, not authorized transition | `ExtensionProposal` is data (kind + demanded set); `ClosureOutcome.propose` carries it; nothing in the package constructs a stage from a proposal | definition (discipline) |
| finite fuel ⇒ termination, uniform orbit bound | `drive_terminates` (generic: fuel exceeding the measure never runs out), instantiated by `tower_fuel_terminates`; the fixed uniform orbit bound is `B = 2` (`tower_orbit_bound`, `tower_orbit_characterized`) | theorem |
| no fuel ⇒ infinite compatible trace | `tower_infinite_trace`: at *every* `n` a bare reflection and an orbit-complete closure step whose application **is** the next closed stage, definitionally (`tower_step_composes`); old distinctions persist across all later stages (`cview_distinct_mono`) — every finite prefix is a legal derivation | theorem |
| countermodels | freshness / tagging / edge / hash / repetition, below | countermodels |

## The concrete realization (non-vacuity)

Carrier `Nat`, result type `Nat × Nat`, observers = kernels of the
horizon-capped rank view `min · h` (every concrete observer is a
kernel observer, so its equivalence laws are inherited from
`kernelObs`, proved once).  A closed stage at size `s` carries horizon
`s − 1`: all live ranks distinct, measure zero (`tower_closed`,
`closed_measure_zero`).  Bare reflection adds the fresh point with the
*stale* observer — the declared parent and the fresh point collide
(`tower_obstruction`), which is exactly the pipeline's active
obstruction.  The demand orbit under the declared symmetries (identity
and the top-swap, which provably preserves liveness, retention,
protection, and live zero-pairs) is the full two-orientation set,
discharged by one uniform horizon re-synchronization — no
representative chosen, the whole orbit at once.  Application of that
step *is* the next closed stage by `rfl`.

The trace is therefore infinite and compatible: reflection, active
obstruction, orbit closure, closed stage — for every `n`, uniformly,
with no fuel and no external act besides the reflection discipline
itself.  With fuel, `drive` reaches `closed` whenever fuel exceeds the
declared measure (`drive_terminates`); the Python mirror runs both
regimes to the 15-round bound and byte-reproduces.

## The family that must propose

Three protected points under the Boolean-view grammar: whatever view
is chosen — including any later refinement drawn from the same grammar
— two points collide (`bool_view_pigeonhole`,
`bool_grammar_obstruction`, `bool_grammar_must_propose`; checked
exhaustively over all eight views in Python).  No same-grammar closure
step can discharge the family, so the pipeline returns
`ExtensionProposal { kind := observerStructure, demanded := … }` —
data carrying the undischarged orbit, authorizing nothing.  This is
the interface-level form of the development's standing result that
observation grammars have capacity ceilings (the expressiveness
ceiling of the F5 run, and conjecture G1).

## Countermodels

Each names a feature that does **not** by itself produce
observer-visible difference, and — with protection absent — does not
produce an active obstruction either.  All are concrete finite
instances (`cm_freshness`, `cm_tagging`, `cm_edge`, `cm_hash`,
`cm_repetition`):

* **freshness** — the genuinely fresh point is observer-zero with its
  parent under the stale horizon; unguarded, it obstructs nothing;
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

Together with the three blocking lemmas, these witness the full
independence of the three obstruction conditions: every proper subset
of {retained, observer-zero, protected} is realized without the
conjunction.

## Boundary statements

* The package assumes nothing about any downstream consumer, imports
  no other module of this development, and names no external theory.
  The caller's adapter is external evidence, out of scope by design.
* `Stage.guarded` is the protection predicate ("must eventually be
  distinguished"); the field is named `guarded` only because
  `protected` is a reserved word.
* All 34 exported theorems report axioms within {propext, Quot.sound}
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
* Quantitative fuel from the orbit bound alone (fuel ≈ orbit count),
  sharpening `drive_terminates`'s measure-based budget.
* The class-general capacity theorem behind the Boolean-grammar
  proposal (conjecture G1 of the F5 run).
