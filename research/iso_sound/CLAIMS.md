# Claims: the CL-ISO-SOUND falsifier hunt

AuthorityEffect: None.  Agreement on a finite space is not a proof of
general soundness.  The words forced, minimal, free, canonical,
equivalent, universal, complete appear only with a proof or a scoped
negation.

**Outcome:** no falsifier inside the declared bound.  General
`CL-ISO-SOUND` remains **OPEN**.

### CL-IS-BOUND

- **Statement**: The hunt enumerates every well-formed regime with
  `n_data ≤ 3`, `n_forms ≤ 2`, arity `≤ 2`, `|insts| ≤ 3`.  Closed-form
  size 56020 equals the enumeration length.
- **Class**: declared metatheory (the bound) plus deterministic
  computation (the count).
- **Evidence**: `space.count_space`, `space.enumerate_regimes`,
  `evidence/hunt.json` `regime_count`.
- **Falsifier**: enumeration length ≠ 56020, or a well-formed regime
  inside the bound that is not yielded.
- **Obligation**: none.  A larger bound is a different hunt.

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

### CL-IS-CORPUS

- **Statement**: The seven mixed regimes from the sealed iso tests sit
  inside the bound and agree pairwise on refined vs brute equality.
- **Class**: finite computation.
- **Evidence**: `corpus.corpus_agreement`; hunt record `seed_corpus`.
- **Falsifier**: a corpus pair that disagrees, or a corpus regime
  outside the bound.
- **Obligation**: the corpus is not the space.

### CL-IS-OPEN

- **Statement**: The general refined-key ⇔ isomorphism bridge is not
  proved here.  Lean records that fact as `general_bridge_recorded_open`.
- **Class**: open obstruction.
- **Lean**: `IsoSound.general_bridge_recorded_open`.  Identity-field
  uniqueness only: `genesis_unique`, `equal_of_fields`.
- **Falsifier**: a general Lean converse, which this tree does not
  claim.
- **Axioms**: none on those three; `{propext}` on the others as
  recorded.

### CL-IS-KERNEL

- **Statement**: The empty regime is the unique 0-data, 0-form,
  empty-store regime, and two regimes with equal fields are equal.
  That is identity serialization, not the refined key.
- **Class**: proved theorem.
- **Lean**: `genesis_unique`, `equal_of_fields`, `genesis_wf`.
- **Falsifier**: a distinct 0-data empty-store regime, or unequal
  field-equal regimes.
