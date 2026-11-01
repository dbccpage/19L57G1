"""Unchanged X302 proof body, exact selected reports; AuthorityEffect: None."""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from booklean import main, NONE, PROPEXT  # noqa: E402
from textbook.reasoning_lab.revision import OWNER, verify_sources  # noqa: E402

verify_sources()
body = (OWNER / 'lean/OperationalReasoning.lean').read_text(encoding='utf-8')
assert not re.search(r'^import ', body, re.M), 'Review changed owner imports'
inventory = (OWNER / 'lean/Inventory.lean').read_text(encoding='utf-8')
names = ['X302OperationalReasoning.' + name for name in re.findall(r'^#print axioms (\w+)$', inventory, re.M)]
assert len(names) == 18 and len(set(names)) == 18
expected = {name: PROPEXT if name.endswith('.conj_intro_support_mem') else NONE for name in names}
source = body + '\n' + '\n'.join('#print axioms ' + name for name in names)

if __name__ == '__main__':
    raise SystemExit(main(source, expected, 'OperationalRevision'))
