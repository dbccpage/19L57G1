// Execute the actual evidence event handlers in a minimal DOM fixture.
// This is a unit check, not browser rendering or accessibility evidence.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const html = fs.readFileSync(new URL('results.template.html', import.meta.url), 'utf8');
const packet = JSON.parse(fs.readFileSync(new URL('recorded_lab.json', import.meta.url), 'utf8'));
const elements = new Map();
let focused = null;
class Element {
  constructor(tag, text = '') {
    this.tag = tag; this.textContent = text; this.children = [];
    this.value = ''; this.hidden = false; this.events = {};
  }
  append(...children) {
    this.children.push(...children);
    if (this.tag === 'select' && this.children.length === children.length) this.value = children[0].value;
  }
  replaceChildren(...children) { this.children = children; this.textContent = ''; }
  addEventListener(event, fn) { this.events[event] = fn; }
  focus() { focused = this; }
  text() { return this.textContent + this.children.map(c => c.text()).join(' '); }
}
for (const match of html.matchAll(/<([a-z]+)\b[^>]*\bid="(evidence-[^"]+)"[^>]*>/g)) {
  assert(!elements.has(match[2]), 'duplicate evidence id');
  const element = new Element(match[1]); element.hidden = /\bhidden\b/.test(match[0]);
  elements.set(match[2], element);
}
const el = id => { assert(elements.has(id), `missing ${id}; fixture ids: ${[...elements.keys()].join(',')}`); return elements.get(id); };
const node = (tag, text) => new Element(tag, text);
const table = (headers, rows) => new Element('table', JSON.stringify({headers, rows}));
const start = html.indexOf('const evidence=packet.evidence;');
const end = html.indexOf('</script>', start);
assert(start >= 0 && end > start);
vm.runInNewContext(html.slice(start, end), {packet, el, node, table, updateDomain() {}});
assert.equal(el('evidence-case').children.length, 12);
assert(el('evidence-outcome').hidden);
el('evidence-reveal').events.click();
assert(el('evidence-outcome').hidden);
assert.equal(focused, el('evidence-prediction'));
assert.match(el('evidence-notice').text(), /Choose a status/);
for (const row of packet.evidence.records) {
  el('evidence-case').value = row.id;
  el('evidence-case').events.change();
  assert.equal(el('evidence-prediction').value, '');
  assert(el('evidence-outcome').hidden);
  assert(el('evidence-raw').text().includes(row.id));
  el('evidence-prediction').value = packet.evidence.outcomes[row.id];
  el('evidence-reveal').events.click();
  assert(!el('evidence-outcome').hidden);
  assert.match(el('evidence-outcome').text(), /Your prediction matches/);
  el('evidence-prediction').events.change();
  assert(el('evidence-outcome').hidden);
}
el('evidence-case').value = 'new-N'; el('evidence-case').events.change();
el('evidence-prediction').value = 'compatible'; el('evidence-reveal').events.click();
assert.match(el('evidence-outcome').text(), /different status/);
el('evidence-case').value = 'repeat-N'; el('evidence-case').events.change();
assert(el('evidence-outcome').hidden);
assert.equal(el('evidence-prediction').value, '');
assert(el('evidence-repeats').text().includes('new-N'));
assert(el('evidence-repeats').text().includes('repeat-N'));
assert.match(html, /Supplied fictional logs. No measurements were taken./);
console.log(JSON.stringify({cases: 12, prediction_gate: true, stale_answer_reset: true,
  incorrect_feedback: true, repeat_rows_retained: true, browser_rendering_checked: false}));
