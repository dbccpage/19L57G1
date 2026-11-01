// Actual handlers in a minimal DOM; no browser-layout or learner evidence.
import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';
const html=fs.readFileSync(new URL('valuations.template.html',import.meta.url),'utf8');
const packet=JSON.parse(fs.readFileSync(new URL('valuations.json',import.meta.url),'utf8'));
const elements=new Map();let focused=null;
class Element{
 constructor(tag,text=''){this.tag=tag;this.textContent=text;this.children=[];this.events={};this.value='';this.hidden=false;}
 append(...children){this.children.push(...children);if(this.tag==='select'&&this.children.length===children.length)this.value=children[0].value;}
 replaceChildren(...children){this.children=children;this.textContent='';}
 addEventListener(event,fn){this.events[event]=fn;}focus(){focused=this;}
 text(){return this.textContent+this.children.map(c=>c.text()).join(' ');}
}


for(const m of html.matchAll(/<([a-z]+)[^>]* id="((?:value|branch)-[^"]+)"[^>]*>/g)){assert(!elements.has(m[2]));const e=new Element(m[1]);e.hidden=m[0].includes(' hidden');elements.set(m[2],e);}
const el=id=>{assert(elements.has(id),id);return elements.get(id);};const node=(tag,text)=>new Element(tag,text),table=(headers,rows)=>node('table',headers.join(' ')+' '+rows.flat().join(' '));
const start=html.indexOf('// Valuation controls:'),end=html.indexOf('// End valuation controls.');assert(start>=0&&end>start);
vm.runInNewContext(html.slice(start,end),{packet,el,node,table});
for(const p of ['value','branch']){el(p+'-reveal').events.click();assert(el(p+'-outcome').hidden);assert.equal(focused,el(p+'-prediction'));}
let valueChecks=0,branchChecks=0;
for(const [key,row]of Object.entries(packet.cases)){
 const [a,b]=key.split('_');el('value-preparation').value=a;el('value-response').value=b;el('value-preparation').events.change();
 for(const answer of packet.answers){el('value-prediction').value=answer;el('value-reveal').events.click();assert(!el('value-outcome').hidden);const text=el('value-outcome').text();assert.equal(text.includes('Your prediction matches'),answer===row.answer);assert(text.includes('Overall Yes chance = '+row.answer));el('value-prediction').events.change();assert(el('value-outcome').hidden);valueChecks++;}
 for(const id of ['value-preparation','value-response']){el('value-prediction').value='1';el(id).events.change();assert.equal(el('value-prediction').value,'');assert(el('value-outcome').hidden);}
}
for(const [key,row]of Object.entries(packet.branches)){
 const [a,b,c]=key.split('_');el('branch-joint').value=a;el('branch-partition').value=b;el('branch-response').value=c;el('branch-joint').events.change();
 for(const answer of packet.answers){el('branch-prediction').value=answer;el('branch-reveal').events.click();const text=el('branch-outcome').text();assert.equal(text.includes('Your prediction matches'),answer===row.answer);assert(text.includes('B Yes after summing both branches = '+row.answer));if(row.partition===2)assert(text.includes('undefined'));el('branch-prediction').events.change();assert(el('branch-outcome').hidden);branchChecks++;}
 for(const id of ['branch-joint','branch-partition','branch-response']){el('branch-prediction').value='1';el(id).events.change();assert.equal(el('branch-prediction').value,'');assert(el('branch-outcome').hidden);}
}
assert(!html.includes('fetch(')&&!html.includes('localStorage'));
console.log(JSON.stringify({pairing_predictions:valueChecks,branch_predictions:branchChecks,gates:true,resets:true,wrong_feedback:true,browser_layout:false}));
