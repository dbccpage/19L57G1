# sign_slice: a finite slice of the section classifier

A caller-supplied classification challenge was translated at the
operator boundary into this tree's native question (see `PROMPT.md`);
the supplied vocabulary appears in no committed file, and
`test_forbidden.py` fails the run if it ever does.  The complete
classification is REFUSED as a terminal: this tree delivers a declared
finite census plus an obstruction register (FW-SET held).

Frozen inputs: native `PROMPT.md` sha256
`ad499c48ebdda0ce64050c6743409d242c7aeec1c54b7b854beabac4da6d9266`;
predictions frozen at
`b4c19752d73d93685c8debaef2846462b823d9dbdc66d261e2ebc8fc03197e7d`
(phases 1-2, before any phase computation) and
`768b36ab7c586691e996629bfac288a43384b8e8fac691ee1d88a643d8604846`
(phases 3-5, before the census, the exhaustion, and the register ran).
Sources read are pinned in `SOURCE_MANIFEST.json` at snapshot
`3bfc9422580a381b53ec635fb8d051c74b0e76fe`; `verify_pins.py` checks
them at the snapshot and at HEAD.

## Terminals, each with its scope

- GENPRES_GRAMMAR_DECLARED (DEFINITION / DECLARED_POLICY): the grammar
  is the priced tuple in `genpres.py` -- objects, arrows with fibre
  transports, the kernel observer, a weighting, generators, the
  declared breadth-first forest rule, and the occurrence-slot list.
  Measure `muG = (objects, arrows, distinct amps)`, lexicographic.
  The iso key forgets presentation tokens only.  G0 admitted and
  trivially sectioned; G1 REFUSED (weighting absent -- FW-BILL); G2,
  G3 admitted with measures; G4 reconstructions admitted; G5 admitted
  as a pair.  The occupancy-2 six-site family is REFUSED by the object
  bound, by name.
- CONESECTION_DECIDES (DECLARED_POLICY implementing a
  CONDITIONAL_THEOREM): the predicate is the packet's proved
  generator/holonomy criterion, reconstructed; the phase form is the
  same predicate and was not forked.  PB1-PB5 all disposed TRUE
  (receipt `phase_2_predicate`), including the reconstructed
  sum-blindness countermodel: a declared signed walk list makes
  twisted equal total at an obstructed member.
- SLICESET_CENSUSED (FINITE_COMPUTATION): 12 members under the
  declared bounds (objects <= 6, site hops <= 8, occupancies 2 and 3,
  unit and signed weightings): 3 sectioned, 9 obstructed.  PC1-PC4
  disposed: recorded verdicts reproduced fixture by fixture; the sign
  pair agrees on the predicate and is separated by the declared mixing
  read-out (64 against 0); the count is pinned at 12; the complement
  is nonempty.
- OCCRELABEL_MOVES_CLASS, within the bound that every slot map is the
  identity or the two-label exchange (FINITE_COMPUTATION): exhausting
  all 65536 slot-map assignments on the obstructed two-label square,
  8192 move it into the sectioned class, every one of the 64
  pointwise-shaped assignments leaves it unmoved (the packet's proved
  invariance, reconstructed -- FW-T1 respected: that proof was not
  cited as this answer), and the cheapest moving assignment differs
  from every pointwise assignment in exactly 2 slots.  A finer
  convention group repairs an obstruction the pointwise group cannot
  describe away, at price 2 within this bound.  This is a bounded
  statement about one member; it is not a grammar-wide theorem.
- REGISTER_WRITTEN (FINITE_COMPUTATION): 9 rows, one per obstructed
  member: witness walk (every row found one within length 6), mover
  count, twisted against total at the named pair, repair-mass
  applicability (NOT_APPLICABLE on every row -- the pricing layer is
  proved on the packet's chord-square family, which no member is),
  the occurrence-relabel outcome, and a priced leftover, executed
  nowhere.  PE1-PE4 disposed TRUE.
- TIES_RETAINED: distinct iso keys stay distinct rows; nothing was
  collapsed by judgement.
- PREDICTIONS_HASHED: the two freeze hashes above.
- MANUAL_RECEIPT_DECLARED: this tree's receipts and scans are a manual
  receipt.  No CI gate reads them.
- OB1_UNCHANGED, S66_UNCHANGED, S9_LAST_UNCHANGED: the three protected
  opens are untouched; `test_forbidden.py` fails the run on any claim
  to the contrary.
- CANDIDATE_SPACE_OPEN: grammar classes outside the declared list, and
  census members outside the declared bounds, stay OPEN.
- FW_SET_HELD: no sentence in this tree claims the completed
  classification.

## Evidence classes and the Lean scoping statement

No theorem-level sentence ORIGINATES in this tree.  Every
theorem-level sentence used here is a citation into the pinned
sibling packet (CONDITIONAL_THEOREM), whose Lean carries it; every
claim made here is DEFINITION, DECLARED_POLICY, FINITE_COMPUTATION,
COUNTERMODEL (computational, at declared bounds), or OPEN.  For that
reason this tree carries no Lean package: there is no new
theorem-level claim for one to carry.  If a future rung promotes the
bounded occurrence-relabel finding to a general statement, that
promotion requires Lean and is OPEN until it has it.

## Adversarial dispositions

All ten are recorded in the receipt under `adversarial`, each with its
refutation, countermodel, citation, or held-open status.

## The registration diff this tree does NOT apply

Adding this tree to the research job would be the following step in
`.github/workflows/verify.yml`, recorded here as text and not applied
(registration is an author act):

    - name: sign_slice pins and tests
      run: |
        python research/sign_slice/verify_pins.py
        python -m unittest discover -s research/sign_slice -p "test_*.py"

## Commands (run from the repository root)

| command | exit | key line |
|---|---|---|
| `python research/sign_slice/verify_pins.py` | 0 | `pins clean: 11 sources at snapshot and HEAD; native PROMPT.md frozen` |
| `cd research/sign_slice && PYTHONDONTWRITEBYTECODE=1 python run_sign_slice.py --out receipts` | 0 | `census: 12 members, 3 sectioned, 9 obstructed`; `occ relabel: OCCRELABEL_MOVES_CLASS, flips 8192, price 2`; `register rows: 9` |
| `cd research/sign_slice && PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s . -p "test_*.py"` | 0 | all tests pass, refusal scans included |
| `cd research/sign_slice && python -m mypy --strict .` | 0 | strict, all source files |
