# What would close the instance channel of OB-1?

AuthorityEffect: None. **Specification of missing work, not new proof.**
The four-stage result is Outcome C: the searched procedures and their failure
boundaries are recorded in `CLAIMS.md`. Native admission and obligation meaning
remain unproved. The two targets below are necessary parts of a positive
instance-channel result; completing them must also preserve E3, E4, and a
proved dynamics classification for the same generator.

## First distinguish the two questions

Literal E2 requires a new member of sealed `reqs` without an `impose` at its
origin. This channel is already closed negatively by
`research/endogenous_demand/`: successful replay introduces such a member only
through its corresponding event. None of these four stages changes `reqs`.
A positive instance result therefore cannot claim to satisfy that literal
condition. It would address the explicitly broader owed-separation reading,
called E2' in `ob1_e2_restatement/FINDING.md`.

That diagnostic recommends a wider negative search but explicitly supplies
neither a Lean formalization of E2' nor a general impossibility proof. Its
finite examples cannot decide every represented instance program. In
particular, occurrence of `admitInst` proves an event was used, not that its
source was external: `InstanceDemand.lean` keeps that distinction explicit.

The native operations presently establish two different facts:

```text
derivable r i = (i is stored in r) or (i's form has a uniform rule)
stepE r event = application of an event already given to replay
```

Neither definition itself chooses or produces the next event. A uniform rule
also does not inspect two premise instances and perform their composition.
This is why successful replay and a computed output do not yet establish E1.

## Target 1: native production of an admission event

State a precise class of represented programs and their interpretation using
the existing data, forms, instances, and uniform rules. The class must include
the instance-program shape allowed by E1, and its membership conditions must
not assume the desired conclusion. Explain which existing admitted structure
gives each interpreted operation its meaning. A new unrestricted event emitter
declared in the host is an additional rule, even when deterministic.

Then exhibit an admitted program, a reachable seed, and a concrete production
step, with Lean proofs of all of the following:

1. The program and its inputs are well-formed and occur in a history replayed
   from genesis. Every operational parameter is accounted for by that admitted
   representation and the fixed interpretation.
2. Reading the admitted instruction and premises produces the claimed output
   under that interpretation. The interpreter takes no externally supplied
   desired pair or desired output and does not select a target by inspecting
   the observational profile. The exact permitted input interface is part of
   the specification, rather than a test with a convenient input omitted.
3. The represented result gives rise to the actual existing instance-admission
   event, and applying that event stores the payload in the predicted state.
   Establish the connection to the existing grammar; do not define a new
   predicate named "native" to mean that the present host wrapper ran.
4. The relevant production history contains no externally supplied demand or
   encoded instruction that merely copies a previously supplied demand into
   another field. The origin of an event must be represented and justified;
   forbidding all instance-admission events would instead exclude the very
   channel being tested.

The missing part is chiefly item 3. Stage 3 already proves exact decoding and
two-step computation agreement for functional operand graphs, plus retention
of successful execution outputs without that functionality premise. It also
proves `represented_run_keeps_graph`: the existing represented execution does
not write its computed result to the regime. Our wrapper performs that write.

There is a specific obstruction to a tempting shortcut:
`Emitter.no_native_join_rule` refutes the universal assertion that an enabled
two-edge output is natively derivable in every well-formed state. Its reachable
unruled seed has the instruction and premises but lacks the conclusion.
Covering the output form makes every tuple on that form derivable; it does not
make the uniform rule perform the admission event. A successful next attempt
must resolve this gap or prove it unavoidable for its stated class.

## Target 2: why the produced payload is an owed separation

Give an exact interpretation relating an admitted output instance to a pair
that the regime owes a separation. Justify that role from the admitted
construct and its permitted semantics. Calling form 0 or form 5 a "demand"
in a reader is currently a convention. A pair being collapsed proves an unmet
separation *if one is owed*; it does not establish that anything owes it.

For the same production step as Target 1, prove a concrete reachable witness
with these properties:

1. The output is a well-formed admitted instance with a proved reading as the
   proposed obligation. Its distinct endpoints are admitted data.
2. At the state **after generation**, the endpoints are still collapsed. This
   excludes the unruled singleton, which separates its own endpoints when
   stored. The covered examples already supply this geometric control.
3. The obligation is not an imported demand or a relabeling of one previously
   supplied. State what is newly generated under the obligation interpretation
   and prove it. Fresh storage, fresh derivability, and fresh obligation are
   separate predicates. The covered examples have fresh storage but their
   payloads were already derivable; this fact alone settles neither the
   presence nor the absence of a newly generated obligation.
4. With this meaning in place, the step satisfies the broader E2' and E3,
   without claiming that sealed `reqs` acquired a new entry.

The required meaning is operational and relative to the stated grammar and
admitted construct. It is not a requirement to prove an unrestricted account
of what every intelligent observer ought to want. Conversely, a host decision
that an arbitrary collapsed pair ought to be separated is not a derivation of
that operational meaning.

## Finish with one joined witness, not separate conditional examples

Use the **same** native generator and obligation interpretation to prove:

| Obligation | Required evidence |
|---|---|
| E1 and E2' | The admitted construction, its interpretation, and the event-production bridge above, with a concrete firing history. |
| E3 | A reachable, non-imported obligation whose endpoints remain collapsed after generation. |
| E4 | An existing `validResponse` to that pair and exact replay of genesis, generation, and response to the claimed final regime. |
| Dynamics | A termination proof or sustained-production proof for this generator and the explicitly stated iteration law. |
| Executable mirror | Python reconstruction of the admitted program and whole history, with controls rejecting imported targets, missing instructions, malformed payloads, and false response claims. |

Retain both reading analogues and identify any maps used to compare them;
neither is a replay of a sealed challenge history with events silently removed.
Current Lean response and replay witnesses can be reused only when their
premises apply to the newly justified generator.

Stage 4 already supplies `stable_by_budget`, `stable_after_budget`, and
`terminal_least` for our repeated host emitter on fixed data/forms with no
interleaved events. It can classify a future native implementation only after
the semantic connection to that exact procedure is proved. Carrier growth,
responses between rounds, or a different program require their own argument.
The four-data chain loses graph functionality after round one, so the
functional computation bridge cannot simply be reapplied at every round.

A raw stored payload may remain after a response; E4 does not require deleting
it. Claiming a continuing queue of *unmet* obligations would additionally need
a proved discharge/update interpretation. That stronger queue claim is not
silently added to the finite witness required by the brief.

## Alternative completion: prove a scoped impossibility

A negative completion must name a natural, nonempty class of admitted
constructs, account for the obvious candidates and the represented-instance
channel, and prove that no member satisfies E1, E2', and E3 together. Give the
failure clause for each allowed shape. State exactly which encodings and
interpretations the quantifier covers.

Requiring demands to be `reqs` members only repeats the existing result.
Excluding every `admitInst` by definition strengthens the requested condition.
Checking only an unruled singleton misses the covered controls. Declaring
every conceivable interpreter impossible without a defined language or class
does not provide a theorem statement.

If no native event-production semantics or obligation interpretation can be
obtained inside the current constitution, identify the missing operation and
prove the obstruction for the justified class. Adding that operation by hand
would produce a conditional extension of the grammar; it would not close OB-1
as a derivation in the sealed grammar. `NoGo.lean` is that scoped negative
for stored form-0 ternary instructions and for the Stage-1 pair-instance
encoding. Native store without that tuple's `admitInst` is a grammar
extension. **OB-1 remains OPEN outside `InClass` and `I1Class`.**
