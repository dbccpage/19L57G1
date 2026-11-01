# 59. Change and compare

Use the same three-card model. Ask “Is A blue?” Its current answer is 1.
An **intervention** here is a supplied procedure that returns a changed
model. We compare the formula's answer before and after that procedure.

| Candidate procedure | Answer before | Answer after |
|---|---|---|
| Keep the model unchanged | 1 | 1 |
| Remove A from blue | 1 | 0 |
| Remove C from blue | 1 | 1 |

<details><summary>Predict: does the middle row show that A was not blue before the change?</summary>

No. The earlier model answer was 1. Removing the fact changes the later
answer. A claim about the earlier model and a claim about the changed
model refer to different inputs.

</details>

## What the witness establishes

The middle procedure is a **discriminating witness** for this formula at
this model: it changes the answer. If our allowed menu contains only
“keep,” we find no witness. Adding “remove A” changes that result.
No witness in one menu means no witness found in that menu, not that
every possible procedure has been ruled out.

The Python search tries each candidate separately from the original model.
Trying “add A” and “remove A” this way differs from executing them in order.
A sequence needs an explicit starting model and an order of updates.

## A model change and a physical trial

The source calls its menu-relative predicate `has_empirical_reference`.
Its executable check compares model evaluations. It does not operate a
physical card, record a sensor reading, or validate a model-to-world link.
The [evidence route](08_from_a_model_to_a_trial.md) explains the additional
procedure and records needed for an actual trial.

Next, compare [agreement between reports](60_agreement_and_the_guard.md)
with evaluation of the underlying model.

AuthorityEffect: None. Supplied model interventions and menu-relative checks.
