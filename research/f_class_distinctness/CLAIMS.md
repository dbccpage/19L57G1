# Claims: reading-F Challenge-3 class distinctness

AuthorityEffect: None.  Pairwise non-isomorphism of five named
representatives is not a proof that those five are all the mu1 minima.
The words forced, minimal, free, canonical, equivalent, universal,
complete appear only with a proof or a scoped negation.

Both readings are carried.  Reading L keeps the sealed three-class
theorems.  Reading F is proved here.  F does not inherit L's proof by
assertion.

### CL-FCD-PAIRWISE

- **Statement**: The five named reading-F Challenge-3 representatives
  `MarkF`, `DiagF`, `LinkF`, `OutF`, `InF` are pairwise
  non-isomorphic.
- **Class**: theorem.
- **Lean**: `FClassDistinctness.five_classes_pairwise_noniso`.
- **Python**: `classes.pairwise_noniso(F_REPS)` is empty;
  `evidence/classes.json` `pairwise_noniso`.
- **Falsifier**: an `Iso` between any two of the five.
- **Axioms**: `{propext, Quot.sound}` as recorded in `evidence/lean.json`.

### CL-FCD-VALID

- **Statement**: Each of the five is a two-item valid response on `R2F`
  to requirement `(1, 2)`.
- **Class**: theorem.
- **Lean**: `five_valid_pairwise_noniso`, the five `delta*F_valid`.
- **Falsifier**: a named delta that fails `validResponse`.

### CL-FCD-WITHIN

- **Statement**: The other member of each size-2 class (swap of the
  required pair) is isomorphic to the named representative.  The mark
  collapse is the sealed `isoU2F_U0F`; the other four are
  `iso*F'_exists` here.
- **Class**: theorem (four new; mark sealed).
- **Falsifier**: swap12 fails to be an `Iso` on one of the four binary
  classes.

### CL-FCD-ENGINE

- **Statement**: Under `Bounds(max_items=2, max_arity=2)` the engine
  finds 5 mu1 classes in reading F and 3 in reading L, and each named
  F representative is isomorphic to exactly one engine class.
- **Class**: finite computation.
- **Evidence**: `classes.class_record`; sealed
  `test_challenge3_reading_f_has_five_classes`.
- **Falsifier**: engine count other than 5/3, or a named representative
  that hits zero or two engine classes.

### CL-FCD-CATALOG

- **Statement**: Completeness of the five as *all* mu1 minima is **not**
  proved here.  That remains the sealed bounded enumeration
  `CL-3-TIE-CLASSES`.  Catalog completeness is **OPEN** as a Lean
  theorem.
- **Class**: open obstruction (completeness); the pairwise theorem does
  not close it.
- **Falsifier**: a Lean proof that every valid two-item response on
  `R2F` is isomorphic to one of the five — which this tree does not
  claim.

### CL-FCD-L-CARRIED

- **Statement**: Reading L is carried, not re-proved.  The sealed
  theorems `U0_not_iso_BL`, `U0_not_iso_BD`, `BL_not_iso_BD`,
  `isoU1U0` are not cited by `FClassDistinctness.lean`.
- **Class**: declared scope.
- **Evidence**: `tests/test_prose.py::test_lean_does_not_cite_l_distinctness_theorems`.
- **Falsifier**: an F distinctness proof that names those L theorems.
