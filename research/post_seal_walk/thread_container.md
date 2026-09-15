# Thread: container, sides, orientation, kind of order

`AuthorityEffect: None.` This is the post-seal derivation that the
previous review did not read. Write-roots, in the order they were run:

`boundary_seed` (33 commits) → `side_free` (13) → `oriented_boundary` (2).

The sealed kernel already had the *priced* orientation bridge
(`two-ness ↛ orientation`; `priced_bridge_oriented`) and
`Apartness.orientations_differ`. This thread asks a different question:
**does genesis start with a container, and is an order that container?**

---

## 1. `research/boundary_seed/` — second derivation from `<|>`

Seed `de6c2f9f` (2026-09-04). Own kernel. Does not import the sealed
derivation. Provenance of the existing run:
`SOURCE_ISOLATED_WITH_DECLARED_PRIOR_EXPOSURE` — the instrument had
already seen `<>`. That is recorded, not repaired.

Admitted primitive (one declaration): a **boundary with two sides**.
Two towers to the end:

| | U (unoriented) | O (oriented) |
|---|---|---|
| sides | distinct, unnamed | named near / far |
| reflection | permitted renaming | not permitted; moves a placed mark |
| C0 empty sides | collapsed | differ by the two names only |
| C0 successor | none forced | none forced |
| C3 `<a|>` vs `<|a>` separable? | **no** | **yes**, cost 0 |
| C3 minimum | **1**, three tied classes | **0**, null only |

C0: emptiness is not an internal judgment. No `OnSide` at genesis. No
event follows from the state.

C3 U minima, all retained:

1. withdraw the side exchange
2. withdraw mark permutations (meets **by unfolding**; the boundary is idle)
3. one further mark, either side (unequal side counts)

Adopting reading O under U costs 2 and is refused as a bundle. Under O,
what meets the requirement is **withdrawal of the side exchange, paid at
genesis**. The two names are idle (four-cell counterfactual).

Continuation stage 2: 0 accepted augmentations; resource frontier after
four supply attempts. Next challenge would be nested `|<a|>`.

Paper: `research/boundary_seed/paper.md`. Receipts:
`receipts/challenge0.json` … `challenge5.json`, `continuation1.json`,
`continuation2.json`.

**What this answers.** A container at genesis is **admitted, not
derived**. Named sides buy internal separation of the two placements for
free. Unnamed sides do not.

---

## 2. `research/side_free/` — drop the container

Design and predictions frozen `6ca1a73a` (2026-09-05) **before any
code**. Same C3 requirement. Carrier: labels in admission order. No
placement, no sides, no two-sided whole.

| field | value |
|---|---|
| side-free min `mu1` | **1**, unique, `withdraw_mark_permutations` |
| unnamed (U) min | 1, 3 tied classes |
| named (O) min | 0, 1 class |
| `delta_vs_unnamed` | **0** |
| `delta_vs_named` | **+1** |
| what the primitive bought in cost | `NOTHING_IN_COST` |
| routes bought | 2, both side-mediated (`withdraw_reflection`, `extra_mark`) |

Terminal sentence (`STATUS.md`):

> It bought no price that the admission order could not buy at the same
> price.

Residue the tree **ends on**, not a side remark:

> what pays for separation in a world with no container is the ADMISSION
> ORDER, and whether an order is itself a container is a further
> question this control does not answer.

That question is `SF-OPEN-A`.

27/27 frozen predictions HIT (four of them FORCED, not counted as
content; P24 mislabelled FORCED in fact). Lean forgetful lemma:
pinned min ≤ side-free min. Gate 11 (pins + Lean receipt is still
manual).

---

## 3. `research/oriented_boundary/` — order is not a container

Landed `c0c4ac50` (2026-09-11). Analytic discharge of `SF-OPEN-A`, then
mechanized. The blind `SEED.md` is **parked** for an independent run.

**(B)-empty lemma** (`lean/OrientedBoundary/Basic.lean`):
`b_is_empty`, `not_in_aut_needs_witness`. `σ ∈ Aut` iff no admitted
judgment distinguishes the pair. Hence `σ ∉ Aut` **forces** an admitted
asymmetric witness (mechanism A). Route (B) — withdraw `σ` with no
witness — is empty. Python exhausts all 16 judgment-sets on four
distinct judgments.

One capability: unoriented (symmetric judgment) has `σ ∈ Aut`; oriented
breaks it at exactly one asymmetric witness.

Kind (analytic, existence conditions):

- Boundary / container: **exists before contents** (empty sides at genesis).
- Order / relation: **exists only with contents** (needs a pair).

So the admission order is not a container. It is a paid
symmetry-breaking admitted witness.

Not succession: orientation is static two-sidedness. No clock entered
the language.

`AUTHOR_READING.md` records the author's withheld mapping of the two
readings onto two imported nouns, and the prediction **two kinds, one
primitive, one toll**. A clean-model run of `TIME_PROMPT_v2.md` scored
HIT / VERDICT T7 on (B)-empty. That is **not** a claim about nature.
The space/time functor is deferred and refused here.

`SF-OPEN-A` is DISCHARGED as a kind-question. The blind seed remains
the independent confirmation that has not been run.

---

## How the three fit the sealed map

Sealed `paper/native_derivation_map.md` already had:

| source | relation | target | status |
|---|---|---|---|
| two-ness | equivariantly yields | orientation | FALSE |
| admission | priced asymmetry yields | orientation | PROVED |

This thread does not redo that bridge. It asks whether **putting a
boundary in at genesis** is forced, cheap, or a different kind of thing
from the order that pays for separation without a boundary.

Answer: not forced (C0 of both `<>` and `<|>`); not cheap for the
unnamed reading (`NOTHING_IN_COST`); a different kind from order
(existence conditions).
