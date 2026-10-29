"""Bundle the standalone swap desk; AuthorityEffect: None."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from textbook.search_lab.build_results import render as render_packet  # noqa: E402


def render(source, links=None):
    html = render_packet(source, links)
    if html.count('__DESK_SCRIPT__') != 1:
        raise ValueError('Expected one swap-desk script marker')
    return html.replace('__DESK_SCRIPT__', (source / 'desk.js').read_text(encoding='utf-8'))


def build(source, output, links=None):
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(source, links), encoding='utf-8', newline='\n')


if __name__ == '__main__':
    source = Path(__file__).resolve().parent
    build(source, source / 'results.html')
