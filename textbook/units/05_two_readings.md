# Unit 05. Is ⟨⟩ admitted? Readings L and F

**Claim.** The seed does not say whether the initial inscription ⟨⟩ is
admitted at genesis. Genesis carries two readings, L and F, each as its own
recorded history, and proves that each history replays exactly to its
Challenge-3 regime. Which reading is right is not decided by anything in
the system. **Status:** open (the choice); derived (each replay).
**Lean:** `Derivation.historyL_replays`, `Derivation.historyF_replays`
(`lean4/Derivation/Inertia.lean` lines 57-73). **Axioms:** `propext`,
`propext`. **Depends on:** `genesis`, `stepE`, `replayE` (Units 01, 03),
`R2L`, `R2F` (Unit 01), `TRegime`, `stepT`, `replayT` (Unit 06, used here
for one check and taught there).

## Question

The seed's first sentence of substance is: "The only initial
object-language inscription is: `<>`" (`prompt/seed_prompt.md` §1). Is ⟨⟩
thereby *admitted*, so that the ledger starts with one datum? Or is it only
*presented*, so that the ledger starts empty? And if the text does not say,
what does a careful derivation do?

## What we already possess

- A ledger changes only through events (Unit 04); a supply changes nothing
  (Unit 03); admission is a separate event (Unit 03).
- Two target regimes are already defined in `Basic.lean`: `R2L`, with two
  data and the demand `(0, 1)`, and `R2F`, with three data and the demand
  `(1, 2)` (Unit 01).
- The seed's later challenges: Challenge 1 "supplies" ⟨A⟩; Challenge 2
  "supplies and retains" ⟨A⟩ and ⟨AB⟩ (`prompt/seed_prompt.md`, Challenges
  1 and 2).

## New concept: an underdetermined text, carried as two readings

A text **underdetermines** a question when two careful readers can follow
it and reach different states. Genesis's rule for such a case is not to
pick. It records both readings as histories and proves facts about each.
A reading is eliminated only by a proof that it is incoherent, and no such
proof exists here.

**Reading L** (strict admission): only an explicit act of retention admits.
Challenge 0 presents ⟨⟩ and retains nothing; Challenge 1 supplies ⟨A⟩ and
retains nothing; Challenge 2 "supplies and retains" ⟨A⟩ and ⟨AB⟩, so those
two are admitted. The ledger at Challenge 2 holds two data.

**Reading F** (possession admission): the one initial inscription is
admitted at genesis, because the seed says it *is* the object language's
inscription. Supplied inscriptions are admitted on retention, as in L. The
ledger at Challenge 2 holds three data: ⟨⟩, ⟨A⟩, ⟨AB⟩.

There is a smaller question nested inside Challenge 1: is ⟨A⟩ admitted when
it is merely supplied? Genesis carries both **sub-readings** too, and shows
by computation that they converge: once Challenge 2 retains ⟨A⟩, admitting
it a second time changes nothing (re-admission designates, Unit 06). So
that question dissolves. The question about ⟨⟩ does not dissolve, because
nothing later retains ⟨⟩.

A second new concept is the proof tactic `decide`. When a statement is
about specific finite values with no variables, Lean can often *compute*
whether it is true. `decide` asks Lean to run that computation inside the
kernel and accept the result as the proof. It fails if any variable is
free, or if the statement has no decision procedure.

## Plain-language interpretation

Two bookkeepers read the same instructions. One starts with an empty
notebook; the other writes ⟨⟩ on the first line because the instructions
mentioned it. Both then follow identical instructions. They end with
different notebooks, and the difference never goes away. Genesis keeps both
notebooks, proves facts about both, and refuses to say which bookkeeper
read correctly, because the instructions do not say.

One consequence matters for everything later: the Challenge-3 demand
"separate ⟨A⟩ from ⟨AB⟩" names the two data by their *position* in the
ledger. In reading L they are data 0 and 1; in reading F they are data 1
and 2. The same demand is written differently in each reading, and each
reading's demand is ill formed in the other (shown below).

## Pseudocode

```
# Gloss
reading L history:  supply <>, supply <a>, supply <a>, supply <ab>,
                    admit <a>, admit <ab>, demand (0, 1)
reading F history:  supply <>, admit <>, supply <a>, supply <a>, supply <ab>,
                    admit <a>, admit <ab>, demand (1, 2)
replay L  = ledger with 2 data and demand (0, 1)     -- R2L
replay F  = ledger with 3 data and demand (1, 2)     -- R2F
R2L ≠ R2F
```

## Python

```python
# Python (Genesis), code/derivation/engine.py lines 64-81
GENESIS_L: tuple[Event, ...] = (
    Supply("<>"),
    Supply("<a>"),
    Supply("<a>"),
    Supply("<ab>"),
    AdmitDatum("<a>"),
    AdmitDatum("<ab>"),
)

GENESIS_F: tuple[Event, ...] = (
    Supply("<>"),
    AdmitDatum("<>"),
    Supply("<a>"),
    Supply("<a>"),
    Supply("<ab>"),
    AdmitDatum("<a>"),
    AdmitDatum("<ab>"),
)
```

```python
from derivation.engine import GENESIS_F, GENESIS_L
from derivation.model import replay

print(replay(GENESIS_L).data)
print(replay(GENESIS_F).data)
```

Output:

```text
('<a>', '<ab>')
('<>', '<a>', '<ab>')
```

## Line-by-line Python explanation

`GENESIS_L: tuple[Event, ...] = (...)`: a name is given a **tuple**, an
ordered sequence that cannot be changed afterwards, written with round
brackets. The part after the colon, `tuple[Event, ...]`, is a type note:
"a tuple of any length whose items are events". Python does not enforce the
note at run time; the project's type checker does.

`Supply("<>")`: builds a supply event carrying the text `"<>"`. In Python
the token is a string; Lean uses a number in its place (Unit 03).

`AdmitDatum("<a>")`: builds an admission event for the token `"<a>"`.
Reading L's tuple has two such events, for ⟨A⟩ and ⟨AB⟩; reading F's has
three, the extra one admitting `"<>"` right after it is supplied.

The histories are written in the seed's order: Challenge 0 supplies ⟨⟩,
Challenge 1 supplies ⟨A⟩, Challenge 2 supplies ⟨A⟩ again together with
⟨AB⟩ and retains both. That is why `Supply("<a>")` appears twice.

`replay(GENESIS_L)`: Unit 04's function, applying each event in turn to the
empty ledger. `.data` reads the tuple of admitted tokens. Reading L gives
two; reading F gives three, with `'<>'` first.

The demand is not in these tuples. Genesis adds it when Challenge 3 is
analysed, using `READING_L.target == (0, 1)` and `READING_F.target == (1, 2)`
(`engine.py` lines 92-106). The check script adds it and shows the two
resulting ledgers match `R2L` and `R2F` in shape.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Inertia.lean lines 59-73
/-- The recorded Challenge 0-3 history of reading L replays exactly to the
Challenge 3 regime (replayability of the admitted state). -/
theorem historyL_replays :
    replayE
      [.supply 0, .supply 1, .supply 1, .supply 2,
       .admitDatum, .admitDatum, .impose 0 1] genesis = some R2L := by
  decide

/-- Reading F likewise. -/
theorem historyF_replays :
    replayE
      [.supply 0, .admitDatum, .supply 1, .supply 1, .supply 2,
       .admitDatum, .admitDatum, .impose 1 2] genesis = some R2F := by
  decide
```

The book's Lean adds what the two theorems leave unsaid: that the two
regimes differ, by how much, that each reading's demand is ill formed in
the other, and (in the token-aware model of Unit 06) that the Challenge-1
sub-readings converge while L and F do not.

```lean
-- Lean (book), textbook/checks/u05_lean.py
theorem R2L_ne_R2F : R2L ≠ R2F := by decide

theorem readings_differ_by_one : R2F.data = R2L.data + 1 := rfl

theorem F_without_genesis_admission :
    replayE [.supply 0, .supply 1, .supply 1, .supply 2,
             .admitDatum, .admitDatum, .impose 1 2] genesis = none := by
  decide

def tgenesis : TRegime := ⟨[], [], [], [], []⟩

theorem subreadings_converge :
    replayT [.supply 0, .supply 1, .admitDatum 1, .supply 1, .supply 2,
             .admitDatum 1, .admitDatum 2] tgenesis
      = replayT [.supply 0, .supply 1, .supply 1, .supply 2,
                 .admitDatum 1, .admitDatum 2] tgenesis := by
  decide

theorem readings_do_not_converge :
    replayT [.supply 0, .admitDatum 0, .supply 1, .supply 1, .supply 2,
             .admitDatum 1, .admitDatum 2] tgenesis
      ≠ replayT [.supply 0, .supply 1, .supply 1, .supply 2,
                 .admitDatum 1, .admitDatum 2] tgenesis := by
  decide
```

## Line-by-line Lean explanation

**`historyL_replays`.** The statement has no variables: a specific list of
seven events, the specific regime `genesis`, and the specific regime `R2L`.
`replayE [...] genesis` is a computation. `some R2L` is a value. The
statement says the computation's result is that value.

The list is written with `.supply 0` and the like; the leading dot picks
the constructor out of `Event`. The numbers are tokens: 0 for ⟨⟩, 1 for
⟨A⟩, 2 for ⟨AB⟩. Lean's `admitDatum` carries no token, because the Lean
`Regime` keeps only a count (Unit 06 explains the erasure). The final
`.impose 0 1` is the Challenge-3 demand, naming data 0 and 1.

`:= by decide`: Lean evaluates `replayE [...] genesis` step by step. Each
`stepE` is a small function on concrete numbers and lists, so the kernel
can unfold it. Four supplies leave `genesis` as it is; two admissions
raise the count to 2; `impose 0 1` passes its guard `0 < 1 ∧ 1 < 2` and
inserts `(0, 1)`. The result is `⟨2, [], [], [], [(0, 1)]⟩`, which is
`R2L` by definition. `decide` compares the two values with the derived
`DecidableEq` instance and finds them equal, so the proof is complete. No
step is hidden from the kernel; the kernel re-runs the computation.

**`historyF_replays`.** The same, with an admission after the first supply
and the demand `.impose 1 2`. The guard `1 < 2 ∧ 2 < 3` passes because the
count is 3. The result is `R2F`.

**Why `propext`?** `decide` itself adds no axiom. The statement mentions
`replayE`, whose definition reaches `insertNew` and `List.getD`, which
depend on `propext` (Unit 03, **Axioms**). The axiom is inherited from the
definitions, not introduced by the proof.

**`R2L_ne_R2F`.** `≠` means "equal is false". `decide` evaluates the
equality test on the two concrete regimes, gets `false`, and so proves the
negation. Report: no axioms, since neither `R2L` nor `R2F` mentions
`stepE`.

**`readings_differ_by_one`.** `R2F.data` is 3, `R2L.data` is 2, and `3 = 2 + 1`
holds by computation, so `rfl` closes it. No axioms.

**`F_without_genesis_admission`.** Take reading F's history and delete the
genesis admission. Replay reaches count 2, then meets `.impose 1 2`. The
guard asks `2 < 2`, which is false, so `stepE` returns `none`, and
`foldlM` stops with `none`. `decide` confirms the whole replay is `none`.
So reading F's demand is ill formed in reading L's ledger: the demand's
indices are relative to the reading. (The symmetric fact, that `impose 0 1`
in reading F names ⟨⟩ and ⟨A⟩ rather than ⟨A⟩ and ⟨AB⟩, is a matter of
which pair the demand picks, not of well-formedness; the Python check
prints both targets.)

**`tgenesis`.** The token-aware starting state, empty in all five fields.
This is a definition made for the book; Genesis's `Erasure.lean` defines
`TRegime` but names no genesis for it.

**`subreadings_converge`.** Two token-aware histories. The left one admits
token 1 at Challenge 1 (the "admit on supply" sub-reading); the right one
does not. Both admit 1 and 2 at Challenge 2. `stepT`'s admission rule is:
if the token is already present, change nothing; otherwise append it. So
the left history's second admission of 1 is a no-op, and both histories
end at tokens `[1, 2]`. `decide` runs both replays and compares. Report:
`propext` and `Quot.sound`; the membership test `tok ∈ t.tokens` is decided
by a library procedure on lists that carries both axioms. Both are inside
Genesis's declared axiom boundary.

**`readings_do_not_converge`.** The same comparison with ⟨⟩ admitted at
genesis on the left. The left ends at `[0, 1, 2]`, the right at `[1, 2]`.
They differ, and `decide` proves the `≠`.

## What has been proved

- Each reading's recorded history replays exactly to its Challenge-3
  regime (Genesis, `historyL_replays`, `historyF_replays`, derived).
- The two regimes differ, by one datum (book Lean, derived).
- Reading F's demand is ill formed on reading L's ledger (book Lean).
- The Challenge-1 sub-readings converge at Challenge 2 close, and readings
  L and F do not (book Lean, on the token-aware model; the paper records
  the convergence as **[finite computation]**, `CL-1-READING-CONVERGENCE`).

## What has not been proved

- Which reading the seed intends. No theorem decides it, and the paper
  marks the matter **[unresolved]** for ⟨A⟩ at Challenge 1 (then resolved
  by convergence) and carries both readings for ⟨⟩ throughout
  (`paper/paper.md` §5; ledger `CL-1-READING-CONVERGENCE` and the
  dual-reading entry). This unit's status is **open** for that reason.
- That the two readings lead to different *answers* later. In fact every
  later theorem is proved for both (`R2L_collapsed` and `R2F_collapsed`,
  `cost1_insufficient` and `cost1_insufficient_F`, and so on). The readings
  differ in bookkeeping, and the derivation shows the bookkeeping does not
  change the minimum cost or the collapse results. It does change the
  indices in every demand.
- That "admitted at genesis" means anything beyond "counted in `data`". In
  reading F the ledger counts ⟨⟩, but ⟨⟩ is as collapsed and as inert as
  any other datum (Unit 16).

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| concrete lists of events, `decide` | the replay theorems | metatheory computation, re-run by the kernel |
| `Nat` tokens 0, 1, 2 | naming ⟨⟩, ⟨A⟩, ⟨AB⟩ in the token-aware model | metatheory labels; the system never sees them (Unit 06) |
| `propext`, `Quot.sound` | inherited through `stepE`, `stepT` | inside the declared boundary |

**What the system holds.** Under L, after Challenge 3: two data and one
demand. Under F: three data and one demand. Under neither does it hold a
reason for the choice.

**Admissions and their price.** Reading F admits one more datum than
reading L. The price is paid in every later index: each demand, each
instance argument, each witness context is shifted by one. Nothing else is
bought: the extra datum has no instances and separates nothing.

**Phrases to read with care.**

- "The system starts with ⟨⟩" is reading F's choice, made by the reader of
  the seed, not by the system.
- "Both readings agree" is true of the theorems proved for both and false of
  the ledgers, which differ. Say which is meant.
- "The sub-readings converge" is a computed fact about a dedup rule that was
  itself chosen (admission dedups on token identity, Unit 06). Under a rule
  that admitted a token twice as two data, they would not converge.

## Student exercise

Reading F's history admits ⟨⟩ *after* its supply. Write a third history,
"F-first", that admits ⟨⟩ before any supply, and say whether it reaches the
same regime as F. Then say whether the question "is ⟨⟩ admitted?" is
affected.

## Answer

```python
F_FIRST = (AdmitDatum("<>"), Supply("<>"), Supply("<a>"), Supply("<a>"),
           Supply("<ab>"), AdmitDatum("<a>"), AdmitDatum("<ab>"))
replay(F_FIRST) == replay(GENESIS_F)   # True
```

Supplies change nothing (Unit 03), so moving an admission across a supply
changes nothing, and F-first reaches the same ledger as F. The question is
not affected: F-first is still reading F, since it admits ⟨⟩. Moving the
supply does not touch whether the admission happens. (In Genesis's own
model, `supply` must come first: the seed presents ⟨⟩ before anything. So
F-first is not a history Genesis records; it is a check that order among
supplies is irrelevant to the admitted state, which is the content of
`Bridge.order_erased_at_object_level`, Unit 11.)

## Verification

| Item | Where |
|---|---|
| The two readings | `paper/paper.md` §5 (Challenge 1, **[unresolved → resolved by convergence]** for ⟨A⟩) and §6; `code/derivation/engine.py` lines 1-13 (classification), 64-106 (`GENESIS_L`, `GENESIS_F`, `READING_L`, `READING_F`) |
| Seed text | `prompt/seed_prompt.md` §1 ("The only initial object-language inscription is: `<>`"), Challenge 1 ("supplies"), Challenge 2 ("supplies and retains") |
| Lean | `lean4/Derivation/Inertia.lean` lines 57-73; `R2L`, `R2F` in `lean4/Derivation/Basic.lean` |
| Axiom report | `artifacts/lean_axioms.txt`: `historyL_replays`, `historyF_replays` each `[propext]` |
| Ledger | `paper/paper_claim_ledger.md`, `CL-1-SUPPLY-NOT-ADMISSION`, `CL-1-READING-CONVERGENCE`, `CL-2-COLLAPSED` |
| Artifact | `artifacts/challenges.json`, `challenge1.sub_readings` and `sub_readings_converge_at_challenge2: true` |
| Check (Python) | `python textbook/checks/u05_two_readings.py`: L data `('<a>', '<ab>')`, F data `('<>', '<a>', '<ab>')`; demands `(0, 1)` and `(1, 2)`; `Impose(1, 2)` in L raises `AdmissionError`; sub-readings converge to `('<a>', '<ab>')`; artifact flag true; L ≠ F |
| Check (book Lean) | `python textbook/checks/u05_lean.py`: seven book theorems plus the two Genesis theorems kernel-checked, Lean 4.33.0; axiom reports none, none, propext, propext, both, both, both, propext, propext |
