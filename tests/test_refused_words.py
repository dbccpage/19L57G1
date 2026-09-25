"""Two words refused anywhere in this repository (author, 2026-09-24).

Gate 12 (``ci/check_prose_watchlist.py``) is a census: a watched word may
appear wherever its per-file count is pinned, and ``--regen`` can adopt a new
hit.  On 2026-09-24 the author ruled that two watched words are not allowed
in this repository at all, after a research tree used both and was merged
with gate 12 red.  This test enforces that ruling, and differs from gate 12
in four ways:

* **No pin.**  Any occurrence fails.  No regeneration can adopt one.
* **Identifiers too.**  The text is cut into maximal runs of ASCII letters
  after gate 12's normalization (NFKD, combining marks dropped, lowercase),
  so ``_``, digits and punctuation separate runs.  A run fails when a
  refused word occurs anywhere inside it.  That covers plurals, derived
  forms, ``snake_case``, ``camelCase`` and glued names, which gate 12 leaves
  to the identifier firewall.
* **Paths too.**  Every tracked path is checked as well as every tracked
  file's text.
* **Every tracked file.**  The seed inputs under ``prompt/``, the
  ``contact/analysis/`` quarantine and gate 12's own list are all in scope.
  None of them carries either word, so nothing needs an exemption.  Files
  that contain a NUL byte are skipped, as gate 12 skips them; text that is
  not UTF-8 is read as Latin-1, so an encoding cannot hide a word.

The words are stored as gate 12 stores its terms: the SHA-256 of the
normalized form, never the word itself.  Each digest is paired with the
word's length, which the substring search needs.  Both digests are also
watched by gate 12, so ``python ci/check_prose_watchlist.py --probe WORD``
says whether a word is one of them.  Extending or pruning ``REFUSED`` is the
author's act.

What this test cannot see: git history, branch names, commit messages and
pull-request text, none of which is a tracked file; and a word spelled with
letters outside ASCII after normalization.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
from collections.abc import Iterable, Mapping
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "ci"))

import check_prose_watchlist as cpw  # noqa: E402

# digest of the normalized word -> its length in letters (author, 2026-09-24)
REFUSED: dict[str, int] = {
    "04464674e585250293545a271a81dad158baf7737224a1737c1f3039278ec518": 11,
    "309d10386e65f08157282bcf3af6b46e628f2e699311b76473aebc056ea06cb9": 7,
}

LETTER_RUN = re.compile(r"[a-z]+")


def _refused_in(run: str, refused: Mapping[str, int]) -> str | None:
    """The digest of the first refused word inside ``run``, or None."""
    for length in sorted(set(refused.values())):
        for start in range(len(run) - length + 1):
            window = run[start:start + length].encode("ascii")
            d = hashlib.sha256(window).hexdigest()
            if refused.get(d) == length:
                return d
    return None


class _Scanner:
    """Refused-word search with one memo of letter runs per scan."""

    def __init__(self, refused: Mapping[str, int]) -> None:
        self.refused = refused
        self.memo: dict[str, str | None] = {}

    def run_hits(self, text: str) -> list[tuple[int, str]]:
        """(1-based line, letter run) for each run holding a refused word."""
        out: list[tuple[int, str]] = []
        memo = self.memo
        for line_no, line in enumerate(text.splitlines(), start=1):
            for run in LETTER_RUN.findall(cpw.normalize(line)):
                if run not in memo:
                    memo[run] = _refused_in(run, self.refused)
                if memo[run] is not None:
                    out.append((line_no, run))
        return out

    def file_hits(self, root: Path, rels: Iterable[str]) -> list[str]:
        """``path: 'run'`` for a refused word in a path, and
        ``path:line: 'run'`` for one in a file's text."""
        found: list[str] = []
        for rel in rels:
            for _, run in self.run_hits(rel):
                found.append(f"{rel}: path holds '{run}'")
            text = cpw.read_text(root / rel)
            if text is None:
                continue
            for line_no, run in self.run_hits(text):
                found.append(f"{rel}:{line_no}: '{run}'")
        return found


def _probe_refused(term: str) -> dict[str, int]:
    """A synthetic refusal table for one neutral probe word."""
    return {cpw.digest(term): len(term)}


# -- the search -------------------------------------------------------------


def test_every_form_the_letter_runs_can_carry_is_refused() -> None:
    scanner = _Scanner(_probe_refused("zzprobe"))
    text = "\n".join([
        "a zzprobe here",          # the word
        "ZZPROBES and Zzprobes",   # case and plural
        "zzprobeic",               # a derived form
        "zzprobe_index",           # snake_case, which gate 12 does not split
        "ZzprobeIndex",            # camelCase
        "antizzprobe",             # glued inside a longer run
        "k9zzprobe2",              # digits separate runs
        "źzprobe",           # a combining mark is dropped first
    ])
    hits = scanner.run_hits(text)
    assert [line for line, _ in hits] == [1, 2, 2, 3, 4, 5, 6, 7, 8]
    assert hits[4] == (4, "zzprobe")
    assert hits[5] == (5, "zzprobeindex")
    assert hits[6] == (6, "antizzprobe")


def test_near_misses_are_not_refused() -> None:
    scanner = _Scanner(_probe_refused("zzprobe"))
    text = "zzprob\nzz_probe\nzz probe\nzzpro-be\nzzprebo\n"
    assert scanner.run_hits(text) == []


def test_a_length_that_does_not_match_its_digest_finds_nothing() -> None:
    # the table pairs each digest with its length; a wrong length makes the
    # window search miss the word, which the live injection guards against
    scanner = _Scanner({cpw.digest("zzprobe"): 8})
    assert scanner.run_hits("zzprobe zzprobes") == []


def test_paths_and_text_are_both_searched(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "ZZPROBE_INDEX.md").write_text("clean\n", "utf-8")
    (tmp_path / "a.md").write_text("one\nthe zzprobe_spec row\n", "utf-8")
    (tmp_path / "b.bin").write_bytes(b"zzprobe\x00")
    (tmp_path / "c.txt").write_bytes(b"zzprobe caf\xe9\n")
    scanner = _Scanner(_probe_refused("zzprobe"))
    found = scanner.file_hits(
        tmp_path, ["a.md", "b.bin", "c.txt", "docs/ZZPROBE_INDEX.md"])
    assert found == [
        "a.md:2: 'zzprobe'",
        "c.txt:1: 'zzprobe'",
        "docs/ZZPROBE_INDEX.md: path holds 'zzprobe'",
    ]


# -- the live check ---------------------------------------------------------


def test_the_refused_words_are_two_watched_terms() -> None:
    # a count guard: pruning an entry must be a visible edit to this test
    assert len(REFUSED) == 2
    data = cpw.load(REPO / cpw.WATCHLIST_REL)
    watched = data["watched"]
    assert isinstance(watched, dict)
    for d, length in REFUSED.items():
        assert d in watched, f"refused digest {d[:12]} is not watched by gate 12"
        assert isinstance(length, int) and length > 0


def test_no_refused_word_appears_in_any_tracked_path_or_file() -> None:
    if shutil.which("git") is None:
        pytest.skip("git unavailable")
    proc = subprocess.run(
        ["git", "ls-files", "-z"], capture_output=True, cwd=REPO, check=True)
    rels = sorted(
        raw.decode("utf-8") for raw in proc.stdout.split(b"\0") if raw)
    assert len(rels) > 1000, "the tracked-file census came back nearly empty"
    found = _Scanner(REFUSED).file_hits(REPO, rels)
    assert not found, (
        "a word the author refused (2026-09-24) appears in this repository:\n"
        + "\n".join(found))
