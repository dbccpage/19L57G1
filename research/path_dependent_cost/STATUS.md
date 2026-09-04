# path_dependent_cost: the price of a commitment is when you make it

`AuthorityEffect: None.`

The preceding rung proved that a cost of the form `P(apply s d) − P s`
telescopes: fixed by the endpoints, blind to the route, zero around every
closed walk, and therefore incapable of carrying an obstruction. It named
what was missing — a cost that is additive along composition, reads the
state, and is **not** of that form — and did not have one.

Here is one, and it has a reading rather than a construction:

> **`rule_span`.** A uniform rule is a commitment over *all* pluggings of
> its form. What that commitment ranges over is not a property of the rule.
> It is a property of the state the rule is made in. So price the rule by
> what it ranges over **at the moment it is made**: commit before the state
> grows and the commitment is narrow, commit after and the same commitment
> reaches further.

Two routes, same start, same finish:

| route | moves | total |
|---|---|---|
| commit early | rule (2), then datum (0) | **2** |
| commit late | datum (0), then rule (3) | **3** |

The end states are equal. The totals are not. So no state functional has
this cost as its difference — not merely no obvious one, but none, by
`not_exact_of_routes_differ`.

## Frozen inputs

Native `PROMPT.md` sha256
`ed3058124605431c7e133d9ab4b66192c0b1e6799182f08f510542f9b4090bb5`.
`PREDICTIONS.md` sha256
`3a6ef227a4f00566c5b0ed7d7f351339f5c65459529aec781af2f91b2477c018`, frozen
as one whole-file digest before any module of this tree existed and before
any move graph had been built — P3, that two routes exist at all, was a
prediction about the sealed grammar and not a report of one.

The chronology section records against itself that the sealed
implementation had been read first, and names which three predictions are
weaker for it.

Sources pinned at snapshot `7fcd72f618e676a88df65efed4926ac3c11eacbe` of
`main`: five blobs and three spans. The spans are the clauses the
structural results rest on — datum absorption, unconditional form
appending, set-union instance and rule admission, and the sealed one-item
enumerator that **is** the edge set of the move graph.

**Neither preceding rung is pinned.** `research/reach_measure` and
`research/reach_additivity` are both open pull requests, so neither is on
`main` and neither is pinnable; stacking is prohibited. `actList` and its
append law are **re-proved here** rather than cited across an open branch,
and the one shared two-line functional is restated and declared in
`SOURCE_MANIFEST.json`.

## Declared readings

1. **No move is invented.** A node is a reachable state; an edge is exactly
   what `iter_cost1_items` offers there. The graph is the estate's own.
   `test_no_move_is_invented` pins it.
2. **Candidates are declared before they are priced.** `FW-TUNED`. Nine
   candidates, each with a native reading written into `costs.py` before any
   circulation was computed, and three of them are present *because* they
   were expected to telescope. A search that lists only its answers is not a
   search, and the exact ones are reported as exact rather than dropped.
3. **Exactness is decided twice.** Once by walking the graph and building
   the functional — constructive, so a positive answer is a witness — and
   once by summing around a cycle basis. The two must agree on every
   candidate, and the agreement is recorded per candidate.
4. **The rectangle is depth three, and the depth is a finding.** At depth
   one the graph has cycle rank **zero**: no closed walk of any kind, so
   every statement about circulation would be vacuous, and `FW-VACUOUS`
   refuses that as a finding. Depth two gives rank 22; depth three, 378.
   The number of moves leaving the rectangle is reported at each depth
   rather than hidden.
5. **Waste and order are kept apart everywhere.** A cost nonzero on a move
   that changes nothing prices waste; a cost nonzero on two routes to one
   state prices order. `FW-DEGENERATE` requires the first to be reported as
   what it is, and the tables below never merge the two columns.

## Terminals, each with its scope

- **SEARCH_SPACE_CHARACTERISED** (PROVED_THEOREM). `additive_empty_zero`:
  additivity forces the empty response to cost nothing — not a convention,
  a consequence, got by applying the law to the empty response twice.
  `additive_eq_sumEdges`: **every additive cost is the summation of its own
  restriction to single moves.** So the space of additive costs *is* the
  space of weightings, the nine candidates below range over that space
  rather than over what occurred to the author, and no cost anyone could
  have proposed is outside it.
- **DIRECTED_CLOSED_WALKS_ARE_STATIONARY** (PROVED_THEOREM).
  `closed_directed_walk_is_stationary`: if a move never decreases the state
  and the order is antisymmetric, a sequence of moves returning to its own
  start never left it. Proved over an abstract action with reflexivity,
  transitivity, antisymmetry and monotonicity supplied as hypotheses, so it
  needs no order library and makes no claim about this estate that the
  estate does not satisfy.

  **The consequence is the structural point of the rung.** Where admission
  only adds, path-dependence cannot come from going around a directed
  cycle, because there are none that move. It has exactly two sources: a
  move that changes nothing, and two different routes to one state. The
  first is waste. The second is order.
- **TWO_ROUTES_EXIST** (COMPUTATION, scope: the rectangle). **770 commuting
  squares** — pairs of two-move routes leaving one state and landing on
  one state. The smallest is a form and a datum at the root, exactly as
  predicted.
- **RANK_COMPUTED** (COMPUTATION, scope: the rectangle). 262 states, 638
  moves, 2 components, cycle rank **378 = 232 waste + 146 order**. The rank
  strictly exceeds the self-loop count, so order cycles contribute
  independently and the path-dependence found here is not an artefact of
  redundancy. `FW-CLASS`: this is the rank of this finite graph and of
  nothing larger.
- **PATH_DEPENDENT_COST_EXHIBITED** (PROVED_THEOREM and COMPUTATION).
  `rule_span`: additive by construction, reads the base (decided from
  evidence, not asserted), not exact by both decision methods, **zero on
  every one of the 232 waste cycles** and nonzero on 4 order cycles. In
  Lean, `Commit.span_is_additive` and `Commit.span_is_not_exact` prove the
  pair on an abstract two-item model, with `commit_early` and `commit_late`
  giving the totals `n` and `n + 1` for every `n`.
- **`ONLY_DEGENERATE_PATH_DEPENDENCE` does not fire** — and it is worth
  saying which candidates would have made it fire. `item_count` and
  `redundancy` are not exact, and their circulation is **zero on every
  order cycle**: they price waste and nothing else. `rule_span`,
  `width_at_admission` and `empty_admission` are the reverse — **zero on
  every waste cycle**, nonzero on order. `mention_deficit` does both.
- **The two properties are independent axes, and all four cells are
  occupied** (COMPUTATION). This is the trap the question contained, and it
  is worth naming: *reading the base is not what makes a cost
  path-dependent.*

  | | exact | not exact |
  |---|---|---|
  | **base-free** | `arity_debt` | `item_count` |
  | **base-relative** | `reach`, `context_opening` | `rule_span`, `width_at_admission`, `empty_admission`, `mention_deficit`, `redundancy` |

- **OPEN_AT_NAMED_TARGET**: the leftovers below, each priced.
- **OB1_UNCHANGED, S66_UNCHANGED, S9_LAST_UNCHANGED, NS95_GROWTH_UNCHANGED**:
  this rung touches none of the protected opens. A cost algebra is not a
  demand generator, proves nothing about the two paper items, and says
  nothing about the growth question of the arithmetic chain.
- **MANUAL_RECEIPT_DECLARED**: no CI gate reads this tree's pins, Lean
  audit, or scans.
- **Axioms**: 17 `#print axioms` reports, 9 axiom-free, the rest within
  `{propext, Quot.sound}`.

## The full candidate table

Every candidate, with the reading it was declared under, priced over the
rectangle. `waste` and `order` are the counts of fundamental cycles of each
kind on which the circulation is nonzero.

| candidate | reading | base-relative | exact | waste | order |
|---|---|---|---|---|---|
| `arity_debt` | a form costs its arity | no | **yes** | 0 | 0 |
| `context_opening` | contexts newly opened, derivable or not | yes | **yes** | 0 | 0 |
| `reach` | pluggings newly made derivable | yes | **yes** | 0 | 0 |
| `item_count` | the sealed count, one per item | no | no | 232 | 0 |
| `redundancy` | one when the move changes nothing | yes | no | 232 | 0 |
| `mention_deficit` | an instance costs the data it ignores | yes | no | 214 | 18 |
| `empty_admission` | the record grows, the content does not | yes | no | 0 | 22 |
| `width_at_admission` | a form costs the state it ranges over | yes | no | 0 | 38 |
| **`rule_span`** | **a commitment costs what it ranges over when made** | **yes** | **no** | **0** | **4** |

The three exact ones are the point of including them. Two of them read the
base and telescope anyway.

## The prediction record

| # | prediction | disposition |
|---|---|---|
| P1 | additive costs are exactly weightings of single moves | **CONFIRMED** — `additive_empty_zero`, `additive_eq_sumEdges` |
| P2 | directed closed walks are stationary, so path-dependence has two sources | **CONFIRMED** — `closed_directed_walk_is_stationary` |
| P3 | two routes exist; the smallest is a form and a datum | **CONFIRMED** — 770 commuting squares; the smallest witness is a form/datum pair at the root |
| P4 | a path-dependent cost must therefore exist, and existence is not the finding | **CONFIRMED and honoured** — nine candidates declared before pricing |
| P5 | the item count is path-dependent only through waste | **CONFIRMED** — 232 waste cycles, **0** order cycles, and no square witness at all |
| P6 | pricing a form by what it ranges over gives nonzero circulation on the form/datum square | **CONFIRMED** — `width_at_admission`, 38 order cycles, witness at the root |
| P7 | candidates built as a difference of a count of the state will be exact even when they read the base | **CONFIRMED** — `reach` and `context_opening` both read the base and both telescope |
| P8 | the rank exceeds the self-loop count | **CONFIRMED** — 378 against 232 |

Eight predictions, eight confirmed. That is a worse sign than it looks and
is recorded as such: the chronology admits the sealed implementation was
read before the predictions were written, and P1, P2 and P3 were reasoned
from it. The unforced ones are P5 and P7, which are about the *costs* and
not about the grammar, and those are the two the reader should weigh.

The prediction that was **not** made, and should have been: nothing
predicted that `rule_span` would be nonzero on so few order cycles — 4 of
146 — because a rule move appears in few of the squares. That is a fact
about where rules occur in the rectangle, not about the cost, and it is
recorded rather than smoothed.

## What this rung settles, and what it does not

It settles the shape of the search: additivity pins the space of costs to
weightings of single moves, so the hunt was over a described set. It settles
where path-dependence can come from in an estate where admission only adds,
and that both sources actually occur here. It settles that base-relative and
path-dependent are independent — the question that prompted the rung
implicitly joined them, and all four cells are occupied. And it exhibits a
cost that is additive, reads the state, prices no waste at all, and is
provably not the difference of any state functional.

It does **not** claim `rule_span` is canonical, or the best, or the one an
optimizer should minimize. It is one weighting with a defensible reading,
and `width_at_admission` and `empty_admission` are two others with the same
qualitative behaviour. It does not compute the group of costs modulo exact
ones, only the rank of the cycle space that would bound it. It proves
nothing about a rectangle deeper than three. And it does **not** show that
any of these costs detects an obstruction the estate cares about — only
that, unlike every cost the estate had, they are the shape that could.

## The injection record

| Gate | Injection | Observed failure |
|---|---|---|
| Pin integrity | first digit of the pinned `code/derivation/candidates.py` blob flipped | `FAIL: code/derivation/candidates.py blob at 7fcd72f6... is 9fa609d8..., pinned afa609d8...`, at the snapshot and at `HEAD`; exit 1, then 0 after reversal |
| Span pin | the enumerator span's last line moved from 269 to 270 | `FAIL: span code/derivation/candidates.py:260-270 at 7fcd72f6... hashes ebeab1a8..., pinned a8f60fe3...`; exit 1, then 0 after reversal |
| Prediction freeze | one word changed in `PREDICTIONS.md` (*are* to *were*) | `FAIL: PREDICTIONS.md hashes 11a72a5e..., recorded 3a6ef227...`; exit 1, then 0 after reversal |
| Reconstruction policy gate | `reconstruction_policy` deleted from the manifest | `FAIL: no source reconstruction bindings recorded and no reconstruction_policy declared to say why`; exit 1, then 0 after reversal |
| Lean forbidden token | a comment carrying the first forbidden token appended to `Cochain.lean` | `FAIL: Cochain.lean contains forbidden token 'sorry'`; exit 1, then 0 after reversal |
| Axiom-report source census | the `le_actList` `#print axioms` line removed | `FAIL: PathDependentCost.le_actList is declared in Cochain.lean but not listed in AxiomReport.lean`; exit 1, then 0 after reversal. Without the census the removal is invisible, because the line removes its own report |
| The two decision methods | the circulation verdict forced to *exact* for every candidate | `AssertionError: False is not true : empty_admission`; exit 1, then 0 after reversal. A weaker first attempt — dropping one cycle from the check — did **not** fire, because for an exact candidate every cycle is zero and for the others the dropped cycle was not the only nonzero one; that attempt is recorded rather than replaced |
| Cycle-basis size | one non-tree edge dropped from the basis | the builder's own `E − V + C` assertion fires before any cost is priced, printing `(377, 378, 2947)` — basis size, rank, moves leaving the rectangle; exit 1, then 0 after reversal |
| Declared-reading gate (FW-TUNED) | a `zzz_probe` candidate added to `CANDIDATES` with no entry in `READINGS` | the module-level assertion fires on import of `costs`, so the tree cannot load with an undeclared candidate; exit 1, then 0 after reversal |
| Census scan (FW-PIN, FW-NAME) | a probe file carrying a watched noun placed in the write root | the scan names the file, the line and the token; exit 1, then 0 after deletion. The token is elided here rather than quoted, because the scan reads this file too |
| Receipt replay | the cycle rank changed from 378 to 379 in the committed receipt | `test_the_committed_receipt_replays_byte_for_byte` fails on the differing byte range; exit 1, then 0 after reversal |

## Leftovers, named and priced, executed nowhere

1. **The group, not the rank** — OPEN. The cycle rank bounds how many
   independent path-dependent costs there can be; it does not say what the
   quotient of additive costs by exact ones actually is, nor give it a basis
   with readings. Price: an integer-module computation over the cycle space, and a
   decision about which basis is native rather than merely spanning.
2. **A cost that detects an obstruction the estate names** — OPEN, and the
   rung after this one. `rule_span` is the right *shape*; nothing here shows
   its nonzero classes correspond to anything the estate already calls an
   obstruction. Price: a declared obstruction and a proof that some cost's
   circulation is nonzero exactly where it stands.
3. **The converse of exactness** — OPEN in Lean. This tree proves that two
   routes with different totals refute exactness, and decides the converse
   computationally by building the functional. The general statement — zero
   circulation everywhere implies exactness — needs a choice of path per
   state and is not attempted without a choice principle. Price: a rooted,
   reachable graph with a chosen spanning structure, supplied rather than
   assumed.
4. **Depth beyond three** — OPEN. Every count is over the declared
   rectangle. The two Lean theorems are the only statements above that do
   not depend on it.
5. **Whether `rule_span` is additive on composites the estate would
   actually offer** — OPEN in one respect: additivity here is by
   construction over single moves, and the sealed grammar's two-item deltas
   were not separately re-priced in this tree. The preceding rung checked
   that composition acts sequentially, but it is unmerged, so this tree
   does not lean on it.

## The registration diff this tree does NOT apply

    - name: path_dependent_cost pins, Lean audit and scans
      run: |
        python research/path_dependent_cost/verify_pins.py
        python research/path_dependent_cost/verify_lean.py
        python -m unittest discover -s research/path_dependent_cost -p "test_*.py"

## Commands (run from this directory unless noted)

| command | exit | key line |
|---|---|---|
| `python verify_pins.py` | 0 | `pins clean: 5 sources and 3 spans at snapshot and HEAD; ... native PROMPT.md frozen; 1 predictions freezes reconstructed` |
| `python verify_lean.py` | 0 | `lean audit clean: 4 sources, 17 axiom reports (9 axiom-free), axioms within ['Quot.sound', 'propext'], 17 originating theorems all listed` |
| `python run_path_dependent.py` | 0 | `graph at depth 3: 262 states, 638 moves, rank 378 = 232 waste + 146 order` |
| `python -m unittest discover -s . -p "test_*.py"` | 0 | 27 tests, refusal scans and unit tests pass |
| `python -m mypy` | 0 | strict, no issues in 8 source files |
| `python ci/check_prose_watchlist.py` (repository root) | 0 | clean without a repin |
