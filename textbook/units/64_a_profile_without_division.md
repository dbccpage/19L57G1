# Unit 64. A profile without division

**Claim.** The declared weight profiles compare proportions by cross-multiplication. Their arithmetic results concern admitted decorations; no bridge to the regime's observations is established here.

<details>
<summary>Source and classification record (optional on a first reading)</summary>

**Status:** FROZEN (all arithmetic theorems on `SameProfile`, `Presents`, `SignedSquarePresents`, `ModulusBlind` descent, `decoratedCarrierShape_exists`, and `claimedReadOutUniqueness_false`); ADMITTED (the definitions `Weights`, `CarrierList`, `total`, `SameProfile`, `Presents`, `sq`, `sqInt`, `SignedSquarePresents`, `mixSum`, `readOut`, `ModulusBlind`, and `ClaimedReadOutUniqueness`, with no proved bridge to `Basic.lean` or `PrimitivePassage.PState`); VERIFIED_FINITE (`artifacts/weight_profile.json`).
**Lean:** `lean4/Derivation/WeightProfile.lean` lines 57–522.
**Axioms:** `propext`, `Quot.sound` on 25 of 31 public theorem reports; `propext` on `WeightProfile.duplicate_list_not_carrier` and `WeightProfile.sq_mul`; `none` on `WeightProfile.profile_refl`, `WeightProfile.profile_symm`, `WeightProfile.profile_order`, and `WeightProfile.decoratedCarrierShape_exists` (`artifacts/lean_axioms.txt` lines 858–888).
**Depends on:** Unit 00 (the standing rule that declared data are admitted, not derived; `WeightProfile.lean` imports `Derivation.Compression` for linear build ordering only and references zero declarations from earlier system modules).

</details>

---

## First pass

Start with two trays holding 2 and 3 counters. Their total is 5. A second
pair of trays holds 4 and 6, with total 10. Every count doubled, so the
shares stayed the same: two of five is the same share as four of ten.

We can compare without division. At the first position, multiply each
entry by the other table's total: 2 × 10 = 4 × 5. At the second position,
3 × 10 = 6 × 5. Both checks pass. The total itself was not preserved.

Predict what happens with the empty table `(0, 0)`. Every cross product
against it is zero, so the raw test passes against every table. That does
not define fractional shares at total zero. The positive-total hypothesis
is what makes the intended proportion comparison behave as expected.

A separate signed-number example shows another kind of information loss.
The inputs `(1, 1)` and `(1, −1)` have equal separate squares, but adding
before squaring gives 4 and 0. This readout rule is admitted; the weights
alone do not choose it, and the module proves no measurement connection.

If any operation is unfamiliar, use the nine short lessons in the
[Number lab](../number_lab/README.md). They introduce totals, shares,
zero, signed steps, squares, and coordinate addition before the formal
claims below. This arithmetic `SameProfile` is a different definition
from the regime's yes-question profile.

## Detailed claim and formal anchors

The module works on a finite position list `l : List Nat` and count
assignments such as `w : Nat → Nat`. Its results fall into separate steps:

1. **Compare proportions.** `SameProfile l w v` checks
   `w p * total l v = v p * total l w` at every listed position.
   It is reflexive and symmetric on all assignments. Transitivity needs
   a positive middle total (`profile_trans`, `zero_scale_boundary`).
2. **Restrict to positive totals.** There the relation is an equivalence
   and is characterized by positive integer multipliers
   (`profile_equivalence_positive`, `profile_iff_ray`). It preserves
   which entries vanish and their pairwise order, while forgetting
   the overall total (`profile_support`, `profile_order`,
   `profile_forgets_total`).
3. **Compare presentations.** If a decoration presents a weight table,
   its mapped weights have the same profile as that table
   (`presentation_profile_redundant`, `presentations_agree_on_profile`).
   This follows from the presentation equation, not a new physical law.
4. **Keep the number domain explicit.** Unsigned squares determine
   their nonnegative inputs (`unsigned_decoration_determined`). Signed
   squares can forget a sign and hence fail to determine the admitted
   add-then-square reading (`signed_square_presentations_split`).
5. **Ask when a readout recovers from squares.** The squared linear
   readout is constant on every pair of `ModulusBlind` inputs exactly
   when `a * b = 0` (`descent_iff_subsingleton_support`). This theorem
   quantifies over all integer inputs; a bounded Python loop alone does not.
6. **Audit proposed conclusions.** `decoratedCarrierShape_exists`
   supplies a weak existential witness, while
   `claimedReadOutUniqueness_false` refutes the stated uniqueness schema.
   `finite_scope_summary` collects the module's scoped conclusions.

The detailed definitions and proofs follow. Each claim carries its own
domain and hypotheses; a shared arithmetic example does not connect
this module to the earlier regime model.

## Question

Suppose a finite list of positions `l : List Nat` is decorated by a natural-number count assignment `w : Nat → Nat`. How can two assignments `w` and `v` be compared for having the same relative proportions across `l` without introducing fractions, rational numbers, or division? Where does that cross-multiplied comparison form an equivalence relation, and where does it degenerate? And if `w` is presented through a modulus map `m : Nat → Nat` (`Presents l m c w`) or through unsigned squares `sq` vs. signed integer squares `sqInt`, what does `w` determine about the decoration `c` and about linear combinations `readOut a b x y := a * x + b * y`?

---

## What we already possess

From Unit 00, any type, operation, or predicate that is not derived from earlier ledger structure is an **admitted** declaration whose scope is exactly what its definition states.

`lean4/Derivation/WeightProfile.lean` imports `Derivation.Compression` at line 1 solely to sit in the linear module chain of `lean4/Derivation.lean`, and uses zero types or theorems from `Compression` or any earlier `Derivation.*` module. Everything in `WeightProfile.lean` is self-contained finite `Nat` and `Int` arithmetic on lists `l : List Nat` and functions `Nat → Nat` or `Nat → Int`. There is no proved bridge in Lean connecting `Weights`, `CarrierList`, or `Presents` to the regimes, contexts, or observers of `Basic.lean` or to the nine-field ledger of `PrimitivePassage.lean`.

---

## New concept: cross-multiplied profiles, square presentations, and modulus-blind descent

`WeightProfile` introduces six groups of definitions on a finite position list `l : List Nat`:

1. **Weights, duplicate-free lists, and list totals (lines 57–118):**
   - `Weights := Nat → Nat` assigns a natural count to each position.
   - `CarrierList (l : List Nat) : Prop := l.Nodup` records that `l` has no duplicate labels (`duplicate_list_not_carrier : ¬ CarrierList [0, 0]`).
   - `total (l : List Nat) (w : Weights) : Nat := (l.map w).foldl (fun a b => a + b) 0` sums `w p` across `l` with multiplicity (`total_cons`, `total_append`, `total_scale`, `total_ray`).

2. **Division-free relative profile (`SameProfile`, lines 121–224):**
   - `SameProfile (l : List Nat) (w v : Weights) : Prop := ∀ p ∈ l, w p * total l v = v p * total l w`.
   - `profile_refl` and `profile_symm` hold for all `w, v`; `profile_trans` requires `0 < total l v` on the middle assignment, because `SameProfile l (fun _ => 0) w` holds for every `w` (`profile_scale_raw l 0 w`, `zero_scale_boundary`), so a zero-total middle assignment links any two assignments regardless of their proportions.
   - On positive-total assignments (`0 < total l w`, `0 < total l v`), `SameProfile l w v` is an equivalence relation (`profile_equivalence_positive`) and is equivalent to the existence of positive scalars `a > 0`, `b > 0` such that `∀ p ∈ l, a * w p = b * v p` (`profile_iff_ray`).

3. **Invariants, forgotten scale, and `Presents` (lines 228–322):**
   - Under positive totals, `SameProfile l w v` preserves zero-vs-nonzero support (`profile_support : w p = 0 ↔ v p = 0`) and pairwise order (`profile_order : w p ≤ w q ↔ v p ≤ v q`) for `p, q ∈ l`, while forgetting the overall scale (`profile_forgets_total`).
   - `Presents (l : List Nat) (m : Nat → Nat) (c : Nat → Nat) (w : Weights) : Prop := CarrierList l ∧ ∀ p ∈ l, m (c p) = w p`.
   - Because `m (c p) = w p` for all `p ∈ l`, `total l (fun p => m (c p)) = total l w` (`total_congr`) and `SameProfile l (fun p => m (c p)) w` holds (`presentation_profile_redundant`), so any two presentations `c, d` of a positive-total `w` satisfy `SameProfile l (fun p => m (c p)) (fun p => m (d p))` (`presentations_agree_on_profile`).

4. **Unsigned determination vs. one signed-square shadow (lines 326–410):**
   - For unsigned decorations `c : Nat → Nat` under `sq x := x * x`, squaring is strictly monotone (`sq_mono`) and injective (`sq_injective : sq c = sq d → c = d`), so `Presents l sq c w` and `Presents l sq d w` force `∀ p ∈ l, c p = d p` (`unsigned_decoration_determined`).
   - For signed decorations `c : Nat → Int` under `sqInt x := x * x`, `SignedSquarePresents l c w := CarrierList l ∧ ∀ p ∈ l, sqInt (c p) = w p`, and `mixSum (x y : Int) : Int := (x + y) * (x + y)`: on `l = [0, 1]`, `signedPlus` (`0 ↦ 1, 1 ↦ 1`) and `signedSplit` (`0 ↦ 1, 1 ↦ -1`) both present `unitIntWeights` (`_ ↦ 1`), differ at position `1`, and satisfy `mixSum (signedPlus 0) (signedPlus 1) = 4 ≠ 0 = mixSum (signedSplit 0) (signedSplit 1)` (`signed_square_presentations_split`, `presentation_scope`).

5. **Two-position descent classification (lines 414–473):**
   - `readOut (a b x y : Int) : Int := a * x + b * y` and `ModulusBlind (x y x' y' : Int) : Prop := x * x = x' * x' ∧ y * y = y' * y'`.
   - Using `sq_add_sub : (a + b) * (a + b) = (a - b) * (a - b) + 4 * (a * b)`, `descent_iff_subsingleton_support` establishes that `(∀ x y x' y', ModulusBlind x y x' y' → readOut a b x y * readOut a b x y = readOut a b x' y' * readOut a b x' y') ↔ a * b = 0`.

6. **Audit of the proposed climb (lines 480–522):**
   - `decoratedCarrierShape_exists` establishes `∃ (D : Type) (m : D → Nat) (op : D → D → D), (∀ n, ∃ d, m d = n) ∧ ∀ d e, m (op d e) = m (op e d)` using `D = Nat`, `m = id`, `op = (· + ·)`.
   - `ClaimedReadOutUniqueness` states that any `F : List Nat → Weights → Nat` that is `SameProfile`-invariant and append-additive (`F (l₁ ++ l₂) v = F l₁ v + F l₂ v`) must equal `total l w` whenever `0 < total l w`. `claimedReadOutUniqueness_false` refutes this by setting `F _ _ := 0` at `l = [0]` and `w _ := 1`.

---

## Plain-language interpretation

When each position `p` in a finite list `l` holds a natural-number count `w p`, we can test whether two count tables `w` and `v` have the same relative proportions without dividing by `total l w` and `total l v`: we cross-multiply (`w p * total l v = v p * total l w` for all `p ∈ l`).

On positive-total tables (`0 < total l w` and `0 < total l v`), this cross-multiplied equation is an equivalence relation (`profile_equivalence_positive`), holds if and only if `a * w p = b * v p` for some positive integers `a, b > 0` (`profile_iff_ray`), preserves which positions are zero (`profile_support`) and which positions are larger (`profile_order`), and forgets the overall multiplier (`profile_forgets_total`). At total `0`, however, both sides of `0 * total l w = w p * 0` evaluate to `0`, so the all-zero table is `SameProfile`-related to every table (`zero_scale_boundary`). That is why transitivity (`profile_trans`) requires `0 < total l v` on the middle table.

If `w` is presented as the square of an underlying decoration on each position:
- Over natural numbers `Nat` (`sq x = x * x`), squaring is injective (`sq_injective`), so `w` determines the decoration on `l` (`unsigned_decoration_determined`).
- Over integers `Int` (`sqInt x = x * x`), `+1` and `-1` have the same square `1`. On `[0, 1]`, `signedPlus` (`1, 1`) and `signedSplit` (`1, -1`) have the same pointwise squares `(1, 1)` while `(1 + 1)^2 = 4 ≠ 0 = (1 + (-1))^2` (`signed_square_presentations_split`). More generally, the squared linear combination `(a * x + b * y)^2` is invariant under sign flips of `x` and `y` (`ModulusBlind`) if and only if the cross term `4 * (a * b)` vanishes, i.e., `a * b = 0` (`descent_iff_subsingleton_support`).

---

## Pseudocode

```text
TOTAL(l, w):
  return sum(w[p] for p in l)

SAME_PROFILE(l, w, v):
  tw := TOTAL(l, w)
  tv := TOTAL(l, v)
  return all(w[p] * tv == v[p] * tw for p in l)

DESCENDS(a, b, bound):
  for x, y, x2, y2 in [-bound .. bound]^4:
    if x^2 == x2^2 and y^2 == y2^2:
      if (a*x + b*y)^2 != (a*x2 + b*y2)^2:
        return False
  return True
  -- This loop checks only the supplied finite box.
  -- The native theorem quantifies over all integer inputs, with no box bound.
```

For example, `DESCENDS(1, 1, 0)` returns true: the only inputs are zero,
so no sign distinction is tested. Yet `1 * 1` is nonzero, and the native
all-input invariance claim is false. At bound 1, inputs `(1,1)` and
`(1,−1)` already supply the differing readings 4 and 0, so the loop
returns false. The theorem and the bounded checker have different scopes.

---

## Python

From `code/derivation/weight_profile.py` (lines 19–47, 114–129, 198–211):

```python
Weights = dict[int, int]


def carrier_list(carrier: tuple[int, ...]) -> bool:
    """Carrier-facing reports require each label exactly once."""
    return len(carrier) == len(set(carrier))


def total(carrier: tuple[int, ...], w: Weights) -> int:
    """Raw list total; repeated labels count with multiplicity."""
    return sum(w.get(p, 0) for p in carrier)


def same_profile(carrier: tuple[int, ...], w: Weights,
                 v: Weights) -> bool:
    """Same normalized profile, cross-multiplied - no division."""
    tw, tv = total(carrier, w), total(carrier, v)
    return all(w.get(p, 0) * tv == v.get(p, 0) * tw for p in carrier)


def scale(w: Weights, a: int) -> Weights:
    return {p: a * x for p, x in w.items()}


def same_ray(carrier: tuple[int, ...], w: Weights, v: Weights,
             bound: int) -> bool:
    """Exists a positive pair (a, b) below the bound with
    a*w == b*v pointwise."""
    return any(
        all(a * w.get(p, 0) == b * v.get(p, 0) for p in carrier)
        for a in range(1, bound + 1) for b in range(1, bound + 1))


def sq(x: int) -> int:
    return x * x


def presents(carrier: tuple[int, ...], c: Weights,
             w: Weights) -> bool:
    """``c`` is a decorated presentation of ``w`` under squaring."""
    return carrier_list(carrier) and all(
        sq(c.get(p, 0)) == w.get(p, 0) for p in carrier)


def mix_sum(carrier: tuple[int, ...], c: Weights) -> int:
    """A declared MIXING read-out: the modulus of the combined
    decoration."""
    return sq(sum(c.get(p, 0) for p in carrier))


def read_out(a: int, b: int, x: int, y: int) -> int:
    return a * x + b * y


def descends(a: int, b: int, bound: int) -> bool:
    """Is the squared read-out constant on modulus-blind inputs?"""
    vals = range(-bound, bound + 1)
    for x, y, x2, y2 in product(vals, repeat=4):
        if x * x == x2 * x2 and y * y == y2 * y2:
            if (sq(read_out(a, b, x, y))
                    != sq(read_out(a, b, x2, y2))):
                return False
    return True
```

---

## Line-by-line Python explanation

- **`carrier_list(carrier)` and `total(carrier, w)` (lines 19–26):** `carrier_list` checks `len(carrier) == len(set(carrier))`; `total` sums `w.get(p, 0)` across `carrier` with multiplicity.
- **`same_profile(carrier, w, v)` and `same_ray(carrier, w, v, bound)` (lines 29–47):** `same_profile` checks `w.get(p, 0) * tv == v.get(p, 0) * tw` for all `p in carrier`; `same_ray` searches positive multipliers `1 <= a, b <= bound` such that `a * w[p] == b * v[p]` on `carrier`.
- **`sq`, `presents`, `mix_sum` (lines 114–129):** Implement squaring `x * x`, the square-presentation predicate `carrier_list(carrier) and all(sq(c[p]) == w[p] ...)`, and the squared sum `sq(sum(c[p] for p in carrier))`.
- **`read_out(a, b, x, y)` and `descends(a, b, bound)` (lines 198–210):** `read_out` evaluates `a * x + b * y`; `descends` tests whether `sq(read_out(a, b, x, y)) == sq(read_out(a, b, x2, y2))` for all 4-tuples `(x, y, x2, y2)` in `[-bound, bound]^4` with `x^2 == x2^2` and `y^2 == y2^2`.

---

## Lean 4

From `lean4/Derivation/WeightProfile.lean` (selected declarations and theorems across lines 57–522):

```lean
namespace WeightProfile

abbrev Weights := Nat → Nat

def CarrierList (l : List Nat) : Prop := l.Nodup

theorem duplicate_list_not_carrier : ¬ CarrierList [0, 0] := by
  simp [CarrierList]

def total (l : List Nat) (w : Weights) : Nat :=
  (l.map w).foldl (fun a b => a + b) 0

def SameProfile (l : List Nat) (w v : Weights) : Prop :=
  ∀ p ∈ l, w p * total l v = v p * total l w

theorem profile_trans (l : List Nat) (w v u : Weights)
    (hv : 0 < total l v) (h1 : SameProfile l w v)
    (h2 : SameProfile l v u) : SameProfile l w u

theorem zero_scale_boundary (l : List Nat) (w : Weights)
    (_hw : 0 < total l w) :
    SameProfile l (fun _ => 0) w ∧
      total l (fun _ => 0) = 0 ∧ ¬ 0 < total l (fun _ => 0)

theorem profile_iff_ray (l : List Nat) (w v : Weights)
    (hw : 0 < total l w) (hv : 0 < total l v) :
    SameProfile l w v ↔
      ∃ a b, 0 < a ∧ 0 < b ∧ ∀ p ∈ l, a * w p = b * v p

def Presents (l : List Nat) (m : Nat → Nat) (c : Nat → Nat)
    (w : Weights) : Prop :=
  CarrierList l ∧ ∀ p ∈ l, m (c p) = w p

theorem presentation_profile_redundant (l : List Nat) (m : Nat → Nat)
    (c : Nat → Nat) (w : Weights) (h : Presents l m c w) :
    SameProfile l (fun p => m (c p)) w

theorem unsigned_decoration_determined (l : List Nat)
    (c d : Nat → Nat) (w : Weights)
    (hc : Presents l sq c w) (hd : Presents l sq d w) :
    ∀ p ∈ l, c p = d p

def SignedSquarePresents (l : List Nat) (c : Nat → Int)
    (w : Nat → Int) : Prop :=
  CarrierList l ∧ ∀ p ∈ l, sqInt (c p) = w p

theorem signed_square_presentations_split :
    SignedSquarePresents [0, 1] signedPlus unitIntWeights ∧
    SignedSquarePresents [0, 1] signedSplit unitIntWeights ∧
    (∃ p ∈ [0, 1], signedPlus p ≠ signedSplit p) ∧
    mixSum (signedPlus 0) (signedPlus 1) ≠
      mixSum (signedSplit 0) (signedSplit 1)

def readOut (a b x y : Int) : Int := a * x + b * y

def ModulusBlind (x y x' y' : Int) : Prop :=
  x * x = x' * x' ∧ y * y = y' * y'

theorem sq_add_sub (a b : Int) :
    (a + b) * (a + b) = (a - b) * (a - b) + 4 * (a * b)

theorem descent_iff_subsingleton_support (a b : Int) :
    (∀ x y x' y', ModulusBlind x y x' y' →
      readOut a b x y * readOut a b x y
        = readOut a b x' y' * readOut a b x' y')
    ↔ a * b = 0

def ClaimedReadOutUniqueness : Prop :=
  ∀ (F : List Nat → Weights → Nat) (l : List Nat) (w : Weights),
    0 < total l w →
    (∀ v, SameProfile l w v → F l w = F l v) →
    (∀ l1 l2 v, F (l1 ++ l2) v = F l1 v + F l2 v) →
    F l w = total l w

theorem claimedReadOutUniqueness_false : ¬ ClaimedReadOutUniqueness
```

---

## Line-by-line Lean explanation

1. **Totals and ray scaling (lines 57–118):**
   - `foldl_add_acc` (line 71) establishes by induction on `l` that `l.foldl (fun x y => x + y) a = a + l.foldl (fun x y => x + y) 0`, yielding `total_cons`, `total_append`, `total_scale`, and `total_ray`.

2. **Profile equivalence and the zero-scale boundary (lines 121–224):**
   - `SameProfile` (line 121) is reflexive (`profile_refl`) and symmetric (`profile_symm`).
   - In `profile_trans` (line 131), `ac_rfl` rearranges `total l v * (w p * total l u)` through `h1 p hp` and `h2 p hp` into `total l v * (u p * total l w)`, and `Nat.eq_of_mul_eq_mul_left hv` cancels `total l v` using `hv : 0 < total l v`.
   - `profile_scale_raw` (line 153) establishes `SameProfile l (fun p => a * w p) w` for every `a : Nat` (including `a = 0`), and `zero_scale_boundary` (line 184) specializes to `a = 0`.
   - **Audit note on `zero_scale_boundary`:** Notice that the hypothesis `_hw : 0 < total l w` in `zero_scale_boundary` is prefixed with an underscore and never referenced in the proof: `SameProfile l (fun _ => 0) w ∧ total l (fun _ => 0) = 0 ∧ ¬ 0 < total l (fun _ => 0)` holds unconditionally for every `l` and `w` (checked in `textbook/checks/u64_lean.py`).
   - `profile_iff_ray` (line 198) establishes the forward direction with `a = total l v > 0` and `b = total l w > 0`, and the reverse direction using `total_ray` and `Nat.eq_of_mul_eq_mul_left ha`.

3. **Support, order, total erasure, and `Presents` (lines 228–322):**
   - `profile_support` (line 228) and `profile_order` (line 248) transfer `w p = 0 ↔ v p = 0` and `w p ≤ w q ↔ v p ≤ v q` across `w p * total l v = v p * total l w` under `hw : 0 < total l w` and `hv : 0 < total l v`.
   - `profile_forgets_total` (line 277) exhibits `(fun p => if p = 0 then 3 else 1)` and its double on `[0, 1]`.
   - `Presents l m c w` (line 290) bundles `CarrierList l` and `∀ p ∈ l, m (c p) = w p`; `presentation_profile_redundant` (line 305) uses only `h.2` and `total_congr` to prove `SameProfile l (fun p => m (c p)) w`.
   - **Audit note on `CarrierList`:** Although `CarrierList l` (`l.Nodup`) is included in `Presents` and `SignedSquarePresents`, and `paper/weight_profile_contact.md` §1 describes carrier-facing statements as using it, no theorem's proof in `WeightProfile.lean` ever reads `hc.1 : CarrierList l`. As shown in `textbook/audit/probes/F1/wp_carrier_unused.lean` and checked in `textbook/checks/u64_lean.py`, both `presentation_profile_redundant` and `unsigned_decoration_determined` hold on the duplicated list `[0, 0]` when `CarrierList` is omitted.

4. **Unsigned vs. signed squares, two-position descent, and climb refutation (lines 326–522):**
   - `sq_mono` (line 329) and `sq_injective` (line 338) establish `sq c = sq d → c = d` on `Nat`, yielding `unsigned_decoration_determined` (line 346).
   - `signed_square_presentations_split` (line 374) establishes that `signedPlus` (`1, 1`) and `signedSplit` (`1, -1`) both satisfy `SignedSquarePresents [0, 1] _ unitIntWeights` while `mixSum (signedPlus 0) (signedPlus 1) = 4 ≠ 0 = mixSum (signedSplit 0) (signedSplit 1)`.
   - `descent_iff_subsingleton_support` (line 442) evaluates `h 1 1 1 (-1)` for the forward direction and uses `sq_add_sub a b` to conclude `a * b = 0`; for the reverse direction, `Int.mul_eq_zero.mp` splits into `a = 0` or `b = 0` and applies `sq_mul`.
   - `decoratedCarrierShape_exists` (line 480) witnesses `(Nat, id, (· + ·))`, and `claimedReadOutUniqueness_false` (line 500) instantiates `ClaimedReadOutUniqueness` at the zero functional `fun _ _ => 0` on `l = [0]` and `w _ = 1` to derive `0 = 1`.

---

## What has been proved

- **Positive-total equivalence and ray characterization (`profile_refl`, `profile_symm`, `profile_trans`, `profile_equivalence_positive`, `profile_iff_ray`):** `SameProfile l w v` is an equivalence relation on assignments with `0 < total l w`, where it holds if and only if `a * w p = b * v p` on `l` for some `a, b > 0`.
- **Zero-total degeneracy (`profile_scale_raw`, `zero_scale_boundary`):** Scaling by `0` produces total `0` while remaining `SameProfile`-related to `w`, explaining why `0 < total l v` is required in `profile_trans`.
- **Invariants and forgotten scale (`profile_support`, `profile_order`, `profile_forgets_total`).**
- **Redundancy of decorated presentations for the profile (`total_congr`, `presentation_profile_redundant`, `presentations_agree_on_profile`).**
- **Unsigned determination vs. signed splitting (`unsigned_decoration_determined`, `signed_square_presentations_split`, `presentation_scope`).**
- **Two-position descent criterion and climb audit (`descent_iff_subsingleton_support`, `decoratedCarrierShape_exists`, `claimedReadOutUniqueness_false`, `finite_scope_summary`).**

---

## What has not been proved

- **No bridge to `Basic.lean` or `PrimitivePassage.lean`:** Nothing in `WeightProfile.lean` connects `Weights`, `CarrierList`, `SameProfile`, `Presents`, `SignedSquarePresents`, or `readOut` to `Basic.Regime`, `Basic.Context`, `Basic.separable`, or `PrimitivePassage.PState`.
- **`CarrierList` (`l.Nodup`) is not consumed in any proof in `WeightProfile.lean`:** Although `CarrierList l` is conjoined into `Presents` and `SignedSquarePresents`, no theorem in `WeightProfile.lean` uses `l.Nodup`; the proofs depend only on pointwise membership `p ∈ l` and `foldl` summation over `l`.
- **`_hw : 0 < total l w` in `zero_scale_boundary` is unused:** Its three conjuncts hold for every `l` and `w` without assuming `0 < total l w`.
- **`decoratedCarrierShape_exists` is a trivial witness (`(Nat, id, (· + ·))`):** As its docstring notes (lines 476–479), it shows only that the bare existential was too weak to be a non-trivial rung.

---

## Outside the system

1. **Metatheory types and quantifiers:**
   - `Weights := Nat → Nat` and `Nat → Int` are total functions on all of `Nat` in Lean's type theory, even though `total l w` and `SameProfile l w v` inspect them only at positions `p ∈ l`.
   - `Int` arithmetic (negation `-1`, subtraction, and `sq_add_sub`), the type-level existential `∃ (D : Type)` in `decoratedCarrierShape_exists`, and the higher-order quantifier `∀ F : List Nat → Weights → Nat` in `ClaimedReadOutUniqueness` belong to the Lean metatheory.
2. **What the system itself holds:**
   - The system ledger of Units 01–63 holds no `Weights` function and no `Int` decoration; `WeightProfile` is a standalone arithmetic module on finite position lists `l : List Nat`.
3. **Admissions and their prices:**
   - Every definition in `WeightProfile.lean` (`Weights`, `CarrierList`, `total`, `SameProfile`, `Presents`, `sq`, `sqInt`, `SignedSquarePresents`, `mixSum`, `readOut`, `ModulusBlind`, `ClaimedReadOutUniqueness`) is admitted directly in Lean (`paper/weight_profile_contact.md`).
4. **Phrases to read without importing outside structure:**
   - Calling `SameProfile` a "ray" relation refers strictly to the cross-multiplied integer equation `w p * total l v = v p * total l w` and the positive-integer multiplier equivalence `profile_iff_ray`, not to a continuum or real-number division.

---

## Student exercise

Let `l = [0, 1]`, and consider the three weight assignments on `l`:
- `u` with `u 0 = 1, u 1 = 2`,
- `v` with `v 0 = 0, v 1 = 0`,
- `w` with `w 0 = 2, w 1 = 1`.

1. Compute `total l u`, `total l v`, and `total l w`.
2. Show that `SameProfile l u v` and `SameProfile l v w` both hold, while `SameProfile l u w` is false. Which hypothesis of `profile_trans` fails here?
3. For `a = 2, b = 3`, evaluate `(readOut 2 3 1 1)^2` and `(readOut 2 3 1 (-1))^2`, and verify that their difference equals `4 * (2 * 3) = 24` (`sq_add_sub`).

---

## Answer

1. **Totals:**
   - `total [0, 1] u = 1 + 2 = 3`,
   - `total [0, 1] v = 0 + 0 = 0`,
   - `total [0, 1] w = 2 + 1 = 3`.
2. **Transitivity failure across a zero-total middle assignment:**
   - For `SameProfile [0, 1] u v`: at `p ∈ {0, 1}`, `u p * total [0, 1] v = u p * 0 = 0 = 0 * 3 = v p * total [0, 1] u`.
   - For `SameProfile [0, 1] v w`: at `p ∈ {0, 1}`, `v p * total [0, 1] w = 0 * 3 = 0 = w p * 0 = w p * total [0, 1] v`.
   - For `SameProfile [0, 1] u w`: at `p = 0`, `u 0 * total [0, 1] w = 1 * 3 = 3`, whereas `w 0 * total [0, 1] u = 2 * 3 = 6`, and `3 ≠ 6`.
   - The hypothesis `hv : 0 < total l v` of `profile_trans` fails because `total [0, 1] v = 0`.
3. **Two-position `readOut` square difference:**
   - `(readOut 2 3 1 1)^2 = (2 * 1 + 3 * 1)^2 = 5^2 = 25`.
   - `(readOut 2 3 1 (-1))^2 = (2 * 1 + 3 * (-1))^2 = (-1)^2 = 1`.
   - Their difference is `25 - 1 = 24 = 4 * (2 * 3)`, matching `sq_add_sub 2 3`.

---

## Verification

| Check | Source |
|---|---|
| Lean | `lean4/Derivation/WeightProfile.lean` lines 57–522 (`lake build Derivation.WeightProfile`) |
| Axiom report | `artifacts/lean_axioms.txt` lines 858–888 (25 `[propext, Quot.sound]`, 2 `[propext]`, 4 `none`) |
| Paper | `paper/weight_profile_contact.md`; `paper/paper_claim_ledger.md` `CL-PD2-WEIGHT-PROFILE` |
| Python | `code/derivation/weight_profile.py`, `code/run_weight_profile.py`, `tests/test_weight_profile.py`, `artifacts/weight_profile.json` |
| Audit | `textbook/audit/modules/WeightProfile.md` and `textbook/audit/probes/F1/wp_carrier_unused.lean` (`CarrierList` unused in proofs; `_hw` unused in `zero_scale_boundary`) |
| Check (Python) | `python textbook/checks/u64_weight_profile.py` |
| Check (book Lean) | `python textbook/checks/u64_lean.py` |
