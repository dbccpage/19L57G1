"""Schema conformance for ``paper/paper_claim_ledger.md``.

The ledger header declares required fields and a closed Class vocabulary.
Until this file, nothing checked that entries obey either.  Evidence-token
resolution is a different gate (``ci/check_ledger_evidence.py``); this
module checks the record shape, Class membership, falsifier presence,
Python-evidence presence, unique IDs, and that every named Lean theorem
exists as a declaration in ``lean4/``.

Population and classification are independent.  Claim IDs come from
``### CL-*`` headings and that regex never mentions field names.  Field
presence is judged by a second pattern.  A heading the field parser cannot
place still counts, so a malformed entry fails instead of vanishing.

KNOWN_* ratchets freeze HEAD gaps so the suite is green.  Tests require
equality with the live gap sets: a new gap fails the "no extras" direction;
an entry that no longer fails must be removed from the ratchet.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEDGER = REPO / "paper" / "paper_claim_ledger.md"
LEAN_ROOT = REPO / "lean4"
AXIOMS = REPO / "artifacts" / "lean_axioms.txt"

HEADING = re.compile(r"^### (?P<id>CL-[A-Za-z0-9-]+)")
# A field opener is a bold key followed by a colon.  The optional tail
# between the closing ** and the colon absorbs parenthetical scopes
# (``**Statement** (review-pass scope):``).
FIELD = re.compile(
    r"\*\*(?P<key>[A-Za-z][^*]*?)\*\*(?:[^*:\n]*)?:"
)
NEXT_BULLET = re.compile(r"\n- \*\*")
IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_.']*$")
TICK = re.compile(r"`([^`]+)`")
DECL = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
    r"(?:theorem|lemma|def|abbrev|structure|inductive|instance|class)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_.']*)"
)
CTOR = re.compile(r"^\s*\|\s*\.?(?P<name>[A-Za-z_][A-Za-z0-9_']*)")
AXIOM_REPORT = re.compile(
    r"^Derivation\.lean:\d+:\d+: '(?P<name>.+?)' "
    r"(?:depends on axioms: \[[^\]]*\]|does not depend on any axioms)"
)

CLOSED_CLASS = frozenset(
    {
        "declared metatheory",
        "definition",
        "finite computation",
        "theorem",
        "bounded theorem",
        "conjecture",
        "counterexample",
        "unresolved",
    }
)

STATEMENT_KEYS = frozenset({"Statement"})
CLASS_KEYS = frozenset({"Class"})
DEPS_KEYS = frozenset({"Deps"})
ASSUMPTIONS_KEYS = frozenset({"Assumptions"})
LEAN_KEYS = frozenset(
    {"Lean", "Evidence", "Evidence (Lean)", "Python / Lean / Axioms"}
)
AXIOM_KEYS = frozenset({"Axioms", "Python / Lean / Axioms"})
PYTHON_KEYS = frozenset(
    {"Python", "Python evidence", "Python / Lean / Axioms"}
)
FALSIFIER_KEYS = frozenset(
    {"Falsifier / boundary", "Falsifier", "Falsifier that fired"}
)
SCOPE_KEYS = frozenset({"Scope"})
SCHEMA_KEYS = (
    STATEMENT_KEYS
    | CLASS_KEYS
    | DEPS_KEYS
    | ASSUMPTIONS_KEYS
    | LEAN_KEYS
    | AXIOM_KEYS
    | PYTHON_KEYS
    | FALSIFIER_KEYS
    | SCOPE_KEYS
)

# Tokens that name apparatus, not a theorem.
LEAN_META = frozenset(
    {
        "--",
        "propext",
        "Quot.sound",
        "{propext, Quot.sound}",
        "#print axioms",
        "rfl",
        "Option",
        "Bool",
        "Nat",
        "Prop",
        "Type",
        "False",
        "True",
        "wit",
        "prot",
        "obs",
        "Metatheory",
        "Classical.choice",
    }
)

VACUOUS_PYTHON = re.compile(
    r"^(?:--|"
    r"n/a(?:\s*\([^)]*\))?|"
    r"none\b.*|"
    r"inventory and receipt binding only.*)$",
    re.I,
)


def _norm_body(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s*-\s*$", "", text).strip()
    return text


def _class_norm(text: str) -> str:
    return _norm_body(text).rstrip(".")


def _key_kind(key: str) -> str:
    if key == "Statement" or key.startswith("Statement"):
        return "Statement"
    if key == "Scope" or key.startswith("Scope"):
        return "Scope"
    return key


@dataclass(frozen=True)
class Claim:
    claim_id: str
    heading_line: int
    body: str
    field_list: tuple[tuple[str, str], ...] = ()


def parse_claims(text: str) -> list[Claim]:
    lines = text.splitlines()
    starts: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if m:
            starts.append((i, m.group("id")))
    claims: list[Claim] = []
    for n, (start, cid) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
        for j in range(start + 1, end):
            if lines[j].startswith("# ") or lines[j].startswith("## "):
                end = j
                break
        body_lines = lines[start:end]
        body = "\n".join(body_lines)
        field_list: list[tuple[str, str]] = []
        matches = list(FIELD.finditer(body))
        for i, m in enumerate(matches):
            kind = _key_kind(m.group("key"))
            cut = len(body)
            for nxt in matches[i + 1 :]:
                if _key_kind(nxt.group("key")) in SCHEMA_KEYS:
                    cut = nxt.start()
                    break
            bullet = NEXT_BULLET.search(body, m.end())
            if bullet is not None and bullet.start() < cut:
                cut = bullet.start()
            field_list.append((kind, body[m.end() : cut]))
        claims.append(
            Claim(
                claim_id=cid,
                heading_line=start + 1,
                body=body,
                field_list=tuple(field_list),
            )
        )
    return claims


def load_ledger() -> list[Claim]:
    return parse_claims(LEDGER.read_text(encoding="utf-8"))


def has_field(claim: Claim, keys: frozenset[str]) -> bool:
    if any(kind in keys for kind, _value in claim.field_list):
        return True
    # ``**Statement** (scope: ...)`` can place the colon after a
    # line wrap, so the opener regex misses it.  The bold word is
    # still the Statement field.
    if keys is STATEMENT_KEYS or "Statement" in keys:
        return "**Statement" in claim.body
    return False


def field_text(claim: Claim, keys: frozenset[str]) -> str:
    """Concatenate every matching field in source order.

    A frozenset walk is hash-seed dependent and would skip a later
    Lean/Evidence sibling whenever the first matching key won.
    """
    parts = [value for kind, value in claim.field_list if kind in keys]
    return "\n".join(parts)


def missing_required(claim: Claim, keys: frozenset[str]) -> bool:
    return not has_field(claim, keys)


def class_value(claim: Claim) -> str | None:
    for kind, value in claim.field_list:
        if kind == "Class":
            return _class_norm(value)
    return None


def python_is_vacuous(claim: Claim) -> bool:
    if not has_field(claim, PYTHON_KEYS):
        return True
    body = _norm_body(field_text(claim, PYTHON_KEYS)).rstrip(".")
    return body == "" or VACUOUS_PYTHON.match(body) is not None


def falsifier_is_missing(claim: Claim) -> bool:
    if not has_field(claim, FALSIFIER_KEYS):
        return True
    return _norm_body(field_text(claim, FALSIFIER_KEYS)) == ""


def lean_names_in(claim: Claim) -> list[str]:
    text = field_text(claim, LEAN_KEYS)
    names: list[str] = []
    for raw in TICK.findall(text):
        token = re.sub(r"\n\s*", "", raw).strip()
        if not token or token in LEAN_META:
            continue
        if token.startswith("CL-"):
            continue
        if token.endswith((".lean", ".py", ".md", ".json", ".txt")):
            continue
        # Family wildcard: keep as written.
        if token.endswith(".*") or token.endswith("_*"):
            names.append(token)
            continue
        core = token.split()[0].rstrip(",;.")
        core = core.lstrip(".")
        if IDENT.match(core):
            names.append(core)
    return names


def load_lean_decls() -> tuple[frozenset[str], frozenset[str]]:
    """Return (last-segment names, file- and namespace-qualified names)."""
    last: set[str] = set()
    qualified: set[str] = set()
    ns_open = re.compile(r"^namespace\s+([A-Za-z_][A-Za-z0-9_.]*)")
    ns_end = re.compile(r"^end\s+([A-Za-z_][A-Za-z0-9_.]*)")
    for path in sorted(LEAN_ROOT.rglob("*.lean")):
        stack: list[str] = []
        stem = path.stem
        rel = ".".join(path.relative_to(LEAN_ROOT).with_suffix("").parts)
        for line in path.read_text(encoding="utf-8").splitlines():
            opened = ns_open.match(line)
            if opened:
                stack.append(opened.group(1))
                continue
            closed = ns_end.match(line)
            if closed and stack and stack[-1] == closed.group(1):
                stack.pop()
                continue
            m = DECL.match(line) or CTOR.match(line)
            if not m:
                continue
            name = m.group("name")
            short = name.split(".")[-1]
            last.add(short)
            qualified.add(name)
            qualified.add(f"{stem}.{short}")
            qualified.add(f"{rel}.{short}")
            if stack:
                qualified.add(".".join([*stack, short]))
    if AXIOMS.exists():
        for line in AXIOMS.read_text(encoding="utf-8").splitlines():
            reported = AXIOM_REPORT.match(line)
            if reported:
                qualified.add(reported.group("name"))
    return frozenset(last), frozenset(qualified)


def lean_name_resolves(
    name: str, last: frozenset[str], qualified: frozenset[str]
) -> bool:
    if name.endswith(".*") or name.endswith("_*"):
        prefix = name[:-1]
        return any(
            q == prefix or q.startswith(prefix) or ("." + prefix) in q
            for q in qualified
        )
    if "." in name:
        return name in qualified
    return name in last


# ---------------------------------------------------------------------------
# KNOWN_* ratchets.  Frozen against the unedited ledger at the merge-base
# of this branch.  Do not add an ID to hide a new gap; if a listed ID no
# longer fails, remove it.  KNOWN_CLAIM_IDS is the complete heading census:
# deleting a conforming claim fails even if it sat in no gap set.
# ---------------------------------------------------------------------------

KNOWN_CLAIM_IDS: tuple[str, ...] = (
    'CL-0-INERTIA',
    'CL-0-NO-PROPOSAL-MUTATION',
    'CL-1-SUPPLY-NOT-ADMISSION',
    'CL-1-READING-CONVERGENCE',
    'CL-2-COLLAPSED',
    'CL-2-NONINCREASE',
    'CL-3-FAIL-CURRENT',
    'CL-3-COST1-IMPOSSIBLE',
    'CL-3-MIN-TWO',
    'CL-3-NONUNIQUE-MU1',
    'CL-3-TIE-CLASSES',
    'CL-3-INFINITE-TIES',
    'CL-3-UNIQUE-MU2-L',
    'CL-3-UNIQUE-MU2-F',
    'CL-PRUNE-RULE',
    'CL-PRUNE-STRUCTURAL',
    'CL-PROGRESS',
    'CL-CLOSURE-POLICY',
    'CL-CLOSURE-TERMINATION',
    'CL-CLOSURE-FIXPOINT',
    'CL-TRANSITION-EQUIVARIANCE',
    'CL-BRANCH-REPORTS',
    'CL-TREE-MU2-COMPLETE',
    'CL-TREE-MU1-FRONTIER',
    'CL-REACHES-REQUESTED-DEPTH-WITH-EXTERNAL-SUPPLY',
    'CL-CLOSURE-VS-EXTERNAL',
    'CL-ROLES',
    'CL-TOKEN-ERASURE',
    'CL-REPLAY',
    'CL-QUOT-BARRIER',
    'CL-ISO-SOUND',
    'CL-COUNT-INVARIANCE',
    'CL-DETERMINISM',
    'CL-READING-UNDERDETERMINATION',
    'CL-NO-UNIVERSAL-PROPERTY',
    'CL-FR6-TERMINAL',
    'CL-FR6-T1-INERTIA',
    'CL-FR6-T2-TRACE',
    'CL-FR6-T3-CONSTRUCTORS',
    'CL-FR6-T4-CARRIER',
    'CL-FR6-T5-BRIDGE',
    'CL-FR6-T6-LAW',
    'CL-FR6-T7-CEILING',
    'CL-FR6-T8-DYNAMICS',
    'CL-FR6-T9-PRICES',
    'CL-FR6-T10-NORMAL-FORM',
    'CL-G-TERMINAL',
    'CL-G-GENERATION',
    'CL-G-OBSTRUCTIONS-EXACT',
    'CL-G-REPAIR-FATES',
    'CL-G-DEPTH2',
    'CL-G-DIRECT-SWAP',
    'CL-G-EXCLUSION',
    'CL-G-OPEN',
    'CL-DI-EQUIVALENCE',
    'CL-DI-OBSTRUCTION',
    'CL-DI-REFLECTION',
    'CL-DI-CLOSURE',
    'CL-DI-PROPOSAL',
    'CL-DI-TERMINATION',
    'CL-DI-COUNTERMODELS',
    'CL-DI-BOUNDARIES',
    'CL-RP-TERMINAL',
    'CL-RP-DEFINITIONS',
    'CL-RP-REPLAY',
    'CL-RP-SUPPORT',
    'CL-RP-NO-HIDDEN-CHOICE',
    'CL-RP-REPAIR-AUG',
    'CL-RP-PROGRESS',
    'CL-RP-CLOSURE',
    'CL-RP-PRODUCTIVITY',
    'CL-RP-CERTIFICATION',
    'CL-RP-COUNTERMODELS',
    'CL-RP-CEILING',
    'CL-NC-TERMINALS',
    'CL-NC-COMMON-STATE',
    'CL-NC-RULE1',
    'CL-NC-RULE2',
    'CL-NC-EVENT-SOURCE',
    'CL-NC-AUTONOMY',
    'CL-NC-CONSTITUTION',
    'CL-NC-INITIALITY',
    'CL-NC-INVENTORY',
    'CL-PD2-HORIZON',
    'CL-PD2-MATRIX',
    'CL-PD2-INITIALITY',
    'CL-PD2-BRANCHING',
    'CL-PD2-APARTNESS',
    'CL-PD2-CONTACT',
    'CL-PD2-PASSAGE',
    'CL-PD2-GROWTH',
    'CL-PD2-LADDER',
    'CL-PD2-CONTROLLER',
    'CL-PD2-INTERPRETER',
    'CL-PD2-RECEIPT',
    'CL-PD2-ATTACHMENT',
    'CL-PD2-LADDER-GENERAL',
    'CL-PD2-COMPRESSION',
    'CL-PD2-RECEIPT-BYTES',
    'CL-PD2-TRACE-STABILITY',
    'CL-PD2-RENAMING-STRUCTURE',
    'CL-PD2-GRAPH-GENESIS',
    'CL-PD2-BOUNDARY-CANCELLATION',
    'CL-PD2-WEIGHT-PROFILE',
    'CL-PD2-TRANSITION-CODEBOOK',
    'CL-PD2-TRACE-ALGEBRA',
    'CL-PD2-CONTACT-RECONSTRUCTION',
    'CL-PD2-CONTACT-BRIDGE',
    'CL-PD2-CONTACT-COUNTERMODELS',
    'CL-PD2-CONTACT-DICTIONARY',
    'CL-PD2-CONTACT-KERNEL',
    'CL-PD2-CONTACT-ENTRY',
    'CL-PD2-CONTACT-VERDICT',
    'CL-PD2-PACKET-02',
    'CL-PD2-PACKET-02R',
    'CL-PD2-PACKET-05',
    'CL-PD2-PACKET-05R',
    'CL-PD2-PACKET-05P',
    'CL-PN-NATURAL-SELECTION',
    'CL-PN-HETEROGENEOUS-TRANSPORT',
    'CL-CAP-BOUND',
    'CL-PREL-RELATIVE-IDENTITY',
    'CL-CLOSURE-SYMMETRY',
    'CL-FIDELITY-DESCENT',
    'CL-QUOTIENT-RETENTION',
    'CL-FIDELITY-CLOSURE',
    'CL-ENDOGENOUS-FIDELITY-GENERATOR',
)

KNOWN_MISSING_STATEMENT: frozenset[str] = frozenset({
    'CL-PD2-PACKET-05',
})

KNOWN_MISSING_CLASS: frozenset[str] = frozenset({
    'CL-ENDOGENOUS-FIDELITY-GENERATOR',
    'CL-FIDELITY-CLOSURE',
    'CL-FIDELITY-DESCENT',
    'CL-PD2-PACKET-05',
    'CL-PN-HETEROGENEOUS-TRANSPORT',
    'CL-QUOTIENT-RETENTION',
})

KNOWN_MISSING_DEPS: frozenset[str] = frozenset({
    'CL-CAP-BOUND',
    'CL-CLOSURE-SYMMETRY',
    'CL-DI-BOUNDARIES',
    'CL-DI-CLOSURE',
    'CL-DI-COUNTERMODELS',
    'CL-DI-EQUIVALENCE',
    'CL-DI-OBSTRUCTION',
    'CL-DI-PROPOSAL',
    'CL-DI-REFLECTION',
    'CL-DI-TERMINATION',
    'CL-ENDOGENOUS-FIDELITY-GENERATOR',
    'CL-FIDELITY-CLOSURE',
    'CL-FIDELITY-DESCENT',
    'CL-FR6-T1-INERTIA',
    'CL-FR6-T10-NORMAL-FORM',
    'CL-FR6-T2-TRACE',
    'CL-FR6-T3-CONSTRUCTORS',
    'CL-FR6-T4-CARRIER',
    'CL-FR6-T5-BRIDGE',
    'CL-FR6-T6-LAW',
    'CL-FR6-T7-CEILING',
    'CL-FR6-T8-DYNAMICS',
    'CL-FR6-T9-PRICES',
    'CL-FR6-TERMINAL',
    'CL-G-DEPTH2',
    'CL-G-DIRECT-SWAP',
    'CL-G-EXCLUSION',
    'CL-G-GENERATION',
    'CL-G-OBSTRUCTIONS-EXACT',
    'CL-G-OPEN',
    'CL-G-REPAIR-FATES',
    'CL-G-TERMINAL',
    'CL-NC-AUTONOMY',
    'CL-NC-COMMON-STATE',
    'CL-NC-CONSTITUTION',
    'CL-NC-EVENT-SOURCE',
    'CL-NC-INITIALITY',
    'CL-NC-INVENTORY',
    'CL-NC-RULE1',
    'CL-NC-RULE2',
    'CL-NC-TERMINALS',
    'CL-PD2-APARTNESS',
    'CL-PD2-ATTACHMENT',
    'CL-PD2-BOUNDARY-CANCELLATION',
    'CL-PD2-BRANCHING',
    'CL-PD2-COMPRESSION',
    'CL-PD2-CONTACT',
    'CL-PD2-CONTROLLER',
    'CL-PD2-GRAPH-GENESIS',
    'CL-PD2-GROWTH',
    'CL-PD2-HORIZON',
    'CL-PD2-INITIALITY',
    'CL-PD2-INTERPRETER',
    'CL-PD2-LADDER',
    'CL-PD2-LADDER-GENERAL',
    'CL-PD2-MATRIX',
    'CL-PD2-PACKET-02R',
    'CL-PD2-PACKET-05',
    'CL-PD2-PACKET-05P',
    'CL-PD2-PACKET-05R',
    'CL-PD2-PASSAGE',
    'CL-PD2-RECEIPT',
    'CL-PD2-RECEIPT-BYTES',
    'CL-PD2-RENAMING-STRUCTURE',
    'CL-PD2-TRACE-ALGEBRA',
    'CL-PD2-TRACE-STABILITY',
    'CL-PD2-TRANSITION-CODEBOOK',
    'CL-PD2-WEIGHT-PROFILE',
    'CL-PN-HETEROGENEOUS-TRANSPORT',
    'CL-PN-NATURAL-SELECTION',
    'CL-PREL-RELATIVE-IDENTITY',
    'CL-QUOTIENT-RETENTION',
    'CL-RP-CEILING',
    'CL-RP-CERTIFICATION',
    'CL-RP-CLOSURE',
    'CL-RP-COUNTERMODELS',
    'CL-RP-DEFINITIONS',
    'CL-RP-NO-HIDDEN-CHOICE',
    'CL-RP-PRODUCTIVITY',
    'CL-RP-PROGRESS',
    'CL-RP-REPAIR-AUG',
    'CL-RP-REPLAY',
    'CL-RP-SUPPORT',
    'CL-RP-TERMINAL',
})

KNOWN_MISSING_ASSUMPTIONS: frozenset[str] = frozenset({
    'CL-3-UNIQUE-MU2-F',
    'CL-CAP-BOUND',
    'CL-CLOSURE-SYMMETRY',
    'CL-CLOSURE-VS-EXTERNAL',
    'CL-DI-BOUNDARIES',
    'CL-DI-CLOSURE',
    'CL-DI-COUNTERMODELS',
    'CL-DI-EQUIVALENCE',
    'CL-DI-OBSTRUCTION',
    'CL-DI-PROPOSAL',
    'CL-DI-REFLECTION',
    'CL-DI-TERMINATION',
    'CL-ENDOGENOUS-FIDELITY-GENERATOR',
    'CL-FIDELITY-CLOSURE',
    'CL-FIDELITY-DESCENT',
    'CL-FR6-T1-INERTIA',
    'CL-FR6-T10-NORMAL-FORM',
    'CL-FR6-T2-TRACE',
    'CL-FR6-T3-CONSTRUCTORS',
    'CL-FR6-T4-CARRIER',
    'CL-FR6-T5-BRIDGE',
    'CL-FR6-T6-LAW',
    'CL-FR6-T7-CEILING',
    'CL-FR6-T8-DYNAMICS',
    'CL-FR6-T9-PRICES',
    'CL-FR6-TERMINAL',
    'CL-G-DEPTH2',
    'CL-G-DIRECT-SWAP',
    'CL-G-EXCLUSION',
    'CL-G-GENERATION',
    'CL-G-OBSTRUCTIONS-EXACT',
    'CL-G-OPEN',
    'CL-G-REPAIR-FATES',
    'CL-G-TERMINAL',
    'CL-NC-AUTONOMY',
    'CL-NC-COMMON-STATE',
    'CL-NC-CONSTITUTION',
    'CL-NC-EVENT-SOURCE',
    'CL-NC-INITIALITY',
    'CL-NC-INVENTORY',
    'CL-NC-RULE1',
    'CL-NC-RULE2',
    'CL-NC-TERMINALS',
    'CL-NO-UNIVERSAL-PROPERTY',
    'CL-PD2-APARTNESS',
    'CL-PD2-ATTACHMENT',
    'CL-PD2-BOUNDARY-CANCELLATION',
    'CL-PD2-BRANCHING',
    'CL-PD2-COMPRESSION',
    'CL-PD2-CONTACT',
    'CL-PD2-CONTROLLER',
    'CL-PD2-GRAPH-GENESIS',
    'CL-PD2-GROWTH',
    'CL-PD2-HORIZON',
    'CL-PD2-INITIALITY',
    'CL-PD2-INTERPRETER',
    'CL-PD2-LADDER',
    'CL-PD2-LADDER-GENERAL',
    'CL-PD2-MATRIX',
    'CL-PD2-PACKET-02',
    'CL-PD2-PACKET-02R',
    'CL-PD2-PACKET-05',
    'CL-PD2-PACKET-05P',
    'CL-PD2-PACKET-05R',
    'CL-PD2-PASSAGE',
    'CL-PD2-RECEIPT',
    'CL-PD2-RECEIPT-BYTES',
    'CL-PD2-RENAMING-STRUCTURE',
    'CL-PD2-TRACE-ALGEBRA',
    'CL-PD2-TRACE-STABILITY',
    'CL-PD2-TRANSITION-CODEBOOK',
    'CL-PD2-WEIGHT-PROFILE',
    'CL-PN-HETEROGENEOUS-TRANSPORT',
    'CL-PN-NATURAL-SELECTION',
    'CL-PREL-RELATIVE-IDENTITY',
    'CL-QUOTIENT-RETENTION',
    'CL-READING-UNDERDETERMINATION',
    'CL-ROLES',
    'CL-RP-CEILING',
    'CL-RP-CERTIFICATION',
    'CL-RP-CLOSURE',
    'CL-RP-COUNTERMODELS',
    'CL-RP-DEFINITIONS',
    'CL-RP-NO-HIDDEN-CHOICE',
    'CL-RP-PRODUCTIVITY',
    'CL-RP-PROGRESS',
    'CL-RP-REPAIR-AUG',
    'CL-RP-REPLAY',
    'CL-RP-SUPPORT',
    'CL-RP-TERMINAL',
    'CL-TREE-MU1-FRONTIER',
    'CL-TREE-MU2-COMPLETE',
})

KNOWN_MISSING_LEAN: frozenset[str] = frozenset({
    'CL-DI-BOUNDARIES',
    'CL-FR6-T10-NORMAL-FORM',
    'CL-FR6-T9-PRICES',
    'CL-G-EXCLUSION',
    'CL-G-OPEN',
    'CL-NC-INVENTORY',
    'CL-NC-TERMINALS',
    'CL-PD2-PACKET-02R',
    'CL-PD2-PACKET-05',
    'CL-PD2-RECEIPT',
    'CL-PD2-RECEIPT-BYTES',
    'CL-RP-CEILING',
    'CL-RP-DEFINITIONS',
    'CL-RP-TERMINAL',
})

KNOWN_MISSING_AXIOMS: frozenset[str] = frozenset({
    'CL-CAP-BOUND',
    'CL-CLOSURE-SYMMETRY',
    'CL-DI-BOUNDARIES',
    'CL-DI-CLOSURE',
    'CL-DI-COUNTERMODELS',
    'CL-DI-EQUIVALENCE',
    'CL-DI-OBSTRUCTION',
    'CL-DI-PROPOSAL',
    'CL-DI-REFLECTION',
    'CL-DI-TERMINATION',
    'CL-ENDOGENOUS-FIDELITY-GENERATOR',
    'CL-FIDELITY-CLOSURE',
    'CL-FIDELITY-DESCENT',
    'CL-FR6-T1-INERTIA',
    'CL-FR6-T10-NORMAL-FORM',
    'CL-FR6-T2-TRACE',
    'CL-FR6-T3-CONSTRUCTORS',
    'CL-FR6-T4-CARRIER',
    'CL-FR6-T5-BRIDGE',
    'CL-FR6-T6-LAW',
    'CL-FR6-T7-CEILING',
    'CL-FR6-T8-DYNAMICS',
    'CL-FR6-T9-PRICES',
    'CL-G-DEPTH2',
    'CL-G-DIRECT-SWAP',
    'CL-G-EXCLUSION',
    'CL-G-GENERATION',
    'CL-G-OBSTRUCTIONS-EXACT',
    'CL-G-OPEN',
    'CL-G-REPAIR-FATES',
    'CL-NC-AUTONOMY',
    'CL-NC-COMMON-STATE',
    'CL-NC-CONSTITUTION',
    'CL-NC-EVENT-SOURCE',
    'CL-NC-INITIALITY',
    'CL-NC-INVENTORY',
    'CL-NC-RULE1',
    'CL-NC-RULE2',
    'CL-NC-TERMINALS',
    'CL-PD2-APARTNESS',
    'CL-PD2-ATTACHMENT',
    'CL-PD2-BOUNDARY-CANCELLATION',
    'CL-PD2-BRANCHING',
    'CL-PD2-COMPRESSION',
    'CL-PD2-CONTACT',
    'CL-PD2-CONTROLLER',
    'CL-PD2-GRAPH-GENESIS',
    'CL-PD2-GROWTH',
    'CL-PD2-HORIZON',
    'CL-PD2-INITIALITY',
    'CL-PD2-INTERPRETER',
    'CL-PD2-LADDER',
    'CL-PD2-LADDER-GENERAL',
    'CL-PD2-MATRIX',
    'CL-PD2-PACKET-05',
    'CL-PD2-PACKET-05P',
    'CL-PD2-PASSAGE',
    'CL-PD2-RECEIPT',
    'CL-PD2-RECEIPT-BYTES',
    'CL-PD2-RENAMING-STRUCTURE',
    'CL-PD2-TRACE-ALGEBRA',
    'CL-PD2-TRACE-STABILITY',
    'CL-PD2-TRANSITION-CODEBOOK',
    'CL-PD2-WEIGHT-PROFILE',
    'CL-PN-HETEROGENEOUS-TRANSPORT',
    'CL-PN-NATURAL-SELECTION',
    'CL-PREL-RELATIVE-IDENTITY',
    'CL-QUOTIENT-RETENTION',
    'CL-RP-CEILING',
    'CL-RP-CERTIFICATION',
    'CL-RP-CLOSURE',
    'CL-RP-COUNTERMODELS',
    'CL-RP-DEFINITIONS',
    'CL-RP-NO-HIDDEN-CHOICE',
    'CL-RP-PRODUCTIVITY',
    'CL-RP-PROGRESS',
    'CL-RP-REPAIR-AUG',
    'CL-RP-REPLAY',
    'CL-RP-SUPPORT',
})

KNOWN_MISSING_FALSIFIER: frozenset[str] = frozenset({
    'CL-DI-CLOSURE',
    'CL-DI-COUNTERMODELS',
    'CL-DI-EQUIVALENCE',
    'CL-DI-OBSTRUCTION',
    'CL-DI-PROPOSAL',
    'CL-DI-REFLECTION',
    'CL-DI-TERMINATION',
    'CL-FIDELITY-CLOSURE',
    'CL-FIDELITY-DESCENT',
    'CL-FR6-T1-INERTIA',
    'CL-FR6-T10-NORMAL-FORM',
    'CL-FR6-T2-TRACE',
    'CL-FR6-T3-CONSTRUCTORS',
    'CL-FR6-T4-CARRIER',
    'CL-FR6-T5-BRIDGE',
    'CL-FR6-T6-LAW',
    'CL-FR6-T7-CEILING',
    'CL-FR6-T8-DYNAMICS',
    'CL-FR6-T9-PRICES',
    'CL-G-DEPTH2',
    'CL-G-DIRECT-SWAP',
    'CL-G-EXCLUSION',
    'CL-G-GENERATION',
    'CL-G-OBSTRUCTIONS-EXACT',
    'CL-G-OPEN',
    'CL-G-REPAIR-FATES',
    'CL-NC-AUTONOMY',
    'CL-NC-COMMON-STATE',
    'CL-NC-CONSTITUTION',
    'CL-NC-EVENT-SOURCE',
    'CL-NC-INITIALITY',
    'CL-NC-INVENTORY',
    'CL-NC-RULE1',
    'CL-NC-RULE2',
    'CL-PD2-APARTNESS',
    'CL-PD2-ATTACHMENT',
    'CL-PD2-BOUNDARY-CANCELLATION',
    'CL-PD2-BRANCHING',
    'CL-PD2-COMPRESSION',
    'CL-PD2-CONTACT',
    'CL-PD2-CONTROLLER',
    'CL-PD2-GRAPH-GENESIS',
    'CL-PD2-GROWTH',
    'CL-PD2-HORIZON',
    'CL-PD2-INITIALITY',
    'CL-PD2-INTERPRETER',
    'CL-PD2-LADDER',
    'CL-PD2-LADDER-GENERAL',
    'CL-PD2-MATRIX',
    'CL-PD2-PASSAGE',
    'CL-PD2-RECEIPT',
    'CL-PD2-RECEIPT-BYTES',
    'CL-PD2-RENAMING-STRUCTURE',
    'CL-PD2-TRACE-ALGEBRA',
    'CL-PD2-TRACE-STABILITY',
    'CL-PD2-TRANSITION-CODEBOOK',
    'CL-PD2-WEIGHT-PROFILE',
    'CL-QUOTIENT-RETENTION',
    'CL-RP-CEILING',
    'CL-RP-CERTIFICATION',
    'CL-RP-CLOSURE',
    'CL-RP-COUNTERMODELS',
    'CL-RP-DEFINITIONS',
    'CL-RP-NO-HIDDEN-CHOICE',
    'CL-RP-PRODUCTIVITY',
    'CL-RP-PROGRESS',
    'CL-RP-REPAIR-AUG',
    'CL-RP-REPLAY',
    'CL-RP-SUPPORT',
})

KNOWN_MISSING_PYTHON: frozenset[str] = frozenset({
    'CL-CAP-BOUND',
    'CL-CLOSURE-SYMMETRY',
    'CL-DI-BOUNDARIES',
    'CL-DI-CLOSURE',
    'CL-DI-EQUIVALENCE',
    'CL-DI-OBSTRUCTION',
    'CL-DI-PROPOSAL',
    'CL-DI-REFLECTION',
    'CL-DI-TERMINATION',
    'CL-ENDOGENOUS-FIDELITY-GENERATOR',
    'CL-FIDELITY-CLOSURE',
    'CL-FIDELITY-DESCENT',
    'CL-FR6-T1-INERTIA',
    'CL-FR6-T2-TRACE',
    'CL-FR6-T4-CARRIER',
    'CL-FR6-T5-BRIDGE',
    'CL-FR6-T7-CEILING',
    'CL-FR6-T8-DYNAMICS',
    'CL-G-DEPTH2',
    'CL-G-DIRECT-SWAP',
    'CL-G-GENERATION',
    'CL-G-OPEN',
    'CL-NC-AUTONOMY',
    'CL-NC-COMMON-STATE',
    'CL-NC-CONSTITUTION',
    'CL-NC-RULE1',
    'CL-NC-RULE2',
    'CL-NC-TERMINALS',
    'CL-NO-UNIVERSAL-PROPERTY',
    'CL-PD2-GROWTH',
    'CL-PD2-INITIALITY',
    'CL-PD2-LADDER',
    'CL-PD2-PACKET-02',
    'CL-PD2-PACKET-02R',
    'CL-PD2-PACKET-05',
    'CL-PD2-PACKET-05P',
    'CL-PD2-PACKET-05R',
    'CL-PN-HETEROGENEOUS-TRANSPORT',
    'CL-PN-NATURAL-SELECTION',
    'CL-PREL-RELATIVE-IDENTITY',
    'CL-QUOT-BARRIER',
    'CL-QUOTIENT-RETENTION',
    'CL-RP-CEILING',
    'CL-RP-CERTIFICATION',
    'CL-RP-CLOSURE',
    'CL-RP-DEFINITIONS',
    'CL-RP-NO-HIDDEN-CHOICE',
    'CL-RP-PRODUCTIVITY',
    'CL-RP-REPAIR-AUG',
    'CL-RP-REPLAY',
    'CL-RP-SUPPORT',
    'CL-RP-TERMINAL',
})

KNOWN_CLASS_OUTSIDE_VOCAB: frozenset[str] = frozenset({
    'CL-0-NO-PROPOSAL-MUTATION',
    'CL-2-NONINCREASE',
    'CL-3-INFINITE-TIES',
    'CL-3-NONUNIQUE-MU1',
    'CL-3-UNIQUE-MU2-F',
    'CL-CAP-BOUND',
    'CL-CLOSURE-FIXPOINT',
    'CL-CLOSURE-POLICY',
    'CL-CLOSURE-SYMMETRY',
    'CL-COUNT-INVARIANCE',
    'CL-DI-BOUNDARIES',
    'CL-DI-COUNTERMODELS',
    'CL-DI-OBSTRUCTION',
    'CL-DI-PROPOSAL',
    'CL-FR6-T10-NORMAL-FORM',
    'CL-FR6-T3-CONSTRUCTORS',
    'CL-FR6-T4-CARRIER',
    'CL-FR6-T5-BRIDGE',
    'CL-FR6-T6-LAW',
    'CL-FR6-T7-CEILING',
    'CL-FR6-T9-PRICES',
    'CL-FR6-TERMINAL',
    'CL-G-DEPTH2',
    'CL-G-DIRECT-SWAP',
    'CL-G-EXCLUSION',
    'CL-G-GENERATION',
    'CL-G-OPEN',
    'CL-G-REPAIR-FATES',
    'CL-G-TERMINAL',
    'CL-NC-AUTONOMY',
    'CL-NC-COMMON-STATE',
    'CL-NC-CONSTITUTION',
    'CL-NC-EVENT-SOURCE',
    'CL-NC-INITIALITY',
    'CL-NC-INVENTORY',
    'CL-NC-RULE1',
    'CL-NC-RULE2',
    'CL-NC-TERMINALS',
    'CL-NO-UNIVERSAL-PROPERTY',
    'CL-PD2-APARTNESS',
    'CL-PD2-ATTACHMENT',
    'CL-PD2-BOUNDARY-CANCELLATION',
    'CL-PD2-BRANCHING',
    'CL-PD2-COMPRESSION',
    'CL-PD2-CONTACT',
    'CL-PD2-CONTACT-BRIDGE',
    'CL-PD2-CONTACT-COUNTERMODELS',
    'CL-PD2-CONTACT-DICTIONARY',
    'CL-PD2-CONTACT-ENTRY',
    'CL-PD2-CONTACT-KERNEL',
    'CL-PD2-CONTACT-RECONSTRUCTION',
    'CL-PD2-CONTACT-VERDICT',
    'CL-PD2-CONTROLLER',
    'CL-PD2-GRAPH-GENESIS',
    'CL-PD2-GROWTH',
    'CL-PD2-HORIZON',
    'CL-PD2-INTERPRETER',
    'CL-PD2-LADDER',
    'CL-PD2-LADDER-GENERAL',
    'CL-PD2-MATRIX',
    'CL-PD2-PACKET-02',
    'CL-PD2-PACKET-02R',
    'CL-PD2-PACKET-05P',
    'CL-PD2-PACKET-05R',
    'CL-PD2-PASSAGE',
    'CL-PD2-RECEIPT',
    'CL-PD2-RECEIPT-BYTES',
    'CL-PD2-RENAMING-STRUCTURE',
    'CL-PD2-TRACE-ALGEBRA',
    'CL-PD2-TRACE-STABILITY',
    'CL-PD2-TRANSITION-CODEBOOK',
    'CL-PD2-WEIGHT-PROFILE',
    'CL-PN-NATURAL-SELECTION',
    'CL-PREL-RELATIVE-IDENTITY',
    'CL-PRUNE-RULE',
    'CL-READING-UNDERDETERMINATION',
    'CL-REPLAY',
    'CL-RP-CEILING',
    'CL-RP-CERTIFICATION',
    'CL-RP-COUNTERMODELS',
    'CL-RP-NO-HIDDEN-CHOICE',
    'CL-RP-PRODUCTIVITY',
    'CL-RP-TERMINAL',
    'CL-TRANSITION-EQUIVARIANCE',
})

KNOWN_UNRESOLVED_LEAN: frozenset[tuple[str, str]] = frozenset({
})



def live_missing(claims: list[Claim], keys: frozenset[str]) -> frozenset[str]:
    return frozenset(c.claim_id for c in claims if missing_required(c, keys))


def live_class_outside(claims: list[Claim]) -> frozenset[str]:
    out: set[str] = set()
    for c in claims:
        val = class_value(c)
        if val is None:
            continue
        if val not in CLOSED_CLASS:
            out.add(c.claim_id)
    return frozenset(out)


def live_missing_class(claims: list[Claim]) -> frozenset[str]:
    return live_missing(claims, CLASS_KEYS)


def live_missing_falsifier(claims: list[Claim]) -> frozenset[str]:
    return frozenset(c.claim_id for c in claims if falsifier_is_missing(c))


def live_missing_python(claims: list[Claim]) -> frozenset[str]:
    return frozenset(c.claim_id for c in claims if python_is_vacuous(c))


def live_unresolved_lean(
    claims: list[Claim], last: frozenset[str], qualified: frozenset[str]
) -> frozenset[tuple[str, str]]:
    bad: set[tuple[str, str]] = set()
    for c in claims:
        for name in lean_names_in(c):
            if not lean_name_resolves(name, last, qualified):
                bad.add((c.claim_id, name))
    return frozenset(bad)


def _assert_gap_eq(live: frozenset[str], known: frozenset[str], label: str) -> None:
    extra = live - known
    stale = known - live
    assert extra == frozenset(), (
        f"{label}: new gap(s) not in the ratchet: {sorted(extra)}"
    )
    assert stale == frozenset(), (
        f"{label}: ratchet stale (no longer fail): {sorted(stale)}"
    )


def test_claim_ids_are_unique() -> None:
    claims = load_ledger()
    ids = [c.claim_id for c in claims]
    dups = sorted({i for i in ids if ids.count(i) > 1})
    assert dups == [], f"duplicate claim IDs: {dups}"
    assert claims, "no CL-* headings parsed — the heading regex is broken"


def hash_heading_lines(text: str) -> list[str]:
    """Population: every ``### `` line.  This pattern never mentions CL-."""
    return [ln for ln in text.splitlines() if ln.startswith("### ")]


def test_heading_population_is_total() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    raw = hash_heading_lines(text)
    unclassified = [ln for ln in raw if HEADING.match(ln) is None]
    assert unclassified == [], (
        "triple-hash heading(s) the ID classifier cannot see: "
        + "; ".join(unclassified)
    )
    parsed = [c.claim_id for c in parse_claims(text)]
    assert len(parsed) == len(raw), (
        f"heading population {len(raw)} != parsed claims {len(parsed)}"
    )


def test_claim_ids_match_frozen_census() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    live = tuple(
        m.group("id")
        for ln in hash_heading_lines(text)
        if (m := HEADING.match(ln))
    )
    extra = [i for i in live if i not in KNOWN_CLAIM_IDS]
    missing = [i for i in KNOWN_CLAIM_IDS if i not in live]
    assert extra == [], f"unpinned claim ID(s): {extra}"
    assert missing == [], f"frozen claim ID(s) missing from the ledger: {missing}"
    assert live == KNOWN_CLAIM_IDS, "claim ID order drifted from the frozen census"
    assert KNOWN_CLAIM_IDS, "KNOWN_CLAIM_IDS is empty — the census is broken"


def test_required_statement_field() -> None:
    claims = load_ledger()
    live = live_missing(claims, STATEMENT_KEYS)
    _assert_gap_eq(live, KNOWN_MISSING_STATEMENT, "Statement")


def test_required_class_field() -> None:
    claims = load_ledger()
    _assert_gap_eq(live_missing_class(claims), KNOWN_MISSING_CLASS, "Class present")


def test_required_deps_field() -> None:
    claims = load_ledger()
    _assert_gap_eq(live_missing(claims, DEPS_KEYS), KNOWN_MISSING_DEPS, "Deps")


def test_required_assumptions_field() -> None:
    claims = load_ledger()
    _assert_gap_eq(
        live_missing(claims, ASSUMPTIONS_KEYS),
        KNOWN_MISSING_ASSUMPTIONS,
        "Assumptions",
    )


def test_required_lean_field() -> None:
    claims = load_ledger()
    _assert_gap_eq(live_missing(claims, LEAN_KEYS), KNOWN_MISSING_LEAN, "Lean")


def test_required_axioms_field() -> None:
    claims = load_ledger()
    _assert_gap_eq(live_missing(claims, AXIOM_KEYS), KNOWN_MISSING_AXIOMS, "Axioms")


def test_class_is_closed_vocabulary() -> None:
    claims = load_ledger()
    _assert_gap_eq(
        live_class_outside(claims), KNOWN_CLASS_OUTSIDE_VOCAB, "Class vocabulary"
    )


def test_falsifier_present_and_nonempty() -> None:
    claims = load_ledger()
    _assert_gap_eq(
        live_missing_falsifier(claims), KNOWN_MISSING_FALSIFIER, "Falsifier"
    )


def test_python_evidence_present_and_nonvacuous() -> None:
    claims = load_ledger()
    _assert_gap_eq(
        live_missing_python(claims), KNOWN_MISSING_PYTHON, "Python evidence"
    )


def test_lean_names_resolve_in_sources() -> None:
    claims = load_ledger()
    last, qualified = load_lean_decls()
    assert last, "no Lean declarations indexed — the source walk is broken"
    live = live_unresolved_lean(claims, last, qualified)
    extra = live - KNOWN_UNRESOLVED_LEAN
    stale = KNOWN_UNRESOLVED_LEAN - live
    assert extra == frozenset(), (
        "Lean names named in the ledger do not exist in lean4/: "
        + ", ".join(f"{cid}:{name}" for cid, name in sorted(extra))
    )
    assert stale == frozenset(), (
        "KNOWN_UNRESOLVED_LEAN is stale: "
        + ", ".join(f"{cid}:{name}" for cid, name in sorted(stale))
    )


def test_closed_class_vocabulary_is_the_header_list() -> None:
    header = LEDGER.read_text(encoding="utf-8").split("Shared assumptions", 1)[0]
    for word in CLOSED_CLASS:
        assert word in header, f"closed Class member {word!r} missing from header"


def _mini(body: str) -> Claim:
    return parse_claims("# Claim ledger\n\n### CL-X\n" + body + "\n")[0]


def test_parser_exact_class_is_in_vocabulary() -> None:
    c = _mini(
        "- **Statement**: s.\n"
        "- **Class**: theorem.\n"
        "- **Deps**: none. **Assumptions**: shared.\n"
        "- **Lean**: `foo`.\n"
        "- **Axioms**: --.\n"
        "- **Falsifier / boundary**: a countermodel.\n"
    )
    assert class_value(c) == "theorem"
    assert class_value(c) in CLOSED_CLASS
    assert not falsifier_is_missing(c)


def test_parser_qualified_class_is_outside_vocabulary() -> None:
    c = _mini("- **Class**: theorem (model-scoped).\n")
    assert class_value(c) == "theorem (model-scoped)"
    assert class_value(c) not in CLOSED_CLASS


def test_parser_inline_class_on_statement_line() -> None:
    c = _mini(
        "- **Statement**: horizon-free inertia. **Class**: theorem.\n"
        "- **Lean**: `silent_repetition_inert`.\n"
    )
    assert class_value(c) == "theorem"
    assert any(kind == "Lean" for kind, _ in c.field_list)


def test_qualified_lean_token_does_not_fall_back_to_short_name() -> None:
    last, qualified = load_lean_decls()
    assert "silent_repetition_inert" in last
    assert lean_name_resolves("silent_repetition_inert", last, qualified)
    assert not lean_name_resolves(
        "Bogus.silent_repetition_inert", last, qualified
    )


def test_field_text_aggregates_every_matching_field_in_source_order() -> None:
    evidence_then_lean = _mini(
        "- **Evidence**: `alpha_one`.\n- **Lean**: `beta_two`.\n"
    )
    lean_then_evidence = _mini(
        "- **Lean**: `beta_two`.\n- **Evidence**: `alpha_one`.\n"
    )
    assert lean_names_in(evidence_then_lean) == ["alpha_one", "beta_two"]
    assert lean_names_in(lean_then_evidence) == ["beta_two", "alpha_one"]


def test_parser_vacuous_python_counts_as_absent() -> None:
    present = _mini("- **Python**: `claims.json:CL-X`.\n")
    vacant = _mini("- **Python**: n/a (purely logical).\n")
    none = _mini("- **Python evidence**: none; Lean-only.\n")
    missing = _mini("- **Lean**: `foo`.\n")
    assert not python_is_vacuous(present)
    assert python_is_vacuous(vacant)
    assert python_is_vacuous(none)
    assert python_is_vacuous(missing)


def dump_ratchets() -> None:
    import json

    claims = load_ledger()
    last, qualified = load_lean_decls()
    groups = {
        "KNOWN_MISSING_STATEMENT": live_missing(claims, STATEMENT_KEYS),
        "KNOWN_MISSING_CLASS": live_missing_class(claims),
        "KNOWN_MISSING_DEPS": live_missing(claims, DEPS_KEYS),
        "KNOWN_MISSING_ASSUMPTIONS": live_missing(claims, ASSUMPTIONS_KEYS),
        "KNOWN_MISSING_LEAN": live_missing(claims, LEAN_KEYS),
        "KNOWN_MISSING_AXIOMS": live_missing(claims, AXIOM_KEYS),
        "KNOWN_MISSING_FALSIFIER": live_missing_falsifier(claims),
        "KNOWN_MISSING_PYTHON": live_missing_python(claims),
        "KNOWN_CLASS_OUTSIDE_VOCAB": live_class_outside(claims),
    }
    payload = {name: sorted(ids) for name, ids in groups.items()}
    unresolved = live_unresolved_lean(claims, last, qualified)
    payload["KNOWN_UNRESOLVED_LEAN"] = [list(p) for p in sorted(unresolved)]
    payload["KNOWN_CLAIM_IDS"] = [c.claim_id for c in claims]
    payload["claim_count"] = len(claims)
    print(json.dumps(payload, indent=2))
    print("class values outside:", file=sys.stderr)
    for c in claims:
        val = class_value(c)
        if val is not None and val not in CLOSED_CLASS:
            print(f"  {c.claim_id}: {val[:100]!r}", file=sys.stderr)


if __name__ == "__main__":
    if "--dump" in sys.argv:
        dump_ratchets()
    else:
        print("pass --dump to print KNOWN_* literals")
        sys.exit(1)
