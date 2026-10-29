"""Small source-backed SVGs; AuthorityEffect: None."""
from html import escape


def race_svg(row):
    log = row['log']
    height = 125 + 42*len(log)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="820" height="{height}" viewBox="0 0 820 {height}" role="img" aria-label="Per-round growth and declared service accounting">',
             f'<rect width="820" height="{height}" fill="#fafbf7"/>']
    def text(x,y,s,size=20):
        parts.append(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" fill="#19322c">{escape(str(s))}</text>')
    text(20,30,f"{row['commitment']}: {row['rounds']} rounds, service budget {row['discharge_rate']}",22)
    for x,label in zip((20,140,300,460,620),('Round','New item','Generated','Discharged','Waiting')):
        text(x,70,label)
    for i,r in enumerate(log):
        for x,key in zip((20,140,300,460,620),('round','admitted','generated','discharged','backlog')):
            text(x,110+42*i,r[key]+1 if key=='round' else r[key])
    text(20,height-12,'Declared removals are not constructed observation repairs.',18)
    return '\n'.join(parts+['</svg>'])+'\n'


def growth_svg(row):
    lines = [('Held items', ', '.join(map(str,row['data'])) or 'none'),
             ('Views', ' ; '.join('{'+','.join(map(str,v))+'}' for v in row['views']) or 'none'),
             ('Commitment', row['commitment']),
             ('Old demands', ', '.join(f'{a}/{b}' for a,b in row['before']) or 'none'),
             ('New item', str(row['new'])),
             ('New demands', ', '.join(f'{a}/{b}' for a,b in row['new_demands']) or 'none'),
             ('All demands after', ', '.join(f'{a}/{b}' for a,b in row['after']) or 'none')]
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="820" height="400" viewBox="0 0 820 400" role="img" aria-label="A represented growth step with old and new demands shown separately">', '<rect width="820" height="400" fill="#fafbf7"/>']
    for i,(label,value) in enumerate(lines):
        y=35+45*i
        parts.append(f'<text x="20" y="{y}" font-family="sans-serif" font-size="20" fill="#19322c">{escape(label)}</text>')
        parts.append(f'<text x="240" y="{y}" font-family="sans-serif" font-size="20" fill="#19322c">{escape(value)}</text>')
    parts.append('<text x="20" y="375" font-family="sans-serif" font-size="18" fill="#19322c">The same views remain; growth adds no observation or repair.</text>')
    return '\n'.join(parts+['</svg>'])+'\n'


def render_figures(packet):
    return {'01_viewless_growth.svg':growth_svg(packet['growth_cases']['7_0_total']),
            '02_quiet_reopens.svg':growth_svg(packet['growth_cases']['15_3_total']),
            '03_bounded_clears.svg':race_svg(packet['races']['bounded_8_1']),
            '04_total_backlog.svg':race_svg(packet['races']['total_8_1'])}
