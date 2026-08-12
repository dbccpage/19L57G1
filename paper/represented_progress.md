# Represented Progress Without an Outside

**Mission.**  Externally imposed challenge (caller assignment,
2026-08-12).  The decisive question:

> Can all load-bearing causes of represented progress themselves be
> represented, without leaving a hidden evaluator, selector, or source
> outside the replay semantics?

Evidence: `lean4/Derivation/Represented.lean` (native, core-Lean-only,
48 exported theorems), mirrored exactly in
`code/derivation/represented.py` with artifact
`artifacts/represented.json`; replay and mutation tests in
`tests/test_represented.py`.  The two proposed rules were treated as
questions, not assumptions; each earned its scoped theorem, and the
places where naive readings fail are countermodels, not prose.

## TERMINAL

```text
REPRESENTED_KERNEL_EXISTS
HIDDEN_INPUT_CLASSES_REFUTED
CERTIFICATION_BOUNDED_BY_PANEL_QUOTIENT
```

* **A represented kernel exists — relative to a fixed kernel
  constitution.**  The constitution is fixed metatheory, not
  represented runtime input: the event grammar (`Event`), the
  separation and satisfaction laws (`sepB`, `satB`), the declared
  response menu (`responseMenu`), the acceptance predicates
  (`reqOkB`, `markOkB`, `augOkB`, `obstructedB`), and the history
  producer that supplies event streams.  Relative to that fixed
  `step` semantics, every *runtime* input that changes a transition —
  evaluator, requirement, scheduler, tie-break, fresh-name source,
  fuel, authorization, stopping condition — occurs in the represented
  state (`World`) or the represented history (`List Event`), and the
  eight target theorems hold within their declared scopes.  The
  answer to the decisive question is **yes for runtime inputs, by
  construction-plus-proof, relative to this constitution**: the step
  function's type admits no other input, and the support theorem
  gives the factorization.  The constitution does not derive
  itself.
* **Every listed failure class is refuted concretely, and the classes
  are split.**  Four countermodels are *hidden runtime inputs* —
  semantics consuming an input in neither state nor history
  (scheduler, fresh-name source, hidden evaluator, order-sensitive
  tie-break).  Four are *neighboring semantic or inference failures* —
  no hidden input, but a wrong definition or a wrong reading
  (incomplete search declaring a false obstruction, destructive
  rewrite passed off as augmentation, repetition mislabeled as
  progress, per-length witnesses mistaken for productivity).  Each is
  minimal and machine-checked.
* **The internal truth candidate is priced exactly.**  Certification
  by represented evaluators is proved equivalent to joint separation
  by the panel's own columns — and proved *not* to be correspondence:
  a unanimous panel certifies an equivalence that a column outside the
  panel refutes.  Agreement reaches the panel's joint quotient and
  nothing beyond it.

## The required definitions (all native)

| requirement | native definition |
|---|---|
| representation | `World`: data store, view columns, recorded requirements, refusals, budget, license, inert notes |
| admitted transformation | `Event` + acceptance-guarded `step` (rejected acts are represented no-ops) |
| represented history / replay | `List Event` / `replay` (a fold of `step`) |
| recorded requirement | `World.reqs` (admitted only through `require` events, well-formedness enforced at admission) |
| obstruction | `obstructedB`: a recorded, currently violated requirement **plus** exhaustive failure of the declared finite response menu — never mere lookalikeness |
| same-structure repair | `Event.mark`, guarded by `markOkB` (discharges a recorded violation and preserves every satisfied requirement) |
| structure-creating augmentation | `Event.addView`, guarded by `augOkB` (bounded, fresh, expressively increasing; append-only) |
| represented support | `supp` (everything but the inert `notes` field) |
| internally determined successor family | `repairFamily`: *all* tied accepted responses, a filter of the declared menu — no minimum, no representative, no selector |
| replay-equivalence between results | `WEquiv`: literal carrier equality (positions are load-bearing occurrence identities) + membership equality of views, requirements, refusals |

## The eight targets

**RP1 — replay determinism and composition.**  [theorem]
`replay_deterministic`, `replay_nil`, `replay_append`.  For the kernel,
determinism is definitional — that is the design point: the step's
type admits no unrepresented argument.  The countermodels show
semantics with extra arguments failing exactly this.

**RP2 — operational-support factorization.**  [theorem]
`support_determines`: the step factors through the `supp` projection —
worlds agreeing on the represented support have support-equal
successors, for every event.  Contrapositive `internal_support`: two
runs whose successor supports differ already differ in their
represented supports.  This is a factorization theorem about the
operational support, not a claim of per-datum result causation.
`notes_inert`: the represented-but-inert field really is inert.

**RP3 — no hidden choice, scoped to `repairFamily`.**  [theorem]
`repairFamily_sound` / `repairFamily_complete` /
`repairFamily_retains_ties`: the same-structure successor family is
exactly the accepted responses, all ties retained; no selector exists
in it.  Invariance: `equiv_step`, `equiv_replay`,
`equiv_repairFamily` — replay-equivalent worlds have replay-equivalent
successors and membership-identical successor families.  The
*structural* branch of RP6 exhibits the canonical augmentation `[i]`,
whose orientation is supplied by the ordered, recorded requirement
`(i, j)` — a represented datum and a stated scoping: augmentation
candidates are not gathered into a retained family here, and the
no-hidden-choice theorem does not extend to them.  Countermodel 7
(`stepHead`) breaks the repairFamily invariance precisely by
consulting list order.

**RP4 — repair.**  [theorem]  `mark_discharges`, `mark_preserves`,
`step_mark_sound`: an accepted repair discharges a recorded violation
and preserves every previously satisfied recorded requirement — the
acceptance checker's verdict is sound at the step level.

**RP5 — augmentation preserves satisfied positive requirements.**
[theorem]  `satB_aug` is the exact positive-satisfaction delta
equation: satisfaction after augmentation is the old verdict or the
new column's.  Every satisfied positive requirement is therefore
preserved (`aug_preserves_satisfied`).  What is *not* preserved — by
design — is old non-separation: augmentation exists precisely to
change such judgments, and `aug_increases` verifies that an accepted
augmentation separates some bounded pair no old view separated.
"Conservativity" would overclaim; the preserved class is exactly the
satisfied positive requirements.

**RP6 — represented progress.**  [theorem]
`represented_progress`: under the explicit hypotheses — replay
well-formedness (`wf_replay`, an invariant, not an assumption) and a
recorded violation — the internally determined repair family is
non-empty, **or** the violation is a certified obstruction *and* the
canonical singleton augmentation is accepted and discharges it.  The
isolated remaining hypotheses are exactly the represented budget and
the represented license (`progress_needs_budget`,
`progress_needs_license`): with either absent the accepting steps are
no-ops, and the same-level exhaustion is recordable as a represented,
certificate-bearing refusal (`refusal_needs_certificate`,
`refusals_are_represented`).  Scoped precisely: refusal is
**non-absorbing** — it records exhaustion and terminates nothing;
ending a bounded run belongs to the history producer, which is part
of the fixed constitution, not a represented terminal driver.  No
claim of terminalization-in-refusal is made.

**RP7 — closure.**  [theorem]  `violation_only_from_require`: a new
violation can arise only from a represented `require` event — marks
cannot create one (the preservation guard), augmentations cannot
(monotonicity), the rest touch neither requirements nor views.
`quiescent_stable`: a quiescent world stays quiescent under every
non-`require` event.

**RP8 — unbounded-run discipline, under a supplied stream.**
[theorem + finite computation]  The event stream `histUpTo` is an
*explicitly supplied, prefix-compatible* stream — a metatheoretic
history producer, not an endogenous source, and it is not called one.
What the kernel contributes: `histUpTo_prefix` (each history extends
the last), `worldAt_data` (the replayed carrier is literally
`range (k+1)`, horizon-free, reached through the acceptance-guarded
`step` alone), `productive_run` (strict growth), the Lean quiescence
instance `worldAt_three_quiescent`, and — computationally, exhaustive
to the 15-round bound — per-event acceptance (`all_events_accepted`:
no event on the stream is silently rejected) and quiescence at every
stage.  The countermodel (`witValid`) has a witness at every finite
length and provably no compatible infinite source (`wit_all_lengths`,
`wit_no_infinite`) — finite witnesses do not assemble into a history,
so productivity and per-length witnessing are separated by proof.

## The internal candidate for truth

[theorem + countermodel]  `cert_scope`: positive certification by a
represented panel is **exactly** joint separation by every evaluator's
own columns.  `cert_not_correspondence`: a unanimous panel certifies
"equivalent" while a column outside the panel separates — agreement,
repetition, and certification never reach an unrepresented outside;
they reach the panel's joint quotient.  `cert_panel_relative`:
extending the panel can break closure — certification is a fact about
a represented panel, not a monotone approach to correspondence.  This
is the strongest defensible finite substitute for truth-from-outside:
*truth-for-a-panel, priced as such*.

Classification: the panel is an **explicit certification argument** —
represented data by type (column lists, no functions from nowhere),
but not yet carried in `World` or admitted by events.  Certification
is therefore not replay-integrated in this kernel; integrating panels
into the replayed state is a separate, unclaimed step.

## The eight required countermodels, split by class

**Hidden runtime inputs** — semantics consuming an input found in
neither the represented state nor the represented history:

| # | hidden input | witness |
|---|---|---|
| 1 | unrecorded scheduler | `scheduler_hidden`: same state, same history, different results by an external tick-order bit |
| 2 | unrecorded fresh-name source | `gensym_hidden`: an external seed replaces the event's token; carrier sizes diverge |
| 3 | hidden evaluator | `oracle_hidden`: an unrepresented oracle pushes through a repair the represented checker rejects |
| 7 | order-sensitive tie-break | `order_sensitivity_splits_equivalents`: two replay-equivalent worlds get observationally different successors under a head-picking semantics; the kernel's `equiv_step` is exactly the theorem this violates |

**Neighboring semantic and inference failures** — no hidden input; a
wrong definition or a wrong reading:

| # | failure | witness |
|---|---|---|
| 4 | incomplete search | `incomplete_search_false_alarm`: a truncated menu declares an obstruction the exhaustive check refutes — obstruction requires exhaustive failure by definition |
| 5 | destructive rewrite as "augmentation" | `augmentation_destroys_old_replay`: overwriting a column kills a previously satisfied requirement; the kernel's append-only augmentation provably cannot (`satB_aug`) |
| 6 | repetition as progress | `repetition_not_progress`: three admissions of one token replay to the state of one; history length grows, the violation set does not |
| 8 | pointwise witnesses as productivity | `wit_all_lengths` + `wit_no_infinite`: valid histories of every length, no compatible infinite source |

## The exact ceiling

What the theorems do **not** say, stated as sharply as what they do:

* The kernel proves *representability of runtime inputs relative to a
  fixed constitution*, not uniqueness and not self-derivation: the
  event grammar, laws, menu, acceptance predicates, and history
  producer are fixed metatheory; budget and license are represented
  **choices** (evidence class: policy).  Rule 2 forbids hidden
  selectors; it does not derive the selected.
* `represented_progress` is scoped by its explicit hypotheses.  Budget
  and license are load-bearing and represented; remove either and the
  accepting steps are no-ops, with the exhaustion recordable as a
  represented refusal.  Refusal is non-absorbing — it certifies
  same-level exhaustion, it does not terminalize; run termination
  belongs to the metatheoretic history producer.  Progress is
  conditional on represented resources, never free.
* Internal certification is bounded by the panel's joint quotient —
  the anti-promotion theorem is part of the package, not a caveat
  outside it.
* Replay-equivalence treats the carrier literally: positions are
  occurrence identities (an established import of this development),
  so order of *admission* is semantic, while order of *views,
  requirements, refusals* is provably not.
* The productivity theorem exhibits one compatible unbounded run
  *under an explicitly supplied stream* and separates it from
  per-length witnessing; the stream is metatheory, never called
  endogenous, and the theorem does not claim every unbounded demand
  stream is realizable — the König-failure countermodel is the reason
  such a claim needs its own hypotheses.
* Determinism for the kernel is definitional; its *content* is
  carried by the support theorem plus the countermodels.  A skeptic
  should read RP1 as "the kernel's type is the theorem" — and the
  countermodels as what that type is worth.

## Relation to the standing rules

Rule 1 (obstruction removed or structure forced) holds in the kernel
in its corrected, checker-verified form: violations either admit an
accepted same-structure repair or are certified obstructions whose
canonical augmentation is accepted (`represented_progress`), with
refusal available only as a represented, certificate-bearing record.
Rule 2 (nothing from nowhere) is not assumed: it is the kernel's type
discipline, made falsifiable by the eight countermodels and made
precise by the support and invariance theorems.  Neither rule is
proved consistent-and-sufficient in general — they are proved
consistent and sufficient *for this kernel within its declared
bounds*, which is the strongest finite theorem available; the general
forms remain conjectures (evidence class: conjecture).
