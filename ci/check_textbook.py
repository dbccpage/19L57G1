"""Verify the Genesis Textbook Python checks, book-Lean checks, video script pacing,
and the GitHub Wiki Textbook mirror builder/verifier.

AuthorityEffect: None. This gate checks the textbook's executable scripts,
book-Lean reconstructions, and Wiki textbook mirror outside the sealed
derivation's authority boundary. Nothing in textbook/ is an input to prompt/,
paper/, code/, lean4/Derivation/, or artifacts/.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parent.parent
PART1_CHECKS = REPO / "textbook" / "checks"
PART2_CHECKS = REPO / "textbook" / "institutions" / "checks"
VIDEO_SCRIPT = REPO / "textbook" / "video_script_15s.md"
WIKI_BUILDER = REPO / "textbook" / "media" / "build_wiki_textbook.py"
WIKI_VERIFIER = REPO / "textbook" / "media" / "verify_wiki_textbook.py"

MIN_PART1_PY = 74
MIN_PART1_LEAN = 71
MIN_PART2_PY = 18
MAX_SEGMENT_WPM = 160.0


def discover_scripts() -> tuple[list[Path], list[Path], list[Path]]:
    part1_py = sorted(
        p for p in PART1_CHECKS.glob("u*.py")
        if not p.name.endswith("_lean.py")
    )
    part1_lean = sorted(PART1_CHECKS.glob("u*_lean.py"))
    part2_py = sorted(PART2_CHECKS.glob("i*.py"))
    return part1_py, part1_lean, part2_py


def check_video_pacing(path: Path = VIDEO_SCRIPT) -> list[str]:
    if not path.is_file():
        return [f"missing {path.relative_to(REPO)}"]
    text = path.read_text(encoding="utf-8")
    row_re = re.compile(
        r'^\|\s*`(\d+):(\d+)[–-](\d+):(\d+)`\s*\|\s*`(\d+)\s*s`\s*\|\s*`(\d+)`\s*\|\s*`(\d+)\s*wpm`\s*\|[^|]+\|\s*"([^"]+)"\s*\|$'
    )
    problems: list[str] = []
    segments = 0
    total_dur = 0
    for line in text.splitlines():
        m = row_re.match(line.strip())
        if not m:
            continue
        segments += 1
        m0, s0, m1, s1, dur_s, words_s, wpm_s, spoken = m.groups()
        span = (int(m1) * 60 + int(s1)) - (int(m0) * 60 + int(s0))
        dur = int(dur_s)
        declared_words = int(words_s)
        declared_wpm = int(wpm_s)
        actual_words = len([w for w in re.split(r"\s+", spoken.strip()) if w])
        actual_wpm = (actual_words * 60.0) / dur if dur > 0 else 999.0
        total_dur += dur
        if span != dur:
            problems.append(f"segment {m0}:{s0}-{m1}:{s1}: span {span}s != declared {dur}s")
        if actual_words != declared_words:
            problems.append(
                f"segment {m0}:{s0}-{m1}:{s1}: spoken text has {actual_words} words != declared {declared_words}"
            )
        if round(actual_wpm) != declared_wpm:
            problems.append(
                f"segment {m0}:{s0}-{m1}:{s1}: pace is {actual_wpm:.1f} wpm != declared {declared_wpm} wpm"
            )
        if actual_wpm > MAX_SEGMENT_WPM:
            problems.append(
                f"segment {m0}:{s0}-{m1}:{s1}: pace {actual_wpm:.1f} wpm exceeds {MAX_SEGMENT_WPM} wpm"
            )
    if segments < 4:
        problems.append(f"expected at least 4 timed narration segments in {path.name}, found {segments}")
    if total_dur != 15:
        problems.append(f"expected 15s total video duration in {path.name}, found {total_dur}s")
    return problems


def check_wiki_textbook_sync() -> list[str]:
    if not WIKI_BUILDER.is_file():
        return [f"missing {WIKI_BUILDER.relative_to(REPO)}"]
    if not WIKI_VERIFIER.is_file():
        return [f"missing {WIKI_VERIFIER.relative_to(REPO)}"]
    with tempfile.TemporaryDirectory() as tmp:
        build_proc = subprocess.run(
            [
                sys.executable,
                str(WIKI_BUILDER),
                "--repo-root",
                str(REPO),
                "--wiki-root",
                tmp,
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if build_proc.returncode != 0:
            return [
                f"build_wiki_textbook.py exited {build_proc.returncode}: {(build_proc.stdout + build_proc.stderr).strip()}"
            ]
        verify_proc = subprocess.run(
            [
                sys.executable,
                str(WIKI_VERIFIER),
                "--repo-root",
                str(REPO),
                "--wiki-root",
                tmp,
                "--skip-manim-media",
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if verify_proc.returncode != 0:
            return [
                f"verify_wiki_textbook.py exited {verify_proc.returncode}: {(verify_proc.stdout + verify_proc.stderr).strip()}"
            ]
    return []


def resolve_lean_env() -> tuple[str | None, str | None]:
    lake = shutil.which("lake")
    if lake is None:
        return None, None
    proc = subprocess.run(
        [lake, "env", sys.executable, "-c", "import os, shutil; print(shutil.which('lean') or ''); print(os.environ.get('LEAN_PATH', ''))"],
        cwd=REPO / "lean4",
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if proc.returncode != 0:
        return None, None
    lines = proc.stdout.splitlines()
    if len(lines) < 2 or not lines[0].strip():
        return None, None
    return lines[0].strip(), lines[1].strip()


def run_one(script: Path, extra_args: list[str] | None = None) -> tuple[Path, int, str]:
    env = dict(os.environ)
    code_dir = str(REPO / "code")
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{code_dir}{os.pathsep}{existing}" if existing else code_dir
    env["PYTHONIOENCODING"] = "utf-8"
    cmd = [sys.executable, str(script), *(extra_args or [])]
    proc = subprocess.run(
        cmd,
        cwd=REPO,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output = (proc.stdout + proc.stderr).strip()
    return script, proc.returncode, output


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--python-only", action="store_true", help="run only Python check scripts, video pacing, and Wiki sync check")
    ap.add_argument("--lean-only", action="store_true", help="run only book-Lean check scripts")
    ap.add_argument("--unit", help="filter scripts by substring (e.g. u59 or i13)")
    ap.add_argument("--workers", type=int, default=4, help="parallel worker count (default: 4)")
    args = ap.parse_args(argv)

    if args.python_only and args.lean_only:
        print("FAIL: --python-only and --lean-only are mutually exclusive", file=sys.stderr)
        return 1

    part1_py, part1_lean, part2_py = discover_scripts()
    if not args.unit:
        if len(part1_py) < MIN_PART1_PY:
            print(f"FAIL: expected >= {MIN_PART1_PY} Part 1 Python checks, found {len(part1_py)}", file=sys.stderr)
            return 1
        if len(part1_lean) < MIN_PART1_LEAN:
            print(f"FAIL: expected >= {MIN_PART1_LEAN} Part 1 Lean checks, found {len(part1_lean)}", file=sys.stderr)
            return 1
        if len(part2_py) < MIN_PART2_PY:
            print(f"FAIL: expected >= {MIN_PART2_PY} Part 2 Python checks, found {len(part2_py)}", file=sys.stderr)
            return 1

    if args.unit:
        part1_py = [p for p in part1_py if args.unit in p.name]
        part1_lean = [p for p in part1_lean if args.unit in p.name]
        part2_py = [p for p in part2_py if args.unit in p.name]

    failures: list[tuple[str, int, str]] = []

    if not args.lean_only:
        pacing_errors = check_video_pacing()
        if pacing_errors:
            for err in pacing_errors:
                print(f"FAIL: video_script_15s.md: {err}", file=sys.stderr)
            return 1
        print("video_script_15s.md pacing: ok (4 segments, 15s total, all <= 160 wpm)")

        if not args.unit:
            wiki_errors = check_wiki_textbook_sync()
            if wiki_errors:
                for err in wiki_errors:
                    print(f"FAIL: wiki textbook sync: {err}", file=sys.stderr)
                return 1
            print("wiki textbook build & verify: ok (all Part 1/Part 2 units, research trees, _Sidebar.md, and internal links verified)")

        py_scripts = [*part1_py, *part2_py]
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            futures = {pool.submit(run_one, s): s for s in py_scripts}
            for fut in as_completed(futures):
                script, code, out = fut.result()
                rel = script.relative_to(REPO).as_posix()
                if code != 0:
                    failures.append((rel, code, out))
        if failures:
            for rel, code, out in sorted(failures):
                print(f"FAIL: {rel} exited {code}\n{out}", file=sys.stderr)
            return 1
        print(
            f"textbook Python checks: {len(part1_py)} Part 1 + {len(part2_py)} Part 2 = "
            f"{len(py_scripts)} passed"
        )

    if not args.python_only:
        lean_bin, lean_path = resolve_lean_env()
        extra = ["--lean", lean_bin, "--lean-path", lean_path] if lean_bin and lean_path else []
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            futures = {pool.submit(run_one, s, extra): s for s in part1_lean}
            for fut in as_completed(futures):
                script, code, out = fut.result()
                rel = script.relative_to(REPO).as_posix()
                if code != 0:
                    failures.append((rel, code, out))
        if failures:
            for rel, code, out in sorted(failures):
                print(f"FAIL: {rel} exited {code}\n{out}", file=sys.stderr)
            return 1
        print(f"textbook book-Lean checks: {len(part1_lean)} passed")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
