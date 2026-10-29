"""Mirror the static same-record teaching route; AuthorityEffect: None."""
import json
from pathlib import Path
import re
import shutil

RAW = 'https://raw.githubusercontent.com/wiki/dbccpage/19L57G1/media/identification_lab/'
SIDEBAR = '- [Same-record lab: equal profiles, distinct positions](textbook_identification_lab)'
HOME = '> **Match answers without merging things:** [Same-record lab](textbook_identification_lab) compares equal profiles, third-party changes, kept promises, bounded refusals, and later prices.\n'


def page_map(source):
    return {p.name: 'textbook_identification_lab' if p.stem == 'README' else 'textbook_identification_lab_' + p.stem.lower()
            for p in sorted(source.glob('*.md')) if not p.name.startswith('REVIEW_')}


def page_text(source, name, commit):
    body = (source / name).read_text(encoding='utf-8')
    for filename, slug in page_map(source).items():
        body = body.replace(f']({filename})', f']({slug})')
    for folder in ('first_steps', 'reasoning_lab', 'search_lab', 'map_lab'):
        body = body.replace(f'](../{folder}/README.md)', f'](textbook_{folder})')
    body = body.replace('](figures/', '](' + RAW + 'figures/')
    prefix = '[Genesis Wiki](Home) · [Same-record lab](textbook_identification_lab)\n\n'
    suffix = f'\n\n---\n\nSource snapshot: [`{commit[:12]}`](https://github.com/dbccpage/19L57G1/blob/{commit}/textbook/identification_lab/{name}). Teaching apparatus; `AuthorityEffect: None`.\n'
    return prefix + body + suffix


def build_identification_lab(repo, wiki, commit):
    source = repo / 'textbook/identification_lab'
    if not source.is_dir():
        return 0
    for name, slug in page_map(source).items():
        (wiki / (slug + '.md')).write_text(page_text(source, name, commit), encoding='utf-8', newline='\n')
    assets = wiki / 'media/identification_lab'
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / 'recorded_lab.json', assets / 'recorded_lab.json')
    shutil.copytree(source / 'figures', assets / 'figures', dirs_exist_ok=True)
    p = wiki / '_Sidebar.md'
    body = p.read_text(encoding='utf-8')
    if SIDEBAR not in body:
        anchor = '- [Boundary lab: reports, swaps, and declared prices](textbook_boundary_lab)'
        assert anchor in body
        p.write_text(body.replace(anchor, anchor + '\n' + SIDEBAR, 1), encoding='utf-8', newline='\n')
    p = wiki / 'Home.md'
    body = p.read_text(encoding='utf-8')
    if HOME not in body:
        start = body.index('> **Ask why an exchange fails:**')
        end = body.index('\n', start)
        p.write_text(body[:end+1] + HOME + body[end+1:], encoding='utf-8', newline='\n')
    return len(page_map(source))


def identification_lab_errors(repo, wiki):
    source = repo / 'textbook/identification_lab'
    if not source.is_dir():
        return []
    errors = []
    for name, slug in page_map(source).items():
        p = wiki / (slug + '.md')
        if not p.is_file():
            errors.append('missing same-record page: ' + slug)
            continue
        body = p.read_text(encoding='utf-8')
        pin = re.search(r'/blob/([0-9a-f]{40})/textbook/identification_lab/', body)
        if not pin or body != page_text(source, name, pin[1]):
            errors.append('stale same-record page: ' + slug)
    for figure in (source / 'figures').glob('*.svg'):
        published = wiki / 'media/identification_lab/figures' / figure.name
        if not published.is_file() or published.read_bytes() != figure.read_bytes():
            errors.append('stale same-record figure: ' + figure.name)
    p = wiki / 'media/identification_lab/recorded_lab.json'
    try:
        equal = json.loads(p.read_text(encoding='utf-8')) == json.loads((source / p.name).read_text(encoding='utf-8'))
    except (FileNotFoundError, ValueError):
        equal = False
    if not equal:
        errors.append('stale same-record record')
    if SIDEBAR not in (wiki / '_Sidebar.md').read_text(encoding='utf-8'):
        errors.append('same-record lab missing from sidebar')
    return errors
