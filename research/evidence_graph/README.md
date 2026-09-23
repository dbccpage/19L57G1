# evidence_graph

AuthorityEffect: None. An index of source statements and independently checked
evidence. This tree consumes existing sources read-only and does not repair
their claims, change the seal, or confer authority through an aggregate pass.

The source snapshot and population are frozen before evidence dispositions
are assigned. Exact inherited prose is represented by a resolving source span,
its snapshot, Git blob, file digest, and span digest. It is not copied here.
Import and reference edges do not establish a semantic bridge.

The implementation is in progress. The completion record will distinguish
source coverage, actual replay, fresh compiled statements, unresolved scope
matches, and the stronger condition of adequate support for every headline.

The independent entry point is `python verify.py --check`, run here. The
canonical verifier checks this tree's local inputs, tests, strict typing, and
its explicitly named local Lean reports. Checks of other trees continue to
belong to those trees. Regenerating pins is a separate deliberate operation.
