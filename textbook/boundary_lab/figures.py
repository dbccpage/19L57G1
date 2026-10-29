"""Small source-backed lesson figures; AuthorityEffect: None."""
from html import escape


def text(x, y, value, size=20, color='#15314b'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(str(value))}</text>'


def figure(title, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" '
            f'viewBox="0 0 900 {height}" role="img" aria-label="{escape(title)}">'
            f'<title>{escape(title)}</title><rect width="900" height="{height}" rx="14" fill="#f4f7fa"/>'
            '<g font-family="Segoe UI, sans-serif">' + text(28, 42, title, 25) + body + '</g></svg>\n')


def render_figures(packet):
    body = ''
    for i, reading in enumerate(('U', 'O')):
        row = packet['boundary_cases'][reading + '_']
        x = 28 + i * 442
        body += f'<rect x="{x}" y="72" width="414" height="205" rx="10" fill="white" stroke="#bdd0df"/>'
        body += text(x+18, 105, reading + (' — unnamed' if reading == 'U' else ' — named'))
        body += text(x+28, 153, 'side 0') + text(x+248, 153, 'side 1')
        body += f'<path d="M{x+207} 122 V190" stroke="#335f7e" stroke-width="3"/>'
        body += text(x+28, 190, 'no marks') + text(x+248, 190, 'no marks')
        body += text(x+18, 228, 'Equal side profiles: ' + ('yes' if row['equal_profiles'] else 'no'))
        body += text(x+18, 257, 'Holding judgments: ' + str(row['holding_judgments']))
    body += text(28, 318, 'U: no visible side names. O: admitted names near and far.', 20)
    body += text(28, 351, 'The labels 0 and 1 let us describe the model; they do not name U sides internally.', 18)
    body += text(28, 382, 'This division is an admitted seed exception, not the Path lab boundary operation.', 18)
    first = figure('An empty placement list does not remove the admitted division', 408, body)

    body = text(35, 88, 'Report: (answer for x,y; answer for y,x)') + text(555, 88, 'Swap preserves it?')
    for i, d in enumerate(((False, False), (True, True), (False, True), (True, False))):
        y = 134 + i * 58
        body += text(50, y, '(' + ', '.join('yes' if v else 'no' for v in d) + ')', 24)
        body += text(575, y, 'YES' if d[0] == d[1] else 'NO', 24,
                     '#166454' if d[0] == d[1] else '#a83f31')
    body += text(35, 378, 'For a family of reports, every selected row must pass.', 21)
    body += text(35, 414, 'No selected reports: none can block the swap.', 21)
    second = figure('Equal answers survive an exchange; unequal answers do not', 442, body)

    body = ''
    cases = [('aa_10_arity', 'Same labels; swaps permitted; labels forgotten'),
             ('ab_11_arity', 'Different labels; swaps permitted; labels kept'),
             ('aa_00_arity', 'Same labels; only identity permitted; labels forgotten')]
    for i, (key, label) in enumerate(cases):
        row = packet['transfer_cases'][key]; y = 82 + i * 144
        body += f'<rect x="28" y="{y}" width="844" height="124" rx="10" fill="white" stroke="#bdd0df"/>'
        body += text(45, y+31, label, 20)
        body += text(45, y+66, 'Permitted: ' + ('identity + swap' if row['permutations_permitted'] else 'identity only'))
        kept = 'identity + swap' if len(row['automorphisms']) == 2 else 'identity only'
        body += text(45, y+101, 'Also preserves the key: ' + kept)
    body += text(28, 548, 'The last two rows retain the same renaming, but for different reasons.', 21)
    body += text(28, 582, 'One changes the stored label information; the other changes the permitted family.', 19)
    third = figure('Keep the permission filter separate from the key-preservation test', 612, body)

    body = text(35, 90, 'Candidate') + text(430, 90, 'Cost') + text(535, 90, 'Automorphisms') + text(745, 90, 'Separates?')
    names = [('000', 'Base'), ('010', 'Keep identical labels'), ('001', 'Add one identical mark'),
             ('100', 'Permit only identity')]
    for i, (key, label) in enumerate(names):
        row = packet['control_menu'][key]; y = 141 + i * 59
        body += text(35, y, label) + text(446, y, row['mu1'])
        body += text(575, y, len(row['automorphisms']))
        body += text(762, y, 'yes' if row['satisfies'] else 'no')
    body += text(35, 413, 'Minimum: 1 changed coordinate, at the declared two-mark case.', 21)
    body += text(35, 449, 'Exclude identity-only solutions: none of these eligible candidates satisfies.', 19)
    body += text(35, 483, 'This is a finite menu and a declared price, not a universal cost of orientation.', 19)
    fourth = figure('The side-free control: base and the three single changes', 512, body)
    return {'00_empty_division.svg': first, '01_answer_pairs.svg': second,
            '02_two_filters.svg': third, '03_fixed_menu.svg': fourth}
