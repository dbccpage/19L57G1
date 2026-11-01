// Exact event handlers in a minimal DOM. This supplies no browser-layout evidence.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const html=fs.readFileSync(new URL('protocols.template.html',import.meta.url),'utf8');
const packet=JSON.parse(fs.readFileSync(new URL('protocols.json',import.meta.url),'utf8'));
const elements=new Map();let focused=null;
class Element{
 constructor(tag,text=''){this.tag=tag;this.textContent=text;this.children=[];this.events={};this.value='';this.hidden=false;}
 append(...children){this.children.push(...children);if(this.tag==='select'&&this.children.length===children.length)this.value=children[0].value;}
 replaceChildren(...children){this.children=children;this.textContent='';}
 addEventListener(event,fn){this.events[event]=fn;}
 focus(){focused=this;}
 text(){return this.textContent+this.children.map(c=>c.text()).join(' ');}
}
for(const m of html.matchAll(/<([a-z]+)[^>]* id="((?:protocol|order)-[^"]+)"[^>]*>/g)){
 assert(!elements.has(m[2]));const e=new Element(m[1]);e.hidden=m[0].includes(' hidden');elements.set(m[2],e);
}
const el=id=>{assert(elements.has(id),`missing ${id}`);return elements.get(id);};
const node=(tag,text)=>new Element(tag,text),table=(headers,rows)=>new Element('table',JSON.stringify({headers,rows}));
el('protocol-record').value='r1';
const start=html.indexOf('// Protocol controls:'),end=html.indexOf('// End protocol controls.');assert(start>=0&&end>start);
vm.runInNewContext(html.slice(start,end),{packet,el,node,table,labels:{l1:'Target A',l2:'Target B',m:'Message',r1:'Record A',r2:'Record B',dist:'Counter'}});
for(const prefix of ['protocol','order']){el(prefix+'-reveal').events.click();assert(el(prefix+'-outcome').hidden);assert.equal(focused,el(prefix+'-prediction'));}
function setup(parts){el('protocol-input').value=parts[0];el('protocol-probe').value=parts[1];el('protocol-input').events.change();assert(el('protocol-outcome').hidden&&el('order-outcome').hidden);assert.equal(el('protocol-prediction').value,'');assert.equal(el('order-prediction').value,'');}
let recordChecks=0,orderChecks=0;
for(const [key,row]of Object.entries(packet.histories))for(const record of ['r1','r2']){
 const parts=key.split('_');setup(parts);el('protocol-sequence').value=parts[2];el('protocol-record').value=record;el('protocol-record').events.change();el('protocol-prediction').value=String(row.end[record]);el('protocol-reveal').events.click();assert.match(el('protocol-outcome').text(),/Your prediction matches/);assert(el('protocol-outcome').text().includes('ends at '+row.end[record]));el('protocol-prediction').events.change();assert(el('protocol-outcome').hidden);recordChecks++;
}
for(const [key,row]of Object.entries(packet.orders)){
 const parts=key.split('_');setup(parts);el('order-case').value=parts[2];el('order-case').events.change();el('order-prediction').value=row.commutes?'yes':'no';el('order-reveal').events.click();assert.match(el('order-outcome').text(),/Your prediction matches/);el('order-prediction').events.change();assert(el('order-outcome').hidden);orderChecks++;
}
el('order-prediction').value='no';el('order-reveal').events.click();assert.match(el('order-outcome').text(),/different result/);
el('protocol-prediction').value='2';el('protocol-reveal').events.click();assert.match(el('protocol-outcome').text(),/different mark/);
for(const probe of ['0','1','2']){el('protocol-probe').value=probe;el('protocol-probe').events.change();assert(el('protocol-ensemble').text().includes('zero physical observations'));assert(el('protocol-ensemble').text().includes('4 of 4'));}
assert(!html.includes('fetch('));
console.log(JSON.stringify({record_predictions:recordChecks,order_predictions:orderChecks,gates:true,shared_reset:true,wrong_feedback:true,browser_layout:false}));
