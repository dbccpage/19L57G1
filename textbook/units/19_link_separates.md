# Unit 19. The link regime `BL` separates

**Claim.** On the two-data starting regime `R2L`, one binary form and one
link instance provide a test distinguishing the data. Their two-item
cost attains the lower bound from Unit 18.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Starting from `R2L`, admitting one binary form and one instance
linking datum 0 to datum 1 produces a regime in which they are separable. The
witness is the context "hole in the first slot, datum 1 in the second":
plugged with 0 it is the admitted link, plugged with 1 it is not. The
two-item delta that builds it is a valid response to the demand, so the
cost floor of Unit 18 is attained.

**Status:** derived. **Lean:**
`Derivation.BL_separable` (`lean4/Derivation/Minimality.lean` lines 52-53),
with `BL` (line 42), `deltaBL` (line 62), `validResponse_R2L` (67-77) and
`deltaBL_valid` (85-86). **Axioms:** `propext, Quot.sound` (by `decide`).
**Depends on:** `separable`, `wfCtx`, `plug`, `derivable` (Unit 08);
`validResponse`, `applyDelta` (Unit 18).

</details>

## First pass

Give a two-place form the temporary name `link`. Admit just
`link(0, 1)`, with no uniform rule. Ask the same question of each datum:
“is `link(□, 1)` derivable?” The square is a place to fill.

| Fill the square with | Result | Derivable? |
|---|---|---|
| 0 | `link(0, 1)` | Yes: it is the admitted instance |
| 1 | `link(1, 1)` | No: there is no instance or rule for it |

One question gives different answers. That is a **witness** of separation.
It is a check of this formal record; the “no” is not a measurement of
a physical relationship.

Adding the form and the instance costs two items. Unit 18 rules out
cheaper answers on this starting regime, so this answer is cheapest
under item count. It need not be the only cheapest answer.

<details><summary>Predict: does adding the uniform rule preserve this distinction?</summary>

No. Both rows then derive, and every context of this form agrees on the
pair. More derivable answers can remove a distinction. Admission permits
the event; the separate response-validity check rejects it as a repair
for this demand.

</details>

## Question

Unit 18 says two items are the least that could work. Do two items work?
What, concretely, can give different derivability answers on the two
data, and how does the paper interpret it in relation to the
caller's ⟨ARB⟩?

## What we already possess

- `separable r d d'` is an existential: a well-formed context whose two
  pluggings differ in derivability (Unit 08).
- `wfCtx` has four parts: the form exists, the slot count is the arity,
  there is a hole, every filled slot names an admitted datum (Unit 08).
- `derivable r i` is membership in `insts` or coverage by a rule
  (Unit 01).
- `validResponse` and `applyDelta` (Unit 18).

## New concept: a witness that carries its own check

`BL = ⟨2, [2], [(0, [0, 1])], [], [(0, 1)]⟩`: two data, one form of arity
2, one instance of that form with arguments `[0, 1]`, no rules, the
demand. The name stands for *binary link*.

The witness context is `⟨0, [none, some 1]⟩`: form 0, first slot a hole,
second slot datum 1. Plugging (Unit 08) fills every hole with the same
datum:

- plug with 0: `(0, [0, 1])`, the admitted instance, derivable;
- plug with 1: `(0, [1, 1])`, not admitted, not derivable.

So the context is a witness. Because `separable` is stated existentially,
the proof *is* this context together with the two checks, and Lean's
`decide` runs both checks on the concrete lists.

## Plain-language interpretation

The system has been given a two-place sentence shape and one sentence in
it: "0 links to 1". Ask "does ⟨ ⟩ link to 1?" with each datum in the
blank. For 0 the derivability answer is Yes; for 1 it is No. This supplied
context treats the two indices differently under the declared observation
rule. The responder added its form and instance; the initial two-data
ledger supplied no separating context. This is one minimum-cost response,
not a uniquely prescribed first response.

This regime realizes the caller's ⟨ARB⟩, with ⟨A⟩ as 0, ⟨AB⟩ as 1 and the
form as R. But read "realizes" carefully: the form is not named R, the
instance is not oriented by anything the system knows, and the mirror
image `(0, [1, 0])` is an equally valid response (the Python check shows
it). The orientation lives in the metatheory's choice of argument order.

### One target and all recorded requests

For `R2L`, the stored request and the chosen target are both (0,1), so
one separating witness discharges both parts of validity. That shortcut
does not apply to an arbitrary list of requests.

Consider a **separate** starting ledger with three data, no forms or
instances, and requests (0,1) and (1,2). Choose (0,1) as the target.

Each pair column says whether that pair is separated:

| Two-item plan | Pair (0,1) | Pair (1,2) |
|---|---|---|
| Unary form, then `marked(0)` | Yes | No |
| Unary form, then `marked(1)` | Yes | Yes |

Both plans replay successfully. The first is not a valid response: on
1 and 2 its only context answers No/No. The second meets both requests:
the context answers No/Yes on (0,1) and Yes/No on (1,2). Neither request
was met in the initial form-less ledger. The added book proofs check
these facts; validity requires meeting all stored requests in the result.

<details>
<summary>Programs and proof walkthroughs (optional)</summary>

## Pseudocode

```
# Gloss
BL: data {0, 1}; form 0 of arity 2; instance (0, [0, 1]); demand (0, 1)
context c := (form 0, slots [hole, 1])
wf(c): form 0 exists; 2 slots = arity 2; a hole is present; 1 is admitted.  ✓
plug(c, 0) = (0, [0, 1])  -- admitted, derivable
plug(c, 1) = (0, [1, 1])  -- not admitted, no rule, not derivable
derivable differs  ⇒  separable(BL, 0, 1)
deltaBL = [newForm 2, newInst 0 [0, 1]]; applyDelta R2L deltaBL = BL  ⇒ valid response
```

## Python

```python
from derivation.candidates import NewForm, NewInst, apply_delta
from derivation.engine import GENESIS_L
from derivation.model import replay
from derivation.observe import contexts, derivable, plug, profile, witness

bl = apply_delta(replay(GENESIS_L), (NewForm(2), NewInst(0, (0, 1))))
print(len(contexts(bl)), witness(bl, 0, 1))
c = witness(bl, 0, 1)
print(plug(c, 0), derivable(bl, plug(c, 0)), plug(c, 1), derivable(bl, plug(c, 1)))
print(sorted(profile(bl, 0)), sorted(profile(bl, 1)))
```

Output:

```text
5 (0, (None, 1))
(0, (0, 1)) True (0, (1, 1)) False
[(0, (None, 1))] [(0, (0, None))]
```

## Line-by-line Python explanation

`apply_delta` (`candidates.py` line 135) translates the two items into
admission events and replays them on the base: `AdmitForm(2)` then
`AdmitInst(0, (0, 1))`. The result is `BL` with tokens instead of a count.

`contexts(bl)` has five entries: the slot tuples over `{hole, 0, 1}` of
length 2, minus the four with no hole (`observe.py` lines 37-45). The
check script prints all five with both pluggings; two are witnesses,
`(0, (None, 1))` and `(0, (0, None))`, and `witness` returns the first in
enumeration order, which is the one Lean names.

`plug(c, d)` (line 47) replaces each `None` by `d`. `derivable` (line 52)
is membership in `insts` or a rule on the form; `bl.rules` is empty.
If the uniform rule is admitted, every plugging for this form is
derivable. The check script and book Lean confirm that the pair then
collapses even though the original link instance remains.

The two profiles are different one-element sets, so `separable` is
`True`. Notice the profiles are *not* each other's complements: three
contexts are derivable for neither datum. Separation needs one
disagreement, not a total ordering.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Minimality.lean lines 42, 52-53, 62, 67-77, 85-86
/-- Binary link. -/
def BL : Regime := ⟨2, [2], [(0, [0, 1])], [], [(0, 1)]⟩

theorem BL_separable : separable BL 0 1 :=
  ⟨⟨0, [none, some 1]⟩, by decide, by decide⟩

def deltaBL : List Item := [.newForm 2, .newInst 0 [0, 1]]

/-- Helper: a response to the single requirement of `R2L` is valid as soon
as it applies and separates the target. -/
theorem validResponse_R2L (δ : List Item) (s : Regime)
    (happ : applyDelta R2L δ = some s) (hsep : separable s 0 1) :
    validResponse R2L 0 1 δ := by
  refine ⟨s, happ, hsep, ?_⟩
  intro q hq
  have : q = (0, 1) := by
    cases hq with
    | head => rfl
    | tail _ h => cases h
  rw [this]
  exact hsep

theorem deltaBL_valid : validResponse R2L 0 1 deltaBL :=
  validResponse_R2L _ BL (by decide) BL_separable
```

## Line-by-line Lean explanation

`BL_separable` is an anonymous constructor with three parts, matching
the shape of `separable`: the context, a proof it is well formed, and a
proof the pluggings differ. Both proofs are `by decide`: `wfCtx BL c` is
decidable (Genesis declares the instance, `Basic.lean` lines 112-113),
and so is the negated iff, since `derivable` is. The kernel evaluates
`plug`, list membership and the arithmetic on the concrete lists.

The book's `BL_separable'` does the same with every step named:
`BL_witness_wf` for the first `decide`, `BL_plug0` and `BL_plug1` by
`rfl` (plugging is a computation), `BL_derivable_01` and
`BL_not_derivable_11` by `decide`, and the final term
`fun h => BL_not_derivable_11 (h.mp BL_derivable_01)`: if the iff `h`
held, its forward direction would carry derivability of the link across
to `(0, [1, 1])`, which is refuted.

`validResponse_R2L` discharges the third conjunct of `validResponse`,
that every demand already in `R2L.reqs` is separated in the result. The
initial pair was collapsed. `R2L.reqs` is
`[(0, 1)]`, so `hq : q ∈ [(0, 1)]` forces `q = (0, 1)` by the two cases
of list membership (`head`, or `tail` into the empty list, impossible),
and `hsep` answers.

`deltaBL_valid` supplies `applyDelta R2L deltaBL = some BL` by `decide`
(the kernel runs both `applyItem` steps) and the witness.

**Axioms.** `propext, Quot.sound` for every `decide` over concrete lists;
`propext` alone for the equation `applyDelta R2L deltaBL = some BL`,
which `decide` proves without `Quot.sound`; the helper
`validResponse_R2L` uses only `propext`.

</details>

## What has been proved

- `BL` separates 0 from 1, with the named witness (Genesis, derived).
- `deltaBL` applies to `R2L`, lands on `BL`, and is a valid response
  (Genesis, derived).
- A second witness exists, `⟨0, [some 0, none]⟩`; a third context,
  `⟨0, [none, some 0]⟩`, is derivable for neither datum (book, derived by
  `decide`).
- `BL` is well formed (book, derived).
- Admitting the uniform rule leaves the link instance in place but
  collapses the pair (book, `BL_uniform_collapsed`).
- The mirror delta with instance `[1, 0]` is also a valid response
  (Genesis, verified finite: it is among the six `mu1` minima in the
  artifact).

## What has not been proved

- That `BL` is the only cheapest answer under item count. It is already
  known to be a cheapest answer: its cost is two and Unit 18 rules out
  smaller costs on this base. Unit 20 gives a second
  two-item answer that is not isomorphic to it; Unit 21 proves the
  non-uniqueness; Unit 22 shows that under the second measure `mu2` the
  link is *not* the minimum (its new-form arity sum is 2).
- A physical interpretation of the argument order. `[0, 1]` and `[1, 0]`
  are different ordered argument lists. The isomorphism maps data at
  each position; it does not swap the argument positions. A swap of the
  two data nevertheless relates the two one-link regimes in this example.
  That symmetry does not erase order from the instance representation.
- That the form "is" R or the instance "means" ⟨ARB⟩. The realization is
  the metatheory's reading.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| the literal `⟨2, [2], [(0, [0, 1])], [], [(0, 1)]⟩` | the regime | admitted by the responder's two items on top of Unit 05's admissions |
| `⟨0, [none, some 1]⟩` | the witness | a metatheory object (a context); the system does not hold contexts, only the instance |
| `decide` | the checks | metatheory evaluation of decidable predicates on finite lists |
| "realizes ⟨ARB⟩" | the paper's gloss | interpretation; the form has no name inside |

**What the system holds.** Two data, one form of arity 2, one instance,
one demand. That is all. The witness context, the profiles and the word
"link" are the metatheory's.

**Phrases to read with care.**

- “Links 0 to 1” names the ordered instance `[0,1]`. Reversing its
  arguments gives a different list; a particular context can distinguish
  their derivability in this regime. No physical direction or named
  relationship follows without an interpretation.
- "Separable" is the declared sense of Unit 08. Other senses (two tokens,
  two indices) were available to the metatheory all along and are not
  what was demanded.

## Student exercise

Change the instance to `(0, [1, 0])`, the mirror link, and keep the same
context `⟨0, [none, some 1]⟩`. Is the context still a witness? If not,
find one that is, and say why the mirror regime is still a valid
response.

## Answer

<details>
<summary>Check the exercise (optional)</summary>

With instance `(0, [1, 0])`: plug 0 gives `(0, [0, 1])`, not admitted;
plug 1 gives `(0, [1, 1])`, not admitted; the context is no longer a
witness. The context `⟨0, [some 1, none]⟩` is: plug 0 gives `(0, [1, 0])`,
the admitted instance; plug 1 gives `(0, [1, 1])`, not admitted. So the
mirror regime separates 0 from 1, and the delta `[.newForm 2,
.newInst 0 [1, 0]]` applies and is valid. The Python check confirms both
deltas valid, and Unit 21's Python shows the two regimes are isomorphic
under the swap of data: they are one class.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Minimality.lean` lines 42, 52-53, 62, 67-77, 85-86 |
| Axiom report | `artifacts/lean_axioms.txt`: `BL_separable`, `deltaBL_valid` `[propext, Quot.sound]`; `validResponse_R2L` `[propext]` |
| Paper | `paper/paper.md` §7.2 (two-item responses exist), §7.3 table row L: "binary link" |
| Ledger | `paper/paper_claim_ledger.md`, `CL-3-MIN-TWO` (existence), `CL-3-TIE-CLASSES` (the link class) |
| Artifact | `artifacts/challenges.json`, `challenge3.L.mu1.iso_classes`, label `form2+inst2`, class size 2 |
| Test | `tests/test_candidates.py::test_c3_cost1_all_fail_and_min_is_two` (6 minima: "2 unary marks + 4 binary variants"); `tests/test_engine.py::test_challenge3_reading_l_classes` |
| Check (Python) | `python textbook/checks/u19_link.py`: five contexts with both pluggings printed, two witnesses, `witness()` equal to Lean's; profiles; demand satisfied; both link deltas valid; a form alone does not separate; adding the uniform rule retains the instance and removes separation |
| Check (book Lean) | `python textbook/checks/u19_lean.py`: sixteen book reports plus three Genesis theorems kernel-checked, Lean 4.33.0. Five added reports check the multi-request example: `partial_lands` uses `propext`; target separation, the other pair's collapse, invalidity and the middle-mark repair use both `propext, Quot.sound`. Original reports retain their exact axiom sets |
