"""Mirror the boundary/swap route; AuthorityEffect: None."""
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from textbook.boundary_lab.build_results import build, render  # noqa: E402

RAW = 'https://raw.githubusercontent.com/wiki/dbccpage/19L57G1/media/boundary_lab/'
DESK = 'https://htmlpreview.github.io/?' + RAW + 'results.html'


def page_map(source):
    return {p.name: 'textbook_boundary_lab' if p.stem == 'README' else 'textbook_boundary_lab_' + p.stem.lower()
            for p in sorted(source.glob('*.md')) if not p.name.startswith('REVIEW_')}


def links(source):
    return {**{name: 'https://github.com/dbccpage/19L57G1/wiki/' + slug
               for name, slug in page_map(source).items()},
            'recorded_lab.json': RAW + 'recorded_lab.json'}


def build_boundary_lab(repo, wiki, commit):
    source = repo / 'textbook/boundary_lab'
    if not source.is_dir():
        return 0
    for name, slug in page_map(source).items():
        text = (source / name).read_text(encoding='utf-8')
        for filename, target in page_map(source).items():
            text = text.replace(f']({filename})', f']({target})')
        for folder in ('reasoning_lab', 'map_lab'):
            text = text.replace(f'](../{folder}/README.md)', f'](textbook_{folder})')
        text = text.replace('](../units/37_an_inventory_is_not_a_derivation.md)',
                            '](textbook_u37_an_inventory_is_not_a_derivation)')
        text = text.replace('](results.html)', f']({DESK})')
        text = text.replace('](figures/', '](' + RAW + 'figures/')
        prefix = f'[Genesis Wiki](Home) · [Boundary lab](textbook_boundary_lab) · [Swap desk]({DESK})\n\n'
        suffix = f'\n\n---\n\nSource snapshot: [`{commit[:12]}`](https://github.com/dbccpage/19L57G1/blob/{commit}/textbook/boundary_lab/{name}). Teaching apparatus; `AuthorityEffect: None`.\n'
        (wiki / (slug + '.md')).write_text(prefix + text + suffix, encoding='utf-8', newline='\n')
    assets = wiki / 'media/boundary_lab'
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / 'recorded_lab.json', assets / 'recorded_lab.json')
    shutil.copytree(source / 'figures', assets / 'figures', dirs_exist_ok=True)
    build(source, assets / 'results.html', links(source))
    sidebar = wiki / '_Sidebar.md'
    text = sidebar.read_text(encoding='utf-8')
    entry = '- [Boundary lab: reports, swaps, and declared prices](textbook_boundary_lab)'
    if entry not in text:
        anchor = '- [Growth lab: commitments, demands, and service](textbook_growth_lab)'
        assert anchor in text
        sidebar.write_text(text.replace(anchor, anchor + '\n' + entry, 1), encoding='utf-8', newline='\n')
    home = wiki / 'Home.md'
    text = home.read_text(encoding='utf-8')
    entry = '> **Ask why an exchange fails:** [Boundary lab](textbook_boundary_lab) separates repeated labels, report witnesses, permitted swaps, and prices in a fixed menu.\n'
    if entry not in text:
        anchor = text.find('> **See why a settled task can reopen:**')
        assert anchor >= 0
        end = text.index('\n', anchor)
        home.write_text(text[:end+1] + entry + text[end+1:], encoding='utf-8', newline='\n')
    return len(page_map(source))


def boundary_lab_errors(repo, wiki):
    source = repo / 'textbook/boundary_lab'
    if not source.is_dir():
        return []
    errors = ['missing boundary-lab page: ' + slug for slug in page_map(source).values()
              if not (wiki / (slug + '.md')).is_file()]
    for figure in (source / 'figures').glob('*.svg'):
        published = wiki / 'media/boundary_lab/figures' / figure.name
        if not published.is_file() or published.read_bytes() != figure.read_bytes():
            errors.append('stale boundary-lab figure: ' + figure.name)
    assets = wiki / 'media/boundary_lab'
    p = assets / 'recorded_lab.json'
    if not p.is_file() or json.loads(p.read_text(encoding='utf-8')) != json.loads((source / p.name).read_text(encoding='utf-8')):
        errors.append('stale boundary-lab record')
    p = assets / 'results.html'
    if not p.is_file() or p.read_text(encoding='utf-8') != render(source, links(source)):
        errors.append('stale boundary-lab desk or links')
    if '](textbook_boundary_lab)' not in (wiki / '_Sidebar.md').read_text(encoding='utf-8'):
        errors.append('boundary lab missing from sidebar')
    return errors
