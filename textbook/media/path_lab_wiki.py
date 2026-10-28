"""Mirror the path and boundary route; AuthorityEffect: None."""
from pathlib import Path
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from textbook.path_lab.build_results import build, render  # noqa: E402

RAW = "https://raw.githubusercontent.com/wiki/dbccpage/19L57G1/media/path_lab/"
DESK = "https://htmlpreview.github.io/?" + RAW + "results.html"


def page_map(source):
    return {p.name: "textbook_path_lab" if p.stem == "README" else "textbook_path_lab_" + p.stem.lower()
            for p in sorted(source.glob("*.md")) if not p.name.startswith("REVIEW_")}


def links(source):
    return {**{name: "https://github.com/dbccpage/19L57G1/wiki/" + slug for name, slug in page_map(source).items()},
            "recorded_lab.json": RAW + "recorded_lab.json"}


def build_path_lab(repo, wiki, commit):
    source = repo / "textbook/path_lab"
    if not source.is_dir():
        return 0
    for name, slug in page_map(source).items():
        text = (source / name).read_text(encoding="utf-8")
        for filename, target in page_map(source).items():
            text = text.replace(f"]({filename})", f"]({target})")
        for folder in ("reasoning_lab", "change_lab"):
            text = text.replace(f"](../{folder}/README.md)", f"](textbook_{folder})")
        text = text.replace("](results.html)", f"]({DESK})")
        text = text.replace("](figures/", "](" + RAW + "figures/")
        prefix = f"[Genesis Wiki](Home) · [Path lab](textbook_path_lab) · [Path desk]({DESK})\n\n"
        suffix = f"\n\n---\n\nSource snapshot: [`{commit[:12]}`](https://github.com/dbccpage/19L57G1/blob/{commit}/textbook/path_lab/{name}). Teaching apparatus; `AuthorityEffect: None`.\n"
        (wiki / (slug + ".md")).write_text(prefix + text + suffix, encoding="utf-8", newline="\n")
    assets = wiki / "media/path_lab"
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / "recorded_lab.json", assets / "recorded_lab.json")
    shutil.copytree(source / "figures", assets / "figures", dirs_exist_ok=True)
    build(source, assets / "results.html", links(source))
    sidebar = wiki / "_Sidebar.md"
    text = sidebar.read_text(encoding="utf-8")
    entry = "- [Path lab: walks, faces, and signed boundaries](textbook_path_lab)"
    if entry not in text:
        anchor = "- [Change lab: retention, protection, and execution](textbook_change_lab)"
        assert anchor in text, "Change-lab navigation anchor is missing"
        sidebar.write_text(text.replace(anchor, anchor + "\n" + entry, 1), encoding="utf-8", newline="\n")
    home = wiki / "Home.md"
    text = home.read_text(encoding="utf-8")
    line = "> **Trace connections and boundaries:** [Path lab](textbook_path_lab) introduces walks, signed endpoint counts, guarded faces, and shared-edge cancellation on four points.\n"
    if line not in text:
        anchor = text.find("> **Separate a proposal from its execution:**")
        assert anchor >= 0, "Change-lab home anchor is missing"
        end = text.index("\n", anchor)
        home.write_text(text[:end + 1] + line + text[end + 1:], encoding="utf-8", newline="\n")
    return len(page_map(source))


def path_lab_errors(repo, wiki):
    source = repo / "textbook/path_lab"
    if not source.is_dir():
        return []
    errors = ["missing path-lab page: " + slug for slug in page_map(source).values()
              if not (wiki / (slug + ".md")).is_file()]
    for figure in (source / "figures").glob("*.svg"):
        published = wiki / "media/path_lab/figures" / figure.name
        if not published.is_file() or published.read_bytes() != figure.read_bytes():
            errors.append("stale or missing path-lab figure: " + figure.name)
    for name in ("recorded_lab.json", "results.html"):
        path = wiki / "media/path_lab" / name
        if not path.is_file():
            errors.append("missing path-lab asset: " + name)
        elif name.endswith(".json"):
            if json.loads(path.read_text(encoding="utf-8")) != json.loads((source / name).read_text(encoding="utf-8")):
                errors.append("stale path-lab record")
        elif path.read_text(encoding="utf-8") != render(source, links(source)):
            errors.append("stale path-lab desk or links")
    if "](textbook_path_lab)" not in (wiki / "_Sidebar.md").read_text(encoding="utf-8"):
        errors.append("reasoning lab missing from sidebar")
    return errors
