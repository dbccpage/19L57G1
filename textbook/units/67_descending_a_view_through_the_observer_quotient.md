# Unit 67. Descending a view through the observer quotient: exactness, the pair obstruction, and the compression dictionary

**Claim.** A view descends to an observer quotient exactly when it agrees on every pair the observer identifies. One identified pair with different view values blocks descent.

**Status:** FROZEN (the
descent theorems and the dictionary); CONDITIONAL (`view_descends_pair_blocked`,
on a compatible view and a blocking witness); REFUTED (descent of the
difference map and identity view on `collapseAllObs`; dropping `∀ D` in the
dictionary); VERIFIED_FINITE (`value_orientation_survives`, and the Python E3
and E4 censuses). **Lean:** `lean4/Derivation/ObsDescent.lean` lines 73-539,
imports `DiffInterface`, `Compression`. **Axioms:** 37 reports in
`artifacts/lean_axioms.txt` (lines 1076-1112); 11 use none, 2 use `propext`,
12 use `Quot.sound`, 12 use `propext, Quot.sound`. **Depends on:** Unit 44
(`DiffObs`, `ZeroRel`, `ObsQuotient`, `obsQuotient_eq_of_zero`, `kernelObs`),
Unit 61 (`FiberConstant`, `FactorsOn`, `factors_iff_fiberConstant`, `SigEq`).

## First pass

A quotient replaces each group of identified items with one class. Descending a view means computing its answer from that class alone.

Suppose the observer groups a and b together. A view with f(a) = f(b) can assign that shared answer to the class. A view with f(a) ≠ f(b) cannot.

For several classes, the view must agree within every class. For a pair of views, both components must pass this test. The formal sections extend this idea to difference maps and further quotients.

## Detailed claim and formal anchors

Unit 44 introduced the observer record `DiffObs X R` (a typed
difference map `delta : X → X → R`, a zero predicate `Zero : R → Prop`,
and three proof fields making `ZeroRel O x y := O.Zero (O.delta x y)` an
equivalence) together with the quotient `ObsQuotient O` and the soundness
half `obsQuotient_eq_of_zero`. `ObsDescent` completes the quotient-descent
theory that quotient earns: two points have equal classes if and only if
they form a zero-pair (`obsQuotient_exact`, `obsQuotient_mk_eq_iff`), and
every quotient class is the class of some point (`obsQuotient_mk_surjective`).

A view `f : X → Y` factors through `ObsQuotient.mk O` if and only if it is
constant on zero-classes (`ClassConstant`, `descend_exists_iff`), uniquely
on the entire quotient because the projection is surjective (`descend_unique`),
and a single zero-pair on which `f` disagrees blocks descent
(`descend_blocked_of_witness`).

The same three facts hold for the binary
difference map itself (`DeltaConstant`, `deltaDescend_exists_iff`,
`deltaDescend_unique`, `deltaDescend_blocked_of_witness`).

Pairing splits
componentwise (`classConstant_pair_iff`, `pair_descend_exists_iff`), yielding
the flagship witness shape: a class-constant view `f` descends alone while
its pairing `(f, g)` with a component that disagrees on a zero-pair is
blocked (`view_descends_pair_blocked`).

Descending into a further quotient
`Quotient S` of the value side reduces to ordinary equality descent for
`Quotient.mk S ∘ f` (`classConstant_comp_mk_iff`, `descendMod_exists_iff`,
`deltaDescendMod_exists_iff`, `coarsenMap`, `pairSetoid_mk_eq_iff`,
`descendMod_exists_of_coarsen`).

Two concrete non-kernel observers bound what
the interface allows: the integer subtraction observer `intDiffObs`, whose
difference values keep orientation while its zero relation cannot
(`value_orientation_survives`), and the all-zero observer `collapseAllObs` on
`Bool`, whose zero relation identifies everything while its difference map
still separates `true` from `false`, so neither its difference map nor the
identity view descends (`collapseAllObs_not_deltaConstant`,
`collapseAllObs_no_delta_descend`, `collapseAllObs_id_not_classConstant`,
`collapseAllObs_no_view_descend`).

Finally, for a kernel observer
`kernelObs p` on `Nat`, global quotient descent is equivalent to the
domain-relative factorization of Unit 61 quantified over every finite list
domain `D : List Nat` (`classConstant_iff_fiberConstant_all`,
`descend_iff_factorsOn_all`), and the quantifier `∀ D` cannot be
dropped (`fiberConstant_fixed_D_not_classConstant`).

## Question

When an observer declares which pairs have zero difference, what does passing
to its quotient allow a downstream view—or the observer's own difference
map—to keep, what blocks a view or a pair of views from descending, and how
does global quotient descent relate to factoring over a finite represented
list of items?

## What we already possess

- From Unit 44 (`DiffInterface`):
  - `DiffObs X R`: a structure with `delta : X → X → R`, `Zero : R → Prop`,
    and three proof fields `zero_refl`, `zero_symm`, `zero_trans`.
  - `ZeroRel O x y : Prop := O.Zero (O.delta x y)`, proved to be an
    equivalence relation (`zeroRel_equivalence`), and its setoid
    `obsSetoid O`.
  - `ObsQuotient O := Quotient (obsSetoid O)` with projection
    `ObsQuotient.mk O : X → ObsQuotient O` and soundness
    `obsQuotient_eq_of_zero : ZeroRel O x y → ObsQuotient.mk O x = ObsQuotient.mk O y`.
  - `kernelObs (view : X → V) : DiffObs X (V × V)` with
    `delta x y := (view x, view y)` and `Zero p := p.1 = p.2`, whose three
    equivalence laws are proved once from the reflexivity, symmetry, and
    transitivity of equality on `V`.
- From Unit 61 (`Compression`):
  - `FiberConstant D p q`: for all `x, x' ∈ D`, `p x = p x' → q x = q x'`.
  - `FactorsOn D p q`: `∃ g : Nat → Nat, ∀ x ∈ D, g (p x) = q x`, proved
    equivalent to `FiberConstant D p q` (`factors_iff_fiberConstant`), with
    factoring maps unique on the image of `D` and non-unique off it
    (`factor_not_unique_off_image`).
  - `SigEq Q x x'`: agreement on every question in `Q : List (Nat → Nat)`.

## New concept: exact quotient descent, non-kernel observers, and the `∀ D` bridge

1. **Exactness and epi projection.** Soundness says zero-related points go to
   the same quotient class; *exactness* (`obsQuotient_exact`) says only
   zero-related points do, via Lean's `Quotient.exact`. Because every element
   of `ObsQuotient O` is constructed as `ObsQuotient.mk O x` for some `x : X`
   (`obsQuotient_mk_surjective`, proved by `Quotient.inductionOn`), a map out
   of the quotient has no "off-image" region where two factorizations could
   disagree.
2. **Unary and binary compatibility.** `ClassConstant O f` says `f : X → Y`
   takes equal values on every zero-pair; `DeltaConstant O` says `O.delta`
   takes equal values when both arguments move within their zero-classes.
   These are the exact conditions for `f` and `O.delta` to descend to the
   quotient (`descend_exists_iff`, `deltaDescend_exists_iff`).
3. **Kernel versus non-kernel observers.** In a *kernel observer*
   `kernelObs view`, `ZeroRel` is view equality `view x = view y` and `delta`
   is the pair `(view x, view y)`, so `DeltaConstant` holds automatically. In
   an arbitrary `DiffObs X R`, `Zero` is an independent predicate on `R` whose
   three laws are admitted as structure fields (or proved for a specific
   construction without coming from a single view). In `collapseAllObs` on
   `Bool`, `delta x y := x` remembers the first point while `Zero _ := True`
   declares every difference value to be zero. That satisfies the three
   equivalence laws trivially, yet `delta` is not constant on zero-classes.
4. **The dictionary between global quotients and finite domains.** For a
   kernel observer `kernelObs p` with `p, q : Nat → Nat`, `ClassConstant (kernelObs p) q`
   is equivalent to `∀ D : List Nat, FiberConstant D p q`. Evaluating at the
   two-element list `[x, y]` recovers global compatibility from finite-list
   compatibility; fixing a single list `D` (such as `[]`) is strictly weaker.

## Plain-language interpretation

An observer `O` does two things: it computes a difference value `O.delta x y`
for each pair of items, and it applies a test `O.Zero` to decide whether that
difference counts as zero. Forming the quotient `ObsQuotient O` glues together
every pair of items whose difference tests as zero.

When can a summary `f : X → Y` be computed from the glued classes alone?
Exactly when `f` never tells apart two items that `O` glues together. If `f`
meets that condition (`ClassConstant O f`), there is one and only one function
on the quotient that reproduces `f`. Why is it unique everywhere, when in
Unit 61 a factoring map was unique only on the image of the domain? Because a
general presentation `p : Nat → Nat` can miss numbers in its codomain, leaving
any factoring map free to return arbitrary values on unreached numbers; the
quotient projection `ObsQuotient.mk O`, by contrast, hits every class by
definition.

What if we pair two summaries into `x ↦ (f x, g x)`? Pairing keeps both pieces
of information, so the pair can be computed from the quotient if and only if
both `f` and `g` can. If `f` respects every zero-pair of `O` while `g` splits
even one zero-pair `(x, y)`, then `f` passes through the quotient on its own
and `(f, g)` is blocked at `(x, y)`.

What if the target `Y` carries its own equivalence relation `S`, and we only
want `f` to descend up to `S`? We do not need a separate theory of
"descent modulo a setoid": composing `f` with the projection `Quotient.mk S`
turns `S`-equivalence in `Y` into equality in `Quotient S`, so the ordinary
equality descent theorem answers the question immediately
(`classConstant_comp_mk_iff`).

Does an observer's own difference map `O.delta` always pass to its quotient?
If the observer was built from a view (`kernelObs view`), yes: zero difference
means equal views, and `delta` is the pair of views. If the observer is
only an instance of the `DiffObs` signature, no: `collapseAllObs` sets
`delta x y = x` on `Bool` and declares every value to be zero. Its quotient
collapses `true` and `false` into one class, but `delta true true = true` and
`delta false false = false`, so `delta` cannot be defined on the single class.
Declaring all differences to be zero erases the quotient without erasing the
values of `delta`. Conversely, in the integer subtraction observer
`intDiffObs` (`delta a b = a - b`, `Zero v := v = 0`), the zero relation is
equality (`a = b`), which is symmetric, while the values `0 - 1 = -1` and
`1 - 0 = 1` distinguish the order of the pair (`value_orientation_survives`).

## Pseudocode

```text
ObsQuotient.mk(O, x) = ObsQuotient.mk(O, y)  <->  ZeroRel(O, x, y)
every q in ObsQuotient(O) is ObsQuotient.mk(O, x) for some x

ClassConstant(O, f) := for all x, y: ZeroRel(O, x, y) -> f(x) = f(y)
descend(O, f) exists  <->  ClassConstant(O, f)          -- and is unique
witness ZeroRel(O, x, y) with f(x) != f(y)  ->  no F factors f

DeltaConstant(O) := for all x, x', y, y':
    ZeroRel(O, x, x') and ZeroRel(O, y, y') -> O.delta(x, y) = O.delta(x', y')
deltaDescend(O) exists  <->  DeltaConstant(O)           -- and is unique

ClassConstant(O, (f, g))  <->  ClassConstant(O, f) and ClassConstant(O, g)
flagship: if ClassConstant(O, f) and ZeroRel(O, x, y) and g(x) != g(y):
    f descends, (f, g) does not descend

collapseAllObs on Bool: delta(x, y) := x, Zero(v) := True
    ZeroRel holds for all (a, b), but delta(true, false) != delta(false, false)
    -> not DeltaConstant, no deltaDescend, id not ClassConstant, no id descend

dictionary (for kernelObs(p) with p, q : Nat -> Nat):
    ClassConstant(kernelObs(p), q)  <->  for all D : List Nat, FiberConstant(D, p, q)
    descend exists                  <->  for all D : List Nat, FactorsOn(D, p, q)
    at fixed D = []: FiberConstant([], const 0, id) holds, ClassConstant fails
```

## Python

Genesis has no standalone `code/derivation/obs_descent.py`; instead, the
compression side of the dictionary lives in `code/derivation/compression.py`
and the exhaustive finite checks of the dictionary (E3) and the flagship pair
obstruction (E4) live in `code/run_primitive_contact.py`:

```python
# Python (Genesis), code/run_primitive_contact.py lines 384-440
def enum_descent_dictionary() -> dict[str, Json]:
    maps = list(product((0, 1), repeat=3))
    fmaps = list(product((0, 1), repeat=2))
    descend = 0
    diverge = 0
    for p in maps:
        for q in maps:
            cc = all(q[x] == q[y]
                     for x in range(3) for y in range(3)
                     if p[x] == p[y])
            ex = any(all(f[p[x]] == q[x] for x in range(3))
                     for f in fmaps)
            fc_full = all(q[x] == q[y]
                          for x in [0, 1, 2] for y in [0, 1, 2]
                          if p[x] == p[y])
            _require(cc == ex and ex == fc_full,
                     "descent/class-constant/fiber-constant diverged")
            fc_zero = all(q[x] == q[y]
                          for x in [0] for y in [0] if p[x] == p[y])
            if cc:
                descend += 1
            if fc_zero and not cc:
                diverge += 1
    _require(diverge > 0, "no fixed-domain divergence witnessed")
    return {
        "combinations": len(maps) * len(maps),
        "descend_count": descend,
        "fixed_domain_divergence_count": diverge,
    }


def enum_flagship_census() -> dict[str, Json]:
    maps = list(product((0, 1), repeat=3))
    count = 0
    for p in maps:
        for phi in maps:
            cc_phi = all(phi[x] == phi[y]
                         for x in range(3) for y in range(3)
                         if p[x] == p[y])
            if not cc_phi:
                continue
            for psi in maps:
                cc_psi = all(psi[x] == psi[y]
                             for x in range(3) for y in range(3)
                             if p[x] == p[y])
                if not cc_psi:
                    count += 1
    _require(count > 0, "no flagship triple exists")
    return {"triples": count}
```

The book's check script, `textbook/checks/u67_obs_descent.py`, runs E3 and E4
against `artifacts/primitive_contact.json`, checks `Compression`'s
`fiber_constant`, `factors_on`, and `sig_eq` against the dictionary, and adds
Python (book) checks for `collapseAllObs` and `value_orientation_survives`.

## Line-by-line Python explanation

- `maps = list(product((0, 1), repeat=3))`: all $2^3 = 8$ two-valued functions
  on the three-point carrier `{0, 1, 2}`, giving $8 \times 8 = 64$ pairs
  `(p, q)` of a kernel-observer view `p` and a target view `q`.
- `cc`: checks `ClassConstant (kernelObs p) q` on the carrier `{0, 1, 2}`,
  namely `p[x] == p[y] -> q[x] == q[y]` for all `x, y`.
- `ex`: searches all $2^2 = 4$ maps `f : {0, 1} → {0, 1}` for a factorization
  `f(p(x)) == q(x)` on `{0, 1, 2}`.
- `fc_full`: checks `FiberConstant [0, 1, 2] p q`. `_require` checks that
  `cc`, `ex`, and `fc_full` agree on all 64 pairs (`descend_count == 28`).
- `fc_zero`: checks `FiberConstant [0] p q` at the single-element domain
  `[0]`, which is always `True`. Whenever `cc` is `False` (the remaining 36
  pairs), `fc_zero and not cc` holds (`fixed_domain_divergence_count == 36`),
  illustrating why a fixed domain `D` is strictly weaker than `∀ D`.
- `enum_flagship_census`: loops over triples `(p, phi, psi)` where `phi` is
  class-constant for `kernelObs p` and `psi` is not; there are 120 such
  triples out of 512, each an instance of `view_descends_pair_blocked`.

## Lean 4

Exactness, unary and binary descent, and pairing
(`lean4/Derivation/ObsDescent.lean` lines 83-256, abridged):

```lean
theorem obsQuotient_exact (O : DiffObs X R) {x y : X}
    (h : ObsQuotient.mk O x = ObsQuotient.mk O y) : ZeroRel O x y :=
  Quotient.exact h

theorem obsQuotient_mk_eq_iff (O : DiffObs X R) (x y : X) :
    ObsQuotient.mk O x = ObsQuotient.mk O y ↔ ZeroRel O x y :=
  ⟨obsQuotient_exact O, obsQuotient_eq_of_zero O⟩

theorem obsQuotient_mk_surjective (O : DiffObs X R)
    (q : ObsQuotient O) : ∃ x, ObsQuotient.mk O x = q :=
  Quotient.inductionOn q fun x => ⟨x, rfl⟩

def ClassConstant (O : DiffObs X R) (f : X → Y) : Prop :=
  ∀ x y, ZeroRel O x y → f x = f y

def descend (O : DiffObs X R) (f : X → Y)
    (hf : ClassConstant O f) : ObsQuotient O → Y :=
  Quotient.lift f hf

theorem descend_exists_iff (O : DiffObs X R) (f : X → Y) :
    (∃ F : ObsQuotient O → Y, ∀ x, F (ObsQuotient.mk O x) = f x) ↔
      ClassConstant O f := by
  constructor
  · intro h x y hxy
    obtain ⟨F, hF⟩ := h
    calc f x = F (ObsQuotient.mk O x) := (hF x).symm
      _ = F (ObsQuotient.mk O y) := by
            rw [obsQuotient_eq_of_zero O hxy]
      _ = f y := hF y
  · intro hf
    exact ⟨descend O f hf, fun _ => rfl⟩

theorem descend_unique (O : DiffObs X R) (f : X → Y)
    (F G : ObsQuotient O → Y)
    (hF : ∀ x, F (ObsQuotient.mk O x) = f x)
    (hG : ∀ x, G (ObsQuotient.mk O x) = f x) : F = G :=
  funext fun q =>
    Quotient.inductionOn q fun x => (hF x).trans (hG x).symm

theorem descend_blocked_of_witness (O : DiffObs X R) (f : X → Y)
    {x y : X} (hxy : ZeroRel O x y) (hne : f x ≠ f y) :
    ¬ ∃ F : ObsQuotient O → Y, ∀ z, F (ObsQuotient.mk O z) = f z :=
  fun h => hne ((descend_exists_iff O f).mp h x y hxy)

def DeltaConstant (O : DiffObs X R) : Prop :=
  ∀ x x' y y', ZeroRel O x x' → ZeroRel O y y' →
    O.delta x y = O.delta x' y'

theorem view_descends_pair_blocked (O : DiffObs X R) (f : X → Y)
    (g : X → Z) (hf : ClassConstant O f) {x y : X}
    (hxy : ZeroRel O x y) (hg : g x ≠ g y) :
    (∃ F : ObsQuotient O → Y, ∀ z, F (ObsQuotient.mk O z) = f z) ∧
      ¬ ∃ F : ObsQuotient O → Y × Z,
          ∀ z, F (ObsQuotient.mk O z) = (f z, g z) :=
  ⟨(descend_exists_iff O f).mpr hf,
   descend_blocked_of_witness O (fun z => (f z, g z)) hxy
     fun he => hg (congrArg Prod.snd he)⟩
```

Mod-setoid reduction, non-kernel observers, and the dictionary (lines 276-537,
abridged):

```lean
theorem classConstant_comp_mk_iff (O : DiffObs X R) (f : X → Y)
    (S : Setoid Y) :
    ClassConstant O (fun x => Quotient.mk S (f x)) ↔
      ∀ x y, ZeroRel O x y → S.r (f x) (f y) :=
  ⟨fun h x y hxy => Quotient.exact (h x y hxy),
   fun h x y hxy => Quotient.sound (h x y hxy)⟩

theorem value_orientation_survives :
    intDiffObs.delta 0 1 ≠ intDiffObs.delta 1 0 ∧
      (ZeroRel intDiffObs 0 1 ↔ ZeroRel intDiffObs 1 0) := by ...

def collapseAllObs : DiffObs Bool Bool where
  delta x _ := x
  Zero _ := True
  zero_refl _ := trivial
  zero_symm _ := trivial
  zero_trans _ _ := trivial

theorem collapseAllObs_not_deltaConstant :
    ¬ DeltaConstant collapseAllObs :=
  fun h => Bool.noConfusion (h true false true false trivial trivial)

theorem classConstant_iff_fiberConstant_all (p q : Nat → Nat) :
    ClassConstant (kernelObs p) q ↔
      ∀ D : List Nat, Compression.FiberConstant D p q := by
  constructor
  · intro h D x _ x' _ hp
    exact h x x' hp
  · intro h x y hp
    exact h [x, y] x List.mem_cons_self y
      (List.mem_cons_of_mem x List.mem_cons_self) hp

theorem descend_iff_factorsOn_all (p q : Nat → Nat) :
    (∃ F : ObsQuotient (kernelObs p) → Nat,
        ∀ x, F (ObsQuotient.mk (kernelObs p) x) = q x) ↔
      ∀ D : List Nat, Compression.FactorsOn D p q :=
  (descend_exists_iff (kernelObs p) q).trans
    ((classConstant_iff_fiberConstant_all p q).trans
      ⟨fun h D => (Compression.factors_iff_fiberConstant D p q).mpr (h D),
       fun h D => (Compression.factors_iff_fiberConstant D p q).mp (h D)⟩)

theorem fiberConstant_fixed_D_not_classConstant :
    Compression.FiberConstant [] (fun _ => 0) (fun x => x) ∧
      ¬ ClassConstant (kernelObs fun _ : Nat => 0) (fun x => x) :=
  ⟨fun _ hx => (nomatch hx),
   fun h => absurd (h 0 1 rfl) (by decide)⟩
```

Lean (book), from `textbook/checks/u67_lean.py`:

```lean
theorem collapseAll_one_class :
    ObsQuotient.mk collapseAllObs true = ObsQuotient.mk collapseAllObs false :=
  obsQuotient_eq_of_zero collapseAllObs trivial

theorem collapseAll_flagship :
    (∃ F : ObsQuotient collapseAllObs → Bool,
        ∀ z, F (ObsQuotient.mk collapseAllObs z) = true) ∧
      ¬ ∃ F : ObsQuotient collapseAllObs → Bool × Bool,
          ∀ z, F (ObsQuotient.mk collapseAllObs z) = (true, z) :=
  view_descends_pair_blocked collapseAllObs (fun _ => true) (fun z => z)
    (fun _ _ _ => rfl) (x := true) (y := false) trivial Bool.noConfusion

theorem kernelObs_deltaConstant {X V : Type} (view : X → V) :
    DeltaConstant (kernelObs view) := by
  intro x x' y y' hx hy
  have hx' : view x = view x' := hx
  have hy' : view y = view y' := hy
  show (view x, view y) = (view x', view y')
  rw [hx', hy']

theorem intDiffObs_deltaConstant : DeltaConstant intDiffObs := by
  intro x x' y y' hx hy
  have hx' : x - x' = 0 := hx
  have hy' : y - y' = 0 := hy
  show x - y = x' - y'
  omega

theorem subsingleton_carrier_classConstant {X R Y : Type} [Subsingleton X]
    (O : DiffObs X R) (f : X → Y) : ClassConstant O f :=
  fun x y _ => congrArg f (Subsingleton.elim x y)
```

## Line-by-line Lean explanation

- `obsQuotient_exact`: applies `Quotient.exact` to turn equality in
  `ObsQuotient O` back into `ZeroRel O x y`. Combined with
  `obsQuotient_eq_of_zero`, this gives `obsQuotient_mk_eq_iff`.
- `obsQuotient_mk_surjective`: uses `Quotient.inductionOn q` to reduce an
  arbitrary class `q` to `ObsQuotient.mk O x`, witnessed by `⟨x, rfl⟩`.
- `descend_exists_iff`: forward direction rewrites `ObsQuotient.mk O x` to
  `ObsQuotient.mk O y` along `obsQuotient_eq_of_zero O hxy`; backward
  direction supplies `descend O f hf := Quotient.lift f hf`, whose defining
  equation `descend_mk` holds by `rfl`.
- `descend_unique`: applies `funext` and `Quotient.inductionOn q`; on a
  representative `x`, `F (mk x) = f x = G (mk x)`.
- `descend_blocked_of_witness`: contraposes the forward direction of
  `descend_exists_iff` at a zero-pair `hxy` where `f x ≠ f y`.
- `view_descends_pair_blocked`: packages `(descend_exists_iff O f).mpr hf`
  with `descend_blocked_of_witness` applied to `z ↦ (f z, g z)`; if the pairs
  `(f x, g x)` and `(f y, g y)` were equal, `congrArg Prod.snd` would give
  `g x = g y`, contradicting `hg`.
- `classConstant_comp_mk_iff`: `Quotient.mk S (f x) = Quotient.mk S (f y)` is
  equivalent to `S.r (f x) (f y)` by `Quotient.exact` and `Quotient.sound`.
- `collapseAllObs_not_deltaConstant`: applies `h : DeltaConstant collapseAllObs`
  to `x = true, x' = false, y = true, y' = false` with `trivial` zero-proofs,
  producing `true = false`, refuted by `Bool.noConfusion`.
- `classConstant_iff_fiberConstant_all`: forward ignores membership in `D`;
  backward instantiates `∀ D` at the two-element list `[x, y]`, where `x` and
  `y` are members by `List.mem_cons_self` and `List.mem_cons_of_mem`.
- `fiberConstant_fixed_D_not_classConstant`: on `D = []`, membership `x ∈ []`
  is uninhabited (`nomatch hx`), so `FiberConstant [] (fun _ => 0) id` holds
  vacuously; globally, `0` and `1` have the same constant view `0 = 0`, yet
  `0 ≠ 1`.
- Book `kernelObs_deltaConstant` and `intDiffObs_deltaConstant`: show why
  every kernel observer and `intDiffObs` have descending difference maps,
  in contrast to `collapseAllObs`. Book `subsingleton_carrier_classConstant`
  establishes the metatheoretic remark in the docstring: on a subsingleton carrier
  every view is class-constant, so `Bool` is the smallest carrier supporting a
  descent obstruction.

## What has been proved

- Exactness and surjectivity of the observer quotient:
  `obsQuotient_exact` (83), `obsQuotient_mk_eq_iff` (88),
  `obsQuotient_mk_surjective` (96).
- Unary and binary descent characterization, global uniqueness, and witness
  blocking: `descend_mk` (113), `descend_exists_iff` (119), `descend_unique`
  (134), `descend_blocked_of_witness` (142), `deltaDescend_mk` (161),
  `deltaDescend_exists_iff` (169), `deltaDescend_unique` (188),
  `deltaDescend_blocked_of_witness` (200).
- Componentwise pairing and the flagship witness theorem:
  `classConstant_pair_iff` (212), `pair_descend_exists_iff` (225),
  `view_descends_pair_blocked` (248).
- Reduction of value-setoid descent to equality descent:
  `coarsenMap_mk` (267), `classConstant_comp_mk_iff` (276),
  `descendMod_exists_iff` (284), `deltaDescendMod_exists_iff` (293),
  `pairSetoid_mk_eq_iff` (327), `descendMod_exists_of_coarsen` (334).
- Tag-view zero relation (`tag_view_zeroRel`, 350) and the integer subtraction
  observer (`intDiffObs_zeroRel`, `int_sub_ne_zero_iff`,
  `int_sub_ne_zero_of_gt`, `int_shift_cancel`, `int_two_mul_eq_zero_iff`,
  `int_add_sub_cancel`, `value_orientation_survives`, 374-417).
- The all-zero countermodel on `Bool`: `collapseAllObs_all_zero` (445),
  `collapseAllObs_not_deltaConstant` (452), `collapseAllObs_no_delta_descend`
  (458), `collapseAllObs_id_not_classConstant` (469),
  `collapseAllObs_no_view_descend` (476).
- The factorization dictionary with `Compression`:
  `classConstant_iff_fiberConstant_all` (494), `descend_iff_factorsOn_all`
  (507), `fiberConstant_fixed_D_not_classConstant` (523), `sigEq_append_iff`
  (532).

## What has not been proved

- Audit finding 1 (`tag_view_zeroRel`): the theorem states
  `ZeroRel (kernelObs fun p : K × X => φ p.2) s t ↔ φ s.2 = φ t.2`, proved by
  `Iff.rfl`. No separate "tag-augmented observer" structure is defined and
  proved equal to a kernel observer; the realization is the definitional
  choice to write a tagged view as `kernelObs (φ ∘ Prod.snd)`.
- Audit finding 2 (the integer arithmetic lemmas): `int_sub_ne_zero_iff`,
  `int_sub_ne_zero_of_gt`, `int_shift_cancel`, `int_two_mul_eq_zero_iff`, and
  `int_add_sub_cancel` are one-line linear integer arithmetic facts (`omega`)
  with no Genesis state or regime content. The ledger note that they "subsume
  the arriving integer tail" refers to an external comparison file outside the
  sealed tree.
- Observer classification (`native_derivation_map.md`): Theorems over a
  parameter `O : DiffObs X R` take the three equivalence laws as admitted
  fields of `O`. Only `kernelObs` derives the laws once from view equality;
  `intDiffObs` and `collapseAllObs` are non-kernel observers that discharge
  the three law fields per instance (by `omega` and `trivial`).
- Scope of the dictionary: `classConstant_iff_fiberConstant_all` and
  `descend_iff_factorsOn_all` are proved for `kernelObs p` with
  `p, q : Nat → Nat` only, not for arbitrary carriers or non-kernel observers.
- No theorem in `ObsDescent` connects quotient descent to the passage
  obstruction predicate `obstP` (which adds retention, protection, and
  declared-observation gates; see Unit 68).

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `{X R Y Z : Type}`, `Setoid Y`, `Int` | carrier, residual, and value types | metatheoretic types |
| `ObsQuotient O`, `Quotient.lift`, `Quotient.lift₂`, `Quotient.sound`, `Quotient.exact`, `Quotient.inductionOn` | quotient construction and elimination | metatheoretic quotient apparatus (`Quot.sound`) |
| `funext` | global uniqueness (`descend_unique`, `deltaDescend_unique`) | metatheoretic function extensionality (via `Quot.sound`) |
| `∀ D : List Nat` | the dictionary quantifier in `descend_iff_factorsOn_all` | metatheoretic quantification over all finite lists |

**What the system holds.** A system state in `Compression` (Unit 61) holds a
single finite domain `D : List Nat`. The quotient `ObsQuotient O` over an
arbitrary type `X` and the quantifier `∀ D : List Nat` live in the
metatheory, as the module header explicitly declares ("the quotient machinery
of the metalanguage").

## Student exercise

Why does `DeltaConstant` hold for every kernel observer `kernelObs view`, and
what goes wrong if you try to repeat that two-line proof for `collapseAllObs`?
Verify your answer against `kernelObs_deltaConstant` in
`textbook/checks/u67_lean.py`.

## Answer

For `O = kernelObs view`, `O.delta x y` is defined as the pair
`(view x, view y)` and `ZeroRel O x x'` is defined as `view x = view x'`. So
given `hx : ZeroRel O x x'` and `hy : ZeroRel O y y'`, we have `view x = view x'`
and `view y = view y'`, and rewriting both sides turns `(view x, view y)` into
`(view x', view y')`.

In `collapseAllObs`, `ZeroRel collapseAllObs x x'` is `True`, not an equality
between values of a view, while `collapseAllObs.delta x y` is `x`. Knowing
`ZeroRel collapseAllObs true false` (`True`) gives no equation `true = false`
with which to rewrite `collapseAllObs.delta true true = true` into
`collapseAllObs.delta false false = false`. That decoupling of `Zero` from
`delta` is what a non-kernel `DiffObs` allows and what `kernelObs` forbids.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/ObsDescent.lean` lines 83-98 (exactness, surjectivity), 104-145 (unary descent), 151-206 (binary descent), 212-256 (pairing, flagship), 261-343 (mod-setoid reduction), 350 (`tag_view_zeroRel`), 359-429 (`intDiffObs`, orientation), 437-480 (`collapseAllObs`), 494-537 (compression dictionary) |
| Axiom report | `artifacts/lean_axioms.txt` lines 1076-1112 (37 theorems; all within `{propext, Quot.sound}`, 11 axiom-free) |
| Paper | `paper/primitive_difference_contact.md`; `paper/paper_claim_ledger.md` `CL-PD2-CONTACT-RECONSTRUCTION`, `CL-PD2-CONTACT-DICTIONARY` |
| Python | `code/run_primitive_contact.py` (`enum_descent_dictionary`, `enum_flagship_census`), `code/derivation/compression.py` (`fiber_constant`, `factors_on`, `sig_eq`), `artifacts/primitive_contact.json` |
| Audit | `textbook/audit/modules/ObsDescent.md` findings 1-4 and sections 2, 6 |
| Check (Python) | `python textbook/checks/u67_obs_descent.py`: E3 (64 combinations, 28 descend, 36 fixed-domain divergences) and E4 (120 flagship triples) matched to artifact, `Compression` dictionary parity, `collapseAllObs` and `intDiffObs` checks |
| Check (book Lean) | `python textbook/checks/u67_lean.py`: nine book declarations plus fifteen Genesis theorems kernel-checked, Lean 4.33.0 |
