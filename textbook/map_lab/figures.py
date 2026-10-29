"""Deterministic class-map lesson figures; AuthorityEffect: None."""
from html import escape
from math import hypot

SCENES = {'01_recover_blue.svg': '15_1_0_0', '02_block_triangle.svg': '15_1_1_0',
          '03_recover_pair.svg': '15_3_2_0', '04_reverse_representatives.svg': '15_1_0_1',
          '05_smaller_domain.svg': '5_1_1_0'}


def answer(value, target):
    if target == 2:
        return '(' + ('Yes' if value // 2 else 'No') + ', ' + ('Yes' if value % 2 else 'No') + ')'
    return 'Yes' if value else 'No'


def render_case(packet, row):
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="840" height="640" viewBox="0 0 840 640" role="img" aria-label="Original cards map to stored class labels; requested answers must agree within each class.">',
             '<title>Stored class labels and requested answers</title><rect width="840" height="640" fill="#fafbf7"/>',
             '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#52645d"/></marker></defs>']
    def text(x, y, value, size=24, color='#19322c'):
        parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" fill="{color}">{escape(value)}</text>')
    def positions(values, y):
        return {value: (170+660*(i+.5)/len(values), y) for i, value in enumerate(values)}
    left = positions(row['domain'], 110)
    middle = positions([g['representative'] for g in row['groups']], 300)
    outputs = list(dict.fromkeys(row['requested'][i] for i in row['domain']))
    bottom = positions(outputs, 490)
    def line(a, b, conflict=False):
        x1,y1=a; x2,y2=b
        length=hypot(x2-x1,y2-y1)
        ux,uy=(x2-x1)/length,(y2-y1)/length
        dash=' stroke-dasharray="9 6"' if conflict else ''
        color='#a43f25' if conflict else '#52645d'
        parts.append(f'<line x1="{x1+35*ux}" y1="{y1+35*uy}" x2="{x2-40*ux}" y2="{y2-40*uy}" stroke="{color}" stroke-width="3" marker-end="url(#arrow)"{dash}/>')
    for card in row['domain']:
        line(left[card], middle[row['presentation'][card]])
    for group in row['groups']:
        for value in group['requested_values']:
            line(middle[group['representative']], bottom[value], group['conflict'])
    text(85,115,'Original cards',20)
    text(85,290,'Stored class',20)
    text(85,315,'labels',20)
    text(85,480,'Requested',20)
    text(85,505,packet['target_names'][row['target']],18)
    for card,(x,y) in left.items():
        parts.append(f'<circle cx="{x}" cy="{y}" r="31" fill="white" stroke="#19322c" stroke-width="2"/>')
        text(x,y+11,packet['cards'][card],32)
    for label,(x,y) in middle.items():
        parts.append(f'<circle cx="{x}" cy="{y}" r="33" fill="#dcebdc" stroke="#19322c" stroke-width="2"/>')
        text(x,y+11,packet['cards'][label],32)
    for value,(x,y) in bottom.items():
        parts.append(f'<rect x="{x-70}" y="{y-29}" width="140" height="58" rx="8" fill="white" stroke="#19322c" stroke-width="2"/>')
        text(x,y+8,answer(value,row['target']),24 if row['target']==2 else 28)
    if not row['domain']:
        text(420,570,'No cards, classes, or observed outputs.')
    else:
        text(420,570,'Consistent class lookup.' if row['recoverable'] else 'Dashed forks mark conflicting requested values.',22)
    text(420,610,'Supplied finite maps; arrows are assignments.',20)
    return '\n'.join(parts+['</svg>'])+'\n'


def render_figures(packet):
    return {name: render_case(packet,packet['cases'][key]) for name,key in SCENES.items()}
