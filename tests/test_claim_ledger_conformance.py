"""Schema conformance for ``paper/paper_claim_ledger.md``.

The ledger header declares required fields and a closed Class vocabulary.
Evidence-token resolution is a different gate
(``ci/check_ledger_evidence.py``).  This module checks record shape,
closed Class membership, falsifier presence, Python-evidence presence,
unique IDs, a frozen heading census, a frozen per-claim body pin, and
that every named Lean theorem exists as a declaration head in ``lean4/``.

Population and classification are independent.  The heading *population*
is CommonMark ATX h3 (``#{3}`` plus a space or tab, optional 0-3 leading
spaces) and never mentions ``CL-``.  The classifier extracts the ID.
A heading the classifier cannot place fails totality instead of vanishing
from both sides.  A tab-separated ``###\\\\tCL-…`` is a heading.

A field opener is not enough: Statement/Class/Falsifier/Deps/Assumptions
with no letter are missing.  Lean ``--`` is the declared none-sentinel.
Body pins catch a rewrite that keeps the field keys.

KNOWN_* ratchets freeze HEAD gaps so the suite is green.  Tests require
equality with the live gap sets: a new gap fails; an entry that no
longer fails must leave the set.  The body pin is a second equality
ratchet over content, not over IDs.
"""

from __future__ import annotations

import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEDGER = REPO / "paper" / "paper_claim_ledger.md"
LEAN_ROOT = REPO / "lean4"
AXIOMS = REPO / "artifacts" / "lean_axioms.txt"
BODY_PIN = REPO / "tests" / "claim_ledger_body_pin.txt"

# Population: CommonMark ATX h3.  Never mentions CL-.
ATX_H3 = re.compile(r"^ {0,3}#{3}[ \t]+")
# Classifier: extracts the ID.  Space and tab are both ATX separators.
HEADING = re.compile(r"^ {0,3}#{3}[ \t]+(?P<id>CL-[A-Za-z0-9-]+)")
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
# Inductive constructors: ``| name :`` or ``| name (args``.  Match-arms
# ``| name =>`` and ``| name x =>`` do not match.
CTOR_HEAD = re.compile(
    r"^\s*\|\s*\.?(?P<name>[A-Za-z_][A-Za-z0-9_']*)\s*(?::|\(|$)"
)
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

# A field with no letter is an empty slot, not content.  Lean/Axioms
# may use the declared none-sentinel ``--``.
LEAN_NONE = "--"
ROOT_WILDCARD_PREFIXES = frozenset({"Derivation.", "Derivation_"})


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


def _has_letter(text: str) -> bool:
    return re.search(r"[A-Za-z]", text) is not None


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
    if not has_field(claim, keys):
        return True
    body = field_text(claim, keys)
    if _has_letter(body):
        return False
    if keys & LEAN_KEYS or keys & AXIOM_KEYS:
        if _norm_body(body).rstrip(".") == LEAN_NONE:
            return False
    if "Statement" in keys and "**Statement" in claim.body:
        after = claim.body.split("**Statement", 1)[1]
        stop = re.search(r"\n- \*\*", after)
        chunk = after if stop is None else after[: stop.start()]
        return not _has_letter(chunk)
    return True


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
    return not _has_letter(field_text(claim, FALSIFIER_KEYS))


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


def strip_lean_comments(src: str) -> str:
    """Drop nested ``/- -/`` blocks and ``--`` line comments."""
    out: list[str] = []
    i = 0
    n = len(src)
    depth = 0
    while i < n:
        if depth == 0 and src.startswith("/-", i):
            depth = 1
            i += 2
            continue
        if depth > 0:
            if src.startswith("/-", i):
                depth += 1
                i += 2
                continue
            if src.startswith("-/", i):
                depth -= 1
                i += 2
                out.append(" ")
                continue
            i += 1
            continue
        if src.startswith("--", i):
            while i < n and src[i] != "\n":
                i += 1
            continue
        out.append(src[i])
        i += 1
    return "".join(out)


def index_lean_source(src: str, stem: str, rel: str) -> tuple[set[str], set[str]]:
    """Index declaration heads only.  Match-arms and comment words are not names."""
    last: set[str] = set()
    qualified: set[str] = set()
    ns_open = re.compile(r"^namespace\s+([A-Za-z_][A-Za-z0-9_.]*)")
    ns_end = re.compile(r"^end\s+([A-Za-z_][A-Za-z0-9_.]*)")
    stack: list[str] = []
    for line in strip_lean_comments(src).splitlines():
        opened = ns_open.match(line)
        if opened:
            stack.append(opened.group(1))
            continue
        closed = ns_end.match(line)
        if closed and stack and stack[-1] == closed.group(1):
            stack.pop()
            continue
        m = DECL.match(line) or CTOR_HEAD.match(line)
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
    return last, qualified


def load_lean_decls() -> tuple[frozenset[str], frozenset[str]]:
    """Return (last-segment names, file- and namespace-qualified names)."""
    last: set[str] = set()
    qualified: set[str] = set()
    for path in sorted(LEAN_ROOT.rglob("*.lean")):
        stem = path.stem
        rel = ".".join(path.relative_to(LEAN_ROOT).with_suffix("").parts)
        file_last, file_qual = index_lean_source(
            path.read_text(encoding="utf-8"), stem, rel
        )
        last |= file_last
        qualified |= file_qual
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
        if prefix in ROOT_WILDCARD_PREFIXES:
            return False
        return any(
            q == prefix or q.startswith(prefix) or ("." + prefix) in q
            for q in qualified
        )
    if "." in name:
        return name in qualified
    return name in last


def claim_fingerprint(claim: Claim) -> str:
    return hashlib.sha256(claim.body.encode("utf-8")).hexdigest()


def load_body_pin() -> dict[str, str]:
    pin: dict[str, str] = {}
    if not BODY_PIN.exists():
        return pin
    for line in BODY_PIN.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        cid, digest = line.split(" ", 1)
        pin[cid] = digest
    return pin


def render_body_pin(claims: list[Claim]) -> str:
    rows = [f"{c.claim_id} {claim_fingerprint(c)}" for c in claims]
    return "\n".join(rows) + "\n"


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
    'CL-G1-LOCAL-CLASS',
    'CL-G1-T5-GENERAL',
    'CL-G1-CAPACITY-APPLICATION',
    'CL-G1-CLASS-EXCLUSION',
    'CL-G1-FIVE-STRATEGIES',
    'CL-G1-G3-COUNTEREXAMPLE',
    'CL-G1-G4-FINITE',
    'CL-PD-TRANSPOSE',
    'CL-PD-INVENTORY',
    'CL-G1-TERMINAL-20260826',
    "CL-IDENTITY-NOT-PROFILE",
    "CL-TRANSITION-STEPS-VS-RESPONSE-ROUNDS",
    "CL-REGISTER-SCOPE",
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
    'CL-PD-INVENTORY',
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
    """Population: every CommonMark ATX h3.  This pattern never mentions CL-."""
    return [ln for ln in text.splitlines() if ATX_H3.match(ln)]


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


def test_claim_bodies_match_frozen_pin() -> None:
    claims = load_ledger()
    pin = load_body_pin()
    assert pin, "body pin is empty — the pin file is missing or unread"
    live = {c.claim_id: claim_fingerprint(c) for c in claims}
    extra = sorted(set(live) - set(pin))
    missing = sorted(set(pin) - set(live))
    changed = sorted(cid for cid in live.keys() & pin.keys() if live[cid] != pin[cid])
    assert extra == [], f"unpinned claim bodies: {extra}"
    assert missing == [], f"pinned claim IDs missing from the ledger: {missing}"
    assert changed == [], f"claim body changed: {changed}"


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


def test_match_arm_and_comment_words_are_not_declarations() -> None:
    src = (
        "/- that worth of carrying -/\n"
        "inductive Item where\n"
        "  | newRuleAll (form : Nat)\n"
        "  | admitTok (tok : Nat)\n"
        "theorem realName : True := by\n"
        "  cases x with\n"
        "  | exact => trivial\n"
        "  | inl => trivial\n"
        "  | admitTok t => trivial\n"
        "-- some step four n _\n"
    )
    last, qualified = index_lean_source(src, "Mod", "Derivation.Mod")
    assert "realName" in last
    assert "newRuleAll" in last
    assert "admitTok" in last
    for noise in ("exact", "cases", "inl", "some", "step", "four", "x", "n", "_",
                  "that", "worth", "of", "carrying"):
        assert noise not in last, noise
    assert "Mod.realName" in qualified


def test_root_namespace_wildcard_does_not_resolve() -> None:
    last, qualified = load_lean_decls()
    assert not lean_name_resolves("Derivation.*", last, qualified)
    assert lean_name_resolves("PresentationRelativity.*", last, qualified)


def test_injection_tab_heading_is_not_invisible() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    text += "###\tCL-ZZZ-SMUGGLED\n- **Statement**: smuggled.\n"
    atx = hash_heading_lines(text)
    ids = [m.group("id") for ln in atx if (m := HEADING.match(ln))]
    assert "CL-ZZZ-SMUGGLED" in ids
    unclassified = [ln for ln in atx if HEADING.match(ln) is None]
    assert unclassified == []
    assert tuple(ids) != KNOWN_CLAIM_IDS


def test_injection_empty_fields_are_missing_not_present() -> None:
    c = _mini(
        "- **Statement**: .\n"
        "- **Class**: .\n"
        "- **Deps**: .\n"
        "- **Assumptions**: .\n"
        "- **Lean**: .\n"
        "- **Axioms**: .\n"
        "- **Falsifier / boundary**: .\n"
    )
    assert missing_required(c, STATEMENT_KEYS)
    assert missing_required(c, CLASS_KEYS)
    assert missing_required(c, DEPS_KEYS)
    assert missing_required(c, ASSUMPTIONS_KEYS)
    assert missing_required(c, LEAN_KEYS)
    assert missing_required(c, AXIOM_KEYS)
    assert falsifier_is_missing(c)
    assert lean_names_in(c) == []


def test_injection_rewritten_inertia_body_breaks_the_pin() -> None:
    original = load_ledger()
    inertia = next(c for c in original if c.claim_id == "CL-0-INERTIA")
    lied = Claim(
        claim_id=inertia.claim_id,
        heading_line=inertia.heading_line,
        body=(
            "### CL-0-INERTIA\n"
            "- **Statement**: P = NP, and every claim in this ledger is a "
            "verified fact.\n"
            "- **Class**: theorem.\n"
            "- **Deps**: none. **Assumptions**: shared only.\n"
            "- **Python**: `challenges.json:challenge0`.\n"
            "- **Lean**: `supply_no_op`.\n"
            "- **Axioms**: `propext`.\n"
            "- **Falsifier / boundary**: nothing could refute this.\n"
        ),
        field_list=inertia.field_list,
    )
    pin = load_body_pin()
    assert pin.get("CL-0-INERTIA") == claim_fingerprint(inertia)
    assert claim_fingerprint(lied) != pin["CL-0-INERTIA"]


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
    if "--write-pin" in sys.argv:
        BODY_PIN.write_text(render_body_pin(claims), encoding="utf-8", newline="\n")
        payload["body_pin_path"] = str(BODY_PIN)
        payload["body_pin_rows"] = len(claims)
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
