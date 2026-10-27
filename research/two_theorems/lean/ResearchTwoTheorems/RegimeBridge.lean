import Derivation.Basic
import Derivation.Represented
import Derivation.Compression
import ResearchTwoTheorems.Observer
import ResearchTwoTheorems.Institution

/-!
# The regime as an observer of its admitted data

Genesis's `collapsed` and `separable` (in `Derivation.Basic`) are judgments
about a regime and two data: no well-formed context separates them by
positive derivability, or some context does.  The observer calculus of this
tree speaks of views and verdicts.  This module is the bridge.

* The *admitted carrier* of a regime is `List.range r.data`: its data are
  the indices below the count.  Every statement below is about admitted
  data; off the carrier the regime's observer reads carrier membership, not
  derivability (`not_mem_ctxView_of_unadmitted`).
* Each well-formed context cuts a view out of the admitted carrier: the
  admitted data whose plugging is derivable.  The regime's observer is the
  list of these views, relative to a list `cs` enumerating the regime's
  well-formed contexts.  Such an enumeration exists (the ignition tree's
  `ctxList` with `mem_ctxList`); this tree does not import it, and states
  the bridge for any `cs` with `∀ c, c ∈ cs ↔ wfCtx r c`.
* On admitted data the regime's observer separates exactly when Genesis
  declares `separable` and merges exactly when Genesis declares
  `collapsed`; collapse is signature equality for the regime's questions.

The contrast the bridge makes formal: an observer's verdicts are monotone in
its views (`verdict_mono`, with `information_mono` in `Institution`), while
admissions are not additions of views.  A regime that collapses an admitted
pair an earlier regime separated has lost or altered one of the earlier
regime's views (`recollapse_changes_views`); the two-datum witness regimes
`R0` and `R0rule` show it happening under one rule admission.
-/

namespace ResearchTwoTheorems.RegimeBridge

open Derivation Represented Compression Institution

/-- The admitted carrier of a regime: its data are the indices below the
count. -/
def admitted (r : Regime) : List Nat := List.range r.data

theorem mem_admitted (r : Regime) (d : Nat) : d ∈ admitted r ↔ d < r.data :=
  List.mem_range

/-- The view a context cuts out of the admitted carrier: the admitted data
whose plugging is derivable. -/
def ctxView (r : Regime) (c : Ctx) : View :=
  (admitted r).filter (fun d => decide (derivable r (plug c d)))

theorem mem_ctxView {r : Regime} {c : Ctx} {d : Nat} (hd : d < r.data) :
    d ∈ ctxView r c ↔ derivable r (plug c d) := by
  unfold ctxView
  rw [List.mem_filter]
  constructor
  · intro h
    exact of_decide_eq_true h.2
  · intro h
    exact ⟨(mem_admitted r d).mpr hd, decide_eq_true h⟩

/-- Off the admitted carrier a datum lies in no view of the regime, whatever
its derivability: the observer reads admission first. -/
theorem not_mem_ctxView_of_unadmitted {r : Regime} (c : Ctx) {d : Nat}
    (hd : ¬ d < r.data) : d ∉ ctxView r c := by
  intro h
  exact hd ((mem_admitted r d).mp (List.mem_filter.mp h).1)

/-- The regime's observer, relative to a list of its well-formed contexts. -/
def regimeViews (r : Regime) (cs : List Ctx) : Evaluator := cs.map (ctxView r)

theorem sep_ctxView {r : Regime} (c : Ctx) {a b : Nat} (ha : a < r.data)
    (hb : b < r.data) :
    sepB (ctxView r c) a b = true ↔
      ¬ (derivable r (plug c a) ↔ derivable r (plug c b)) := by
  constructor
  · intro h hiff
    have hf : sepB (ctxView r c) a b = false :=
      (sepB_eq_false_iff _ a b).mpr
        ((mem_ctxView ha).trans (hiff.trans (mem_ctxView hb).symm))
    rw [hf] at h
    exact Bool.noConfusion h
  · intro h
    cases hs : sepB (ctxView r c) a b with
    | true => rfl
    | false =>
      exact absurd
        ((mem_ctxView ha).symm.trans (((sepB_eq_false_iff _ a b).mp hs).trans (mem_ctxView hb)))
        h

/-- **The bridge, positive half.**  When `cs` enumerates the well-formed
contexts of `r`, the regime's observer separates two admitted data exactly
when Genesis declares them separable. -/
theorem verdict_regime_iff (r : Regime) (cs : List Ctx)
    (hcs : ∀ c, c ∈ cs ↔ wfCtx r c) {a b : Nat} (ha : a < r.data) (hb : b < r.data) :
    verdictB (regimeViews r cs) a b = true ↔ separable r a b := by
  unfold verdictB regimeViews
  rw [List.any_map, List.any_eq_true]
  constructor
  · intro h
    obtain ⟨c, hc, hs⟩ := h
    exact ⟨c, (hcs c).mp hc, (sep_ctxView c ha hb).mp hs⟩
  · intro h
    obtain ⟨c, hwf, hne⟩ := h
    exact ⟨c, (hcs c).mpr hwf, (sep_ctxView c ha hb).mpr hne⟩

/-- **The bridge, negative half.**  The regime's observer merges two admitted
data exactly when Genesis declares them collapsed. -/
theorem collapsed_iff_verdict_false (r : Regime) (cs : List Ctx)
    (hcs : ∀ c, c ∈ cs ↔ wfCtx r c) {a b : Nat} (ha : a < r.data) (hb : b < r.data) :
    collapsed r a b ↔ verdictB (regimeViews r cs) a b = false := by
  constructor
  · intro h
    cases hv : verdictB (regimeViews r cs) a b with
    | false => rfl
    | true =>
      obtain ⟨c, hwf, hne⟩ := (verdict_regime_iff r cs hcs ha hb).mp hv
      exact absurd (h c hwf) hne
  · intro hv c hwf
    cases hs : sepB (ctxView r c) a b with
    | false =>
      exact (mem_ctxView ha).symm.trans (((sepB_eq_false_iff _ a b).mp hs).trans (mem_ctxView hb))
    | true =>
      have ht : verdictB (regimeViews r cs) a b = true := by
        unfold verdictB regimeViews
        rw [List.any_map, List.any_eq_true]
        exact ⟨c, (hcs c).mpr hwf, hs⟩
      rw [ht] at hv
      exact Bool.noConfusion hv

/-- Collapse is signature equality for the regime's questions. -/
theorem collapsed_iff_sigEq (r : Regime) (cs : List Ctx)
    (hcs : ∀ c, c ∈ cs ↔ wfCtx r c) {a b : Nat} (ha : a < r.data) (hb : b < r.data) :
    collapsed r a b ↔ SigEq (questions (regimeViews r cs)) a b := by
  rw [collapsed_iff_verdict_false r cs hcs ha hb, verdictB_false_iff_sigEq]

/-! ## The regime's observer on its admitted carrier -/

/-- The regime's own observer is sharp for an actor exactly when collapse
coincides with the actor's fibers on the admitted carrier. -/
theorem sharp_regime_iff (r : Regime) (cs : List Ctx)
    (hcs : ∀ c, c ∈ cs ↔ wfCtx r c) (p : Presentation) :
    Sharp (admitted r) (regimeViews r cs) p ↔
      ∀ a, a < r.data → ∀ b, b < r.data → (collapsed r a b ↔ p a = p b) := by
  unfold Sharp
  constructor
  · intro h a ha b hb
    rw [collapsed_iff_verdict_false r cs hcs ha hb]
    exact h a ((mem_admitted r a).mpr ha) b ((mem_admitted r b).mpr hb)
  · intro h a ha b hb
    have ha' := (mem_admitted r a).mp ha
    have hb' := (mem_admitted r b).mp hb
    rw [← collapsed_iff_verdict_false r cs hcs ha' hb']
    exact h a ha' b hb'

/-- A regime knows a question (in the sense of `Institution.Knows`, with the
regime's questions as the institution) exactly when the question respects
collapse on the admitted carrier. -/
theorem regime_knows_iff (r : Regime) (cs : List Ctx)
    (hcs : ∀ c, c ∈ cs ↔ wfCtx r c) (q : Nat → Nat) :
    Knows (admitted r) (questions (regimeViews r cs)) q ↔
      ∀ a, a < r.data → ∀ b, b < r.data → collapsed r a b → q a = q b := by
  rw [knows_iff_determined]
  constructor
  · intro h a ha b hb hc
    exact h a ((mem_admitted r a).mpr ha) b ((mem_admitted r b).mpr hb)
      ((collapsed_iff_sigEq r cs hcs ha hb).mp hc)
  · intro h a ha b hb hs
    have ha' := (mem_admitted r a).mp ha
    have hb' := (mem_admitted r b).mp hb
    exact h a ha' b hb' ((collapsed_iff_sigEq r cs hcs ha' hb').mpr hs)

/-- The regime's information: the number of its observational classes on the
admitted carrier. -/
def regimeInformation (r : Regime) (cs : List Ctx) : Nat :=
  information (admitted r) (questions (regimeViews r cs))

/-- A regime with `n` well-formed contexts has at most `2 ^ n` observational
classes, and never more than it has data. -/
theorem regimeInformation_le (r : Regime) (cs : List Ctx) :
    regimeInformation r cs ≤ 2 ^ cs.length ∧ regimeInformation r cs ≤ r.data := by
  unfold regimeInformation
  constructor
  · have h := information_le_resolution (admitted r) (regimeViews r cs)
    have hl : (regimeViews r cs).length = cs.length := by
      simp [regimeViews]
    rw [hl] at h
    exact h
  · have h := information_le_carrier (admitted r) (questions (regimeViews r cs))
    have hl : (admitted r).length = r.data := by
      simp [admitted]
    rw [hl] at h
    exact h

/-! ## Views against admissions -/

/-- More views, no fewer separations: an observer's verdicts are monotone in
its views. -/
theorem verdict_mono {E E' : Evaluator} (h : ∀ c, c ∈ E → c ∈ E') {a b : Nat}
    (hv : verdictB E a b = true) : verdictB E' a b = true := by
  unfold verdictB at hv ⊢
  obtain ⟨c, hc, hs⟩ := List.any_eq_true.mp hv
  exact List.any_eq_true.mpr ⟨c, h c hc, hs⟩

/-- **Admissions are not additions of views.**  A regime that collapses an
admitted pair which an earlier regime separated has lost or altered one of
the earlier regime's views.  Had every earlier view survived, monotonicity
would have kept the pair separated. -/
theorem recollapse_changes_views (r r' : Regime) (cs cs' : List Ctx)
    (hcs : ∀ c, c ∈ cs ↔ wfCtx r c) (hcs' : ∀ c, c ∈ cs' ↔ wfCtx r' c)
    {a b : Nat} (ha : a < r.data) (hb : b < r.data) (ha' : a < r'.data) (hb' : b < r'.data)
    (hsep : separable r a b) (hcol : collapsed r' a b) :
    ∃ v, v ∈ regimeViews r cs ∧ v ∉ regimeViews r' cs' := by
  have hv : verdictB (regimeViews r cs) a b = true :=
    (verdict_regime_iff r cs hcs ha hb).mpr hsep
  have hv' : verdictB (regimeViews r' cs') a b = false :=
    (collapsed_iff_verdict_false r' cs' hcs' ha' hb').mp hcol
  cases hall : (regimeViews r cs).all (fun v => decide (v ∈ regimeViews r' cs')) with
  | true =>
    have hsub : ∀ v, v ∈ regimeViews r cs → v ∈ regimeViews r' cs' := by
      intro v hv0
      exact of_decide_eq_true (List.all_eq_true.mp hall v hv0)
    have ht := verdict_mono hsub hv
    rw [ht] at hv'
    exact Bool.noConfusion hv'
  | false =>
    obtain ⟨v, hv0, hf⟩ := all_false_witness _ _ hall
    exact ⟨v, hv0, of_decide_eq_false hf⟩

/-! ## A two-datum witness -/

/-- Two data, one unary form, the instance `0 [0]`, no rule. -/
def R0 : Regime := ⟨2, [1], [(0, [0])], [], []⟩

/-- `R0` with the uniform rule on its form. -/
def R0rule : Regime := ⟨2, [1], [(0, [0])], [0], []⟩

/-- Every well-formed context of a one-unary-form regime is `⟨0, [none]⟩`. -/
theorem ctx_unary {r : Regime} (hf : r.forms = [1]) {c : Ctx}
    (hc : wfCtx r c) : c = ⟨0, [none]⟩ := by
  obtain ⟨h1, h2, h3, _⟩ := hc
  rw [hf] at h1 h2
  have h0 : c.form = 0 := by
    simp at h1
    exact h1
  rw [h0] at h2
  cases c with
  | mk form slots =>
    simp only at h0 h2 h3
    subst h0
    match slots, h2, h3 with
    | [x], _, h3 =>
      have : x = none := by
        simp at h3
        exact h3.symm
      subst this
      rfl

/-- The one-context enumeration of a one-unary-form regime. -/
theorem unary_enumeration {r : Regime} (hf : r.forms = [1]) :
    ∀ c, c ∈ [(⟨0, [none]⟩ : Ctx)] ↔ wfCtx r c := by
  intro c
  constructor
  · intro hc
    have hc' : c = ⟨0, [none]⟩ := List.mem_singleton.mp hc
    subst hc'
    unfold wfCtx
    rw [hf]
    refine ⟨by decide, by decide, by decide, ?_⟩
    intro s hs
    have hs' : s = none := List.mem_singleton.mp hs
    subst hs'
    trivial
  · intro hc
    rw [ctx_unary hf hc]
    exact List.mem_singleton_self _

theorem R0_separable : separable R0 0 1 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩

theorem R0rule_collapsed : collapsed R0rule 0 1 := by
  intro c hc
  rw [ctx_unary rfl hc]
  decide

/-- The rule admission turns the view `[0]` into the view `[0, 1]`: a view
is altered, not added. -/
theorem recollapse_witness :
    regimeViews R0 [⟨0, [none]⟩] = [[0]] ∧ regimeViews R0rule [⟨0, [none]⟩] = [[0, 1]] ∧
      verdictB (regimeViews R0 [⟨0, [none]⟩]) 0 1 = true ∧
      verdictB (regimeViews R0rule [⟨0, [none]⟩]) 0 1 = false := by
  decide

/-- The general theorem applied to the witness: a view of `R0` is not a view
of `R0rule`. -/
theorem recollapse_witness_changes_views :
    ∃ v, v ∈ regimeViews R0 [⟨0, [none]⟩] ∧ v ∉ regimeViews R0rule [⟨0, [none]⟩] :=
  recollapse_changes_views R0 R0rule _ _ (unary_enumeration rfl) (unary_enumeration rfl)
    (by decide) (by decide) (by decide) (by decide) R0_separable R0rule_collapsed

end ResearchTwoTheorems.RegimeBridge
