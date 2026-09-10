# Reading-F Challenge-3 class distinctness

AuthorityEffect: None.  Outside the sealed derivation; consumes it read-only.
Not registered in `.github/workflows/verify.yml`.

**Result.**  The five named reading F mu1 representatives are pairwise
non-isomorphic, as the Lean theorem `five_classes_pairwise_noniso`,
axiom-clean.  Reading L keeps its sealed three-class proof; reading F
does not inherit that proof by assertion.
Completeness of the catalog as *all* minima remains the sealed engine
enumeration under `Bounds(2,2)` and is **OPEN** as a Lean theorem.

## The five

On `R2F` (data `{0,1,2}`, requirement `(1,2)`, genesis datum `0`
outside the pair):

| name | form | instance |
|---|---|---|
| MarkF | arity 1 | `(0, [1])` |
| DiagF | arity 2 | `(0, [1, 1])` |
| LinkF | arity 2 | `(0, [1, 2])` |
| OutF | arity 2 | `(0, [1, 0])` |
| InF | arity 2 | `(0, [0, 1])` |

Distinctions: arity (mark vs binary); self-loop vs mixed endpoints;
required-pair endpoints vs a genesis endpoint; Out vs In by the
requirement-preserving sort of the instance.

## What is not claimed

The pairwise theorem is not `CL-3-TIE-CLASSES`.  It does not say these
five are every minimum, and it does not close the sealed catalog bound.
Reading L is not re-proved here.

## Running

```powershell
cd research/f_class_distinctness
python verify.py
```

Regenerate records deliberately: `python run.py --write`,
`python verify_lean.py --write`.

## Pins

Baseline `cea346d7f3603fd8da374947e76c9b3cd426d122`.  Consumed:
`code/derivation`, `lean4/Derivation`.  Runtime: `model`, `observe`,
`candidates`, `iso`, `engine`.
