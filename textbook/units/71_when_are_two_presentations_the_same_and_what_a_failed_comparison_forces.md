# Unit 71. When do two presentations preserve the same distinctions?

**Claim.** On a supplied finite list of natural numbers, two numerical presentations preserve the same distinctions exactly when each can be recovered from the other. A failed recovery has a witnessing pair.

**Status:** derived under the stated finite-domain and factorization hypotheses; no preferred repair or termination of future comparisons is established. **Lean:** `PresentationRelativity.presentationIdentity_iff_fiberIdentity`, `presentationIdentity_iff_residualEmpty`, `forced_split_of_factorization_failure`, `jointPresentation_strict_of_factorization_failure`; `ResidualClosure.common_refinement_closes_current_obstruction`. **Sources:** `lean4/Derivation/PresentationRelativity.lean`, `lean4/Derivation/ClosureSymmetry.lean`, `lean4/Derivation/ResidualClosure.lean`. **Axioms:** the cited source reports lie within `{propext, Quot.sound}`. **Depends on:** Unit 61 (signatures and factorization), Unit 47 (operational support), and Unit 40 (the declared generator). **AuthorityEffect:** None.

## First pass: compare the groups, then the labels

A presentation assigns a numerical label to each datum. Two presentations can use different labels yet group the data in exactly the same way.

On `D = [0, 1, 2]`, the tables `p = [0, 0, 1]` and `q = [7, 7, 9]` both group `0` with `1` and keep `2` separate. Looking up either presentation's label is enough to recover the other's label.

Now replace `q` by `[0, 1, 1]`. The pair `0, 1` has the same `p`-label but different `q`-labels. No lookup using only `p` can recover this `q`. That pair is the failure witness, called a **directional residual**.

## Question

Which distinctions do two presentations share? If one presentation loses a distinction made by the other, what must any repair preserve?

## What we already possess

The source uses `D : List Nat` and `p q : Nat → Nat`: a finite represented domain and numerical maps. This chapter does not claim the source theorem for arbitrary domain or codomain types.

From Unit 61:

- A **fiber** of `p` groups data with the same `p`-value.
- `FactorsOn D p q` means that **q can be recovered from p** on `D`.
- `FiberConstant D p q` means that equal `p`-values imply equal `q`-values on `D`. The theorem `factors_iff_fiberConstant` equates these conditions.
- `pQ D Q` chooses the first datum in `D` with the same answer signature. It returns a natural number, rather than the signature list itself.
- `classCount D Q` counts classes distinguished by a **list of questions** `Q`. For a single presentation, write `classCount D [p]`.

The argument order matters: `FactorsOn D p q` reads “q factors through p.”

## 1. Same distinctions in both directions

These are source definitions:

```lean
def FiberIdentityOn (D : List Nat) (p q : Nat → Nat) : Prop :=
  ∀ x, x ∈ D → ∀ y, y ∈ D → (p x = p y ↔ q x = q y)

def PresentationIdentityOn (D : List Nat) (p q : Nat → Nat) : Prop :=
  FactorsOn D p q ∧ FactorsOn D q p
```

`presentationIdentity_iff_fiberIdentity` says these conditions agree. This is equality of distinctions on `D`; it does not say `p` and `q` are equal functions or use equal labels.

Read the symbols one at a time: `∀` means “for every”; `∈ D` restricts data to the supplied list; `↔` means “if and only if”; and `∧` requires both conditions.

## 2. A failure comes with a pair

The source packages a failure witness as data:

```lean
structure DirectionalResidual
    (D : List Nat) (p q : Nat → Nat) where
  left : Nat
  right : Nat
  left_mem : left ∈ D
  right_mem : right ∈ D
  identified : p left = p right
  separated : q left ≠ q right
```

Read the last two fields first: `p` merges the pair and `q` separates it. The membership fields check that both data belong to the stated domain.

`ResidualEmptyOn D p q` requires absence of residuals **in both directions**. The theorem `presentationIdentity_iff_residualEmpty` equates this bilateral condition with presentation identity. Its proof uses the declared decidable comparisons and introduces no classical choice principle.

## 3. What a repair must do

Suppose `q` cannot be recovered from `p` on `D`. The theorem `forced_split_of_factorization_failure` finds `x, y ∈ D` with `p x = p y` and `q x ≠ q y`.

Every proposed presentation `r` that carries **both** old presentations must then satisfy:

1. `r x ≠ r y`: it separates that witnessing pair.
2. `classCount D [p] < classCount D [r]`: it has strictly more represented classes than `p`.

This necessity result does not choose `r`. A later theorem constructs one particular repair:

```lean
def jointPresentation
    (D : List Nat) (p q : Nat → Nat) : Nat → Nat :=
  pQ D [p, q]
```

It groups two data together only when they agree on both `p` and `q`. Its representative is the first matching datum in the supplied list. The theorem does not make that order preferred or invariant under every relabeling.

## 4. Symmetry and closure of this comparison

`ClosureSymmetry` turns a residual into `InternalSymmetryBreak D p q`. Its `transpose` swaps the two witnessing natural numbers **in the datum domain**. The old presentation `p` is unchanged by the swap on `D`; `q` changes at the witnessing point. This is a domain map, rather than an operation that merely reverses an ordered-pair record.

If `r` carries `q`, `ResidualClosure` shows that `r` must also change under that witnessing swap. If `r` carries `p` as well, its class count strictly increases over `p`.

The current directional residual from `r` to `q` is then empty: `¬ Nonempty (DirectionalResidual D r q)`. This means **q factors through r**. It does not assert the bilateral condition `ResidualEmptyOn D r q`, and leaves future comparisons with other maps open.

## Python: a small table example

This is Python (book), an illustration on three listed data. It tests fiber constancy directly. It is not a verbatim source definition or a replacement for the Lean theorem.

```python
D = (0, 1, 2)
p = (0, 0, 1)
q = (0, 1, 1)

def factors_on(source, target):
    return all(source[x] != source[y] or target[x] == target[y]
               for x in D for y in D)

joint_signature = tuple((p[x], q[x]) for x in D)
assert not factors_on(p, q)
assert factors_on(joint_signature, p)
assert factors_on(joint_signature, q)
assert len(set(p)) == 2
assert len(set(joint_signature)) == 3
```

Here `joint_signature` records pairs of values. Lean's `jointPresentation` instead returns first-match representative indices. They have the same fibers on this example; their output types differ.

## What has been proved

For the stated numerical maps on a supplied finite list:

- Mutual factorization, equal fiber relations, and bilateral residual emptiness are equivalent.
- Failed recovery has a witnessing pair. Any common refinement must split it and strictly increase the represented class count over `p`.
- A first-match joint refinement supplies one repair. Carrying `q` closes the current directional comparison against `q`.

The module also contains separately scoped examples involving operational support, certification panels, and declared generator profiles. Its `Metatheory` subsection studies ambient Boolean views; those views are not thereby admitted into the represented state.

## What has not been proved

This does not select a preferred repair or guarantee closure against future comparisons. It supplies no first presentation, physical interpretation, general heterogeneous-carrier theorem, or multi-step termination result. When `D` is empty, every map factors through every other, so the failed-recovery hypothesis cannot hold.

## Checks and source custody

`textbook/checks/u71_presentation_relativity.py` contains book computations. `textbook/checks/u71_lean.py` checks book examples against the source modules. Run them from the repository root after preparing the documented environment:

```text
python textbook/checks/u71_presentation_relativity.py
python textbook/checks/u71_lean.py
```

The audit records are `textbook/audit/modules/PresentationRelativity.md`, `textbook/audit/modules/ClosureSymmetry.md`, and `textbook/audit/modules/ResidualClosure.md`.

**Correction, 2026-10-28.** The previous lesson attributed generic `List X` domains, heterogeneous codomains, signature-list outputs, and a pair-record transpose to these source definitions. It also reversed the direction of factorization and confused unilateral with bilateral residual emptiness. The definitions above follow the numerical source interfaces; the sealed sources were not changed.

## Student exercise

On `D = [0, 1, 2]`, take `p = [0, 0, 1]` and `q = [0, 1, 1]`. Which pair witnesses failure of `FactorsOn D p q`? How many classes does the joint signature have? What table does the first-match `jointPresentation` return?

## Answer

The pair `0, 1` witnesses failure: both have `p`-value `0`, but their `q`-values are `0` and `1`. The signatures are `(0, 0)`, `(0, 1)`, and `(1, 1)`, giving three classes. Each first occurs at its own index, so the representative table is `[0, 1, 2]`.
