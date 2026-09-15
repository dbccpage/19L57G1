from collections import defaultdict
from pathlib import Path

text = Path("research/post_seal_walk/commits_files.txt").read_text(encoding="utf-8")
commits = []
cur = None
for line in text.splitlines():
    if line.startswith("COMMIT "):
        if cur:
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
if cur:
    commits.append(cur)


def trees(files):
    t = set()
    r = set()
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
by_day = defaultdict(list)
for c in chrono:
    by_day[c["date"]].append(c)

lines = [
    "# Post-seal commit index",
    "",
    "Pin: after `052e657` (2026-08-17 stopping re-run merge) through local HEAD `0e781408`.",
    f"Count: {len(commits)} commits. Newest-last. Every SHA is listed.",
    "Origin/main is 4 commits ahead; those four are in `commits_to_origin_main.tsv` and not in this list.",
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

out = Path("research/post_seal_walk/commits_grouped.md")
out.write_text("\n".join(lines), encoding="utf-8")
print("days", len(by_day), "commits", len(commits), "bytes", out.stat().st_size)
print("first", chrono[0]["sha"][:8], chrono[0]["date"], chrono[0]["subject"][:70])
print("last", chrono[-1]["sha"][:8], chrono[-1]["date"], chrono[-1]["subject"][:70])
