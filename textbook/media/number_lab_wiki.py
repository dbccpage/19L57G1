"""Mirror numerical prerequisites and selected readout lessons."""
import json
import re
import shutil

RAW = 'https://raw.githubusercontent.com/wiki/dbccpage/19L57G1/media/number_lab/'
SIDEBAR = '- [Number lab: counts, shares, and combined readings](textbook_number_lab)'
HOME = '> **Build the arithmetic before the readout:** [Number lab](textbook_number_lab) teaches counts, shares, zero, signed steps, squares, and coordinate sums before the selected finite bridge examples.\n'


def page_map(source):
    return {p.name: 'textbook_number_lab' if p.stem == 'README' else 'textbook_number_lab_'+p.stem.lower()
            for p in sorted(source.glob('*.md')) if not p.name.startswith('REVIEW_')}


def page_text(source, name, commit):
    body = (source/name).read_text(encoding='utf-8')
    for filename, slug in page_map(source).items():
        body = body.replace(f']({filename})', f']({slug})')
    for folder in ('first_steps', 'reasoning_lab', 'map_lab'):
        body = body.replace(f'](../{folder}/README.md)', f'](textbook_{folder})')
        for sibling in (source.parent/folder).glob('*.md'):
            if sibling.name!='README.md':
                body=body.replace(f'](../{folder}/{sibling.name})',f'](textbook_{folder}_{sibling.stem.lower()})')
    body=body.replace('](../learning_path.md)','](textbook_learning_path)')
    body = body.replace('](../units/64_a_profile_without_division.md)',
                        '](textbook_u64_a_profile_without_division)')
    body = body.replace('](figures/', ']('+RAW+'figures/')
    prefix = '[Genesis Wiki](Home) · [Number lab](textbook_number_lab)\n\n'
    suffix = f'\n\n---\n\nSource snapshot: [`{commit[:12]}`](https://github.com/dbccpage/19L57G1/blob/{commit}/textbook/number_lab/{name}). Teaching apparatus; `AuthorityEffect: None`.\n'
    return prefix+body+suffix


def build_number_lab(repo, wiki, commit):
    source = repo/'textbook/number_lab'
    if not source.is_dir():
        return 0
    for name, slug in page_map(source).items():
        (wiki/(slug+'.md')).write_text(page_text(source, name, commit), encoding='utf-8', newline='\n')
    assets = wiki/'media/number_lab'
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source/'recorded_lab.json', assets/'recorded_lab.json')
    shutil.copytree(source/'figures', assets/'figures', dirs_exist_ok=True)
    p = wiki/'_Sidebar.md'; body = p.read_text(encoding='utf-8')
    if SIDEBAR not in body:
        anchor = '- [Same-record lab: equal profiles, distinct positions](textbook_identification_lab)'
        assert anchor in body
        p.write_text(body.replace(anchor, anchor+'\n'+SIDEBAR, 1), encoding='utf-8', newline='\n')
    p = wiki/'Home.md'; body = p.read_text(encoding='utf-8')
    if HOME not in body:
        start = body.index('> **Match answers without merging things:**')
        end = body.index('\n', start)
        p.write_text(body[:end+1]+HOME+body[end+1:], encoding='utf-8', newline='\n')
    return len(page_map(source))


def number_lab_errors(repo, wiki):
    source = repo/'textbook/number_lab'
    if not source.is_dir():
        return []
    errors = []
    for name, slug in page_map(source).items():
        p = wiki/(slug+'.md')
        if not p.is_file():
            errors.append('missing number-lab page: '+slug)
            continue
        body = p.read_text(encoding='utf-8')
        pin = re.search(r'/blob/([0-9a-f]{40})/textbook/number_lab/', body)
        if not pin or body != page_text(source, name, pin[1]):
            errors.append('stale number-lab page: '+slug)
    for figure in (source/'figures').glob('*.svg'):
        p = wiki/'media/number_lab/figures'/figure.name
        if not p.is_file() or p.read_bytes() != figure.read_bytes():
            errors.append('stale number-lab figure: '+figure.name)
    p = wiki/'media/number_lab/recorded_lab.json'
    try:
        equal = json.loads(p.read_text(encoding='utf-8')) == json.loads((source/p.name).read_text(encoding='utf-8'))
    except (FileNotFoundError, ValueError):
        equal = False
    if not equal:
        errors.append('stale number-lab record')
    if SIDEBAR not in (wiki/'_Sidebar.md').read_text(encoding='utf-8'):
        errors.append('number lab missing from sidebar')
    return errors
