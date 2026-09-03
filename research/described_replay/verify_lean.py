"""Build and audit the rung-local Lean package and its frozen receipts.

The verifier has no authority outside ``research/described_replay``.  Its
injections are string mutations held in memory; they never modify a source or
receipt on disk.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import os
import re
import stat
import subprocess
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import TypeAlias, cast

from receipt_io import (
    JSONValue,
    deterministic_json_bytes,
    load_json_object,
    strict_json_loads,
    write_bytes_atomic,
)


HERE = Path(__file__).resolve().parent
LEAN_ROOT = HERE / "lean"
RECEIPT_ROOT = HERE / "receipts" / "lean"

BUILD_TARGETS: tuple[str, ...] = (
    "DescribedReplay",
    "DescribedReplay.AxiomReport",
)
ALLOWED_AXIOMS: frozenset[str] = frozenset({"propext", "Quot.sound"})

EXPECTED_IMPORTS: dict[str, tuple[str, ...]] = {
    "lean/DescribedReplay.lean": (
        "DescribedReplay.Core",
        "DescribedReplay.Provenance",
        "DescribedReplay.Description",
        "DescribedReplay.Stepper",
        "DescribedReplay.Reproduction",
        "DescribedReplay.Reporting",
    ),
    "lean/DescribedReplay/AxiomReport.lean": ("DescribedReplay",),
    "lean/DescribedReplay/Core.lean": ("Std",),
    "lean/DescribedReplay/Description.lean": ("DescribedReplay.Core",),
    "lean/DescribedReplay/Provenance.lean": ("DescribedReplay.Reporting",),
    "lean/DescribedReplay/Reporting.lean": ("DescribedReplay.Reproduction",),
    "lean/DescribedReplay/Reproduction.lean": ("DescribedReplay.Stepper",),
    "lean/DescribedReplay/Stepper.lean": ("DescribedReplay.Description",),
    "lean/lakefile.lean": ("Lake",),
}

EXPECTED_THEOREMS_BY_FILE: dict[str, tuple[str, ...]] = {
    "lean/DescribedReplay.lean": (),
    "lean/DescribedReplay/AxiomReport.lean": (),
    "lean/DescribedReplay/Core.lean": (
        "supply_inertia",
        "replayFrom_eq_replayTotalFrom",
        "replay_eq_replayTotal_of_member",
    ),
    "lean/DescribedReplay/Description.lean": (
        "events_encodeTokensFrom",
        "rawHistory_encode",
        "decode_encode_id",
        "encode_injective",
        "encode_admission_only",
        "decoder_domain_iff",
        "endpoint_insufficient",
        "empty_self_description_witness",
        "nonempty_description_outside_class",
    ),
    "lean/DescribedReplay/Reporting.lean": (
        "candidate_report_uses_described_replay",
        "bounded_reporter_diagonal_member",
        "diagonal_disagrees",
        "no_fixed_candidate_reporter",
        "outside_reporter_correct",
    ),
    "lean/DescribedReplay/Reproduction.lean": (
        "empty_self_replay_witness",
        "fixed_candidate_no_class_replay",
    ),
    "lean/DescribedReplay/Provenance.lean": (
        "reconstruction_notes_cover_kernel_definitions",
        "reconstruction_notes_cover_local_definitions",
    ),
    "lean/DescribedReplay/Stepper.lean": (
        "eventAt_exists_of_lt",
        "eventAt_length",
        "prefixFoldFrom_eq_replayFrom_take",
        "prefixState_eq_replay_take",
        "prefixFoldFrom_next",
        "prefixState_next",
        "wellFormed_transition_at",
        "stateTraceFrom_length",
        "stateTrace_length",
        "eventAt_stateTraceFrom_eq_prefixFoldFrom",
        "eventAt_stateTrace_eq_prefixState",
        "prepare_encode_exists",
        "stepper_one",
        "stepper_current_mismatch",
        "decode_failure_prepares_none",
        "preparation_dispatch_decode_failure",
        "preparation_dispatch_total",
        "stepper_transition_semantics",
        "stepped_state_shape",
        "stepped_state_prefix",
        "runSteps_from_prefix",
        "stepper_full_iteration",
        "encoded_member_full_iteration",
        "stepper_iterate",
        "stepper_total",
    ),
    "lean/lakefile.lean": (),
}

# This is deliberately explicit rather than derived from the source scanner.
# It is the ordered report contract carried by AxiomReport.lean.
THEOREM_CENSUS: tuple[str, ...] = (
    "DescribedReplay.supply_inertia",
    "DescribedReplay.replayFrom_eq_replayTotalFrom",
    "DescribedReplay.replay_eq_replayTotal_of_member",
    "DescribedReplay.reconstruction_notes_cover_kernel_definitions",
    "DescribedReplay.reconstruction_notes_cover_local_definitions",
    "DescribedReplay.events_encodeTokensFrom",
    "DescribedReplay.rawHistory_encode",
    "DescribedReplay.decode_encode_id",
    "DescribedReplay.encode_injective",
    "DescribedReplay.encode_admission_only",
    "DescribedReplay.decoder_domain_iff",
    "DescribedReplay.endpoint_insufficient",
    "DescribedReplay.empty_self_description_witness",
    "DescribedReplay.nonempty_description_outside_class",
    "DescribedReplay.prepare_encode_exists",
    "DescribedReplay.stateTraceFrom_length",
    "DescribedReplay.stateTrace_length",
    "DescribedReplay.eventAt_stateTraceFrom_eq_prefixFoldFrom",
    "DescribedReplay.eventAt_stateTrace_eq_prefixState",
    "DescribedReplay.stepper_one",
    "DescribedReplay.stepper_current_mismatch",
    "DescribedReplay.decode_failure_prepares_none",
    "DescribedReplay.preparation_dispatch_decode_failure",
    "DescribedReplay.preparation_dispatch_total",
    "DescribedReplay.stepper_transition_semantics",
    "DescribedReplay.eventAt_exists_of_lt",
    "DescribedReplay.eventAt_length",
    "DescribedReplay.prefixFoldFrom_eq_replayFrom_take",
    "DescribedReplay.prefixState_eq_replay_take",
    "DescribedReplay.prefixFoldFrom_next",
    "DescribedReplay.prefixState_next",
    "DescribedReplay.wellFormed_transition_at",
    "DescribedReplay.runSteps_from_prefix",
    "DescribedReplay.stepper_full_iteration",
    "DescribedReplay.encoded_member_full_iteration",
    "DescribedReplay.stepped_state_shape",
    "DescribedReplay.stepped_state_prefix",
    "DescribedReplay.stepper_iterate",
    "DescribedReplay.stepper_total",
    "DescribedReplay.empty_self_replay_witness",
    "DescribedReplay.fixed_candidate_no_class_replay",
    "DescribedReplay.candidate_report_uses_described_replay",
    "DescribedReplay.bounded_reporter_diagonal_member",
    "DescribedReplay.diagonal_disagrees",
    "DescribedReplay.no_fixed_candidate_reporter",
    "DescribedReplay.outside_reporter_correct",
)

SUPPORT_FILES: tuple[str, ...] = (
    "lean/lake-manifest.json",
    "lean/lean-toolchain",
)
SOURCE_FILES: tuple[str, ...] = tuple(sorted((*EXPECTED_IMPORTS, *SUPPORT_FILES)))
RECEIPT_PAYLOADS: tuple[str, ...] = ("axioms.json", "injections.json")
RECEIPT_NAMES: tuple[str, ...] = (*RECEIPT_PAYLOADS, "machine_receipt.json")

_FORBIDDEN_TOKEN = re.compile(
    r"(?im)(?:^\s*axiom\s|\b(?:sorry|admit|unsafe|partial)\b)"
)
_IMPORT = re.compile(r"(?m)^\s*import\s+([A-Za-z0-9_.'/-]+)\s*$")
_THEOREM = re.compile(r"(?m)^\s*theorem\s+([A-Za-z_][A-Za-z0-9_']*)\b")
_PRINT_AXIOMS = re.compile(
    r"(?m)^\s*#print\s+axioms\s+([A-Za-z_][A-Za-z0-9_.']*)\s*$"
)
_AXIOM_DEPENDENCIES = re.compile(
    r"'(?P<name>DescribedReplay\.[^']+)' depends on axioms: "
    r"\[(?P<axioms>[^\]]*)\]"
)
_NO_AXIOM_DEPENDENCIES = re.compile(
    r"'(?P<name>DescribedReplay\.[^']+)' does not depend on any axioms"
)
_ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

TextMap: TypeAlias = Mapping[str, str]


class LeanVerificationError(ValueError):
    """A deterministic local Lean verification failure."""


@dataclass(frozen=True)
class SourceAudit:
    source_sha256: dict[str, str]
    theorem_census: tuple[str, ...]
    print_census: tuple[str, ...]


def _require_lf(relative: str, payload: bytes) -> str:
    if b"\r" in payload:
        raise LeanVerificationError(f"non-LF source bytes: {relative}")
    if not payload.endswith(b"\n") or payload.endswith(b"\n\n"):
        raise LeanVerificationError(
            f"source must end in exactly one LF: {relative}"
        )
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise LeanVerificationError(f"non-UTF-8 source: {relative}") from error


def _plain_file(path: Path, relative: str) -> bytes:
    try:
        info = path.lstat()
    except FileNotFoundError as error:
        raise LeanVerificationError(f"missing Lean source: {relative}") from error
    attributes = int(getattr(info, "st_file_attributes", 0))
    reparse_tag = int(getattr(info, "st_reparse_tag", 0))
    if (
        not stat.S_ISREG(info.st_mode)
        or stat.S_ISLNK(info.st_mode)
        or attributes & 0x400
        or reparse_tag != 0
    ):
        raise LeanVerificationError(f"Lean source is not a plain file: {relative}")
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(HERE.resolve(strict=True)):
        raise LeanVerificationError(f"Lean source escapes the write root: {relative}")
    return path.read_bytes()


def _read_source_texts() -> dict[str, str]:
    observed_files = tuple(
        sorted(
            path.relative_to(HERE).as_posix()
            for path in LEAN_ROOT.rglob("*")
            if path.is_file()
            if ".lake" not in path.parts
        )
    )
    if observed_files != SOURCE_FILES:
        raise LeanVerificationError(
            "Lean package file census differs: "
            f"got={list(observed_files)} wanted={list(SOURCE_FILES)}"
        )
    observed = tuple(path for path in observed_files if path.endswith(".lean"))
    expected = tuple(sorted(EXPECTED_IMPORTS))
    if observed != expected:
        raise LeanVerificationError(
            f"Lean source census differs: got={list(observed)} wanted={list(expected)}"
        )
    result: dict[str, str] = {}
    for relative in expected:
        result[relative] = _require_lf(
            relative, _plain_file(HERE / relative, relative)
        )
    return result


def _mask_comments_and_strings(text: str) -> str:
    """Mask Lean comments/strings while preserving line structure."""

    output = list(text)
    index = 0
    block_depth = 0
    in_line = False
    in_string = False
    escaped = False
    while index < len(text):
        current = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if in_line:
            if current == "\n":
                in_line = False
            else:
                output[index] = " "
            index += 1
            continue
        if block_depth:
            if current == "/" and following == "-":
                output[index] = output[index + 1] = " "
                block_depth += 1
                index += 2
            elif current == "-" and following == "/":
                output[index] = output[index + 1] = " "
                block_depth -= 1
                index += 2
            else:
                if current != "\n":
                    output[index] = " "
                index += 1
            continue
        if in_string:
            if current != "\n":
                output[index] = " "
            if escaped:
                escaped = False
            elif current == "\\":
                escaped = True
            elif current == '"':
                in_string = False
            index += 1
            continue
        if current == "-" and following == "-":
            output[index] = output[index + 1] = " "
            in_line = True
            index += 2
        elif current == "/" and following == "-":
            output[index] = output[index + 1] = " "
            block_depth = 1
            index += 2
        elif current == '"':
            output[index] = " "
            in_string = True
            index += 1
        else:
            index += 1
    if block_depth:
        raise LeanVerificationError("unterminated Lean block comment")
    if in_string:
        raise LeanVerificationError("unterminated Lean string")
    return "".join(output)


def _declaration_body(masked: str, kind: str, name: str) -> str:
    start = re.search(rf"(?m)^{re.escape(kind)}\s+{re.escape(name)}\b", masked)
    if start is None:
        raise LeanVerificationError(f"{kind} declaration is absent: {name}")
    after_header = masked.find("\n", start.start())
    if after_header < 0:
        raise LeanVerificationError(f"{kind} declaration has no body: {name}")
    next_declaration = re.search(
        r"(?m)^(?:def|theorem|structure|inductive|namespace|end)\s+",
        masked[after_header + 1 :],
    )
    end = (
        len(masked)
        if next_declaration is None
        else after_header + 1 + next_declaration.start()
    )
    return masked[start.start() : end]


def _definition_implementation(masked: str, name: str) -> str:
    declaration = _declaration_body(masked, "def", name)
    marker = declaration.find(":=")
    if marker >= 0:
        return declaration[marker + 2 :]
    first_line = declaration.find("\n")
    if first_line < 0:
        raise LeanVerificationError(f"definition body marker is absent: {name}")
    return declaration[first_line + 1 :]


def _identifier_count(text: str, name: str) -> int:
    return len(re.findall(rf"\b{re.escape(name)}\b", text))


def _first_identifier(text: str, names: tuple[str, ...]) -> str | None:
    for name in names:
        if _identifier_count(text, name):
            return name
    return None


_FULL_HISTORY_NAMES: tuple[str, ...] = (
    "decode",
    "member",
    "wellFormed",
    "wellFormedFrom",
    "replay",
    "replayFrom",
    "replayTotal",
    "replayTotalFrom",
    "prefixFoldFrom",
    "prefixState",
    "stateTrace",
    "stateTraceFrom",
    "prepare",
    "preparedEncode",
    "preparationDispatcher",
    "runSteps",
)


def _audit_stepper(texts: TextMap) -> None:
    stepper_source = _mask_comments_and_strings(
        texts["lean/DescribedReplay/Stepper.lean"]
    )
    core_source = _mask_comments_and_strings(
        texts["lean/DescribedReplay/Core.lean"]
    )
    body = _definition_implementation(stepper_source, "stepper")
    forbidden = _first_identifier(body, _FULL_HISTORY_NAMES)
    if forbidden is not None:
        raise LeanVerificationError(
            f"stepper body invokes forbidden history dependency: {forbidden}"
        )
    transitions = _identifier_count(body, "transition")
    if transitions != 1:
        raise LeanVerificationError(
            f"stepper body transition-call count differs: {transitions}"
        )
    event_lookups = _identifier_count(body, "eventAt")
    if event_lookups != 2:
        raise LeanVerificationError(
            f"stepper body event-lookup count differs: {event_lookups}"
        )
    if _identifier_count(body, "applyEvent"):
        raise LeanVerificationError("stepper body bypasses transition via applyEvent")

    event_lookup = _definition_implementation(stepper_source, "eventAt")
    event_forbidden = _first_identifier(
        event_lookup,
        (
            "transition",
            "applyEvent",
            "eventValid",
            *_FULL_HISTORY_NAMES,
            "stepper",
        ),
    )
    if event_forbidden is not None:
        raise LeanVerificationError(
            "eventAt helper invokes forbidden history dependency: "
            f"{event_forbidden}"
        )

    transition = _definition_implementation(core_source, "transition")
    transition_apply = _identifier_count(transition, "applyEvent")
    if transition_apply != 1:
        raise LeanVerificationError(
            "transition applyEvent-call count differs: "
            f"{transition_apply}"
        )
    transition_forbidden = _first_identifier(
        transition,
        tuple(name for name in _FULL_HISTORY_NAMES if name != "wellFormed"),
    )
    if transition_forbidden is not None:
        raise LeanVerificationError(
            "transition invokes forbidden history dependency: "
            f"{transition_forbidden}"
        )

    preparation = _definition_implementation(stepper_source, "prepare")
    for name, wanted in (("decode", 1), ("member", 1), ("stateTrace", 1)):
        observed = _identifier_count(preparation, name)
        if observed != wanted:
            raise LeanVerificationError(
                f"preparation {name}-call count differs: {observed}"
            )
    preparation_forbidden = _first_identifier(
        preparation,
        (
            "transition",
            "replay",
            "replayFrom",
            "replayTotal",
            "replayTotalFrom",
            "prefixFoldFrom",
            "prefixState",
            "stepper",
            "runSteps",
        ),
    )
    if preparation_forbidden is not None:
        raise LeanVerificationError(
            "preparation invokes costed or replay dependency: "
            f"{preparation_forbidden}"
        )

    trace = _definition_implementation(stepper_source, "stateTraceFrom")
    trace_apply = _identifier_count(trace, "applyEvent")
    if trace_apply != 1:
        raise LeanVerificationError(
            f"preparation trace applyEvent-call count differs: {trace_apply}"
        )
    trace_forbidden = _first_identifier(
        trace,
        (
            "transition",
            "decode",
            "member",
            "wellFormed",
            "wellFormedFrom",
            "replay",
            "replayFrom",
            "replayTotal",
            "replayTotalFrom",
            "prefixFoldFrom",
            "prefixState",
            "stepper",
            "runSteps",
        ),
    )
    if trace_forbidden is not None:
        raise LeanVerificationError(
            "preparation trace invokes forbidden dependency: "
            f"{trace_forbidden}"
        )

    dispatcher = _definition_implementation(
        stepper_source, "preparationDispatcher"
    )
    dispatcher_forbidden = _first_identifier(
        dispatcher,
        ("prepare", "decode", "member", "stateTrace", "stateTraceFrom",
         "replay", "replayFrom", "replayTotal", "replayTotalFrom",
         "prefixFoldFrom", "prefixState", "transition", "applyEvent"),
    )
    if dispatcher_forbidden is not None:
        raise LeanVerificationError(
            "preparation dispatcher repeats work: "
            f"{dispatcher_forbidden}"
        )
    dispatcher_steps = _identifier_count(dispatcher, "stepper")
    if dispatcher_steps != 1:
        raise LeanVerificationError(
            "preparation dispatcher stepper-call count differs: "
            f"{dispatcher_steps}"
        )

    iteration = _definition_implementation(stepper_source, "runSteps")
    iteration_forbidden = _first_identifier(
        iteration,
        ("prepare", "preparationDispatcher", "decode", "member",
         "stateTrace", "stateTraceFrom", "replay", "replayFrom",
         "replayTotal", "replayTotalFrom", "prefixFoldFrom", "prefixState",
         "transition", "applyEvent"),
    )
    if iteration_forbidden is not None:
        raise LeanVerificationError(
            f"runSteps repeats preparation or transition work: {iteration_forbidden}"
        )
    iteration_steps = _identifier_count(iteration, "stepper")
    if iteration_steps != 1:
        raise LeanVerificationError(
            f"runSteps stepper-call count differs: {iteration_steps}"
        )


def _source_hashes() -> dict[str, str]:
    result: dict[str, str] = {}
    for relative in SOURCE_FILES:
        payload = _plain_file(HERE / relative, relative)
        _require_lf(relative, payload)
        result[relative] = sha256(payload).hexdigest()
    return result


def _audit_source_texts(texts: TextMap) -> SourceAudit:
    if tuple(sorted(texts)) != tuple(sorted(EXPECTED_IMPORTS)):
        raise LeanVerificationError("in-memory Lean source census differs")

    theorem_census: list[str] = []
    print_census: list[str] = []
    for relative in sorted(EXPECTED_IMPORTS):
        raw = texts[relative]
        forbidden = _FORBIDDEN_TOKEN.search(raw)
        if forbidden is not None:
            token = forbidden.group(0).strip().split()[0]
            raise LeanVerificationError(
                f"forbidden Lean token in {relative}: {token}"
            )

        masked = _mask_comments_and_strings(raw)
        imports = tuple(_IMPORT.findall(masked))
        if imports != EXPECTED_IMPORTS[relative]:
            raise LeanVerificationError(
                f"import census differs in {relative}: "
                f"got={list(imports)} wanted={list(EXPECTED_IMPORTS[relative])}"
            )

        local_theorems = tuple(_THEOREM.findall(masked))
        wanted_theorems = EXPECTED_THEOREMS_BY_FILE[relative]
        if local_theorems != wanted_theorems:
            raise LeanVerificationError(
                f"theorem census differs in {relative}: "
                f"got={list(local_theorems)} wanted={list(wanted_theorems)}"
            )
        theorem_census.extend(
            f"DescribedReplay.{name}" for name in local_theorems
        )

        local_prints = tuple(_PRINT_AXIOMS.findall(masked))
        if relative == "lean/DescribedReplay/AxiomReport.lean":
            if local_prints != THEOREM_CENSUS:
                raise LeanVerificationError(
                    "#print axioms census differs: "
                    f"got={list(local_prints)} wanted={list(THEOREM_CENSUS)}"
                )
            print_census.extend(local_prints)
        elif local_prints:
            raise LeanVerificationError(
                f"unexpected #print axioms outside report module: {relative}"
            )

    if set(theorem_census) != set(THEOREM_CENSUS):
        raise LeanVerificationError(
            "global theorem census and explicit report contract differ"
        )
    _audit_stepper(texts)
    return SourceAudit(
        source_sha256=_source_hashes(),
        theorem_census=THEOREM_CENSUS,
        print_census=tuple(print_census),
    )


def _run_build() -> str:
    environment = os.environ.copy()
    environment["NO_COLOR"] = "1"
    environment["CLICOLOR"] = "0"
    try:
        completed = subprocess.run(
            ["lake", "build", *BUILD_TARGETS],
            cwd=LEAN_ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=environment,
        )
    except FileNotFoundError as error:
        raise LeanVerificationError("lake executable is unavailable") from error
    if completed.returncode != 0:
        tail = completed.stdout[-4000:].replace("\r", "")
        raise LeanVerificationError(
            f"Lean build failed with exit {completed.returncode}:\n{tail}"
        )
    return completed.stdout.replace("\r", "")


def _audit_build_output(output: str) -> dict[str, tuple[str, ...]]:
    clean = _ANSI.sub("", output)
    reports: list[tuple[str, tuple[str, ...]]] = []
    for line in clean.splitlines():
        dependency_match = _AXIOM_DEPENDENCIES.search(line)
        no_dependency_match = _NO_AXIOM_DEPENDENCIES.search(line)
        if dependency_match is not None:
            raw_axioms = dependency_match.group("axioms").strip()
            axioms = tuple(
                item.strip() for item in raw_axioms.split(",") if item.strip()
            )
            reports.append((dependency_match.group("name"), axioms))
        elif no_dependency_match is not None:
            reports.append((no_dependency_match.group("name"), ()))

    names = tuple(name for name, _ in reports)
    if names != THEOREM_CENSUS:
        raise LeanVerificationError(
            "build axiom-report census differs: "
            f"got={list(names)} wanted={list(THEOREM_CENSUS)}"
        )
    if len(set(names)) != len(names):
        raise LeanVerificationError("build contains duplicate axiom reports")

    dependencies: dict[str, tuple[str, ...]] = {}
    for name, axioms in reports:
        forbidden = sorted(set(axioms) - ALLOWED_AXIOMS)
        if forbidden:
            raise LeanVerificationError(
                f"forbidden axiom dependencies for {name}: {forbidden}"
            )
        dependencies[name] = tuple(sorted(axioms))
    return dependencies


def _expect_failure(
    injection_id: str,
    expected_fragment: str,
    action: Callable[[], object],
) -> dict[str, JSONValue]:
    try:
        action()
    except (LeanVerificationError, ValueError) as error:
        observed = str(error)
        if expected_fragment not in observed:
            raise LeanVerificationError(
                f"injection {injection_id} failed for the wrong reason: {observed}"
            ) from error
        return {
            "expected_failure": expected_fragment,
            "id": injection_id,
            "observed_failure": observed,
            "recovered": True,
        }
    raise LeanVerificationError(f"injection did not fail: {injection_id}")


def _with_text(
    texts: TextMap, relative: str, replacement: str
) -> dict[str, str]:
    result = dict(texts)
    result[relative] = replacement
    return result


def _replace_once(text: str, old: str, new: str, anchor: str) -> str:
    replaced = text.replace(old, new, 1)
    if replaced == text:
        raise LeanVerificationError(f"injection anchor is absent: {anchor}")
    return replaced


def _validate_receipt_census(observed: tuple[str, ...]) -> None:
    wanted = tuple(sorted(RECEIPT_NAMES))
    if observed != wanted:
        raise LeanVerificationError(
            f"Lean receipt census differs: got={list(observed)} wanted={list(wanted)}"
        )


def _validate_receipt_bytes(name: str, observed: bytes, wanted: bytes) -> None:
    if observed != wanted:
        raise LeanVerificationError(f"Lean receipt differs: {name}")


def _render_injections(
    texts: TextMap, build_output: str
) -> dict[str, JSONValue]:
    description_path = "lean/DescribedReplay/Description.lean"
    report_path = "lean/DescribedReplay/AxiomReport.lean"
    core_path = "lean/DescribedReplay/Core.lean"
    stepper_path = "lean/DescribedReplay/Stepper.lean"

    extra_theorem = texts[description_path].replace(
        "\nend DescribedReplay\n",
        "\ntheorem verifierProbe : True := by trivial\n\nend DescribedReplay\n",
    )
    duplicate_print = (
        texts[report_path]
        + "#print axioms DescribedReplay.events_encodeTokensFrom\n"
    )
    forbidden_token = texts[core_path].replace(
        "\nend DescribedReplay\n",
        "\naxiom verifierProbe : True\n\nend DescribedReplay\n",
    )
    forbidden_import = texts[core_path].replace(
        "import Std", "import UnlistedModule", 1
    )
    stepper_header = (
        "def stepper (prepared : PreparedDescription) "
        "(state : DescribedState) : StepResult :=\n"
    )
    replay_in_stepper = _replace_once(
        texts[stepper_path],
        stepper_header,
        stepper_header + "  let _probe := replayTotal []\n",
        "costed stepper header",
    )
    preparation_in_stepper = _replace_once(
        texts[stepper_path],
        stepper_header,
        stepper_header + "  let _probe := prepare state.description\n",
        "costed stepper preparation boundary",
    )
    missing_event_lookup = _replace_once(
        texts[stepper_path],
        "match eventAt prepared.states state.pointer with",
        "match none with",
        "costed stepper cached-state lookup",
    )
    replay_in_event_lookup = _replace_once(
        texts[stepper_path],
        "| [], _ => none",
        "| [], _ => let _probe := replayTotal []; none",
        "eventAt empty case",
    )
    double_transition_apply = _replace_once(
        texts[core_path],
        "def transition (regime : Regime) (event : Event) : Option Regime :=\n",
        "def transition (regime : Regime) (event : Event) : Option Regime :=\n"
        "  let _probe := applyEvent regime event\n",
        "transition header",
    )
    replay_in_transition = _replace_once(
        texts[core_path],
        "def transition (regime : Regime) (event : Event) : Option Regime :=\n",
        "def transition (regime : Regime) (event : Event) : Option Regime :=\n"
        "  let _probe := replayTotal []\n",
        "transition history boundary",
    )
    transition_in_preparation = _replace_once(
        texts[stepper_path],
        "def prepare (description : DescriptionRegime) : Option PreparedDescription :=\n",
        "def prepare (description : DescriptionRegime) : Option PreparedDescription :=\n"
        "  let _probe := transition emptyRegime .supplyA\n",
        "preparation header",
    )
    missing_preparation_decode = _replace_once(
        texts[stepper_path],
        "match hdecode : decode description with",
        "match hdecode : none with",
        "preparation decode",
    )
    transition_in_trace = _replace_once(
        texts[stepper_path],
        "regime :: stateTraceFrom rest (applyEvent regime event)",
        "let _probe := transition regime event\n"
        "      regime :: stateTraceFrom rest (applyEvent regime event)",
        "preparation trace",
    )
    double_trace_apply = _replace_once(
        texts[stepper_path],
        "regime :: stateTraceFrom rest (applyEvent regime event)",
        "let _probe := applyEvent regime event\n"
        "      regime :: stateTraceFrom rest (applyEvent regime event)",
        "preparation trace applyEvent",
    )
    dispatcher_header = (
        "    (state : DescribedState) : StepResult :=\n"
        "  match prepared with"
    )
    revalidation_in_dispatcher = _replace_once(
        texts[stepper_path],
        dispatcher_header,
        "    (state : DescribedState) : StepResult :=\n"
        "  let _probe := prepare state.description\n"
        "  match prepared with",
        "preparation dispatcher",
    )
    missing_dispatch_step = _replace_once(
        texts[stepper_path],
        "| some witness => stepper witness state",
        "| some _ => .invalid",
        "preparation dispatcher delegation",
    )
    revalidation_in_iteration = _replace_once(
        texts[stepper_path],
        "  | 0, state => .stepped state",
        "  | 0, state => let _probe := prepare state.description; .stepped state",
        "runSteps zero case",
    )
    missing_iteration_step = _replace_once(
        texts[stepper_path],
        "match stepper prepared state with",
        "match StepResult.done with",
        "runSteps step delegation",
    )

    forbidden_build = re.sub(
        r"axioms: \[propext\]",
        "axioms: [propext, unlisted.dependency]",
        build_output,
        count=1,
    )
    if forbidden_build == build_output:
        raise LeanVerificationError("axiom-dependency injection anchor is absent")
    missing_report_lines = [
        line
        for line in build_output.splitlines()
        if "'DescribedReplay.events_encodeTokensFrom' depends on axioms:" not in line
    ]
    missing_report = "\n".join(missing_report_lines) + "\n"

    entries: list[dict[str, JSONValue]] = [
        _expect_failure(
            "lean-extra-theorem",
            "theorem census differs",
            lambda: _audit_source_texts(
                _with_text(texts, description_path, extra_theorem)
            ),
        ),
        _expect_failure(
            "lean-duplicate-print",
            "#print axioms census differs",
            lambda: _audit_source_texts(
                _with_text(texts, report_path, duplicate_print)
            ),
        ),
        _expect_failure(
            "lean-forbidden-token",
            "forbidden Lean token",
            lambda: _audit_source_texts(
                _with_text(texts, core_path, forbidden_token)
            ),
        ),
        _expect_failure(
            "lean-forbidden-import",
            "import census differs",
            lambda: _audit_source_texts(
                _with_text(texts, core_path, forbidden_import)
            ),
        ),
        _expect_failure(
            "lean-stepper-direct-replay",
            "stepper body invokes forbidden history dependency: replayTotal",
            lambda: _audit_source_texts(
                _with_text(texts, stepper_path, replay_in_stepper)
            ),
        ),
        _expect_failure(
            "lean-stepper-direct-preparation",
            "stepper body invokes forbidden history dependency: prepare",
            lambda: _audit_source_texts(
                _with_text(texts, stepper_path, preparation_in_stepper)
            ),
        ),
        _expect_failure(
            "lean-stepper-event-lookup-count",
            "stepper body event-lookup count differs: 1",
            lambda: _audit_source_texts(
                _with_text(texts, stepper_path, missing_event_lookup)
            ),
        ),
        _expect_failure(
            "lean-eventAt-transitive-replay",
            "eventAt helper invokes forbidden history dependency: replayTotal",
            lambda: _audit_source_texts(
                _with_text(texts, stepper_path, replay_in_event_lookup)
            ),
        ),
        _expect_failure(
            "lean-transition-double-apply",
            "transition applyEvent-call count differs: 2",
            lambda: _audit_source_texts(
                _with_text(texts, core_path, double_transition_apply)
            ),
        ),
        _expect_failure(
            "lean-transition-history-dependency",
            "transition invokes forbidden history dependency: replayTotal",
            lambda: _audit_source_texts(
                _with_text(texts, core_path, replay_in_transition)
            ),
        ),
        _expect_failure(
            "lean-preparation-costed-transition",
            "preparation invokes costed or replay dependency: transition",
            lambda: _audit_source_texts(
                _with_text(texts, stepper_path, transition_in_preparation)
            ),
        ),
        _expect_failure(
            "lean-preparation-missing-decode",
            "preparation decode-call count differs: 0",
            lambda: _audit_source_texts(
                _with_text(texts, stepper_path, missing_preparation_decode)
            ),
        ),
        _expect_failure(
            "lean-preparation-trace-transition",
            "preparation trace invokes forbidden dependency: transition",
            lambda: _audit_source_texts(
                _with_text(texts, stepper_path, transition_in_trace)
            ),
        ),
        _expect_failure(
            "lean-preparation-trace-double-apply",
            "preparation trace applyEvent-call count differs: 2",
            lambda: _audit_source_texts(
                _with_text(texts, stepper_path, double_trace_apply)
            ),
        ),
        _expect_failure(
            "lean-dispatcher-revalidation",
            "preparation dispatcher repeats work: prepare",
            lambda: _audit_source_texts(
                _with_text(texts, stepper_path, revalidation_in_dispatcher)
            ),
        ),
        _expect_failure(
            "lean-dispatcher-missing-step",
            "preparation dispatcher stepper-call count differs: 0",
            lambda: _audit_source_texts(
                _with_text(texts, stepper_path, missing_dispatch_step)
            ),
        ),
        _expect_failure(
            "lean-iteration-revalidation",
            "runSteps repeats preparation or transition work: prepare",
            lambda: _audit_source_texts(
                _with_text(texts, stepper_path, revalidation_in_iteration)
            ),
        ),
        _expect_failure(
            "lean-iteration-missing-step",
            "runSteps stepper-call count differs: 0",
            lambda: _audit_source_texts(
                _with_text(texts, stepper_path, missing_iteration_step)
            ),
        ),
        _expect_failure(
            "lean-forbidden-axiom-dependency",
            "forbidden axiom dependencies",
            lambda: _audit_build_output(forbidden_build),
        ),
        _expect_failure(
            "lean-missing-axiom-report",
            "build axiom-report census differs",
            lambda: _audit_build_output(missing_report),
        ),
        _expect_failure(
            "lean-receipt-census",
            "Lean receipt census differs",
            lambda: _validate_receipt_census(("axioms.json",)),
        ),
        _expect_failure(
            "lean-receipt-duplicate-json-name",
            "duplicate JSON object name",
            lambda: strict_json_loads(
                b'{"status":"PASS","status":"FAIL"}',
                source="in-memory Lean receipt injection",
            ),
        ),
        _expect_failure(
            "lean-receipt-bytes",
            "Lean receipt differs",
            lambda: _validate_receipt_bytes(
                "axioms.json", b'{"result":"FAIL"}\n', b'{"result":"PASS"}\n'
            ),
        ),
    ]

    # Recovery is not inferred merely from using copies: replay both clean
    # audits after every injected family has been exercised.
    _audit_source_texts(texts)
    _audit_build_output(build_output)
    return {
        "authority_effect": None,
        "injections": cast(JSONValue, entries),
        "mutation_scope": "in_memory_only",
        "result": "PASS",
        "schema": "described-replay-lean-injections-v1",
        "sealed_paths_touched": False,
    }


def _render_outputs(
    audit: SourceAudit,
    dependencies: Mapping[str, tuple[str, ...]],
    injections: dict[str, JSONValue],
) -> dict[str, bytes]:
    axiom_payload: dict[str, JSONValue] = {
        "allowed_axioms": cast(JSONValue, sorted(ALLOWED_AXIOMS)),
        "authority_effect": None,
        "build_targets": cast(JSONValue, list(BUILD_TARGETS)),
        "dependencies": cast(
            JSONValue,
            {name: list(dependencies[name]) for name in THEOREM_CENSUS},
        ),
        "package": "described_replay",
        "print_census": cast(JSONValue, list(audit.print_census)),
        "schema": "described-replay-lean-axioms-v1",
        "source_sha256": cast(JSONValue, audit.source_sha256),
        "theorem_census": cast(JSONValue, list(audit.theorem_census)),
        "theorem_count": len(audit.theorem_census),
        "toolchain": _plain_file(
            HERE / "lean/lean-toolchain", "lean/lean-toolchain"
        )
        .decode("ascii")
        .strip(),
    }
    payloads: dict[str, JSONValue] = {
        "axioms.json": axiom_payload,
        "injections.json": injections,
    }
    rendered = {
        name: deterministic_json_bytes(payloads[name])
        for name in RECEIPT_PAYLOADS
    }
    machine_payload: dict[str, JSONValue] = {
        "authority_effect": None,
        "output_sha256": {
            name: sha256(rendered[name]).hexdigest()
            for name in RECEIPT_PAYLOADS
        },
        "receipt_census": cast(JSONValue, list(RECEIPT_NAMES)),
        "result": "PASS",
        "schema": "described-replay-lean-machine-v1",
        "theorem_count": len(THEOREM_CENSUS),
    }
    rendered["machine_receipt.json"] = deterministic_json_bytes(machine_payload)
    return rendered


def _actual_receipt_census() -> tuple[str, ...]:
    if not RECEIPT_ROOT.exists():
        return ()
    return tuple(sorted(path.name for path in RECEIPT_ROOT.iterdir()))


def _check_outputs(rendered: Mapping[str, bytes]) -> None:
    _validate_receipt_census(_actual_receipt_census())
    for name in RECEIPT_NAMES:
        path = RECEIPT_ROOT / name
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode):
            raise LeanVerificationError(f"Lean receipt is not a plain file: {name}")
        load_json_object(path)
        _validate_receipt_bytes(name, path.read_bytes(), rendered[name])

    machine = load_json_object(RECEIPT_ROOT / "machine_receipt.json")
    hashes = machine.get("output_sha256")
    wanted_hashes = {
        name: sha256((RECEIPT_ROOT / name).read_bytes()).hexdigest()
        for name in RECEIPT_PAYLOADS
    }
    if hashes != wanted_hashes:
        raise LeanVerificationError("Lean machine-receipt hashes differ")


def _evaluate() -> tuple[dict[str, bytes], int]:
    texts = _read_source_texts()
    audit = _audit_source_texts(texts)
    build_output = _run_build()
    dependencies = _audit_build_output(build_output)
    injections = _render_injections(texts, build_output)
    return _render_outputs(audit, dependencies, injections), len(
        cast(list[JSONValue], injections["injections"])
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--write", action="store_true", help="write then check frozen receipts"
    )
    mode.add_argument(
        "--check", action="store_true", help="check frozen receipts byte for byte"
    )
    mode.add_argument(
        "--self-test",
        action="store_true",
        help="run all audits and in-memory injections without writing",
    )
    args = parser.parse_args()

    rendered, injection_count = _evaluate()
    if args.self_test:
        print(
            "Lean verifier self-test clean: "
            f"theorems={len(THEOREM_CENSUS)} injections={injection_count} "
            "mutation_scope=in_memory_only"
        )
        return
    if args.write:
        RECEIPT_ROOT.mkdir(parents=True, exist_ok=True)
        for name in RECEIPT_NAMES:
            write_bytes_atomic(RECEIPT_ROOT / name, rendered[name])
    _check_outputs(rendered)
    print(
        "Lean receipt replay clean: "
        f"theorems={len(THEOREM_CENSUS)} receipts={len(RECEIPT_NAMES)} "
        f"injections={injection_count}"
    )


if __name__ == "__main__":
    main()
