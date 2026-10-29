# Unit 29. Renaming the data changes nothing a context can see

**Claim.** Consistent reversible renaming preserves collapse when the
renaming also keeps the admitted index range. Candidate pairs must be
renamed with the data. This does not promise unchanged answers for a
fixed list of old index names.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Observational collapse is invariant under a renaming of the
datum indices. For a renaming `σ`, a bijection on `Nat` that keeps the
admitted range in both directions, `collapsed (renameRegime σ.f r) (σ.f d)
(σ.f d') ↔ collapsed r d d'`; so the number of collapsed pairs over any
list of candidate pairs is the same before and after (`collapsedCount_rename`).
The candidate list is mapped with the data in this count comparison.
The bijection hypothesis is doing work: under the constant map the
transport is false (`non_injective_does_not_transport`).

**Status:** derived. **Lean:** `Derivation.DRen` (`lean4/Derivation/CountTransport.lean`
line 50), `mapInst` (79), `mapCtx` (83), `renameRegime` (90),
`plug_mapCtx` (125), `derivable_rename` (137), `wfCtx_rename` (154),
`collapsed_rename` (204-220), `collapsedCount_rename` (239-253),
`cmRegime` (286), `cm_separable` (292), `non_injective_does_not_transport`
(300-305). **Axioms:** `propext, Quot.sound` throughout. **Depends on:**
contexts, plugging and collapse (Unit 08); the witness theorem (Unit 09);
the engine's quotient by isomorphism (Unit 21).

</details>

## First pass

There are three data and one unary form `marked`. Admit exactly
`marked(0)`, with no uniform rule. Data 1 and 2 have the same answers,
so their pair is collapsed.

Swap the names 0 and 1 consistently. The mark moves to 1. The old
pair `(1, 2)` becomes `(0, 2)`, whose two members still agree.
If we instead keep asking about the literal pair `(1, 2)`, one is now
marked and the other is not.

| Compared pair | Result |
|---|---|
| Original record, `(1, 2)` | Collapsed |
| Renamed record, renamed pair `(0, 2)` | Collapsed |
| Renamed record, fixed old pair `(1, 2)` | Separated |

The theorem carries both the record and the question through the
renaming. Its count theorem likewise compares a pair list with its
mapped list.

A renaming must be reversible and keep admitted positions admitted.
Sending two different data to one position is a merge, with no inverse.
A reversible map on all natural numbers can also move an admitted
position out of range; that is outside the theorem's conditions.

## Question

The engine quotients its branch tree by isomorphism, and an isomorphism
renames the data. Does anything a context can see depend on which index a
datum happens to carry? If the count of collapsed pairs changed under a
renaming, the quotient would be unsound. What exactly is transported, by
what action, and is the hypothesis that the renaming is a bijection
really needed?

## What we already possess

- A context is a form with slots, at least one a hole; plugging fills
  every hole with one datum; `derivable` is membership in `insts` or
  coverage by a rule; `collapsed r d d'` says every well-formed context
  agrees on `d` and `d'` (Unit 08).
- `separable_not_collapsed` (Unit 09): a witness context rules out
  collapse.
- The Python `iso.rename(r, pi, phi)` applies a bijection of data and of
  forms, and `canonical` is invariant under it (Unit 21).

## New concept: an action on regimes, and transport along it

To say "renaming changes nothing" one must first say what renaming *does*
to each part of the model. Genesis defines three maps from one function
`f : Nat → Nat`:

- `mapInst f` renames the arguments of an instance;
- `mapCtx f` renames the filled slots of a context and leaves holes as
  holes, because a hole is a position, not a datum;
- `renameRegime f` maps every instance and touches nothing else: `data`
  is a count, `forms` and `rules` are indexed by form, and `reqs` is left
  alone deliberately, because collapse never reads it (`wfCtx` reads
  `forms` and `data`; `derivable` reads `insts` and `rules`).

A *renaming* `DRen n` packages `f` with an inverse `g`, the two
cancellation laws, and the two bounds that keep indices below `n` on
both sides. "Transport" then means: a property holds of the renamed thing
exactly when it holds of the original. Genesis proves it for plugging
(`plug_mapCtx`), for derivability (`derivable_rename`), for
well-formedness (`wfCtx_rename`) and then for collapse
(`collapsed_rename`), each from the one before.

## Plain-language interpretation

Indices are the metatheory's names for data. A context does not read
names; it reads which instances are present. If you rename every datum
consistently, inside the instances and inside the contexts alike, every
question "is this plugging derivable?" gets the same answer as before,
because the renamed instance is present exactly when the original was.
So two data that no context could tell apart still cannot be told apart
after renaming, and two that could still can.

To show collapse in the original regime implies collapse in the renamed
regime, the proof pulls a target context back with `g`. In the other
direction, it maps an original context forward with `f` and uses
injectivity. Both context transports need the stated range conditions.
A map without an inverse can send two different data to one
index, after which "the two data are collapsed" is true for a trivial
reason, while the original pair is separable. The module exhibits exactly
that failure.

## Pseudocode

```
# Gloss
rename(r):   same data count, same forms, same rules, same demands;
             every instance (form, args) becomes (form, f(args))
mapCtx(c):   same form; each filled slot x becomes f(x); holes stay holes

plug_mapCtx:      plug(mapCtx(c), f(d)) = mapInst(f, plug(c, d))
derivable_rename: derivable(rename(r), mapInst(f, i)) <-> derivable(r, i)   [f injective]
wfCtx_rename:     wfCtx(rename(r), mapCtx(c)) <-> wfCtx(r, c)               [bounds both ways]

from original collapse to renamed collapse: take a context c' of rename(r);
   it is mapCtx(c) for c = mapCtx(g, c'); c is well formed in r; apply collapse
   to c; carry the answer across the two transports above.
from renamed collapse to original collapse: map an original context through f;
   apply the renamed collapse and transport the answers back using injectivity.
count: map the candidate list through f; each entry's answer is unchanged;
   so the count is unchanged.
```

## Python

`iso.rename` is the implementation's action; `collapsed_pairs` is the
decision procedure Lean's `collapsedCount_rename` leaves to the caller.

```python
from itertools import permutations
from derivation.iso import rename
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, replay
from derivation.observe import collapsed_pairs, separable

cm = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitForm(1), AdmitInst(0, (0,))])
print(separable(cm, 0, 1), collapsed_pairs(cm), separable(cm, 0, 0))

reg = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitDatum("c"), AdmitDatum("d"),
              AdmitForm(1), AdmitInst(0, (2,)), AdmitInst(0, (3,))])
print(collapsed_pairs(reg), collapsed_pairs(rename(reg, (3, 2, 1, 0), (0,))))
print(all(len(collapsed_pairs(rename(reg, pi, (0,)))) == 2
          for pi in permutations(range(4))))
```

Output:

```text
True () False
((0, 1), (2, 3)) ((0, 1), (2, 3))
True
```

## Line-by-line Python explanation

`cm` is `cmRegime`: two data, one unary form, datum 0 marked.
`separable(cm, 0, 1)` is `True` and `collapsed_pairs(cm)` is empty: the
one-hole context says yes on 0 and no on 1. `separable(cm, 0, 0)` is
`False`: a datum has one profile, so it is never separable from itself.
That is the Python face of the countermodel: send both data to index 0
and the renamed "pair" is `(0, 0)`, collapsed for no reason that concerns
the original.

`reg` is the regression regime of the test suite (Unit 31 returns to it):
four data, one unary form, marks on data 2 and 3. Its collapsed pairs are
`(0, 1)` and `(2, 3)`. `rename(reg, (3, 2, 1, 0), (0,))` reverses the data
(the second tuple is the identity on the one form); the collapsed pairs
are again `(0, 1)` and `(2, 3)`, now with the marked pair first. The pairs
were carried through the permutation and renormalized to `i < j`.

The last line runs all 24 permutations: the count is 2 every time. The
check script also verifies, for each permutation, that the renamed
collapsed pairs are exactly the images of the originals.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/CountTransport.lean lines 50-57, 79-91
structure DRen (n : Nat) where
  f : Nat → Nat
  g : Nat → Nat
  fg : ∀ x, g (f x) = x
  gf : ∀ x, f (g x) = x
  fbound : ∀ x, x < n → f x < n
  gbound : ∀ x, x < n → g x < n

def mapInst (f : Nat → Nat) (i : Inst) : Inst := (i.1, i.2.map f)

def mapCtx (f : Nat → Nat) (c : Ctx) : Ctx :=
  ⟨c.form, c.slots.map (Option.map f)⟩

def renameRegime (f : Nat → Nat) (r : Regime) : Regime :=
  { r with insts := r.insts.map (mapInst f) }
```

```lean
-- Lean (Genesis), lean4/Derivation/CountTransport.lean lines 204-220
theorem collapsed_rename {n : Nat} (σ : DRen n) (r : Regime) (hn : r.data = n)
    (d d' : Nat) :
    collapsed (renameRegime σ.f r) (σ.f d) (σ.f d') ↔ collapsed r d d' := by
  constructor
  · intro h c hc
    have hwf := (wfCtx_rename σ r hn c).mpr hc
    have hh := h (mapCtx σ.f c) hwf
    rw [plug_mapCtx, plug_mapCtx] at hh
    rwa [derivable_rename σ.f_inj, derivable_rename σ.f_inj] at hh
  · intro h c' hc'
    have hc : mapCtx σ.f (mapCtx σ.g c') = c' := mapCtx_f_g σ c'
    have hwf : wfCtx r (mapCtx σ.g c') := by
      rw [← wfCtx_rename σ r hn (mapCtx σ.g c'), hc]; exact hc'
    have hh := h (mapCtx σ.g c') hwf
    have e1 : plug c' (σ.f d) = mapInst σ.f (plug (mapCtx σ.g c') d) := by
      rw [← plug_mapCtx, hc]
    have e2 : plug c' (σ.f d') = mapInst σ.f (plug (mapCtx σ.g c') d') := by
      rw [← plug_mapCtx, hc]
    rw [e1, e2, derivable_rename σ.f_inj, derivable_rename σ.f_inj]
    exact hh
```

```lean
-- Lean (Genesis), lean4/Derivation/CountTransport.lean lines 286-305
def cmRegime : Regime := ⟨2, [1], [(0, [0])], [], []⟩

theorem cm_separable : separable cmRegime 0 1 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩

theorem non_injective_does_not_transport :
    collapsed (renameRegime (fun _ => 0) cmRegime)
        ((fun _ => 0) 0) ((fun _ => 0) 1)
      ∧ ¬ collapsed cmRegime 0 1 :=
  ⟨fun _ _ => Iff.rfl, separable_not_collapsed cm_separable⟩
```

The book's Lean builds the swap of two data as a `DRen 2`, applies the
transport to the countermodel, records which fields the action leaves
alone, and shows why the constant map is not a renaming.

```lean
-- Lean (book), textbook/checks/u29_lean.py
def swapFun : Nat → Nat
  | 0 => 1
  | 1 => 0
  | n + 2 => n + 2

def swap2 : DRen 2 :=
  ⟨swapFun, swapFun, swapFun_invol, swapFun_invol, swapFun_bound, swapFun_bound⟩

theorem renamed_cm : renameRegime swap2.f cmRegime = ⟨2, [1], [(0, [1])], [], []⟩ := by
  decide

theorem cm_transport :
    collapsed (renameRegime swap2.f cmRegime) 1 0 ↔ collapsed cmRegime 0 1 :=
  collapsed_rename swap2 cmRegime rfl 0 1

theorem renamed_not_collapsed : ¬ collapsed (renameRegime swap2.f cmRegime) 1 0 :=
  fun h => separable_not_collapsed cm_separable (cm_transport.mp h)

theorem rename_reqs (f : Nat → Nat) (r : Regime) : (renameRegime f r).reqs = r.reqs := rfl

theorem const_has_no_inverse : ¬ ∃ g : Nat → Nat, ∀ x, g ((fun _ : Nat => 0) x) = x := by
  rintro ⟨g, hg⟩
  have h0 : g 0 = 0 := hg 0
  have h1 : g 0 = 1 := hg 1
  omega
```

## Line-by-line Lean explanation

**`DRen n`.** A structure with six fields: the map `f`, its inverse `g`,
the two cancellation laws `fg` and `gf`, and the two bounds. The bounds
are what make `wfCtx` transport: a slot below `n` must stay below `n`.
The cancellation laws are what make the inverse direction of
`collapsed_rename` possible.

**`mapInst`, `mapCtx`, `renameRegime`.** `i.2.map f` renames every
argument. `c.slots.map (Option.map f)` renames `some x` to `some (f x)`
and sends `none` to `none`. `{ r with insts := ... }` copies `r` and
replaces one field; `data`, `forms`, `rules`, `reqs` are unchanged, which
the book's `rename_reqs` and its three siblings record as `rfl`.

**`collapsed_rename`, forward direction.** `intro h c hc`: assume collapse
in the renamed regime, take a context `c` well formed in `r`. `hwf`: by
`wfCtx_rename` (right to left), `mapCtx σ.f c` is well formed in the
renamed regime. `hh`: apply the assumed collapse to it; the statement is
about plugging `σ.f d` and `σ.f d'` into `mapCtx σ.f c`. `rw [plug_mapCtx,
plug_mapCtx] at hh` rewrites both pluggings as renamed instances of the
original pluggings. `rwa [derivable_rename ...]` rewrites both
derivabilities back to the original regime (needing only injectivity,
`σ.f_inj`) and closes the goal with the result.

**Backward direction.** `intro h c' hc'`: assume collapse in `r`, take a
context `c'` well formed in the renamed regime. `hc`: pulling `c'` back
through `g` and pushing through `f` returns `c'` (`mapCtx_f_g`). `hwf`:
the pulled-back context is well formed in `r`, by `wfCtx_rename` read
through `hc`. `hh`: apply collapse to it. `e1`, `e2`: the pluggings of
`σ.f d` and `σ.f d'` into `c'` are the renamed pluggings into the
pulled-back context, again by `plug_mapCtx` and `hc`. Rewrite with `e1`,
`e2` and `derivable_rename`, and `hh` is the goal.

**`non_injective_does_not_transport`.** The map `fun _ => 0` sends both
data to index 0. The renamed regime's "pair" is `(0, 0)`, and
`collapsed _ 0 0` holds by `Iff.rfl` for every context: the two pluggings
are the same instance. Meanwhile `cm_separable` gives a witness (the
one-hole context, decided) that `0` and `1` are separable in `cmRegime`,
so by Unit 09 they are not collapsed. The conjunction records that the
left side of the transport can hold while the right fails.

**The book's `swap2`.** `swapFun` exchanges 0 and 1 and fixes everything
else; it is its own inverse, and it preserves `< 2`. `renamed_cm`,
decided, shows the action moves the mark to datum 1. `cm_transport` is
Genesis's theorem at this renaming: `σ.f 0 = 1` and `σ.f 1 = 0` reduce by
computation, so Lean accepts the statement with `1 0` written out.
`renamed_not_collapsed` carries the countermodel's separability across.

**`const_has_no_inverse`.** Suppose `g` undid the constant map. Then `g 0
= 0` (from `x = 0`) and `g 0 = 1` (from `x = 1`), and `omega` sees the
contradiction. So no `DRen` can be built from the constant map, and the
countermodel lies outside the theorem's hypothesis, as it must.

**Axioms.** Everything here reports `propext, Quot.sound`, through
`simp`, `decide` on structures and the `List` lemmas. `rename_reqs` and
its siblings report no axiom: they are `rfl`.

The added `jump_invol` and `requirement_guard_unchanged` likewise use no
axioms. The failed-range context example uses `propext, Quot.sound`.

## What has been proved

- Plugging, derivability and well-formedness each transport along a
  renaming (Genesis, derived; the first needs no hypothesis, the second
  injectivity, the third the bounds).
- Collapse transports as an `iff` under the full `DRen` conditions:
  bijectivity on `Nat` and preservation of the admitted range in both
  directions (Genesis, derived).
- The collapsed-pair count over any candidate list, with any decision
  procedure that tracks `collapsed`, is preserved (Genesis, derived).
- That count compares the list with its mapped list and counts list
  entries, including repetitions if supplied. The separate Python
  three-datum example shows that leaving a literal pair list fixed can
  change its answer.
- The bijection hypothesis cannot be dropped (Genesis, countermodel).
- At the swap of two data, the countermodel's separability is carried to
  the renamed regime (book Lean).

## What has not been proved

- That `collapsed` is decidable, or any enumeration of well-formed
  contexts. `collapsedCount_rename` takes the decision procedure as a
  parameter with a proof that it agrees with `collapsed`; Python supplies
  it (`collapsed_pairs`). This is the division of labour the module
  header states.
- Transport under a renaming of *forms*, or under presentation tokens.
  `renameRegime` acts on datum indices only. The full two-bijection case
  is `IsoCollapse.collapsed_transport` and `FormTransport.lean` (parked
  modules, taught later); tokens do not exist in the Lean model at all.
- Renaming of the demand endpoints in this action. It leaves `reqs` and
  `data` unchanged, so the requirement conjunct of `Regime.wf` is
  definitionally unchanged (`requirement_guard_unchanged`, book). That
  is different from carrying the named demands to corresponding renamed
  endpoints. Unit 31 extends the action to requirements for that purpose.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `structure DRen` | packaging a bijection with bounds | metatheory |
| `List.map`, `Option.map`, `List.mem_map` | the three actions | metatheory |
| `rw`, `rwa`, `simp only`, `funext` | the transports | metatheory tactics |
| `decide` on `Regime` equality and on `wfCtx` | the concrete instances | metatheory; derived `DecidableEq` |
| `omega` | the no-inverse witness | metatheory |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The regime's instances with their argument
indices. Renaming is the metatheory relabelling those indices; the
regime has no view of its own indices and no context that reads them.

**Phrases to read with care.**

- "Isomorphic regimes are the same regime" is the engine's convention,
  justified by this theorem for collapse and by Unit 31 for transitions.
  It is a quotient the metatheory chose; nothing in the regime asks for
  it.
- "The count is a Lean theorem" is true with the parameters stated: over a
  caller's list, with a caller's decider that provably tracks `collapsed`.
  The enumeration itself is Python.

## Student exercise

Why does `DRen` require both reversibility and range bounds? Which proof
uses the bounds? Give a reversible map on all natural indices that sends
an admitted filled slot outside the admitted range.

## Answer

<details>
<summary>Worked answer</summary>

`wfCtx_rename` uses them. Well-formedness requires every filled slot to
name a datum below `r.data`. After renaming, a slot `some x` with `x <
r.data` becomes `some (σ.f x)`, and `fbound` is what keeps it below
`r.data`; in the other direction `gbound` does the same for the pulled-back
context. Swap 1 with 2 and fix all other natural numbers. This map is its
own inverse. With two data and a binary form, `[hole, 1]` is well formed
but its image `[hole, 2]` is not. The book checks this particular failure
of context transport. The collapse statement remains expressible; this
proof cannot apply its context-transport lemma without the bounds.
`derivable_rename` and `plug_mapCtx`, by contrast, never look at the
bounds, which is why the module says the transport is "unconditional in
the renaming's bounds" apart from well-formedness.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/CountTransport.lean` lines 50-57, 79-91, 125, 137, 154, 204-220, 239-253, 286-305 |
| Axiom report | `artifacts/lean_axioms.txt`: `plug_mapCtx`, `derivable_rename`, `wfCtx_rename`, `collapsed_rename`, `collapsedCount_rename`, `cm_separable`, `non_injective_does_not_transport` all `[propext, Quot.sound]` |
| Paper | `paper/paper.md` §10 question 7 and §12 residual R6 (discharged 2026-08-17; scope stated 2026-09-08); ledger `CL-COUNT-INVARIANCE` |
| Check (Python) | `python textbook/checks/u29_rename_count.py`: the original 24 and 6 permutations preserve transported pairs and counts; a separate three-datum unary example distinguishes a fixed pair list from its mapped list |
| Check (book Lean) | `python textbook/checks/u29_lean.py`: nine book reports plus four native results kernel-checked, Lean 4.33.0; `jump_invol` and `requirement_guard_unchanged` use no axioms, `bounded_context_needed` uses `propext, Quot.sound`; original reports are unchanged |
