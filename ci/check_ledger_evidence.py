"""Evidence gate for the claim ledger.

Usage: python ci/check_ledger_evidence.py

Every ``CL-*`` entry in ``paper/paper_claim_ledger.md`` names its machine
evidence in **Python** / **Lean** / **Evidence** fields.  Nothing checked
that those names still exist: a theorem could be renamed, a test deleted,
or an artifact key restructured, and the ledger would keep citing the old
name.  This gate resolves every backticked token in an evidence field
against the thing it names.

The raw population and the classifier are defined SEPARATELY, on the model
of ``ci/check_transport_citations.py``.  The population is arithmetic --
half the backtick count of each evidence-field chunk -- and never mentions
the token pattern, so a token the classifier cannot see fails totality
instead of cancelling out on both sides of the comparison.  An odd
backtick count in a chunk fails by itself.

Resolution, by field side:

* Lean-side tokens resolve against ``artifacts/lean_axioms.txt`` first.
  NAMESPACE MATCHING, decided explicitly: exact match on the quoted
  report name, then SUFFIX match on a dot boundary (token ``name``
  matches report ``Anything.name``).  The suffix match is REQUIRED, not
  a convenience: the kernel entries cite ``supply_no_op`` while every
  artifact report is fully qualified (``Derivation.supply_no_op``).  Its
  price is documented ambiguity -- the ledger cites
  ``refusal_object_inert``, which exists in two namespaces
  (``Completion.``, ``PrimitivePassage.``), and a suffix match proves
  EXISTENCE of some report, never identity of the intended one.  A
  leading-dot token (``.act_id``) strips the dot first.  A name in
  neither place falls through to a Lean source declaration index over
  ``lean4/Derivation/**/*.lean`` (theorem/def/abbrev/structure/
  inductive/instance/class heads, plus constructor alternatives
  ``| name`` -- ``admitTok`` is a constructor), matched on its final
  segment; that tier certifies a declaration exists, NOT that it carries
  an axiom report.  ``Namespace.*`` is a wildcard family and needs at
  least one report under that prefix -- nonemptiness only, never the
  prose counts ("all 32", "seven") stated alongside.

* Python-side tokens resolve as: ``file.json:dotted.key.path`` (walked
  through the parsed JSON, ``*`` segments end the walk, `` = value`` and
  ``: value`` suffixes are annotation, not path); pytest paths
  ``file::test_name`` or bare ``::test_name``; ``def test_*(`` names in
  ``tests/*.py``; top-level ``def`` names in ``code/`` and ``ci/``; file
  or directory paths (tried as given, then under the known roots);
  nested key occurrence in any artifact JSON; literal substring in
  artifact JSON text (collision-cell row labels such as
  ``observer_placement (H1)`` are list VALUES, not keys); literal
  substring in Python sources (``terminal_no_response`` is a status
  string whose evidential content is its ABSENCE from every export).
  Each tier is strictly weaker than the one before it, and the summary
  counts per tier so a drift toward the weak tiers is visible.

* A token shaped like a claim ID (``CL-FR6-T*``) on either side is a
  CROSS-REFERENCE to other ledger entries, not a theorem or test name.
  It resolves against the set of ``### CL-*`` headings: an exact ID must
  be an entry, a ``*``/``?`` glob must match at least one.  (Today the
  ledger writes such family references in unbackticked prose, so this
  tier is exercised zero times; it exists so a future backticked family
  reference is classified honestly instead of failing as a fake theorem
  or passing as a substring.)

A small pinned allowlist admits meta tokens that name apparatus rather
than evidence (``#print axioms``, ``rfl``, core type names, and the
none-marker ``--``, which the ledger never backticks today).  Everything
else that resolves nowhere is an unresolved citation and fails, naming
the entry, the ledger line, and the token.

The gate cannot tell a live citation from a historical mention: an
evidence field that backticks a deliberately dead name (a renamed
theorem, a stale filename) fails here, and the fix is to move the old
name out of backticks or out of the evidence field -- the same rule
``ci/check_paper_citations.py`` states for dead paper paths.  Statement,
Falsifier, and Axioms fields are out of scope on purpose: statements may
quote withdrawn names as history, and axiom names are audited by
``ci/check_lean_audit.py``.
"""

from __future__ import annotations

import fnmatch
import json
import pathlib
import re
import sys
from dataclasses import dataclass

LEDGER = pathlib.Path("paper") / "paper_claim_ledger.md"
AXIOMS = pathlib.Path("artifacts") / "lean_axioms.txt"
LEAN_DIR = pathlib.Path("lean4") / "Derivation"
TESTS_DIR = pathlib.Path("tests")
CODE_DIRS = (pathlib.Path("code"), pathlib.Path("ci"))
ARTIFACT_DIRS = (pathlib.Path("artifacts"), pathlib.Path("contact") / "analysis")
PATH_ROOTS = (
    pathlib.Path("."),
    pathlib.Path("tests"),
    pathlib.Path("code"),
    pathlib.Path("code") / "derivation",
    pathlib.Path("artifacts"),
    pathlib.Path("artifacts") / "full",
    pathlib.Path("contact") / "analysis",
    pathlib.Path("lean4"),
    pathlib.Path("paper"),
)

ENTRY = re.compile(r"^### (?P<id>CL-[A-Za-z0-9-]+)")
# An evidence field opens at one of these bold keys.  The Lean side and the
# Python side resolve differently, so the side is carried with the chunk.
LEAN_FIELDS = ("Lean", "Evidence", "Evidence (Lean)")
FIELD_OPEN = re.compile(
    r"\*\*(?P<key>Python|Lean|Evidence|Evidence \(Lean\)|Python evidence|"
    r"Python / Lean / Axioms)\*\*:"
)
# Any bold key closes an open field (Axioms, Falsifier, Class, Deps, ...).
FIELD_ANY = re.compile(r"\*\*[A-Z][^*\n]*\*\*:")
# The classifier's token pattern.  The population count NEVER uses it.
TOKEN = re.compile(r"`([^`]+)`", re.S)

REPORT = re.compile(
    r"^Derivation\.lean:\d+:\d+: '(?P<name>[^']+)' "
    r"(?:depends on axioms: \[[^\]]*\]|does not depend on any axioms)"
)
DECL = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
    r"(?:theorem|lemma|def|abbrev|structure|inductive|instance|class)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_.']*)"
)
# Constructor alternatives.  Over-broad on purpose (it also matches match
# arms); this is an existence index, and a name only reachable as a match
# arm is a name the sources really contain.
CTOR = re.compile(r"^\s*\|\s*\.?(?P<name>[A-Za-z_][A-Za-z0-9_']*)")
TESTDEF = re.compile(r"^def (?P<name>test_\w+)\(", re.M)
CODEDEF = re.compile(r"^def (?P<name>\w+)", re.M)
ARTKEY = re.compile(
    r"^(?P<file>[\w./-]+\.json(?:\.gz)?):(?P<path>[^=]+?)(?:\s*=\s.*)?$"
)
PATHLIKE = re.compile(r"^[\w./-]+(?:\.py|\.lean|\.md|\.json|\.json\.gz|\.txt|/)$")
VALUE_SUFFIX = re.compile(r"^(?P<key>[\w.*-]+(?:\s*->\s*[\w.*-]+)?)\s*[:=]\s+\S.*$")
CLAIM_REF = re.compile(r"^CL-[A-Za-z0-9*?-]+$")

# Meta tokens: apparatus named inside an evidence field, not evidence.
# Pinned exactly; growing this list is a reviewed change, not a reflex.
META = frozenset(
    {
        "#print axioms",
        "propext",
        "Quot.sound",
        "{propext, Quot.sound}",
        "Classical.choice",
        "rfl",
        "Option",
        "Bool",
        "Nat",
        "Prop",
        "wit",
        "prot",
        "obs",
        "Metatheory",
        "--",
    }
)


@dataclass(frozen=True)
class Token:
    entry: str
    side: str  # "lean" or "python"
    line: int  # ledger line of the field opener
    raw: str  # token text as written (may contain a wrapped newline)
    norm: str  # normalized: wrap joined, whitespace collapsed


@dataclass(frozen=True)
class Verdict:
    token: Token
    category: str  # lean-theorem / lean-decl / lean-family / test-name /
    #                artifact-key / artifact-subkey / artifact-literal /
    #                module-path / code-def / code-literal / cross-reference /
    #                meta / UNRESOLVED
    detail: str


def normalize(raw: str) -> str:
    """Join a line-wrapped token.  The ledger wraps mid-identifier, so the
    newline and its indent are removed with NO joining space."""
    return re.sub(r"\n\s*", "", raw).strip()


def evidence_chunks(text: str) -> list[tuple[str, str, int, str]]:
    """Return (entry, side, opener_line, chunk_text) for every evidence
    field of every CL-* entry.  The legend above the first entry is out of
    scope.  A chunk closes at the next bold key, the next heading, or a
    rule line."""
    chunks: list[tuple[str, str, int, str]] = []
    lines = text.splitlines()
    entry: str | None = None
    i = 0
    while i < len(lines):
        line = lines[i]
        m = ENTRY.match(line)
        if m:
            entry = m.group("id")
            i += 1
            continue
        if entry is None:
            i += 1
            continue
        opened = list(FIELD_OPEN.finditer(line))
        if not opened:
            i += 1
            continue
        for fm in opened:
            key = fm.group("key")
            side = "lean" if key in LEAN_FIELDS else "python"
            start = fm.end()
            # Close on the same line if another bold key follows.
            later = FIELD_ANY.search(line, start)
            if later is not None:
                chunks.append((entry, side, i + 1, line[start : later.start()]))
                continue
            # Otherwise the chunk runs over following lines.
            body = [line[start:]]
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                if nxt.startswith("#") or nxt.startswith("---"):
                    break
                stop = FIELD_ANY.search(nxt)
                if stop is not None:
                    body.append(nxt[: stop.start()])
                    break
                body.append(nxt)
                j += 1
            chunks.append((entry, side, i + 1, "\n".join(body)))
            break
        i += 1
    return chunks


def population(chunks: list[tuple[str, str, int, str]]) -> tuple[int, list[str]]:
    """The raw population: half the backtick count of every chunk.  This is
    arithmetic on the text and never consults TOKEN, so a token the
    classifier drops fails totality rather than vanishing from both
    sides.  Odd counts are reported as their own failure."""
    total = 0
    odd: list[str] = []
    for entry, _side, line, chunk in chunks:
        ticks = chunk.count("`")
        if ticks % 2:
            odd.append(f"  {LEDGER}:{line}: {entry}: unbalanced backticks")
        total += ticks // 2
    return total, odd


def load_axiom_names() -> frozenset[str]:
    names = set()
    for line in AXIOMS.read_text(encoding="utf-8").splitlines():
        m = REPORT.match(line)
        if m:
            names.add(m.group("name"))
    return frozenset(names)


def load_lean_decls() -> frozenset[str]:
    names = set()
    for path in sorted(LEAN_DIR.rglob("*.lean")):
        for line in path.read_text(encoding="utf-8").splitlines():
            m = DECL.match(line) or CTOR.match(line)
            if m:
                names.add(m.group("name").split(".")[-1])
    return frozenset(names)


def load_test_defs() -> frozenset[str]:
    names = set()
    for path in sorted(TESTS_DIR.glob("*.py")):
        names.update(TESTDEF.findall(path.read_text(encoding="utf-8")))
    return frozenset(names)


def load_code_defs() -> frozenset[str]:
    names = set()
    for root in CODE_DIRS:
        for path in sorted(root.rglob("*.py")):
            names.update(CODEDEF.findall(path.read_text(encoding="utf-8")))
    return frozenset(names)


def load_artifacts() -> tuple[dict[str, object], frozenset[str], str]:
    """Parsed JSON per artifact basename, the nested key index, and the
    concatenated raw text for the literal tier."""
    parsed: dict[str, object] = {}
    keys: set[str] = set()
    raw: list[str] = []

    def walk(obj: object) -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                keys.add(key)
                walk(value)
        elif isinstance(obj, list):
            for value in obj:
                walk(value)

    for root in ARTIFACT_DIRS:
        for path in sorted(root.glob("*.json")):
            text = path.read_text(encoding="utf-8")
            raw.append(text)
            data = json.loads(text)
            parsed[path.name] = data
            walk(data)
    return parsed, frozenset(keys), "\n".join(raw)


def resolve_artifact_key(token: str, parsed: dict[str, object]) -> str | None:
    """Resolve ``file.json:dotted.path``; None on success, reason on
    failure.  Wildcard segments end the walk (everything up to the first
    ``*`` is verified).  A trailing `` = value`` is annotation, not path."""
    m = ARTKEY.match(token)
    assert m is not None
    fname = pathlib.Path(m.group("file")).name
    if fname.endswith(".json.gz"):
        # Compressed exports are opaque here; existence is the claim.
        for root in ARTIFACT_DIRS + (pathlib.Path("artifacts") / "full",):
            if (root / fname).exists():
                return None
        return f"no artifact file {fname}"
    if fname not in parsed:
        return f"no artifact file {fname}"
    node: object = parsed[fname]
    walked: list[str] = []
    segments = m.group("path").strip().split(".")
    for i, seg in enumerate(segments):
        if "*" in seg:
            return None
        if isinstance(node, dict):
            if seg in node:
                node = node[seg]
                walked.append(seg)
                continue
            rest = ".".join(segments[i:])
            if rest in node:  # a key that itself contains dots
                return None
        at = ".".join(walked) or "top level"
        return f"{fname} has no key {seg!r} under {at}"
    return None


def resolve_path(token: str) -> bool:
    cleaned = token.rstrip("/")
    for root in PATH_ROOTS:
        if (root / cleaned).exists():
            return True
    return False


def resolve_claim_ref(token: str, entry_ids: frozenset[str]) -> Verdict | None:
    """A CL-*-shaped token is a cross-reference to other ledger entries,
    never a theorem or test name.  Exact IDs must exist; a glob must match
    at least one entry.  Returns None when the token is not claim-shaped."""
    if not CLAIM_REF.match(token):
        return None
    if "*" in token or "?" in token:
        hits = sorted(e for e in entry_ids if fnmatch.fnmatchcase(e, token))
        if hits:
            return Verdict(
                Token("", "", 0, token, token),
                "cross-reference",
                f"{len(hits)} entr(ies)",
            )
        return Verdict(
            Token("", "", 0, token, token),
            "UNRESOLVED",
            f"no CL- entry matches {token}",
        )
    if token in entry_ids:
        return Verdict(Token("", "", 0, token, token), "cross-reference", token)
    return Verdict(
        Token("", "", 0, token, token),
        "UNRESOLVED",
        f"no CL- entry named {token}",
    )


def classify(
    tok: Token,
    entry_ids: frozenset[str],
    axioms: frozenset[str],
    decls: frozenset[str],
    tests: frozenset[str],
    codedefs: frozenset[str],
    parsed: dict[str, object],
    art_keys: frozenset[str],
    art_text: str,
    code_text: str,
) -> Verdict:
    t = tok.norm
    if t in META:
        return Verdict(tok, "meta", t)
    ref = resolve_claim_ref(t, entry_ids)
    if ref is not None:
        return Verdict(tok, ref.category, ref.detail)

    if tok.side == "lean":
        name = t.lstrip(".")
        if name.endswith(".*") or name.endswith("_*"):
            prefix = name[:-1]
            hits = sum(
                1
                for a in axioms
                if a == prefix or a.startswith(prefix) or ("." + prefix) in a
            )
            if hits:
                return Verdict(tok, "lean-family", f"{hits} report(s)")
            return Verdict(tok, "UNRESOLVED", f"no axiom report matches {t}")
        if name in axioms:
            return Verdict(tok, "lean-theorem", "exact")
        if any(a.endswith("." + name) for a in axioms):
            return Verdict(tok, "lean-theorem", "suffix")
        if PATHLIKE.match(t) and resolve_path(t):
            return Verdict(tok, "module-path", t)
        if name.split(".")[-1] in decls:
            return Verdict(tok, "lean-decl", "declared, no axiom report")
        return Verdict(
            tok,
            "UNRESOLVED",
            "not in artifacts/lean_axioms.txt and not declared in "
            "lean4/Derivation sources",
        )

    # Python side.
    if ARTKEY.match(t):
        reason = resolve_artifact_key(t, parsed)
        if reason is None:
            return Verdict(tok, "artifact-key", t.split(":", 1)[0])
        return Verdict(tok, "UNRESOLVED", reason)
    if "::" in t:
        name = t.rsplit("::", 1)[-1]
        if name in tests:
            return Verdict(tok, "test-name", name)
        return Verdict(tok, "UNRESOLVED", f"no test def {name} in tests/")
    if t in tests:
        return Verdict(tok, "test-name", t)
    if PATHLIKE.match(t):
        if resolve_path(t):
            return Verdict(tok, "module-path", t)
        return Verdict(tok, "UNRESOLVED", f"path {t} does not exist")
    stripped = t
    vm = VALUE_SUFFIX.match(t)
    if vm is not None:
        stripped = vm.group("key")
    if stripped in codedefs:
        return Verdict(tok, "code-def", stripped)
    lead = stripped.split(".")[0].split(" ")[0].rstrip("*").rstrip("_")
    if stripped in art_keys or lead in art_keys:
        return Verdict(tok, "artifact-subkey", stripped)
    if "*" in stripped:
        probe = stripped.replace("*", "")
        if probe and probe in art_text:
            return Verdict(tok, "artifact-literal", f"wildcard {stripped}")
    if stripped in art_text or t in art_text:
        return Verdict(tok, "artifact-literal", stripped)
    if stripped in code_text:
        return Verdict(tok, "code-literal", stripped)
    return Verdict(
        tok,
        "UNRESOLVED",
        "matches no test, code def, artifact key, artifact text, or "
        "source literal",
    )


def main() -> int:
    for required in (LEDGER, AXIOMS, LEAN_DIR, TESTS_DIR):
        if not required.exists():
            print(f"FAIL: {required} not found")
            return 1
    text = LEDGER.read_text(encoding="utf-8")
    entry_ids = frozenset(
        m.group("id") for m in (ENTRY.match(ln) for ln in text.splitlines()) if m
    )
    chunks = evidence_chunks(text)
    entries = {entry for entry, _s, _l, _c in chunks}
    if not chunks or not entries or not entry_ids:
        print(f"FAIL: no evidence fields found in {LEDGER} - the parser is broken")
        return 1

    expected, odd = population(chunks)
    if odd:
        print(f"FAIL: {len(odd)} chunk(s) with unbalanced backticks")
        for row in odd:
            print(row)
        return 1
    if expected == 0:
        print(f"FAIL: zero evidence tokens in {LEDGER} - the population is broken")
        return 1

    axioms = load_axiom_names()
    if not axioms:
        print(f"FAIL: no reports parsed from {AXIOMS}")
        return 1
    decls = load_lean_decls()
    tests = load_test_defs()
    codedefs = load_code_defs()
    parsed, art_keys, art_text = load_artifacts()
    code_text = "\n".join(
        p.read_text(encoding="utf-8")
        for root in CODE_DIRS
        for p in sorted(root.rglob("*.py"))
    )

    tokens: list[Token] = []
    for entry, side, line, chunk in chunks:
        for m in TOKEN.finditer(chunk):
            tokens.append(Token(entry, side, line, m.group(1), normalize(m.group(1))))

    # Totality: the arithmetic population against what the classifier will
    # actually judge.  Backtick pairs the TOKEN pattern cannot see fail
    # here instead of disappearing.
    if len(tokens) != expected:
        print(
            f"FAIL: token enumeration is not total: {expected} backtick "
            f"pair(s), {len(tokens)} token(s) extracted"
        )
        return 1

    verdicts = [
        classify(t, entry_ids, axioms, decls, tests, codedefs, parsed,
                 art_keys, art_text, code_text)
        for t in tokens
    ]
    failures = [v for v in verdicts if v.category == "UNRESOLVED"]
    if failures:
        print(f"FAIL: {len(failures)} unresolved evidence citation(s) in {LEDGER}")
        for v in failures:
            print(
                f"  {LEDGER}:{v.token.line}: {v.token.entry} "
                f"[{v.token.side}] `{v.token.norm}`: {v.detail}"
            )
        return 1
    counts: dict[str, int] = {}
    for v in verdicts:
        counts[v.category] = counts.get(v.category, 0) + 1
    summary = ", ".join(f"{counts[k]} {k}" for k in sorted(counts))
    print(
        f"ledger evidence resolves: {len(tokens)} token(s) across "
        f"{len(entries)} entr(ies): {summary}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
