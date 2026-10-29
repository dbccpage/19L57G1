"""Regression checks for Wiki claim custody and Markdown/link generation.

AuthorityEffect: None.
"""
import re
import unittest
from unittest.mock import patch
from pathlib import Path

from build_wiki_textbook import extract_header_meta, first_sentences, resolve_commit_sha, rewrite_links_for_wiki


class WikiTextbookTests(unittest.TestCase):
    def test_missing_source_revision_is_not_replaced_by_a_historical_pin(self):
        with patch("build_wiki_textbook.subprocess.run", side_effect=OSError("Git unavailable")):
            with self.assertRaises(RuntimeError):
                resolve_commit_sha(Path("unavailable-checkout"))

    def test_metadata_after_long_claim_is_preserved(self):
        md = "# Lesson\n\n**Claim.** " + "A statement.\n" * 40
        md += "**Status:** FROZEN; CONDITIONAL (on a witness). **Lean:** `Anchor`.\n\n## Question\n"
        meta = extract_header_meta(md)
        self.assertEqual(meta["status"], "FROZEN; CONDITIONAL (on a witness)")
        self.assertEqual(meta["lean"], "`Anchor`")
        self.assertEqual(meta["claim"].count("A statement."), 40)

    def test_missing_status_is_not_promoted(self):
        self.assertEqual(extract_header_meta("# Lesson\n\n**Claim.** A definition.")["status"], "See unit classification")

    def test_table_metadata(self):
        meta = extract_header_meta("# Lesson\n\n| **Claim** | A finite claim. |\n| **Mark** | `CONDITIONAL` (nonempty domain) |\n\n## Question\n")
        self.assertEqual(meta["claim"], "A finite claim.")
        self.assertIn("CONDITIONAL", meta["status"])

    def test_preview_does_not_cut_hypotheses_or_markdown(self):
        self.assertEqual(first_sentences("A short sentence. The theorem holds only under " + "the hypothesis " * 30, 6), "A short sentence.")
        self.assertNotIn("...", first_sentences("An overlong statement " * 40, 6))
        self.assertEqual(first_sentences("A `left | right` choice.", 20), "A left &#124; right choice.")

    def test_relative_links_and_anchors(self):
        part1 = {"08_contexts.md": "textbook_u08_contexts"}
        body = "[unit](08_contexts.md#profile) [check](../checks/u08.py) [source](../../code/model.py) [hub](../README.md)"
        rewritten = rewrite_links_for_wiki(body, part1, {}, "https://example.invalid/blob/SHA", False, "textbook/units")
        self.assertIn("](textbook_u08_contexts#profile)", rewritten)
        self.assertIn("/textbook/checks/u08.py)", rewritten)
        self.assertIn("/code/model.py)", rewritten)
        self.assertIn("](textbook_overview)", rewritten)
        self.assertNotIn("/../", rewritten)

    def test_institution_hub_and_literal_code_links(self):
        result = rewrite_links_for_wiki("[hub](../README.md)\n```text\n[example](../README.md)\n```", {}, {}, "BASE", True, "textbook/institutions/units")
        self.assertIn("](textbook_institutions)", result)
        self.assertIn("[example](../README.md)", result)

    def test_beginner_route_links_stay_in_the_wiki(self):
        folders=('first_steps','reasoning_lab','search_lab','change_lab','path_lab','map_lab','growth_lab','boundary_lab','identification_lab','number_lab')
        for folder in folders:
            body=f'[route](../{folder}/README.md) [lesson](../{folder}/SOURCE_MAP.md#scope)'
            result=rewrite_links_for_wiki(body,{}, {},'BLOB',False,'textbook/units')
            self.assertIn(f'](textbook_{folder})',result)
            self.assertIn(f'](textbook_{folder}_source_map#scope)',result)

    def test_reading_guide_links_and_source_only_files(self):
        body='[guide](../reading_formal_statements.md) [review](../map_lab/REVIEW_2026-10-28.md) [program](../map_lab/run_lab.py)'
        result=rewrite_links_for_wiki(body,{}, {},'BLOB',False,'textbook/units')
        self.assertIn('](textbook_reading_formal)',result)
        self.assertIn('](BLOB/textbook/map_lab/REVIEW_2026-10-28.md)',result)
        self.assertIn('](BLOB/textbook/map_lab/run_lab.py)',result)

    def test_unit71_book_example_runs(self):
        root = Path(__file__).resolve().parents[2]
        lesson = next((root / "textbook/units").glob("71_*.md")).read_text(encoding="utf-8")
        examples = re.findall(r"```python\n(.*?)```", lesson, flags=re.DOTALL)
        self.assertEqual(len(examples), 1)
        exec(compile(examples[0], "Unit71_example", "exec"), {})

    def test_unit71_quoted_definitions_match_source(self):
        root = Path(__file__).resolve().parents[2]
        lesson = next((root / "textbook/units").glob("71_*.md")).read_text(encoding="utf-8")
        source = (root / "lean4/Derivation/PresentationRelativity.lean").read_text(encoding="utf-8")
        normalize = lambda value: " ".join(value.split())
        for block in re.findall(r"```lean\n(.*?)```", lesson, flags=re.DOTALL):
            for declaration in re.split(r"\n(?=def |structure )", block):
                self.assertIn(normalize(declaration), normalize(source))


if __name__ == "__main__":
    unittest.main()
