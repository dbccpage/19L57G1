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
sealed paths and follows the precedent already established by two sibling
trees, `research/primitive_difference_tower/` and
`research/portable_interface/`.

### Paths this packet does not touch

Every sealed path above, and both sibling research trees.

### Verification status of this tree

**Not gated.** `.github/workflows/verify.yml`'s `research` job names its
two trees explicitly by path; it does not glob `research/`. This tree is
therefore invisible to CI, exactly as the sibling trees were before that
job existed. This packet contains prose only — no code, no tests, no
pinned hashes — so there is nothing here for a gate to check. If anything
executable is added later, registering it in that job is a separate act,
and until then its receipts go stale silently.

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
  declared reflective rule, and its repair half is empty in the declared
  bounded class. Continuing past this requires either a repair channel
  that separates without minting identity-grade distinctions, or a proof
  that none exists. The repository names this G1 and does not have it.
* **OB-2** — initiality. `CL-NO-UNIVERSAL-PROPERTY` is **refused**: no
  universal property was proved for the process among a defined class.
  Per the repository's own discipline the word "minimal" is therefore not
  used of the whole process. This packet does not use it either.

## Two boundary observations found while reading

Recorded because they bear on the repository boundary, not repaired here.
Repairing either is a claim-level act on sealed prose and is the author's
call.

* **OB-3 — the blindness attestation is false at HEAD.** `paper/paper.md`
  §13 states that the post-hoc comparison is "Withheld in full" and that
  "No external theory, architecture, or terminology is named anywhere in
  this repository outside the read-only seed prompt." Six other files
  under `paper/` carry comparison sections that do name external
  mathematics:

      paper/bridge_provenance.md:243
      paper/endogenous_generator.md:302
      paper/primitive_difference.md:407
      paper/primitive_difference_map.md:213   (a "Known mathematics" table column)
      paper/refusal_as_difference.md:393
      paper/refusal_difference.md:267

  No gate detects this: `ci/check_paper_citations.py` checks that cited
  `paper/*.md` paths resolve, and the vocabulary firewall in
  `tests/test_primitive_contact.py` bars a denylist of CamelCase
  identifiers, not prose naming of external theories. The attestation is
  an operator claim, and it is currently wrong.

* **OB-4 — `README.md` counts are stale.** It records nine gate families
  (there are ten since the `research` job landed), 1417 axiom reports
  (1424), and "72 modules, 59 imported and 13 parked" (12 parked since
  `Derivation.Breaking` was imported). `README.md` is outside the sealed
  paths, so this is a cheap repair; it is listed rather than done because
  it is not what this packet was asked for.

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
