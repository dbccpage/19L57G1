# Claims

Stable IDs for this packet. Classes are the repository's own, counted
from `paper/paper_claim_ledger.md`, not invented here.

A claim marked **observation** is about the repository, not about the
object language. It is discharged by looking at a named file, and it can
go stale when that file changes. It is never evidence for a mathematical
payload.

Where a claim restates a sealed ledger entry, the `CL-*` ID is given and
this packet adds nothing to it. Where this packet asserts something the
ledger does not, that is marked **new here** and carries its own
falsifier.

| ID | class | short statement |
|---|---|---|
| GC-1 | observation | a reusable finite process meeting the nine conditions is present in the record |
| GC-2 | theorem | supply is not admission |
| GC-3 | theorem + countermodel | admission alone need not increase expressive power |
| GC-4 | theorem | the first requirement's minimum response costs exactly two items |
| GC-5 | theorem (L) + bounded theorem (F) | the minimum is tied under `mu1` and unique up to isomorphism under `mu2` |
| GC-6 | theorem | every supplied separation demand on an accepted regime has a valid response |
| GC-7 | finite computation | every certified node and every edge replays |
| GC-8 | finite computation | tied non-isomorphic continuations are all retained |
| GC-9 | declared metatheory + bounded theorem | no object-language endogenous demand generator was derived — **OB-1** |
| GC-10 | bounded theorem | pair-separation closure terminates with the external policy disabled |
| GC-11 | theorem + finite computation + open | generation is proved for a declared rule; repair is empty in the declared bounded class |
| GC-12 | **refused** | no universal property or initiality for the process |
| GC-13 | unresolved | two admission readings survive with no internal fact separating them |
| GC-14 | declared metatheory | four declarations the process does not derive |
| GC-15 | observation | the blindness attestation is false at HEAD — **OB-3** |
| GC-16 | observation | `README.md` counts are stale — **OB-4** |
| GC-17 | observation | this tree is not read by any gate |

---

### GC-1
- **Statement**: The repository's existing record contains a reusable
  finite process satisfying all nine conditions of the work order. It is
  implemented, not proposed.
- **Class**: observation. **New here** as a composite statement; each
  condition is separately backed below and in `process_candidate.md`.
- **Python**: `code/derivation/{model,observe,candidates,iso,engine,export}.py`;
  `code/run_derivation.py`; the committed branch trees under
  `artifacts/full/`.
- **Lean**: none as a composite. The parts are proved separately; the
  composite is not a theorem and is not claimed as one.
- **Falsifier / boundary**: any one of the nine conditions with no cited
  implementation. The claim is about presence, not about adequacy,
  minimality, or initiality — see GC-12.

### GC-2
- **Statement**: Supply presents a token and changes no admitted state.
  Admission is a separate event.
- **Class**: theorem. Restates `CL-0-INERTIA`, `CL-1-SUPPLY-NOT-ADMISSION`.
- **Python**: `model.step` returns the regime unchanged on `Supply`.
- **Lean**: `supply_no_op`. **Axioms**: within `{propext, Quot.sound}`.
- **Falsifier**: a `Supply` event whose replay differs from its base.

### GC-3
- **Statement**: With data admitted but no judgment structure, all
  profiles are equal: externally distinct data can remain internally
  indistinguishable. Admission need not increase expressive power.
- **Class**: theorem + countermodel. Restates `CL-2-COLLAPSED`,
  `CL-2-NONINCREASE`; `paper.md` §11(b).
- **Python**: `observe.collapsed_pairs`; `engine.challenge2_report`.
- **Falsifier**: a regime with no admitted forms exhibiting two data with
  differing profiles.

### GC-4
- **Statement**: The first separability requirement has minimum response
  cost exactly two items, **absolutely over the item grammar**, in both
  admission readings.
- **Class**: theorem. Restates `CL-3-COST1-IMPOSSIBLE`, `CL-3-MIN-TWO`;
  `paper.md` §11(c).
- **Boundary**: the impossibility below two items is grammar-wide. What
  the declared bounds limit is the *completeness of the enumeration*, not
  this lower bound. The two must not be conflated.

### GC-5
- **Statement**: Under `mu1` the minimum is not unique — three
  non-isomorphic tied classes in reading L, plus a countably infinite tie
  family indexed by arity; five classes in reading F within the declared
  bounds. Under `mu2` the minimum is unique up to the implemented
  isomorphism, grammar-wide, in both readings.
- **Class**: theorem for reading L; bounded theorem for the reading-F
  count. Restates `CL-3-NONUNIQUE-MU1`, `CL-3-TIE-CLASSES`,
  `CL-3-INFINITE-TIES`, `CL-3-UNIQUE-MU2-L`, `CL-3-UNIQUE-MU2-F`.
- **Lean**: `mu2_unique`, `mu2_unique_F`.
- **Boundary**: the reading-F non-uniqueness count is by engine
  enumeration within bounds; there is no reading-F Lean non-uniqueness or
  k-ary family. `paper.md` §11(d) records that an earlier version of this
  clause over-tagged the whole sentence as theorem.

### GC-6
- **Statement**: On any well-formed regime whose imposed requirements are
  all separated, every supplied separation demand has a valid response
  keeping every imposed requirement separated.
- **Class**: theorem. Restates `CL-PROGRESS`.
- **Lean**: `mark_progress`.
- **Boundary**: **response existence only.** It does not assert
  autonomous demand generation and does not assert an unbounded tower.
  Quoting it for either is the misuse the ledger explicitly guards
  against.

### GC-7
- **Statement**: Every node's regime equals the replay of its recorded
  history, and every edge is certified: creation edges by regime-hash
  equality, merge edges by explicit datum and form bijections onto the
  stored representative.
- **Class**: finite computation. Restates `CL-REPLAY`.
- **Python**: `model.certify`; `export.verify_full_export`;
  `Tree.stats()["all_certified"]`.
- **Falsifier**: any exported node or edge whose stored hash differs from
  the replay of its recorded history.

### GC-8
- **Statement**: At every expansion, all minimum valid responses are
  quotiented by the implemented isomorphism relation and **every** class
  is attached as a branch. No tie is dropped.
- **Class**: finite computation.
- **Python**: `engine._quotient`; the attach loop in `engine.build_tree`;
  the `expansions_with_ties` counters in the exported tree statistics.
- **Falsifier**: an expansion whose child count is smaller than its
  class count.

### GC-9 — OB-1
- **Statement**: No object-language endogenous demand generator was
  derived. A collapsed pair is not an active obstruction unless
  separation is required, and the requirement pattern originates
  externally. What stands in its place is the *declared* pair-separation
  closure policy.
- **Class**: declared metatheory + bounded theorem. Restates
  `CL-CLOSURE-POLICY`; `paper.md` §11(f).
- **Python**: `engine.closure_challenge_orbits`;
  `test_closure_policy_is_token_blind`, `test_closure_policy_fixpoint`.
- **Falsifier / boundary**: any dependence of the challenge orbits on
  token renaming or representative labelling would break the policy's
  stated virtues. Selection of this policy among conceivable ones is a
  declared-metatheory judgment — the ledger says so in its own falsifier
  field, and this packet does not improve on it.
- **This is the first point at which the process is not forced.**

### GC-10
- **Statement**: With the external continuation policy disabled, every
  maximal branch reaches the all-pairs-separated fixpoint within
  `n(n-1)/2` rounds: reading L in 1 round with 3 terminal branches,
  reading F in 3 rounds with 16, no guard cut, no round cut, none open.
- **Class**: bounded theorem. Restates `CL-CLOSURE-TERMINATION`.
- **Boundary**: closed-system runs under measure `mu1` only; no `mu2`
  closed run is exported.

### GC-11
- **Statement**: For the declared reflective chain rule, generation is
  proved horizon-free (`generation_never_dries`): from the third round on
  a live obstruction always exists and the only event consumed is the
  internally enabled reflection. Over the five declared repair
  strategies, the class that fires, clears every firing round, and avoids
  recurring imports is **empty within the declared 15-round computation**.
- **Class**: theorem (generation) + finite computation within declared
  bounds (the exclusion) + **open** (the class-general cycle claim).
- **Python**: `code/derivation/generator.py`; `artifacts/generator.json`,
  key `endogenous_cycle_found: false`.
- **Lean**: `generation_never_dries`, `automark_presence_vacuous`,
  `finite_marks_outrun`, `valued_marks_collapse_generation`.
- **Falsifier / boundary**: the generating rule is itself **declared**.
  This does not close GC-9. The remaining obligation is stated by the
  repository as G1: a repair channel that separates without minting
  identity-grade distinctions, or a proof that none exists.

### GC-12
- **Statement**: The process is minimal or initial among a defined class
  of finite processes satisfying the same challenges.
- **Class**: **refused.** Restates `CL-NO-UNIVERSAL-PROPERTY`. No
  universal property was proved; per the repository's discipline the word
  "minimal" is not used of the whole process, and it is not used of P in
  this packet.
- **Boundary**: what survives instead is per-stage minimality with
  declared scope (GC-4, GC-5), determinism (`CL-DETERMINISM`), and
  bounded completeness (`CL-TREE-MU2-COMPLETE`).

### GC-13
- **Statement**: Two admission readings of the challenge text survive,
  and no internal fact separates them. Both towers are carried in full.
- **Class**: unresolved. Restates `CL-READING-UNDERDETERMINATION`;
  `paper.md` §11(h).

### GC-14
- **Statement**: The process is forced only relative to four declarations
  it does not derive: the candidate space and bounds; the cost measure;
  the isomorphism relation; and the challenge source (both the closure
  policy and the external continuation policy).
- **Class**: declared metatheory. Restates `paper.md` §12.
- **Falsifier / boundary**: a derivation of any one of the four from the
  object language would move it out of this list. The `mu1`/`mu2` split
  is the exhibited sensitivity: the two measures disagree about
  uniqueness at the first answerable question.

### GC-15 — OB-3
- **Statement**: `paper/paper.md` §13 asserts that no external theory,
  architecture, or terminology is named anywhere in this repository
  outside the read-only seed prompt. That assertion is **false at HEAD**.
  Six files under `paper/` carry comparison sections naming external
  mathematics.
- **Class**: observation. **New here.**
- **Evidence**: `paper/bridge_provenance.md:243`;
  `paper/endogenous_generator.md:302`;
  `paper/primitive_difference.md:407`;
  `paper/primitive_difference_map.md:213` (a "Known mathematics" table
  column); `paper/refusal_as_difference.md:393`;
  `paper/refusal_difference.md:267`. Each was read, not inferred from its
  heading.
- **Falsifier / boundary**: show that those sections name no external
  theory, or that `CLAUDE.md`'s prohibition does not reach them. No gate
  detects this: the paper-citation gate checks that cited paths resolve,
  and the vocabulary firewall bars a denylist of identifiers, not prose
  naming. The attestation is an operator claim and is currently wrong.
  This packet records it and repairs nothing — the repair is a
  claim-level act on sealed prose.

### GC-16 — OB-4
- **Statement**: `README.md` records nine gate families, 1417 axiom
  reports, and 13 parked Lean modules. At HEAD there are ten gate
  families, 1424 reports, and 12 parked modules.
- **Class**: observation. **New here.**
- **Evidence**: `.github/workflows/verify.yml` (three jobs, ten
  families); `artifacts/lean_axioms.txt`; `lean4/Derivation.lean` imports
  `Derivation.Breaking`.
- **Boundary**: `README.md` is outside the sealed paths, so this is a
  cheap repair; it is recorded, not done.

### GC-17
- **Statement**: No gate reads `research/genesis_continuation/`.
- **Class**: observation.
- **Evidence**: `.github/workflows/verify.yml`'s `research` job names
  `research/primitive_difference_tower` and `research/portable_interface`
  by path and does not glob `research/`.
- **Boundary**: this packet is prose only, so there is nothing here for a
  gate to check. If anything executable is added, registering it is a
  separate act.

## Post-Hoc Comparison

**Withheld**, for the reason recorded in `continuation_plan.md`. No
external theory is named in this packet, and no claim above depends on
one.
