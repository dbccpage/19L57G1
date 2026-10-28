"""Check deployable bundles and refuse incomplete transformations.

AuthorityEffect: None. These checks do not assess reader comprehension.
"""
from pathlib import Path
import shutil
import tempfile
import unittest

from build import build_explorer

SOURCE = Path(__file__).resolve().parent


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.source.mkdir()
        for name in ("explorer.html", "explorer.css", "explorer.mjs", "model.mjs", "cards.json"):
            shutil.copyfile(SOURCE / name, self.source / name)
        self.output = self.root / "output/explorer.html"

    def test_bundle_needs_no_fetch_module_or_stylesheet_and_rewrites_reading_links(self):
        build_explorer(self.source, self.output, {"README.md": "https://example.invalid/reading"})
        html = self.output.read_text(encoding="utf-8")
        self.assertNotIn('src="explorer.mjs', html)
        self.assertNotIn('href="explorer.css"', html)
        self.assertNotIn('await fetch(', html)
        self.assertNotIn('import.meta', html)
        self.assertIn('href="https://example.invalid/reading"', html)
        self.assertIn('No answers recorded', html)

    def test_changed_load_protocol_is_refused_instead_of_publishing_broken_bundle(self):
        path = self.source / "explorer.mjs"
        path.write_text(path.read_text(encoding="utf-8").replace("await fetch(", "await loadTable("), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "supplied-table load"):
            build_explorer(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_missing_entry_script_is_refused(self):
        path = self.source / "explorer.html"
        path.write_text(path.read_text(encoding="utf-8").replace('src="explorer.mjs?lesson=1"', 'src="other.mjs"'), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "script element"):
            build_explorer(self.source, self.output)


if __name__ == "__main__":
    unittest.main()
