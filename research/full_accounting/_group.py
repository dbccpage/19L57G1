"""Group every commit on HEAD into a dated index and era buckets."""

from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("research/full_accounting")
SEAL = "052e65739ddfd8c23c657562a51288cb083a2464"
text = Path("research/full_accounting/commits_files.txt").read_text(encoding="utf-8")

commits = []
cur = None
for line in text.splitlines():
    if line.startswith("COMMIT "):
        if cur:
            commits.append(cur)
        bits = line[7:].split(" ", 4)
        cur = {
            "sha": bits[0],
            "date": bits[1] if len(bits) > 1 else "",
            "time": bits[2] if len(bits) > 2 else "",
            "subject": bits[4] if len(bits) > 4 else "",
            "files": [],
        }
    elif line.strip() and cur is not None:
        cur["files"].append(line.strip().replace("\\", "/"))
if cur:
    commits.append(cur)


def loc(files):
    trees = set()
    roots = set()
    for f in files:
        p = f.replace("\\", "/")
        if p.startswith("research/"):
            parts = p.split("/")
            if len(parts) >= 2:
                trees.add(parts[1])
        else:
            roots.add(p.split("/")[0] if "/" in p else p)
    return sorted(trees), sorted(roots)


def era_of(c):
    d = c["date"]
    subj = c["subject"].lower()
    if d < "2026-08-17":
        return "A-sealed-derivation"
    if c["sha"] == SEAL or d == "2026-08-17":
        # 08-17 includes seal merge, coda isolate, residual close
        if "coda" in subj or "isolate" in subj:
            return "B-seal-and-isolate"
        if d == "2026-08-17":
            return "B-seal-and-isolate"
    if d < "2026-08-21":
        return "C-residuals-and-gates"
    if d < "2026-09-03":
        return "D-research-native"
    if d < "2026-09-09":
        return "E-boundary-second"
    return "F-cohorts-and-remainder"


by_day = defaultdict(list)
by_era = defaultdict(list)
root_touch = Counter()
tree_touch = Counter()
for c in commits:
    by_day[c["date"]].append(c)
    by_era[era_of(c)].append(c)
    trees, roots = loc(c["files"])
    for t in trees:
        tree_touch[t] += 1
    for r in roots:
        root_touch[r] += 1

lines = [
    "# Full commit index (HEAD)",
    "",
    f"Pin: HEAD `{commits[-1]['sha'][:12]}`. First listed `{commits[0]['sha'][:12]}`.",
    f"Count: {len(commits)} commits, newest-last within each day. Every SHA is listed.",
    "Merge commits often show 0 files (`git log --name-only` without `-m`).",
    "",
]
for day in sorted(by_day):
    cs = by_day[day]
    lines.append(f"## {day} ({len(cs)})")
    lines.append("")
    for c in cs:
        trees, roots = loc(c["files"])
        place = ",".join(trees[:6]) if trees else ",".join(roots[:6])
        extra = ""
        if len(trees) > 6:
            extra = f" +{len(trees) - 6} trees"
        elif not trees and len(roots) > 6:
            extra = f" +{len(roots) - 6} roots"
        lines.append(f"- `{c['sha'][:12]}` {c['subject']}")
        lines.append(f"  _{len(c['files'])} files; {place}{extra}_")
    lines.append("")

Path("research/full_accounting/commits_grouped.md").write_text(
    "\n".join(lines), encoding="utf-8"
)

era_lines = ["# Era buckets", "", f"n={len(commits)}", ""]
for k, cs in by_era.items():
    era_lines.append(f"## {k} ({len(cs)})")
    era_lines.append("")
    for c in cs:
        era_lines.append(f"- `{c['sha'][:12]}` {c['date']} {c['subject']}")
    era_lines.append("")
Path("research/full_accounting/eras.md").write_text("\n".join(era_lines), encoding="utf-8")

count_lines = [f"# touch counts n_commits={len(commits)}", "", "## roots"]
for k, v in root_touch.most_common():
    count_lines.append(f"{v}\t{k}")
count_lines += ["", "## research trees"]
for k, v in tree_touch.most_common():
    count_lines.append(f"{v}\t{k}")
Path("research/full_accounting/touch_counts.txt").write_text(
    "\n".join(count_lines) + "\n", encoding="utf-8"
)

print("commits", len(commits))
print("days", len(by_day))
print("eras", {k: len(v) for k, v in by_era.items()})
print("first", commits[0]["sha"][:8], commits[0]["date"], commits[0]["subject"][:70])
print("last", commits[-1]["sha"][:8], commits[-1]["date"], commits[-1]["subject"][:70])
