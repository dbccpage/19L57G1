"""Generate local subject indexes and the tracked touch census at fixed pins."""

from collections import Counter, defaultdict
from pathlib import Path
import subprocess
from typing import TypedDict

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(__file__).resolve().parent
SEAL = "052e65739ddfd8c23c657562a51288cb083a2464"
WALK_SNAPSHOT = "0e7814089db5ed387489acd9553a9105b0b69462"
ORIGIN_SNAPSHOT = "dfe649445403d7d0326594c918430ae5456b1f6b"


class Commit(TypedDict):
    sha: str
    date: str
    time: str
    subject: str
    files: list[str]


def git_output(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


text = git_output(
    "log",
    "--format=COMMIT %H %ad %s",
    "--date=iso",
    "--name-only",
    f"{SEAL}..{WALK_SNAPSHOT}",
)
commits: list[Commit] = []
cur: Commit | None = None
for line in text.splitlines():
    if line.startswith("COMMIT "):
        if cur is not None:
            commits.append(cur)
        rest = line[7:]
        bits = rest.split(" ", 4)
        cur = {
            "sha": bits[0],
            "date": bits[1] if len(bits) > 1 else "",
            "time": bits[2] if len(bits) > 2 else "",
            "subject": bits[4] if len(bits) > 4 else "",
            "files": [],
        }
    elif line.strip() and cur is not None:
        cur["files"].append(line.strip().replace("\\", "/"))
if cur is not None:
    commits.append(cur)


def trees(files: list[str]) -> tuple[list[str], list[str]]:
    t: set[str] = set()
    r: set[str] = set()
    for f in files:
        p = f.replace("\\", "/")
        if p.startswith("research/"):
            parts = p.split("/")
            if len(parts) >= 2:
                t.add(parts[1])
        else:
            r.add(p.split("/")[0] if "/" in p else p)
    return sorted(t), sorted(r)


chrono = list(reversed(commits))
by_day: defaultdict[str, list[Commit]] = defaultdict(list)
for c in chrono:
    by_day[c["date"]].append(c)

lines = [
    "# Post-seal commit index",
    "",
    "Pin: after `052e657` (2026-08-17 stopping re-run merge) through walk snapshot `0e781408`.",
    f"Count: {len(commits)} commits. Newest-last. Every SHA is listed.",
    f"The origin snapshot `{ORIGIN_SNAPSHOT[:8]}` is 4 commits ahead; its expanded list is in `commits_origin_extra_shas.tsv`.",
    "",
]
for day in sorted(by_day):
    cs = by_day[day]
    lines.append(f"## {day} ({len(cs)})")
    lines.append("")
    for c in cs:
        t, r = trees(c["files"])
        loc = ",".join(t[:6]) if t else ",".join(r[:6])
        extra = ""
        if len(t) > 6:
            extra = f" +{len(t) - 6} trees"
        elif not t and len(r) > 6:
            extra = f" +{len(r) - 6} roots"
        nfiles = len(c["files"])
        short = c["sha"][:12]
        lines.append(f"- `{short}` {c['subject']}")
        lines.append(f"  _{nfiles} files; {loc}{extra}_")
    lines.append("")

out = ROOT / "commits_grouped.md"
out.write_text("\n".join(lines), encoding="utf-8")

root_touch: Counter[str] = Counter()
tree_touch: Counter[str] = Counter()
for commit in commits:
    commit_trees, commit_roots = trees(commit["files"])
    tree_touch.update(commit_trees)
    root_touch.update(commit_roots)

count_lines = [
    "# commit touch counts, generated from the pinned git history",
    f"# n_commits={len(commits)}",
    "",
    "## root",
]
count_lines.extend(
    f"{count}\t{name}"
    for name, count in sorted(root_touch.items(), key=lambda item: (-item[1], item[0]))
)
count_lines.extend(["", "## research trees"])
count_lines.extend(
    f"{count}\t{name}"
    for name, count in sorted(tree_touch.items(), key=lambda item: (-item[1], item[0]))
)
(ROOT / "commit_touch_counts.txt").write_text(
    "\n".join(count_lines) + "\n", encoding="utf-8"
)
print("days", len(by_day), "commits", len(commits), "bytes", out.stat().st_size)
print("first", chrono[0]["sha"][:8], chrono[0]["date"], chrono[0]["subject"][:70])
print("last", chrono[-1]["sha"][:8], chrono[-1]["date"], chrono[-1]["subject"][:70])
