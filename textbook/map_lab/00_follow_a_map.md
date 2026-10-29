# 00. Follow a map

[Map lab](README.md) · [Next](01_agreement_and_classes.md)

## Predict first

Keep only the blue answer. A and B go to the same recorded value, Yes.
Could a second lookup recover **blue?**? Could it recover **triangle?**?

## Two routes to compare

A **map** here is a function: each input in its domain has one output.
Name the recording map p, the requested-answer map q, and a proposed
lookup g. These letters are short names, not new objects inside the recorder.

There are two routes from a card to a requested answer:

1. Read q directly on the original card.
2. Read its stored p value, then apply g to that value.

Applying one map after another is **composition**. We write the second
route as g(p(x)), meaning “apply p to x, then g to its result.”

The lookup succeeds on the declared domain exactly when both routes
give the same answer on every listed card. Mathematicians call such a
diagram **commuting**. The word describes agreement of outputs, not
physical motion or an order in time.

## A concrete success and failure

Blue can be recovered from the blue record: return its supplied answer.
Triangle cannot: A and B have the same stored blue value but need different
triangle answers. A lookup receives one input Yes; it cannot assign both
No and Yes to that same input.

## Your turn

Keep triangle instead of blue. Which pair blocks recovering blue? State
both routes' required values for that pair.

AuthorityEffect: None. The recording and requested-answer maps are supplied.
