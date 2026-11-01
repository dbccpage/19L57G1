"""Bundle the claim desk; AuthorityEffect: None."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from textbook.search_lab.build_results import build, render  # noqa: E402,F401

if __name__ == "__main__":
    source = Path(__file__).resolve().parent
    build(source, source / "results.html")
    build(source, source / 'protocols.html',template_name='protocols.template.html',packet_name='protocols.json')
    build(source, source / 'calibration.html',template_name='calibration.template.html',packet_name='calibration.json')
    build(source, source / 'clocks.html',template_name='clocks.template.html',packet_name='clocks.json')
    build(source, source / 'composites.html',template_name='composites.template.html',packet_name='composites.json')
