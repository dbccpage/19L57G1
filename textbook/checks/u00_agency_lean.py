"""Exact reports from the separate X303 Lean toy; AuthorityEffect: None."""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from booklean import main, BOTH  # noqa: E402
from textbook.reasoning_lab.agency import ROOT, verify_sources  # noqa: E402

verify_sources()
owner = ROOT / 'research/x303_bounded_agency/lean'
body = (owner / 'BoundedAgency.lean').read_text(encoding='utf-8')
assert not re.search(r'^import ', body, re.M), 'Review changed Lean imports'
inventory = (owner / 'Inventory.lean').read_text(encoding='utf-8')
names = ['X303BoundedAgency.' + n for n in re.findall(r'^#print axioms (\w+)$', inventory, re.M)]
assert len(names) == len(set(names)) == 16
source = body + '\n' + '\n'.join('#print axioms ' + n for n in names)

if __name__ == '__main__':
    raise SystemExit(main(source, {n: BOTH for n in names}, 'BoundedAgency'))
