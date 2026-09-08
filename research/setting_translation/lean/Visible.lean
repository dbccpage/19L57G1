import Magnification
import Chains

/-!
# Visible: when an encoded difference is internal, and what the engine does there

For a regime whose forms are all binary, a well-formed context is one of
three shapes — both slots holes, a hole beside an admitted datum on the
right, or on the left (`wfCtx_binary`).  So the declared sense of internal
separability reduces to a decidable criterion (`separable_iff_visible`):
two data are separable exactly when some form's **self-instance**, **row**
or **column** differs at them; and collapse is the negation
(`collapsed_iff_not_visible`); the self-instance clause is never the only
witness (`visible_iff_rows_columns`).

On an encoded setting this reads: the designated pair is internal exactly
when some form — a store or an operation graph — treats the two endpoints
differently in a self-instance, a row or a column.  A witnessed pair with
no self-instance is always internal (`A_separable`): the row context at the
second endpoint sees the link `(0, [a, b])` present and the self-instance
`(0, [b, b])` absent.  A bare witness is not enough: the constant relation
on two points with empty stores and no operation asserts the pair and
leaves it collapsed (`witness_alone_invisible`).

At a collapsed pair of a binary regime, every absent link and every absent
self-instance is a valid response (`link_valid`, `self_valid`) and hence a
minimum under both measures (`one_inst_min`, `link_min`, `self_min`); on
the two-point setting with no assertion the self-instance and the link on
the difference form are such minima (`noPair_fires_self`,
`noPair_fires_link`), and on the constant relation a self-instance on the
empty retention form is (`everyPair_fires`).  When every instance of every
form is present no one-instance response exists and the theorems say
nothing.  At a visible pair the engine has no seed firing, in either order
of the endpoints (`A_no_fire`), while the three fresh-form responses of the
seed remain valid there (`seed_embeds`).

AuthorityEffect: None.
-/

namespace Visible

open Derivation EngineClass Magnification Translation Chains

/-! ## 1. Contexts of a binary regime -/

/-- A regime all of whose forms are binary. -/
def Binary (r : Regime) : Prop := ∀ a ∈ r.forms, a = 2

instance (r : Regime) : Decidable (Binary r) := by
  unfold Binary; infer_instance

theorem binary_getD {r : Regime} (hb : Binary r) {f : Nat} (hf : f < r.forms.length) :
    r.forms.getD f 0 = 2 :=
  getD_of_all_two r.forms hb f hf

theorem two_slots :
    ∀ (s : List (Option Nat)), s.length = 2 → none ∈ s →
      s = [none, none] ∨ ∃ z, s = [none, some z] ∨ s = [some z, none]
  | [], h, _ => absurd h (by decide)
  | [_], h, _ => absurd h (by show ¬ (1 = 2); decide)
  | [none, none], _, _ => Or.inl rfl
  | [none, some z], _, _ => Or.inr ⟨z, Or.inl rfl⟩
  | [some z, none], _, _ => Or.inr ⟨z, Or.inr rfl⟩
  | [some _, some _], _, hh => by
      exfalso
      rcases List.mem_cons.mp hh with h | h
      · cases h
      · rcases List.mem_cons.mp h with h | h
        · cases h
        · exact List.not_mem_nil h
  | _ :: _ :: _ :: t, h, _ =>
      absurd (Nat.succ.inj (Nat.succ.inj (h : t.length + 3 = 2))) (Nat.succ_ne_zero _)

/-- The well-formed contexts of a binary regime are exactly the three shapes:
both holes, or one hole beside an admitted datum on the right or on the
left. -/
theorem wfCtx_binary {r : Regime} (hb : Binary r) (c : Ctx) :
    wfCtx r c ↔ c.form < r.forms.length ∧
      (c.slots = [none, none] ∨
        ∃ z, z < r.data ∧ (c.slots = [none, some z] ∨ c.slots = [some z, none])) := by
  constructor
  · rintro ⟨hf, hlen, hhole, hok⟩
    refine ⟨hf, ?_⟩
    rw [binary_getD hb hf] at hlen
    rcases two_slots c.slots hlen hhole with h | ⟨z, h | h⟩
    · exact Or.inl h
    · refine Or.inr ⟨z, ?_, Or.inl h⟩
      exact hok (some z) (by rw [h]; exact List.mem_cons_of_mem _ List.mem_cons_self)
    · refine Or.inr ⟨z, ?_, Or.inr h⟩
      exact hok (some z) (by rw [h]; exact List.mem_cons_self)
  · rintro ⟨hf, h | ⟨z, hz, h | h⟩⟩
    · refine ⟨hf, ?_, ?_, ?_⟩
      · rw [h, binary_getD hb hf]
        rfl
      · rw [h]
        exact List.mem_cons_self
      · rw [h]
        intro s hs
        rcases List.mem_cons.mp hs with rfl | hs
        · trivial
        · rcases List.mem_cons.mp hs with rfl | hs
          · trivial
          · exact absurd hs List.not_mem_nil
    · refine ⟨hf, ?_, ?_, ?_⟩
      · rw [h, binary_getD hb hf]
        rfl
      · rw [h]
        exact List.mem_cons_self
      · rw [h]
        intro s hs
        rcases List.mem_cons.mp hs with rfl | hs
        · trivial
        · rcases List.mem_cons.mp hs with rfl | hs
          · exact hz
          · exact absurd hs List.not_mem_nil
    · refine ⟨hf, ?_, ?_, ?_⟩
      · rw [h, binary_getD hb hf]
        rfl
      · rw [h]
        exact List.mem_cons_of_mem _ List.mem_cons_self
      · rw [h]
        intro s hs
        rcases List.mem_cons.mp hs with rfl | hs
        · exact hz
        · rcases List.mem_cons.mp hs with rfl | hs
          · trivial
          · exact absurd hs List.not_mem_nil

theorem wfCtx_row {r : Regime} (hb : Binary r) {f z : Nat} (hf : f < r.forms.length)
    (hz : z < r.data) : wfCtx r ⟨f, [none, some z]⟩ :=
  (wfCtx_binary hb _).mpr ⟨hf, Or.inr ⟨z, hz, Or.inl rfl⟩⟩

theorem wfCtx_column {r : Regime} (hb : Binary r) {f z : Nat} (hf : f < r.forms.length)
    (hz : z < r.data) : wfCtx r ⟨f, [some z, none]⟩ :=
  (wfCtx_binary hb _).mpr ⟨hf, Or.inr ⟨z, hz, Or.inr rfl⟩⟩

/-! ## 2. Internal visibility -/

/-- **Internal visibility**: some form's self-instance, row or column differs
at the two data. -/
def Visible (r : Regime) (x y : Nat) : Prop :=
  ∃ f, f < r.forms.length ∧
    (¬ (derivable r (f, [x, x]) ↔ derivable r (f, [y, y])) ∨
      ∃ z, z < r.data ∧
        (¬ (derivable r (f, [x, z]) ↔ derivable r (f, [y, z])) ∨
          ¬ (derivable r (f, [z, x]) ↔ derivable r (f, [z, y]))))

instance (r : Regime) (x y : Nat) : Decidable (Visible r x y) := by
  unfold Visible; infer_instance

theorem plug_slots (c : Ctx) (d : Nat) :
    plug c d = (c.form, c.slots.map (fun s => s.getD d)) := rfl

theorem visible_of_ctx {r : Regime} (hb : Binary r) {x y : Nat} (c : Ctx) (hc : wfCtx r c)
    (hne : ¬ (derivable r (plug c x) ↔ derivable r (plug c y))) : Visible r x y := by
  obtain ⟨hf, hs⟩ := (wfCtx_binary hb c).mp hc
  refine ⟨c.form, hf, ?_⟩
  rw [plug_slots, plug_slots] at hne
  rcases hs with h | ⟨z, hz, h | h⟩
  · rw [h] at hne
    exact Or.inl hne
  · rw [h] at hne
    exact Or.inr ⟨z, hz, Or.inl hne⟩
  · rw [h] at hne
    exact Or.inr ⟨z, hz, Or.inr hne⟩

/-- **The declared separability of a binary regime is internal visibility.** -/
theorem separable_iff_visible {r : Regime} (hb : Binary r) (x y : Nat) :
    separable r x y ↔ Visible r x y := by
  constructor
  · rintro ⟨c, hc, hne⟩
    exact visible_of_ctx hb c hc hne
  · rintro ⟨f, hf, h | ⟨z, hz, h | h⟩⟩
    · exact ⟨⟨f, [none, none]⟩, (wfCtx_binary hb _).mpr ⟨hf, Or.inl rfl⟩, h⟩
    · exact ⟨⟨f, [none, some z]⟩, wfCtx_row hb hf hz, h⟩
    · exact ⟨⟨f, [some z, none]⟩, wfCtx_column hb hf hz, h⟩

/-- Collapse of a binary regime is the absence of visibility. -/
theorem collapsed_iff_not_visible {r : Regime} (hb : Binary r) (x y : Nat) :
    collapsed r x y ↔ ¬ Visible r x y := by
  constructor
  · intro hc hv
    exact separable_not_collapsed ((separable_iff_visible hb x y).mpr hv) hc
  · intro hv c hc
    refine Decidable.of_not_not ?_
    intro hne
    exact hv (visible_of_ctx hb c hc hne)

/-- **The self-instance clause is never the only witness**: when the
self-instances differ, the row at the second datum or the column at the
first differs too.  On admitted data, visibility is a row or column
difference.  (Found by injection: deleting the clause from the computed
criterion changed no verdict over the sealed universe.) -/
theorem visible_iff_rows_columns {r : Regime} {x y : Nat} (hx : x < r.data) (hy : y < r.data) :
    Visible r x y ↔
      ∃ f, f < r.forms.length ∧ ∃ z, z < r.data ∧
        (¬ (derivable r (f, [x, z]) ↔ derivable r (f, [y, z])) ∨
          ¬ (derivable r (f, [z, x]) ↔ derivable r (f, [z, y]))) := by
  constructor
  · rintro ⟨f, hf, hd | ⟨z, hz, h⟩⟩
    · refine ⟨f, hf, ?_⟩
      rcases Decidable.em (derivable r (f, [x, y]) ↔ derivable r (f, [y, y])) with h1 | h1
      · rcases Decidable.em (derivable r (f, [x, x]) ↔ derivable r (f, [x, y])) with h2 | h2
        · exact absurd (h2.trans h1) hd
        · exact ⟨x, hx, Or.inr h2⟩
      · exact ⟨y, hy, Or.inl h1⟩
    · exact ⟨f, hf, z, hz, h⟩
  · rintro ⟨f, hf, z, hz, h⟩
    exact ⟨f, hf, Or.inr ⟨z, hz, h⟩⟩

/-! ## 3. On an encoded setting -/

theorem encode_binary (F : FiniteSetting) : Binary (encode F) := encode_forms_two F

theorem encode_separable_iff (F : FiniteSetting) (x y : Nat) :
    separable (encode F) x y ↔ Visible (encode F) x y :=
  separable_iff_visible (encode_binary F) x y

theorem encode_collapsed_iff (F : FiniteSetting) (x y : Nat) :
    collapsed (encode F) x y ↔ ¬ Visible (encode F) x y :=
  collapsed_iff_not_visible (encode_binary F) x y

theorem encode_form0_lt (F : FiniteSetting) : 0 < (encode F).forms.length := by
  rw [encode_forms_length]
  omega

/-- **A witnessed pair with no self-instance is internal**: the row context
at the second endpoint separates. -/
theorem A_separable (F : FiniteSetting) (h : PrimitiveCore.A (toSetting F)) :
    separable (encode F) F.a F.b := by
  obtain ⟨hw, hns⟩ := (A_iff F).mp h
  refine ⟨⟨0, [none, some F.b]⟩, wfCtx_row (encode_binary F) (encode_form0_lt F) F.b_lt, ?_⟩
  intro hiff
  exact hns F.b F.b_lt (hiff.mp hw)

/-! ## 4. Two-point exhibits -/

/-- A two-point setting carrying only an asserted relation. -/
def two (rel : Nat → Nat → Bool) : FiniteSetting :=
  ⟨2, rel, fun _ _ => false, fun _ _ => false, 0, 1, [], by decide, by decide,
   fun _ hg => absurd hg List.not_mem_nil⟩

/-- Only the self-instance at the first point. -/
def selfOnly : Nat → Nat → Bool := fun x y => decide (x = 0 ∧ y = 0)

/-- Only the link from the first point to the second. -/
def linkOnly : Nat → Nat → Bool := fun x y => decide (x = 0 ∧ y = 1)

/-- The self-instance and the link. -/
def selfAndLink : Nat → Nat → Bool := fun x y => decide (x = 0 ∧ (y = 0 ∨ y = 1))

/-- Both links, no self-instance. -/
def bothLinks : Nat → Nat → Bool := fun x y => decide (x ≠ y)

/-- Every pair. -/
def everyPair : Nat → Nat → Bool := fun _ _ => true

/-- No pair. -/
def noPair : Nat → Nat → Bool := fun _ _ => false

theorem selfOnly_visible : separable (encode (two selfOnly)) 0 1 :=
  (encode_separable_iff _ 0 1).mpr (by decide)

theorem linkOnly_visible : separable (encode (two linkOnly)) 0 1 :=
  (encode_separable_iff _ 0 1).mpr (by decide)

theorem selfAndLink_visible : separable (encode (two selfAndLink)) 0 1 :=
  (encode_separable_iff _ 0 1).mpr (by decide)

theorem bothLinks_visible : separable (encode (two bothLinks)) 0 1 :=
  (encode_separable_iff _ 0 1).mpr (by decide)

theorem everyPair_collapsed : collapsed (encode (two everyPair)) 0 1 :=
  (encode_collapsed_iff _ 0 1).mpr (by decide)

theorem noPair_collapsed : collapsed (encode (two noPair)) 0 1 :=
  (encode_collapsed_iff _ 0 1).mpr (by decide)

/-- **A bare witness leaves the pair invisible**: the constant relation
asserts the designated pair, and the pair is collapsed. -/
theorem witness_alone_invisible :
    PrimitiveCore.W (toSetting (two everyPair)) ∧ collapsed (encode (two everyPair)) 0 1 :=
  ⟨rfl, everyPair_collapsed⟩

/-- The symmetric irreflexive relation on two points is A and internal. -/
theorem bothLinks_A : PrimitiveCore.A (toSetting (two bothLinks)) :=
  (A_iff _).mpr (by decide)

/-! ## 5. The engine at an encoded pair -/

theorem encode_good (F : FiniteSetting) : Good (encode F) :=
  ⟨encode_wf F, rfl, fun _ hq => absurd hq List.not_mem_nil⟩

/-- At the encoded pair, the mark, the link and the self-instance on a fresh
form are valid responses (the sealed seed's three first-round classes). -/
theorem seed_embeds (F : FiniteSetting) (hab : F.a ≠ F.b) :
    validResponse (encode F) F.a F.b [.newForm 1, .newInst (encode F).forms.length [F.a]] ∧
    validResponse (encode F) F.a F.b [.newForm 2, .newInst (encode F).forms.length [F.a, F.b]] ∧
    validResponse (encode F) F.a F.b [.newForm 2, .newInst (encode F).forms.length [F.a, F.a]] :=
  bare_round_embeds (encode F) (encode_good F) F.a F.b F.a_lt F.b_lt hab

/-- A separable pair admits no firing: the seed round needs a collapsed target. -/
theorem no_fire_of_separable {m : Measure} {r : Regime} {i j : Nat} {δ : List Item}
    {t : Regime} (h : separable r i j) : ¬ Fire m r i j δ t :=
  fun hf => separable_not_collapsed h hf.2.2.1

/-- Separability is symmetric. -/
theorem separable_symm {r : Regime} {x y : Nat} (h : separable r x y) : separable r y x := by
  obtain ⟨c, hc, hne⟩ := h
  exact ⟨c, hc, fun h' => hne h'.symm⟩

theorem A_separable_rev (F : FiniteSetting) (h : PrimitiveCore.A (toSetting F)) :
    separable (encode F) F.b F.a :=
  separable_symm (A_separable F h)

/-- **At a witnessed irreflexive pair the engine has nothing to do**, whichever
of the two endpoints the engine orders first. -/
theorem A_no_fire (F : FiniteSetting) (h : PrimitiveCore.A (toSetting F)) (m : Measure)
    (δ : List Item) (t : Regime) :
    ¬ Fire m (encode F) F.a F.b δ t ∧ ¬ Fire m (encode F) F.b F.a δ t :=
  ⟨no_fire_of_separable (A_separable F h), no_fire_of_separable (A_separable_rev F h)⟩

/-- At a collapsed pair, a valid one-instance response is a minimum under
both measures. -/
theorem one_inst_min (m : Measure) {r : Regime} {i j f : Nat} {args : List Nat}
    (hc : collapsed r i j) (hv : validResponse r i j [.newInst f args]) :
    IsMin m r i j [.newInst f args] := by
  refine ⟨⟨by show 1 ≤ 2; decide, fun a ha => ?_⟩, hv, ?_⟩
  · rcases List.mem_cons.mp ha with h | h
    · cases h
    · exact absurd h List.not_mem_nil
  · intro δ' _ hv'
    cases δ' with
    | nil =>
        obtain ⟨s, hs, hsep, _⟩ := hv'
        have hsr : s = r := (Option.some.inj hs).symm
        subst hsr
        exact absurd hsep (fun h => separable_not_collapsed h hc)
    | cons it rest =>
        cases m with
        | mu1 =>
            show 1 < (it :: rest).length ∨ (1 = (it :: rest).length ∧ 0 ≤ 0)
            cases rest with
            | nil => exact Or.inr ⟨rfl, Nat.le_refl 0⟩
            | cons _ _ => exact Or.inl (Nat.succ_lt_succ (Nat.succ_pos _))
        | mu2 =>
            show 1 < (it :: rest).length ∨ (1 = (it :: rest).length ∧ 0 ≤ aritySum (it :: rest))
            cases rest with
            | nil => exact Or.inr ⟨rfl, Nat.zero_le _⟩
            | cons _ _ => exact Or.inl (Nat.succ_lt_succ (Nat.succ_pos _))

/-! ## 6. Absent instances at a collapsed pair -/

/-- Derivability after admitting one absent instance: the old derivable
instances and the new one. -/
theorem derivable_add {r : Regime} {p : Inst} (hp : p ∉ r.insts) (x : Inst) :
    derivable { r with insts := insertNew r.insts p } x ↔ derivable r x ∨ x = p := by
  show (x ∈ insertNew r.insts p ∨ x.1 ∈ r.rules) ↔ (x ∈ r.insts ∨ x.1 ∈ r.rules) ∨ x = p
  rw [insertNew_of_not_mem hp, List.mem_append, List.mem_singleton]
  constructor
  · rintro ((h | h) | h)
    · exact Or.inl (Or.inl h)
    · exact Or.inr h
    · exact Or.inl (Or.inr h)
  · rintro ((h | h) | h)
    · exact Or.inl (Or.inl h)
    · exact Or.inr h
    · exact Or.inl (Or.inr h)

theorem applyItem_newInst {r : Regime} {f : Nat} {args : List Nat}
    (hf : f < r.forms.length) (hlen : args.length = r.forms.getD f 0)
    (hargs : ∀ x ∈ args, x < r.data) :
    applyItem r (.newInst f args) = some { r with insts := insertNew r.insts (f, args) } := by
  show (if f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧ (∀ x ∈ args, x < r.data)
      then some { r with insts := insertNew r.insts (f, args) } else none) = _
  rw [if_pos ⟨hf, hlen, hargs⟩]

/-- **An absent link is a valid response at a collapsed pair** of a binary
regime without standing requirements: the row context at the second datum
sees the link present and the second self-instance absent (collapse forced
that self-instance absent through the same context). -/
theorem link_valid {r : Regime} (hb : Binary r) (hq : r.reqs = []) {i j f : Nat}
    (hi : i < r.data) (hj : j < r.data) (hij : i ≠ j) (hf : f < r.forms.length)
    (hc : collapsed r i j) (habs : ¬ derivable r (f, [i, j])) :
    validResponse r i j [.newInst f [i, j]] := by
  have hmem : ((f, [i, j]) : Inst) ∉ r.insts := fun h => habs (Or.inl h)
  have hjj : ¬ derivable r (f, [j, j]) := fun h =>
    habs ((hc ⟨f, [none, some j]⟩ (wfCtx_row hb hf hj)).mpr h)
  refine ⟨{ r with insts := insertNew r.insts (f, [i, j]) }, ?_, ?_, ?_⟩
  · rw [applyDelta_single]
    exact applyItem_newInst hf (by rw [binary_getD hb hf]; rfl) (two_args_lt hi hj)
  · refine ⟨⟨f, [none, some j]⟩, wfCtx_row hb hf hj, ?_⟩
    show ¬ (derivable _ (f, [i, j]) ↔ derivable _ (f, [j, j]))
    rw [derivable_add hmem, derivable_add hmem]
    intro hiff
    rcases hiff.mp (Or.inr rfl) with h | h
    · exact hjj h
    · injection h with _ h2
      exact hij (list_two_inj h2).1.symm
  · intro q hq'
    rw [hq] at hq'
    exact absurd hq' List.not_mem_nil

/-- **An absent self-instance is a valid response at a collapsed pair**: the
column context at the first datum sees it present and the link absent. -/
theorem self_valid {r : Regime} (hb : Binary r) (hq : r.reqs = []) {i j f : Nat}
    (hi : i < r.data) (hij : i ≠ j) (hf : f < r.forms.length)
    (hc : collapsed r i j) (habs : ¬ derivable r (f, [i, i])) :
    validResponse r i j [.newInst f [i, i]] := by
  have hmem : ((f, [i, i]) : Inst) ∉ r.insts := fun h => habs (Or.inl h)
  have hij' : ¬ derivable r (f, [i, j]) := fun h =>
    habs ((hc ⟨f, [some i, none]⟩ (wfCtx_column hb hf hi)).mpr h)
  refine ⟨{ r with insts := insertNew r.insts (f, [i, i]) }, ?_, ?_, ?_⟩
  · rw [applyDelta_single]
    exact applyItem_newInst hf (by rw [binary_getD hb hf]; rfl) (two_args_lt hi hi)
  · refine ⟨⟨f, [some i, none]⟩, wfCtx_column hb hf hi, ?_⟩
    show ¬ (derivable _ (f, [i, i]) ↔ derivable _ (f, [i, j]))
    rw [derivable_add hmem, derivable_add hmem]
    intro hiff
    rcases hiff.mp (Or.inr rfl) with h | h
    · exact hij' h
    · injection h with _ h2
      exact hij (list_two_inj h2).2.symm
  · intro q hq'
    rw [hq] at hq'
    exact absurd hq' List.not_mem_nil

/-- Every absent link at a collapsed pair is a minimum under both measures. -/
theorem link_min (m : Measure) {r : Regime} (hb : Binary r) (hq : r.reqs = []) {i j f : Nat}
    (hi : i < r.data) (hj : j < r.data) (hij : i ≠ j) (hf : f < r.forms.length)
    (hc : collapsed r i j) (habs : ¬ derivable r (f, [i, j])) :
    IsMin m r i j [.newInst f [i, j]] :=
  one_inst_min m hc (link_valid hb hq hi hj hij hf hc habs)

/-- Every absent self-instance at a collapsed pair is a minimum under both
measures. -/
theorem self_min (m : Measure) {r : Regime} (hb : Binary r) (hq : r.reqs = []) {i j f : Nat}
    (hi : i < r.data) (hij : i ≠ j) (hf : f < r.forms.length)
    (hc : collapsed r i j) (habs : ¬ derivable r (f, [i, i])) :
    IsMin m r i j [.newInst f [i, i]] :=
  one_inst_min m hc (self_valid hb hq hi hij hf hc habs)

/-- On an encoded setting whose designated pair is collapsed, an absent link
on any form is a minimum response. -/
theorem encode_link_min (F : FiniteSetting) (m : Measure) {f : Nat}
    (hf : f < (encode F).forms.length) (hab : F.a ≠ F.b)
    (hc : collapsed (encode F) F.a F.b) (habs : ¬ derivable (encode F) (f, [F.a, F.b])) :
    IsMin m (encode F) F.a F.b [.newInst f [F.a, F.b]] :=
  link_min m (encode_binary F) rfl F.a_lt F.b_lt hab hf hc habs

/-- On an encoded setting whose designated pair is collapsed, an absent
self-instance on any form is a minimum response. -/
theorem encode_self_min (F : FiniteSetting) (m : Measure) {f : Nat}
    (hf : f < (encode F).forms.length) (hab : F.a ≠ F.b)
    (hc : collapsed (encode F) F.a F.b) (habs : ¬ derivable (encode F) (f, [F.a, F.a])) :
    IsMin m (encode F) F.a F.b [.newInst f [F.a, F.a]] :=
  self_min m (encode_binary F) rfl F.a_lt hab hf hc habs

/-! ## 7. The exhibits fired -/

/-- The state after the seed round on the two-point setting with no
assertion, answered by the self-instance. -/
def noPairSelf : Regime := ⟨2, [2, 2, 2], [(0, [0, 0])], [], [(0, 1)]⟩

/-- The same, answered by the link. -/
def noPairLink : Regime := ⟨2, [2, 2, 2], [(0, [0, 1])], [], [(0, 1)]⟩

theorem noPair_self_valid : validResponse (encode (two noPair)) 0 1 [.newInst 0 [0, 0]] :=
  self_valid (encode_binary _) rfl (by decide) (by decide) (by decide) noPair_collapsed (by decide)

theorem noPair_link_valid : validResponse (encode (two noPair)) 0 1 [.newInst 0 [0, 1]] :=
  link_valid (encode_binary _) rfl (by decide) (by decide) (by decide) (by decide)
    noPair_collapsed (by decide)

/-- **The self-instance is a minimum response at the two-point pair with no
assertion.** -/
theorem noPair_fires_self (m : Measure) :
    Fire m (encode (two noPair)) 0 1 [.newInst 0 [0, 0]] noPairSelf :=
  ⟨by decide, by decide, noPair_collapsed, one_inst_min m noPair_collapsed noPair_self_valid,
   by decide⟩

/-- **The link is a minimum response at the two-point pair with no
assertion.** -/
theorem noPair_fires_link (m : Measure) :
    Fire m (encode (two noPair)) 0 1 [.newInst 0 [0, 1]] noPairLink :=
  ⟨by decide, by decide, noPair_collapsed, one_inst_min m noPair_collapsed noPair_link_valid,
   by decide⟩

theorem noPair_rooted_self (m : Measure) (supply : Bool) :
    Rooted m supply (encode (two noPair)) (0, 1) noPairSelf :=
  Rooted.seed (noPair_fires_self m)

theorem noPair_rooted_link (m : Measure) (supply : Bool) :
    Rooted m supply (encode (two noPair)) (0, 1) noPairLink :=
  Rooted.seed (noPair_fires_link m)

/-- The state after the seed round on the constant two-point relation,
answered by a self-instance on the empty retention form. -/
def everyPairFired : Regime :=
  ⟨2, [2, 2, 2], [(0, [0, 0]), (0, [0, 1]), (0, [1, 0]), (0, [1, 1]), (1, [0, 0])], [], [(0, 1)]⟩

theorem everyPair_self_valid :
    validResponse (encode (two everyPair)) 0 1 [.newInst 1 [0, 0]] :=
  self_valid (encode_binary _) rfl (by decide) (by decide) (by decide) everyPair_collapsed
    (by decide)

/-- **Where the asserted relation is constant across the pair, a self-instance
on the empty retention form is a minimum response.** -/
theorem everyPair_fires (m : Measure) :
    Fire m (encode (two everyPair)) 0 1 [.newInst 1 [0, 0]] everyPairFired :=
  ⟨by decide, by decide, everyPair_collapsed,
   one_inst_min m everyPair_collapsed everyPair_self_valid, by decide⟩

end Visible

#print axioms Visible.binary_getD
#print axioms Visible.two_slots
#print axioms Visible.wfCtx_binary
#print axioms Visible.wfCtx_row
#print axioms Visible.wfCtx_column
#print axioms Visible.plug_slots
#print axioms Visible.visible_of_ctx
#print axioms Visible.separable_iff_visible
#print axioms Visible.collapsed_iff_not_visible
#print axioms Visible.visible_iff_rows_columns
#print axioms Visible.encode_binary
#print axioms Visible.encode_separable_iff
#print axioms Visible.encode_collapsed_iff
#print axioms Visible.encode_form0_lt
#print axioms Visible.A_separable
#print axioms Visible.selfOnly_visible
#print axioms Visible.linkOnly_visible
#print axioms Visible.selfAndLink_visible
#print axioms Visible.bothLinks_visible
#print axioms Visible.everyPair_collapsed
#print axioms Visible.noPair_collapsed
#print axioms Visible.witness_alone_invisible
#print axioms Visible.bothLinks_A
#print axioms Visible.encode_good
#print axioms Visible.seed_embeds
#print axioms Visible.no_fire_of_separable
#print axioms Visible.separable_symm
#print axioms Visible.A_separable_rev
#print axioms Visible.A_no_fire
#print axioms Visible.one_inst_min
#print axioms Visible.derivable_add
#print axioms Visible.applyItem_newInst
#print axioms Visible.link_valid
#print axioms Visible.self_valid
#print axioms Visible.link_min
#print axioms Visible.self_min
#print axioms Visible.encode_link_min
#print axioms Visible.encode_self_min
#print axioms Visible.noPair_self_valid
#print axioms Visible.noPair_link_valid
#print axioms Visible.noPair_fires_self
#print axioms Visible.noPair_fires_link
#print axioms Visible.noPair_rooted_self
#print axioms Visible.noPair_rooted_link
#print axioms Visible.everyPair_self_valid
#print axioms Visible.everyPair_fires
