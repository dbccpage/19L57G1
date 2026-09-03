import FreshCharacters.Characters

/-!
# The fresh part of a layer, and the integer a fresh total reduces to

Stages 2 and 3 of the fresh_characters run, in Lean.  Everything here
originates in this tree.

Menu member V6, declared in `PREDICTIONS.md` before any computation: the
value carrier is the free abelian group on the layer's members -- integer
combinations of members, the step permuting them -- taken modulo the layer's
FRESH PART.  The fresh part is defined by the same divisor recursion the
pinned `balance` uses: the layer's own difference, `x^n - 1`, divided by the
fresh parts of every proper divisor layer.  `Balance.balanceFuel` is that
recursion on integers; `freshPartFuel` below is the same recursion on
integer combinations, and no other property of it is assumed.

`total n a` is the integer a fresh total reduces to under V6, when it
reduces to one at all; `isConst` records whether it did, and no statement
below reads `total` without it.

Every general statement here is about the DEFINITIONS.  Every numeric
statement is a kernel-decided instance with its bound in its name and in its
statement, and nothing extends past that bound (FW-SCOPE).
AuthorityEffect: None.
-/

namespace FreshCharacters
namespace FreshPart

/-- An integer combination of the layer's members, little-endian: index `i`
is the coefficient of the `i`-th member. -/
abbrev Poly : Type := List Int

/-- Drop the trailing zero coefficients. -/
def trim : Poly → Poly
  | [] => []
  | a :: p =>
    match trim p with
    | [] => if a == 0 then [] else [a]
    | q => a :: q

def padd : Poly → Poly → Poly
  | [], q => q
  | p, [] => p
  | a :: p, b :: q => (a + b) :: padd p q

def pneg (p : Poly) : Poly := p.map (fun x => -x)

def psub (p q : Poly) : Poly := padd p (pneg q)

/-- Multiply by the `k`-th power of the step generator. -/
def shift (k : Nat) (p : Poly) : Poly := List.replicate k 0 ++ p

def cscale (s : Int) (p : Poly) : Poly := p.map (fun x => s * x)

/-- The generator raised to `k`. -/
def monoOne (k : Nat) : Poly := shift k [1]

/-- Division with remainder by a MONIC divisor, from the top, with fuel.
Exact on the divisors this tree uses, all of which are monic. -/
def pdivmodAux : Nat → Poly → Poly → Poly → Poly × Poly
  | 0, r, _, q => (q, trim r)
  | fuel + 1, r, g, q =>
    let tr := trim r
    let tg := trim g
    if tg.length == 0 then (q, tr)
    else if tr.length < tg.length then (q, tr)
    else
      let k := tr.length - tg.length
      let c := tr.getLast?.getD 0
      pdivmodAux fuel (psub tr (shift k (cscale c tg))) g (padd q (shift k [c]))

def pdivmod (p g : Poly) : Poly × Poly :=
  pdivmodAux ((trim p).length + 1) p g []

/-- The layer's own difference: the `n`-th power of the generator, less the
unit. -/
def layerDiff (n : Nat) : Poly := psub (monoOne n) [1]

/-- The fresh part of the layer, by the divisor recursion: the layer's
difference divided by the fresh part of every proper divisor layer.  Same
shape as the pinned `balanceFuel`. -/
def freshPartFuel : Nat → Nat → Poly
  | 0, _ => [1]
  | f + 1, n =>
    (Balance.divisorsBelow n).foldl
      (fun acc d => (pdivmod acc (freshPartFuel f d)).1) (layerDiff n)

def freshPart (n : Nat) : Poly := freshPartFuel n n

/-- The fresh total at step `a`, as an integer combination of members. -/
def freshPoly (n a : Nat) : Poly :=
  (Char.freshExp n a).foldl (fun acc e => padd acc (monoOne e)) []

def reduceMod (p g : Poly) : Poly := trim (pdivmod p g).2

/-- Whether the reduced fresh total is a plain integer multiple of the
unit. -/
def isConst (p : Poly) : Bool := decide ((trim p).length ≤ 1)

def constOf (p : Poly) : Int := (trim p).headD 0

/-- The integer a fresh total reduces to under V6.  Read only alongside
`isConstTotal`. -/
def total (n a : Nat) : Int := constOf (reduceMod (freshPoly n a) (freshPart n))

def isConstTotal (n a : Nat) : Bool :=
  isConst (reduceMod (freshPoly n a) (freshPart n))

/-! ## Decided instances -- stage 2

Each theorem names its bound and says nothing beyond it. -/

set_option maxRecDepth 40000 in
/-- Every fresh total at every step reduces to a plain integer, for part
counts `1..20`.  A statement about `n <= 20` and nothing beyond it. -/
theorem total_is_constant_to_20 :
    (List.range 20).all (fun i =>
      (List.range (i + 1)).all (fun a => isConstTotal (i + 1) a)) = true := by
  decide +kernel

set_option maxRecDepth 40000 in
/-- The fresh total at the unit step IS the pinned balance, for part counts
`1..20`.  A statement about `n <= 20` and nothing beyond it; the general
statement is not proved here. -/
theorem total_unit_step_is_balance_to_20 :
    (List.range 20).map (fun i => total (i + 1) 1)
      = (List.range 20).map (fun i => Balance.balance (i + 1)) := by
  decide +kernel

set_option maxRecDepth 40000 in
/-- The fresh total at the zero step is the pinned fresh count, for part
counts `1..20` -- the computed half of `character_trivial_total`, which
`Char.freshExp_zero` proves for every part count. -/
theorem total_zero_step_is_freshCount_to_20 :
    (List.range 20).map (fun i => total (i + 1) 0)
      = (List.range 20).map (fun i => (Balance.freshCount (i + 1) : Int)) := by
  decide +kernel

/-! ## Decided instances -- stage 3 -/

/-- The divisor sum of the totals at a fixed step, each divisor layer read
at the step taken in that layer. -/
def divisorTotal (n a : Nat) : Int :=
  Balance.sumI ((Balance.divisors n).map (fun d => total d (a % d)))

set_option maxRecDepth 40000 in
/-- The divisor recursion, decided for part counts `1..16` and every step
below the part count: the divisor sum of the totals is the part count when
the step is zero and vanishes otherwise.  At the unit step and a part count
above one this is the pinned `balance_divisor_sum`; the statement here is
the same shape carried to every step, and it is decided, not proved.  A
statement about `n <= 16` and nothing beyond it. -/
theorem divisor_recursion_to_16 :
    (List.range 16).all (fun i =>
      (List.range (i + 1)).all (fun a =>
        divisorTotal (i + 1) a == (if a == 0 then ((i + 1 : Nat) : Int) else 0)))
      = true := by
  decide +kernel

set_option maxRecDepth 40000 in
/-- The totals depend on the step only through the largest divisor the step
shares with the part count, decided for part counts `1..20`.  A statement
about `n <= 20` and nothing beyond it. -/
theorem total_depends_on_shared_divisor_to_20 :
    (List.range 20).all (fun i =>
      (List.range (i + 1)).all (fun a =>
        (List.range (i + 1)).all (fun b =>
          (Nat.gcd a (i + 1) != Nat.gcd b (i + 1))
            || (total (i + 1) a == total (i + 1) b))))
      = true := by
  decide +kernel

end FreshPart
end FreshCharacters
