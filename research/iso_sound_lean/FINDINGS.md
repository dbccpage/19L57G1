# Findings: CL-ISO-SOUND Lean Mechanization

`AuthorityEffect: None.`

## VERDICT
CLOSED / MECHANIZED under declared group-action assumptions.
Location: CARRIER (Orbit Minimization & Constructive Witness Inversion).

### Summary
The custody gap `CL-ISO-SOUND` (`canonical(r_1) = canonical(r_2) → r_1 ≅ r_2`), left open as an empirical observation across 338,650 bounded regimes in `research/iso_sound/`, is mechanized in Lean 4 under declared group-action and orbit-choice assumptions without reliance on empirical hunts or external oracles.

The mathematical mechanism: the Lean formalization proves that for any canonical selector satisfying `InOrbitChoice`, representative equality yields structural isomorphism via constructive witness extraction. In Python, `witness_inversion.py` implements the constructive composite permutation witness inversion $\pi = \pi_2^{*-1} \circ \pi_1^*$, $\phi = \phi_2^{*-1} \circ \phi_1^*$. (The equivalence of the concrete Python partition refinement search in `code/derivation/iso.py` to `InOrbitChoice` remains an empirical/implementation connection and an open target for end-to-end AST mechanization).

---

## THE SOUNDNESS THEOREM
In `research/iso_sound_lean/lean/CanonicalMinimizer.lean`:

1. **Orbit-Choice Specification (`InOrbitChoice` & `OrbitInvariant`)**:
   A canonical form algorithm $C : \text{Regime} \to \text{Regime}$ is an orbit-choice selector if for every $r$, $C(r) \in S(n) \cdot r$ and $r_1 \cong r_2 \implies C(r_1) = C(r_2)$.

2. **Soundness (`cl_iso_sound`)**:
   Under any orbit-choice canonical selector $C$:
   $$\forall r_1\ r_2,\ C(r_1) = C(r_2) \implies r_1 \cong r_2$$

3. **Biconditional Canonical Classification (`canonical_classification`)**:
   $$\forall r_1\ r_2,\ C(r_1) = C(r_2) \iff r_1 \cong r_2$$

4. **Key-Valued Serialization Soundness (`key_soundness`)**:
   When serialized keys factor injectively through canonical regimes, identical serialization keys certify structural isomorphism:
   $$\forall r_1\ r_2,\ K(r_1) = K(r_2) \implies r_1 \cong r_2$$

---

## THE CONSTRUCTIVE WITNESS
In `research/iso_sound_lean/python/witness_inversion.py`:

Given two regimes $r_1, r_2$ where $\text{canonical}(r_1) == \text{canonical}(r_2)$, let $(\pi_1^*, \phi_1^*)$ and $(\pi_2^*, \phi_2^*)$ be the canonicalizing permutations returned by `canonical_witness`. The witness:
$$\pi = \pi_2^{*-1} \circ \pi_1^*, \quad \phi = \phi_2^{*-1} \circ \phi_1^*$$
is extracted and verified directly in `verify_isomorphism(r_1, r_2, \pi, \phi)`.

---

## WHAT WOULD HAVE CHANGED OUR MIND
- Finding a pair of non-isomorphic regimes $(r_1, r_2)$ that produced identical canonical keys in `iso.py`.
- Demonstrating that the individualization-refinement search tree terminates at a non-orbit-invariant branch choice.
- An axiom leakage beyond `{propext, Quot.sound}` in the Lean 4 formalization.

---

## CLAIM HYGIENE SUMMARY
1. **What it supports**: It supports the claim that canonical form equality in this individualization-refinement setting is sound and complete for structural isomorphism under finite permutation actions.
2. **What it does not support**: It does not support polynomial-time isomorphism testing for general graphs, nor does it support claims about systems with unquotiented infinite presentations.
3. **The narrowest defensible claim**: For finite regimes under finite symmetric group actions $S(n)$, any canonical selector choosing a representative in the group orbit satisfies $C(r_1) = C(r_2) \iff r_1 \cong r_2$, and the witness $\pi_2^{-1} \circ \pi_1$ maps $r_1$ to $r_2$.
4. **The next test needed**: Formalize the polynomial termination bound of the equitable partition refinement engine in Lean 4.

---

## LEDGER

| Theorem | File | Type | Axioms |
| :--- | :--- | :--- | :--- |
| `IsoSoundLean.Perm.ext` | `Permutation.lean` | Extensionality of permutations | `[Quot.sound]` |
| `IsoSoundLean.Perm.id_comp` | `Permutation.lean` | Identity composition | `[Quot.sound]` |
| `IsoSoundLean.Perm.comp_id` | `Permutation.lean` | Identity composition | `[Quot.sound]` |
| `IsoSoundLean.Perm.comp_assoc` | `Permutation.lean` | Associativity | `[Quot.sound]` |
| `IsoSoundLean.Perm.comp_left_inv` | `Permutation.lean` | Left inverse | `[Quot.sound]` |
| `IsoSoundLean.Perm.comp_right_inv` | `Permutation.lean` | Right inverse | `[Quot.sound]` |
| `IsoSoundLean.Perm.inv_id` | `Permutation.lean` | Inverse of identity | `[Quot.sound]` |
| `IsoSoundLean.Perm.inv_inv` | `Permutation.lean` | Double inverse | `[Quot.sound]` |
| `IsoSoundLean.Perm.inv_comp` | `Permutation.lean` | Antiautomorphism of inverse | `[Quot.sound]` |
| `IsoSoundLean.inv_act_act` | `RegimeAction.lean` | Action inverse cancellation | `[Quot.sound]` |
| `IsoSoundLean.act_inv_act` | `RegimeAction.lean` | Action inverse cancellation | `[Quot.sound]` |
| `IsoSoundLean.act_inj` | `RegimeAction.lean` | Action injectivity | `[Quot.sound]` |
| `IsoSoundLean.act_eq_iff` | `RegimeAction.lean` | Action equation equivalence | `[Quot.sound]` |
| `IsoSoundLean.iso_refl` | `RegimeAction.lean` | Reflexivity of isomorphism | `[]` |
| `IsoSoundLean.iso_symm` | `RegimeAction.lean` | Symmetry of isomorphism | `[Quot.sound]` |
| `IsoSoundLean.iso_trans` | `RegimeAction.lean` | Transitivity of isomorphism | `[]` |
| `IsoSoundLean.mem_orbit_iff` | `RegimeAction.lean` | Orbit membership condition | `[]` |
| `IsoSoundLean.iso_iff_same_orbit` | `RegimeAction.lean` | Orbit-isomorphism equivalence | `[Quot.sound]` |
| `IsoSoundLean.witness_extract` | `CanonicalMinimizer.lean` | Inverted composition witness | `[Quot.sound]` |
| `IsoSoundLean.iso_witness_of_orbit_choice` | `CanonicalMinimizer.lean` | Constructive witness from orbit choice | `[Quot.sound]` |
| `IsoSoundLean.cl_iso_sound` | `CanonicalMinimizer.lean` | General soundness `CL-ISO-SOUND` | `[Quot.sound]` |
| `IsoSoundLean.cl_iso_complete` | `CanonicalMinimizer.lean` | Completeness `CL-ISO-COMPLETE` | `[]` |
| `IsoSoundLean.canonical_classification` | `CanonicalMinimizer.lean` | Biconditional classification | `[Quot.sound]` |
| `IsoSoundLean.key_soundness` | `CanonicalMinimizer.lean` | Key serialization soundness | `[Quot.sound]` |
| `IsoSoundLean.key_classification` | `CanonicalMinimizer.lean` | Key serialization classification | `[Quot.sound]` |
| `IsoSoundLean.equivariant_search_same_image` | `CanonicalMinimizer.lean` | Equivariant search invariance | `[propext, Quot.sound]` |
| `IsoSoundLean.minimizer_isomorphism_sound` | `CanonicalMinimizer.lean` | Minimizer soundness | `[Quot.sound]` |
