"""The rung's refusal scans.  Any hit fails the run.  AuthorityEffect: None.

Five scans, each named for what it can see and, where it matters, for what
it cannot.

``RefusedVocabularyScan``.  The operator packet that drives this rung is
written in outside vocabulary.  None of that vocabulary may reach a file of
this tree.  The terms are held ONLY as SHA-256 digests in
``REFUSED_VOCABULARY``: a plaintext list would itself be the thing the scan
watches for, and CLAUDE.md records a refused outside grid on exactly that
ground -- describe, never name.  Digests are not secrets;
``python ci/check_prose_watchlist.py --probe WORD`` says whether a word is
in a table and writes nothing.  Every file of the tree is scanned, this one
included, and a gzipped member is decompressed before scanning rather than
dropped.  The only exemption is the sixty-four character hex RUNS of this
file's own digest tables, and it is granted to those runs and not to the
lines that carry them: an earlier version blanked the whole line, so
plaintext parked after a table entry was invisible to this scan, and a
reviewer demonstrated it with a live term.  The exemption is now
``HEX64_LITERAL.sub``, and it is keyed on this file's RESOLVED path, so a
second file of the same basename elsewhere in the tree inherits nothing.

``CensusScan``.  The repository's own census scanner, run over every file of
the write root with zero tolerance.  Its pin is read and never rewritten
here.  Its reach is the watchlist's own table, which is a file outside this
tree: ``ci/prose_watchlist.json`` is therefore pinned in
``SOURCE_MANIFEST.json``, so a committed prune of that table fails
``verify_pins.py`` instead of silently shrinking this scan, and the scan
additionally asserts a floor on the watched-term count so a pruned table
cannot pass here vacuously.

``DenylistScan``.  The one hundred and two working names of
``contact/analysis/contact_countermodels.json``, matched as WHOLE
IDENTIFIERS rather than as substrings.  The substring form was a defect the
author repaired in ``research/closed_family``: a sealed native name there
CONTAINS a denylist name as a substring, so the substring form flagged the
sealed name.  The firewall bars identifiers, so the scan matches
identifiers, with underscore and digits counted as identifier characters.
The count assertion is a vacuity guard and NOT a content pin -- substituting
one name for another preserves it -- so the census file is pinned in
``SOURCE_MANIFEST.json``, and the pin, not the count, is what fixes which
names are barred.

What NEITHER this scan nor the two above reaches: an outside word carried by
a new ``snake_case`` or ``SCREAMING_SNAKE`` identifier of this tree's own
modules.  This scan bars one hundred and two enumerated names and no others,
and the two word-level scans treat ``_`` and digits as word characters, so
such an identifier is seen by nothing here.  That is the repository-level
residual CLAUDE.md records, restated rather than glossed: the identifier
firewall is not open-ended coverage.

``SealedAndSharedPathScan``.  ``git status --porcelain`` reports no
unignored working-tree or index change under a sealed prefix and none
outside this rung's declared write set.  BOTH sides of a rename or copy
entry are checked: keeping only the destination let a sealed file be MOVED
into the write root and reported clean by both halves, which a reviewer
demonstrated on a real ``git mv`` record.  The committed snapshot-to-HEAD
population attributable to this rung is a separate NUL-safe check in
``verify_pins.py``.

``GuardedWordScan``.  The SEVEN words CLAUDE.md's assumption discipline
guards, plus ``engine`` from this rung's own operator brief -- eight in all
-- may appear in prose only on a line that also names a scope, a proof, or
an evidence class.  They are held as digests too, so this file needs no
self-exemption for them.  An earlier version of this sentence said six and
the table held six: two of CLAUDE.md's seven were absent.  No live breach
was found when they were added, so this closed a latent hole and not an
escape.

What the guarded scan CANNOT see, stated so a pass is not read as more than
it is.  (a) It reads Markdown pages and the comment and string tokens of
Python modules; JSON, TOML and attribute files are machine data, and a
guarded word inside one is invisible to it -- a receipt key or a pinned path
is not a claim, but neither is anything else in those files checked.  (b) A
word inside backticks is treated as a code citation and dropped before
matching, so a claim smuggled inside a backticked span is invisible.  (c) A
claim split across two lines, with the guarded word on one line and its
scope on the next, passes.  (d) The marker set is generous: any
SCREAMING_SNAKE token satisfies it, so a line carrying an unrelated terminal
name carries a marker whether or not that terminal scopes the claim.  (e)
Only the exact words and their ``s``/``es`` plurals are matched; an adverbial
or nominal form of the same claim is not reached.  (f) The two frozen inputs
are skipped, because they were hashed before this file existed and cannot be
edited to satisfy it.  A pass therefore means "no unscoped guarded word was
found by this construction", never "the prose is honest".

How much that pass is worth, measured rather than assumed.  Sweeping this
tree's prose with the scan's own construction finds a handful of occurrences,
almost all of them spared, and at least one is spared by an unrelated
SCREAMING_SNAKE token on the same line rather than by anything that scopes the
claim -- caveat (d), live.  Do not cite a pass here as evidence that the
tree's prose is scoped.  The scan HAS bitten once: adding the two CLAUDE.md
words the table had dropped flagged a line of ``test_stream.py`` on the first
run afterwards, and that line was reworded rather than marked.
"""

from __future__ import annotations

import gzip
import importlib.util
import io
import json
import re
import sys
import tokenize
import unittest
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
WRITE_ROOT = "research/second_stream/"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import verify_pins as VP  # noqa: E402

SEALED_PREFIXES = ("prompt/", "paper/", "code/", "lean4/Derivation/", "artifacts/")

# The rung's declared write set: this tree, the two handoff pages of the
# run's own directory, and the workflow the rung registers itself in.  A
# path outside it fails, whether modified or untracked.
ALLOWED_PREFIXES = (WRITE_ROOT,)
ALLOWED_PATHS = (
    ".github/workflows/verify.yml",
    "research/second/HANDOFF.md",
    "research/second/MANUAL.md",
)

SKIP_DIRS = frozenset(
    {".git", ".lake", ".mypy_cache", ".pytest_cache", ".ruff_cache", "__pycache__", "htmlcov"}
)

# A coverage run drops an SQLite database beside the modules it records.
# It is gitignored at the repository root, carries no prose, and is not a
# file of the rung; running coverage must not change what the scans below
# see. Parallel coverage mode is not configured, so the one exact database
# name is excluded and a similarly prefixed payload remains in the census.
SKIP_FILES = frozenset({".coverage"})

# Hashed before this file existed, and never edited to satisfy it.  The
# sentence-level scan below skips them; the vocabulary, census and denylist
# scans do NOT.
FROZEN_INPUTS = ("PROMPT.md", "PREDICTIONS.md")

# The number of terms ``ci/prose_watchlist.json`` carried when this rung was
# calibrated against it.  A FLOOR and not an equality: the author may extend
# that table, and an extension only widens the census scan below.  A PRUNE
# narrows it, which is the direction that hides a hit, so a table below this
# floor fails here.  The exact bytes are pinned in ``SOURCE_MANIFEST.json``,
# so an extension is still a repin obligation and not a silent change.
WATCHED_TERM_FLOOR = 49

# ---------------------------------------------------------------------------
# The digest tables.  No plaintext appears in this file.
# ---------------------------------------------------------------------------

# Outside vocabulary carried by the operator packet.  Each tag records only
# how many whole words the term has, which is what the scan needs in order to
# know which passes to run; the tag names nothing.  Sorted by digest, so the
# order of the table carries no correspondence to the order of any list.
REFUSED_VOCABULARY: dict[str, str] = {
    "0adc36057cef79f8a7b8a862bb9fab8cbdc13828498c636c4d92d761fd621a0f": "outside term, 1-word",
    "0ec5fcd5aef97a5b2d76142b945331f2cd133f47c394a3d0c12bfd19dd23438f": "outside term, 2-word",
    "0ecdd9c9b94ebdb4968cb7b69b13e790e00f691841f88c25ed87f2e15adfbf8f": "outside term, 3-word",
    "0fd19d4493362e556af1ebdc48882cd4e0716760b125936ec8a00e8baeeac054": "outside term, 1-word",
    "1124524a9be2dc24e6756eb4d7ad60802ab0687b50d9e74b13eac0de598a8bbb": "outside term, 2-word",
    "28f52601458acbe2fb886c414f02767bfafc9547f0a4bb558300ef977bb703ad": "outside term, 3-word",
    "2db681579fbe43e8e0d7ae0a009fa8b894d17934454ded75431f7b6c34d602f9": "outside term, 1-word",
    "2e202645e0bf719435a77324a025ec6c3ba59bd3ab0a775bee675a5160bc5d70": "outside term, 1-word",
    "3632ba7b1f3c76983fc85ebdd7a0a0a990680cd8ea6154e3802910fd625d89f3": "outside term, 1-word",
    "3fb06d49cb3c247cb1b7afbd7fd7efaa73175f4e341a63b49b83c168d8d0b1cf": "outside term, 3-word",
    "3fe9a8dfca0f4e96aa36bca306729179202f3854488648a3aca7bdf80bc1bb81": "outside term, 1-word",
    "5b693ab9fb721a2434b5087726703c18e1a46dc358a8fa2e79192dc0964177bf": "outside term, 1-word",
    "64b3f29ddeb1d678feeda3cc8f87d1b1f9d196397de5799b53cf33eba030147d": "outside term, 1-word",
    "6c5a6990038d66c5ecddf6c983345ed18acc416e188ff1476e3cd7201699aaed": "outside term, 1-word",
    "6cd7417d01d9d074880f6280667dd884bc8147a69e37b5807eb6b41739ab56ed": "outside term, 1-word",
    "88fe58c62a73c6a6d3f6022a576aaf410c79e5518e16f6ebc2b1fc7319767997": "outside term, 1-word",
    "a573833103933aeb214663a6554b2c8753e666b4c7656102b5e16142d1ab4ccb": "outside term, 1-word",
    "ac5e23b45528ce0f608e34153b8b4740931ac57f1d4c73ff56da5b3e9bcf0fc6": "outside term, 1-word",
    "b28a1b683a70224b6bfcdf1de6c3f7789609dc9ca2d3e557a9dfa5a7d28bcba2": "outside term, 2-word",
    "b29175341d7f6f72bf0bb666c59c3143ca7d3ddc3763772e66af0c3a16510404": "outside term, 1-word",
    "b3ec4a7517ce59208d02a2df9d0172c772be0f6ae504ba216fec2408188df823": "outside term, 2-word",
    "b98289b749d9d30657d0f92bdfa37e56cfb82d218584dd031cce9d61338ccdd7": "outside term, 1-word",
    "c2961d2b0892e9ca7fdac14ecf5b1b33ffbc88ea6c0d282ba86ac08916c52c47": "outside term, 2-word",
    "ce6d7c9f2019b56186229be01cd8c09f14f43d0b3ce4ccfb93bf5af901ca7a8e": "outside term, 2-word",
    "e433ceea3ec18922b47d3e91bad7ee888123fd5772763eabf88ab888efd668d3": "outside term, 3-word",
    "e6e2b826e31fca5c36125c48f130dcb6f961e698ff8a8776a1f290cf0892e8e6": "outside term, 1-word",
    "f7496f1fc9731f2ed7dd3f1d968469b89382f5f9030a86e08638f638699264f9": "outside term, 1-word",
    "fab566a669ed153bb8b8aa7321678778ab8e0e0dbe1701146d8a07386e31ab3e": "outside term, 1-word",
}

# The seven words CLAUDE.md's assumption discipline guards, plus one from
# this rung's own operator brief, as digests, sorted.  Two of the seven were
# missing while the comment above them said six; a reviewer resolved the
# table against the clause and named them.
GUARDED_WORDS: tuple[str, ...] = (
    "0deeb8fa1dbbee4c0dbe7f5e3c9183940139f26d22797ee8ab07c00557a4c2ff",
    "38c8632dfc3b9f597420c9564a4850f9176ae335bc06fd04d0c60cbfcb58616a",
    "a703788f832056626d71b7db4d8055243ceafe416d1798cd634b9143c9074b54",
    "a9fd078562420a276b6902ca3d8bf583c0366e38af72e23be99b16035a76b39a",
    "ad95d5fa651ba86d8923fe1238d24a4f1988a752acfe426ac72ac7c04471bc17",
    "cc73c906e945aa99228f8b61869a81f099a4541b33ee1d1f58ac5dbe5894e5a6",
    "ed9f6f25068608efd412958da4dfc19328ca3511251fa6d5f9c42baf230e32f8",
    "eebbf6457e46a7f63acdf9b97390f790ba443d60cfa44b607da7e5c40aa1cc1d",
)

HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX64_LITERAL = re.compile(r'"([0-9a-f]{64})"')
TAG_SHAPE = re.compile(r"^outside term, (\d+)-word$")
BACKTICKED = re.compile(r"`[^`]*`")

# A line carrying a guarded word must also carry one of these: a named
# theorem, test or function; a terminal or evidence class; a proof word; or
# an explicit statement of scope.
SCOPE_MARKER = re.compile(
    r"`\w*_\w*`"
    r"|\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b"
    r"|\bLean\b"
    r"|\bPROVED\b|\bCONJECTURE\b|\bOPEN\b|\bREFUSED\b|\bCOUNTERMODEL\b|\bVACUOUS\b"
    r"|\bproof\b|\bproved\b|\bproves\b|\btheorem\b|\bcertificate\b|\bcertified\b"
    r"|\bscope\b|\bscoped\b|\bbound\b|\bbounds\b|\bbounded\b"
    r"|\bdeclared\b|\bdeclares\b|\bwithin\b|\bat most\b|\bunder the\b|\bthis rung\b"
)


# ---------------------------------------------------------------------------
# One definition of a whole word, borrowed rather than restated.
# ---------------------------------------------------------------------------


class HitLike(Protocol):
    """The census scanner's hit record: 1-based line, surface, digest."""

    @property
    def line(self) -> int: ...

    @property
    def surface(self) -> str: ...

    @property
    def digest(self) -> str: ...


def load_scanner() -> ModuleType:
    """The repository's census scanner, loaded by path.

    Loaded rather than restated so that there is exactly one definition in
    this repository of what a whole word is, of how a word is normalized,
    and of which plurals a word reaches.  A change to its tokenizer or its
    plural rule changes what this file can see, which is why the rung pins
    it: among the frozen texts, at HEAD, since 2026-09-18.
    """

    spec = importlib.util.spec_from_file_location(
        "second_stream_prose_scanner", REPO / "ci" / "check_prose_watchlist.py"
    )
    if spec is None or spec.loader is None:
        raise AssertionError("ci/check_prose_watchlist.py could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCANNER = load_scanner()

word_digest: Callable[[str], str] = cast(Callable[[str], str], SCANNER.digest)
words_of: Callable[[str], list[str]] = cast(Callable[[str], list[str]], SCANNER.tokens)
stems_of: Callable[[str], list[str]] = cast(Callable[[str], list[str]], SCANNER.stems)
read_text: Callable[[Path], str | None] = cast(
    Callable[[Path], str | None], SCANNER.read_text
)
scan_text: Callable[[str, Mapping[str, str]], list[HitLike]] = cast(
    Callable[[str, Mapping[str, str]], list[HitLike]], SCANNER.scan_text
)
load_watchlist: Callable[[Path], dict[str, object]] = cast(
    Callable[[Path], dict[str, object]], SCANNER.load
)
WATCHLIST_REL: str = cast(str, SCANNER.WATCHLIST_REL)


# ---------------------------------------------------------------------------
# The write root's files
# ---------------------------------------------------------------------------


def readable_text(path: Path) -> str | None:
    """The text of one file of the tree, or ``None`` when it has none.

    A gzipped member is DECOMPRESSED and then scanned.  Dropping it left the
    compressed export -- two megabytes of the run's own output -- read by no
    scan at all, while the module docstring said every file of the tree was
    scanned.  A member whose decompressed bytes are not UTF-8 is reported
    unreadable the way any other binary file is.
    """

    if path.suffix == ".gz":
        try:
            return gzip.decompress(path.read_bytes()).decode("utf-8")
        except (OSError, gzip.BadGzipFile, UnicodeDecodeError):
            return None
    return read_text(path)


def tree_files() -> list[Path]:
    """Every file of the write root, tracked or not, minus build caches."""

    return sorted(
        f
        for f in HERE.rglob("*")
        if f.is_file()
        and not (set(f.parts) & SKIP_DIRS)
        and f.name not in SKIP_FILES
    )


def prose_files() -> list[Path]:
    """The files the guarded-word scan reads: this tree's own Markdown pages
    and Python modules, minus the two frozen inputs."""

    return [
        f
        for f in tree_files()
        if f.suffix in (".md", ".py") and f.name not in FROZEN_INPUTS
    ]


def relative(path: Path) -> str:
    return path.relative_to(HERE).as_posix()


# ---------------------------------------------------------------------------
# The phrase pass
# ---------------------------------------------------------------------------


def term_sizes(watched: Mapping[str, str]) -> tuple[int, ...]:
    """The word counts the table declares, ascending."""

    sizes: set[int] = set()
    for tag in watched.values():
        match = TAG_SHAPE.match(tag)
        if match is None:
            raise AssertionError(f"tag does not declare a word count: {tag!r}")
        sizes.add(int(match.group(1)))
    return tuple(sorted(sizes))


def scan_phrases(
    text: str, watched: Mapping[str, str], sizes: Sequence[int]
) -> list[tuple[int, str]]:
    """Every hit of an ``n``-word term, for each ``n`` in ``sizes``.

    A phrase is the space-joined run of ``n`` adjacent whole words on one
    line, with the LAST word allowed to stand for its de-pluralized forms.
    That is exactly the census scanner's own two-word rule, generalized to
    ``n``; the one-word and two-word cases are cross-checked against it in
    ``PhrasePassTests``.  Runs do not cross a line break, so a term split
    over two lines is not reached -- the same reach the scanner has.
    """

    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        toks = words_of(line)
        for i, _ in enumerate(toks):
            for n in sorted(sizes):
                if i + n > len(toks):
                    continue
                head = toks[i : i + n - 1]
                for form in stems_of(toks[i + n - 1]):
                    phrase = " ".join([*head, form])
                    if word_digest(phrase) in watched:
                        hits.append((line_no, " ".join(toks[i : i + n])))
                        break
    return hits


def strip_digest_literals(text: str) -> str:
    """This file's own digest tables, blanked -- the RUNS OF HEX only.

    This is the one exemption the vocabulary scan grants, and it is granted
    to nothing else.  It removes nothing a scan could see: a sixty-four
    character run of hex contains no word boundary, so the tokenizer yields
    no whole word from it, and every other character of the line survives.

    An earlier version returned a predicate and the caller blanked the WHOLE
    LINE.  That was an escape and not a technicality: a reviewer appended a
    watched plaintext term as a trailing comment on a table entry and every
    test of this file stayed green with the term sitting in a tree file.
    The substitution below is the repair; it changes no line count, so a
    reported line number stays true.
    """

    return HEX64_LITERAL.sub(" ", text)


SELF_PATH = Path(__file__).resolve()


def refused_vocabulary_hits() -> list[str]:
    """Every outside-term hit in the write root, as ``path:line: surface``.

    The exemption is keyed on the RESOLVED path of this module, not on its
    basename: a second file of the same name elsewhere in the tree would
    otherwise inherit it.
    """

    sizes = term_sizes(REFUSED_VOCABULARY)
    hits: list[str] = []
    for path in tree_files():
        text = readable_text(path)
        if text is None:
            continue
        if path.resolve() == SELF_PATH:
            text = strip_digest_literals(text)
        for line_no, surface in scan_phrases(text, REFUSED_VOCABULARY, sizes):
            hits.append(f"{relative(path)}:{line_no}: {surface}")
    return sorted(hits)


# ---------------------------------------------------------------------------
# The porcelain
# ---------------------------------------------------------------------------


def porcelain_paths(record: str) -> list[tuple[str, str]]:
    """``(line, path)`` for EVERY path an entry of ``git status --porcelain``
    output names.

    A rename or copy entry reports ``old -> new`` and names TWO paths.  An
    earlier version kept the destination alone, on the reading that the
    destination is the path the run touched.  That was wrong in the
    direction that matters: ``git mv paper/paper.md
    research/second_stream/borrowed.md`` produces exactly one such entry,
    and with the source dropped the move was reported clean by BOTH the
    sealed-path check and the write-set check.  Both sides are returned, so
    a sealed source fails on its source and an outside destination fails on
    its destination.
    """

    out: list[tuple[str, str]] = []
    for line in record.splitlines():
        if not line.strip():
            continue
        raw = line[3:].strip()
        for part in raw.split(" -> "):
            out.append((line, part.strip().strip('"').replace("\\", "/")))
    return out


def _lines_once(pairs: Sequence[tuple[str, str]]) -> list[str]:
    """The named lines, each at most once, in the order they were named.

    A rename whose two sides both fail names one entry, not two.
    """

    seen: dict[str, None] = {}
    for line, _path in pairs:
        seen.setdefault(line, None)
    return list(seen)


def sealed_paths_touched(record: str) -> list[str]:
    return _lines_once(
        [
            (line, path)
            for line, path in porcelain_paths(record)
            if path.startswith(SEALED_PREFIXES)
        ]
    )


def outside_write_set(record: str) -> list[str]:
    return _lines_once(
        [
            (line, path)
            for line, path in porcelain_paths(record)
            if not (path.startswith(ALLOWED_PREFIXES) or path in ALLOWED_PATHS)
        ]
    )


# ---------------------------------------------------------------------------
# The guarded-word pass
# ---------------------------------------------------------------------------


def prose_lines(path: Path, text: str) -> tuple[list[tuple[int, str]], str | None]:
    """The human prose of a file, with 1-based line numbers, and an error.

    A Markdown page is prose throughout.  A Python module is prose only in
    its comments and its string literals; its identifiers are the identifier
    firewall's business, and its expressions are not claims.  A module that
    cannot be tokenized is reported rather than skipped.
    """

    if path.suffix == ".md":
        return [(n, line) for n, line in enumerate(text.splitlines(), start=1)], None
    out: list[tuple[int, str]] = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type not in (tokenize.COMMENT, tokenize.STRING):
                continue
            for offset, line in enumerate(tok.string.splitlines()):
                out.append((tok.start[0] + offset, line))
    except (tokenize.TokenError, SyntaxError, IndentationError) as exc:
        return out, f"{relative(path)}: prose could not be read: {exc}"
    return out, None


def unscoped_guarded_words() -> tuple[list[str], list[str]]:
    """``(failures, errors)``: guarded words on lines that name no scope."""

    watched = {d: "guarded" for d in GUARDED_WORDS}
    failures: list[str] = []
    errors: list[str] = []
    for path in prose_files():
        text = read_text(path)
        if text is None:
            continue
        lines, error = prose_lines(path, text)
        if error is not None:
            errors.append(error)
        for line_no, line in lines:
            if SCOPE_MARKER.search(line) is not None:
                continue
            for tok in words_of(BACKTICKED.sub(" ", line)):
                if any(word_digest(form) in watched for form in stems_of(tok)):
                    failures.append(
                        f"{relative(path)}:{line_no}: guarded word {tok!r} "
                        f"on a line naming no scope, proof, or evidence class"
                    )
    return sorted(failures), sorted(errors)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class DigestTableTests(unittest.TestCase):
    def test_tables_are_digests_and_nothing_else(self) -> None:
        self.assertEqual(len(REFUSED_VOCABULARY), 28)
        self.assertEqual(len(GUARDED_WORDS), 8)
        for key, tag in REFUSED_VOCABULARY.items():
            self.assertIsNotNone(HEX64.match(key), f"not a digest: {key!r}")
            self.assertTrue(tag, f"empty tag for {key[:12]}")
            self.assertIsNotNone(TAG_SHAPE.match(tag), f"tag shape: {tag!r}")
        for key in GUARDED_WORDS:
            self.assertIsNotNone(HEX64.match(key), f"not a digest: {key!r}")
        self.assertEqual(len(set(GUARDED_WORDS)), len(GUARDED_WORDS))
        self.assertEqual(
            set(REFUSED_VOCABULARY) & set(GUARDED_WORDS),
            set(),
            "a term is in both tables",
        )

    def test_no_digest_literal_is_written_twice(self) -> None:
        """A duplicate key in a dict literal collapses silently, so the
        table's own source text is counted rather than the parsed dict."""

        literals = HEX64_LITERAL.findall(Path(__file__).read_text("utf-8"))
        self.assertEqual(len(literals), len(set(literals)), "a digest is written twice")
        self.assertEqual(
            sorted(set(literals)),
            sorted(set(REFUSED_VOCABULARY) | set(GUARDED_WORDS)),
        )

    def test_table_order_is_sorted_by_digest(self) -> None:
        self.assertEqual(list(REFUSED_VOCABULARY), sorted(REFUSED_VOCABULARY))
        self.assertEqual(list(GUARDED_WORDS), sorted(GUARDED_WORDS))

    def test_every_declared_word_count_is_actually_scanned(self) -> None:
        """A term tagged with a word count the phrase pass does not run
        would be watched by the table and seen by nothing."""

        sizes = term_sizes(REFUSED_VOCABULARY)
        self.assertEqual(sizes, (1, 2, 3))
        text = "a b c d e f"
        self.assertEqual(scan_phrases(text, {}, sizes), [])


class PhrasePassTests(unittest.TestCase):
    def test_one_and_two_word_passes_agree_with_the_census_scanner(self) -> None:
        """The phrase pass generalizes the scanner's own rule rather than
        replacing it: at one and two words the two must agree exactly, hit
        for hit and in the same order."""

        probe = {word_digest("zzprobe"): "t", word_digest("zzprobe alpha"): "t"}
        text = (
            "zzprobes zzprobe ZZPROBE\n"
            "zzprobed zzprobe_x\n"
            "zzprobe alphas and zzprobe alpha\n"
        )
        theirs = [(h.line, h.surface) for h in scan_text(text, probe)]
        mine = scan_phrases(text, probe, (1, 2))
        self.assertEqual(mine, theirs)

    def test_three_word_terms_are_reached_only_by_the_phrase_pass(self) -> None:
        probe = {word_digest("zzprobe beta gamma"): "t"}
        text = "the zzprobe beta gammas here\n"
        self.assertEqual([h.surface for h in scan_text(text, probe)], [])
        self.assertEqual(scan_phrases(text, probe, (1, 2, 3)), [(1, "zzprobe beta gammas")])

    def test_injected_probe_word_is_seen_exactly_where_expected(self) -> None:
        """The scan's reach, pinned on a neutral word.  Two lessons are
        pinned at once: a trailing ``s`` is reached, and a word inside an
        identifier is NOT -- identifiers stay with the firewall below."""

        probe = {word_digest("zzprobe"): "t"}
        text = "zzprobes zzprobe ZZPROBE\nzzprobed zzprobe_x"
        self.assertEqual(
            [(h.line, h.surface) for h in scan_text(text, probe)],
            [(1, "zzprobes"), (1, "zzprobe"), (1, "zzprobe")],
        )
        self.assertEqual(
            scan_phrases(text, probe, (1,)),
            [(1, "zzprobes"), (1, "zzprobe"), (1, "zzprobe")],
        )

    def test_digest_table_exemption_removes_no_readable_word(self) -> None:
        """The one exemption is exercised, and shown to remove only hex: a
        hex run carries no word boundary, so blanking it changes nothing a
        scan could have seen."""

        probe = {word_digest("zzprobe"): "t"}
        line = '    "' + "0" * 64 + '": "outside term, 1-word",'
        self.assertEqual(scan_phrases(line, probe, (1, 2, 3)), [])
        self.assertEqual(scan_phrases(strip_digest_literals(line), probe, (1, 2, 3)), [])
        self.assertNotIn("0" * 64, strip_digest_literals(line))
        self.assertIn("outside term, 1-word", strip_digest_literals(line))

    def test_a_table_line_carrying_prose_is_still_scanned(self) -> None:
        """The escape a reviewer demonstrated, pinned as a test.

        A watched word parked as a trailing comment on a table entry used to
        be blanked with the line.  It must survive the exemption and be
        reported, and the line number must still be the line it sits on.
        """

        probe = {word_digest("zzprobe"): "t"}
        entry = '    "' + "0" * 64 + '": "outside term, 1-word",  # zzprobe rides here'
        text = "\n".join(["a first line", entry, "a third line"])
        stripped = strip_digest_literals(text)
        self.assertEqual(len(stripped.splitlines()), 3)
        self.assertEqual(scan_phrases(stripped, probe, (1, 2, 3)), [(2, "zzprobe")])

    def test_the_exemption_is_keyed_on_this_module_and_not_on_a_basename(self) -> None:
        """A second file of the same basename elsewhere in the tree must
        inherit nothing; the key is the resolved path."""

        self.assertEqual(SELF_PATH, Path(__file__).resolve())
        self.assertNotEqual(SELF_PATH, HERE / "sub" / Path(__file__).name)


class RefusedVocabularyScan(unittest.TestCase):
    def test_no_outside_term_in_the_write_root(self) -> None:
        """The operator packet's vocabulary reaches no file of this tree,
        the frozen inputs and this file included."""

        self.assertEqual(refused_vocabulary_hits(), [])

    def test_the_scan_reads_every_file_of_the_write_root(self) -> None:
        """A scan that reads nothing passes vacuously, so the population is
        asserted to be non-trivial, to contain the frozen inputs, and -- the
        clause that was missing -- to yield TEXT for every one of its files.

        A file silently dropped by the reader satisfied the name checks
        while being read by no scan.  The compressed export was exactly that
        file, and is now decompressed rather than dropped.
        """

        paths = tree_files()
        names = {f.name for f in paths}
        self.assertIn(".coverage", SKIP_FILES)
        self.assertNotIn(".coverage_payload.md", SKIP_FILES)
        self.assertGreaterEqual(len(names), 4)
        for frozen in FROZEN_INPUTS:
            self.assertIn(frozen, names, f"{frozen} is not in the scanned population")
        self.assertIn(Path(__file__).name, names, "the scan file is not scanned")
        unreadable = sorted(relative(f) for f in paths if readable_text(f) is None)
        self.assertEqual(unreadable, [], "a file of the tree is read by no scan")
        compressed = sorted(relative(f) for f in paths if f.suffix == ".gz")
        self.assertTrue(compressed, "the compressed export is not in the population")
        for name in compressed:
            text = readable_text(HERE / name)
            self.assertIsNotNone(text)
            self.assertGreater(len(text or ""), len(name))


class CensusScan(unittest.TestCase):
    def test_no_watched_prose_word_in_the_write_root(self) -> None:
        """The repository's census scanner run over every file of the write
        root, tracked or not, must find nothing; the pin is read here and
        never rewritten."""

        data = load_watchlist(REPO / WATCHLIST_REL)
        watched = cast(Mapping[str, str], data["watched"])
        self.assertGreaterEqual(
            len(watched),
            WATCHED_TERM_FLOOR,
            "the repository watchlist has fewer terms than this scan was "
            "calibrated against; a pruned table shrinks this scan's reach "
            "and must not pass quietly",
        )
        hits: list[str] = []
        for path in tree_files():
            text = readable_text(path)
            if text is None:
                continue
            for hit in scan_text(text, watched):
                hits.append(f"{relative(path)}:{hit.line}: {hit.surface}")
        self.assertEqual(sorted(hits), [])


class DenylistScan(unittest.TestCase):
    def test_no_working_denylist_identifier_in_the_write_root(self) -> None:
        census = json.loads(
            (REPO / "contact" / "analysis" / "contact_countermodels.json").read_text("utf-8")
        )
        full = set(census["denylist"]["full_census"])
        subtracted = set(census["denylist"]["subtracted_as_native_or_core"])
        working = sorted(full - subtracted)
        # A vacuity guard, NOT a content pin: substituting one name for
        # another preserves the count.  The census file is pinned in
        # SOURCE_MANIFEST.json, and the pin is what fixes which names are
        # barred.
        self.assertEqual(len(working), 102)
        pattern = re.compile(
            r"(?<![A-Za-z0-9_])(?:" + "|".join(re.escape(n) for n in working) + r")(?![A-Za-z0-9_])"
        )
        hits: list[str] = []
        for path in tree_files():
            text = readable_text(path)
            if text is None:
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                for match in pattern.finditer(line):
                    hits.append(f"{relative(path)}:{line_no}: {match.group(0)}")
        self.assertEqual(sorted(hits), [])

    def test_the_firewall_matches_identifiers_and_not_substrings(self) -> None:
        """Whole-identifier matching, not substring matching.  The substring
        form was a defect the author repaired in ``research/closed_family``,
        where a sealed native name CONTAINS a denylist name and the
        substring form therefore flagged the sealed name."""

        pattern = re.compile(r"(?<![A-Za-z0-9_])" + re.escape("ZzProbeName") + r"(?![A-Za-z0-9_])")
        self.assertIsNotNone(pattern.search("uses ZzProbeName here"))
        self.assertIsNone(pattern.search("uses ZzProbeNameSuffix here"))
        self.assertIsNone(pattern.search("uses zzZzProbeName here"))
        self.assertIsNone(pattern.search("uses ZzProbeName_tail here"))
        self.assertIsNone(pattern.search("uses ZzProbeName2 here"))


class SealedAndSharedPathScan(unittest.TestCase):
    def test_the_porcelain_checks_are_pure_functions_of_the_record(self) -> None:
        """The injection for this scan is synthetic: writing a probe file
        outside the write root would itself be the breach the scan exists to
        refuse, so the checks are exercised on porcelain text instead."""

        record = (
            "?? research/zzz_probe.txt\n"
            "?? research/second_stream/receipts/stream.json\n"
            " M artifacts/claims.json\n"
            " M .github/workflows/verify.yml\n"
            "R  research/second/MANUAL.md -> research/second/HANDOFF.md\n"
        )
        self.assertEqual(
            sealed_paths_touched(record), [" M artifacts/claims.json"]
        )
        self.assertEqual(
            outside_write_set(record),
            ["?? research/zzz_probe.txt", " M artifacts/claims.json"],
        )
        # A rename whose SOURCE is sealed and whose destination is inside
        # the write root.  The destination-only reader called this clean on
        # both halves; the record shape is the one `git mv` actually emits.
        moved = "R  paper/paper.md -> research/second_stream/borrowed.md"
        self.assertEqual(sealed_paths_touched(moved), [moved])
        self.assertEqual(outside_write_set(moved), [moved])
        copied = "C  prompt/prompt.md -> research/second_stream/p.md"
        self.assertEqual(sealed_paths_touched(copied), [copied])
        # Both sides failing names the entry once, not twice.
        both = "R  paper/paper.md -> artifacts/claims.json"
        self.assertEqual(sealed_paths_touched(both), [both])
        self.assertEqual(outside_write_set(both), [both])
        self.assertEqual(sealed_paths_touched(""), [])
        self.assertEqual(outside_write_set(" M paper/paper.md\n"), [" M paper/paper.md"])
        self.assertEqual(sealed_paths_touched(" M paper/paper.md\n"), [" M paper/paper.md"])
        self.assertEqual(
            outside_write_set("?? research/second_stream/x\n M research/second/MANUAL.md\n"),
            [],
        )

    def test_nothing_sealed_or_shared_is_touched(self) -> None:
        """No modified or untracked path under a sealed prefix, and none
        outside the rung's declared write set."""

        paths = VP._worktree_paths()
        try:
            VP._check_paths(paths, "working tree/index")
        except ValueError as exc:
            self.fail(str(exc))


class GuardedWordScan(unittest.TestCase):
    def test_a_guarded_word_in_prose_names_a_scope(self) -> None:
        failures, errors = unscoped_guarded_words()
        self.assertEqual(errors, [])
        self.assertEqual(failures, [])

    def test_the_scan_sees_an_unscoped_word_and_spares_a_scoped_one(self) -> None:
        """Exercised in memory on the same construction the scan runs, so a
        pass above is not a pass of a scan that matches nothing."""

        watched = {d: "guarded" for d in GUARDED_WORDS}

        def unscoped(line: str) -> bool:
            if SCOPE_MARKER.search(line) is not None:
                return False
            return any(
                word_digest(form) in watched
                for tok in words_of(BACKTICKED.sub(" ", line))
                for form in stems_of(tok)
            )

        self.assertTrue(unscoped("the response is " + "min" + "imal"))
        self.assertFalse(
            unscoped("the response is " + "min" + "imal within the declared bound")
        )
        self.assertFalse(unscoped("the sealed `" + "canon" + "ical` key is reused"))
        self.assertFalse(unscoped("a plain sentence carrying no guarded word"))
        self.assertTrue(unscoped("every such state is " + "forc" + "ed"))
        self.assertFalse(unscoped("every such state is " + "forc" + "ed: NO_FRESH_DATUM"))

    def test_the_python_prose_reader_sees_comments_and_strings_only(self) -> None:
        source = '"""A docstring line.\nA second line."""\n# a comment\nname = 1\n'
        lines, error = prose_lines(HERE / "zz.py", source)
        self.assertIsNone(error)
        self.assertEqual(
            lines,
            [
                (1, '"""A docstring line.'),
                (2, 'A second line."""'),
                (3, "# a comment"),
            ],
        )

    def test_an_unreadable_python_module_is_reported_not_skipped(self) -> None:
        lines, error = prose_lines(HERE / "zz.py", "def f(:\n")
        self.assertIsNotNone(error)
        self.assertIn("prose could not be read", str(error))
        self.assertEqual(lines, [])

    def test_the_prose_population_is_not_empty(self) -> None:
        names = {f.name for f in prose_files()}
        self.assertIn(Path(__file__).name, names)
        for frozen in FROZEN_INPUTS:
            self.assertNotIn(frozen, names, f"{frozen} must be skipped by this scan")


if __name__ == "__main__":
    unittest.main()
