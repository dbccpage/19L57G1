"""Every count this tree's prose states, bound to the record that carries it.

Three editorial repair passes ran over these documents and each one left, or
made, another number that no record field carries.  The reason is structural,
not clerical: the tree restates computed values across five prose documents
with no mechanical binding between them, so an editorial fix cannot terminate.
Prose has no gate.  This is that gate.

It is built in the shape of this repository's other totality gates, and the
shape is what makes it worth anything:

**The population is enumerated independently of the classifier.**  Every
numeric literal of every tracked prose file is gathered by a pattern that owes
nothing to the rules below -- bare integers, decimals, percentages, byte
counts, and the number words this tree writes.  Over-gathering is safe,
because every gathered item must then be classified; under-gathering is the
failure mode, because a number the population never sees can never fail.  A
second, cruder scanner re-gathers the same files and every one of ITS hits
must lie inside a gathered item, so narrowing the population pattern fires a
guard by name instead of quietly shrinking what the gate can see.

**Classification is total and fails closed.**  Each gathered number resolves
into exactly one of: a value equal to a named field of ``receipts/*.json``,
cited by its JSON path; a value the gate computes directly and cheaply, with
the computation named; or a declared exemption, listed as data below with its
file, its reason, and a marker phrase on the line.  A number no rule reaches
FAILS, naming the file, the line, the number and the text around it.  A number
whose rule resolves to a different value FAILS, naming stated and true.

**The rules fail in both directions.**  A rule that matches nothing is stale
and fails too, so an exemption cannot outlive the line it was written for.

Three files are exempt WHOLE, and each exemption is proved here rather than
asserted.  ``COMPARISON.md`` is rendered from ``receipts/comparison.json`` by
``run_comparison.py``; the proof is that re-rendering the committed receipt
reproduces the committed document byte for byte, so every number in it is a
function of the record already.  ``DESIGN.md`` and ``PREDICTIONS.md`` are
frozen; the proof is that their bytes still carry the digests ``verify_pins``
pins, so no number in either can drift, and the tree's standing rule is that
corrections to frozen text are recorded in the live documents rather than
edited into the frozen ones.

Classification: METATHEORY APPARATUS.  It reads prose and records and asserts
nothing about the object language.
"""

from __future__ import annotations

import hashlib
import io
import json
import pathlib
import re
import subprocess
import sys
import unittest
from unittest.mock import patch
from typing import Any, Callable, NamedTuple

TREE = pathlib.Path(__file__).resolve().parent.parent
ROOT = TREE.parent.parent
REL = "research/side_free"

sys.path.insert(0, str(TREE))

import check_coverage  # noqa: E402
import comparison  # noqa: E402
import verify_pins  # noqa: E402
from sidefree import mirror  # noqa: E402

# ---------------------------------------------------------------------------
# The population
# ---------------------------------------------------------------------------

# The tracked prose census, pinned.  It is recomputed from ``git ls-files``
# below and diffed against this tuple in both directions, so a prose file that
# appears -- or disappears -- without being considered here fails by name.
PROSE_CENSUS: tuple[str, ...] = (
    "CLAIM_LEDGER.md",
    "COMPARISON.md",
    "DELETED.md",
    "DESIGN.md",
    "MANUAL.md",
    "PREDICTIONS.md",
    "STATUS.md",
    "change_log.md",
    "pinned/QUOTATIONS.md",
)

# The whole-file exemptions, each with the proof that discharges it.  These
# are the only files whose numbers are not classified one by one, and the
# tests named here are what make that safe.
WHOLE_FILE: dict[str, str] = {
    "COMPARISON.md": (
        "rendered from receipts/comparison.json by run_comparison.py, never "
        "written; proved by test_the_rendered_document_is_a_function_of_the_record"
    ),
    "DESIGN.md": (
        "frozen before any code existed and never edited; proved by "
        "test_the_frozen_files_still_carry_their_pinned_digests"
    ),
    "PREDICTIONS.md": (
        "frozen before any code existed and never edited; proved by "
        "test_the_frozen_files_still_carry_their_pinned_digests"
    ),
}

SCANNED: tuple[str, ...] = tuple(
    name for name in PROSE_CENSUS if name not in WHOLE_FILE
)

# The gathering pattern.  Deliberately generous and deliberately ignorant of
# every rule below: a run of digits with optional thousands separators, an
# optional decimal part and an optional percent sign.
DIGIT_RUN = re.compile(r"\d(?:[\d,]*\d)?(?:\.\d+)?%?")

# The number words this tree writes, gathered as numbers too, because a count
# spelled out is still a count -- "nine of P22's twelve cells" was one of the
# defects that made this gate necessary.
NUMBER_WORDS: dict[str, float] = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}
WORD_RUN = re.compile(
    r"\b(?:" + "|".join(sorted(NUMBER_WORDS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)

# The independent cross-check.  A cruder scanner, built differently on
# purpose: bare digit runs, and every alphabetic token tested against the word
# table rather than an alternation compiled from it.  Every hit of THIS must
# lie inside a gathered item, so narrowing the population pattern above fires
# a guard by name instead of quietly shrinking what the gate can see.
CRUDE_DIGITS = re.compile(r"[0-9]+")
CRUDE_TOKENS = re.compile(r"[A-Za-z_]+")


def crude_hits(line: str) -> list[tuple[int, str]]:
    """Digits, and word-numbers written as PROSE rather than inside a name.

    A number word inside a ``snake_case`` identifier -- ``retains_one_mark``,
    ``the_two_criteria_disagree_on`` -- is not prose, and is the identifier
    firewall's business rather than this gate's.  That is the same declared
    reading the repository's prose watchlist takes, and both scanners here
    take it, so the cross-check compares like with like.
    """
    hits = [(match.start(), match.group(0)) for match in CRUDE_DIGITS.finditer(line)]
    hits += [
        (match.start(), match.group(0))
        for match in CRUDE_TOKENS.finditer(line)
        if "_" not in match.group(0) and match.group(0).lower() in NUMBER_WORDS
    ]
    return hits

# Pinned per-file population sizes.  A census, in the sense this repository
# uses the word: it fails in both directions, so a population that silently
# shrinks cannot pass, and one that grows must be looked at.  Regenerate
# deliberately with ``--census`` and never while an injection is live.
POPULATION_CENSUS: dict[str, tuple[int, int]] = {
    "CLAIM_LEDGER.md": (130, 103),
    "DELETED.md": (7, 9),
    "MANUAL.md": (152, 36),
    "STATUS.md": (210, 99),
    "change_log.md": (123, 140),
    "pinned/QUOTATIONS.md": (18, 19),
}


class Number(NamedTuple):
    """One gathered numeric literal, before any rule has looked at it.

    ``start``/``end`` are columns on the line; ``window`` is that line with its
    neighbours, and ``wstart``/``wend`` are the same span inside it.  Rules are
    matched against the window because this tree's prose WRAPS: a phrase and
    the number it governs routinely land on different lines, and a gate that
    could not see across a wrap would force every rule to be written twice.
    """

    file: str
    line: int
    start: int
    end: int
    text: str
    kind: str
    context: str
    window: str
    wstart: int
    wend: int


def gather(name: str, text: str) -> list[Number]:
    """Every numeric literal of one file, by the population pattern alone."""
    lines = text.splitlines()
    found: list[Number] = []
    for index, line in enumerate(lines):
        before = lines[index - 1] if index else ""
        after = lines[index + 1] if index + 1 < len(lines) else ""
        offset = len(before) + 1 if index else 0
        window = "\n".join(
            part for part in (before if index else None, line, after) if part is not None
        )
        for kind, pattern in (("digit", DIGIT_RUN), ("word", WORD_RUN)):
            for match in pattern.finditer(line):
                found.append(
                    Number(
                        name,
                        index + 1,
                        match.start(),
                        match.end(),
                        match.group(0),
                        kind,
                        line,
                        window,
                        offset + match.start(),
                        offset + match.end(),
                    )
                )
    return found


def prose_text(name: str) -> str:
    return (TREE / name).read_text(encoding="utf-8")


def tracked_prose() -> tuple[str, ...]:
    """The tracked prose files of this tree, from git rather than from a list."""
    proc = subprocess.run(
        ["git", "ls-files", "--", REL],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return tuple(
        sorted(
            path[len(REL) + 1 :]
            for path in proc.stdout.splitlines()
            if path.endswith(".md")
        )
    )


# ---------------------------------------------------------------------------
# The sources a bound number may resolve against
# ---------------------------------------------------------------------------

PATH_STEP = re.compile(r"([^.\[\]]+)|\[(\d+)\]")


def dig(root: object, path: str) -> object:
    """Read ``a.b[0].c`` out of a loaded record; a trailing ``#`` is length."""
    wants_length = path.endswith("#")
    here: object = root
    for step in PATH_STEP.finditer(path.rstrip("#")):
        key, index = step.group(1), step.group(2)
        if index is not None:
            if not isinstance(here, list):
                raise KeyError(f"{path}: not a list at [{index}]")
            here = here[int(index)]
        else:
            if not isinstance(here, dict):
                raise KeyError(f"{path}: not an object at {key}")
            if key not in here:
                raise KeyError(f"{path}: no field {key}")
            here = here[key]
    if wants_length:
        if not isinstance(here, (list, dict, str)):
            raise KeyError(f"{path}: nothing to take the length of")
        return len(here)
    return here


_RECEIPTS: dict[str, Any] = {}


def receipt(which: str) -> Any:
    if which not in _RECEIPTS:
        path = TREE / "receipts" / f"{which}.json"
        _RECEIPTS[which] = json.loads(path.read_text(encoding="utf-8"))
    return _RECEIPTS[which]


def suite_size() -> float:
    """The tests ``unittest discover`` finds under ``tests/``."""
    loader = unittest.TestLoader()
    suite = loader.discover(
        str(TREE / "tests"), pattern="test_*.py", top_level_dir=str(TREE / "tests")
    )
    return float(suite.countTestCases())


def mypy_source_files() -> float:
    """The Python files strict mypy checks, from ``pyproject.toml``'s own list."""
    text = (TREE / "pyproject.toml").read_text(encoding="utf-8")
    block = text.split("files = [", 1)[1].split("]", 1)[0]
    entries = re.findall(r'"([^"]+)"', block)
    total = 0
    for entry in entries:
        target = TREE / entry
        total += (
            len(list(target.rglob("*.py"))) if target.is_dir() else int(target.is_file())
        )
    return float(total)


def measured_files() -> float:
    """The files ``check_coverage.py`` holds the coverage report to."""
    return float(len(check_coverage.measured_files()))


def lean_axiom_reports() -> float:
    """The ``#print axioms`` lines of this tree's Lean root."""
    text = (TREE / "lean" / "SideFree.lean").read_text(encoding="utf-8")
    return float(len(re.findall(r"^#print axioms ", text, re.M)))


def manifest_field(path: str) -> Callable[[], float]:
    def read() -> float:
        record = json.loads(
            (TREE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        value = dig(record, path)
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise KeyError(f"SOURCE_MANIFEST.json: {path} is not a number")
        return float(value)

    return read


def declared_values() -> float:
    record = json.loads(
        (TREE / "pinned" / "BOUNDARY_PIN.json").read_text(encoding="utf-8")
    )
    values = record["declared_values"]
    return float(len(values))


def file_bytes(relative: str) -> Callable[[], float]:
    def read() -> float:
        return float(len((TREE / relative).read_bytes()))

    return read


def frozen_file_count() -> float:
    return float(len(verify_pins.FROZEN))


def coverage_bar() -> float:
    return float(check_coverage.BAR)


def own_receipts() -> float:
    return float(len(list((TREE / "receipts").glob("*.json"))))


def own_gates() -> float:
    """This tree's own gates: the ``G<n>`` keys, not the roll-up beside them."""
    gates = dig(receipt("side_free"), "gates")
    if not isinstance(gates, dict):
        raise KeyError("gates is not an object")
    return float(sum(1 for key in gates if re.fullmatch(r"G\d+", str(key))))


def pinned_coordinates() -> float:
    """The pinned world's coordinates: those that transfer, plus those deleted."""
    transferring = dig(receipt("side_free"), "gates.G3.transferring#")
    deleted = dig(receipt("side_free"), "gates.G3.deleted#")
    return float(int(str(transferring)) + int(str(deleted)))


def joined_route_rows() -> float:
    rows = dig(receipt("side_free"), "route_table")
    if not isinstance(rows, list):
        raise KeyError("route_table is not a list")
    return float(sum(1 for row in rows if isinstance(row, dict) and row.get("joined")))


def secondary_survivors() -> float:
    """The unnamed reading's minimum points, less those the secondary rule cuts."""
    points = dig(receipt("side_free"), "mirror.U.minima_by_mu1.points#")
    excluded = dig(receipt("side_free"), "secondary.mirror_everywhere_satisfying.U#")
    return float(int(str(points)) - int(str(excluded)))


def other_dependence_entries() -> float:
    total = dig(receipt("comparison"), "pinned_dependence_claims.entry_count")
    selected = dig(receipt("comparison"), "pinned_dependence_claims.universal_entries#")
    return float(int(str(total)) - int(str(selected)))


def as_map(value: object) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def keep_label_points() -> float:
    """The candidate points of this carrier whose ``keep_labels`` is set."""
    rows = dig(receipt("side_free"), "control.rows")
    if not isinstance(rows, list):
        raise KeyError("control.rows is not a list")
    return float(
        sum(
            1
            for row in rows
            if isinstance(row, dict)
            and bool(as_map(row.get("coordinates")).get("keep_labels"))
        )
    )


def named_one_step_points() -> float:
    """The named reading's one-step points, from the mirror's own rows."""
    rows = dig(receipt("side_free"), "mirror.O.rows")
    if not isinstance(rows, list):
        raise KeyError("mirror.O.rows is not a list")
    return float(
        sum(1 for row in rows if isinstance(row, dict) and bool(row.get("one_step")))
    )


SCORING_NOTE = re.compile(r"^\* ", re.M)


def status_scoring_notes() -> float:
    """The scoring notes of ``STATUS.md``: the bullets under their own heading."""
    text = prose_text("STATUS.md")
    after = text.split("notes on the scoring", 1)[1]
    section = after.split("\n## ", 1)[0]
    return float(len(SCORING_NOTE.findall(section)))


COMPUTED: dict[str, Callable[[], float]] = {
    "suite size, from unittest discover": suite_size,
    "mypy's file list, expanded from pyproject.toml": mypy_source_files,
    "check_coverage.measured_files()": measured_files,
    "the coverage bar, check_coverage.BAR": coverage_bar,
    "#print axioms lines in lean/SideFree.lean": lean_axiom_reports,
    "verify_pins.FROZEN, the frozen file count": frozen_file_count,
    "BOUNDARY_PIN.json declared_values, counted": declared_values,
    "SOURCE_MANIFEST.json carve.allowed_paths, counted": manifest_field(
        "carve.allowed_paths#"
    ),
    "SOURCE_MANIFEST.json vendored_receipts, counted": manifest_field(
        "vendored_receipts#"
    ),
    "SOURCE_MANIFEST.json sources, counted": manifest_field("sources#"),
    "bytes of receipts/side_free.json": file_bytes("receipts/side_free.json"),
    "bytes of receipts/comparison.json": file_bytes("receipts/comparison.json"),
    "bytes of COMPARISON.md": file_bytes("COMPARISON.md"),
    "bytes of pinned/boundary_challenge0.json": file_bytes(
        "pinned/boundary_challenge0.json"
    ),
    "bytes of pinned/boundary_challenge1.json": file_bytes(
        "pinned/boundary_challenge1.json"
    ),
    "bytes of pinned/boundary_challenge2.json": file_bytes(
        "pinned/boundary_challenge2.json"
    ),
    "bytes of pinned/boundary_challenge3.json": file_bytes(
        "pinned/boundary_challenge3.json"
    ),
    "this tree's own receipts, counted": own_receipts,
    "this tree's own gates, counted": own_gates,
    "the pinned coordinates: transferring plus deleted": pinned_coordinates,
    "route table rows that joined": joined_route_rows,
    "the unnamed reading's minimum points, less the excluded ones": (
        secondary_survivors
    ),
    "the pinned dependence entries other than the selected universal one": (
        other_dependence_entries
    ),
    "the scoring notes of STATUS.md, counted": status_scoring_notes,
    "the candidate points that keep the labels": keep_label_points,
    "the named reading's one-step points": named_one_step_points,
    "lemma cells with retained marks": lambda: float(len([
        regime for regime, _wr, _mp, _kl in mirror.lemma_cells() if regime.n_marks() >= 2
    ])),
    "SOURCE_MANIFEST.json sources that are Python modules": lambda: float(
        sum(
            1
            for source in json.loads(
                (TREE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
            )["sources"]
            if str(source["path"]).endswith(".py")
        )
    ),
}


def resolve(source: tuple[str, str]) -> float:
    """The true value behind a binding, from the record or the computation."""
    kind, name = source
    if kind == "computed":
        if name not in COMPUTED:
            raise KeyError(f"no computation named {name}")
        return COMPUTED[name]()
    value = dig(receipt(kind), name)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise KeyError(f"{kind}:{name} is not a number: {value!r}")
    return float(value)


# ---------------------------------------------------------------------------
# The rules
# ---------------------------------------------------------------------------


class Binding(NamedTuple):
    """A prose number tied to the field or computation that carries it."""

    files: tuple[str, ...]
    pattern: str
    source: tuple[str, str]


class Exemption(NamedTuple):
    """A prose number that is legitimately not a live claim about the record."""

    files: tuple[str, ...]
    pattern: str
    reason: str


ALL = SCANNED
LEDGER = ("CLAIM_LEDGER.md",)
STATUS = ("STATUS.md",)
LOG = ("change_log.md",)
MAN = ("MANUAL.md",)
DEL = ("DELETED.md",)
QUOTES = ("pinned/QUOTATIONS.md",)

def sf(path: str) -> tuple[str, str]:
    return ("side_free", path)


def cp(path: str) -> tuple[str, str]:
    return ("comparison", path)


def co(name: str) -> tuple[str, str]:
    return ("computed", name)


BINDINGS: tuple[Binding, ...] = (
    # --- the battery transcript, and the counts it prints -------------------
    Binding(ALL, r"^(?P<n>\d+) tests, OK$", co("suite size, from unittest discover")),
    Binding(ALL, r"over (?P<n>\d+) files", co("check_coverage.measured_files()")),
    Binding(
        ALL,
        r"at or above (?P<n>\d+%)",
        co("the coverage bar, check_coverage.BAR"),
    ),
    Binding(
        ALL,
        r"no issues found in (?P<n>\d+) source files",
        co("mypy's file list, expanded from pyproject.toml"),
    ),
    Binding(
        ALL,
        r"receipt ok: (?P<n>\d+) bytes",
        co("bytes of receipts/side_free.json"),
    ),
    Binding(
        ALL,
        r"comparison ok: (?P<n>\d+) receipt bytes",
        co("bytes of receipts/comparison.json"),
    ),
    Binding(ALL, r"and (?P<n>\d+) document bytes", co("bytes of COMPARISON.md")),
    Binding(
        ALL,
        r"(?P<n>\d+) axiom reports",
        co("#print axioms lines in lean/SideFree.lean"),
    ),
    Binding(
        MAN,
        r"exit 0, (?P<n>\d+) reports",
        co("#print axioms lines in lean/SideFree.lean"),
    ),
    Binding(
        ALL,
        r"(?P<n>\d+) frozen file",
        co("verify_pins.FROZEN, the frozen file count"),
    ),
    Binding(
        ALL,
        r"at (?P<n>\d+) bytes",
        co("bytes of pinned/boundary_challenge3.json"),
    ),
    Binding(
        ALL,
        r"(?P<n>\d+) bytes, no CR",
        co("bytes of pinned/boundary_challenge3.json"),
    ),
    Binding(
        ALL,
        r"(?P<n>\d+) vendored receipt",
        co("SOURCE_MANIFEST.json vendored_receipts, counted"),
    ),
    Binding(
        ALL,
        r"(?P<n>\d+) declared value",
        co("BOUNDARY_PIN.json declared_values, counted"),
    ),
    Binding(ALL, r"(?P<n>\d+) receipt\(s\)", co("this tree's own receipts, counted")),
    # --- the decided block --------------------------------------------------
    Binding(ALL, r"under `mu1` \| \*\*(?P<n>\d+)\*\*", sf("decided.side_free_minimum")),
    Binding(
        ALL,
        r"the side-free minimum is \*\*(?P<n>\d+)\*\*",
        sf("decided.side_free_minimum"),
    ),
    Binding(
        ALL,
        r"side-free minimum (?P<n>\d+) \|",
        sf("decided.side_free_minimum"),
    ),
    Binding(
        ALL,
        r"tied non-isomorphic minima \| \*\*(?P<n>\d+)\*\*",
        sf("decided.side_free_classes"),
    ),
    Binding(ALL, r"\| (?P<n>\d+) tied class,", sf("decided.side_free_classes")),
    Binding(
        ALL, r"a class count above (?P<n>\d+)\.", sf("decided.side_free_classes")
    ),
    Binding(ALL, r"class counts (?P<n>\d+) against", sf("decided.side_free_classes")),
    Binding(ALL, r"class counts \d+ against (?P<n>\d+)", sf("decided.unnamed_classes")),
    Binding(ALL, r"\| (?P<n>\d+), in \d+ tied classes", sf("decided.unnamed_minimum")),
    Binding(ALL, r"\| \d+, in (?P<n>\d+) tied classes", sf("decided.unnamed_classes")),
    Binding(ALL, r"its (?P<n>three) tied minima", sf("decided.unnamed_classes")),
    Binding(ALL, r"\| (?P<n>\d+), in \d+ class \|", sf("decided.named_minimum")),
    Binding(ALL, r"\| \d+, in (?P<n>\d+) class \|", sf("decided.named_classes")),
    Binding(
        ALL,
        r"`delta_vs_unnamed`[^|\n]*\| \*\*(?P<n>[−+-]?\d+)\*\*",
        sf("decided.delta_vs_unnamed"),
    ),
    Binding(
        ALL,
        r"`delta_vs_named`[^|\n]*\| \*\*(?P<n>[−+-]?\d+)\*\*",
        sf("decided.delta_vs_named"),
    ),
    Binding(
        ALL,
        r"`delta_vs_unnamed = (?P<n>[−+-]?\d+)`",
        sf("decided.delta_vs_unnamed"),
    ),
    Binding(
        ALL, r"`delta_vs_named = (?P<n>[−+-]?\d+)`", sf("decided.delta_vs_named")
    ),
    Binding(ALL, r"delta (?P<n>\d+) and [−+-]?\d+,", sf("decided.delta_vs_unnamed")),
    Binding(ALL, r"delta \d+ and (?P<n>[−+-]?\d+),", sf("decided.delta_vs_named")),
    Binding(
        ALL,
        r"`plurality_vs_unnamed`[^|\n]*\| (?P<n>[−+-]?\d+) \|",
        sf("decided.plurality_vs_unnamed"),
    ),
    Binding(
        ALL,
        r"primitive bought \| \*\*(?P<n>\d+)\*\*",
        sf("decided.routes_bought_count"),
    ),
    Binding(
        ALL,
        r"`routes_bought_count` is \*{0,2}(?P<n>\d+)\*{0,2}",
        sf("decided.routes_bought_count"),
    ),
    Binding(
        ALL, r"exactly (?P<n>\d+) routes bought", sf("decided.routes_bought_count")
    ),
    Binding(
        ALL,
        r"reduced the price of the required[\s\S]{0,60}?by (?P<n>ZERO)",
        sf("decided.delta_vs_unnamed"),
    ),
    Binding(
        ALL,
        r"(?P<n>zero)-cost minimum",
        sf("decided.named_minimum"),
    ),
    # --- the withdrawal that ports -----------------------------------------
    Binding(ALL, r"`mu1 = (?P<n>\d+)` in both worlds", sf("withdrawal_port.control_mu1")),
    Binding(ALL, r"it costs (?P<n>\d+) in both", sf("withdrawal_port.control_mu1")),
    # --- the candidate space ------------------------------------------------
    Binding(ALL, r"(?P<n>\d+) points, \d+ one-step", sf("candidate_space.space_size")),
    Binding(ALL, r"\d+ points, (?P<n>\d+) one-step", sf("candidate_space.one_step_count")),
    Binding(
        ALL, r"(?P<n>\d+) refused bundles", sf("candidate_space.bundles_refused_count")
    ),
    Binding(ALL, r"(?P<n>eight)-point", sf("candidate_space.space_size")),
    Binding(ALL, r"at all (?P<n>eight) points", sf("candidate_space.space_size")),
    Binding(ALL, r"of the (?P<n>eight) points", sf("candidate_space.space_size")),
    Binding(
        ALL, r"(?P<n>three) declared coordinates", sf("candidate_space.coordinates#")
    ),
    Binding(
        ALL, r"these (?P<n>three)\s+coordinates", sf("candidate_space.coordinates#")
    ),
    Binding(
        ALL,
        r"(?P<n>three) (?:surviving|transferring) "
        r"(?:capability sentences|coordinates)",
        sf("gates.G3.transferring#"),
    ),
    Binding(ALL, r"all (?P<n>three) byte for byte", sf("gates.G3.transferring#")),
    Binding(
        ALL,
        r"partitions the pinned (?P<n>five)",
        co("the pinned coordinates: transferring plus deleted"),
    ),
    # --- the gates ----------------------------------------------------------
    Binding(ALL, r"All (?P<n>six) gates passed", co("this tree's own gates, counted")),
    Binding(ALL, r"Gate G4, (?P<n>\d+) rows", sf("gates.G4.row_count")),
    Binding(ALL, r", (?P<n>\d+) agreements", sf("gates.G4.agreements")),
    Binding(
        ALL,
        r"(?P<n>fourteen)\s+rows(?: the minimum ranges over| \|)",
        sf("gates.G4.row_count"),
    ),
    Binding(ALL, r"Gate G5: (?P<n>\d+) cells", sf("gates.G5.report.cells")),
    Binding(ALL, r"census of (?P<n>\d+) cells", sf("gates.G5.report.cells")),
    Binding(
        ALL,
        r"(?P<n>\d+) automorphisms checked",
        sf("gates.G5.report.automorphisms_checked"),
    ),
    Binding(
        ALL,
        r"reproduced (?P<n>\d+), \d+ and \d+ exactly",
        sf("gates.G5.report.automorphisms_checked"),
    ),
    Binding(
        ALL,
        r"reproduced \d+, (?P<n>\d+) and \d+ exactly",
        sf("gates.G5.report.converse_failure_cells"),
    ),
    Binding(
        ALL,
        r"reproduced \d+, \d+ and (?P<n>\d+) exactly",
        sf("smuggle_tripwire.violations"),
    ),
    Binding(
        ALL,
        r"(?P<n>\d+) cells where the side-typed world separates",
        sf("gates.G5.report.converse_failure_cells"),
    ),
    Binding(
        ALL,
        r"those (?P<n>\d+) cells the\s+antecedent",
        sf("gates.G5.report.converse_failure_cells"),
    ),
    Binding(
        ALL,
        r"The (?P<n>\d+) was reported as",
        sf("gates.G5.report.converse_failure_cells"),
    ),
    Binding(
        ALL,
        r"The (?P<n>\d+) is unchanged",
        sf("gates.G5.report.converse_failure_cells"),
    ),
    Binding(
        ALL,
        r"`non_vacuity_cells = (?P<n>\d+)`",
        sf("gates.G5.report.converse_failure_cells"),
    ),
    Binding(
        ALL,
        r"\*\*(?P<n>\d+)\*\* where the\s+side-typed world separates",
        sf("gates.G5.report.converse_failure_cells"),
    ),
    Binding(
        ALL,
        r"\*\*(?P<n>\d+)\*\* where the corollary's antecedent holds",
        sf("gates.G5.report.corollary_antecedent_cells"),
    ),
    Binding(
        ALL,
        r"\*\*(?P<n>\d+)\*\* of the \d+ cells of two or",
        sf("gates.G5.report.corollary_antecedent_cells"),
    ),
    Binding(
        ALL,
        r"is the (?P<n>\d+), which nothing reported",
        sf("gates.G5.report.corollary_antecedent_cells"),
    ),
    Binding(
        ALL,
        r"what the (?P<n>\d+) now",
        sf("gates.G5.report.corollary_antecedent_cells"),
    ),
    Binding(ALL, r"(?P<n>\d+) lemma violations", sf("gates.G5.report.violations")),
    Binding(
        ALL,
        r"of the (?P<n>\d+) cells of two or",
        co("lemma cells with retained marks"),
    ),
    Binding(
        ALL,
        r"(?P<n>\d+) corollary violations",
        sf("gates.G5.report.corollary_violations"),
    ),
    Binding(
        ALL,
        r"checked, (?P<n>\d+)\s+violations",
        sf("gates.G5.report.violations"),
    ),
    Binding(
        ALL, r"injection gives (?P<n>\d+) violations", sf("smuggle_tripwire.violations")
    ),
    Binding(
        ALL,
        r"converse count to (?P<n>zero)",
        sf("smuggle_tripwire.converse_failure_cells"),
    ),
    Binding(
        ALL,
        r"antecedent still holds at (?P<n>\d+) cells",
        sf("smuggle_tripwire.corollary_antecedent_cells"),
    ),
    Binding(ALL, r"Gate G6, (?P<n>\d+) rows compared", sf("gates.G6.rows_compared")),
    Binding(ALL, r"(?P<n>\d+) rows per reading", sf("mirror.U.space_size")),
    Binding(ALL, r"(?P<n>\d+)\s+points per reading", sf("mirror.U.space_size")),
    # --- the predictions ----------------------------------------------------
    Binding(ALL, r"All (?P<n>\d+) HIT", sf("predictions.hits")),
    Binding(ALL, r"HIT; (?P<n>\d+) MISS", sf("predictions.misses")),
    Binding(ALL, r"(?P<n>Four) are labelled FORCED", sf("predictions.forced_hits")),
    Binding(
        STATUS,
        r"\*\*(?P<n>Six) notes on the scoring",
        co("the scoring notes of STATUS.md, counted"),
    ),
    Binding(ALL, r"base: mu1 (?P<n>\d+),", sf("control.summary.base.mu1")),
    Binding(
        ALL,
        r"base: mu1 \d+, (?P<n>\d+) automorphisms",
        sf("control.summary.base.automorphism_count"),
    ),
    Binding(ALL, r"keep_labels: mu1 (?P<n>\d+),", sf("control.summary.keep_labels.mu1")),
    Binding(
        ALL,
        r"keep_labels: mu1 \d+, (?P<n>\d+) automorphisms",
        sf("control.summary.keep_labels.automorphism_count"),
    ),
    Binding(ALL, r"extra_mark: mu1 (?P<n>\d+),", sf("control.summary.extra_mark.mu1")),
    Binding(
        ALL,
        r"extra_mark: mu1 \d+, (?P<n>\d+) automorphisms",
        sf("control.summary.extra_mark.automorphism_count"),
    ),
    Binding(
        ALL,
        r"withdraw_mark_permutations: mu1 (?P<n>\d+),",
        sf("control.summary.withdraw_mark_permutations.mu1"),
    ),
    Binding(
        ALL,
        r"withdraw_mark_permutations: mu1 \d+, (?P<n>\d+) automorphism",
        sf("control.summary.withdraw_mark_permutations.automorphism_count"),
    ),
    Binding(
        ALL,
        r"by row: (?P<n>\d+), \d+, \d+, \d+",
        sf("control.summary.base.mu2"),
    ),
    Binding(
        ALL,
        r"by row: \d+, (?P<n>\d+), \d+, \d+",
        sf("control.summary.keep_labels.mu2"),
    ),
    Binding(
        ALL,
        r"by row: \d+, \d+, (?P<n>\d+), \d+",
        sf("control.summary.withdraw_mark_permutations.mu2"),
    ),
    Binding(
        ALL,
        r"by row: \d+, \d+, \d+, (?P<n>\d+)",
        sf("control.summary.extra_mark.mu2"),
    ),
    Binding(
        ALL,
        r"`mu2_restricted` minimum (?P<n>\d+) in all",
        sf("second_measures.control_minima_by_mu2_restricted.minimum"),
    ),
    Binding(
        ALL,
        r"(?P<n>\d+)/\d+ against \d+/\d+; \d+/\d+ against \d+/\d+",
        sf("censuses.withdrawal.mirror.separating_with_permutations_withdrawn"),
    ),
    Binding(
        ALL,
        r"\d+/(?P<n>\d+) against \d+/\d+; \d+/\d+ against \d+/\d+",
        sf("censuses.withdrawal.mirror.cells"),
    ),
    Binding(
        ALL,
        r"\d+/\d+ against (?P<n>\d+)/\d+; \d+/\d+ against \d+/\d+",
        sf("censuses.withdrawal.mirror.separating_with_permutations_kept"),
    ),
    Binding(
        ALL,
        r"\d+/\d+ against \d+/(?P<n>\d+); \d+/\d+ against \d+/\d+",
        sf("censuses.withdrawal.mirror.cells"),
    ),
    Binding(
        ALL,
        r"\d+/\d+ against \d+/\d+; (?P<n>\d+)/\d+ against \d+/\d+",
        sf("censuses.withdrawal.control.separating_with_permutations_withdrawn"),
    ),
    Binding(
        ALL,
        r"\d+/\d+ against \d+/\d+; \d+/(?P<n>\d+) against \d+/\d+",
        sf("censuses.withdrawal.control.cells"),
    ),
    Binding(
        ALL,
        r"\d+/\d+ against \d+/\d+; \d+/\d+ against (?P<n>\d+)/\d+",
        sf("censuses.withdrawal.control.separating_with_permutations_kept"),
    ),
    Binding(
        ALL,
        r"\d+/\d+ against \d+/\d+; \d+/\d+ against \d+/(?P<n>\d+)",
        sf("censuses.withdrawal.control.cells"),
    ),
    Binding(
        ALL,
        r"(?P<n>sixteen) assertions",
        sf("predictions.scored[13].clauses"),
    ),
    Binding(
        ALL,
        r"carries (?P<n>twelve) CLAUSES",
        sf("predictions.scored[21].clauses"),
    ),
    Binding(
        ALL,
        r"(?P<n>twelve) clauses over",
        sf("predictions.scored[21].clauses"),
    ),
    Binding(
        ALL,
        r"holds the (?P<n>twelve), the",
        sf("predictions.scored[21].clauses"),
    ),
    Binding(
        ALL,
        r"declared cell of (?P<n>twelve)",
        sf("predictions.scored[21].clauses"),
    ),
    Binding(
        ALL,
        r"over (?P<n>NINE) (?:ledger )?cells",
        sf("predictions.scored[21].ledger_cells.cells#"),
    ),
    Binding(
        ALL,
        r"one of the (?P<n>nine), the",
        sf("predictions.scored[21].ledger_cells.cells#"),
    ),
    Binding(
        ALL,
        r"the\s+(?P<n>nine), the one and the eight",
        sf("predictions.scored[21].ledger_cells.cells#"),
    ),
    Binding(
        ALL,
        r"the other (?P<n>eight) are in",
        sf("predictions.scored[21].ledger_cells.computed#"),
    ),
    Binding(
        ALL,
        r"the one and the (?P<n>eight),",
        sf("predictions.scored[21].ledger_cells.computed#"),
    ),
    # --- the endowment ledger ----------------------------------------------
    Binding(
        LEDGER,
        r"and (?P<n>four) of its cells are not",
        sf("endowment_ledger.declared_cells#"),
    ),
    Binding(
        ALL, r"(?P<n>three) prose\s+lists", sf("endowment_ledger.columns#")
    ),
    Binding(
        ALL, r"those (?P<n>three) cells are statements", sf("endowment_ledger.columns#")
    ),
    Binding(
        ALL,
        r"the (?P<n>three) cells of the renaming row",
        sf("endowment_ledger.columns#"),
    ),
    Binding(
        ALL, r"enumerated (?P<n>three) columns", sf("endowment_ledger.columns#")
    ),
    Binding(
        ALL,
        r"all (?P<n>three) of whose columns",
        sf("endowment_ledger.columns#"),
    ),
    Binding(
        ALL,
        r"(?P<n>four), spread across those two rows",
        sf("endowment_ledger.declared_cells#"),
    ),
    Binding(
        ALL, r"All (?P<n>four) are flagged", sf("endowment_ledger.declared_cells#")
    ),
    Binding(
        ALL, r"flags (?P<n>four) cells", sf("endowment_ledger.declared_cells#")
    ),
    Binding(
        ALL,
        r"`declared_cells` and says (?P<n>four)",
        sf("endowment_ledger.declared_cells#"),
    ),
    Binding(
        ALL,
        r"one of the (?P<n>four) declared cells",
        sf("endowment_ledger.declared_cells#"),
    ),
    Binding(
        ALL,
        r"is a typed (?P<n>zero)",
        sf("endowment_ledger.by_row.coordinates_the_genesis_declaration_fixes.control"),
    ),
    Binding(
        ALL,
        r"control (?P<n>zero) of its first row",
        sf("endowment_ledger.by_row.coordinates_the_genesis_declaration_fixes.control"),
    ),
    Binding(
        ALL,
        r"(?P<n>Six)\s+rows mismatch",
        sf("endowment_ledger.mismatching_rows#"),
    ),
    Binding(
        ALL,
        r"union is the (?P<n>six)",
        sf("endowment_ledger.mismatching_rows#"),
    ),
    Binding(
        ALL,
        r"one of the (?P<n>six) carries a price",
        sf("endowment_ledger.mismatching_rows#"),
    ),
    Binding(
        ALL,
        r"the\s+(?P<n>six), and the summary",
        sf("endowment_ledger.mismatching_rows#"),
    ),
    Binding(
        ALL,
        r"the other (?P<n>five)\s+listed by name as carrying none",
        sf("endowment_ledger.mismatching_rows_with_no_stated_price#"),
    ),
    # --- the route table and the two criteria -------------------------------
    Binding(ALL, r"(?P<n>four) joined rows", co("route table rows that joined")),
    Binding(ALL, r"the (?P<n>four) rows, at the", sf("route_table#")),
    Binding(
        ALL, r"route census, (?P<n>\d+) of \d+", co("route table rows that joined")
    ),
    Binding(ALL, r"route census, \d+ of (?P<n>\d+)", sf("route_table#")),
    Binding(
        ALL,
        r"all (?P<n>three) (?:of which |)READ the placement",
        cp("minima_and_the_sides.the_two_criteria_disagree_on#"),
    ),
    Binding(
        ALL,
        r"all (?P<n>three) of which read the placement",
        cp("minima_and_the_sides.the_two_criteria_disagree_on#"),
    ),
    # --- the deletion register ---------------------------------------------
    Binding(ALL, r"(?P<n>\d+) entries, \d+ deleted", sf("deletion_register.entries#")),
    Binding(ALL, r"(?P<n>\d+) deleted and", sf("deletion_register.deleted_count")),
    Binding(ALL, r"(?P<n>\d+)\s+narrowed", sf("deletion_register.narrowed_count")),
    Binding(ALL, r"DELETED: (?P<n>\d+) names", sf("deletion_register.deleted_count")),
    Binding(ALL, r"NARROWED: (?P<n>\d+) names", sf("deletion_register.narrowed_count")),
    Binding(
        ALL,
        r"allowlist of (?P<n>six) names",
        sf("deletion_register.stem_allowlist#"),
    ),
    Binding(
        ALL,
        r"(?P<n>six)-name allowlist",
        sf("deletion_register.stem_allowlist#"),
    ),
    Binding(
        ALL,
        r"(?P<n>Six) identifiers of the side-free modules",
        sf("deletion_register.stem_allowlist#"),
    ),
    # --- the price list -----------------------------------------------------
    Binding(ALL, r"\*\*(?P<n>\d+)\*\*, across genesis", cp("row_count")),
    Binding(ALL, r"Over (?P<n>\d+) compared items", cp("row_count")),
    Binding(ALL, r"Two of the (?P<n>\d+) —", cp("row_count")),
    Binding(
        ALL,
        r"at its price \| \*\*(?P<n>\d+)\*\*",
        cp("verdict.counts.bought_nothing"),
    ),
    Binding(
        ALL,
        r"the control differs \| \*\*(?P<n>\d+)\*\*",
        cp("verdict.counts.bought_something"),
    ),
    Binding(
        ALL,
        r"evidence for neither \| \*\*(?P<n>\d+)\*\*",
        cp("verdict.counts.absent"),
    ),
    Binding(
        ALL,
        r"verdicts or prices \| same in \*\*(?P<n>\d+)\*\*",
        cp("verdict.counts.verdict_or_price_bought_nothing"),
    ),
    Binding(
        ALL,
        r"verdicts or prices \| same in \*\*\d+\*\*, differs in \*\*(?P<n>\d+)\*\*",
        cp("verdict.counts.verdict_or_price_bought_something"),
    ),
    Binding(
        ALL,
        r"DEFINITION-level \| same in \*\*(?P<n>\d+)\*\*",
        cp("verdict.counts_without_the_declared_field_rows.bought_nothing"),
    ),
    Binding(
        ALL,
        r"DEFINITION-level \| same in \*\*\d+\*\*, differs in \*\*(?P<n>\d+)\*\*",
        cp("verdict.counts_without_the_declared_field_rows.bought_something"),
    ),
    Binding(
        ALL,
        r"restricted to verdicts and prices, same in \*\*(?P<n>\d+)\*\*",
        cp(
            "verdict.counts_without_the_declared_field_rows."
            "verdict_or_price_bought_nothing"
        ),
    ),
    Binding(
        ALL,
        r"restricted to verdicts and prices, same in \*\*\d+\*\*, "
        r"differs in \*\*(?P<n>\d+)\*\*",
        cp(
            "verdict.counts_without_the_declared_field_rows."
            "verdict_or_price_bought_something"
        ),
    ),
    Binding(
        ALL,
        r"price in (?P<n>\d+), differs in \d+, and has no statement",
        cp("verdict.counts.bought_nothing"),
    ),
    Binding(
        ALL,
        r"price in \d+, differs in (?P<n>\d+), and has no statement",
        cp("verdict.counts.bought_something"),
    ),
    Binding(
        ALL,
        r"no statement in one world in (?P<n>\d+)\.",
        cp("verdict.counts.absent"),
    ),
    Binding(
        ALL,
        r"same price in (?P<n>\d+) and differs in \d+\.",
        cp("verdict.counts.verdict_or_price_bought_nothing"),
    ),
    Binding(
        ALL,
        r"same price in \d+ and differs in (?P<n>\d+)\.",
        cp("verdict.counts.verdict_or_price_bought_something"),
    ),
    Binding(
        ALL,
        r"Setting both aside: same in (?P<n>\d+), differs in \d+",
        cp("verdict.counts_without_the_declared_field_rows.bought_nothing"),
    ),
    Binding(
        ALL,
        r"Setting both aside: same in \d+, differs in (?P<n>\d+)",
        cp("verdict.counts_without_the_declared_field_rows.bought_something"),
    ),
    Binding(
        ALL,
        r"restricted to verdicts and prices same in (?P<n>\d+) and differs",
        cp(
            "verdict.counts_without_the_declared_field_rows."
            "verdict_or_price_bought_nothing"
        ),
    ),
    Binding(
        ALL,
        r"restricted to verdicts and prices same in \d+ and differs in (?P<n>\d+)",
        cp(
            "verdict.counts_without_the_declared_field_rows."
            "verdict_or_price_bought_something"
        ),
    ),
    Binding(
        LOG,
        r"(?P<n>\d+) and \d+ becomes \d+ and \d+, and \d+ and \d+ becomes \d+ and \d+",
        cp("verdict.counts.bought_nothing"),
    ),
    Binding(
        LOG,
        r"\d+ and (?P<n>\d+) becomes \d+ and \d+, and \d+ and \d+ becomes \d+ and \d+",
        cp("verdict.counts.bought_something"),
    ),
    Binding(
        LOG,
        r"\d+ and \d+ becomes (?P<n>\d+) and \d+, and \d+ and \d+ becomes \d+ and \d+",
        cp("verdict.counts_without_the_declared_field_rows.bought_nothing"),
    ),
    Binding(
        LOG,
        r"\d+ and \d+ becomes \d+ and (?P<n>\d+), and \d+ and \d+ becomes \d+ and \d+",
        cp("verdict.counts_without_the_declared_field_rows.bought_something"),
    ),
    Binding(
        LOG,
        r"becomes \d+ and \d+, and (?P<n>\d+) and \d+ becomes",
        cp("verdict.counts.verdict_or_price_bought_nothing"),
    ),
    Binding(
        LOG,
        r"becomes \d+ and \d+, and \d+ and (?P<n>\d+) becomes",
        cp("verdict.counts.verdict_or_price_bought_something"),
    ),
    Binding(
        LOG,
        r"becomes \d+ and \d+, and \d+ and \d+ becomes (?P<n>\d+) and",
        cp(
            "verdict.counts_without_the_declared_field_rows."
            "verdict_or_price_bought_nothing"
        ),
    ),
    Binding(
        LOG,
        r"becomes \d+ and \d+, and \d+ and \d+ becomes \d+ and (?P<n>\d+)",
        cp(
            "verdict.counts_without_the_declared_field_rows."
            "verdict_or_price_bought_something"
        ),
    ),
    # --- the pinned dependence dictionary -----------------------------------
    Binding(
        ALL,
        r"\*\*(?P<n>\d+)\*\* entries: \d+ dependent",
        cp("pinned_dependence_claims.entry_count"),
    ),
    Binding(
        ALL,
        r"entries: (?P<n>\d+) dependent",
        cp("pinned_dependence_claims.counts_by_class.DEPENDENT"),
    ),
    Binding(
        ALL,
        r"(?P<n>\d+) independent",
        cp("pinned_dependence_claims.counts_by_class.INDEPENDENT"),
    ),
    Binding(
        ALL, r"(?P<n>\d+) mixed", cp("pinned_dependence_claims.counts_by_class.MIXED")
    ),
    Binding(
        ALL,
        r"(?P<n>\d+) unclassified",
        cp("pinned_dependence_claims.counts_by_class.UNCLASSIFIED"),
    ),
    Binding(
        ALL,
        r"\| \*\*(?P<n>\d+)\*\*, and it is \*\*CONTRADICTED\*\*",
        cp("pinned_dependence_claims.universal_entries#"),
    ),
    Binding(
        ALL,
        r"dictionary — (?P<n>\d+) entries",
        cp("pinned_dependence_claims.entry_count"),
    ),
    Binding(
        ALL, r"Its (?P<n>\d+)\s+entries", cp("pinned_dependence_claims.entry_count")
    ),
    Binding(
        ALL,
        r"The other (?P<n>\d+) entries",
        co("the pinned dependence entries other than the selected universal one"),
    ),
    # --- gate C1's declared values ------------------------------------------
    Binding(ALL, r"(?P<n>\d+) declared, \d+ read", cp("gates.C1.declared")),
    Binding(ALL, r"\d+ declared, (?P<n>\d+) read", cp("gates.C1.used_by_rows")),
    Binding(ALL, r"read, (?P<n>\d+) checked", cp("gates.C1.checked")),
    Binding(ALL, r"(?P<n>\d+) for \d+\.", cp("gates.C1.declared")),
    Binding(ALL, r"\d+ for (?P<n>\d+)\.", cp("gates.C1.checked")),
    Binding(ALL, r"folded into the (?P<n>\d+)\.", cp("gates.C1.declared")),
    # --- the vendored receipts and the manifest -----------------------------
    Binding(
        ALL,
        r"the (?P<n>four) (?:vendored )?pinned receipts",
        co("SOURCE_MANIFEST.json vendored_receipts, counted"),
    ),
    Binding(
        ALL,
        r"(?P<n>four) challenge\s+modules",
        co("SOURCE_MANIFEST.json sources that are Python modules"),
    ),
    Binding(
        ALL,
        r"its (?P<n>four) rungs",
        co("SOURCE_MANIFEST.json vendored_receipts, counted"),
    ),
    Binding(
        ALL,
        r"the (?P<n>three) declared\s+files",
        co("SOURCE_MANIFEST.json carve.allowed_paths, counted"),
    ),
    Binding(
        ALL,
        r"(?P<n>three) files of this tree",
        co("SOURCE_MANIFEST.json carve.allowed_paths, counted"),
    ),
    # --- the remainder ------------------------------------------------------
    Binding(
        ALL,
        r"in all (?P<n>three) columns",
        sf("endowment_ledger.columns#"),
    ),
    Binding(
        ALL,
        r"at the (?P<n>four) points that keep the labels",
        co("the candidate points that keep the labels"),
    ),
    Binding(
        ALL,
        r"scored on is (?P<n>four) clauses",
        sf("predictions.scored[3].clauses"),
    ),
    Binding(
        ALL,
        r"stands on the (?P<n>four) clauses",
        sf("predictions.scored[3].clauses"),
    ),
    Binding(
        ALL,
        r"cell of\s+(?P<n>twelve) is a declaration",
        sf("predictions.scored[21].clauses"),
    ),
    Binding(
        MAN,
        r"same (?P<n>three);",
        co("SOURCE_MANIFEST.json carve.allowed_paths, counted"),
    ),
    Binding(
        LOG,
        r"reading has (?P<n>six) points",
        co("the named reading's one-step points"),
    ),
    # --- the secondary enumeration ------------------------------------------
    Binding(
        ALL,
        r"still has (?P<n>three) at price one",
        co("the unnamed reading's minimum points, less the excluded ones"),
    ),
    Binding(
        ALL,
        r"at price one in (?P<n>two) classes",
        sf("secondary.decided.unnamed_classes"),
    ),
)

# Order matters and is declared: the first rule whose span contains a number
# classifies it, bindings before exemptions, and the two catch-alls last.
NUMERAL = (
    r"(?:[−+-]?\d(?:[\d,]*\d)?(?:\.\d+)?%?|(?i:\b(?:"
    + "|".join(sorted(NUMBER_WORDS, key=len, reverse=True))
    + r")\b))"
)


def quantity_pattern(pattern: str) -> str:
    """Locate a quantity by its surrounding phrase, never by its value.

    The examples in the rule table retain their original spelling for ease
    of review. Every numeric capture accepts all declared number spellings:
    changing 'three' to 'two' must still select the same source field.
    """
    widened, count = re.subn(
        r"\(\?P<n>[^()]*\)", lambda _m: "(?P<n>" + NUMERAL + ")", pattern
    )
    if count != 1:
        raise ValueError(f"binding must have one simple numeric capture: {pattern!r}")
    return widened


BINDINGS = tuple(
    Binding(rule.files, quantity_pattern(rule.pattern), rule.source)
    for rule in BINDINGS
)


EXEMPTIONS: tuple[Exemption, ...] = (
    Exemption(
        ALL,
        r"(?P<n>\b\d{4}-\d{2}-\d{2}\b)",
        "a date, not a count",
    ),
    Exemption(
        ALL,
        r"(?P<n>\b(?=[0-9a-f]*[a-f])[0-9a-f]{6,}\b)",
        "a sha256 prefix, a git blob id or a commit id, not a count",
    ),
    Exemption(
        ALL,
        r"(?P<n>\b(?:R|P|G|C|I)\d+\b)",
        "a declared row, prediction, gate, comparison-gate or injection id",
    ),
    Exemption(
        ALL,
        r"(?P<n>\b[A-Za-z_][A-Za-z0-9_]*[0-9][A-Za-z0-9_]*\b)",
        "the number is part of an identifier -- a field, coordinate, module "
        "or theorem name -- and is read as a name, not as a count",
    ),
    Exemption(
        ALL,
        r"§(?P<n>\d+)",
        "a section number of a cited document",
    ),
    Exemption(
        ALL,
        r"UTF-(?P<n>8)",
        "part of an encoding name",
    ),
    Exemption(
        ALL,
        r"\"(?P<n>\d+:[A-Za-z_][\w.]*)\"",
        "a pinned declared-value key, whose leading number is a challenge index",
    ),
    Exemption(
        ALL,
        r"rungs (?P<n>\d+) to \d+",
        "a rung index of the pinned world",
    ),
    Exemption(
        ALL,
        r"rungs \d+ to (?P<n>\d+)",
        "a rung index of the pinned world",
    ),
    Exemption(
        ALL,
        r"challenge (?P<n>\d+)",
        "a challenge index of the pinned world",
    ),
    Exemption(
        ALL,
        r"exit (?P<n>\d+)",
        "a process exit status",
    ),
    Exemption(
        MAN,
        r"\| (?P<n>1(?: and 1)?) \| [a-z]",
        "the exit column of the injection table: a process exit status",
    ),
    Exemption(
        MAN,
        r"'(?:placement|permutation)': \[(?P<n>\d+, ?\d+)\]",
        "a cell locator inside a reported first violation, not a count",
    ),
    Exemption(
        STATUS,
        r"(?P<n>\(\d+,\d+\)/\(reflected,\[\d+,\d+\]\))",
        "a cell locator inside a reported first violation, not a count",
    ),
    Exemption(
        MAN,
        r"from `(?P<n>\d+)` to `\d+`",
        "the value an injection replaced, recorded in the injection row",
    ),
    Exemption(
        MAN,
        r"from `\d+` to `(?P<n>\d+)`",
        "the value an injection wrote, recorded in the injection row",
    ),
    Exemption(
        MAN,
        r"changed from (?P<n>\d+) to \d+",
        "the value an injection replaced, recorded in the injection row",
    ),
    Exemption(
        MAN,
        r"changed from \d+ to (?P<n>\d+)",
        "the value an injection wrote, recorded in the injection row",
    ),
    Exemption(
        MAN,
        r"pins Ran (?P<n>\d+) tests and this suite discovers \d+",
        "a diagnostic quoted verbatim from a recorded injection run",
    ),
    Exemption(
        MAN,
        r"pins Ran \d+ tests and this suite discovers (?P<n>\d+)",
        "a diagnostic quoted verbatim from a recorded injection run",
    ),
    Exemption(
        MAN,
        r"AssertionError: (?P<n>\d+) != \d+",
        "a diagnostic quoted verbatim from a recorded injection run",
    ),
    Exemption(
        MAN,
        r"AssertionError: \d+ != (?P<n>\d+)",
        "a diagnostic quoted verbatim from a recorded injection run",
    ),
    Exemption(
        MAN,
        r"'expected': (?P<n>\d+)",
        "a diagnostic quoted verbatim from a recorded injection run",
    ),
    Exemption(
        MAN,
        r"'computed': (?P<n>\d+)",
        "a diagnostic quoted verbatim from a recorded injection run",
    ),
    Exemption(
        (*MAN, *LOG),
        r"written at (?P<n>\d+)",
        "HISTORICAL: the value a pin carried before it drifted",
    ),
    Exemption(
        (*MAN, *LOG),
        r"stood at (?P<n>\d+)",
        "HISTORICAL: the value a pin carried before it was repaired",
    ),
    Exemption(
        (*MAN, *LOG),
        r"a suite of (?P<n>\d+)",
        "HISTORICAL: the suite size at the time the drift was found",
    ),
    Exemption(
        (*MAN, *LOG),
        r"the suite ran (?P<n>\d+)",
        "HISTORICAL: the suite size at the time the drift was found",
    ),
    Exemption(
        LOG,
        r"stays at (?P<n>\d+) tests",
        "HISTORICAL: the suite size as of that dated entry",
    ),
    Exemption(
        LOG,
        r"moves from (?P<n>[\d,]+) tests to",
        "HISTORICAL: the suite size before that dated entry's change",
    ),
    Exemption(
        LOG,
        r"moves from [\d,]+ tests to\s+(?P<n>[\d,]+)",
        "HISTORICAL: the suite size after that dated entry's change",
    ),
    Exemption(
        LOG,
        r"\bfrom\s+(?P<n>[\d,]+)\s+to\s+[\d,]+",
        "HISTORICAL: the size before a transition recorded in a dated entry; "
        "the CURRENT value is bound in the battery transcript of STATUS.md",
    ),
    Exemption(
        LOG,
        r"\bfrom\s+[\d,]+\s+to\s+(?P<n>[\d,]+)",
        "HISTORICAL: the size after a transition recorded in a dated entry; "
        "the CURRENT value is bound in the battery transcript of STATUS.md",
    ),
    Exemption(
        LOG,
        r"then stood at\s+(?P<n>[\d,]+)",
        "HISTORICAL: a byte count quoted while recording that it went stale",
    ),
    Exemption(
        LOG,
        r"asserted on the literal `(?P<n>[\d,]+)`",
        "HISTORICAL: a stale literal quoted in the description of its own defect",
    ),
    Exemption(
        LOG,
        r'(?P<n>"[^"]{0,400}")',
        "a quotation of the prose the entry is correcting: it must reproduce "
        "what was written, so its numbers are historical by construction",
    ),
    Exemption(
        LEDGER,
        r"The earlier figures (?P<n>[\d,]+) against [\d,]+",
        "HISTORICAL: named as superseded on the line that names it",
    ),
    Exemption(
        LEDGER,
        r"The earlier figures [\d,]+ against (?P<n>[\d,]+)",
        "HISTORICAL: named as superseded on the line that names it",
    ),
    Exemption(
        LOG,
        r"(?P<n>twelve) unchecked places",
        "HISTORICAL: arithmetic inside the description of a repaired defect",
    ),
    Exemption(
        LOG,
        r"scored (?P<n>four) of the sixteen",
        "HISTORICAL: what the scorer covered before that entry repaired it",
    ),
    Exemption(
        ALL,
        r"(?P<n>three) digests",
        "the vendored pin's sha256, git blob id and byte count: a count of "
        "checks declared in verify_pins.py, not a value of the record",
    ),
    Exemption(
        MAN,
        r"pin's (?P<n>four) values",
        "those three digests plus the CR refusal: a count of checks declared "
        "in verify_pins.py, not a value of the record",
    ),
    Exemption(
        MAN,
        r"remaining (?P<n>three) published comparison gates",
        "the comparison gates other than C0 and C1, whose probes the rows "
        "above record",
    ),
    Exemption(
        LEDGER,
        r"All (?P<n>three): no axioms",
        "a count of the Lean theorem names listed in the same entry's Lean "
        "bullet; the axiom reports themselves are checked by verify_lean.py",
    ),
    Exemption(
        LEDGER,
        r"All (?P<n>five): no axioms",
        "a count of the Lean theorem names listed in the same entry's Lean "
        "bullet; the axiom reports themselves are checked by verify_lean.py",
    ),
    Exemption(
        LEDGER,
        r"for each of the (?P<n>five)",
        "a count of the Lean theorem names listed in the same entry's Lean "
        "bullet; the axiom reports themselves are checked by verify_lean.py",
    ),
    Exemption(
        LEDGER,
        r"(?P<n>four) theorems cited above",
        "a count of the theorem names listed in the same entry",
    ),
    Exemption(
        LEDGER,
        r"declared (?P<n>twelve): METATHEORY",
        "the source classifications declared by the repository's assumption "
        "discipline, listed in the same sentence",
    ),
    Exemption(
        STATUS,
        r"(?P<n>four) numeric endowment rows",
        "the rows of P22's own table in the frozen PREDICTIONS.md: a "
        "description of the prediction's shape, not a value of the record; "
        "the record's own population for P22 is bound in the note below",
    ),
    Exemption(
        ALL,
        r"(?P<n>\b[A-Za-z_][A-Za-z0-9_./\\-]*\.(?:lean|py|json|md):\d+)",
        "a line number in a citation",
    ),
    Exemption(
        ALL,
        r"^(?P<n>#{1,6}\s+\d+\.)\s",
        "a numbered section heading",
    ),
    Exemption(
        ALL,
        r"^(?P<n>\s*\d+\.)\s",
        "an ordered-list marker",
    ),
    Exemption(
        QUOTES,
        r"^(?P<n>>.*)$",
        "a verbatim quotation of the pinned world, reproduced byte for byte "
        "and asserted as bytes by gates G2 and G3; the number belongs to the "
        "quoted text and this file may not edit it",
    ),
    Exemption(
        MAN,
        r"declared value (?P<n>\d+):[A-Za-z_]",
        "a pinned declared-value key, whose leading number is a challenge index",
    ),
    Exemption(
        MAN,
        r"minimum is (?P<n>\d+), the pinned",
        "a diagnostic quoted verbatim from a recorded injection run",
    ),
    Exemption(
        MAN,
        r"pinned (?:bytes say|receipt says) (?P<n>\d+)",
        "a diagnostic quoted verbatim from a recorded injection run",
    ),
    Exemption(
        LOG,
        r"(?P<n>Nine plus two\s+is eleven)",
        "HISTORICAL: arithmetic quoted while showing that neither figure was "
        "the population",
    ),
    Exemption(
        LOG,
        r"(?P<n>thirteen) lines later",
        "a line offset inside a description of two disagreeing sentences",
    ),
    Exemption(
        LOG,
        r"described (?P<n>three) cells",
        "HISTORICAL: what a paragraph said before the entry repaired it",
    ),
    Exemption(
        LOG,
        r"shows (?P<n>five) names",
        "the names the declared collapse map yields for those points; the map "
        "itself is gate C3's, and the point count beside it is bound",
    ),
    Exemption(
        LOG,
        r"(?P<n>zero)(?: would have| there)",
        "a hypothetical value in a description of what a gate's message would "
        "have said",
    ),
    Exemption(
        LOG,
        r"(?:closed |)(?P<n>five) (?:carried |)findings",
        "a count of the findings a dated repair pass carried: that pass's own "
        "bookkeeping, fixed at the moment it was written",
    ),
    Exemption(
        LOG,
        r"introduced (?P<n>three), and all three were",
        "a count of the findings a dated repair pass carried: that pass's own "
        "bookkeeping, fixed at the moment it was written",
    ),
    Exemption(
        LOG,
        r"introduced three, and all (?P<n>three) were",
        "a count of the findings a dated repair pass carried: that pass's own "
        "bookkeeping, fixed at the moment it was written",
    ),
    Exemption(
        LOG,
        r"(?P<n>Three) published gates",
        "a count of the gates one dated entry found missing from the census; "
        "the census itself is the injection table of MANUAL.md",
    ),
    Exemption(
        LOG,
        r"names these (?P<n>six)",
        "a count of the probes one dated entry added to the injection table",
    ),
    Exemption(
        LOG,
        r"the (?P<n>three) checks after it",
        "a count of the commands that follow the grep in this tree's CI step",
    ),
    Exemption(
        LOG,
        r"(?:in|[Tt]he) (?P<n>three) (?:places|editable copies)",
        "a count of the places one dated entry repaired: that entry's own "
        "bookkeeping, fixed at the moment it was written",
    ),
    Exemption(
        LOG,
        r"other (?P<n>four) (?:frozen-file |)corrections",
        "a count of this tree's recorded frozen-file corrections, which live "
        "in prose notes and are not a field of the record",
    ),
    # The two catch-alls, last by declaration.  RESIDUAL, named rather than
    # hidden: this tree writes `one` and `two` overwhelmingly as determiners
    # -- "one of the three files", "the two worlds" -- and hand-classifying
    # 281 of them would produce a rule set nobody could audit.  A count of a
    # record field spelled `one` or `two` is therefore outside this gate
    # unless a binding above reaches it first.  The population census still
    # counts them, so they cannot proliferate unnoticed.
    Exemption(
        ALL,
        r"(?i)(?P<n>\bone\b)",
        "RESIDUAL: the word `one`, read as a determiner rather than a count",
    ),
    Exemption(
        ALL,
        r"(?i)(?P<n>\btwo\b)",
        "RESIDUAL: the word `two`, read as a determiner rather than a count",
    ),
)


# ---------------------------------------------------------------------------
# Applying them
# ---------------------------------------------------------------------------


class Cover(NamedTuple):
    """One rule's claim over one span of one line."""

    rule: int
    start: int
    end: int
    text: str


def spans(pattern: str, line: str) -> list[tuple[int, int, str]]:
    found: list[tuple[int, int, str]] = []
    for match in re.finditer(pattern, line, re.M):
        try:
            group = match.group("n")
        except IndexError as exc:  # pragma: no cover - a malformed rule
            raise ValueError(f"rule {pattern!r} has no group 'n'") from exc
        if group is None:  # pragma: no cover - a malformed rule
            raise ValueError(f"rule {pattern!r} matched with group 'n' unset")
        found.append((match.start("n"), match.end("n"), group))
    return found


def rules_for(
    name: str,
) -> tuple[list[tuple[int, Binding]], list[tuple[int, Exemption]]]:
    """This file's rules, each carrying its index in the declared order.

    The index travels with the rule so that "which rule fired" is answered by
    position and never by equality: two rules may legitimately be written
    identically for different files, and an equality lookup would credit the
    wrong one and report the other as stale.
    """
    return (
        [(i, rule) for i, rule in enumerate(BINDINGS) if name in rule.files],
        [(i, rule) for i, rule in enumerate(EXEMPTIONS) if name in rule.files],
    )


def numeric(text: str) -> float:
    """The value a bound span states, digits or spelled out."""
    body = text.replace(",", "").replace("%", "").replace("−", "-").strip()
    body = body.strip("*` ")
    if body.lower() in NUMBER_WORDS:
        return float(NUMBER_WORDS[body.lower()])
    return float(body)


class Verdict(NamedTuple):
    """What classified one number: which kind of rule, its index, its span."""

    number: Number
    kind: str
    rule: int
    covered: str


def classify(
    number: Number,
    bindings: list[tuple[int, Binding]],
    exemptions: list[tuple[int, Exemption]],
) -> Verdict | None:
    """The first rule, in declared order, whose span contains this number."""
    if number.file == "pinned/QUOTATIONS.md" and number.context.lstrip().startswith(">"):
        bindings = []  # Verbatim pinned quotations use their declared exemption.
    for index, binding in bindings:
        for start, end, text in spans(binding.pattern, number.window):
            if start <= number.wstart and number.wend <= end:
                return Verdict(number, "binding", index, text)
    for index, exemption in exemptions:
        for start, end, text in spans(exemption.pattern, number.window):
            if start <= number.wstart and number.wend <= end:
                return Verdict(number, "exemption", index, text)
    return None


_POPULATION: dict[str, list[Number]] = {}


def population() -> dict[str, list[Number]]:
    if not _POPULATION:
        for name in SCANNED:
            _POPULATION[name] = gather(name, prose_text(name))
    return _POPULATION


_REPORT: list[tuple[list[str], list[str], list[str]]] = []


def report() -> tuple[list[str], list[str], list[str]]:
    if not _REPORT:
        _REPORT.append(run())
    return _REPORT[0]


def run() -> tuple[list[str], list[str], list[str]]:
    """Unclassified numbers, value mismatches, and stale rules."""
    unclassified: list[str] = []
    mismatched: list[str] = []
    used_bindings: set[int] = set()
    used_exemptions: set[int] = set()
    for name, numbers in population().items():
        bindings, exemptions = rules_for(name)
        for number in numbers:
            verdict = classify(number, bindings, exemptions)
            if verdict is None:
                unclassified.append(
                    f"{name}:{number.line}: [{number.text}] no rule classifies "
                    f"this number -- {number.context.strip()[:160]}"
                )
                continue
            if verdict.kind == "binding":
                rule = BINDINGS[verdict.rule]
                used_bindings.add(verdict.rule)
                try:
                    true = resolve(rule.source)
                except KeyError as exc:
                    mismatched.append(f"{name}:{number.line}: {exc}")
                    continue
                stated = numeric(verdict.covered)
                if stated != true:
                    mismatched.append(
                        f"{name}:{number.line}: [{verdict.covered}] resolved "
                        f"against {rule.source[0]}:{rule.source[1]} -- stated "
                        f"{stated:g}, true {true:g} -- "
                        f"{number.context.strip()[:120]}"
                    )
            else:
                used_exemptions.add(verdict.rule)
    stale = [
        f"binding {index} matches nothing and has outlived the line it was "
        f"written for: {BINDINGS[index].pattern!r} -> "
        f"{BINDINGS[index].source[0]}:{BINDINGS[index].source[1]}"
        for index in range(len(BINDINGS))
        if index not in used_bindings
    ] + [
        f"exemption {index} matches nothing and has outlived the line it was "
        f"written for: {EXEMPTIONS[index].pattern!r} -- "
        f"{EXEMPTIONS[index].reason}"
        for index in range(len(EXEMPTIONS))
        if index not in used_exemptions
    ]
    return unclassified, mismatched, stale


class Population(unittest.TestCase):
    def test_the_prose_census_is_what_git_tracks(self) -> None:
        tracked = tracked_prose()
        self.assertEqual(
            sorted(tracked),
            sorted(PROSE_CENSUS),
            "the tracked prose census moved; consider every new file here and "
            "update PROSE_CENSUS in the same commit",
        )

    def test_every_census_file_is_scanned_or_exempt_with_a_proof(self) -> None:
        for name in PROSE_CENSUS:
            self.assertTrue(
                name in SCANNED or name in WHOLE_FILE,
                f"{name} is in the census but is neither scanned nor exempt",
            )

    def test_the_crude_scanner_finds_nothing_the_population_missed(self) -> None:
        escaped: list[str] = []
        for name in SCANNED:
            covered = {
                (number.line, position)
                for number in gather(name, prose_text(name))
                for position in range(number.start, number.end)
            }
            for lineno, line in enumerate(prose_text(name).splitlines(), 1):
                for position, token in crude_hits(line):
                    if (lineno, position) not in covered:
                        escaped.append(
                            f"{name}:{lineno}: [{token}] is found by the crude "
                            f"scanner and not by the population pattern -- "
                            f"{line.strip()[:120]}"
                        )
        self.assertEqual(escaped, [], "\n".join(escaped))

    def test_the_population_census_matches_its_pin(self) -> None:
        counted = {
            name: (
                sum(1 for number in numbers if number.kind == "digit"),
                sum(1 for number in numbers if number.kind == "word"),
            )
            for name, numbers in population().items()
        }
        moved = [
            f"{name}: gathered {counted.get(name, ('-', '-'))}, "
            f"pinned {POPULATION_CENSUS.get(name, ('-', '-'))} (digits, words)"
            for name in sorted(set(counted) | set(POPULATION_CENSUS))
            if counted.get(name) != POPULATION_CENSUS.get(name)
        ]
        self.assertEqual(
            moved,
            [],
            "the gathered population moved against its pin; a population that "
            "shrinks silently cannot fail, so regenerate the pin deliberately "
            "with `python tests/test_prose_numbers.py --census` and never while "
            "an injection is live:\n" + "\n".join(moved),
        )


class Rules(unittest.TestCase):
    def test_the_runner_names_an_altered_count_and_recovers(self) -> None:
        original = population()
        name = "CLAIM_LEDGER.md"
        text = prose_text(name).replace(
            "Within the three declared coordinates", "Within the two declared coordinates", 1
        )
        altered = dict(original)
        altered[name] = gather(name, text)
        with patch.object(sys.modules[__name__], "_POPULATION", altered):
            _unknown, mismatched, _stale = run()
        self.assertTrue(any(name in row and "stated 2, true 3" in row for row in mismatched))
        self.assertFalse(any("stated 2, true 3" in row for row in run()[1]))

    def test_an_altered_word_count_cannot_fall_into_a_determiner_exemption(self) -> None:
        for word, wanted in (("three", 3.0), ("two", 2.0), ("one", 1.0), ("7", 7.0)):
            sentence = f"Within the {word} declared coordinates"
            numbers = gather("CLAIM_LEDGER.md", sentence)
            self.assertEqual(len(numbers), 1)
            verdict = classify(numbers[0], *rules_for("CLAIM_LEDGER.md"))
            self.assertIsNotNone(verdict)
            assert verdict is not None
            self.assertEqual(verdict.kind, "binding", sentence)
            self.assertEqual(numeric(verdict.covered), wanted)
            self.assertEqual(resolve(BINDINGS[verdict.rule].source), 3.0)

    def test_the_live_cell_count_is_bound_to_the_cell_population(self) -> None:
        for word in ("four", "two"):
            sentence = f"computed throughout, and {word} of its cells are not."
            number = gather("CLAIM_LEDGER.md", sentence)[0]
            verdict = classify(number, *rules_for("CLAIM_LEDGER.md"))
            assert verdict is not None
            self.assertEqual(verdict.kind, "binding")
            self.assertEqual(resolve(BINDINGS[verdict.rule].source), 4.0)

    def test_a_coverage_claim_is_not_verified_against_a_literal_percentage(self) -> None:
        sentence = "line 100.00% branch 100.00% over 9 files"
        for number in gather("STATUS.md", sentence)[:2]:
            self.assertIsNone(classify(number, *rules_for("STATUS.md")))

    def test_every_rule_compiles_and_locates_a_number(self) -> None:
        for kind, rules in (
            ("binding", [rule.pattern for rule in BINDINGS]),
            ("exemption", [rule.pattern for rule in EXEMPTIONS]),
        ):
            for index, pattern in enumerate(rules):
                compiled = re.compile(pattern, re.M)
                self.assertIn(
                    "n",
                    compiled.groupindex,
                    f"{kind} {index} has no group 'n' to locate the number: "
                    f"{pattern!r}",
                )

    def test_every_rule_names_a_file_of_the_scanned_census(self) -> None:
        for kind, files in (
            ("binding", [rule.files for rule in BINDINGS]),
            ("exemption", [rule.files for rule in EXEMPTIONS]),
        ):
            for index, names in enumerate(files):
                self.assertTrue(names, f"{kind} {index} names no file")
                for name in names:
                    self.assertIn(
                        name,
                        SCANNED,
                        f"{kind} {index} names {name}, which is not scanned",
                    )

    def test_every_source_a_binding_names_resolves(self) -> None:
        for index, rule in enumerate(BINDINGS):
            try:
                resolve(rule.source)
            except (KeyError, ValueError) as exc:  # pragma: no cover - a bad rule
                self.fail(f"binding {index} cites {rule.source}, which fails: {exc}")

    def test_the_prediction_indices_the_rules_cite_are_the_ones_they_name(self) -> None:
        """A cited ``scored[i]`` must still be the prediction it was written for.

        The rules above reach P4, P14 and P22 by position.  If that list were
        reordered the positions would silently point at other predictions and
        every check built on them would compare the wrong pair of numbers.
        """
        for index, want in ((3, "P4"), (13, "P14"), (21, "P22")):
            self.assertEqual(
                dig(receipt("side_free"), f"predictions.scored[{index}].id"),
                want,
                f"predictions.scored[{index}] is no longer {want}",
            )


class WholeFileExemptions(unittest.TestCase):
    def test_the_frozen_files_still_carry_their_pinned_digests(self) -> None:
        for name in ("DESIGN.md", "PREDICTIONS.md"):
            got = hashlib.sha256((TREE / name).read_bytes()).hexdigest()
            self.assertEqual(
                got,
                verify_pins.FROZEN[name],
                f"{name} is exempt from this gate ONLY because its bytes are "
                "pinned; that pin no longer holds",
            )

    def test_the_rendered_document_is_a_function_of_the_record(self) -> None:
        record = json.loads(
            (TREE / "receipts" / "comparison.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            comparison.document(record),
            (TREE / "COMPARISON.md").read_bytes(),
            "COMPARISON.md is exempt from this gate ONLY because it is a "
            "function of receipts/comparison.json; re-rendering the committed "
            "receipt no longer reproduces the committed document",
        )


class ProseNumbers(unittest.TestCase):
    def test_every_prose_number_is_classified(self) -> None:
        unclassified, _, _ = report()
        self.assertEqual(
            unclassified,
            [],
            "TOTALITY: these prose numbers are bound to nothing.  A count in "
            "prose that no record field carries is the defect this gate "
            "exists to catch.\n" + "\n".join(unclassified),
        )

    def test_every_bound_number_equals_the_field_it_names(self) -> None:
        _, mismatched, _ = report()
        self.assertEqual(
            mismatched, [], "STATED AGAINST TRUE:\n" + "\n".join(mismatched)
        )

    def test_no_rule_outlives_the_line_it_was_written_for(self) -> None:
        _, _, stale = report()
        self.assertEqual(stale, [], "STALE RULES:\n" + "\n".join(stale))


def main(argv: list[str]) -> int:  # pragma: no cover - operator entry point
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    if "--census" in argv:
        for name, numbers in population().items():
            digits = sum(1 for number in numbers if number.kind == "digit")
            words = sum(1 for number in numbers if number.kind == "word")
            print(f'    "{name}": ({digits}, {words}),')
        return 0
    unclassified, mismatched, stale = report()
    for line in unclassified:
        print(f"UNCLASSIFIED: {line}")
    for line in mismatched:
        print(f"MISMATCH: {line}")
    for line in stale:
        print(f"STALE: {line}")
    print(
        f"prose numbers: {sum(len(v) for v in population().values())} gathered, "
        f"{len(unclassified)} unclassified, {len(mismatched)} mismatched, "
        f"{len(stale)} stale"
    )
    return 1 if unclassified or mismatched or stale else 0


if __name__ == "__main__":  # pragma: no cover - operator entry point
    if len(sys.argv) > 1 and sys.argv[1].startswith("--"):
        sys.exit(main(sys.argv[1:]))
    unittest.main()
