"use strict";
function lookup(data, mode, state) {
  let row, yes;
  if (mode === "reports") {
    row=data.report_cases[String(state.mask)]; yes=row?.swap_preserves_all;
  } else if (mode === "menu") {
    row=data.control_menu[state.bits]; yes=row?.satisfies;
  } else if (mode === "labels") {
    row=data.transfer_cases[state.labels+"_"+Number(state.permit)+Number(state.keep)+"_"+state.key];
    yes=row?.separates_0_1;
  } else throw new Error("Unknown experiment");
  if (!row || typeof yes !== "boolean") throw new Error("Unknown recorded case");
  return {row, yes};
}
if (typeof module !== "undefined") module.exports={lookup};
if (typeof document !== "undefined") {
  const el=id=>document.getElementById(id);
  const yesNo=v=>v?"yes":"no";
  for (const labels of [...new Set(Object.values(packet.transfer_cases).map(r=>r.labels.join("")))].sort((a,b)=>a.length-b.length||a.localeCompare(b))) {
    const option=document.createElement("option"); option.value=labels; option.textContent=labels.split("").join(", ");
    el("marks").append(option);
  }
  function selected() {
    const mode=el("mode").value;
    let mask=0; for(let i=0;i<4;i++) if(el("report"+i).checked) mask|=1<<i;
    return {mode, state:{mask, bits:["restrict","keep","extra"].map(id=>Number(el(id).checked)).join(""),
      labels:el("marks").value, permit:el("permit").checked, keep:el("retain").checked, key:el("key").value}};
  }
  function changed() {
    const {mode}=selected();
    for(const panel of ["reports","menu","labels"]) el(panel).hidden=panel!==mode;
    el("question").textContent=mode==="reports"?"Will the swap preserve every selected report?":
      mode==="menu"?"Will this candidate satisfy separation of marks 0 and 1?":"Will marks 0 and 1 be separated under these settings?";
    el("result").hidden=true; el("prompt").textContent="";
    for(const p of document.querySelectorAll('input[name="prediction"]')) p.checked=false;
  }
  for(const input of document.querySelectorAll("select, input[type=checkbox]")) input.addEventListener("change",changed);
  el("reveal").addEventListener("click",()=>{
    const prediction=document.querySelector('input[name="prediction"]:checked');
    if(!prediction){el("prompt").textContent="Choose yes or no first.";return;}
    el("prompt").textContent="";
    const {mode,state}=selected(), {row,yes}=lookup(packet,mode,state);
    el("feedback").textContent="Your prediction: "+prediction.value+". Recorded answer: "+yesNo(yes)+".";
    el("verdict").textContent=(mode==="reports"?"Swap preserves every report: ":"Marks 0 and 1 separated: ")+yesNo(yes);
    el("tags").replaceChildren(); el("mappings").replaceChildren();
    if(mode==="reports") {
      el("reason").textContent=yes?(row.admitted.length?"Every selected report has equal answers.":"There is no selected report that could fail preservation."):
        "At least one selected report changes its answer under exchange.";
      el("details").textContent="Unequal-answer witnesses: "+(row.breaking_witnesses.map(d=>"("+d.map(yesNo).join(", ")+")").join("; ")||"none")+".";
    } else {
      for(const [i,label] of row.labels.entries()){const tag=document.createElement("span");tag.className="tag";tag.textContent=i+": "+label;el("tags").append(tag);}
      el("reason").textContent=mode==="menu"?(row.identity_only?"The permission restriction retains only identity. This is satisfaction by the declared rule.":"A permitted key-preserving permutation still carries mark 0 to mark 1."):
        "First restrict to permitted permutations, then keep those preserving the key. Check which marks each remaining permutation moves.";
      const extra=mode==="menu"?" Changed settings: "+row.mu1+". Eligible for the one-step minimum: "+yesNo(row.eligible)+".":"";
      el("details").textContent="Permitted automorphisms: "+row.automorphisms.length+". Separated pairs: "+
        (row.separated_pairs.map(p=>p.join("–")).join(", ")||"none")+"."+extra;
      for(const pi of row.automorphisms){const div=document.createElement("div");div.className="mapping";
        const image=row.images.find(x=>x.permutation.join(",")===pi.join(","));
        div.textContent=pi.map((v,i)=>i+" → "+v).join("; ")+". Image labels: ["+image.labels.join(", ")+"].";el("mappings").append(div);}
    }
    el("result").hidden=false;
  });
  changed();
}
