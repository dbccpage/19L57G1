"""Negative tests for the forbidden closures of PROMPT.md steps 35-40, the
ledger-evidence rule of step 30, and the discipline of the synthesis
documents (CLAIM_LEDGER.md, STATUS.md, PROPOSED_S9.md).

Each forbidden closure gets a test that fails the run when the closure is
attempted, and each scanner is shown to bite on an injected string built at
runtime, so a green run is a receipt that the listed phrasings and markers
are absent -- never that the prose is right.  The scanners are mechanical
proxies; the prose rules of steps 36, 37 and 40 are wider and stay a manual
check.  Nothing here computes a result about S9.1, S9.2 or S9.3.

Declared decisions of this module (recorded in STATUS.md too):

* step 36's mention rule is applied per markdown TABLE ROW, per LIST ITEM,
  and otherwise per PARAGRAPH (a maximal run of non-blank lines), because
  prose wraps at the column and a physical line cannot carry a whole
  sentence; the accepted markers are the brief's three (``UNCHANGED``,
  ``not in scope``, ``out of scope``) plus ``protected open(s)``, step 36's
  own name for the three, so a unit describing the rule can name them; a
  mention of a protected name that lies inside a double-quoted span is
  exempt from the marker rule only (it is still subject to the claim-pattern
  rule), so a recorded injection sentence can be quoted without exempting a
  quoted claim;
* step 37's phrase list is the brief's three phrases plus their "every
  type" relatives, and the check is applied to rows classified finite
  computation, bounded theorem, or countermodel; since repair round 1 it
  is also applied to every sentence of STATUS.md and PROPOSED_S9.md (a
  diff fence read as its ``+`` lines) and, per list item, paragraph or
  table row, to P2_FINDINGS.md, each such sentence or unit having to name
  a Lean theorem -- any theorem of this tree's package or of the sealed
  ``PrimDiff.lean``, a declared proxy: nothing checks that the named
  theorem states the general case -- or to carry a declared openness
  marker (``OPEN_MARKERS``; for P2_FINDINGS.md also ``FINDINGS_MARKERS``,
  the markers P1's own scanner accepts); P1_FINDINGS.md and
  P3_FINDINGS.md are scanned by their parts' own step-37 tests;
* the definition of done's "bounded in the same sentence as the result"
  rule is applied, since repair round 1, to the ``+`` lines of every diff
  fence of PROPOSED_S9.md: a sentence naming a computed result (a word of
  ``RESULT_MARKER``, or a number of two or more digits) must contain
  "bounded" or name a Lean theorem -- a proxy, declared as one, added
  after a reviewer found the S9.3 bullet's boundary sentence unbounded;
  since repair round 2 "interval(s)" is a result word, a section, step,
  line or row number is blanked first as a cross-reference
  (``CROSS_REFERENCE``), and the same scanner runs over the "Outcome" and
  "What stayed open" sections of STATUS.md and over no other section of
  it (the terminal lines have their own test; the remaining sections
  carry report counts, hashes, line numbers and test tallies);
* step 39 walks every regular file under the tree, skipping directories
  whose name begins with a dot (Lake and mypy build products, gitignored)
  and ``__pycache__``, and scans all 102 working-denylist identifiers with
  the firewall's boundary regex, the native subject name included;
* step 40's markers are matched in ``.md``, ``.py`` and ``.lean`` files,
  with one declared exemption: string literals in a ``test_*.py`` file that
  sit in an assignment whose target name contains ``MARKER`` or in a call
  to a function whose name contains ``marker`` -- that is where the parts'
  own scanners keep their marker lists.

AuthorityEffect: None.
"""

from __future__ import annotations

import ast
import json
import re
import tempfile
import unittest
from pathlib import Path
from typing import Iterator

import axiom_lattice as al
import common
import verify_lean
import verify_pins

TREE = Path(__file__).resolve().parent
REPO = TREE.parents[1]
RECEIPTS = TREE / "receipts"
LEDGER = TREE / "CLAIM_LEDGER.md"
STATUS = TREE / "STATUS.md"
PROPOSED = TREE / "PROPOSED_S9.md"
FINDINGS = tuple(TREE / name for name in ("P1_FINDINGS.md", "P2_FINDINGS.md", "P3_FINDINGS.md"))
SYNTHESIS_DOCUMENTS = (LEDGER, STATUS, PROPOSED)
PAPER = REPO / "paper" / "primitive_difference.md"
WORKFLOW = REPO / ".github" / "workflows" / "verify.yml"
SEALED_LEAN = REPO / "lean4" / "Derivation" / "PrimDiff.lean"
DENYLIST_JSON = REPO / "contact" / "analysis" / "contact_countermodels.json"

CLASSIFICATIONS = frozenset(
    {
        "proved theorem",
        "bounded theorem",
        "finite computation",
        "countermodel",
        "conjecture",
        "open",
    }
)
RECEIPT_NAMES = ("axiom_lattice", "morphism_classes", "witness_types")

_ROW_ID = re.compile(r"^(?:PRE|S9-[123]|DEC)-\d{2}$")
_TOKEN = re.compile(r"`([^`]+)`")
_TEST_TOKEN = re.compile(r"^(?:(test_\w+)\.)?(test_\w+)$")
_RECEIPT_TOKEN = re.compile(r"^(axiom_lattice|morphism_classes|witness_types):(.+)$")
_RESEARCH_LEAN_TOKEN = re.compile(r"^S9Obligations\.(\w+)\.([A-Za-z_][\w']*)$")
_SEALED_LEAN_TOKEN = re.compile(r"^PrimDiff\.([A-Za-z_][\w']*)$")
_SEGMENT = re.compile(r"^([^\[\]]+)((?:\[\d+\])*)$")

# Step 37: phrases that promote a bounded sweep to a carrier-general claim.
CARRIER_GENERAL = re.compile(
    r"for all carriers|every carrier|all carriers|carrier-general|carrier general"
    r"|on every type|for every type|for all types|every alpha",
    re.I,
)
# A sentence of prose may carry a step-37 phrase without naming a theorem
# only when it says, in these words, that the general case is open.
OPEN_MARKERS = re.compile(
    r"no Lean theorem|not attempted|not proposed|is open|stays open|no carrier-general claim",
    re.I,
)
# P2_FINDINGS.md is another agent's prose, scanned per unit with the wider
# markers P1's own scanner accepts (a proposal, a bound, a pointer to the
# Lean stage, a denial).
FINDINGS_MARKERS = re.compile(
    r"bounded|target|attempt|propos|Lean stage|Lean theorem|does not promote",
    re.I,
)
# Definition of done, applied to the proposed paper text: a sentence that
# names a computed result must say "bounded" or name a Lean theorem.
RESULT_MARKER = re.compile(
    r"\binvisible\b|hides nothing|enumerated space|separated by|pair counts?|\bintervals?\b|\b\d{2,}\b",
    re.I,
)
# A section, step, line or row number is a cross-reference, not a computed
# result; it is blanked before RESULT_MARKER looks for a bare number
# (declared exemption, repair round 2).
CROSS_REFERENCE = re.compile(
    r"\b(?:sections?|steps?|lines?|rows?)\s+\d+(?:[.-]\d+)*", re.I
)
_HUNK = re.compile(r"^@@ -(\d+),(\d+) \+(\d+),(\d+) @@")

# Step 36: the protected opens, the verbs, and the denial phrases.
_NAME = r"(?:OB-?1\b|S6\.6|inscription bridge|last bullet|sixth bullet)"
PROTECTED = re.compile(_NAME, re.I)
MENTION_MARKER = re.compile(r"UNCHANGED|not in scope|out of scope|protected opens?", re.I)
_VERB = r"(?:clos(?:e|es|ed|ing)|narrow(?:s|ed|ing)?|pric(?:e|es|ed|ing))"
_PAST = r"(?:closed|narrowed|priced)"
_BASE = r"(?:close|narrow|price)"
_LIST_PAST = rf"{_PAST}(?:\s*,\s*{_PAST})*(?:\s*,?\s*(?:or|nor|and)\s+{_PAST})?"
_LIST_BASE = rf"{_BASE}(?:\s*,\s*{_BASE})*(?:\s*,?\s*(?:or|nor|and)\s+{_BASE})?"
DENIALS = (
    re.compile(
        rf"\b(?:is|are|was|were|be|been|being|get|gets|got)?\s*(?:not|never|neither|nor)\s+{_LIST_PAST}",
        re.I,
    ),
    re.compile(
        rf"\b(?:does|do|did|will|would|can|cannot|could|shall|should|must)\s+not\s+{_LIST_BASE}",
        re.I,
    ),
    re.compile(
        rf"\b(?:does not|do not|did not|makes no|make no|made no|making no|no)\s+claims?\b.*?\b{_LIST_PAST}",
        re.I,
    ),
    re.compile(rf"\bnever\s+(?:to\s+)?(?:{_BASE}|closes|narrows|prices)\b", re.I),
)
CLAIMS = (
    re.compile(rf"\b{_VERB}\s+(?:the\s+)?(?:S9\s+)?{_NAME}", re.I),
    re.compile(
        rf"{_NAME}\s+(?:is|was|are|were|has been|have been|gets|got|becomes|became|is now|are now)\s+{_PAST}\b",
        re.I,
    ),
    re.compile(rf"{_NAME}(?:\s*\([^)]*\))?\s+{_PAST}\b", re.I),
)
QUOTED = re.compile(r'"[^"\n]*"')
_LIST_ITEM = re.compile(r"^\s*(?:[*-]|\d+\.)\s+")


# ---------------------------------------------------------------------------
# Helpers: files, documents, the ledger, the paper.


def tree_files() -> Iterator[Path]:
    """Every regular file under the tree, skipping dot-directories and caches."""

    for path in sorted(TREE.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(TREE).parts
        if any(part.startswith(".") or part == "__pycache__" for part in relative[:-1]):
            continue
        yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def units(text: str) -> list[str]:
    """Table rows one by one; other lines grouped into paragraphs."""

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


def sentences(unit: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.;!?])\s+", unit) if s.strip()]


def prose_sentences(unit: str) -> list[str]:
    """Period-delimited sentences: a semicolon chain is one sentence here."""

    return [s for s in re.split(r"(?<=[.!?])\s+", unit) if s.strip()]


def strip_denials(sentence: str) -> str:
    for pattern in DENIALS:
        sentence = pattern.sub(" ", sentence)
    return sentence


def protected_claims(text: str) -> list[str]:
    """Sentences that attach close/narrow/price to a protected open."""

    found: list[str] = []
    for unit in units(text):
        for sentence in sentences(unit):
            stripped = strip_denials(sentence)
            if any(pattern.search(stripped) for pattern in CLAIMS):
                found.append(sentence.strip())
    return found


def unmarked_mentions(text: str) -> list[str]:
    """Units mentioning a protected open outside quotes with no marker."""

    found: list[str] = []
    for unit in units(text):
        unquoted = QUOTED.sub(" ", unit)
        if PROTECTED.search(unquoted) and not MENTION_MARKER.search(unit):
            found.append(unit.strip())
    return found


class Row:
    def __init__(self, cells: list[str]) -> None:
        self.id = cells[0]
        self.statement = cells[1]
        self.classification = cells[2] if len(cells) == 4 else None
        self.evidence = cells[-1]

    @property
    def tokens(self) -> list[str]:
        return _TOKEN.findall(self.evidence)

    @property
    def is_claim(self) -> bool:
        return self.classification is not None


def ledger_rows() -> list[Row]:
    rows: list[Row] = []
    for line in read_text(LEDGER).split("\n"):
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or not _ROW_ID.match(cells[0]):
            continue
        if len(cells) not in (3, 4):
            raise AssertionError(f"ledger row {cells[0]} has {len(cells)} cells")
        rows.append(Row(cells))
    return rows


def load_receipt(name: str) -> object:
    payload: object = json.loads((RECEIPTS / f"{name}.json").read_text(encoding="utf-8"))
    return payload


def lookup(obj: object, path: str) -> object:
    """Walk a dotted path with optional ``[n]`` indexes; raise on a miss."""

    for segment in path.split("."):
        match = _SEGMENT.match(segment)
        if match is None:
            raise KeyError(segment)
        key, indexes = match.group(1), match.group(2)
        if not isinstance(obj, dict) or key not in obj:
            raise KeyError(key)
        obj = obj[key]
        for index in re.findall(r"\[(\d+)\]", indexes):
            if not isinstance(obj, list) or int(index) >= len(obj):
                raise KeyError(f"{key}[{index}]")
            obj = obj[int(index)]
    return obj


def test_defs() -> dict[str, set[str]]:
    """Test-module stem -> the names of the test functions it defines."""

    defs: dict[str, set[str]] = {}
    for path in sorted(TREE.glob("test_*.py")):
        names = set(re.findall(r"^\s*def (test_\w+)\(", read_text(path), re.M))
        defs[path.stem] = names
    return defs


def research_lean_theorems() -> dict[str, set[str]]:
    """Module stem -> theorem names declared in lean/S9Obligations/<Module>.lean."""

    out: dict[str, set[str]] = {}
    for path in sorted((TREE / "lean" / "S9Obligations").glob("*.lean")):
        out[path.stem] = set(re.findall(r"^theorem ([A-Za-z_][\w']*)", read_text(path), re.M))
    return out


def sealed_theorems() -> set[str]:
    return set(re.findall(r"^theorem ([A-Za-z_][\w']*)", read_text(SEALED_LEAN), re.M))


def is_lean_token(token: str) -> bool:
    research = _RESEARCH_LEAN_TOKEN.match(token)
    if research is not None:
        return token in verify_lean.AXIOM_REPORT_DECLARATIONS
    sealed = _SEALED_LEAN_TOKEN.match(token)
    return sealed is not None and sealed.group(1) in sealed_theorems()


def bare_lean_theorems() -> set[str]:
    """Every theorem name of this tree's package and of the sealed file, unqualified."""

    names = set(sealed_theorems())
    for module_names in research_lean_theorems().values():
        names |= module_names
    return names


def names_a_lean_theorem(sentence: str, theorems: set[str]) -> bool:
    return any(token in theorems or is_lean_token(token) for token in _TOKEN.findall(sentence))


def carrier_general_prose_violations(
    text: str, theorems: set[str], markers: re.Pattern[str], per_sentence: bool
) -> list[str]:
    """Sentences (or units) with a step-37 phrase, no Lean theorem, no marker."""

    out: list[str] = []
    for unit in units(text):
        for piece in prose_sentences(unit) if per_sentence else [unit]:
            if (
                CARRIER_GENERAL.search(piece)
                and not names_a_lean_theorem(piece, theorems)
                and not markers.search(piece)
            ):
                out.append(piece.strip())
    return out


def proposed_scan_text(text: str) -> str:
    """PROPOSED_S9.md with each diff fence replaced by its ``+`` lines."""

    out: list[str] = []
    inside = False
    for line in text.split("\n"):
        if line.startswith("```diff"):
            inside = True
            out.append("")
        elif line.startswith("```"):
            inside = False
            out.append("")
        elif inside:
            if line.startswith("+") and not line.startswith("+++"):
                out.append(line[1:])
        else:
            out.append(line)
    return "\n".join(out)


def plus_line_units(text: str) -> list[str]:
    """One unit per diff fence: its ``+`` lines joined."""

    fences: list[list[str]] = []
    inside = False
    for line in text.split("\n"):
        if line.startswith("```diff"):
            inside = True
            fences.append([])
        elif line.startswith("```"):
            inside = False
        elif inside and line.startswith("+") and not line.startswith("+++"):
            fences[-1].append(line[1:].strip())
    return [" ".join(fence) for fence in fences if fence]


def unbounded_results(unit: str, theorems: set[str]) -> list[str]:
    """Sentences naming a computed result with neither "bounded" nor a theorem."""

    out: list[str] = []
    for sentence in prose_sentences(unit):
        if (
            RESULT_MARKER.search(CROSS_REFERENCE.sub(" ", sentence))
            and "bounded" not in sentence.lower()
            and not names_a_lean_theorem(sentence, theorems)
        ):
            out.append(sentence.strip())
    return out


def status_registration_diff() -> list[str]:
    """The lines inside the first ```diff fence of STATUS.md."""

    text = read_text(STATUS)
    return text.split("```diff", 1)[1].split("```", 1)[0].strip("\n").split("\n")


def status_section(text: str, heading: str) -> str:
    """The body of the ``## <heading>`` section: up to the next ``## `` line."""

    marker = f"\n## {heading}"
    if marker not in text:
        raise AssertionError(f"STATUS.md has no section {heading!r}")
    body = text.split(marker, 1)[1].split("\n", 1)[1]
    return body.split("\n## ", 1)[0]


def resolve(token: str, defs: dict[str, set[str]], theorems: dict[str, set[str]]) -> str | None:
    """Return None when the token resolves, else the reason it does not."""

    test = _TEST_TOKEN.match(token)
    if test is not None:
        module, name = test.group(1), test.group(2)
        if module is not None:
            return None if name in defs.get(module, set()) else f"no def {name} in {module}.py"
        return None if any(name in names for names in defs.values()) else f"no test def {name}"
    receipt = _RECEIPT_TOKEN.match(token)
    if receipt is not None:
        try:
            lookup(load_receipt(receipt.group(1)), receipt.group(2))
        except KeyError as missing:
            return f"receipt {receipt.group(1)} has no key {missing} along {receipt.group(2)}"
        return None
    research = _RESEARCH_LEAN_TOKEN.match(token)
    if research is not None:
        module, name = research.group(1), research.group(2)
        if token not in verify_lean.AXIOM_REPORT_DECLARATIONS:
            return f"{token} is not in AXIOM_REPORT_DECLARATIONS"
        if name not in theorems.get(module, set()):
            return f"no theorem {name} in lean/S9Obligations/{module}.lean"
        return None
    sealed = _SEALED_LEAN_TOKEN.match(token)
    if sealed is not None:
        return None if sealed.group(1) in sealed_theorems() else f"no sealed theorem {sealed.group(1)}"
    return f"unrecognized evidence token {token!r}"


def paper_s9_bullets() -> list[list[str]]:
    """The bullets of section S9 of the sealed paper, each as its lines."""

    lines = PAPER.read_text(encoding="utf-8").split("\n")
    start = lines.index("## S9. Unresolved obligations")
    bullets: list[list[str]] = []
    for line in lines[start + 1 :]:
        if line.startswith("---") or line.startswith("# "):
            break
        if line.startswith("* "):
            bullets.append([line])
        elif line.startswith("  ") and bullets:
            bullets[-1].append(line)
    return bullets


def paper_f3_lines() -> list[str]:
    lines = PAPER.read_text(encoding="utf-8").split("\n")
    start = next(i for i, line in enumerate(lines) if line.startswith("**F3."))
    out: list[str] = []
    for line in lines[start:]:
        if not line.strip():
            break
        out.append(line)
    return out


def ascii_quote(line: str) -> str:
    """The sealed line as this ASCII-only tree quotes it: em dash as ``--``."""

    return line.replace("\u2014", "--")


def diff_fence_lines(text: str) -> list[str]:
    """The lines inside ```diff fences, in order."""

    out: list[str] = []
    inside = False
    for line in text.split("\n"):
        if line.startswith("```diff"):
            inside = True
        elif line.startswith("```"):
            inside = False
        elif inside:
            out.append(line)
    return out


def legal_terminals() -> list[str]:
    text = read_text(TREE / "PROMPT.md")
    block = text.split("## Legal terminals, each with scope", 1)[1].split("---", 1)[0]
    return re.findall(r"^\s{4}([A-Z0-9_]+)\s*$", block, re.M)


def status_terminal_lines() -> list[str]:
    text = read_text(STATUS)
    block = text.split("## Terminals", 1)[1].split("\n## ", 1)[0]
    return [line for line in block.split("\n") if line.startswith("* `")]


def working_denylist() -> list[str]:
    payload = json.loads(DENYLIST_JSON.read_text(encoding="utf-8"))
    block = payload["denylist"]
    full = block["full_census"]
    subtracted = set(block["subtracted_as_native_or_core"])
    names = [name for name in full if isinstance(name, str) and name not in subtracted]
    if len(names) != 102:
        raise AssertionError(f"working denylist has {len(names)} names, expected 102")
    return names


def denylist_pattern(names: list[str]) -> re.Pattern[str]:
    """The firewall's boundary regex, as one alternation over the names."""

    return re.compile(r"(?<![\w])(?:" + "|".join(re.escape(n) for n in names) + r")(?![\w])")


def external_marker_patterns() -> list[tuple[str, re.Pattern[str]]]:
    """Step 40's markers, built from pieces so this file does not carry them."""

    pieces = {
        "et" + " al": r"\bet\s+" + r"al\b",
        "ar" + "Xiv": "ar" + "xiv",
        "do" + "i:": r"\bdo" + "i:",
        "http" + "://": "http" + "://",
        "https" + "://": "https" + "://",
        "IS" + "BN": r"\bIS" + r"BN\b",
        "Wiki" + "pedia": "wiki" + "pedia",
        # A numeric citation bracket closing a line; an index such as
        # ``parts[1]`` or ``f(x)[0]`` is preceded by a word character, a
        # parenthesis or a bracket and is not one.
        "[n] at line end": r"(?<![\w)\]])\[\d+\]\s*$",
    }
    return [(label, re.compile(pattern, re.I | re.M)) for label, pattern in pieces.items()]


def _marker_exempt_lines(source: str) -> set[int]:
    """Lines of a test module whose string literals hold a marker list."""

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
                for arg in cursor.args:
                    if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name):
                        names.append(arg.func.id)
                if any("marker" in name.lower() for name in names):
                    exempt.add(node.lineno)
            cursor = parents.get(cursor)
    return exempt


def external_marker_hits(path: Path, text: str) -> list[str]:
    exempt = _marker_exempt_lines(text) if path.name.startswith("test_") and path.suffix == ".py" else set()
    hits: list[str] = []
    for lineno, line in enumerate(text.split("\n"), start=1):
        if lineno in exempt:
            continue
        for label, pattern in external_marker_patterns():
            if pattern.search(line):
                hits.append(f"{path.name}:{lineno}: {label}")
    return hits


# ---------------------------------------------------------------------------
# Step 35: sealed paths.


class SealedPathTests(unittest.TestCase):
    def test_sealed_prefix_refusal_on_synthetic_porcelain_lines(self) -> None:
        for line in (
            "?? paper/x.md",
            " M prompt/prompt.md",
            "A  code/derivation/zzz.py",
            " M lean4/Derivation/PrimDiff.lean",
            "?? artifacts/zzz.json",
            "R  paper/a.md -> research/s9_obligations/b.md",
        ):
            self.assertEqual(verify_pins.sealed_prefix_violations(line + "\n"), [line], line)
        self.assertEqual(
            verify_pins.sealed_prefix_violations(
                "?? research/s9_obligations/CLAIM_LEDGER.md\n?? lean4/Zzz.lean\n"
            ),
            [],
        )

    def test_write_root_guard_refuses_every_sealed_prefix_and_the_outside(self) -> None:
        for sealed in ("prompt/x.md", "paper/x.md", "code/x.py", "lean4/Derivation/X.lean", "artifacts/x.json"):
            with self.assertRaisesRegex(ValueError, "refusing to write outside"):
                common.assert_inside_tree(REPO / sealed)
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "r.json"
            with self.assertRaisesRegex(ValueError, "refusing to write outside"):
                common.assert_inside_tree(target)
            with self.assertRaisesRegex(ValueError, "refusing to write outside"):
                common.write_receipt(target, {"never": "written"})
            self.assertFalse(target.exists())
        self.assertTrue(common.assert_inside_tree(TREE / "receipts" / "x.json").is_relative_to(TREE))

    def test_live_sealed_prefixes_carry_no_change(self) -> None:
        self.assertEqual(verify_pins.sealed_prefix_violations(verify_pins._live_porcelain()), [])


# ---------------------------------------------------------------------------
# Step 30: the ledger's evidence resolves.


class LedgerEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = ledger_rows()
        self.defs = test_defs()
        self.theorems = research_lean_theorems()

    def test_ledger_has_rows_with_unique_ids_and_legal_classifications(self) -> None:
        self.assertGreater(len(self.rows), 40)
        ids = [row.id for row in self.rows]
        self.assertEqual(len(ids), len(set(ids)), "duplicate ledger IDs")
        for row in self.rows:
            if row.is_claim:
                self.assertIn(row.classification, CLASSIFICATIONS, row.id)
            self.assertTrue(row.tokens, f"{row.id} names no evidence token")
        for prefix in ("PRE-", "S9-1-", "S9-2-", "S9-3-", "DEC-"):
            self.assertTrue(any(row.id.startswith(prefix) for row in self.rows), prefix)

    def test_every_evidence_token_resolves(self) -> None:
        failures: list[str] = []
        for row in self.rows:
            for token in row.tokens:
                reason = resolve(token, self.defs, self.theorems)
                if reason is not None:
                    failures.append(f"{row.id}: {reason}")
        self.assertEqual(failures, [])

    def test_resolver_rejects_dead_tokens(self) -> None:
        dead = (
            "test_zzz_probe_absent",
            "test_forbidden.test_zzz_probe_absent",
            "axiom_lattice:sweeps.N9.fragments",
            "witness_types:lean_targets[99].residual",
            "S9Obligations.AxiomLattice.zzz_probe_absent",
            "PrimDiff.zzz_probe_absent",
            "zzz_probe_absent",
        )
        for token in dead:
            self.assertIsNotNone(resolve(token, self.defs, self.theorems), token)
        alive = (
            "test_every_evidence_token_resolves",
            "test_forbidden.test_every_evidence_token_resolves",
            "axiom_lattice:sweeps.N4.fragments.PURE.lattice.closure_size",
            "witness_types:lean_targets[3].residual",
            "S9Obligations.AxiomLattice.transfers_iff_has_falsum_clause",
            "PrimDiff.D2_initial_pointed",
        )
        for token in alive:
            self.assertIsNone(resolve(token, self.defs, self.theorems), token)

    def test_bounded_rows_say_bounded(self) -> None:
        for row in self.rows:
            if row.classification == "bounded theorem":
                self.assertIn("bounded", row.statement.lower(), row.id)
            prose = re.sub(r"`[^`]*`", " ", row.statement)
            if row.classification == "finite computation" and re.search(
                r"\bN = \d|\bT = \d|\bcarrier", prose
            ):
                self.assertIn("bounded", prose.lower(), row.id)

    def test_terminal_rows_name_legal_terminals(self) -> None:
        legal = set(legal_terminals())
        self.assertEqual(len(legal), 25)
        seen: set[str] = set()
        for row in self.rows:
            match = re.match(r"^terminal `([A-Z0-9_]+)`", row.statement)
            if match is not None:
                self.assertIn(match.group(1), legal, row.id)
                seen.add(match.group(1))
        self.assertIn("PROPOSED_TEXT_WRITTEN", seen)
        self.assertIn("MANUAL_RECEIPT_DECLARED", seen)
        self.assertIn("OB1_UNCHANGED", seen)


# ---------------------------------------------------------------------------
# Step 36: the protected opens.


class ProtectedOpenTests(unittest.TestCase):
    def test_documents_carry_no_claim_on_a_protected_open(self) -> None:
        for path in SYNTHESIS_DOCUMENTS + FINDINGS:
            self.assertEqual(protected_claims(read_text(path)), [], path.name)

    def test_every_mention_of_a_protected_open_carries_a_marker(self) -> None:
        for path in SYNTHESIS_DOCUMENTS + FINDINGS:
            self.assertEqual(unmarked_mentions(read_text(path)), [], path.name)

    def test_scanners_bite_on_injected_claims_and_stay_quiet_on_denials(self) -> None:
        injections = (
            "This run narrows OB-1.",
            "S6.6 is closed by this run.",
            "The inscription bridge was priced here.",
            "We claim OB-1 closed.",
            "The S9 last bullet is now narrowed.",
            'A quoted claim: "this part closes the S9 last bullet".',
            "OB-1 is not closed here, but this run narrows OB-1 anyway.",
        )
        for text in injections:
            self.assertEqual(len(protected_claims(text)), 1, text)
        quiet = (
            "OB-1 is not closed, narrowed, or priced here.",
            "It does not claim OB-1, S6.6, or the S9 last bullet (the inscription "
            "bridge) closed, narrowed, or priced; they are out of scope.",
            "OB1_UNCHANGED -- this run makes no claim about OB-1.",
            "The bullet was narrowed; OB-1 is out of scope.",
            'a sentence denying one verb and asserting another -- "OB-1 is not '
            'closed here, but this part narrows it anyway" -- was invisible.',
        )
        for text in quiet:
            self.assertEqual(protected_claims(text), [], text)
        self.assertEqual(len(unmarked_mentions("OB-1 is mentioned with no marker here.")), 1)
        self.assertEqual(unmarked_mentions("OB-1 is out of scope here."), [])
        self.assertEqual(unmarked_mentions('the record "OB-1 is not closed here" is quoted.'), [])
        self.assertEqual(len(protected_claims('the record "this part narrows OB-1" is quoted.')), 1)
        self.assertEqual(
            len(unmarked_mentions("| S9-9-99 | OB-1 in a table row | open | `x` |\n| S9-9-98 | fine, UNCHANGED | open | `y` |")),
            1,
        )

    def test_proposed_text_touches_none_of_the_protected_bullets(self) -> None:
        bullets = paper_s9_bullets()
        self.assertEqual(len(bullets), 6)
        minus_lines = [
            line[1:] for line in diff_fence_lines(read_text(PROPOSED))
            if line.startswith("-") and not line.startswith("---")
        ]
        self.assertTrue(minus_lines)
        sixth_first_line = ascii_quote(bullets[5][0])
        self.assertNotIn(sixth_first_line, minus_lines)
        self.assertNotIn(bullets[5][0], minus_lines)
        allowed = {ascii_quote(line) for bullet in bullets[:3] for line in bullet}
        allowed |= {ascii_quote(line) for line in paper_f3_lines()}
        for line in minus_lines:
            self.assertIn(line, allowed, f"'-' line is not a current S9.1-S9.3 or F3 line: {line!r}")
        for bullet in bullets[:3]:
            for line in bullet:
                self.assertIn(ascii_quote(line), minus_lines, line)


# ---------------------------------------------------------------------------
# Step 37: no promotion to a carrier-general claim.


class CarrierGeneralTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = ledger_rows()

    def test_proved_theorem_rows_name_a_lean_theorem(self) -> None:
        for row in self.rows:
            if row.classification == "proved theorem":
                self.assertTrue(any(is_lean_token(t) for t in row.tokens), row.id)

    def test_bounded_rows_with_a_general_phrase_name_a_lean_theorem(self) -> None:
        for row in self.rows:
            if row.classification in ("finite computation", "bounded theorem", "countermodel"):
                if CARRIER_GENERAL.search(row.statement):
                    self.assertTrue(
                        any(is_lean_token(t) for t in row.tokens),
                        f"{row.id} speaks of every carrier without a Lean theorem",
                    )

    def test_phrase_list_bites(self) -> None:
        for phrase in ("for all carriers", "on every carrier", "carrier-general", "on every type"):
            self.assertIsNotNone(CARRIER_GENERAL.search(f"the result holds {phrase}"), phrase)
        self.assertIsNone(CARRIER_GENERAL.search("finite computation, bounded by N = 4"))

    def test_prose_sentences_with_a_general_phrase_name_a_lean_theorem(self) -> None:
        """Step 37 over the synthesis prose: STATUS.md, PROPOSED_S9.md (its
        diff fences read as their ``+`` lines), and per unit P2_FINDINGS.md."""

        theorems = bare_lean_theorems()
        self.assertEqual(
            carrier_general_prose_violations(read_text(STATUS), theorems, OPEN_MARKERS, True), [], "STATUS.md"
        )
        self.assertEqual(
            carrier_general_prose_violations(proposed_scan_text(read_text(PROPOSED)), theorems, OPEN_MARKERS, True),
            [],
            "PROPOSED_S9.md",
        )
        self.assertEqual(
            carrier_general_prose_violations(read_text(FINDINGS[1]), theorems, FINDINGS_MARKERS, False),
            [],
            "P2_FINDINGS.md",
        )

    def test_prose_scanner_bites_and_accepts_a_theorem_or_an_openness_marker(self) -> None:
        theorems = bare_lean_theorems()
        probe = "The admitting sets hold on every carrier by the two theorems above."
        self.assertEqual(carrier_general_prose_violations(probe, theorems, OPEN_MARKERS, True), [probe])
        self.assertEqual(
            carrier_general_prose_violations(
                "The admitting sets hold on every carrier by `admits_primary_exactly`.", theorems, OPEN_MARKERS, True
            ),
            [],
        )
        self.assertEqual(
            carrier_general_prose_violations(
                "A uniform argument was tried.  It holds on every carrier (`PrimDiff.D2_initial_pointed`).",
                theorems,
                OPEN_MARKERS,
                True,
            ),
            [],
        )
        self.assertEqual(
            carrier_general_prose_violations(
                "The lattice over all carriers as an object: no Lean theorem describes it.",
                theorems,
                OPEN_MARKERS,
                True,
            ),
            [],
        )
        two = "The lattice over all carriers is described by `zzz_probe_absent`.  Another sentence."
        self.assertEqual(len(carrier_general_prose_violations(two, theorems, OPEN_MARKERS, True)), 1)
        unit = "* The bounded answer is here.  The carrier-general one is the Lean stage's."
        self.assertEqual(carrier_general_prose_violations(unit, theorems, FINDINGS_MARKERS, False), [])
        self.assertEqual(len(carrier_general_prose_violations(unit, theorems, OPEN_MARKERS, True)), 1)
        fenced = "```diff\n-old text on every carrier\n+new text, bounded by N = 4\n```\nprose on every type here.\n"
        self.assertEqual(carrier_general_prose_violations(proposed_scan_text(fenced), theorems, OPEN_MARKERS, True),
                         ["prose on every type here."])

    def test_proposed_plus_lines_say_bounded_beside_each_computed_result(self) -> None:
        """Definition of done: a proposed sentence that names a computed
        result carries "bounded" or a Lean theorem in that sentence."""

        theorems = bare_lean_theorems()
        fences = plus_line_units(read_text(PROPOSED))
        self.assertEqual(len(fences), 4)
        for fence in fences:
            self.assertEqual(unbounded_results(fence, theorems), [], fence[:80])

    def test_unbounded_result_scanner_bites(self) -> None:
        theorems = bare_lean_theorems()
        bad = "Naming tokens hides nothing but separates renamings.  Fine sentence."
        self.assertEqual(unbounded_results(bad, theorems), ["Naming tokens hides nothing but separates renamings."])
        self.assertEqual(unbounded_results("The closure has 75 elements.", theorems), ["The closure has 75 elements."])
        self.assertEqual(unbounded_results("The closure has 75 elements, bounded by N = 4.", theorems), [])
        self.assertEqual(unbounded_results("In every enumerated space pairs are separated by one question.", theorems),
                         ["In every enumerated space pairs are separated by one question."])
        self.assertEqual(
            unbounded_results("The pair is separated by one question (`S9_3_sep_V2_ANON_separates`).", theorems), []
        )
        self.assertEqual(unbounded_results("A2 with witness types rather than counts.", theorems), [])
        self.assertEqual(
            plus_line_units("```diff\n-a\n+b c\n+d\n```\ntext\n```diff\n+e\n```\n"), ["b c d", "e"]
        )
        # Repair round 2: "interval(s)" is a result word; a section, step,
        # line or row number is a cross-reference, not a result.
        self.assertEqual(
            unbounded_results("So the admitting sets are not intervals.", theorems),
            ["So the admitting sets are not intervals."],
        )
        self.assertEqual(
            unbounded_results("The sets are not intervals, bounded by N = 4 as computed.", theorems), []
        )
        self.assertEqual(unbounded_results("The inspection is in P2_FINDINGS.md section 11.", theorems), [])
        self.assertEqual(unbounded_results("See lines 21-24 and step 13.", theorems), [])
        self.assertEqual(
            unbounded_results("Section 11 lists 16 candidates.", theorems), ["Section 11 lists 16 candidates."]
        )

    def test_status_outcome_and_open_sections_say_bounded_beside_each_computed_result(self) -> None:
        """Definition of done over the two prose sections of STATUS.md that
        state results (repair round 2, after a reviewer found an open item
        naming a count with its bound but not the word); the terminal lines
        have their own test, and the other sections carry report counts,
        hashes, line numbers and test tallies rather than computed results."""

        theorems = bare_lean_theorems()
        text = read_text(STATUS)
        for heading in ("Outcome, one line per bullet", "What stayed open, and why, per part"):
            for unit in units(status_section(text, heading)):
                self.assertEqual(unbounded_results(unit, theorems), [], heading)

    def test_status_section_helper_isolates_one_section(self) -> None:
        text = "# T\n\n## A\n\nfirst.\n\n## B\n\nsecond, 42 items.\n\n## C\n\nthird.\n"
        self.assertEqual(status_section(text, "B").strip(), "second, 42 items.")
        self.assertEqual(status_section(text, "C").strip(), "third.")
        with self.assertRaisesRegex(AssertionError, "no section"):
            status_section(text, "D")
        self.assertEqual(len(unbounded_results(status_section(text, "B"), bare_lean_theorems())), 1)

    def test_status_bounded_results_name_their_bound(self) -> None:
        for line in status_terminal_lines():
            name = re.match(r"^\* `([A-Z0-9_]+)`", line)
            assert name is not None
            if name.group(1) in (
                "S9_1_LATTICE_COMPLETE",
                "S9_1_LATTICE_BOUNDED",
                "S9_2_CLASSES_BOUNDED",
                "S9_3_WITNESS_OBSERVABLE",
                "S9_3_WITNESS_INVISIBLE",
                "F3_SUPPORTED_BOUNDED",
                "PYTHON_ONLY_SCOPE_DECLARED",
            ):
                self.assertIn("bounded", line.lower(), line)
                self.assertRegex(line, r"N = \d", line)


# ---------------------------------------------------------------------------
# Step 38: the F3 test can fail.


class F3CanFailTests(unittest.TestCase):
    def test_classifier_reports_a_nonempty_step11_set_under_the_second_definition(self) -> None:
        table = al.build_table(3)
        eq = al.analyze_fragment(al.EQ_BEARING, table)
        above = lookup(eq, "transfer.TRANSFER_ABOVE_POINT")
        assert isinstance(above, dict)
        f3 = above["f3_set"]
        assert isinstance(f3, dict)
        members = f3["members"]
        assert isinstance(members, list)
        self.assertGreater(int(str(f3["count"])), 0)
        self.assertEqual(len(members), int(str(f3["count"])))
        self.assertTrue(f3["nonempty_by_construction"])
        self.assertTrue(al.f3_terminal(al.EQ_BEARING, al.TRANSFER_ABOVE_POINT, above, 3).startswith("F3_REFUTED"))

    def test_by_construction_empty_definition_alone_is_untested(self) -> None:
        table = al.build_table(3)
        for fragment in al.FRAGMENTS:
            analysis = al.analyze_fragment(fragment, table)
            default = lookup(analysis, "transfer.TRANSFER_ALL_CARRIERS")
            assert isinstance(default, dict)
            f3 = default["f3_set"]
            assert isinstance(f3, dict)
            self.assertEqual(f3["count"], 0)
            self.assertTrue(f3["empty_by_definitional_identity"])
            self.assertTrue(al.f3_terminal(fragment, al.TRANSFER_ALL_CARRIERS, default, 3).startswith("F3_UNTESTED"))
        receipt = load_receipt("axiom_lattice")
        for fragment in al.FRAGMENTS:
            line = lookup(receipt, f"terminals.f3.{fragment}.TRANSFER_ALL_CARRIERS")
            self.assertTrue(str(line).startswith("F3_UNTESTED"), fragment)
        self.assertTrue(str(lookup(receipt, "terminals.f3.EQ_BEARING.TRANSFER_ABOVE_POINT")).startswith("F3_REFUTED"))
        self.assertTrue(str(lookup(receipt, "terminals.f3.PURE.TRANSFER_ABOVE_POINT")).startswith("F3_SUPPORTED_BOUNDED"))

    def test_a_synthetic_nonempty_set_is_reported_nonempty(self) -> None:
        f3: dict[str, object] = {
            "count": 2,
            "members": [{"uses_eq_atom": True}, {"uses_eq_atom": True}],
            "decided_before_the_sweep": {
                "verdict": "nonempty_by_named_generator",
                "named_generator": "r x x -> x = y",
            },
        }
        line = al.f3_terminal(al.EQ_BEARING, al.TRANSFER_ABOVE_POINT, {"f3_set": f3}, 3)
        self.assertTrue(line.startswith("F3_REFUTED"))
        self.assertIn("2 member", line)


# ---------------------------------------------------------------------------
# Step 39: the vocabulary firewall over the whole tree.


class FirewallTests(unittest.TestCase):
    def test_no_working_denylist_identifier_anywhere_in_the_tree(self) -> None:
        names = working_denylist()
        pattern = denylist_pattern(names)
        leaks: list[str] = []
        scanned = 0
        for path in tree_files():
            scanned += 1
            text = read_text(path)
            for match in pattern.finditer(text):
                leaks.append(f"{path.relative_to(TREE).as_posix()}: {match.group(0)}")
        self.assertGreater(scanned, 30)
        self.assertEqual(leaks, [])

    def test_boundary_regex_matches_the_firewall(self) -> None:
        pattern = denylist_pattern(["AaBbToken", "CcDd"])
        self.assertIsNotNone(pattern.search("uses AaBbToken here"))
        self.assertIsNone(pattern.search("AaBbTokenMod"))
        self.assertIsNone(pattern.search("notAaBbToken"))
        self.assertIsNotNone(pattern.search("x.CcDd("))
        names = working_denylist()
        self.assertIsNotNone(denylist_pattern(names).search("see " + names[0] + " here"))
        self.assertIsNone(denylist_pattern(names).search("see " + names[0] + "Suffix here"))


# ---------------------------------------------------------------------------
# Step 40: no external name, citation, or literature marker.


class ExternalNameTests(unittest.TestCase):
    """Mechanical proxy for step 40.  It matches the markers listed in
    ``external_marker_patterns`` and nothing else; the prose rule -- naming
    no external theory, project, or body of literature in any wording --
    is wider than any marker list and stays a manual check."""

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
            external_marker_hits(Path("clean.md"), "a list [1, 2], an index x[0]\nand f(y)[1]\nand z[2]"),
            [],
        )
        url = "https" + "://"
        exempt_probe = 'EXTERNAL_MARKERS = ("' + url + '",)\nself.assertEqual(marker_scan("x"), ["' + url + '"])\n'
        self.assertEqual(external_marker_hits(Path("test_probe.py"), exempt_probe), [])
        self.assertTrue(external_marker_hits(Path("probe.py"), 'EXTERNAL_MARKERS = ("' + url + '",)\n'))
        self.assertTrue(external_marker_hits(Path("test_probe.py"), 'X = ("' + url + '",)\n'))
        self.assertTrue(external_marker_hits(Path("test_probe.py"), 'Y = "' + url + '"\n'))


# ---------------------------------------------------------------------------
# Steps 29 and 31: the manual receipt, the terminals, and the census.


class StatusTests(unittest.TestCase):
    def test_manual_receipt_sentence_is_in_status_in_those_words(self) -> None:
        text = read_text(STATUS)
        self.assertIn("This tree's axiom reports are a manual receipt", text)
        self.assertIn("No CI gate reads them", text)

    def test_no_workflow_step_names_this_tree(self) -> None:
        """Documents MANUAL_RECEIPT_DECLARED: registration has not happened.
        This test is expected to need updating on the day the tree is
        registered; until then a green run says the reports are unread."""

        self.assertNotIn("s9_obligations", read_text(WORKFLOW))

    def test_status_registration_diff_matches_the_workflow_shape(self) -> None:
        added = [line[1:] for line in status_registration_diff() if line.startswith("+") and not line.startswith("+++")]
        block = "\n".join(added)
        self.assertIn("run: python research/s9_obligations/verify_pins.py", block)
        self.assertIn("working-directory: research/s9_obligations", block)
        self.assertIn('python -m unittest discover -s . -p "test_*.py"', block)
        self.assertIn("run: python -m mypy", block)
        self.assertIn("PYTHONPATH: ${{ github.workspace }}/code", block)
        for line in added:
            if "run:" in line:
                self.assertNotIn("verify_lean", line, "the registration must not run the Lean build")

    def test_status_registration_diff_is_anchored_to_the_workflow(self) -> None:
        """Step 31's "exact registration diff": a unified diff whose context
        lines are the workflow's own lines at the numbers the hunk names,
        with no line removed and the workflow itself untouched."""

        lines = status_registration_diff()
        self.assertEqual(lines[0], "--- a/.github/workflows/verify.yml")
        self.assertEqual(lines[1], "+++ b/.github/workflows/verify.yml")
        hunk = _HUNK.match(lines[2])
        self.assertIsNotNone(hunk, lines[2])
        assert hunk is not None
        old_start, old_count, new_start, new_count = (int(hunk.group(i)) for i in range(1, 5))
        self.assertEqual(old_start, new_start)
        body = lines[3:]
        self.assertTrue(all(line[:1] in (" ", "+") for line in body), "a registration removes nothing")
        context = [line[1:] for line in body if line.startswith(" ")]
        added = [line for line in body if line.startswith("+")]
        self.assertEqual(len(context), old_count)
        self.assertEqual(len(context) + len(added), new_count)
        workflow = read_text(WORKFLOW).rstrip("\n").split("\n")
        self.assertEqual(workflow[old_start - 1 : old_start - 1 + old_count], context)
        self.assertEqual(old_start - 1 + old_count, len(workflow), "the hunk ends at the workflow's last line")
        self.assertTrue(any("s9_obligations" in line for line in added))
        self.assertEqual([line for line in workflow if "s9_obligations" in line], [])

    def test_status_terminals_are_legal_and_scoped(self) -> None:
        legal = set(legal_terminals())
        lines = status_terminal_lines()
        self.assertGreater(len(lines), 20)
        names: set[str] = set()
        for line in lines:
            match = re.match(r"^\* `([A-Z0-9_]+)` -- (.+)$", line)
            self.assertIsNotNone(match, line)
            assert match is not None
            self.assertIn(match.group(1), legal, line)
            self.assertGreater(len(match.group(2)), 20, line)
            names.add(match.group(1))
        for required in (
            "OB1_UNCHANGED",
            "S66_UNCHANGED",
            "S9_LAST_UNCHANGED",
            "PROPOSED_TEXT_WRITTEN",
            "MANUAL_RECEIPT_DECLARED",
            "LEAN_CARRIED",
            "LEAN_NOT_CARRIED",
            "REFUSED",
        ):
            self.assertIn(required, names)
        self.assertNotIn("S9_1_TRANSFER_OPEN", names)
        self.assertNotIn("S9_2_INTERVAL_SHAPE", names)

    def test_status_records_the_prompt_blob_and_snapshot_commit(self) -> None:
        text = read_text(STATUS)
        self.assertIn(common.PROMPT_BLOB_ID, text)
        self.assertIn(common.SNAPSHOT_COMMIT, text)
        manifest = verify_pins.read_manifest()
        self.assertEqual(manifest["prompt"]["blob"], common.PROMPT_BLOB_ID)

    def test_lean_root_imports_every_report_module_and_the_scan_sees_them(self) -> None:
        root = read_text(TREE / "lean" / "S9Obligations.lean")
        imported = set(re.findall(r"^import S9Obligations\.(\w+)", root, re.M))
        modules = {
            name.split(".")[1] for name in verify_lean.AXIOM_REPORT_DECLARATIONS
        }
        self.assertEqual(modules, imported)
        scanned = {path.stem for path in verify_lean.research_lean_sources()}
        for module in imported:
            self.assertTrue((TREE / "lean" / "S9Obligations" / f"{module}.lean").is_file(), module)
            self.assertIn(module, scanned)
        theorems = research_lean_theorems()
        for name in verify_lean.AXIOM_REPORT_DECLARATIONS:
            _, module, short = name.split(".")
            self.assertIn(short, theorems[module], name)

    def test_proposed_document_states_it_is_a_proposal(self) -> None:
        text = read_text(PROPOSED)
        flat = " ".join(text.split())
        self.assertIn("proposal", flat.lower())
        self.assertIn("the sealed paper is not edited by this run", flat)
        for heading in ("## S9.1", "## S9.2", "## S9.3", "## F3"):
            self.assertIn(heading, text)
        self.assertIn("```diff", text)

    def test_synthesis_files_are_ascii_and_lf_only(self) -> None:
        for path in SYNTHESIS_DOCUMENTS + (Path(__file__),):
            raw = path.read_bytes()
            self.assertNotIn(b"\r", raw, path.name)
            raw.decode("ascii")


if __name__ == "__main__":
    unittest.main()
