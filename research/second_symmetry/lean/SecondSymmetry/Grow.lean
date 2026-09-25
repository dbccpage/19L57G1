import SecondSymmetry.Meet

/-!
# Admitting a datum or a form loses no automorphism; the element count

Native to rung five.

* `datum_lift`, `form_lift`: every automorphism of a well-formed regime
  extends, fixing the new index, to an automorphism of the regime after
  admitting a datum, and after admitting a form.  So no automorphism is
  lost at either kind.  How MANY are gained is not stated here; it is a
  finite computation of this rung.
* `size_step`: every event either leaves the regime unchanged or raises
  its element count by exactly one.
* `size_counts_changes`: the element count of the regime a history
  reaches from a base is the base's count plus the number of the
  history's events that change the regime.  `size_replay_mono` and
  `no_return` follow.

`no_return` is irreversibility of the REGIME, a presentation.  Whether a
history can return to a regime the sealed isomorphism relates to one it
left is not proved here: that needs the element count to be carried
across an isomorphism, which this rung does not prove.

AuthorityEffect: None.
-/

namespace SecondSymmetry
namespace Aut

open Sealed

/-- Extend a map on `[0, n)` by the identity at and above `n`. -/
def ext (n : Nat) (g : Nat → Nat) (d : Nat) : Nat :=
  if d < n then g d else d

theorem ext_lt {n : Nat} {g : Nat → Nat} {d : Nat} (h : d < n) :
    ext n g d = g d := if_pos h

theorem ext_ge {n : Nat} {g : Nat → Nat} {d : Nat} (h : ¬ d < n) :
    ext n g d = d := if_neg h

/-- A map extended past `n` stays in `[0, n + 1)` when the map keeps
`[0, n)` inside `[0, n)`. -/
theorem ext_range {n : Nat} {g : Nat → Nat}
    (hg : ∀ d ∈ List.range n, g d < n) :
    ∀ d ∈ List.range (n + 1), ext n g d < n + 1 := by
  intro d hd
  have hd' : d < n + 1 := List.mem_range.mp hd
  by_cases hc : d < n
  · rw [ext_lt hc]
    exact Nat.lt_succ_of_lt (hg d (List.mem_range.mpr hc))
  · rw [ext_ge hc]
    exact hd'

/-- Two maps undoing each other on `[0, n)` still do after extension. -/
theorem ext_inverse {n : Nat} {g h : Nat → Nat}
    (hg : ∀ d ∈ List.range n, g d < n)
    (hgh : ∀ d ∈ List.range n, h (g d) = d) :
    ∀ d ∈ List.range (n + 1), ext n h (ext n g d) = d := by
  intro d _
  by_cases hc : d < n
  · rw [ext_lt hc, ext_lt (hg d (List.mem_range.mpr hc))]
    exact hgh d (List.mem_range.mpr hc)
  · rw [ext_ge hc, ext_ge hc]

theorem datum_lift {r : Regime} (hwf : r.wf) (σ : Iso r r) :
    ∃ τ : Iso (addDatum r) (addDatum r),
      (∀ d, d < r.data → τ.dmap d = σ.dmap d) ∧ τ.dmap r.data = r.data ∧
      τ.fmap = σ.fmap ∧ τ.finv = σ.finv := by
  have hargs : ∀ p ∈ r.insts, ∀ g : Nat → Nat,
      p.2.map (ext r.data g) = p.2.map g := by
    intro p hp g
    exact map_agree (fun a ha => ext_lt ((hwf.1 p hp).2.2 a ha))
  have hreq : ∀ q ∈ r.reqs, ∀ g : Nat → Nat,
      sortPair (ext r.data g q.1, ext r.data g q.2) = sortPair (g q.1, g q.2) := by
    intro q hq g
    have h1 := (hwf.2.2.1 q hq).1
    have h2 := (hwf.2.2.1 q hq).2
    rw [ext_lt (Nat.lt_trans h1 h2), ext_lt h2]
  refine ⟨{ dmap := ext r.data σ.dmap, dinv := ext r.data σ.dinv,
            fmap := σ.fmap, finv := σ.finv,
            dmap_lt := ext_range σ.dmap_lt, dinv_lt := ext_range σ.dinv_lt,
            dinv_dmap := ext_inverse σ.dmap_lt σ.dinv_dmap,
            dmap_dinv := ext_inverse σ.dinv_lt σ.dmap_dinv,
            fmap_lt := σ.fmap_lt, finv_lt := σ.finv_lt,
            finv_fmap := σ.finv_fmap, fmap_finv := σ.fmap_finv,
            arity := σ.arity,
            insts_fwd := ?_, insts_bwd := ?_,
            rules_fwd := σ.rules_fwd, rules_bwd := σ.rules_bwd,
            reqs_fwd := ?_, reqs_bwd := ?_ },
          fun d hd => ext_lt hd, ext_ge (Nat.lt_irrefl r.data), rfl, rfl⟩
  · intro p hp
    show (σ.fmap p.1, p.2.map (ext r.data σ.dmap)) ∈ r.insts
    rw [hargs p hp]
    exact σ.insts_fwd p hp
  · intro p hp
    show (σ.finv p.1, p.2.map (ext r.data σ.dinv)) ∈ r.insts
    rw [hargs p hp]
    exact σ.insts_bwd p hp
  · intro q hq
    show sortPair (ext r.data σ.dmap q.1, ext r.data σ.dmap q.2) ∈ r.reqs
    rw [hreq q hq]
    exact σ.reqs_fwd q hq
  · intro q hq
    show sortPair (ext r.data σ.dinv q.1, ext r.data σ.dinv q.2) ∈ r.reqs
    rw [hreq q hq]
    exact σ.reqs_bwd q hq

/-- Reading a list extended at its end, at an index inside the list. -/
theorem getD_append_lt (l : List Nat) (a : Nat) {i : Nat} (h : i < l.length) :
    (l ++ [a]).getD i 0 = l.getD i 0 := by
  induction l generalizing i with
  | nil => exact absurd h (Nat.not_lt_zero i)
  | cons x xs ih =>
    cases i with
    | zero => rfl
    | succ k =>
      have hk : k < xs.length := Nat.lt_of_succ_lt_succ h
      exact ih hk

theorem form_lift {r : Regime} (a : Nat) (hwf : r.wf) (σ : Iso r r) :
    ∃ τ : Iso (addForm r a) (addForm r a),
      τ.dmap = σ.dmap ∧ τ.dinv = σ.dinv ∧
      (∀ f, f < r.forms.length → τ.fmap f = σ.fmap f) ∧
      τ.fmap r.forms.length = r.forms.length := by
  have hlen : (r.forms ++ [a]).length = r.forms.length + 1 := by
    rw [List.length_append]
    rfl
  have hrange : List.range (addForm r a).forms.length
      = List.range (r.forms.length + 1) := by
    show List.range (r.forms ++ [a]).length = List.range (r.forms.length + 1)
    rw [hlen]
  have hrule : ∀ f ∈ r.rules, ∀ g : Nat → Nat, ext r.forms.length g f = g f :=
    fun f hf _ => ext_lt (hwf.2.1 f hf)
  have hinst : ∀ p ∈ r.insts, ∀ g : Nat → Nat,
      ext r.forms.length g p.1 = g p.1 :=
    fun p hp _ => ext_lt (hwf.1 p hp).1
  refine ⟨{ dmap := σ.dmap, dinv := σ.dinv,
            fmap := ext r.forms.length σ.fmap,
            finv := ext r.forms.length σ.finv,
            dmap_lt := σ.dmap_lt, dinv_lt := σ.dinv_lt,
            dinv_dmap := σ.dinv_dmap, dmap_dinv := σ.dmap_dinv,
            fmap_lt := ?_, finv_lt := ?_, finv_fmap := ?_, fmap_finv := ?_,
            arity := ?_,
            insts_fwd := ?_, insts_bwd := ?_,
            rules_fwd := ?_, rules_bwd := ?_,
            reqs_fwd := σ.reqs_fwd, reqs_bwd := σ.reqs_bwd },
          rfl, rfl, fun f hf => ext_lt hf,
          ext_ge (Nat.lt_irrefl r.forms.length)⟩
  · intro f hf
    rw [hrange] at hf
    show ext r.forms.length σ.fmap f < (r.forms ++ [a]).length
    rw [hlen]
    exact ext_range σ.fmap_lt f hf
  · intro f hf
    rw [hrange] at hf
    show ext r.forms.length σ.finv f < (r.forms ++ [a]).length
    rw [hlen]
    exact ext_range σ.finv_lt f hf
  · intro f hf
    rw [hrange] at hf
    exact ext_inverse σ.fmap_lt σ.finv_fmap f hf
  · intro f hf
    rw [hrange] at hf
    exact ext_inverse σ.finv_lt σ.fmap_finv f hf
  · intro f hf
    rw [hrange] at hf
    show (r.forms ++ [a]).getD (ext r.forms.length σ.fmap f) 0
        = (r.forms ++ [a]).getD f 0
    by_cases hc : f < r.forms.length
    · have himg : σ.fmap f < r.forms.length := σ.fmap_lt f (List.mem_range.mpr hc)
      rw [ext_lt hc, getD_append_lt r.forms a himg, getD_append_lt r.forms a hc]
      exact σ.arity f (List.mem_range.mpr hc)
    · rw [ext_ge hc]
  · intro p hp
    show (ext r.forms.length σ.fmap p.1, p.2.map σ.dmap) ∈ r.insts
    rw [hinst p hp]
    exact σ.insts_fwd p hp
  · intro p hp
    show (ext r.forms.length σ.finv p.1, p.2.map σ.dinv) ∈ r.insts
    rw [hinst p hp]
    exact σ.insts_bwd p hp
  · intro f hf
    show ext r.forms.length σ.fmap f ∈ r.rules
    rw [hrule f hf]
    exact σ.rules_fwd f hf
  · intro f hf
    show ext r.forms.length σ.finv f ∈ r.rules
    rw [hrule f hf]
    exact σ.rules_bwd f hf

/-! ## The element count -/

/-- Inserting into a listed collection keeps it or adds exactly one. -/
theorem insertNew_cases {α : Type} [DecidableEq α] (l : List α) (a : α) :
    insertNew l a = l ∨ (insertNew l a).length = l.length + 1 := by
  by_cases h : a ∈ l
  · exact Or.inl (insertNew_of_mem h)
  · refine Or.inr ?_
    rw [insertNew_of_not_mem h, List.length_append]
    rfl

theorem size_step {r r' : Regime} {e : Event} (h : stepE r e = some r') :
    r' = r ∨ size r' = size r + 1 := by
  cases e with
  | supply t =>
    injection h with h
    exact Or.inl h.symm
  | admitDatum =>
    injection h with h
    subst h
    refine Or.inr ?_
    show r.data + 1 + r.forms.length + r.insts.length + r.rules.length
        + r.reqs.length = size r + 1
    unfold size
    omega
  | admitForm a =>
    by_cases hc : 1 ≤ a
    · rw [stepE_form r a hc] at h
      injection h with h
      subst h
      refine Or.inr ?_
      show r.data + (r.forms ++ [a]).length + r.insts.length + r.rules.length
          + r.reqs.length = size r + 1
      rw [List.length_append]
      unfold size
      show r.data + (r.forms.length + 1) + r.insts.length + r.rules.length
          + r.reqs.length = _
      omega
    · have hn : stepE r (.admitForm a) = none := by
        dsimp only [stepE]
        rw [if_neg hc]
      rw [hn] at h
      cases h
  | admitInst f args =>
    by_cases hc : f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
        (∀ x ∈ args, x < r.data)
    · rw [stepE_inst r f args hc] at h
      injection h with h
      subst h
      cases insertNew_cases r.insts (f, args) with
      | inl hk =>
        refine Or.inl ?_
        show { r with insts := insertNew r.insts (f, args) } = r
        rw [hk]
      | inr hk =>
        refine Or.inr ?_
        show r.data + r.forms.length + (insertNew r.insts (f, args)).length
            + r.rules.length + r.reqs.length = size r + 1
        rw [hk]
        unfold size
        omega
    · have hn : stepE r (.admitInst f args) = none := by
        dsimp only [stepE]
        rw [if_neg hc]
      rw [hn] at h
      cases h
  | admitRuleAll f =>
    by_cases hc : f < r.forms.length
    · rw [stepE_rule r f hc] at h
      injection h with h
      subst h
      cases insertNew_cases r.rules f with
      | inl hk =>
        refine Or.inl ?_
        show { r with rules := insertNew r.rules f } = r
        rw [hk]
      | inr hk =>
        refine Or.inr ?_
        show r.data + r.forms.length + r.insts.length
            + (insertNew r.rules f).length + r.reqs.length = size r + 1
        rw [hk]
        unfold size
        omega
    · have hn : stepE r (.admitRuleAll f) = none := by
        dsimp only [stepE]
        rw [if_neg hc]
      rw [hn] at h
      cases h
  | impose i j =>
    by_cases hc : i < j ∧ j < r.data
    · rw [stepE_req r i j hc] at h
      injection h with h
      subst h
      cases insertNew_cases r.reqs (i, j) with
      | inl hk =>
        refine Or.inl ?_
        show { r with reqs := insertNew r.reqs (i, j) } = r
        rw [hk]
      | inr hk =>
        refine Or.inr ?_
        show r.data + r.forms.length + r.insts.length + r.rules.length
            + (insertNew r.reqs (i, j)).length = size r + 1
        rw [hk]
        unfold size
        omega
    · have hn : stepE r (.impose i j) = none := by
        dsimp only [stepE]
        rw [if_neg hc]
      rw [hn] at h
      cases h

/-- The number of events of a history, replayed from a base, that change
the regime.  An ill-formed event ends the count, as it ends replay. -/
def changes : Regime → List Event → Nat
  | _, [] => 0
  | r, e :: es =>
    match stepE r e with
    | none => 0
    | some r' => (if r' = r then 0 else 1) + changes r' es

theorem replayE_cons (e : Event) (es : List Event) (b : Regime) :
    replayE (e :: es) b = (stepE b e).bind (fun r => replayE es r) := by
  unfold replayE
  rw [List.foldlM_cons]
  cases stepE b e <;> rfl

theorem size_counts_changes (h : List Event) :
    ∀ (b r : Regime), replayE h b = some r → size r = size b + changes b h := by
  induction h with
  | nil =>
    intro b r hr
    have hb : b = r := by
      injection hr
    subst hb
    rfl
  | cons e es ih =>
    intro b r hr
    rw [replayE_cons] at hr
    cases hs : stepE b e with
    | none =>
      rw [hs] at hr
      cases hr
    | some b' =>
      rw [hs] at hr
      have hrest := ih b' r hr
      have hc : changes b (e :: es) = (if b' = b then 0 else 1) + changes b' es := by
        show (match stepE b e with
          | none => 0
          | some r' => (if r' = b then 0 else 1) + changes r' es) = _
        rw [hs]
      rw [hc, hrest]
      cases size_step hs with
      | inl heq =>
        rw [if_pos heq, heq]
        omega
      | inr hsz =>
        by_cases hq : b' = b
        · rw [if_pos hq, hq]
          omega
        · rw [if_neg hq, hsz]
          omega

theorem size_replay_mono {h : List Event} {b r : Regime}
    (hr : replayE h b = some r) : size b ≤ size r := by
  rw [size_counts_changes h b r hr]
  exact Nat.le_add_right _ _

/-- No history returns to a regime it left by a changing event. -/
theorem no_return {r r' r'' : Regime} {e : Event} {h : List Event}
    (hs : stepE r e = some r') (hch : r' ≠ r)
    (hr : replayE h r' = some r'') : r'' ≠ r := by
  intro heq
  have h1 : size r' = size r + 1 := by
    cases size_step hs with
    | inl h => exact absurd h hch
    | inr h => exact h
  have h2 := size_replay_mono hr
  rw [heq, h1] at h2
  exact Nat.not_succ_le_self _ h2

end Aut
end SecondSymmetry
