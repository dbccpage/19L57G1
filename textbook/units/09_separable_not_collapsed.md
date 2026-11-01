# Unit 09. A witness rules out collapse

**Claim.** If two data are separable, they are not collapsed. The proof is
constructive: the witness context that separates them is the very context
on which collapse would have to hold.

<details>
<summary>Source and classification record (optional on a first reading)</summary>

**Status:** derived. **Lean:**
`Derivation.separable_not_collapsed` (`lean4/Derivation/Basic.lean` lines
128-130). **Axioms:** `propext` (from the definitions). **Depends on:**
`collapsed`, `separable` (Unit 08).

</details>

## First pass

Suppose somebody claims every available question gives the same
answer for 0 and 1. You show Unit 08's `marked(_)`, which is derivable
on 1 and not on 0. That one question refutes the all-agreement claim.
No further search is needed once this witness is supplied.

<details><summary>Predict: does checking two tests without finding a difference establish collapse?</summary>

Only if those tests cover every allowed context, or another proof rules
out all remaining witnesses. Stopping after two tests from a longer list
does not establish the all-agreement claim.

</details>

## Follow a complete small search

Use a separate model with data 0 and 1, a two-place form linked, only
`linked(0,1)` admitted, and no uniform rule. Here are all five contexts;
every hole receives the tested datum.

| Test slots | On 0 | On 1 |
|---|---|---|
| `(_,_)` | No | No |
| `(_,0)` | No | No |
| `(_,1)` | Yes | No |
| `(0,_)` | No | Yes |
| `(1,_)` | No | No |

The first two rows agree. The third is a witness, so search can stop
there when its task is to find one. Checking every row would also find
the fourth witness. Different valid witnesses establish the same
separability claim; the definition does not require a unique witness.

If no row differs, the conclusion needs the whole allowed list. The new
book-Lean search proves both that its enumeration covers every well-formed
context and that its returned answer has the stated meaning. This adds a
general constructive search for the native finite-context grammar. The
Python forty-regime check remains separate implementation evidence.

## Question

Unit 08 defined collapse as "every context agrees" and separability as
"some context disagrees". Are these two definitions really opposites, or
could a pair of data be both? And is the connection a matter of logic
alone, or does it need a search?

## What we already possess

- `collapsed r d d'`: for every well-formed context `c`, the pluggings of
  `d` and `d'` are derivable together or not at all.
- `separable r d d'`: there exists a well-formed context on which they
  disagree.
- One concrete separable pair: datum 0 and datum 1 in `U1 = ⟨2, [1],
  [(0, [1])], [], [(0, 1)]⟩`, with witness `⟨0, [none]⟩`
  (`Minimality.U1_separable`, met in Unit 08's check).

## New concept: a proof that uses its hypothesis's witness

An existential hypothesis, "there is a `c` such that...", can be *opened*:
the proof gets to name that `c` and use the facts that came with it. A
universal hypothesis, "for every `c`...", can be *applied* to any `c` the
proof names. The theorem here opens the separability witness and applies
the collapse hypothesis to it. The two facts about that one context
contradict each other. No search over contexts is needed, because the
witness was handed over with the hypothesis.

This is why `separable` was defined with `∃` and not as "not collapsed":
a proof of `separable` must carry a witness, and the theorem can use it.

## Plain-language interpretation

Collapse says: "every stencil treats the two alike." Separability says:
"here is a stencil that does not." Hold the two claims next to each other
and point at the stencil: collapse promised it would treat them alike, and
it does not. One of the claims is false. Since the stencil is in hand, it
is collapse that fails.

The book first proves a different converse: **no separating witness exists
implies every context agrees**. Together with the first theorem, this
gives `collapsed ↔ ¬ separable`. That displayed proof does not by itself
turn `¬ collapsed` into a positive witness. Doing that constructively
requires an additional argument, such as a proved complete finite
context search. Deciding each individual context is not that whole-search
argument. The separate book search now supplies the missing enumeration
and correctness proofs for this grammar. It does not rely on an arbitrary
early cutoff or on a test pass over forty sample regimes.

## What the proved search returns

`firstWitness r d e` builds a finite list of contexts for the supplied
ledger, then checks their answers in order. A returned context is
well formed and distinguishes the two inputs. A return of `none` means
every well-formed context agrees: exactly `collapsed r d e`.

The completeness proof lists each admitted form index and every slot
list of its required length. Each slot is a hole or an in-range filled
index; the well-formedness filter keeps the actual tests. This covers an
arbitrary ledger's native `wfCtx` predicate, not just the five-row example.
The scan proof then connects the entire list to the all-context claim.

Consequently `¬ collapsed r d e → separable r d e` has a separate
constructive book proof. This result uses the finite grammar and decidable
derivability tests. It is not a principle extracting witnesses from every
negated universal claim. The enumeration can be large; no speed bound is
claimed. The native predicates themselves accept any natural-number
inputs; an application to admitted data still checks their range.

<details><summary>Finite-search proof and source names (optional)</summary>

[The book source](../checks/context_search_lean.py) defines `slotChoices`,
`slotLists`, `allContexts`, `scan` and `firstWitness`. It proves
`allContexts_sound`, `allContexts_complete`, `firstWitness_some_sound`,
`firstWitness_none_iff_collapsed` and `separable_of_not_collapsed`, with
supporting list lemmas. All nine added reports use exactly `propext,
Quot.sound`. Native sealed sources are unchanged. This is a proof over
the Lean definitions, not over the Python source or physical measurements.

</details>

<details>
<summary>Programs and proof walkthroughs (optional)</summary>

## Pseudocode

```
# Gloss
given: a context c, well formed, on which d and d' disagree
suppose collapse: every well-formed context agrees on d and d'
apply collapse to c:  c agrees on d and d'
but c disagrees.  contradiction.
therefore: not collapsed.
```

## Python

Python has no proof. It has the two computed predicates, and they are
each other's complement by construction: `separable` is `profile(i) !=
profile(j)`, and `collapsed_pairs` lists the pairs with `profs[i] ==
profs[j]`. The check script confirms, on a finite family of regimes, that
a witness exists exactly when the pair is separable and exactly when it is
not in `collapsed_pairs`.

```python
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, replay
from derivation.observe import collapsed_pairs, separable, witness

r = replay([AdmitDatum("<a>"), AdmitDatum("<ab>"), AdmitForm(1), AdmitInst(0, (1,))])
print(separable(r, 0, 1), witness(r, 0, 1), collapsed_pairs(r))
```

Output:

```text
True (0, (None,)) ()
```

## Line-by-line Python explanation

`r = replay([...])` builds the regime `U1` of the Lean, token by token:
two data, one unary form, the instance "datum 1 is marked". (The Lean `U1`
also carries the demand `(0, 1)`; the demand plays no part in
separability.)

`separable(r, 0, 1)` compares the two profiles (Unit 08) and finds them
different: `True`.

`witness(r, 0, 1)` returns the first context that disagrees: the unary
stencil `(0, (None,))`.

`collapsed_pairs(r)` lists pairs with equal profiles: the empty tuple `()`.
The pair `(0, 1)` is not collapsed.

So the three outputs agree with the theorem: separable, witness in hand,
not collapsed. The check script does this for forty regimes.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Basic.lean lines 127-130
/-- Separability contradicts collapse (constructively). -/
theorem separable_not_collapsed {r : Regime} {d d' : Nat}
    (h : separable r d d') : ¬ collapsed r d d' :=
  fun hc => h.elim fun c hc' => hc'.2 (hc c hc'.1)
```

The book's Lean restates the same proof with each step on its own line,
proves collapse from absence of separation, records the precise
negated consequence, and instantiates on `U1`.

```lean
-- Lean (book), textbook/checks/u09_lean.py
theorem separable_not_collapsed' (r : Regime) (d d' : Nat)
    (h : separable r d d') : ¬ collapsed r d d' := by
  intro hc
  obtain ⟨c, hwf, hne⟩ := h
  have hiff : derivable r (plug c d) ↔ derivable r (plug c d') := hc c hwf
  exact hne hiff

theorem collapsed_of_not_separable (r : Regime) (d d' : Nat)
    (h : ¬ separable r d d') : collapsed r d d' := by
  intro c hwf
  by_cases hiff : derivable r (plug c d) ↔ derivable r (plug c d')
  · exact hiff
  · exact absurd ⟨c, hwf, hiff⟩ h

theorem collapsed_iff_not_separable (r : Regime) (d d' : Nat) :
    collapsed r d d' ↔ ¬ separable r d d' :=
  ⟨fun hc hs => separable_not_collapsed hs hc, collapsed_of_not_separable r d d'⟩

theorem not_collapsed_iff_not_not_separable (r : Regime) (d d' : Nat) :
    ¬ collapsed r d d' ↔ ¬¬ separable r d d' := by
  constructor
  · intro hnc hns
    exact hnc (collapsed_of_not_separable r d d' hns)
  · intro hnns hc
    exact hnns ((collapsed_iff_not_separable r d d').mp hc)

theorem U1_not_collapsed : ¬ collapsed U1 0 1 :=
  separable_not_collapsed U1_separable
```

## Line-by-line Lean explanation

**Genesis's one-line proof.** `{r : Regime} {d d' : Nat}` in curly braces
are *implicit* inputs: Lean works them out from `h`. `(h : separable r d d')`
is the hypothesis. The conclusion `¬ collapsed r d d'` means "collapse
implies `False`".

`fun hc => ...`: to prove a negation, assume the thing (`hc : collapsed r
d d'`) and derive `False`.

`h.elim fun c hc' => ...`: open the existential `h`. `elim` says: to use
"there exists `c` with property", give a function that, for any `c` and
proof `hc'` of the property, produces the goal. Here `hc'` is a pair:
`hc'.1 : wfCtx r c` and `hc'.2 : ¬ (derivable ... ↔ derivable ...)`.

`hc c hc'.1`: apply collapse to the witness `c` and its well-formedness.
Result: the two pluggings are equivalent, `derivable r (plug c d) ↔
derivable r (plug c d')`.

`hc'.2 (...)`: `hc'.2` is the negation of exactly that equivalence. Applying
a negation to a proof of what it negates gives `False`. Done.

**The book's `separable_not_collapsed'`.** The same, step by step. `intro
hc` assumes collapse. `obtain ⟨c, hwf, hne⟩ := h` opens the witness and
names its two facts. `have hiff : ... := hc c hwf` applies collapse to it.
`exact hne hiff` is the contradiction.

**`collapsed_of_not_separable`.** Assume no witness exists. To prove
collapse, `intro c hwf`: take any well-formed context. `by_cases hiff : (...
↔ ...)`: either the two pluggings are equivalent or not. Lean accepts this
case split constructively because `derivable` is decidable (Genesis
declares the instance in `Basic.lean` line 88), and so is the `↔` of two
decidables. First case: that is the goal. Second case: then `⟨c, hwf,
hiff⟩` is a witness of separability, contradicting `h`; `absurd` turns the
contradiction into the goal. The axiom report confirms no
`Classical.choice` was used.

**`collapsed_iff_not_separable`.** The two directions packaged with `⟨_, _⟩`.
The first direction is Genesis's theorem with the arguments swapped into
place: given collapse `hc` and separability `hs`, `separable_not_collapsed
hs hc : False`.

**`U1_not_collapsed`.** Genesis's theorem applied to Genesis's
`U1_separable`. No new computation; the witness inside `U1_separable` does
the work.

**Negating the equivalence.** The new theorem says `¬ collapsed`
is equivalent to ruling out `¬ separable`. It records the double negation;
it does not eliminate that negation to exhibit a context. The proof first
uses the no-witness-to-collapse direction and then the opposite direction
of the existing equivalence. A stronger positive extraction claim needs
its own proof.

**Axioms.** `separable_not_collapsed` reports `propext`, inherited from
the definitions. The book's per-context decision also reaches
`Quot.sound`, even when the regime is an arbitrary parameter. The eight
original reports comprise three `propext` and five `{propext, Quot.sound}`
sets. The finite-search continuation adds nine reports, each exactly
`propext, Quot.sound`: seventeen combined reports, three `propext` and
fourteen both. It adds no `Classical.choice` dependency.

</details>

## What has been proved

- Separable implies not collapsed, for every regime and every pair
  (Genesis, derived).
- Not separable implies collapsed, constructively (book Lean, derived).
- Precisely, `collapsed ↔ ¬ separable`; negating this gives
  `¬ collapsed ↔ ¬¬ separable` (book Lean). This last statement is not
  a displayed witness-extraction theorem.
- The separately defined finite search is sound and complete for native
  contexts, and supplies `¬ collapsed → separable` constructively (book).

## What has not been proved

- Which pairs are separable in any given regime. That is decided case by
  case (Unit 10 for regimes with no instances; Units 18-22 for the first
  regimes that separate anything).
- That the Lean search verifies Python's implementation, physical observations,
  or a different context grammar. Those need their own connections. The
  forty-regime Python check is scoped computational evidence; the general
  search proof concerns the explicitly enumerated native Lean contexts.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `∃`-elimination, `∀`-application | the proof | metatheory logic (constructive) |
| `Decidable` instance for `derivable`, `by_cases` | the converse | metatheory; decidability is a property of the admitted definitions, not an added axiom |
| `{r : Regime} {d d' : Nat}` | the universal statement | metatheory quantifiers |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** Unchanged: the ledger. The theorem is about the
metatheory's two descriptions of it.

**Phrases to read with care.**

- "The system knows the two are different" overstates. The metatheory has
  a witness context; the system has the ledger from which the witness's
  pluggings are derivable or not.
- "Collapse is the absence of a witness" is now a theorem, not a
  definition. Genesis chose to define separability positively and prove
  the link.

## Student exercise

Why does Genesis state `separable` with `∃` rather than defining it as
`¬ collapsed`? Give one consequence for proofs.

<details>
<summary>Check the exercise (optional)</summary>

## Answer

With `∃`, every proof of separability must present a context, and that
context can be opened and used, as this theorem does. A negation-only
definition would not by itself supply a context. The original
`collapsed_of_not_separable` proof gives `¬ separable → collapsed`;
it does not alone give `¬ collapsed → separable`. The new finite search
does supply a witness for this grammar, with an additional completeness
proof. The explicit
witness form is the one used in the named later separation proofs (`U0_separable`,
`BL_separable`, `BD_separable`, `markK_separable` all begin with a
concrete context).

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Basic.lean` lines 127-130; decidability instance for `derivable` line 88 |
| Axiom report | `artifacts/lean_axioms.txt`: `separable_not_collapsed` `[propext]`; `U1_separable` `[propext, Quot.sound]` |
| Paper | `paper/paper.md` §3 item 5 (profile, collapse, internal separability) |
| Check (Python) | `python textbook/checks/u09_witness.py`: 40 regimes (two data, one form of arity 1 or 2, every instance subset, rule or not); 16 separable with a verified witness, 24 collapsed with no differing context; `separable` equals "witness exists" equals "not in `collapsed_pairs`" on every one |
| Check (book Lean) | `python textbook/checks/u09_lean.py`: the original eight reports plus nine finite-search reports; seventeen total: three `propext`, fourteen `{propext, Quot.sound}` |
