# Unit 21. The cheapest answer is not unique

**Claim.** Under the item-count measure `mu1`, the minimum corrective
augmentation at Challenge 3 is not unique: the unary mark `deltaU0` and
the binary link `deltaBL` are both valid two-item responses, nothing
cheaper is valid, and their results `U0` and `BL` are not isomorphic,
because an isomorphism preserves arities and the two regimes' only forms
have arities 1 and 2. **Status:** derived (reading L; reading F's count is
a bounded computation). **Lean:** `Derivation.mu1_minimum_not_unique`
(`lean4/Derivation/Minimality.lean` lines 281-294), with `Iso`
(176-197), `isoRefl` (199-221), `isoU1U0` (227-248), `U0_not_iso_BL`
(250-258). **Axioms:** `propext, Quot.sound`. **Depends on:** Units 18
(cost floor), 19 and 20 (the two-item answers), `U0`/`U1`/`deltaU0`
(Minimality lines 38-61, introduced here).

## Question

Units 19 and 20 gave two-item answers to the demand. Is the cheapest
answer *the* answer? If two answers tie on cost, are they secretly the
same structure under renaming, or genuinely different ways the system
could grow?

## What we already possess

- No delta of length at most one is valid (Unit 18).
- `deltaBL` and `deltaBD` are valid two-item responses (Units 19, 20).
- The unary regimes `U0 = ⟨2, [1], [(0, [0])], [], [(0, 1)]⟩` and
  `U1 = ⟨2, [1], [(0, [1])], [], [(0, 1)]⟩`: one unary form and one
  instance marking datum 0, or datum 1. `deltaU0 = [.newForm 1,
  .newInst 0 [0]]` is valid (Minimality lines 79-80, the same pattern as
  Unit 19).
- `BL_not_iso_BD` (Unit 20) used two fields of a structure not yet
  explained: `insts_fwd` and `dinv_dmap`.

## New concept: isomorphism of regimes

Two regimes are **isomorphic** when there is a relabelling of data and a
relabelling of forms under which they agree. Genesis makes this a
structure, `Iso r s`, with four functions and fourteen conditions
(Minimality lines 176-197):

| Fields | Say |
|---|---|
| `dmap`, `dinv` | a bijection of the data indices, as a map and its inverse, each landing in range |
| `fmap`, `finv` | the same for form indices |
| `arity` | the form `fmap f` of `s` has the arity of the form `f` of `r` |
| `insts_fwd`, `insts_bwd` | instances are carried to instances, both ways |
| `rules_fwd`, `rules_bwd` | rules likewise |
| `reqs_fwd`, `reqs_bwd` | demands likewise, re-sorted after mapping (`sortPair`) |

Presentation tokens are not in the Lean model at all, so an isomorphism
never sees them; the Python side forgets them explicitly
(`test_tokens_are_forgotten`). This is the paper's definition 8, and it is
*declared*: it is what Genesis means by "the same up to renaming".

Two consequences used here. **Reflexivity:** every regime whose demands
are written small-first is isomorphic to itself by the identity
(`isoRefl`, which is why Unit 17's invariant matters). **Arity is an
invariant:** `U0_not_iso_BL` reads the `arity` field at form 0 and finds
`2 = 1`.

## Plain-language interpretation

Imagine two notebooks answering the same demand. One has a one-place
stamp ("marked") pressed on ⟨A⟩. The other has a two-place stamp
("links") pressed on the pair. Rename the pages however you like; a
one-place stamp does not become a two-place stamp. So the two notebooks
are different answers, and both are as short as an answer can be.

That is the paper's result: *under `mu1`, minimality does not pick out a
unique structure*. The system's growth is underdetermined by the demand
plus the cost. What chooses between the mark and the link is not inside
the system, and not inside the cost either. Unit 22 shows that a finer,
declared measure does choose.

Two further facts sharpen it. The tie is not two-way but three-way
within the enumerated bounds (mark, link, loop), and, grammar-wide, it is
infinite: a `k`-ary mark is a valid two-item answer for every `k ≥ 1`,
and marks of different arity are pairwise non-isomorphic
(`markK_pairwise_noniso`). Any finite table of tied minima is complete
only relative to an arity bound.

## Pseudocode

```
# Gloss
deltaU0 = [form of arity 1, instance (form 0, [0])]  -> U0, valid, length 2
deltaBL = [form of arity 2, instance (form 0, [0,1])] -> BL, valid, length 2
no delta of length <= 1 is valid                      -- Unit 18
suppose iso : Iso U0 BL
  iso.fmap 0 < length BL.forms = 1,  so iso.fmap 0 = 0
  iso.arity 0 : BL.forms[fmap 0] = U0.forms[0],  i.e. 2 = 1.  ✗
so the two minima are not isomorphic: the minimum is not unique.
```

## Python

```python
from derivation.candidates import Bounds, NewForm, NewInst, apply_delta, min_responses
from derivation.engine import GENESIS_L, delta_label
from derivation.iso import group_by_canonical, isomorphic
from derivation.model import Impose, replay, step

base = replay(GENESIS_L)
mr = min_responses(base, (0, 1), "mu1", Bounds(2, 2))
results = [step(apply_delta(base, d), Impose(0, 1)) for d in mr.deltas]
groups = group_by_canonical(zip(results, mr.deltas))
print(mr.cost, len(mr.deltas), len(groups))
print(sorted(delta_label(base, g[0]) for g in groups.values()))
u0 = apply_delta(base, (NewForm(1), NewInst(0, (0,))))
bl = apply_delta(base, (NewForm(2), NewInst(0, (0, 1))))
print(isomorphic(u0, bl))
```

Output:

```text
(2, -1) 6 3
['form1+inst1', 'form2+inst2', 'form2+inst2diag']
False
```

## Line-by-line Python explanation

`min_responses(..., "mu1", Bounds(2, 2))` (Unit 18) returns the six
valid deltas at the minimum cost 2: two unary marks (datum 0 or 1) and
four binary instances (`[0,1]`, `[1,0]`, `[0,0]`, `[1,1]`).

`step(apply_delta(base, d), Impose(0, 1))` builds each result *with the
demand recorded*. The Lean regimes carry the demand in `reqs`; the
Python base does not (Unit 16), and the implemented isomorphism must
carry demands to demands (`reqs_fwd`), so the demand has to be present
for the classes to match the engine's. In reading L it makes no
difference to the count; in reading F it does, which is why the paper's
table has five classes there and not three
(`test_direction_relative_to_requirement_matters`).

`group_by_canonical` (`iso.py` line 238) buckets regimes by their
canonical form, the implemented quotient. Three buckets: mark, link,
loop. `delta_label` (`engine.py` line 111) gives the artifact's neutral
names.

`isomorphic(u0, bl)` (`iso.py` line 215) compares canonical forms:
`False`. The check script also confirms `U0 ~ U1`, `BL ~ BL(1,0)`, the
non-isomorphism of all three class representatives pairwise, and the
`k`-ary marks for `k = 1 … 5` valid and pairwise non-isomorphic.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Minimality.lean lines 250-258, 281-294
/-- Arity is an isomorphism invariant, so the unary mark and the binary
link are non-isomorphic tied minima. -/
theorem U0_not_iso_BL (iso : Iso U0 BL) : False := by
  have hlt := iso.fmap_lt 0 (by decide)
  have ha := iso.arity 0 (by decide)
  have h0 : iso.fmap 0 = 0 := by
    have h1 : iso.fmap 0 < 1 := by simpa [BL] using hlt
    omega
  rw [h0] at ha
  simp [U0, BL] at ha

theorem mu1_minimum_not_unique :
    validResponse R2L 0 1 deltaU0 ∧ validResponse R2L 0 1 deltaBL ∧
    deltaU0.length = 2 ∧ deltaBL.length = 2 ∧
    (∀ δ, δ.length ≤ 1 → ¬ validResponse R2L 0 1 δ) ∧
    applyDelta R2L deltaU0 = some U0 ∧
    applyDelta R2L deltaBL = some BL ∧
    (Iso U0 BL → False) :=
  ⟨deltaU0_valid, deltaBL_valid, rfl, rfl, cost1_insufficient,
   by decide, by decide, U0_not_iso_BL⟩
```

```lean
-- Lean (book), textbook/checks/u21_lean.py
/-- An isomorphism runs backwards. -/
def isoSymm {r s : Regime} (iso : Iso r s) : Iso s r where
  dmap := iso.dinv
  dinv := iso.dmap
  fmap := iso.finv
  finv := iso.fmap
  dmap_lt := iso.dinv_lt
  dinv_lt := iso.dmap_lt
  dinv_dmap := iso.dmap_dinv
  dmap_dinv := iso.dinv_dmap
  fmap_lt := iso.finv_lt
  finv_lt := iso.fmap_lt
  finv_fmap := iso.fmap_finv
  fmap_finv := iso.finv_fmap
  arity := fun f hf => by
    have h := iso.arity (iso.finv f) (List.mem_range.mpr (iso.finv_lt f hf))
    rw [iso.fmap_finv f hf] at h
    exact h.symm
  insts_fwd := iso.insts_bwd
  insts_bwd := iso.insts_fwd
  rules_fwd := iso.rules_bwd
  rules_bwd := iso.rules_fwd
  reqs_fwd := iso.reqs_bwd
  reqs_bwd := iso.reqs_fwd

theorem BL_not_iso_U0 (iso : Iso BL U0) : False := U0_not_iso_BL (isoSymm iso)
theorem BD_not_iso_BL (iso : Iso BD BL) : False := BL_not_iso_BD (isoSymm iso)
```

## Line-by-line Lean explanation

**`U0_not_iso_BL`.** Suppose `iso : Iso U0 BL`.

- `iso.fmap_lt 0 (by decide)`: form 0 of `U0` exists (`0 ∈ List.range 1`,
  decided), so its image is below `BL.forms.length`.
- `iso.arity 0 (by decide)`: the image form has the arity of form 0.
- `h0`: `BL.forms.length` is `1`, so `fmap 0 < 1`, so `fmap 0 = 0`
  (`omega` on the inequality).
- `rw [h0] at ha` turns `ha` into `BL.forms.getD 0 0 = U0.forms.getD 0 0`;
  `simp [U0, BL]` evaluates both sides, `2 = 1`, and closes the goal from
  the contradiction.

`getD l i 0` reads position `i` of a list with default `0` when the index
is out of range. The default never triggers here; `fmap_lt` keeps the
index in range.

**`mu1_minimum_not_unique`** is a conjunction of eight facts, each
already proved: the two validity theorems (Units 19 and this unit's
`deltaU0_valid`), two lengths by `rfl`, the cost floor (Unit 18), two
landing equations by `decide`, and the non-isomorphism. The theorem is a
summary; its content is in its parts.

**`isoSymm` (book).** Every field of the reverse isomorphism is a field
of the original with "forward" and "backward" exchanged. The one field
needing a proof is `arity`: the original says
`s.forms[fmap f] = r.forms[f]` for `f` a form of `r`; applied to
`finv f` and rewritten with `fmap (finv f) = f`, it says
`s.forms[f] = r.forms[finv f]`, whose symmetric form is what the reverse
needs. With `isoSymm`, the two directions Genesis does not state follow
in one line each, including Unit 20's missing `Iso BD BL → False`.

**`isoU1U0`** (Genesis, lines 227-248) maps the mark on 1 to the mark on
0 by `swap01`, with every field decided. So the two unary marks are one
class, and the tie between `U0` and `BL` is a tie between classes, not a
bookkeeping artefact of which datum got marked.

**Axioms.** `propext, Quot.sound` throughout: the `decide` calls on
concrete lists. `isoSymm` reports both because it rewrites with list
lemmas; `markK_pairwise_noniso` reports `propext` only.

## What has been proved

- The eight conjuncts above (Genesis, derived, reading L).
- `U0 ≇ BL`, `U0 ≇ BD`, `BL ≇ BD` (Genesis, derived); their converses
  (book, by `isoSymm`).
- `U0 ≅ U1` (Genesis, by `isoU1U0`); `U0 ≅ U0` (book, by `isoRefl`).
- For every `k ≥ 1` the `k`-ary mark is a valid two-item response, and
  distinct arities are non-isomorphic: infinitely many tied minimum
  classes (Genesis, derived, reading L; `CL-3-INFINITE-TIES`).
- Within bounds 2 items and arity 2: exactly 3 classes in reading L and
  5 in reading F (Genesis, verified finite; `CL-3-TIE-CLASSES`).

## What has not been proved

- Reading F non-uniqueness as a Lean theorem. The Lean is stated over
  `R2L`; the `{F: 5}` count is the bounded enumeration, and the ledger
  says so (`CL-3-NONUNIQUE-MU1`, scope made explicit 2026-08-18).
- That the implemented isomorphism is the right notion of sameness. It
  is declared (paper §3, definition 8). A coarser notion would merge more
  classes; a finer one, fewer. The non-uniqueness result is relative to
  it.
- That `mu1` is the right cost. Unit 22 changes the measure and the
  answer changes.
- That anything inside the system chooses between the mark and the link.
  Nothing does. The demand is met by either, and the system has no
  preference.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `structure Iso` | sameness up to renaming | declared metatheory (definition 8) |
| `arity`, `getD`, `omega` | the invariant | metatheory arithmetic on list positions |
| `mu1` = list length | the cost | declared measure |
| `swap01`, `isoRefl` | explicit isomorphisms | metatheory functions on indices |

**What the system holds.** After either response: two data, one form,
one instance, one demand. The system does not hold both responses, does
not compare them, and has no notion of "class". The tie is visible only
from outside, to a metatheory that can enumerate responses and quotient
them.

**Phrases to read with care.**

- "Not unique" means: not unique up to the implemented isomorphism, under
  `mu1`. Both qualifiers are load-bearing.
- "The system could grow either way" is the metatheory's description of
  two admissible responder choices; the system grows the way the
  responder admits, and knows nothing of the other way.

## Student exercise

Is `Iso U0 BD → False` provable by the arity argument, the instance
argument, or both? Write the three-line proof sketch for whichever
applies, and say which field of `Iso` is read first.

## Answer

The arity argument applies: `U0` has a unary form, `BD` a binary one, and
`U0_not_iso_BD` (Minimality lines 259-267) is word for word
`U0_not_iso_BL` with `BD` for `BL`. The first field read is `fmap_lt`, to
pin `fmap 0 = 0`; then `arity` gives `2 = 1`. The instance argument would
also work (`U0`'s instance `(0, [0])` has one argument, `BD`'s has two,
and `insts_fwd` maps a one-element list to a one-element list), but it is
longer, and Genesis uses the arity invariant for both unary-versus-binary
cases and the instance invariant only for link-versus-loop, where the
arities agree.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Minimality.lean` lines 38-61 (`U0`, `U1`, `deltaU0`), 79-80 (`deltaU0_valid`), 176-197 (`Iso`), 199-221 (`isoRefl`), 223-248 (`swap01`, `isoU1U0`), 250-267 (`U0_not_iso_BL`, `U0_not_iso_BD`), 281-294 (`mu1_minimum_not_unique`), 297-370 (the `k`-ary family) |
| Axiom report | `artifacts/lean_axioms.txt`: `mu1_minimum_not_unique`, `U0_not_iso_BL`, `isoU1U0` `[propext, Quot.sound]`; `markK_pairwise_noniso` `[propext]` |
| Paper | `paper/paper.md` §7.3 (**[theorem]**, **[bounded theorem]** table, infinite family), §3 definition 8 |
| Ledger | `paper/paper_claim_ledger.md`, `CL-3-NONUNIQUE-MU1`, `CL-3-TIE-CLASSES`, `CL-3-INFINITE-TIES` |
| Artifact | `artifacts/claims.json`, `CL-3-NONUNIQUE-MU1 = {L: 3, F: 5}`; `artifacts/challenges.json`, `challenge3.{L,F}.mu1.iso_classes` |
| Test | `tests/test_iso.py::test_arity_distinguishes_classes`, `::test_mark_variants_are_isomorphic`, `::test_link_variants_are_isomorphic`, `::test_diag_is_not_link`, `::test_direction_relative_to_requirement_matters`, `::test_tokens_are_forgotten`; `tests/test_engine.py::test_challenge3_reading_l_classes` |
| Check (Python) | `python textbook/checks/u21_mu1_not_unique.py`: 6 deltas, 3 classes (L); 10 deltas, 5 classes (F), labels equal to the artifact's; the five pairwise (non-)isomorphisms; `k`-ary marks `k = 1 … 5` valid and pairwise non-isomorphic |
| Check (book Lean) | `python textbook/checks/u21_lean.py`: fourteen book declarations plus four Genesis theorems kernel-checked, Lean 4.33.0; `isoSymm` and the three reversed non-isomorphisms; `propext, Quot.sound` where lists are decided, `propext` for `aritySum` by `rfl`, none for the length equations |
