# Setting translation: a primitive-difference setting as a regime of the sealed grammar

AuthorityEffect: None.  Outside the sealed derivation; consumes it read-only.
Not registered in `.github/workflows/verify.yml`: its checks run locally
through `verify.py` (section 7).

**Result.** A finite setting of the primitive-difference signature — a
carrier `{0, …, n-1}`, decidable difference, retention and protection
stores, two designated endpoints and finitely many admitted operations — is
a regime of the sealed grammar, with no new primitive: every store is a
binary judgment form whose instances are the pairs it asserts, and every
admitted operation is a binary judgment form whose instances are its graph.
The encoding is well-formed and faithful instance by instance, and all nine
candidate readings of the setting (`W`, `A`, `Bs`, `Bc`, `Bl`, `C`, `D`,
`E`, `F`) are decided on it beside the designated pair, which the regime
does not carry.  Reading `E` — no admitted composite identifies the
endpoints — is exactly "no chain of operation-form instances runs the
endpoints together", and a chain longer than `n * n` revisits a pair of
positions, so the criterion is decidable.  This closes the item PR #149
listed under *Not claimed*: "a translation of a setting's operations,
retention or protection into the sealed grammar".

What the translation shows about the readings: the declared separability of
a binary regime is *internal visibility* — some form's self-instance, row or
column differs at the two data — and so a witnessed pair with no
self-instance (`A`) is always internal, by the row context at the second
endpoint, while a bare witness (`W`) can leave the pair collapsed.  In the
sealed universe of 56 088 settings, every one of the 2 352 `A` settings has
an internal pair and 66 `W` settings do not.  At an internal pair the sealed
engine has nothing to do.  At a collapsed pair every absent link and every
absent self-instance on any form is a minimum response; on the two-point
setting with no assertion the self-instance and the link on the difference
form are two of them.

Lean: 144 authored theorems, 173 reports with the compiler-generated ones,
all within `{propext, Quot.sound}`, in a package importing the sealed
package and the merged `local_reuse` and `magnification` packages.  Python:
the translation, the nine readings and the visibility criterion checked
against the sealed evaluators on every setting of the sealed universe, the
42 sealed verdicts resolved against both Lean sources, the sealed engine
restarted from the sealed concrete settings and six two-point exhibits, 52
tests, strict typing, a byte-identical record.  Execution base
`f12a498ea75899ea119df958d54209fee25819f1` (main); no sealed path is written.

## 1. The translation (`lean/Translation.lean`)

| definition | content |
|---|---|
| `FiniteSetting` | carrier size `n`, three boolean-valued stores `rel`, `ret`, `prot`, endpoints `a`, `b` below `n`, a list of operations closed on the carrier |
| `toSetting` | the sealed `PrimitiveCore.Setting` it presents: carrier `Fin n`, stores read as `= true`, the operation family lifted to the carrier |
| `encode` | the regime: `n` data; forms `[2, 2, 2]` then one binary form per operation; instances `storeInsts` for the three stores and `graphsFrom` for the operation graphs; no rule, no requirement |
| `encode_wf` | the encoding is well-formed |
| `derivable_rel`, `derivable_ret`, `derivable_prot` | `(f, [x, y])` is derivable exactly when store `f` asserts `(x, y)`, for admitted `x`, `y` |
| `derivable_op` | `(3 + k, [x, y])` is derivable exactly when `y` is the `k`-th operation's value at `x` |
| `Witnessed`, `NoSelf`, `Symmetric`, `Splitting`, `Retained`, `Protected` | decidable statements about derivable instances of the encoding at the designated pair |
| `W_iff`, `A_iff`, `Bs_iff`, `Bc_iff`, `Bl_iff`, `C_iff`, `D_iff`, `F_iff` | each reading of the presented setting is the corresponding statement on the encoding beside the pair; `D_iff` is endpoint inequality; `Bl` is `A` because a finite setting is located (the sealed `located_of_decidable`, which needs the decidable stores) |

The stores of the signature are forms even when empty: the encoding presents
the signature, not a chosen subset of it, and an empty retention form is
available to responses (section 4).  Protection in particular is presented
as data and not enforced: the engine's demand at the designated pair is the
seed imposition, made whether or not the pair is protected, and no other
protected pair is ever imposed.  An encoding that places the protected pairs
into the regime's requirements instead would be a different family.

## 2. Operations as forms, and reading E (`lean/Chains.lean`)

Following the `k`-th operation form from `x` means taking the unique `y`
with `(3 + k, [x, y])` derivable (`follow_derivable`, `follow_unique`); a word
of operation indices runs by following its forms in order (`run`).

| theorem | content |
|---|---|
| `word_in_clos` | every word runs as a member of the closure of the admitted family |
| `clos_word` | every member of the closure (the sealed `PrimDiff.Clos`: base, identity, composition) runs some word |
| `E_iff` | reading `E` is exactly: no word over the operation forms runs the endpoints to the same datum |
| `cut`, `shorten` | a word longer than `n * n` that identifies the endpoints revisits a coded pair of positions (the sealed `CapacityBound.encode` for the code, `Pigeonhole.pigeonhole` for the collision) and shortens |
| `bounded_shorten`, `noChain_iff` | words of length at most `n * n` suffice |
| `E_iff_noChain` | reading `E` is the decidable criterion `NoChain` |

Computed: the bounded criterion (`translation.no_chain`, exponential in the
operation count — it is the theorem's literal shape, not the readings path)
agrees with the unbounded one decided by reachability over pairs of
positions (`no_chain_reach`, which `readings` uses) and with the sealed
closure-of-tables evaluator on every setting of the universe.

## 3. When a difference is internal (`lean/Visible.lean`)

For a regime whose forms are all binary, a well-formed context has one of
three shapes — both slots holes, a hole beside an admitted datum on the
right, or on the left (`wfCtx_binary`).  Hence, for binary regimes:

| theorem | content |
|---|---|
| `separable_iff_visible` | the declared separability is `Visible`: some form's self-instance, row or column differs at the two data — a decidable statement |
| `collapsed_iff_not_visible` | collapse is the negation |
| `visible_iff_rows_columns` | for admitted data the self-instance clause is never the only witness: when the self-instances differ, the row at the second datum or the column at the first differs too |
| `A_separable`, `A_separable_rev` | a witnessed pair with no self-instance is internal, in either order: the row context at the second endpoint sees the link present and the second self-instance absent |
| `witness_alone_invisible` | the constant relation on two points with empty stores and no operation asserts the pair and leaves it collapsed |
| `selfOnly_visible`, `linkOnly_visible`, `selfAndLink_visible`, `bothLinks_visible`, `everyPair_collapsed`, `noPair_collapsed` | the six two-point exhibits, decided |

In the native words of the derivation, and for binary regimes only: two
data are internally separable exactly when some form — a store or an
operation graph — treats them differently in a self-instance, a row or a
column.  When every form treats the pair alike the difference is external:
it exists only as the imposed requirement.  The self-instance (`(f, [a, a])`)
and the link (`(f, [a, b])`) are the two instance shapes a binary form
offers, and the criterion says which of their presences and absences make
the pair internal.  The self-instance clause stays in the definition because
the equivalence with the sealed `separable` holds without any admittedness
hypothesis; its redundancy needs the two data admitted.  A state the seed's
own mark response reaches carries a unary form and is outside the criterion.

Computed over the sealed universe (56 088 settings: 24 on one point, 768 on
two, 55 296 on three): visibility equals the sealed collapse verdict on
every pair of every encoding, and its row-column form equals it too.  Of the
37 248 settings with distinct endpoints, 37 116 have an internal pair and
132 a collapsed one; per reading, every setting satisfying `A` (2 352,
the theorem `A_separable`) has an internal pair, while `W` holds at 66
collapsed pairs, `D` at all 132 and `E` at 100.  The universe also shows no
collapsed `C` pair, but that is an artifact of its decoration of protection
(empty, or exactly the designated pair, which the protection form then
exhibits): the 66 `C` settings that are internal only through the
protection form are the 66 collapsed `W` pairs, and no theorem says `C`
makes a pair internal.  Irreducibility and visibility are different notions
in both directions: an admitted merger can make a pair visible by its own
graph (`boolEmptyMerged`: `E` fails, the pair is internal), and the empty
relation with no operations is irreducible with a collapsed pair
(`boolEmpty`).

## 4. The engine at an encoded pair

| theorem | content |
|---|---|
| `encode_good` | the encoding satisfies the merged invariant `Good` |
| `seed_embeds` | at the encoded pair of a setting with distinct endpoints, the mark, the link and the self-instance on a fresh form are valid responses (the merged `bare_round_embeds`) |
| `A_no_fire` | at a witnessed irreflexive pair the engine has no seed firing, whichever endpoint it orders first: the pair is already separable |
| `link_valid`, `self_valid` | at a collapsed pair of a binary regime with no standing requirement, an absent link and an absent self-instance on any form are valid responses |
| `one_inst_min`, `link_min`, `self_min`, `encode_link_min`, `encode_self_min` | a valid one-instance response at a collapsed pair is a minimum under both measures; so every absent link and self-instance is |
| `noPair_fires_self`, `noPair_fires_link`, `noPair_rooted_self`, `noPair_rooted_link` | on the two-point setting with no assertion, the self-instance and the link on the difference form are each a minimum response and a rooted seed step |
| `everyPair_fires` | on the constant relation, a self-instance on the empty retention form is a minimum response |

The scope of the minima: an absent instance is needed.  The setting with
all three stores complete on two points is collapsed at its pair and has no
one-instance response; the sealed `min_responses` returns two-item minima
there (`tests/test_translation.py`).

Computed (`translation.restart`, the sealed `build_tree` certified by the
sealed `verify_full_export`): from the encoding of each of the eleven sealed
concrete settings with distinct endpoints and of the six two-point exhibits,
under both measures.  At every visible pair the root round's minimum is the
empty response and the closed run ends at once with every pair separated.
At the collapsed pairs (`boolEmpty`, `everyPair`, `noPair`) the root round
has exactly two classes at one item — the self-instance class and the link
class, the two instance shapes of section 3; that these are *all* the
minima is computed, not proved.  The receipt (`run.py`) refuses to record a
restart whose root round says otherwise.  The sealed role census names the
empty response with an empty string, a shape the sealed engine never
reached before; the record keeps node counts and statuses instead.

## 5. The sealed settings transcribed (`lean/Transcription.lean`)

The thirteen sealed concrete settings on `Unit`, `Bool` and `Fin 3` are
transcribed as finite settings (`Transcription.unitBare` …
`boolEmptyMerged`; `false = 0`, `true = 1`, the merger as the constant
operation to `0`), and each of the 42 sealed verdicts is re-proved on the
transcription by deciding the reading's regime-level form through the
`*_iff` theorems, under the sealed theorem's own name.  The Python table
`SEALED_VERDICTS` is resolved by setting, reading, sign and theorem name
against both Lean sources (`translation.verdict_sources`), so a row that no
theorem states is a failure.  Not proved: an isomorphism of settings between
a sealed setting and its transcription.

## 6. The answer to the OPEN item

PR #149 left "a translation of a setting's operations, retention or
protection into the sealed grammar" unclaimed.  It exists for every finite
setting: retention and protection are binary forms, an operation is a binary
form carrying its graph, and the closure of the admitted family is the set of
chains along those forms.  Every reading is decided on the translation
beside the designated pair, `E` by the chain criterion.  The three
hypotheses the theorems carry — a finite carrier, decidable stores and
finitely many operations — are the scope; nothing is claimed beyond it.

## 7. Evidence

**Lean** (`lean/`, `evidence/lean.json`): 144 authored theorems and 29
compiler-generated ones, 173 reports, all within `{propext, Quot.sound}`;
`Translation` 49, `Chains` 24, `Visible` 50, `Transcription` 50; the report
population equals the environment census of the four namespaces in both
directions; no private theorem; forbidden-token scan clean.  The list
lemmas `getD_mem`, `getD_of_all_two` read the core and the sealed
`Attachment.getD_lt`; the position-pair code of `Chains` is the sealed
`CapacityBound.encode` and its bound and injectivity are the sealed
`encode_lt`, `encode_inj`; the three stores are one recursion
(`storesFrom`, `derivable_store`) and the three context shapes one
equivalence (`wfCtx_binary`); the context and word enumerations
(`two_slots`, `words`) are local instances of the general enumerations
the merged ignition family carries, which is not a dependency here.

**Python** (`translation.py`, `run.py`, `evidence/census.json`, `tests/`):
52 tests, strict typing over nine files, the record replays byte-identically
(about twenty-five seconds; the suite walks the sealed universe once in its
own pass and once in the record replay).  `verify.py`, `verify_sources.py`,
`verify_lean.py`, `run.py`, the three custody, gate and record test files
and `lean/Inventory.lean` follow the merged `research/magnification` files
with names and refusals changed; there is no shared helper across the
research trees, so a repair to one copy must be carried to the others.

**Negative cases** (`tests/test_translation.py`, `tests/test_evidence.py`),
one per check: an extra instance or a rule is not faithful; a wrong entry in
the verdict table, a wrong theorem name or reading letter, a row naming no
setting, and a mis-transcribed sealed setting are each named; an unfaithful
encoding of a full-store setting is a failure; a unary form is refused by
the visibility criterion; a tampered restart export is refused by the sealed
certification; a two-step chain is found where a one-step chain is absent;
the minima at the two-point pair with no assertion are exactly the twelve
absent instances, at a visible pair the sealed `min_responses` returns the
empty response alone, and with every instance present it returns two items;
the record's `--check` refuses a changed figure; and the receipt refuses,
by name, an unfaithful setting, an unreproduced verdict, a visibility
verdict against the sealed collapse verdict, a visible pair with a
non-empty root round and a collapsed pair without the two one-item classes.

**Injection record** (this family's own gates; each reversed, no record
regenerated while live):

| gate | injection | observed failure | reversed |
|---|---|---|---|
| custody census | untracked `ZzzProbe.lean` in `research/magnification/lean` | `FAIL: SOURCE_CENSUS: research/magnification/lean: missing=[] unexpected=['research/magnification/lean/ZzzProbe.lean']` | PASS |
| custody pin | one line appended to `code/derivation/primitive_core.py` | `FAIL: SOURCE_CHANGED: code/derivation/primitive_core.py` and `FAIL: CONSUMED_TRACKED_DIFF: …` | PASS |
| census record | `distinct_endpoints_collapsed` lowered by one | `FAIL: evidence/census.json differs from fresh computation` | PASS |
| Lean report census | the `#print axioms` line of `Chains.shorten` removed | `FAIL: report/census mismatch: missing=['Chains.shorten'], extra=[]` | PASS |
| Lean forbidden token | the first forbidden token in a comment of `Visible.lean` | `FAIL: forbidden source token: Visible.lean` | PASS |
| Lean record | one report's axioms edited in `evidence/lean.json` | `FAIL: evidence/lean.json differs from fresh compilation` | PASS |
| verdict transcription | `d2Bare` transcribed with the symmetric relation | `failures: [{'setting': 'd2Bare', 'theorem': 'd2Bare_not_bs'}]` | PASS |
| visibility criterion, column clause | the column test deleted from `translation.visible_rows_columns` | 6 168 universe failures (1 536 against the sealed collapse verdict, 4 632 against the three-clause form), the first naming the two-point setting with one merger at pair `(0, 1)` | PASS |
| visibility criterion, self-instance clause | the self-instance test deleted from the computed criterion | **no failure over all 56 088 settings.** The clause is redundant for admitted data in general, not only there: `Visible.visible_iff_rows_columns` was proved from this observation, and `translation.visible_rows_columns` now cross-checks it on every pair | n/a |

**Custody** (`verify_sources.py`, `SOURCE_MANIFEST.json`): at
`0bb7fe5ecc16da8b6ee7c5e94df933eae7b65779` (re-baselined 2026-09-08 from
`f12a498e` when the magnification package took the ignition family as a
dependency), the eight derivation modules by digest and runtime origin, the
sealed `lean4/Derivation` tree and the `research/local_reuse/lean`,
`research/ignition/lean` and `research/magnification/lean` trees by Git
tree object, the four Lean configurations by digest; an untracked `.py` on
the import path or `.lean` in any of the four Lean trees is refused.  No
export is read.  The runtime census reads the whole interpreter, so the
family's checks run in their own interpreter, as `verify.py` runs them.

**Author-recorded regression gates at the execution base `f12a498e`, with
the family staged**: (1) prompt hashes ok; (2) transport citations clean, 190
verified; (3) the full sealed suite under coverage, exit 0, line 99.10 %,
branch 96.71 % (four workers); (4) mypy clean over 60 files; (5) artifacts
reproducible, 40 JSON byte-identical and 6 full exports content-identical;
(6) Lean audit clean on a fresh log, 77 sources, 1530 reports within the
whitelist, report pin matching; (7) 7 skills well formed; (8) 62 paper
cross-references resolve; (9) 1152 ledger evidence tokens resolve; (10)
parked audit complete, 75 modules, 12 parked; (11) the portable-interface,
blind-restart and partial-Decide checks pass at `f12a498e`, and the four
registered trees' tests and strict typing pass, while the primitive-difference
manifest check fails with `FAIL: commits since the source snapshot touched a
protected path`, naming five commits (the merge of PR #148 and the review
repairs) that are all ancestors of the execution base — a red already on
`main`, not caused by this family, and repinning that manifest is the
author's act, not done here; (12) prose watchlist clean with no pin
regenerated, 49 terms, 130 files, 1826 hits; the identifier firewall passes
over the index.  Unavailable: hosted CI.  Pre-existing failures observed: the
one named under (11).

## Not claimed

* Anything about infinite carriers, undecidable stores or infinite operation
  families: every theorem is about `FiniteSetting`.
* An isomorphism of settings between the sealed `Unit`, `Bool` and `Fin 3`
  settings and their transcriptions: the transcriptions carry the 42
  verdicts as Lean theorems and agree with the sealed Python evaluator; the
  carriers are not matched in Lean.
* That the Python mirror computes the Lean predicates: the agreement is
  exhaustive over the sealed universe, which reaches three points, two
  decoration choices per store and three operation choices, plus the three
  full-store sealed settings.
* Anything about the engine's later rounds from an encoded setting, or that
  the two one-item classes are all the minima at a collapsed pair.
* Any reading of the two instance shapes beyond what the theorems state.
* That protection is enforced by the engine: it is presented as a form.

## Files and running

| file | role |
|---|---|
| `lean/Translation.lean` | the finite setting, the encoding, faithfulness, eight readings |
| `lean/Chains.lean` | operations as forms, reading E, the bound |
| `lean/Visible.lean` | the visibility criterion, the exhibits, the engine at an encoded pair, the absent-instance minima |
| `lean/Transcription.lean` | the thirteen sealed settings transcribed, their 42 verdicts decided |
| `lean/Inventory.lean` | the environment census |
| `translation.py`, `run.py`, `evidence/census.json` | the translation, the census over the sealed universe, the verdict sources, the restarts, and the record with its semantic refusals |
| `verify_lean.py`, `evidence/lean.json` | the Lean build, two-way census and reliance record |
| `verify_sources.py`, `SOURCE_MANIFEST.json` | custody of the consumed inputs |
| `verify.py` | every check in order |
| `tests/` | 52 tests: the translation, the negative cases, custody, the parser, the record |
| `CLAIMS.md` | one `CL-ST-*` entry per claim |

```powershell
cd research/setting_translation
python verify.py     # sources, tests, mypy, lean (lake build + census), census --check
```

Regenerate the two records deliberately and never under a live injection:
`python run.py --write`, `python verify_lean.py --write`.
