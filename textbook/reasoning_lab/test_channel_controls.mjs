// Actual handlers in a minimal DOM; no browser-layout or learner evidence.
import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';
const html=fs.readFileSync(new URL('channels.template.html',import.meta.url),'utf8');
const packet=JSON.parse(fs.readFileSync(new URL('channels.json',import.meta.url),'utf8'));
const elements=new Map();let focused=null;
class Element{
 constructor(tag,text=''){this.tag=tag;this.textContent=text;this.children=[];this.events={};this.value='';this.hidden=false;}
 append(...children){this.children.push(...children);if(this.tag==='select'&&this.children.length===children.length)this.value=children[0].value;}
 replaceChildren(...children){this.children=children;this.textContent='';}
 addEventListener(event,fn){this.events[event]=fn;}focus(){focused=this;}
 text(){return this.textContent+this.children.map(c=>c.text()).join(' ');}
}



for(const m of html.matchAll(/<([a-z]+)[^>]* id="((?:order|record)-[^"]+)"[^>]*>/g)){assert(!elements.has(m[2]));const e=new Element(m[1]);e.hidden=m[0].includes(' hidden');elements.set(m[2],e);}
const el=id=>{assert(elements.has(id),id);return elements.get(id);};const node=(tag,text)=>new Element(tag,text),table=(headers,rows)=>node('table',headers.join(' ')+' '+rows.flat().join(' '));
const start=html.indexOf('// Channel controls:'),end=html.indexOf('// End channel controls.');assert(start>=0&&end>start);
vm.runInNewContext(html.slice(start,end),{packet,el,node,table});
for(const p of ['order','record']){el(p+'-reveal').events.click();assert(el(p+'-outcome').hidden);assert.equal(focused,el(p+'-prediction'));}
let checks=0;
for(const [prefix,records,controls]of [['order',packet.orders,['order-first','order-second']],['record',packet.records,['record-pair','record-post']]]){
 for(const[key,row]of Object.entries(records)){
  const values=key.split('_');controls.forEach((id,i)=>el(id).value=values[i]);el(controls[0]).events.change();
  for(const answer of ['yes','no']){
   el(prefix+'-prediction').value=answer;el(prefix+'-reveal').events.click();assert(!el(prefix+'-outcome').hidden);
   const text=el(prefix+'-outcome').text();assert.equal(text.includes('Your prediction matches'),answer===row.answer);
   for(const v of(prefix==='order'?row.forward_rows.flat():row.processed))assert(text.includes(String(v)));
   el(prefix+'-prediction').events.change();assert(el(prefix+'-outcome').hidden);checks++;
  }
  for(const id of controls){el(prefix+'-prediction').value='yes';el(id).events.change();assert.equal(el(prefix+'-prediction').value,'');assert(el(prefix+'-outcome').hidden);}
 }
}
assert.equal(checks,90);assert(!html.includes('fetch(')&&!html.includes('localStorage'));
console.log(JSON.stringify({order_predictions:72,record_predictions:18,gates:true,resets:true,wrong_feedback:true,browser_layout:false}));
