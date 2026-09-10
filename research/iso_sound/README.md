# Iso sound: hunt a CL-ISO-SOUND falsifier

AuthorityEffect: None.  Outside the sealed derivation; consumes it read-only.
Not registered in `.github/workflows/verify.yml`.

**Result.**  Exhaustive search over a declared finite space found **no**
pair of regimes on which refined canonical-key equality disagrees with
brute-force-key equality.  That is evidence at the stated bound, not a
proof that the implemented key decides isomorphism in general.  The
sealed Lean field for `CL-ISO-SOUND` stays unresolved.

## The space

Well-formed regimes with dummy presentation tokens `d0..d{n-1}`,
`n_data ≤ 3`, `n_forms ≤ 2`, arity `≤ 2`, `|insts| ≤ 3`.  The
implemented isomorphism forgets tokens.  Closed-form size **56020**,
matching the enumeration.  On this run: **5698** refined classes and
**5698** brute-force classes, `agreement: true`, `falsifier_count: 0`.

The seven mixed regimes from the sealed iso tests sit inside the bound
and agree pairwise.  They are a named corpus, not the space.

## What is not claimed

Equal keys on this space do **not** prove `CL-ISO-SOUND`.  The general
refined-key ⇔ isomorphism bridge remains **OPEN**.  A later bound, or a
Lean converse, is a different hunt.

## Running

```powershell
cd research/iso_sound
python verify.py
```

Regenerate records deliberately: `python run.py --write`,
`python verify_lean.py --write`.

## Pins

Baseline `cea346d7f3603fd8da374947e76c9b3cd426d122`.  Consumed:
`code/derivation`, `lean4/Derivation`.  Runtime: `model` and `iso` only.
