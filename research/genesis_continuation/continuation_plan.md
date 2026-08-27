# Continuation plan

A packet asking one question of the existing record: does the repository's
own derivation already contain a reusable finite process, and if so, where
does that process stop being forced?

Nothing here is a new derivation. Every statement below is either a
citation of existing evidence with its declared scope, or a recorded
obstruction. No sealed file is modified by this packet.

## Repository boundary

`CLAUDE.md` scopes the blind protocol to exactly five paths. They are
**sealed**:

    prompt/            read-only inputs; byte-identity is gated
    paper/             named whole
    code/              named whole
    lean4/Derivation/  carved (the rest of lean4/ is not sealed)
    artifacts/         named whole

Sealed does not mean unwritable. The operating manual instructs
regenerating `artifacts/`, rewriting `artifacts/lean_axioms.txt` when a
theorem is added, and recording material changes in
`paper/paper_change_log.md`. What is sealed is the **boundary**: the
protocol's scope is not retired retroactively, because the derivation's
value is that it was carried out blind.

What is forbidden outright, and named separately in `CLAUDE.md`:

* amending the contract (an author act, not an agent act);
* writing a `paper/coda/` tree;
* external citation, anywhere in the repository;
* modifying `prompt/prompt.md` or `prompt/seed_prompt.md`.

### Paths safe to touch for this packet

`research/genesis_continuation/` — this directory. It is outside all five
sealed paths. The research job now registers four other trees explicitly:
`research/primitive_difference_tower/`, `research/portable_interface/`,
`research/blind_restart/`, and `research/partial_decide/`.

### Paths this packet does not touch

Every sealed path above, and the other research trees.

### Verification status of this tree

**Not gated.** `.github/workflows/verify.yml`'s `research` job names
`primitive_difference_tower`, `portable_interface`, `blind_restart`, and
`partial_decide` explicitly by path; it does not glob `research/` and names no
step for `genesis_continuation`. This tree is therefore invisible to CI. This
packet contains prose only — no code, no tests, no pinned hashes — so there is
nothing here for a gate to check. If anything executable is added later,
registering it in that job is a separate act, and until then its receipts go
stale silently.

## Assumptions

Carried from the sealed derivation, not re-derived here:

1. The metatheory/object-language split of `paper/paper.md` §2.
2. The declared sense of internal separability: profiles differ
   (behavioral separation by positive derivability), `observe.py`.
3. The declared candidate space `Bounds(max_items=2, max_arity=2)` and the
   two declared cost measures `mu1`, `mu2`, `candidates.py`.
4. The implemented isomorphism relation and its canonical keys, `iso.py`.
5. Both admission readings L and F, carried in full and not merged.

Every one of these is **declared**, not derived. That is stated in
`paper/paper.md` §12 and is the single most important input to this
packet's conclusion.

## Stopping conditions for this packet

This packet stops, and does not continue, at the first point where
continuing would require any of:

* an undeclared measure;
* external language;
* an author choice about the contract;
* a theorem the repository does not have.

Two such points were reached and are recorded rather than crossed:

* **OB-1** — the challenge source. No object-language endogenous demand
  generator was derived (`CL-CLOSURE-POLICY`, `paper.md` §11(f)). The one
  horizon-free generator exhibited (`generation_never_dries`) is for a
  declared reflective rule. `G1Class.g1_class_exclusion` now proves the
  cycle impossible for every fixed-radius, fixed-finite-alphabet member of
  `LocalStrategy`; the earlier five-strategy, 15-round computation remains a
  historical witness only. Continuing past this requires an out-of-class
  repair channel or a theorem for a wider declared class. `OB1_UNCHANGED`.
* **OB-2** — initiality. `CL-NO-UNIVERSAL-PROPERTY` is **refused**: no
  universal property was proved for the process among a defined class.
  Per the repository's own discipline the word "minimal" is therefore not
  used of the whole process. This packet does not use it either.

## Two boundary observations found while reading

Recorded because they bear on the repository boundary. OB-3 remains a
claim-level author act on sealed prose. OB-4 was repository hygiene outside
the sealed paths and is discharged below.

* **OB-3 — paper-global sentence withdrawn; comparison policy OPEN.** The
  former claim that §13 still asserts the repository-wide sentence is
  WITHDRAWN as current. Section 13 withdraws that sentence and narrows the
  evidenced boundary, but its replacement inventory is not exact: it says all
  six comparison surfaces are at document ends and describes the first five
  as unfenced.

      paper/bridge_provenance.md:243        headed "Post-hoc comparison with existing names"
      paper/endogenous_generator.md:302     same heading
      paper/primitive_difference.md:407     same heading
      paper/refusal_as_difference.md:393    same heading
      paper/refusal_difference.md:267       same heading
      paper/primitive_difference_map.md:213 "Post-hoc realization table", fenced,
                                            with a "Known mathematics" table column

  All five surfaces headed “Post-hoc comparison with existing names” carry
  explicit end-only markers: “End-only, as before”, “End-only”, “Comparison
  authorized at the end only; nothing above depended on it”, “End-only”, and
  “End-only, as before”, respectively. The map surface is different because
  it explicitly cites the run directive to name identical mathematical
  objects; the other five do not cite that directive.

  The live conflict is between the immutable run directives, which permit or
  require end-only comparison, and `CLAUDE.md`'s restored no-exception
  prohibition, with those six sealed surfaces still present. Two are not
  actually final: substantive sections follow the comparisons in
  `paper/endogenous_generator.md` and `paper/primitive_difference_map.md`.
  Resolving the precedence rule, exact allowed path set, and sealed-paper
  repair is an author act, and this packet does not perform it.

  No gate should encode an allowlist before the author chooses it.
  `ci/check_paper_citations.py` checks only that cited paths resolve, and the
  vocabulary firewall is not a comparison-policy gate. Current terminal:

      OB3_PAPER_GLOBAL_SENTENCE_WITHDRAWN
      OB3_SECTION13_INVENTORY_INEXACT
      OB3_END_ONLY_PLACEMENT_DEFECTS=2
      OB3_COMPARISON_POLICY_OPEN
      AuthorityEffect: None

* **OB-4 — DISCHARGED by this README update from the `24d1bc64` census.**
  The former stale-count paragraph is WITHDRAWN as current. `README.md` now
  records eleven gate families, 58
  Python sources, 74 Lean modules (62 root-closure plus 12 parked), 37 test
  files / 481 collected cases (480 passed, one skipped), 39 deterministic
  JSON exports plus six full exports, 135 `CL-*` headings, and 1506 axiom
  reports. These are dated repository measurements, not mathematical claims.

## What this packet claims

Only what `claims.md` states, with the class and falsifier each entry
carries. The short form: a reusable finite process **is** present in the
existing record and is described in `process_candidate.md` using native
terms only; it is forced only relative to declarations it does not
derive; and the first point at which it is not forced is its challenge
source, OB-1.

## Post-Hoc Comparison

**Withheld.** `CLAUDE.md` states that external citation is not permitted
anywhere in this repository, and `paper/paper.md` §13 withholds the
sealed derivation's own comparison section for the same reason. Adding
one here would widen a prohibition that the contract records as
deliberately restored after having once been narrowed, and amending that
contract is the author's act.

This section is present, and empty, so that its absence is a recorded
decision rather than an omission. See OB-3 for the six existing sections
that do not observe the same rule.
