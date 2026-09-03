"""Verify SOURCE_MANIFEST.json: every pinned read-only source is
byte-identical at the snapshot and at HEAD; every pinned span (a line
range of a pinned file, hashed as its LF-joined lines with trailing LF)
matches at the snapshot and at HEAD; each copied Lean projection is an
exact declared slice of its pinned source after only the namespace rename;
the snapshot is an exact 40-digit id and an ancestor of HEAD; no tracked
path under a sealed prefix differs between the snapshot and HEAD; the
worktree carries nothing modified or untracked outside the write root; the
frozen native PROMPT.md still matches its recorded hash; and both recorded
PREDICTIONS.md content states reconstruct from the final append-only file.
Exit 0 on success, 1 with a named failure otherwise.  A manual receipt: no
CI gate runs this file.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys
import hashlib
import json
import re
import subprocess
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
WRITE_ROOT = "research/fresh_characters/"
SEALED_PATHSPECS = ("prompt", "paper", "code", "lean4/Derivation", "artifacts")


def git(*args: str) -> bytes:
    proc = subprocess.run(["git", *args], capture_output=True, cwd=REPO, check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)}: {proc.stderr.decode('utf-8', 'replace').strip()}"
        )
    return proc.stdout


def git_text(*args: str) -> str:
    return git(*args).decode("utf-8").strip()


def span_hash(blob: bytes, first: int, last: int) -> str:
    lines = blob.split(b"\n")
    if first < 1 or last < first or last > len(lines):
        raise RuntimeError(f"span {first}-{last} outside the blob's {len(lines)} lines")
    chunk = b"\n".join(lines[first - 1 : last]) + b"\n"
    return hashlib.sha256(chunk).hexdigest()


def outside_write_root(porcelain: str) -> list[str]:
    """Porcelain records naming a path outside the write root; pure."""
    out: list[str] = []
    for line in porcelain.splitlines():
        if not line.strip():
            continue
        paths = [p.strip().strip('"') for p in line[3:].split(" -> ")]
        if any(not p.replace("\\", "/").startswith(WRITE_ROOT) for p in paths):
            out.append(line)
    return out


def selected_lines(blob: bytes, ranges: list[list[int]]) -> list[bytes]:
    """Select inclusive, one-based line ranges from a pinned blob."""

    lines = blob.split(b"\n")
    selected: list[bytes] = []
    for item in ranges:
        if len(item) != 2:
            raise RuntimeError(f"source range must have two endpoints: {item}")
        first, last = item
        if first < 1 or last < first or last > len(lines):
            raise RuntimeError(f"source range {first}-{last} outside the blob's {len(lines)} lines")
        selected.extend(lines[first - 1 : last])
    return selected


def reconstructed_lines(blob: bytes, spec: dict[str, object]) -> list[bytes]:
    """The exact pinned source projection after the declared namespace rename."""

    raw_ranges = spec["source_ranges"]
    if not isinstance(raw_ranges, list) or not all(isinstance(item, list) for item in raw_ranges):
        raise RuntimeError("source_ranges must be a list of line-range lists")
    ranges = [[int(endpoint) for endpoint in item] for item in raw_ranges]
    old = str(spec["namespace_from"]).encode("ascii")
    new = str(spec["namespace_to"]).encode("ascii")
    expected: list[bytes] = []
    for line in selected_lines(blob, ranges):
        if line == b"namespace " + old:
            line = b"namespace " + new
        elif line == b"end " + old:
            line = b"end " + new
        expected.append(line)
    return expected


def prediction_freeze_hashes(predictions: bytes, boundary: bytes) -> list[str]:
    """Reconstruct the stage-1/2 prefix freeze and the final whole-file freeze."""

    prefix, separator, _ = predictions.partition(boundary)
    if not separator:
        raise RuntimeError(f"prediction freeze boundary not found: {boundary!r}")
    return [hashlib.sha256(prefix).hexdigest(), hashlib.sha256(predictions).hexdigest()]


def main() -> int:
    manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text("ascii"))
    snap = manifest["snapshot_commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", snap):
        print(f"FAIL: snapshot commit must be an exact 40-digit id: {snap}")
        return 1
    try:
        git("merge-base", "--is-ancestor", snap, "HEAD")
    except RuntimeError:
        print(f"FAIL: snapshot {snap} is not an ancestor of HEAD")
        return 1
    failures = 0
    for path, want in sorted(manifest["pins"].items()):
        for rev in (snap, "HEAD"):
            try:
                got = git_text("rev-parse", f"{rev}:{path}")
            except RuntimeError:
                print(f"FAIL: {path} missing at {rev}")
                failures += 1
                continue
            if got != want:
                print(f"FAIL: {path} blob at {rev} is {got}, pinned {want}")
                failures += 1
    for span in manifest["spans"]:
        path = span["path"]
        if path not in manifest["pins"]:
            print(f"FAIL: span path {path} is not itself pinned")
            failures += 1
        for rev in (snap, "HEAD"):
            try:
                blob = git("show", f"{rev}:{path}")
                got = span_hash(blob, int(span["first_line"]), int(span["last_line"]))
            except RuntimeError as exc:
                print(f"FAIL: span {path}:{span['first_line']}-{span['last_line']} at {rev}: {exc}")
                failures += 1
                continue
            if got != span["sha256"]:
                print(
                    f"FAIL: span {path}:{span['first_line']}-{span['last_line']} at {rev}"
                    f" hashes {got}, pinned {span['sha256']}"
                )
                failures += 1
    reconstructions = manifest.get("reconstructions", [])
    if not isinstance(reconstructions, list) or not reconstructions:
        print("FAIL: no source reconstruction bindings recorded")
        failures += 1
        reconstructions = []
    for spec in reconstructions:
        if not isinstance(spec, dict):
            print(f"FAIL: malformed reconstruction record: {spec!r}")
            failures += 1
            continue
        source_path = str(spec["source_path"])
        local_path = str(spec["local_path"])
        if source_path not in manifest["pins"]:
            print(f"FAIL: reconstruction source {source_path} is not itself pinned")
            failures += 1
            continue
        try:
            source_blob = git("show", f"{snap}:{source_path}")
            expected = reconstructed_lines(source_blob, spec)
            local_blob = (REPO / local_path).read_bytes()
            local_lines = local_blob.split(b"\n")
            first = int(spec["local_first_line"])
            last = int(spec["local_last_line"])
            if first < 1 or last < first or last > len(local_lines):
                raise RuntimeError(
                    f"local range {first}-{last} outside the file's {len(local_lines)} lines"
                )
            actual = local_lines[first - 1 : last]
        except (OSError, RuntimeError, ValueError) as exc:
            print(f"FAIL: reconstruction {source_path} -> {local_path}: {exc}")
            failures += 1
            continue
        if actual != expected:
            print(
                f"FAIL: {local_path}:{first}-{last} is not the declared exact projection"
                f" of pinned {source_path}"
            )
            failures += 1
    moved = [
        p
        for p in git("diff", "--name-only", "-z", snap, "HEAD", "--", *SEALED_PATHSPECS)
        .decode("utf-8")
        .split("\0")
        if p
    ]
    if moved:
        print("FAIL: tracked sealed paths differ between the snapshot and HEAD: " + ", ".join(moved))
        failures += 1
    porcelain = git("status", "--porcelain=v1", "--untracked-files=all").decode("utf-8")
    stray = outside_write_root(porcelain)
    if stray:
        print("FAIL: worktree carries changes outside the write root:\n  " + "\n  ".join(stray))
        failures += 1
    prompt_hash = hashlib.sha256((HERE / "PROMPT.md").read_bytes()).hexdigest()
    if prompt_hash != manifest["prompt_native_sha256"]:
        print(
            f"FAIL: PROMPT.md hash {prompt_hash} differs from frozen"
            f" {manifest['prompt_native_sha256']}"
        )
        failures += 1
    freezes = manifest["predictions_freezes"]
    if not isinstance(freezes, list) or len(freezes) != 2:
        print("FAIL: exactly two predictions freezes must be recorded")
        failures += 1
    else:
        predictions = (HERE / "PREDICTIONS.md").read_bytes()
        boundary = str(manifest["predictions_first_freeze_boundary"]).encode("ascii")
        try:
            got_freezes = prediction_freeze_hashes(predictions, boundary)
        except RuntimeError as exc:
            print(f"FAIL: {exc}")
            failures += 1
        else:
            for index, (got, want) in enumerate(zip(got_freezes, freezes, strict=True), start=1):
                if got != want:
                    print(
                        f"FAIL: reconstructed predictions freeze {index} hashes {got},"
                        f" recorded {want}"
                    )
                    failures += 1
    if failures:
        return 1
    print(
        f"pins clean: {len(manifest['pins'])} sources and {len(manifest['spans'])} spans"
        f" at snapshot and HEAD; sealed prefixes unchanged; nothing outside the write"
        f" root; {len(reconstructions)} source projections exact; native PROMPT.md frozen;"
        f" {len(freezes)} predictions freezes reconstructed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
