import ClosedFamily.Base

/-!
# Closing a declared family, and what a section owes the closure

The pinned `Family` says of itself: *"Nothing is assumed about closure
under composition or inverses; the family is exactly what it lists."*
So a section that is natural for a declared family is natural for a LIST
of isomorphisms, not for a structure closed under the operations
`PresIso` already carries (`refl`, `symm`, `trans`).  That gap is the
subject of this rung.

The closure is built here as a free construction, not assumed: `Path`
is the inductive type of finite words in the declared arrows and their
formal inverses, `pathIso` interprets a word by the pinned `refl`,
`symm`, and `trans`, and `closure D` is the declared family whose arrows
are exactly the words.

Two things are proved, and they pull in opposite directions:

* the closure is a genuine enlargement -- `closure_contains_inverse` and
  `closure_contains_composite` exhibit arrows in it that the declared
  family need not list; and
* **the enlargement costs a section nothing**.
  `natural_iff_natural_closure`: a section is natural for the closure
  exactly when it is natural for the declared family.  The obligations a
  section carries are unchanged by closing.

The operation laws -- associativity, both units, both inverses -- are
proved on the transported bundle map `mapPair`, which is the only thing
`IsNatural` reads.  They are NOT proved as equalities of `PresIso`
records, and no sentence here says they are.

`Sec (closure D)` and `Sec D` are the same type, by `rfl`
(`sec_closure_eq`): closing changes the arrows and not the objects.

AuthorityEffect: None.  Nothing here amends the sealed derivation, and
the pinned `Family` keeps its declared meaning; this rung adds a
construction beside it and measures the difference.
-/

namespace ClosedFamily
namespace Closure

variable {X R : Type}

/-! ## 1. Words in the declared arrows and their formal inverses -/

/-- A finite word from `a` to `b`: each step is a declared arrow taken
forwards or backwards.  Indexed by its endpoints, so no equality proof
between objects is ever needed and nothing is transported by hand. -/
inductive Path (D : Family X R) : D.Obj → D.Obj → Type where
  | nil (a : D.Obj) : Path D a a
  | cons (f : D.Arr) {c : D.Obj} (p : Path D (D.tgt f) c) : Path D (D.src f) c
  | consInv (f : D.Arr) {c : D.Obj} (p : Path D (D.src f) c) : Path D (D.tgt f) c

variable {D : Family X R}

/-- Concatenation of words. -/
def Path.comp : {a b c : D.Obj} → Path D a b → Path D b c → Path D a c
  | _, _, _, .nil _, q => q
  | _, _, _, .cons f p, q => .cons f (p.comp q)
  | _, _, _, .consInv f p, q => .consInv f (p.comp q)

/-- Reversal of a word, each step flipped. -/
def Path.inv : {a b : D.Obj} → Path D a b → Path D b a
  | _, _, .nil a => .nil a
  | _, _, .cons f p => p.inv.comp (.consInv f (.nil (D.src f)))
  | _, _, .consInv f p => p.inv.comp (.cons f (.nil (D.tgt f)))

/-- The single-step word on a declared arrow. -/
def Path.one (f : D.Arr) : Path D (D.src f) (D.tgt f) :=
  .cons f (.nil (D.tgt f))

/-- The single-step word on a declared arrow, taken backwards. -/
def Path.oneInv (f : D.Arr) : Path D (D.tgt f) (D.src f) :=
  .consInv f (.nil (D.src f))

/-! ## 2. Interpreting a word by the pinned operations -/

/-- A word is interpreted by the pinned identity, inverse, and
composition, and by nothing else. -/
def pathIso (D : Family X R) :
    {a b : D.Obj} → Path D a b → PresIso (D.obs a) (D.obs b)
  | _, _, .nil a => PresIso.refl (D.obs a)
  | _, _, .cons f p => (D.iso f).trans (pathIso D p)
  | _, _, .consInv f p => (D.iso f).symm.trans (pathIso D p)

/-! ## 3. The closed family -/

/-- The closure of a declared family: the same objects and the same
observers, with every word as an arrow. -/
def closure (D : Family X R) : Family X R where
  Obj := D.Obj
  obs := D.obs
  Arr := (a : D.Obj) × (b : D.Obj) × Path D a b
  src t := t.1
  tgt t := t.2.1
  iso t := pathIso D t.2.2

/-- Closing changes the arrows and not the objects, so the two families
have literally the same sections. -/
theorem sec_closure_eq (D : Family X R) : Sec (closure D) = Sec D := rfl

/-- Every declared arrow is an arrow of the closure. -/
def declared (f : D.Arr) : (closure D).Arr :=
  ⟨D.src f, D.tgt f, Path.one f⟩

/-- The closure is a genuine enlargement, first witness: the formal
inverse of every declared arrow is an arrow of the closure, running the
other way. -/
def closure_contains_inverse (f : D.Arr) : (closure D).Arr :=
  ⟨D.tgt f, D.src f, Path.oneInv f⟩

/-- The closure is a genuine enlargement, second witness: any two
composable words compose. -/
def closure_contains_composite {a b c : D.Obj}
    (p : Path D a b) (q : Path D b c) : (closure D).Arr :=
  ⟨a, c, p.comp q⟩

/-! ## 4. The operation laws, on the transported bundle

`IsNatural` reads exactly one thing about an isomorphism: what its
`mapPair` does.  The laws are therefore proved there.  They are not
claimed as equalities of `PresIso` records. -/

theorem mapPair_nil (D : Family X R) (a : D.Obj) (x : NonZeroPair (D.obs a)) :
    (pathIso D (Path.nil a)).mapPair x = x :=
  mapPair_refl (D.obs a) x

theorem mapPair_comp (D : Family X R) :
    ∀ {a b c : D.Obj} (p : Path D a b) (q : Path D b c)
      (x : NonZeroPair (D.obs a)),
      (pathIso D (p.comp q)).mapPair x
        = (pathIso D q).mapPair ((pathIso D p).mapPair x)
  | _, _, _, .nil _, q, x => by
      show (pathIso D q).mapPair x = (pathIso D q).mapPair ((pathIso D (Path.nil _)).mapPair x)
      rw [mapPair_nil]
  | _, _, _, .cons f p, q, x => by
      show (pathIso D ((Path.cons f p).comp q)).mapPair x = _
      show ((D.iso f).trans (pathIso D (p.comp q))).mapPair x = _
      rw [mapPair_trans, mapPair_comp D p q]
      show _ = (pathIso D q).mapPair (((D.iso f).trans (pathIso D p)).mapPair x)
      rw [mapPair_trans]
  | _, _, _, .consInv f p, q, x => by
      show (pathIso D ((Path.consInv f p).comp q)).mapPair x = _
      show ((D.iso f).symm.trans (pathIso D (p.comp q))).mapPair x = _
      rw [mapPair_trans, mapPair_comp D p q]
      show _ = (pathIso D q).mapPair (((D.iso f).symm.trans (pathIso D p)).mapPair x)
      rw [mapPair_trans]

theorem mapPair_one (D : Family X R) (f : D.Arr)
    (x : NonZeroPair (D.obs (D.src f))) :
    (pathIso D (Path.one f)).mapPair x = (D.iso f).mapPair x := by
  show ((D.iso f).trans (pathIso D (Path.nil (D.tgt f)))).mapPair x = _
  rw [mapPair_trans, mapPair_nil]

theorem mapPair_oneInv (D : Family X R) (f : D.Arr)
    (y : NonZeroPair (D.obs (D.tgt f))) :
    (pathIso D (Path.oneInv f)).mapPair y = (D.iso f).symm.mapPair y := by
  show ((D.iso f).symm.trans (pathIso D (Path.nil (D.src f)))).mapPair y = _
  rw [mapPair_trans, mapPair_nil]

/-- Both inverse laws, on the bundle: walking a word and then its
reversal returns the pair unchanged. -/
theorem mapPair_inv (D : Family X R) :
    ∀ {a b : D.Obj} (p : Path D a b) (x : NonZeroPair (D.obs a)),
      (pathIso D p.inv).mapPair ((pathIso D p).mapPair x) = x
  | _, _, .nil a, x => by
      show (pathIso D (Path.nil a)).mapPair ((pathIso D (Path.nil a)).mapPair x) = x
      rw [mapPair_nil, mapPair_nil]
  | _, _, .cons f p, x => by
      show (pathIso D (p.inv.comp (Path.consInv f (Path.nil (D.src f))))).mapPair
             (((D.iso f).trans (pathIso D p)).mapPair x) = x
      rw [mapPair_comp, mapPair_trans, mapPair_inv D p]
      show (pathIso D (Path.oneInv f)).mapPair ((D.iso f).mapPair x) = x
      rw [mapPair_oneInv, mapPair_symm_left]
  | _, _, .consInv f p, x => by
      show (pathIso D (p.inv.comp (Path.cons f (Path.nil (D.tgt f))))).mapPair
             (((D.iso f).symm.trans (pathIso D p)).mapPair x) = x
      rw [mapPair_comp, mapPair_trans, mapPair_inv D p]
      show (pathIso D (Path.one f)).mapPair ((D.iso f).symm.mapPair x) = x
      rw [mapPair_one, mapPair_symm_right]

/-- Associativity of concatenation, on the words themselves. -/
theorem comp_assoc :
    ∀ {a b c d : D.Obj} (p : Path D a b) (q : Path D b c) (r : Path D c d),
      (p.comp q).comp r = p.comp (q.comp r)
  | _, _, _, _, .nil _, _, _ => rfl
  | _, _, _, _, .cons f p, q, r => congrArg (Path.cons f) (comp_assoc p q r)
  | _, _, _, _, .consInv f p, q, r => congrArg (Path.consInv f) (comp_assoc p q r)

/-- The empty word is a left unit, definitionally. -/
theorem nil_comp {a b : D.Obj} (p : Path D a b) : (Path.nil a).comp p = p := rfl

/-- The empty word is a right unit. -/
theorem comp_nil :
    ∀ {a b : D.Obj} (p : Path D a b), p.comp (Path.nil b) = p
  | _, _, .nil _ => rfl
  | _, _, .cons f p => congrArg (Path.cons f) (comp_nil p)
  | _, _, .consInv f p => congrArg (Path.consInv f) (comp_nil p)

/-! ## 5. What a section owes the closure

The substantive half is the inverse step: naturality is stated in one
direction only, and a closed family demands the other. -/

/-- Naturality runs backwards along a declared arrow.  This is the step
the declared family does not state and the closure requires. -/
theorem natural_symm (D : Family X R) (s : Sec D) (hs : IsNatural D s)
    (f : D.Arr) : (D.iso f).symm.mapPair (s (D.tgt f)) = s (D.src f) := by
  have h := hs f
  have h2 := congrArg (D.iso f).symm.mapPair h
  rw [mapPair_symm_left] at h2
  exact h2.symm

/-- Naturality along an arbitrary word, from naturality on the declared
arrows alone. -/
theorem natural_on_path (D : Family X R) (s : Sec D) (hs : IsNatural D s) :
    ∀ {a b : D.Obj} (p : Path D a b), (pathIso D p).mapPair (s a) = s b
  | _, _, .nil a => mapPair_nil D a (s a)
  | _, _, .cons f p => by
      show ((D.iso f).trans (pathIso D p)).mapPair (s (D.src f)) = _
      rw [mapPair_trans, hs f]
      exact natural_on_path D s hs p
  | _, _, .consInv f p => by
      show ((D.iso f).symm.trans (pathIso D p)).mapPair (s (D.tgt f)) = _
      rw [mapPair_trans, natural_symm D s hs f]
      exact natural_on_path D s hs p

/-- **The theorem this rung exists for.**  A section is natural for the
closed family exactly when it is natural for the declared one.  Closing
under composition and inverses enlarges the arrows and imposes no new
obligation on a section. -/
theorem natural_iff_natural_closure (D : Family X R) (s : Sec D) :
    IsNatural D s ↔ IsNatural (closure D) s := by
  constructor
  · intro hs t
    exact natural_on_path D s hs t.2.2
  · intro hs f
    have h := hs (declared f)
    show (D.iso f).mapPair (s (D.src f)) = s (D.tgt f)
    rw [← mapPair_one D f (s (D.src f))]
    exact h

/-- The obstruction is unchanged too: a declared family carries a
natural section exactly when its closure does. -/
theorem has_natural_section_iff (D : Family X R) :
    (∃ s : Sec D, IsNatural D s) ↔ (∃ s : Sec (closure D), IsNatural (closure D) s) :=
  ⟨fun ⟨s, hs⟩ => ⟨s, (natural_iff_natural_closure D s).mp hs⟩,
   fun ⟨s, hs⟩ => ⟨s, (natural_iff_natural_closure D s).mpr hs⟩⟩

/-- Idempotence at the level of obligations: closing a closure imposes
nothing further. -/
theorem natural_closure_closure (D : Family X R) (s : Sec D) :
    IsNatural (closure D) s ↔ IsNatural (closure (closure D)) s := by
  have h1 := natural_iff_natural_closure D s
  have h2 := natural_iff_natural_closure (closure D) s
  exact ⟨fun h => h2.mp h, fun h => h1.mp (h1.mpr (h2.mpr h))⟩

end Closure
end ClosedFamily
