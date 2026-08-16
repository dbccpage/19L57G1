# Anti-skill inbox

Procedures this repository should refuse to encode as skills.
AuthorityEffect: None. Nothing here is enforced by CI unless a separate
gate is added later under its own review.

## 2026-08-16 — auto-implement from inbox

- **Anti-pattern:** turning an inbox entry into a skill directory without a
  separate reviewed PR
- **Why it is anti:** would let a note acquire authority by being filed
- **Related skill:** skill-inbox (this is its reverse)
- **Source:** same request; keep collection ≠ implementation

## 2026-08-16 — merge on green

- **Anti-pattern:** merging because CI reports green, without an approval
  pinned to the exact head and without watching the state settle
- **Why it is anti:** green is evidence only about what CI inspected. This
  repository merged Lean modules `lake build` never elaborated on three
  consecutive pull requests, each reported as "CI green". A `mergeStateStatus`
  of UNSTABLE means checks are still pending, and a head can move between
  review and merge — so the approval must name a SHA, not a branch
- **Related skill:** pin (this is its reverse)
- **Source:** the defect that motivated the per-module elaboration gate;
  on 2026-08-16 four pull requests were each held until UNSTABLE → CLEAN
  and re-pinned immediately before merging

## 2026-08-16 — trust a committed receipt

- **Anti-pattern:** reading a checked-in report file and treating its
  numbers as a current measurement
- **Why it is anti:** `coverage.json` was tracked, so a fresh clone shipped
  one and `ci/check_coverage.py` read it with no freshness check. Where
  `coverage` is absent from PATH both upstream commands fail silently and
  the gate prints the stale numbers at exit 0. This produced a false pass on
  2026-08-16 (99.20% / 96.92% reported against a true 99.10% / 96.73%), and
  then produced it a SECOND time the same evening when a routine branch
  switch made git restore the committed report over a freshly generated one.
  The file set was identical across that swap, so a file-set check alone
  does not catch it
- **Related skill:** gates (this is its reverse)
- **Source:** observed twice in one session, the second time while building
  the fix for the first

## 2026-08-16 — count by grepping

- **Anti-pattern:** deriving a count of theorems, modules, or claims by
  pattern-matching source text
- **Why it is anti:** a docstring line that happens to begin with the word
  `theorem` was counted as a theorem, twice, in the same review. Counts must
  come from machine resolution — Lean resolving the names, or the compiler's
  own report. The same class of error made a totality invariant tautological
  when the citation checker enumerated its population with the classifier's
  own regex, silently dropping two path-prefixed citations from both sides
  at once
- **Related skill:** claims-audit (this is its reverse)
- **Source:** the grep miscount, and the transport-citation circularity that
  `ci/check_transport_citations.py` now avoids with an independent pattern
