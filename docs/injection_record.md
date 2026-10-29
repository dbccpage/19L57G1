# The injection record

A gate is proved only by failing on the exact defect it exists to catch,
with the failure naming the injected object, and by recovering when the
injection is reversed (`CLAUDE.md`, "Proving a gate"). This file is the
standing record of injections actually performed. It moved here from
`CLAUDE.md` on 2026-09-21, unchanged. Append a row when you prove a gate,
and put the same receipt in the pull request body.

What has actually been injected, and what failed:

| Gate | Injection | Observed failure |
|---|---|---|
| Lean census pin | added `Derivation/PinProbe.lean` | `diff` against `elaborated_modules.txt` |
| Per-module elaboration | type error in a parked module | root `lake build` stayed green; the per-module loop failed |
| Runner census | new unregistered `code/run_zzz_probe.py` | census went 24 → 25 with no registration, then `FAIL: regenerated but not committed: zzz_probe.json` |
| Regeneration, committed side | deleted one regenerated `*.json` | `FAIL: missing regeneration: apartness.json` |
| Regeneration, other side | stray `*.json` in the regenerated dir only | `FAIL: regenerated but not committed` |
| Empty-census guard | census pointed at a directory with no matches | guard fired before the pin was consulted |
| Skill authority | probe skill with no `AuthorityEffect: None` line | `FAIL: ... does not declare 'AuthorityEffect: None'` |
| Skill identity | frontmatter `name` ≠ directory name | `FAIL: ... frontmatter name 'wrong_name' does not match directory` |
| Skill shape | directory with no `SKILL.md`; body with no frontmatter | both named individually |
| Paper cross-reference | citation to a sibling that exists on no branch | `FAIL: … cites paper/zzz_probe_absent.md, which does not exist` |
| Paper cross-reference, real case | the original dead link re-injected verbatim | `FAIL: … cites paper/representative_selection.md, which does not exist` |
| Axiom-report pin, new theorem | dropped `collapsed_rename` from `artifacts/lean_axioms.txt` | `FAIL: axiom reports differ between CI build and artifact`, naming the missing report |
| Lean census pin, new module | removed `Derivation.CountTransport` from `elaborated_modules.txt` | census diff named the module and the check exited non-zero |
| Ledger evidence gate | renamed a cited test to `test_supply_is_not_admission_zzz_probe` | `FAIL: ... CL-0-INERTIA [python] ... matches no test, code def, artifact key, artifact text, or source literal` |
| Ledger evidence gate, real case | first real run, no injection | three dead references found and named: two stale tree-export filenames, one renamed theorem surviving only in a rename note |
| Axiom-report parser, primed names | (found live, not injected) four primed theorems absent from `lean_axioms.txt` while the match gate stayed green — both parsers shared the blind `'[^']+'` pattern | audit line count 1417 vs artifact 1413 exposed it; non-greedy capture fixed both, counts agree |
| Parked-audit completeness, unnamed module | added `Derivation/ZzzProbe.lean`, imported by nothing | `FAIL: Derivation.ZzzProbe is outside Derivation.lean's import closure but is not named in lean4/ParkedAudit.lean`; exit 0 after deletion. The in-Lean self-check stayed GREEN throughout — a module nothing imports is absent from the environment, which is why this gate is Python |
| Parked-audit completeness, other direction | added `import Derivation.Composing` to the root | `FAIL: Derivation.Composing is named in lean4/ParkedAudit.lean but IS inside Derivation.lean's import closure`; exit 0 after reversal |
| Research pin drift (gate 11) | restored the stale `PrimitivePassage.lean` hash in `SOURCE_MANIFEST.json` | `FAIL: hash mismatch for lean4/Derivation/PrimitivePassage.lean`, exit 1, naming the module; exit 0 after reversal. The exit status was checked directly, NOT through a pipeline — `$?` after `\| tail` reports tail's status and showed 0 while the script was returning 1 |
| Parked-module axiom census | `Classical.em` theorem added to the parked `Derivation/IsoCollapseCompat.lean` | `FAIL: disallowed axioms ['Classical.choice']`, naming `zzz_probe_choice`; plus the counterfactual on the same tree — reverting `defaultTargets` to `["Derivation"]` made the identical injection report `lean audit clean`, which is the residual itself, observed rather than argued |
| Research pin drift, real case | (found live, not injected) merging #76 and #77 | five research tests failed on `main` at `a1738fa` while the CI rollup reported SUCCESS; no job read the tree, and the two changes only interact once both are present |
| Partial-Decide source pin | changed the first byte of the pinned `model.py` digest | `FAIL: hash mismatch for code/derivation/model.py`, printing wanted, snapshot, and HEAD hashes; exit 1, then 0 after reversal |
| Partial-Decide import authority | added `from derivation.represented import cert_neg` to the production consumer | `FAIL: authorized import mismatch`, naming the extra module and symbol; exit 1, then 0 after reversal |
| Partial-Decide receipt bytes | changed `authority_effect` in the committed receipt | `FAIL: partial_decide_c3.json differs from the deterministic renderer`; exit 1, then 0 after reversal |
| Partial-Decide grade separation | changed the live-tie return to bounded `None` | `test_c3_mu1_retains_all_tied_classes` failed for both L and F and receipt equality failed; exit 1, then 0 after reversal |
| Partial-Decide measure totality | removed `mu2` from one reading at `43b57b9311ba4cacfde58904732b6bd0c1a211e8` | `FAIL: reading L grades keys differ: missing ['mu2'], extra []`; exit 1, then 0 after reversal |
| Partial-Decide dynamic-import refusal | called `builtins.__import__` at `61c172657bcde93d9fc4f9773785807a8ea4f560` | `FAIL: ... uses prohibited dynamic execution/import attribute __import__`; exit 1, then 0 after reversal |
| Partial-Decide source closure | omitted `derivation.observe` at `e24548b0ee503ba249ebae19628ccfd477cef8b6` | `FAIL: derivation.candidates has unpinned derivation dependencies: derivation.observe`; exit 1, then 0 after reversal |
| Partial-Decide conjecture freeze | removed inherited `G4_REMAINS_CONJECTURE` at `ae5d1f651dee47e34a0138df1caf2590e20551b8` | `FAIL: status input required_terminals differ from G3/G4 freeze`; exit 1, then 0 after reversal |
| Partial-Decide module mapping | mapped `derivation.model` to `observe.py` at `3f5fdd16cafbf82304b512e7196c289d16b8d4d6` | `FAIL: module/path mismatch for derivation.model`; exit 1, then 0 after reversal |
| Partial-Decide shadow refusal | registered local `derivation.py` at `12b9f3de4287456a20a2b7b26e34871cb795c18b` | `FAIL: reserved derivation shadow path: research/partial_decide/derivation.py`; exit 1, then 0 after reversal |
| Partial-Decide package-tree pin | replaced the pinned tree with zeroes at `6b30c490aebcc52f80f548a34f3458f65b0b947e` | `FAIL: source package tree mismatch`, naming wanted, snapshot, and HEAD trees; exit 1, then 0 after reversal |
| Partial-Decide refusal-policy pin | replaced the refusal with a totalizing policy at `1f5ee586fd7890fdb8d9cae9b9141886dba761e6` | `FAIL: source policy differs from the exact refusal declaration`; exit 1, then 0 after reversal |
| Partial-Decide exact snapshot | replaced the commit id with `HEAD` at `15c8ab7d57d80bbefdd129f82013881131349d47` | `FAIL: source snapshot commit must be an exact 40-digit lowercase hex id`; exit 1, then 0 after reversal |
| Partial-Decide early custody | dirtied tracked `c3_receipt.py` before preflight | `FAIL: partial-Decide executable package or transport policy has worktree changes before custody preflight`, naming the file; exit 1, then 0 after reversal |
| Partial-Decide package census, first diagnostic | committed an unlisted consumer at `758ec430baaa946177a5948676f4049a4d86333f` | `FAIL: tracked package census differs across declaration, HEAD, and index`; exit 1, then 0 after reversal. It detected divergence but did not name the injected file, so this first probe did not meet the diagnostic standard |
| Partial-Decide package census, repaired diagnostic | repeated the unlisted consumer at `431d172bee890ae37fa7e5fabcadefa5e19f0fda` | `FAIL: ... research/partial_decide/zzz_consumer_probe.py [declaration=no, HEAD=yes, index=yes]`; exit 1, then 0 after reversal |
| Partial-Decide mypy census | added an uncommitted type-invalid consumer | mypy named the incompatible assignment and checked six source files; exit 1, then five clean files and exit 0 after reversal |
| Partial-Decide transport attribute | changed `-text` to `text` at `80ddae268710c4d0a5be671ad254cfa7b4fa6944` | `FAIL: receipt transport attribute must be committed as -text`; exit 1, then 0 after reversal |
| Partial-Decide CRLF refusal | committed CRLF receipt bytes at `5e1eb4b2ac42e06f565272b55130bbe9dd9819b9` | `FAIL: partial_decide_c3.json contains CR bytes`; exit 1, then 0 after reversal |
| Partial-Decide class-key binding | exchanged members between two L/mu1 classes while preserving counts and the exact partition | `test_literal_receipt_contract_binds_members_to_canonical_classes` now reports `canonical key differs`; the pre-repair verifier at `4869cb2` accepted the same mutation |
| Partial-Decide duplicate JSON names | duplicated root `policy` and nested `authority_effect` names with authorization-bearing last values | `test_json_decoder_rejects_root_and_nested_duplicate_keys` reports `duplicate JSON key`; the pre-repair decoder accepted both through last-wins semantics |
| Partial-Decide status namespace | added `statuses.g4_result = G4_HOLDS_UNDER_MU2` | the status mutation test reports `G1 class statuses keys differ`; the pre-repair verifier at `4869cb2` accepted it |
| Ledger conformance, tab heading | `###\tCL-ZZZ-SMUGGLED` appended to the ledger text | `test_injection_tab_heading_is_not_invisible`: the ATX population sees it, the classifier names it, `KNOWN_CLAIM_IDS` fails. A space-only `### ` scan would have dropped it from both sides |
| Ledger conformance, empty fields | `**Statement**: .` (and the other seven keys) | `test_injection_empty_fields_are_missing_not_present`: each required field is missing; a presence-only check stayed green |
| Ledger conformance, rewritten body | CL-0-INERTIA statement replaced with a lie that keeps every key | `test_injection_rewritten_inertia_body_breaks_the_pin`: body pin digest moves; ID ratchets would have stayed green |
| Ledger conformance, match-arm index | synthetic `| exact =>` / comment words `that worth of carrying` | `test_match_arm_and_comment_words_are_not_declarations`: those strings are absent from the declaration index; constructors `| name (` still index |
| Ledger conformance, root wildcard | token `Derivation.*` | `test_root_namespace_wildcard_does_not_resolve`: returns false. `PresentationRelativity.*` still resolves |
| Prose watchlist, new hit | appended one line carrying a watched noun to `research/notes/README.md` | `FAIL: NEW HIT: research/notes/README.md: watched term 1d1d155e7584 appears 1 times, pinned 0 -- line 15 '…'`, exit 1; `prose watchlist clean: 49 watched terms, 153 files with pinned hits, 1886 hits` and exit 0 after `git checkout` of the file |
| Prose watchlist, stale pin | deleted the one line of `research/notes/peirce_semiotics_note.md` carrying a pinned noun | `FAIL: STALE PIN: research/notes/peirce_semiotics_note.md: watched term d4e3fc7b0477 appears 0 times, pinned 1; if the removal is intended, regenerate with --regen`, exit 1; exit 0 after reversal |
| Prose watchlist, real case | (found live, not injected) the gate's own test file used an outside proper name as a tokenization sample | `FAIL: NEW HIT: tests/test_prose_watchlist.py: watched term 5cc10d9143b2 appears 2 times, pinned 0 -- line 48 '…'; line 49 '…'` on the first run over the staged tree; the sample was reworded, the pin was NOT regenerated |
| Prose watchlist, stemmer over-reach | (found live, not injected) the phrase "prose hopes" in `research/convention_price/PROMPT.md` was pinned as a hit on a watched three-letter noun: the `es` strip reached it through a vowel | the strip was narrowed to the English rule (after s, x, z, ch, sh), `test_es_strip_does_not_reach_a_three_letter_stem_through_a_vowel` fixes it, the gate then reported `STALE PIN: research/convention_price/PROMPT.md: … appears 2 times, pinned 3`, and the pin dropped by exactly that one hit on the next deliberate `--regen` |
| X310 verifier entry point, clean interpreter (2026-09-23) | found live: execute the documented script with no site-preloaded modules, from both the tree and repository roots | both `test_verifier_help_without_site_preloaded_modules` cases failed with `ImportError` from local `types.py` shadowing the standard library; both pass after removing only the script directory from the initial search path; the complete verifier and regenerated receipt check also pass |
| Root suite, external contact-file candidates, shallow checkout (2026-09-23) | in `tests/test_primitive_contact.py`, put back the unguarded third-ancestor index (`base.parents[2]` for `*base.parents[2:3]`); an earlier probe did the same to the first form of the guard | `test_external_candidates_tolerate_a_shallow_checkout` failed with `IndexError: 2`, exit 1; exit 0 with the original bytes restored |
| Same, main-checkout base | dropped the main checkout from the candidate bases | `test_a_linked_worktree_searches_where_the_main_checkout_does` failed, naming the missing main-checkout candidate `C:/u/src/repos/repo/external/file.lean`, exit 1; exit 0 when restored |
| Same, common-directory check | returned the git common directory's parent without checking that it is named `.git` | `test_main_checkout_is_read_from_the_git_common_directory` failed with `assert WindowsPath('C:/srv') is None`, exit 1; exit 0 when restored |
| New-tree contract, second-derivation rung (2026-09-23) | an untracked `research/second_zzz_probe/` shaped as the seed's section 4 requires (`PROMPT.md`, `PREDICTIONS.md`, `STATUS.md`, `CLAIM_LEDGER.md`, `verify_pins.py`, a manifest recording the seed's sha256), run through `main`'s checker at `ed028912` | `FAIL: research/second_zzz_probe/CLAIMS.md: require exactly this claim-document filename`, then `verify.py` and `TREE_CONTRACT.json` failures: no rung that obeys its seed could pass. The patched checker exits 0 on the same probe |
| Same, patched, claim document | removed the probe's `CLAIM_LEDGER.md` | `FAIL: research/second_zzz_probe/CLAIM_LEDGER.md: require exactly this claim-document filename (research/second/SEED.md, section 4)`, exit 1; exit 0 when restored |
| Same, patched, seed binding | replaced the probe's manifest with `{}` | `FAIL: research/second_zzz_probe/SOURCE_MANIFEST.json: records no pinned seed hash, so the new-tree contract applies`, then the three new-tree failures, exit 1; exit 0 when restored, and exit 0 after the probe was deleted |
| Same, seed binding by path (review of #233) | put back the first binding, which accepted the seed's sha256 anywhere in the manifest text | `test_the_seed_must_be_recorded_at_its_path_and_hash` failed: a manifest naming the hash only in a note was accepted as a rung with no failure at all; exit 0 with the binding restored to an entry whose `path` is the seed and whose `sha256` is the pin |

The Partial-Decide injection commit IDs above are local throwaway objects with
no branch or tag reachability; they may be pruned and are locators rather than
durable evidence. `research/partial_decide/STATUS.md` records the exact
mutation, command, diagnostic, exit, and recovery needed to replay the repaired
package-census probe without relying on its commit object.

What injection does NOT prove: that the population is the right
mathematical object. A perfect pin of the wrong set is still the wrong set.
An earlier version added that it "cannot close the parked-module axiom
residual above — it can only demonstrate that the residual is still live".
That is WITHDRAWN as to the parked-module residual, which is closed, and
injection is exactly how the closure was shown to bite. The general point
survives and still applies to the research-tree axiom receipt above:
injection demonstrates that a residual is live; it does not close one.

## G012 wrapped axiom reports, 2026-09-23

The new native admission obstruction generated long helper names whose axiom
lists Lean wraps over two lines. The existing single-line reader rejected
five such reports as missing. A three-case parser regression uses an actual
wrapped helper report, a forbidden-axiom mutation, and an unterminated list.
Before the repair, the allowed report failed and the forbidden report was
misclassified as missing (two failures, one pass). After reading complete
records across wrapped lists, all three tests pass: the allowed report is
counted, the forbidden axiom is named by the violation, and the malformed
report remains missing. No generated helper is excluded from the census.

## Direct verifier startup (2026-09-23)

The full research custody census exposed a clean-interpreter failure in
`research/x310_vertical_integration/verify_sources.py`: its local `types.py`
shadowed the standard library before source verification began. The same
startup problem affected `verify.py`. Four regression cases execute both
scripts with `python -S`, from the repository root and the tree directory.
All four failed with the import error before the repair and passed afterward.
Each script now removes its own script-directory search entry before importing
standard-library dependencies; qualified model imports retain their scope.
The tree's full verifier and receipt remain independent checks.

## Evidence graph controls, 2026-09-23

These are synthetic input mutations in the new consumer's tests. They exercise
the named schema and population guards without editing a sealed source theorem,
altering another tree's verifier, or regenerating a scientific receipt under
an injection. Recovery is the unmodified fixture or byte-identical regeneration.

| Guard | Injected input defect | Named failure or discriminating result |
|---|---|---|
| Header census | nested comment containing an import, string mention, or import-looking text after the module body | none joins the header-import population; malformed headers fail by name |
| Typed links | missing parent bridge or assumption | LINK_MISSING; empty conditional assumptions give CONDITIONAL_ASSUMPTIONS_MISSING |
| Source custody | changed source digest or wrong replay head | SOURCE_REFERENCE_MISMATCH; REPLAY_NOT_SUCCESSFUL |
| Compiled scope | stale declaration or added local premise in a report | THEOREM_NOT_IN_REPORT; THEOREM_SCOPE_CHANGED; altered payload gives COMPILED_PAYLOAD_CHANGED |
| Finite scope | increase the claim's bound, or increase both claim and computation without a renewed review | FINITE_BOUND_SCOPE_CHANGED |
| Native lineage | relabel a parallel research fixture native without its parent map | NATIVE_BRIDGE_MISSING |
| Headline population | remove a headline while retaining its expected source population, or supply an empty population | HEADLINE_POPULATION_MISMATCH; HEADLINE_POPULATION_EMPTY |
| Independent verifier | substitute an aggregate helper for the named tree-local command | INDEPENDENT_VERIFIER_SUBSTITUTED; foreign origin gives INDEPENDENT_VERIFIER_ORIGIN |
| Artifact population | add, remove or change a generated artifact | ARTIFACT_POPULATION_MISMATCH; GRAPH_ARTIFACT_DIFFERS |
| Incremental custody | delete a cached headline or alter the bound graph | REFRESH_CACHE_POPULATION_CHANGED; source drift invalidates its descendants while historical evidence remains unchanged |
| Corrected source custody | absent or duplicate subject, a source from another subject, stale span, failed check, absent check link, or a check of another tree | CORRECTION_POPULATION_MISMATCH; CORRECTION_SUBJECT_SOURCE_MISSING; SOURCE_REFERENCE_MISMATCH; CORRECTION_CHECK_FAILED; CORRECTION_CHECK_LINK_MISSING; CORRECTION_CHECK_WRONG_TREE |
| Correction publication boundary | unmerged or unavailable main ancestry, the original source presented as a correction, or promotion to a theorem | CORRECTION_NOT_MERGED; CORRECTION_REQUIRES_NEW_SOURCE_VERSION; CORRECTION_DISPOSITION; corrected wording retains its open mathematical obligations |

## Foundations trees registered in the local gates (2026-09-23)

Plan G registered the four foundations trees:

- each tree's canonical `verify.py --check` runs in the `lean` job;
- each tree's `run.py --check` runs in the `research` job.

Every injection below was made on disk, uncommitted, in a worktree of
`chore/foundations-registration`, and reverted with `git checkout` or a
byte copy. The step was then re-run and exited 0. No receipt or pin was
regenerated while an injection was live.

| Step | Injection | Observed failure |
|---|---|---|
| `lean`: native_bridge tree verifier | one byte appended to the pinned `input.json` | exit 1; `FAIL: SOURCE_MANIFEST.json: stale pin population or digest: ['research/native_bridge/input.json']` |
| `lean`: native_structure tree verifier | the same, on its `input.json` | exit 1, naming `research/native_structure/input.json` |
| `lean`: conservation_ladder tree verifier | the same, on its `input.json` | exit 1, naming `research/conservation_ladder/input.json` |
| `lean`: domain_adapters tree verifier | the same, on its `input.json` | exit 1, naming `research/domain_adapters/input.json` |
| `lean`: native_bridge tree verifier, axiom scope | `#print axioms ResearchNativeBridge.run_step` appended to `AxiomReport.lean`, outside the contract's declared list | exit 1; `FAIL: AxiomReport.lean: expected [...], reported [...]`, listing `ResearchNativeBridge.run_step` among the reported names |
| `lean`: native_bridge tree verifier, forbidden token | a comment carrying the forbidden proof-shortcut word appended to `Path.lean` | exit 1; `FAIL: lean\ResearchNativeBridge\Path.lean: forbidden proof shortcut` |
| `research`: native_bridge receipt | `"authority_effect": "None"` changed to `"Nonf"` in `evidence/receipt.json` | exit 1; `FAIL: evidence/receipt.json differs from a fresh computation` |
| `research`: native_structure receipt | the same | the same failure |
| `research`: conservation_ladder receipt | the same | the same failure |
| `research`: domain_adapters receipt | the same | the same failure |

## Seed-contract selection, real case (2026-09-23)

Found live, not injected. Rung three (`research/second_index`, #239)
records `research/second/SEED.md` in its manifest with the correct digest
in upper case. `ci/check_new_research_trees.py` compared that digest with
its lower-case constant, so it did not select the seed's rung contract and
failed the rung by name:

- `FAIL: research/second_index/SOURCE_MANIFEST.json: records no pinned seed hash, so the new-tree contract applies`
- the ordinary contract's `CLAIMS.md`, `verify.py` and `TREE_CONTRACT.json` failures

`tests/test_new_research_tree_contract.py::test_current_repository_is_grandfathered_and_clean`
was red on `main` at `013be46f`. That was the coordinator's error: #239 was
merged before this check's result was read.

**The repair.** `records_seed` compares a string digest without regard to
letter case. With it the live check is clean and the test passes.

**The test added.** It accepts the upper-case record, and still refuses a
non-string digest, a wrong digest, and the seed's hash at another path.

## Rung three's registered test step, real cases (2026-09-23)

Found live, not injected, after #239 merged. Both come from the
coordinator's merge, not from the rung's own run.

- **Scope scan on `main`.** `test_the_scan_sees_this_branch_at_all` failed
  on `main` at `03409c1c`: with HEAD as the comparison base, it asserted
  over an empty change set. It is the defect `second_nofirst` recorded
  at `7d2e6e86`. The same scan also attributed every branch's commits to
  the rung, so a branch touching another research tree failed
  `test_no_sibling_research_tree_is_written`. Observed on
  `chore/custody-drift-report`, naming `research/diagonal_identity/STATUS.md`.
- **Line endings on a fresh Windows checkout.**
  `test_the_log_is_stored_with_no_carriage_return` refused
  `receipts/lean_axioms.txt`, because the tree lacked the sibling rungs'
  `-text` attributes.

**The repair** is in `research/second_index/` alone:

- the scan reads only commits that touch the write root;
- the non-vacuity guard skips both empty cases by name;
- `.gitattributes` matches the siblings'.

A synthetic test covers the ownership rule: a sibling commit is not the
rung's, and a mixed commit exposes every path.

## Custody verifiers report HEAD drift (2026-09-23)

Six research-tree custody verifiers were converted so that provenance at
the snapshot fails and drift at HEAD is reported (`CLAUDE.md`, "A research
tree's pins certify its snapshot, not the present").
`research/primitive_difference_tower/verify_manifest.py` was left strict by
the author's decision of 2026-09-23.

**The injection.** One throwaway commit, `0c68e56d`, on top of `7841d7bf`
(this branch before its rebase onto `main`; the six verifier files are
byte-identical after the rebase), appended one line each to five pinned
sealed files:

- `lean4/Derivation/PrimDiff.lean`
- `lean4/Derivation/Quot.lean`
- `lean4/Derivation/Apartness.lean`
- `code/derivation/iso.py`
- `code/derivation/engine.py`

The commit was discarded with `git reset --hard 7841d7bf`. No receipt was
regenerated while it was live.

| Verifier | Plain run under the injection | `--require-current` under the injection | After discard |
|---|---|---|---|
| `research/diagonal_identity/verify_pins.py` | exit 0; `DRIFT: lean4/Derivation/PrimDiff.lean at HEAD is 7BC6DDB5…, pinned F46C3BC4…`; five sealed-path `DRIFT:` lines; count 6 | exit 1; `FAIL: pinned inputs moved between the snapshot and HEAD (--require-current):`, naming `lean4/Derivation/PrimDiff.lean` | exit 0 both ways; drift 0 |
| `research/higher_order_diagonalization/verify_sources.py` | exit 0; `DRIFT: code/derivation/iso.py at HEAD is 41CE33CE…, pinned B0F1F3BC…`; count 6 | exit 1, naming `code/derivation/iso.py` | exit 0 both ways; drift 0 |
| `research/natural_sections/verify_pins.py` | exit 0; `DRIFT:` for `lean4/Derivation/Apartness.lean` and `lean4/Derivation/PrimDiff.lean`; count 7 | exit 1, naming both modules | exit 0 both ways; drift 0 |
| `research/seventh_constructor/verify_sources.py` | exit 0; `DRIFT: code/derivation/iso.py at HEAD is 41CE33CE…`; count 6 | exit 1, naming `code/derivation/iso.py` | exit 0 both ways; drift 0 |
| `research/twin_pricing/verify_sources.py` | exit 0; `DRIFT: lean4/Derivation/Quot.lean at HEAD is 7FFB8282…, pinned 0D1DF5E6…`; count 6 | exit 1, naming `lean4/Derivation/Quot.lean` | exit 0 both ways; drift 0 |
| `research/second_nofirst/verify_pins.py` | exit 0; `DRIFT: source moved at HEAD for code/derivation/engine.py`; count 1 | exit 1, naming `code/derivation/engine.py` | exit 0 both ways; drift 0 |

**Provenance still fails.** Each tree's own tests keep the snapshot-side
failures, for example a mutated recorded hash is refused as a mismatch at
the snapshot. The new tests also cover a pin that is tracked at HEAD but
cannot be read: it still fails as `could not read`.

## Rung three's custody verifier reports HEAD drift (2026-09-24)

`research/second_index/verify_pins.py` was the one second-derivation
verifier left strict after the six above. It was converted the same way:
a port of the `second_nofirst` change, with the same four tests. Its
`STATUS.md` is untouched, because the next blind rung reads it.

**The injection.** One throwaway commit, `11e36dbd`, on top of
`f959dcb2`. That is the conversion commit before it moved onto this
branch as `c724fe6a`; the tree is byte-identical between the two. The
throwaway commit:

- appended one line to `code/derivation/engine.py`, a pinned sealed
  source;
- prepended one line to `research/second/PLAN.md`, which is pinned whole
  and by the span `26-32`.

The commit was discarded with `git reset --hard f959dcb2`. No receipt was
regenerated while it was live.

| Run | Under the injection | After discard |
|---|---|---|
| plain | exit 0; `DRIFT: source moved at HEAD for code/derivation/engine.py: expected 23803A3D…, got E798E8A5…`; the same for `research/second/PLAN.md`; `DRIFT: span moved at HEAD for research/second/PLAN.md:26-32`; count 3 | exit 0; drift 0 |
| `--require-current` | exit 1; `FAIL: pinned inputs moved between the snapshot and HEAD (--require-current):`, naming all three | exit 0; drift 0 |

**Provenance still fails.** The tree's existing tests keep every
snapshot-side refusal by name, and the new tests cover a pin that is
tracked at HEAD but cannot be read.

## The runner's timeout-restore test, made deterministic (2026-09-24)

`tests/test_run_gates.py::test_a_timeout_restores_tracked_research_receipts`
failed once in a full python job run on 2026-09-24, under heavy machine load.
It gave its step a 0.5 s timeout. The timeout fired before the shell had run
its first line, so the receipt was never rewritten, and the result's note
was empty. The runner was not at fault.

**The fix.** The step now writes the receipt, then an untracked marker, then
sleeps 60 s. The timeout doubles from 1 s to 16 s until the marker shows that
the write happened. The restore note is asserted on that attempt. The
receipt's bytes and the TIMEOUT outcome are asserted on every attempt.
`ci/run_gates.py` is unchanged.

**The race, reproduced.** A scratch script put `sleep 1.5` before the write,
standing in for a slow shell start:

- the old logic (one 0.5 s timeout) gave `TIMEOUT` with note `''`, the
  observed failure;
- the new logic gave no marker at 1 s, with the bytes still restored, then
  the marker and the note
  `rewrote research/probe/receipts/value.json; restored` at 2 s.

**The injections.** Each edited `ci/run_gates.py` in the working tree only,
and each was reverted with `git checkout -- ci/run_gates.py`. No receipt was
regenerated while one was live.

| Injection | The fixed test under it | After revert |
|---|---|---|
| A: no restore after a timeout (`restored = []` when the outcome is `TIMEOUT`) | fails: `research/probe/receipts/value.json was not restored after a 1 s timeout` (`b'partial\n' == b'original\n'`) | passes |
| B: the restore happens, but the note naming it is dropped | fails: `the note does not name the restored receipt: ''` | passes |

## Two refused words, enforced without a pin (2026-09-24)

By the author's ruling of 2026-09-24, two watched words are not allowed
anywhere in this repository. Pull request #246 had used both in
`research/exchange_coefficients` and was merged with gate 12 red. The fix
removes them from that tree and adds
`tests/test_refused_words.py::test_no_refused_word_appears_in_any_tracked_path_or_file`.
The test stores each word as a digest with its length, cuts every tracked
file's text and every tracked path into letter runs, and fails on any run
holding either word. It has no pin, so no regeneration can adopt a hit.

**The defect it exists to catch.** Run against `a371ab74`, main as #246 left
it, the test named 15 places. Four of them were invisible to gate 12: the
note's file name as a path, a `snake_case` column name in the note, and the
same file name inside the tree's README and its receipt.

**The injections.** Each was made in the committed fix's working tree and
reverted with `git checkout` (or a reversing `git mv`). No receipt was
regenerated while one was live.

| Injection | The test under it | Gate 12 under it | After revert |
|---|---|---|---|
| A: the first word as prose, appended to `research/exchange_coefficients/README.md` | fails: `README.md:92` | fails: new hit | passes |
| B: the second word inside a `snake_case` name appended to `bipartite_index.py` | fails: `bipartite_index.py:277` | **clean**: identifiers are outside its reach | passes |
| C: the index note renamed so its path holds the first word | fails: `path holds` the word | clean | passes |

## Estate hygiene: three repaired trees, four receipt trees, seven Lean audits (2026-09-24)

Four pull requests, integrated and gated together. Each injection was a
minimal edit to a committed tree, run against the check it exists to catch,
reverted with `git checkout`, and run again. No receipt, inventory or pin was
regenerated while an injection was live.

**#250: three trees repaired.**

| Check | Injection | Failing line | After revert |
|---|---|---|---|
| `endogenous_demand/verify_lean.py` | the report line for `endogenous_termination_bound` deleted | `FAIL: report/census mismatch: missing=['EndogenousDemandObstruction.endogenous_termination_bound']` | passes |
| `endogenous_demand` census test and verifier | an unreported theorem appended | `Lists differ: ['injected_unreported'] != []`; verifier `missing=['injected_unreported']` | passes |
| `cost_cohomology` file-set pin | an extra `rank_float.py` in the tree | `Lists differ: ['rank_float.py', ...]` | passes |
| `cost_cohomology` no-numpy check | `import numpy` added to `verify_sources.py` | `Regex matched: 'import numpy' ... : verify_sources.py` | passes |
| `admit_leftover` collection guard | one check renamed so it is not collected | `COLLECTION_GUARD: collected 9 tests, expected 10` | passes |

**#251: four exact-arithmetic trees registered, x300 refuses bad rows.**

| Check | Injection | Failing line | After revert |
|---|---|---|---|
| p208a test-count minimum | one test hidden | `ran 20 tests; minimum is 21` | 21 pass |
| p208b test-count minimum | one test hidden | `ran 24 tests; minimum is 25` | 25 pass |
| p208c test-count minimum | one test hidden | `ran 14 tests; minimum is 15` | 15 pass |
| p209c test-count minimum | one test hidden | `ran 28 tests; minimum is 29` | 29 pass |
| receipt diff, each of the four trees | a comment line in the tree's module, no regeneration | `FAIL: existing receipt does not match freshly generated verification` | passes |
| p209c receipt diff | the committed receipt's `"passed"` changed from 29 to 30 | the same line | passes |
| p208c strict typing | a mistyped assignment | `tomography.py:312: error: Incompatible types in assignment` | clean |
| p209c strict typing | a mistyped assignment | `stabilizer_codes.py:177: error: Incompatible types in assignment` | clean |
| p208a negative test | the unlisted-order refusal disabled | `FAILED ...::test_cyclotomic_rational_refuses_an_unlisted_order` | passes |
| p208b negative tests | the negative-entry check disabled | `FAILED ...::test_negative_entry_is_refused_even_when_the_row_sums_to_one`, and the bound test | passes |
| p208c negative test | the empty-carrier refusal disabled | `FAILED ...::test_commutation_obstruction_refuses_an_empty_carrier` | passes |
| p209c negative test | the inconsistent-syndrome refusal disabled | `FAILED ...::test_steane_code_weight_two_errors_are_not_corrected` | passes |
| x300 refusal | the old rescaling restored | `4 failed, 19 passed` | 23 pass |

**#252 and the integration: seven Lean audits registered in the `lean` job.**

| Step | Injection | Failing line | After revert |
|---|---|---|---|
| natural_sections | `wedge_total_positive` proved through `Classical.em` | `FAIL: NaturalSections.SignRepair.wedge_total_positive depends on disallowed axioms: ['Classical.choice']` | passes |
| balance_carrier | one `#print axioms` line removed from `AxiomReport.lean` | `FAIL: BalanceCarrier.Observer.layer_observer_grades is declared in LayerObserver.lean but not listed in AxiomReport.lean` (main's script passed this injection) | passes |
| convention_price, axioms | `holo_nil` proved through `Classical.em` | `FAIL: ConventionPrice.holo_nil depends on disallowed axioms ['Classical.choice']` | passes |
| convention_price, census | one `#print axioms` line removed | `FAIL: ConventionPrice.cycle_parity_sum is declared in ParityLaws.lean but not listed in AxiomReport.lean` | passes |
| closed_family | a comment line carrying a forbidden token | `FAIL: Closure.lean contains forbidden token sorry` | passes |
| coherent_process_limits | `Limits.toSeq_ofSeq` proved through `Classical.em` | `FAIL: disallowed reliance: Limits.toSeq_ofSeq: ['Classical.choice', 'Quot.sound', 'propext']` | passes |
| boundary_seed | `supply_no_op` proved through `Classical.em` | `FAIL: disallowed axioms ['Classical.choice'] in BoundarySeed.supply_no_op` | passes |
| endogenous_continuum (integration) | `sumAllocated_nil` given a `Classical.choice` term | `FAIL: Disallowed axioms in theorem AdaptiveBudget.sumAllocated_nil: {'Classical.choice'}` | passes |
| estate_honesty, dropped tree (2026-09-25) | removed `blind_restart`'s three research-job steps and `closed_family`'s lean-job step from `verify.yml`, `research/README.md` regenerated | `AssertionError: ... research-job trees dropped from the workflow: ['blind_restart']` and `Lists differ: ['closed_family'] != []` in the lean-job test | passes |
| estate_honesty, two readings agree (2026-09-25) | `audit_estate.py`'s new `working-directory` lean-job read disabled | `test_lean_ci_axiom_gate_counts`: `Items in the second set but not the first:` naming `native_bridge`, `p208a_path_interference`, `domain_adapters` and six more | passes |
| closed_family, Base.lean census (2026-09-25) | `#print axioms ClosedFamily.symm_symm_car` removed from `AxiomReport.lean` | `FAIL: ClosedFamily.symm_symm_car is declared in Base.lean but not listed in AxiomReport.lean`, exit 1 (main's script, with main's list minus `zeroRel_transport`: `lean audit clean: ... 20 axiom reports ... 14 originating theorems all listed`, exit 0) | passes |
| x300 float refusal (2026-09-25) | the `limit_denominator(10**9)` path restored ahead of the refusal | the four `TestFloatRefusal` tests that pass a float fail by name | 28 pass |
| p208c zero scalar (2026-09-25) | `True` restored as the answer at `c = 0` | `test_commutation_at_zero_is_not_obstructed` fails | 16 pass |
| record_reading file pins (2026-09-25) | one line appended to the consumed `research/coherent_process_limits/lean/Observe.lean` | `FAIL: SOURCE_CHANGED: ...Observe.lean` and `FAIL: CONSUMED_TRACKED_DIFF: ...Observe.lean`; the same edit to the unconsumed `Limits.lean` and to that tree's `README.md` passes (the README edit failed as `CONSUMED_TRACKED_DIFF` before this change) | passes |
| iso_sound opened file (2026-09-25) | one line appended to `tests/test_iso.py` | `FAIL: SOURCE_CHANGED: tests/test_iso.py` (no pin on origin/main named it) | passes |
| unboundedness Lake config (2026-09-25) | one line appended to `research/magnification/lean/lakefile.toml` | `FAIL: SOURCE_CHANGED: ...` and `FAIL: CONSUMED_TRACKED_DIFF: ...` for that file (no pin on origin/main named it) | passes |
| ignition file pins (2026-09-25) | one line appended to the consumed `research/local_reuse/lean/LocalReuse.lean` | `FAIL: SOURCE_CHANGED: ...LocalReuse.lean` and `FAIL: CONSUMED_TRACKED_DIFF: ...LocalReuse.lean` | passes |

## Genesis closeout: the Alpha admission boundary (2026-09-25)

The closeout audit of `research/alpha_engine` (PR #268, `docs/GENESIS_CLOSEOUT.md`
section 7) reproduced three admission defects through the real path and
repaired them in one pass. `python research/alpha_engine/inject_boundary.py`
reverts each repair in the real `driver_a.py`, shows the named failure,
and restores the file; the coordinator re-ran it at the final audit. The
last two rows were run by hand against `python verify.py`. No receipt was
regenerated while any injection was live. These rows are written here at
the author's instruction of 2026-09-25 to finish the closeout; they also
stand in `research/alpha_engine/STATUS.md`.

| Gate | Injection | Observed failure | Recovery |
|---|---|---|---|
| B1 member (M1) | `apply_licensed` executes `representative_delta(result, key)` again and both `check_evidence` calls are removed | `B1 REPRODUCED: apply_licensed executed an empty substituted member of an authorized key`; the same for a member of an unauthorized class, through `explore`, and for a forged cost (4 tests) | 4 tests pass with the bytes restored |
| H5 evidence (M5) | the `check_evidence` call in `apply_licensed` removed and the caller's member executed | `H5 REPRODUCED: apply_licensed accepted evidence from which two retained classes had disappeared` | 1 test passes |
| B2 node integrity (M2) | `check_node_integrity(node)` removed from `bound_evaluation` | `B2 REPRODUCED: apply_licensed accepted a parent whose history does not replay to its stated regime`; the same through `explore` | 2 tests pass |
| B3 binding (M3, M4) | `check_license_binding` removed and the fresh evaluation taken from the call (target, the evidence's measure and bounds), as before the repair | `B3 REPRODUCED: a License granted at one source node was accepted at a relabelled source`; also another history, target `(1, 2)` used at `(0, 1)`, mu1 used for mu2, `Bounds(2, 2)` used under `(2, 3)` and `(2, 1)`, through `explore`; and `H4 REPRODUCED: a unique mu2 class was admitted under a License granted for mu1` (8 lines, 7 tests) | 7 tests pass |
| One command, failing check (M8) | one byte of `evidence/handoff_demo.json` changed | `FAIL: test_committed_record_matches (test_handoff.HandoffDemonstrations...)`, `FAIL: tests exited 1`, the seven later steps listed `NOT RUN`, exit 1 | exit 0, all nine steps PASS |
| One command, skipped check (M8) | `evidence/lean.json` moved aside, so a unit test skips | `SKIPPED CHECK: tests: test_lean_gate.CommittedRecord.test_record_is_within_the_whitelist_and_not_a_proof`, `FAIL: tests skipped a check`, later steps `NOT RUN`, exit 1 | exit 0 |

## Textbook verification gate (2026-10-28, PR #287 review)

| Gate | Injection | Observed failure | Recovery |
|---|---|---|---|
| `lean` job Python setup (`tests/test_run_gates.py`) | `actions/setup-python@v5` or `Install pinned dependencies` removed from `lean:` in `.github/workflows/verify.yml` | `AssertionError: job 'lean' is missing actions/setup-python@v5` | passes with both steps present before the first Python command |
| `textbook` job book-Lean gate (`ci/check_textbook.py --lean-only`) | `freshTok s12 = 3 := rfl` changed to `freshTok s12 = 99 := rfl` in `textbook/checks/u59_lean.py` | `FAIL: textbook/checks/u59_lean.py exited 1` (`U59.lean:7:0: error: Not a definitional equality ... lean exit code 1`), exit 1 | exit 0 (`textbook book-Lean checks: 71 passed`) |
| `textbook` video pacing gate (`ci/check_textbook.py --python-only`) | first segment in `textbook/video_script_15s.md` changed to 11 words in 3 s (220 wpm) | `FAIL: video_script_15s.md: segment 0:00-0:03: pace 220.0 wpm exceeds 160.0 wpm`, exit 1 | exit 0 (`video_script_15s.md pacing: ok (4 segments, 15s total, all <= 160 wpm)`) |

## First-steps route and research inventory (2026-10-28)

No sealed file or research receipt was changed. The inventory injection
used a generated scratch Wiki; the load injection used a disposable copy
of the explorer. No receipt was regenerated while either defect was live.

| Gate | Injection | Observed failure | Recovery |
|---|---|---|---|
| `textbook/media/verify_wiki_textbook.py` | Remove the `boundary_seed` table row and insert an excluded `notes` row in a generated research index | exit 1: `research inventory mismatch; missing research tree: boundary_seed; unexpected research tree: notes` | Restore the original bytes; exit 0, all 123 trees and 1,964 internal Wiki links checked |
| First-steps browser load | Serve a copied explorer with its `cards.json` absent | Visible supplied-table load error; Run, Check recovery, and Reset disabled | Remove the temporary fixture; the ordinary explorer and single-file bundle display the declared cards, groups, and blocking pair |

## Search-lab records and results desk (2026-10-28)

Only generated scratch Wiki files and temporary/in-memory teaching copies
were changed. No sealed source or receipt was rewritten. No regeneration
ran while either scratch-Wiki injection was live.

| Gate | Injection | Observed failure | Recovery |
|---|---|---|---|
| Wiki search-lab asset consistency | Remove one mu1 minimum from the copied `media/search_lab/recorded_lab.json` | Actual Wiki verifier exits 1: `stale search-lab record: recorded_lab.json` | Restore bytes; exit 0, 2,034 generated internal links pass |
| Wiki search-lab desk consistency | Substitute `null` for the embedded packet in a copied `results.html` | Actual Wiki verifier exits 1: `stale search-lab results desk or unresolved reading/download links` | Restore bytes; exit 0 |
| Full lesson-record check | Drop a raw minimum or change an exported price to `[999,999]` in temporary records | `check_recorded` raises the named record/export mismatch; both unit tests pass only on this refusal | Unchanged source-backed records pass |
| Lesson population table | Change the arity-two reading-L class count from 3 to 99 in a temporary lesson source | `check_recorded` raises `The lesson population table differs from the computed cases` | Original six-row table passes |

The lesson also evaluates separate in-memory export copies. Wrong root
hash and missing merge map fail `verify_full_export`; changed cost metadata
passes that narrower replay contract. The latter is an expected scope
boundary, not a claim that event replay validates prices. The full
lesson-record check separately rejects that price change.

## Passage teaching route (2026-10-28)

No sealed file was edited. Wiki injections used the generated scratch
Wiki; original bytes were restored before the next check, without
regenerating assets while a defect was live. The Lean injection altered
only generated source in memory and used the actual book-Lean runner.

| Gate | Injection | Observed failure | Recovery |
|---|---|---|---|
| Wiki passage record consistency | Drop one singleton proposal from the copied packet | Actual Wiki verifier exits 1: `stale change-lab record` | Restore original bytes; exit 0, 2,109 generated internal links pass |
| Wiki passage desk consistency | Replace the embedded packet binding with `null` in the copied desk | Actual Wiki verifier exits 1: `stale change-lab desk or links` | Restore bytes; exit 0 |
| Book-Lean event equality | Change only the expected after-state budget from zero to 99 in `operation_0_refine_C` | Lean rejects the equality; shared book-Lean runner exits 1 | Original 120 kernel/axiom reports pass, exactly `{propext, Quot.sound}` |
| Full passage teaching record | Forge refinement's recorded outcome or drop a singleton proposal | `check_recorded` rejects the source/record mismatch | Original packet passes |
| Passage population table | Replace the all-pairs repair count zero with 99 in a temporary source map | `check_recorded` rejects the population table | Original two-row table passes |

The five authoring tests also check the fresh single-file desk and refuse
negative tokens, endpoints, column members, and budgets in the teaching
encoding. These tests do not change the sealed Python API's integer domain
or establish a general Python-to-Lean refinement.

## Reasoning prerequisite route (2026-10-28)

Injections changed only generated scratch-Wiki files, temporary teaching
records, or generated Lean source in memory. Original Wiki bytes were
restored between checks; no regeneration ran with a live defect. No
sealed source or research receipt was edited.

| Gate | Injection | Observed failure | Recovery |
|---|---|---|---|
| Wiki reasoning record consistency | Forge a common witness from the default pairwise witnesses | Actual Wiki verifier exits 1: `stale reasoning-lab record` | Restore bytes; exit 0, 2,180 generated internal links pass |
| Wiki reasoning desk consistency | Bind the copied desk's packet to `null` | Actual Wiki verifier exits 1: `stale reasoning-lab desk or links` | Restore bytes; exit 0 |
| Book-Lean counterexample | Change `round 1 ≠ 1` to `round 1 = 1` in `reverse_fails_at_b` | Lean reports that `blue 1 = 1 ∧ round 1 = 1` is false; shared runner exits 1 | Original twelve kernel/axiom reports pass |
| Full reasoning record | Adopt the failed reverse, invent an empty-domain witness, conflate pairwise/common witnesses, or remove a recovery blocking pair | `check_recorded` rejects each source/record disagreement | Original packet passes |
| Reasoning population table | Enlarge the recorded conditional-comparison count from 147456 to 999999 in a temporary source map | `check_population` rejects the lesson population table after recomputation | Original eight-row table passes |

The false-proof injection initially encountered a Windows output encoding
failure while printing the Lean error. Repeating it with UTF-8 subprocess
output exposed the actual named proof failure above. It was not accepted
as a Lean rejection until that diagnostic was captured. The six authoring
tests and record/desk checks pass after restoration.

## Path and boundary route (2026-10-28)

Only generated scratch-Wiki files, temporary teaching records, and a
generated Lean source string were injected. Original Wiki bytes were
restored between checks. No regeneration ran with a live defect; no
sealed source or research receipt was edited.

| Gate | Injection | Observed failure | Recovery |
|---|---|---|---|
| Wiki path record | Invent an admitted ABC face when no face step was requested | Actual Wiki verifier exits 1: `stale path-lab record` | Restore bytes; exit 0, 2244 generated internal links pass |
| Wiki path desk | Bind the copied embedded packet to `null` | Actual Wiki verifier exits 1: `stale path-lab desk or links` | Restore bytes; exit 0 |
| Wiki path diagram | Change the shared AC coefficient from zero to 99 in the copied two-face SVG | Actual Wiki verifier exits 1: `stale or missing path-lab figure: 04_two_faces.svg` | Restore bytes; exit 0 |
| Book-Lean history | Replace the expected fourth vertex 3 by 99 in `faces_0_0` | Lean reports the vertex-store equality is false; shared runner exits 1 | Original 164 kernel/axiom reports pass |
| Source-backed path record | Invent a missing-edge closed walk, invent a face without its event, erase an edge with zero coefficient, retain cancellation after reversing a face, or zero the all-positive control | `check_recorded` rejects each recomputation mismatch | Original packet passes |
| Source population and figures | Enlarge face settings 256→999, or change the source figure's AC coefficient to 99 | The actual record check rejects the named population/figure mismatch | Original six-row table and five figures pass |

Nine authoring tests include those refusals, a fresh standalone desk,
and rejection of empty or out-of-domain walk sequences in the teaching
wrapper. Native cell admission and boundary cancellation remain separate.

## Map, class, and lookup route (2026-10-28)

Only temporary teaching records, generated scratch-Wiki copies, and a
generated Lean source string were injected. Original bytes were restored
between checks; no regeneration ran with a live defect. No sealed source
or research receipt changed.

| Gate | Injection | Observed failure | Recovery |
|---|---|---|---|
| Wiki map record | Declare blue-only sufficient for the paired blue/triangle answer | Actual Wiki verifier exits 1: `stale map-lab record` | Restore bytes; exit 0, 2318 generated internal links pass |
| Wiki map desk | Replace the copied embedded packet by `null` | Actual Wiki verifier exits 1: `stale map-lab desk or links` | Restore bytes; exit 0 |
| Wiki map diagram | Remove the conflict figure's dashed forks | Actual Wiki verifier exits 1: `stale or missing map-lab figure: 02_block_triangle.svg` | Restore bytes; exit 0 |
| Book-Lean empty domain | Change the expected class count from 0 to 99 in `representation_0_0_0` | Lean's `decide` reports the conjunction containing the class-count equality is false; shared runner exits 1 | Original 270 exact kernel/axiom reports pass |
| Source-backed map record | Misalign a shortened domain, invent recovery after representative reversal, recover a pair from one component, make an unused-label completion unique, or invent an empty class | `check_recorded` rejects each recomputation mismatch | Original packet passes |
| Source population and diagrams | Enlarge 512 settings to 999 or make conflict arrows solid | Actual record check rejects the population/figure mismatch | Original six-row table and five diagrams pass |

Ten authoring tests include those refusals, current standalone bundling,
explicit SVG dimensions, and successful complete lookup examples checked
against their own selected domains. Complete lookup counts use the declared
four-label input set and finite output alphabet, not all `Nat → Nat` maps.

## Growth and service route (2026-10-28)

Only scratch-Wiki copies, temporary teaching records, and a generated Lean
source string were injected. Original bytes were restored between checks;
no regeneration ran with a live defect. No research source, receipt,
prediction freeze, or sealed file was edited.

| Gate | Injection | Observed failure | Recovery |
|---|---|---|---|
| Wiki growth record | Set the bounded eight-round least clearing budget to the peak 3 rather than 1 | Actual Wiki verifier exits 1: `stale growth-lab record` | Restore bytes; exit 0, 2388 generated internal links pass |
| Wiki growth desk | Replace the copied embedded packet with `null` | Actual Wiki verifier exits 1: `stale growth-lab desk or links` | Restore bytes; exit 0 |
| Wiki growth figure | Replace displayed counts of 3 by 99 in the bounded-run SVG | Actual Wiki verifier exits 1: `stale or missing growth-lab figure: 03_bounded_clears.svg` | Restore bytes; exit 0 |
| Book-Lean growth | Change the expected post-growth count with no previously held items from 0 to 99 | Lean's `decide` reports the demand-count conjunction is false; shared runner exits 1 | Original 334 exact kernel/axiom reports pass |
| Source-backed teaching record | Ignore supplied views, erase old demands after growth, invent an empty-commitment demand, suppress reopening, save unused capacity, erase a temporary backlog, or equate peak generation with threshold | `check_recorded` rejects each recomputation mismatch | Original packet passes |
| Source population and figures | Enlarge 845 race settings to 999 or corrupt the bounded-run figure | Actual record check rejects the population/figure mismatch | Original four-row population table and four figures pass |

Eleven authoring tests also check standalone bundling and intrinsic SVG
dimensions. The book runner re-elaborates the actual research source text,
checks all fourteen originating theorem names against their report list,
and adds 320 finite growth instances. It does not reclassify assumed
service as a proved represented-world repair.

## Formal-reading and observer-interpretation review (2026-10-28)

No source or receipt was mutated for these checks. Navigation regressions
exercise the actual rewriter with isolated strings. The false mathematical
claim is appended only to a temporary book-Lean driver in memory.

| Gate | Defect exercised | Observed failure | Recovery |
|---|---|---|---|
| Wiki beginner-route navigation | The original rewriter sends a relative beginner README or source-map link to a repository blob | The new route-link regression fails at `textbook_first_steps`; it tests all seven routes | The repaired rewriter emits Wiki slugs, with anchors retained; full fourteen-test Wiki suite passes |
| Wiki reading-guide navigation | A new guide link falls through to a repository blob | The new guide regression fails on `textbook_reading_formal` | Explicit guide mapping passes; reviews and Python files retain their source URLs |
| Book-Lean semantic counterexample | Assert that the book's active stage has no active pair | Lean's `decide` reports `¬(True ∧ false = false ∧ True)` is false; shared runner exits 1 | Original eight exact reports pass: four empty axiom sets, four `propext` |

The native driver returns `closed` at that stage because the supplied next
function returns `none`; the active pair is separately proved. The failure
therefore tests the proposed semantic inference, not a parser or output
encoding error. The observer fixture also constructs a valid observer from
an arbitrary proposition without a decision argument. Neither fixture
claims a general undecidability theorem or changes the sealed definitions.

## Declaration reconciliation and classification lesson (2026-10-28)

The new textbook inventory tool reads comments separately from source heads
and binds candidates to compiled names and source locations. Its fixture
checks do not establish parser completeness or semantic teaching coverage.
No sealed file, historical inventory, or receipt is mutated.

| Check | Defect exercised | Observed failure | Recovery |
|---|---|---|---|
| Source-head scan | Put `theorem`, `lemma`, and `structure` prose inside nested comments, while retaining a real theorem and an unnamed instance | The raw historical regex counts comment prose; the comment-aware scan excludes it and retains the actual heads | Four regression tests pass, including actual false-match source lines |
| Compiled binding | Supply a same-name record at the wrong source line, two matching records, a wrong compiled kind, or an unnamed-instance match without instance status | `bind_candidate` raises a named `ValueError` for each defective input | Unique same-line, same-module candidates bind; the actual reconciliation resolves all 2,564 source heads |
| Unit 37 book Lean | Append the false claim `EmptyRel false true ↔ D2 false true` only to a temporary driver string | Lean's `decide` reports that exact proposition is false; shared runner exits 1 | Original script checks 18 exact reports: fourteen book theorems and four imported theorems |

The false claim tests an actual distinction between two relations allowed
by the same no-self-loop rule. The two new pairwise-inequality proofs have
empty axiom sets. Full compiled-census output and build logs are local
receipts under `artifacts2/declaration_review/`; no regeneration ran with
a live defective driver.

## Boundary and swap teaching route (2026-10-28)

All mutations use copied Wiki/teaching assets, fixture inputs, or a
temporary Lean driver. The three research owners' source files, ledgers,
frozen predictions, and receipts remain read-only. No regeneration occurs
with a live defect.

| Check | Defect exercised | Observed failure | Recovery |
|---|---|---|---|
| Actual Wiki verifier: boundary record | Make keeping two identical labels satisfy the retained-pair requirement | Exit 1 names `stale boundary-lab record` | Restore bytes; exit 0 |
| Actual Wiki verifier: boundary desk | Replace the bundle by missing-content text | Exit 1 names `stale boundary-lab desk or links` | Restore bytes; exit 0 |
| Actual Wiki verifier: boundary figure | Replace the fixed-menu SVG by missing-content text | Exit 1 names `stale boundary-lab figure` | Restore bytes; exit 0 |
| Source-backed packet | Make empty reports reject swap, erase an asymmetric witness, invent U names, change the fixed labels, remove an actual swap, admit a bundle to the minimum, or invent a secondary minimum | The actual recomputation rejects each copied packet as differing from source-backed cases | Original packet passes; eleven authoring tests pass |
| Teaching population and figure | Change 16 report subsets to 17, or replace a displayed cost 1 by 99 | Named population-table or figure mismatch | Original population table and four SVGs pass |
| Book Lean | Append `swapInAut [] = false` and the claim that the exchange changes the retained identical-label key | `decide` names both exact propositions as false; shared runner exits 1 | Original 125 exact reports pass separately |

The actual JavaScript lookup passes all 120 desk settings and rejects
unknown cases. Static figure geometry and PNG previews are checked
separately. Browser rendering, responsive layout, and keyboard interaction
remain unverified after the local preview/error-page policy rejection;
pure lookup tests are not a substitute for those interaction checks.

## Same-record teaching route (2026-10-28)

All mutations use copied teaching/Wiki assets. The sealed and research
sources, frozen predictions, and campaign receipts remain read-only.
No regeneration occurs with a live defect.

| Check | Defect exercised | Observed failure | Recovery |
|---|---|---|---|
| Source-backed matching packet | Invent a zero-cost reply, erase a third-party change, change the double-hole answer, invent an extra collapsed pair, ignore a kept promise, mark the three-item reply within bound, apply separation pruning, or change a continuation/practice price | `check_recorded` raises the named source-backed mismatch | Original packet passes; twelve authoring tests pass |
| Teaching population and figure | Change 24 root probes to 25, or replace a generated SVG with an empty payload | Named population-table or figure mismatch | Original count and four figures pass |
| Actual Wiki verifier: lesson | Change the selected continuation's total from three to one | Exit 1 names `stale same-record page` and its slug | Restore bytes; exit 0 |
| Actual Wiki verifier: record | Mark the explicit three-item reply as within the two-item bound | Exit 1 names `stale same-record record` | Restore bytes; exit 0 |
| Actual Wiki verifier: figure | Replace the three-addition figure with an empty SVG | Exit 1 names `stale same-record figure` | Restore bytes; exit 0 |

Five Wiki helper tests also detect malformed JSON, false figures and
lesson prices, and a missing page, while checking prerequisite/answer
destinations. This route adds deterministic bounded computations, not
book-Lean proofs or a new native theorem. Static figure inspection does
not establish hosted rendering or reader learning.

## Numerical teaching and readout route (2026-10-29)

All mutations use copied teaching/Wiki assets or a temporary book driver.
Sealed and research sources, predictions, contracts, and receipts remain
read-only. No regeneration occurs under an injected defect.

| Check | Defect exercised | Observed failure | Recovery |
|---|---|---|---|
| Source-backed number packet | Alter a total, define a zero-total share, reverse the zero-only-box result, erase a sign effect, change the middle reading, invent information, ignore a carrier restriction, split reversal groups, or make doubled coordinates scale linearly | Named mismatch against recomputed source-backed cases | Original packet passes; twelve authoring tests pass |
| Population and figure | Change 2,401 coordinate input pairs to 2,402, or replace a generated SVG | Named population-table or figure mismatch | Original count and five figures pass |
| Actual Wiki verifier: lesson | Replace the middle weight/readout 2 by 9 | Exit 1 names `stale number-lab page` and its slug | Restore bytes; exit 0 |
| Actual Wiki verifier: record | Make the zero-only box reject instead of pass | Exit 1 names `stale number-lab record` | Restore bytes; exit 0 |
| Actual Wiki verifier: figure | Replace the coordinate figure by an empty SVG | Exit 1 names `stale number-lab figure` | Restore bytes; exit 0 |
| Book Lean | Append the false combined reading 2 at two rightward unit inputs and `2 * 5 = 3 * 5` | Lean's `decide` names both exact propositions as false; shared runner exits 1 | Original 37 exact reports pass separately |

The zero-box example also corrects Unit 64's former inference from a
finite loop to an all-integer theorem. Five new Wiki tests exercise
page/asset failure detection and route links. These checks do not prove
the physical interpretation or reader transfer.

## Early formal-chapter scope review (2026-10-29)

These injections use only temporary book drivers. Sealed sources,
predictions, axiom reports, research inputs, and receipts remain read-only.
No regeneration occurs under a live defect.

| Check | Defect exercised | Observed failure | Recovery |
|---|---|---|---|
| Kernel: cross-reading indices | Assert that `(0,1)` is refused on the three-token state | `decide` names the exact `stepT ... = none` proposition as false; shared runner exits 1 | The accepted-wrong-pair theorem passes in u05 |
| Kernel: starting state | Assert a two-token base has length at most one | `decide` names the exact length bound as false; shared runner exits 1 | u11 proves the base fails the initial invariant while an empty history keeps its two tokens |
| Kernel: fresh class | Assert the newcomer in the two-marked-data example has a derivable unary mark | `decide` names that exact plugged derivability proposition as false; shared runner exits 1 | u12 proves old collapse and the newcomer's separation |
| Kernel: mention scope | Assert equal unary answers after marking target 1 while avoiding only target 0 | `decide` names the exact derivability biconditional as false; shared runner exits 1 | u12 checks one-target failure and two-target preservation |
| Exact axiom report | Add a well-typed `Classical.em` theorem while expecting the existing `{propext, Quot.sound}` boundary | Lean accepts the proof, but the shared runner reports 0 of 1 expected dependencies and exits 1 on `outsideBoundary` | Final nine added book proofs remain at seven `{propext, Quot.sound}` and two `propext` reports |

The actual dependency gate also caught a draft helper's simplifier use of
`Nat.add_eq_right._simp_1`, which carries `Classical.choice`. Direct
constructor reasoning removes that dependency. The boundary is preserved,
not repinned to the draft. The four affected book scripts check 58 exact
reports; no general positive witness-extraction theorem is claimed from
their negated equivalence.

## Requests and cost chapter review (2026-10-29)

Four separate temporary book drivers test exact false propositions.
Sealed sources and native receipts remain unchanged. No artifact or pin is
regenerated under an injection.

| Check | Defect exercised | Observed failure | Recovery |
|---|---|---|---|
| Repeated request | Assert `stepE R2L (.impose 0 1) ≠ some R2L` | Lean's `decide` names this exact proposition as false; shared runner exits 1 | u17 proves repeated admissible requests leave the record unchanged |
| Unknown form | Assert `[0,1].length = [].getD 0 0` | Lean names the arity equality as false; shared runner exits 1 | u18 proves no-form non-separation and checks the malformed raw record |
| Uniform rule | Assert the link's `(0,[1,1])` remains non-derivable after adding rule 0 | Lean names the negative derivability claim as false; shared runner exits 1 | u19/u20 prove collapse with the uniform rule while retaining their instances |
| Cost comparison | Assert `aritySum deltaBL < aritySum deltaU0` | Lean names the reversed inequality as false; shared runner exits 1 | u22 checks the correct arity inequality and the separate instance-count tie |

The five affected scripts pass 67 exact reports after the injections;
eight new book reports use four `propext` and four
`propext, Quot.sound` dependency sets. These kernel checks do not establish
reader understanding or the correctness of a physical interpretation.

## Relation, property, and extension review (2026-10-29)

Four temporary book drivers exercise exact false claims. Native sources,
axiom artifacts, research receipts, and pin populations remain unchanged;
no regeneration occurs under an injection.

| Check | Defect exercised | Observed failure | Recovery |
|---|---|---|---|
| Same point | Assert `(() : Unit) ≠ ()` | Lean's `decide` names the exact inequality as false; runner exits 1 | u23 retains the one-point witness and equality countermodel |
| Particular versus global | Deny `mixed true true` while retaining its definition | After unfolding, Lean names the negated Boolean proposition as false; runner exits 1 | u24 proves an unequal asserted pair coexists with a self-pair |
| Pushed shortcut | Assert `Push disjointArrows joinMiddle 0 3` using source edge `(0,1)` | Lean rejects the endpoint equation `joinMiddle 1 = 3` as false; runner exits 1 | u25 proves target transitivity fails, no collision occurs, and the narrower obstruction is absent |
| Positive extension | Deny the self-pair added by `withSelf D2 false` | Lean names the unfolded negation as false; runner exits 1 | u26 proves self-pair extension, finite negative checks, and the empty-carrier exception |

The four original drivers recover 50 reports: the eight added ones have
four empty dependency sets and four `propext` sets. These checks do not
establish an operational enforcement policy or a general physical law.

## Grouping, bounds, renaming, and pruning review (2026-10-29)

Temporary book drivers test four exact false propositions. A separate
process changes only a book check's imported generator binding; the sealed
generator file, artifacts, and pin populations are untouched.

| Check | Defect exercised | Observed failure | Recovery |
|---|---|---|---|
| Raw quotient | Assert `rawLink 0 2`, rather than equality generated by the 0–1–2 chain | After unfolding, Lean names the exact relation proposition as false; book runner exits 1 | u27 proves equal quotient values without the direct raw relation |
| States versus rounds | Assert `(allPairs 3).length + 1 ≤ 3` | Lean names the false four-states-at-most-three bound; runner exits 1 | u28 distinguishes four states from three accepted rounds and proves the general conversion |
| Range condition | Assert well-formedness of the context whose filled slot moves from 1 to 2 with only two data | Lean names the exact `wfCtx` proposition as false; runner exits 1 | u29 proves the reversible map and the failed context-range check |
| Uniform rule | Deny derivability of the fresh-slot plugging despite the old rule | Lean names the exact negative derivability claim as false; runner exits 1 | u30 checks both positive answers and old-form hypothesis activation |
| Generation versus validity | Suppress only the newcomer-only mark from a temporary binding of `iter_cost2_deltas` | The actual u30 book checker exits 1 naming `generation versus validity` | Original generator binding is checked in a fresh process and in the full textbook job |

The four original book drivers recover 49 exact reports. The eleven added
reports use two empty dependency sets, three `propext` sets, and six
`propext, Quot.sound` sets; one is a setoid definition with its proof.
No native receipt is regenerated while an injected claim or binding is live.

## Transitions, rounds, and response existence review (2026-10-29)

Four temporary book drivers exercise exact false propositions. Two other
process-local substitutions change only book-check bindings; imported
native owners, sealed files, artifacts, and pin populations are untouched.

| Check | Defect exercised | Observed failure | Recovery |
|---|---|---|---|
| Demand ordering | Assert exact response transport on the raw list `[(1,0)]` under identity renaming | Lean names the response equality as false; runner exits 1 | u31 proves the inequality: sorting before versus after insertion leaves one versus two copies |
| Replay versus validity | Assert the unanswered closed run's demand list is empty | Lean names the concrete list equality as false; runner exits 1 | u34 proves the closed run exists and its empty response is invalid |
| Freshness | Assert a repeated response's retained demand count equals itself plus one | Lean names the exact length equation as false; runner exits 1 | u34 proves repeated imposition on `U0` returns `U0` |
| Stale rule | Deny derivability of `(0,[0])` after the raw stale rule becomes active | Lean names the negative derivability proposition as false; runner exits 1 | u35 proves the malformed record defeats the fresh-mark recipe |
| Recorded challenge | Temporarily omit all `Impose` events from u32's book `replay` binding | The actual checker exits 1 naming the missing L and F demand stores | Original binding retains both targets and checks isomorphism with the demands present |
| Newcomer collapse | Temporarily hide pair `(1,3)` from u33's book observation binding | The actual checker exits 1 naming `fresh datum collapse` | Original binding records that newcomer 3 remains collapsed with datum 1 |

The five original book drivers recover 70 exact reports. Seven are new:
three `propext` and four `propext, Quot.sound` sets. The longer repair and
unadmitted-target examples are checked without changing the native theorem
statements. None of this establishes beginner mastery or a physical law.

