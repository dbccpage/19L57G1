# Process candidate

## Answer to the main question

**Yes.** The repository's existing record already contains a reusable
finite process meeting the nine conditions of the work order. It is not
proposed here; it is implemented in `code/derivation/` and exercised by
`code/run_derivation.py`, and its outputs are the committed branch trees.

It is **not forced**. It is forced only relative to four declarations it
does not derive: the candidate space, the cost measure, the isomorphism
relation, and the challenge source. The fourth is the first at which the
process cannot continue on its own materials at all, and is OB-1.

Called **P** below purely as an abbreviation. `native_terms.md` records
that the repository has no native noun for the composite and that
`CL-NO-UNIVERSAL-PROPERTY` refuses to call it minimal or initial. No
property of P is asserted here that is not asserted of one of its parts.

## P, in native terms

P is a loop over rounds. Each round reads a regime, obtains a finite set
of challenges, computes the minimum valid responses to each under a
declared measure and declared bounds, quotients those responses by the
implemented isomorphism relation, and attaches **every** resulting class
as a separate branch.

    genesis history
      -> regime (by replay)
      -> challenges (round 1: the imposed requirement;
                     later: the declared closure policy, else the
                     declared external continuation policy)
      -> minimum valid responses per challenge (declared measure, declared bounds)
      -> quotient by the implemented isomorphism relation
      -> one branch per class, all retained
      -> attach; certify each node by replay; enqueue
      -> stop at a terminal, a refusal, or a declared bound

### The nine conditions, each located

| condition | where it is met | scope |
|---|---|---|
| begins from an admitted state | `replay(reading.genesis)` | two readings carried, L and F |
| receives finite challenges | `reading.target`; `closure_challenge_orbits` | the second is **declared**, not derived |
| separates supply / mention / admission / retention / observation / equality / state change | `model.step`; `observe.profile`; `Supply` is a no-op | `CL-1-SUPPLY-NOT-ADMISSION`, `CL-0-INERTIA` |
| decides what is expressible under current resources | `observe.profiles`, `collapsed_pairs` | the declared sense of separability only |
| proposes only the weakest justified next change | `candidates.min_responses` | weakest **under a declared measure within declared bounds** |
| preserves all tied non-isomorphic continuations | `engine._quotient`, then a branch per class | ties are retained, never collapsed for readability |
| records refusals and open obstructions without hiding them | node `status`; `paper/paper.md` §12 | see the refusal rule below |
| replays every certified result | `Node.certified`; `export.verify_full_export` | every node **and every edge** |
| stops when no next challenge or no justified response | `terminal_all_separated`; `terminal_no_response` | plus two declared bounds |

## The exact admission rules

State changes only through these, and through nothing else.

**A1. Supply admits nothing.** `step(r, Supply(t)) = r`.

* reads: nothing.
* admits: no state change.
* replays: trivially, as a no-op in any history.
* witness: `CL-0-INERTIA`, `CL-1-SUPPLY-NOT-ADMISSION`; Lean
  `supply_no_op`.
* refusal on failure: none possible — it is an identity.
* ties: none.

**A2. Datum admission.** `AdmitDatum(t)` appends `t` unless `t` is
already present, in which case it designates the existing datum.

* reads: `r.data`.
* admits: one datum, or nothing on re-admission.
* replays: by position; indices increase strictly along a history.
* witness: dedup on presentation identity is a declared metatheoretic
  convention, stated in `model.AdmitDatum`'s docstring.
* refusal: none; the event is total.
* ties: none.

**A3. Form admission.** `AdmitForm(a)` appends arity `a >= 1`.

* refusal: `AdmissionError` when `a < 1`.

**A4. Instance admission.** `AdmitInst(f, args)` adds `(f, args)`.

* refusal: `AdmissionError` on unknown form, arity mismatch, or an
  argument out of range. Ill-formedness is refused, not coerced.

**A5. Uniform rule admission.** `AdmitRuleAll(f)` marks form `f`
all-tuples-derivable.

* refusal: `AdmissionError` on unknown form.

**A6. Requirement imposition.** `Impose(i, j)` adds the persistent
separation requirement `(i, j)`, `i < j`.

* reads: `r.data` for range.
* admits: a constraint, not an object. It changes what counts as a valid
  response; it adds no datum, form, instance or rule.
* refusal: `AdmissionError` when out of range.

**A7. Nothing else.** A candidate delta is *proposal data*. It mutates no
regime until translated into A2–A5 events by `delta_events` and replayed.
`CL-0-NO-PROPOSAL-MUTATION` records this.

## The exact replay rule

    replay(history, base = EMPTY) = fold step over history

and a regime is **certified** exactly when

    replay(recorded history) == claimed regime

This is checked at three places, and the third is the strong one:

1. per node, at construction: `Node.certified`;
2. per tree, in `Tree.stats()`: `all_certified`;
3. per **edge**, in `export.verify_full_export`: the parent history
   extended by the edge's events is replayed, and a creation edge must
   reproduce the stored child by regime hash, while a merge edge must
   carry explicit datum and form bijections mapping the replayed result
   onto the stored representative, tokens excluded.

Evidence: `CL-REPLAY`. Falsifier: any exported node or edge whose stored
regime hash differs from the replay of its recorded history.

## The exact refusal rule

P emits typed outcomes, never silence. The status vocabulary is:

| status | meaning | forced? |
|---|---|---|
| `terminal_all_separated` | pair-separation closure fixpoint reached and the external continuation policy is disabled | genuine termination, independent of the round budget |
| `terminal_no_response` | some challenge has no valid response within the declared bounds | never observed in any committed run; see below |
| `completed` | the declared round budget was reached | **declared bound**, not termination |
| `frontier_guard` | the declared node guard was reached before expansion | **declared bound**, not termination |
| `expanded` | the node produced children | — |

Two of the five are declared bounds and must not be read as the process
stopping of its own accord. The exported frontier is what is complete
within those bounds, and nothing beyond them is claimed.

`terminal_no_response` is unreached: `CL-PROGRESS` proves every supplied
separation demand on an accepted regime has a valid response — a fresh
unary form plus one mark. Its scope is response existence only. It does
not assert autonomous demand generation and does not assert an unbounded
tower.

Refusal is also studied as a difference source in its own right
(`code/derivation/refusal.py`, `paper/refusal_difference.md`), where five
re-admission disciplines are compared without assuming that refusal,
repetition, occurrence and state difference are equivalent.

## The tie rule

At every expansion, `_quotient` groups the minimum valid responses by the
canonical key of the **resulting** regime, and the loop attaches one
branch per class. No class is dropped. Isomorphic regimes arriving at any
depth merge into one node, and the merge edge carries an explicit
isomorphism certifying it.

The ties that must be preserved, as the record has them:

* Challenge 3, measure `mu1`: three non-isomorphic classes in reading L
  (`CL-3-TIE-CLASSES`), five in reading F within the declared bounds, and
  a countably infinite tie family indexed by arity in reading L
  (`CL-3-INFINITE-TIES`).
* Challenge 3, measure `mu2`: unique up to isomorphism, grammar-wide, in
  both readings (`CL-3-UNIQUE-MU2-L`, `CL-3-UNIQUE-MU2-F`).

That `mu1` and `mu2` disagree about uniqueness at the very first
answerable question is the sharpest available evidence that the measure
is a declaration and not a discovery.

* Both admission readings L and F are carried in full, with no internal
  fact separating them (`CL-READING-UNDERDETERMINATION`,
  `paper.md` §11(h)).

## Where P is not forced

In dependency order. The first two are needed at round 1; the third at
every quotient; the fourth from round 2 on.

**N1 — the candidate space.** `Bounds(max_items=2, max_arity=2)` and the
four item kinds are declared. A different grammar admits different
minima. What *is* proved is impossibility below two items, absolutely
over the item grammar (`CL-3-COST1-IMPOSSIBLE`, `CL-3-MIN-TWO`) — that
result is grammar-wide, and the enumeration completeness is what the
bound limits.

**N2 — the cost measure.** `mu1` and `mu2` are both declared, and they
yield different trees. `paper.md` §12 names this as the documented
sensitivity. "Weakest justified next change" is therefore always
"weakest under a stated measure", never "weakest".

**N3 — the isomorphism relation.** Implemented and declared. It is
cross-checked for soundness (`CL-ISO-SOUND`) and against brute force,
but it is not derived from the object language, and it decides what
counts as one continuation rather than two.

**N4 — the challenge source. This is the first point at which P cannot
proceed on its own materials, and it is OB-1.**

After the imposed requirement is discharged, P needs another challenge.
The object language supplies none. `CL-CLOSURE-POLICY` states it
exactly: a collapsed pair is not an active obstruction unless separation
is required, and the requirement pattern originates externally. The
declared closure policy is what converts a collapsed pair into a demand.
Its virtues are real and checked — token-blind, no fresh data, no new
goal kind, isomorphism-equivariant, and it reaches a fixpoint — but its
*selection among conceivable policies* is a declared-metatheory judgment,
and the ledger says so in its own falsifier field.

The alternative branch, the external continuation policy, is the supply
and admission of one fresh opaque token, and is explicitly external.
Runs with `supply=False` are the closed-system baseline, and they
terminate quickly: 1 round in reading L, 3 in reading F
(`CL-CLOSURE-TERMINATION`).

So the closed system stops, and the open system continues only because
something outside it keeps handing it tokens.

### What was achieved against N4, and what it does not close

`paper/endogenous_generator.md` is the one place the record pushes
directly on N4, and the two halves come apart:

* **Generation is proved, horizon-free.** `generation_never_dries`: from
  the third round on the composite always has a live obstruction, and the
  only event consumed is the internally enabled reflection. This is the
  first horizon-free challenge generator exhibited in the development. No
  minimality or uniqueness claim is attached to it.
* **Repair is excluded for the declared finite-local class.**
  `G1Class.g1_class_exclusion` proves horizon-free that no fixed-radius,
  fixed-finite-alphabet member of `LocalStrategy` fires, clears, and avoids
  recurring import. The earlier five-strategy, 15-round computation remains
  a bounded historical witness: its branches fire unrepaired, repair by
  recurring import, or kill generation. Strategies outside the proved class
  remain open.

The rule that generates is itself declared. So the record does not yet
contain a demand the object language raises unaided. The unrestricted
remainder is an out-of-class repair channel, or a theorem for a wider declared
class. `OB1_UNCHANGED`.

P stops here. Continuing would require an undeclared measure or an author
choice, and `continuation_plan.md` records that as a stopping condition
rather than crossing it.

## What P is not

* Not proved minimal or initial among any class — `CL-NO-UNIVERSAL-PROPERTY`
  is **refused**, and the word "minimal" is therefore not used of P.
* Not unbounded. The committed runs reach the requested 15 rounds under
  the external continuation policy; continuation beyond the exported
  depths is unresolved and no unboundedness is claimed
  (`paper.md` §11(g)).
* Not a decision procedure for arbitrary problems. It handles declared
  finite challenge packets, and its outputs are exactly the typed
  outcomes in the refusal rule above.
* Not independent of its readings. Two survive; both are carried.
