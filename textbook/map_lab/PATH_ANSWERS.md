# Path practice answers

Attempt [the questions](PATH_PRACTICE.md) first.

1. B → C → C → A. The shorter history gives B → C → A. The endpoints
   agree; the event lists and intermediate records differ. An inert stay
   does not disappear from the longer history.
2. Write 8, then 8, then 2. These are three supplied native set-budget
   events. Repeating the first write throughout would end at budget 8,
   while the encoding of the final source state A has budget 2.
3. Yes: 2, 5, 8 are distinct. No: these states have one genesis core and
   the same specified native observation. A/B are a blocking pair, as are
   A/C or B/C. Distinct stored budgets are not distinct native readings.
4. Decode 2 as A, 5 as B, 8 as C. The task supplies no requirement at 3;
   several total extensions are possible. Reading budget changes the
   target observation. It no longer reads only the native core, so the
   earlier impossibility statement does not apply to this new requirement.
5. The source now has only one observation value, Yes. A map on that
   one-value domain is injective: no two distinct source answers are
   merged. With the state question there were three distinct answers;
   making their images equal lost faithfulness. Keep the observation's
   declared value domain with the claim; do not require injectivity on
   extra unused values without stating that stronger requirement.
6. No: the first after-state is not the second before-state. Use the
   state with [0] as the second before-state, and that same state with its
   terminal flag true as the second after-state. Halt retains the
   occurrence. The repaired rows join and each event reaches its recorded
   target.

For transfer, declare source and target observations and a map between
their answer values. Require observation agreement after encoding, and
faithfulness if distinct source answers must survive. The budget encoding
has correct step squares and distinct states but loses the state-answer
under the specified native observation. Permitting a target budget reader
recovers these used codes. That changes the observation requirement; it
does not disprove the theorem about the original one.

The dial and the paper switch are formal examples with supplied rules.
To apply a model to a physical device, declare how its states, events and
readings are obtained, then collect observations under that protocol. The
[Reasoning-lab evidence route](../reasoning_lab/08_from_a_model_to_a_trial.md)
explains that additional work.

AuthorityEffect: None. These are worked answers, not recorded novice
performance or an empirical validation.
