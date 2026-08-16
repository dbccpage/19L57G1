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
