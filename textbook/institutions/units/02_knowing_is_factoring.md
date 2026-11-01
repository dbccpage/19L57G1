# Unit 02. Knowing a claim is factoring through the representative

**Claim.** A family knows a question, in this model, when its answer is
recoverable from the combined signature. This is functional
determination on the carrier, rather than belief or truth.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** A family knows a claim exactly when data the family cannot tell
apart always get the same value from the claim:
`Knows D Q q ↔ ∀ x ∈ D, ∀ y ∈ D, SigEq Q x y → q x = q y`.

**Status:** derived. **Lean:** `Institution.knows_iff_determined`
(`two_theorems`). **Sources:**
`research/two_theorems/lean/ResearchTwoTheorems/Institution.lean` lines
65–80; `lean4/Derivation/Compression.lean` lines 100–105 and 171–189.

"Knows" is the first word of this part that a reader will want to mean
more than it does. This unit fixes what it is attached to: a claim is one
more presentation `q`, and the family knows it when `q` is a function of
the family's representative. Nothing is believed, asserted or true here;
Unit 08 is about truth and Unit 09 about asserting.

</details>

## First pass

Keep I00's first presentation, [0,1,0] on inputs [0,1,2]. A lookup using
that presentation receives the same stored label for inputs 0 and 2.

| Requested answer table | Recoverable? | Reason |
|---|---|---|
| [7,9,7] | Yes | Label 0 gives 7; label 1 gives 9 |
| [7,8,9] | No | Label 0 would need two different answers |

Factors through means this recoverability condition. Knows applies it
to the family's combined representative. Both terms describe a condition
on supplied tables; neither asserts that an answer is true.

**Predict:** does a recoverable constant answer 7 establish a correct
prediction about the world?

<details><summary>Check your prediction</summary>

No. It establishes that a lookup can return 7. Comparing that answer
with a target is a separate question introduced in I08.

</details>

## What you need first

Unit 00 (`SigEq`) and Unit 01 (`pQ`, `pQ_exact`, `pick`).

Keep the roles separate: `p` is the available presentation, `q` is the
requested answer table, and `g` is one lookup receiving only p's output.
The same g must work for every input on the carrier. It cannot inspect
the original input to decide which answer to return.

### 1. Factoring

<details>
<summary>Lean source: FiberConstant, FactorsOn (optional)</summary>

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 99–105
/-- The fibers of `p` over `D` are `q`-constant. -/
def FiberConstant (D : List Nat) (p q : Nat → Nat) : Prop :=
  ∀ x, x ∈ D → ∀ x', x' ∈ D → p x = p x' → q x = q x'

/-- `q` factors through `p` on `D`. -/
def FactorsOn (D : List Nat) (p q : Nat → Nat) : Prop :=
  ∃ g : Nat → Nat, ∀ x, x ∈ D → g (p x) = q x
```

</details>

There are two ways to ask whether the lookup can work.

**Build a lookup.** `q` *factors through* `p` if one function g recovers
q from p on the carrier. In the successful table above, g(0)=7 and
g(1)=9 work for all three inputs. Values of g on unused labels are not
fixed by this requirement.

**Look for a conflict.** A **fiber** is a group of inputs with the same
p-value. `q` is *fiber-constant* for `p` when q gives the same answer
throughout each such group. In the failed table, inputs 0 and 2 would
require both g(0)=7 and g(0)=9. One function cannot do both.

On the finite carrier, the two conditions are equivalent. The sealed
proof constructs a lookup when no such conflict exists:

<details>
<summary>Lean source: factors_iff_fiberConstant (optional)</summary>

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 171–189
theorem factors_iff_fiberConstant (D : List Nat) (p q : Nat → Nat) :
    FactorsOn D p q ↔ FiberConstant D p q := by
  constructor
  · intro hf x hx x' hx' hp
    obtain ⟨g, hg⟩ := hf
    rw [← hg x hx, ← hg x' hx', hp]
  · intro hfc
    refine ⟨fun y => q ((pick D (fun z => decide (p z = y))).getD 0),
      ?_⟩
    intro x hx
    obtain ⟨r, hr⟩ :=
      pick_some_of_mem D (fun z => decide (p z = p x)) x hx
        (decide_eq_true rfl)
    have hrD := pick_mem D (fun z => decide (p z = p x)) r hr
    have hpr : p r = p x :=
      of_decide_eq_true (pick_holds D _ r hr)
    show q ((pick D (fun z => decide (p z = p x))).getD 0) = q x
    rw [hr]
    exact hfc r hrD x hx hpr
```

</details>

Left to right: given `g` with `g (p x) = q x` on the carrier, if `p x =
p x'` then `q x = g (p x) = g (p x') = q x'` (the three rewrites). Right
to left is the constructive half: define `g y` to be the value of `q` at
the first datum of the carrier whose `p`-value is `y`. For `x` on the
carrier, that search finds some `r` with `p r = p x` (`pick_some_of_mem`,
`pick_holds`), on the carrier (`pick_mem`), and fiber-constancy gives
`q r = q x`. No choice principle is used: `g` is a list search.

```
# Gloss
q factors through p  <=>  q is a function of p's value  <=>  p merges x, x'  implies  q merges x, x'
```

### 2. Knowing

<details>
<summary>Lean source: Knows (optional)</summary>

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Institution.lean lines 65–67
/-- The institution knows `q` on `D`: `q` factors through its actor. -/
def Knows (D : List Nat) (Q : Institution) (q : Nat → Nat) : Prop :=
  FactorsOn D (pQ D Q) q
```

</details>

The family knows `q` when `q` factors through the representative. By
Unit 01 the representative's fibers are the signature classes, so the
unit's theorem is one rewrite away.

```python
# Python (research), research/actor_institution/model.py lines 135–137
def knows(n: int, Q: Institution, q: Presentation) -> bool:
    """`Institution.Knows` on range(n): equal signatures force equal values."""
    return all(sig(Q, x) != sig(Q, y) or q[x] == q[y] for x in range(n) for y in range(n))
```

The Python takes the theorem's right-hand side as the definition; the
check below confirms it agrees with factoring through the representative.

```
# Gloss
on [0, 1, 2] with Q = (p1, p2):   every signature differs, so the family knows EVERY claim
with Q = (p1) alone:   0 and 2 share a signature, so the family knows q  iff  q(0) = q(2);
                       it knows p1 and knows the constants; it does not know q3 = (0, 0, 1)
```

## The theorem

<details>
<summary>Lean source: knows_iff_determined (optional)</summary>

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Institution.lean lines 71–80
theorem knows_iff_determined (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q q ↔ ∀ x, x ∈ D → ∀ y, y ∈ D → SigEq Q x y → q x = q y := by
  unfold Knows
  rw [factors_iff_fiberConstant]
  unfold FiberConstant
  constructor
  · intro h x hx y hy hs
    exact h x hx y hy ((pQ_exact D Q x hx y hy).mpr hs)
  · intro h x hx y hy hp
    exact h x hx y hy ((pQ_exact D Q x hx y hy).mp hp)
```

</details>

Read: "the family knows `q` exactly when, for any two data on the carrier
that every member gives the same value, `q` gives them the same value."
The right-hand side is what `two_theorems` calls *signature
determination*: the signature determines the value of `q`.

I01 identifies equal representative labels with equal signatures on the carrier. I02 can therefore replace one condition by the other when checking whether the requested answers agree. Both directions use that same identification.

<details>
<summary>Detailed proof steps (optional)</summary>

## The proof, step by step

**Step 1. `unfold Knows`.** Replace `Knows D Q q` by its definition,
`FactorsOn D (pQ D Q) q`.

**Step 2. `rw [factors_iff_fiberConstant]`.** Replace factoring by
fiber-constancy, by the sealed theorem above. The goal's left side is now
`FiberConstant D (pQ D Q) q`.

**Step 3. `unfold FiberConstant`.** Spell it out: for all `x`, `x'` on the
carrier, `pQ D Q x = pQ D Q x' → q x = q x'`. Now both sides of the `↔`
have the same shape; they differ only in the hypothesis, `pQ D Q x = pQ D
Q y` on the left against `SigEq Q x y` on the right.

**Step 4. `constructor`.** Two implications.

**Step 5. Left to right.** Assume `h` (the representative-form) and take
`x`, `y` on the carrier with `hs : SigEq Q x y`. `pQ_exact` read right to
left turns `hs` into `pQ D Q x = pQ D Q y`, which is what `h` needs; `h`
returns `q x = q y`.

**Step 6. Right to left.** Assume `h` (the signature form) and take `x`,
`y` with `hp : pQ D Q x = pQ D Q y`. `pQ_exact` read left to right turns
`hp` into `SigEq Q x y`; `h` returns `q x = q y`.

Both directions are Unit 01 applied once. The content of the theorem is
that "known" can be checked pair by pair on the carrier, with no function
`g` to find: if a claim never splits a signature class, the `g` exists,
and the sealed proof builds it.

</details>

## The same fact in Python

The check tests whether the claim's value at `x` equals its value at the
representative of `x`. For this particular first-input representative,
that condition gives the witness g(r)=q(r). It is not a test for factoring
through an arbitrary presentation p: for that task, p's output label
need not be a representative input.

It compares this condition with `model.knows` on `range(n)`, `1 ≤ n ≤ 4`,
using the empty family, each single partition, and one ordering of each
pair of distinct partitions, with every partition as the claim:
1905 cases, no disagreement, 1187 of them known. These cases do not
enumerate all ordered lists or repetitions.

```
python textbook/institutions/checks/i02_knowing.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `∃ g : Nat → Nat, …` | "there is a way to read `q` off the representative" | an existential over Lean's function type, discharged by building `g` from a list search (no choice principle; the tree's axiom report lists `propext` and `Quot.sound` only) |
| `Nat → Nat` for `q` | the claim | metatheory; the system holds its table on `D` |
| `∀ x, x ∈ D → ∀ y, y ∈ D → …` | the pairwise condition | over the finite carrier, finitely many pairs |
| `unfold`, `rw`, `constructor`, `exact` | checking the proof | metatheory |

**What the system holds.** The carrier, the members' tables, the claim's
table. "Knows" adds nothing to the ledger: it is a relation between tables
already there, decided by comparing finitely many pairs (`knowsB`, Unit
09, computes it).

**Admissions relied on, and their price.** Unit 00's three. The
definition of `Knows` itself is admitted: the tree declares that knowing
is factoring. Its price is that "knows" says nothing about where the
claim came from, whether anyone holds it, or whether it is true. What it
buys is a notion that is decided by the tables alone.

**Phrases to read with care.**

- "The institution knows `q`" means `q` is determined by the signature.
  No member need know it (Unit 04), and nothing need be true (Unit 08).
- "`g` recovers `q`" names a function in Lean's metatheory. The system
  does not compute `g`; the theorem says one exists, and the sealed proof
  says how one would be written down.
- "Determined" is functional determination: same signature, same value.
  It is not causation and not justification.

## What it shows, and what it does not

It shows that knowing, as the trees define it, is a pairwise condition on
the carrier: the claim never separates what the family merges.

It shows that the definition is stable under the two readings, factoring
and determination; later units use whichever is convenient.

It does not show that any member knows the claim. Unit 04 gives a family
that knows a claim none of its members knows.

It does not show that a known claim is true, or that the family can say
how it knows. "Knows" is a property of tables. Unit 08 proves that the
family knows two claims that cannot both correspond to anything, and Unit
09 says what the family can do with a claim it does not know.

## Sources

| Item | Where |
|---|---|
| `FiberConstant`, `FactorsOn`, `factors_iff_fiberConstant` | `lean4/Derivation/Compression.lean` lines 100–105, 171–189 |
| `Knows` | `research/two_theorems/lean/ResearchTwoTheorems/Institution.lean` lines 65–67 |
| `knows_iff_determined` | the same file, lines 71–80; axiom reports emitted by the tree's `AxiomReport.lean` and checked by `research/two_theorems/verify.py --check` (`propext`, `Quot.sound`) |
| Python mirror | `research/actor_institution/model.py` lines 135–137 |
| Check | `textbook/institutions/checks/i02_knowing.py` |
| Ledger | `research/two_theorems/CLAIMS.md` TT-08 (knowledge is signature determination); sealed factoring in `paper/paper_claim_ledger.md`, `CL-PD2-COMPRESSION` part A |
