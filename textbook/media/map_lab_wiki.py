"""Mirror the class and lookup route; AuthorityEffect: None."""
from pathlib import Path
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from textbook.map_lab.build_results import build, render  # noqa: E402

RAW = "https://raw.githubusercontent.com/wiki/dbccpage/19L57G1/media/map_lab/"
DESK = "https://htmlpreview.github.io/?" + RAW + "results.html"


def page_map(source):
    return {p.name: "textbook_map_lab" if p.stem == "README" else "textbook_map_lab_" + p.stem.lower()
            for p in sorted(source.glob("*.md")) if not p.name.startswith("REVIEW_")}


def links(source):
    return {**{name: "https://github.com/dbccpage/19L57G1/wiki/" + slug for name, slug in page_map(source).items()},
            "recorded_lab.json": RAW + "recorded_lab.json"}


def build_map_lab(repo, wiki, commit):
    source = repo / "textbook/map_lab"
    if not source.is_dir():
        return 0
    for name, slug in page_map(source).items():
        text = (source / name).read_text(encoding="utf-8")
        for filename, target in page_map(source).items():
            text = text.replace(f"]({filename})", f"]({target})")
        for folder in ("first_steps", "reasoning_lab", "path_lab"):
            text = text.replace(f"](../{folder}/README.md)", f"](textbook_{folder})")
        text = text.replace("](results.html)", f"]({DESK})")
        text = text.replace("](figures/", "](" + RAW + "figures/")
        prefix = f"[Genesis Wiki](Home) · [Map lab](textbook_map_lab) · [Map desk]({DESK})\n\n"
        suffix = f"\n\n---\n\nSource snapshot: [`{commit[:12]}`](https://github.com/dbccpage/19L57G1/blob/{commit}/textbook/map_lab/{name}). Teaching apparatus; `AuthorityEffect: None`.\n"
        (wiki / (slug + ".md")).write_text(prefix + text + suffix, encoding="utf-8", newline="\n")
    assets = wiki / "media/map_lab"
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / "recorded_lab.json", assets / "recorded_lab.json")
    shutil.copytree(source / "figures", assets / "figures", dirs_exist_ok=True)
    build(source, assets / "results.html", links(source))
    sidebar = wiki / "_Sidebar.md"
    text = sidebar.read_text(encoding="utf-8")
    entry = "- [Map lab: classes, representatives, and recovery](textbook_map_lab)"
    if entry not in text:
        anchor = "- [Path lab: walks, faces, and signed boundaries](textbook_path_lab)"
        assert anchor in text, "Path-lab navigation anchor is missing"
        sidebar.write_text(text.replace(anchor, anchor + "\n" + entry, 1), encoding="utf-8", newline="\n")
    home = wiki / "Home.md"
    text = home.read_text(encoding="utf-8")
    line = "> **Follow an answer through a merge:** [Map lab](textbook_map_lab) introduces functions, equivalence classes, representative labels, paired questions, and recovery on a declared domain.\n"
    if line not in text:
        anchor = text.find("> **Trace connections and boundaries:**")
        assert anchor >= 0, "Path-lab home anchor is missing"
        end = text.index("\n", anchor)
        home.write_text(text[:end + 1] + line + text[end + 1:], encoding="utf-8", newline="\n")
    return len(page_map(source))


def map_lab_errors(repo, wiki):
    source = repo / "textbook/map_lab"
    if not source.is_dir():
        return []
    errors = ["missing map-lab page: " + slug for slug in page_map(source).values()
              if not (wiki / (slug + ".md")).is_file()]
    for figure in (source / "figures").glob("*.svg"):
        published = wiki / "media/map_lab/figures" / figure.name
        if not published.is_file() or published.read_bytes() != figure.read_bytes():
            errors.append("stale or missing map-lab figure: " + figure.name)
    for name in ("recorded_lab.json", "results.html"):
        path = wiki / "media/map_lab" / name
        if not path.is_file():
            errors.append("missing map-lab asset: " + name)
        elif name.endswith(".json"):
            if json.loads(path.read_text(encoding="utf-8")) != json.loads((source / name).read_text(encoding="utf-8")):
                errors.append("stale map-lab record")
        elif path.read_text(encoding="utf-8") != render(source, links(source)):
            errors.append("stale map-lab desk or links")
    if "](textbook_map_lab)" not in (wiki / "_Sidebar.md").read_text(encoding="utf-8"):
        errors.append("map lab missing from sidebar")
    return errors
