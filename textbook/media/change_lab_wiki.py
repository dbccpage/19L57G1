"""Publish the passage teaching route; AuthorityEffect: None."""
from pathlib import Path
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from textbook.change_lab.build_results import build, render  # noqa: E402

RAW = "https://raw.githubusercontent.com/wiki/dbccpage/19L57G1/media/change_lab/"
DESK = "https://htmlpreview.github.io/?" + RAW + "results.html"


def page_map(source):
    return {p.name: "textbook_change_lab" if p.stem == "README" else "textbook_change_lab_" + p.stem.lower()
            for p in sorted(source.glob("*.md")) if not p.name.startswith("REVIEW_")}


def links(source):
    return {**{name: "https://github.com/dbccpage/19L57G1/wiki/" + slug for name, slug in page_map(source).items()},
            "recorded_lab.json": RAW + "recorded_lab.json"}


def build_change_lab(repo, wiki, commit):
    source = repo / "textbook/change_lab"
    if not source.is_dir():
        return 0
    for name, slug in page_map(source).items():
        text = (source / name).read_text(encoding="utf-8")
        for filename, target in page_map(source).items():
            text = text.replace(f"]({filename})", f"]({target})")
        for folder, target in (("first_steps", "textbook_first_steps"), ("search_lab", "textbook_search_lab"), ("path_lab", "textbook_path_lab")):
            text = text.replace(f"](../{folder}/README.md)", f"]({target})")
        text = text.replace("](results.html)", f"]({DESK})")
        for filename, target in (("reading_formal_statements.md", "textbook_reading_formal"),
                                 ("learning_path.md", "textbook_learning_path")):
            text = text.replace(f"](../{filename})", f"]({target})")
        prefix = f"[Genesis Wiki](Home) · [Change lab](textbook_change_lab) · [Passage desk]({DESK})\n\n"
        suffix = f"\n\n---\n\nSource snapshot: [`{commit[:12]}`](https://github.com/dbccpage/19L57G1/blob/{commit}/textbook/change_lab/{name}). Teaching apparatus; `AuthorityEffect: None`.\n"
        (wiki / (slug + ".md")).write_text(prefix + text + suffix, encoding="utf-8", newline="\n")
    assets = wiki / "media/change_lab"
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / "recorded_lab.json", assets / "recorded_lab.json")
    build(source, assets / "results.html", links(source))
    sidebar = wiki / "_Sidebar.md"
    text = sidebar.read_text(encoding="utf-8")
    entry = "- [Change lab: retention, protection, and execution](textbook_change_lab)"
    if entry not in text:
        anchor = "- [Search lab: demands, repairs, ties, and replay](textbook_search_lab)"
        text = text.replace(anchor, anchor + "\n" + entry, 1) if anchor in text else text.replace("## Textbook\n", "## Textbook\n\n" + entry + "\n", 1)
        sidebar.write_text(text, encoding="utf-8", newline="\n")
    home = wiki / "Home.md"
    text = home.read_text(encoding="utf-8")
    line = "> **Separate a proposal from its execution:** [Change lab](textbook_change_lab) follows retention, protection, observation, budget, permission, refusal, and halt on three entries.\n"
    if line not in text:
        anchor = text.find("> **Then build a witnessed distinction:**")
        end = text.find("\n", anchor if anchor >= 0 else 0)
        home.write_text(text[:end + 1] + line + text[end + 1:], encoding="utf-8", newline="\n")
    return len(page_map(source))


def change_lab_errors(repo, wiki):
    source = repo / "textbook/change_lab"
    if not source.is_dir():
        return []
    errors = ["missing change-lab page: " + slug for slug in page_map(source).values()
              if not (wiki / (slug + ".md")).is_file()]
    for name in ("recorded_lab.json", "results.html"):
        path = wiki / "media/change_lab" / name
        if not path.is_file():
            errors.append("missing change-lab asset: " + name)
        elif name.endswith(".json"):
            if json.loads(path.read_text(encoding="utf-8")) != json.loads((source / name).read_text(encoding="utf-8")):
                errors.append("stale change-lab record")
        elif path.read_text(encoding="utf-8") != render(source, links(source)):
            errors.append("stale change-lab desk or links")
    if "](textbook_change_lab)" not in (wiki / "_Sidebar.md").read_text(encoding="utf-8"):
        errors.append("change lab missing from sidebar")
    return errors
