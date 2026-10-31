# 12. Preserve the requested observation

Return to the earlier Map-lab question: can one stored answer recover a
requested answer? Here the target observation is the available answer;
the source's current switch state is the requested answer.

**Predict:** can a lookup given the same native observation in both cases
return 0 for one case and 1 for the other?

<details><summary>The blocking pair returns</summary>

It cannot. A function gives one answer for each input. The encoded
states form a blocking pair: equal available answers, different requested
answers. This is the same recovery obstruction as the blue-only card
record that loses triangle information.

</details>

## What would a stronger translation require?

Declare the source observation, the target observation, and the rule
translating observation values. Require that encoding a source state and
then observing it gives the translated source observation. A **faithful
observation map** keeps distinct source answers distinct.

With the source observed by its own state, faithfulness must keep the
answers 0 and 1 apart. A constant observation map would satisfy a weaker
agreement equation by erasing the distinction. It fails this requirement.

## Why changing only the encoding is insufficient here

The switch can go from 0 to 1 and back. Such a return route is a **cycle**.
The native research proves that every commuting translation into this
passage gives states on a source cycle the same **core**: the fields
other than budget and license. Its specified observation reads only that
core. Therefore no commuting translation of this state-observed switch
can preserve its two answers faithfully with that target observation.

This conclusion concerns this passage rule, this observation, and those
translation requirements. It does not rule out other target machines or
an observation allowed to read budget. The passage's identity translation
preserves its own observation faithfully, so the definition has a positive
example as well as an obstruction.

**Try a change:** ask only “is the switch in either allowed state?” Both
source answers are Yes. The constant target answer can preserve this
weaker question; it still cannot recover the original state question.

Continue with [13. Labels do not certify steps](13_labels_do_not_certify_steps.md).

AuthorityEffect: None. The all-translation cycle conclusion is NB-16,
using NB-8. Book checks instantiate the exact source theorem and the
two-code blocking pair; they do not supply a physical correspondence.
