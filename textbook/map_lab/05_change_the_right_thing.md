# 05. Refine the input or weaken the question

[Previous](04_pair_the_questions.md) · [Map lab](README.md) · [Next](06_unique_on_the_image.md)

## Predict first

Triangle is blocked when only blue is kept. Compare these proposed fixes:
keep another copy of blue; keep triangle too; ask a constant question
that returns Yes on every card.

## Three different changes

Keeping a second copy of blue gives the patterns (Yes, Yes) and (No, No).
A/B remain together, so the same triangle conflict remains.

Keeping triangle alongside blue separates all four cards. It adds a
new distinguishing answer to the input and resolves the recovery task.

Requesting “always Yes” can be answered even with no kept questions.
It asks a weaker question. Its success does not mean we recovered triangle.

| Change | What it supplies |
|---|---|
| Duplicate an existing answer | A longer record with the same distinctions |
| Add a question that splits a conflicting class | A finer recorded distinction |
| Replace the requested question by a constant | An easier, different task |

An encoding computed only from the old record cannot distinguish two
items that have exactly the same old record. The encoding receives the
same input in both cases. Reformatting an answer does not create a new test.

## Your turn

Suppose an application needs both color and shape, but its record keeps
only color. Explain the difference between adding a shape observation
and changing the requested report to mention only color.

AuthorityEffect: None. All information comparisons are relative to the
declared questions; no absolute measure of physical information is supplied.
