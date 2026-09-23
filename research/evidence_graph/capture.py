"""Run explicit independent checks in a disposable snapshot checkout.

Outputs are observations, not a replacement for any source tree's verifier.
Logs, elapsed times and machine paths are written only to --run-dir.
AuthorityEffect: None.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

from eg_census import lean_imports
from eg_inventory import require_local_verifier, tree_inventory
from eg_reports import parse_report, report_program
from eg_sources import HERE, Snapshot, canonical, digest, git, load_snapshot, read_object

# Reviewed independent entry points; specialized checks retain their own scope.
SELECTED = ("endogenous_demand", "instance_demand", "primitive_difference_tower", "represented_execution",
            "x310_vertical_integration", "alpha_engine", "endogenous_continuum", "path_dependent_cost",
            "oriented_boundary", "balance_carrier", "cost_cohomology", "reach_measure", "reach_additivity",
            "second", "second_nofirst", "g013_trace_calculus", "g014_observer_descent", "g018_self_hosting",
            "p208c_commutator_tomography", "p209a_wigner_phase_space", "p209b_clifford_symplectic",
            "p209c_stabilizer_codes", "p209d_nonclassical_horizons", "g012_typed_translation")


def modules_for(snapshot: Snapshot, package: str) -> dict[str, str]:
    prefix = package + "/"
    return {path[len(prefix):-5].replace("/", "."): path for path in snapshot.files
            if path.startswith(prefix) and path.endswith(".lean") and Path(path).name != "lakefile.lean"
            and Path(path).name not in {"Inventory.lean", "AxiomReport.lean", "ParkedAudit.lean"}}


class Collector:
    def __init__(self, workspace: Path, run_dir: Path, output: Path) -> None:
        self.snapshot = load_snapshot()
        self.workspace, self.run_dir, self.output = workspace.resolve(), run_dir.resolve(), output
        if self.workspace == self.snapshot.repo.resolve():
            raise ValueError("DISPOSABLE_CHECKOUT_REQUIRED")
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.snapshot.preload(list(self.snapshot.files))
        head = git(self.workspace, "rev-parse", "HEAD").decode().strip()
        if head != self.snapshot.snapshot:
            raise ValueError("REPLAY_WRONG_SOURCE_HEAD")
        if git(self.workspace, "diff", "HEAD", "--name-only"):
            raise ValueError("REPLAY_TRACKED_WORKTREE_DIRTY")
        self.data: dict[str, Any] = {"schema": 1, "source_snapshot": head, "authority_effect": "None",
                                    "runs": [], "reports": [], "dependencies": []}
        if output.exists():
            self.data = read_object(output)
            if self.data["source_snapshot"] != head:
                raise ValueError("CAPTURE_SOURCE_HEAD_CHANGED")
        self.environment = dict(os.environ)
        self.environment["PYTHONUTF8"] = "1"
        self.environment["PATH"] = str(Path(sys.executable).parent) + os.pathsep + self.environment.get("PATH", "")
        self.environment["PYTHONPATH"] = str(self.workspace / "code") + os.pathsep + str(self.workspace)

    def save(self) -> None:
        self.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.output.with_suffix(".tmp")
        temporary.write_bytes(canonical(self.data))
        temporary.replace(self.output)

    def refresh_reports(self) -> None:
        """Refresh report apparatus only, retaining successful source builds and independent checks."""
        previous = list(self.data["reports"])
        for before in previous:
            package = before["package"]
            program = report_program(before["modules"])
            program_path = self.run_dir / (package.replace("/", "_") + "_report.lean")
            program_path.write_bytes(program)
            run, output = self.run(before["report_id"], ["lake", "env", "lean", str(program_path)], package, "compiled_types_and_binders")
            run["command"][-1] = "<generated-report.lean>"
            if run["exit_code"]:
                self.data["reports"] = [r for r in self.data["reports"] if r["package"] != package]
            else:
                report = parse_report(output, before["modules"])
                report.update({key: before[key] for key in ("package", "source_snapshot", "module_sources", "build_id", "report_id")})
                report["report_program_sha256"] = digest(program)
                self.data["reports"] = [r for r in self.data["reports"] if r["package"] != package] + [report]
            self.save()

    def run(self, identifier: str, command: list[str], cwd: str, scope: str, *, timeout: int = 900) -> tuple[dict[str, Any], str]:
        actual = [sys.executable if token == "python" and index == 0 else token for index, token in enumerate(command)]
        started = time.monotonic()
        try:
            process = subprocess.run(actual, cwd=self.workspace / cwd, env=self.environment,
                                     capture_output=True, timeout=timeout, check=False)
            code, raw = process.returncode, process.stdout + b"\n" + process.stderr
        except subprocess.TimeoutExpired as error:
            code, raw = 124, (error.stdout or b"") + b"\n" + (error.stderr or b"")
        except OSError as error:
            code, raw = 127, str(error).encode("utf-8")
        log_name = identifier.replace(":", "_").replace("/", "_")
        (self.run_dir / (log_name + ".log")).write_bytes(raw)
        (self.run_dir / (log_name + ".environment.json")).write_bytes(canonical({
            "command": actual, "cwd": str(self.workspace / cwd), "python": sys.executable,
            "elapsed_seconds": time.monotonic() - started, "log_sha256": digest(raw)}))
        changed = git(self.workspace, "diff", "--name-only").decode().splitlines()
        # Only this detached checkout's tracked files are restored; its untracked data remain.
        for path in changed:
            if path not in self.snapshot.files:
                raise ValueError("REPLAY_UNEXPECTED_TRACKED_FILE: " + path)
            target = (self.workspace / path).resolve()
            if not target.is_relative_to(self.workspace):
                raise ValueError("REPLAY_PATH_ESCAPE")
            target.write_bytes(self.snapshot.raw(path))
        record = {"id": identifier, "command": command, "cwd": cwd, "scope": scope,
                  "exit_code": code, "result": "PASSED" if code == 0 else "FAILED",
                  "output_digest": digest(raw), "source_snapshot": self.snapshot.snapshot,
                  "source_tree": git(self.workspace, "rev-parse", "HEAD^{tree}").decode().strip(),
                  "rewritten_tracked_paths": changed,
                  "gap": None if code == 0 else f"Independent command exited {code}; inspect its retained external log. No evidence promotion."}
        self.data["runs"] = [r for r in self.data["runs"] if r["id"] != identifier] + [record]
        self.save()
        print(f"{identifier}: {record['result']} ({code})", flush=True)
        return record, raw.decode("utf-8", "replace")

    def compiled(self, package: str, modules: dict[str, str]) -> None:
        label = package.replace("/", "_")
        build, _ = self.run("build:" + label, ["lake", "build", *sorted(modules)], package, "module_build")
        if build["exit_code"]:
            return
        program = report_program(sorted(modules))
        program_path = self.run_dir / (label + "_report.lean")
        program_path.write_bytes(program)
        run, output = self.run("report:" + label, ["lake", "env", "lean", str(program_path)], package, "compiled_types_and_binders")
        # Keep scientific command portable; machine command is retained outside the repository.
        run["command"][-1] = "<generated-report.lean>"
        self.save()
        if run["exit_code"] == 0:
            report = parse_report(output, sorted(modules))
            report.update({"package": package, "source_snapshot": self.snapshot.snapshot,
                           "module_sources": modules, "report_program_sha256": digest(program),
                           "build_id": build["id"], "report_id": run["id"]})
            self.data["reports"] = [r for r in self.data["reports"] if r["package"] != package] + [report]
            self.save()
        for module, path in sorted(modules.items()):
            command = ["lake", "env", "lean", "--deps", path[len(package) + 1:]]
            dep_run, raw = self.run("deps:" + label + ":" + module, command, package, "compiler_direct_dependencies", timeout=120)
            paths = []
            for line in raw.splitlines():
                candidate = Path(line.strip())
                if candidate.suffix != ".olean":
                    continue
                if not candidate.is_absolute():
                    candidate = self.workspace / package / candidate
                candidate = candidate.resolve()
                if candidate.is_relative_to(self.workspace):
                    paths.append(candidate.relative_to(self.workspace).as_posix())
                else:
                    parts = candidate.as_posix().split("/lib/lean/", 1)
                    paths.append("<toolchain>/" + parts[-1] if len(parts) == 2 else "<external>/" + candidate.name)
            record = {"source": self.snapshot.reference(path), "package": package, "module": module,
                      "header_imports": lean_imports(self.snapshot.text(path)), "dependencies": sorted(paths),
                      "replay_id": dep_run["id"], "result": dep_run["result"],
                      "gap": None if dep_run["exit_code"] == 0 and paths else "No successful nonempty compiler dependency population."}
            self.data["dependencies"] = [r for r in self.data["dependencies"] if r["source"]["path"] != path] + [record]
            self.save()

    def core(self) -> None:
        self.compiled("lean4", modules_for(self.snapshot, "lean4"))

    def research(self, names: list[str]) -> None:
        trees = {row["name"]: row for row in tree_inventory(self.snapshot)}
        for name in names:
            tree = trees[name]
            commands = tree["verifier_commands"]
            complete = [row for row in commands if row["role"] == "complete"]
            for index, row in enumerate(complete or commands):
                require_local_verifier(tree, row["argv"], row["cwd"])
                self.run(f"independent:{name}:{index}", row["argv"], row["cwd"], "tree_own_" + row["role"])
            package = f"research/{name}/lean"
            modules = modules_for(self.snapshot, package)
            if modules:
                self.compiled(package, modules)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=HERE / "evidence" / "capture.json")
    parser.add_argument("--mode", choices=("core", "research", "reports"), required=True)
    parser.add_argument("--trees", nargs="*", choices=SELECTED)
    args = parser.parse_args()
    collector = Collector(args.workspace, args.run_dir, args.output)
    if args.mode == "core":
        collector.core()
    elif args.mode == "reports":
        collector.refresh_reports()
    else:
        collector.research(list(SELECTED) if args.trees is None else args.trees)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
