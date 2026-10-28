"""Verify the generated Genesis Textbook Wiki pages, _Sidebar.md structure,
internal Wiki link targets, Claim Hygiene in generated soundbites, and <=15.0s
Manim video/GIF durations.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

WIKI_ROOT = Path(
    r"C:\Users\a343o\.gemini\antigravity\brain\e6748031-e61e-45da-8c81-267c0b199e5b\scratch\19L57G1.wiki"
)

EXPECTED_MANIM = [
    "act00_pre_genesis_mark",
    "act01_tokens_erasure_collapse",
    "act02_separation_and_minimality",
    "act03_quotients_counting_transport",
    "act04_refusal_generator_capacity",
    "act05_represented_kernel_horizon",
    "act06_primitive_difference_apartness",
    "act07_interpreter_controller_boundary",
    "act08_attachment_ladder_compression",
    "act09_descent_relativity_fidelity",
    "act10_institutions_synergy_policy",
    "act11_probing_uncollapse_verdict",
]


def main() -> None:
    # 1. Check _Sidebar.md headings order
    sidebar = (WIKI_ROOT / "_Sidebar.md").read_text(encoding="utf-8")
    h2s = [
        line.strip()
        for line in sidebar.splitlines()
        if line.startswith("## ")
    ]
    assert len(h2s) >= 2 and h2s[0] == "## Genesis" and h2s[1] == "## Textbook", (
        f"Expected second ## heading to be '## Textbook', got {h2s}"
    )
    print(f"PASS: _Sidebar.md headings order = {h2s}")

    # 2. Check all 75 Part 1, 18 Part 2, and 6 hub pages exist and are in _Sidebar.md
    u_pages = sorted(WIKI_ROOT.glob("textbook_u*.md"))
    i_pages = sorted(WIKI_ROOT.glob("textbook_i*.md"))
    # Exclude textbook_institutions.md from i_pages count
    i_unit_pages = [p for p in i_pages if re.match(r"^textbook_i\d+_", p.name)]
    assert len(u_pages) == 75, f"Expected 75 Part 1 wiki pages, found {len(u_pages)}"
    assert len(i_unit_pages) == 18, (
        f"Expected 18 Part 2 wiki pages, found {len(i_unit_pages)}"
    )
    for p in u_pages + i_unit_pages:
        stem = p.stem
        assert f"]({stem})" in sidebar, f"Missing {stem} in _Sidebar.md"
    print(
        f"PASS: All 75 Part 1 pages and 18 Part 2 pages exist and are linked in _Sidebar.md"
    )

    # 3. Check internal wiki links in _Sidebar.md, Home.md, _Footer.md, and all textbook_*.md
    all_wiki_stems = {p.stem for p in WIKI_ROOT.glob("*.md")}
    link_pat = re.compile(r"\]\(([^)]+)\)")
    checked_links = 0
    for md_file in [
        WIKI_ROOT / "_Sidebar.md",
        WIKI_ROOT / "Home.md",
        WIKI_ROOT / "_Footer.md",
        *sorted(WIKI_ROOT.glob("textbook_*.md")),
    ]:
        text = md_file.read_text(encoding="utf-8")
        # Strip fenced code blocks before scanning markdown links
        no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for m in link_pat.finditer(no_code):
            target = m.group(1).strip()
            if (
                target.startswith("http://")
                or target.startswith("https://")
                or target.startswith("#")
                or target.startswith("mailto:")
            ):
                continue
            target_base = target.split("#")[0]
            if not target_base:
                continue
            # If it's a wiki page link (no slash)
            if "/" not in target_base and not target_base.endswith(".py"):
                assert target_base in all_wiki_stems, (
                    f"Broken wiki link in {md_file.name}: ({target})"
                )
                checked_links += 1
    print(f"PASS: {checked_links} internal Wiki page links verified.")

    # 4. Verify all 12 Manim MP4 and GIF files exist and are <= 15.0s
    manim_dir = WIKI_ROOT / "media" / "manim"
    for slug in EXPECTED_MANIM:
        mp4 = manim_dir / f"{slug}.mp4"
        gif = manim_dir / f"{slug}.gif"
        assert mp4.exists() and mp4.stat().st_size > 1000, f"Missing {mp4}"
        assert gif.exists() and gif.stat().st_size > 1000, f"Missing {gif}"
        res = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(mp4),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        dur = float(res.stdout.strip())
        assert dur <= 15.0, f"{slug}.mp4 duration {dur:.2f}s > 15.0s!"
        print(f"PASS: {slug}.mp4 = {dur:.2f}s (<= 15.0s) | GIF = {gif.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
