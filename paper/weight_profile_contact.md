# Finite weight profiles and the contact ceiling

**Corrected contact response.** The native result in this repository is a
finite `Nat`/`Int` weight-profile calculation. It is not a Hilbert lift and it
does not price a path to one. The supplied `qm_020` package is mentioned only
in Section 6 as a scope comparison; it supplies no premise or evidence here.

Evidence:

- `lean4/Derivation/WeightProfile.lean`;
- `code/derivation/weight_profile.py`;
- `artifacts/weight_profile.json`; and
- ledger claim `CL-PD2-WEIGHT-PROFILE`.

## 1. Declared data and carrier policy

A weight assignment is a declared natural-number count at each label. The raw
function `total` is list algebra: if a label is repeated, its weight is counted
again. Carrier-facing claims use `CarrierList l := l.Nodup`. Thus duplicate
labels have an explicit meaning in raw sums and are explicitly inadmissible as
a carrier presentation; they are never silently quotient-deduplicated.

Nothing in the passage calculus generates the weights or this carrier policy.

## 2. The positive-domain profile

`SameProfile l w v` cross-multiplies by the two totals instead of dividing.
Reflexivity and symmetry hold for all assignments. Transitivity needs the
middle total to be positive. Consequently:

- `profile_equivalence_positive` packages an equivalence law on the declared
  positive-total domain;
- `profile_scale_positive` proves that a positive scale preserves both the
  profile and that domain; and
- `profile_iff_ray` says that two positive-total assignments have the same
  profile exactly when they have common positive cross-multiples pointwise.

The last statement is an exact finite classifier in natural arithmetic. The
word "ray" here abbreviates that displayed cross-multiple relation; it does not
introduce a real vector space.

Zero scale must be kept separate. `profile_scale_raw` also holds at scale zero
because the cross-product equations become zero equations, while
`zero_scale_boundary` proves the scaled total is zero and therefore outside
the positive domain. Zero scale is not a positive-ray action.

Within the positive domain the profile preserves support and coordinate order
and forgets total mass (`profile_support`, `profile_order`, and
`profile_forgets_total`).

## 3. What a decorated presentation proves

`Presents l m c w` means that `l` is duplicate-free and `m (c p) = w p` on
that carrier. It follows directly that the resulting weight assignment has
the same profile as `w` (`presentation_profile_redundant`), and two such
presentations agree at the profile level (`presentations_agree_on_profile`).

This is only a factorization identity for a declared finite presentation. It
does not construct a vector space, an inner product, a state, a dynamics, a
probability rule, or a representation theorem.

## 4. Unsigned determination and the signed-square fixture

For the particular map `sq : Nat -> Nat`, squaring is injective. Hence two
valid unsigned square presentations of the same weights agree at every carrier
label (`unsigned_decoration_determined`). There is no nonuniqueness witness in
this unsigned square model.

The valid nonuniqueness witness lives in a separately declared integer fixture:

- carrier `[0, 1]`;
- integer square map;
- weight assignment `(1, 1)`;
- presentations `(1, 1)` and `(1, -1)`; and
- declared mixing read-out `(x + y)^2`.

Both presentations square to the same weights, they differ at label `1`, and
the declared mixing read-out separates them
(`signed_square_presentations_split`). This proves only that this square map
forgets a sign which this mixing read-out can see. It does not show that every
sign is observable, that every mixing question separates, or that a general
"lift" has extra capacity.

## 5. Exact two-coordinate descent and the failed climb

For two integer coordinates, `readOut a b x y = a*x + b*y`. After squaring,
this read-out is constant on inputs with equal coordinate squares exactly when
`a*b = 0` (`descent_iff_subsingleton_support`). The identity `sq_add_sub`
isolates the cross term used in that proof. This classification is scoped to
that read-out, that square observation, and two coordinates.

The earlier three-rung "priced climb" was invalid:

| Former rung | Correct disposition |
| --- | --- |
| A decorated carrier with a surjective modulus and commutative modulus of combination | Trivially inhabited by `Nat`, the identity map, and addition (`decoratedCarrierShape_exists`); too weak to be a substantive import |
| Additivity over appended lists | Already a theorem of `total` (`total_append`); overlap means multiplicity, not disjoint union |
| The displayed read-out uniqueness schema | False: the zero read-out is profile-invariant and append-additive but differs from positive total (`claimedReadOutUniqueness_false`) |

The old `eB` example was also invalid evidence: it did not present the claimed
weights. A non-presentation cannot witness nonuniqueness of presentations and
has been removed.

The honest terminal is therefore:

```text
FINITE_WEIGHT_PROFILE_AND_SIGN_SHADOW_PROVED
READOUT_UNIQUENESS_SCHEMA_REFUTED
NO_REPRESENTATION_CLIMB_DERIVED
```

## 6. Comparison ceiling for `qm_020`

The supplied package discusses Born normalization and a conditional Hilbert
lift. The native contact reaches only the following lower-level analogies:

| Package-facing phrase | Native result | Ceiling |
| --- | --- | --- |
| normalization | `SameProfile` and `profile_iff_ray` | finite natural weights, cross-multiplication, positive totals |
| scale invariance | `profile_scale_positive` | positive natural scales only; zero scale explicitly exits the domain |
| redundant re-encoding | `presentation_profile_redundant` | declared finite factorization identity only |
| phase or sign sensitivity | `signed_square_presentations_split` | one two-coordinate integer-square/mixing fixture |
| sparse descent | `descent_iff_subsingleton_support` | one two-coordinate linear read-out followed by squaring |

No native theorem supplies complex scalars, a Hilbert space, an inner product,
unit vectors, amplitudes, phases as a group action, tensor products, operators,
dynamics, the Born rule, continuity, limits, or a uniqueness characterization.
The finite result may be a useful prerequisite or counterexample generator for
a later contact, but it is not that contact's representation lift.

Nothing in this note upgrades a theorem by analogy.
