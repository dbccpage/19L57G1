"""Mirror the beginner route without the Act-summary wrapper.

AuthorityEffect: None. Exact lesson sources remain in textbook/first_steps/.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from textbook.first_steps.build import build_explorer  # noqa: E402

WIKI_BASE = "https://github.com/dbccpage/19L57G1/wiki"
RAW_EXPLORER = "https://raw.githubusercontent.com/wiki/dbccpage/19L57G1/media/first_steps/explorer.html"
EXPLORER_URL = "https://htmlpreview.github.io/?" + RAW_EXPLORER


def page_map(source: Path) -> dict[str, str]:
    return {p.name: "textbook_first_steps" if p.stem == "README" else "textbook_first_steps_" + p.stem.lower()
            for p in sorted(source.glob("*.md")) if not p.name.startswith("REVIEW_")}


def build_first_steps(repo: Path, wiki: Path, commit: str) -> int:
    source = repo / "textbook/first_steps"
    if not source.is_dir():
        return 0
    pages = page_map(source)
    for name, slug in pages.items():
        text = (source / name).read_text(encoding="utf-8")
        for filename, target in pages.items():
            text = text.replace(f"]({filename})", f"]({target})")
        text = text.replace("](explorer.html)", f"]({EXPLORER_URL})")
        text = text.replace("](../search_lab/README.md)", "](textbook_search_lab)")
        text = text.replace("](../reasoning_lab/README.md)", "](textbook_reasoning_lab)")
        prefix = f"[Genesis Wiki](Home) · [First steps](textbook_first_steps) · [Card explorer]({EXPLORER_URL})\n\n"
        suffix = f"\n\n---\n\nSource snapshot: [`{commit[:12]}`](https://github.com/dbccpage/19L57G1/blob/{commit}/textbook/first_steps/{name}). Teaching examples and apparatus; `AuthorityEffect: None`.\n"
        (wiki / f"{slug}.md").write_text(prefix + text + suffix, encoding="utf-8", newline="\n")
    build_explorer(source, wiki / "media/first_steps/explorer.html",
                   {name: f"{WIKI_BASE}/{slug}" for name, slug in pages.items()})
    sidebar = wiki / "_Sidebar.md"
    content = sidebar.read_text(encoding="utf-8")
    content = content.replace("## Textbook\n", "## Textbook\n\n- [First steps: three cards, two questions](textbook_first_steps)\n", 1)
    sidebar.write_text(content, encoding="utf-8", newline="\n")
    home = wiki / "Home.md"
    content = home.read_text(encoding="utf-8")
    announcement = ("\n> **Begin with one small example:** [First steps: three cards, two questions](textbook_first_steps). "
                    "Five short lessons, a prediction-first explorer, and separate practice answers.\n")
    title_end = content.find("\n")
    home.write_text(content[:title_end + 1] + announcement + content[title_end + 1:], encoding="utf-8", newline="\n")
    return len(pages)


def first_steps_errors(repo: Path, wiki: Path) -> list[str]:
    source = repo / "textbook/first_steps"
    if not source.is_dir():
        return []
    errors = [f"missing first-steps page: {slug}" for slug in page_map(source).values()
              if not (wiki / f"{slug}.md").is_file()]
    asset = wiki / "media/first_steps/explorer.html"
    if not asset.is_file():
        errors.append("missing first-steps explorer")
    else:
        text = asset.read_text(encoding="utf-8")
        if (re.search(r'src="explorer\.mjs(?:[?\"])', text)
                or 'href="explorer.css"' in text or 'await fetch(' in text):
            errors.append("first-steps explorer has unresolved local assets")
    sidebar = (wiki / "_Sidebar.md").read_text(encoding="utf-8")
    if "](textbook_first_steps)" not in sidebar:
        errors.append("first-steps route is missing from sidebar")
    return errors
