"use strict";
const fs=require("node:fs"), path=require("node:path"), assert=require("node:assert/strict");
const {lookup}=require("./desk.js");
const p=JSON.parse(fs.readFileSync(path.join(__dirname,"recorded_lab.json"),"utf8"));
let count=0;
for(let mask=0;mask<16;mask++) {
  const x=lookup(p,"reports",{mask});
  assert.equal(x.yes,x.row.admitted.every(([a,b])=>a===b)); count++;
}
for(const [bits,row] of Object.entries(p.control_menu)) {
  const x=lookup(p,"menu",{bits});
  assert.equal(x.yes,!x.row.automorphisms.some(pi=>pi[0]===1));
  assert.equal(x.row.eligible,row.mu1<=1); count++;
  for(const pi of row.automorphisms) assert.ok(row.images.some(x=>x.permutation.join(",")===pi.join(",")));
}
for(const row of Object.values(p.transfer_cases)) {
  const x=lookup(p,"labels",{labels:row.labels.join(""),permit:row.permutations_permitted,
    keep:row.keep_labels,key:row.key_choice});
  assert.equal(x.yes,!row.automorphisms.some(pi=>pi[0]===1)); count++;
  for(const pi of row.automorphisms) assert.ok(row.images.some(x=>x.permutation.join(",")===pi.join(",")));
}
assert.throws(()=>lookup(p,"menu",{bits:"999"}),/Unknown recorded case/);
assert.throws(()=>lookup(p,"different-model",{}),/Unknown experiment/);
assert.equal(count,120); console.log("Swap-desk lookups: 120 recorded settings and invalid cases pass");
