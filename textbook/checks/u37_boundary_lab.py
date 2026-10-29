"""Recompute the boundary/swap packet and figures; AuthorityEffect: None."""
from pathlib import Path
import shutil
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from textbook.boundary_lab.run_lab import check_recorded  # noqa: E402
from textbook.boundary_lab.build_results import render  # noqa: E402

if __name__ == '__main__':
    print(check_recorded())
    source = Path(__file__).resolve().parents[1] / 'boundary_lab'
    assert (source / 'results.html').read_text(encoding='utf-8') == render(source)
    node = shutil.which('node')
    if node is None:
        raise RuntimeError('Node is required to check the swap desk')
    subprocess.run([node, str(source / 'test_desk.cjs')], check=True)
