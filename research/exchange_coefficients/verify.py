"""Replay the supplied examples and audit their pinned Lean correspondence.

This tree is a local receipt, outside the sealed derivation. Dependencies are
staged from the pinned Git blobs into this tree only. AuthorityEffect: None.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PIN = 'cea346d7f3603fd8da374947e76c9b3cd426d122'
ALLOWED = {'propext', 'Quot.sound'}
LOCAL_MODULES = ['ExchangeCoefficients', 'ClaimExample']


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def stage_sources():
    manifest = json.loads((HERE / 'SOURCE_MANIFEST.json').read_text())
    assert manifest['source_commit'] == PIN
    assert subprocess.run(['git', 'merge-base', '--is-ancestor', PIN, 'HEAD'], cwd=REPO).returncode == 0
    modules = manifest['modules']
    assert modules and set(manifest['roots']) <= modules.keys()
    seen = set()

    def visit(name):
        if name in seen or name == 'Init':
            return
        entry = modules[name]
        rel = entry['path']
        assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
        blob = git('show', f'{PIN}:{rel}')
        assert digest(blob) == entry['sha256'], ('Pinned digest mismatch', rel)
        assert git('show', f'HEAD:{rel}') == blob, ('Source changed at HEAD', rel)
        assert subprocess.run(['git', 'diff', '--quiet', 'HEAD', '--', rel], cwd=REPO).returncode == 0
        destination = HERE / 'lean/pinned' / (name.replace('.', '/') + '.lean')
        assert destination.resolve().is_relative_to((HERE / 'lean/pinned').resolve())
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(blob)
        seen.add(name)
        for dep in re.findall(r'^import\s+(\S+)', blob.decode(), re.M):
            visit(dep)

    for root in manifest['roots']:
        visit(root)
    assert seen == set(modules), 'Manifest must be exactly the declared import closure'
    staged = {p.relative_to(HERE / 'lean/pinned').as_posix() for p in (HERE / 'lean/pinned').rglob('*.lean')}
    assert staged == {n.replace('.', '/') + '.lean' for n in modules}, 'Unexpected staged source'
    return len(seen)


def declared_theorems(source):
    # Lean names may end in apostrophes; `\w+` alone would stop before
    # them and misname a primed theorem.  Repaired 2026-09-18.
    return re.findall(r"^theorem\s+([\w']+)", source, re.M)


def parse_axioms(text, expected):
    reports = {}
    # `.+?` and not `[^']+`: a primed theorem name ends in a quote
    # character, and the character-class pattern cannot capture it --
    # the recorded primed-names parser defect.  `.` stops at a line end,
    # so one capture never spans two reports.  Repaired 2026-09-18.
    pattern = r"'(.+?)' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)"
    for match in re.finditer(pattern, text):
        name = match[1]
        assert name not in reports, ('Duplicate report', name)
        reports[name] = [s.strip() for s in (match[2] or '').split(',') if s.strip()]
    assert set(reports) == set(expected), ('Report census mismatch', sorted(set(reports) ^ set(expected)))
    assert all(set(values) <= ALLOWED for values in reports.values()), reports
    return reports


def lean_checks(lake):
    expected = json.loads((HERE / 'AXIOM_DECLARATIONS.json').read_text())
    assert len(expected) == len(set(expected))
    own = []
    forbidden = [r'\bsorry\b', r'\badmit\b', r'^\s*axiom\s', r'\bunsafe\b', r'\bpartial\b']
    for module in LOCAL_MODULES:
        source = (HERE / f'lean/{module}.lean').read_text(encoding='utf-8')
        assert not any(re.search(p, source, re.M) for p in forbidden)
        own += [module + '.' + n for n in declared_theorems(source)]
    assert set(own) == {n for n in expected if n.split('.')[0] in LOCAL_MODULES}
    build = subprocess.run([lake, 'build'], cwd=HERE / 'lean', capture_output=True, text=True,
                           encoding='utf-8', errors='replace')
    (HERE / 'evidence/lean_build.log').write_text(build.stdout + build.stderr, encoding='utf-8')
    if build.returncode:
        raise RuntimeError((build.stdout + build.stderr)[-6000:])
    audit = subprocess.run([lake, 'env', 'lean', 'ExamplesAudit.lean'], cwd=HERE / 'lean',
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
    assert audit.returncode == 0, audit.stdout + audit.stderr
    axioms = parse_axioms(audit.stdout, expected)
    (HERE / 'evidence/lean_axioms.txt').write_text(audit.stdout, encoding='utf-8')
    return axioms


def main():
    if sys.flags.optimize:
        raise RuntimeError('Run without -O: the example checks use assertions')
    parser = argparse.ArgumentParser()
    parser.add_argument('--lake', default=shutil.which('lake'))
    parser.add_argument('--python-only', action='store_true')
    args = parser.parse_args()
    (HERE / 'evidence').mkdir(exist_ok=True)
    count = stage_sources()
    namespace = runpy.run_path(str(HERE / 'test_examples.py'))
    tests = []
    for name, value in namespace.items():
        if name.startswith('test_') and callable(value):
            value()
            tests.append(name)
    assert tests, 'Empty test discovery'
    import examples
    import bipartite_index
    import claim_example
    catalogue = bipartite_index.catalog()
    for file, value in [('examples.json', examples.report()),
                        ('bipartite_summary.json', {k: v for k, v in catalogue.items() if k != 'rows'}),
                        ('claims.json', claim_example.examples())]:
        (HERE / 'evidence' / file).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    (HERE / 'evidence/bipartite_catalog.jsonl').write_text(
        ''.join(json.dumps(row, sort_keys=True, separators=(',', ':')) + '\n'
                for row in catalogue['rows']), encoding='utf-8')
    result = {'status': 'PASS', 'source_commit': PIN, 'source_modules': count,
              'python_tests': tests, 'python_version': sys.version.split()[0], 'lean': 'NOT_RUN'}
    if not args.python_only:
        if not args.lake:
            raise RuntimeError('Lake not found; supply --lake PATH')
        result['axioms'] = lean_checks(args.lake)
        result['lean'] = 'PASS'
    # Bind inputs and deterministic outputs; generated logs are excluded from
    # the input inventory. These hashes attest bytes, not semantic truth.
    paths = [p for p in HERE.rglob('*') if p.is_file() and
             not any(s in {'.lake', 'pinned', 'evidence', '__pycache__', '.pytest_cache', '.mypy_cache'}
                     for s in p.relative_to(HERE).parts)]
    result['input_sha256'] = {p.relative_to(HERE).as_posix(): digest(p.read_bytes()) for p in sorted(paths)}
    result['result_sha256'] = {n: digest((HERE / 'evidence' / n).read_bytes())
                               for n in ['examples.json', 'bipartite_summary.json',
                                         'bipartite_catalog.jsonl', 'claims.json']}
    (HERE / 'evidence/verification.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps({'source_modules': count, 'python_tests': len(tests), 'lean': result['lean'], 'status': 'PASS'}))


if __name__ == '__main__':
    main()
