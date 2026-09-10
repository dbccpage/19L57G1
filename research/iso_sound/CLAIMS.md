# Claims: the CL-ISO-SOUND falsifier hunt

AuthorityEffect: None.  Agreement on a finite space is not a proof of
general soundness.  The words forced, minimal, free, canonical,
equivalent, universal, complete appear only with a proof or a scoped
negation.

**Outcome:** no falsifier inside the declared bound.  General
`CL-ISO-SOUND` remains **OPEN**.

### CL-IS-BOUND

- **Statement**: The hunt enumerates every well-formed regime whose
  presentation tokens are the dummy labels `d0..d{n-1}`, with
  `n_data ≤ 3`, `n_forms ≤ 2`, arity `≤ 2`, `|insts| ≤ 3`.  The
  implemented isomorphism forgets tokens, so other token assignments
  are the same iso-classes.  Closed-form size 56020 equals the
  enumeration length.
- **Class**: declared metatheory (the bound) plus deterministic
  computation (the count).
- **Evidence**: `space.count_space`, `space.enumerate_regimes`,
  `evidence/hunt.json` `regime_count`.
- **Falsifier**: enumeration length ≠ 56020, or a dummy-token
  well-formed regime inside the bound that is not yielded.
- **Obligation**: none.  A larger bound, or a token-sensitive key, is a
  different hunt.

### CL-IS-HUNT

- **Statement**: On that space, refined-key equality agrees with
  brute-force-key equality.  5698 classes on each side.  Zero
  falsifiers.
- **Class**: finite computation.
- **Evidence**: `hunt.hunt`; `evidence/hunt.json`;
  `test_evidence.py`.
- **Falsifier**: a pair in the space whose refined-equality bit differs
  from its brute-equality bit.
- **Obligation**: this is not `CL-ISO-SOUND`.  `general_soundness` is
  OPEN.

### CL-IS-HUNT-DEEP

- **Statement**: On the enlarged bound `n_data ≤ 3`, `n_forms ≤ 1`,
  arity `≤ 3`, `|insts| ≤ 4`, refined-key equality agrees with
  brute-force-key equality.  338,650 regimes, 57,266 classes, zero
  falsifiers.  General soundness remains OPEN.
- **Class**: finite computation.
- **Evidence**: `hunt_cl_iso.py`; `space.count_space(3, 1, 3, 4)`;
  `evidence/hunt_deep.json`.
- **Falsifier**: enumeration length ≠ 338650, or a pair in the space
  whose refined-equality bit differs from its brute-equality bit.
- **Obligation**: this is not `CL-ISO-SOUND`.

### CL-IS-CORPUS

- **Statement**: The seven mixed regimes from the sealed iso tests sit
  inside the bound and agree pairwise on refined vs brute equality.
- **Class**: finite computation.
- **Evidence**: `corpus.corpus_agreement`; hunt record `seed_corpus`;
  `test_seed_corpus_matches_sealed_iso_fixtures`.
- **Falsifier**: a corpus pair that disagrees, or a corpus regime
  outside the bound.
- **Obligation**: the corpus is not the space.

### CL-IS-OPEN

- **Statement**: The general refined-key ⇔ isomorphism bridge is not
  proved here.  Lean records that fact as `general_bridge_recorded_open`.
- **Class**: open obstruction.
- **Lean**: `IsoSound.general_bridge_recorded_open` (statement `True`;
  the name records the open field, it does not prove openness).
  Identity-field uniqueness only: `genesis_unique`, `equal_of_fields`.
- **Falsifier**: a general Lean converse, which this tree does not
  claim.
- **Axioms**: `{propext}` on `genesis_wf` only; the other eight reports
  are empty, as recorded in `evidence/lean.json`.

### CL-IS-KERNEL

- **Statement**: The empty regime is the unique 0-data, 0-form,
  empty-store regime, and two regimes with equal fields are equal.
  That is identity serialization, not the refined key.
- **Class**: proved theorem.
- **Lean**: `genesis_unique`, `equal_of_fields`, `genesis_wf`.
- **Falsifier**: a distinct 0-data empty-store regime, or unequal
  field-equal regimes.
