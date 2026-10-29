# Unit 44. Reflect, obstruct, close, or propose: a typed interface for primitive difference

**Claim.** An active obstruction requires a retained pair, protection, and observer-zero agreement. The declared interface then describes a same-carrier closure or an extension proposal under its stated hypotheses.

**Status:** derived; the abstract theorems are conditional
on declared bundles; the tower driver closes in one step, so the
concrete termination instance is degenerate; the countermodels' `¬
Active` conjunct is the removal of protection, by construction.
**Lean:** `lean4/Derivation/DiffInterface.lean` lines 33-760, core Lean
only. **Axioms:** 17 theorems use none; `obsQuotient_eq_of_zero`
`Quot.sound`; `tower_demand_characterized` `propext`; the other 16
`{propext, Quot.sound}`. **Depends on:** nothing in Genesis; the
closure-policy discipline of Unit 29 (three separate conditions) is the
reason for the shape.

## First pass

Read the three tests separately. Is the pair retained? Is it protected? Does the current observer still merge it?

Only their conjunction is an active obstruction. A proposal for extending the carrier records possible work; it does not execute that work.

For concrete examples, use the [Change lab](../change_lab/README.md) and
[Map lab](../map_lab/README.md). The [reading guide](../reading_formal_statements.md)
explains the symbols and the distinction between a condition and a decider.

## Detailed claim and formal anchors

`DiffInterface` is a self-contained package, written to an
external request of 2026-08-12, that types the pipeline *reflection
certificate → retained, protected, observer-zero pair → active
obstruction → same-carrier closure step, or an extension proposal*.

A
difference observer is `δ : X → X → R` with a zero predicate and the
three equivalence laws as fields; `ZeroRel` is proved an equivalence
(`zeroRel_equivalence`) before the quotient is built.

A stage has
liveness, retention, protection (`guarded`) and an observer; an active
obstruction is the conjunction retained ∧ observer-zero ∧ guarded, and
dropping any conjunct blocks it.

A `BareReflection` certificate contains
an active obstruction on its parent/fresh pair
(`bare_reflection_certifies_active_obstruction`).

A `ClosureStep`
refines the observer over the same carrier: it keeps every old
distinction, kills every demanded pair, and creates no new obstruction.

An `ExtensionProposal` is data, never applied.

A fuel driver returns a result tagged
`closed` or `proposal` when fuel exceeds a strictly decreasing measure
(`drive_terminates`).

The tower `mkStage s h` (horizon-capped rank
views) realizes every piece at every `n` (`tower_obstruction`,
`tower_step_composes`, `closed_measure_zero`, `tower_fuel_terminates`).

Three protected points under a single Boolean-valued view cannot all be distinguished
(`bool_grammar_obstruction`), and five countermodels (freshness, tagging,
an edge, a hash, repetition) show a feature without observer-visible
difference.

## Question

The derivation keeps three things apart: whether a pair is still in
play (retained), whether the observer can tell its members apart
(observer-zero or not), and whether the system has promised to tell
them apart (protected). What is the smallest typed interface in which a
"reflection" step produces such a pair, a "closure" step discharges it
without choosing a representative, and a request for new structure is
recorded without being granted? And what does the interface refuse to
do?

## What we already possess

- The closure policy's three conditions (Unit 29) and the reflective
  chain (Unit 40).
- Equivalence relations and quotients in Lean (`Setoid`, `Quotient`,
  `Quotient.sound`).
- Recursion on a fuel argument (Unit 31's engine bounds, in spirit).

## New concept: an observer with its laws, a stage, a certificate, a step

### The observer: a report and a condition

`DiffObs X R` names an input type X and a report type R. Its `delta`
function assigns a report to each ordered pair of inputs. Its `Zero`
condition says which reports count as zero. R need not be a type of numbers;
"zero" is the declared condition's name.

`ZeroRel O x y := O.Zero (O.delta x y)` means the report for x and y
satisfies that condition. `Zero : R → Prop` is a mathematical property.
The abstract record does not require an algorithm deciding it. Concrete
Python implementations supply executable tests separately.

### The laws and the classes

Three proof fields make this zero relation an equivalence: every item is
related to itself; reversing a related pair preserves the relation; and
two consecutive related pairs give a related endpoint pair. A `Setoid`
packages the relation with these laws. `ObsQuotient O` then groups items
by it. This is the source's "equivalence before quotient" dependency.

`kernelObs view` is a particular construction: its report is the ordered
pair of view values, and zero means those values are equal. Equality
supplies its three laws. This particular construction does not make every
abstract observer an executable measurement procedure.

*Stage.* `live`, `retained`, `guarded`, `obs`, four independent fields.
`ActiveObstruction S x y := retained ∧ ZeroRel ∧ guarded`.
This definition does not automatically require live endpoints; liveness
is a separate field with separate hypotheses in the certificate and map records.

*Certificate.* `BareReflection S S'` has fifteen fields. The theorem uses
the `embed`, `parent`, and `fresh` data and five proof fields.
`fresh_from_live_image` and `parent_live` establish that the new point
differs from the embedded parent. `pair_retained`, `pair_guarded`, and
`pair_zero` establish the three active-obstruction conditions. Freshness
alone does not establish those three supplied pair properties.

*Step.* `StageMaps` is a list of maps containing the identity;
`MapSaturated G D` says the demand `D` is symmetric and closed under
every map; `ClosureStep` is a demand (active, off-diagonal, saturated), a
new observer `obs'` refining the old (`Refines obs' S.obs`: every new
zero pair was an old zero pair) and a proof that every demanded pair is
no longer zero. `apply` replaces the observer and nothing else.

The chosen demand condition D need not include every active pair, or even
any pair. With D empty and the old observer kept, the interface admits an
identity step. The book check constructs this for any supplied stage and
stage-map bundle. A strictly decreasing measure is an additional progress
hypothesis, not a consequence of naming an object `ClosureStep`.

*Proposal.* `ExtensionProposal` is a kind and a demanded set. Nothing
builds a stage from it.

*Driver.* `drive next fuel s` runs `next` until `none` (closed), a
proposal, or fuel runs out.

Here `closed` is the generic driver's result tag when `next s = none`.
The termination theorem assumes each continuing step decreases a measure;
it does not require `next` to search all repairs or make that tag mean
there are no active pairs. The book counterexample supplies a `next` that
immediately returns `none` while a retained, protected zero-pair remains
active. A stronger interpretation needs the concrete driver's additional
properties.

## Plain-language interpretation

As an analogy, think of a ruler together with rules for when two readings
count as the same. The formal observer is the specified function and
condition, with equivalence proofs; no physical instrument or decision
algorithm follows from the interface alone. A stage specifies which
points are live, which pairs are retained in the record, which pairs are
protected by the supplied rule, and which observer is in use. An active
obstruction is a retained, protected pair that is zero-related under
that observer.
A reflection adds a fresh point the stale ruler cannot tell from its
parent, and the certificate says so in its own fields. A closure
replaces the ruler by a finer one over the same points: everything that
was distinct stays distinct, every demanded pair becomes distinct, and
nothing new becomes an obstruction. A supplied driver can instead return
a request for new structure. Returning that proposal does not itself
prove that every same-carrier closure is impossible. The interface records
the request without granting it.

The tower is the worked example: points `0, 1, 2, …`, the ruler "rank
capped at the horizon `h`". A closed stage has horizon one below its
size, so every point has its own rank. Adding the point `s` with the
old horizon makes it look like `s − 1`; raising the horizon by one
fixes it. Three points with one yes/no answer per point can never all be
told apart, whichever single question is chosen. Using several questions
can give more answer patterns, as in the Map lab; that changes this declared
single-Boolean-view setting. And five features (being new, being
tagged, being an endpoint of an edge, having a distinct label, being
repeated) do nothing to a ruler that does not read them.

Two things the lesson flags. The driver on the tower closes in one
step, always, so the "fuel termination" instance tests the generic
theorem only in its trivial case. And each countermodel's "not an
active obstruction" conjunct holds because the countermodel stage has
no protected pairs at all: it says nothing about the feature under
protection. The book check protects the tagging stage and the pair
becomes active.

## Pseudocode

```
DiffObs X R     = (delta : X → X → R, Zero : R → Prop, refl, symm, trans)
ZeroRel O x y   = O.Zero (O.delta x y)
kernelObs view  = (delta x y := (view x, view y), Zero p := p.1 = p.2)

Stage X R       = (live, retained, guarded, obs)
Active S x y    = retained x y ∧ ZeroRel S.obs x y ∧ guarded x y

certificate B : S → S'  ⟹  embed parent ≠ fresh ∧ Active S' (embed parent) fresh
                             -- from fresh_from_live_image parent_live, pair_retained, pair_zero, pair_guarded

ClosureStep C   = (D, D ⊆ Active, D off-diagonal, D map-saturated, obs', obs' refines obs, D ⊆ ¬ZeroRel obs')
C.apply         = S with obs := obs'
  old distinction kept;  demanded pair no longer active;  Active C.apply ⊆ Active S

drive next fuel s:  fuel = 0 → outOfFuel; next s = none → closed; inl s' → drive (fuel−1) s'; inr p → proposal
drive_terminates:   μ strictly decreases on inl steps, μ s < fuel  ⟹  closed or proposal

tower:  cview h i = min i h;  mkStage s h = (i < s, i<s ∧ j<s, i<s ∧ j<s ∧ i≠j, kernelObs (cview h))
        towerReflection n : mkStage (n+1) n → mkStage (n+2) n, fresh n+1, parent n
        towerClosure n : D = {(n,n+1),(n+1,n)}, obs' = kernelObs (cview (n+1)); apply = mkStage (n+2) (n+1)  (rfl)
        measureC s h = #{(i,j) : i,j < s, i ≠ j, min i h = min j h};  measureC s (s−1) = 0
        towerNext (s,h) = none if measureC = 0 else inl (s, s−1)        -- one step, always
bool:   any view : Nat → Bool identifies two of 0,1,2  ⟹  bStage view has an active obstruction
```

## Python

Genesis's mirror is `code/derivation/diff_interface.py`, artifact
`artifacts/diff_interface.json`.

```python
from derivation.diff_interface import active_pairs, measure, drive, tower_next, bool_grammar_report
print(active_pairs(4, 2), measure(4, 3))          # [(2, 3), (3, 2)] 0
print(drive(tower_next, 2, (5, 3)))              # ('closed', (5, 4), None)
print(drive(tower_next, 1, (5, 3)))              # ('out_of_fuel', (5, 4), None)
print(bool_grammar_report()["every_view_obstructed"])   # True
```

The check script's run:

```text
tower, rounds 0..14: closed measure before, pre-closure measure, demand support, measure after
  round 0: 0, 2, [[0, 1], [1, 0]], 0
  round 1: 0, 2, [[1, 2], [2, 1]], 0
  round 2: 0, 2, [[2, 3], [3, 2]], 0
  round 3: 0, 2, [[3, 4], [4, 3]], 0
  ... all 15 rounds: {'all_closed_before': True, 'all_obstruct_after_reflection': True, 'all_strictly_decrease': True, 'all_preserve_old': True}; uniform demand bound 2; artifact agrees: True
active pairs of (s, h) = (4, 1): [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]; measure 6; (4, 2): [(2, 3), (3, 2)]; (4, 3): []
swap_top 3 on 0..5: [0, 1, 2, 4, 3, 2]; views under horizon 3: [0, 1, 2, 3, 3, 3] -> [0, 1, 2, 3, 3, 2]
fuel driver from (n+2, n): measure [2], fuel measure+1 -> ['closed']; fuel 2 -> closed at ('closed', (5, 4), None); fuel 1 -> {'out_of_fuel'}
Boolean views of three protected points and their surviving pairs:
  [0, 0, 0] -> [[0, 1], [0, 2], [1, 2]]
  [0, 0, 1] -> [[0, 1]]
  [0, 1, 0] -> [[0, 2]]
  [0, 1, 1] -> [[1, 2]]
  [1, 0, 0] -> [[1, 2]]
  [1, 0, 1] -> [[0, 2]]
  [1, 1, 0] -> [[0, 1]]
  [1, 1, 1] -> [[0, 1], [0, 2], [1, 2]]
  every view obstructed: True; artifact agrees: True
  a three-valued view (identity) leaves []: the grammar, not the points, forces the obstruction
countermodels (feature present, observer zero, guarded, active); active if the stage were protected:
  freshness: True, True, False, False; protected -> True
  tagging: True, True, False, False; protected -> True
  edge: True, True, False, False; protected -> True
  new_hash: True, True, False, False; protected -> True
  repetition: True, True, False, False; protected -> True
  artifact agrees: True
failures: []
```

## Line-by-line Python explanation

`cview(h, i)` is `min(i, h)`. `active_pairs(s, h)` lists ordered pairs
`i ≠ j` below `s` with equal capped rank; `measure` is its length:
Lean's `activePairs` and `measureC`. `tower_round(n)` records one round:
the closed stage `(n + 1, n)` has measure 0; the reflected stage
`(n + 2, n)` has measure 2, the pair `(n, n + 1)` both ways; the demand
support is that pair closed under the top swap (which fixes it as a
set); after closure `(n + 2, n + 1)` the measure is 0 again; and every
pair distinct under horizon `n` is distinct under `n + 1`. Fifteen
rounds, all flags true, the artifact byte-identical.

The `(4, 1)` line shows a stage two horizons stale: points 1, 2, 3 all
read 1, six ordered pairs. `swap_top(3, ·)` exchanges 3 and 4 and fixes
0, 1, 2; on 5, outside the live region `0..4`, it gives 2, and the view
changes from 3 to 2: the module's boundary statement that the swap is
not view-preserving off the live region, made concrete.

`drive` runs `next` for at most `fuel` iterations. `tower_next` returns
`None` when no active pair remains, else the step to `(s, s − 1)`. So
from any stale stage the run is one step: fuel 2 closes at `(5, 4)`,
fuel 1 takes the step and then reports out of fuel at the same state.
Genesis's `fuel_report` uses `measure + 1 = 3`; the check shows 2 is
enough and 1 is not, which is the content of "one step".

`bool_grammar_report` enumerates all eight views of three points and
lists the pairs with equal values; every row is non-empty. The identity
view with three values has no colliding pair: the obstruction is a fact
about the two-valued grammar.

`countermodel_report` computes, for each feature, that it is present,
that the chosen observer reads zero on the pair, that the stage is
unguarded, and that activity (the three-way conjunction) is false. The
check adds the column "protected": with `guarded = True` and the same
two other conjuncts, every row is active. That is the audit's point: the
countermodels show a feature invisible to one observer; they show
nothing about what protection would do.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/DiffInterface.lean lines 33-82, 92-122
structure DiffObs (X R : Type) where
  delta : X → X → R
  Zero : R → Prop
  zero_refl : ∀ x, Zero (delta x x)
  zero_symm : ∀ {x y}, Zero (delta x y) → Zero (delta y x)
  zero_trans : ∀ {x y z},
    Zero (delta x y) → Zero (delta y z) → Zero (delta x z)

def ZeroRel (O : DiffObs X R) (x y : X) : Prop := O.Zero (O.delta x y)

theorem zeroRel_equivalence (O : DiffObs X R) :
    Equivalence (ZeroRel O) :=
  ⟨fun x => O.zero_refl x, fun h => O.zero_symm h,
   fun h1 h2 => O.zero_trans h1 h2⟩

def kernelObs (view : X → V) : DiffObs X (V × V) where
  delta x y := (view x, view y)
  Zero p := p.1 = p.2
  zero_refl _ := rfl
  zero_symm h := h.symm
  zero_trans h1 h2 := h1.trans h2

def obsSetoid (O : DiffObs X R) : Setoid X :=
  ⟨ZeroRel O, zeroRel_equivalence O⟩

def ObsQuotient (O : DiffObs X R) : Type := Quotient (obsSetoid O)

theorem obsQuotient_eq_of_zero (O : DiffObs X R) {x y : X}
    (h : ZeroRel O x y) : ObsQuotient.mk O x = ObsQuotient.mk O y :=
  Quotient.sound h

structure Stage (X R : Type) where
  live : X → Prop
  retained : X → X → Prop
  guarded : X → X → Prop
  obs : DiffObs X R

def ActiveObstruction (S : Stage X R) (x y : X) : Prop :=
  S.retained x y ∧ ZeroRel S.obs x y ∧ S.guarded x y

theorem no_guard_no_obstruction (S : Stage X R)
    (h : ∀ x y, ¬ S.guarded x y) : ∀ x y, ¬ ActiveObstruction S x y :=
  fun x y ⟨_, _, hg⟩ => h x y hg
```

```lean
-- Lean (Genesis), lean4/Derivation/DiffInterface.lean lines 133-161, 203-236, 264-293
structure BareReflection (S : Stage X R) (S' : Stage X' R) where
  embed : X → X'
  retract : X' → X
  retract_embed : ∀ x, retract (embed x) = x
  fresh : X'
  fresh_live : S'.live fresh
  fresh_from_live_image : ∀ x, S.live x → embed x ≠ fresh
  parent : X
  parent_live : S.live parent
  live_embed : ∀ x, S.live x → S'.live (embed x)
  zero_preserved : ∀ x y, S.live x → S.live y →
    (ZeroRel S.obs x y ↔ ZeroRel S'.obs (embed x) (embed y))
  retained_embed : ∀ x y, S.retained x y →
    S'.retained (embed x) (embed y)
  guarded_embed : ∀ x y, S.guarded x y → S'.guarded (embed x) (embed y)
  pair_retained : S'.retained (embed parent) fresh
  pair_guarded : S'.guarded (embed parent) fresh
  pair_zero : ZeroRel S'.obs (embed parent) fresh

theorem bare_reflection_certifies_active_obstruction
    {S : Stage X R} {S' : Stage X' R} (B : BareReflection S S') :
    B.embed B.parent ≠ B.fresh ∧
      ActiveObstruction S' (B.embed B.parent) B.fresh :=
  ⟨B.fresh_from_live_image _ B.parent_live,
   B.pair_retained, B.pair_zero, B.pair_guarded⟩

structure ClosureStep (S : Stage X R) (G : StageMaps S) where
  D : X → X → Prop
  demands_active : ∀ x y, D x y → ActiveObstruction S x y
  demand_offdiag : ∀ x y, D x y → x ≠ y
  map_saturated : MapSaturated G D
  obs' : DiffObs X R
  refines : Refines obs' S.obs
  discharges : ∀ x y, D x y → x ≠ y → ¬ ZeroRel obs' x y

def ClosureStep.apply {S : Stage X R} {G : StageMaps S}
    (C : ClosureStep S G) : Stage X R := S.withObs C.obs'

theorem closure_kills_demanded {S : Stage X R} {G : StageMaps S}
    (C : ClosureStep S G) (x y : X) (hD : C.D x y) :
    ¬ ActiveObstruction C.apply x y :=
  fun ⟨_, hz, _⟩ => C.discharges x y hD (C.demand_offdiag x y hD) hz

theorem closure_adds_no_obstruction {S : Stage X R} {G : StageMaps S}
    (C : ClosureStep S G) (x y : X) :
    ActiveObstruction C.apply x y → ActiveObstruction S x y :=
  fun ⟨hr, hz, hg⟩ => ⟨hr, C.refines x y hz, hg⟩

def drive {σ P : Type} (next : σ → Option (σ ⊕ P)) :
    Nat → σ → RunResult σ P
  | 0, s => .outOfFuel s
  | fuel + 1, s =>
      match next s with
      | none => .closed s
      | some (.inl s') => drive next fuel s'
      | some (.inr p) => .proposal s p

theorem drive_terminates {σ P : Type} (next : σ → Option (σ ⊕ P))
    (μ : σ → Nat)
    (hdec : ∀ s s', next s = some (.inl s') → μ s' < μ s) :
    ∀ fuel s, μ s < fuel →
      (∃ s', drive next fuel s = .closed s') ∨
        (∃ s' p, drive next fuel s = .proposal s' p) := by
  intro fuel
  induction fuel with
  | zero => intro s h; exact absurd h (Nat.not_lt_zero _)
  | succ f ih =>
      intro s h
      cases hn : next s with
      | none => exact Or.inl ⟨s, by simp [drive, hn]⟩
      | some v =>
          cases v with
          | inl s' =>
              have hd := hdec s s' hn
              have := ih s' (by omega)
              simpa [drive, hn] using this
          | inr p => exact Or.inr ⟨s, p, by simp [drive, hn]⟩
```

```lean
-- Lean (Genesis), lean4/Derivation/DiffInterface.lean lines 306-331, 368-370, 482-491, 523-524, 537-549, 594-601, 617-623, 632-654, 680-688
def cview (h i : Nat) : Nat := min i h

def mkStage (s h : Nat) : Stage Nat (Nat × Nat) where
  live i := i < s
  retained i j := i < s ∧ j < s
  guarded i j := i < s ∧ j < s ∧ i ≠ j
  obs := kernelObs (cview h)

theorem tower_closed (s : Nat) (x y : Nat)
    (h : ActiveObstruction (mkStage s (s - 1)) x y) : False := by
  obtain ⟨⟨hx, hy⟩, hz, _, _, hne⟩ := h
  have hv : min x (s - 1) = min y (s - 1) := hz
  omega

theorem tower_obstruction (n : Nat) :
    (n : Nat) ≠ n + 1 ∧ ActiveObstruction (mkStage (n + 2) n) n (n + 1) :=
  bare_reflection_certifies_active_obstruction (towerReflection n)

theorem tower_step_composes (n : Nat) :
    (towerClosure n).apply = mkStage (n + 2) (n + 1) := rfl

def measureC (s h : Nat) : Nat := (activePairs s h).length

theorem closed_measure_zero (s : Nat) : measureC s (s - 1) = 0 := by
  unfold measureC
  have hnil : activePairs s (s - 1) = [] := by
    cases hp : activePairs s (s - 1) with
    | nil => rfl
    | cons p l =>
        exfalso
        have hm : p ∈ activePairs s (s - 1) := by
          rw [hp]; exact List.mem_cons_self
        obtain ⟨i, j⟩ := p
        rw [mem_activePairs] at hm
        obtain ⟨hi, hj, hne, hv⟩ := hm
        omega
  rw [hnil]
  rfl

def towerNext (st : Nat × Nat) :
    Option ((Nat × Nat) ⊕ ExtensionProposal Nat (Nat × Nat)) :=
  if activePairs st.1 st.2 = [] then none
  else some (.inl (st.1, st.1 - 1))

theorem tower_fuel_terminates (s h fuel : Nat)
    (hfuel : measureC s h < fuel) :
    (∃ st, drive towerNext fuel (s, h) = .closed st) ∨
      (∃ st p, drive towerNext fuel (s, h) = .proposal st p) :=
  drive_terminates towerNext (fun st => measureC st.1 st.2)
    towerNext_decrease fuel (s, h) hfuel

theorem bool_view_pigeonhole (view : Nat → Bool) :
    view 0 = view 1 ∨ view 0 = view 2 ∨ view 1 = view 2 := by
  cases h0 : view 0 <;> cases h1 : view 1 <;> cases h2 : view 2 <;>
    decide

theorem bool_grammar_obstruction (view : Nat → Bool) :
    ∃ x y, x ≠ y ∧ ActiveObstruction (bStage view) x y := by
  rcases bool_view_pigeonhole view with h | h | h
  · exact ⟨0, 1, by omega,
      ⟨by omega, by omega⟩, h, by omega, by omega, by omega⟩
  · exact ⟨0, 2, by omega,
      ⟨by omega, by omega⟩, h, by omega, by omega, by omega⟩
  · exact ⟨1, 2, by omega,
      ⟨by omega, by omega⟩, h, by omega, by omega, by omega⟩

def freshUnguarded : Stage Nat (Nat × Nat) :=
  { mkStage 2 0 with guarded := fun _ _ => False }

theorem cm_freshness :
    ((0 : Nat) ≠ 1) ∧ ZeroRel (mkStage 2 0).obs 0 1 ∧
      ¬ ActiveObstruction freshUnguarded 0 1 :=
  ⟨by decide, by show cview 0 0 = cview 0 1; decide,
   no_guard_no_obstruction _ (fun _ _ h => h) 0 1⟩
```

The book's Lean instantiates the abstract notions on the tower and
makes the two flagged points precise: the countermodel pair is active
once protection is restored, and the driver's run is one step.

```lean
-- Lean (book), textbook/checks/u44_lean.py
theorem kernel_zero_instance : ZeroRel (kernelObs (cview 2)) 2 5 := by
  show min 2 2 = min 5 2
  decide

theorem kernel_apart_instance : ¬ ZeroRel (kernelObs (cview 2)) 1 5 := by
  show ¬ (min 1 2 = min 5 2)
  decide

theorem quotient_instance :
    ObsQuotient.mk (kernelObs (cview 0)) 0 = ObsQuotient.mk (kernelObs (cview 0)) 1 :=
  obsQuotient_eq_of_zero _ (by show min 0 0 = min 1 0; decide)

theorem active_instance : ActiveObstruction (mkStage 2 0) 0 1 :=
  ⟨⟨by omega, by omega⟩, by show min 0 0 = min 1 0; decide, by omega, by omega, by omega⟩

theorem fresh_unguarded_vs_guarded :
    ¬ ActiveObstruction freshUnguarded 0 1 ∧ ActiveObstruction (mkStage 2 0) 0 1 :=
  ⟨cm_freshness.2.2, active_instance⟩

def tagGuarded : Stage Nat (Bool × Bool) :=
  { tagStage with guarded := fun i j => i < 3 ∧ j < 3 ∧ i ≠ j }

theorem tagging_active_when_protected : ActiveObstruction tagGuarded 1 2 :=
  ⟨⟨by omega, by omega⟩, by show tagView 1 = tagView 2; decide, by omega, by omega, by omega⟩

theorem measure_values :
    measureC 3 2 = 0 ∧ measureC 3 1 = 2 ∧ measureC 4 2 = 2 ∧ measureC 4 1 = 6 ∧
    activePairs 4 2 = [(2, 3), (3, 2)] := by
  decide

theorem swapTop_values : swapTop 3 3 = 4 ∧ swapTop 3 4 = 3 ∧ swapTop 3 1 = 1 := by decide

theorem swapTop_off_live : cview 3 (swapTop 3 7) ≠ cview 3 7 := by decide

theorem demand_three : towerDemandList 3 = [(3, 4), (4, 3)] := rfl

theorem closure_kills_instance : ¬ ActiveObstruction (towerClosure 2).apply 2 3 :=
  closure_kills_demanded (towerClosure 2) 2 3 (Or.inl ⟨rfl, rfl⟩)

theorem drive_two_closes : drive towerNext 2 (5, 3) = .closed (5, 4) := rfl

theorem drive_one_starves : drive towerNext 1 (5, 3) = .outOfFuel (5, 4) := rfl

theorem three_values_close :
    ∀ x y : Nat, x ≠ y → ¬ ZeroRel (kernelObs (fun i : Nat => i)) x y :=
  fun _ _ h hz => h hz

theorem bool_instance : ActiveObstruction (bStage (fun i => decide (i = 0))) 1 2 :=
  ⟨⟨by omega, by omega⟩, by show decide (1 = 0) = decide (2 = 0); decide, by omega, by omega, by omega⟩
```

## Line-by-line Lean explanation

**`DiffObs`, `ZeroRel`, `zeroRel_equivalence` (33-48).** The three laws
are fields, so `zeroRel_equivalence` is three projections wrapped in
`Equivalence`'s constructor, with no axiom. `kernelObs` (54-59) builds
the laws from `rfl`, `Eq.symm`, `Eq.trans`; every concrete observer in
the module is a kernel observer, so the laws are proved once. The
book's two instances read `min 2 2 = min 5 2` (zero: horizon 2 caps
both at 2) and `min 1 2 ≠ min 5 2`.

**`obsSetoid`, `ObsQuotient`, `obsQuotient_eq_of_zero` (69-80).** The
`Setoid` is the relation plus the equivalence proof; `Quotient` of it is
the type; `Quotient.sound` is the sound half (zero pair ⇒ equal
classes), which is where `Quot.sound` enters and the only place. The
completeness half (`mk x = mk y ⇒ ZeroRel`) is not in this module; the
ledger says `ObsDescent.obsQuotient_exact` supplies it (Unit 66).

**`Stage`, `ActiveObstruction`, the blocking lemmas (92-122).** Four
independent fields; the conjunction; and three one-line lemmas: no
guarded pairs ⇒ no obstruction (projection to the third conjunct), not
retained ⇒ not active, distinguished ⇒ not active. Each is a lambda on
the anonymous-constructor pattern.

**`BareReflection` (133-150) and the certificate theorem (155-161).**
Fifteen fields. The theorem's proof is a four-tuple: `fresh_from_live_image
parent parent_live` gives `embed parent ≠ fresh`; the pair fields give
the three conjuncts. `retract`, `retract_embed`, `live_embed`,
`zero_preserved`, `retained_embed`, `guarded_embed` are not used by any
theorem of the module; they are the shape the caller asked for, and
the tower instance discharges them. The docstring says "not derived
from freshness alone": correct, and worth more than it sounds, since
the conclusion is literally the hypotheses re-bundled.

**`Refines`, `StageMaps`, `MapSaturated`, `ClosureStep` (166-212).**
Refinement is inclusion of zero-pairs. A `StageMaps` is a list with the
identity and four preservation fields, none of which any theorem here
uses (`MapSaturated` reads only the list). The step has seven fields;
`discharges` carries an `x ≠ y` hypothesis that `demand_offdiag` already
implies.

**The three closure theorems (216-236).** Old distinctions are kept
(contrapositive of refinement); a demanded pair is not active after the
step because `discharges` makes it non-zero; activity after pulls back
to activity before (the new zero-pair was an old one). The docstring
says these are "an ingredient of a decrease proof"; no abstract decrease
is proved, only the concrete one below.

**`ExtensionProposal`, `ClosureOutcome`, `RunResult`, `drive` (244-272).**
Data types and a fuel recursion: zero fuel is `outOfFuel`; otherwise
`next` decides closed, step, or proposal.

**`drive_terminates` (276-293).** Induction on fuel. Zero fuel
contradicts `μ s < 0`. At `f + 1`: if `next s = none`, closed; if a
step, the measure dropped so `μ s' < f`, apply the hypothesis and
rewrite `drive` by `hn`; if a proposal, done.

**The tower (306-491).** `cview h i = min i h`; `mkStage s h` has live
`i < s`, retained on live pairs, guarded on live distinct pairs.
`tower_closed`: at horizon `s − 1` two live points with equal capped
ranks are equal, by `omega` on `min`. `towerReflection n` (335-366)
fills the fifteen fields with the identity embedding, fresh `n + 1`,
parent `n`, and `min n n = min (n + 1) n` as the zero fact;
`tower_obstruction` is the abstract theorem applied to it. `swapTop n`
exchanges `n` and `n + 1` and fixes points below `n`; `swapTop_view` and
`swapTop_live_inj` hold on `x < n + 2` only (the book's
`swapTop_off_live`: at 7 with `n = 3` the value is 0, view 0 against 3).
`towerMaps n` is `[id, swapTop n]` with the preservation proofs by cases
on list membership. `towerDemand n` is the pair both ways;
`towerClosure n` refines to horizon `n + 1` and discharges by `omega`.
`tower_step_composes` is `rfl`: `apply` replaces the observer, and
`mkStage (n + 2) (n + 1)` is that record. `tower_successor_step`
packages the two witnesses pointwise, with the docstring's disclaimer
that no trace object is built.

**The measure (497-560).** `activePairs s h` is the list of ordered
`i ≠ j` below `s` with equal capped rank, built with `flatMap`, `filter`
on `i != j && (min i h == min j h)`, and `map`; `mem_activePairs`
unpacks that (the `Bool` tests through `bne_iff_ne`, `beq_iff_eq`).
`closed_measure_zero` proves the list empty by cases rather than by a
library lemma, because `List.eq_nil_iff_forall_not_mem` carries
`Classical.choice` on this toolchain (the paper's boundary note).
`preclose_measure_pos`: `(n, n + 1)` is a member. The book's
`measure_values` evaluates 0, 2, 2, 6 and the list at `(4, 2)`, with no
axiom at all: pure kernel computation.

**`towerNext`, `towerNext_decrease`, `tower_fuel_terminates` (594-623).**
The driver closes if the list is empty, else steps to `(s, s − 1)`, whose
measure is 0 by `closed_measure_zero`; so the decrease is "positive is
more than zero". The termination instance is the generic theorem
applied. The book's `drive_two_closes` and `drive_one_starves`, both
`rfl`, show the run from `(5, 3)`: one step to `(5, 4)`, then closed; or
out of fuel at `(5, 4)` with fuel 1. The audit's finding: the instance
exercises `drive_terminates` only in its one-step case.

**The Boolean grammar (632-668).** `bool_view_pigeonhole` is eight cases
by `decide` after fixing the three values. `bStage view` has three live
protected points; `bool_grammar_obstruction` turns each pigeonhole case
into the active pair. `no_bool_view_is_closed` is the same statement
proved by naming it: one theorem under two names. `boolProposal` is a
record, built and never applied. The book's `three_values_close`: with
the identity view the kernel is never zero on a distinct pair, so the
three points are closable in a three-valued grammar; the obstruction is
a fact about `Bool`, as the theorem's hypothesis says.

**The countermodels (680-760).** Each stage sets `guarded := fun _ _ =>
False`, and each theorem's last conjunct is
`no_guard_no_obstruction _ (fun _ _ h => h) _ _`: the removal of
protection makes everything inactive, whatever the feature. The content
of each countermodel is its zero conjunct: the stale horizon sees `0`
and `1` alike (freshness); the tag bit is set on both 1 and 2 (tagging);
both endpoints of the edge `(0, 1)` are incident (edge); the constant
observer ignores distinct labels (hash); one token for two occurrences
(repetition). The book's `fresh_unguarded_vs_guarded` puts
`cm_freshness`'s inactive conjunct beside the same pair's activity in
`mkStage 2 0`; `tagging_active_when_protected` restores protection to
the tagging stage and the pair is active. So each countermodel shows an
observer blind to a feature; it shows nothing about the feature under
protection, which is where the derivation's obstructions live.

## What has been proved

- An admitted observer's zero relation is an equivalence; the quotient
  is sound (Genesis, core Lean only).
- A reflection certificate contains an active obstruction; a closure
  step preserves distinctions, discharges its demands, and adds no
  obstruction (Genesis; by projection from the bundles).
- The fuel driver terminates when fuel exceeds a strictly decreasing
  measure (Genesis).
- The tower realizes every piece at every `n`, with the closure applying
  to the next closed stage definitionally; the measure is 0 at closed
  stages and positive before closure; the driver terminates (Genesis).
- No Boolean view closes three protected points (Genesis); a
  three-valued view does (book).
- Five features are invisible to a suitable observer (Genesis); each is
  an active obstruction once the stage is protected (book, two of them).

## What has not been proved

- An abstract decrease theorem: `closure_kills_demanded` and
  `closure_adds_no_obstruction` are ingredients; finiteness and a
  removed pair are proved only for the tower's measure.
- The completeness half of the quotient (deferred to `ObsDescent`).
- Anything about processing a proposal: the package stops at the data.
- Anything about maps outside the live region.
- Non-trivial termination: the tower run is one step, so
  `tower_fuel_terminates` needs fuel 2 at most.
- That any feature is inert under protection: the countermodels are
  unprotected by construction, and the book shows the pairs active when
  protected.
- Unrestricted G1 (the capacity theorem behind the Boolean obstruction
  is Unit 43's class-relative result).

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `X X' R V : Type`, `view : X → V`, `μ : σ → Nat` | the abstract interface | metatheory; declared bundles; the finitude rule flags the arbitrary function types |
| `Setoid`, `Quotient`, `Quotient.sound` | the optional quotient | metatheory; `Quot.sound` only here |
| `Nat`, `min` | the tower | metatheory; the chain of Unit 40 in another dress (ranks, not edges) |
| `Bool` | the grammar | metatheory; the grammar is declared |
| `List.flatMap/filter/map`, `omega`, `decide` | computation and arithmetic | metatheory |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The discipline: three separate conditions,
equivalence before quotient, demands as predicates so that closure
chooses no representative, proposals as data. These are the shape of
Unit 29's closure policy made into types. The module imports nothing
from Genesis and names no consumer; the adapter from these types to the
derivation's own is, by the module's own statement, the caller's
evidence and out of scope.

**Phrases to read with care.**

- "The certificate contains an active obstruction": the certificate's
  fields are the obstruction; the theorem re-bundles them.
- "Finite fuel ⇒ termination, instantiated by the tower": one step,
  every time.
- "Each feature does not by itself produce observer-visible
  difference": for the observer chosen; and "not an active obstruction"
  because nothing is protected.
- "No Boolean view closes the family": a fact about two values and three
  points; the proposal that follows is available data, and no theorem
  selects it.

## Student exercise

Write down the stage `(s, h) = (5, 2)`: its live points, its active
pairs, its measure. Say what `towerNext` does to it, what the measure
is afterwards, and how much fuel `drive` needs to report `closed`.
Then say why `drive_terminates` promises `closed` with fuel `measure + 1`
and whether that promise is sharp here.

## Answer

Live points `0..4`. Under horizon 2 the capped ranks are `0, 1, 2, 2,
2`, so the active pairs are the ordered pairs among `{2, 3, 4}`: six of
them, measure 6. `towerNext (5, 2)` returns the step to `(5, 4)`, whose
measure is 0 (`closed_measure_zero`), and the next call returns `none`.
Fuel 2 reports `closed (5, 4)`; fuel 1 reports `outOfFuel (5, 4)` after
taking the step. `drive_terminates` promises `closed` or `proposal` with
any fuel above the measure, here 7, because each step lowers the measure
by at least one and the measure cannot go below 0; the promise is not
sharp for the tower, where one step always suffices, because the driver
jumps straight to the closed horizon rather than discharging one pair
at a time.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/DiffInterface.lean` lines 33-82 (observers, quotient), 92-122 (stages, blocking), 133-161 (certificate), 166-236 (refinement, maps, closure), 244-293 (proposals, driver), 306-491 (tower), 497-623 (measure, concrete driver), 632-668 (Boolean grammar), 680-760 (countermodels) |
| Axiom report | `artifacts/lean_axioms.txt` lines 176-210: 17 none, `obsQuotient_eq_of_zero` `Quot.sound`, `tower_demand_characterized` `propext`, 16 `{propext, Quot.sound}` |
| Paper | `paper/difference_interface.md` (DELIVERED table, the concrete realization, the grammar, the countermodels, boundary statements, open extensions); `paper/paper_claim_ledger.md` `CL-DI-EQUIVALENCE`, `CL-DI-OBSTRUCTION`, `CL-DI-REFLECTION`, `CL-DI-CLOSURE`, `CL-DI-PROPOSAL`, `CL-DI-TERMINATION`, `CL-DI-COUNTERMODELS`, `CL-DI-BOUNDARIES` |
| Python | `code/derivation/diff_interface.py`, `artifacts/diff_interface.json`, `tests/test_diff_interface.py` |
| Check (Python) | `python textbook/checks/u44_diff_interface.py`: 15 tower rounds against the artifact; active pairs and the swap off the live region; the one-step driver; eight Boolean views; the countermodels with the "protected" column; a three-valued view |
| Check (book Lean) | `python textbook/checks/u44_lean.py`: fifteen book declarations plus eleven Genesis theorems kernel-checked, Lean 4.33.0 |
| Interface and reading-guide check | `python textbook/checks/u44_observer_spec_lean.py`: an arbitrary-proposition observer, explicit decider transfer, the finite lookup example, a generic `closed` result with an active pair, and an idle empty-demand step |
