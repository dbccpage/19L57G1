# Claims Ledger: Stabilizer Error-Correcting Codes on Affine Grids (Target P209c)

This ledger documents the formal mathematical and computational claims established by `research/p209c_stabilizer_codes/` under constructive core Lean 4 and exact Python implementations.

Evidence boundary: Lean proves explicit Pauli-string and syndrome equalities,
ending with seven X-error syndrome evaluations. Codespace dimensions, distance,
decoding, and projector statements below are Python calculations for named
finite examples unless an exact Lean theorem is individually cited.

AuthorityEffect: None.
Axiom Scope: Strictly contained within `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## CL-P209C-01: Three-Carrier Bit-Flip Code [[3, 1, 1]]

- **Statement**: On a 3-carrier discrete carrier space, the stabilizer operators $S_1 = ZZI$ and $S_2 = IZZ$ commute identically. The logical operators $Z_L = ZZZ$ and $X_L = XXX$ commute with both stabilizers, while $X_L$ and $Z_L$ mutually anticommute on the encoded subspace. Single bit-flip errors generate four distinct syndrome pairs, enabling deterministic identification of each single bit-flip.
- **Formal Theorems**:
  - `P209cStabilizerCodes.bitflip_s1_comm_s2`
  - `P209cStabilizerCodes.bitflip_xl_comm_s1`
  - `P209cStabilizerCodes.bitflip_xl_comm_s2`
  - `P209cStabilizerCodes.bitflip_zl_comm_s1`
  - `P209cStabilizerCodes.bitflip_zl_comm_s2`
  - `P209cStabilizerCodes.bitflip_xl_anticomm_zl`
  - `P209cStabilizerCodes.syndrome3_i` through `syndrome3_x3`
  - `P209cStabilizerCodes.syndrome3_dist_0_1` through `syndrome3_dist_2_3`
- **Axiom Status**: Strictly within `{propext}` (zero choice).
- **Evidence Paths**:
  - `research/p209c_stabilizer_codes/lean/StabilizerCodes.lean`
  - `research/p209c_stabilizer_codes/stabilizer_codes.py`
  - `research/p209c_stabilizer_codes/tests/test_stabilizer.py`
- **Claim Discipline**:
  1. *What it supports*: Lean checks the named commutations and syndrome signatures; the codespace dimension is a separate Python calculation.
  2. *What it does not support*: Does not protect against single-carrier sign-flip ($Z$) errors or arbitrary composite noise channels.
  3. *Narrowest defensible claim*: For the discrete Pauli string algebra on 3 carriers, $S_1 = ZZI$ and $S_2 = IZZ$ yield four pairwise distinct syndrome pairs over $\{I, X_1, X_2, X_3\}$.
  4. *Next test needed*: Concatenation with a 3-carrier sign-flip code to construct the 9-carrier Shor code architecture.

---

## CL-P209C-02: Four-Carrier CSS Torus Code [[4, 2, 2]]

- **Statement**: On a discrete 2-torus represented by 4 state carriers, the dual stabilizers $S_Z = ZZZZ$ and $S_X = XXXX$ commute identically ($(-1)^4 = +1$). The codespace encodes two independent logical carriers with operators $(Z_{L1} = ZZII, X_{L1} = XIXI)$ and $(Z_{L2} = ZIZI, X_{L2} = XXII)$, and all 12 single-carrier Pauli errors produce non-trivial syndrome pairs, establishing code distance 2.
- **Formal Theorems**:
  - `P209cStabilizerCodes.torus_sz_comm_sx`
  - `P209cStabilizerCodes.torus_zl1_comm_sz`
  - `P209cStabilizerCodes.torus_zl1_comm_sx`
  - `P209cStabilizerCodes.torus_xl1_comm_sz`
  - `P209cStabilizerCodes.torus_xl1_comm_sx`
  - `P209cStabilizerCodes.torus_zl2_comm_sz`
  - `P209cStabilizerCodes.torus_zl2_comm_sx`
  - `P209cStabilizerCodes.torus_xl2_comm_sz`
  - `P209cStabilizerCodes.torus_xl2_comm_sx`
  - `P209cStabilizerCodes.torus_xl1_anticomm_zl1`
  - `P209cStabilizerCodes.torus_xl2_anticomm_zl2`
  - `P209cStabilizerCodes.torus_xl1_comm_xl2`
  - `P209cStabilizerCodes.torus_zl1_comm_zl2`
  - `P209cStabilizerCodes.torus_xl1_comm_zl2`
  - `P209cStabilizerCodes.torus_xl2_comm_zl1`
  - `P209cStabilizerCodes.torus_detect_x0` through `torus_detect_z3`
  - `P209cStabilizerCodes.torus_distance2_detected`
- **Axiom Status**: Strictly within `{propext}` (zero choice).
- **Evidence Paths**:
  - `research/p209c_stabilizer_codes/lean/StabilizerCodes.lean`
  - `research/p209c_stabilizer_codes/stabilizer_codes.py`
  - `research/p209c_stabilizer_codes/tests/test_stabilizer.py`
- **Claim Discipline**:
  1. *What it supports*: Lean checks selected explicit commutations and Python checks the named four-carrier error-detection example; no general Lean distance theorem is cited.
  2. *What it does not support*: Does not support deterministic correction of weight-1 errors, as syndromes identify error type ($X, Z, Y$) rather than carrier locus.
  3. *Narrowest defensible claim*: For $S_Z = Z^{\otimes 4}$ and $S_X = X^{\otimes 4}$, all 12 single-carrier Pauli operators have syndrome $(s_Z, s_X) \neq (0, 0)$.
  4. *Next test needed*: Surface code extensions on $L \times L$ planar discrete grids with boundary boundaries.

---

## CL-P209C-03: Steane [[7, 1, 3]] CSS Code on Fano Plane Geometry

- **Statement**: The 7 state carriers assigned to the points of the finite projective plane $PG(2, 2)$ (the Fano plane) admit 6 stabilizer generators derived from 3 dual lines of weight 4. The dual lines exhibit pairwise even intersection cardinalities ($|h_i \cap h_j| = 2 \equiv 0 \pmod 2$), ensuring mutual commutativity across all 15 generator pairs.
- **Formal Theorems**:
  - `P209cStabilizerCodes.fano_h1_weight` through `fano_h3_weight`
  - `P209cStabilizerCodes.fano_inter_h1_h2` through `fano_inter_h2_h3`
  - `P209cStabilizerCodes.steane_comm_mx1_mx2` through `steane_comm_mz3_mx3` (15 commutations)
  - `P209cStabilizerCodes.steane_xl_comm_mz1` through `steane_zl_comm_mx3` (12 commutations)
  - `P209cStabilizerCodes.steane_xl_anticomm_zl`
- **Axiom Status**: Strictly within `{propext}` (zero choice).
- **Evidence Paths**:
  - `research/p209c_stabilizer_codes/lean/StabilizerCodes.lean`
  - `research/p209c_stabilizer_codes/stabilizer_codes.py`
  - `research/p209c_stabilizer_codes/tests/test_stabilizer.py`
- **Claim Discipline**:
  1. *What it supports*: Demonstrates that the incidence geometry of $PG(2, 2)$ dual lines constructs an abelian group of 6 commuting Pauli strings encoding 1 logical carrier into 7 physical carriers.
  2. *What it does not support*: Does not establish fault-tolerant thresholds under correlated or non-Markovian noise.
  3. *Narrowest defensible claim*: Dual lines of $PG(2, 2)$ have size 4 and pairwise intersection 2, and the corresponding 6 Pauli operators commute pairwise.
  4. *Next test needed*: Generalized Reed-Muller and affine geometry code constructions $AG(m, 2)$.

---

## CL-P209C-04: Transversal Hadamard Gate Preservation

- **Statement**: Transversal application of the Hadamard operational step $H^{\otimes 7}$ preserves the Steane [[7, 1, 3]] stabilizer group setwise by mapping each $X$-generator to its corresponding $Z$-generator ($M_{Xi} \mapsto M_{Zi}$, $M_{Zi} \mapsto M_{Xi}$) and implements logical Hadamard conjugation $H_L$ by interchanging logical $X_L \leftrightarrow Z_L$.
- **Formal Theorems**:
  - `P209cStabilizerCodes.steane_hadamard_mx1` through `steane_hadamard_mz3`
  - `P209cStabilizerCodes.steane_hadamard_xl`
  - `P209cStabilizerCodes.steane_hadamard_zl`
- **Axiom Status**: Zero axioms (definitional equality `rfl`).
- **Evidence Paths**:
  - `research/p209c_stabilizer_codes/lean/StabilizerCodes.lean`
  - `research/p209c_stabilizer_codes/stabilizer_codes.py`
  - `research/p209c_stabilizer_codes/tests/test_stabilizer.py`
- **Claim Discipline**:
  1. *What it supports*: Confirms that transversal single-carrier operations leave the codespace invariant while implementing logical non-trivial operations.
  2. *What it does not support*: Does not show that non-Clifford operations (such as the $T$ gate) can be implemented transversally on the Steane code.
  3. *Narrowest defensible claim*: Under $H^{\otimes 7}$, $M_{Xi} \mapsto M_{Zi}$, $M_{Zi} \mapsto M_{Xi}$, $X_L \mapsto Z_L$, and $Z_L \mapsto X_L$ holds by definition.
  4. *Next test needed*: Verification of the Eastin-Knill restriction across discrete stabilizer code families.

---

## CL-P209C-05: Deterministic Single-Carrier Error Diagnosis and Correction

- **Statement**: The Steane code syndrome mapping $(s_Z, s_X) \in \mathbb{F}_2^3 \times \mathbb{F}_2^3$ assigns a distinct non-zero syndrome to each of the 21 single-carrier Pauli errors ($7 \times X, 7 \times Z, 7 \times Y$). Applying the diagnosed recovery operator deterministically returns the corrupted carrier state to the codespace.
- **Formal Theorems**:
  - `P209cStabilizerCodes.steane_syn_x0` through `steane_syn_x6`
- **Evidence Paths**:
  - `research/p209c_stabilizer_codes/lean/StabilizerCodes.lean`
  - `research/p209c_stabilizer_codes/stabilizer_codes.py`
  - `research/p209c_stabilizer_codes/tests/test_stabilizer.py`
- **Claim Discipline**:
  1. *What it supports*: Python checks the declared finite correction examples; Lean evaluates seven explicit X-error syndromes only.
  2. *What it does not support*: Does not protect against weight-2 or higher errors, which can mimic weight-1 errors or act as non-trivial logical operators.
  3. *Narrowest defensible claim*: In Lean, the seven named X errors have the displayed syndrome values. The 21-error lookup and recovery are Python-level results for the named code.
  4. *Next test needed*: Minimum-weight perfect matching decoding for higher-distance surface geometries.

---

## CL-P209C-06: Exact Stabilizer Projection Operator Idempotence

- **Statement**: For the three explicitly evaluated Python groups, the unnormalized operator sum $K_S$ satisfies the checked matrix identity $K_S^2 = |S|K_S$, with the reported traces. No universal projector theorem is implemented in Lean here.
- **Evidence Paths**:
  - `research/p209c_stabilizer_codes/stabilizer_codes.py`
  - `research/p209c_stabilizer_codes/tests/test_stabilizer.py`
- **Claim Discipline**:
  1. *What it supports*: Verifies exact integer matrix idempotence $K_S^2 = |S| \cdot K_S$ for [[3, 1, 1]], [[4, 2, 2]], and [[7, 1, 3]] stabilizer codes.
  2. *What it does not support*: Does not address infinite-dimensional projection operators or continuous carrier fields.
  3. *Narrowest defensible claim*: For the evaluated codes, $K_S^2 = |S| \cdot K_S$ holds with zero numerical difference, giving codespace dimensions 2, 4, and 2 respectively.
  4. *Next test needed*: Construction of stabilizer projectors for subsystem and operator codes on discrete affine grids.
