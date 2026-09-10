"""axiom_inventory.py — Research Estate Axiom Inventory and Gate Inspector.

Audits Lean axiom configurations and verify_lean.py scripts across all research trees.

Claim Hygiene:
- Narrow claim: Inspects the declared allowed axioms in every research tree verify_lean.py
  and checks whether any tree permits non-constructive axioms (e.g. Classical.choice).
- AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]


def inspect_tree_axiom_scripts(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Inspect all verify_lean.py files across research trees."""
    research_dir = repo_root / "research"
    tree_inventories: dict[str, Any] = {}

    allowed_re = re.compile(r"(?:ALLOWED_AXIOMS|WHITELIST|AXIOM_WHITELIST)\s*=\s*(\{[^}]+\})")
    doc_whitelist_re = re.compile(r"\{propext,\s*Quot\.sound\}")

    for p in sorted(research_dir.glob("*/verify_lean.py")):
        tree_name = p.parent.name
        content = p.read_text(encoding="utf-8")

        match = allowed_re.search(content)
        if match:
            allowed_decl = match.group(1)
        elif doc_whitelist_re.search(content):
            allowed_decl = "{'propext', 'Quot.sound'}"
        else:
            allowed_decl = "{'propext', 'Quot.sound'} (implicit / hardcoded)"

        # Check for Classical.choice
        permits_choice = "Classical.choice" in allowed_decl

        # Check for lean source directory
        lean_dir = p.parent / "lean"
        lean_sources = list(lean_dir.glob("**/*.lean")) if lean_dir.is_dir() else []

        tree_inventories[tree_name] = {
            "verify_lean_script": str(p.relative_to(repo_root)).replace("\\", "/"),
            "allowed_axioms_declaration": allowed_decl,
            "permits_choice": permits_choice,
            "lean_source_count": len(lean_sources),
            "lean_sources": [str(s.relative_to(repo_root)).replace("\\", "/") for s in lean_sources],
        }

    return tree_inventories


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit research tree Lean axiom gates.")
    parser.add_argument("--json", action="store_true", help="Emit inventory as JSON")
    args = parser.parse_args()

    inventory = inspect_tree_axiom_scripts()

    if args.json:
        print(json.dumps(inventory, indent=2))
    else:
        print(f"=== RESEARCH AXIOM INVENTORY ({len(inventory)} trees with verify_lean.py) ===")
        any_choice = False
        for tree, data in sorted(inventory.items()):
            choice_flag = " [DISALLOWED: permits Classical.choice!]" if data["permits_choice"] else ""
            if data["permits_choice"]:
                any_choice = True
            print(f"  {tree:30} -> {data['allowed_axioms_declaration']}{choice_flag} ({data['lean_source_count']} lean files)")

        print("---")
        print(f"Classical.choice permitted in any research tree: {any_choice}")

    # Write output to research/estate_honesty/research_axioms.json
    out_file = REPO_ROOT / "research" / "estate_honesty" / "research_axioms.json"
    out_file.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote axiom inventory to {out_file.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
