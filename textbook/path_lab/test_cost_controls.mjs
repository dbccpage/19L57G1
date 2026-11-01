// Exact new event handlers in a minimal DOM; no browser-layout assertion.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const html=fs.readFileSync(new URL('results.template.html',import.meta.url),'utf8');
const packet=JSON.parse(fs.readFileSync(new URL('recorded_lab.json',import.meta.url),'utf8'));
const elements=new Map();let focused=null;
class Element{
 constructor(tag,text=''){this.tag=tag;this.textContent=text;this.children=[];this.events={};this.value='';this.hidden=false;}
 append(...children){this.children.push(...children);if(this.tag==='select'&&this.children.length===children.length)this.value=children[0].value;}
 replaceChildren(...children){this.children=children;this.textContent='';}
 addEventListener(event,fn){this.events[event]=fn;}
 focus(){focused=this;}
 text(){return this.textContent+this.children.map(c=>c.text()).join(' ');}
}
for(const m of html.matchAll(/<([a-z]+)[^>]* id="((?:cost|square)-[^"]+)"[^>]*>/g)){
 assert(!elements.has(m[2]));const e=new Element(m[1]);e.hidden=m[0].includes(' hidden');elements.set(m[2],e);
}
const el=id=>{assert(elements.has(id),`missing ${id}`);return elements.get(id);};
const node=(tag,text)=>new Element(tag,text),table=(headers,rows)=>new Element('table',JSON.stringify({headers,rows}));
for(const [id,value]of [['cost-budget','0'],['cost-license','1'],['cost-terminal','0'],['cost-kind','delta']])el(id).value=value;
const start=html.indexOf('// Native cost controls:'),end=html.indexOf('// End native cost controls.');assert(start>=0&&end>start);
vm.runInNewContext(html.slice(start,end),{packet,el,node,table});
for(const prefix of ['cost','square']){el(prefix+'-reveal').events.click();assert(el(prefix+'-outcome').hidden);assert.equal(focused,el(prefix+'-prediction'));}
let histories=0,squares=0;
function setStart(parts){for(const [id,value]of [['cost-budget',parts[0]],['cost-license',parts[1]],['cost-terminal',parts[2]]])el(id).value=value;el('cost-budget').events.change();assert(el('cost-outcome').hidden&&el('square-outcome').hidden);assert.equal(el('cost-prediction').value,'');assert.equal(el('square-prediction').value,'');}
for(const [key,row]of Object.entries(packet.costs.histories))for(const kind of ['delta','changes']){
 const parts=key.split('_');setStart(parts);el('cost-history').value=parts[3];el('cost-kind').value=kind;el('cost-kind').events.change();el('cost-prediction').value=String(row.totals[kind]);el('cost-reveal').events.click();assert(!el('cost-outcome').hidden);assert.match(el('cost-outcome').text(),/Your prediction matches/);assert(el('cost-outcome').text().includes('Chosen total: '+row.totals[kind]));el('cost-prediction').events.change();assert(el('cost-outcome').hidden);histories++;
}
for(const [key,row]of Object.entries(packet.costs.squares)){
 const parts=key.split('_');setStart(parts);el('square-first').value=parts[3];el('square-second').value=parts[4];el('square-first').events.change();el('square-prediction').value=row.commutes?'yes':'no';el('square-reveal').events.click();assert.match(el('square-outcome').text(),/Your prediction matches/);assert(el('square-outcome').text().includes(row.commutes?'a commuting square':'not a commuting square'));el('square-prediction').events.change();assert(el('square-outcome').hidden);squares++;
}
el('square-prediction').value='no';el('square-reveal').events.click();assert.match(el('square-outcome').text(),/different result/);
el('cost-prediction').value='-2';el('cost-reveal').events.click();assert.match(el('cost-outcome').text(),/different total/);
console.log(JSON.stringify({history_readings:histories,squares,prediction_gates:true,shared_reset:true,wrong_feedback:true,browser_layout:false}));
