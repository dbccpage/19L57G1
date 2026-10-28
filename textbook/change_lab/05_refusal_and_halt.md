# 05. Refusal and halt

[Previous](04_proposal_and_execution.md) · [Change lab](README.md) · [Next: legal histories](06_records_and_histories.md)

## Two records that can look like “stop”

The passage has separate events for **refusal** and **halt**. Predict
whether they have the same effect on a later funded, permitted repair.

A refusal records a currently active pair. It changes no observation,
retention, protection, budget, or halt flag. It can be recorded even if
a structural repair exists. This kernel's refusal guard requires activity;
it does not additionally require exhaustion of the repair menu.

A halt sets the halt flag. Once halted, this machine leaves every later
event inert. That includes attempts to change its budget or permission.

## Replay the two branches

Start with `[A]`, all pairs protected, B/C active, budget zero, permission off.

| Branch | Later events | Final result |
|---|---|---|
| Record refusal of B/C | Turn permission on; set budget one; append [B] | B/C separates; the old refusal record remains |
| Halt | Attempt those same three events | No later change; B/C is still active |

A stored refusal is a historical record. After the first branch's repair,
the current observation separates B/C even though the refusal register
still mentions it. Re-evaluate the current state rather than reading
the register as a list of current failures.

Halting does not itself resolve a distinction. It stops this transition
system from taking further action under its declared event rules.

## Do not import another kernel's refusal rule

The represented-world model in Unit 45 uses a stronger refusal condition:
its named obstruction includes exhaustive failure of its repair menu.
The [model map](MODEL_MAP.md) records that difference. A shared word does
not make the guards identical.

## Your turn

Explain why “a refusal is recorded,” “no repair is available,” and “the
machine is halted” are three different statements. Give the evidence
you would inspect for each in this passage model.

AuthorityEffect: None. Refusal and halt follow their distinct supplied guards.
