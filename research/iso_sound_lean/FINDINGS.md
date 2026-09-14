# Findings: CL-ISO-SOUND Lean Mechanization

`AuthorityEffect: None.`

## VERDICT
CONDITIONAL-ON-ORBIT-HYPOTHESES / ISO-PY-UNLINKED
Location: CARRIER (abstract orbit-choice lemmas on a toy $S(n)$ action).

### Summary
Lean 4 proves that *if* a map $C$ lands in each orbit (`InOrbitChoice`), then $C(r_1)=C(r_2)$ implies $r_1 \cong r_2$ (`cl_iso_sound`). The converse (`cl_iso_complete`) additionally requires orbit-invariance of $C$. The paper-ledger claim `CL-ISO-SOUND` for `code/derivation/iso.py` remains OPEN: this tree does not show that the individualization-refinement canonical selector inhabits those hypotheses.

Python `witness_inversion.py` extracts $\pi = \pi_2^{*-1} \circ \pi_1^*$ once the canonicalizing permutations are given. That is a group-action identity, not a proof that `iso.py` supplies those permutations.

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
- A countermodel to `cl_iso_sound` under `InOrbitChoice` (equal representatives, non-isomorphic regimes).
- An axiom leakage beyond `{propext, Quot.sound}` in the Lean 4 formalization.
- A Lean inhabitant showing `iso.py`'s `canonical` satisfies `InOrbitChoice` and `OrbitInvariant` on the sealed carrier — that would be the missing link to `CL-ISO-SOUND`, not a refutation of the lemmas already proved.

---

## CLAIM HYGIENE SUMMARY
1. **What it supports**: Under `InOrbitChoice`, equal representatives imply `Iso`. Under that plus `OrbitInvariant`, representative equality classifies `Iso` on the toy $S(n)$ carrier defined in `RegimeAction.lean`.
2. **What it does not support**: It does not close `CL-ISO-SOUND` for `code/derivation/iso.py`. It does not prove that individualization-refinement is an `OrbitMinimizer`. $C = \mathrm{id}$ is `InOrbitChoice` and is not complete. The witness $\pi_2^{-1}\circ\pi_1$ needs the concrete canonicalizing permutations, not mere orbit membership.
3. **The narrowest defensible claim**: On this carrier, `InOrbitChoice` gives $C(r_1)=C(r_2)\implies r_1\cong r_2$; adding `OrbitInvariant` gives the converse. Linking those hypotheses to `iso.py` is OPEN.
4. **The next test needed**: Exhibit `iso.py`'s `canonical` / `canonical_witness` as an inhabitant of `InOrbitChoice` and `OrbitInvariant` on the sealed regime type, or keep `CL-ISO-SOUND` OPEN.

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
