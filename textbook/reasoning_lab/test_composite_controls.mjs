// Actual handlers in a minimal DOM; no browser-layout or learner evidence.
import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';
const html=fs.readFileSync(new URL('composites.template.html',import.meta.url),'utf8');
const packet=JSON.parse(fs.readFileSync(new URL('composites.json',import.meta.url),'utf8'));
const elements=new Map();let focused=null;
class Element{
 constructor(tag,text=''){this.tag=tag;this.textContent=text;this.children=[];this.events={};this.value='';this.hidden=false;}
 append(...children){this.children.push(...children);if(this.tag==='select'&&this.children.length===children.length)this.value=children[0].value;}
 replaceChildren(...children){this.children=children;this.textContent='';}
 addEventListener(event,fn){this.events[event]=fn;}focus(){focused=this;}
 text(){return this.textContent+this.children.map(c=>c.text()).join(' ');}
}

for(const m of html.matchAll(/<([a-z]+)[^>]* id="((?:share|graph)-[^"]+)"[^>]*>/g)){assert(!elements.has(m[2]));const e=new Element(m[1]);e.hidden=m[0].includes(' hidden');elements.set(m[2],e);}
const el=id=>{assert(elements.has(id),id);return elements.get(id);};const node=(tag,text)=>new Element(tag,text),table=(headers,rows)=>node('table',headers.join(' ')+' '+rows.flat().join(' '));
const start=html.indexOf('// Composite controls:'),end=html.indexOf('// End composite controls.');assert(start>=0&&end>start);
vm.runInNewContext(html.slice(start,end),{packet,el,node,table});
for(const p of ['share','graph']){el(p+'-reveal').events.click();assert(el(p+'-outcome').hidden);assert.equal(focused,el(p+'-prediction'));}
let shareChecks=0,graphChecks=0;
for(const [key,row]of Object.entries(packet.cases)){
 const [a,b,c]=key.split('_');el('share-preparation').value=a;el('share-procedure').value=b;el('share-readout').value=c;el('share-procedure').events.change();assert.equal(el('share-prediction').value,'');assert(el('share-outcome').hidden);
 for(const answer of packet.share_answers){el('share-prediction').value=answer;el('share-reveal').events.click();assert(!el('share-outcome').hidden);const text=el('share-outcome').text();assert.equal(text.includes('Your prediction matches'),answer===row.answer);assert(text.includes('Outcome-share distance = '+row.answer));if(row.answer==='0'&&row.marks_changed)assert(text.includes('hidden changes'));el('share-prediction').events.change();assert(el('share-outcome').hidden);shareChecks++;}
 for(const id of ['share-preparation','share-procedure','share-readout']){el('share-prediction').value='1';el(id).events.change();assert.equal(el('share-prediction').value,'');assert(el('share-outcome').hidden);}
}
for(const [key,row]of Object.entries(packet.graphs)){
 const [a,b]=key.split('_');el('graph-menu').value=a;el('graph-pair').value=b;el('graph-menu').events.change();
 for(const answer of packet.distance_answers){el('graph-prediction').value=answer;el('graph-reveal').events.click();assert.equal(el('graph-outcome').text().includes('Your prediction matches'),answer===row.answer);assert(el('graph-outcome').text().includes('Operations executed to draw this graph: 0'));el('graph-prediction').events.change();assert(el('graph-outcome').hidden);graphChecks++;}
 for(const id of ['graph-menu','graph-pair']){el('graph-prediction').value='1';el(id).events.change();assert.equal(el('graph-prediction').value,'');assert(el('graph-outcome').hidden);}
}
assert(!html.includes('fetch(')&&!html.includes('localStorage'));
console.log(JSON.stringify({share_predictions:shareChecks,graph_predictions:graphChecks,gates:true,resets:true,wrong_feedback:true,browser_layout:false}));
