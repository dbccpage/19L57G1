"""Bundle the recorded search desk; AuthorityEffect: None."""
from pathlib import Path
import argparse
import json


def render(source: Path, links: dict[str, str] | None = None) -> str:
    html = (source / "results.template.html").read_text(encoding="utf-8")
    if html.count("__LAB_PACKET__") != 1:
        raise ValueError("Expected one data marker; refusing an incomplete results desk")
    data = json.loads((source / "recorded_lab.json").read_text(encoding="utf-8"))
    literal = json.dumps(data, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c")
    html = html.replace("__LAB_PACKET__", literal)
    for name, target in (links or {}).items():
        html = html.replace(f'href="{name}"', f'href="{target}"')
    return html


def build(source: Path, output: Path, links: dict[str, str] | None = None) -> None:
    html = render(source, links)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "results.html")
    args = parser.parse_args()
    build(Path(__file__).resolve().parent, args.output)
    print(args.output.resolve())
