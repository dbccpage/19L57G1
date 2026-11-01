# Unit 20. The self-loop regime `BD` separates

**Claim.** On `R2L`, one binary form and a self-loop instance also distinguish
the data at cost two. Reversible renaming cannot turn this loop into the
link of Unit 19.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Starting from `R2L`, admitting one binary form and one instance
relating datum 0 to itself also separates the two data. The witness is "hole first, datum 0
second": plugged with 0 it is the admitted loop `(0, [0, 0])`, plugged
with 1 it is `(0, [1, 0])`, not admitted. This regime, `BD`, is not
isomorphic to the link `BL`: an isomorphism would have to send both ends
of the link onto one datum.

**Status:** derived. **Lean:**
`Derivation.BD_separable` (`lean4/Derivation/Minimality.lean` lines
55-56), `BD` (line 44), `deltaBD_valid` (88-89), `BL_not_iso_BD`
(270-280). **Axioms:** `propext, Quot.sound`. **Depends on:** Unit 19
(the same machinery, a different instance); `Iso` (Unit 21, introduced
there in full).

</details>

## First pass

Keep two data and one two-place form. This time admit only
`link(0, 0)`, with no uniform rule. Ask “is `link(□, 0)` derivable?”

| Fill the square with | Result | Derivable? |
|---|---|---|
| 0 | `link(0,0)` | Yes |
| 1 | `link(1,0)` | No |

The question distinguishes the pair even though
the admitted instance mentions only 0.

A **self-loop** repeats one datum in both argument positions. This is
allowed by this admission grammar. It is separate from asking the caller
to impose a self-demand, which Unit 17's guard rejects.

**Predict:** can renaming turn `link(0, 1)` into `link(0, 0)`?

<details>
<summary>Check your prediction</summary>

No. A reversible renaming cannot send two different data to the same
datum. The link and loop remain different structures under the declared
notion of renaming, although each costs two items.

</details>

The separation claim uses the exact record above. With a uniform rule,
both pluggings derive and the loop no longer distinguishes the pair.

## Question

The link used both data. Can a sentence about *one* datum separate the
two? And if a self-loop on 0 separates 0 from 1, is the resulting regime
really different from the link, or the same structure drawn differently?

## What we already possess

- `separable`, `wfCtx`, `plug`, `derivable` (Unit 08); the existential
  shape of a separability proof (Unit 19).
- `validResponse_R2L` (Unit 19): applying and separating is enough on
  `R2L`.
- Isomorphism of regimes is, informally, a relabelling of data and
  forms that preserves everything (Unit 21 gives the Lean structure).

## New concept: separating by presence, not by relation to the other

`BD = ⟨2, [2], [(0, [0, 0])], [], [(0, 1)]⟩`; the name stands for *binary
diagonal*. The instance mentions datum 0 twice and datum 1 not at all.
Still 1 is separated from 0, because "⟨ ⟩ relates to 0" is true of 0 and
false of 1. Separation in Genesis's declared sense needs one datum to
have a property the other lacks; it does not need the two to be related
to each other.

The paper calls this the self-loop realizing ⟨ARA⟩. It appears among the
`mu1` minima as the class `form2+inst2diag`.

## Plain-language interpretation

Imagine a record of numbered cards with only the entry “0 links to 0.”
The fixed question “does this card link to 0?” has different lookup
answers on 0 and 1. This is a toy record; no physical card relationship
has been observed. Here the demand is met by one positive derivability
answer and one negative answer to the same question. Mentioning just one datum
is not sufficient in every regime: other instances or a uniform rule
can make the other plugging derivable too. The example works because
there is exactly this one instance and no rule.

Then the second question. The link and the loop each have one form of
arity 2 and one instance. Are they the same regime up to renaming? No.
A renaming is a bijection of data; it must send the link's instance
`(0, [0, 1])` to an instance of the loop regime, and the only instance
there is `(0, [0, 0])`. That forces both 0 and 1 to go to 0, which is
not a bijection. So the two are genuinely different answers to the same
demand at the same cost. Unit 21 draws the consequence.

<details>
<summary>Programs and proof walkthroughs (optional)</summary>

## Pseudocode

```
# Gloss
BD: data {0, 1}; form 0 of arity 2; instance (0, [0, 0]); demand (0, 1)
context c := (form 0, slots [hole, 0])
plug(c, 0) = (0, [0, 0])  -- admitted
plug(c, 1) = (0, [1, 0])  -- not admitted
⇒ separable(BD, 0, 1)
No isomorphism BL → BD:
  the link instance (0, [0, 1]) must map to an instance of BD, i.e. to (0, [0, 0])
  so dmap 0 = 0 and dmap 1 = 0;  then dinv (dmap 0) = dinv (dmap 1), so 0 = 1.  ✗
```

## Python

```python
from derivation.candidates import NewForm, NewInst, apply_delta
from derivation.engine import GENESIS_L
from derivation.iso import isomorphic
from derivation.model import replay
from derivation.observe import profile, witness

base = replay(GENESIS_L)
bd = apply_delta(base, (NewForm(2), NewInst(0, (0, 0))))
bl = apply_delta(base, (NewForm(2), NewInst(0, (0, 1))))
print(witness(bd, 0, 1), sorted(profile(bd, 0), key=str), sorted(profile(bd, 1), key=str))
print(isomorphic(bl, bd), isomorphic(bd, apply_delta(base, (NewForm(2), NewInst(0, (1, 1))))))
```

Output:

```text
(0, (None, None)) [(0, (0, None)), (0, (None, 0)), (0, (None, None))] []
False True
```

## Line-by-line Python explanation

`bd` is the loop regime built by `apply_delta` (Unit 19).

`witness(bd, 0, 1)` returns `(0, (None, None))`, the two-hole context,
because it comes first in enumeration order: plugging both holes with 0
gives the loop, with 1 gives `(0, (1, 1))`. Lean names a different
witness, `(0, (None, 0))`. Both are witnesses; the check script prints
all three (`(None, None)`, `(None, 0)`, `(0, None)`). A separability
claim is true as soon as one exists.

Datum 0's profile has three contexts; datum 1's is empty. Compare the
link, where each profile had one. The loop gives 0 more to say, and 1
nothing.

`isomorphic` (`iso.py` line 215) compares canonical forms under the
implemented isomorphism (paper §3, definition 8). Link and loop: `False`.
Loop on 0 and loop on 1: `True`, the swap of data carries one to the
other, so the artifact's `form2+inst2diag` class has size 2.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Minimality.lean lines 44, 55-56, 270-280
/-- Binary self-loop. -/
def BD : Regime := ⟨2, [2], [(0, [0, 0])], [], [(0, 1)]⟩

theorem BD_separable : separable BD 0 1 :=
  ⟨⟨0, [none, some 0]⟩, by decide, by decide⟩

/-- The self-loop is not the link: instance preservation would force the
datum bijection to collapse two data. -/
theorem BL_not_iso_BD (iso : Iso BL BD) : False := by
  have h := iso.insts_fwd (0, [0, 1]) (by decide)
  have h01 : iso.dmap 0 = 0 ∧ iso.dmap 1 = 0 := by
    simp [BD] at h
    exact ⟨h.2.1, h.2.2⟩
  have i0 := iso.dinv_dmap 0 (by decide)
  have i1 := iso.dinv_dmap 1 (by decide)
  rw [h01.1] at i0
  rw [h01.2] at i1
  omega
```

## Line-by-line Lean explanation

`BD_separable` has the same three-part shape as Unit 19's proof, with
the witness `⟨0, [none, some 0]⟩`. The book's `BD_separable'` names the
steps: `plug … 0 = (0, [0, 0])` and `plug … 1 = (0, [1, 0])` by `rfl`,
derivability of the first and not the second by `decide`.

`BL_not_iso_BD` takes a supposed isomorphism `iso : Iso BL BD` (Unit 21
lists the fields) and derives `False`.

- `iso.insts_fwd` says every instance of `BL` is carried to an instance of
  `BD`: `(iso.fmap 0, [0, 1].map iso.dmap) ∈ BD.insts`. The membership
  `(0, [0, 1]) ∈ BL.insts` is by `decide`.
- `BD.insts` is the one-element list `[(0, [0, 0])]`, so `simp [BD] at h`
  turns membership into equations: the form maps to 0, and
  `iso.dmap 0 = 0`, `iso.dmap 1 = 0`. The last two are `h.2.1` and
  `h.2.2`.
- `iso.dinv_dmap` says `dinv` undoes `dmap` on admitted data:
  `dinv (dmap 0) = 0` and `dinv (dmap 1) = 1`. Rewriting with the two
  equations gives `dinv 0 = 0` and `dinv 0 = 1`.
- `omega` finds `0 = 1` among the hypotheses and closes the goal.

The argument does not need the arity-preservation field or the
form-inverse fields; the two regimes have the same arity. Instance
preservation already forces two distinct data to have the same image,
contradicting the datum-inverse fields.

**Axioms.** `propext, Quot.sound` for `BD_separable`, `deltaBD_valid` and
`BL_not_iso_BD` (all decide concrete memberships); `propext` for the
landing equation `applyDelta R2L deltaBD = some BD`.

</details>

## What has been proved

- `BD` separates 0 from 1 with the named witness (Genesis, derived).
- `deltaBD` lands on `BD` and is a valid response (Genesis, derived).
- There is no isomorphism from `BL` to `BD` (Genesis, derived).
- The link's witness does not witness the loop, and the two-hole context
  witnesses the loop but not the link (book, derived by `decide`).
- The loop on 1 is isomorphic to the loop on 0 (Genesis, verified finite
  in Python; the Lean `isoU1U0` of Unit 21 is the analogous statement for
  the unary marks).
- With the uniform rule for its only form, `BD` is collapsed despite
  retaining the loop instance (book, `BD_uniform_collapsed`). Mentioning
  one datum alone is not a general guarantee of separation.

## What has not been proved

- `Iso BD BL → False` in the frozen derivation. Genesis proves the
  direction it needs; no Genesis theorem states the other. The book
  proves it in Unit 21 (`isoSymm`, then `BL_not_iso_BD`), as book Lean
  outside the frozen inventory.
- That the loop is a *good* answer. Under `mu2` (Unit 22) it is not
  minimal, for the same reason as the link.
- That the system "knows" 0 is related to itself. It holds the list
  `[0, 0]`; the word "self" is the metatheory noticing the two entries
  are equal.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `BD` literal | the regime | admitted by two items |
| `⟨0, [none, some 0]⟩` | the witness | metatheory context |
| `Iso` fields `insts_fwd`, `dinv_dmap` | non-isomorphism | the declared isomorphism relation (paper §3, definition 8); metatheory |
| `omega` | the arithmetic contradiction | metatheory decision procedure for linear arithmetic over `Nat` |
| "⟨ARA⟩", "self-loop" | the gloss | interpretation |

**What the system holds.** Two data, one binary form, one instance whose
two arguments happen to be the same index, one demand.

**Phrases to read with care.**

- “Not isomorphic” is relative to the declared maps, which preserve
  instances in both directions and admit inverse maps on the data.
  Replacing that notion requires specifying new preservation conditions;
  no conclusion about an unspecified coarser comparison follows here.
- "Realizes ⟨ARA⟩" is the metatheory's reading of `[0, 0]`.

## Student exercise

Prove in your own words that there is no isomorphism from `BD` to `BL`
either (the direction Genesis does not state). Which field of `Iso`
would you use, and what goes wrong?

## Answer

<details>
<summary>Check the exercise (optional)</summary>

Use `insts_fwd` on the loop's instance `(0, [0, 0])`: it must be carried
to an instance of `BL`, that is to `(0, [0, 1])`, so `dmap 0 = 0` from
the first argument and `dmap 0 = 1` from the second; `0 = 1`,
contradiction. This time the clash is already in `dmap` at one datum,
and the inverse field is not needed. Unit 21 gives a second route that
needs no new case analysis: every `Iso` can be reversed (`isoSymm`), so
`Iso BD BL → False` follows from `BL_not_iso_BD` in one line. Both are
book Lean; the frozen derivation did not need either.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Minimality.lean` lines 44, 55-56, 63, 88-89, 270-280 |
| Axiom report | `artifacts/lean_axioms.txt`: `BD_separable`, `deltaBD_valid`, `BL_not_iso_BD` `[propext, Quot.sound]` |
| Paper | `paper/paper.md` §7.3 table row L: "binary self-loop"; §3 definition 8 (isomorphism) |
| Ledger | `paper/paper_claim_ledger.md`, `CL-3-TIE-CLASSES` (class distinctness: `U0_not_iso_BL`, `U0_not_iso_BD`, `BL_not_iso_BD`) |
| Artifact | `artifacts/challenges.json`, `challenge3.L.mu1.iso_classes`, label `form2+inst2diag`, class size 2 |
| Test | `tests/test_engine.py::test_challenge3_reading_l_classes` (labels include `form2+inst2diag`); `tests/test_iso.py` |
| Check (Python) | `python textbook/checks/u20_loop.py`: all five contexts with both pluggings, three witnesses including Lean's; profiles; cross-witness failures; both loop deltas valid; loop on 0 isomorphic to loop on 1; link not isomorphic to loop; a uniform rule removes separation while retaining the loop |
| Check (book Lean) | `python textbook/checks/u20_lean.py`: eleven book reports plus three Genesis theorems kernel-checked, Lean 4.33.0, including `BD_uniform_collapsed`; `propext, Quot.sound` throughout except the landing equation (`propext`) |
