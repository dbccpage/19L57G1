import SecondSymmetry.Aut

/-!
# Which automorphisms survive an adding event

Native to rung five.  For each of the three event kinds that add one
element -- an instance, a uniform rule, a requirement -- and an element
that is well-formed and not already admitted, three facts:

* `*_fixed_of_survives`: a pair of maps that is an automorphism before
  and an automorphism after FIXES the added element;
* `*_survives_of_fixed`: an automorphism before that fixes it survives,
  with the same maps;
* `*_descends_of_fixed`: for a well-formed regime before, an automorphism
  after that fixes it is, with the same maps, an automorphism before.

So the maps common to both sides are exactly the fixers before
(`*_meet`) and exactly the fixers after (`*_meet_after`).  Nothing here
counts an automorphism set: these are statements about WHICH pairs of
maps survive, never about how many.  No decidability hypothesis is taken.

AuthorityEffect: None.
-/

namespace SecondSymmetry
namespace Aut

open Sealed

/-- A list is fixed by a map that fixes each of its members. -/
theorem map_fix {l : List Nat} {g : Nat → Nat}
    (hg : ∀ a ∈ l, g a = a) : l.map g = l := by
  induction l with
  | nil => rfl
  | cons a as ih =>
    simp only [List.map_cons]
    rw [hg a (List.mem_cons.mpr (Or.inl rfl)),
        ih (fun x hx => hg x (List.mem_cons.mpr (Or.inr hx)))]

/-- Two maps agreeing on a list's members map it alike. -/
theorem map_agree {l : List Nat} {g h : Nat → Nat}
    (hg : ∀ a ∈ l, g a = h a) : l.map g = l.map h := by
  induction l with
  | nil => rfl
  | cons a as ih =>
    simp only [List.map_cons]
    rw [hg a (List.mem_cons.mpr (Or.inl rfl)),
        ih (fun x hx => hg x (List.mem_cons.mpr (Or.inr hx)))]

/-! ## Round trips of the image maps -/

/-- Carrying an admitted instance forward and back returns it. -/
theorem inst_back {r s : Regime} (σ : Iso r s) {p : Inst}
    (hf : p.1 < r.forms.length) (ha : ∀ a ∈ p.2, a < r.data) :
    (σ.finv (instImage σ p).1, (instImage σ p).2.map σ.dinv) = p := by
  have k1 : σ.finv (σ.fmap p.1) = p.1 := σ.finv_fmap p.1 (List.mem_range.mpr hf)
  have k2 : (p.2.map σ.dmap).map σ.dinv = p.2 := by
    rw [List.map_map]
    exact map_fix (fun a h => σ.dinv_dmap a (List.mem_range.mpr (ha a h)))
  show (σ.finv (σ.fmap p.1), (p.2.map σ.dmap).map σ.dinv) = p
  rw [k1, k2]

/-- Carrying an instance of the target back and forward returns it. -/
theorem inst_fwd_back {r s : Regime} (σ : Iso r s) {p : Inst}
    (hf : p.1 < s.forms.length) (ha : ∀ a ∈ p.2, a < s.data) :
    instImage σ (σ.finv p.1, p.2.map σ.dinv) = p := by
  have k1 : σ.fmap (σ.finv p.1) = p.1 := σ.fmap_finv p.1 (List.mem_range.mpr hf)
  have k2 : (p.2.map σ.dinv).map σ.dmap = p.2 := by
    rw [List.map_map]
    exact map_fix (fun a h => σ.dmap_dinv a (List.mem_range.mpr (ha a h)))
  show (σ.fmap (σ.finv p.1), (p.2.map σ.dinv).map σ.dmap) = p
  rw [k1, k2]

/-- An ordered pair survives a round trip through two maps that undo
each other on its entries. -/
theorem sortPair_round (g h : Nat → Nat) {q : Nat × Nat} (hq : q.1 < q.2)
    (h1 : h (g q.1) = q.1) (h2 : h (g q.2) = q.2) :
    sortPair (h (sortPair (g q.1, g q.2)).1, h (sortPair (g q.1, g q.2)).2)
      = q := by
  by_cases hc : g q.1 ≤ g q.2
  · have e : sortPair (g q.1, g q.2) = (g q.1, g q.2) := if_pos hc
    rw [e]
    show sortPair (h (g q.1), h (g q.2)) = q
    rw [h1, h2]
    exact if_pos (Nat.le_of_lt hq)
  · have e : sortPair (g q.1, g q.2) = (g q.2, g q.1) := if_neg hc
    rw [e]
    show sortPair (h (g q.2), h (g q.1)) = q
    rw [h1, h2]
    have hn : ¬ q.2 ≤ q.1 := Nat.not_le_of_gt hq
    exact if_neg hn

/-! ## Instances -/

theorem inst_fixed_of_survives {r : Regime} {e : Inst}
    (hnew : e ∉ r.insts) (hf : e.1 < r.forms.length)
    (ha : ∀ a ∈ e.2, a < r.data)
    (σ : Iso r r) (τ : Iso (addInst r e) (addInst r e))
    (hs : SameMaps σ τ) : instImage σ e = e := by
  have hmem : (τ.fmap e.1, e.2.map τ.dmap) ∈ insertNew r.insts e :=
    τ.insts_fwd e (mem_insertNew.mpr (Or.inr rfl))
  rw [← hs.1, ← hs.2.2.1] at hmem
  cases mem_insertNew.mp hmem with
  | inl hin =>
    have hb := σ.insts_bwd _ hin
    have hback := inst_back σ hf ha
    exact absurd (hback ▸ hb) hnew
  | inr heq => exact heq

theorem inst_survives_of_fixed {r : Regime} {e : Inst}
    (hf : e.1 < r.forms.length) (ha : ∀ a ∈ e.2, a < r.data)
    (σ : Iso r r) (hfix : instImage σ e = e) : Survives σ (addInst r e) := by
  have hinv : (σ.finv e.1, e.2.map σ.dinv) = e := by
    have hb := inst_back σ hf ha
    rw [hfix] at hb
    exact hb
  refine ⟨{ dmap := σ.dmap, dinv := σ.dinv, fmap := σ.fmap, finv := σ.finv,
            dmap_lt := σ.dmap_lt, dinv_lt := σ.dinv_lt,
            dinv_dmap := σ.dinv_dmap, dmap_dinv := σ.dmap_dinv,
            fmap_lt := σ.fmap_lt, finv_lt := σ.finv_lt,
            finv_fmap := σ.finv_fmap, fmap_finv := σ.fmap_finv,
            arity := σ.arity,
            insts_fwd := ?_, insts_bwd := ?_,
            rules_fwd := σ.rules_fwd, rules_bwd := σ.rules_bwd,
            reqs_fwd := σ.reqs_fwd, reqs_bwd := σ.reqs_bwd },
          rfl, rfl, rfl, rfl⟩
  · intro p hp
    cases mem_insertNew.mp hp with
    | inl hin => exact mem_insertNew.mpr (Or.inl (σ.insts_fwd p hin))
    | inr heq => exact mem_insertNew.mpr (Or.inr (heq ▸ hfix))
  · intro p hp
    cases mem_insertNew.mp hp with
    | inl hin => exact mem_insertNew.mpr (Or.inl (σ.insts_bwd p hin))
    | inr heq => exact mem_insertNew.mpr (Or.inr (heq ▸ hinv))

theorem inst_descends_of_fixed {r : Regime} {e : Inst} (hwf : r.wf)
    (hnew : e ∉ r.insts) (hf : e.1 < r.forms.length)
    (ha : ∀ a ∈ e.2, a < r.data)
    (τ : Iso (addInst r e) (addInst r e)) (hfix : instImage τ e = e) :
    ∃ σ : Iso r r, SameMaps τ σ := by
  refine ⟨{ dmap := τ.dmap, dinv := τ.dinv, fmap := τ.fmap, finv := τ.finv,
            dmap_lt := τ.dmap_lt, dinv_lt := τ.dinv_lt,
            dinv_dmap := τ.dinv_dmap, dmap_dinv := τ.dmap_dinv,
            fmap_lt := τ.fmap_lt, finv_lt := τ.finv_lt,
            finv_fmap := τ.finv_fmap, fmap_finv := τ.fmap_finv,
            arity := τ.arity,
            insts_fwd := ?_, insts_bwd := ?_,
            rules_fwd := τ.rules_fwd, rules_bwd := τ.rules_bwd,
            reqs_fwd := τ.reqs_fwd, reqs_bwd := τ.reqs_bwd },
          rfl, rfl, rfl, rfl⟩
  · intro p hp
    have hpf := (hwf.1 p hp).1
    have hpa := (hwf.1 p hp).2.2
    have hm := τ.insts_fwd p (mem_insertNew.mpr (Or.inl hp))
    cases mem_insertNew.mp hm with
    | inl hin => exact hin
    | inr heq =>
      -- the image of `p` is the image of `e`, so `p` is `e`
      have hpe : p = e := by
        have b1 : (τ.finv (instImage τ p).1, (instImage τ p).2.map τ.dinv) = p :=
          inst_back τ hpf hpa
        have b2 : (τ.finv (instImage τ e).1, (instImage τ e).2.map τ.dinv) = e :=
          inst_back τ hf ha
        have hi : instImage τ p = instImage τ e := heq.trans hfix.symm
        rw [hi] at b1
        exact b1.symm.trans b2
      exact absurd (hpe ▸ hp) hnew
  · intro p hp
    have hpf := (hwf.1 p hp).1
    have hpa := (hwf.1 p hp).2.2
    have hm := τ.insts_bwd p (mem_insertNew.mpr (Or.inl hp))
    cases mem_insertNew.mp hm with
    | inl hin => exact hin
    | inr heq =>
      -- carrying `e` forward returns `p`, and also returns `e`
      have hpe : p = e := by
        have b1 : instImage τ (τ.finv p.1, p.2.map τ.dinv) = p :=
          inst_fwd_back τ hpf hpa
        rw [heq, hfix] at b1
        exact b1.symm
      exact absurd (hpe ▸ hp) hnew

theorem inst_meet {r : Regime} {e : Inst}
    (hnew : e ∉ r.insts) (hf : e.1 < r.forms.length)
    (ha : ∀ a ∈ e.2, a < r.data) (σ : Iso r r) :
    Survives σ (addInst r e) ↔ instImage σ e = e :=
  ⟨fun ⟨τ, hs⟩ => inst_fixed_of_survives hnew hf ha σ τ hs,
   inst_survives_of_fixed hf ha σ⟩

theorem inst_meet_after {r : Regime} {e : Inst} (hwf : r.wf)
    (hnew : e ∉ r.insts) (hf : e.1 < r.forms.length)
    (ha : ∀ a ∈ e.2, a < r.data) (τ : Iso (addInst r e) (addInst r e)) :
    (∃ σ : Iso r r, SameMaps τ σ) ↔ instImage τ e = e := by
  constructor
  · intro ⟨σ, hs⟩
    have h := inst_fixed_of_survives hnew hf ha σ τ (sameMaps_symm hs)
    unfold instImage at h ⊢
    rw [hs.1, hs.2.2.1]
    exact h
  · exact inst_descends_of_fixed hwf hnew hf ha τ

/-! ## Uniform rules -/

theorem rule_fixed_of_survives {r : Regime} {e : Nat}
    (hnew : e ∉ r.rules) (hf : e < r.forms.length)
    (σ : Iso r r) (τ : Iso (addRule r e) (addRule r e))
    (hs : SameMaps σ τ) : σ.fmap e = e := by
  have hmem : τ.fmap e ∈ insertNew r.rules e :=
    τ.rules_fwd e (mem_insertNew.mpr (Or.inr rfl))
  rw [← hs.2.2.1] at hmem
  cases mem_insertNew.mp hmem with
  | inl hin =>
    have hb := σ.rules_bwd _ hin
    rw [σ.finv_fmap e (List.mem_range.mpr hf)] at hb
    exact absurd hb hnew
  | inr heq => exact heq

theorem rule_survives_of_fixed {r : Regime} {e : Nat}
    (hf : e < r.forms.length) (σ : Iso r r) (hfix : σ.fmap e = e) :
    Survives σ (addRule r e) := by
  have hinv : σ.finv e = e := by
    have hb := σ.finv_fmap e (List.mem_range.mpr hf)
    rw [hfix] at hb
    exact hb
  refine ⟨{ dmap := σ.dmap, dinv := σ.dinv, fmap := σ.fmap, finv := σ.finv,
            dmap_lt := σ.dmap_lt, dinv_lt := σ.dinv_lt,
            dinv_dmap := σ.dinv_dmap, dmap_dinv := σ.dmap_dinv,
            fmap_lt := σ.fmap_lt, finv_lt := σ.finv_lt,
            finv_fmap := σ.finv_fmap, fmap_finv := σ.fmap_finv,
            arity := σ.arity,
            insts_fwd := σ.insts_fwd, insts_bwd := σ.insts_bwd,
            rules_fwd := ?_, rules_bwd := ?_,
            reqs_fwd := σ.reqs_fwd, reqs_bwd := σ.reqs_bwd },
          rfl, rfl, rfl, rfl⟩
  · intro p hp
    cases mem_insertNew.mp hp with
    | inl hin => exact mem_insertNew.mpr (Or.inl (σ.rules_fwd p hin))
    | inr heq => exact mem_insertNew.mpr (Or.inr (heq ▸ hfix))
  · intro p hp
    cases mem_insertNew.mp hp with
    | inl hin => exact mem_insertNew.mpr (Or.inl (σ.rules_bwd p hin))
    | inr heq => exact mem_insertNew.mpr (Or.inr (heq ▸ hinv))

theorem rule_descends_of_fixed {r : Regime} {e : Nat} (hwf : r.wf)
    (hnew : e ∉ r.rules) (hf : e < r.forms.length)
    (τ : Iso (addRule r e) (addRule r e)) (hfix : τ.fmap e = e) :
    ∃ σ : Iso r r, SameMaps τ σ := by
  refine ⟨{ dmap := τ.dmap, dinv := τ.dinv, fmap := τ.fmap, finv := τ.finv,
            dmap_lt := τ.dmap_lt, dinv_lt := τ.dinv_lt,
            dinv_dmap := τ.dinv_dmap, dmap_dinv := τ.dmap_dinv,
            fmap_lt := τ.fmap_lt, finv_lt := τ.finv_lt,
            finv_fmap := τ.finv_fmap, fmap_finv := τ.fmap_finv,
            arity := τ.arity,
            insts_fwd := τ.insts_fwd, insts_bwd := τ.insts_bwd,
            rules_fwd := ?_, rules_bwd := ?_,
            reqs_fwd := τ.reqs_fwd, reqs_bwd := τ.reqs_bwd },
          rfl, rfl, rfl, rfl⟩
  · intro p hp
    have hpf := hwf.2.1 p hp
    have hm := τ.rules_fwd p (mem_insertNew.mpr (Or.inl hp))
    cases mem_insertNew.mp hm with
    | inl hin => exact hin
    | inr heq =>
      have hpe : p = e := by
        have b1 := τ.finv_fmap p (List.mem_range.mpr hpf)
        have b2 := τ.finv_fmap e (List.mem_range.mpr hf)
        rw [heq] at b1
        rw [hfix] at b2
        exact b1.symm.trans b2
      exact absurd (hpe ▸ hp) hnew
  · intro p hp
    have hpf := hwf.2.1 p hp
    have hm := τ.rules_bwd p (mem_insertNew.mpr (Or.inl hp))
    cases mem_insertNew.mp hm with
    | inl hin => exact hin
    | inr heq =>
      have hpe : p = e := by
        have b1 := τ.fmap_finv p (List.mem_range.mpr hpf)
        rw [heq, hfix] at b1
        exact b1.symm
      exact absurd (hpe ▸ hp) hnew

theorem rule_meet {r : Regime} {e : Nat}
    (hnew : e ∉ r.rules) (hf : e < r.forms.length) (σ : Iso r r) :
    Survives σ (addRule r e) ↔ σ.fmap e = e :=
  ⟨fun ⟨τ, hs⟩ => rule_fixed_of_survives hnew hf σ τ hs,
   rule_survives_of_fixed hf σ⟩

theorem rule_meet_after {r : Regime} {e : Nat} (hwf : r.wf)
    (hnew : e ∉ r.rules) (hf : e < r.forms.length)
    (τ : Iso (addRule r e) (addRule r e)) :
    (∃ σ : Iso r r, SameMaps τ σ) ↔ τ.fmap e = e := by
  constructor
  · intro ⟨σ, hs⟩
    have h := rule_fixed_of_survives hnew hf σ τ (sameMaps_symm hs)
    rw [hs.2.2.1]
    exact h
  · exact rule_descends_of_fixed hwf hnew hf τ

/-! ## Requirements -/

theorem req_fixed_of_survives {r : Regime} {e : Nat × Nat}
    (hnew : e ∉ r.reqs) (hlt : e.1 < e.2) (hd : e.2 < r.data)
    (σ : Iso r r) (τ : Iso (addReq r e) (addReq r e))
    (hs : SameMaps σ τ) : reqImage σ e = e := by
  have hmem : sortPair (τ.dmap e.1, τ.dmap e.2) ∈ insertNew r.reqs e :=
    τ.reqs_fwd e (mem_insertNew.mpr (Or.inr rfl))
  rw [← hs.1] at hmem
  cases mem_insertNew.mp hmem with
  | inl hin =>
    have hb := σ.reqs_bwd _ hin
    have hback := sortPair_round σ.dmap σ.dinv hlt
      (σ.dinv_dmap e.1 (List.mem_range.mpr (Nat.lt_trans hlt hd)))
      (σ.dinv_dmap e.2 (List.mem_range.mpr hd))
    exact absurd (hback ▸ hb) hnew
  | inr heq => exact heq

theorem req_survives_of_fixed {r : Regime} {e : Nat × Nat}
    (hlt : e.1 < e.2) (hd : e.2 < r.data)
    (σ : Iso r r) (hfix : reqImage σ e = e) : Survives σ (addReq r e) := by
  have hinv : sortPair (σ.dinv e.1, σ.dinv e.2) = e := by
    have hb := sortPair_round σ.dmap σ.dinv hlt
      (σ.dinv_dmap e.1 (List.mem_range.mpr (Nat.lt_trans hlt hd)))
      (σ.dinv_dmap e.2 (List.mem_range.mpr hd))
    have hfix' : sortPair (σ.dmap e.1, σ.dmap e.2) = e := hfix
    rw [hfix'] at hb
    exact hb
  refine ⟨{ dmap := σ.dmap, dinv := σ.dinv, fmap := σ.fmap, finv := σ.finv,
            dmap_lt := σ.dmap_lt, dinv_lt := σ.dinv_lt,
            dinv_dmap := σ.dinv_dmap, dmap_dinv := σ.dmap_dinv,
            fmap_lt := σ.fmap_lt, finv_lt := σ.finv_lt,
            finv_fmap := σ.finv_fmap, fmap_finv := σ.fmap_finv,
            arity := σ.arity,
            insts_fwd := σ.insts_fwd, insts_bwd := σ.insts_bwd,
            rules_fwd := σ.rules_fwd, rules_bwd := σ.rules_bwd,
            reqs_fwd := ?_, reqs_bwd := ?_ },
          rfl, rfl, rfl, rfl⟩
  · intro p hp
    cases mem_insertNew.mp hp with
    | inl hin => exact mem_insertNew.mpr (Or.inl (σ.reqs_fwd p hin))
    | inr heq => exact mem_insertNew.mpr (Or.inr (heq ▸ hfix))
  · intro p hp
    cases mem_insertNew.mp hp with
    | inl hin => exact mem_insertNew.mpr (Or.inl (σ.reqs_bwd p hin))
    | inr heq => exact mem_insertNew.mpr (Or.inr (heq ▸ hinv))

theorem req_descends_of_fixed {r : Regime} {e : Nat × Nat} (hwf : r.wf)
    (hnew : e ∉ r.reqs) (hlt : e.1 < e.2) (hd : e.2 < r.data)
    (τ : Iso (addReq r e) (addReq r e)) (hfix : reqImage τ e = e) :
    ∃ σ : Iso r r, SameMaps τ σ := by
  have hfix' : sortPair (τ.dmap e.1, τ.dmap e.2) = e := hfix
  refine ⟨{ dmap := τ.dmap, dinv := τ.dinv, fmap := τ.fmap, finv := τ.finv,
            dmap_lt := τ.dmap_lt, dinv_lt := τ.dinv_lt,
            dinv_dmap := τ.dinv_dmap, dmap_dinv := τ.dmap_dinv,
            fmap_lt := τ.fmap_lt, finv_lt := τ.finv_lt,
            finv_fmap := τ.finv_fmap, fmap_finv := τ.fmap_finv,
            arity := τ.arity,
            insts_fwd := τ.insts_fwd, insts_bwd := τ.insts_bwd,
            rules_fwd := τ.rules_fwd, rules_bwd := τ.rules_bwd,
            reqs_fwd := ?_, reqs_bwd := ?_ },
          rfl, rfl, rfl, rfl⟩
  · intro p hp
    have hplt := (hwf.2.2.1 p hp).1
    have hpd := (hwf.2.2.1 p hp).2
    have hm := τ.reqs_fwd p (mem_insertNew.mpr (Or.inl hp))
    cases mem_insertNew.mp hm with
    | inl hin => exact hin
    | inr heq =>
      have hpe : p = e := by
        have b1 := sortPair_round τ.dmap τ.dinv hplt
          (τ.dinv_dmap p.1 (List.mem_range.mpr (Nat.lt_trans hplt hpd)))
          (τ.dinv_dmap p.2 (List.mem_range.mpr hpd))
        have b2 := sortPair_round τ.dmap τ.dinv hlt
          (τ.dinv_dmap e.1 (List.mem_range.mpr (Nat.lt_trans hlt hd)))
          (τ.dinv_dmap e.2 (List.mem_range.mpr hd))
        rw [heq] at b1
        rw [hfix'] at b2
        exact b1.symm.trans b2
      exact absurd (hpe ▸ hp) hnew
  · intro p hp
    have hplt := (hwf.2.2.1 p hp).1
    have hpd := (hwf.2.2.1 p hp).2
    have hm := τ.reqs_bwd p (mem_insertNew.mpr (Or.inl hp))
    cases mem_insertNew.mp hm with
    | inl hin => exact hin
    | inr heq =>
      have hpe : p = e := by
        have b1 := sortPair_round τ.dinv τ.dmap hplt
          (τ.dmap_dinv p.1 (List.mem_range.mpr (Nat.lt_trans hplt hpd)))
          (τ.dmap_dinv p.2 (List.mem_range.mpr hpd))
        rw [heq, hfix'] at b1
        exact b1.symm
      exact absurd (hpe ▸ hp) hnew

theorem req_meet {r : Regime} {e : Nat × Nat}
    (hnew : e ∉ r.reqs) (hlt : e.1 < e.2) (hd : e.2 < r.data) (σ : Iso r r) :
    Survives σ (addReq r e) ↔ reqImage σ e = e :=
  ⟨fun ⟨τ, hs⟩ => req_fixed_of_survives hnew hlt hd σ τ hs,
   req_survives_of_fixed hlt hd σ⟩

theorem req_meet_after {r : Regime} {e : Nat × Nat} (hwf : r.wf)
    (hnew : e ∉ r.reqs) (hlt : e.1 < e.2) (hd : e.2 < r.data)
    (τ : Iso (addReq r e) (addReq r e)) :
    (∃ σ : Iso r r, SameMaps τ σ) ↔ reqImage τ e = e := by
  constructor
  · intro ⟨σ, hs⟩
    have h := req_fixed_of_survives hnew hlt hd σ τ (sameMaps_symm hs)
    unfold reqImage at h ⊢
    rw [hs.1]
    exact h
  · exact req_descends_of_fixed hwf hnew hlt hd τ

end Aut
end SecondSymmetry
