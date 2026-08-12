/-!
# Primitive Difference

Candidates for the weakest formal object deserving the name *primitive
difference*, before contexts, profiles, observers, quotients, or repairs
exist.  Self-contained: nothing here imports or assumes the regime model
of the earlier development.

Metatheory used (declared): types, functions, one binary relation symbol
per structure, propositional logic, and finite case analysis.  No
quotient machinery, no context spaces, no state.

Candidate glossary (paper: `paper/primitive_difference.md`):

* A1  — positive apartness datum: a relation with one asserted pair,
        no axioms;
* A1i — A1 plus irreflexivity;
* A2  — witnessed non-identification: witness multiplicities over pairs;
* A3  — non-factorization through a point (= metatheoretic inequality);
* A4  — irreducibility under an admitted operation family;
* A5  — the two-element carriers: oriented `D2` and symmetric `S2`.
-/

namespace PrimDiff

/-- Irreflexivity: the weakest object-level fidelity commitment studied
here. -/
def Irrefl {α : Type} (r : α → α → Prop) : Prop := ∀ x, ¬ r x x

/-- Symmetrization of a relation. -/
def Sym {α : Type} (r : α → α → Prop) : α → α → Prop :=
  fun x y => r x y ∨ r y x

/-- Transpose of a relation. -/
def Transpose {α : Type} (r : α → α → Prop) : α → α → Prop :=
  fun x y => r y x

/-! ## A1 versus A3: assertion versus metatheoretic inequality -/

/-- Soundness from irreflexivity (A1i → A3): an irreflexive witnessed
pair is metatheoretically distinct. -/
theorem irrefl_witness_ne {α : Type} {r : α → α → Prop} (hi : Irrefl r)
    {a b : α} (h : r a b) : a ≠ b :=
  fun he => hi b (he ▸ h)

/-- Countermodel (A1 ⇏ A3): bare assertion is consistent with
metatheoretic identity — the one-point carrier hosts a self-difference. -/
theorem selfdiff_consistent :
    ∃ r : Unit → Unit → Prop, r () () :=
  ⟨fun _ _ => True, trivial⟩

/-- Countermodel (symmetry does not restore soundness): the self-difference
model is symmetric.  Among {no axiom, symmetry, irreflexivity}, only
irreflexivity entails metatheoretic inequality. -/
theorem symm_selfdiff_consistent :
    ∃ r : Unit → Unit → Prop,
      (∀ x y, r x y → r y x) ∧ r () () :=
  ⟨fun _ _ => True, fun _ _ h => h, trivial⟩

/-- Countermodel (A3 ⇏ A1): metatheoretic inequality with an empty
relation — a difference that exists outside the object language is not
thereby admitted inside it. -/
theorem meta_diff_without_assertion :
    ∃ r : Bool → Bool → Prop,
      ¬ r false true ∧ false ≠ true :=
  ⟨fun _ _ => False, id, Bool.noConfusion⟩

/-- A3 stated as non-factorization: the selection of `a` and `b` factors
through the one-point carrier exactly when they are metatheoretically
equal.  Non-factorization is therefore *definitionally* metatheoretic
inequality once function composition is admitted. -/
theorem factors_through_point_iff {α : Type} (a b : α) :
    (∃ p : Unit → α, p () = a ∧ p () = b) ↔ a = b := by
  constructor
  · intro ⟨p, h1, h2⟩
    exact h1.symm.trans h2
  · intro he
    exact ⟨fun _ => a, rfl, he ▸ rfl⟩

/-! ## The one-point bound and the two-element carriers -/

/-- With irreflexivity admitted, no witnessed pair lives on a subsingleton
carrier: the two-element carrier is forced. -/
theorem no_witness_on_subsingleton {α : Type} [Subsingleton α]
    {r : α → α → Prop} (hi : Irrefl r) (a b : α) : ¬ r a b :=
  fun h => irrefl_witness_ne hi h (Subsingleton.elim a b)

/-- The oriented two-element difference: one edge, one orientation. -/
def D2 : Bool → Bool → Prop := fun x y => x = false ∧ y = true

/-- The reversed orientation. -/
def D2rev : Bool → Bool → Prop := fun x y => x = true ∧ y = false

/-- The symmetric two-element difference: the symmetrization of `D2`. -/
def S2 : Bool → Bool → Prop := Sym D2

instance (x y : Bool) : Decidable (D2 x y) := by
  unfold D2; infer_instance

instance (x y : Bool) : Decidable (D2rev x y) := by
  unfold D2rev; infer_instance

instance (x y : Bool) : Decidable (S2 x y) := by
  unfold S2 Sym; infer_instance

theorem D2_irrefl : Irrefl D2 := by
  intro x hx
  have h2 := hx.2
  rw [hx.1] at h2
  exact Bool.noConfusion h2

theorem S2_irrefl : Irrefl S2 := by
  intro x hx
  cases hx with
  | inl h => exact D2_irrefl x h
  | inr h => exact D2_irrefl x h

theorem D2_witness : D2 false true := by decide

/-- Initiality of the oriented two-element carrier among pointed witnessed
structures: for every structure with an asserted pair there is exactly one
point-preserving map from `D2`, and it preserves the oriented edge. -/
theorem D2_initial_pointed {α : Type} (r : α → α → Prop) (a b : α)
    (h : r a b) :
    ∃ f : Bool → α,
      (f false = a ∧ f true = b ∧ ∀ x y, D2 x y → r (f x) (f y)) ∧
      ∀ g : Bool → α, g false = a → g true = b →
        ∀ t, g t = f t := by
  refine ⟨fun t => cond t b a, ⟨rfl, rfl, ?_⟩, ?_⟩
  · intro x y hxy
    have hx : x = false := hxy.1
    have hy : y = true := hxy.2
    subst hx; subst hy
    simpa using h
  · intro g hga hgb t
    cases t with
    | false => exact hga
    | true => exact hgb

/-- Not forced without irreflexivity: the one-point self-difference model
already hosts an asserted pair (see `selfdiff_consistent`), so the
two-element carrier is *false as a necessity* for bare A1. -/
theorem one_point_hosts_bare_witness :
    ∃ r : Unit → Unit → Prop, r () () := selfdiff_consistent

/-- Merely minimal, not unique: witnessed irreflexive structures exist on
larger carriers (three-element example), so the two-element carrier is
sufficient and minimal but not exhaustive. -/
theorem larger_witnessed_carrier_exists :
    ∃ r : (Bool × Bool) → (Bool × Bool) → Prop,
      Irrefl r ∧ r (false, false) (true, false) := by
  refine ⟨fun x y => x = (false, false) ∧ y = (true, false), ?_, by decide⟩
  intro x hx
  have h1 := hx.1
  have h2 := hx.2
  rw [h1] at h2
  exact Bool.noConfusion (congrArg Prod.fst h2)

/-! ## Collapse: pushforward, clash, and the fidelity dichotomy -/

/-- Pushforward of a relation along a map (the collapsed structure's
relation).  This is a construction on relations and functions only — no
quotient machinery. -/
def Push {α β : Type} (r : α → α → Prop) (c : α → β) :
    β → β → Prop :=
  fun x y => ∃ u v, r u v ∧ c u = x ∧ c v = y

/-- A *collapse clash*: some asserted edge has both endpoints identified
by the map.  Stated positively (an existence), in the same spirit as
positive apartness. -/
def CollapseClash {α β : Type} (r : α → α → Prop) (c : α → β) : Prop :=
  ∃ u v, r u v ∧ c u = c v

/-- The witness survives every collapse: pushforward preserves the
asserted pair.  Bare assertion (A1) creates no obstruction to collapse —
the collapsed structure is again a bare-assertion structure. -/
theorem push_witness {α β : Type} {r : α → α → Prop} {a b : α}
    (h : r a b) (c : α → β) : Push r c (c a) (c b) :=
  ⟨a, b, h, rfl, rfl⟩

/-- The fidelity dichotomy, obstruction half: identifying a witnessed pair
clashes, and a clash destroys irreflexivity of the pushforward.  Under the
irreflexivity commitment, collapse of a witnessed pair is obstructed —
internally, with no external fidelity demand. -/
theorem clash_of_identifying_witness {α β : Type} {r : α → α → Prop}
    {a b : α} (h : r a b) {c : α → β} (hc : c a = c b) :
    CollapseClash r c :=
  ⟨a, b, h, hc⟩

theorem clash_not_irrefl {α β : Type} {r : α → α → Prop} {c : α → β}
    (h : CollapseClash r c) : ¬ Irrefl (Push r c) := by
  intro hi
  obtain ⟨u, v, huv, hc⟩ := h
  exact hi (c u) ⟨u, v, huv, rfl, hc.symm⟩

/-- The fidelity dichotomy, no-obstruction half: without irreflexivity the
collapse always succeeds — the one-point self-difference structure is a
legitimate bare-assertion structure, and every pushforward exists. -/
theorem collapse_unobstructed_without_fidelity :
    ∃ r : Unit → Unit → Prop, r () () := selfdiff_consistent

/-- Collapse clash is orientation-blind: transposing the relation changes
nothing about which maps clash.  Obstruction sees only the symmetrization
of a difference. -/
theorem clash_transpose_invariant {α β : Type} (r : α → α → Prop)
    (c : α → β) :
    CollapseClash r c ↔ CollapseClash (Transpose r) c := by
  constructor
  · intro ⟨u, v, huv, hc⟩
    exact ⟨v, u, huv, hc.symm⟩
  · intro ⟨u, v, huv, hc⟩
    exact ⟨v, u, huv, hc.symm⟩

/-- Orientation is real data at the assertion level: the oriented edge and
its reverse are not pointed-isomorphic (no point-preserving map carries
one onto the other), even though `clash_transpose_invariant` makes them
indistinguishable at the obstruction level. -/
theorem orientation_data_invisible_to_collapse :
    (∀ f : Bool → Bool,
      f false = false → f true = true →
        ¬ (∀ x y, D2 x y ↔ D2rev (f x) (f y))) ∧
    (CollapseClash D2 (fun _ => ()) ↔
      CollapseClash D2rev (fun _ => ())) := by
  constructor
  · intro f hf ht hiff
    have h := (hiff false true).mp (by decide)
    rw [hf, ht] at h
    exact absurd h (by decide)
  · constructor
    · intro _
      exact ⟨true, false, by decide, rfl⟩
    · intro _
      exact ⟨false, true, by decide, rfl⟩

/-! ## What an observer adds: the orientation gap -/

/-- On the symmetric two-element difference, every classifier that is
equivariant under the swap automorphism is constant: symmetric primitive
difference admits no definable observer.  The observer's content is
exactly an orientation-breaking choice. -/
theorem symmetric_no_equivariant_classifier :
    ∀ f : Bool → Bool, (∀ x, f (Bool.not x) = f x) → f false = f true := by
  intro f h
  have := h false
  simpa using this.symm

/-- The swap really is an automorphism of the symmetric structure. -/
theorem swap_is_S2_automorphism :
    ∀ x y, S2 x y ↔ S2 (Bool.not x) (Bool.not y) := by decide

/-- The oriented two-element difference is rigid: any endomap preserving
and reflecting the oriented edge is the identity.  In particular the
orientation itself already plays the observer's role. -/
theorem oriented_rigid (f : Bool → Bool)
    (hiff : ∀ x y, D2 x y ↔ D2 (f x) (f y)) : ∀ x, f x = x := by
  have h := (hiff false true).mp (by decide)
  intro x
  cases x with
  | false => exact h.1
  | true => exact h.2

/-- The oriented structure carries a separating classifier compatible with
its (trivial) automorphisms: oriented difference is self-observing. -/
theorem oriented_classifier_exists :
    ∃ f : Bool → Bool,
      (∀ x y, D2 x y ↔ D2 (f x) (f y)) ∧ f false ≠ f true :=
  ⟨id, fun _ _ => Iff.rfl, by decide⟩

/-! ## A2: witnessed non-identification and multiplicity -/

/-- A single witness for a single orientation is consistent: neither a
reverse witness nor a second same-orientation witness is forced. -/
theorem single_oriented_witness_consistent :
    ∃ W : Bool → Bool → Nat,
      W false true = 1 ∧ W true false = 0 :=
  ⟨fun x y => if x = false ∧ y = true then 1 else 0, by decide, by decide⟩

/-- Witness multiplicity is data invisible to the induced assertion: two
witness assignments with different multiplicities induce the same
presence relation.  A2 refines A1 with data, not with new distinctions. -/
theorem multiplicity_invisible_to_presence :
    ∃ W1 W2 : Bool → Bool → Nat,
      W1 ≠ W2 ∧ ∀ x y, (0 < W1 x y ↔ 0 < W2 x y) := by
  refine ⟨fun _ _ => 1, fun _ _ => 2, ?_, by decide⟩
  intro h
  have := congrFun (congrFun h false) false
  omega

/-! ## Repetition: occurrences, not identity -/

/-- Asserting an already-present pair again adds nothing at the
membership level. -/
theorem repetition_no_new_content {p : Nat × Nat}
    (L : List (Nat × Nat)) (h : p ∈ L) :
    ∀ q, q ∈ L ++ [p] ↔ q ∈ L := by
  intro q
  constructor
  · intro hq
    cases List.mem_append.mp hq with
    | inl hq => exact hq
    | inr hq =>
        have : q = p := by
          cases hq with
          | head => rfl
          | tail _ h => cases h
        exact this ▸ h
  · intro hq
    exact List.mem_append.mpr (Or.inl hq)

/-- Yet repetition is a genuinely new occurrence: the occurrence count
grows.  Repetition creates another occurrence, never an identity. -/
theorem repetition_new_occurrence (L : List (Nat × Nat))
    (p : Nat × Nat) : (L ++ [p]).length = L.length + 1 := by
  simp

/-! ## Faithfulness is a demand, not a fact -/

/-- Constant presentations into any irreflexive target lose every
asserted pair: unfaithful presentations exist, so preservation of a
distinction is an external demand on presentations. -/
theorem const_presentation_unfaithful {β : Type} {r' : β → β → Prop}
    (hi : Irrefl r') (v : β) : ¬ r' v v := hi v

/-- The identity presentation is faithful. -/
theorem id_presentation_faithful {α : Type} {r : α → α → Prop}
    {a b : α} (h : r a b) : r (id a) (id b) := h

/-! ## A4: irreducibility under an admitted operation family -/

/-- Closure of an operation family under identity and composition. -/
inductive Clos {α : Type} (F : (α → α) → Prop) : (α → α) → Prop where
  | base {f : α → α} : F f → Clos F f
  | id : Clos F id
  | comp {f g : α → α} : Clos F f → Clos F g → Clos F (f ∘ g)

/-- Irreducibility of a pair under an admitted family: no admitted
composite identifies the pair. -/
def Irred {α : Type} (F : (α → α) → Prop) (a b : α) : Prop :=
  ∀ f, Clos F f → f a ≠ f b

/-- The closure of the empty family is extensionally the identity. -/
theorem clos_empty_id {α : Type} :
    ∀ f, Clos (fun _ : α → α => False) f → ∀ x, f x = x := by
  intro f hf
  induction hf with
  | base h => exact h.elim
  | id => intro _; rfl
  | comp _ _ ihf ihg =>
      intro x
      show _ = x
      rw [Function.comp_apply, ihg, ihf]

/-- A4 over the empty family is exactly A3: with no admitted operations,
irreducibility is metatheoretic inequality. -/
theorem irred_empty_iff_ne {α : Type} (a b : α) :
    Irred (fun _ : α → α => False) a b ↔ a ≠ b := by
  constructor
  · intro h
    exact h id Clos.id
  · intro hne f hf he
    have ha := clos_empty_id f hf a
    have hb := clos_empty_id f hf b
    exact hne ((ha.symm.trans he).trans hb)

/-- Irreducibility is antitone in the admitted family: admitting more
operations can only erase differences. -/
theorem irred_antitone {α : Type} {F G : (α → α) → Prop}
    (hsub : ∀ f, F f → G f) {a b : α} (h : Irred G a b) :
    Irred F a b := by
  intro f hf
  refine h f ?_
  induction hf with
  | base hb => exact Clos.base (hsub _ hb)
  | id => exact Clos.id
  | comp _ _ ihf ihg => exact Clos.comp ihf ihg

/-- One admitted merger erases every difference it touches: A3 does not
imply A4 for nonempty families.  Relative to the full function family no
pair is irreducible — difference under A4 is family-relative all the way
down. -/
theorem merger_erases {α : Type} {F : (α → α) → Prop} {v : α}
    (hF : F (fun _ => v)) (a b : α) : ¬ Irred F a b :=
  fun h => h _ (Clos.base hF) rfl

end PrimDiff
