// Actual calibration event handlers in a minimal DOM; no layout evidence.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const html=fs.readFileSync(new URL('calibration.template.html',import.meta.url),'utf8');
const packet=JSON.parse(fs.readFileSync(new URL('calibration.json',import.meta.url),'utf8'));
const elements=new Map();let focused=null;
class Element{
 constructor(tag,text=''){this.tag=tag;this.textContent=text;this.children=[];this.events={};this.value='';this.hidden=false;}
 append(...children){this.children.push(...children);if(this.tag==='select'&&this.children.length===children.length)this.value=children[0].value;}
 replaceChildren(...children){this.children=children;this.textContent='';}
 addEventListener(event,fn){this.events[event]=fn;}
 focus(){focused=this;}
 text(){return this.textContent+this.children.map(c=>c.text()).join(' ');}
}
for(const m of html.matchAll(/<([a-z]+)[^>]* id="(cal-[^"]+)"[^>]*>/g)){assert(!elements.has(m[2]));const e=new Element(m[1]);e.hidden=m[0].includes(' hidden');elements.set(m[2],e);}
const el=id=>{assert(elements.has(id),id);return elements.get(id);};
const node=(tag,text)=>new Element(tag,text),table=(headers,rows)=>node('table',headers.join(' ')+' '+rows.flat().join(' '));
const start=html.indexOf('// Calibration controls:'),end=html.indexOf('// End calibration controls.');assert(start>=0&&end>start);
vm.runInNewContext(html.slice(start,end),{packet,el,node,table});
for(const [button,prediction,outcome]of [['cal-reveal','cal-prediction','cal-outcome'],['cal-ratio-reveal','cal-ratio-prediction','cal-ratio-outcome']]){el(button).events.click();assert(el(outcome).hidden);assert.equal(focused,el(prediction));}
let conversions=0,comparisons=0;
for(const [key,c]of Object.entries(packet.conversions)){
 const [i,j]=key.split('_');el('cal-object').value=i;el('cal-unit').value=j;el('cal-object').events.change();assert.equal(el('cal-prediction').value,'');assert(el('cal-outcome').hidden);
 for(const answer of packet.conversion_answers){el('cal-prediction').value=answer;el('cal-reveal').events.click();assert(!el('cal-outcome').hidden);assert.equal(el('cal-outcome').text().includes('Your prediction matches'),answer===c.answer);assert(el('cal-outcome').text().includes(c.after.number+' '+c.after.standard));el('cal-prediction').events.change();assert(el('cal-outcome').hidden);conversions++;}
 el('cal-unit').events.change();assert.equal(el('cal-prediction').value,'');assert(el('cal-outcome').hidden);
}
for(const [i,c]of packet.comparisons.entries()){
 el('cal-case').value=String(i);el('cal-case').events.change();assert.equal(el('cal-ratio-prediction').value,'');assert(el('cal-ratio-outcome').hidden);
 for(const answer of ['0','1/3','2/3','1','3/2','refuse']){el('cal-ratio-prediction').value=answer;el('cal-ratio-reveal').events.click();assert(!el('cal-ratio-outcome').hidden);assert.equal(el('cal-ratio-outcome').text().includes('Your prediction matches'),answer===c.answer);if(c.answer==='refuse')assert(el('cal-ratio-outcome').text().includes(c.reason));el('cal-ratio-prediction').events.change();assert(el('cal-ratio-outcome').hidden);comparisons++;}
}
el('cal-case').value='5';el('cal-case').events.change();el('cal-ratio-prediction').value='2/3';el('cal-ratio-reveal').events.click();assert(el('cal-ratio-outcome').text().includes('24 and 36'));
assert(!html.includes('fetch(')&&!html.includes('localStorage'));
console.log(JSON.stringify({conversion_predictions:conversions,comparison_predictions:comparisons,gates:true,resets:true,zero_answer:true,wrong_feedback:true,browser_layout:false}));
