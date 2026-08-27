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
| GC-11 | theorem + finite computation + open | generation and the finite-local class exclusion are horizon-free theorems; the 15-round search is historical witness only |
| GC-12 | **refused** | no universal property or initiality for the process |
| GC-13 | unresolved | two admission readings survive with no internal fact separating them |
| GC-14 | declared metatheory | four declarations the process does not derive |
| GC-15 | observation + open author act | the old global attestation is withdrawn; comparison-policy precedence remains **OB-3** |
| GC-16 | observation | `README.md` refreshed from the `24d1bc64` census; **OB-4 DISCHARGED by this update** |
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
  internally enabled reflection. For every fixed-radius, fixed-finite-
  alphabet member of `LocalStrategy`, the capacity theorem gives a deep
  collision and `g1_class_exclusion` proves the full cycle impossible.
- **Class**: theorem (generation) + theorem (the declared finite-local class
  exclusion) + finite computation (historical five-strategy witness) +
  **open** (strategies outside the declared class).
- **Python**: `code/derivation/generator.py`; `artifacts/generator.json`, key
  `endogenous_cycle_found: false`, is the bounded 15-round historical witness,
  not the class proof. `artifacts/g1_class_receipt.json` binds the class result.
- **Lean**: `Generator.generation_never_dries`,
  `LocalFiniteAlphabet.strategy_capacity_collision`, and
  `G1Class.g1_class_exclusion`.
- **Falsifier / boundary**: the generating rule is itself **declared**.
  This does not close GC-9 or quantify over repair channels outside
  `LocalStrategy d` with `FiniteDeclaration k`. `OB1_UNCHANGED`.

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
- **Previous statement — WITHDRAWN as current**: “`paper/paper.md` §13
  asserts a repository-wide no-comparison sentence which is false at HEAD.”
  Section 13 now explicitly withdraws that paper-global sentence and narrows
  the evidence-backed blindness boundary. The replacement inventory is now
  exact about the local paper fence and still records the two placement
  defects rather than hiding them.
- **Statement**: the live OB-3 conflict is between the immutable run
  directives, which permit or require end-only comparison, and `CLAUDE.md`'s
  restored no-exception prohibition, while six sealed comparison surfaces
  remain. All six known surfaces carry the uniform fence: post-hoc comparison
  only, not derivational input, theorem evidence, or authorization. Two
  surfaces are not actually final:
  substantive sections follow the comparison in `paper/endogenous_generator.md`
  and `paper/primitive_difference_map.md`. The exact allowed path set,
  precedence rule, and sealed-paper repair remain author acts.
- **Class**: observation + OPEN author act.
- **Evidence**: the five same-heading surfaces are
  `paper/bridge_provenance.md:243`, `paper/endogenous_generator.md:302`,
  `paper/primitive_difference.md:407`,
  `paper/refusal_as_difference.md:393`, and
  `paper/refusal_difference.md:267`.
  The sixth, `paper/primitive_difference_map.md:213`, is a “Post-hoc
  realization table” with a “Known mathematics” column. Each surface and the
  following section structure was read, not inferred from a heading.
- **Boundary — do not collapse the six.** All six are comparison-labelled;
  the map surface is different because it is a table rather than the shared
  heading. The fence does not select an allowlist or weaken the no-exception
  rule.
- **Falsifier / closure condition**: an author declares which instruction has
  precedence and an exact comparison-path allowlist (possibly empty), then
  reconciles the sealed surfaces, repairs the two end-placement defects, and
  installs a zero/exact-allowlist and placement gate.
- **Not repaired here.** A gate before that declaration would silently encode
  the missing policy choice. This packet records only:

  ```text
  OB3_PAPER_GLOBAL_SENTENCE_WITHDRAWN
  OB3_PAPER_FENCE_UNIFORM
  OB3_END_ONLY_PLACEMENT_DEFECTS=2
  OB3_COMPARISON_POLICY_STILL_OPEN
  AuthorityEffect: None
  ```

### GC-16 — OB-4
- **Previous statement — WITHDRAWN as current**: “`README.md` records nine
  gate families, 1417 axiom reports, and 13 parked Lean modules. At HEAD
  there are ten gate families, 1424 reports, and 12 parked modules.” Both
  sides of that comparison subsequently drifted.
- **Statement**: `README.md` now records the `24d1bc64` census: eleven gate
  families; 58 typed Python sources; 74 Lean modules, comprising 62 in the
  root import closure and 12 parked; 37 test files with 481 collected cases
  (480 passed, one skipped on GitHub `verify` run #267); 39 deterministic JSON
  exports plus six full exports; 135 `CL-*` headings; and 1506 axiom reports.
- **Class**: observation. **OB-4 DISCHARGED by this README update, using the
  `24d1bc64` census.**
- **Evidence**: `.github/workflows/verify.yml`; `ci/check_parked_audit.py`;
  `artifacts/elaborated_modules.txt`; `artifacts/lean_axioms.txt`;
  `artifacts/completion_receipt.json`; the tracked source, test, artifact, and
  claim-heading censuses; GitHub `verify` run #267 on `89c9239`, whose tree
  `2e80261ef11b9bcd2fc3a87597892aafec83dbf6` is identical to merge commit
  `24d1bc64`.
- **Boundary**: this is a dated repository census, not mathematical evidence.
  A later source, test, artifact, claim, or workflow change can make it stale.

### GC-17
- **Statement**: No gate reads `research/genesis_continuation/`.
- **Class**: observation.
- **Evidence**: `.github/workflows/verify.yml`'s `research` job names
  `research/primitive_difference_tower`, `research/portable_interface`,
  `research/blind_restart`, and `research/partial_decide` by path and does not
  glob `research/`.
- **Boundary**: this packet is prose only, so there is nothing here for a
  gate to check. If anything executable is added, registering it is a
  separate act.

## Post-Hoc Comparison

**Withheld**, for the reason recorded in `continuation_plan.md`. No
external theory is named in this packet, and no claim above depends on
one.

### GC-18 — T5 and T6 scoped closure (2026-08-26)

- **Statement**: the general radius-one/depth-two equality
  correspondence is proved, and the capacity theorem now yields a
  horizon-free exclusion for every member of the declared fixed-radius,
  finite-alphabet local-strategy class.
- **Class**: theorem.
- **Evidence**: `SeparationCapacity.radius_one_agrees_with_sealed_depth2`,
  `LocalFiniteAlphabet.strategy_capacity_collision`, and
  `G1Class.g1_class_exclusion`; exact reports and declarations in
  `artifacts/g1_class_receipt.json`.
- **Boundary**: this closes T5 and T6 in their stated scopes only. It does
  not derive the class, quantify over every repair channel, or advance
  OB-1. `OBJECT_LANGUAGE_GENERATOR_NOT_IN_SCOPE`; `OB1_UNCHANGED`.
