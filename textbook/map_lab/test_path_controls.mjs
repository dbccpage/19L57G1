// Execute exact desk handlers in a minimal DOM. No browser-layout claim.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const html=fs.readFileSync(new URL('results.template.html',import.meta.url),'utf8');
const packet=JSON.parse(fs.readFileSync(new URL('recorded_lab.json',import.meta.url),'utf8'));
const elements=new Map(); let focused=null;
class Element{
  constructor(tag,text=''){this.tag=tag;this.textContent=text;this.children=[];this.events={};this.value='';this.hidden=false;}
  append(...children){this.children.push(...children);if(this.tag==='select'&&this.children.length===children.length)this.value=children[0].value;}
  replaceChildren(...children){this.children=children;this.textContent='';}
  addEventListener(event,fn){this.events[event]=fn;}
  focus(){focused=this;}
  text(){return this.textContent+this.children.map(c=>c.text()).join(' ');}
}
for(const match of html.matchAll(/<([a-z]+)[^>]* id="((?:path|trace)-[^"]+)"[^>]*>/g)){
  assert(!elements.has(match[2]));const e=new Element(match[1]);e.hidden=match[0].includes(' hidden');elements.set(match[2],e);
}
const el=id=>{assert(elements.has(id),`missing ${id}`);return elements.get(id);};
const node=(tag,text)=>new Element(tag,text),table=(headers,rows)=>new Element('table',JSON.stringify({headers,rows}));
el('path-start').value='0';el('path-reader').value='native';
const start=html.indexOf('// Native path controls:'),end=html.indexOf('// End native path controls.');
assert(start>=0&&end>start);vm.runInNewContext(html.slice(start,end),{packet,el,node,table});
assert.equal(el('path-history').children.length,63);assert.equal(el('trace-case').children.length,7);
assert.deepEqual(el('trace-case').children.map(option=>option.textContent),['Record A','Record B','Record C','Record D','Record E','Record F','Record G']);
for(const prefix of ['path','trace']){el(prefix+'-reveal').events.click();assert(el(prefix+'-outcome').hidden);assert.equal(focused,el(prefix+'-prediction'));}
let checks=0;
for(const row of Object.values(packet.native_paths.histories)){
  for(const reading of ['native','budget']){
    el('path-start').value=String(row.start);el('path-history').value=row.events.join('');el('path-reader').value=reading;el('path-reader').events.change();
    assert.equal(el('path-prediction').value,'');assert(el('path-outcome').hidden);
    el('path-prediction').value=reading==='budget'?'yes':'no';el('path-reveal').events.click();
    assert(!el('path-outcome').hidden);assert.match(el('path-outcome').text(),/Your prediction matches/);
    el('path-prediction').events.change();assert(el('path-outcome').hidden);checks++;
  }
}
for(const [name,row]of Object.entries(packet.native_paths.traces)){
  el('trace-case').value=name;el('trace-case').events.change();assert.equal(el('trace-prediction').value,'');assert(el('trace-outcome').hidden);
  el('trace-prediction').value=row.valid?'yes':'no';el('trace-reveal').events.click();assert.match(el('trace-outcome').text(),/Your prediction matches/);assert(el('trace-outcome').text().includes(row.reason));
  el('trace-prediction').events.change();assert(el('trace-outcome').hidden);
}
el('path-prediction').value='no';el('path-reveal').events.click();assert.match(el('path-outcome').text(),/different result/);
el('trace-case').value='wrong event label';el('trace-case').events.change();el('trace-prediction').value='yes';el('trace-reveal').events.click();assert.match(el('trace-outcome').text(),/different result/);
console.log(JSON.stringify({reading_selections:checks,traces:7,prediction_gate:true,reset:true,wrong_feedback:true,browser_layout:false}));
