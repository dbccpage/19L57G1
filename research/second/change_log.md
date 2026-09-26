# UNFROZEN DRAFT -- change log of the second derivation

**UNFROZEN DRAFT, dated 2026-09-25 and updated the same day.  The
research stage is still running.**  Continuation attempt one (Challenge 3)
has closed and the author merged it (pull request 267, merge `dabe9a92`).
Continuation attempt two (Challenge 4) is startable and had not been
launched when this draft was updated.  This log is finalized only after
attempt two closes and the author approves the freeze; entries after this
one are expected.

`AuthorityEffect: None`.  The dated history of the run: rungs, author
rulings, operator acts, supersessions and known defects.  Newest last.
Every entry names the commit or pull request that carries it.  A
withdrawn sentence is quoted where the rung that withdrew it quoted it;
this log withdraws nothing of its own and revises no rung's receipt.
Times are the committer's local times as Git records them.

## Sources for this log

The rung trees' `STATUS.md` and `CLAIM_LEDGER.md` files, the injection
record and handoffs in `research/second/MANUAL.md`, `CLAUDE.md` (gate 11),
`docs/GENESIS_CLOSEOUT.md` sections 0, 1 and 4, the Git history of
`main` up to `dabe9a92`, and the closeout coordinator's attestation of
2026-09-25.  The operator acts in the section "Operator acts attested by
the closeout coordinator" below were not previously committed anywhere;
this log is their first committed record, and they rest on that
attestation.

## 2026-09-03: seed, plan, rung zero

- `83fdabef`: the seed `research/second/SEED.md` is committed, sha256
  `52439e5f75d1c599ce52dc716beb88f1dd7bfc83856ee73ce85f3a7eeec5e70e`.  It
  has not changed since; every rung manifest pins it.
- `7dabce4e`: `PLAN.md` and `MANUAL.md` are committed before substantive
  work.  Recorded in the manual: the seed's author and the run's first
  session are the same session (declared reading one), so rung zero is not
  blind to its author's expectation; it is replay and census, which no
  prediction can steer.
- `f2d40f59` (20:16): rung zero, `research/second_inheritance/`,
  Challenge 0, at snapshot `7dabce4e`.  Two trees the seed names,
  `standing_commitment` and `two_sided_commitment` (pull requests 127 and
  128), are absent at that snapshot; their replay is recorded OPEN.  Three
  of three frozen predictions hit.
- Pull requests 127 and 128 merge (`e40109f3`, `dd2aba24`).
- `dbaa4b73` (22:53): rung zero repaired to replay both landed trees at
  exact base `dd2aba24`.  The historical absence stands; the landed replay
  is a repair result and is not scored as a fourth prediction.
- Injection: the rung-zero frozen-text pin, committed throwaway probe
  `08cb4808`.  It is the only injection recorded for rung zero.
- Pull request 130 merges (`3f445712`, 23:16).

## 2026-09-04: rung one and the two tracks of rung two

- `cdefee90` (00:35): rung one freezes its question and predictions.  The
  prediction file discloses that the sealed kernel and sibling trees were
  read before it was written, and labels each prediction FORCED or NOT
  FORCED accordingly.  Rungs one and two were launched with an operator
  packet held outside this repository; the rung files name it (the
  "standing orders" and the `[OUTSIDE BET]` slot, which read `none`).
- Rung one, `research/second_stream/`, pull request 133 (merged
  `9b9bea87`, 11:24).  The unrestricted question stays OPEN; ten
  predictions hit, R1-9 missed, R1-X pending.
- **Author act: the next-rung tie.**  The seed's rule tied Challenge 2
  with the no-first-demand question.  The author resolved the tie by
  running both in parallel as two separately scoped tracks with disjoint
  write roots (recorded in `research/second_stake/STATUS.md` and
  `research/second_nofirst/STATUS.md`).  Track two froze at `d4d5830e`
  (10:15); track one at `3be6a2a9` (10:49).
- Rung two track one, `research/second_nofirst/`, pull request 136
  (merged `b22b292c`, 17:40).  Eighteen of nineteen scored predictions
  hit; N-16 missed (three demand-inert kinds, not two); four FW-DEF census
  misses; N-X pending.
- Rung two track two, `research/second_stake/`, pull request 135 (merged
  `7d2e6e86`, 18:13).  Six hits, nine misses, one unscored declared
  policy, one pending.
- **Known defect, found live on `main` at `7d2e6e86`.**  Rung one's scope
  check read every commit against its first parent, so three integration
  merges were attributed to rung one and `main` went red naming files rung
  one never touched.  Repaired by pull request 137 (`f7d10e70`): a commit
  is attributed by what it contributed.  The sentence rung one withdrew is
  quoted in its `STATUS.md`.
- **Known defect.**  Track one's write-root vacuity guard asserted through
  an empty diff on `main`; repaired by pull request 138 (`43f26aff`).
  Track two's boundary scan measured against a fixed base and failed on
  pull request 138's branch; repaired by pull request 139 (`db1412e2`).
  Pull request 140 (`b3f325be`) added coverage for two receipt-bearing
  guards of track two.
- Withdrawals made inside the rungs on this date, each quoted where it was
  withdrawn and left standing there: rung one's narrow-constant comparison
  claims (its ST-13), its four-generation determinism claim and its claim
  that the runner refused an unstaged frozen-text edit; track one's
  "six of them" span count, its "well-formed regime" wording of the
  at-most-one terminal, "three of its five conjuncts", the sentence giving
  the first demand of any run one source, "Every row carries exactly one
  evidence class", "sixty-four" and the "109 tests"/"115 tests" census;
  track two's manual row saying the P-G scorer followed growth origins.

## 2026-09-08 to 2026-09-20: maintenance of the early rungs

- 2026-09-08, pull request 146 (`24fcc7c5`): track one's boundary checks
  scoped to its own commits.
- 2026-09-10, pull request 159 (`92495610`): rung one pins
  `ci/prose_watchlist.json` at HEAD only, not at the snapshot.
- 2026-09-10, pull request 164 (`c7d43ae2`): `paper/paper.md` moved on
  `main`, so track one's pinned span of the sealed paper was repinned to
  lines 531-537 at snapshot `23362172`; frozen texts were not repinned.
- 2026-09-14, pull request 188 (`94ce8aca`): the custody ratchet adds
  `research/second/SOURCE_MANIFEST.json` and `verify_sources.py`.
- 2026-09-18, pull request 200 (`c22aa358`): rung one pins
  `ci/check_prose_watchlist.py` at HEAD only; the injection is in the
  manual.  Pull request 203 (`827bf983`): track two's sealed-path check
  scoped to its own commits; four injections recorded.
- 2026-09-20, pull request 223 (`95680125`): track one's registration
  bound to minimum test counts and mandatory comparisons.

## 2026-09-23: rung three, and the rung contract

- Pull request 231 (`3809f783`): the author-authorized correction of the
  sealed paper's section three moved `paper/paper.md`; track one repinned
  at snapshot `16fcffd6`, its pinned span unchanged.
- Pull request 233 (`89fc568a`): `ci/check_new_research_trees.py` holds
  second-derivation rungs to their seed's contract.  **Author ruling,
  pull request 234 (`8bd40790`):** a rung's registration also covers the
  generated views of a new tree, regenerated by the named commands.
- `7a5d0952` (16:18), `99bd6cf9` (16:23): rung three freezes its question
  and predictions.  Rung three, `research/second_index/`, pull request 239
  (merged `013be46f`, 18:31), at snapshot `110feded`.
- **Protocol deviation, recorded by rung three.**  `PLAN.md` item four
  assigns the engine of Challenge 3 to this ordinal; the seed's next-rung
  rule, which the plan's item six defers to, selects L-2 instead.  Rung
  three follows the rule and names the engine as leftover X-5.  Every
  later rung does the same, and `PLAN.md` is not edited.
- **Known defect, found on `main` after the merge.**  Rung three's scope
  scan attributed every branch to itself, and its tree had no
  `.gitattributes`, so its axiom log arrived with CRLF on a Windows
  checkout.  Repaired by pull request 243 (`b55fc96a`), with no receipt,
  frozen text, pin, prediction or status text changed.
- Pull request 242 (`03409c1c`): the seed contract check accepts either
  letter case of the seed digest; `db434a28` names rung three's gate
  scripts in the gates skill.

## 2026-09-24: custody drift and rung four's start

- Pull request 241 (`a444f199`): track one's and rung three's pins
  certify their snapshot, and movement at HEAD is reported as drift rather
  than failing, under the author's ruling of 2026-09-22 recorded in
  `CLAUDE.md`.
- `61215adc` (23:01), `7db41384` (23:04): rung four freezes its question
  and predictions, at snapshot `bdbe5832`.

## 2026-09-25: rungs four to ten, three author rulings, the continuation

- Rung four, `research/second_iso/`, pull request 255 (merged `34855eac`,
  00:19).  J-12 missed (largest automorphism group 240, predicted 24).
  **Known defect:** rung four's registration left
  `tests/test_gates_skill_matches_workflow.py` red until its companion
  edit landed; the companion (`fix/gates-skill-rung-four`) was merged into
  rung four's landing branch.  **Found live:** nineteen theorems reached
  `Classical.choice` through two `simp` calls; repaired before any
  injection.
- **Operator acts at rung four** (attested; see the section below): the
  rung was launched headless from `bdbe5832` after a memory canary; it
  listed running processes and saw another repository's name and paths,
  with no content; at landing the operator merged `main` in, regenerated
  `docs/index/pins.md` and folded in the skill lines of pull request 256.
- **Author ruling, pull request 257 (`630622da`, 00:23):** a rung adds its
  own registered gate scripts to `.claude/skills/gates/SKILL.md`.
- Rung five, `research/second_symmetry/`, pull request 258 (`144d9c2b`,
  02:04).  K-14 missed (largest fall 24, predicted 20).
- Rung six, `research/second_succession/`, pull request 259 (`d6dca750`,
  02:45).  Six of six hits; FW-DEF seventeen of seventeen.
- Rung seven, `research/second_duration/`, pull request 260 (`535fb553`,
  03:23).  Seven of seven hits; three FW-DEF misses.  Rung seven applied
  rung six's reading (a leftover refining a decided row is not eligible)
  to every carried row and marked Y-1 ineligible, which removed a tie
  that would have turned on the meaning of "named first".
- **Operator act** (attested): the rung sequence was paused after rung
  seven, pending the author's "named first" ruling, and resumed after it.
- **Author ruling, pull request 261 (`35e680ec`, 10:34):** "named first"
  in the next-rung rule means first in the list of leftovers as the
  applying rung writes it, never earliest in time.
- Rung eight, `research/second_class/`, pull request 262 (`ff584d44`,
  11:54).  P-13 missed (the Lean countermodel's two sides lie in two
  classes in the Python grammar).  **Found live:** three library lemmas
  reached `Classical.choice`; replaced.
- **Supersessions, dated 2026-09-25 and left standing** (rung eight's
  `STATUS.md`): rung five's SYM-14, rung six's class-level OPEN (SUC-17),
  and the sum part of rung seven's class-level OPEN are closed for clean
  regimes and bases by `size_iso` and `counts_of_class`.  Each earlier
  sentence stands as written at its rung.
- Pull request 263 (`5c7d3060`): repository hygiene; no second-derivation
  file changed.
- Rung nine, `research/second_profile/`, pull request 264 (`77ad2a78`,
  13:19).  Seven of seven hits; four FW-DEF misses.  Rung nine applied its
  own reading of a leftover carrying several rows (decide the first two,
  name the rest) and recorded the budget ambiguity: by ordinal two rungs
  remained, by tree one.  **Found live:** `omega` closing a conjunction or
  a non-arithmetic goal reached `Classical.choice`; rewritten.
- `fbc804ab` (13:28), `16aeba85` (13:32): rung ten freezes its question
  and predictions.
- **Author and operator act** (attested): the author paused all work at
  13:38, while rung ten had frozen its question and predictions; rung ten
  was resumed at 18:32 with a bare "continue" into the same session.  The
  commit history is consistent with it: the predictions froze at 13:32 and
  the next rung-ten commit, `081085d3`, is at 18:55.
- Rung ten, `research/second_response/`, pull request 265 (`4c785017`,
  19:21).  R-11 missed (no refusal within two items).  X-6 closed; the
  next-rung rule, as rungs three to nine read it, selects no leftover.
  Twelve research attempts exist, eleven ordinal labels zero to ten.
- **Author ruling, pull request 266 (`01876f3a`, 19:57):** the
  continuation ruling, recorded verbatim in `CLAUDE.md` (gate 11) and in
  `research/second/MANUAL.md`.  In short: resolving an unresolved FORCED
  classification, positively or negatively, extends the census, and a
  named prerequisite (X-5) is eligible; the twelve-rung limit counts
  distinct research attempts, so the twelve recorded attempts exhaust the
  original budget; at most two further attempts are authorized, Challenge
  3 and then Challenge 4 with its engine-dependent census evaluations, the
  first closing before the second opens, with no outcome prescribed;
  `SEED.md` stays byte-identical; a closeout session writes this file,
  the paper and the claim ledger; budget exhaustion is not completion.
  `3a95a976` pins the watched word the ruling's verbatim copies carry;
  `3a60ed2b` repins rung one's HEAD-only pin of the watchlist census.
- Continuation attempt one (Challenge 3) is launched headless by the
  coordinator from `01876f3a` on branch
  `research/second-engine-continuation` (attested).  It freezes its
  question at `03b67607` (20:08) and its predictions at `596e2c6e` (20:14).
- `2e8ba8cf`: the author's Genesis closeout scope is recorded in
  `CLAUDE.md`; `ccd0ab06`: the closeout acceptance scope is frozen in
  `docs/GENESIS_CLOSEOUT.md`.
- This draft: `research/second/paper.md`, `research/second/change_log.md`
  and `research/second/claim_ledger.md` are created on branch
  `closeout/second-report` from `ccd0ab06`.  Reporting consumes no
  research attempt.  Before the files were written, every registered
  step of the run was re-run at `ccd0ab06` on a clean worktree: 48 of 48
  passed (`research/second/paper.md`, section 9.2).  Committed as
  `4c528d3e` (20:59), while attempt one was still open.
- Continuation attempt one, `research/second_engine/`: the result at
  `cfeb1b81` (20:47); the generated views at `d746c185` (20:49); the
  custody pin, handoff and fifteen injections at `c8655ef7` (20:56).
- **Self-correction before the merge, `7f069c7f` (21:05).**  The attempt's
  `STATUS.md` had described the composite of two isomorphisms as something
  "which no earlier tree had".  The attempt replaced that clause with a
  credit to the sealed estate's `Iso.trans` in
  `lean4/Derivation/IsoCanon.lean`, pinned that module as a source,
  credited it in the module comment, census note and ledger, and corrected
  two counts: the plan item that assigns the engine (four, not three) and
  the FORCED rows among the thirteen computed ones (three, not four).  The
  replaced clause is quoted here because the attempt's `STATUS.md` does not
  quote it.  `e23a3fa6` (21:07) records the gate time.
- **Operator landing repair, `9fc917ad` (21:13).**  The correction commit
  pinned `IsoCanon.lean` without regenerating `docs/index/pins.md`, so the
  root test that the lookup indexes are current failed; the operator
  regenerated that generated view only.  No research content changed.
- **Pull request 267 merged by the author, `dabe9a92` (21:13).**
  Continuation attempt one is closed: a 144-member engine class (108
  without its HALT member) declared, counted and probed to depth two;
  minimal members exist, none unique up to probe-isomorphism, none initial
  under inclusions of declarations; E1, E3, E4 and E8 carried in its Lean
  mirror, E6 OPEN; no census row decided; the input count stays two.
  Thirteen of thirteen computed predictions hit, which the attempt calls
  weak evidence; forty-eight of fifty Lean class predictions hit.
- `b205bb4e`: the coordinator merges `main` at `dabe9a92` into
  `closeout/second-report`.  This draft is then updated for attempt one
  and for the attested operator acts.  Continuation attempt two is
  startable and had not been launched.

## Operator acts attested by the closeout coordinator (2026-09-25)

Attested to this closeout by the closeout coordinator, the session that
ran them, on 2026-09-25, and not previously committed:

- Rungs four to ten and continuation attempt one were launched headless
  by the coordinator, with Claude Code 2.1.281, auto-memory off, project
  settings only, no MCP servers, no slash commands and a fixed tool list.
  The prompt in every case was exactly `Follow research/second/SEED.md.`.
  Each launched from `main` at: rung four `bdbe5832`, rung five
  `630622da`, rung six `144d9c2b`, rung seven `d6dca750`, rung eight
  `35e680ec`, rung nine `ff584d44`, rung ten `77ad2a78`, continuation
  attempt one `01876f3a`.  Each launch commit is the snapshot commit that
  tree's `SOURCE_MANIFEST.json` records, which this draft checked.
- Before rung four, a memory canary run with the same flags answered
  "MEMORY: NONE", with no skills and no MCP servers.
- Rung four listed running processes while checking machine load, and saw
  another repository's name and paths in command lines.  It saw no
  content, and nothing of it reached the rung's output or diff.
- The author paused all work at 13:38 on 2026-09-25, while rung ten had
  frozen its question and predictions.  Rung ten was resumed at 18:32
  with a bare "continue" into the same session.
- The rung sequence was paused after rung seven, pending the author's
  "named first" ruling (pull request 261), then resumed.
- Operator landing repairs, all generated views, skill lines or merges of
  `main`, never research content: at rung four, `main` merged in,
  `docs/index/pins.md` regenerated and the skill lines of pull request 256
  folded in; at continuation attempt one, `docs/index/pins.md` regenerated
  (`9fc917ad`).
- Rungs zero to three were not launched by this coordinator.  Rungs one
  and two were launched with an operator packet held outside the
  repository, as their own files disclose (2026-09-04 above).

## Known defects and open process gaps, standing at this draft

- Rung zero carries no coverage gate; its line and branch coverage were
  never measured by any registered step (rung one records this).
- Several registered gates carry no recorded injection: rung zero's tests
  and typing, and strict typing in rungs one, two track one, three to ten
  and continuation attempt one.  Only rung two track two injected its
  strict-typing gate.
- The operator acts above had no committed record before this draft; they
  rest on the coordinator's attestation, and the prompts and launch
  settings themselves are not committed anywhere.
- Continuation attempt one's Lean orbit (an inhabitant of the sealed
  isomorphism structure) and the Python orbit its rules read (the sealed
  serialization's automorphisms) are not checked against each other
  (its G-9).
- The continuation ruling's verbatim copies carry a watched word, pinned
  by `3a95a976`; this draft paraphrases the ruling rather than quoting it.
- The Lean reading regimes and the Python genesis readings differ by the
  requirement imposed at the sealed Challenge 3; two frozen predictions
  missed on it (J-12 at rung four, P-13 at rung eight), and no bridge
  between the two carriers is claimed.
