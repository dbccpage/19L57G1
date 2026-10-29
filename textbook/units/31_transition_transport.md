# Unit 31. Renaming carries transitions; choosing by index can change the outcome

**Claim.** A reversible renaming carries each allowed transition to a matching
transition when instances and demands satisfy the stated bounds. Choosing
the pair with the smallest indices can still select a different kind of
challenge after renaming.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Suppose every instance argument is admitted and
every stored demand is an ordered pair of admitted data. One round,
"impose the challenged pair, then apply the response", is carried by
every bounded datum renaming: a step of `r` becomes a
step of the renamed regime with the renamed pair, the renamed response
and the renamed child (`transStep_rename_fwd`), and every step of the
renamed regime arises that way (`transStep_image_total`). The relation is
congruent. A *selection* from it need not be: on the regression regime
the index-least collapsed pair is `(0, 1)` before and after the
renaming, yet the renaming carries `(0, 1)` to `(2, 3)`
(`least_pair_selection_not_congruent`).

**Status:** derived (R7,
discharged 2026-08-18 at the relation level; the class-set form stays
computational). **Lean:** `Derivation.padF`
(`lean4/Derivation/TransitionTransport.lean` line 53), `DRen.pad` (97),
`mapReq` (109), `renameRegimeR` (117), `mapReq_cases` (121),
`collapsed_renameR` (214), `respond` (677), `validResponse_rename` (751),
`TransStep` (820), `transStep_rename_fwd` (828), `transStep_image_total`
(866), `validCount_rename` (937), `regRegime` (972), `regSwap` (1000),
`one_unary_form_ctx_char` (1010), `reg_collapsed_01` (1045),
`reg_renamed_collapsed_01` (1051), `least_pair_selection_not_congruent`
(1064-1068). **Axioms:** `propext, Quot.sound`. **Depends on:** demands
and the impose guard (Unit 17); valid responses and `respond` (Units 18,
19); the quotient by isomorphism and challenge orbits (Unit 21); collapse
transport under renaming (Unit 29).

</details>

## First pass

Put four cards on a table, numbered 0, 1, 2, and 3. One unary form,
`marked`, applies to cards 2 and 3 only. With that sole test, cards 0 and
1 agree, and cards 2 and 3 agree. These are two collapsed pairs.

Now exchange the names 0 with 2 and 1 with 3 throughout the record. The
old unmarked pair `(0,1)` becomes the unmarked pair `(2,3)`. A response to
the old challenge can be renamed into a response to this matching pair.

But “choose the smallest numbered collapsed pair” chooses the literal
pair `(0,1)` in both records. Before renaming, it chooses the unmarked
pair; afterward, it chooses the marked pair. The questions no longer
correspond.

**Predict:** does carrying every allowed move through a renaming also
prove that every procedure for choosing a move respects that renaming?

<details>
<summary>Check your prediction</summary>

No. The available transitions and a procedure selecting among them are
different objects. The Python example below checks that this index-based
selection even produces different child classes.

</details>

The [Search lab](../search_lab/README.md) follows candidate choices and
their result classes before returning to this distinction.

## Question

Unit 29 showed that renaming the data leaves collapse alone. The engine
does more than observe collapse: it picks a collapsed pair, imposes it as
a demand, enumerates the cheapest valid responses, and builds children.
If two regimes are the same up to renaming, do they have the same
children up to renaming? And is "pick the least collapsed pair"
compatible with that? Genesis found, by a test, that it was not. This
unit proves transport of the full transition relation and gives a concrete witness of what
is not.

## What we already possess

- `renameRegime f` acts on instances only (Unit 29). It leaves `reqs`
  alone, and `collapsed` never reads `reqs`.
- `validResponse r i j δ`: some `s` with `applyDelta r δ = some s`, `i`
  and `j` separable in `s`, and every demand of `r` still separable in `s`
  (Unit 18). The impose step inserts the ordered pair `(i, j)` into `reqs`
  (Unit 17).
- The engine's closure policy challenges one representative per
  automorphism orbit of collapsed pairs, and `tests/test_equivariance.py`
  records the regression it fixed (Unit 21).
- The regression regime `regRegime`: four data, one unary form, marks on
  data 2 and 3; collapsed pairs `(0, 1)` and `(2, 3)`.

## New concept: an action that must be extended, and padding

Collapse transport could ignore `reqs`. A transition cannot: validity
quantifies over `r.reqs`, and imposing writes to it. So the module
extends the action. `mapReq f (i, j) = (min (f i) (f j), max (f i) (f j))`
renames a demand and puts it back in ordered form, because a bijection
need not keep `i < j`. `renameRegimeR f r` is `renameRegime f r` with its
demands mapped. The extension is forced by what the transition reads, and
nothing is redefined: the instance action is reused.

A second care: a response may admit a fresh datum, index `r.data`, above
the renaming's range. `padF n f` acts as `f` below `n` and as the identity
from `n` on. `σ.pad m hm` is a `DRen m` for any `m ≥ n`, not just
`n + 1`. A response may admit several fresh data; all their new indices
stay fixed. The child is renamed by this padded map.

The transition object is `TransStep r i j δ s`: `i < j < r.data`, `(i, j)`
collapsed in `r`, `δ` a valid response, and `respond r i j δ = some s`,
where `respond` is impose then apply. Genesis names this composite here
for the first time; `stepE` and `applyDelta` were its parts.

## Plain-language interpretation

Under the theorem's bounds, two regimes that differ only by the names of
their data have corresponding transitions. Every collapsed-pair challenge
with every valid response can be carried to the renamed regime,
with the names swapped throughout: the pair it challenges, the response
it applies, the child it reaches. That is the relation being congruent.

But "the same situation" says nothing about which pair a *procedure*
picks when it is told to pick one. Index 0 in one labelling is the
unmarked datum; index 0 in the other labelling is a marked datum. A rule
that says "challenge the pair with the smallest indices" challenges a
different pair in the two labellings, and gets different children. The
relation knows nothing of this because the relation does not pick; it
holds every step at once. The engine's repair was to pick by orbit, a
notion that renaming respects, and to keep every orbit.

## Pseudocode

```
# Gloss
mapReq(f, (i, j)) = ordered pair of (f i, f j)
renameR(f, r)     = rename instances by f; map every demand by mapReq f
pad(n, f)(x)      = f x if x < n else x

TransStep(r, i, j, delta, s):
    i < j < data(r), (i, j) collapsed in r, delta valid for (i, j) in r,
    impose (i, j) then apply delta reaches s

forward:  TransStep(r, i, j, delta, s)
          -> TransStep(renameR(f, r), mapReq f (i, j), rename delta by pad, renameR(pad f, s))
   pair ordered:  f injective keeps the two images distinct
   bound:         fbound on both images
   collapsed:     Unit 29's transport, with symmetry if mapReq swapped the order
   valid:         validity transports (validResponse_rename), symmetry again
   child:         respond commutes with the action (respond_rename)

image total:  apply forward to the inverse renaming and read it backwards

selection:  regRegime, swap 0<->2, 1<->3
   least collapsed pair of both regimes: (0, 1)       [decided]
   mapReq swap (0, 1) = (2, 3) != (0, 1)              [decided]
```

## Python

The check script rebuilds the regression regime of
`tests/test_equivariance.py`, applies the renaming `(2, 3, 0, 1)`, and
compares children of the index-least pair with children of the related
pair; then it runs the orbit policy's full expansion under all 24
renamings. The essential lines:

```python
from derivation.candidates import Bounds, delta_events, min_responses
from derivation.engine import _quotient, closure_challenge_orbits
from derivation.iso import canonical, rename
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, Impose, replay
from derivation.observe import collapsed_pairs

reg = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitDatum("c"), AdmitDatum("d"),
              AdmitForm(1), AdmitInst(0, (2,)), AdmitInst(0, (3,))])
rr = rename(reg, (2, 3, 0, 1), (0,))
print(sorted(reg.insts), sorted(rr.insts))
print(collapsed_pairs(reg), collapsed_pairs(rr), canonical(reg) == canonical(rr))

def children(r, target):
    mr = min_responses(r, target, "mu1", Bounds(max_items=2, max_arity=2))
    return frozenset(canonical(replay((Impose(*target),) + delta_events(r, rep), r))
                     for rep, _ in _quotient(r, target, mr))

print(children(reg, (0, 1)) != children(rr, (0, 1)),
      children(reg, (0, 1)) == children(rr, (2, 3)))
print(closure_challenge_orbits(reg))
```

Output (from `python textbook/checks/u31_transition.py`):

```text
regRegime insts [(0, (2,)), (0, (3,))]; renamed insts [(0, (0,)), (0, (1,))]
collapsed: ((0, 1), (2, 3)) and ((0, 1), (2, 3)); same canonical key: True
mapReq of (0, 1) under the renaming: (2, 3)
children of the index-least pair (0, 1) on both sides differ: True; children of (0, 1) and of its image (2, 3) agree: True
challenge orbits of regRegime: ((0, 1), (2, 3))
expansion has 6 child classes; equal under all 24 renamings: True
```

## Line-by-line Python explanation

`reg` is `regRegime` built from events: four data, one unary form, two
instances marking data 2 and 3. `rename(reg, (2, 3, 0, 1), (0,))` sends
datum `k` to `pi[k]`, with the identity on the one form. The printed
instance lists show the marks moved to data 0 and 1: `rr` is
`renameRegimeR regSwap.f regRegime` of the Lean, up to the field the Lean
action leaves alone (`reqs` is empty here, so they agree exactly).

Both regimes have collapsed pairs `(0, 1)` and `(2, 3)`, and the same
canonical key: the quotient sees one regime. In `reg` the pair `(0, 1)` is
two unmarked data; in `rr` the same index pair is two marked data.

`children(r, target)` does one engine step for one challenge:
`min_responses` finds the cheapest valid responses under `mu1` within the
declared bounds, `_quotient` keeps one representative per isomorphism
class, and each representative is replayed after the imposition and
canonicalised. `children(reg, (0, 1)) != children(rr, (0, 1))` is `True`:
the index-least pair gives different children. `children(reg, (0, 1)) ==
children(rr, (2, 3))` is `True`: the pair and its image under the renaming
give the same children. That is the theorem, read on the implementation:
steps correspond under `mapReq`, not under the index.

`closure_challenge_orbits(reg)` returns both pairs: no automorphism of
`reg` exchanges the marked pair with the unmarked one (the regime has
four automorphisms, the test records), so the policy challenges both,
and the full expansion has six child classes. The last line of the check
runs that expansion under every one of the 24 renamings and finds the
same six classes every time. This is the class-set statement the ledger
leaves on the Python side.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/TransitionTransport.lean lines 109-118
def mapReq (f : Nat → Nat) (q : Nat × Nat) : Nat × Nat :=
  (min (f q.1) (f q.2), max (f q.1) (f q.2))

def renameRegimeR (f : Nat → Nat) (r : Regime) : Regime :=
  { renameRegime f r with reqs := r.reqs.map (mapReq f) }
```

```lean
-- Lean (Genesis), lean4/Derivation/TransitionTransport.lean lines 677-678, 820-823
def respond (r : Regime) (i j : Nat) (δ : List Item) : Option Regime :=
  (stepE r (.impose i j)).bind (fun s => applyDelta s δ)

def TransStep (r : Regime) (i j : Nat) (δ : List Item) (s : Regime) :
    Prop :=
  i < j ∧ j < r.data ∧ collapsed r i j ∧
  validResponse r i j δ ∧ respond r i j δ = some s
```

```lean
-- Lean (Genesis), lean4/Derivation/TransitionTransport.lean lines 828-857
theorem transStep_rename_fwd {n : Nat} (σ : DRen n) (r : Regime)
    (hn : r.data = n)
    (hinst : ∀ p ∈ r.insts, ∀ a ∈ p.2, a < r.data)
    (hreq : ∀ q ∈ r.reqs, q.1 < q.2 ∧ q.2 < r.data)
    {i j : Nat} {δ : List Item} {s : Regime}
    (h : TransStep r i j δ s) :
    TransStep (renameRegimeR σ.f r)
      (mapReq σ.f (i, j)).1 (mapReq σ.f (i, j)).2
      (δ.map (mapItem (padF n σ.f)))
      (renameRegimeR (padF n σ.f) s) := by
  obtain ⟨hij, hjd, hcol, hval, hresp⟩ := h
  refine ⟨mapReq_ordered σ.f_inj hij, ?_, ?_, ?_, ?_⟩
  · show max (σ.f i) (σ.f j) < (renameRegimeR σ.f r).data
    show max (σ.f i) (σ.f j) < r.data
    rw [hn]
    exact Nat.max_lt.mpr
      ⟨σ.fbound i (hn ▸ Nat.lt_trans hij hjd), σ.fbound j (hn ▸ hjd)⟩
  · rcases mapReq_cases σ.f (i, j) with hc | hc <;> rw [hc]
    · exact (collapsed_renameR σ r hn i j).mpr hcol
    · exact (collapsed_renameR σ r hn j i).mpr
        ((collapsed_symm r i j).mp hcol)
  · rcases mapReq_cases σ.f (i, j) with hc | hc <;> rw [hc]
    · exact (validResponse_rename σ r hn hinst hreq
        (Nat.lt_trans hij hjd) hjd δ).mpr hval
    · exact (validResponse_symm _ _ _ _).mp
        ((validResponse_rename σ r hn hinst hreq
          (Nat.lt_trans hij hjd) hjd δ).mpr hval)
  · rw [respond_rename σ r hn hinst hreq hij hjd δ, hresp]
    rfl
```

```lean
-- Lean (Genesis), lean4/Derivation/TransitionTransport.lean lines 972, 1000, 1064-1068
def regRegime : Regime := ⟨4, [1], [(0, [2]), (0, [3])], [], []⟩

def regSwap : DRen 4 where
  f := regSwapFun
  g := regSwapFun
  fg := regSwapFun_invol
  gf := regSwapFun_invol
  fbound := regSwapFun_bound
  gbound := regSwapFun_bound

theorem least_pair_selection_not_congruent :
    collapsed regRegime 0 1 ∧
    collapsed (renameRegimeR regSwap.f regRegime) 0 1 ∧
    mapReq regSwap.f (0, 1) ≠ (0, 1) :=
  ⟨reg_collapsed_01, reg_renamed_collapsed_01, by decide⟩
```

The book's Lean computes the renaming on the regression regime, records
that `mapReq` forgets order and so the action is not injective, shows
padding, and instantiates Genesis's transport at this renaming. A raw
disordered-demand example also shows why exact response transport needs
more than preservation of separability.

```lean
-- Lean (book), textbook/checks/u31_lean.py
theorem mapReq_swap_01 : mapReq regSwap.f (0, 1) = (2, 3) := by decide

theorem renamed_regRegime :
    renameRegimeR regSwap.f regRegime = ⟨4, [1], [(0, [0]), (0, [1])], [], []⟩ := by
  decide

theorem mapReq_comm (f : Nat → Nat) (i j : Nat) : mapReq f (i, j) = mapReq f (j, i) := by
  simp [mapReq, Nat.min_comm, Nat.max_comm]

theorem not_injective_on_disordered :
    renameRegimeR regSwap.f ⟨4, [1], [], [], [(0, 1)]⟩
      = renameRegimeR regSwap.f ⟨4, [1], [], [], [(1, 0)]⟩
    ∧ (⟨4, [1], [], [], [(0, 1)]⟩ : Regime) ≠ ⟨4, [1], [], [], [(1, 0)]⟩ :=
  ⟨by decide, by decide⟩

theorem padF_values : padF 4 regSwap.f 0 = 2 ∧ padF 4 regSwap.f 4 = 4 ∧ padF 4 regSwap.f 7 = 7 := by
  decide

theorem swap_carries_collapse :
    collapsed (renameRegimeR regSwap.f regRegime) 2 3 ↔ collapsed regRegime 0 1 :=
  collapsed_renameR regSwap regRegime rfl 0 1

theorem renamed_separable_02 : separable (renameRegimeR regSwap.f regRegime) 0 2 :=
  ⟨⟨0, [none]⟩, by decide, by decide⟩
```

## Line-by-line Lean explanation

**`mapReq`, `renameRegimeR`.** `min` and `max` of the two images put the
renamed demand in ordered form. The record update keeps everything
`renameRegime` did and replaces `reqs` by the mapped list.

**`respond`, `TransStep`.** `stepE r (.impose i j)` is `some` of the
regime with `(i, j)` added to its demands when the guard passes (Unit
17), else `none`; `Option.bind` then applies the response. `TransStep`
is a five-fold conjunction; the order of the conjuncts is the order the
proof discharges them.

**`transStep_rename_fwd`.** The hypotheses select two parts of
`Regime.wf`: every instance argument is below `r.data`, and each demand
is ordered with both endpoints admitted. The theorem does not ask for
the other `wf` fields. `obtain` splits the step into its five facts.
`refine ⟨_, ?_, ?_, ?_, ?_⟩` supplies the first conjunct at once
(`mapReq_ordered`: an injective map keeps `i < j` as a strict inequality
after ordering) and opens four goals.

*Bound.* The second component of `mapReq` is `max (σ.f i) (σ.f j)`; the two
`show` lines unfold the renamed regime's `data`, which the action did not
change. `Nat.max_lt.mpr` needs both images below `n`, which `fbound`
gives from `i < j < r.data`.

*Collapse.* `mapReq_cases` says the image pair is `(σ.f i, σ.f j)` or
`(σ.f j, σ.f i)`. In the first case Unit 29's transport, in its
requirements-aware form `collapsed_renameR`, gives the goal; in the
second the same after `collapsed_symm`.

*Validity.* The same split; `validResponse_rename` transports validity
(it needs `hinst`, `hreq` and the index bounds), and `validResponse_symm`
handles the swapped order.

*Child.* `respond_rename` says responding in the renamed regime is the
renamed response of the original, with the padded map on the child; `rw`
with it and with `hresp : respond r i j δ = some s` closes by `rfl`.

**`transStep_image_total`.** Not reproduced in full: it builds the
boundedness facts for the renamed regime (`rename_insts_bound`, and the
demand bound), applies `transStep_rename_fwd` to `σ.inv`, and shows the
result is the given step with `σ` and `σ.inv` cancelling. So every step
of the renamed regime is the image of a step of `r`.

**`least_pair_selection_not_congruent`.** Three facts. `reg_collapsed_01`
and `reg_renamed_collapsed_01` are proved alike: `one_unary_form_ctx_char`
says that in a regime whose only form is unary, every well-formed context
is the one-hole context `⟨0, [none]⟩`; `subst` replaces `c` by it, and
`decide` evaluates the two pluggings. The third fact is a decision:
`mapReq regSwap.f (0, 1)` computes to `(2, 3)`, which is not `(0, 1)`.
The theorem does not mention children or selection policies; it isolates
the one fact a selection would need and shows the renaming breaks it.

**The book's `mapReq_swap_01`, `renamed_regRegime`.** Decided on the
concrete data: the renaming carries the unmarked pair to the marked pair,
and moves the marks to data 0 and 1. `renamed_regRegime` is the Lean form
of the Python output `renamed insts [(0, (0,)), (0, (1,))]`.

**`mapReq_comm`, `not_injective_on_disordered`.** Because `mapReq` orders
its output, a regime with the demand `(0, 1)` and one with `(1, 0)` have
the same image, while they are different regimes. This refutes an
unrestricted inverse on raw records. It does not refute every possible
`iff`: a statement restricted to ordered records is a different claim.

**`respond_order_needed`.** Start with the raw demand list `[(1,0)]` and
rename by the identity. Ordering the demand gives `[(0,1)]`; imposing
`(0,1)` then leaves that list unchanged. In the other order, imposing
first gives `[(1,0),(0,1)]`, whose renamed list has two copies of `(0,1)`.
The literal response records differ. Both examples violate the theorem's
ordered-demand hypothesis; neither is a valid admission history.

**`padF_values`.** Below 4 the padded map is the swap; at 4 and 7 it is
the identity. A response that admits datum 4 therefore keeps it as datum 4
in the renamed child.

**`swap_carries_collapse`, `renamed_separable_02`.** Genesis's transport at
this renaming: `σ.f 0 = 2` and `σ.f 1 = 3` reduce, so the statement reads
`collapsed (renamed) 2 3 ↔ collapsed regRegime 0 1`. The separability
witness in the renamed regime shows the same index pair `(0, 2)` is
separated on both sides but for opposite reasons: in the original 0 is
unmarked and 2 marked, in the renamed regime the reverse. (The book's
first attempt stated `separable (renamed) 0 1`; `decide` reported it
false, since `(0, 1)` is the marked pair there. The check now carries
the true statement.)

**Axioms.** The concrete pair/regime equalities and `padF_values` report
no axioms. `mapReq_comm` and `respond_order_needed` report `propext`.
The collapse, separation, and cited native transport reports use
`propext, Quot.sound`. These are measured dependencies of these proofs;
using the same tactic name elsewhere need not give the same report.

## What has been proved

- Validity, the response composite and the one-round transition each
  transport along a datum renaming, with the child renamed by the padded
  map (Genesis, derived).
- The renamed transition relation is exactly the image of the original:
  forward mapping and image totality (Genesis, derived).
- The count of valid responses, comparing a caller's list with its mapped
  list and using correct deciders, is preserved (Genesis, derived; `validCount_rename`, the
  transition analogue of Unit 29's count).
- The index-least collapsed pair is `(0, 1)` on both sides of the
  regression renaming, and the renaming does not fix `(0, 1)` (Genesis,
  countermodel).
- The action is not injective on raw regimes with disordered demands;
  exact response transport can fail there (book Lean).

## What has not been proved

- The class-set statement: that the *set of canonical keys* of all
  children, across every challenge orbit, is equal under renaming. That
  needs the soundness of `canonical` (`CL-ISO-SOUND`, Python) to turn
  "children correspond under the padded renaming" into "equal keys", and
  it is the exhaustive test `test_orbit_policy_transition_congruence_exhaustive`
  and the last line of this unit's check.
- Transport under a renaming of forms, or under a general isomorphism
  (a pair of bijections). The Lean covers datum renamings with forms
  fixed; the ledger says so under `CL-TRANSITION-EQUIVARIANCE`.
- Transport of the minimum family itself (that `min_responses` of the
  renamed regime is the renamed minimum family). `validCount_rename`
  carries counts, not minima; minima are the Python enumeration's.
- Any statement about policies other than the one witnessed. The theorem
  refutes "least index"; it does not prove the orbit policy congruent.
  That is the test and the check, again computational.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `min`, `max`, `Nat.max_lt`, `Nat.le_total` | ordering a renamed demand | metatheory |
| `Option.bind`, `Option.map` | the response composite | metatheory |
| `padF`, `DRen.pad` | the fresh datum | metatheory; a construction on the renaming |
| `obtain`, `refine`, `rcases ... <;>`, `show`, `subst` | the transport | metatheory tactics |
| `decide` on `Regime` equality and on `mapReq` | the witnesses | metatheory; derived `DecidableEq` |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The regime, including its demands. A step is
the metatheory's description of one round; the regime holds the before
and after, and after a round it holds one more demand.

**Phrases to read with care.**

- "Datum-renamed regimes have corresponding transitions" is the proved
  relation statement with fixed forms and the stated bounds. Equal child
  class sets are checked within the explored Python bounds. The concrete
  index-least policy fails; this does not refute every policy that reads
  an index, including policies whose result happens to be invariant.
- "The policy was repaired" is a statement about Python. The Lean
  countermodel is the shape of the defect, not a theorem about the repair.
- "Equivariance" in the ledger names this congruence. The word carries no
  group theory the system can see; the regime has no automorphisms of its
  own, only the metatheory's renamings of it.

## Student exercise

`transStep_rename_fwd` needs `hreq : ∀ q ∈ r.reqs, q.1 < q.2 ∧ q.2 <
r.data`, while Unit 29's `collapsed_rename` needed nothing about `reqs`.
Which parts of transition transport read the demands? Use the raw
disordered-demand example to explain how exact response transport can
fail, even when the demand endpoints are still admitted.

## Answer

<details>
<summary>Worked answer</summary>

Both validity and the response composite read demands. Validity must
preserve every recorded pair; the response also inserts the target and
returns a literal demand list. With `[(1,0)]`, identity renaming sorts the
pair before insertion on one path and after insertion on the other.
One result has one copy of `(0,1)`, the other two. Thus their literal
records differ. This is a failure of exact response transport, not a
failure caused merely by two requirements having the same separation
test: separability is symmetric and repeating a test does not change its
truth. Collapse alone never reads demands, so its transport needs no
`hreq`.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/TransitionTransport.lean` lines 53-60, 97-104, 109-118, 121-126, 214-221, 677-678, 744-760, 820-823, 828-857, 866-901, 937-956, 972-1010, 1045-1068 |
| Axiom report | `artifacts/lean_axioms.txt`: `collapsed_renameR`, `transStep_rename_fwd`, `transStep_image_total`, `validCount_rename`, `least_pair_selection_not_congruent` all `[propext, Quot.sound]` |
| Paper | `paper/paper.md` §12 residual R7 (discharged 2026-08-18, scope stated 2026-09-08); ledger `CL-TRANSITION-EQUIVARIANCE` (theorem + finite computation + counterexample) |
| Tests | `tests/test_equivariance.py`: `test_regression_canonical_equal_under_rename`, `test_least_pair_selection_is_not_equivariant`, `test_regression_orbits_are_distinct_and_both_retained`, `test_orbit_policy_transition_congruence_exhaustive` |
| Check (Python) | `python textbook/checks/u31_transition.py`: the regression regime under `(2, 3, 0, 1)`; children of the index-least pair differ, children of the related pair agree; two challenge orbits; six child classes equal under all 24 renamings |
| Check (book Lean) | `python textbook/checks/u31_lean.py`: ten book theorems plus four Genesis theorems kernel-checked, Lean 4.33.0 |
