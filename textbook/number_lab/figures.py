"""Numerical worked figures generated from the checked packet."""
from html import escape


def text(x, y, value, size=21, color='#15314b'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(str(value))}</text>'


def figure(title, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" '
            f'viewBox="0 0 900 {height}" role="img" aria-label="{escape(title)}">'
            f'<title>{escape(title)}</title><rect width="900" height="{height}" rx="14" fill="#f4f7fa"/>'
            '<g font-family="Segoe UI, sans-serif">'+text(28, 42, title, 25)+body+'</g></svg>\n')


def pair(xs):
    return '('+', '.join(str(x).replace('-', '−') for x in xs)+')'


def render_figures(packet):
    shares = packet['shares_example']
    body = ''
    for k, key in enumerate(('before', 'after')):
        values = shares[key]; y = 100+120*k
        body += text(28, y, pair(values)+'; total '+str(shares['totals'][k]), 23)
        for i in range(sum(values)):
            color = '#276b9e' if i < values[0] else '#d2dde7'
            body += f'<rect x="{28+37*i}" y="{y+19}" width="29" height="29" rx="4" fill="{color}"/>'
    body += text(464, 106, 'Left position cross check', 22)
    body += text(464, 151, '2 × 10 = 4 × 5 = 20', 24)
    body += text(464, 222, 'Right position cross check', 22)
    body += text(464, 267, '3 × 10 = 6 × 5 = 30', 24)
    body += text(28, 342, 'Blue counts the left tray. Both left shares are 2/5 = 4/10.', 22)
    body += text(28, 385, 'Equal proportions can forget a doubled total. Both totals here are positive.', 19)
    first = figure('Double every count; keep the same shares', 416, body)

    body = text(28, 95, 'Signed inputs')+text(290, 95, 'Separate squares')+text(589, 95, 'Add, then square')
    for i, xs in enumerate(([1, 1], [1, -1])):
        row = next(r for r in packet['signed_cases'] if r['inputs'] == xs)
        y = 158+80*i
        body += text(48, y, pair(xs), 28)+text(340, y, pair(row['weights']), 28)
        body += text(688, y, row['readout'], 30)
    body += text(28, 323, 'Square first, then add: 1 + 1 = 2 in both rows.', 22)
    body += text(28, 367, 'Add first, then square: the signs can change the reading.', 22)
    body += text(28, 410, 'The readout operation is supplied. The separate weights do not choose it.', 19)
    second = figure('The same weights can hide a sign that matters later', 441, body)

    body = text(28, 94, 'First input is (1, 0) in every row. Weight of (x, y) = x² + y².', 22)
    headings = [(28, 'Second input'), (254, 'Separate weights'), (509, 'Input sum'), (736, 'Reading')]
    for x, label in headings:
        body += text(x, 148, label, 21)
    for i, row in enumerate(packet['coordinate_instance']):
        y = 208+66*i
        body += text(58, y, pair(row['inputs'][1]), 25)
        body += text(311, y, pair(row['weights']), 25)
        body += text(538, y, pair(row['sum']), 25)+text(772, y, row['readout'], 28)
    body += text(28, 397, 'Right + right gives 4. Right + up gives 2. Right + left gives 0.', 22)
    body += text(28, 439, 'These are squared scores, not distances or measured probabilities.', 20)
    third = figure('Add coordinates first, then apply the weight rule', 470, body)

    body = ''
    for k, n in enumerate((4, 5)):
        row = packet['loops'][n-1]; x = 28+442*k
        body += f'<rect x="{x}" y="78" width="414" height="250" rx="10" fill="white" stroke="#bdd0df"/>'
        body += text(x+18, 115, str(n)+' positions', 24)
        for i, group in enumerate(row['groups']):
            body += text(x+29, 160+45*i, '{'+', '.join(map(str, group))+'}', 25)
        body += text(x+206, 206, 'At most '+str(row['maximum_distinct']), 22)
        body += text(x+206, 244, 'readings', 22)
    body += text(28, 378, 'Every pair in one group must share its reading under the reversal rule.', 21)
    body += text(28, 420, 'Dropping that rule can allow a different answer at every position.', 21)
    body += text(28, 461, 'A group-label reading attains the bound; a chosen physical formula needs more.', 19)
    fourth = figure('Reversal groups limit the distinct readings', 492, body)

    row = packet['domain_cases'][-1]
    body = text(28, 100, 'Recorded input')+text(360, 100, 'Required reading')+text(652, 100, 'Preparation')
    for i, case in enumerate(packet['coordinate_instance']):
        y = 158+64*i
        body += text(81, y, pair(case['weights']), 27)+text(439, y, case['readout'], 28)
        body += text(708, y, 'ABC'[i], 25)
    body += text(28, 384, 'Only weights: '+str(row['information_before'])+' signature class.', 22)
    body += text(28, 425, 'Weights plus reading: '+str(row['information_after'])+' signature classes.', 22)
    body += text(28, 467, 'No lookup seeing only (1, 1) can return all three required answers.', 21)
    body += text(28, 506, 'The allowed carrier here is A, B, C. The class count is not a bit count.', 19)
    fifth = figure('A conflicting output blocks recovery from the weights', 537, body)
    return {'00_shares.svg': first, '01_signed_readings.svg': second,
            '02_coordinate_readings.svg': third, '03_reversal_classes.svg': fourth,
            '04_information_gap.svg': fifth}
