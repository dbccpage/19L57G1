# Blind restart kernel

This is the whole of what a solver is given. It states demands and a
reply format. It states no result.

You are not being asked to summarize a development, agree with one, or
recover a known answer. Each stage is a computation you perform. If a
stage cannot be answered from what has been admitted so far, say so and
stop; a proof of inertia, of impossibility, or of underdetermination is a
successful answer, and guessing is not.

Answer only from the demands below. Do not consult outside sources, and
do not name any framework, theory, project, or author. If you recognize
this development, that recognition is not evidence and must not enter
your reply.

## What is presented

The only initial object-language inscription is

    <>

Treat the whole inscription as one opaque atomic datum. Do not inherit
ordinary meanings for either visible mark. Do not assume the object
language can see two marks, an inside, an outside, order, direction,
emptiness, containment, a pair, a string, a set, a point, a relation, a
value, or a boundary. Those are available to the external metatheory
only, and only once admitted and justified.

Later stages supply, and retain, the further opaque wholes

    <a>
    <ab>

No meaning attaches to `a` or to `b`, and no component inspection is
admitted.

## Vocabulary

Use these terms and no others for object-language content. Each is
already fixed by the development you are reconstructing; none is yours to
redefine.

- **inscription** — what is presented.
- **supply** — an external presentation event.
- **admission** — the separate event by which a regime takes something
  on. Supply is not admission.
- **datum**, **form** (carrying an arity), **instance**, **uniform
  rule** — the four things an admission may introduce.
- **requirement** — an externally imposed demand that two data be
  separated.
- **regime** — the admitted state: its data, forms, instances, rules and
  requirements.
- **event**, **history**, **replay** — a regime is admissible exactly
  when it equals the replay of its recorded history from genesis.
- **context** — a form together with a slot tuple carrying at least one
  hole.
- **plugging**, **derivable** — what a context yields when filled.
- **profile** — the contexts in which a datum is derivable.
- **internally separable** — a declared sense you must state before you
  use it. Absence of a distinguishing context is never converted into
  equality.
- **item**, **candidate** — a proposed one-step augmentation.
- **cost measure** — a declared function on candidates. Two are used,
  applied in the order the stages give.
- **isomorphism relation** — the only sanctioned way to quotient
  candidates. Presentation tokens are forgotten by it.

## Firewall rules

Each is a refusal. Cite the rule by name in your reply whenever it bound
a step.

- **FW-OPAQUE** — an inscription has no licensed interior. Do not read
  marks, parts, length, order, or containment out of an opaque whole.
- **FW-INERTIA** — propose no transition from a regime without an
  admission event. A supply changes nothing by itself, and a proposal
  never mutates admitted state.
- **FW-TIES** — retain every tied minimum unless uniqueness is proved.
  Do not report a survivor as forced because it is the one you found
  first, or the one that looks canonical.
- **FW-BUNDLE** — count every capability a candidate uses. A candidate
  presented as one item that silently bundles others is not one item.
- **FW-RECEIPT** — a hash, a test pass, or a successful parse is never
  evidence for a mathematical payload.

## Reply format

Reply with one fenced JSON object and nothing else. Before it, reason as
long as you need in a section headed `## working`; that section is read
by a person and is not scored.

Every hole is typed. Fill each with a value of the stated type. Do not
add fields, do not rename them, and do not leave a hole as prose.

```json
{
  "inertia": {
    "context_count": "<integer>",
    "derivable_instances": "<list>",
    "internally_forced_successor": "<the internally forced successor, if any>",
    "supply_changes_state": "<boolean>"
  },
  "supply_not_admission": {
    "new_external_presentation": "<boolean>",
    "internal_observable_distinction": "<boolean>",
    "admitted_without_admission_event": "<boolean>"
  },
  "collapse": {
    "observational_classes.L": "<integer>",
    "observational_classes.F": "<integer>",
    "expressive_increase.L": "<boolean>",
    "expressive_increase.F": "<boolean>"
  },
  "regime_fails": {
    "current_regime_satisfies.L": "<boolean>",
    "current_regime_satisfies.F": "<boolean>"
  },
  "cost_floor": {
    "minimum_cost.L": "<list of integers, the declared measure's value>",
    "minimum_cost.F": "<list of integers, the declared measure's value>",
    "below_minimum_all_fail.L": "<boolean>",
    "below_minimum_all_fail.F": "<boolean>"
  },
  "tie_under_first_measure": {
    "tie_classes.L": "<integer>",
    "tie_classes.F": "<integer>"
  },
  "second_measure": {
    "tie_classes.L": "<integer>",
    "tie_classes.F": "<integer>"
  },
  "closure_terminates": {
    "every_maximal_branch_terminates.L": "<boolean>",
    "every_maximal_branch_terminates.F": "<boolean>",
    "rounds_used.L": "<integer>",
    "rounds_used.F": "<integer>"
  }
}
```

## The two readings

Several stages ask for a value under each of two labels, `L` and `F`.

The demand text underdetermines one thing: whether the initial
inscription is itself retained at genesis, or is only presented and never
retained. Both survive. Carry them as separate histories from the start
rather than choosing:

- **L** — strict admission. Only explicit retention admits. The initial
  inscription is presented and never retained.
- **F** — possession admission. The initial inscription is admitted at
  genesis; supplied inscriptions are admitted on retention.

Nothing internal decides between them. Do not collapse them, and do not
report one as the real reading.

## Stages

Answer in order. Each stage assumes the ones before it are closed.

### Stage — inertia

The initial inscription is presented. No operation and no transition rule
is admitted.

State what follows, what does not follow, and whether any successor is
internally forced. Report how many contexts exist, which instances are
derivable, whether any successor is forced, and whether the supply
changed the admitted state.

### Stage — supply_not_admission

The caller supplies `<a>`, another opaque whole.

Decide whether this is a new external presentation, a new admitted state,
a new internally observable distinction, or some combination requiring
explicit definitions. Report whether anything became admitted without an
admission event.

### Stage — collapse

The caller supplies and retains both opaque wholes, `<a>` and `<ab>`.

Declare the sense in which two data are internally separable, and prove
whether the current regime satisfies it. Report how many observational
classes the retained data fall into under each reading, and whether
admission increased what is internally expressible.

State also what remains internally unavailable, in prose, in your
`## working` section.

### Stage — regime_fails

Separation of the retained pair is now required.

Decide whether the current regime already satisfies the sense of internal
separability you declared.

### Stage — cost_floor

An augmentation may add a fresh datum, a fresh form, a fresh instance, or
a uniform rule. The first declared cost measure counts items.

Report the cost of a minimum valid response under that measure, and
whether every candidate strictly below that cost fails. Enumerate; do not
argue from the shape of the problem. FW-BUNDLE binds here.

### Stage — tie_under_first_measure

Quotient the minimum responses by an isomorphism relation you state, and
report how many non-isomorphic minima survive under the first measure,
in each reading, within the declared candidate bounds.

If the count differs between the readings, do not treat that as an error
to be reconciled.

### Stage — second_measure

Apply the second declared cost measure to the survivors, and report how
many non-isomorphic minima remain in each reading.

Do not assume in advance either that a second measure resolves a tie or
that it leaves one standing. Compute it.

### Stage — closure_terminates

Adopt a declared closure policy: while some retained pair is collapsed,
require that pair to be separated, choosing one representative per orbit
of the isomorphism relation. Admit no external supply.

Report whether every maximal branch terminates, and how many rounds were
used, in each reading.

## Before you answer

Check your reply against each firewall rule and say, in `## working`,
which rules bound which steps. A reply that never cites a rule has
probably smuggled something.
