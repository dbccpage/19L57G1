"""Mirror the source-backed search lab; AuthorityEffect: None."""
from pathlib import Path
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from textbook.search_lab.build_results import build, render  # noqa: E402

RAW_BASE = "https://raw.githubusercontent.com/wiki/dbccpage/19L57G1/media/search_lab/"
DESK_URL = "https://htmlpreview.github.io/?" + RAW_BASE + "results.html"


def page_map(source: Path) -> dict[str, str]:
    return {p.name: "textbook_search_lab" if p.stem == "README" else "textbook_search_lab_" + p.stem.lower()
            for p in sorted(source.glob("*.md")) if not p.name.startswith("REVIEW_")}


def asset_links(source: Path) -> dict[str, str]:
    links = {name: f"https://github.com/dbccpage/19L57G1/wiki/{slug}" for name, slug in page_map(source).items()}
    links.update({name: RAW_BASE + name for name in ("recorded_lab.json", "reading_L_mu1_rounds5.json")})
    return links


def build_search_lab(repo: Path, wiki: Path, commit: str) -> int:
    source = repo / "textbook/search_lab"
    if not source.is_dir():
        return 0
    pages = page_map(source)
    for name, slug in pages.items():
        text = (source / name).read_text(encoding="utf-8")
        for filename, target in pages.items():
            text = text.replace(f"]({filename})", f"]({target})")
        text = text.replace("](../first_steps/README.md)", "](textbook_first_steps)")
        text = text.replace("](results.html)", f"]({DESK_URL})")
        prefix = f"[Genesis Wiki](Home) · [Search lab](textbook_search_lab) · [Results desk]({DESK_URL})\n\n"
        suffix = f"\n\n---\n\nSource snapshot: [`{commit[:12]}`](https://github.com/dbccpage/19L57G1/blob/{commit}/textbook/search_lab/{name}). Teaching apparatus; `AuthorityEffect: None`.\n"
        (wiki / f"{slug}.md").write_text(prefix + text + suffix, encoding="utf-8", newline="\n")
    assets = wiki / "media/search_lab"
    assets.mkdir(parents=True, exist_ok=True)
    for name in ("recorded_lab.json", "reading_L_mu1_rounds5.json"):
        shutil.copyfile(source / name, assets / name)
    build(source, assets / "results.html", asset_links(source))
    sidebar = wiki / "_Sidebar.md"
    content = sidebar.read_text(encoding="utf-8")
    entry = "- [Search lab: demands, repairs, ties, and replay](textbook_search_lab)"
    if entry not in content:
        anchor = "- [First steps: three cards, two questions](textbook_first_steps)"
        content = content.replace(anchor, anchor + "\n" + entry, 1) if anchor in content else content.replace("## Textbook\n", "## Textbook\n\n" + entry + "\n", 1)
        sidebar.write_text(content, encoding="utf-8", newline="\n")
    home = wiki / "Home.md"
    content = home.read_text(encoding="utf-8")
    announcement = "> **Then build a witnessed distinction:** [Search lab](textbook_search_lab) follows a demand through costs, tied repairs, protected distinctions, stopping bounds, and replay.\n"
    if announcement not in content:
        anchor = content.find("> **Begin with one small example:**")
        end = content.find("\n", anchor if anchor >= 0 else 0)
        content = content[:end + 1] + announcement + content[end + 1:]
        home.write_text(content, encoding="utf-8", newline="\n")
    return len(pages)


def search_lab_errors(repo: Path, wiki: Path) -> list[str]:
    source = repo / "textbook/search_lab"
    if not source.is_dir():
        return []
    errors = [f"missing search-lab page: {slug}" for slug in page_map(source).values()
              if not (wiki / f"{slug}.md").is_file()]
    for name in ("recorded_lab.json", "reading_L_mu1_rounds5.json", "results.html"):
        asset = wiki / "media/search_lab" / name
        if not asset.is_file():
            errors.append(f"missing search-lab asset: {name}")
        elif name.endswith(".json"):
            if json.loads(asset.read_text(encoding="utf-8")) != json.loads((source / name).read_text(encoding="utf-8")):
                errors.append(f"stale search-lab record: {name}")
        elif asset.read_text(encoding="utf-8") != render(source, asset_links(source)):
            errors.append("stale search-lab results desk or unresolved reading/download links")
    if "](textbook_search_lab)" not in (wiki / "_Sidebar.md").read_text(encoding="utf-8"):
        errors.append("search lab missing from sidebar")
    return errors
