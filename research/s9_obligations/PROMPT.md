# 19L57G1 research run -- S9 bullets 1-3: closed, bounded, or named

Run on merged main as read-only input.  Write only under
`research/s9_obligations/`.

AuthorityEffect: None.

Subject: the first three unresolved obligations of S9 in
`paper/primitive_difference.md`, counted in the order they appear
there.  They are referred to below as S9.1, S9.2, S9.3.  That
numbering is this prompt's, not the paper's; state that in the
receipt.

    S9.1  Axiom lattice.  Only {no axiom, symmetry, irreflexivity}
          were compared.  The complete lattice of one-variable and
          two-variable Horn axioms over one relation, with the
          soundness-transfer property characterized, is open.
    S9.2  Morphism classes.  Initiality of `D2` is proved for
          point-preserving morphisms.  Which edge-preserving
          morphism classes leave some two-element object initial
          is open.
    S9.3  Witness types.  A2 with proof-relevant witnesses carrying
          their own identity rather than counts: whether any
          witness-level structure ever becomes observable below
          function spaces.

This run does not amend the sealed derivation.  It does not close
OB-1, S6.6, or the S9 last bullet (the inscription bridge).  It does
not name any external theory, project, or literature, and writes no
post-hoc comparison.  It does not target a predetermined answer: the
conjecture in F3 is a thing to test, not a thing to confirm.

House rule: nothing happens that is not declared.  A green test is
not a discharged obligation.  A table is not a computation.  An
absent separation is not an equality.

---

## What already exists, and exactly what it says

Read these before writing anything, and do not re-derive them.

* `lean4/Derivation/PrimDiff.lean`
  - `Irrefl`, `Sym`, `Transpose`, `D2`, `D2rev`, `S2`, `Push`,
    `CollapseCollision`, `FidelityObstruction`, `Clos`, `Irred`.
  - `irrefl_witness_ne`, `no_witness_on_subsingleton`,
    `obstruction_under_irrefl` -- irreflexivity's three consequences.
  - `D2_initial_pointed` -- **read its statement, not its name.**  It
    gives existence of a point-preserving map out of `D2` that also
    preserves the oriented edge, and uniqueness quantified over every
    point-preserving `g`, with *no* edge condition imposed on `g`.
    That is one cell of S9.2's classification.  It is not the
    classification, and it is not "initiality for edge-preserving
    morphisms".
  - `bool_irrefl_witness_classification`, `D2_not_pointed_iso_S2`,
    `D2_S2_collapse_equiv`, `oriented_classifier_exists`,
    `symmetric_no_equivariant_classifier`.
  - `single_oriented_witness_consistent`,
    `multiplicity_invisible_to_presence` -- the second is about counts
    *after truncation to presence*.  Do not cite it for a claim about
    witness tokens.
* `code/derivation/primdiff.py` -- `enumerate_pointed`, `pointed_maps`,
  `all_functions_between`, `preserves_rel`, `automorphisms`,
  `pointed_isomorphic`, `collision_profile`, `implication_matrix`.
* `artifacts/primdiff.json`, written by `code/run_primdiff.py`.
* `paper/primitive_difference.md` S1 (the exact metatheory bill of each
  candidate), S7 (the scoped terminal statement), S9, F3.

---

## Preflight

1. Hash this prompt file and record the Git blob id in every receipt.
   Stop on drift.

2. State the write root and the sealed paths in one block:
   `prompt/`, `paper/`, `code/`, `lean4/Derivation/`, `artifacts/` are
   read-only here.  Writing any of them fails the run.  Amending the
   seal is the author's act, not this run's.

3. Write `SOURCE_MANIFEST.json` pinning the canonical Git blob hash of
   every sealed file you read, and `verify_pins.py` that re-checks
   those pins against HEAD and exits non-zero on mismatch.  Follow the
   pin shape already used under `research/`; do not invent a new one.
   Pin the exact 40-digit snapshot commit, never `HEAD`.

4. Declare the resource bounds before running anything: the carrier
   bound `N` for each part, the closure-size bound for S9.1's lattice,
   and what you do when a bound is hit (report BOUNDED with the
   partial, never extrapolate).

---

## P1 -- S9.1, the axiom lattice

5. Declare the axiom space in writing before enumerating.  Universally
   quantified Horn clauses over one binary relation `r` in at most two
   variables.  Atoms: `r x x`, `r x y`, `r y x`, `r y y`.  Head is one
   atom or falsum.  Body is a subset of atoms.  An axiom is a finite
   set of clauses.  Print the clause count before and after quotienting
   by the swap of `x` and `y`, and say which count you use downstream.

6. Any clause mentioning `x = y` in body or head imports the
   metatheory's own identity -- that is A3's bill, not A1's (S1).
   Enumerate that fragment **separately**, label it `EQ_BEARING`, and
   never merge its results into the pure fragment's without saying so
   in the same sentence.

7. Define soundness transfer in one displayed line before computing
   anything.  Default definition: an axiom `phi` transfers iff for
   every pointed structure `(X, r, a, b)` with `r a b` and `phi(r)`,
   the metatheory has `a != b`.  If you use another definition, name
   it, say why, and compute both.

8. Compute extents over all relations on carriers `1..N`.  `N = 3` is
   required; report whether `N = 4` completed inside the bound.  Do not
   attempt `N = 5`; refuse it by name.

9. The lattice is a lattice of **extents**, not of syntax.  Deduplicate
   axioms by extent, report the syntax-class count and the extent-class
   count side by side, and take the meet-closure of the single-clause
   extents up to the declared bound.  If closure hits the bound, say
   so; a truncated closure is not a complete lattice.

10. Fix the order once and print which direction is "stronger".  Then
    report, as separate findings: whether the transferring set is
    upward closed; whether it is closed under meet; whether it has a
    unique minimum.  Only if it has a unique minimum whose extent
    equals irreflexivity's extent may you write that the transferring
    axioms are generated by irreflexivity -- and that stays bounded by
    `N` until Lean carries it.

11. Print the set of axioms that transfer but do not entail
    irreflexivity, **even when it is empty**.  That set is the entire
    content of F3's conjecture; a conjecture confirmed by not looking
    is not confirmed.

12. Negative test: if the classifier returns "all transfer" or "none
    transfer", print the witness structure and treat the result as a
    defect until you have shown otherwise.

13. Lean, carrier-general half.  Attempt the general statement that
    makes the finite sweep more than a table -- for instance, whether a
    clause whose head is an atom can transfer at all, given that the
    one-point full relation satisfies every such clause and already
    hosts a self-difference (`selfdiff_consistent`).  If it proves,
    cite the theorem name.  If it does not, report the bounded result
    and say what blocked it.  No prose proof, ever.

---

## P2 -- S9.2, morphism classes and initiality

14. Restate `D2_initial_pointed`'s exact quantification in the ledger,
    in the terms of step 5's discipline, and record it as one cell of
    the classification.  If your model of that cell disagrees with the
    Lean theorem, your model is wrong; fix the model and never weaken
    the theorem.

15. Declare the finite menu of morphism conditions, each with a short
    name and a one-line definition.  At minimum: designated points
    preserved; edges preserved; non-edges preserved; injective;
    surjective.  Declare the object class separately -- carrier bound,
    asserted pair required, and whether irreflexivity is imposed on
    objects.  A morphism class is a subset of the menu.  Print the
    menu size and the class count.

16. For every class `C` and every two-element pointed structure `O`
    with an asserted pair, decide by finite search: is `O` initial --
    for every object `Y`, exactly one `C`-morphism `O -> Y`?  Report
    existence failures and uniqueness failures in separate columns,
    each with a named witness object.  "Not initial" with no witness
    is not a result.

17. Quotient candidate objects with the implemented relation
    (`pointed_isomorphic`), never by hand.  Retain ties: if two
    non-isomorphic two-element objects are both initial for a class,
    keep both, the way S7 keeps `D2` and `S2`.

18. Report the classification as a table, then state its shape: the
    minimal classes admitting an initial two-element object and the
    maximal ones.  If the admitting classes form an interval under
    inclusion, give both endpoints; if they do not, print an
    incomparable pair.  Do not describe the shape you expected.

19. Mark the whole classification BOUNDED: initiality quantifies over
    all objects and your sweep reaches carrier `N`.  For any class
    where a uniform argument exists, carry it in Lean as its own
    theorem.  Cells without a Lean theorem stay finite computation.

20. Say plainly whether your own sweep reproduces S9's fifth bullet --
    a finite scope whose exhaustiveness lives in Python only.  If it
    does, name it as such rather than letting it pass.

---

## P3 -- S9.3, proof-relevant witness types

21. Declare the witness-type layer against A2's bill (S1).  A2 supplies
    `W : X -> X -> Nat`.  Replace the counts by a finite token domain
    with identity across pairs.  State in one line exactly what is
    admitted beyond A2 -- token identity is an admitted primitive, not
    a derived one.  If you need an equality judgment on tokens, admit
    it by name and price it.

22. Declare the observation vocabularies as explicit finite sets of
    expressible questions, none of them using function types:
    `V0` presence only; `V1` presence and count comparisons; `V2`
    presence and token-identity questions.  State exactly what "below
    function spaces" forbids -- maps as data, composition, quotients --
    and refuse any construction that needs them, by name.

23. Build the separating pair: two witness assignments over one carrier
    that `V1` cannot distinguish and `V2` can, or prove none exists in
    the declared finite space.  Enumerate; do not hand-pick a pair and
    call the space searched.

24. Test the other direction too: exhibit witness-level structure that
    remains invisible even in `V2`, or report that none was found.  The
    answer to S9.3 is a boundary, not a yes.

25. Answer S9.3 in one sentence with its scope attached: witness-level
    structure becomes observable below function spaces exactly when
    <the named admission of step 21> is admitted, within the declared
    vocabularies and the declared finite space.

26. Lean: formalize the separating pair as concrete finite types.
    Prove presence-equal, count-equal, and non-isomorphic as witness
    families.  If the negative half -- that no `V1` question separates
    them -- is not formalizable under your encoding of the vocabulary,
    mark it finite computation and name the encoding as the obstacle.

---

## Lean discipline for this tree

27. Lean work lives in this tree's own Lake package, requiring the
    sealed package as a dependency, exactly as the existing research
    package does.  Do not add modules under `lean4/Derivation/`.

28. No `sorry`, `admit`, user-declared axiom, `unsafe`, or `partial`.
    Every exported theorem gets a `#print axioms` report, and every
    report must lie within `{propext, Quot.sound}`.  That rules out
    classical choice: decidability has to be constructive, so finite
    claims go through `decide` and explicit instances.

29. This tree's axiom reports are a **manual receipt**.  No CI gate
    reads them.  Say so in `STATUS.md` in those words; do not let a
    committed report imply enforcement it does not have.

---

## Synthesis

30. `CLAIM_LEDGER.md`: one row per claim, each naming its evidence --
    test name, artifact key, Lean theorem name -- and each classified
    as exactly one of proved theorem, bounded theorem, finite
    computation, countermodel, conjecture, or open.  A row whose
    evidence does not resolve is a defect, not a claim.

31. `STATUS.md`: the terminals with their scopes, the resource bounds
    actually reached, what stayed open and why, and the manual-receipt
    sentence from step 29.  Include the exact registration diff that
    would add this tree to the research gate, as text.  **Do not edit
    `.github/workflows/verify.yml`.**

32. `PROPOSED_S9.md`: for each bullet you claim to discharge, the exact
    replacement text as a diff against the current bullet, with the
    residual scope written into the bullet itself.  It is a proposal.
    The author applies it or does not.  A bullet you only narrowed gets
    a narrowed bullet, not a deletion.

33. Receipts are timestamp-free and replay byte-identically.  Generate
    twice into different directories and compare bytes.

34. Tests, with `unittest`, strict `mypy` clean: the declared axiom
    space and its counts; the transfer classifier against hand-checked
    cases including irreflexivity and symmetry; the `D2_initial_pointed`
    cell; existence and uniqueness failures carrying witnesses; the
    witness-type separating pair or its declared impossibility; tie
    retention; and negative tests for every forbidden closure below.

---

## Forbidden, each with a negative test that fails the run

35. Writing any sealed path, or amending another tree's receipt.

36. Claiming OB-1, S6.6, or the S9 last bullet closed, narrowed, or
    priced.  They are a different obligation and are not in scope.

37. Promoting a bounded sweep to a carrier-general claim, in prose or
    in a ledger row, without a Lean theorem naming the general case.

38. Reading the F3 conjecture as an input.  If your run cannot fail it,
    it did not test it.

39. Any identifier from the working denylist in
    `contact/analysis/contact_countermodels.json` appearing outside
    `contact/analysis/`.  The firewall walks every tracked file.

40. Naming an external theory, project, or body of literature anywhere
    in what you write.

---

## Legal terminals, each with scope

    S9_1_LATTICE_COMPLETE
    S9_1_LATTICE_BOUNDED
    S9_1_TRANSFER_CHARACTERIZED
    S9_1_TRANSFER_OPEN
    F3_SUPPORTED_BOUNDED
    F3_REFUTED
    F3_UNTESTED
    EQ_FRAGMENT_SEPARATED
    S9_2_CLASSES_CLASSIFIED
    S9_2_CLASSES_BOUNDED
    S9_2_INTERVAL_SHAPE
    S9_2_INCOMPARABLE_CLASSES
    TIES_RETAINED
    S9_3_WITNESS_OBSERVABLE
    S9_3_WITNESS_INVISIBLE
    S9_3_ADMISSION_NAMED
    LEAN_CARRIED
    LEAN_NOT_CARRIED
    PYTHON_ONLY_SCOPE_DECLARED
    MANUAL_RECEIPT_DECLARED
    OB1_UNCHANGED
    S66_UNCHANGED
    S9_LAST_UNCHANGED
    PROPOSED_TEXT_WRITTEN
    REFUSED

---

## Definition of done

The axiom space, the morphism menu, the token domain, and the three
vocabularies are each declared before use, with counts.  Every claim
carries evidence that resolves.  Each of S9.1, S9.2, S9.3 ends in
exactly one of: discharged with scope, narrowed with the residual
written, or open with the obstruction named -- and the proposed
replacement text exists for each one you touched.  Bounded results say
`bounded` in the same sentence as the result.  The three protected
opens are untouched.  The prompt hash is stable and the receipts
replay byte-identically.

---

## Running this

The three parts are independent up to the synthesis step.  They may be
run in one session, or by three agents in parallel, on the condition
that each part writes only its own modules, tests, and receipt
fragment; `CLAIM_LEDGER.md`, `STATUS.md`, and `PROPOSED_S9.md` are
written once, last, by a single pass that reads all three.

P1 and P2 need Python only until their Lean steps.  P3 needs the Lake
package from step 27.  If Lean is unavailable in the environment, run
P1 and P2 to their bounded terminals, emit `LEAN_NOT_CARRIED`, and stop
-- do not substitute prose for the missing proofs.
