"""Check that native bare imports cannot replace other book routes' modules."""
import sys
import types
import unittest
from textbook.reasoning_lab import semantics


class NativeImportIsolation(unittest.TestCase):
    def test_existing_modules_and_path_survive_native_checks(self):
        names = ('formulas', 'intervention', 'model', 'panel', 'valuation')
        missing = object()
        previous = {name: sys.modules.get(name, missing) for name in names}
        markers = {name: types.ModuleType(name) for name in names}
        path_before = list(sys.path)
        try:
            sys.modules.update(markers)
            result = semantics.check_examples()
            self.assertEqual(result['guard_contexts'], 96)
            self.assertTrue(all(sys.modules[name] is marker for name, marker in markers.items()))
            self.assertEqual(sys.path, path_before)
        finally:
            for name, original in previous.items():
                if original is missing:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = original


if __name__ == '__main__':
    unittest.main()
