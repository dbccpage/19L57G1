"""Evidence gate for the claim ledger.

Usage: python ci/check_ledger_evidence.py [--ledger PATH]

``--ledger`` (and the ``ledger`` parameter of ``main``) reads another copy
of the ledger.  It exists for tests and injection only; the gate's own
run takes no argument and reads ``paper/paper_claim_ledger.md``.

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
  EXISTENCE of some report, never identity of the intended one.  [That
  example is WITHDRAWN 2026-09-18; see the note below.]  A
  leading-dot token (``.act_id``) strips the dot first.  A name in
  neither place falls through to a Lean source declaration index over
  ``lean4/Derivation/**/*.lean`` (theorem/def/abbrev/structure/
  inductive/instance/class heads, plus constructor alternatives
  ``| name`` -- ``admitTok`` is a constructor), matched on its final
  segment; that tier certifies a declaration exists, NOT that it carries
  an axiom report.  ``Namespace.*`` is a wildcard family and needs at
  least one report under that prefix -- nonemptiness only, never the
  prose counts ("all 32", "seven") stated alongside.

  Note, 2026-09-18.  The ``refusal_object_inert`` example above is
  WITHDRAWN: the ledger no longer cites that name bare.  It writes
  ``Completion.refusal_object_inert`` and
  ``PrimitivePassage.refusal_object_inert``, and each matches its own
  report.  The example is kept above, marked rather than rewritten.  The
  price it described was real, and it had a live instance the gate
  counted as a strong pass.  CL-PROGRESS cites bare ``getD_append_lt``,
  and in context that means the theorem in ``Progress.lean``.  That
  theorem has no report.  The only report is
  ``Attachment.getD_append_lt``, a different theorem in
  ``Attachment.lean`` with the same final segment, and the suffix match
  counted it as ``lean-theorem``.  Resolution is by final name segment,
  so two weaker results are now split out of the passes and counted on
  their own:

  - ``lean-ambiguous``: a dot-free Lean-side token whose final segment is
    declared more than once under ``lean4/Derivation``, or that matches
    more than one report.  The gate cannot say which declaration is meant.
    ``getD_append_lt`` is one.  ``admitTok`` is the other: it is a
    constructor of the event types in both ``Refusal.lean`` and
    ``Represented.lean``.
  - ``lean-theorem-unreported``: a token that resolves only at the
    declaration tier while a candidate's head is ``theorem`` or
    ``lemma``.  It names a theorem with no ``#print axioms`` report.

  Ambiguity is decided first, so a token is never counted in both.  Both
  populations are pinned exactly, by (entry id, token), in
  ``PINNED_AMBIGUOUS`` and ``PINNED_UNREPORTED``.  The pins fail in both
  directions.  A new member fails with its entry, ledger line, token, and
  every candidate.  A pinned member that no longer classifies that way
  fails as a stale pin.  The pins record residuals, not a repair.
  Qualifying the ledger's citations would write ``paper/``.  Adding the
  missing reports would write ``lean4/Derivation.lean`` and
  ``artifacts/lean_axioms.txt``.  All three are sealed, so the residuals
  are recorded here and not closed.

  How declarations are counted, measured rather than assumed.  The
  existence index above stays over-broad and unchanged.  The COUNT uses a
  stricter scan: Lean comments are stripped, and a ``|`` line counts as a
  constructor only inside an ``inductive`` block.  The over-broad
  patterns count match arms and doc-comment lines as declarations.  With
  them, ``newRuleAll`` (one constructor, and 23 more ``|`` lines that are
  match arms) came out ambiguous.  The count decides only the two new
  verdicts.  It moves nothing to ``UNRESOLVED``, because existence is
  still read from the over-broad index.  At ``827bf983``, every citation
  that resolved at the declaration tier also had at least one declaration
  in the counted index, so each one's head keyword was known.

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

import argparse
import fnmatch
import json
import pathlib
import re
import sys
from collections.abc import Mapping, Sequence
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

#: Prefix-agnostic, deliberately.  This was anchored `^Derivation\.lean:`,
#: which was true while one root emitted every report.  `lean4/ParkedAudit.lean`
#: is a second root, so the anchored form saw 1424 of the artifact's 1472
#: names and every parked theorem was invisible here -- a ledger entry citing
#: one would miss the strong `lean-theorem` tier and fall through to the
#: bare-name file scan, while this gate still printed success.
#:
#: Every other reader of this artifact is already prefix-agnostic
#: (`check_axiom_report.normalize`, `regen_axiom_artifact.REPORT`,
#: `completion.parse_axiom_reports`, `tests/test_axiom_artifact_bytes`), so
#: this was the lone disagreeing parser -- the same one-artifact-two-parsers
#: shape as the 2026-08-18 primed-name defect this file's own docstring
#: narrates.
REPORT = re.compile(
    r"^[^\s:]+\.lean:\d+:\d+: '(?P<name>.+?)' "
    r"(?:depends on axioms: \[[^\]]*\]|does not depend on any axioms)"
)
DECL = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
    r"(?P<head>theorem|lemma|def|abbrev|structure|inductive|instance|class)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_.']*)"
)
# Constructor alternatives.  Over-broad on purpose (it also matches match
# arms); this is an existence index, and a name only reachable as a match
# arm is a name the sources really contain.
CTOR = re.compile(r"^\s*\|\s*\.?(?P<name>[A-Za-z_][A-Za-z0-9_']*)")
# The COUNTED index (2026-09-18) is stricter than the existence index: it
# reads comment-stripped lines, and it takes ``|`` alternatives only inside
# an ``inductive`` block, every alternative on the line (``| t0 | t1``).
CTOR_ALT = re.compile(r"(?:^|\s)\|\s*\.?(?P<name>[A-Za-z_][A-Za-z0-9_']*)")
#: Declaration heads that make a decl-tier citation a theorem citation.
THEOREM_HEADS = frozenset({"theorem", "lemma"})
#: Head recorded for an alternative of an ``inductive``.
CONSTRUCTOR = "constructor"
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

#: ``lean-ambiguous`` citations, frozen 2026-09-18 at ``827bf983`` as the
#: implemented rule finds them.  Keyed by (entry id, token as written).
#: ``getD_append_lt`` is declared in Attachment.lean and in Progress.lean,
#: and only the Attachment one has a report.  ``admitTok`` is a constructor
#: in Refusal.lean and in Represented.lean.  Equality, not a ceiling: a new
#: member fails, and so does a member that no longer classifies this way.
PINNED_AMBIGUOUS: frozenset[tuple[str, str]] = frozenset(
    {
        ("CL-PROGRESS", "getD_append_lt"),
        ("CL-RP-PRODUCTIVITY", "admitTok"),
    }
)

#: ``lean-theorem-unreported`` citations, frozen 2026-09-18 at
#: ``827bf983``.  Each is a ``theorem`` declared once under
#: ``lean4/Derivation`` with no line in ``artifacts/lean_axioms.txt``, so
#: its axioms are unreported.  Same equality rule as above.
PINNED_UNREPORTED: frozenset[tuple[str, str]] = frozenset(
    {
        ("CL-PROGRESS", "derivable_extend"),
        ("CL-PROGRESS", "getD_concat_self"),
        ("CL-TOKEN-ERASURE", "insertNew_of_mem"),
        ("CL-TOKEN-ERASURE", "insertNew_of_not_mem"),
        ("CL-TOKEN-ERASURE", "mem_insertNew"),
        ("CL-TOKEN-ERASURE", "replayE_cons"),
        ("CL-TOKEN-ERASURE", "replayT_cons"),
    }
)


@dataclass(frozen=True)
class Token:
    entry: str
    side: str  # "lean" or "python"
    line: int  # ledger line where the token starts (2026-09-18; was the
    #            field opener's line, which is the same for a one-line field)
    raw: str  # token text as written (may contain a wrapped newline)
    norm: str  # normalized: wrap joined, whitespace collapsed


@dataclass(frozen=True)
class Verdict:
    token: Token
    category: str  # lean-theorem / lean-ambiguous / lean-theorem-unreported /
    #                lean-decl / lean-family / test-name /
    #                artifact-key / artifact-subkey / artifact-literal /
    #                module-path / code-def / code-literal / cross-reference /
    #                meta / UNRESOLVED
    detail: str


@dataclass(frozen=True)
class Decl:
    """One counted Lean declaration.  ``head`` is the declaring keyword,
    or ``constructor`` for an alternative of an ``inductive``.  ``name`` is
    written as declared; a constructor carries its inductive's name as a
    prefix."""

    name: str
    head: str
    path: str
    line: int

    def describe(self) -> str:
        return f"{self.head} {self.name} at {self.path}:{self.line}"


@dataclass(frozen=True)
class DeclIndex:
    """``names`` is the existence tier: over-broad, final segments.
    ``counted`` maps a final segment to its declarations, from the
    comment-stripped, inductive-scoped scan."""

    names: frozenset[str]
    counted: Mapping[str, tuple[Decl, ...]]

    def __contains__(self, name: object) -> bool:
        return name in self.names


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


def population(
    chunks: list[tuple[str, str, int, str]], ledger: pathlib.Path = LEDGER
) -> tuple[int, list[str]]:
    """The raw population: half the backtick count of every chunk.  This is
    arithmetic on the text and never consults TOKEN, so a token the
    classifier drops fails totality rather than vanishing from both
    sides.  Odd counts are reported as their own failure."""
    total = 0
    odd: list[str] = []
    for entry, _side, line, chunk in chunks:
        ticks = chunk.count("`")
        if ticks % 2:
            odd.append(f"  {ledger}:{line}: {entry}: unbalanced backticks")
        total += ticks // 2
    return total, odd


def load_axiom_names() -> frozenset[str]:
    names = set()
    for line in AXIOMS.read_text(encoding="utf-8").splitlines():
        m = REPORT.match(line)
        if m:
            names.add(m.group("name"))
    return frozenset(names)


def strip_lean_comments(text: str) -> list[str]:
    """Return ``text``'s lines with Lean comments blanked out, one output
    line per input line.  Handles ``--`` line comments and nestable
    ``/- ... -/`` blocks (which covers ``/--`` and ``/-!``), and skips
    string literals so a comment marker inside a string is not taken for
    one.  A character literal holding a double quote is not handled.  None
    occurs under ``lean4/Derivation`` today, and no string there holds a
    comment marker either."""
    out: list[str] = []
    depth = 0
    for line in text.splitlines():
        kept: list[str] = []
        i = 0
        n = len(line)
        while i < n:
            pair = line[i : i + 2]
            if depth:
                if pair == "/-":
                    depth += 1
                    i += 2
                elif pair == "-/":
                    depth -= 1
                    i += 2
                else:
                    i += 1
                continue
            if pair == "/-":
                depth += 1
                i += 2
                continue
            if pair == "--":
                break
            if line[i] == '"':
                j = i + 1
                while j < n and line[j] != '"':
                    j += 2 if line[j] == "\\" else 1
                kept.append(line[i : j + 1])
                i = j + 1
                continue
            kept.append(line[i])
            i += 1
        out.append("".join(kept))
    return out


def count_decls(path: pathlib.Path, text: str) -> list[Decl]:
    """The counted declarations of one file: every DECL head on a
    comment-stripped line, plus every ``|`` alternative inside an
    ``inductive`` block.  The block opens at an ``inductive`` head and
    closes at the next head, or at the next non-blank line that starts in
    column 0 with something other than ``|`` (``deriving``, ``namespace``,
    ``end``, ...).  Match arms in a later ``def`` or proof are therefore
    never counted as constructors."""
    found: list[Decl] = []
    shown = path.as_posix()
    inductive: str | None = None
    for number, line in enumerate(strip_lean_comments(text), 1):
        m = DECL.match(line)
        if m is not None:
            head, name = m.group("head"), m.group("name")
            found.append(Decl(name, head, shown, number))
            inductive = name if head == "inductive" else None
            if inductive is not None:
                for c in CTOR_ALT.finditer(line, m.end()):
                    found.append(
                        Decl(f"{inductive}.{c.group('name')}", CONSTRUCTOR,
                             shown, number)
                    )
            continue
        if inductive is None or not line.strip():
            continue
        if not line[0].isspace() and not line.startswith("|"):
            inductive = None
            continue
        if line.lstrip().startswith("|"):
            for c in CTOR_ALT.finditer(line):
                found.append(
                    Decl(f"{inductive}.{c.group('name')}", CONSTRUCTOR,
                         shown, number)
                )
    return found


def load_lean_decls(lean_dir: pathlib.Path = LEAN_DIR) -> DeclIndex:
    """Both declaration indexes over ``lean_dir``.  The existence tier is
    unchanged: the per-line DECL/CTOR patterns over raw lines, comments
    and match arms included.  The counted index keeps each declaration's
    head keyword, so the gate can tell a theorem from a definition and
    count how many declarations share a final segment."""
    names: set[str] = set()
    counted: dict[str, list[Decl]] = {}
    for path in sorted(lean_dir.rglob("*.lean")):
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            m = DECL.match(line) or CTOR.match(line)
            if m:
                names.add(m.group("name").split(".")[-1])
        for decl in count_decls(path, text):
            counted.setdefault(decl.name.split(".")[-1], []).append(decl)
    return DeclIndex(
        frozenset(names), {k: tuple(v) for k, v in sorted(counted.items())}
    )


def report_candidates(name: str, axioms: frozenset[str]) -> list[str]:
    """Every report ``name`` resolves to: the exact report, and every
    report ending in ``.name``."""
    return sorted(a for a in axioms if a == name or a.endswith("." + name))


def describe_candidates(reports: Sequence[str], decls: Sequence[Decl]) -> str:
    parts = [f"report {r}" for r in reports]
    parts += [d.describe() for d in decls]
    return "candidates: " + ("; ".join(parts) if parts else "none")


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
    decls: DeclIndex,
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
        reports = report_candidates(name, axioms)
        counted = decls.counted.get(name.split(".")[-1], ())
        # Decided before any pass: a bare name that could mean more than
        # one declaration is not evidence for any one of them.
        if "." not in name and (len(counted) > 1 or len(reports) > 1):
            return Verdict(
                tok, "lean-ambiguous", describe_candidates(reports, counted)
            )
        if name in axioms:
            return Verdict(tok, "lean-theorem", "exact")
        if reports:
            return Verdict(tok, "lean-theorem", "suffix")
        if PATHLIKE.match(t) and resolve_path(t):
            return Verdict(tok, "module-path", t)
        if name.split(".")[-1] in decls:
            if any(d.head in THEOREM_HEADS for d in counted):
                return Verdict(
                    tok,
                    "lean-theorem-unreported",
                    "declared as a theorem, no axiom report; "
                    + describe_candidates(reports, counted),
                )
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


def pin_failures(
    verdicts: Sequence[Verdict],
    category: str,
    pinned: frozenset[tuple[str, str]],
    pin_name: str,
    ledger: pathlib.Path = LEDGER,
) -> list[str]:
    """Compare the live ``category`` population with its frozen pin, in
    both directions.  A member the pin does not hold is named with its
    entry, ledger line, token, and candidates.  A pinned member that no
    longer classifies as ``category`` is named as a stale pin, with what
    it classifies as now."""
    live: dict[tuple[str, str], list[Verdict]] = {}
    for v in verdicts:
        if v.category == category:
            live.setdefault((v.token.entry, v.token.norm), []).append(v)
    rows: list[str] = []
    for key in sorted(live.keys() - pinned):
        for v in live[key]:
            rows.append(
                f"  NEW {category}: {ledger}:{v.token.line}: {v.token.entry} "
                f"[{v.token.side}] `{v.token.norm}`: {v.detail}"
            )
    for entry, token in sorted(pinned - live.keys()):
        now = sorted(
            {
                v.category
                for v in verdicts
                if (v.token.entry, v.token.norm) == (entry, token)
            }
        )
        where = (
            "now classifies as " + ", ".join(now)
            if now
            else "is no longer cited in an evidence field"
        )
        rows.append(
            f"  STALE PIN: ({entry}, `{token}`) is in {pin_name} as "
            f"{category} but {where}; remove it from {pin_name}"
        )
    return rows


def main(ledger: pathlib.Path | None = None) -> int:
    """Run the gate.  ``ledger`` reads another copy of the ledger and is
    for tests and injection only."""
    ledger = LEDGER if ledger is None else ledger
    for required in (ledger, AXIOMS, LEAN_DIR, TESTS_DIR):
        if not required.exists():
            print(f"FAIL: {required} not found")
            return 1
    text = ledger.read_text(encoding="utf-8")
    entry_ids = frozenset(
        m.group("id") for m in (ENTRY.match(ln) for ln in text.splitlines()) if m
    )
    chunks = evidence_chunks(text)
    entries = {entry for entry, _s, _l, _c in chunks}
    if not chunks or not entries or not entry_ids:
        print(f"FAIL: no evidence fields found in {ledger} - the parser is broken")
        return 1

    expected, odd = population(chunks, ledger)
    if odd:
        print(f"FAIL: {len(odd)} chunk(s) with unbalanced backticks")
        for row in odd:
            print(row)
        return 1
    if expected == 0:
        print(f"FAIL: zero evidence tokens in {ledger} - the population is broken")
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
            at = line + chunk[: m.start()].count("\n")
            tokens.append(Token(entry, side, at, m.group(1), normalize(m.group(1))))

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
    failed = False
    failures = [v for v in verdicts if v.category == "UNRESOLVED"]
    if failures:
        failed = True
        print(f"FAIL: {len(failures)} unresolved evidence citation(s) in {ledger}")
        for v in failures:
            print(
                f"  {ledger}:{v.token.line}: {v.token.entry} "
                f"[{v.token.side}] `{v.token.norm}`: {v.detail}"
            )
    for category, pinned, pin_name in (
        ("lean-ambiguous", PINNED_AMBIGUOUS, "PINNED_AMBIGUOUS"),
        ("lean-theorem-unreported", PINNED_UNREPORTED, "PINNED_UNREPORTED"),
    ):
        rows = pin_failures(verdicts, category, pinned, pin_name, ledger)
        if rows:
            failed = True
            print(f"FAIL: {category} citations in {ledger} differ from {pin_name}")
            for row in rows:
                print(row)
    if failed:
        return 1
    counts: dict[str, int] = {"lean-ambiguous": 0, "lean-theorem-unreported": 0}
    for v in verdicts:
        counts[v.category] = counts.get(v.category, 0) + 1
    summary = ", ".join(f"{counts[k]} {k}" for k in sorted(counts))
    print(
        f"ledger evidence resolves: {len(tokens)} token(s) across "
        f"{len(entries)} entr(ies): {summary}; the "
        f"{counts['lean-ambiguous']} lean-ambiguous and "
        f"{counts['lean-theorem-unreported']} lean-theorem-unreported "
        f"citation(s) match their pins"
    )
    return 0


def parse_args(argv: Sequence[str] | None = None) -> pathlib.Path | None:
    parser = argparse.ArgumentParser(
        description="Resolve every evidence citation in the claim ledger."
    )
    parser.add_argument(
        "--ledger",
        type=pathlib.Path,
        default=None,
        help="read this copy of the ledger instead (tests and injection only)",
    )
    ledger: pathlib.Path | None = parser.parse_args(argv).ledger
    return ledger


if __name__ == "__main__":
    sys.exit(main(parse_args()))
