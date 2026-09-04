# BOUNDARY SEED — a second blind derivation, from `<|>`

Long-horizon seed prompt.  This file is read-only for the run.  Its
SHA-256 is recorded in the run's paper.  It states no expected result.
It is pasted as the single user turn of every session of the run.

## 0. Isolation, and the one thing this run is blind to

Use only this repository.  Do not use the network, external files, prior
project instructions, plugins, agents, skills, memories, or user guidance.
Do not ask questions.  Do not modify this file.

This run lives inside the repository that holds the sealed derivation
from `<>`.  It is a second derivation, from a different initial
inscription, and its value is that it is carried out **without consuming
the first derivation's results** until its own results are frozen.  So:

- The write root is `research/boundary_seed/` and nothing else, plus
  the append-only registration of this tree in the research job of
  `.github/workflows/verify.yml`.
- Read, before anything else: `CLAUDE.md` sections "Repository boundary",
  "Assumption discipline", "Proof gates", "Test gates", and "Stopping
  conditions"; and this file.  Nothing else in the repository is read
  until the freeze of section 10: not `paper/`, not `artifacts/`, not
  `lean4/Derivation/`, not `code/derivation/`, not any other
  `research/` tree, not the operating manual below the rule in
  `CLAUDE.md`.  The sealed kernel is not imported, not copied, and not
  consulted; this run builds its own.
- The blindness is by rule, not by ignorance.  The instrument that runs
  this seed knows the first derivation exists and may remember its
  vocabulary.  That is recorded as declared reading zero in the run's
  `MANUAL.md` on the first session, in these words, and every place the
  run notices itself reaching for a remembered result rather than
  deriving one is recorded next to it.  A mechanical check enforces the
  part that can be enforced: `test_blind.py` fails the run if, before
  the freeze, any committed file of the write root contains a citation
  into the sealed paths, a `CL-` claim identifier, a `Derivation.` Lean
  name, or the name of any other research tree.
- Toolchains already installed (Python, pytest, coverage, mypy, Lean 4
  and Lake) are metatheoretic apparatus, not inputs.

Create `research/boundary_seed/PLAN.md` first.  It may contain only the
execution plan, the write-root boundary, the assumption discipline, the
proof gates, the test gates, and the stopping conditions.  Put every
operating instruction in `research/boundary_seed/MANUAL.md`.  Commit
both before substantive work.

## 1. Initial inscription

The only initial object-language inscription is:

<|>

Treat the whole inscription as one opaque atomic datum, with exactly one
admitted exception, stated next.  Do not inherit ordinary meanings for
the visible marks.  Do not assume that the object language can see three
marks, a pair, a string, a set, a point, a relation, a value, emptiness,
order, direction, or containment beyond what the exception admits.

**The admitted exception.**  The object language is admitted to see the
middle mark as a BOUNDARY with two SIDES, and to see that a further
inscription, when one is supplied, lies on one side or the other.  This
is an admitted primitive, declared here, priced in the run's ledger as
one declaration, and never called derived.

The exception admits two readings, and the run carries both to the end
as separate towers, as the first derivation carried two admission
readings:

- **Reading U (unoriented).**  The two sides are distinct but unnamed:
  a mark on one side and the same mark on the other side are different
  wholes, and nothing internal says which side is which.  A reflection
  exchanging the sides is a renaming the object language cannot see.
- **Reading O (oriented).**  The two sides are distinct and named: one
  is the near side and one is the far side, and the object language can
  tell them apart.

Whether either reading makes the sides themselves data, and whether an
empty side is an internally visible fact, are questions for Challenge
zero, not assumptions.

## 2. Research question

Determine the weakest finite formal process that can begin from the
initial datum with its admitted boundary, receive finite external
challenges, determine what is and is not expressible under its current
admitted resources, and change only when a change is justified.

Do not assume that the process is unique, linear, infinite, nontrivial,
computational, geometric, logical, algebraic, categorical, or related to
any known theory.  Do not assume that it is, or is not, related to the
process derived from `<>` in this repository; that comparison is made
once, after the freeze, in section 10.

At every stage record which results depend on the admitted boundary and
which hold without it.  A proof of inertia, termination, branching,
impossibility, or underdetermination is a successful result.

## 3. Mandatory blind challenge sequence

The following are metatheoretic interventions.  They are not
object-language conclusions.  Each challenge is closed before the next
is opened, and for each the run freezes its predictions by hash before
computing.

**Challenge 0 — Initial state.**  Analyze `<|>` with no object-language
operation or transition rule.  Determine exactly what follows from the
admitted boundary alone: whether there is any datum; whether the two
sides are a distinction the object language can act on with nothing on
them; whether an empty side is a fact or nothing; whether any successor
is forced.  If none is forced, prove it.  Do this under both readings.

**Challenge 1 — First additional inscription.**  After Challenge 0 is
closed, the caller supplies:

<a|>

Treat it as another opaque whole, except that the admitted boundary
places the mark on a side.  Determine whether this is a new external
presentation, a new admitted state, a new internally observable
distinction, or some combination requiring explicit definitions.  Do not
conflate supply, mention, admission, current-state designation,
retention, observation, side, or equality.

**Challenge 2 — Second additional inscription.**  After Challenge 1 is
closed, the caller supplies and retains both opaque wholes:

<a|>
<|a>

The same mark, the other side.  Determine what changed merely by
admission and what remains unavailable internally, under each reading:
in particular whether the two wholes are internally distinguishable by
the admitted boundary alone, and if so what that distinguishability cost
and who paid it.

**Challenge 3 — Required separation.**  The caller now requires the
process to make `<a|>` and `<|a>` internally separable in a precisely
declared sense.  Define the chosen meaning; prove whether the current
regime satisfies it under each reading; if it does, state exactly which
declaration made it so and price that declaration in capabilities; if
it does not, enumerate every non-isomorphic minimum one-step
augmentation that could satisfy it, count every undeclared capability
each candidate uses, reject any candidate called one-step that bundles
capabilities, and retain all tied minimum branches unless uniqueness is
proved.  Do not assume that one augmentation is forced, and do not
assume that the boundary makes the requirement trivial.

**Challenge 4 — Two marks across the boundary.**  The caller supplies
and retains:

<a|b>
<b|a>

and requires their internal separability in the declared sense.  The
object language has no licensed access to glyph identity, order, or
matching beyond what it has already derived and admitted.  Determine
what the boundary contributes here that it did not contribute in
Challenge 3, and what it cannot contribute.

**Challenge 5 — A whole within a side.**  The caller supplies and
retains:

<<a|>|>

Determine whether the object language can see a boundary within a side;
whether a whole on a side is a datum, a side, or something requiring a
new definition; what "within" means at depth two under each reading;
whether depth is an internally available count; and what admission, if
any, is needed to treat the inner whole as the outer whole was treated.
Do not assume nesting is admissible; do not assume it is not.

## 4. Autonomous continuation

After Challenge 5, continue without further user input.  For each
surviving branch under each reading: declare its admitted data,
operations, judgments, transition rules, historical state, and every
metatheoretic assumption; devise the weakest deterministic finite
procedure you can justify for generating the next challenge from that
branch alone, and prove it imports no undeclared object-language
structure; enumerate all minimum valid responses; preserve ties as
branches; record unresolved requirements and how they persist, split,
disappear, or create new ones; replay the branch from its recorded
history before certifying any result; stop the branch when no next
challenge or no justified response exists.

If the generator proposes deeper nesting, that proposal is examined
under Challenge 5's definitions and priced; nesting is never free by
default.

Attempt fifteen accepted augmentation rounds per finite branch.  Do not
fabricate a linear sequence.  If the tree becomes too large, state a
deterministic resource bound, export the exact frontier, and prove what
remains complete within that bound.

## 5. Required questions

Answer by proof, executable countermodel, or explicit OPEN status, under
each reading where the reading matters:

1. Does any object-language transition follow from `<|>` alone?
2. Can a proposed transition alter state without a separate admission
   rule?
3. Does a new external inscription necessarily increase internal
   expressive power?
4. Can two externally different admitted inscriptions remain internally
   undecidable or observationally collapsed, the boundary
   notwithstanding?
5. If a current abstraction identifies two cases that a declared task
   requires to be separate, can any operation defined only on that
   abstraction recover the distinction?
6. Is a minimum corrective augmentation necessarily unique?
7. What additional rule, if any, makes a long or unbounded sequence of
   augmentations possible rather than immediate termination, and is
   nesting such a rule?
8. Can unresolved requirements be counted invariantly under renaming or
   isomorphism, the side reflection of reading U included?
9. What recurring transition roles emerge from the derivation itself?
10. Is the final process minimal or initial among a clearly defined class
    of finite processes satisfying the same challenges?  Prove the
    universal property or refuse the claim.
11. Does the process ever formulate an outside of its outermost
    boundary?  Is "the side that has no boundary beyond it" an
    internally available object, a declaration, or unformulable?
12. Does nesting depth become an internal count, and does anything
    definable from the stages of increasing depth converge to an object
    definable from the stages alone?
13. What does the admitted boundary cost, counted in capabilities, and
    what does it buy: which separations, if any, are free under it, and
    which prices, if any, it changes.
14. Does the difference between reading U and reading O change any
    price, any count, or any terminal?
15. At what first stage, if any, do familiar mathematical structures
    become definable?  Distinguish definable, useful realization, and
    forced.  Answer this only in the comparison of section 10, after the
    freeze, and nowhere else.

## 6. Assumption and claim discipline

Every substantive notion must be classified as exactly one of:
metatheory apparatus; supplied object-language datum; externally imposed
challenge; admitted primitive; derived definition; proved theorem;
deterministic computation; countermodel; optional realization;
conjecture; open obstruction; refuted claim.  The admitted boundary is an
admitted primitive and is listed first in every ledger.

Never write "forced", "minimal", "free", "canonical", "equivalent",
"universal", or "complete" without a proof or a precise conditional
scope.  Never write that the boundary is free.

Keep presentation identity, internal identity, observational
equivalence, behavioral separation, and semantic interpretation distinct.
Keep side, containment, and order distinct from one another and from
identity.

Do not silently turn absence of a test into equality.  Do not silently
turn a model proposal into an admitted state change.  Do not use a
receipt, hash, test pass, or successful parser as proof of an unverified
mathematical payload.  Predictions are frozen by hash before each
challenge's computation and before any Lean; a missed prediction is
recorded next to its value and never edited.  Every prediction set
carries one extrapolation about the next challenge or the next depth,
frozen before it is computed.

## 7. Python requirements

Implement the finite reference model under `research/boundary_seed/code/`
and tests under `research/boundary_seed/tests/`.  The implementation
must: be deterministic and typed, mypy strict from inside the tree;
represent histories, admissions, sides, regimes, challenges, candidates,
branches, witnesses, refusals, and terminals explicitly if the
derivation requires them; enumerate terms and candidate augmentations
only under declared finite bounds; quotient duplicate branches only
under an implemented and documented isomorphism relation, which under
reading U includes the side reflection; replay every certified result
from genesis; export machine-readable branch, level, assumption, and
claim data with no timestamp and no environment value; never ask a
language model to decide equality, minimality, isomorphism, survivor
counts, or proof status.  It must not import `code/derivation`, and
`test_blind.py` fails the run if it does.

All tests must pass with at least 95% line and 95% branch coverage over
the tree's own code, measured from inside the tree by a committed
`check_coverage.py`.  Include negative tests for every smuggling or
false-minimality failure discovered.

## 8. Lean 4 requirements

Create a buildable Lean 4 project under `research/boundary_seed/lean/`
with no dependency on the sealed package.  Formalize every theorem-level
claim used by the run's paper.  `lake build` passes; no `sorry`,
`admit`, user-declared `axiom`, `unsafe`, or `partial`, in code or in
comments; every exported theorem cited by the paper has a `#print
axioms` report in a committed axiom log checked by the tree's verifier
against a fresh build; reliance on library axioms is recorded exactly
in the claim ledger; failed theorem targets remain counterexamples or
OPEN, never prose proofs.

## 9. Paper requirements

Create `research/boundary_seed/paper.md`, `change_log.md`, and
`claim_ledger.md`.  The paper must contain: the experimental boundary
and this seed's hash; the metatheory/object-language separation; the
admitted boundary stated as the one declaration and its two readings;
definitions in dependency order; Challenges 0–5 and exact results under
each reading; the autonomous branch procedure; branch and tree results
through the achieved depth; proofs and countermodels; Python and Lean
receipts; the strongest defensible terminal theorem; limitations and
open obstructions; and, after the freeze only, the comparison of
section 10.  The change log records every material revision and its
reason.  The claim ledger gives each claim a stable ID, exact statement,
status, dependencies, assumptions, Python evidence, Lean theorem, axiom
report, falsifier, and surviving boundary.

## 10. The freeze, and the comparison

The freeze happens once, when the stopping conditions of section 11 are
met for both readings or their obstructions are recorded OPEN.  It is a
commit that hashes every file of the write root and writes
`research/boundary_seed/FREEZE.md` with those hashes.  After that commit
and only after it, `test_blind.py` stops enforcing the citation ban, and
the run reads, for the first time, the sealed paper, its ledger, its
Lean, and the research trees, and writes `comparison.md` in the write
root, in native vocabulary only, with no outside name anywhere.

The comparison carries one row per result of this run and one row per
terminal result of the first derivation and of its research extensions
(at least: the sealed terminal statement; the identification dual; the
standing commitment; the two-sided stake; the second derivation's
rungs; the natural sections; the path-dependent cost), each row saying:
same, differs and how, or absent on one side; and, for every price the
first derivation states, the corresponding price here with the
boundary's cost added.  It ends with one table: what the admitted
boundary bought, what it cost, and which results of either derivation
depend on its presence or absence.  Nothing in this run is revised in
response to the comparison; a defect the comparison reveals is logged
OPEN.

## 11. Gates, operation, and completion

Gates: prompt byte-identity of this seed; the tree's own tests under
coverage; strict typing; artifact regeneration byte-identical; Lean
build with the forbidden-token scan and axiom whitelist; the blindness
scan of `test_blind.py` before the freeze; the repository's identifier
firewall and prose watchlist, clean without a pin regeneration; every
gate the tree adds proved by injection and recorded in `MANUAL.md`.
Register the tree's verifier, tests, and typing in the research job.

Operation: one session may close at most one challenge or one
continuation stage.  At the start of a session read the handoff, this
seed, `PLAN.md`, `MANUAL.md`, and the run's own latest status; at the
end write the handoff.  Never merge; the author merges.  When blocked,
record OPEN with the exact obstruction and continue.  Keep every
session's full local battery under fifteen minutes of wall time.

Finish only when: every introduced notion has a source classification,
the admitted boundary first; every state change has a replayable
admission history; every theorem-level claim used by the paper has Lean
evidence or is downgraded; every computational claim has deterministic
Python evidence; all tied minimum branches are retained unless
eliminated by proof under each reading; both coverage thresholds are
met; Lean builds without forbidden gaps and the axiom log is committed;
the blindness scan passed at every commit before the freeze; every
required question is answered or OPEN under each reading; the freeze is
committed; the comparison is written after it and has caused no
revision; and the paper states what was actually derived, including
termination or failure, without targeting a predetermined conclusion.
