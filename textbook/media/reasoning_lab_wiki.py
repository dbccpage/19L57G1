"""Mirror the reasoning prerequisite route; AuthorityEffect: None."""
from pathlib import Path
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from textbook.reasoning_lab.build_results import build, render  # noqa: E402

RAW = "https://raw.githubusercontent.com/wiki/dbccpage/19L57G1/media/reasoning_lab/"
DESK = "https://htmlpreview.github.io/?" + RAW + "results.html"
PROTOCOL_DESK = 'https://htmlpreview.github.io/?'+RAW+'protocols.html'
CALIBRATION_DESK = 'https://htmlpreview.github.io/?'+RAW+'calibration.html'
CLOCK_DESK = 'https://htmlpreview.github.io/?'+RAW+'clocks.html'
COMPOSITE_DESK = 'https://htmlpreview.github.io/?'+RAW+'composites.html'


def page_map(source):
    return {p.name: "textbook_reasoning_lab" if p.stem == "README" else "textbook_reasoning_lab_" + p.stem.lower()
            for p in sorted(source.glob("*.md")) if not p.name.startswith("REVIEW_")}


def links(source):
    return {**{name: "https://github.com/dbccpage/19L57G1/wiki/" + slug for name, slug in page_map(source).items()},
            "recorded_lab.json": RAW + "recorded_lab.json",'protocols.json':RAW+'protocols.json',
            'calibration.json':RAW+'calibration.json','clocks.json':RAW+'clocks.json','composites.json':RAW+'composites.json'}


def build_reasoning_lab(repo, wiki, commit):
    source = repo / "textbook/reasoning_lab"
    if not source.is_dir():
        return 0
    for name, slug in page_map(source).items():
        text = (source / name).read_text(encoding="utf-8")
        for filename, target in page_map(source).items():
            text = text.replace(f"]({filename})", f"]({target})")
        for folder in ("first_steps", "search_lab", "number_lab", "map_lab"):
            text = text.replace(f"](../{folder}/README.md)", f"](textbook_{folder})")
            for sibling in (repo/'textbook'/folder).glob('*.md'):
                if sibling.name!='README.md':
                    text=text.replace(f"](../{folder}/{sibling.name})",f"](textbook_{folder}_{sibling.stem.lower()})")
        text = text.replace("](results.html)", f"]({DESK})")
        text = text.replace("](protocols.html)",f"]({PROTOCOL_DESK})")
        text = text.replace("](calibration.html)",f"]({CALIBRATION_DESK})")
        text = text.replace("](clocks.html)",f"]({CLOCK_DESK})")
        text = text.replace("](composites.html)",f"]({COMPOSITE_DESK})")
        prefix = f"[Genesis Wiki](Home) · [Reasoning lab](textbook_reasoning_lab) · [Claim desk]({DESK})\n\n"
        suffix = f"\n\n---\n\nSource snapshot: [`{commit[:12]}`](https://github.com/dbccpage/19L57G1/blob/{commit}/textbook/reasoning_lab/{name}). Teaching apparatus; `AuthorityEffect: None`.\n"
        (wiki / (slug + ".md")).write_text(prefix + text + suffix, encoding="utf-8", newline="\n")
    assets = wiki / "media/reasoning_lab"
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / "recorded_lab.json", assets / "recorded_lab.json")
    build(source, assets / "results.html", links(source))
    shutil.copyfile(source/'protocols.json',assets/'protocols.json')
    build(source,assets/'protocols.html',links(source),template_name='protocols.template.html',packet_name='protocols.json')
    shutil.copyfile(source/'calibration.json',assets/'calibration.json')
    build(source,assets/'calibration.html',links(source),template_name='calibration.template.html',packet_name='calibration.json')
    shutil.copyfile(source/'clocks.json',assets/'clocks.json')
    build(source,assets/'clocks.html',links(source),template_name='clocks.template.html',packet_name='clocks.json')
    shutil.copyfile(source/'composites.json',assets/'composites.json')
    build(source,assets/'composites.html',links(source),template_name='composites.template.html',packet_name='composites.json')
    sidebar = wiki / "_Sidebar.md"
    text = sidebar.read_text(encoding="utf-8")
    entry = "- [Reasoning lab: rules, witnesses, and conditions](textbook_reasoning_lab)"
    if entry not in text:
        anchor = "- [First steps: three cards, two questions](textbook_first_steps)"
        assert anchor in text, "First-steps navigation anchor is missing"
        sidebar.write_text(text.replace(anchor, anchor + "\n" + entry, 1), encoding="utf-8", newline="\n")
    home = wiki / "Home.md"
    text = home.read_text(encoding="utf-8")
    line = "> **Read a claim precisely:** [Reasoning lab](textbook_reasoning_lab) teaches rules, functions, if-then claims, witnesses, counterexamples, hypotheses, and evidence on the same three cards.\n"
    if line not in text:
        anchor = text.find("> **Begin with one small example:**")
        assert anchor >= 0, "First-steps home anchor is missing"
        end = text.index("\n", anchor)
        home.write_text(text[:end + 1] + line + text[end + 1:], encoding="utf-8", newline="\n")
    return len(page_map(source))


def reasoning_lab_errors(repo, wiki):
    source = repo / "textbook/reasoning_lab"
    if not source.is_dir():
        return []
    errors = ["missing reasoning-lab page: " + slug for slug in page_map(source).values()
              if not (wiki / (slug + ".md")).is_file()]
    for name in ("recorded_lab.json", "results.html",'protocols.json','protocols.html','calibration.json','calibration.html','clocks.json','clocks.html','composites.json','composites.html'):
        path = wiki / "media/reasoning_lab" / name
        if not path.is_file():
            errors.append("missing reasoning-lab asset: " + name)
        elif name.endswith(".json"):
            if json.loads(path.read_text(encoding="utf-8")) != json.loads((source / name).read_text(encoding="utf-8")):
                errors.append("stale reasoning-lab record")
        else:
            expected = (render(source,links(source),
                        template_name=name.replace('.html','.template.html'),
                        packet_name=name.replace('.html','.json'))
                        if name in ('protocols.html','calibration.html','clocks.html','composites.html')
                        else render(source,links(source)))
            if path.read_text(encoding="utf-8") != expected:
                errors.append("stale reasoning-lab desk or links")
    if "](textbook_reasoning_lab)" not in (wiki / "_Sidebar.md").read_text(encoding="utf-8"):
        errors.append("reasoning lab missing from sidebar")
    return errors
