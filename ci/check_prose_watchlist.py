"""Prose-level watchlist census for physics-shaped and outside-target words.

The identifier firewall in ``tests/test_primitive_contact.py`` bars a fixed
list of Lean identifiers.  It cannot see prose: a docstring, a STATUS page,
or a Lean comment can carry a physics-shaped noun as if it were a house
word, and no gate reads it.  This gate reads it.

Design, stated so it cannot be quietly weakened:

* **The terms are digests, not words.**  ``ci/prose_watchlist.json`` stores
  the SHA-256 of each watched term's normalized form.  CLAUDE.md records a
  refused outside grid on exactly this ground - describe, do not name - so
  the list itself must not be the smuggle it watches for.  Digests are not
  secrets; ``--probe WORD`` answers whether a word is watched.
* **It is a census, not a ban.**  Every whole-word hit in tracked prose is
  pinned per file in the ``baseline`` block.  A hit above its pinned count
  fails by file, line, and surface token; a hit below it fails as a stale
  pin.  ``--regen`` rewrites the pin deliberately, never implicitly.  The
  pin puts the tree's physics-shaped vocabulary in one inspectable place.
* **Scope is tracked files** (``git ls-files``), minus the two read-only
  seed inputs under ``prompt/`` (the one place CLAUDE.md permits outside
  terms), the ``contact/analysis/`` quarantine (the identifier firewall
  excludes it for the same reason), this gate's own JSON, and files that
  contain a NUL byte.  Text that is not UTF-8 is decoded as Latin-1 rather
  than skipped, so an encoding cannot hide a hit.
* **Matching is whole-word after normalization** (NFKD, combining marks
  dropped, lowercase).  A token matches if it, or it minus a trailing
  ``s`` or ``es``, digests to a watched term.  Two-word terms match two
  adjacent tokens on one line.  Word boundaries treat ``_`` and digits as
  word characters, so ``snake_case`` and ``camelCase`` identifiers are not
  split: this is a PROSE gate, and identifiers stay with the firewall.

Exit 0 on a matching census, 1 with named failures otherwise.
AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import NamedTuple

REPO = Path(__file__).resolve().parent.parent
WATCHLIST_REL = "ci/prose_watchlist.json"
EXCLUDED_PATHS = frozenset(
    {"prompt/prompt.md", "prompt/seed_prompt.md", WATCHLIST_REL}
)
EXCLUDED_PREFIXES: tuple[str, ...] = ("contact/analysis/",)

TOKEN = re.compile(r"\b[a-z]+\b")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class Hit(NamedTuple):
    """One watched-term occurrence: 1-based line, normalized surface, digest."""

    line: int
    surface: str
    digest: str


def normalize(text: str) -> str:
    """NFKD, drop combining marks, lowercase.  Idempotent.

    Two shortcuts, neither of which changes the result: ASCII text has no
    decomposition and no combining mark, so it is only lowercased; and a
    decomposition that came out ASCII has no combining mark to drop.  Only
    text that stays non-ASCII after NFKD pays the per-character filter.
    """
    if text.isascii():
        return text.lower()
    decomposed = unicodedata.normalize("NFKD", text)
    if decomposed.isascii():
        return decomposed.lower()
    stripped = "".join(
        ch for ch in decomposed if not unicodedata.combining(ch))
    return stripped.lower()


def digest(term: str) -> str:
    """SHA-256 hex of the normalized term."""
    return hashlib.sha256(normalize(term).encode("utf-8")).hexdigest()


def tokens(text: str) -> list[str]:
    """Whole words of the normalized text.  ``_`` and digits are word
    characters for ``\\b``, so identifiers containing them yield nothing."""
    return TOKEN.findall(normalize(text))


ES_PLURAL_STEMS: tuple[str, ...] = ("ses", "xes", "zes", "ches", "shes")


def stems(token: str) -> list[str]:
    """The token and its de-pluralized forms, most specific first.

    The ``es`` strip applies only after s, x, z, ch, sh -- the English
    plural rule.  Found live: ``hopes`` stripped to a watched three-letter
    noun and pinned as a hit; the narrowed rule leaves ``hopes`` as
    ``hope`` only, while ``boxes``, ``classes``, ``wishes`` still reach
    their singulars, and ``-e`` singulars are reached by the plain ``s``
    strip.
    """
    forms = [token]
    if token.endswith(ES_PLURAL_STEMS) and len(token) > 4:
        forms.append(token[:-2])
    if token.endswith("s") and len(token) > 3:
        forms.append(token[:-1])
    return forms


def _match_unigram(token: str, watched: Mapping[str, str]) -> str | None:
    for form in stems(token):
        d = digest(form)
        if d in watched:
            return d
    return None


def _match_bigram(
    first: str, second: str, watched: Mapping[str, str]
) -> str | None:
    for form in stems(second):
        d = digest(f"{first} {form}")
        if d in watched:
            return d
    return None


class _Memo:
    """Match results already computed against one ``watched`` mapping.

    For a fixed ``watched``, ``_match_unigram`` and ``_match_bigram`` are
    deterministic in their token arguments, and a line's hits (less its
    line number) are deterministic in the line's text.  A repeated token,
    adjacent pair, or whole line is therefore answered from here instead of
    being re-tokenized, re-stemmed, and re-digested; the tree repeats all
    three heavily.  A memo is built for one scan and dropped with it; it is
    never shared across scans, so a mapping that changes between scans
    (``--add``) cannot be answered from a stale entry.
    """

    __slots__ = ("watched", "unigram", "bigram", "lines")

    def __init__(self, watched: Mapping[str, str]) -> None:
        self.watched = watched
        self.unigram: dict[str, str | None] = {}
        self.bigram: dict[tuple[str, str], str | None] = {}
        self.lines: dict[str, tuple[tuple[str, str], ...]] = {}

    def one(self, token: str) -> str | None:
        unigram = self.unigram
        if token in unigram:
            return unigram[token]
        found = unigram[token] = _match_unigram(token, self.watched)
        return found

    def two(self, first: str, second: str) -> str | None:
        key = (first, second)
        bigram = self.bigram
        if key in bigram:
            return bigram[key]
        found = bigram[key] = _match_bigram(first, second, self.watched)
        return found


def _line_hits(line: str, memo: _Memo) -> tuple[tuple[str, str], ...]:
    """(surface, digest) for every hit on one line, in scan order."""
    out: list[tuple[str, str]] = []
    toks = tokens(line)
    for i, tok in enumerate(toks):
        one = memo.one(tok)
        if one is not None:
            out.append((tok, one))
        if i + 1 < len(toks):
            two = memo.two(tok, toks[i + 1])
            if two is not None:
                out.append((f"{tok} {toks[i + 1]}", two))
    return tuple(out)


def _scan_text(text: str, memo: _Memo) -> list[Hit]:
    hits: list[Hit] = []
    lines = memo.lines
    for line_no, line in enumerate(text.splitlines(), start=1):
        found = lines.get(line)
        if found is None:
            found = lines[line] = _line_hits(line, memo)
        for surface, d in found:
            hits.append(Hit(line_no, surface, d))
    return hits


def scan_text(text: str, watched: Mapping[str, str]) -> list[Hit]:
    """Every watched-term hit in ``text``, in line order."""
    return _scan_text(text, _Memo(watched))


def in_scope(rel: str) -> bool:
    """Whether a repository-relative path is scanned."""
    posix = rel.replace("\\", "/")
    if posix in EXCLUDED_PATHS:
        return False
    return not posix.startswith(EXCLUDED_PREFIXES)


def read_text(path: Path) -> str | None:
    """File text, or None for a NUL-bearing (binary) file.  Non-UTF-8
    bytes fall back to Latin-1 so an encoding cannot hide a hit."""
    data = path.read_bytes()
    if b"\x00" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1")


def tracked_files(repo: Path) -> list[str]:
    """``git ls-files`` at ``repo``, sorted, forward slashes."""
    proc = subprocess.run(
        ["git", "ls-files", "-z"], capture_output=True, cwd=repo,
        check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            "git ls-files failed: " + proc.stderr.decode("utf-8", "replace"))
    return sorted(
        raw.decode("utf-8").replace("\\", "/")
        for raw in proc.stdout.split(b"\0") if raw)


def scan_repo(
    repo: Path,
    watched: Mapping[str, str],
    files: Iterable[str] | None = None,
) -> dict[str, list[Hit]]:
    """Hits per in-scope, non-binary tracked file (files with no hits are
    omitted).  ``files`` overrides the git census, for tests."""
    rels = tracked_files(repo) if files is None else sorted(
        f.replace("\\", "/") for f in files)
    memo = _Memo(watched)
    out: dict[str, list[Hit]] = {}
    for rel in rels:
        if not in_scope(rel):
            continue
        text = read_text(repo / rel)
        if text is None:
            continue
        hits = _scan_text(text, memo)
        if hits:
            out[rel] = hits
    return out


def census_of(hits_by_file: Mapping[str, list[Hit]]) -> dict[str, dict[str, int]]:
    """Per-file, per-digest counts; sorted keys at both levels."""
    census: dict[str, dict[str, int]] = {}
    for rel in sorted(hits_by_file):
        counts: Counter[str] = Counter(h.digest for h in hits_by_file[rel])
        census[rel] = dict(sorted(counts.items()))
    return census


def compare(
    baseline: Mapping[str, Mapping[str, int]],
    current: Mapping[str, Mapping[str, int]],
    hits_by_file: Mapping[str, list[Hit]] | None = None,
) -> list[str]:
    """Failures in both directions.  A NEW HIT names the file and, when the
    hits are supplied, every line and surface token above the pin."""
    failures: list[str] = []
    for rel in sorted(set(baseline) | set(current)):
        pinned = baseline.get(rel, {})
        seen = current.get(rel, {})
        for d in sorted(set(pinned) | set(seen)):
            n_pin = int(pinned.get(d, 0))
            n_now = int(seen.get(d, 0))
            if n_now > n_pin:
                msg = (f"FAIL: NEW HIT: {rel}: watched term {d[:12]} "
                       f"appears {n_now} times, pinned {n_pin}")
                if hits_by_file is not None:
                    where = [f"line {h.line} '{h.surface}'"
                             for h in hits_by_file.get(rel, [])
                             if h.digest == d]
                    msg += " -- " + "; ".join(where)
                failures.append(msg)
            elif n_now < n_pin:
                failures.append(
                    f"FAIL: STALE PIN: {rel}: watched term {d[:12]} appears "
                    f"{n_now} times, pinned {n_pin}; if the removal is "
                    f"intended, regenerate with --regen")
    return failures


def load(path: Path) -> dict[str, object]:
    """Parse the watchlist file and validate its shape."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("watchlist root must be an object")
    watched = data.get("watched")
    baseline = data.get("baseline")
    if not isinstance(watched, dict) or not watched:
        raise ValueError("watchlist 'watched' must be a non-empty object")
    for d, cls in watched.items():
        if not (isinstance(d, str) and HEX64.match(d)):
            raise ValueError(f"watched key is not a 64-hex digest: {d!r}")
        if not isinstance(cls, str) or not cls:
            raise ValueError(f"watched class for {d[:12]} must be text")
    if not isinstance(baseline, dict):
        raise ValueError("watchlist 'baseline' must be an object")
    for rel, counts in baseline.items():
        if not isinstance(rel, str) or not isinstance(counts, dict):
            raise ValueError(f"baseline entry malformed: {rel!r}")
        for d, n in counts.items():
            if d not in watched:
                raise ValueError(
                    f"baseline {rel} pins unwatched digest {str(d)[:12]}")
            if not isinstance(n, int) or n <= 0:
                raise ValueError(f"baseline {rel} count must be positive")
    result: dict[str, object] = dict(data)
    return result


def dump(path: Path, data: Mapping[str, object]) -> None:
    """Deterministic bytes: sorted keys, two-space indent, LF, ASCII."""
    text = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=True)
    path.write_bytes((text + "\n").encode("ascii"))


def run(
    repo: Path,
    data: Mapping[str, object],
    files: Iterable[str] | None = None,
) -> tuple[int, list[str], dict[str, list[Hit]]]:
    """Scan and compare.  Returns (exit code, messages, hits)."""
    watched = data["watched"]
    baseline = data["baseline"]
    assert isinstance(watched, dict) and isinstance(baseline, dict)
    hits = scan_repo(repo, watched, files)
    current = census_of(hits)
    failures = compare(baseline, current, hits)
    if failures:
        return 1, failures, hits
    total = sum(len(v) for v in hits.values())
    return 0, [
        f"prose watchlist clean: {len(watched)} watched terms, "
        f"{len(hits)} files with pinned hits, {total} hits, census "
        f"matches its pin"], hits


def report(hits: Mapping[str, list[Hit]]) -> list[str]:
    """Every hit as ``path:line: surface``, then per-file totals."""
    lines: list[str] = []
    for rel in sorted(hits):
        for h in hits[rel]:
            lines.append(f"{rel}:{h.line}: {h.surface}")
    lines.append("")
    lines.append("per-file totals:")
    for rel, n in sorted(((r, len(v)) for r, v in hits.items()),
                         key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"  {n:5d}  {rel}")
    return lines


def regen(repo: Path, path: Path, data: dict[str, object]) -> list[str]:
    """Rewrite the baseline block from a fresh scan; report the diff."""
    watched = data["watched"]
    old = data["baseline"]
    assert isinstance(watched, dict) and isinstance(old, dict)
    new = census_of(scan_repo(repo, watched))
    diff = compare(old, new)
    data["baseline"] = new
    dump(path, data)
    total = sum(sum(c.values()) for c in new.values())
    return [d.replace("FAIL: ", "regen: ") for d in diff] + [
        f"regen: baseline rewritten: {len(new)} files, {total} hits"]


def probe(words: Iterable[str], watched: Mapping[str, str]) -> list[str]:
    """Whether each word (or quoted two-word phrase) would match as a
    token, under the same stemming the scanner applies."""
    out: list[str] = []
    for w in words:
        toks = tokens(w)
        d: str | None = None
        if len(toks) == 1:
            d = _match_unigram(toks[0], watched)
        elif len(toks) == 2:
            d = _match_bigram(toks[0], toks[1], watched)
        if d is not None:
            out.append(f"{w!r}: WATCHED ({watched[d]}) digest {d}")
        else:
            out.append(f"{w!r}: not watched (exact digest {digest(w)})")
    return out


def add(
    repo: Path, path: Path, data: dict[str, object], term: str, tag: str
) -> list[str]:
    """Register one term by digest with its class tag, then repin.  The
    term reaches the console only; the file receives its digest."""
    watched = data["watched"]
    assert isinstance(watched, dict)
    d = digest(term)
    if d in watched:
        return [f"already watched ({watched[d]}) digest {d}"]
    watched[d] = tag
    return [f"added digest {d} tagged {tag!r}"] + regen(repo, path, data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--report", action="store_true",
                        help="print every hit with file, line, and token")
    parser.add_argument("--regen", action="store_true",
                        help="rewrite the baseline pin from a fresh scan")
    parser.add_argument("--probe", nargs="+", metavar="WORD",
                        help="say whether each word is a watched term")
    parser.add_argument("--add", metavar="TERM",
                        help="watch one more term (stored as a digest) and repin")
    parser.add_argument("--tag", default="physics-shaped common noun",
                        help="class tag recorded next to the digest for --add")
    parser.add_argument("--repo", type=Path, default=REPO)
    args = parser.parse_args(argv)
    path = args.repo / WATCHLIST_REL
    try:
        data = load(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {WATCHLIST_REL}: {exc}")
        return 1
    watched = data["watched"]
    assert isinstance(watched, dict)
    if args.probe:
        print("\n".join(probe(args.probe, watched)))
        return 0
    if args.add:
        print("\n".join(add(args.repo, path, data, args.add, args.tag)))
        return 0
    if args.regen:
        print("\n".join(regen(args.repo, path, data)))
        return 0
    code, messages, hits = run(args.repo, data)
    if args.report:
        print("\n".join(report(hits)))
        print()
    print("\n".join(messages))
    return code


if __name__ == "__main__":
    sys.exit(main())
