"""Regression checks for Wiki claim custody and Markdown/link generation.

AuthorityEffect: None.
"""
import re
from collections import Counter
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from build_wiki_textbook import build_all, build_unit_wiki_page, extract_header_meta, first_sentences, resolve_commit_sha, rewrite_links_for_wiki
from unit_page_custody import VIDEO, unit_lesson_errors


class WikiTextbookTests(unittest.TestCase):
    def test_all_93_lessons_keep_full_text_before_optional_video(self):
        root = Path(__file__).resolve().parents[2]
        groups = [sorted((root / folder).glob('*.md'))
                  for folder in ('textbook/units', 'textbook/institutions/units')]
        maps = [{p.name: 'textbook_' + prefix + p.stem for p in files}
                for prefix, files in zip(('u', 'i'), groups)]
        checked = 0
        for part, files in enumerate(groups):
            folder = 'textbook/institutions/units' if part else 'textbook/units'
            for p in files:
                raw = p.read_text(encoding='utf-8')
                page = build_unit_wiki_page(int(p.name[:2]), len(files), raw,
                    None, None, *maps, 'https://example.invalid/blob/' + 'a'*40,
                    'a'*12, bool(part))
                expected = rewrite_links_for_wiki(raw, *maps,
                    'https://example.invalid/blob/' + 'a'*40, bool(part), folder)
                self.assertEqual(page.count(expected), 1, p.name)
                self.assertLess(page.index(expected) + len(expected), page.index(VIDEO), p.name)
                # No generated diagram or shortened quotation replaces a source block.
                self.assertEqual(Counter(re.findall(r'```.*?```', page, re.S)),
                                 Counter(re.findall(r'```.*?```', raw, re.S)), p.name)
                self.assertNotIn('Short preview (', page)
                self.assertNotRegex(page[:page.index(expected)], r'\]\(#')
                checked += 1
        self.assertEqual(checked, 93)

    def test_custody_refuses_dropped_text_wrong_pins_and_video_changes(self):
        root = Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory() as temp:
            wiki = Path(temp)
            build_all(root, wiki)
            self.assertEqual(unit_lesson_errors(root, wiki), [])
            path = wiki / 'textbook_u00_mark_and_constructor.md'
            original = path.read_text(encoding='utf-8')
            pin = resolve_commit_sha(root)
            def swap_pin(target):
                return original.replace(pin, target).replace(pin[:12], target[:12])
            start = original.index(VIDEO)
            end = original.index('</details>', start) + len('</details>')
            video = original[start:end]
            cases = {
                'dropped scope sentence': (original.replace('The mark does not supply one.', ''), 'Unit lesson text'),
                'video before lesson': (video + original.replace(video, '', 1), 'precede its folded video'),
                'open video': (original.replace(VIDEO, VIDEO.replace('<details>', '<details open>')), 'folded video'),
                'missing GIF': (original.replace('act00_pre_genesis_mark.gif', 'wrong.gif'), 'Act media link'),
                'unprefixed fragment shortcut': ('[First pass](#first-pass)\n' + original, 'fragment shortcut'),
                'prefixed fragment shortcut': ('[First pass](#user-content-first-pass)\n' + original, 'fragment shortcut'),
                'unavailable source pin': (swap_pin('0'*40), 'unavailable Unit source blob'),
                'real pin with different source': (swap_pin('e492b100aaa298e886a690e7fec955480c10d817'), 'source pin differs'),
            }
            for name, (faulty, message) in cases.items():
                with self.subTest(name=name):
                    path.write_text(faulty, encoding='utf-8')
                    try:
                        self.assertTrue(any(message in e for e in unit_lesson_errors(root, wiki)))
                    finally:
                        path.write_text(original, encoding='utf-8')
            self.assertEqual(unit_lesson_errors(root, wiki), [])

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

    def test_change_route_publishes_its_core_exit(self):
        from change_lab_wiki import build_change_lab
        root = Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory() as temporary:
            wiki = Path(temporary)
            for name in ('Home.md', '_Sidebar.md'):
                (wiki / name).write_text('', encoding='utf-8')
            build_change_lab(root, wiki, 'a' * 40)
            for slug in ('textbook_change_lab', 'textbook_change_lab_07_keep_the_model_in_view', 'textbook_change_lab_answers'):
                page = (wiki / (slug + '.md')).read_text(encoding='utf-8')
                self.assertIn('](textbook_reading_formal)', page)
                self.assertNotIn('](../reading_formal_statements.md)', page)
            self.assertIn('](textbook_learning_path)', (wiki / 'textbook_change_lab.md').read_text(encoding='utf-8'))

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
