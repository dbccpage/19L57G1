# Described replay status

`AuthorityEffect: None`.

## Boundary and chronology

[METATHEORY] The source snapshot is
`f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be`; its tree is
`c992aa1f6270399439f02319e436d2d789776f92`.

[DECLARED_POLICY] The only write root is `research/described_replay/`.
The sealed paths, shared files, root tests and configuration, the prose census
pin, and every sibling research tree remained read-only.

[METATHEORY] Commit
`950b0a75982c8a0c80c33a74d98f9d2a7eba1457` froze `PROMPT.md`,
`PREDICTIONS.md`, and the first source-object/span manifest and verifier
versions before the first enumeration. The native prompt SHA-256 is
`26181bc26863a085f423606020e8a4576ee32b06b1ea14a3c93f5afe0df16eb7`;
the sole predictions freeze SHA-256 is
`3c78da7af6d25296d34020eb5e6579070ad4e8dc529ef415b375a19f6bd1f204`.

[METATHEORY] The supplied outside-bet commitment was omitted from the first
manifest version and added during the completion audit as
`outside_bet_commitment_sha256`; `verify_pins.py` was amended at the same time
to enforce that exact field. This post-computation custody repair changes no
prediction, declared class, source object, source span, or result.

[METATHEORY] The first `.gitattributes` order allowed generic JSON handling to
override the exact-byte receipt and manifest rules. The completion audit moved
the two `-text` rules after the generic rule and added explicit LF handling for
the local Python, Markdown, TOML, Lean, and toolchain text families. Attribute
and byte checks below record this transport repair; it changes no payload.

[DECLARED_POLICY] The Python kernel and the core Lean package are local
reconstructions. `lean/DescribedReplay/Provenance.lean` maps fourteen
reconstructed Lean kernel definitions to the pinned model source and maps
the class-membership definition to the frozen local class declaration. No
sealed or sibling implementation is imported.

## Declared readings

[DECLARED_POLICY] In stage two, “one admission event” is read as one event
from the frozen nine-symbol process alphabet. That alphabet contains inert
supply and imposition as well as admission events, so the stepper consumes
exactly one declared event on a successful application and never skips it.

[DECLARED_POLICY] A description supplied to an in-class candidate is a
validated metatheoretic argument. The candidate then runs its own fixed event
history from its fixed `EMPTY` base. No class event reads, removes, dispatches
on, or starts from the description regime.

[DECLARED_POLICY] The Python decoder accepts concrete position-tagged text
tokens; the Lean decoder accepts the corresponding typed finite tokens. Their
separate results are recorded. No cross-language correspondence is assumed.

[DECLARED_POLICY] Candidate reporting cost for candidate `C` and target `T`
is `length(C) + length(T)`: one stepper application per candidate event plus
one admission per target-description token. Outside finite reporting follows
the target and therefore costs `2 * length(T)`. Observing the final `Done` tag
and evaluating the declared predicate are audit operations outside the frozen
cost.

[DECLARED_POLICY] The stage-five demand family is the singleton imposed pair
`(0,1)`, evaluated separately under `mu1` and `mu2`. The phrase “finite list”
therefore includes one declared demand rather than an unstated family.

[OPEN] A typed correspondence proving that the Python and Lean
reconstructions commute with encoding, decoding, stepping, and terminals is
`CROSS_LANGUAGE_EQUIVALENCE`; it is a priced leftover, not a result.

## Five-stage register

| Stage | Evidence class | Terminal and scope |
| --- | --- | --- |
| 1. Description | PROVED_THEOREM | `DESCRIPTION_PROVED` for `DR-C-2-1-3`: two datum symbols, nine event symbols, unary arity at most one, history length at most three. |
| 2. Stepper | PROVED_THEOREM | `STEPPER_PROVED` on valid descriptions of the same declared class: one consumed event and one pointer advance per successful application; iteration agrees with guarded prefix replay. |
| 3. ClassReplay | PROVED_THEOREM | Within `DR-C-2-1-3` with two datum symbols, nine event symbols, arity at most one, and history length at most three, `NO_SUCH_MEMBER_IN_CLASS`: no fixed-history member reproduces every described target. |
| 4a. Self-description | PROVED_THEOREM | Within `DR-C-2-1-3` with two datum symbols, nine event symbols, arity at most one, and history length at most three, `SELF_DESCRIBING_EXHIBITED`: the empty member's description lies in the class and it reproduces its own replay. |
| 4b. Reporting | PROVED_THEOREM | Within `DR-C-2-1-3` with two datum symbols, nine event symbols, arity at most one, history length at most three, and candidate-step plus target-description cost at most six, `DECIDER_REFUSED_WITHIN_COST`: no fixed member reports every target; every candidate has a class-member disagreement target within that cost. |
| 4b. Unbounded form | OPEN | `OPEN_UNBOUNDED`: no result is stated beyond the declared class and cost six. |
| 5. Cost ledger | FINITE_COMPUTATION | For the singleton demand, arity at most one, at most one fresh datum, at most one fresh form, and at most two response items, `COST_TABLE_WRITTEN`. |
| 5. Unbounded form | OPEN | `OPEN_UNBOUNDED`: enlarged response bounds and a bound-uniform cost comparison are not executed. |
| Register | FINITE_COMPUTATION | `REGISTER_WRITTEN`: all five stages appear in order; the all-policy frontier is named and not started. |
| Protected source open | OPEN | `OB1_UNCHANGED`: the pinned challenge-source obstruction is untouched. |
| Protected charter open | OPEN | `S66_UNCHANGED`: the protected sixth item is untouched. |
| Protected charter open | OPEN | `S9_LAST_UNCHANGED`: the protected last item is untouched. |

## Computed values

[FINITE_COMPUTATION] The declared class has 178 members with length histogram
`{0: 1, 1: 5, 2: 26, 3: 146}` and 22 literal replay endpoints.

[FINITE_COMPUTATION] The concrete decoder-domain enumeration covers all
20,440 words of length zero through three over the 27-token alphabet. Its 178
accepted regimes equal the encoding image exactly; tagged tests separately
reject extra components, misplaced positions, excess length, mismatched
admission history, and ill-formed decoded prefixes.

[COUNTERMODEL] Member 0 has the empty history and member 1 has the one-event
`Supply(a)` history. They are distinct class members with distinct
descriptions and the same `EMPTY` endpoint.

[FINITE_COMPUTATION] Within `DR-C-2-1-3` with two datum symbols, nine event
symbols, arity at most one, and history length at most three, the normalized
candidate-target receipt has 178 member and description catalog entries and
31,684 matrix cells. All 31,684 candidate executions certify against their
own fixed base; 2,724 cells equal the target replay and 28,960 do not. No row
succeeds on all 178 targets within those bounds.

[FINITE_COMPUTATION] Within `DR-C-2-1-3` with two datum symbols, nine event
symbols, arity at most one, and history length at most three,
self-description has the sole witness index 0.

[FINITE_COMPUTATION] Within `DR-C-2-1-3` with two datum symbols, nine event
symbols, arity at most one, history length at most three, and outside report
cost at most six, the terminal partition has 50 false targets and 128 true
targets, and the outside table costs 990 operations in aggregate.

[FINITE_COMPUTATION] Within `DR-C-2-1-3` with two datum symbols, nine event
symbols, arity at most one, history length at most three, and candidate-step
plus target-description cost at most six, the bounded fixed-candidate matrix
has 31,684 cells, 14,984 correct cells, no complete row, and 178 of 178
constructed disagreements.

[FINITE_COMPUTATION] For the one declared separation demand with arity at
most one, at most one fresh datum, at most one fresh form, and at most two
response items, `mu1` attains item count 2 and `mu2` attains `(2,1)`. Each
measure checks five candidates through the first successful level, spends
finding cost 12, retains two tied raw responses, and places both in one
declared secondary isomorphism class. Each supplied winner costs 4 to check,
so each finite row records the ratio 12 to 4, or 3 to 1. This is a table value
at that frozen bound, not a rate.

[METATHEORY] The Python execution surface now makes both charged transition
counts literal. A class candidate validates the supplied description, then
executes its own fixed history through one prepared DR stepper witness. The
immutable validation and fixed-history result are cached across the repeated
matrix dimension: every cell refers to a validated target argument, while each
of the 178 pure candidate histories is physically stepped once rather than
recomputed for all 178 columns. The stage-five checker uses a narrowly
separate response-event stepper: its
nonempty base and response tokens are outside the frozen DR decoder alphabet,
so it does not claim to be that decoder surface. Each response item records
one description-admission charge and performs exactly one call to the same
reconstructed one-event transition. Checking and finding costs are summed
from those returned execution counts, not inferred from response length.
This clarifies the pre-frozen cost rule;
it changes neither the declared price nor any census result.

## Prediction dispositions

- [PREDICTION] `decode_encode_id`, `encode_injective`,
  `encode_admission_only`, and `decoder_domain_iff`: matched. Lean proves the
  typed statements; Python exhausts the declared 20,440-word surface and all
  178 class encodings.
- [PREDICTION] The same-endpoint, different-history pair: matched by the empty
  and one-supply members; the descriptions differ.
- [PREDICTION] `stepper_one`, `stepper_iterate`, and `stepper_total`: matched
  by the constructive Lean theorems and the 178 Python runs.
- [PREDICTION] `stepper_no_replay`: matched by structural source audits. The
  immutable decoder witness is prepared once outside the frozen
  `(description, pointer, current)` state triple. A successful step calls the
  one-event transition exactly once and transitively performs no decode or
  whole-history fold.
- [PREDICTION] Stage-three branch: no value was predicted. Within
  `DR-C-2-1-3` with two datum symbols, nine event symbols, arity at most one,
  and history length at most three, exhaustion and the class theorem select
  the pre-agreed `NO_SUCH_MEMBER_IN_CLASS` branch.
- [PREDICTION] Self-description and fixed-report outcomes: no values were
  predicted. Within `DR-C-2-1-3` with two datum symbols, nine event symbols,
  arity at most one, history length at most three, and reporting cost at most
  six, the observed values are the exhibited empty witness and the bounded
  no-reporter theorem above.
- [PREDICTION] Conditional diagonal expectation after a reporter miss:
  matched. Within `DR-C-2-1-3` with two datum symbols, nine event symbols,
  arity at most one, history length at most three, and candidate-step plus
  target-description cost at most six, the constructed target is a class
  member and disagrees with its fixed candidate.
- [PREDICTION] Cost values: none were predicted. Both measures retain the two
  ties and record check 4, find 12, and ratio 3 to 1.
- [PREDICTION] Missed frozen predictions: none. Values deliberately marked
  “recorded, not predicted” are observations, not matches claimed after the
  fact.

## Lean scope and manual receipt

[METATHEORY] The rung-local package has 46 theorem declarations and 46
ordered `#print axioms` entries. The recorded dependencies are contained in
`{propext, Quot.sound}`. The exact claims are the theorem types in `lean/`;
the build does not establish the Python census, the cross-language bridge, or
any unbounded statement.

[METATHEORY] `MANUAL_RECEIPT_DECLARED`: no CI gate consumes this tree's Lean
build, axiom report, Python receipts, pin checks, or scans. `verify_lean.py` is
a manual receipt: it records a local run, grants no authority, and does not by
itself prove a mathematical payload.

## Local verifier performance

[METATHEORY] After caching each immutable target validation and each pure
fixed candidate execution across the opposite matrix dimension, the complete
semantic module ran 42 tests serially in 19.87 seconds. The same 42 tests ran
with eight `pytest-xdist` workers in 22.92 seconds. The final local packet
therefore uses the serial command: shared in-process census caches reduce
elapsed time by about 13 percent relative to the eight-worker run. This timing
choice changes no receipt value or evidence class.

## Injection record

[METATHEORY] Every probe below was reversed before the recovery run. No pin or
receipt was regenerated while a probe was live.

| Verifier | Evidence class | Injection | Exact observed failure | Recovery |
| --- | --- | --- | --- | --- |
| `verify_pins.py --check-scope` | METATHEORY | Twenty-nine in-memory mutations cover source census, declared and resolved source bytes and blobs, missing HEAD source, snapshot declaration/tree/ancestry, toolchain declaration, declared and recomputed span bytes, freeze declaration/parent/HEAD/worktree, native prompt and prediction hashes, outside-bet commitment, write root, authority, deterministic manifest bytes, duplicate JSON names, missing and extra pin receipts, receipt type/reparse/bytes, and ignored-untracked scope classification. | The exact 29 diagnostic lists are frozen in `receipts/pins/injections.json`; every observed list equals its expected list and every row has `recovered: true`. | Exit 0 after the in-memory reversals: `sources=12 spans=6 scope=checked`. |
| `run_described_replay.py --check` | METATHEORY | Twelve in-memory receipt snapshots inject payload drift; extra, missing, directory, reparse, and other entries; invalid, duplicate-name, and non-object JSON; absent and wrong output-hash maps; and a reparse receipt root. | The exact 12 diagnostic lists are frozen in `receipts/python/injections.json`; every observed list equals its expected list and every row has `recovered: true`. | Exit 0 after the in-memory reversals: `Python receipt replay clean: outputs=9 terminal=REGISTER_WRITTEN`. |
| `verify_lean.py` | METATHEORY | Twenty-three in-memory mutations cover the file, import, theorem and report censuses; forbidden tokens; the costed stepper dependency and transition boundary; one-time preparation, trace, dispatcher, and iteration boundaries; build reports; dependency whitelist; receipt census, duplicate JSON names, and receipt bytes. | The exact 23 diagnostics are frozen in `receipts/lean/injections.json`; each row has `recovered: true`. | `verify_lean.py --check` exits 0 with 46 theorems, 3 receipts, 23 injections. |
| `test_forbidden.py` | METATHEORY | In-memory path/content, camel-case, and underscore-compound name probes; a non-name embedded substring; plain-file, directory, and reparse probes; and five whole-process determiners exercise the scanners without writing a live forbidden token. | Name probes are reported as indexed path/content hits; directory/reparse probes raise their exact boundary diagnostics; all positive whole-process probes are classified and both negative controls remain clear. | The 23 scanner and receipt-I/O tests pass after every probe. |
| strict mypy | METATHEORY | Added `value: int = "probe"` in a transient source. | `zzz_type_probe.py:1: error: Incompatible types in assignment (expression has type "str", variable has type "int") [assignment]` | Strict mypy passed after deletion. |
| semantic pytest | METATHEORY | The suite supplies malformed decoder inputs, invalid stepper states, an unknown measure, duplicate JSON names, unsafe receipt targets, and all four named pruning exclusions. | Each injected input receives its exact declared exception, invalid tag, or false predicate; assertion messages are bound by the named tests. | The full suite passes with every injected input retained as a negative test. |

## Adversarial dispositions

- [REFUSED] A1: the class theorem does not narrow the pinned whole-process
  refusal; every positive or negative result carries `DR-C-2-1-3` and its
  bounds.
- [REFUSED] A2: `DECIDER_REFUSED_WITHIN_COST` is not an unbounded
  impossibility; `OPEN_UNBOUNDED` is explicit.
- [REFUSED] A3: the cost ledger distinguishes no classes of questions; it
  records two counts on one finite demand at one bound.
- [REFUSED] A4: consuming a supplied description is not an endogenous demand;
  `OB1_UNCHANGED` remains terminal.
- [REFUSED] A5: neither stepper advances a whole history in one application.
- [REFUSED] A6: the pinned sibling pair is not used as this tree's
  countermodel.
- [REFUSED] A7: no sealed kernel module or sibling package is imported.
- [REFUSED] A8: Lean proves theorem types; receipts record deterministic
  computations and do not prove those types.
- [REFUSED] A9: only the outside-bet digest is recorded; no plaintext was an
  input.
- [REFUSED] A10: the parallel write root is disjoint and no shared file was
  changed.
- [REFUSED] A11: `DR-C-2-1-3` is a declared bounded class, not every process.
- [REFUSED] A12: no outside target is named in prose or identifiers.

## Priced leftovers

| Leftover | Evidence class | Price of a future attempt |
| --- | --- | --- |
| Cross-language correspondence | OPEN | Declare a typed relation between the two reconstructions and prove constructor, decoder, step, and terminal commuting laws. |
| Enlarged class | OPEN | Declare new finite alphabets and bounds, add an input-reading event or prove its absence, and rebuild the complete candidate-target matrix within those bounds. |
| Unbounded reporting | OPEN | Quantify over every admitted finite description length and construct either a reporting member or a closure-preserving disagreement member. |
| Unbounded cost ledger | OPEN | Define a cost-indexed family for every response bound and prove a statement uniform in that bound. |
| All-policy quotient frontier | OPEN | Declare the finite generator family and resource bounds, construct the bounded quotient tree, and construct every single-policy embedding. The frontier was not started. |
| `OB1_UNCHANGED` | OPEN | Construct an object-language challenge source or prove the pinned wider-class target; neither act occurs here. |

## Unapplied registration diff

[DECLARED_POLICY] Registration is a shared author act. This run does not apply
the following diff to `.github/workflows/verify.yml`:

```yaml
- name: Described replay local packet
  run: |
    python research/described_replay/verify_pins.py --check-scope
    python research/described_replay/verify_lean.py --check
    python research/described_replay/run_described_replay.py --check
    python -m pytest -q research/described_replay
    python -m mypy --config-file research/described_replay/pyproject.toml research/described_replay
```

## Parallel-track note

[METATHEORY] The declared parallel write root is
`research/fresh_characters/`; it is absent from the pinned snapshot used by
this branch. This run neither reads an unavailable receipt nor writes that
root. Frozen shared files remain untouched. If that track moves a pinned
source before publication, only the affected pin and publication-base record
may be updated; the frozen predictions are not rewritten.

## Local verifier battery

[METATHEORY] The final battery is recorded after the injection
recoveries:

| Command | Evidence class | Result |
| --- | --- | --- |
| `python verify_pins.py --check-scope` | METATHEORY | PASS: 12 source objects, 6 spans, scope checked. |
| `python verify_lean.py --check` | METATHEORY | PASS: 46 theorems, 3 receipts, 23 injections. |
| `python run_described_replay.py --check` | METATHEORY | PASS: 9 byte-identical Python receipts, including 12 replayed verifier injections. |
| `python -m pytest -q` | METATHEORY | PASS: 69 tests in 54.12 seconds. |
| `python -m mypy --strict .` | METATHEORY | PASS: no issues in 13 source files. |
| `python ci/check_prose_watchlist.py` from repository root | METATHEORY | PASS without repin: 49 watched terms, 130 files with pinned hits, 1,826 hits; census matches its pin. |
| `git diff --cached --check` | METATHEORY | PASS after removing two trailing blank-line defects found by the first staged run. |
| `git check-attr text eol` plus `git ls-files --eol --cached` on the write root | METATHEORY | PASS: all 45 tracked write-root paths are LF in both index and worktree (43 implementation-commit changes plus the two earlier frozen inputs); local source/text paths are `text eol=lf`, while the manifest and receipt paths are `-text` exact-byte surfaces. |

## TAU

[METATHEORY] `receipts/python/tau.json` is the deterministic mixed-evidence
machine register. Each terminal row carries its own evidence class and Lean
pointer where applicable; the export itself is not classified as a theorem or
finite computation. This selected summary preserves the machine field shapes;
the receipt contains all twelve terminal rows and all six priced leftovers:

```yaml
steps_completed: [Description, Stepper, ClassReplay, Diagonal, CostLedger]
write_root: research/described_replay/
snapshot: f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be
sealed_paths_touched: []
shared_files_touched: []
census_pin_regenerated: false
prompt_hash_native: 26181bc26863a085f423606020e8a4576ee32b06b1ea14a3c93f5afe0df16eb7
predictions_hashes: [3c78da7af6d25296d34020eb5e6579070ad4e8dc529ef415b375a19f6bd1f204]
class_declaration: {class_id: DR-C-2-1-3, alphabet: 9, datum_alphabet: 2, arity_bound: 1, length_bound: 3, class_size: 178}
description: {terminal: DESCRIPTION_PROVED, price_rule: one_description_admission_per_source_event, endpoint_countermodel: [0, 1]}
stepper: {terminal: STEPPER_PROVED, defined_through_replay: false}
class_replay: {terminal: NO_SUCH_MEMBER_IN_CLASS, member: none, certified_pairs: 2724, failures: 28960}
diagonal: {self_description: SELF_DESCRIBING_EXHIBITED, decider_by_exhaustion_cost: 990, decider_within_declared_cost: DECIDER_REFUSED_WITHIN_COST, unbounded: OPEN_UNBOUNDED}
cost_ledger:
  rows: 2
  check_costs:
    - {measure: mu1, values: [4, 4]}
    - {measure: mu2, values: [4, 4]}
  find_costs:
    - {measure: mu1, value: 12}
    - {measure: mu2, value: 12}
  largest_row: 2
  terminal: COST_TABLE_WRITTEN
  unbounded: OPEN_UNBOUNDED
opens_unchanged: [OB1_UNCHANGED, S66_UNCHANGED, S9_LAST_UNCHANGED]
outside_bet_hash: 5534f09d5cfcbb20b45fdc1ee42c615d4af224c5ced973dda5b74d522bb1cfd6
authority_effect: None
stage_register_complete: true
publication_complete: false
publication_completion: author acceptance and merge are outside this run
final_state: false
```

[OPEN] The machine export also carries the costed cross-language, enlarged
class, unbounded reporting, unbounded cost, all-policy frontier, and OB-1
leftovers. No leftover is executed by this run.

[METATHEORY] The run stops at `REGISTER_WRITTEN` with all five declared stages
walked in order, `OB1_UNCHANGED`, and `OPEN_UNBOUNDED`. The direct PR is an
authorized handoff, while acceptance and merge remain author acts. The
stage-local terminal is `stage_register_complete: true`; top-level
`final_state` remains false because this tree does not claim that the
author-controlled boundary has occurred.
