"""Verify exact inputs and custody for the partial-Decide recorder.

The verifier checks canonical source blobs, a static import/census contract,
runtime module origins, complete tracked-package custody, transport attributes,
the literal C3 receipt contract, and byte-identical receipt regeneration. It
does not recognize arbitrary semantic adapters or authorize any response.

Bootstrap boundary: Python necessarily executes this file before it can check
its own Git custody.  Until the early custody preflight returns, only this
running verifier, the standard library, Git, and parsed SOURCE_PINS JSON are
trusted; no partial-Decide consumer or derivation source is parsed or executed.

AuthorityEffect: None
"""

from __future__ import annotations

import ast
import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CODE = REPO / "code"
PACKAGE_PREFIX = PurePosixPath("research/partial_decide")
PINS_PATH = HERE / "SOURCE_PINS.json"
RECEIPT_PATH = HERE / "partial_decide_c3.json"
SCHEMA = "partial_decide_source_pins/v2"
RECEIPT_SCHEMA = "partial_decide_c3_receipt/v1"
POLICY = (
    "Exact sealed source inputs for a bounded metatheoretic recorder. "
    "No source correspondence, panel adapter, generator, measure choice, "
    "reading choice, response authorization, or object-language event is "
    "declared."
)
REQUIRED_TERMINALS = (
    "C3_UNIQUE_DELTA_EMPTY",
    "C3_MU2_UNIQUE_CLASS_INHABITED",
    "G3_REMAINS_CONJECTURE",
    "G4_REMAINS_CONJECTURE",
    "NO_DECISION_INPUT_SELECTION",
    "NO_OBJECT_LANGUAGE_EVENT",
    "NO_PANEL_ENGINE_ADAPTER",
    "NO_RESPONSE_APPLICATION",
    "NO_RESPONSE_AUTHORIZATION",
    "OBJECT_LANGUAGE_GENERATOR_NOT_IN_SCOPE",
    "PANEL_TO_ENGINE_LINK_NOT_DEFINED",
)
FORBIDDEN_RECEIPT_KEYS = {
    "apply",
    "authorized_delta",
    "representative",
    "selected_delta",
    "transition",
}
FORBIDDEN_DYNAMIC_NAMES = {
    "__import__",
    "compile",
    "eval",
    "exec",
    "import_module",
}
FORBIDDEN_DYNAMIC_MODULES = {"importlib", "pkgutil", "runpy", "zipimport"}
STDLIB_MODULES = frozenset(sys.stdlib_module_names) | {"__future__"}
DERIVATION_MODULE_RE = re.compile(r"derivation(?:\.[A-Za-z_][A-Za-z0-9_]*)*")
EXPECTED_RECEIPT_CONTRACT = {
    "none": "no minimum inside the declared finite candidate bounds",
    "tie": "at least two quotient classes",
    "unique_class": "one quotient class with multiple raw deltas",
    "unique_delta": "one literal raw minimum",
}
EXPECTED_RECEIPT_READINGS: dict[
    str, tuple[tuple[int, int], dict[str, tuple[str, int, int]]]
] = {
    "L": ((0, 1), {"mu1": ("tie", 6, 3), "mu2": ("unique_class", 2, 1)}),
    "F": ((1, 2), {"mu1": ("tie", 10, 5), "mu2": ("unique_class", 2, 1)}),
}
REGULAR_BLOB_MODES = {"100644", "100755"}


def _git_bytes(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, check=False
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"git {' '.join(args)} failed: {stderr}")
    return result.stdout


def _git(*args: str) -> str:
    return _git_bytes(*args).decode("utf-8").strip()


def _sha256_git_blob(revision: str, relative: PurePosixPath) -> str:
    return hashlib.sha256(
        _git_bytes("show", f"{revision}:{relative.as_posix()}")
    ).hexdigest().upper()


def _read_pins() -> dict[str, Any]:
    payload: object = json.loads(PINS_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("SOURCE_PINS.json must contain an object")
    return payload


def _required_string(block: dict[str, Any], key: str, where: str) -> str:
    value = block.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{where}: missing nonempty string {key!r}")
    return value


def _require_hex(value: str, width: int, where: str, *, uppercase: bool) -> None:
    alphabet = r"[0-9A-F]" if uppercase else r"[0-9a-f]"
    if re.fullmatch(f"{alphabet}{{{width}}}", value) is None:
        case = "uppercase" if uppercase else "lowercase"
        raise ValueError(f"{where} must be an exact {width}-digit {case} hex id")


def _safe_relative(raw: str) -> PurePosixPath:
    if "\\" in raw:
        raise ValueError(f"unsafe path separator in relative path: {raw}")
    relative = PurePosixPath(raw)
    if (
        relative.is_absolute()
        or not relative.parts
        or any(part in ("", ".", "..") for part in relative.parts)
        or ":" in relative.parts[0]
    ):
        raise ValueError(f"unsafe relative path: {raw}")
    return relative


def _source_text(relative: PurePosixPath) -> str:
    return (REPO / Path(*relative.parts)).read_text(encoding="utf-8")


def _declarations(relative: PurePosixPath) -> set[str]:
    tree = ast.parse(_source_text(relative), filename=relative.as_posix())
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
    return names


def _controlled_imports(
    relative: PurePosixPath,
    local_modules: set[str],
    *,
    enforce_dynamic_policy: bool,
) -> dict[str, set[str]]:
    tree = ast.parse(_source_text(relative), filename=relative.as_posix())
    imports: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = {alias.name for alias in node.names}
            controlled = sorted(
                name
                for name in names
                if name == "derivation"
                or name.startswith("derivation.")
                or name in local_modules
            )
            if controlled:
                raise ValueError(
                    f"{relative} uses module import instead of an authorized "
                    f"from-import: {', '.join(controlled)}"
                )
            forbidden_modules = sorted(
                name
                for name in names
                if name.split(".", 1)[0] in FORBIDDEN_DYNAMIC_MODULES
            )
            if enforce_dynamic_policy and forbidden_modules:
                raise ValueError(
                    f"{relative} imports prohibited dynamic loader(s): "
                    + ", ".join(forbidden_modules)
                )
            external = sorted(
                name
                for name in names
                if name not in controlled
                and name.split(".", 1)[0] not in STDLIB_MODULES
            )
            if external:
                raise ValueError(
                    f"{relative} imports outside the pinned/local/stdlib surface: "
                    + ", ".join(external)
                )
        elif isinstance(node, ast.ImportFrom):
            if node.level != 0:
                raise ValueError(f"{relative} uses an unsupported relative import")
            module = node.module or ""
            root = module.split(".", 1)[0]
            if enforce_dynamic_policy and root in FORBIDDEN_DYNAMIC_MODULES:
                raise ValueError(
                    f"{relative} imports prohibited dynamic loader {module}"
                )
            forbidden_names = sorted(
                alias.name
                for alias in node.names
                if alias.name in FORBIDDEN_DYNAMIC_NAMES
            )
            if enforce_dynamic_policy and forbidden_names:
                raise ValueError(
                    f"{relative} imports prohibited dynamic name(s): "
                    + ", ".join(forbidden_names)
                )
            is_controlled = (
                module.startswith("derivation") or module in local_modules
            )
            if not is_controlled:
                if root not in STDLIB_MODULES:
                    raise ValueError(
                        f"{relative} imports outside the pinned/local/stdlib "
                        f"surface: {module}"
                    )
                continue
            if module == "derivation":
                raise ValueError(
                    f"{relative} imports from derivation package root; "
                    "use the exact source module"
                )
            if any(alias.name == "*" for alias in node.names):
                raise ValueError(f"{relative} uses a wildcard controlled import")
            imports.setdefault(module, set()).update(alias.name for alias in node.names)
        elif enforce_dynamic_policy and isinstance(node, ast.Name):
            if node.id in FORBIDDEN_DYNAMIC_NAMES:
                raise ValueError(
                    f"{relative} uses prohibited dynamic execution/import name {node.id}"
                )
        elif enforce_dynamic_policy and isinstance(node, ast.Attribute):
            if node.attr in FORBIDDEN_DYNAMIC_NAMES:
                raise ValueError(
                    f"{relative} uses prohibited dynamic execution/import attribute "
                    f"{node.attr}"
                )
    return imports


def _resolve_relative_module(
    current: str, node: ast.ImportFrom, *, is_package: bool
) -> str:
    if node.level == 0:
        return node.module or ""
    package = current.split(".") if is_package else current.split(".")[:-1]
    climb = node.level - 1
    if climb > len(package):
        raise ValueError(f"relative import escapes package in {current}")
    prefix = package[: len(package) - climb]
    suffix = [] if node.module is None else node.module.split(".")
    return ".".join(prefix + suffix)


def _internal_dependencies(
    module: str,
    relative: PurePosixPath,
    module_map: dict[str, PurePosixPath],
) -> set[str]:
    tree = ast.parse(_source_text(relative), filename=relative.as_posix())
    dependencies: set[str] = set()

    def add_with_parents(candidate: str) -> None:
        parts = candidate.split(".")
        for length in range(1, len(parts)):
            parent = ".".join(parts[:length])
            if parent in module_map:
                dependencies.add(parent)
        dependencies.add(candidate)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "derivation" or alias.name.startswith("derivation."):
                    add_with_parents(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if any(alias.name == "*" for alias in node.names):
                resolved_probe = _resolve_relative_module(
                    module,
                    node,
                    is_package=module_map.get(module, relative).name == "__init__.py",
                )
                if resolved_probe == "derivation" or resolved_probe.startswith(
                    "derivation."
                ):
                    raise ValueError(
                        f"{relative} uses a wildcard derivation import from "
                        f"{resolved_probe}"
                    )
            resolved = _resolve_relative_module(
                module,
                node,
                is_package=module_map.get(module, relative).name == "__init__.py",
            )
            if resolved == "derivation" or resolved.startswith("derivation."):
                add_with_parents(resolved)
                for alias in node.names:
                    candidate = f"{resolved}.{alias.name}"
                    if candidate in module_map:
                        add_with_parents(candidate)
    dependencies.discard(module)
    parts = module.split(".")
    for length in range(1, len(parts)):
        parent = ".".join(parts[:length])
        if parent in module_map:
            dependencies.add(parent)
    return dependencies


def _parse_tree_records(
    raw: bytes, where: str
) -> dict[PurePosixPath, str]:
    entries: dict[PurePosixPath, str] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, separator, raw_path = record.partition(b"\t")
        if not separator:
            raise ValueError(f"malformed Git tree entry in {where}")
        try:
            mode, object_type, object_id = metadata.decode("ascii").split(" ")
            relative = PurePosixPath(raw_path.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as error:
            raise ValueError(f"malformed Git tree entry in {where}") from error
        if object_type != "blob" or mode not in REGULAR_BLOB_MODES:
            raise ValueError(
                f"non-regular Git entry in {where}: {relative} "
                f"mode={mode} type={object_type}"
            )
        _require_hex(object_id, 40, f"Git object for {relative}", uppercase=False)
        if relative in entries:
            raise ValueError(f"duplicate Git tree path in {where}: {relative}")
        entries[relative] = object_id
    return entries


def _parse_index_records(
    raw: bytes, where: str
) -> dict[PurePosixPath, str]:
    entries: dict[PurePosixPath, str] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, separator, raw_path = record.partition(b"\t")
        if not separator:
            raise ValueError(f"malformed Git index entry in {where}")
        try:
            mode, object_id, stage = metadata.decode("ascii").split(" ")
            relative = PurePosixPath(raw_path.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as error:
            raise ValueError(f"malformed Git index entry in {where}") from error
        if stage != "0" or mode not in REGULAR_BLOB_MODES:
            raise ValueError(
                f"non-regular or unmerged Git index entry in {where}: "
                f"{relative} mode={mode} stage={stage}"
            )
        _require_hex(object_id, 40, f"index object for {relative}", uppercase=False)
        if relative in entries:
            raise ValueError(f"duplicate Git index path in {where}: {relative}")
        entries[relative] = object_id
    return entries


def _tree_entries(
    revision: str, prefix: PurePosixPath
) -> dict[PurePosixPath, str]:
    raw = _git_bytes(
        "ls-tree", "-r", "-z", revision, "--", prefix.as_posix()
    )
    return _parse_tree_records(raw, f"{revision}:{prefix}")


def _index_entries(prefix: PurePosixPath) -> dict[PurePosixPath, str]:
    raw = _git_bytes("ls-files", "--stage", "-z", "--", prefix.as_posix())
    return _parse_index_records(raw, f"index:{prefix}")


def _derivation_module_map(revision: str) -> dict[str, PurePosixPath]:
    entries = _tree_entries(revision, PurePosixPath("code/derivation"))
    out: dict[str, PurePosixPath] = {}
    for relative in entries:
        if relative.suffix != ".py":
            continue
        module_parts = list(relative.with_suffix("").parts[1:])
        if module_parts[-1] == "__init__":
            module_parts.pop()
        module_name = ".".join(module_parts)
        if not module_name:
            raise ValueError(f"cannot derive module name for {relative}")
        if DERIVATION_MODULE_RE.fullmatch(module_name) is None:
            raise ValueError(
                f"invalid derivation module name derived from {relative}: {module_name}"
            )
        if module_name in out:
            raise ValueError(f"duplicate derivation module mapping: {module_name}")
        out[module_name] = relative
    if "derivation" not in out:
        raise ValueError(f"{revision} has no derivation package root")
    return out


def _tree_files(revision: str, prefix: PurePosixPath) -> set[PurePosixPath]:
    return set(_tree_entries(revision, prefix))


def _index_files(prefix: PurePosixPath) -> set[PurePosixPath]:
    return set(_index_entries(prefix))


def _declared_imports(
    value: object,
    consumer: str,
    allowed_modules: set[str],
) -> dict[str, set[str]]:
    if not isinstance(value, dict):
        raise ValueError(f"authorized imports for {consumer} must be an object")
    out: dict[str, set[str]] = {}
    for module, names in value.items():
        if not isinstance(module, str) or module not in allowed_modules:
            raise ValueError(f"invalid authorized module for {consumer}: {module!r}")
        if (
            not isinstance(names, list)
            or not names
            or not all(isinstance(name, str) and name for name in names)
        ):
            raise ValueError(
                f"authorized symbols for {consumer}:{module} must be nonempty strings"
            )
        if len(set(names)) != len(names):
            raise ValueError(f"duplicate authorized symbol for {consumer}:{module}")
        out[module] = set(names)
    return out


def _python_population() -> set[PurePosixPath]:
    return {
        PurePosixPath(path.relative_to(REPO).as_posix())
        for path in HERE.rglob("*.py")
        if "__pycache__" not in path.parts
    }


def _local_module_paths(
    population: set[PurePosixPath],
) -> dict[str, PurePosixPath]:
    out: dict[str, PurePosixPath] = {}
    prefix_length = len(PACKAGE_PREFIX.parts)
    for relative in sorted(population):
        local = PurePosixPath(*relative.parts[prefix_length:])
        if not local.parts:
            raise ValueError(f"consumer has no package-relative path: {relative}")
        if local.parts[0] == "derivation" or local.name == "derivation.py":
            raise ValueError(f"reserved derivation shadow path: {relative}")
        if len(local.parts) != 1:
            raise ValueError(f"nested Python consumer is outside this package contract: {relative}")
        module = local.stem
        if module in out:
            raise ValueError(f"duplicate local module name: {module}")
        out[module] = relative
    return out


def _declared_package_files(pins: dict[str, Any]) -> set[PurePosixPath]:
    raw_files = pins.get("package_files")
    if not isinstance(raw_files, list) or not raw_files:
        raise ValueError("package_files must be a nonempty list")
    if not all(isinstance(item, str) for item in raw_files):
        raise ValueError("package_files entries must be strings")
    if raw_files != sorted(raw_files):
        raise ValueError("package_files must be in deterministic order")
    if len(set(raw_files)) != len(raw_files):
        raise ValueError("package_files contains duplicates")
    files = {_safe_relative(item) for item in raw_files}
    if any(item.parts[:2] != PACKAGE_PREFIX.parts for item in files):
        raise ValueError("package_files contains a path outside research/partial_decide")
    return files


def _tracked_package_files() -> set[PurePosixPath]:
    return _index_files(PACKAGE_PREFIX)


def _status_records(
    *pathspecs: str,
) -> list[tuple[str, tuple[PurePosixPath, ...]]]:
    raw = _git_bytes(
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "--",
        *pathspecs,
    )
    items = raw.split(b"\0")
    records: list[tuple[str, tuple[PurePosixPath, ...]]] = []
    index = 0
    while index < len(items):
        record = items[index]
        index += 1
        if not record:
            continue
        if len(record) < 4 or record[2:3] != b" ":
            raise ValueError("malformed git status record")
        try:
            status = record[:2].decode("ascii")
            paths = [PurePosixPath(record[3:].decode("utf-8"))]
        except UnicodeDecodeError as error:
            raise ValueError("non-UTF-8 path in git status") from error
        if "R" in status or "C" in status:
            if index >= len(items) or not items[index]:
                raise ValueError("rename/copy git status record lost its source path")
            try:
                paths.append(PurePosixPath(items[index].decode("utf-8")))
            except UnicodeDecodeError as error:
                raise ValueError("non-UTF-8 path in git status") from error
            index += 1
        records.append((status, tuple(paths)))
    return records


def _format_status_records(
    records: list[tuple[str, tuple[PurePosixPath, ...]]]
) -> str:
    return "\n".join(
        f"{status} {' -> '.join(str(path) for path in paths)}"
        for status, paths in records
    )


def _bootstrap_custody(
    pins: dict[str, Any], *, allow_receipt_dirty: bool
) -> tuple[set[PurePosixPath], list[tuple[str, tuple[PurePosixPath, ...]]]]:
    """Fail before parsing/importing consumers, except for this file's bootstrap."""

    declared_files = _declared_package_files(pins)
    head_files = _tree_files("HEAD", PACKAGE_PREFIX)
    tracked_files = _tracked_package_files()
    if not (declared_files == head_files == tracked_files):
        raise ValueError(
            "tracked package census differs across declaration, HEAD, and index"
        )

    attributes_path = PurePosixPath(".gitattributes")
    if set(_tree_entries("HEAD", attributes_path)) != {attributes_path}:
        raise ValueError(".gitattributes must be one regular tracked HEAD blob")
    if set(_index_entries(attributes_path)) != {attributes_path}:
        raise ValueError(".gitattributes must be one regular tracked index blob")
    attribute = _git(
        "check-attr", "--cached", "text", "--", RECEIPT_PATH.relative_to(REPO).as_posix()
    )
    if attribute != "research/partial_decide/partial_decide_c3.json: text: unset":
        raise ValueError(
            "receipt transport attribute must be committed as -text; got " + attribute
        )

    package_changes = _status_records(
        ".gitattributes",
        PACKAGE_PREFIX.as_posix(),
    )
    receipt_relative = PurePosixPath(RECEIPT_PATH.relative_to(REPO).as_posix())
    receipt_changes: list[tuple[str, tuple[PurePosixPath, ...]]] = []
    disallowed_changes: list[tuple[str, tuple[PurePosixPath, ...]]] = []
    for record in package_changes:
        status, paths = record
        if allow_receipt_dirty and paths == (receipt_relative,) and not (
            "R" in status or "C" in status
        ):
            receipt_changes.append(record)
        else:
            disallowed_changes.append(record)
    if disallowed_changes:
        raise ValueError(
            "partial-Decide executable package or transport policy has "
            "worktree changes before custody preflight:\n"
            + _format_status_records(disallowed_changes)
        )

    derivation_changes = _status_records("code/derivation")
    if derivation_changes:
        raise ValueError(
            "derivation source package has worktree changes before custody "
            "preflight:\n"
            + _format_status_records(derivation_changes)
        )
    return tracked_files, receipt_changes


def _normal_path(path: str | Path) -> str:
    return os.path.normcase(os.path.realpath(os.path.abspath(os.fspath(path))))


def _assert_module_origin(
    module: ModuleType, expected: Path, module_name: str
) -> None:
    origin = getattr(module, "__file__", None)
    spec = getattr(module, "__spec__", None)
    spec_origin = getattr(spec, "origin", None)
    if (
        not isinstance(origin, str)
        or _normal_path(origin) != _normal_path(expected)
        or not isinstance(spec_origin, str)
        or _normal_path(spec_origin) != _normal_path(expected)
    ):
        raise ValueError(
            f"runtime import origin mismatch for {module_name}: "
            f"expected {expected}, got file={origin!r}, spec={spec_origin!r}"
        )
    if module_name == "derivation" or module_name.startswith("derivation."):
        code_root = Path(_normal_path(CODE))
        resolved_expected = Path(_normal_path(expected))
        if not resolved_expected.is_relative_to(code_root):
            raise ValueError(
                f"runtime import for {module_name} resolves outside code/: "
                f"{resolved_expected}"
            )
    if module_name == "derivation":
        package_path = getattr(module, "__path__", None)
        actual_paths = (
            []
            if package_path is None
            else sorted(_normal_path(item) for item in package_path)
        )
        expected_paths = [_normal_path(expected.parent)]
        if actual_paths != expected_paths:
            raise ValueError(
                "runtime package path mismatch for derivation: "
                f"expected {expected_paths}, got {actual_paths}"
            )


def _put_runtime_paths_first() -> None:
    code = _normal_path(CODE)
    here = _normal_path(HERE)
    remainder = [
        item
        for item in sys.path
        if _normal_path(item or os.getcwd()) not in {code, here}
    ]
    sys.path[:] = [str(CODE), str(HERE), *remainder]


def _verify_runtime_origins(
    module_paths: dict[str, PurePosixPath]
) -> list[str]:
    _put_runtime_paths_first()
    lines: list[str] = []
    for module_name, relative in sorted(module_paths.items()):
        module = importlib.import_module(module_name)
        expected = REPO / Path(*relative.parts)
        _assert_module_origin(module, expected, module_name)
        lines.append(f"runtime origin: {module_name} {relative}")
    loaded = {
        name
        for name in sys.modules
        if name == "derivation" or name.startswith("derivation.")
    }
    unexpected = sorted(loaded - set(module_paths))
    if unexpected:
        raise ValueError(
            "runtime loaded unpinned derivation modules: " + ", ".join(unexpected)
        )
    return lines


def _receipt_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        keys = {key for key in value if isinstance(key, str)}
        for nested in value.values():
            keys.update(_receipt_keys(nested))
        return keys
    if isinstance(value, list):
        list_keys: set[str] = set()
        for nested in value:
            list_keys.update(_receipt_keys(nested))
        return list_keys
    return set()


def _object_dict(value: object, where: str) -> dict[str, object]:
    if not isinstance(value, dict) or not all(
        isinstance(key, str) for key in value
    ):
        raise ValueError(f"{where} must be an object with string keys")
    return {key: item for key, item in value.items() if isinstance(key, str)}


def _expect_exact_keys(
    value: dict[str, object], expected: set[str], where: str
) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{where} keys differ: missing {sorted(expected - actual)}, "
            f"extra {sorted(actual - expected)}"
        )


def _validate_receipt_contract(
    payload: dict[str, object], *, snapshot_commit: str, snapshot_tree: str
) -> None:
    """Validate literal receipt claims independently of renderer constants."""

    _expect_exact_keys(
        payload,
        {
            "authority_effect",
            "classification",
            "contract",
            "panel_input",
            "readings",
            "schema",
            "source_snapshot",
            "terminals",
        },
        "receipt",
    )
    if payload["schema"] != RECEIPT_SCHEMA:
        raise ValueError("receipt schema differs from the exact C3 contract")
    if payload["authority_effect"] != "None":
        raise ValueError("receipt authority_effect must be exactly None")
    if payload["classification"] != "deterministic metatheoretic computation":
        raise ValueError("receipt classification differs from the exact contract")
    if payload["contract"] != EXPECTED_RECEIPT_CONTRACT:
        raise ValueError("receipt grade meanings differ from the exact contract")
    if payload["panel_input"] != {
        "status": "not_connected_without_a_declared_correspondence",
        "meaning": (
            "certNeg and PanelEquiv may motivate a separately declared "
            "request but do not choose this engine pair"
        ),
    }:
        raise ValueError("receipt panel boundary differs from the exact contract")
    if payload["source_snapshot"] != {
        "commit": snapshot_commit,
        "tree": snapshot_tree,
    }:
        raise ValueError("receipt source_snapshot differs from the verified pin")
    if payload["terminals"] != list(REQUIRED_TERMINALS):
        raise ValueError("receipt terminals differ from the exact refusal/open set")

    readings = payload["readings"]
    if not isinstance(readings, list) or len(readings) != 2:
        raise ValueError("receipt readings must be exactly [L, F]")
    for index, (reading_name, expected) in enumerate(
        EXPECTED_RECEIPT_READINGS.items()
    ):
        expected_target, expected_grades = expected
        row = _object_dict(readings[index], f"receipt readings[{index}]")
        _expect_exact_keys(row, {"grades", "reading", "target"}, f"reading {reading_name}")
        if row["reading"] != reading_name:
            raise ValueError(
                f"receipt reading order/name differs at index {index}: "
                f"expected {reading_name}"
            )
        if row["target"] != list(expected_target):
            raise ValueError(f"receipt target differs for reading {reading_name}")
        grades = _object_dict(row["grades"], f"reading {reading_name} grades")
        _expect_exact_keys(
            grades, {"mu1", "mu2"}, f"reading {reading_name} grades"
        )
        for measure, (expected_kind, raw_count, class_count) in expected_grades.items():
            option = _object_dict(
                grades[measure], f"reading {reading_name} grade {measure} option"
            )
            _expect_exact_keys(
                option, {"grade", "option"}, f"reading {reading_name} grade {measure} option"
            )
            if option["option"] != "some":
                raise ValueError(
                    f"receipt C3 grade unexpectedly absent for {reading_name}/{measure}"
                )
            grade = _object_dict(
                option["grade"], f"reading {reading_name} grade {measure}"
            )
            _expect_exact_keys(
                grade,
                {
                    "bounds",
                    "classes",
                    "iso_class_count",
                    "iso_perm_budget",
                    "kind",
                    "measure",
                    "minimum_cost",
                    "raw_minima",
                    "raw_minimum_count",
                    "target",
                },
                f"reading {reading_name} grade {measure}",
            )
            if grade["kind"] != expected_kind:
                raise ValueError(
                    f"receipt grade kind differs for {reading_name}/{measure}"
                )
            if grade["measure"] != measure or grade["target"] != list(expected_target):
                raise ValueError(
                    f"receipt grade request differs for {reading_name}/{measure}"
                )
            if grade["bounds"] != {"max_arity": 2, "max_items": 2}:
                raise ValueError(
                    f"receipt bounds differ for {reading_name}/{measure}"
                )
            expected_cost = {
                "items": 2,
                "new_form_arity_sum": None if measure == "mu1" else 1,
            }
            if grade["minimum_cost"] != expected_cost:
                raise ValueError(
                    f"receipt minimum cost differs for {reading_name}/{measure}"
                )
            if grade["iso_perm_budget"] != 100_000:
                raise ValueError(
                    f"receipt permutation budget differs for {reading_name}/{measure}"
                )
            if grade["raw_minimum_count"] != raw_count:
                raise ValueError(
                    f"receipt raw-minimum count differs for {reading_name}/{measure}"
                )
            raw_minima = grade["raw_minima"]
            if not isinstance(raw_minima, list) or len(raw_minima) != raw_count:
                raise ValueError(
                    f"receipt raw-minimum population differs for {reading_name}/{measure}"
                )
            if grade["iso_class_count"] != class_count:
                raise ValueError(
                    f"receipt class count differs for {reading_name}/{measure}"
                )
            classes = grade["classes"]
            if not isinstance(classes, list) or len(classes) != class_count:
                raise ValueError(
                    f"receipt class population differs for {reading_name}/{measure}"
                )
            retained_members: list[object] = []
            for class_index, raw_class in enumerate(classes):
                response_class = _object_dict(
                    raw_class,
                    f"reading {reading_name} grade {measure} class {class_index}",
                )
                _expect_exact_keys(
                    response_class,
                    {"canonical_key", "members", "size"},
                    f"reading {reading_name} grade {measure} class {class_index}",
                )
                members = response_class["members"]
                size = response_class["size"]
                if (
                    not isinstance(members, list)
                    or isinstance(size, bool)
                    or not isinstance(size, int)
                    or size != len(members)
                    or size <= 0
                ):
                    raise ValueError(
                        f"receipt class membership differs for "
                        f"{reading_name}/{measure}/{class_index}"
                    )
                retained_members.extend(members)
            raw_keys = sorted(
                json.dumps(item, sort_keys=True, separators=(",", ":"))
                for item in raw_minima
            )
            retained_keys = sorted(
                json.dumps(item, sort_keys=True, separators=(",", ":"))
                for item in retained_members
            )
            if retained_keys != raw_keys:
                raise ValueError(
                    f"receipt classes do not retain every raw minimum for "
                    f"{reading_name}/{measure}"
                )

    forbidden = sorted(_receipt_keys(payload) & FORBIDDEN_RECEIPT_KEYS)
    if forbidden:
        raise ValueError(
            "receipt contains selecting/applying keys: " + ", ".join(forbidden)
        )


def _fresh_receipt(
    module_paths: dict[str, PurePosixPath],
    *,
    snapshot_commit: str,
    snapshot_tree: str,
) -> tuple[bytes, dict[str, object]]:
    expected_origins = {
        name: str(REPO / Path(*relative.parts))
        for name, relative in module_paths.items()
    }
    child = r"""
import json
import os
import pathlib
import sys

code, here, cache, expected_json = sys.argv[1:5]
sys.pycache_prefix = cache
sys.path[:] = [code, here, *sys.path]
expected = json.loads(expected_json)
if not isinstance(expected, dict):
    raise RuntimeError("fresh renderer expected-origin map is not an object")
allowed_project_modules = set(expected) | {"c3_receipt", "partial_decide"}
stdlib_roots = set(sys.stdlib_module_names) | {"__future__"}
audited_imports = []

def audit_imports(event, args):
    if event != "import" or not args or not isinstance(args[0], str):
        return
    name = args[0]
    audited_imports.append(name)
    root_name = name.split(".", 1)[0]
    if name not in allowed_project_modules and root_name not in stdlib_roots:
        raise RuntimeError(f"fresh renderer audited unauthorized import {name}")

sys.addaudithook(audit_imports)
import c3_receipt

norm = lambda value: os.path.normcase(os.path.realpath(os.path.abspath(value)))
local_expected = {
    "c3_receipt": str(pathlib.Path(here) / "c3_receipt.py"),
    "partial_decide": str(pathlib.Path(here) / "partial_decide.py"),
}

def under(path, root_path):
    try:
        return os.path.commonpath([norm(path), norm(root_path)]) == norm(root_path)
    except ValueError:
        return False

def check_loaded(stage):
    loaded = {
        name for name in sys.modules
        if name == "derivation" or name.startswith("derivation.")
    }
    if loaded != set(expected):
        raise RuntimeError(
            f"fresh renderer {stage} derivation modules {sorted(loaded)}, "
            f"expected {sorted(expected)}"
        )
    for name, wanted in {**expected, **local_expected}.items():
        required_root = code if name.startswith("derivation") else here
        if not under(wanted, required_root):
            raise RuntimeError(
                f"fresh renderer {stage} expected path escapes its bound root for {name}"
            )
        module = sys.modules.get(name)
        if module is None:
            raise RuntimeError(f"fresh renderer {stage} lost module {name}")
        file_origin = getattr(module, "__file__", None)
        spec_origin = getattr(getattr(module, "__spec__", None), "origin", None)
        if not isinstance(file_origin, str) or norm(file_origin) != norm(wanted):
            raise RuntimeError(
                f"fresh renderer {stage} file origin mismatch for {name}"
            )
        if not isinstance(spec_origin, str) or norm(spec_origin) != norm(wanted):
            raise RuntimeError(
                f"fresh renderer {stage} spec origin mismatch for {name}"
            )
    root = sys.modules["derivation"]
    paths = sorted(norm(item) for item in root.__path__)
    wanted_path = [norm(str(pathlib.Path(code) / "derivation"))]
    if paths != wanted_path:
        raise RuntimeError(
            f"fresh renderer {stage} package path mismatch: {paths}"
        )
    for name, module in tuple(sys.modules.items()):
        origin = getattr(module, "__file__", None)
        if not isinstance(origin, str):
            continue
        if (under(origin, code) or under(origin, here)) and name not in allowed_project_modules:
            raise RuntimeError(
                f"fresh renderer {stage} loaded unauthorized project module {name}"
            )

check_loaded("before receipt_bytes")
render_audit_start = len(audited_imports)
rendered = c3_receipt.receipt_bytes()
check_loaded("after receipt_bytes")
for name in audited_imports[render_audit_start:]:
    root_name = name.split(".", 1)[0]
    if name not in allowed_project_modules and root_name not in stdlib_roots:
        raise RuntimeError(
            f"fresh renderer receipt_bytes audited unauthorized import {name}"
        )
sys.stdout.buffer.write(rendered)
"""
    with tempfile.TemporaryDirectory(prefix="partial-decide-pycache-") as cache:
        result = subprocess.run(
            [
                sys.executable,
                "-I",
                "-B",
                "-c",
                child,
                str(CODE),
                str(HERE),
                cache,
                json.dumps(expected_origins, sort_keys=True),
            ],
            cwd=REPO,
            capture_output=True,
            check=False,
        )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"fresh receipt renderer failed: {stderr}")
    rendered = result.stdout
    payload_object: object = json.loads(rendered.decode("utf-8"))
    if not isinstance(payload_object, dict):
        raise ValueError("fresh receipt renderer did not return a JSON object")
    payload = _object_dict(payload_object, "fresh receipt")
    _validate_receipt_contract(
        payload,
        snapshot_commit=snapshot_commit,
        snapshot_tree=snapshot_tree,
    )
    return rendered, payload


def _verify_status_inputs(
    pins: dict[str, Any], snapshot_commit: str
) -> tuple[list[str], list[str]]:
    raw_inputs = pins.get("status_inputs")
    if not isinstance(raw_inputs, list) or len(raw_inputs) != 1:
        raise ValueError("status_inputs must contain exactly one pinned receipt")
    entry = raw_inputs[0]
    if not isinstance(entry, dict):
        raise ValueError("status input must be an object")
    relative = _safe_relative(_required_string(entry, "path", "status input"))
    if relative != PurePosixPath("artifacts/g1_class_receipt.json"):
        raise ValueError("status input must be artifacts/g1_class_receipt.json")
    wanted = _required_string(entry, "sha256", "status input")
    _require_hex(wanted, 64, "status input sha256", uppercase=True)
    expected_terminals = [
        "G3_REMAINS_CONJECTURE",
        "G4_REMAINS_CONJECTURE",
    ]
    if entry.get("required_terminals") != expected_terminals:
        raise ValueError("status input required_terminals differ from G3/G4 freeze")
    snapshot_hash = _sha256_git_blob(snapshot_commit, relative)
    head_hash = _sha256_git_blob("HEAD", relative)
    if snapshot_hash != wanted or head_hash != wanted:
        raise ValueError(
            f"status input hash mismatch for {relative}: wanted {wanted}, "
            f"snapshot {snapshot_hash}, HEAD {head_hash}"
        )
    payload: object = json.loads(_git_bytes("show", f"HEAD:{relative.as_posix()}"))
    if not isinstance(payload, dict):
        raise ValueError("G1 class status receipt must contain an object")
    terminals = payload.get("terminals")
    if not isinstance(terminals, list) or not all(
        isinstance(item, str) for item in terminals
    ):
        raise ValueError("G1 class status receipt terminals must be strings")
    missing = [item for item in expected_terminals if item not in terminals]
    if missing:
        raise ValueError(
            "G1 class status receipt lost inherited terminal(s): "
            + ", ".join(missing)
        )
    return (
        [f"inherited status: {relative} {wanted} G3/G4 conjectural"],
        [relative.as_posix()],
    )


def _verify(*, compare_receipt: bool) -> tuple[list[str], bytes]:
    pins = _read_pins()
    if _required_string(pins, "schema", "pins") != SCHEMA:
        raise ValueError("unsupported SOURCE_PINS schema")
    if _required_string(pins, "policy", "pins") != POLICY:
        raise ValueError("source policy differs from the exact refusal declaration")
    tracked_files, receipt_changes = _bootstrap_custody(
        pins, allow_receipt_dirty=True
    )

    verification_commit = _git("rev-parse", "HEAD")
    _require_hex(verification_commit, 40, "verification commit", uppercase=False)
    snapshot = pins.get("source_snapshot")
    if not isinstance(snapshot, dict):
        raise ValueError("source_snapshot must be an object")
    snapshot_commit = _required_string(snapshot, "commit", "source_snapshot")
    snapshot_tree = _required_string(snapshot, "tree", "source_snapshot")
    _require_hex(snapshot_commit, 40, "source snapshot commit", uppercase=False)
    _require_hex(snapshot_tree, 40, "source snapshot tree", uppercase=False)
    if _git("cat-file", "-t", snapshot_commit) != "commit":
        raise ValueError(f"source snapshot is not a commit object: {snapshot_commit}")
    if _git("cat-file", "-t", snapshot_tree) != "tree":
        raise ValueError(f"source snapshot tree is not a tree object: {snapshot_tree}")
    actual_snapshot_tree = _git("rev-parse", f"{snapshot_commit}^{{tree}}")
    if actual_snapshot_tree != snapshot_tree:
        raise ValueError(
            "source snapshot tree mismatch: "
            f"expected {snapshot_tree}, got {actual_snapshot_tree}"
        )
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", snapshot_commit, "HEAD"],
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    if ancestor.returncode != 0:
        raise ValueError(f"source snapshot is not an ancestor of HEAD: {snapshot_commit}")

    status_lines, status_paths = _verify_status_inputs(pins, snapshot_commit)

    source_package = pins.get("source_package")
    if not isinstance(source_package, dict):
        raise ValueError("source_package must be an object")
    if _required_string(source_package, "module", "source_package") != "derivation":
        raise ValueError("source_package module must be exactly derivation")
    package_path = _safe_relative(
        _required_string(source_package, "path", "source_package")
    )
    if package_path != PurePosixPath("code/derivation"):
        raise ValueError("source_package path must be exactly code/derivation")
    package_tree = _required_string(source_package, "tree", "source_package")
    _require_hex(package_tree, 40, "source package tree", uppercase=False)
    snapshot_package_tree = _git(
        "rev-parse", f"{snapshot_commit}:{package_path.as_posix()}"
    )
    head_package_tree = _git("rev-parse", f"HEAD:{package_path.as_posix()}")
    if snapshot_package_tree != package_tree or head_package_tree != package_tree:
        raise ValueError(
            "source package tree mismatch: "
            f"wanted {package_tree}, snapshot {snapshot_package_tree}, "
            f"HEAD {head_package_tree}"
        )
    snapshot_package_files = _tree_files(snapshot_commit, package_path)
    head_package_files = _tree_files("HEAD", package_path)
    index_package_files = _index_files(package_path)
    if not snapshot_package_files:
        raise ValueError("source package census is empty")
    if not (
        snapshot_package_files == head_package_files == index_package_files
    ):
        raise ValueError(
            "source package population differs across snapshot, HEAD, and index"
        )
    snapshot_module_map = _derivation_module_map(snapshot_commit)
    head_module_map = _derivation_module_map("HEAD")
    if snapshot_module_map != head_module_map:
        raise ValueError("derivation module/path map differs between snapshot and HEAD")
    working_importables = {
        PurePosixPath(path.relative_to(REPO).as_posix())
        for path in (REPO / "code" / "derivation").rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix.lower() in {".py", ".pyc", ".pyd", ".so"}
    }
    untracked_importables = sorted(working_importables - index_package_files)
    if untracked_importables:
        raise ValueError(
            "untracked importable derivation paths: "
            + ", ".join(str(item) for item in untracked_importables)
        )

    modules = pins.get("modules")
    if not isinstance(modules, list) or not modules:
        raise ValueError("pins must name a nonempty module population")
    module_paths: dict[str, PurePosixPath] = {}
    used_paths: set[PurePosixPath] = set()
    lines = [
        "verifier bootstrap boundary: running verifier trusted through early custody preflight",
        f"verification commit: {verification_commit}",
        f"source snapshot: {snapshot_commit} / {snapshot_tree}",
        f"source package: derivation {package_tree} "
        f"({len(snapshot_package_files)} tracked files)",
        *status_lines,
    ]
    for entry in modules:
        if not isinstance(entry, dict):
            raise ValueError("each pinned module must be an object")
        module_name = _required_string(entry, "module", "pinned module")
        if DERIVATION_MODULE_RE.fullmatch(module_name) is None:
            raise ValueError(f"invalid pinned derivation module name: {module_name}")
        relative = _safe_relative(_required_string(entry, "path", module_name))
        wanted = _required_string(entry, "sha256", module_name)
        _require_hex(wanted, 64, f"{module_name} sha256", uppercase=True)
        if module_name in module_paths:
            raise ValueError(f"duplicate pinned module: {module_name}")
        if relative in used_paths:
            raise ValueError(f"duplicate pinned source path: {relative}")
        expected_path = snapshot_module_map.get(module_name)
        if expected_path is None:
            raise ValueError(f"pinned module is absent from the derivation module map: {module_name}")
        if relative != expected_path:
            raise ValueError(
                f"module/path mismatch for {module_name}: expected {expected_path}, "
                f"got {relative}"
            )
        snapshot_hash = _sha256_git_blob(snapshot_commit, relative)
        head_hash = _sha256_git_blob("HEAD", relative)
        if snapshot_hash != wanted or head_hash != wanted:
            raise ValueError(
                f"hash mismatch for {relative}: wanted {wanted}, "
                f"snapshot {snapshot_hash}, HEAD {head_hash}"
            )
        module_paths[module_name] = relative
        used_paths.add(relative)
        lines.append(f"source: {module_name} {relative} {wanted}")

    source_paths = [relative.as_posix() for relative in sorted(used_paths)]
    source_dirty = _git(
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--",
        *source_paths,
        *status_paths,
    )
    if source_dirty:
        raise ValueError("pinned source/status input has worktree changes:\n" + source_dirty)

    module_names = set(module_paths)
    dependency_graph: dict[str, set[str]] = {}
    for module_name, relative in module_paths.items():
        dependencies = _internal_dependencies(
            module_name, relative, snapshot_module_map
        )
        missing = sorted(dependencies - module_names)
        if missing:
            raise ValueError(
                f"{module_name} has unpinned derivation dependencies: "
                + ", ".join(missing)
            )
        dependency_graph[module_name] = dependencies

    python_population = _python_population()
    local_paths = _local_module_paths(python_population)
    local_modules = set(local_paths)
    authorized = pins.get("authorized_imports")
    if not isinstance(authorized, dict) or not authorized:
        raise ValueError("authorized_imports must be a nonempty object")
    if not all(isinstance(item, str) for item in authorized):
        raise ValueError("authorized_imports consumer paths must be strings")
    declared_consumers = {_safe_relative(item) for item in authorized}
    if declared_consumers != python_population:
        missing_consumers = sorted(python_population - declared_consumers)
        stale_consumers = sorted(declared_consumers - python_population)
        raise ValueError(
            "consumer census mismatch: missing "
            + ", ".join(str(item) for item in missing_consumers)
            + "; stale "
            + ", ".join(str(item) for item in stale_consumers)
        )

    allowed_import_modules = module_names | local_modules
    imported_derivation_modules: set[str] = set()
    for raw_consumer, declaration in authorized.items():
        assert isinstance(raw_consumer, str)
        consumer = _safe_relative(raw_consumer)
        declared = _declared_imports(
            declaration, raw_consumer, allowed_import_modules
        )
        actual = _controlled_imports(
            consumer,
            local_modules,
            enforce_dynamic_policy=consumer.name != "verify_pins.py",
        )
        if actual != declared:
            raise ValueError(
                f"authorized import mismatch for {consumer}: "
                f"declared {declared}, actual {actual}"
        )
        for imported_module, symbols in declared.items():
            imported_relative = module_paths.get(imported_module) or local_paths.get(
                imported_module
            )
            if imported_relative is None:
                raise ValueError(f"consumer imports unbound module: {imported_module}")
            missing_symbols = sorted(symbols - _declarations(imported_relative))
            if missing_symbols:
                raise ValueError(
                    f"{consumer} imports absent symbols from {imported_module}: "
                    + ", ".join(missing_symbols)
                )
            if imported_module.startswith("derivation."):
                imported_derivation_modules.add(imported_module)
        lines.append(f"authorized imports: {consumer}")

    reachable = {"derivation"} | imported_derivation_modules
    frontier = list(imported_derivation_modules)
    while frontier:
        module_name = frontier.pop()
        for dependency in dependency_graph[module_name]:
            if dependency not in reachable:
                reachable.add(dependency)
                frontier.append(dependency)
    unused_modules = sorted(module_names - reachable)
    if unused_modules:
        raise ValueError(
            "pinned modules are outside the consumer dependency closure: "
            + ", ".join(unused_modules)
        )

    lines.extend(_verify_runtime_origins(module_paths))
    expected_receipt, _ = _fresh_receipt(
        module_paths,
        snapshot_commit=snapshot_commit,
        snapshot_tree=snapshot_tree,
    )
    _verify_runtime_origins(module_paths)
    receipt_for_digest = expected_receipt
    if compare_receipt:
        actual_receipt = RECEIPT_PATH.read_bytes()
        if b"\r" in actual_receipt:
            raise ValueError("partial_decide_c3.json contains CR bytes")
        if actual_receipt != expected_receipt:
            raise ValueError(
                "partial_decide_c3.json differs from the deterministic renderer; "
                "run run_receipt.py --write deliberately"
            )
        if receipt_changes:
            raise ValueError(
                "receipt has Git worktree/index changes after byte equality:\n"
                + _format_status_records(receipt_changes)
            )
        receipt_for_digest = actual_receipt

    digest = hashlib.sha256(receipt_for_digest).hexdigest().upper()
    lines.append(f"tracked package: {len(tracked_files)} exact files, clean at HEAD")
    lines.append("derivation source package worktree: clean")
    lines.append("receipt transport: -text, LF-only")
    lines.append(f"receipt: {RECEIPT_PATH.name} {digest}")
    lines.append("AuthorityEffect: None")
    return lines, expected_receipt


def verify() -> list[str]:
    lines, _ = _verify(compare_receipt=True)
    return lines


def render_verified_receipt() -> bytes:
    """Render after full custody checks, allowing only the receipt to be dirty."""

    _, rendered = _verify(compare_receipt=False)
    return rendered


def main() -> int:
    try:
        lines = verify()
    except (
        ImportError,
        OSError,
        RuntimeError,
        ValueError,
        subprocess.SubprocessError,
    ) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "RECEIPT_PATH",
    "_assert_module_origin",
    "_controlled_imports",
    "_fresh_receipt",
    "_internal_dependencies",
    "_parse_tree_records",
    "_require_hex",
    "_safe_relative",
    "_validate_receipt_contract",
    "_verify_runtime_origins",
    "render_verified_receipt",
    "verify",
]
