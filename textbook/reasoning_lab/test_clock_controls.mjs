// Actual handlers in a minimal DOM; no browser-layout or learner evidence.
import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';
const html=fs.readFileSync(new URL('clocks.template.html',import.meta.url),'utf8');
const packet=JSON.parse(fs.readFileSync(new URL('clocks.json',import.meta.url),'utf8'));
const elements=new Map();let focused=null;
class Element{
 constructor(tag,text=''){this.tag=tag;this.textContent=text;this.children=[];this.events={};this.value='';this.hidden=false;}
 append(...children){this.children.push(...children);if(this.tag==='select'&&this.children.length===children.length)this.value=children[0].value;}
 replaceChildren(...children){this.children=children;this.textContent='';}
 addEventListener(event,fn){this.events[event]=fn;}focus(){focused=this;}
 text(){return this.textContent+this.children.map(c=>c.text()).join(' ');}
}
for(const m of html.matchAll(/<([a-z]+)[^>]* id="((?:clock|future)-[^"]+)"[^>]*>/g)){assert(!elements.has(m[2]));const e=new Element(m[1]);e.hidden=m[0].includes(' hidden');elements.set(m[2],e);}
const el=id=>{assert(elements.has(id),id);return elements.get(id);};const node=(tag,text)=>new Element(tag,text),table=(headers,rows)=>node('table',headers.join(' ')+' '+rows.flat().join(' '));
const start=html.indexOf('// Clock controls:'),end=html.indexOf('// End clock controls.');assert(start>=0&&end>start);
vm.runInNewContext(html.slice(start,end),{packet,el,node,table});
for(const p of ['clock','future']){el(p+'-reveal').events.click();assert(el(p+'-outcome').hidden);assert.equal(focused,el(p+'-prediction'));}
let clockChecks=0,futureChecks=0;
for(const [key,row]of Object.entries(packet.cases)){
 const [rule,start,span]=key.split('_');el('clock-rule').value=rule;el('clock-start').value=start;el('clock-span').value=span;el('clock-rule').events.change();assert.equal(el('clock-prediction').value,'');assert(el('clock-outcome').hidden);
 for(const answer of packet.rate_answers){el('clock-prediction').value=answer;el('clock-reveal').events.click();assert(!el('clock-outcome').hidden);const text=el('clock-outcome').text();assert.equal(text.includes('Your prediction matches'),answer===row.answer);assert(text.includes('Fast change = '+row.fast_change));if(row.answer==='refuse')assert(text.includes('No ratio is supplied'));el('clock-prediction').events.change();assert(el('clock-outcome').hidden);clockChecks++;}
 for(const id of ['clock-start','clock-span']){el('clock-prediction').value='2';el(id).events.change();assert.equal(el('clock-prediction').value,'');assert(el('clock-outcome').hidden);}
}
for(const h of packet.horizons){el('future-horizon').value=String(h);el('future-horizon').events.change();assert.equal(el('future-prediction').value,'');assert(el('future-outcome').hidden);if(h===0)assert(el('future-given').text().includes('No samples'));
 for(const answer of ['yes','no']){el('future-prediction').value=answer;el('future-reveal').events.click();assert.equal(el('future-outcome').text().includes('Your prediction matches'),answer==='no');assert(el('future-outcome').text().includes('A reaches zero'));el('future-prediction').events.change();assert(el('future-outcome').hidden);futureChecks++;}
}
assert(!html.includes('fetch(')&&!html.includes('localStorage'));
console.log(JSON.stringify({clock_predictions:clockChecks,countdown_predictions:futureChecks,gates:true,resets:true,zero_intervals:true,wrong_feedback:true,browser_layout:false}));
