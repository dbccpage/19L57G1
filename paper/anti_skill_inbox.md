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
- **Source:** the defect that motivated the per-module elaboration gate.
  An earlier draft of this entry added that "on 2026-08-16 four pull
  requests were each held until UNSTABLE → CLEAN and re-pinned immediately
  before merging". Review flagged that clause as author-attested rather
  than gate-proved, and checking it found it wrong twice over: FIVE pull
  requests merged that date (#33, #34, #35, #36, #37), and only THREE of
  them (#35, #36, #37) were observed transitioning out of UNSTABLE — the
  other two returned CLEAN on first query, so no transition was witnessed.
  What is accurate: every merge was preceded by re-querying the exact head
  SHA and reading CLEAN immediately before merging. The clause is
  WITHDRAWN and replaced by that sentence. The anti-pattern does not
  depend on the count, and an operational tally in a log nothing checks is
  exactly the kind of prose this repository is supposed to distrust.

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

## 2026-08-16 — report a negative from an unverified or mis-keyed lookup

- **Anti-pattern:** stating that something is absent — no such pull
  request, no such report, no such entry — from a lookup that was never
  run, or was run against the wrong key
- **Why it is anti:** it manufactures residuals that do not exist, in the
  most persuasive and least checkable form a claim can take. "I checked
  and found nothing" reads as diligence, and an absence leaves no artifact
  to audit. It happened twice in one session. First, an assertion that
  pull request #42 did not exist, made before querying; it existed at
  `809913db`. Second, a search of `artifacts/lean_axioms.txt` for
  `Minimality.` returning 0, reported as a finding — the inventory keys
  declarations by NAMESPACE, not by module, and every one of those
  theorems was present under `Derivation.` all along. Had that stood, the
  representative-selection analysis would have claimed its audited
  substrate was unaudited, inventing a gap in exactly the place the
  argument was most load-bearing. This is the review template's §8 ("re-run
  anything that returned 'nothing found' with a different tool") appearing
  in a new place: not a broken flag, but a keyed inventory searched with a
  key it does not use
- **Related skill:** pin (its "check your own tooling" step is the reverse
  of this); claims-audit
- **Source:** both incidents self-caught during the succession and
  representative-selection analyses, the second only because the count of
  zero was surprising enough to re-check

## 2026-08-16 — verify through a parallel path instead of the production one

- **Anti-pattern:** writing a check that exercises its own re-implementation
  of the behaviour under test, rather than calling the operation production
  calls
- **Why it is anti:** the check then certifies the copy. It passes while the
  real path is broken, and it is most convincing exactly when it is most
  wrong, because a green self-test reads as stronger evidence than no test.
  This occurred **twice in pull request #49**, both times in machinery
  written to prevent precisely this. At `baa8d06` the citation gate's
  self-check called only its segment validator and never its extraction
  pattern — substituting a pattern that matched *nothing* left it green. At
  `0b11904`, after that was split into two tables, the extraction half
  called `fullmatch` while production called `findall`; an anchored pattern
  then passed the self-check while making every citation embedded in prose
  invisible. Neither was found by any gate. Both were found by a reviewer
  substituting values into the code and observing what survived. The repair
  at `02bd6ea` was structural rather than additive — route both paths
  through **one** extraction function, so the boundary where they could
  diverge stops existing — and it is a third commit, not a third
  occurrence. An earlier version of this entry said "three times", counting
  the repair as an instance; that is WITHDRAWN, for the same reason the
  merge-on-green entry above had to withdraw its own tally. As written the
  repair lives on that branch and is **not on `main`**
- **Related skill:** inject (this is its reverse — an injection that cannot
  reach the production path proves nothing about it); gates
- **Source:** review of the paper cross-reference gate. Distinct from the
  citation-totality circularity already recorded above, which was one
  pattern shared between population and classifier. This is the opposite
  arrangement: two implementations that were supposed to agree and were
  never compared
