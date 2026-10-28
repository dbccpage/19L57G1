# qm_bridge: the first rows of a bridge from Genesis objects to a finite amplitude formalism

AuthorityEffect: None.

A research tree outside the sealed derivation.  It consumes the merged
`research/two_theorems` package read-only (`Institution`, `Knows`,
`information`, `know_or_witness`, `information_lt_of_not_knows`,
`knows_iff_information_eq`) and the sealed `Derivation.Compression` through
it.  It adds nothing to `lean4/`, edits nothing in `two_theorems`, and proves
its statements in core Lean 4.33 with no library beyond those two packages.
Every `#print axioms` report named in `TREE_CONTRACT.json` lies within
`{propext, Quot.sound}`; no proof uses a choice principle
(`python verify.py --check`, 22 named declarations).

This tree is milestone M2 of the 18-month plan approved by the author on
2026-10-28 (sub-theorem B1, clauses (i) to (iii)).  It proves nothing about
nature.  It states which structure a finite challenge forces relative to
named admissions, and which it does not.

## Supplied vocabulary

The words amplitude, phase, interference and their relatives are supplied
vocabulary, used outside the seal under the author's vocabulary ruling of
2026-09-23.  They name the challenge and the admitted model; they supply
neither a derivation nor a proved bridge into the sealed derivation.  Their
hits are pinned in the prose watchlist census.

## Admissions and challenge

| name | kind | what it is | where |
|---|---|---|---|
| A_G | admitted (Genesis) | a finite carrier `D : List Nat` of preparation labels, presentations `Nat → Nat` on it, question families, Genesis signature equality | sealed `Compression`, `two_theorems` |
| R_int | externally imposed challenge | `InterferenceChallenge D Q₀ q`: two preparations the weight presentations `Q₀` do not tell apart on which the readout `q` differs | `Residual.lean` |
| A_amp | admitted at a price | amplitudes in `ℤ[i]`, the involution, the modulus `c·c̄`, and the add-then-square readout of a two-sector mixing context; a readout on a cyclic phase group is invariant under conjugation | `Gauss.lean`, `Multiplicity.lean` |
| A_cos | imported classical fact, priced, not proved | the cosine is injective on `[0, π]`, so `Re ζ_N^j` separates the conjugation classes of every order `N` | QB-11 only |

The weights are presentations, so A_W of the plan (a weight presentation
per context) is here the special case of A_G in which `Q₀` is read as
weights.

## What is proved

**B1(i), RECOVERED (`Residual.lean`).**  The interference challenge holds
exactly when the weight institution does not know the readout
(`challenge_iff_not_knows`), exactly when adding the readout changes Genesis
information, and then strictly raises it (`challenge_iff_information_ne`,
`challenge_information_lt`).  Either the weights know the readout or the
challenge holds (`challenge_or_knows`).  So an interference challenge is a
residual in the sense of `two_theorems`: a question the institution's
fibers do not determine.  The proofs are two lines; the content is the
identification.

**B1(ii), NECESSARY (`Gauss.lean`, `Multiplicity.lean`).**  Under A_amp:

- the mixing readout is the two weights plus twice the cross term
  `Re(c₁·c̄₂)` (`polarization`); with the weights fixed it separates two
  preparations exactly when their cross terms differ
  (`separates_iff_cross`).  So every model meeting the challenge has two
  amplitude pairs on one fiber of the weight map (`fiber_necessary`): a
  nontrivial fiber is necessary;
- a conjugation-invariant readout on the order-`N` cyclic group is a
  function of the class representative, which is at most `N / 2`
  (`readout_factors`), so it separates at most `N / 2 + 1` phases
  (`multiplicity_bound`, through a choice-free pigeonhole `nodup_le`);
- for `k ≥ 1` and `N ≥ 1`, some invariant readout separates `k` phases of
  order `N` exactly when `2k - 2 ≤ N` (`realizable_iff`).  The least order
  for `k ≥ 2` separated readouts on one fiber is `2k - 2`; the sign group
  carries exactly two (`signs_iff`); three need order four
  (`three_needs_four`).

Exact witnesses: `(1, 1)` and `(1, -1)` share weights and read 4 and 0
(`sign_pair`); `(1, 1)`, `(1, i)`, `(1, -1)` share weights and read 4, 2, 0
(`mu4_triple`); on the four units of `ℤ[i]` the readout is invariant under
conjugation and separates the three classes (`mu4_readout_invariant`,
`mu4_readout_values`), so at order four the real part itself realizes the
bound.

**B1(iii), OPTIONAL (`Multiplicity.lean`).**  Every finite multiplicity is
realized in a finite cyclic group (`finite_order_suffices`).  No finite
interference challenge of this form forces the circle.  This says the circle
is not admitted as primitive by these challenges; it does not say the circle
is absent from anything.

**The model meets the challenge (`Instance.lean`).**  The carrier
`[0, 1, 2]` with the amplitude pairs above, read through A_amp, gives three
presentations: two weights and the readout.  The weights carry information
1; with the readout, 3; they do not know the readout
(`instance_information`, `instance_not_knows`, `instance_challenge`).

## Encoding audit

The plan requires, for every NECESSARY row, a check that the forced
structure does not appear in the definitions used to state the challenge.

- `InterferenceChallenge D Q₀ q` mentions a list of naturals, a list of
  presentations `Nat → Nat`, one presentation and Genesis `SigEq`.  It names
  no ring, involution, group, phase or modulus.  The mechanical check
  `test_challenge_mentions_no_amplitude` decides it on presentations alone.
- The fiber of B1(ii) appears only after A_amp is admitted: the theorem says
  that *within* models of the stated amplitude form, meeting the challenge
  forces two amplitude pairs on one weight fiber.  Relative to A_G alone the
  forced structure is the residual of B1(i); the fiber is its form under
  A_amp.  The row is NECESSARY relative to A_G ∪ A_amp, not relative to A_G.
- The multiplicity bound reads the readout only through conjugation
  invariance, which A_amp states; it assumes nothing about which readout.
- Outstanding: the plan asks for this audit to be repeated by a reviewer
  who did not write the proofs.  That review has not happened.

## Outside the system

`N`, `k` and the box bounds are metatheory numbers.  Each theorem about
every `N` or every `k` is proved once, uniformly; no totality of phase
groups, carriers or readouts is held by the system.  `Int` and `Nat` in the
Lean statements are the metatheory's.  The finite model checks the bounds in
`input.json` and nothing beyond them.

## Not claimed

That Genesis selects this formalism; that A_amp is derived; that the real
part realizes the bound at every order (QB-11 is CONDITIONAL on A_cos); the
holonomy row B1(iv) and its native source B1(iv′) (OPEN, milestone M4).

## Run

`python verify.py --check` runs local pins, tests, strict typing, every
Lean source and the named report scope.  It needs `lake` for Lean 4.33 on
the path.  `python verify.py --write-pins` regenerates the input digest.
`verify.py` is the canonical new-tree copy, unchanged.
