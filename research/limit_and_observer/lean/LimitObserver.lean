/-
`research/limit_and_observer` — the theorem-level claims of this rung.

Core Lean 4 only.  No Mathlib, no import of the sealed `Derivation` package.
Every object below is this rung's own; sealed results are cited in the prose
by pinned path and are never imported, so nothing here inherits a sealed
proof by accident.

Scope, stated once and meant: this file proves

  * the refinement obstruction, for any block count that rises strictly along
    the chain and is bounded by the carrier (`chain_bounded`), with a witness
    that those hypotheses are satisfiable (`chain_bound_has_an_instance`);
  * the growth obstruction for growth by uninstantiated data, with an
    explicit witness and no counting (`fresh_data_are_never_separated`,
    `growth_defeats_every_reader`);
  * that a novel family verdict forces a constant verdict sequence, in full
    generality (`novel_forces_constant`), which is what makes the
    family-verdict demand unsatisfiable for a stage-local reader;
  * the shape of the sealed relation and the existence of a rival, as
    decidable identities on the bit pair.

What it does NOT prove, and the prose says so in the same breath: the sharper
growth threshold `2 ^ w`, which needs a pigeonhole over signatures.  That is
checked exhaustively in Python at every width up to the declared bound and is
recorded as an OPEN Lean obligation, not as a theorem.
-/

namespace LimitObserver

/-! ## The two derivability bits, and the sealed relation -/

/-- The sealed relation: coverage ∨ admission.  A transcription of
`code/derivation/observe.py` line 52, pinned in `SOURCE_MANIFEST.json`.  (An
earlier version of this line said 56, which is `profile`; the quoted body was
always right and only the anchor was wrong.) -/
def sealedDerivable (coverage admission : Bool) : Bool :=
  coverage || admission

/-- The reading that declines the conflation: the admission bit alone. -/
def admissionOnly (_coverage admission : Bool) : Bool := admission

/-- Whether a reading separates two data at one context: its value differs. -/
def separatesAt (b : Bool → Bool → Bool) (coverage bi bj : Bool) : Bool :=
  b coverage bi != b coverage bj

/-- **The conflation, stated exactly.**  Where the uniform rule covers the
form, the sealed relation reads true for every datum, so it separates nothing
there, however the admission bits differ. -/
theorem sealed_is_blind_where_covered (bi bj : Bool) :
    separatesAt sealedDerivable true bi bj = false := by
  cases bi <;> cases bj <;> rfl

/-- Where coverage is absent the sealed relation reads the admission bit, so
it separates exactly when the admission bits differ. -/
theorem sealed_reads_admission_where_uncovered (bi bj : Bool) :
    separatesAt sealedDerivable false bi bj = (bi != bj) := by
  cases bi <;> cases bj <;> rfl

/-- **The rival exists.**  At a covered context with differing admission bits
the sealed relation identifies the pair and the admission reading separates
it.  A decidable exhibit, not an argument. -/
theorem rival_separates_where_sealed_identifies :
    separatesAt sealedDerivable true true false = false ∧
    separatesAt admissionOnly true true false = true := by
  exact ⟨rfl, rfl⟩

/-- The admission reading agrees with the sealed one wherever coverage is
absent, so the rival is not a wholesale replacement: it differs exactly on
the covered contexts. -/
theorem rival_agrees_where_uncovered (bi bj : Bool) :
    separatesAt admissionOnly false bi bj = separatesAt sealedDerivable false bi bj := by
  cases bi <;> cases bj <;> rfl

/-! ## Refinement without end is obstructed at the carrier

A lawful reader's induced partition of the admitted data has at least one
block and at most `n` blocks, and along a chain of strict splits every step
raises the block count.  A chain of `m` strict splits therefore needs `m + 1`
distinct block counts inside `[1, n]`, so `m < n`.  Nothing about readers
enters the proof: it is a statement about any block count that rises strictly
along the chain and is bounded by the carrier, which is why it survives every
choice of reading and aggregation.

**The strictness hypothesis is bounded by the chain, and that bound is a
repair.**  The first version of this section quantified strictness over EVERY
index — `∀ k, g k < g (k + 1)` — while also bounding `g` by the carrier at
every index.  Those two hypotheses are jointly unsatisfiable, because a
strictly increasing sequence of naturals leaves every bound, so every theorem
below was vacuous: the chain length `m` occurred in no hypothesis and the
conclusion followed from the contradiction rather than from the chain.  That
version is **WITHDRAWN**.  Strictness is now asked only below `m` and
boundedness only up to `m`, which is what a finite chain actually supplies,
and `chain_bound_has_an_instance` exhibits an `(n, m, g)` meeting all three so
the hypotheses cannot quietly become unsatisfiable again. -/

/-- A sequence rising strictly at every step below `m` rises at least as fast
as its index up to `m`. -/
theorem strict_ge (g : Nat → Nat) :
    ∀ m, (∀ k, k < m → g k < g (k + 1)) → g 0 + m ≤ g m := by
  intro m
  induction m with
  | zero => intro _; omega
  | succ n ih =>
      intro h
      have hn : g n < g (n + 1) := h n (by omega)
      have h0 : g 0 + n ≤ g n := ih (fun k hk => h k (by omega))
      omega

/-- **The refinement obstruction.**  If the block count starts at least at
one, never exceeds the carrier `n` along the chain, and rises strictly at
every step of the chain, then a chain of `m` strict splits has `m < n`.  In
particular no chain is longer than the carrier, so the demand `m > n` is met
by nothing. -/
theorem chain_bounded (n m : Nat) (g : Nat → Nat)
    (hpos : 1 ≤ g 0) (hle : ∀ k, k ≤ m → g k ≤ n)
    (hstrict : ∀ k, k < m → g k < g (k + 1)) : m < n := by
  have h1 : g 0 + m ≤ g m := strict_ge g m hstrict
  have h2 : g m ≤ n := hle m (Nat.le_refl m)
  omega

/-- The block count of a chain of strict splits at a carrier of three: one
block before any split, then two, then three. -/
def blockCount (k : Nat) : Nat := k + 1

/-- **The hypotheses are satisfiable**, exhibited rather than argued.  At a
carrier of three, a chain of two strict splits with block count `k + 1` meets
all three hypotheses of `chain_bounded` at once.  This exhibit exists because
the first version of the bound had no instance at all and nothing detected
it: an axiom report says only which axioms a proof used, never whether its
hypotheses can be met. -/
theorem chain_bound_has_an_instance :
    1 ≤ blockCount 0
    ∧ (∀ k, k ≤ 2 → blockCount k ≤ 3)
    ∧ (∀ k, k < 2 → blockCount k < blockCount (k + 1)) := by
  refine ⟨?_, ?_, ?_⟩
  · unfold blockCount; omega
  · intro k hk; unfold blockCount; omega
  · intro k _; unfold blockCount; omega

-- The exhibit really is an instance: this application elaborates only if
-- every hypothesis of `chain_bounded` is met by it.  It is an `example` and
-- so carries no name into the axiom census.
example : 2 < 3 :=
  chain_bounded 3 2 blockCount
    chain_bound_has_an_instance.1
    chain_bound_has_an_instance.2.1
    chain_bound_has_an_instance.2.2

/-- The demand asks for a chain strictly longer than the carrier.  No such
chain exists, at any state, for any lawful reader. -/
theorem refinement_demand_unsatisfiable (n m : Nat) (g : Nat → Nat)
    (hpos : 1 ≤ g 0) (hle : ∀ k, k ≤ m → g k ≤ n)
    (hstrict : ∀ k, k < m → g k < g (k + 1)) : ¬ (n < m) := by
  have := chain_bounded n m g hpos hle hstrict
  omega

/-- **Growth does not lift it.**  Admitting data raises the carrier and the
ceiling together, so the bound holds at every carrier reached by any finite
number of growth items.  This is why no finite delta over the declared
alphabet lifts the refinement obstruction. -/
theorem refinement_obstruction_survives_growth (n extra m : Nat)
    (g : Nat → Nat)
    (hpos : 1 ≤ g 0) (hle : ∀ k, k ≤ m → g k ≤ n + extra)
    (hstrict : ∀ k, k < m → g k < g (k + 1)) : ¬ (n + extra < m) := by
  have := chain_bounded (n + extra) m g hpos hle hstrict
  omega

/-! ## Growth without end defeats a fixed selection

A datum admitted by a growth item and mentioned by no instance has a false
admission bit at every context, so any two such data have equal signatures.
Equal signatures give a separating count of zero, and `a 0 = false` for every
admitted aggregation, so the pair is not separated — by any reader, of any
width, under any reading and any lawful aggregation.

This is the growth obstruction with an explicit witness and no counting.  The
sharper threshold `2 ^ w`, which holds even when growth carries content, is
checked in Python and recorded OPEN here. -/

/-- A reader's signature of one datum over a selection, as a list. -/
def signature (reads : Nat → Bool) (admission : Nat → Nat → Bool)
    (d : Nat) : List Nat → List Bool
  | [] => []
  | c :: cs => (reads c && admission c d) :: signature reads admission d cs

/-- The separating count: positions at which two signatures differ. -/
def diffCount : List Bool → List Bool → Nat
  | [], _ => 0
  | _, [] => 0
  | x :: xs, y :: ys => (if x == y then 0 else 1) + diffCount xs ys

/-- Equal signatures give a separating count of zero. -/
theorem diffCount_self (s : List Bool) : diffCount s s = 0 := by
  induction s with
  | nil => rfl
  | cons x xs ih =>
      simp [diffCount, ih]

/-- **Fresh data are never separated.**  Two data whose admission bit is
false at every context of the selection have equal signatures, hence a
separating count of zero, hence no separation under any aggregation with
`a 0 = false`. -/
theorem fresh_data_are_never_separated
    (reads : Nat → Bool) (admission : Nat → Nat → Bool) (i j : Nat)
    (K : List Nat)
    (hi : ∀ c, admission c i = false) (hj : ∀ c, admission c j = false)
    (a : Nat → Bool) (ha : a 0 = false) :
    a (diffCount (signature reads admission i K)
                 (signature reads admission j K)) = false := by
  have h : signature reads admission i K = signature reads admission j K := by
    induction K with
    | nil => rfl
    | cons c cs ih =>
        simp [signature, hi c, hj c, ih]
  rw [h, diffCount_self, ha]

/-- **The growth obstruction, with its witness.**  Once two data admitted by
growth items carry no instance, every reader identifies them, so no
fixed-selection reader separates every pair of the grown carrier. -/
theorem growth_defeats_every_reader
    (reads : Nat → Bool) (admission : Nat → Nat → Bool) (i j : Nat)
    (K : List Nat)
    (hi : ∀ c, admission c i = false) (hj : ∀ c, admission c j = false)
    (a : Nat → Bool) (ha : a 0 = false) :
    ¬ (a (diffCount (signature reads admission i K)
                    (signature reads admission j K)) = true) := by
  rw [fresh_data_are_never_separated reads admission i j K hi hj a ha]
  intro h
  exact Bool.noConfusion h

/-! ## The family-determined verdict

A verdict is a `Bool`.  A family verdict that is *novel* differs from every
stage verdict.  A two-valued verdict cannot differ from every member of a
sequence containing both values, so novelty forces the sequence to be
constant — and a stage-local reader's family verdict, being one of the stage
verdicts, is then not novel.

The implication that stage-local readers agreeing at every stage have equal
family verdicts is true by unfolding and is reported as definition-level.  The
content is the exhaustiveness check over the item alphabet, which lives in
Python because it is a property of the enumeration, not of `Bool`. -/

/-- Novelty: the family verdict differs from every stage verdict. -/
def novel (f : Bool) (vs : List Bool) : Prop := ∀ v ∈ vs, f ≠ v

/-- **Novelty forces a constant sequence.**  Every stage verdict equals the
negation of the family verdict. -/
theorem novel_forces_constant (f : Bool) (vs : List Bool) (h : novel f vs) :
    ∀ v ∈ vs, v = !f := by
  intro v hv
  have : f ≠ v := h v hv
  cases f <;> cases v <;> simp_all

/-- A sequence carrying both verdicts admits no novel family verdict. -/
theorem no_novel_verdict_on_a_mixed_sequence (f : Bool) (vs : List Bool)
    (ht : true ∈ vs) (hf : false ∈ vs) : ¬ novel f vs := by
  intro h
  have h1 : true = !f := novel_forces_constant f vs h true ht
  have h2 : false = !f := novel_forces_constant f vs h false hf
  exact Bool.noConfusion (h1.trans h2.symm)

/-- A stage-local reader's verdict at a stage is one of the stage verdicts,
so it is not novel whenever the sequence is non-empty. -/
theorem stage_local_verdict_is_not_novel (vs : List Bool)
    (v : Bool) (hv : v ∈ vs) : ¬ novel v vs := by
  intro h
  exact (h v hv) rfl

/-! ## The reading axis is complete and small

The sixteen readings of the bit pair collapse to exactly four
induced-separation behaviours, because at a fixed context the coverage bit is
constant across data.  Both halves below are decided, not argued. -/

/-- Whether a reading varies with the admission bit at a given coverage. -/
def readsAt (b : Bool → Bool → Bool) (coverage : Bool) : Bool :=
  b coverage false != b coverage true

/-- The behaviour of a reading: whether it reads where coverage is absent,
and whether it reads where coverage is present. -/
def behaviour (b : Bool → Bool → Bool) : Bool × Bool :=
  (readsAt b false, readsAt b true)

/-- The sealed relation reads admission only where coverage is absent. -/
theorem sealed_behaviour : behaviour sealedDerivable = (true, false) := rfl

/-- The rival reads admission everywhere, including where coverage is
present.  It is the sealed behaviour's exact complement on the covered
half. -/
theorem admission_only_behaviour : behaviour admissionOnly = (true, true) := rfl

/-- Separation at a context factors through `readsAt`: a reading separates
there exactly when it reads there and the admission bits differ. -/
theorem separatesAt_eq_readsAt (b : Bool → Bool → Bool)
    (coverage bi bj : Bool) :
    separatesAt b coverage bi bj = (readsAt b coverage && (bi != bj)) := by
  unfold separatesAt readsAt
  cases bi <;> cases bj <;>
    cases hbf : b coverage false <;> cases hbt : b coverage true <;>
    simp [hbf, hbt]

/-- The behaviour determines separation at a context: two readings sharing a
behaviour separate the same pairs, everywhere. This relation statement does
not identify their reading classes under the full-reader transport. -/
theorem behaviour_determines_separation
    (b b' : Bool → Bool → Bool) (h : behaviour b = behaviour b')
    (coverage bi bj : Bool) :
    separatesAt b coverage bi bj = separatesAt b' coverage bi bj := by
  have h0 : readsAt b false = readsAt b' false := congrArg Prod.fst h
  have h1 : readsAt b true = readsAt b' true := congrArg Prod.snd h
  rw [separatesAt_eq_readsAt, separatesAt_eq_readsAt]
  cases coverage
  · rw [h0]
  · rw [h1]

end LimitObserver
