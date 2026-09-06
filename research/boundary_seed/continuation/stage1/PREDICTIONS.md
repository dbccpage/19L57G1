# Continuation stage 1 — predictions, written and hashed before any code or proof

`AuthorityEffect: None`.  Each prediction carries a falsifier and a
FORCED / NOT FORCED label: FORCED means the writer expects it to follow
from the definitions the run has not yet written, and a hit on a FORCED
prediction is evidence of the order of the work and not of insight.  A
missed prediction is recorded next to its value in `STATUS.md` and never
edited here.  The sha256 of this file as frozen is recorded in `STATUS.md`
and pinned by `verify_pins.py` and the tests.

**Disclosure, sharper than the earlier rungs gave.**  The mandatory challenge
sequence is closed, and this stage opens the seed's autonomous continuation.
Before freezing this file the writer ran scratch computations against the
tree's own committed code and therefore already knew four of the numbers below:
the branch counts, the text the enumeration generator emits first, the pairs
the further-mark branch leaves undemanded, and the arithmetic of the node
bound.  Those are named here so that a reader can discount the corresponding
hits to zero.  What was not computed before the freeze: whether the implemented
branch quotient identifies the adoptions the writer expects it to, whether the
demand generator is eliminated on every branch of reading O, whether the two
cost readings of "one step" agree in this space, and what the stage's own
census says about the generator reading state.

The stage: the seed's section 4 asks, for each surviving branch under each
reading, for the weakest deterministic finite procedure the run can justify for
generating the next challenge from that branch alone, with a proof that it
imports no undeclared object-language structure, and for the declared resource
bounds under which the continuation runs.  This stage declares those and runs
no round.  The state inherited is the one Challenge 5 left: under each reading
the configuration is the replay of the Challenge 4 caller history — four marks,
placement `(0, 1, 0, 1)`, labels `("a", "b", "b", "a")` — with every minimum of
Challenges 3, 4 and 5 a retained candidate and none of them taken.

- S1-1 (the declared branch set).  A branch is a certified line of the run: the
  declarations in force on it, the caller history it replays, and the
  configuration that replay produces.  The base branch adopts nothing; every
  other declared branch adopts exactly one retained tied-minimum class of one
  closed rung, and a branch adopting two or more is not enumerated.  Under that
  rule the declared branch set is **six branches under reading U and five under
  reading O**: the base; under U the three Challenge 3 minima and under O none,
  the Challenge 3 minimum under O being the null point, which adopts nothing
  and is the base; the Challenge 4 minima, one under U and two under O; and the
  two Challenge 5 policy minima under each.  The implemented quotient
  identifies the Challenge 3 and Challenge 4 withdrawals of the mark
  permutations, which are one declaration named at two rungs, and identifies
  the two further-mark points, which are one class.  NOT FORCED: the
  one-adoption rule is a declaration of this stage and a wider set is
  available.  Falsifier: a branch count other than six and five; the two
  withdrawals not identified by the implemented quotient; the two further-mark
  points not identified; or the Challenge 3 minimum under O adding a branch.
- S1-2 (the branch key must carry more than the configuration).  The two
  Challenge 5 policy branches retain configurations with the same canonical key
  under both readings — one mark on one side — so a branch key read at the
  configuration alone reports one branch where the declarations give two, which
  is the defect the Challenge 5 class key was widened over the whole declared
  domain to avoid.  The implemented branch key therefore carries the
  declarations in force, the Challenge 5 class key of the policy among them,
  beside the least key of the configuration under the branch's own permitted
  renamings.  With the policy part dropped the branch counts fall to five and
  four.  FORCED.  Falsifier: the two policy branches having different
  configuration keys; the branch counts not falling when the policy part is
  dropped; or the branch key not being the only sanctioned quotient of
  branches.
- S1-3 (the generator space, and its prices).  What the run may do to a branch
  from that branch alone is not decided by anything the run has declared, so
  this stage declares a finite space of generators and prices each in
  capabilities.  A generated challenge is at most one inscription of the
  declared domain, supplied; whether that inscription is also retained; and at
  most one demand that two named retained wholes of the branch be internally
  separable in the declared sense.  The space has three coordinates — the
  source of the next inscription, whether it is retained, whether a demand is
  imposed — and **twelve points**.  Four capabilities are declared: that the
  process and not only the caller supplies; that the process and not only the
  caller admits, which is the capability the further-mark candidate of
  Challenge 3 was priced at, read as its admission half because supply and
  admission are never conflated; that the next presentation is computed from
  the branch's admitted state; and that the process and not the caller imposes
  a requirement.  A generator is one step exactly when its capability count is
  one, and a candidate of two or more bundles capabilities and is refused as
  one step, so a generator that both supplies and retains is refused.  NOT
  FORCED: the space is declared and a different space is available.  Falsifier:
  a space size other than twelve; a generator that supplies and retains costing
  one; or the capability count and the coordinate count disagreeing in this
  space.
- S1-4 (the weakest generator that emits, and the tie under U).  Among the
  generators that emit a challenge on a branch at all, the minimum capability
  count is **one** under both readings and on every declared branch.  The
  generator that costs nothing emits nothing, so it is not eligible, exactly as
  the refusing policy of Challenge 5 was not.  The generator that emits the
  least member of the declared domain the branch has not been presented emits
  on every branch and attains the minimum everywhere.  The generator that
  imposes a demand costs one as well, and whether it emits is computed and not
  declared: it emits nothing on any branch whose only retained wholes are the
  caller's two, that pair having been demanded at Challenge 4 already, and it
  emits on the further-mark branch, whose grouping carries a third tag no
  caller whole introduced.  So the minimum is attained by **one class on every
  branch of reading O and on five of the six branches of reading U, and by two
  tied classes on the further-mark branch of reading U**, both of which are
  retained.  FORCED.  Falsifier: a minimum other than one on any branch; the
  demand generator emitting where the caller's two wholes are the only retained
  wholes; the demand generator emitting nothing on the further-mark branch; or
  a tie anywhere under reading O.
- S1-5 (the first challenge, and that it is the same on every branch).  The
  first challenge the enumeration generator emits is the same inscription on
  every declared branch and under both readings: `<|b>`, the least member of
  the declared 144-member domain, in that domain's own order, that the caller's
  presented record does not carry.  It has **one mark and depth one** — a
  further mark and not a deeper nesting.  FORCED.  Falsifier: two branches
  whose first challenge differs; a first challenge of depth greater than one;
  a first challenge carrying other than one mark; or a first challenge already
  in the presented record.
- S1-6 (the generator imports no object-language structure).  The challenge the
  weakest emitting generator emits does not move when the branch's
  configuration is replaced by that of any other declared branch, under either
  reading, so the generator reads no component of any state: not a placement,
  not an address, not a judgment, not a profile.  Every value it does read is
  metatheory the run has already declared — the domain enumeration of
  Challenge 5 and the record of what the caller has presented — and the run's
  own census of functions returning an event finds none in this stage's module,
  so the stage issues no event either.  FORCED.  Falsifier: any substitution of
  one branch's configuration for another's that moves the emitted challenge; a
  declared generator input that is a regime, a deep regime, a judgment, or a
  profile; or a function of this stage returning an event.
- S1-7 (determinism, non-repetition, and that the generator does not stop
  early).  The generator is a function of the presented record alone; the
  challenge it emits is not in that record; once an emitted challenge is
  recorded the same challenge is never emitted again, so no branch can be fed
  one inscription for ever; and it emits nothing only when the record already
  carries every member of the declared domain, so a branch that stops for want
  of a next challenge stops because the domain is exhausted and not because the
  procedure gave up.  FORCED.  Falsifier: an emitted challenge already in the
  record; the same challenge emitted twice from records differing by that
  emission; or the generator emitting nothing while some member of the domain
  is unpresented.
- S1-8 (the declared bounds, and the computed round bound).  The stage declares
  a node ceiling of one thousand and reads a branching bound of **three** off
  the three closed rungs' own receipts — the largest number of tied
  non-isomorphic minimum classes any of them produced.  The round bound is then
  computed and not declared: it is the largest number of rounds for which a
  tree of that branching from the declared branch set stays inside the ceiling,
  and it is **four under both readings**, short of the seed's fifteen.  So the
  continuation owes an exact frontier under a declared bound and does not
  attempt fifteen rounds.  NOT FORCED: the ceiling is a declaration, and a
  different ceiling gives a different round bound, which the stage reports.
  Falsifier: a branching bound other than three off the receipts; a round bound
  declared rather than computed from the ceiling and the branch counts; a round
  bound of fifteen or more; or a round bound differing between the readings.
- S1-9 (nothing is run, and nothing is adopted).  This stage accepts no
  augmentation round, adopts no candidate, admits nothing, and issues no event:
  the initial datum and the reading are unchanged on every branch, the
  event-follows relation stays empty on every probe of both grammars, and every
  reported configuration is the replay of an explicit recorded history and is
  certified from genesis.  No branch is stopped, so the stopping conditions are
  not met for either reading and no obstruction is recorded OPEN by this stage.
  FORCED.  Falsifier: a non-empty event-follows relation at any branch; a
  configuration that does not replay from genesis; any round accepted; any
  candidate adopted; or a changed initial datum or reading.
- S1-X (the extrapolation, scored by the next stage).  The next stage runs the
  accepted rounds.  Its first round presents `<|b>` to every branch, and a
  supply changes no admitted state, which this run proved at Challenge 0 and
  again at Challenge 1.  So **no branch will accept an augmentation at the first
  round**: the justified response to a challenge that only supplies is the null
  response, at capability count zero, and the branch set will not grow at round
  one.  The stage that runs the rounds will therefore report termination rather
  than growth — every branch stopping for want of a justified response well
  short of the four-round bound — unless it first declares the further
  capability that lets the process admit as well as supply, which costs a
  second capability and is refused as one step.  NOT FORCED.  Falsifier: any
  branch accepting an augmentation at round one; the branch set growing at
  round one; the first round being refused rather than answered by the null
  response; or the stage reaching the round bound on any branch.
