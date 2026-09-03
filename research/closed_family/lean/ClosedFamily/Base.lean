/-!
# The pinned presentation machinery, reconstructed verbatim

PIN NOTE.  Every declaration in this file is reproduced VERBATIM from the
sealed sources pinned in `SOURCE_MANIFEST.json` at snapshot
`f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be` of `main`:

* `lean4/Derivation/DiffInterface.lean`, blob `450b434f09d922fe117e3bbf72fa454d6b3dbeda`
* `lean4/Derivation/ContactKernel.lean`, blob `04c923534f67c99889677186d42a9657d051e096`
* `lean4/Derivation/PresentationNaturality.lean`, blob `ef4d76c7a07d38966150923691d1a0bba65bde68`

The only change is the outer namespace, so this package stays
self-contained and imports nothing sealed.  `verify_pins.py` checks every
block against its source ranges and fails on any drift.  Nothing here is
claimed as original: these are CONDITIONAL_THEOREM citations into the
sealed packet, compiled here so that the closure below is stated against
the pinned definitions themselves.  AuthorityEffect: None.
-/

namespace ClosedFamily

variable {A B C X R X' R' X'' R'' V : Type}

/-! ## Reconstructed: the typed difference operation, its zero relation, and the equivalence -/

structure DiffObs (X R : Type) where
  delta : X → X → R
  Zero : R → Prop
  zero_refl : ∀ x, Zero (delta x x)
  zero_symm : ∀ {x y}, Zero (delta x y) → Zero (delta y x)
  zero_trans : ∀ {x y z},
    Zero (delta x y) → Zero (delta y z) → Zero (delta x z)

/-- `ZeroRel x y` iff the observer's difference value is zero. -/
def ZeroRel (O : DiffObs X R) (x y : X) : Prop := O.Zero (O.delta x y)

/-- The equivalence proof — established *before* any quotient below. -/
theorem zeroRel_equivalence (O : DiffObs X R) :
    Equivalence (ZeroRel O) :=
  ⟨fun x => O.zero_refl x, fun h => O.zero_symm h,
   fun h1 h2 => O.zero_trans h1 h2⟩

/-! ## Reconstructed: the admissible pairs of an observer -/

/-- The admissible pairs of an observer: exactly the data `ofDiffObs`
consumes beyond the observer record. -/
abbrev NonZeroPair (O : DiffObs X R) : Type :=
  { p : X × X // ¬ ZeroRel O p.1 p.2 }

/-! ## Reconstructed: explicit bijections -/

structure Bij (A B : Type) where
  fwd : A → B
  bwd : B → A
  fwd_bwd : ∀ b, fwd (bwd b) = b
  bwd_fwd : ∀ a, bwd (fwd a) = a

def Bij.rfl' (A : Type) : Bij A A where
  fwd a := a
  bwd a := a
  fwd_bwd _ := rfl
  bwd_fwd _ := rfl

def Bij.symm (f : Bij A B) : Bij B A where
  fwd := f.bwd
  bwd := f.fwd
  fwd_bwd := f.bwd_fwd
  bwd_fwd := f.fwd_bwd

def Bij.trans (f : Bij A B) (g : Bij B C) : Bij A C where
  fwd a := g.fwd (f.fwd a)
  bwd c := f.bwd (g.bwd c)
  fwd_bwd c := by rw [f.fwd_bwd, g.fwd_bwd]
  bwd_fwd a := by rw [g.bwd_fwd, f.bwd_fwd]

/-- A bijection separates what it distinguishes: the forward map is
injective, with no appeal to a choice principle. -/
theorem Bij.fwd_injective (f : Bij A B) {a a' : A} (h : f.fwd a = f.fwd a') :
    a = a' := by
  have := congrArg f.bwd h
  rwa [f.bwd_fwd, f.bwd_fwd] at this

/-! ## Reconstructed: presentation isomorphisms, and the transport of the zero relation -/

/-- A presentation isomorphism carries one observer to another: a
bijection of carriers, a bijection of residual values, and the two
transport laws that make `delta` and `Zero` agree across them. -/
structure PresIso (O : DiffObs X R) (O' : DiffObs X' R') where
  car : Bij X X'
  res : Bij R R'
  delta_transport : ∀ x y, res.fwd (O.delta x y) = O'.delta (car.fwd x) (car.fwd y)
  zero_transport : ∀ r, O.Zero r ↔ O'.Zero (res.fwd r)

/-- **The zero relation transports.**  This is the law-level content of
a presentation isomorphism: the relation `ZeroRel` induced by `O` and
the one induced by `O'` correspond along the carrier bijection.  Both
endpoint observers are named. -/
theorem zeroRel_transport {O : DiffObs X R} {O' : DiffObs X' R'}
    (F : PresIso O O') (x y : X) :
    ZeroRel O x y ↔ ZeroRel O' (F.car.fwd x) (F.car.fwd y) := by
  show O.Zero (O.delta x y) ↔ O'.Zero (O'.delta (F.car.fwd x) (F.car.fwd y))
  rw [← F.delta_transport x y]
  exact F.zero_transport (O.delta x y)


/-! ## Reconstructed: identity, inverse, composition, and their component laws -/

def PresIso.refl (O : DiffObs X R) : PresIso O O where
  car := Bij.rfl' X
  res := Bij.rfl' R
  delta_transport _ _ := rfl
  zero_transport _ := Iff.rfl

def PresIso.symm {O : DiffObs X R} {O' : DiffObs X' R'} (F : PresIso O O') :
    PresIso O' O where
  car := F.car.symm
  res := F.res.symm
  delta_transport x' y' := by
    have h := F.delta_transport (F.car.bwd x') (F.car.bwd y')
    rw [F.car.fwd_bwd, F.car.fwd_bwd] at h
    have h2 := congrArg F.res.bwd h
    rw [F.res.bwd_fwd] at h2
    show F.res.bwd (O'.delta x' y') = O.delta (F.car.bwd x') (F.car.bwd y')
    exact h2.symm
  zero_transport r' := by
    have h := F.zero_transport (F.res.bwd r')
    rw [F.res.fwd_bwd] at h
    exact h.symm

def PresIso.trans {O : DiffObs X R} {O' : DiffObs X' R'} {O'' : DiffObs X'' R''}
    (F : PresIso O O') (G : PresIso O' O'') : PresIso O O'' where
  car := F.car.trans G.car
  res := F.res.trans G.res
  delta_transport x y := by
    show G.res.fwd (F.res.fwd (O.delta x y)) = _
    rw [F.delta_transport x y, G.delta_transport]
    rfl
  zero_transport r := by
    show O.Zero r ↔ O''.Zero (G.res.fwd (F.res.fwd r))
    exact (F.zero_transport r).trans (G.zero_transport (F.res.fwd r))

theorem refl_car (O : DiffObs X R) (x : X) :
    (PresIso.refl O).car.fwd x = x := rfl

theorem trans_car {O : DiffObs X R} {O' : DiffObs X' R'} {O'' : DiffObs X'' R''}
    (F : PresIso O O') (G : PresIso O' O'') (x : X) :
    (F.trans G).car.fwd x = G.car.fwd (F.car.fwd x) := rfl

theorem symm_car_left {O : DiffObs X R} {O' : DiffObs X' R'}
    (F : PresIso O O') (x : X) : F.symm.car.fwd (F.car.fwd x) = x :=
  F.car.bwd_fwd x

theorem symm_car_right {O : DiffObs X R} {O' : DiffObs X' R'}
    (F : PresIso O O') (x' : X') : F.car.fwd (F.symm.car.fwd x') = x' :=
  F.car.fwd_bwd x'

theorem symm_symm_car {O : DiffObs X R} {O' : DiffObs X' R'}
    (F : PresIso O O') (x : X) : F.symm.symm.car.fwd x = F.car.fwd x := rfl

/-! ## Reconstructed: the transported pair bundle -/

/-- **The bundle transports.**  A presentation isomorphism carries an
admissible pair of `O` to an admissible pair of `O'`; admissibility is
preserved because the zero relation transports.  Both endpoint
observers are named. -/
def PresIso.mapPair {O : DiffObs X R} {O' : DiffObs X' R'}
    (F : PresIso O O') (p : NonZeroPair O) : NonZeroPair O' :=
  ⟨(F.car.fwd p.val.1, F.car.fwd p.val.2), fun h =>
    p.property ((zeroRel_transport F p.val.1 p.val.2).mpr h)⟩

/-! ## Reconstructed: declared families, sections, naturality -/

/-- A DECLARED presentation family: observers indexed by `Obj`, and a
collection of isomorphisms `Arr` between them.  Nothing is assumed
about closure under composition or inverses; the family is exactly what
it lists. -/
structure Family (X R : Type) where
  Obj : Type
  obs : Obj → DiffObs X R
  Arr : Type
  src : Arr → Obj
  tgt : Arr → Obj
  iso : (f : Arr) → PresIso (obs (src f)) (obs (tgt f))

/-- A section of the admissible-pair bundle: a pair chosen at every
observer of the family, dependently typed in that observer. -/
def Sec (D : Family X R) : Type := ∀ a : D.Obj, NonZeroPair (D.obs a)

/-- Naturality: the section commutes with every isomorphism the family
declares. -/
def IsNatural (D : Family X R) (s : Sec D) : Prop :=
  ∀ f : D.Arr, (D.iso f).mapPair (s (D.src f)) = s (D.tgt f)

/-! ## Reconstructed: coherence of the transported bundle -/

theorem mapPair_refl (O : DiffObs X R) (p : NonZeroPair O) :
    (PresIso.refl O).mapPair p = p := by
  apply Subtype.ext
  rfl

theorem mapPair_trans {O : DiffObs X R} {O' : DiffObs X' R'}
    {O'' : DiffObs X'' R''} (F : PresIso O O') (G : PresIso O' O'')
    (p : NonZeroPair O) :
    (F.trans G).mapPair p = G.mapPair (F.mapPair p) := by
  apply Subtype.ext
  rfl

theorem mapPair_symm_left {O : DiffObs X R} {O' : DiffObs X' R'}
    (F : PresIso O O') (p : NonZeroPair O) :
    F.symm.mapPair (F.mapPair p) = p := by
  apply Subtype.ext
  show (F.car.bwd (F.car.fwd p.val.1), F.car.bwd (F.car.fwd p.val.2)) = p.val
  rw [F.car.bwd_fwd, F.car.bwd_fwd]

theorem mapPair_symm_right {O : DiffObs X R} {O' : DiffObs X' R'}
    (F : PresIso O O') (q : NonZeroPair O') :
    F.mapPair (F.symm.mapPair q) = q := by
  apply Subtype.ext
  show (F.car.fwd (F.car.bwd q.val.1), F.car.fwd (F.car.bwd q.val.2)) = q.val
  rw [F.car.fwd_bwd, F.car.fwd_bwd]

end ClosedFamily
