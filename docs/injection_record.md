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
| Root suite, external contact-file candidates, shallow checkout (2026-09-23) | in `tests/test_primitive_contact.py`, put back the unguarded third-ancestor index (`base.parents[2]` for `*base.parents[2:3]`); an earlier probe did the same to the first form of the guard | `test_external_candidates_tolerate_a_shallow_checkout` failed with `IndexError: 2`, exit 1; exit 0 with the original bytes restored |
| Same, main-checkout base | dropped the main checkout from the candidate bases | `test_a_linked_worktree_searches_where_the_main_checkout_does` failed, naming the missing main-checkout candidate `C:/u/src/repos/repo/external/file.lean`, exit 1; exit 0 when restored |
| Same, common-directory check | returned the git common directory's parent without checking that it is named `.git` | `test_main_checkout_is_read_from_the_git_common_directory` failed with `assert WindowsPath('C:/srv') is None`, exit 1; exit 0 when restored |

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
