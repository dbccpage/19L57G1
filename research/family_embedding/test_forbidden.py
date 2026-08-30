"""Negative tests: denylist identifiers, external markers, carrier-general
prose without a theorem name, ledger evidence resolution, sealed writes.

Each scanner is shown to bite on an injected string built at runtime, so a
green run is a receipt that the listed phrasings and markers are absent --
never that the prose is right.  AuthorityEffect: None.
"""

from __future__ import annotations

import ast
import json
import re
import unittest
from pathlib import Path
from typing import Iterator

import verify_lean

TREE = Path(__file__).resolve().parent
REPO = TREE.parents[1]
LEDGER = TREE / "CLAIM_LEDGER.md"
STATUS = TREE / "STATUS.md"
DENYLIST_JSON = REPO / "contact" / "analysis" / "contact_countermodels.json"
NATIVE_SUBJECT = "PrimitiveDifference"

CARRIER_GENERAL = re.compile(
    r"for all carriers|every carrier|all carriers|carrier-general|carrier general"
    r"|on every type|for every type|for all types|every alpha",
    re.I,
)
_TOKEN = re.compile(r"`([^`]+)`")
_LIST_ITEM = re.compile(r"^\s*(?:[*-]|\d+\.)\s+")
_THEOREM = re.compile(r"^theorem ([A-Za-z_][\w']*)", re.M)
_TEST_DEF = re.compile(r"^\s*def (test_\w+)\(", re.M)


def tree_files() -> Iterator[Path]:
    for path in sorted(TREE.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(TREE).parts
        if any(part.startswith(".") or part == "__pycache__" for part in relative[:-1]):
            continue
        yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def working_denylist() -> list[str]:
    payload = json.loads(DENYLIST_JSON.read_text(encoding="utf-8"))
    block = payload["denylist"]
    assert isinstance(block, dict)
    full = block["full_census"]
    subtracted = block["subtracted_as_native_or_core"]
    assert isinstance(full, list) and isinstance(subtracted, list)
    names = [n for n in full if isinstance(n, str) and n not in set(subtracted)]
    assert len(names) == 102
    return names


def denylist_pattern(names: list[str]) -> re.Pattern[str]:
    return re.compile(r"(?<![\w])(?:" + "|".join(re.escape(n) for n in names) + r")(?![\w])")


def identifier_token(name: str) -> re.Pattern[str]:
    return re.compile(r"(?<![\w])" + re.escape(name) + r"(?![\w])")


def external_marker_patterns() -> list[tuple[str, re.Pattern[str]]]:
    pieces = {
        "et" + " al": r"\bet\s+" + r"al\b",
        "ar" + "Xiv": "ar" + "xiv",
        "do" + "i:": r"\bdo" + "i:",
        "http" + "://": "http" + "://",
        "https" + "://": "https" + "://",
        "IS" + "BN": r"\bIS" + r"BN\b",
        "Wiki" + "pedia": "wiki" + "pedia",
        "[n] at line end": r"(?<![\w)\]])\[\d+\]\s*$",
    }
    return [(label, re.compile(pattern, re.I | re.M)) for label, pattern in pieces.items()]


def _marker_exempt_lines(source: str) -> set[int]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    parents: dict[ast.AST, ast.AST] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node
    exempt: set[int] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        cursor: ast.AST | None = node
        for _ in range(4):
            if cursor is None:
                break
            if isinstance(cursor, (ast.Assign, ast.AnnAssign)):
                targets = cursor.targets if isinstance(cursor, ast.Assign) else [cursor.target]
                if any(isinstance(t, ast.Name) and "MARKER" in t.id.upper() for t in targets):
                    exempt.add(node.lineno)
            if isinstance(cursor, ast.Call):
                names: list[str] = []
                if isinstance(cursor.func, ast.Name):
                    names.append(cursor.func.id)
                if isinstance(cursor.func, ast.Attribute):
                    names.append(cursor.func.attr)
                if any("marker" in name.lower() for name in names):
                    exempt.add(node.lineno)
            cursor = parents.get(cursor)
    return exempt


def external_marker_hits(path: Path, text: str) -> list[str]:
    exempt = (
        _marker_exempt_lines(text)
        if path.name.startswith("test_") and path.suffix == ".py"
        else set()
    )
    hits: list[str] = []
    for lineno, line in enumerate(text.split("\n"), start=1):
        if lineno in exempt:
            continue
        for label, pattern in external_marker_patterns():
            if pattern.search(line):
                hits.append(f"{path.name}:{lineno}: {label}")
    return hits


def units(text: str) -> list[str]:
    out: list[str] = []
    paragraph: list[str] = []
    for line in text.split("\n"):
        if line.startswith("|"):
            if paragraph:
                out.append(" ".join(paragraph))
                paragraph = []
            out.append(line)
        elif line.strip():
            if _LIST_ITEM.match(line) and paragraph:
                out.append(" ".join(paragraph))
                paragraph = []
            paragraph.append(line.strip())
        elif paragraph:
            out.append(" ".join(paragraph))
            paragraph = []
    if paragraph:
        out.append(" ".join(paragraph))
    return out


def prose_sentences(unit: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+", unit) if s.strip()]


def theorem_names() -> set[str]:
    names: set[str] = set()
    for path in verify_lean.research_lean_sources():
        names.update(_THEOREM.findall(read_text(path)))
    names.update(verify_lean.AXIOM_REPORT_DECLARATIONS)
    names.update(
        _THEOREM.findall(
            read_text(REPO / "lean4" / "Derivation" / "PresentationNaturality.lean")
        )
    )
    return names


def names_a_theorem(sentence: str, theorems: set[str]) -> bool:
    for token in _TOKEN.findall(sentence):
        if token in theorems:
            return True
        if token.split(".")[-1] in theorems:
            return True
    return False


def ledger_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    for line in read_text(LEDGER).split("\n"):
        if not line.startswith("| FE-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4:
            continue
        rows.append(cells)
    return rows


def test_defs() -> set[str]:
    names: set[str] = set()
    for path in sorted(TREE.glob("test_*.py")):
        names.update(_TEST_DEF.findall(read_text(path)))
    return names


def receipt_keys(obj: object, prefix: str = "") -> set[str]:
    keys: set[str] = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            keys.add(path)
            keys |= receipt_keys(value, path)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            keys |= receipt_keys(value, f"{prefix}[{i}]")
    return keys


def evidence_resolves(token: str, tests: set[str], theorems: set[str], keys: set[str]) -> bool:
    if token in theorems or token in verify_lean.AXIOM_REPORT_DECLARATIONS:
        return True
    if token in tests:
        return True
    if "." in token:
        head, name = token.split(".", 1)
        if head in {p.stem for p in TREE.glob("test_*.py")} and name in tests:
            return True
    if token.startswith("receipts/") and (TREE / token).is_file():
        return True
    if token.startswith("embedding:") and token[len("embedding:") :] in keys:
        return True
    return token in keys


class DenylistTests(unittest.TestCase):
    def test_no_working_denylist_identifier_anywhere_in_the_tree(self) -> None:
        names = [n for n in working_denylist() if n != NATIVE_SUBJECT]
        pattern = denylist_pattern(names)
        leaks: list[str] = []
        scanned = 0
        for path in tree_files():
            scanned += 1
            text = read_text(path)
            for match in pattern.finditer(text):
                leaks.append(f"{path.relative_to(TREE).as_posix()}: {match.group(0)}")
        self.assertGreater(scanned, 8)
        self.assertEqual(leaks, [])

    def test_boundary_regex_matches_an_injected_identifier(self) -> None:
        names = working_denylist()
        self.assertIsNotNone(denylist_pattern(names).search("see " + names[0] + " here"))
        self.assertIsNone(denylist_pattern(names).search("see " + names[0] + "Suffix here"))
        pat = identifier_token("AaBbToken")
        self.assertIsNotNone(pat.search("uses AaBbToken here"))
        self.assertIsNone(pat.search("AaBbTokenMod"))


class ExternalMarkerTests(unittest.TestCase):
    def test_no_external_marker_in_md_py_or_lean_files(self) -> None:
        hits: list[str] = []
        for path in tree_files():
            if path.suffix in (".md", ".py", ".lean"):
                hits.extend(external_marker_hits(path, read_text(path)))
        self.assertEqual(hits, [])

    def test_markers_bite_on_injected_text(self) -> None:
        samples = (
            "see Smith et" + " al. for the argument",
            "posted on ar" + "Xiv last year",
            "do" + "i:10.1000/xyz",
            "http" + "://example",
            "https" + "://example",
            "IS" + "BN 0-00",
            "as Wiki" + "pedia says",
            "a numeric citation [1]",
        )
        for sample in samples:
            self.assertTrue(external_marker_hits(Path("probe.md"), sample), sample)
        self.assertEqual(
            external_marker_hits(
                Path("clean.md"), "a list [1, 2], an index x[0]\nand f(y)[1]\nand z[2]"
            ),
            [],
        )


class CarrierGeneralTests(unittest.TestCase):
    def test_carrier_general_prose_names_a_theorem(self) -> None:
        theorems = theorem_names()
        violations: list[str] = []
        for path in (STATUS, LEDGER):
            for unit in units(read_text(path)):
                for sentence in prose_sentences(unit):
                    if CARRIER_GENERAL.search(sentence) and not names_a_theorem(
                        sentence, theorems
                    ):
                        violations.append(f"{path.name}: {sentence.strip()}")
        self.assertEqual(violations, [])

    def test_injected_carrier_general_sentence_is_caught(self) -> None:
        sample = "The construction works for all carriers without further hypotheses."
        self.assertTrue(CARRIER_GENERAL.search(sample))
        self.assertFalse(names_a_theorem(sample, theorem_names()))


class LedgerEvidenceTests(unittest.TestCase):
    def test_every_ledger_evidence_token_resolves(self) -> None:
        tests = test_defs()
        theorems = theorem_names()
        payload = json.loads((TREE / "receipts" / "embedding.json").read_text(encoding="ascii"))
        keys = receipt_keys(payload)
        missing: list[str] = []
        rows = ledger_rows()
        self.assertGreaterEqual(len(rows), 6)
        for cells in rows:
            for token in _TOKEN.findall(cells[3]):
                if not evidence_resolves(token, tests, theorems, keys):
                    missing.append(f"{cells[0]}: {token}")
        self.assertEqual(missing, [])

    def test_injected_dead_token_does_not_resolve(self) -> None:
        tests = test_defs()
        theorems = theorem_names()
        keys = receipt_keys(
            json.loads((TREE / "receipts" / "embedding.json").read_text(encoding="ascii"))
        )
        self.assertFalse(evidence_resolves("test_this_does_not_exist", tests, theorems, keys))
        self.assertFalse(
            evidence_resolves(
                "{ f : F.Arr // F.src f = a ∧ F.tgt f = b }", tests, theorems, keys
            )
        )


if __name__ == "__main__":
    unittest.main()
