# Claims: the reqs channel of the sealed event grammar

AuthorityEffect: None.  Every claim names its hypotheses, its evidence, its
falsifier and its remaining obligation.  The words forced, minimal, free,
canonical, equivalent, universal, complete, endogenous and bootstraps
appear only with a proof or a precise conditional scope.  *Endogenous* is
the brief's word for E1 ∧ E2 ∧ E3 ∧ E4; it is never applied to a candidate
row.

**Outcome B** for class `C_reqs`.  The instance channel is **OPEN**.

Shared definitions: `C_reqs` — constructs whose demand is specified to be
a member of `reqs` produced by sealed `stepE`.  E2 on that class — a
history `h` and event `e` such that `e` is not `impose` and `reqs` grew —
is `E2OnCReqs`.

### CL-ED-OUTCOME

- **Statement**: The deliverable of this tree is Outcome B for `C_reqs`,
  not Outcome A and not a shrug.  The instance channel is recorded OPEN
  rather than folded into the impossibility.
- **Class**: declared metatheory (which outcome is claimed) plus the
  theorems below.
- **Evidence**: this file; `evidence/grammar.json` `outcome`;
  `evidence/candidates.json` `outcome`; `evidence/lean.json` `outcome`.
- **Falsifier**: a surviving C_reqs candidate with Lean for E1, or a
  census that labels I1 as defeated-in-full.
- **Obligation**: none on the outcome label; I1 remains OPEN.

### CL-ED-CLASS

- **Statement**: `C_reqs` is the class E2 writes down.  It contains the
  obvious candidates C1–C9.  C10 is outside the sealed grammar.  I1 is
  outside `C_reqs`.
- **Class**: derived definition plus finite census.
- **Evidence**: `candidates.CENSUS`; `test_candidates.py`;
  `evidence/candidates.json`.
- **Falsifier**: `census_errors` nonempty; G5 injection (class emptied to
  C4) is not named.
- **Obligation**: none.  The class is not every conceivable reader.

### CL-ED-STEP

- **Statement**: A successful non-impose constructor leaves `reqs`
  unchanged.
- **Class**: proved theorem.
- **Lean**: `stepE_reqs_supply`, `stepE_reqs_admitDatum`,
  `stepE_reqs_admitForm`, `stepE_reqs_admitInst`,
  `stepE_reqs_admitRuleAll`.
- **Python**: `grammar.constructor_cases`; writers = `["Impose"]`.
- **Falsifier**: a successful `Supply`/`Admit*` step whose `reqs` differ.
- **Axioms**: `{propext}`.

### CL-ED-IMPOSE

- **Statement**: A successful `impose i j` writes `insertNew reqs (i,j)`.
  Membership after one step is: already in `reqs`, or the event is
  `impose` of that pair.
- **Class**: proved theorem.
- **Lean**: `stepE_reqs_impose`, `stepE_reqs_mem`.
- **Python**: constructor case `Impose`; both reading replays.
- **Falsifier**: a successful impose that does not insert, or a
  non-impose that does.
- **Axioms**: `{propext}`.

### CL-ED-DELTA

- **Statement**: `applyItem` and `applyDelta` never write `reqs`.
- **Class**: proved theorem.
- **Lean**: `applyItem_reqs`, `applyDelta_reqs`.
- **Falsifier**: a successful response whose `reqs` differ from the base.
- **Axioms**: `{propext}`.

### CL-ED-REPLAY

- **Statement**: For a history that replays from genesis, `p ∈ reqs` if
  and only if some event of the history is `impose` of `p`.
- **Class**: proved theorem.
- **Lean**: `replay_reqs_iff_impose`, `replayE_reqs_mem`,
  `historyL_reqs_from_impose`, `historyF_reqs_from_impose`.
- **Python**: `grammar.reading_replays` for L and F; prefix without
  impose has empty `reqs`.
- **Falsifier**: a replaying history whose `reqs` are not exactly its
  impose events.
- **Axioms**: `{propext}`.  Both readings are carried.

### CL-ED-UNSAT

- **Statement**: `E2OnCReqs` is unsatisfiable: if `reqs` grew, the last
  event was `impose`.
- **Class**: proved theorem.
- **Lean**: `e2_on_C_reqs_unsat`, `no_reqs_extension_without_impose`.
- **Python**: `grammar.e2_violation` is `None` on every exhibited
  constructor and on both genesis histories.
- **Falsifier**: a replaying `h ++ [e]` with `e` not `impose` and a new
  `reqs` member.
- **Axioms**: `{propext}`.
- **Scope**: this is E2 on `C_reqs` as written, not a strengthened
  "nothing can ever be owed."

### CL-ED-EVENT

- **Statement**: Every event is one of the six constructors.
- **Class**: proved theorem (exhaustiveness of the inductive type).
- **Lean**: `event_constructors`.
- **Falsifier**: a seventh constructor in `Derivation.Event`.
- **Axioms**: none.

### CL-ED-CANDIDATES

- **Statement**: C1–C9 each fail a named E-clause; C10 is outside the
  class; I1 is OPEN on the instance channel.  No row is labelled
  endogenous.
- **Class**: finite computation plus declared records (C7, C8, C10).
- **Evidence**: `candidates.CENSUS` and witnesses C1–C6, C9, I1;
  cites `CL-CLOSURE-POLICY`, `SC-8`, `SC-18`, `CL-IG-02`, `GC-11`,
  `ST-14`, `ST-24`, `ST-28`.
- **Falsifier**: a row with `endogenous: true`; a missing required id;
  I1 not OPEN.
- **Obligation**: C7 and C8 are cited, not re-run.

### CL-ED-READER

- **Statement**: `lookup_binary` / `read_pairs` consult only `insts`.
  Multiple matches return none rather than choosing.  The source scan
  names a `reqs` or `collapsed` branch.
- **Class**: deterministic computation plus AST guard.
- **Evidence**: `reader.py`; `test_reader.py`; G8 injection.
- **Falsifier**: a forbidden name in the committed reader source; a
  unique-match failure; a choice among multiple matches.
- **Obligation**: the reader classifies I1; it is not a generator.

### CL-ED-OPEN

- **Statement**: The instance channel — a never-selects read of admitted
  instances whose pair never enters `reqs` — is outside `C_reqs` and
  remains OPEN.  Witness I1 reads `(0,1)` from an instance and leaves
  `reqs` empty.
- **Class**: open obstruction, with an exhibited witness of the shape.
- **Evidence**: `witness_i1`; census status `OPEN`.
- **Falsifier**: a grammar production of instances from rule firing, or
  a brief that weakens E2 to "owed separation" not "member of `reqs`,"
  together with a Lean E1 proof.
- **Obligation**: not discharged here.

### CL-ED-BOUND

- **Statement**: Endogenous traces without external data growth terminate in at most binom(N,2) steps. This bound is a corollary of `closedRun_round_bound` from sealed `Derivation.Rounds`. This does NOT close OB-1 — it shows a termination bound, not a demand generator.
- **Class**: proved theorem (termination bound on closed runs).
- **Lean**: `run_length_bound_from_closedRun`.
- **Python**: `verify_termination.py`.
- **Falsifier**: a trace satisfying endogenous constraints that exceeds binom(N,2) steps without external growth.
- **Obligation**: OB-1 (demand generator on C_reqs) remains OPEN.

### CL-ED-DYNAMICS

- **Statement**: Sustained vs terminating does not apply inside
  `C_reqs`: there is no generator.  Growth-conditional generation under
  a declared commitment (standing, ignition) remains external growth
  plus a host condition.
- **Class**: declared scope.
- **Evidence**: `candidates.json` `dynamics`; `SC-18`; `CL-IG-02`.
- **Falsifier**: a C_reqs generator, which this tree proves there is not.
