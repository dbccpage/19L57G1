# Claims Ledger: Target X301 (Formal Semantics, Empirical Reference & Intervention Grounding)

## 1. What it supports

1. **Compositional Semantic Interpretation**:
   Supports an internal compositional semantics mapping operational formulas over a 5-partition relational carrier to an exact rational Heyting truth structure (poset) in $[0, 1] \cap \mathbb{Q}$ without consulting external host oracles.

2. **Signature Transport & Canonical Isomorphism Invariance**:
   Demonstrates in this setting semantic truth invariance under signature transport and canonical isomorphism ($M \models \phi \iff \tau_*(M) \models \tau(\phi)$) across all 3 Challenge-3 canonical classes under Reading L ($U_0, BL, BD$) and all 5 canonical classes under Reading F ($\text{MarkF}, \text{DiagF}, \text{LinkF}, \text{OutF}, \text{InF}$).

3. **Intervention-Linked Grounding & Empirical Reference**:
   Supports operational empirical reference grounded in executable state perturbations ($I: S \to S$), establishing that an assertion possesses empirical reference if and only if there exists a counterfactual intervention whose observable readout discriminates it.

4. **Behavioral Observational Congruence**:
   Demonstrates in this model that indistinguishable assertions across all admissible carrier interventions satisfy behavioral congruence ($\phi \equiv_{\text{obs}} \psi$), identifying ungrounded decorative distinctions.

5. **Demarcation of Multi-Observer Consensus and Empirical Truth ("Panel agreement is not truth")**:
   Demonstrates that a committee panel of $N \ge 3$ independent observers voting under coarse or defective projections can form unanimous consensus on an assertion that is refuted by the ground carrier state.

6. **Grounding Firewall & Typed Refusal**:
   Supports the Grounding Firewall: when unanimous panel consensus holds for an assertion that is refuted by ground carrier reality or counterfactual intervention, the engine overrides panel agreement, emits a cryptographically-pinned `PanelIllusionReceipt` (SHA-256), and triggers typed refusal `StepResult.refusal`, preserving the carrier state strictly unmutated.

## 2. What it does not support

1. Does not support infinite relational carrier domains or unbounded first-order quantification; all carrier domains and quantifiers are finitary.
2. Does not describe toy tests as comprehensive empirical studies of production AI systems or general human committee dynamics.
3. Does not support non-constructive classical principles requiring unrestricted choice or excluded middle on infinite collections.
4. Does not claim automated synthesis of arbitrary empirical ground truths without supplied executable intervention operators.

## 3. The narrowest defensible claim

Within the declared finitary relational carrier and candidate intervention space, unanimous agreement among $N \ge 3$ panel observers evaluating coarse projections is insufficient to establish empirical truth and is overridden by localized counterfactual carrier interventions, halting execution via state-preserving typed refusal and emitting an immutable cryptographic receipt.

## 4. The next test needed

Constructively link the Python semantics engine's Grounding Firewall with the Lean 4 formalization in `research/x301_formal_semantics/lean/FormalSemantics.lean`, verifying that the Lean theorem `grounding_firewall_refuses_panel_illusion` holds under axioms strictly within `{propext, Quot.sound}`.
