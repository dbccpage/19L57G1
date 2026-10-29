"""Verify the generated Genesis Textbook Wiki pages, _Sidebar.md structure,
research-tree sync, internal Wiki link targets, and <=15.0s Manim video/GIF
durations.

AuthorityEffect: None. Re-run whenever new textbook units or research trees are
added to main.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from research_population import inventory_errors, research_trees
from first_steps_wiki import first_steps_errors
from search_lab_wiki import search_lab_errors
from change_lab_wiki import change_lab_errors
from reasoning_lab_wiki import reasoning_lab_errors
from path_lab_wiki import path_lab_errors
from map_lab_wiki import map_lab_errors
from growth_lab_wiki import growth_lab_errors
from boundary_lab_wiki import boundary_lab_errors

DEFAULT_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_WIKI_ROOT = Path(
    os.environ.get(
        "GENESIS_WIKI_ROOT",
        str(DEFAULT_REPO_ROOT.parent / "19L57G1.wiki"),
    )
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

# Legacy baseline wiki page stems present in 19L57G1.wiki.git
BASELINE_WIKI_STEMS = {
    "Home",
    "_Footer",
    "_Sidebar",
    "admission_kernel",
    "alpha_harness",
    "artifacts_and_replay",
    "build_order_and_dependencies",
    "candidates_costs_and_ties",
    "closeout_and_historical_receipts",
    "concepts_and_glossary",
    "consumer_integration",
    "contribution_workflow",
    "engine_and_frontiers",
    "evidence_and_provenance",
    "faq",
    "foundations_and_passage",
    "genesis_overview",
    "getting_started",
    "isomorphism_and_quotients",
    "lean_verification",
    "limitations_and_open_obligations",
    "local_validation",
    "observation_and_separation",
    "papers_and_claim_ledgers",
    "python_module_reference",
    "repository_map",
    "research_alpha_engine",
    "research_atlas",
    "research_tree_index",
    "research_verification_and_custody",
    "review_scope_and_findings",
    "second_derivation_and_freeze",
    "source_contract",
    "troubleshooting",
    "wiki_maintenance",
    "worked_examples",
}


def verify_wiki(
    repo_root: Path,
    wiki_root: Path,
    skip_manim_media: bool = False,
) -> int:
    # 1. Check _Sidebar.md headings order
    sidebar_path = wiki_root / "_Sidebar.md"
    if not sidebar_path.is_file():
        print(f"FAIL: missing {sidebar_path}", file=sys.stderr)
        return 1
    sidebar = sidebar_path.read_text(encoding="utf-8")
    h2s = [
        line.strip()
        for line in sidebar.splitlines()
        if line.startswith("## ")
    ]
    if len(h2s) < 2 or h2s[0] != "## Genesis" or h2s[1] != "## Textbook":
        print(
            f"FAIL: Expected second ## heading to be '## Textbook', got {h2s}",
            file=sys.stderr,
        )
        return 1
    print(f"PASS: _Sidebar.md headings order = {h2s}")

    # 2. Check every Part 1 and Part 2 source unit in repo_root is mirrored and in _Sidebar.md
    expected_u_stems: list[str] = []
    for f in sorted((repo_root / "textbook" / "units").glob("*.md")):
        m = re.match(r"^(\d+)_(.+)\.md$", f.name)
        if m:
            expected_u_stems.append(f"textbook_u{int(m.group(1)):02d}_{m.group(2)}")

    expected_i_stems: list[str] = []
    for f in sorted((repo_root / "textbook" / "institutions" / "units").glob("*.md")):
        m = re.match(r"^(\d+)_(.+)\.md$", f.name)
        if m:
            expected_i_stems.append(f"textbook_i{int(m.group(1)):02d}_{m.group(2)}")

    if len(expected_u_stems) < 75 or len(expected_i_stems) < 18:
        print(
            f"FAIL: Expected >= 75 Part 1 and >= 18 Part 2 units, got {len(expected_u_stems)} and {len(expected_i_stems)}",
            file=sys.stderr,
        )
        return 1

    for stem in expected_u_stems + expected_i_stems:
        p = wiki_root / f"{stem}.md"
        if not p.is_file():
            print(f"FAIL: Missing mirrored Wiki page {p.name}", file=sys.stderr)
            return 1
        if f"]({stem})" not in sidebar:
            print(f"FAIL: Missing {stem} link in _Sidebar.md", file=sys.stderr)
            return 1
    print(
        f"PASS: All {len(expected_u_stems)} Part 1 pages and {len(expected_i_stems)} Part 2 pages exist and are linked in _Sidebar.md"
    )

    # 3. Check textbook_research_trees.md accounts for all research trees on main
    res_trees_page = wiki_root / "textbook_research_trees.md"
    if not res_trees_page.is_file():
        print("FAIL: Missing textbook_research_trees.md", file=sys.stderr)
        return 1
    res_trees_text = res_trees_page.read_text(encoding="utf-8")
    errors = inventory_errors(repo_root, res_trees_text)
    if errors:
        print("FAIL: research inventory mismatch; " + "; ".join(errors), file=sys.stderr)
        return 1
    synced_tree_count = len(research_trees(repo_root))
    print(
        f"PASS: textbook_research_trees.md synced with all {synced_tree_count} research trees on main"
    )

    # 4. Check internal wiki links in _Sidebar.md, Home.md, _Footer.md, and all textbook_*.md
    all_wiki_stems = {p.stem for p in wiki_root.glob("*.md")} | BASELINE_WIKI_STEMS
    link_pat = re.compile(r"\]\(([^)]+)\)")
    checked_links = 0
    for md_file in [
        wiki_root / "_Sidebar.md",
        wiki_root / "Home.md",
        wiki_root / "_Footer.md",
        *sorted(wiki_root.glob("textbook_*.md")),
    ]:
        text = md_file.read_text(encoding="utf-8")
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
            if "/" not in target_base and not target_base.endswith(".py"):
                if target_base not in all_wiki_stems:
                    print(
                        f"FAIL: Broken wiki link in {md_file.name}: ({target})",
                        file=sys.stderr,
                    )
                    return 1
                checked_links += 1
    print(f"PASS: {checked_links} internal Wiki page links verified.")

    route_errors = (first_steps_errors(repo_root, wiki_root) + search_lab_errors(repo_root, wiki_root)
                    + change_lab_errors(repo_root, wiki_root)
                    + reasoning_lab_errors(repo_root, wiki_root)
                    + path_lab_errors(repo_root, wiki_root)
                    + map_lab_errors(repo_root, wiki_root)
                    + growth_lab_errors(repo_root, wiki_root)
                    + boundary_lab_errors(repo_root, wiki_root))
    if route_errors:
        print("FAIL: " + "; ".join(route_errors), file=sys.stderr)
        return 1
    if (repo_root / "textbook/first_steps").is_dir():
        print("PASS: beginner lesson pages, sidebar entry, and self-contained explorer exist.")

    # 5. Verify all 12 Manim MP4 and GIF files if present and not skipped
    manim_dir = wiki_root / "media" / "manim"
    if not skip_manim_media:
        if not manim_dir.is_dir():
            print(f"FAIL: Missing media directory {manim_dir}", file=sys.stderr)
            return 1
        for slug in EXPECTED_MANIM:
            mp4 = manim_dir / f"{slug}.mp4"
            gif = manim_dir / f"{slug}.gif"
            if not mp4.exists() or mp4.stat().st_size <= 1000:
                print(f"FAIL: Missing {mp4}", file=sys.stderr)
                return 1
            if not gif.exists() or gif.stat().st_size <= 1000:
                print(f"FAIL: Missing {gif}", file=sys.stderr)
                return 1
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
            if dur > 15.0:
                print(
                    f"FAIL: {slug}.mp4 duration {dur:.2f}s > 15.0s!",
                    file=sys.stderr,
                )
                return 1
            gif_probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(gif)],
                capture_output=True, text=True, check=True,
            )
            gif_duration = float(gif_probe.stdout.strip())
            if not 0 < gif_duration <= 15.0:
                print(f"FAIL: {slug}.gif duration {gif_duration:.2f}s outside (0, 15.0]", file=sys.stderr)
                return 1
            print(
                f"PASS: {slug}.mp4 = {dur:.2f}s (<= 15.0s) | GIF = {gif.stat().st_size // 1024} KB"
            )
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help="Path to 19L57G1 repository root",
    )
    ap.add_argument(
        "--wiki-root",
        type=Path,
        default=None,
        help="Path to 19L57G1.wiki checkout (if omitted and default does not exist, builds into a temporary directory and verifies)",
    )
    ap.add_argument(
        "--skip-manim-media",
        action="store_true",
        help="Skip ffprobe check on media/manim/*.mp4 when verifying markdown generation in a temporary directory",
    )
    args = ap.parse_args(argv)
    repo_root = args.repo_root.resolve()

    if args.wiki_root is not None:
        wiki_root = args.wiki_root.resolve()
        return verify_wiki(repo_root, wiki_root, skip_manim_media=args.skip_manim_media)

    if DEFAULT_WIKI_ROOT.is_dir() and (DEFAULT_WIKI_ROOT / "_Sidebar.md").is_file():
        return verify_wiki(
            repo_root, DEFAULT_WIKI_ROOT.resolve(), skip_manim_media=args.skip_manim_media
        )

    # Otherwise, build into a temporary directory and verify automatically
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import build_wiki_textbook  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        build_wiki_textbook.build_all(repo_root, tmp_path)
        return verify_wiki(repo_root, tmp_path, skip_manim_media=True)


if __name__ == "__main__":
    raise SystemExit(main())
