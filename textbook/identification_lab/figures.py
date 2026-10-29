"""Recorded table figures; teaching apparatus, AuthorityEffect: None."""
from html import escape


def text(x, y, value, size=20, color='#15314b'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(str(value))}</text>'


def figure(title, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" '
            f'viewBox="0 0 900 {height}" role="img" aria-label="{escape(title)}">'
            f'<title>{escape(title)}</title><rect width="900" height="{height}" rx="14" fill="#f4f7fa"/>'
            '<g font-family="Segoe UI, sans-serif">' + text(28, 42, title, 25) + body + '</g></svg>\n')


def word(value):
    return 'yes' if value else '—'


def small_table(x, y, heading, table):
    result = f'<rect x="{x}" y="{y}" width="268" height="222" rx="10" fill="white" stroke="#bdd0df"/>'
    result += text(x+16, y+33, heading, 21)
    result += text(x+110, y+69, 'P') + text(x+195, y+69, 'Q')
    for i, row in enumerate(table['answers']):
        yy = y+110+43*i
        result += text(x+25, yy, 'ABC'[i], 23)
        result += text(x+110, yy, word(row[0])) + text(x+195, yy, word(row[1]))
    return result


def render_figures(packet):
    unary = packet['roots']['g00']['released']
    paths = packet['paths']
    body = small_table(28, 75, 'Before', unary)
    body += small_table(316, 75, 'Add Q(B)', paths['focused']['first']['after'])
    body += small_table(604, 75, 'Rule Q on every card', paths['uniform']['first']['after'])
    body += text(28, 341, 'Both replies cost one item. Only the rule changes C.', 22)
    body += text(28, 381, 'C still differs from A and B on P. All three positions remain.', 21)
    body += text(28, 419, 'yes = derivable here; — = not derivable here', 19)
    first = figure('Two one-item replies, two different effects on C', 447, body)

    before = packet['roots']['g05']['released']
    focused = next(r for r in packet['probes']['g05_release_02_mu1']['responses']
                   if not r['diagnostics']['contains_rule'])
    body = text(28, 85, 'Questions')
    for i in range(7):
        body += text(205+92*i, 85, 'q'+str(i), 19)
    for k, (label, table) in enumerate((('Before', before), ('Add B → A', focused['after']))):
        y = 125+k*180
        body += text(28, y, label, 22)
        for i, row in enumerate(table['answers']):
            yy = y+38+39*i
            body += text(72, yy, 'ABC'[i], 21)
            for j, value in enumerate(row):
                body += text(205+92*j, yy, word(value), 19)
    body += text(28, 493, 'q0: _ → _      q1: _ → A      q2: _ → B      q3: _ → C', 20)
    body += text(28, 530, 'q4: A → _      q5: B → _      q6: C → _', 20)
    body += text(28, 568, 'Fill all holes with the same tested card. A and C match after the addition.', 19)
    body += text(28, 603, 'B changes at q1, yet still differs from A and C. A dash is not physical falsity.', 19)
    second = figure('Read all seven questions, including both arrow places', 632, body)

    table = packet['larger_reply']['after']
    body = text(28, 91, '1. New one-place form S', 22)
    body += text(28, 133, '2. Uniform rule for arrows', 22)
    body += text(28, 175, '3. Single instance S(C)', 22)
    body += text(505, 91, 'Card') + text(590, 91, 'Every arrow test') + text(807, 91, 'S')
    for i, row in enumerate(table['answers']):
        y = 137+53*i
        body += text(521, y, 'ABC'[i], 23)
        assert all(row[:7])
        body += text(644, y, 'yes') + text(808, y, word(row[7]))
    body += text(28, 308, 'A and B match; C stays distinguishable from both.', 22)
    body += text(28, 351, 'Valid reply: yes. Within the two-item search: no.', 22)
    body += text(28, 392, 'The three data positions remain. This is an exhibited reply outside the bound.', 19)
    third = figure('Keep both old promises with three additions', 422, body)

    body = text(28, 88, 'First reply') + text(390, 88, 'First items')
    body += text(552, 88, 'Next items') + text(729, 88, 'Total items')
    for i, (key, label) in enumerate((('focused', 'Q(B)'), ('uniform', 'Uniform rule Q'))):
        row = paths[key]; y = 158+i*90
        body += text(35, y, label, 23) + text(430, y, row['first']['items'], 25)
        body += text(594, y, row['next']['minimum'], 25)
        body += text(777, y, row['least_total_items_along_this_choice'], 25)
    body += text(28, 327, 'First match A and B; then keep that requirement and match A and C.', 21)
    body += text(28, 370, 'Both paths use two reply rounds. Their item totals differ.', 21)
    body += text(28, 410, 'These are selected continuations, not a general rule about future cost.', 19)
    fourth = figure('A tie at this step can change the next price', 440, body)
    return {'00_two_replies.svg': first, '01_binary_questions.svg': second,
            '02_three_additions.svg': third, '03_next_step.svg': fourth}
