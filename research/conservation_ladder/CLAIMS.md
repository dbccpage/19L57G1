# Claims

AuthorityEffect: None.  Every Lean name below is in the
`ResearchConservationLadder` namespace and is reported in
`lean/ResearchConservationLadder/AxiomReport.lean`.  Each reports only
`propext` and `Quot.sound`, or no axiom.  Counts dated 2026-09-23.

**Classification of supplied structure.**  The following are declared by
this tree as metatheory apparatus or supplied data, and are not read off the
sealed seed or its difference relation:

- integer configurations;
- histories;
- the two-point weight and its action;
- admissible one-point variations;
- dual numbers;
- symmetry generators.

The vocabulary of charges, weights and generators is this tree's own
classified vocabulary.  It supplies no native derivation.

| Claim | Status | Statement | Evidence |
| --- | --- | --- | --- |
| CL-1 | PROVED_THEOREM | For every step function, a quantity preserved by every step is preserved along every actual-step path. | `conserved_path` |
| CL-2 | PROVED_THEOREM | Evaluating a polynomial expression over dual numbers returns its integer value and, as the dual coefficient, exactly its syntactic directional derivative. That derivative is linear in the direction. | `Expr.evalD_eq`, `Expr.ddir_zero`, `Expr.ddir_add`, `Expr.ddir_smul` |
| CL-3 | PROVED_THEOREM | For an interior point, the dual coefficient of the action of a history varied at that point is the left side of the stationarity equation. A history is stationary under all admissible variations at a point exactly when the stationarity equation holds there. | `action_variation`, `stationary_iff_variation` |
| CL-4 | PROVED_THEOREM | Invariance of a weight under a generator, stated as the vanishing of the dual coefficient along the generated flow, is the identity `D₁L·ξ(q₀) + D₂L·ξ(q₁) = 0`. | `invariant_iff_dual` |
| CL-5 | PROVED_THEOREM | **Conditional conservation.** If the weight is invariant under the generator and the history is stationary at a point, the charge `D₂L·ξ` is equal on the two edges at that point. Along a history stationary at every interior point, the charge is constant. | `charge_step`, `charge_const` |
| CL-6 | PROVED_THEOREM | The central weight `(x₁-x₀)² + (y₁-y₀)² - c(x₀²+y₀²)` is invariant under the rotation generator for every integer `c`. Its charge on the edge `(a, b)` is `2(a.x·b.y - a.y·b.x)`, which takes different values on different edges. The generated history `q_{k+1} = (2-c)q_k - q_{k-1}` is stationary at every interior point, so the charge is constant along it. | `d1_central`, `d2_central`, `central_invariant`, `central_charge`, `charge_nonconstant`, `solve_stationary`, `solve_charge_const` |
| CL-7 | PROVED_THEOREM | The generated history is a one-event step system on consecutive pairs. Its charge is preserved by that step and along every path of it. | `charge_tick`, `tick_path_charge` |
| CL-8 | REFUTED | "The charge is conserved without the symmetry." With the potential on the first coordinate only, the rotation generator is not a symmetry. Along that weight's own stationary history from `(1,0), (1,1)`, the charge changes from 2 to 4. | `aniso_not_invariant`, `aniso_next_stationary`, `aniso_charge_moves` |
| CL-9 | REFUTED | "The charge is conserved without the stationarity equation." On the non-stationary history `(0,0), (1,0), (1,1)`, the charge of the free weight changes. | `nonstationary_charge_moves` |
| CL-10 | REFUTED | "Every generator is a symmetry." The constant generator `(1, 0)` is a symmetry of the free weight (`c = 0`) and not of `c = 1`. | `shift_invariant_free`, `shift_not_invariant` |
| CL-11 | PROVED_THEOREM | On the sealed passage, a quantity preserved by every event takes the same value on a live state as on its budget and license variants and on its halted version. | `passage_conserved_blind` |
| CL-12 | VERIFIED_FINITE | Over a 25-point grid and coefficients -2 to 2: 9,375 dual evaluations are exact and match both closed-form derivatives. The central weight has no rotation-invariance failure on 625 pairs per coefficient, while the anisotropic weight fails on 400 of 625. On all 3,125 generated histories of eight points the charge is constant, and all 37,500 interior variations vanish. 576 of 625 anisotropic stationary histories carry a moving charge. 1,528 of 2,197 arbitrary three-point histories move the charge. | `evidence/receipt.json`, `tests/test_ladder.py` |
| CL-13 | OPEN | A symmetry and a charge of the sealed passage itself. The passage supplies no action, variation or one-parameter generator, and CL-11 bounds what any conserved quantity of it can see. | none |
| CL-14 | OPEN | The smooth tier: real configurations, differentiable weights, a one-parameter group action, and the specialization to a symplectic flow with its conserved map. By the author's choice on 2026-09-23 this tree uses no library of analysis; that tier needs a separate, explicitly approved package. | none |

Lean reach: only the declarations named in `TREE_CONTRACT.json`.  This is
not a census of every compiled constant.
