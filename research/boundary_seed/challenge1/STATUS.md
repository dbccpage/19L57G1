# Challenge 1 — status

`AuthorityEffect: None`.  Session of 2026-09-04, branch
`research/boundary-run`, opened from main at `7d2e6e86` with Challenge 0
in its repaired state (53 tests, line and branch 100%, 20 Lean reports).

## Order of the work, as committed

1. `152ed096` `challenge1/PREDICTIONS.md` frozen, sha256
   `7cf17e56fffb4e45d4100750010265582fa921fabeed7fb1b84aa798f6e56dc7`,
   before any Challenge 1 code or proof existed in the working tree.  The
   existing `challenge*/PREDICTIONS.md -text` attribute already covered it
   (`git check-attr` reports `text: unset`), so no attributes change was
   needed.
2. This rung's commit: presentation layer, kernel extensions, Lean,
   receipt, tests, prose, registration, and injections.  Its id is in the
   session's final report; it is the commit that adds this file.

This history proves “committed before” only.  It cannot prove when any
untracked or off-tree code or proof was written.

## Provenance ceiling

Inherited unchanged: `SOURCE_ISOLATED_WITH_DECLARED_PRIOR_EXPOSURE`.  The
session that closed this rung read nothing outside the write root, the
seed, and the contract sections the harness loads, but it is an instrument
of the same kind as the one that declared prior exposure, and the notes
below record where a remembered shape was used.

## Results

Inscription `<a|>`, supplied after the close of Challenge 0.  Receipt
`receipts/challenge1.json`; full tables in `paper.md` section 5.

| | reading U | reading O |
|---|---|---|
| the supply of `<a|>` | presentation only: regime equals genesis, no judgment changes (PROVED) | same (PROVED) |
| a new admitted state | only through the separate admission event, refused without the prior supply (DEFINITION); the admitted mark's judgment survives every later event of the grammar (PROVED) | same |
| new holding judgments after admission | exactly one, `OnSide(0, s)`; the other side's does not hold; no name judgment (PROVED) | exactly one, `OnSide(0, s)`; the two name judgments hold as at genesis (PROVED) |
| the mark's profile | its side, nothing else (DEFINITION) | same |
| the two sides after one mark | profiles differ (PROVED); the sides went from collapsed to distinct by the admission alone | profiles differ (PROVED); the sides were already distinct by name |
| the two candidate regimes (`a` on side 0, on side 1) | unequal, each the other's reflection, related by the permitted reflection: one class (PROVED, COMPUTED) | unequal, each the other's reflection, related by no permitted renaming: two classes (PROVED, COMPUTED) |
| “which side” as an internal fact | not one: no permitted-renaming-invariant judgment of the bounded domain separates the candidates (PROVED, COMPUTED) | one: `OnSide(0, s)` separates them and every renaming is the identity at one mark (PROVED, COMPUTED) |
| the presentation convention (left is side 0) | invisible up to the permitted reflection | visible; the other convention's regime is the reflection of the designated one (PROVED) and is retained as a branch |
| designated current state | `a` on side 0, by the declared convention, not by proof | same, with the side-1 candidate retained |
| an event follows from the state | none (PROVED) | none (PROVED) |
| initial datum and reading | unchanged by every event (PROVED) | same |
| new event kind or judgment form needed | none | none |

Boundary dependence: the supply's inertia, the admission discipline, the
invariance of the initial datum and reading, and the empty event-follows
relation do not require the admitted boundary.  The one new judgment, the
profiles, the two candidates, the convention, and the class counts require
it and are not formulated after removing it.

What the challenge exercises, by the seed's list: supply (yes, the
`Supply` event of the read whole's mark); mention (yes, the token is named
by the supply and by every candidate admission, and a mention is not an
event); admission (examined: applied only inside certified candidate
histories, never by the supply); current-state designation (yes, by the
declared convention); retention (probed by hypothetical later events, none
admitted); observation (yes, one new `OnSide` judgment); side (yes, the
presented side mapped by convention); equality (yes, structural, and
distinct from the isomorphism relation).

## Predictions scored

| id | label | status | note |
|---|---|---|---|
| C0-X | NOT FORCED | HIT | U half: genesis collapsed, the admitted regime not, with one supply and one admission and no new form; O half: sides distinct before and after, the only new holding judgment is the mark's own side |
| C1-1 | FORCED | HIT | supply leaves the regime and every judgment unchanged |
| C1-2 | FORCED | HIT | unsupplied admission refused; the admitted mark's judgment survives supplies, re-designation, and a hypothetical second admission |
| C1-3 | FORCED | HIT | exactly one new judgment; other side false; names unchanged; supply adds none |
| C1-4 | FORCED | HIT | U profiles differ; one class; no permitted-renaming-invariant judgment separates the candidates |
| C1-5 | NOT FORCED | HIT | a convention was declared; two O classes; the other candidate is the reflection and is retained |
| C1-6 | FORCED | HIT | empty event-follows relation; datum and reading unchanged; no new form |
| C1-7 | NOT FORCED | HIT on its mechanical part | one initial datum and one mark in every certified regime; the modelling clause can only be falsified by a later challenge; whole-as-datum is OPEN for Challenge 5 |
| C1-X | NOT FORCED | PENDING | scored by Challenge 2 |

Seven of seven scored predictions hit, and C0-X hit in both halves.  Five
of the seven were labelled FORCED in the frozen file, and every FORCED
hit follows from Challenge 0's definitions plus the admission event that
Challenge 0 already declared.  The two NOT FORCED hits are about
decisions the run made (declare a convention; one boundary), not about
facts the run discovered.  Git history establishes that the prediction
file was committed before this rung's code and proofs; it establishes
nothing about off-tree work and is not evidence of insight.

## Where the run reached for a remembered result (declared reading 0)

- The shape of the answer to the seed's “presentation, admitted state, or
  observable distinction” question — presentation by one event, state by
  a separate event, distinction only after it — is the shape the
  instrument remembers from the sealed derivation's treatment of its own
  first supply.  The facts were computed and proved here; the framing was
  not re-derived.
- The presentation reader and the “left is side 0” convention were
  written from the instrument's habit of separating presentation from
  admission.  The convention's O-visibility and U-invisibility, and that
  the other convention's tower is the reflection of this one, were derived
  here first and were not remembered.
- The retention probes and the per-module generator census were written
  from the discipline the repository contract states, not from a
  remembered result.
- Nothing in the separating-judgment computation, the isomorphism
  witness, or the reflection-commutation theorems was remembered.

## Leftovers, for Challenge 2 and later

- Score C1-X: whether Challenge 2 admits two internal identities for the
  two wholes despite the shared glyph, and what the boundary alone
  distinguishes under each reading.
- `Supply` carries the token only; the presented side is metatheoretic and
  is consumed by the convention at admission.  Challenge 2 must say
  whether `<a|>` and `<|a>` are two presentations or one presented twice,
  and must not let the Challenge 0 token-uniqueness rule turn the second
  whole into a designation of the first mark silently.
- The reader is bounded to one mark and one bar by declaration; Challenge
  2 extends the bound deliberately, and Challenge 5 must revisit nesting.
- Whether a whole on a side is a datum (C1-7's modelling clause) is OPEN
  until Challenge 5 asks it.
- The Lean isomorphism relation `oneMarkRelated` is sufficient at one
  mark only; the general relation with mark permutations is Python, cross-
  checked against the canonical key to three marks, with no unbounded
  theorem.
- Challenge 0's leftovers survive: no Lean statement of the equal-count
  law or the class-count closed forms; no unbounded canonical-key theorem;
  the O names have now been proved never to change but nothing yet makes
  them earn their keep beyond separating the two one-mark candidates.
- The freeze manifest protocol remains OPEN as recorded at Challenge 0.

## Repairs and live failures during the challenge

Recorded in `change_log.md` and as rows in `MANUAL.md`:

- The Challenge 0 generator census fired on the new candidate enumerator
  while it lived in the kernel.  The enumerator moved to the metatheory
  module and the census is now reported per module; the kernel reports
  none.
- The no-timestamp scan matched the substring `date` inside `candidates`;
  it now matches whole words.
- The first `lake build` did not elaborate `Challenge1.lean` because
  nothing imported it; the root now imports it, and `verify_lean.py` fails
  on any module under `lean/BoundarySeed/` outside the root's import
  closure, proved by injection.
- Five Lean proofs first failed because `simp only [replay, List.foldl]`
  unfolded past the induction hypothesis; they now step by a definitional
  `show`.  A drafting placeholder theorem was removed before the build.

## Gates run in this session

| gate | result |
|---|---|
| `verify_pins.py` | `pins ok: seed ba30bcd600d8 and 2 frozen prediction file(s)` |
| `unittest discover -s tests` | `Ran 97 tests`, OK |
| `mypy` (strict, tree pyproject) | `Success: no issues found in 17 source files` |
| `coverage` + `check_coverage.py` | `line 100.00% branch 100.00% over 5 files` |
| `run_challenge0.py`, `run_challenge1.py` | both receipts byte-identical on rerun; `git diff --exit-code -- receipts` clean |
| `verify_lean.py` | `lean ok: 49 axiom reports within ['Quot.sound', 'propext'], matching lean/axioms.txt` |
| `ci/check_prose_watchlist.py` | `prose watchlist clean: 49 watched terms, 130 files with pinned hits, 1826 hits, census matches its pin`; no regeneration |
| `tests/test_primitive_contact.py` | `............s...  [100%]`: 15 passed, 1 skipped |
| `ci/check_paper_citations.py` | `paper cross-references resolve: 62 citation(s) across 29 document(s)` |
| injections | five gates proved, three live failures recorded (`MANUAL.md`) |

## Next session

Open Challenge 2 fresh: read the handoff, the seed, `PLAN.md`,
`MANUAL.md`, and this file; write and commit
`challenge2/PREDICTIONS.md` with its own extrapolation before any code;
extend the reader's bound to two wholes deliberately; decide how the
shared glyph relates to internal identity and say who pays; score C1-X.
The designated current state under each reading is `a` on side 0 by the
declared convention, with the side-1 candidate retained under O as the
reflection of it.
