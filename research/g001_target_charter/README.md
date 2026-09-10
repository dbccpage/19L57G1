# G001: TOE Target-Class Charter

## Overview

The G001 package establishes a pre-registered, independent target-class charter
specifying what constitutes adequacy for candidate Theory of Everything (TOE)
formal systems before candidate evaluation begins.

This package defines 9 independent adequacy criteria, their 4-way dimension
partition, an evaluation engine that evaluates candidate systems without retrospective
target shifting, and functorial comparison morphisms with identity and associative
composition laws.

## Nine Frozen Adequacy Criteria

The 9 independent criteria are pre-registered and frozen under status
`TOE_TARGET_CLASS_FROZEN` prior to candidate evaluation:

1. **Computational capacity criteria**: discrete state transition simulation, fuel and step accounting, and termination or progress detection.
2. **Reasoning adequacy**: explicit deduction tracking with separation between operational refusal and logical falsehood.
3. **Representational and operational completeness**: operations driven by stored carrier representations without unencoded host function calls or silent scheduler selection.
4. **Mathematical foundation recovery**: constructive recovery of discrete mathematical structures without non-constructive shortcuts.
5. **Physical adequacy**: embedded observer boundaries, causal locality across independent loci, and monotone resource accounting.
6. **Empirical adequacy**: finite observational resolution, rational frequency readouts, and quantitative error bounds.
7. **Calculus uniqueness**: presentation invariance under representation isomorphism and minimal primitive bases.
8. **Physical-model uniqueness**: prospective discriminating experiments breaking observational bisimulation between rival models.
9. **Comparison morphisms**: functorial comparison morphisms between target systems preserving adequacy structures with bounded distortion metrics.

## Categorical Comparison Morphisms

Candidate target systems form objects in a category whose arrows are `ComparisonMorphism` records:
- `idMorphism`: Identity morphism on a target system.
- `compMorphism`: Associative composition of morphisms.
- Category laws: `id_comp`, `comp_id`, and `comp_assoc` are formalized constructively in Lean 4 without additional axioms.
- Adequacy preservation: Theorems establish that morphisms preserving faithful observation or state injectivity transfer adequacy properties between candidate systems.

## Constructive Formalization & Axiom Boundary

All formal theorems in `lean/` are verified constructively:
- `#print axioms` strictly within `{propext, Quot.sound}`.
- Zero reliance on `Classical.choice`.
- Zero reliance on external `mathlib` components.
- An environment theorem census (`Inventory.lean`) enumerates all compiled declarations across `Charter`, `Adequacy`, and `Morphism` namespaces.

## Verification

To run verification locally:
```powershell
python verify.py --write
```
This executes:
1. Python unit and property tests via pytest.
2. Lean 4 package build via Lake.
3. Metaprogrammed theorem census matching all `#print axioms` reports.
4. Claim hygiene verification scan.
5. Emits machine-readable evidence to `evidence/receipt.json`.

## Artifact Assessment

1. **What it supports**:
   - Supports pre-registering 9 independent adequacy criteria before candidate evaluation.
   - Supports detecting and refusing circular self-definition and unencoded host oracles.
   - Supports constructive representation of candidate systems, 4-way adequacy predicates, and category laws for comparison morphisms within the strict constructive axiom boundary `{propext, Quot.sound}`.

2. **What it does not support**:
   - Does not establish that any existing sub-system is a complete Theory of Everything.
   - Does not claim global physical closure or real continuum derivation.
   - Does not replace empirical measurement with mathematical definitions.

3. **Narrowest defensible claim**:
   The 9 criteria and comparison morphism category specify an independent, non-retrospective evaluation framework under which candidate systems can be evaluated and compared without post-hoc target adjustments.

4. **Next test needed**:
   Evaluate candidate systems from Target A and Target B against the frozen charter and measure adequacy preservation along explicit comparison morphisms.
