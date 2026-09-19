from __future__ import annotations

import importlib.util
import os
import re
import stat
import subprocess
import sys
import tempfile
import types
import unittest
from collections.abc import Iterator
from pathlib import Path
from typing import Protocol, cast

from receipt_io import (
    JSONValue,
    deterministic_json_bytes,
    load_json_object,
    strict_gzip_payload,
    strict_json_loads,
    write_bytes_atomic,
    write_json_atomic,
)
from run_described_replay import GZIP_PAYLOAD_NAMES, stored_name
from verify_pins import WRITE_ROOT as SCOPE_ROOT
from verify_pins import changed_paths, scope_failures


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
WRITE_ROOT = "research/described_replay/"
_FILE_ATTRIBUTE_REPARSE_POINT = 0x400

_NONCLAIM_FILES = {
    "PREDICTIONS.md",
    "PROMPT.md",
    "SOURCE_MANIFEST.json",
    "test_forbidden.py",
}


class _WatchlistModule(Protocol):
    def load(self, path: Path) -> object: ...

    def scan_repo(
        self,
        repo: Path,
        watched: object,
        files: list[str] | None = None,
    ) -> dict[str, list[str]]: ...

    def scan_text(self, text: str, watched: object) -> list[object]: ...


def _git_population() -> tuple[str, ...]:
    completed = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
            "--",
            WRITE_ROOT.rstrip("/"),
        ],
        cwd=REPO,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    paths = {
        os.fsdecode(raw).replace("\\", "/")
        for raw in completed.stdout.split(b"\0")
        if raw
    }
    invalid = sorted(path for path in paths if not path.startswith(WRITE_ROOT))
    if invalid:
        raise AssertionError(f"write-root census escaped its root: {invalid}")
    return tuple(sorted(paths))


def _is_reparse(info: os.stat_result) -> bool:
    attributes = int(getattr(info, "st_file_attributes", 0))
    tag = int(getattr(info, "st_reparse_tag", 0))
    return bool(attributes & _FILE_ATTRIBUTE_REPARSE_POINT) or tag != 0


def _same_identity(left: os.stat_result, right: os.stat_result) -> bool:
    return left.st_dev == right.st_dev and left.st_ino == right.st_ino


def _require_plain_component(
    info: os.stat_result,
    *,
    is_leaf: bool,
    relative: str,
) -> None:
    if stat.S_ISLNK(info.st_mode) or _is_reparse(info):
        raise AssertionError(f"census path crosses a reparse point: {relative}")
    if is_leaf and not stat.S_ISREG(info.st_mode):
        raise AssertionError(f"census path is not a plain regular file: {relative}")
    if not is_leaf and not stat.S_ISDIR(info.st_mode):
        raise AssertionError(f"census parent is not a plain directory: {relative}")


def _plain_surface_path(relative: str) -> tuple[Path, os.stat_result]:
    normalized = relative.replace("\\", "/")
    parts = tuple(part for part in normalized.split("/") if part)
    if (
        normalized.startswith("/")
        or not parts
        or any(part in {".", ".."} for part in parts)
        or any(":" in part for part in parts)
    ):
        raise AssertionError(f"write-root census contains a non-relative path: {relative}")
    if not normalized.startswith(WRITE_ROOT):
        raise AssertionError(f"write-root census escaped its root: {relative}")

    root_info = REPO.lstat()
    _require_plain_component(root_info, is_leaf=False, relative=relative)
    current = REPO
    for index, part in enumerate(parts):
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError as error:
            raise AssertionError(f"census path is missing: {relative}") from error
        is_leaf = index == len(parts) - 1
        _require_plain_component(info, is_leaf=is_leaf, relative=relative)
    return current, current.lstat()


def _plain_surface_bytes(relative: str) -> bytes:
    path, before = _plain_surface_path(relative)
    flags = os.O_RDONLY | int(getattr(os, "O_BINARY", 0))
    no_follow = int(getattr(os, "O_NOFOLLOW", 0))
    descriptor = os.open(path, flags | no_follow)
    try:
        opened = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened.st_mode)
            or _is_reparse(opened)
            or not _same_identity(before, opened)
        ):
            raise AssertionError(f"census file identity changed before read: {relative}")
        with os.fdopen(descriptor, "rb", closefd=True) as handle:
            descriptor = -1
            data = handle.read()
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    after = path.lstat()
    if (
        not stat.S_ISREG(after.st_mode)
        or stat.S_ISLNK(after.st_mode)
        or _is_reparse(after)
        or not _same_identity(opened, after)
    ):
        raise AssertionError(f"census file identity changed during read: {relative}")
    return data


def _text(relative: str) -> str | None:
    """The text every scan reads for one census member.

    A ``.gz`` member is read through the strict gzip reader and its
    DECOMPRESSED bytes are scanned: the two large receipts are stored that
    way, and skipping them as binary would leave their content read by no
    scan in this file.  A member that fails the strict reader fails the scan.
    """

    data = _plain_surface_bytes(relative)
    if relative.endswith(".gz"):
        data = strict_gzip_payload(data, source=relative)
    if b"\0" in data:
        return None
    return data.decode("utf-8")


def _surfaces() -> Iterator[tuple[str, str | None]]:
    for relative in _git_population():
        content = _text(relative)
        yield relative, content


def _texts(*, claims_only: bool = False) -> Iterator[tuple[str, str]]:
    for relative, content in _surfaces():
        if claims_only and Path(relative).name in _NONCLAIM_FILES:
            continue
        if content is not None:
            yield relative, content


def _substring_name_hits(
    relative: str, content: str | None, names: tuple[str, ...], label: str
) -> tuple[str, ...]:
    hits: list[str] = []
    folded_path = relative.casefold()
    folded_content = content.casefold() if content is not None else None
    for ordinal, name in enumerate(names):
        folded = name.casefold()
        if folded in folded_path:
            hits.append(f"{label}[{ordinal}]:path")
        if folded_content is not None and folded in folded_content:
            hits.append(f"{relative}: {label}[{ordinal}]:content")
    return tuple(hits)


def _identifier_words(value: str) -> tuple[str, ...]:
    separated = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", value)
    separated = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", separated)
    return tuple(piece.casefold() for piece in re.findall(r"[A-Za-z0-9]+", separated))


def _identifier_word_sequences(value: str) -> tuple[tuple[str, ...], ...]:
    return tuple(
        words
        for segment in re.split(r"[^A-Za-z0-9_\s-]+", value)
        if (words := _identifier_words(segment))
    )


def _contains_word_sequence(words: tuple[str, ...], wanted: tuple[str, ...]) -> bool:
    width = len(wanted)
    return width > 0 and any(
        words[index : index + width] == wanted
        for index in range(len(words) - width + 1)
    )


def _bounded_name_hits(
    relative: str, content: str | None, names: tuple[str, ...], label: str
) -> tuple[str, ...]:
    hits: list[str] = []
    for surface, value in (("path", relative), ("content", content)):
        if value is None:
            continue
        sequences = _identifier_word_sequences(value)
        for ordinal, name in enumerate(names):
            wanted = _identifier_words(name)
            if any(_contains_word_sequence(words, wanted) for words in sequences):
                hits.append(
                    f"{label}[{ordinal}]:path"
                    if surface == "path"
                    else f"{relative}: {label}[{ordinal}]:content"
                )
    return tuple(hits)


def _load_watchlist_module() -> _WatchlistModule:
    module_path = REPO / "ci" / "check_prose_watchlist.py"
    spec = importlib.util.spec_from_file_location("described_replay_watchlist", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load prose watchlist scanner: {module_path}")
    module = importlib.util.module_from_spec(spec)
    if not isinstance(module, types.ModuleType):
        raise RuntimeError("watchlist loader did not create a module")
    spec.loader.exec_module(module)
    return cast(_WatchlistModule, module)


def _working_denylist() -> tuple[str, ...]:
    payload = load_json_object(REPO / "contact" / "analysis" / "contact_countermodels.json")
    denylist = payload.get("denylist")
    if not isinstance(denylist, dict):
        raise AssertionError("contact census does not contain a denylist object")
    full = denylist.get("full_census")
    subtracted = denylist.get("subtracted_as_native_or_core")
    if not isinstance(full, list) or not isinstance(subtracted, list):
        raise AssertionError("contact census does not contain both name lists")
    if not all(isinstance(item, str) for item in full + subtracted):
        raise AssertionError("contact census contains a non-string name")
    names = set(cast(list[str], full)) - set(cast(list[str], subtracted))
    if len(names) != 102:
        raise AssertionError(f"working denylist cardinality changed: {len(names)}")
    return tuple(sorted(names))


def _outside_computation_names() -> tuple[str, ...]:
    fragments = (
        ("Tur", "ing"),
        ("Klee", "ne"),
        ("Chur", "ch"),
        ("Ri", "ce"),
        ("Chai", "tin"),
        ("Post ", "correspondence"),
        ("halt", "ing problem"),
        ("recursion ", "theorem"),
        ("universal ", "machine"),
    )
    return tuple(left + right for left, right in fragments)


def _units(text: str) -> tuple[str, ...]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    paragraphs = [
        re.sub(r"\s+", " ", paragraph).strip()
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
        and not all(
            line.lstrip().startswith("|")
            for line in paragraph.splitlines()
            if line.strip()
        )
    ]
    return tuple(dict.fromkeys(lines + paragraphs))


def _nearby_negation(unit: str, action_start: int) -> bool:
    prefix = unit[max(0, action_start - 100) : action_start]
    return bool(
        re.search(
            r"\b(?:no|not|never|without|refus(?:e|es|ed|ing)|"
            r"den(?:y|ies|ied)|cannot|can't|doesn't|isn't|aren't)\b",
            prefix,
            re.IGNORECASE,
        )
    )


_PROTECTED_NAME = (
    r"(?:OB[- ]?1\b|S6(?:\.|§)?6\b|S9(?:[_ -]LAST)?\b|"
    r"(?:last|sixth) bullet\b|OPEN_UNBOUNDED\b|"
    r"unbounded (?:case|question|import)\b)"
)
_CLOSING_ACTION = (
    r"(?:clos(?:e|es|ed|ing)|narrow(?:s|ed|ing)?|pric(?:e|es|ed|ing)|"
    r"resolv(?:e|es|ed|ing)|discharg(?:e|es|ed|ing)|"
    r"settl(?:e|es|ed|ing)|prov(?:e|es|ed|ing))"
)
_PROTECTED_PATTERNS = (
    re.compile(
        rf"(?P<action>\b{_CLOSING_ACTION}\b)[^.\n]{{0,100}}?\b{_PROTECTED_NAME}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\b{_PROTECTED_NAME}[^.\n]{{0,60}}?"
        rf"(?P<action>\b{_CLOSING_ACTION}\b)",
        re.IGNORECASE,
    ),
)


def protected_open_claims(text: str) -> tuple[str, ...]:
    failures: list[str] = []
    for unit in _units(text):
        for pattern in _PROTECTED_PATTERNS:
            for match in pattern.finditer(unit):
                if not _nearby_negation(unit, match.start("action")):
                    failures.append(unit)
                    break
            else:
                continue
            break
    return tuple(dict.fromkeys(failures))


_GENERAL_OBJECT = re.compile(
    r"\b(?:all|every|any)\s+(?:possible\s+)?"
    r"(?:process(?:es)?|histor(?:y|ies)|replayer(?:s)?|description(?:s)?|"
    r"semantic(?:s)?|system(?:s)?)\b|"
    r"\bwithout (?:an?\s+|any\s+)?(?:finite\s+)?bound\b|"
    r"\bunbounded\b[^.\n]{0,80}\b(?:proved|decided|classified|closed|resolved|complete)\b",
    re.IGNORECASE,
)
_NEGATIVE_SCOPE = re.compile(
    r"\b(?:no claim|does not|do not|did not|not claimed|never|refus(?:e|es|ed|ing)|"
    r"remains? open|stays? open|outside (?:the )?scope)\b|OPEN_UNBOUNDED",
    re.IGNORECASE,
)
_FINITE_QUALIFIER = re.compile(
    r"\b(?:declared finite class|finite declared class|class-relative|"
    r"within (?:the )?(?:declared )?(?:class|bound)|"
    r"in (?:the )?(?:declared )?(?:finite )?class|"
    r"DR-C-[A-Za-z0-9-]+|cost\s*(?:<=|≤)|length\s*(?:<=|≤))\b",
    re.IGNORECASE,
)


def bounded_to_unbounded_claims(text: str) -> tuple[str, ...]:
    failures: list[str] = []
    for unit in _units(text):
        if not _GENERAL_OBJECT.search(unit):
            continue
        if _NEGATIVE_SCOPE.search(unit) or _FINITE_QUALIFIER.search(unit):
            continue
        failures.append(unit)
    return tuple(dict.fromkeys(failures))


_TABLE_PROOF = re.compile(
    r"\b(?:table|receipt|matrix|census)\b[^.\n]{0,50}"
    r"\b(?:proves?|is (?:a )?proof|establishes?|demonstrates? (?:the )?theorem|"
    r"certifies? (?:the )?theorem)\b|"
    r"\bproof\b[^.\n]{0,30}\b(?:by|from) (?:the )?(?:table|receipt|matrix|census)\b",
    re.IGNORECASE,
)


def table_as_proof_claims(text: str) -> tuple[str, ...]:
    failures: list[str] = []
    for unit in _units(text):
        for match in _TABLE_PROOF.finditer(unit):
            if not _nearby_negation(unit, match.start()):
                failures.append(unit)
                break
    return tuple(dict.fromkeys(failures))


_COMPLETE_CLASSIFICATION = re.compile(
    r"\bcomplete classification\b|"
    r"\bclassification (?:is|was|stands) complete\b|"
    r"\b(?:all|every) (?:possible )?(?:process(?:es)?|replayer(?:s)?|"
    r"description(?:s)?|semantic(?:s)?) (?:is|are|has been|have been) classified\b|"
    r"\bALL_(?:REPLAYERS_FOUND|PROCESSES_CLASSIFIED)\b",
    re.IGNORECASE,
)


def completed_classification_claims(text: str) -> tuple[str, ...]:
    failures: list[str] = []
    for unit in _units(text):
        match = _COMPLETE_CLASSIFICATION.search(unit)
        if match is None:
            continue
        if _NEGATIVE_SCOPE.search(unit) or _FINITE_QUALIFIER.search(unit):
            continue
        if _nearby_negation(unit, match.start()):
            continue
        failures.append(unit)
    return tuple(dict.fromkeys(failures))


_WHOLE_PROCESS_PROPERTY = re.compile(
    r"\b(?:final|whole|this|the|our)\s+process\b[^.\n]{0,120}?"
    r"(?P<action>\b(?:minimal|initial|free|canonical|universal)\b)",
    re.IGNORECASE,
)


def whole_process_property_claims(text: str) -> tuple[str, ...]:
    failures: list[str] = []
    for unit in _units(text):
        for match in _WHOLE_PROCESS_PROPERTY.finditer(unit):
            if not _nearby_negation(unit, match.start("action")):
                failures.append(unit)
                break
    return tuple(dict.fromkeys(failures))


class ForbiddenSurfaceTests(unittest.TestCase):
    def test_census_contains_tracked_and_untracked_write_root_files(self) -> None:
        paths = _git_population()
        self.assertIn(f"{WRITE_ROOT}PROMPT.md", paths)
        self.assertIn(f"{WRITE_ROOT}test_forbidden.py", paths)

    def test_repository_prose_watchlist_is_clean(self) -> None:
        scanner = _load_watchlist_module()
        watched = scanner.load(REPO / "ci" / "prose_watchlist.json")
        hits = scanner.scan_repo(REPO, watched, files=list(_git_population()))
        self.assertEqual({}, hits)
        # The repository scanner skips a gzip member as binary, so the
        # decompressed text of each one is scanned here with the same terms.
        compressed_hits = {
            relative: found
            for relative in _git_population()
            if relative.endswith(".gz")
            and (content := _text(relative)) is not None
            and (found := scanner.scan_text(content, watched))
        }
        self.assertEqual({}, compressed_hits)

    def test_every_census_member_is_read_as_text(self) -> None:
        population = _git_population()
        for name in GZIP_PAYLOAD_NAMES:
            self.assertIn(f"{WRITE_ROOT}receipts/python/{stored_name(name)}", population)
            self.assertNotIn(f"{WRITE_ROOT}receipts/python/{name}", population)
        unread = [relative for relative in population if _text(relative) is None]
        self.assertEqual([], unread)

    def test_gzip_receipts_are_stored_as_binary(self) -> None:
        paths = [
            f"{WRITE_ROOT}receipts/python/{stored_name(name)}"
            for name in GZIP_PAYLOAD_NAMES
        ]
        completed = subprocess.run(
            ["git", "check-attr", "-z", "binary", "text", "diff", "merge", "--", *paths],
            cwd=REPO,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        fields = completed.stdout.split(b"\0")
        observed = {
            (os.fsdecode(fields[index]), os.fsdecode(fields[index + 1])):
            os.fsdecode(fields[index + 2])
            for index in range(0, len(fields) - 2, 3)
        }
        wanted = {
            (path, attribute): value
            for path in paths
            for attribute, value in (
                ("binary", "set"),
                ("text", "unset"),
                ("diff", "unset"),
                ("merge", "unset"),
            )
        }
        self.assertEqual(wanted, observed)

    def test_working_102_name_denylist_is_clean(self) -> None:
        names = _working_denylist()
        failures = [
            hit
            for relative, content in _surfaces()
            for hit in _substring_name_hits(
                relative, content, names, "working-denylist"
            )
        ]
        self.assertEqual([], failures)

    def test_working_denylist_scans_path_and_content_injections(self) -> None:
        names = _working_denylist()
        token = names[0]
        self.assertTrue(
            any(hit.endswith(":path") for hit in _substring_name_hits(
                f"research/described_replay/{token}.probe", "", names,
                "working-denylist",
            ))
        )
        self.assertTrue(
            any(hit.endswith(":content") for hit in _substring_name_hits(
                "research/described_replay/probe", token, names,
                "working-denylist",
            ))
        )

    def test_outside_computation_names_are_absent(self) -> None:
        names = _outside_computation_names()
        failures = [
            hit
            for relative, content in _surfaces()
            for hit in _bounded_name_hits(relative, content, names, "outside-name")
        ]
        self.assertEqual([], failures)

    def test_outside_name_scans_path_and_content_injections(self) -> None:
        names = _outside_computation_names()
        token = names[0]
        self.assertTrue(
            any(hit.endswith(":path") for hit in _bounded_name_hits(
                f"research/described_replay/{token}.probe", "", names,
                "outside-name",
            ))
        )
        self.assertTrue(
            any(hit.endswith(":content") for hit in _bounded_name_hits(
                "research/described_replay/probe", token, names,
                "outside-name",
            ))
        )
        for compound in (f"{token}Replay", f"{token}_replay"):
            self.assertTrue(
                any(hit.endswith(":content") for hit in _bounded_name_hits(
                    "research/described_replay/probe", compound, names,
                    "outside-name",
                ))
            )
        embedded = f"p{names[3].casefold()}"
        self.assertEqual(
            (),
            _bounded_name_hits(
                "research/described_replay/probe", embedded, names, "outside-name"
            ),
        )

    def test_surface_reader_rejects_nonplain_and_reparse_injections(self) -> None:
        scratch_root = HERE / ".pytest_tmp"
        scratch_root.mkdir(exist_ok=True)
        scratch = Path(tempfile.mkdtemp(prefix="surface-reader-", dir=scratch_root))
        plain = scratch / "plain.txt"
        directory = scratch / "entry"
        plain.write_bytes(b"plain\n")
        directory.mkdir()
        try:
            relative = plain.relative_to(REPO).as_posix()
            self.assertEqual(b"plain\n", _plain_surface_bytes(relative))
            with self.assertRaisesRegex(AssertionError, "not a plain regular file"):
                _plain_surface_bytes(directory.relative_to(REPO).as_posix())
            regular = plain.lstat()
            injected = cast(
                os.stat_result,
                types.SimpleNamespace(
                    st_mode=regular.st_mode,
                    st_file_attributes=_FILE_ATTRIBUTE_REPARSE_POINT,
                    st_reparse_tag=0,
                    st_dev=regular.st_dev,
                    st_ino=regular.st_ino,
                ),
            )
            with self.assertRaisesRegex(AssertionError, "crosses a reparse point"):
                _require_plain_component(
                    injected,
                    is_leaf=True,
                    relative="research/described_replay/probe",
                )
        finally:
            plain.unlink(missing_ok=True)
            directory.rmdir()
            scratch.rmdir()

    def test_scope_checker_rejects_synthetic_escapes(self) -> None:
        self.assertEqual((), scope_failures([f"{SCOPE_ROOT}STATUS.md"]))
        failures = scope_failures(
            [
                "research/described_replay_escape/file.txt",
                "research/other/file.txt",
                "paper/paper.md",
                r"research\described_replay_escape\file.txt",
            ]
        )
        self.assertEqual(4, len(failures))

    def test_actual_changes_stay_inside_write_root(self) -> None:
        paths = changed_paths()
        self.assertTrue(paths)
        self.assertEqual((), scope_failures(paths))

    def test_protected_open_detector_has_live_injection(self) -> None:
        injected = "This calculation closes OB-1 and resolves the unbounded question."
        self.assertTrue(protected_open_claims(injected))
        refusal = "This calculation does not close OB-1; OPEN_UNBOUNDED remains open."
        self.assertEqual((), protected_open_claims(refusal))

    def test_protected_opens_remain_unchanged(self) -> None:
        failures = [
            f"{relative}: {claim}"
            for relative, content in _texts(claims_only=True)
            for claim in protected_open_claims(content)
        ]
        self.assertEqual([], failures)

    def test_status_preserves_required_open_terminals_when_present(self) -> None:
        status = HERE / "STATUS.md"
        if not status.exists():
            self.skipTest("STATUS.md has not been written yet")
        content = status.read_text(encoding="utf-8")
        for terminal in (
            "OB1_UNCHANGED",
            "S66_UNCHANGED",
            "S9_LAST_UNCHANGED",
            "OPEN_UNBOUNDED",
        ):
            self.assertIn(terminal, content)

    def test_bounded_to_unbounded_detector_has_live_injection(self) -> None:
        self.assertTrue(bounded_to_unbounded_claims("The matrix classifies every process."))
        scoped = "Within the declared finite class, the matrix lists every history."
        self.assertEqual((), bounded_to_unbounded_claims(scoped))
        refusal = "No claim covers every process; OPEN_UNBOUNDED remains open."
        self.assertEqual((), bounded_to_unbounded_claims(refusal))

    def test_no_bounded_result_is_promoted_to_an_unbounded_claim(self) -> None:
        failures = [
            f"{relative}: {claim}"
            for relative, content in _texts(claims_only=True)
            for claim in bounded_to_unbounded_claims(content)
        ]
        self.assertEqual([], failures)

    def test_table_as_proof_detector_has_live_injection(self) -> None:
        self.assertTrue(table_as_proof_claims("The receipt proves the theorem."))
        self.assertEqual((), table_as_proof_claims("The receipt is not a proof."))

    def test_tables_and_receipts_are_not_claimed_as_proofs(self) -> None:
        failures = [
            f"{relative}: {claim}"
            for relative, content in _texts(claims_only=True)
            for claim in table_as_proof_claims(content)
        ]
        self.assertEqual([], failures)

    def test_completed_classification_detector_has_live_injection(self) -> None:
        self.assertTrue(completed_classification_claims("This is a complete classification."))
        bounded = "This is a complete classification within the declared finite class."
        self.assertEqual((), completed_classification_claims(bounded))
        refusal = "There is no complete classification; OPEN_UNBOUNDED remains open."
        self.assertEqual((), completed_classification_claims(refusal))

    def test_no_unqualified_complete_classification_is_claimed(self) -> None:
        failures = [
            f"{relative}: {claim}"
            for relative, content in _texts(claims_only=True)
            for claim in completed_classification_claims(content)
        ]
        self.assertEqual([], failures)

    def test_whole_process_property_detector_has_live_injection(self) -> None:
        for determiner in ("final", "whole", "this", "the", "our"):
            injected = f"The {determiner} process is minimal among the declared class."
            self.assertTrue(whole_process_property_claims(injected))
        refusal = "No claim says the final process is minimal or initial."
        self.assertEqual((), whole_process_property_claims(refusal))

    def test_refused_whole_process_property_is_not_promoted(self) -> None:
        failures = [
            f"{relative}: {claim}"
            for relative, content in _texts(claims_only=True)
            for claim in whole_process_property_claims(content)
        ]
        self.assertEqual([], failures)


class ReceiptIOTests(unittest.TestCase):
    def test_strict_decoder_rejects_duplicate_names_at_every_depth(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid JSON input"):
            strict_json_loads(b'{"outer":{"same":1,"same":2}}')

    def test_deterministic_json_is_sorted_ascii_lf_only(self) -> None:
        value: JSONValue = {"z": "\N{SNOWMAN}", "a": [2, 1]}
        rendered = deterministic_json_bytes(value)
        self.assertEqual(b'{\n  "a": [\n    2,\n    1\n  ],\n  "z": "\\u2603"\n}\n', rendered)
        self.assertNotIn(b"\r", rendered)

    def test_atomic_writer_is_rooted_and_rejects_bad_line_endings(self) -> None:
        scratch_root = HERE / ".pytest_tmp"
        scratch_root.mkdir(exist_ok=True)
        scratch = Path(tempfile.mkdtemp(prefix="receipt-io-", dir=scratch_root))
        target = scratch / "probe.json"
        try:
            value: JSONValue = {"b": 2, "a": 1}
            written = write_json_atomic(target, value)
            self.assertEqual(target, written)
            self.assertEqual(b'{\n  "a": 1,\n  "b": 2\n}\n', target.read_bytes())
            with self.assertRaisesRegex(ValueError, "parent traversal"):
                write_bytes_atomic(Path("..") / "escape.json", b"{}\n")
            with self.assertRaisesRegex(ValueError, "LF-only"):
                write_bytes_atomic(scratch / "crlf.json", b"{}\r\n")
            with self.assertRaisesRegex(ValueError, "exactly one LF"):
                write_bytes_atomic(scratch / "double-lf.json", b"{}\n\n")
        finally:
            target.unlink(missing_ok=True)
            scratch.rmdir()


if __name__ == "__main__":
    unittest.main()
