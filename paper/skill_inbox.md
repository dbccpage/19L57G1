# Skill inbox

Candidates only. AuthorityEffect: None. Nothing here is approved or scheduled.

## 2026-08-16 — skill-inbox / anti-skill-inbox

- **Need:** capture skill ideas and their reverses without implementing them
- **Proposed behaviour:** append-only markdown inboxes
- **Not in scope:** creating skill dirs, CI enforcement, ledger entries
- **Source:** explicit request for simple dual skills on the clean repo

## 2026-08-16 — paper-numbers gate

- **Need:** no gate compares numbers written in `paper/` to machine output,
  which is exactly why section 12's receipts went stale unnoticed — 82 vs
  435 tests, 51 vs 1314 axiom reports, and coverage figures that had
  drifted downward, so the stale text was flattering
- **Proposed behaviour:** a CI check binding specific `paper/` figures to
  `artifacts/claims.json` keys and to freshly measured gate output, in the
  style of `ci/check_transport_citations.py` — population enumerated
  independently of the classifier
- **Not in scope:** editing the paper automatically; a number that diverges
  is a finding for a human, never a silent rewrite, since silent rewriting
  would destroy the record that the paper was once wrong
- **Source:** the `claims-audit` skill has no authority and cannot gate;
  the divergence it found on 2026-08-16 had to be corrected by hand

## 2026-08-16 — parked-module declaration census

- **Need:** close the standing "elaboration is not auditing" residual. Every
  module under `lean4/Derivation/` elaborates against a pinned census, but a
  module the root does not import emits no `#print axioms` report, so
  "axiom-clean" covers only the 1314 enumerated reports
- **Proposed behaviour:** enumerate declarations from the ELABORATOR, not
  from text, and emit a report per parked declaration
- **Not in scope:** any regex over `.lean` source. That approach is already
  known to fail here — a docstring line beginning with the word `theorem`
  defeated a grep count twice — and adopting it would close the residual
  badly rather than closing it
- **Source:** recorded OPEN in CLAUDE.md and in paper section 12; `leagent`
  (`leanprover/leagent`) is a candidate route, tested only through Lean
  v4.32.2 against this repository's v4.33.0

## 2026-08-16 — cross-reference gate, resolved against the merge result

- **Need:** a `paper/*.md` file can cite a sibling that exists only on a
  branch. Nothing catches it. The ascent analysis shipped in a pull request
  citing the representative-selection analysis, which was written but
  unmerged, so the citation was dead on `main`. A reviewer caught it; no
  gate did. (Those two documents are named here in prose rather than by
  path, because the gate proposed below treats any written-out
  `paper/…​.md` as a pointer a reader will follow, and will not distinguish
  a live citation from a narrative mention of a dead one — see the note on
  its population below)
- **Proposed behaviour:** for every `paper/*.md` path cited inside
  `paper/`, verify the path exists **in the merge result** — the state CI
  actually builds — and fail by name otherwise. Same genre as
  `ci/check_transport_citations.py`, which already binds citations to
  sources, but for intra-repository document paths rather than Lean
  declarations
- **Not in scope:** judging whether a citation is *apt*, rewriting or
  inserting citations, and any authority over merge order. It reports a
  dead path; it does not decide whether the sibling should land first
- **Known limit of the population:** the gate cannot tell a live citation
  from a prose mention of a path that is deliberately dead — an incident
  narrative, a withdrawal notice, a worked example. Both look identical.
  The resolution taken is that prose must not write a `paper/…​.md` path it
  does not want a reader to follow, and should name such documents
  descriptively instead. This entry had to be rewritten on exactly that
  ground, which is the first evidence the constraint bites
- **Source:** the incident above. An earlier version of this entry claimed
  that a working-tree check "**passes** on the very defect it is meant to
  catch, because the cited file is present on the branch doing the
  citing", and that "my own post-incident sweep … would not have found the
  original". **Both are WITHDRAWN — they are false.**
  `representative_selection.md` was on its own branch, present on neither
  `main` nor the citing branch, so a plain existence check on the citing
  branch would have failed and caught it. The sweep passed for a duller
  reason: it was run *after* the citation had already been removed. The
  motivation is therefore weaker than claimed — a plain path-existence
  check suffices for this incident, and the merge-result framing is a
  strictly stronger property covering the case where `main` moves under a
  branch, not a necessity for the defect that occurred. Recorded this way
  because a gate justified by a trap that did not apply is a gate built on
  a false premise
