"""Native source import effects stay inside the isolated worker."""
import sys
import types
import unittest
from textbook.reasoning_lab.agency import check_examples


class AgencyImportIsolation(unittest.TestCase):
    def test_existing_names_and_search_path_survive(self):
        names = ('model', 'formulas', 'intervention', 'isomorphism', 'panel', 'valuation')
        missing = object()
        previous = {name: sys.modules.get(name, missing) for name in names}
        markers = {name: types.ModuleType(name) for name in names}
        path_before = list(sys.path)
        try:
            sys.modules.update(markers)
            result = check_examples()
            self.assertEqual(result['controller_cases'], 2304)
            self.assertTrue(all(sys.modules[name] is marker for name, marker in markers.items()))
            self.assertEqual(sys.path, path_before)
        finally:
            for name, module in previous.items():
                if module is missing:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = module


if __name__ == '__main__':
    unittest.main()
