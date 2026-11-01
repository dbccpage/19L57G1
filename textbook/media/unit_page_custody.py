"""Check the full Unit text, source pin and optional-video placement."""
from io import BytesIO
from pathlib import Path
import re
import subprocess

VIDEO = '<details>\n<summary>Act video (optional)</summary>'


def unit_lesson_errors(repo: Path, wiki: Path) -> list[str]:
    # Import at call time: build/verify entry points already own these helpers.
    from build_wiki_textbook import act_for_part1, act_for_part2, first_pass_anchor, rewrite_links_for_wiki
    folders = [('textbook/units', 'u'), ('textbook/institutions/units', 'i')]
    groups = [sorted((repo / folder).glob('*.md')) for folder, _ in folders]
    maps = [{p.name: 'textbook_' + prefix + p.stem for p in files}
            for files, (_, prefix) in zip(groups, folders)]
    errors = []
    bindings = []
    for part, files in enumerate(groups):
        folder, _ = folders[part]
        for source in files:
            page = maps[part][source.name]
            path = wiki / (page + '.md')
            if not path.is_file():
                errors.append('missing Unit lesson: ' + page)
                continue
            text = path.read_text(encoding='utf-8')
            rel = folder + '/' + source.name
            pattern = (r'\[source edition `([0-9a-f]{12})`\]\('
                       r'https://github\.com/dbccpage/19L57G1/blob/([0-9a-f]{40})/'
                       + re.escape(rel) + r'\)')
            pins = re.findall(pattern, text)
            if len(pins) != 1 or pins[0][0] != pins[0][1][:12]:
                errors.append('missing or inconsistent Unit source pin: ' + page)
                continue
            pin = pins[0][1]
            raw = source.read_text(encoding='utf-8')
            expected = rewrite_links_for_wiki(raw, *maps,
                'https://github.com/dbccpage/19L57G1/blob/' + pin, bool(part), folder)
            bindings.append((page, pin + ':' + rel, raw))
            if text.count(expected) != 1:
                errors.append('stale or nonunique Unit lesson text: ' + page)
                continue
            start = text.index(expected)
            end = start + len(expected)
            video = text.find(VIDEO)
            if video < end or text.count(VIDEO) != 1:
                errors.append('Unit lesson must precede its folded video: ' + page)
            try:
                jump = first_pass_anchor(raw)
            except ValueError:
                errors.append('missing or ambiguous Unit First pass target: ' + page)
            else:
                if '](' + jump + ')' not in text[:start]:
                    errors.append('missing Unit First pass jump: ' + page)
            video_end = text.find('</details>', video)
            act, _, _ = (act_for_part2(int(source.name[:2])) if part
                         else act_for_part1(int(source.name[:2])))
            media = text[video:video_end]
            for suffix in ('.gif', '.mp4'):
                target = 'https://raw.githubusercontent.com/wiki/dbccpage/19L57G1/media/manim/' + act + suffix
                if '](' + target + ')' not in media:
                    errors.append('missing Unit Act media link: ' + page + suffix)

    # One batch reads all exact committed files, rather than trusting a URL's shape.
    if bindings:
        requests = '\n'.join(spec for _, spec, _ in bindings) + '\n'
        try:
            proc = subprocess.run(['git', '-C', str(repo), 'cat-file', '--batch'],
                                  input=requests.encode(), capture_output=True, check=True)
            stream = BytesIO(proc.stdout)
            for page, spec, raw in bindings:
                header = stream.readline().decode('utf-8').rstrip('\n')
                match = re.fullmatch(r'[0-9a-f]{40} blob (\d+)', header)
                if not match:
                    errors.append('unavailable Unit source blob: ' + page)
                    continue
                blob = stream.read(int(match[1]))
                if stream.read(1) != b'\n':
                    raise ValueError('Malformed Git batch response')
                if blob.decode('utf-8').replace('\r\n', '\n') != raw:
                    errors.append('Unit source pin differs from lesson source: ' + page)
        except (OSError, ValueError, UnicodeError, subprocess.CalledProcessError) as exc:
            errors.append('Unit source custody check failed: ' + str(exc))
    return errors
