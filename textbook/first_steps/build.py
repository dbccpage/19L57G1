"""Build a self-contained local/hosted explorer; AuthorityEffect: None."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


def build_explorer(source: Path, destination: Path, links: dict[str, str] | None = None) -> None:
    html = (source / "explorer.html").read_text(encoding="utf-8")
    css = (source / "explorer.css").read_text(encoding="utf-8")
    model = (source / "model.mjs").read_text(encoding="utf-8").replace("export function createQuestionModel", "function createQuestionModel")
    script = (source / "explorer.mjs").read_text(encoding="utf-8")
    script = re.sub(r'^import .*?;\n', '', script, flags=re.MULTILINE)
    data = json.dumps(json.loads((source / "cards.json").read_text(encoding="utf-8")), ensure_ascii=True).replace("<", "\\u003c")
    script, replacements = re.subn(
        r'  const response = await fetch\(.*?\n  const data = await response\.json\(\);',
        lambda _: "  const data = " + data + ";", script, count=1, flags=re.DOTALL)
    if replacements != 1:
        raise ValueError("Explorer's supplied-table load was not found; refusing an incomplete bundle")
    html = html.replace('<link rel="stylesheet" href="explorer.css">', f"<style>\n{css}\n</style>")
    html, replacements = re.subn(r'<script type="module" src="explorer\.mjs(?:\?[^\"]*)?"></script>',
                        lambda _: "<script>\naddEventListener('DOMContentLoaded', async () => {\n" + model + "\n" + script + "\n});\n</script>", html)
    if replacements != 1:
        raise ValueError("Explorer script element was not found; refusing an incomplete bundle")
    for name, target in (links or {}).items():
        html = html.replace(f'href="{name}"', f'href="{target}"')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("artifacts2/first_steps/explorer.html"))
    args = parser.parse_args()
    build_explorer(Path(__file__).resolve().parent, args.output)
    print(args.output.resolve())
