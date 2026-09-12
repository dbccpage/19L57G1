# Target X301: Formal Semantics, Empirical Reference & Intervention Grounding

## Overview

Target X301 formalizes and implements an internal operational semantics where empirical reference
is grounded in executable counterfactual state perturbations rather than multi-observer committee consensus.
It embodies the foundational architectural principle: **"Panel agreement is not truth."**

When a panel of independent observers evaluating partial or coarse projections unanimously certifies an
assertion that is refuted by ground carrier reality or counterfactual intervention, the **Grounding Firewall**
overrides committee consensus, emits an immutable, byte-pinned `PanelIllusionReceipt` (SHA-256), and triggers
a typed refusal `StepResult.refusal`, preserving the carrier state strictly unmutated.

## Architecture

```text
research/x301_formal_semantics/
├── README.md               # Architecture, specification, and usage documentation
├── CLAIMS.md               # Reconciled claims ledger (Claim Hygiene compliant)
├── pyproject.toml          # Package configuration and pytest settings
├── valuation.py / formulas.py / model.py / isomorphism.py / intervention.py / panel.py
├── semantics.py            # Thin re-export of the split kernels
├── tests/                  # Verification test suite (satisfaction, invariance, firewall)
├── lean/                   # Constructive Core Lean 4 formalization
│   ├── lakefile.toml       # Lake package configuration
│   ├── lean-toolchain      # Pinned to leanprover/lean4:v4.33.0
│   ├── FormalSemantics.lean# Constructive Lean 4 proofs
│   └── Inventory.lean      # Theorem census and axiom audit
└── evidence/               # Signed cryptographic verification receipts
```

## Key Components

1. **Exact Rational Heyting Truth Structure**:
   - Valuations in $[0, 1] \cap \mathbb{Q}$ using exact rational arithmetic (`Fraction`), eliminating floating point imprecision.
   - Poset operations: meet ($\min$), join ($\max$), Heyting implication ($a \to b = 1$ if $a \le b$ else $b$), and pseudo-complement ($\neg a = a \to 0$).

2. **Operational Formula AST**:
   - `Atom(rel, args)`: Atomic relation assertion over relational carrier.
   - `Identity(left, right)`: Internal identity statement.
   - `Conj(left, right)`: Conjunction via meet.
   - `Disj(left, right)`: Disjunction via join.
   - `Imp(ant, con)`: Intuitionistic implication.
   - `Neg(inner)`: Operational refusal / constructive negation.
   - `BoundedForall(var, sort, body)`: Bounded universal quantification over finite sort domains.
   - `BoundedExists(var, sort, body)`: Bounded existential quantification over finite sort domains.

3. **Relational Carrier Model**:
   - 5-partition relational carrier state $(data, forms, insts, rules, reqs)$ compatible with `code/derivation/model.py` (`Regime`) and `research/g012_typed_translation/codec.py` (`RelationalState`).
   - Positive derivability readout: $inst \in insts \lor form \in rules$.

4. **Signature Transport & Canonical Isomorphism Invariance**:
   - Pushforward $\tau_*(M)$ and formula renaming $\tau(\phi)$ under isomorphism $\tau = (\pi, \phi)$.
   - Commutation verification: $M, \sigma \models \phi \iff \tau_*(M), \tau(\sigma) \models \tau(\phi)$.
   - Verified across all Challenge-3 Reading L classes ($U_0, BL, BD$) and Reading F classes ($\text{MarkF}, \text{DiagF}, \text{LinkF}, \text{OutF}, \text{InF}$) with their respective transposition swap representatives.

5. **Executable Interventions & Empirical Reference**:
   - Explicit state perturbations $I: S \to S$ (`add_instance`, `remove_instance`, `add_requirement`, `toggle_rule`).
   - An assertion possesses empirical reference iff an admissible intervention sequence discriminates it: $\mathcal{V}(M, \phi) \neq \mathcal{V}(I(M), \phi)$.
   - Behavioral congruence ($\phi \equiv_{\text{obs}} \psi$): rejecting ungrounded decorative distinctions lacking intervention witnesses.

6. **Multi-Observer Panel Protocol & Grounding Firewall**:
   - `Observer(id, projection_fn)`: Evaluates assertions through restricted or coarse projection views.
   - `Panel(observers)`: Aggregates $N \ge 3$ independent observers to compute unanimous consensus.
   - `GroundingFirewall`: Prioritizes ground intervention refutation over unanimous committee agreement.
   - `PanelIllusionReceipt`: Byte-pinned receipt recording observer IDs, false consensus, discriminating intervention, and canonical SHA-256 digest.
   - `StepResult.refusal`: Typed refusal preserving carrier state strictly intact without mutation.

## Usage Example

```python
from semantics import (
    RelationalModel, atom, evaluate, Observer, Panel,
    remove_instance_intervention, evaluate_with_grounding_firewall,
)

# 1. Carrier state with form 0 marking datum 0
model = RelationalModel(
    data=("d0", "d1"),
    forms=(1,),
    insts=frozenset({(0, (0,))}),
    reqs=frozenset({(0, 1)}),
)

# 2. Candidate assertion: form 0 marks datum 1 (False on carrier)
phi = atom("0", "1")

# 3. Panel of 3 observers with coarse projections creating false consensus
def coarse_view(m):
    return RelationalModel(m.data, m.forms, m.insts | {(0, (1,))}, m.rules, m.reqs)

obs = [Observer(f"obs_{i}", coarse_view) for i in range(3)]
panel = Panel(obs)

# 4. Grounding Firewall execution
result = evaluate_with_grounding_firewall(
    model=model,
    formula=phi,
    panel=panel,
    candidate_interventions=[remove_instance_intervention(0, (0,))],
)

# 5. Committee agreement refuted: typed refusal emitted, state preserved unmutated
assert result.is_refusal
assert result.state == model  # Carrier state strictly unmutated
print("Receipt SHA-256:", result.receipt.receipt_sha256)
```

## Vocabulary & Claim Hygiene Compliance

- **Prose Watchlist**: Zero occurrences of watched vocabulary terms. The valuation structure is designated strictly as a `poset`, `Heyting truth structure`, `truth algebra`, or `valuation domain`.
- **Claim Hygiene Rule**: Scoped to finitary relational carriers and declared candidate intervention spaces. No ungrounded generalizations or hyperbolic claims.
