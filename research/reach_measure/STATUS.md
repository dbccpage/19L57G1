# reach_measure: a base-relative cost, and the prediction it broke

`AuthorityEffect: None.`

The sealed measures read the response and nothing else. `mu1` is the item
count; `mu2` refines it by new-form arity sum. A single instance and a
single uniform rule are both one item of zero new-form arity, so both cost
`mu1 = 1` and `mu2 = (1, 0)`. An optimizer running on either cannot tell
"adjust these two" from "abolish the distinction for everyone."

This rung declares a third measure that reads the state:

    REACH(base, delta) = the number of pluggings that become derivable.

Nothing is weighted by hand. `mu3 = (reach, item count)`, lexicographic,
reach leading.

## Frozen inputs, and an amendment recorded rather than hidden

Native `PROMPT.md` and `PREDICTIONS.md` were frozen before either side ran.
`PREDICTIONS.md` says so in its own chronology section: `reach.py` existed,
neither side module did, the Lean package did not, and no value in the file
had been computed.

**Both frozen files were then amended after the run**, and the amendment is
recorded here because it is a real breach of the freeze, small as it is.
The frozen text carried a noun on the repository's prose watchlist, and the
census gate refuses it. One line in each file changed:

| file | pre-amendment sha256 | post-amendment sha256 |
|---|---|---|
| `PREDICTIONS.md` | `502f22e8e0eac...c3aa11c1cfe` | `b589787ccb3bb...bcfcba0a7f78c` |
| `PROMPT.md` | `4ac1c9ba74000...11bc064dccc9a1` | `240e7ed70e761...8ac8f6ed486b6175c5` |

The claim that the amendment was vocabulary only is **checked, not
asserted**. `SOURCE_MANIFEST.json` declares each amendment as an exact
substitution, and `verify_pins.py` undoes that substitution on the amended
bytes and requires the result to hash to the pre-amendment digest. A repair
that also quietly moved a value cannot survive that check, and the injection
record below shows it does not: tampering with a prediction and re-recording
every digest to match still fails, because the pre-amendment digest is an
anchor the tamperer does not hold the text for.

Sources pinned at snapshot `7fcd72f618e676a88df65efed4926ac3c11eacbe` of
`main`: nine blobs and one span. **No reconstructions.** The Python side
imports the pinned sealed modules and the pinned dual module as libraries
and re-prices their output; the Lean side restates the sealed item grammar
in miniature because the theorem is about the FORM of a base-free measure
and needs no enumerator. `SOURCE_MANIFEST.json` declares that absence rather
than leaving a reader to infer it.

## Declared readings

1. **Reading R on the dual side.** The dual tree's identification demands
   are asked at its pinned genesis states. Those states stand under the
   sealed separations, and with the separations standing no demand has a
   response at all. This tree therefore applies the dual tree's own pinned
   `Retract()` event rather than editing a state by hand, and prices what
   follows. Reading P — separations left standing — was run too, and returns
   *no response* at every root, which is the dual tree's own P6 finding
   reached from a second code path. R is declared; P is recorded.
2. **Reach counts pluggings, not items.** A plugging is the estate's own
   unit of observable content: a context filled by a datum, derivable or
   not. A datum's profile is exactly the set of contexts derivable for it,
   so total profile size is the state's observable content and reach is its
   growth. Nothing here invents a weight.
3. **The valid set is never widened.** `minima_under` takes a candidate list
   rather than enumerating. The sealed and dual enumerators remain the
   authority on validity; this tree re-prices what they accepted. `FW-VALID`
   holds by construction, not by inspection.
4. **The rectangle is 19 pinned genesis states and one sealed challenge.**
   Every count below carries that scope. These are not the states.

## Terminals, each with its scope

- **BLINDNESS_PROVED** (PROVED_THEOREM). `base_free_is_blind`: for any
  target type and any `G : List Item → β`, if `G` gives equal cost to
  responses of equal `mu2`, then `G` gives the single instance and the
  single uniform rule the same cost. `of_mu2_is_blind` states it for a
  measure presented as a function of the sealed pair, which is the shape
  `mu1` and `mu2` actually have. The result is about the **form** of a
  base-free measure, not about these two measures in particular: no
  re-weighting, no tie-break, no lexicographic extension escapes it.
  `separating_is_not_base_free` is the useful direction — a measure that
  does separate them provably does not factor through the sealed pair, so
  it must read something else. Reading the base is one choice, but a
  base-free syntax-sensitive measure is another; the theorem does not force
  base dependence. `gap_unbounded` concerns a separately declared abstract
  fresh-plugging model: for every `k` its rule value exceeds its instance
  value by more than `k` at some size. It is not a correspondence theorem
  for Python `reach`, which counts only newly derivable pluggings. 10
  `#print axioms` reports, 3 axiom-free, the rest within `{propext}`;
  nothing near `Quot.sound` is used.
- **MEASURE_SEPARATES** (COMPUTATION, scope: the pinned rectangle). On the
  dual side, 51 demands, all answered. `mu1` leaves 24 of them tied across
  two item kinds — a tie in which the measure cannot say whether the cheapest
  repair is local or global. `mu3` leaves 11. At 13 demands `mu3` selects
  the instance where `mu1` had tied it with the rule, and at 18 demands it
  narrows the tie set at all. Reach values run 1..20 over the rectangle.
- **MEASURE_DOES_NOT_SEPARATE** (COMPUTATION, scope: 3 named demands). The
  other pre-registered branch fires too, and it is the more interesting
  half. See the prediction record.
- **PARTITION_RECORDED** (COMPUTATION, scope: the pinned rectangle). Of the
  51 answered demands, **27 admit only rule responses**, 16 admit both
  kinds, and **0 admit only instances**. The asymmetry is the finding: at
  most demands of this rectangle a local repair is not available at the
  minimum item count, so the choice `mu3` exists to make does not arise
  there, and no measure could have made it. Where the choice does arise,
  `mu3` makes it at 13 of 16.
- **On the sealed side there is no choice to make** (COMPUTATION). R1
  predicted no uniform-rule item among the sealed Challenge-3 minima. What
  the run found is stronger: the sealed Challenge-3 base declares **no
  forms at all**, so a uniform-rule item is not merely non-minimal, it is
  not well-formed there. Every valid minimum response is `form+inst`. `mu1`
  minima 6 under reading L and 10 under reading F; `mu2` minima 2 under
  both; **`mu3` minima 2 under both, and `mu2` and `mu3` agree**. The
  sealed side carries no local-versus-global axis, exactly as predicted,
  and this rung's headline could not have come from there.
- **OPEN_AT_NAMED_TARGET**: the leftovers below, each priced.
- **OB1_UNCHANGED, S66_UNCHANGED, S9_LAST_UNCHANGED, NS95_GROWTH_UNCHANGED**:
  this rung touches none of the protected opens. A new measure is not a
  demand generator, proves nothing about the two paper items, and says
  nothing about the growth question of the arithmetic chain.
  `test_forbidden.py` fails the run on a claim to the contrary.
- **MANUAL_RECEIPT_DECLARED**: no CI gate reads this tree's pins, its Lean
  audit, or its scans. All three are manual receipts, as in the sibling
  trees, and the registration diff this tree does **not** apply is printed
  below.

## The prediction record

| # | prediction | disposition |
|---|---|---|
| R1 | no uniform-rule item among the sealed minima | **CONFIRMED, and more strongly than stated** — a rule is not well-formed at that base |
| R2 | no function of `mu1` and `mu2` separates local from global | **CONFIRMED** — `base_free_is_blind`, for arbitrary target type |
| R3 | reach is not a refinement of the item count; a searched pair inverts the two orders | **CONFIRMED** — on `g00`, two instances have reach 1 and one rule has reach 2, so `mu1` prefers the rule and `mu3` prefers the strictly larger response |
| R4 | *wherever* both kinds are valid, `mu3` strictly prefers the instance; predicted at a majority | **the universal clause MISSED at 3 of 16; the majority clause holds at 13 of 16** |
| R5 | the rule-alone minima split into re-selected and kept; sizes recorded, not predicted | **RECORDED** — 16 mixed, 27 rule-only, 0 instance-only |
| R6 | `mu3` never selects a response the enumerators rejected | **CONFIRMED** — by construction; `minima_under` cannot enumerate |
| R7 | reach is base-relative, exhibited | **CONFIRMED** — `rule(form 0)` has reach 1 on `g00` and 19 on `g13` while `mu1 = 1` and `mu2 = (1, 0)` on both |

### R4, the miss, with its value

The three demands where `mu3` does **not** prefer the instance:

| genesis | demand | reach values available | `mu1` kinds | `mu3` kinds |
|---|---|---|---|---|
| `g00` | `[1, 2]` | `[1]` | inst, rule | inst, rule |
| `g01` | `[1, 2]` | `[1]` | inst, rule | inst, rule |
| `g16` | `[0, 1]` | `[1]` | inst, rule | inst, rule |

At each of the three, the rule's reach is also **1**: its form has exactly
one plugging that was not already derivable, so applying it to everything
and applying it to the one thing are the same act. Reach prices them the
same because they *are* the same, and `mu3` keeps the tie.

The prediction was wrong in a specific way worth naming. It quantified over
the item **kind** — instance versus rule — and asserted a fact about
locality from it. That is exactly the move `PROMPT.md` had already refused
under `FW-SYNTAX`: *an item kind is not a locality claim; whether a response
is local is a fact about its effect on the base, not about which constructor
it uses.* The refusal was written before the run and the prediction violated
it anyway. The run enforced the refusal.

So the finding is sharper than the prediction would have been:

> **A uniform rule is not global by construction. It is global exactly when
> the base leaves it room to be, and reach measures the room.**

An optimizer that penalizes rule-shaped moves is doing syntax. An optimizer
that penalizes reach is doing the thing the syntax was a proxy for, and on
these three demands the proxy and the thing come apart.

## What this rung settles, and what it does not

It settles that no function of the sealed pair can distinguish the two
responses, whatever function you pick. It does not force base dependence:
a measure could instead inspect response syntax. The declared refusal of
syntax-as-locality is metatheoretic, not a consequence of the theorem. On
the pinned data, the chosen base-relative measure does distinguish the two,
and the two orders are not nested — reach can prefer strictly more items.
The run also settles the partition of the rectangle's demands into those
where the choice arises and those where it cannot.

It does **not** claim reach is the right measure, or better than the sealed
ones; `FW-BETTER` forbids that and nothing here says it. It does not claim
reach is the only base-relative measure, or canonical among them. The
monotonicity and fixed-instance theorems belong only to the abstract model;
actual Python reach can fall as data count rises and a single instance can
have reach zero. Above all this does not close the question of what an
optimizer should minimize: it shows the sealed measures cannot express the
question.

## A defect carried in, and repaired

`verify_lean.py` arrived from the sibling trees with the **substring**
forbidden-token scan and with **no source census**. Both are known defects
of that file in this estate: one sibling found the substring form flagging
a sealed identifier that merely contains a denylist token, and one found
that removing a `#print axioms` line removes its report too, so a
reported-against-listed diff cannot see a silent drop. Neither had bitten
here — this tree's Lean carries no colliding vocabulary and no dropped line
— but a gate that is dead only by luck is a dead gate. Repaired to word
boundaries and given a source census; both repairs are exercised in the
injection record.

The working-denylist scan of `test_forbidden.py` is **left in its strict
substring form**, because in this tree it passes, and the substring form is
the stronger check. That is a deliberate choice, recorded so the difference
between the two files is not read as an oversight.

## The injection record

| Gate | Injection | Observed failure |
|---|---|---|
| Amendment integrity, the load-bearing case | a prediction's wording changed from *a majority of the demands* to *every one of the demands*, **and every digest re-recorded to match** | plain freeze check passes; `FAIL: PREDICTIONS.md amendment 1 is not the declared substitution: undoing ... hashes 6ce2247a..., recorded pre-digest 502f22e8...`; exit 1, then 0 after reversal |
| Amendment integrity, plain case | the same wording change with digests left alone | four failures, naming the file hash, the post-digest, the substitution, and the chain end; exit 1, then 0 after reversal |
| Pin integrity | first digit of the pinned `code/derivation/observe.py` blob flipped in `SOURCE_MANIFEST.json` | `FAIL: code/derivation/observe.py blob at 7fcd72f6... is 2552c041..., pinned f552c041...`, once at the snapshot and once at `HEAD`; exit 1, then 0 after reversal |
| Span pin | the dual census span's first line moved from 47 to 48 | `FAIL: span research/identification_dual/STATUS.md:48-54 at 7fcd72f6... hashes 2b08ed76..., pinned 21ac0d55...`, at the snapshot and at `HEAD`; exit 1, then 0 after reversal |
| Lean forbidden token, word-boundary form | a comment carrying the first forbidden token appended to `Blindness.lean` | `FAIL: Blindness.lean contains forbidden token 'sorry'`; exit 1, then 0 after reversal |
| Axiom-report source census — the injection that did not fire in a sibling | one `#print axioms` line removed from `AxiomReport.lean` | `FAIL: ReachMeasure.ruleReach_monotone is declared in Blindness.lean but not listed in AxiomReport.lean`; exit 1, then 0 after reversal. Without the census this injection is invisible, because the removed line removes its own report |
| Census scan (FW-PIN, FW-NAME) | a probe file carrying a watched noun placed in the write root | `test_no_watched_prose_word_in_the_write_root` fails naming file, line and token; exit 1, then 0 after deletion |
| Census scan, real case | (found live, not injected) the frozen `PREDICTIONS.md` and `PROMPT.md` carried a watched noun | the gate fired on the frozen files; repaired by the recorded amendment above rather than by a suppression |
| Growth-sentence scan (FW-GROWTH), real case | (found live, not injected) a `Blindness.lean` docstring used a watched FW-GROWTH phrase about the gap | the scan named the file and the phrase; the docstring was reworded to *no constant bounds the gap*, the theorem `gap_unbounded` untouched. The scan cannot tell a quoted phrase from an asserted one, so this row does not quote it either |
| Validity widening (FW-VALID) | a hand-built response priced and offered as a minimum | not injectable: `minima_under` takes the enumerator's list and has no enumerator of its own, so the widening has no code path. Recorded as a structural refusal, not a passing test |

## Leftovers, named and priced, executed nowhere

1. **Reach on the sealed side has nothing to act on** — OPEN. The sealed
   Challenge-3 base has no forms, so the rectangle where reach matters and
   the rectangle the sealed derivation argues over do not overlap. Price: a
   sealed-side demand posed at a base that already carries a form, which is
   a different challenge and needs its own charter.
2. **Additivity of reach along composition** — OPEN, and the sharper of the
   two outcomes either way. If `reach(base, d ; e) = reach(base, d) +
   reach(apply(base, d), e)`, the measure is an action along a path of
   moves and a composite has a price rather than a re-measurement. If it
   fails, reach is not a cost in the usual sense and the failure is a
   result. Price: a composition operation on responses, which the sealed
   candidate grammar does not currently declare.
3. **The order type of `mu3`** — OPEN. Reach leads and the item count
   breaks its ties, which is a choice, not a derivation. Whether any other
   lexicographic order of the three coordinates gives a different selection
   on this rectangle is computable and not computed.
4. **Reach under isomorphism** — OPEN. Profile size should be invariant
   under the estate's renaming, so reach should be too, and this is a
   theorem-shaped statement the tree does not prove. Price: transport along
   the pinned `iso` module and a proof that `profiles` commutes with it.
5. **A base-relative measure that is not reach** — OPEN, named so it cannot
   be smuggled in later. `separating_is_not_base_free` says a separating
   measure must read something beyond the response. It does not say it must
   read the base, and it does not say reach is canonical among those that
   do.

## The registration diff this tree does NOT apply

    - name: reach_measure pins, Lean audit and scans
      run: |
        python research/reach_measure/verify_pins.py
        python research/reach_measure/verify_lean.py
        python -m unittest discover -s research/reach_measure -p "test_*.py"

## Commands (run from this directory unless noted)

| command | exit | key line |
|---|---|---|
| `python verify_pins.py` | 0 | `pins clean: 9 sources and 1 spans at snapshot and HEAD; sealed prefixes unchanged; nothing outside the write root; 0 source projections exact; native PROMPT.md frozen; 1 predictions freezes reconstructed; 2 declared amendments each exactly its substitution` |
| `python verify_lean.py` | 0 | `lean audit clean: 4 sources, 10 axiom reports (3 axiom-free), axioms within ['Quot.sound', 'propext'], 10 originating theorems all listed` |
| `python run_reach.py` | 0 | `dual side: 51 demands answered, 27 admit only rules, 13 re-selected` |
| `python -m unittest discover -s . -p "test_*.py"` | 0 | 22 tests, refusal scans and unit tests pass |
| `python -m mypy` | 0 | `Success: no issues found in 8 source files` (strict) |
| `python ci/check_prose_watchlist.py` (repository root) | 0 | clean without a repin |
