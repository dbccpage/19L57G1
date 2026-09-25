import SecondClass.Kernel
import SecondClass.IsoKernel
import SecondClass.Rounds
import SecondClass.Count

/-!
# Neither hypothesis can be dropped, and the base matters

Native to rung eight.  Every theorem here is a countermodel, closed by
kernel computation on concrete regimes and concrete maps: each is at the
level of a definition and is never counted as content.

For each of the three lists the sealed isomorphism carries as membership
-- instances, uniform rules, requirements -- two regimes the structure
relates, with different lengths of that list:

* `*_need_nodup`: both well formed, and the target duplicate-free; the
  source holds one entry twice.
* `*_need_wf`: both duplicate-free, and the target well formed; the
  source holds an entry naming an index outside its admitted range (an
  instance or a rule), or a requirement in the wrong order, which the
  maps carry onto an entry the target already has.

So for none of the three is either hypothesis of `Count.insts_le`,
`Count.rules_le` or `Count.reqs_le` idle.

`counts_not_of_class`: the empty history from the sealed reading regime
L, and a datum, a datum and the requirement between them from the sealed
empty regime, reach one regime with CHANGING counts zero and three; so
across two bases the class, and even the regime, does not carry the
count.

AuthorityEffect: None.
-/

namespace SecondClass
namespace Counter

open Sealed
open Rounds (changes)
open Count (Dupfree)

/-- A regime holding one instance twice, and the regime holding it once. -/
def instTwice : Regime := ⟨1, [1], [(0, [0]), (0, [0])], [], []⟩
def instOnce : Regime := ⟨1, [1], [(0, [0])], [], []⟩
/-- An instance naming a datum index outside the admitted range. -/
def instOutside : Regime := ⟨1, [1], [(0, [0]), (0, [5])], [], []⟩

def ruleTwice : Regime := ⟨0, [1], [], [0, 0], []⟩
def ruleOnce : Regime := ⟨0, [1], [], [0], []⟩
/-- A uniform rule naming a form index outside the admitted range. -/
def ruleOutside : Regime := ⟨0, [1], [], [0, 5], []⟩

def reqTwice : Regime := ⟨2, [], [], [], [(0, 1), (0, 1)]⟩
def reqOnce : Regime := ⟨2, [], [], [], [(0, 1)]⟩
/-- A requirement written in the wrong order. -/
def reqReversed : Regime := ⟨2, [], [], [], [(0, 1), (1, 0)]⟩

/-- Every map is the identity. -/
def idIso (r s : Regime)
    (dmap_lt : ∀ d ∈ List.range r.data, id d < s.data)
    (dinv_lt : ∀ d ∈ List.range s.data, id d < r.data)
    (fmap_lt : ∀ f ∈ List.range r.forms.length, id f < s.forms.length)
    (finv_lt : ∀ f ∈ List.range s.forms.length, id f < r.forms.length)
    (arity : ∀ f ∈ List.range r.forms.length,
      s.forms.getD (id f) 0 = r.forms.getD f 0)
    (insts_fwd : ∀ p ∈ r.insts, (id p.1, p.2.map id) ∈ s.insts)
    (insts_bwd : ∀ p ∈ s.insts, (id p.1, p.2.map id) ∈ r.insts)
    (rules_fwd : ∀ f ∈ r.rules, id f ∈ s.rules)
    (rules_bwd : ∀ f ∈ s.rules, id f ∈ r.rules)
    (reqs_fwd : ∀ q ∈ r.reqs, sortPair (id q.1, id q.2) ∈ s.reqs)
    (reqs_bwd : ∀ q ∈ s.reqs, sortPair (id q.1, id q.2) ∈ r.reqs) :
    Iso r s :=
  ⟨id, id, id, id, dmap_lt, dinv_lt, fun _ _ => rfl, fun _ _ => rfl,
    fmap_lt, finv_lt, fun _ _ => rfl, fun _ _ => rfl, arity,
    insts_fwd, insts_bwd, rules_fwd, rules_bwd, reqs_fwd, reqs_bwd⟩

theorem insts_need_nodup :
    ∃ r s : Regime, r.wf ∧ s.wf ∧ Dupfree s ∧ Nonempty (Iso r s) ∧
      r.insts.length ≠ s.insts.length :=
  ⟨instTwice, instOnce,
    by refine ⟨?_, ?_, ?_, ?_⟩ <;> decide,
    by refine ⟨?_, ?_, ?_, ?_⟩ <;> decide,
    by refine ⟨?_, ?_, ?_⟩ <;> decide,
    ⟨idIso _ _ (by decide) (by decide) (by decide) (by decide) (by decide)
      (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)⟩,
    by decide⟩

theorem insts_need_wf :
    ∃ r s : Regime, Dupfree r ∧ Dupfree s ∧ s.wf ∧ Nonempty (Iso r s) ∧
      r.insts.length ≠ s.insts.length :=
  ⟨instOutside, instOnce,
    by refine ⟨?_, ?_, ?_⟩ <;> decide,
    by refine ⟨?_, ?_, ?_⟩ <;> decide,
    by refine ⟨?_, ?_, ?_, ?_⟩ <;> decide,
    ⟨⟨fun _ => 0, id, id, id, by decide, by decide, by decide, by decide,
      by decide, by decide, by decide, by decide, by decide, by decide,
      by decide, by decide, by decide, by decide, by decide⟩⟩,
    by decide⟩

theorem rules_need_nodup :
    ∃ r s : Regime, r.wf ∧ s.wf ∧ Dupfree s ∧ Nonempty (Iso r s) ∧
      r.rules.length ≠ s.rules.length :=
  ⟨ruleTwice, ruleOnce,
    by refine ⟨?_, ?_, ?_, ?_⟩ <;> decide,
    by refine ⟨?_, ?_, ?_, ?_⟩ <;> decide,
    by refine ⟨?_, ?_, ?_⟩ <;> decide,
    ⟨idIso _ _ (by decide) (by decide) (by decide) (by decide) (by decide)
      (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)⟩,
    by decide⟩

theorem rules_need_wf :
    ∃ r s : Regime, Dupfree r ∧ Dupfree s ∧ s.wf ∧ Nonempty (Iso r s) ∧
      r.rules.length ≠ s.rules.length :=
  ⟨ruleOutside, ruleOnce,
    by refine ⟨?_, ?_, ?_⟩ <;> decide,
    by refine ⟨?_, ?_, ?_⟩ <;> decide,
    by refine ⟨?_, ?_, ?_, ?_⟩ <;> decide,
    ⟨⟨id, id, fun _ => 0, id, by decide, by decide, by decide, by decide,
      by decide, by decide, by decide, by decide, by decide, by decide,
      by decide, by decide, by decide, by decide, by decide⟩⟩,
    by decide⟩

theorem reqs_need_nodup :
    ∃ r s : Regime, r.wf ∧ s.wf ∧ Dupfree s ∧ Nonempty (Iso r s) ∧
      r.reqs.length ≠ s.reqs.length :=
  ⟨reqTwice, reqOnce,
    by refine ⟨?_, ?_, ?_, ?_⟩ <;> decide,
    by refine ⟨?_, ?_, ?_, ?_⟩ <;> decide,
    by refine ⟨?_, ?_, ?_⟩ <;> decide,
    ⟨idIso _ _ (by decide) (by decide) (by decide) (by decide) (by decide)
      (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)⟩,
    by decide⟩

theorem reqs_need_wf :
    ∃ r s : Regime, Dupfree r ∧ Dupfree s ∧ s.wf ∧ Nonempty (Iso r s) ∧
      r.reqs.length ≠ s.reqs.length :=
  ⟨reqReversed, reqOnce,
    by refine ⟨?_, ?_, ?_⟩ <;> decide,
    by refine ⟨?_, ?_, ?_⟩ <;> decide,
    by refine ⟨?_, ?_, ?_, ?_⟩ <;> decide,
    ⟨idIso _ _ (by decide) (by decide) (by decide) (by decide) (by decide)
      (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)⟩,
    by decide⟩

/-- Across two bases the class of the regime reached does not carry the
CHANGING count. -/
theorem counts_not_of_class :
    ∃ (b₁ b₂ r₁ r₂ : Regime) (h₁ h₂ : List Event),
      replayE h₁ b₁ = some r₁ ∧ replayE h₂ b₂ = some r₂ ∧
      Nonempty (Iso r₁ r₂) ∧ changes b₁ h₁ = 0 ∧ changes b₂ h₂ = 3 :=
  ⟨R2L, genesis, R2L, R2L, [], [.admitDatum, .admitDatum, .impose 0 1],
    rfl, by decide, ⟨isoRefl R2L (by decide)⟩, rfl, by decide⟩

end Counter
end SecondClass
