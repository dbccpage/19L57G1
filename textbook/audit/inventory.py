"""Mechanical inventory of lean4/Derivation/*.lean and the root."""
import hashlib, json, re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
sha = subprocess.run(["git","rev-parse","HEAD"],cwd=root,capture_output=True,text=True).stdout.strip()
files = sorted(root.glob("lean4/Derivation/*.lean")) 
rootfile = root/"lean4/Derivation.lean"
root_imports = set(re.findall(r"^import Derivation\.(\S+)", rootfile.read_text(encoding="utf-8"), re.M))
parked = (root/"lean4/ParkedAudit.lean").read_text(encoding="utf-8")
parked_imports = set(re.findall(r"^import Derivation\.(\S+)", parked, re.M))
ax = (root/"artifacts/lean_axioms.txt").read_text(encoding="utf-8")
ax_names = re.findall(r"^'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", ax, re.M)
ax_map = {n: a for n, a in ax_names}
decl_re = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private |protected |noncomputable |nonrec )*(theorem|lemma|def|abbrev|structure|inductive|instance|class|axiom|opaque)\s+([^\s:({\[]+)", re.M)
ns_re = re.compile(r"^namespace\s+(\S+)", re.M)
out = []
for f in files:
    txt = f.read_text(encoding="utf-8")
    h = hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16]
    imps = re.findall(r"^import (\S+)", txt, re.M)
    decls = decl_re.findall(txt)
    kinds = {}
    for k, n in decls: kinds[k] = kinds.get(k,0)+1
    names = [n for k,n in decls if k in ("theorem","lemma")]
    nss = ns_re.findall(txt)
    # axiom report hits: count artifact lines whose last component is a declared name in this file
    hits = 0; axset=set()
    declnames = set(n for _, n in decls)
    for full, a in ax_names:
        last = full.split(".")[-1]
        if last in declnames and any(full.startswith(ns) or full.startswith("Derivation."+ns) or full.startswith("Derivation.") for ns in nss or ["Derivation"]):
            hits += 1; axset.add(a)
    sorry = bool(re.search(r"\bsorry\b|\badmit\b|^\s*axiom\s", txt, re.M))
    out.append(dict(module=f.stem, path=str(f.relative_to(root)), lines=txt.count("\n")+1,
        sha256_16=h, imports=imps, namespaces=nss, decl_counts=kinds,
        theorems=names, root_import=f.stem in root_imports, parked=f.stem in parked_imports,
        axiom_report_hits=hits, axioms_seen=sorted(axset), forbidden_tokens=sorry))
print(json.dumps(dict(commit=sha, root_direct_imports=len(root_imports), modules=out), indent=1))
