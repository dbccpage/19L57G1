import SecondNoFirst.Stake

/-!
# Stage two: no demand without a stake

Every theorem in this file is about ONE grammar: the sealed grammar
reconstructed in `Kernel.lean`, extended by a declared two-sided stake as
defined in `Stake.lean`.  It is about no other grammar, and each statement
carries that scope in its own sentence.  Nothing here is a claim about
grammars in general, and nothing here treats the sealed estate's standing
obstruction as anything other than standing.

AuthorityEffect: None.
-/

namespace SecondNoFirst
namespace NoFirst

open SecondNoFirst.Sealed
open SecondNoFirst.Stake

/-! ## 1. A supply changes no demand -/

/-- **supplies_preserve_regime.**  In the sealed grammar reconstructed
here, replaying any sequence made only of supplies returns the regime
unchanged.  The single-step case is the sealed `supply_no_op`, cited as
the sealed theorem it is; the sequence case is this rung's induction. -/
theorem supplies_preserve_regime (r : Regime) (ts : List Nat) :
    replayE (ts.map Event.supply) r = some r := by
  unfold replayE
  induction ts generalizing r with
  | nil => rfl
  | cons t rest ih =>
      show (List.map Event.supply (t :: rest)).foldlM stepE r = some r
      simp only [List.map_cons, List.foldlM]
      rw [supply_no_op r t]
      exact ih r

/-- **supply_preserves_demands.**  In the sealed grammar reconstructed
here, extended by a declared two-sided stake, the demands after a supply
are the demands before it, for every stake and every pair.  The content is
carried by the sealed `supply_no_op`; what this theorem adds is the
transport of that fact through the demand predicate, which is one
substitution. -/
theorem supply_preserves_demands (S : Stake) (r r' : Regime) (t : Nat)
    (h : stepE r (.supply t) = some r') (i j : Nat) :
    Demand S r' i j ↔ Demand S r i j := by
  rw [supply_no_op r t] at h
  rw [Option.some.inj h]

/-- The same fact over a whole sequence of supplies. -/
theorem supplies_preserve_demands (S : Stake) (r r' : Regime) (ts : List Nat)
    (h : replayE (ts.map Event.supply) r = some r') (i j : Nat) :
    Demand S r' i j ↔ Demand S r i j := by
  rw [supplies_preserve_regime r ts] at h
  rw [Option.some.inj h]

/-! ## 2. A demand needs a label -/

/-- **demand_needs_label.**  In the sealed grammar reconstructed here,
extended by a declared two-sided stake, a pair that is a demand at a
regime is a pair the stake labels apart or labels same.
AT THE LEVEL OF A DEFINITION: `Demand` carries the labelling condition as
a conjunct, and the three-way case split on the label is immediate. -/
theorem demand_needs_label (S : Stake) (r : Regime) (i j : Nat)
    (h : Demand S r i j) :
    S.label i j = Label.apart ∨ S.label i j = Label.same :=
  labelled_cases _ h.2.2.1

/-- **demand_depends_only_on_the_label.**  In the sealed grammar
reconstructed here, extended by a declared two-sided stake, whether a pair
is a demand at a regime depends on the stake only through the label the
declaration gives that pair.  Two stakes that agree at a pair agree on
whether that pair is a demand, at every regime; so a label has one source,
and that source is the declaration. -/
theorem demand_depends_only_on_the_label (S S' : Stake) (r : Regime)
    (i j : Nat) (h : S.label i j = S'.label i j) :
    Demand S r i j ↔ Demand S' r i j := by
  unfold Demand
  rw [h]

/-! ## 3. The grammar carries no stake -/

/-- A total code for the reconstructed event type: every event is
determined by a kind index and a list of natural numbers.  Written to make
the field types of the six constructors explicit. -/
def eventCode : Event → Nat × List Nat
  | .supply t => (0, [t])
  | .admitDatum => (1, [])
  | .admitForm a => (2, [a])
  | .admitInst f args => (3, f :: args)
  | .admitRuleAll f => (4, [f])
  | .impose i j => (5, [i, j])

/-- **grammar_carries_no_stake.**  In the sealed grammar reconstructed
here, every event is one of exactly six kinds; the kind code above is
total, bounded by six, and injective.

WHAT THIS THEOREM PROVES AND WHAT IT DOES NOT.  It proves the three
displayed conjuncts and nothing else.  It does NOT prove, and cannot
state, that no constructor carries a field of stake type: that is a fact
about the SIGNATURE of the reconstructed `Event` type and of `stepE`,
which reads `Regime -> Event -> Option Regime` and mentions no stake at
all.  A signature fact is checked by the compiler accepting the
declaration, not by a proposition; it is recorded in the ledger as
metatheory read off the type, and the name of this theorem is wider than
its statement.  An adversarial reading before this package was committed
made exactly that objection, and the response was to narrow the doc
comment rather than to widen the claim.

Everything here is about the RECONSTRUCTED event type and about nothing
else.  That the reconstruction is faithful to the sealed type is the pin's
business, and a pin proves only that the sealed source did not move. -/
theorem grammar_carries_no_stake :
    (∀ e : Event,
        (∃ t, e = .supply t) ∨ e = .admitDatum ∨ (∃ a, e = .admitForm a) ∨
        (∃ f args, e = .admitInst f args) ∨ (∃ f, e = .admitRuleAll f) ∨
        (∃ i j, e = .impose i j))
    ∧ (∀ e : Event, (eventCode e).1 < 6)
    ∧ (∀ e e' : Event, eventCode e = eventCode e' → e = e') := by
  refine ⟨?_, ?_, ?_⟩
  · intro e
    cases e with
    | supply t => exact Or.inl ⟨t, rfl⟩
    | admitDatum => exact Or.inr (Or.inl rfl)
    | admitForm a => exact Or.inr (Or.inr (Or.inl ⟨a, rfl⟩))
    | admitInst f args => exact Or.inr (Or.inr (Or.inr (Or.inl ⟨f, args, rfl⟩)))
    | admitRuleAll f =>
        exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨f, rfl⟩))))
    | impose i j =>
        exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr ⟨i, j, rfl⟩))))
  · intro e
    cases e with
    | supply t => exact (by decide : (0 : Nat) < 6)
    | admitDatum => exact (by decide : (1 : Nat) < 6)
    | admitForm a => exact (by decide : (2 : Nat) < 6)
    | admitInst f args => exact (by decide : (3 : Nat) < 6)
    | admitRuleAll f => exact (by decide : (4 : Nat) < 6)
    | impose i j => exact (by decide : (5 : Nat) < 6)
  · intro e e' h
    cases e <;> cases e' <;> simp_all [eventCode]

/-! ## 4. The conjunction -/

/-- **`no_first_demand` (the frozen target name).**  In the sealed grammar reconstructed in
`Kernel.lean`, extended by a declared two-sided stake as defined in
`Stake.lean`, and in no other grammar:

1. a demand at a regime is at a pair the declared stake labels apart or
   labels same;
2. whether a pair is a demand depends on the stake only through the label
   the declaration gives that pair;
3. every event of the grammar is one of the six recorded kinds;
4. a supply changes no regime, hence no demand;
5. under the stake that labels every pair free there is no demand at any
   regime whatever, reachable or not.

SCOPE OF THE STATEMENT.  These clauses say that the constraint LABEL has
one source, the stake declaration.  They do not say when the `Demand`
predicate first becomes true and they do not prove that the declaration is
the only trigger of a demand's first occurrence.  Datum, instance, and
uniform-rule admissions can change demand sets.  The arbitrary-run index is
therefore OPEN, as the ledger records; only inert runs receive a temporal
theorem in `Run.lean`.  The scope excludes every other grammar. -/
theorem no_first_demand :
    (∀ (S : Stake) (r : Regime) (i j : Nat), Demand S r i j →
        S.label i j = Label.apart ∨ S.label i j = Label.same)
  ∧ (∀ (S S' : Stake) (r : Regime) (i j : Nat),
        S.label i j = S'.label i j → (Demand S r i j ↔ Demand S' r i j))
  ∧ (∀ e : Event,
        (∃ t, e = .supply t) ∨ e = .admitDatum ∨ (∃ a, e = .admitForm a) ∨
        (∃ f args, e = .admitInst f args) ∨ (∃ f, e = .admitRuleAll f) ∨
        (∃ i j, e = .impose i j))
  ∧ (∀ (S : Stake) (r r' : Regime) (t i j : Nat),
        stepE r (.supply t) = some r' → (Demand S r' i j ↔ Demand S r i j))
  ∧ (∀ (r : Regime) (i j : Nat), ¬ Demand freeStake r i j) :=
  ⟨fun S r i j h => demand_needs_label S r i j h,
   fun S S' r i j h => demand_depends_only_on_the_label S S' r i j h,
   grammar_carries_no_stake.1,
   fun S r r' t i j h => supply_preserves_demands S r r' t h i j,
   fun r i j => free_stake_no_demand r i j⟩

/-! ## 5. What the demand set is, where the grammar has not yet built one -/

/-- Collapse rules out separability, constructively. -/
theorem collapsed_not_separable {r : Regime} {d d' : Nat}
    (h : collapsed r d d') : ¬ separable r d d' :=
  fun ⟨c, hw, hne⟩ => hne (h c hw)

/-- Failing to separate is being collapsed: derivability is decidable, so
the double negation is eliminated without any choice. -/
theorem collapsed_of_not_separable {r : Regime} {d d' : Nat}
    (h : ¬ separable r d d') : collapsed r d d' := by
  intro c hw
  by_cases hd : (derivable r (plug c d) ↔ derivable r (plug c d'))
  · exact hd
  · exact absurd ⟨c, hw, hd⟩ h

/-- **apart_demand_of_no_forms.**  In the sealed grammar reconstructed
here, extended by a declared two-sided stake: at a regime with no admitted
form there is no well-formed context, so no pair is separable, and every
held pair the stake labels apart is a demand. -/
theorem apart_demand_of_no_forms (S : Stake) (r : Regime) (hf : r.forms = [])
    (i j : Nat) (hij : i < j) (hj : j < r.data)
    (hlab : S.label i j = Label.apart) : Demand S r i j := by
  refine ⟨hij, hj, by rw [hlab]; rfl, ?_⟩
  rw [hlab]
  intro ⟨c, hw, _⟩
  have := hw.1
  rw [hf] at this
  exact absurd this (by simp)

/-- **demand_iff_apart_of_no_insts.**  In the sealed grammar reconstructed
here, extended by a declared two-sided stake: at a regime with no admitted
instance, a held pair is a demand exactly when the stake labels it apart.
The forward direction rules out the same label, because with no instance
every pair is collapsed and a same label is therefore honoured; the
backward direction uses the same collapse to defeat separability. -/
theorem demand_iff_apart_of_no_insts (S : Stake) (r : Regime)
    (hi : r.insts = []) (i j : Nat) (hij : i < j) (hj : j < r.data) :
    Demand S r i j ↔ S.label i j = Label.apart := by
  constructor
  · intro h
    rcases demand_needs_label S r i j h with hap | hsm
    · exact hap
    · exfalso
      have hno := h.2.2.2
      rw [hsm] at hno
      exact hno (collapsed_of_no_insts r hi i j)
  · intro hlab
    refine ⟨hij, hj, by rw [hlab]; rfl, ?_⟩
    rw [hlab]
    exact collapsed_not_separable (collapsed_of_no_insts r hi i j)

end NoFirst
end SecondNoFirst
