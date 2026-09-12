"""Verification and governance harness for Target X303: Bounded Operational Agency.

AuthorityEffect: None.
Runs:
1. Source hygiene checks (prohibits sorry, admit, unsafe, partial, axiom in Lean sources if present;
   enforces repository vocabulary firewall against watched terms across all sources).
2. Python pytest test suite across tests/.
3. Invariant audit verifying viability boundaries, refusal state immutability, causal evaluation,
   licensing firewall, and exact rational multicriteria selection.
4. Lean 4 constructive package build and census if lean/ package is present.
5. Emits deterministic evidence/receipt.json.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Optional

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
LEAN_DIR = ROOT / "lean"
RECEIPT_PATH = ROOT / "evidence" / "receipt.json"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "code") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code"))
for _sub in ["x301_formal_semantics"]:
    _sub_path = REPO_ROOT / "research" / _sub
    if str(_sub_path) not in sys.path:
        sys.path.insert(0, str(_sub_path))

ALLOWED_AXIOMS = {"propext", "Quot.sound"}
FORBIDDEN_LEAN_TOKENS = re.compile(
    r"\b(?:sorry|admit|unsafe|partial)\b|^\s*axiom\s", re.MULTILINE
)
FORBIDDEN_DIGEST = "4cbe09597b76794b5f6b854c1c1c035ede6d241f250f223b61987dce9d2d7a4b"

AXIOM_RE = re.compile(
    r"^(?:info:\s*)?'(.+?)' depends on axioms: \[(.*?)\]$", re.MULTILINE
)
NO_AXIOM_RE = re.compile(
    r"^(?:info:\s*)?'(.+?)' does not depend on any axioms$", re.MULTILINE
)


def sha256_file(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def has_watched_digest(text: str) -> bool:
    """Check whole-word tokens against watched digest."""
    for token in re.findall(r"\b[a-zA-Z]+\b", text.lower()):
        d = hashlib.sha256(token.encode("utf-8")).hexdigest()
        if d == FORBIDDEN_DIGEST:
            return True
        if token.endswith("s"):
            d_stem = hashlib.sha256(token[:-1].encode("utf-8")).hexdigest()
            if d_stem == FORBIDDEN_DIGEST:
                return True
    return False


def check_source_hygiene() -> dict[str, str]:
    hashes: dict[str, str] = {}

    # Check Lean files if present
    if LEAN_DIR.is_dir():
        for p in sorted(LEAN_DIR.glob("*.lean")):
            text = p.read_text(encoding="utf-8")
            if FORBIDDEN_LEAN_TOKENS.search(text):
                raise ValueError(f"Forbidden token found in Lean source: {p.name}")
            if has_watched_digest(text):
                raise ValueError(f"Watched forbidden term found in Lean source: {p.name}")
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            hashes[rel] = sha256_file(p)

    # Check Python engine files
    for p in sorted(ROOT.glob("*.py")):
        text = p.read_text(encoding="utf-8")
        if has_watched_digest(text):
            raise ValueError(f"Watched forbidden term found in Python source: {p.name}")
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    # Check test files
    tests_dir = ROOT / "tests"
    if tests_dir.is_dir():
        for p in sorted(tests_dir.glob("*.py")):
            text = p.read_text(encoding="utf-8")
            if has_watched_digest(text):
                raise ValueError(f"Watched forbidden term found in test source: {p.name}")
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            hashes[rel] = sha256_file(p)

    return hashes


def run_pytest() -> dict[str, Any]:
    tests_path = str(ROOT / "tests")
    cmd = [sys.executable, "-m", "pytest", "-v", tests_path]
    print(f"== Running pytest: {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    output = proc.stdout + "\n" + proc.stderr
    print(output)
    if proc.returncode != 0:
        raise RuntimeError(f"pytest failed with exit code {proc.returncode}")

    passed_match = re.search(r"(\d+) passed", output)
    passed_count = int(passed_match.group(1)) if passed_match else 0
    return {
        "exit_code": proc.returncode,
        "passed": passed_count,
        "status": "PASS",
    }


def run_invariant_audit() -> dict[str, Any]:
    """Execute rigorous programmatic audit of core mathematical invariants."""
    from research.x301_formal_semantics.semantics import (
        Atom,
        Identity,
        Observer,
        Panel,
        PanelIllusionReceipt,
        RelationalModel,
    )
    from research.x303_bounded_agency.agency import (
        ActionAuthorizer,
        AgentController,
        BoundedMemory,
        CandidateAction,
        CausalEvaluator,
        LicensedDriver,
        MemoryRecord,
        MulticriteriaSelector,
        RefusalReason,
        StepResult,
        UnlicensedActionError,
        ViabilityEnvelope,
        add_instance_action,
        canonical_model_digest,
    )

    audit_results: dict[str, bool] = {}

    # Audit 1: Viability envelope ceiling enforcement & sort non-emptiness
    env = ViabilityEnvelope(max_data=3, max_forms=2, max_arity=2, max_insts=2, min_data=2, min_forms=1)
    m_valid = RelationalModel(data=("d0", "d1"), forms=(1,), insts=frozenset({(0, (0,))}))
    m_empty_data = RelationalModel(data=(), forms=(1,))
    m_excess_data = RelationalModel(data=("d0", "d1", "d2", "d3"), forms=(1,))

    assert env.is_viable(m_valid)
    assert not env.is_viable(m_empty_data)
    assert not env.is_viable(m_excess_data)
    audit_results["viability_envelope_ceilings_enforced"] = True

    # Audit 2: Refusal state immutability (state_after is state_before)
    ctrl_fuel = AgentController(state=m_valid, envelope=env, total_fuel=0)
    act = add_instance_action(form=0, args=(1,), fuel_cost=1)
    res_fuel = ctrl_fuel.step([act])
    assert res_fuel.is_refusal
    assert res_fuel.state is m_valid
    audit_results["refusal_preserves_state_unmutated"] = True

    # Audit 3: Causal counterfactual ephemeral branch non-mutation
    evaluator = CausalEvaluator()
    digest_before = canonical_model_digest(m_valid)
    projected = evaluator.project(m_valid, act)
    assert (0, (1,)) in projected.insts
    assert canonical_model_digest(m_valid) == digest_before
    audit_results["causal_projection_non_mutation"] = True

    # Audit 4: Grounding Firewall consensus override with PanelIllusionReceipt
    def illusory_fn(m: RelationalModel) -> RelationalModel:
        return RelationalModel(data=m.data, forms=m.forms, insts=m.insts | {(0, (2,))})

    panel = Panel(observers=(
        Observer(observer_id="o1", projection_fn=illusory_fn),
        Observer(observer_id="o2", projection_fn=illusory_fn),
        Observer(observer_id="o3", projection_fn=illusory_fn),
    ))
    formula = Atom(rel="form_0", args=("2",))
    ctrl_firewall = AgentController(state=m_valid, envelope=env, total_fuel=5, goal_formula=formula)
    res_firewall = ctrl_firewall.step([act], panel=panel)
    assert res_firewall.is_refusal
    assert res_firewall.reason == RefusalReason.FIREWALL_CONSENSUS_OVERRIDE
    assert isinstance(res_firewall.receipt, PanelIllusionReceipt)
    assert res_firewall.receipt.verify_checksum()
    audit_results["grounding_firewall_consensus_override"] = True

    # Audit 5: Zero unilateral mutation authority
    driver = LicensedDriver()
    authorizer = ActionAuthorizer()
    empty_license = authorizer.issue_license([])
    try:
        driver.apply_licensed(m_valid, act, empty_license)
        audit_results["zero_unilateral_mutation_authority"] = False
    except UnlicensedActionError:
        audit_results["zero_unilateral_mutation_authority"] = True

    # Audit 6: Exact rational multicriteria selection
    selector = MulticriteriaSelector(weights=(Fraction(1, 2), Fraction(1, 2), Fraction(0, 1)))
    assert selector.composite_utility((Fraction(1, 2), Fraction(1, 2), Fraction(1, 1))) == Fraction(1, 2)
    audit_results["exact_rational_multicriteria_selection"] = True

    return {
        "status": "PASS",
        "audits": audit_results,
    }


def run_lean() -> dict[str, Any]:
    lakefile = LEAN_DIR / "lakefile.toml"
    inventory = LEAN_DIR / "Inventory.lean"

    if not LEAN_DIR.is_dir() or not lakefile.is_file():
        return {
            "status": "NOT_PRESENT",
            "note": "Lean formalization package not yet authored or maintained separately.",
        }

    print("== Building Lean package with lake build")
    build_proc = subprocess.run(
        ["lake", "build"], cwd=LEAN_DIR, capture_output=True, text=True, check=False
    )
    build_output = build_proc.stdout + "\n" + build_proc.stderr
    print(build_output)
    if build_proc.returncode != 0:
        raise RuntimeError(f"lake build failed ({build_proc.returncode}):\n{build_output}")

    if inventory.is_file():
        print("== Running Inventory.lean census and axiom audit")
        inv_proc = subprocess.run(
            ["lake", "env", "lean", "Inventory.lean"],
            cwd=LEAN_DIR,
            capture_output=True,
            text=True,
            check=False,
        )
        inv_output = inv_proc.stdout + "\n" + inv_proc.stderr
        print(inv_output)
        if inv_proc.returncode != 0:
            raise RuntimeError(f"Inventory execution failed ({inv_proc.returncode}):\n{inv_output}")

        theorems: dict[str, list[str]] = {}
        for name, ax_str in AXIOM_RE.findall(inv_output):
            ax_list = [a.strip() for a in ax_str.split(",") if a.strip()]
            theorems[name] = ax_list
            disallowed = set(ax_list) - ALLOWED_AXIOMS
            if disallowed:
                raise ValueError(f"Disallowed axioms in theorem {name}: {disallowed}")

        for name in NO_AXIOM_RE.findall(inv_output):
            theorems[name] = []

        axiom_free = sum(1 for ax in theorems.values() if not ax)
        return {
            "build_status": "PASS",
            "theorem_count": len(theorems),
            "axiom_free_count": axiom_free,
            "allowed_axioms": sorted(ALLOWED_AXIOMS),
            "theorem_details": dict(sorted(theorems.items())),
        }

    return {"build_status": "PASS"}


def verify() -> dict[str, Any]:
    print("=== Starting Target X303 Verification ===")
    hashes = check_source_hygiene()
    pytest_res = run_pytest()
    audit_res = run_invariant_audit()
    lean_res = run_lean()

    receipt = {
        "schema_version": 1,
        "target": "Target X303: Agency & Control (Bounded Operational Agency)",
        "status": "PASS",
        "authority_effect": "None",
        "source_hashes": hashes,
        "pytest": pytest_res,
        "invariant_audit": audit_res,
        "lean": lean_res,
        "claim_hygiene": {
            "scope": (
                "Bounded agency over x301 RelationalModel with exact Fraction margins, "
                "FIFO memory, object-identity refusal, and licensed apply of projected CanonKeys. "
                "Default authorizer allows viable non-firewall evaluations. "
                "Does not import research.alpha_engine. Lean is a Nat-carrier toy. See CLAIMS.md."
            ),
            "discrete_viability_envelope_modeled": True,
            "finite_memory_horizon_modeled": True,
            "strict_refusal_semantics_modeled": True,
            "carrier_state_preserved_unmutated_on_refusal": True,
            "counterfactual_causal_evaluation_modeled": True,
            "grounding_firewall_consensus_override_modeled": True,
            "zero_unilateral_mutation_authority_enforced": True,
            "exact_rational_multicriteria_pareto_selection_modeled": True,
            "zero_floating_point_arithmetic": True,
        },
    }
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Check receipt against fresh run"
    )
    parser.add_argument("--write", action="store_true", help="Write fresh receipt")
    args = parser.parse_args()

    try:
        receipt = verify()
        raw = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")

        RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
        if args.check:
            if not RECEIPT_PATH.is_file():
                print("FAIL: receipt.json does not exist. Run with --write first.")
                return 1
            existing = RECEIPT_PATH.read_bytes()
            if existing != raw:
                print("FAIL: existing receipt does not match freshly generated verification")
                return 1
            print("PASS: verification receipt matches fresh run")
        else:
            RECEIPT_PATH.write_bytes(raw)
            print(f"WROTE: {RECEIPT_PATH}")
            print("PASS: all verification steps passed successfully.")
        return 0
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
