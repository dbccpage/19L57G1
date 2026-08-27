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
import stat
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
    "No panel-derived decision input, panel adapter, object-language generator, "
    "measure choice, reading choice, response authorization, authorized or "
    "persistent response application, or event committed to the declared base "
    "is declared."
)
REQUIRED_TERMINALS = (
    "C3_UNIQUE_DELTA_EMPTY",
    "C3_MU2_UNIQUE_CLASS_INHABITED",
    "G3_REMAINS_CONJECTURE",
    "G4_REMAINS_CONJECTURE",
    "NO_AUTHORIZED_OR_PERSISTENT_RESPONSE_APPLICATION",
    "NO_EVENT_COMMITTED_TO_DECLARED_BASE",
    "NO_PANEL_DERIVED_INPUT",
    "NO_PANEL_ENGINE_ADAPTER",
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
FRESH_RENDERER_FLAGS = ("-I", "-B", "-S")
G3_STATUS = "G3_REMAINS_CONJECTURE"
G4_STATUS = "G4_REMAINS_CONJECTURE"
EXPECTED_G1_STATUS_KEYS = {"g1", "g3", "g4", "ob1", "object_language", "t5"}
FINITE_G4_WITHDRAWAL = (
    "The terminals G4_HOLDS_UNDER_MU2 and "
    "G4_FAILS_AT_<3,mu1,reading_F_outside_target_argument> are WITHDRAWN "
    "because no chain correspondence was computed."
)
PIN_ROOT_KEYS = {
    "authorized_imports",
    "modules",
    "package_files",
    "policy",
    "schema",
    "source_package",
    "source_snapshot",
    "status_inputs",
}


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


def _loads_no_duplicate_keys(raw: str | bytes, where: str) -> object:
    """Decode JSON while refusing last-wins duplicate object names."""

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        decoded: dict[str, Any] = {}
        for key, value in pairs:
            if key in decoded:
                raise ValueError(f"{where}: duplicate JSON key {key!r}")
            decoded[key] = value
        return decoded

    return json.loads(raw, object_pairs_hook=reject_duplicates)


def _read_pins() -> dict[str, Any]:
    payload = _loads_no_duplicate_keys(
        PINS_PATH.read_text(encoding="utf-8"), "SOURCE_PINS.json"
    )
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


def _format_package_census_difference(
    declared_files: set[PurePosixPath],
    head_files: set[PurePosixPath],
    tracked_files: set[PurePosixPath],
) -> str:
    populations = (
        ("declaration", declared_files),
        ("HEAD", head_files),
        ("index", tracked_files),
    )
    differing = [
        path
        for path in sorted(declared_files | head_files | tracked_files)
        if len({path in files for _, files in populations}) != 1
    ]
    if not differing:
        raise ValueError("package census formatter received equal populations")
    return "; ".join(
        f"{path} ["
        + ", ".join(
            f"{label}={'yes' if path in files else 'no'}"
            for label, files in populations
        )
        + "]"
        for path in differing
    )


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


def _require_regular_receipt_target(path: Path = RECEIPT_PATH) -> None:
    """Reject a missing, non-regular, symlink, or Windows reparse target."""

    try:
        target_stat = path.lstat()
    except FileNotFoundError as error:
        raise ValueError(
            f"receipt worktree target must be an existing regular file: {path}"
        ) from error
    file_attributes = getattr(target_stat, "st_file_attributes", 0)
    if (
        not stat.S_ISREG(target_stat.st_mode)
        or stat.S_ISLNK(target_stat.st_mode)
        or bool(file_attributes & 0x400)
    ):
        raise ValueError(
            "receipt worktree target must be a regular non-symlink, "
            f"non-reparse file: {path}"
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
            "tracked package census differs across declaration, HEAD, and index: "
            + _format_package_census_difference(
                declared_files,
                head_files,
                tracked_files,
            )
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
    if allow_receipt_dirty:
        _require_regular_receipt_target()

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


def _expect_exact_integer(value: object, expected: int, where: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value != expected:
        raise ValueError(f"{where} must be the exact integer {expected}")


def _nonnegative_integer(value: object, where: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{where} must be a nonnegative integer")
    return value


def _expect_exact_integer_sequence(
    value: object, expected: tuple[int, ...], where: str
) -> None:
    if not isinstance(value, list) or len(value) != len(expected):
        raise ValueError(f"{where} must be the exact integer list {list(expected)}")
    for index, expected_item in enumerate(expected):
        _expect_exact_integer(value[index], expected_item, f"{where}[{index}]")


def _validate_pin_structure(pins: dict[str, Any]) -> None:
    """Reject undeclared structure before any pin value can carry a claim."""

    _expect_exact_keys(pins, PIN_ROOT_KEYS, "SOURCE_PINS")

    snapshot = _object_dict(pins["source_snapshot"], "source_snapshot")
    _expect_exact_keys(snapshot, {"commit", "tree"}, "source_snapshot")
    source_package = _object_dict(pins["source_package"], "source_package")
    _expect_exact_keys(
        source_package, {"module", "path", "tree"}, "source_package"
    )

    modules_value = pins["modules"]
    if not isinstance(modules_value, list) or not modules_value:
        raise ValueError("modules must be a nonempty list")
    module_names: set[str] = set()
    for index, raw_entry in enumerate(modules_value):
        entry = _object_dict(raw_entry, f"modules[{index}]")
        _expect_exact_keys(
            entry, {"module", "path", "sha256"}, f"modules[{index}]"
        )
        module_name = _required_string(entry, "module", f"modules[{index}]")
        if DERIVATION_MODULE_RE.fullmatch(module_name) is None:
            raise ValueError(f"invalid pinned derivation module name: {module_name}")
        if module_name in module_names:
            raise ValueError(f"duplicate pinned module: {module_name}")
        module_names.add(module_name)

    status_inputs = pins["status_inputs"]
    if not isinstance(status_inputs, list) or not status_inputs:
        raise ValueError("status_inputs must be a nonempty list")
    for index, raw_entry in enumerate(status_inputs):
        entry = _object_dict(raw_entry, f"status_inputs[{index}]")
        _expect_exact_keys(
            entry,
            {"path", "required_terminals", "sha256"},
            f"status_inputs[{index}]",
        )

    declared_files = _declared_package_files(pins)
    declared_python = {path for path in declared_files if path.suffix == ".py"}
    local_modules = set(_local_module_paths(declared_python))
    allowed_modules = module_names | local_modules
    authorized = _object_dict(pins["authorized_imports"], "authorized_imports")
    expected_consumers = {path.as_posix() for path in declared_python}
    if set(authorized) != expected_consumers:
        raise ValueError(
            "authorized_imports consumer keys differ from declared Python files"
        )
    for consumer, declaration in authorized.items():
        _declared_imports(declaration, consumer, allowed_modules)


def _validate_g3_g4_status_payload(payload: dict[str, object]) -> None:
    statuses = _object_dict(payload.get("statuses"), "G1 class statuses")
    _expect_exact_keys(
        statuses,
        EXPECTED_G1_STATUS_KEYS,
        "G1 class statuses",
    )
    if statuses["g3"] != G3_STATUS or statuses["g4"] != G4_STATUS:
        raise ValueError("G1 class receipt statuses.g3/g4 differ from conjecture freeze")

    terminals = payload.get("terminals")
    if not isinstance(terminals, list) or not all(
        isinstance(item, str) for item in terminals
    ):
        raise ValueError("G1 class status receipt terminals must be strings")
    for required in (G3_STATUS, G4_STATUS):
        if terminals.count(required) != 1:
            raise ValueError(
                f"G1 class receipt must contain exactly one {required} terminal"
            )
    competing = sorted(
        item
        for item in terminals
        if (item.startswith("G3_") or item.startswith("G4_"))
        and item not in {G3_STATUS, G4_STATUS}
    )
    if competing:
        raise ValueError(
            "G1 class receipt contains competing G3/G4 terminals: "
            + ", ".join(competing)
        )

    withdrawn = payload.get("withdrawn_sentences")
    if not isinstance(withdrawn, list) or not all(
        isinstance(item, str) for item in withdrawn
    ):
        raise ValueError("G1 class receipt withdrawn_sentences must be strings")
    if withdrawn.count(FINITE_G4_WITHDRAWAL) != 1:
        raise ValueError("G1 class receipt lost the exact finite-G4 withdrawal")


def _validate_delta_item(
    value: object, where: str
) -> tuple[int, int, tuple[int, ...]]:
    item = _object_dict(value, where)
    kind = item.get("kind")
    if kind == "datum":
        _expect_exact_keys(item, {"kind"}, where)
        return (0, 0, ())
    if kind == "form":
        _expect_exact_keys(item, {"arity", "kind"}, where)
        arity = _nonnegative_integer(item["arity"], f"{where}.arity")
        return (1, arity, ())
    if kind == "rule_all":
        _expect_exact_keys(item, {"form", "kind"}, where)
        form = _nonnegative_integer(item["form"], f"{where}.form")
        return (2, form, ())
    if kind == "inst":
        _expect_exact_keys(item, {"args", "form", "kind"}, where)
        form = _nonnegative_integer(item["form"], f"{where}.form")
        raw_args = item["args"]
        if not isinstance(raw_args, list):
            raise ValueError(f"{where}.args must be an integer list")
        args = tuple(
            _nonnegative_integer(argument, f"{where}.args[{index}]")
            for index, argument in enumerate(raw_args)
        )
        return (3, form, args)
    raise ValueError(f"{where}.kind is not a closed delta-item kind: {kind!r}")


def _validate_delta(value: object, where: str, *, expected_items: int) -> str:
    if not isinstance(value, list):
        raise ValueError(f"{where} delta must be a list")
    if len(value) != expected_items:
        raise ValueError(f"{where} delta must contain exactly {expected_items} items")
    item_keys = [
        _validate_delta_item(item, f"{where}[{index}]")
        for index, item in enumerate(value)
    ]
    if len(set(item_keys)) != len(item_keys):
        raise ValueError(f"{where} delta contains duplicate items")
    if item_keys != sorted(item_keys):
        raise ValueError(f"{where} delta items are not in canonical order")
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _computed_member_canonical_key(
    value: object,
    *,
    reading_name: str,
    target: tuple[int, int],
    perm_budget: int,
    where: str,
) -> str:
    """Recompute a class member's key from the pinned engine semantics."""

    # The production verifier calls this helper only after the custody/import
    # checks have pinned these blobs and verified their runtime origins.
    from derivation.candidates import (
        NewDatum,
        NewForm,
        NewInst,
        NewRuleAll,
        delta_events,
    )
    from derivation.engine import READING_F, READING_L
    from derivation.iso import canonical
    from derivation.model import Impose, replay

    readings = {"F": READING_F, "L": READING_L}
    reading = readings.get(reading_name)
    if reading is None or reading.target != target:
        raise ValueError(f"{where} has no pinned reading/target semantics")
    if not isinstance(value, list):
        raise ValueError(f"{where} delta must be a list")

    items: list[NewDatum | NewForm | NewInst | NewRuleAll] = []
    for index, raw_item in enumerate(value):
        item_where = f"{where}[{index}]"
        item = _object_dict(raw_item, item_where)
        kind = item.get("kind")
        if kind == "datum":
            _expect_exact_keys(item, {"kind"}, item_where)
            items.append(NewDatum())
        elif kind == "form":
            _expect_exact_keys(item, {"arity", "kind"}, item_where)
            items.append(
                NewForm(_nonnegative_integer(item["arity"], f"{item_where}.arity"))
            )
        elif kind == "rule_all":
            _expect_exact_keys(item, {"form", "kind"}, item_where)
            items.append(
                NewRuleAll(_nonnegative_integer(item["form"], f"{item_where}.form"))
            )
        elif kind == "inst":
            _expect_exact_keys(item, {"args", "form", "kind"}, item_where)
            raw_args = item["args"]
            if not isinstance(raw_args, list):
                raise ValueError(f"{item_where}.args must be an integer list")
            args = tuple(
                _nonnegative_integer(argument, f"{item_where}.args[{arg_index}]")
                for arg_index, argument in enumerate(raw_args)
            )
            items.append(
                NewInst(
                    _nonnegative_integer(item["form"], f"{item_where}.form"),
                    args,
                )
            )
        else:
            raise ValueError(
                f"{item_where}.kind is not a closed delta-item kind: {kind!r}"
            )

    regime = replay(reading.genesis)
    child = replay(
        (Impose(target[0], target[1]),) + delta_events(regime, tuple(items)),
        regime,
    )
    return json.dumps(
        canonical(child, perm_budget), sort_keys=True, separators=(",", ":")
    )


def _validate_canonical_key(value: object, where: str) -> str:
    if not isinstance(value, list) or len(value) != 5:
        raise ValueError(f"{where} canonical_key must be a five-item list")
    n_data = _nonnegative_integer(value[0], f"{where}.canonical_key[0]")

    raw_forms = value[1]
    if not isinstance(raw_forms, list):
        raise ValueError(f"{where} canonical_key forms must be an integer list")
    forms = tuple(
        _nonnegative_integer(arity, f"{where}.canonical_key.forms[{index}]")
        for index, arity in enumerate(raw_forms)
    )

    raw_insts = value[2]
    if not isinstance(raw_insts, list):
        raise ValueError(f"{where} canonical_key insts must be a list")
    insts: list[tuple[int, tuple[int, ...]]] = []
    for index, raw_inst in enumerate(raw_insts):
        if not isinstance(raw_inst, list) or len(raw_inst) != 2:
            raise ValueError(
                f"{where}.canonical_key.insts[{index}] must be [form, args]"
            )
        form = _nonnegative_integer(
            raw_inst[0], f"{where}.canonical_key.insts[{index}].form"
        )
        raw_args = raw_inst[1]
        if not isinstance(raw_args, list):
            raise ValueError(
                f"{where}.canonical_key.insts[{index}].args must be an integer list"
            )
        args = tuple(
            _nonnegative_integer(
                argument,
                f"{where}.canonical_key.insts[{index}].args[{arg_index}]",
            )
            for arg_index, argument in enumerate(raw_args)
        )
        if form >= len(forms) or len(args) != forms[form] or any(
            argument >= n_data for argument in args
        ):
            raise ValueError(
                f"{where}.canonical_key.insts[{index}] is outside its form/data table"
            )
        insts.append((form, args))
    if insts != sorted(set(insts)):
        raise ValueError(f"{where} canonical_key insts must be unique and sorted")

    raw_rules = value[3]
    if not isinstance(raw_rules, list):
        raise ValueError(f"{where} canonical_key rules must be an integer list")
    rules = tuple(
        _nonnegative_integer(rule, f"{where}.canonical_key.rules[{index}]")
        for index, rule in enumerate(raw_rules)
    )
    if any(rule >= len(forms) for rule in rules) or list(rules) != sorted(set(rules)):
        raise ValueError(
            f"{where} canonical_key rules must be in-range, unique, and sorted"
        )

    raw_requirements = value[4]
    if not isinstance(raw_requirements, list):
        raise ValueError(f"{where} canonical_key requirements must be a list")
    requirements: list[tuple[int, int]] = []
    for index, raw_pair in enumerate(raw_requirements):
        if not isinstance(raw_pair, list) or len(raw_pair) != 2:
            raise ValueError(
                f"{where}.canonical_key.requirements[{index}] must be an integer pair"
            )
        left = _nonnegative_integer(
            raw_pair[0], f"{where}.canonical_key.requirements[{index}][0]"
        )
        right = _nonnegative_integer(
            raw_pair[1], f"{where}.canonical_key.requirements[{index}][1]"
        )
        if not left < right < n_data:
            raise ValueError(
                f"{where}.canonical_key.requirements[{index}] is not ordered/in-range"
            )
        requirements.append((left, right))
    if requirements != sorted(set(requirements)):
        raise ValueError(
            f"{where} canonical_key requirements must be unique and sorted"
        )
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


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
        _expect_exact_integer_sequence(
            row["target"], expected_target, f"receipt target for reading {reading_name}"
        )
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
            if grade["measure"] != measure:
                raise ValueError(
                    f"receipt grade request differs for {reading_name}/{measure}"
                )
            _expect_exact_integer_sequence(
                grade["target"],
                expected_target,
                f"receipt grade target for {reading_name}/{measure}",
            )
            bounds = _object_dict(
                grade["bounds"], f"receipt bounds for {reading_name}/{measure}"
            )
            _expect_exact_keys(
                bounds,
                {"max_arity", "max_items"},
                f"receipt bounds for {reading_name}/{measure}",
            )
            try:
                _expect_exact_integer(
                    bounds["max_arity"],
                    2,
                    f"receipt bounds.max_arity for {reading_name}/{measure}",
                )
                _expect_exact_integer(
                    bounds["max_items"],
                    2,
                    f"receipt bounds.max_items for {reading_name}/{measure}",
                )
            except ValueError as error:
                raise ValueError(
                    f"receipt bounds differ for {reading_name}/{measure}"
                ) from error
            minimum_cost = _object_dict(
                grade["minimum_cost"],
                f"receipt minimum cost for {reading_name}/{measure}",
            )
            _expect_exact_keys(
                minimum_cost,
                {"items", "new_form_arity_sum"},
                f"receipt minimum cost for {reading_name}/{measure}",
            )
            try:
                _expect_exact_integer(
                    minimum_cost["items"],
                    2,
                    f"receipt minimum cost items for {reading_name}/{measure}",
                )
                if measure == "mu1":
                    if minimum_cost["new_form_arity_sum"] is not None:
                        raise ValueError("mu1 arity sum must be null")
                else:
                    _expect_exact_integer(
                        minimum_cost["new_form_arity_sum"],
                        1,
                        f"receipt minimum arity cost for {reading_name}/{measure}",
                    )
            except ValueError as error:
                raise ValueError(
                    f"receipt minimum cost differs for {reading_name}/{measure}"
                ) from error
            try:
                _expect_exact_integer(
                    grade["iso_perm_budget"],
                    100_000,
                    f"receipt permutation budget for {reading_name}/{measure}",
                )
            except ValueError as error:
                raise ValueError(
                    f"receipt permutation budget differs for {reading_name}/{measure}"
                ) from error
            try:
                _expect_exact_integer(
                    grade["raw_minimum_count"],
                    raw_count,
                    f"receipt raw-minimum count for {reading_name}/{measure}",
                )
            except ValueError as error:
                raise ValueError(
                    f"receipt raw-minimum count differs for {reading_name}/{measure}"
                ) from error
            raw_minima = grade["raw_minima"]
            if not isinstance(raw_minima, list) or len(raw_minima) != raw_count:
                raise ValueError(
                    f"receipt raw-minimum population differs for {reading_name}/{measure}"
                )
            normalized_raw = [
                _validate_delta(
                    delta,
                    f"receipt raw minimum {reading_name}/{measure}/{raw_index}",
                    expected_items=2,
                )
                for raw_index, delta in enumerate(raw_minima)
            ]
            if len(set(normalized_raw)) != len(normalized_raw):
                raise ValueError(
                    f"receipt raw minima are not unique for {reading_name}/{measure}"
                )
            try:
                _expect_exact_integer(
                    grade["iso_class_count"],
                    class_count,
                    f"receipt class count for {reading_name}/{measure}",
                )
            except ValueError as error:
                raise ValueError(
                    f"receipt class count differs for {reading_name}/{measure}"
                ) from error
            classes = grade["classes"]
            if not isinstance(classes, list) or len(classes) != class_count:
                raise ValueError(
                    f"receipt class population differs for {reading_name}/{measure}"
                )
            retained_members: set[str] = set()
            canonical_keys: set[str] = set()
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
                canonical_key = _validate_canonical_key(
                    response_class["canonical_key"],
                    f"receipt class {reading_name}/{measure}/{class_index}",
                )
                if canonical_key in canonical_keys:
                    raise ValueError(
                        f"receipt canonical keys are not unique for "
                        f"{reading_name}/{measure}"
                    )
                canonical_keys.add(canonical_key)
                members = response_class["members"]
                size = response_class["size"]
                if not isinstance(members, list) or not members:
                    raise ValueError(
                        f"receipt class membership differs for "
                        f"{reading_name}/{measure}/{class_index}"
                    )
                try:
                    _expect_exact_integer(
                        size,
                        len(members),
                        f"receipt class size for {reading_name}/{measure}/{class_index}",
                    )
                except ValueError as error:
                    raise ValueError(
                        f"receipt class membership differs for "
                        f"{reading_name}/{measure}/{class_index}"
                    ) from error
                normalized_members = {
                    _validate_delta(
                        member,
                        "receipt class member "
                        f"{reading_name}/{measure}/{class_index}/{member_index}",
                        expected_items=2,
                    )
                    for member_index, member in enumerate(members)
                }
                if len(normalized_members) != len(members):
                    raise ValueError(
                        f"receipt class contains duplicate members for "
                        f"{reading_name}/{measure}/{class_index}"
                    )
                overlap = retained_members & normalized_members
                if overlap:
                    raise ValueError(
                        f"receipt classes overlap for {reading_name}/{measure}"
                    )
                retained_members.update(normalized_members)
            if retained_members != set(normalized_raw):
                raise ValueError(
                    f"receipt classes do not retain every raw minimum for "
                    f"{reading_name}/{measure}"
                )

    forbidden = sorted(_receipt_keys(payload) & FORBIDDEN_RECEIPT_KEYS)
    if forbidden:
        raise ValueError(
            "receipt contains selecting/applying keys: " + ", ".join(forbidden)
        )


def _validate_receipt_class_bindings(payload: dict[str, object]) -> None:
    """Bind every retained member to its independently recomputed class key."""

    readings = payload.get("readings")
    if not isinstance(readings, list) or len(readings) != 2:
        raise ValueError("receipt readings must be exactly [L, F]")
    for reading_index, (reading_name, expected) in enumerate(
        EXPECTED_RECEIPT_READINGS.items()
    ):
        expected_target, expected_grades = expected
        row = _object_dict(readings[reading_index], f"receipt readings[{reading_index}]")
        grades = _object_dict(row.get("grades"), f"reading {reading_name} grades")
        for measure in expected_grades:
            option = _object_dict(
                grades.get(measure),
                f"reading {reading_name} grade {measure} option",
            )
            grade = _object_dict(
                option.get("grade"), f"reading {reading_name} grade {measure}"
            )
            perm_budget = _nonnegative_integer(
                grade.get("iso_perm_budget"),
                f"receipt permutation budget for {reading_name}/{measure}",
            )
            classes = grade.get("classes")
            if not isinstance(classes, list):
                raise ValueError(
                    f"receipt class population differs for {reading_name}/{measure}"
                )
            for class_index, raw_class in enumerate(classes):
                response_class = _object_dict(
                    raw_class,
                    f"reading {reading_name} grade {measure} class {class_index}",
                )
                canonical_key = _validate_canonical_key(
                    response_class.get("canonical_key"),
                    f"receipt class {reading_name}/{measure}/{class_index}",
                )
                members = response_class.get("members")
                if not isinstance(members, list):
                    raise ValueError(
                        f"receipt class membership differs for "
                        f"{reading_name}/{measure}/{class_index}"
                    )
                for member_index, member in enumerate(members):
                    member_where = (
                        "receipt class member "
                        f"{reading_name}/{measure}/{class_index}/{member_index}"
                    )
                    computed_key = _computed_member_canonical_key(
                        member,
                        reading_name=reading_name,
                        target=expected_target,
                        perm_budget=perm_budget,
                        where=member_where,
                    )
                    if computed_key != canonical_key:
                        raise ValueError(
                            "receipt class member canonical key differs for "
                            f"{reading_name}/{measure}/{class_index}/{member_index}"
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
import sys

if "site" in sys.modules:
    raise RuntimeError("fresh renderer started with ambient site loaded")
if any("site-packages" in item.replace("\\", "/").lower() for item in sys.path):
    raise RuntimeError("fresh renderer started with ambient site-packages")

import json
import os
import pathlib

code, here, cache, expected_json = sys.argv[1:5]
sys.pycache_prefix = cache
sys.path[:] = [code, here, *sys.path]

def reject_duplicates(pairs):
    decoded = {}
    for key, value in pairs:
        if key in decoded:
            raise RuntimeError(f"fresh renderer duplicate JSON key {key!r}")
        decoded[key] = value
    return decoded

expected = json.loads(expected_json, object_pairs_hook=reject_duplicates)
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
                *FRESH_RENDERER_FLAGS,
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
    payload_object = _loads_no_duplicate_keys(rendered, "fresh receipt")
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
    _expect_exact_keys(
        entry,
        {"path", "required_terminals", "sha256"},
        "status input",
    )
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
    payload_object = _loads_no_duplicate_keys(
        _git_bytes("show", f"HEAD:{relative.as_posix()}"),
        "G1 class status receipt",
    )
    if not isinstance(payload_object, dict):
        raise ValueError("G1 class status receipt must contain an object")
    payload = _object_dict(payload_object, "G1 class status receipt")
    _validate_g3_g4_status_payload(payload)
    return (
        [f"inherited status: {relative} {wanted} G3/G4 conjectural"],
        [relative.as_posix()],
    )


def _verify(*, compare_receipt: bool) -> tuple[list[str], bytes]:
    pins = _read_pins()
    _validate_pin_structure(pins)
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
    expected_receipt, expected_payload = _fresh_receipt(
        module_paths,
        snapshot_commit=snapshot_commit,
        snapshot_tree=snapshot_tree,
    )
    _validate_receipt_class_bindings(expected_payload)
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
