"""Ultra closure run, Stage I: theorem inventory and dependency graph.

Classification: metatheory apparatus for
``paper/native_derivation_completion.md`` and
``paper/native_derivation_map.md``.

The inventory is source-derived, never transcribed: theorem names and
axiom sets come from ``artifacts/lean_axioms.txt``; statements are
extracted from the Lean sources; consuming modules and citing ledger
claims are found by search.  Only the kind/role labels are declared
metadata, and the tests pin them to exactly the exported estate (no
orphan, no phantom).

The dependency graph records every bridge of the final derivation
chain with one of the statuses
``PROVED / DECLARED / COMPUTED_WITHIN_BOUNDS / FALSE_WITH_COUNTERMODEL
/ OPEN`` and evidence references that the tests resolve against the
axioms artifact and the repository.
"""

from __future__ import annotations

import re
from functools import cache
from pathlib import Path

LEAN_DIR = Path("lean4") / "Derivation"
AXIOMS_FILE = Path("artifacts") / "lean_axioms.txt"
LEDGER_FILE = Path("paper") / "paper_claim_ledger.md"

DERIVATION_FILES = [
    "Basic.lean", "Inertia.lean", "Quot.lean", "Counting.lean",
    "Minimality.lean", "Progress.lean", "Erasure.lean", "Ext.lean",
    "CountTransport.lean", "Mention.lean", "TransitionTransport.lean",
    "MinimalityF.lean", "RuleBridge.lean", "Rounds.lean",
    # Parked modules that also open `namespace Derivation`.  They are outside
    # `Derivation.lean`'s import closure, so their theorems reached this
    # inventory only once `lean4/ParkedAudit.lean` began reporting them.
    "FormRenaming.lean", "FormTransport.lean",
    "IsoBridge.lean", "IsoCanon.lean", "IsoCollapse.lean",
]

NAMESPACE_FILES: dict[str, list[str]] = {
    "Derivation": DERIVATION_FILES,
    # Parked modules with namespaces of their own.  Deliberately absent from
    # NAMESPACE_DEFAULTS: they fall back to ("generic", "undeclared"), which
    # is the honest record for work the paper never classified, and is what
    # that role exists for.  Giving them a role here would assert a place in
    # the claim structure they do not have.
    "Composing": ["Composing.lean"],
    "DiffAnchor": ["DiffAnchor.lean"],
    # `Derivation.Iso` is a nested namespace: these files open `Derivation`
    # and then `Iso`, so a theorem in them is `Derivation.Iso.foo` while the
    # source reads `theorem foo`. Without this entry the search falls back to
    # ns `Derivation` and looks for `theorem Iso.foo`, which no file spells.
    "Derivation.Iso": ["IsoBridge.lean", "IsoCanon.lean", "IsoCollapse.lean"],
    "PrimDiff": ["PrimDiff.lean"],
    "ObserverInventory": ["ObserverInventory.lean"],
    "Bridge": ["Bridge.lean"],
    "Refusal": ["Refusal.lean"],
    "RefusalFrontier": ["RefusalFrontier.lean"],
    "Generator": ["Generator.lean"],
    "SeparationCapacity": ["SeparationCapacity.lean"],
    "LocalFiniteAlphabet": ["LocalStrategy.lean"],
    "G1Class": ["G1Class.lean"],
    "DiffInterface": ["DiffInterface.lean"],
    "Represented": ["Represented.lean"],
    "Completion": ["Completion.lean"],
    "NoOutside": ["NoOutside.lean"],
    "Constitution": ["Constitution.lean"],
    "Initiality": ["Initiality.lean"],
    "Horizon": ["Horizon.lean"],
    "PrimitiveCore": ["PrimitiveCore.lean"],
    "PrimitiveCats": ["PrimitiveCats.lean"],
    "PrimitiveContact": ["PrimitiveContact.lean"],
    "PrimitivePassage": ["PrimitivePassage.lean"],
    "HigherStructure": ["HigherStructure.lean"],
    "Apartness": ["Apartness.lean"],
    "InterpreterBoundary": ["InterpreterBoundary.lean"],
    "ControllerCategory": ["ControllerCategory.lean"],
    "Attachment": ["Attachment.lean"],
    "LadderGeneral": ["LadderGeneral.lean"],
    "Compression": ["Compression.lean"],
    "StableContent": ["StableContent.lean"],
    "RenamingStructure": ["RenamingStructure.lean"],
    "GraphGenesis": ["GraphGenesis.lean"],
    "BoundaryCancellation": ["BoundaryCancellation.lean"],
    "WeightProfile": ["WeightProfile.lean"],
    "TransitionAlphabet": ["TransitionAlphabet.lean"],
    "TraceAlgebra": ["TraceAlgebra.lean"],
    "ObsDescent": ["ObsDescent.lean"],
    "ContactBridge": ["ContactBridge.lean"],
    "ContactKernel": ["ContactKernel.lean"],
    "PresentationNaturality": ["PresentationNaturality.lean"],
    "Pigeonhole": ["Pigeonhole.lean"],
    "CapacityBound": ["CapacityBound.lean"],
    "PresentationRelativity": ["PresentationRelativity.lean"],
    "PresentationRelativity.Metatheory": ["PresentationRelativity.lean"],
    "ClosureSymmetry": ["ClosureSymmetry.lean"],
    "ResidualClosure": ["ResidualClosure.lean"],
    "PresentationDescent": ["PresentationDescent.lean"],
    "QuotientRetention": ["QuotientRetention.lean"],
    "FidelityClosure": ["FidelityClosure.lean"],
    "NoOutsideFidelity": ["NoOutsideFidelity.lean"],
    "EndogenousFidelityGenerator": ["EndogenousFidelityGenerator.lean"],
    "Breaking": ["Breaking.lean"],
}

VALID_KINDS = ("concrete", "generic", "bounded", "horizon-free")
VALID_ROLES = (
    "existence", "uniqueness", "minimality", "preservation",
    "termination", "example", "countermodel", "equivalence",
    "classification", "simulation",
    # The explicit absence of a classification.  Not a role a theorem
    # plays -- the honest record that its namespace has never been
    # classified.  See classify().
    "undeclared",
)

REFERENCE_MEMBER_SUFFIXES = ("1", "2", "mp", "mpr", "symm")

#: An optional same-line attribute before `theorem`, as in
#: `@[simp] theorem relabel_data ...`.  An attribute on its OWN line needs
#: nothing, because the `theorem` keyword still starts a line.
#:
#: This gap was latent, not new.  `Basic.lean` has carried `@[simp] theorem`
#: since long before the parked-module census, but the hand-maintained
#: `#print axioms` inventory in `lean4/Derivation.lean` never listed one, so
#: no report ever reached this pattern.  `lean4/ParkedAudit.lean` enumerates
#: from the compiled environment instead of by hand, which is exactly why it
#: surfaced: a complete population finds the holes a curated one hides.
ATTR_PREFIX = r"(?:@\[[^\]]*\][ \t]*)?"

#: Asserts a theorem name ENDED here, so `theorem foo` cannot match the source
#: line `theorem fooBar`.  A negative lookahead rather than a positive
#: terminator class, because it consumes nothing and so can be shared by a
#: pattern that stops at the name and one that goes on to capture a signature.
#:
#: The two patterns disagreeing is what made this necessary.  `source_module`
#: terminated the name with ``[\s({\[⟨]`` and `extract_statement` terminated it
#: with nothing at all, so every prefix-named pair silently mismatched: the
#: module was resolved from the right declaration and the statement copied from
#: whichever same-prefixed theorem appeared first.  Six records shipped that
#: way, among them `Derivation.cost1_insufficient` carrying
#: `cost1_insufficient_general`'s statement -- a theorem the claim ledger
#: cites.  `test_inventory_covers_axiom_artifact_exactly` could not see it: the
#: field was populated, just populated from the wrong theorem.
#:
#: `'`, `?` and `!` are excluded alongside `\w` because Lean admits them in
#: identifiers, so `foo` must not match `foo'` or `foo?` either.
DECL_END = r"(?![\w'?!])"


@cache
def lean_source(fname: str) -> str:
    """Read one immutable Lean source once per inventory process."""
    return (LEAN_DIR / fname).read_text(encoding="utf-8")


@cache
def ledger_claim_blocks() -> tuple[str, ...]:
    """Split the immutable claim ledger once per inventory process."""
    text = LEDGER_FILE.read_text(encoding="utf-8")
    return tuple(re.split(r"^### ", text, flags=re.MULTILINE)[1:])


@cache
def exported_final_counts() -> dict[str, int]:
    """Count exported theorem final components for shorthand resolution."""
    counts: dict[str, int] = {}
    for rec in parse_axiom_reports():
        final = str(rec["name"]).rpartition(".")[2]
        counts[final] = counts.get(final, 0) + 1
    return counts


def parse_axiom_reports() -> list[dict[str, object]]:
    """One record per exported theorem: qualified name and axiom set."""
    out: list[dict[str, object]] = []
    text = AXIOMS_FILE.read_text(encoding="utf-8")
    for line in text.splitlines():
        # Non-greedy: a primed theorem name ends in a quote, so the
        # blind [^']+ capture cannot parse its report and silently
        # skipped it. Found live 2026-08-18; same fix as the ci parsers.
        m = re.search(r"'(?P<name>.+?)' (?P<rest>(?:depends on axioms|does not depend).*)", line)
        if not m:
            continue
        name = m.group("name")
        rest = m.group("rest")
        if "does not depend" in rest:
            axioms: list[str] = []
        else:
            inner = re.search(r"\[(.*)\]", rest)
            axioms = (
                [a.strip() for a in inner.group(1).split(",")]
                if inner and inner.group(1) else []
            )
        out.append({"name": name, "axioms": axioms})
    return out


def declared_splits(qualified: str) -> list[tuple[str, str]]:
    """Candidate (namespace, declared-name) pairs: a theorem may be
    declared with a dotted name inside a shorter namespace (e.g.
    ``theorem Renaming.f_inj`` inside ``namespace Attachment``)."""
    parts = qualified.split(".")
    return [
        (".".join(parts[:cut]), ".".join(parts[cut:]))
        for cut in range(len(parts) - 1, 0, -1)
    ]


def source_module(qualified: str) -> str:
    """The Lean file that declares the theorem (searched, not guessed)."""
    for ns, decl in declared_splits(qualified):
        for fname in NAMESPACE_FILES.get(ns, []):
            path = LEAN_DIR / fname
            if not path.exists():
                continue
            if re.search(
                rf"^{ATTR_PREFIX}theorem {re.escape(decl)}{DECL_END}",
                lean_source(fname),
                re.MULTILINE,
            ):
                return fname
    return "UNRESOLVED"


def extract_statement(qualified: str, module: str) -> str:
    """The statement text from the source, up to the proof marker."""
    path = LEAN_DIR / module
    if not path.exists():
        return "UNRESOLVED"
    text = lean_source(module)
    for _, decl in declared_splits(qualified):
        m = re.search(
            rf"^{ATTR_PREFIX}theorem {re.escape(decl)}{DECL_END}"
            rf"(?P<sig>.*?)(?:[ \t]*:=|^[ \t]*\|)",
            text,
            re.MULTILINE | re.DOTALL,
        )
        if m:
            return re.sub(r"\s+", " ", m.group("sig")).strip()
    return "UNRESOLVED"


@cache
def qualified_reference_pattern(qualified: str) -> re.Pattern[str]:
    """Match qualified names and only known theorem-result members."""
    spellings = {qualified}
    for ns, decl in declared_splits(qualified):
        if ns in NAMESPACE_FILES and "." in decl:
            spellings.add(decl)
    alternatives = "|".join(
        re.escape(spelling)
        for spelling in sorted(spellings, key=len, reverse=True)
    )
    suffixes = "|".join(map(re.escape, REFERENCE_MEMBER_SUFFIXES))
    return re.compile(
        rf"(?<![\w.])(?:{alternatives})"
        rf"(?=(?:\.(?:{suffixes}))*(?![\w.]))"
    )


def _lean_code(text: str) -> str:
    """Replace comments and strings with spaces, preserving line breaks."""
    out: list[str] = []
    i = 0
    block_depth = 0
    in_line = False
    in_string = False
    escaped = False
    while i < len(text):
        pair = text[i : i + 2]
        char = text[i]
        if in_line:
            if char == "\n":
                in_line = False
                out.append(char)
            else:
                out.append(" ")
            i += 1
            continue
        if block_depth:
            if pair == "/-":
                block_depth += 1
                out.extend((" ", " "))
                i += 2
            elif pair == "-/":
                block_depth -= 1
                out.extend((" ", " "))
                i += 2
            else:
                out.append(char if char == "\n" else " ")
                i += 1
            continue
        if in_string:
            out.append(" ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            i += 1
            continue
        if pair == "--":
            in_line = True
            out.extend((" ", " "))
            i += 2
        elif pair == "/-":
            block_depth = 1
            out.extend((" ", " "))
            i += 2
        elif char == '"':
            in_string = True
            out.append(" ")
            i += 1
        else:
            out.append(char)
            i += 1
    return "".join(out)


@cache
def lean_module_code(fname: str) -> str:
    """Comment- and string-free code for one immutable Lean module."""
    return _lean_code(lean_source(fname))


def _declaring_namespace(qualified: str) -> str:
    for ns, _ in declared_splits(qualified):
        if ns in NAMESPACE_FILES:
            return ns
    return qualified.rpartition(".")[0]


def _namespace_is_current(namespace: str, code: str) -> bool:
    """True when `namespace` is entered, in either spelling Lean allows.

    A nested namespace has two spellings -- `namespace Derivation.Iso`, and
    `namespace Derivation` followed by `namespace Iso` -- and the sources here
    use the second. Matching only the dotted form made this test False in
    every module for `Derivation.Iso`, which silently disabled bare-name
    consumer detection for the six theorems in it: `consuming_modules` could
    only ever return the qualified-reference matches. The shipped
    `consumers: []` values were right only because every current reference is
    intra-module; the first sibling to use one of these theorems by its bare
    name -- the normal spelling inside that scope -- would have been recorded
    as consuming nothing.
    """
    dotted = re.escape(namespace)
    if re.search(rf"^[ \t]*namespace[ \t]+{dotted}(?:[ \t]|$)", code,
                 re.MULTILINE):
        return True
    parts = namespace.split(".")
    if len(parts) == 1:
        return False
    return all(
        re.search(rf"^[ \t]*namespace[ \t]+{re.escape(part)}(?:[ \t]|$)",
                  code, re.MULTILINE)
        for part in parts
    )


def _bare_reference_in_scope(qualified: str, code: str) -> bool:
    """Allow bare code references only where the namespace is current/open."""
    namespace = _declaring_namespace(qualified)
    if _namespace_is_current(namespace, code):
        return True
    for match in re.finditer(r"^[ \t]*open[ \t]+([^\n]+)", code,
                             re.MULTILINE):
        if namespace in match.group(1).split():
            return True
    return False


@cache
def _bare_reference_pattern(qualified: str) -> re.Pattern[str]:
    bare = re.escape(qualified.rpartition(".")[2])
    suffixes = "|".join(map(re.escape, REFERENCE_MEMBER_SUFFIXES))
    return re.compile(
        rf"(?<![\w.]){bare}(?=(?:\.(?:{suffixes}))*(?![\w.]))"
    )


@cache
def _ledger_reference_pattern(qualified: str) -> re.Pattern[str]:
    """Qualified names, plus globally unique backticked shorthand."""
    bare_name = qualified.rpartition(".")[2]
    bare = re.escape(bare_name)
    qualified_pattern = qualified_reference_pattern(qualified).pattern
    if exported_final_counts().get(bare_name) == 1:
        return re.compile(rf"(?:{qualified_pattern}|`(?:\.)?{bare}`)")
    return re.compile(qualified_pattern)


def consuming_modules(qualified: str, own_module: str) -> list[str]:
    """Every other module containing a resolved theorem reference."""
    qualified_pattern = qualified_reference_pattern(qualified)
    bare_pattern = _bare_reference_pattern(qualified)
    out = []
    for path in sorted(LEAN_DIR.glob("*.lean")):
        if path.name == own_module:
            continue
        code = lean_module_code(path.name)
        if qualified_pattern.search(code) or (
            _bare_reference_in_scope(qualified, code)
            and bare_pattern.search(code)
        ):
            out.append(path.name)
    return out


def citing_claims(qualified: str) -> list[str]:
    """Ledger claim IDs with qualified or unique backticked references."""
    pattern = _ledger_reference_pattern(qualified)
    out = []
    for block in ledger_claim_blocks():
        claim_id = block.splitlines()[0].strip()
        if pattern.search(block):
            out.append(claim_id)
    return out


# --------------------------------------------------------------------------
# Declared kind/role metadata.  Defaults per namespace; overrides where a
# theorem departs from its module's typical shape.  The tests pin exact
# coverage of the exported estate.
# --------------------------------------------------------------------------

NAMESPACE_DEFAULTS: dict[str, tuple[str, str]] = {
    "Derivation": ("generic", "preservation"),
    "PrimDiff": ("generic", "classification"),
    "ObserverInventory": ("generic", "classification"),
    "Bridge": ("generic", "classification"),
    "Refusal": ("concrete", "equivalence"),
    "RefusalFrontier": ("generic", "classification"),
    "Generator": ("horizon-free", "classification"),
    "DiffInterface": ("generic", "preservation"),
    "Represented": ("generic", "preservation"),
    "Completion": ("generic", "preservation"),
    "NoOutside": ("generic", "preservation"),
    "Constitution": ("generic", "simulation"),
    "Initiality": ("bounded", "minimality"),
    "Pigeonhole": ("generic", "preservation"),
    "CapacityBound": ("generic", "preservation"),
    # The two G1 namespaces were classified on arrival. Every exported
    # theorem is overridden below; these defaults are fail-safe metadata,
    # not a shortcut for silently assigning the same role to the surface.
    "LocalFiniteAlphabet": ("generic", "classification"),
    "G1Class": ("horizon-free", "countermodel"),
    "PresentationRelativity": ("generic", "classification"),
    "PresentationRelativity.Metatheory": ("generic", "classification"),
    "ClosureSymmetry": ("generic", "equivalence"),
    "ResidualClosure": ("generic", "classification"),
    "PresentationDescent": ("generic", "classification"),
    "QuotientRetention": ("generic", "classification"),
    "FidelityClosure": ("generic", "classification"),
    "NoOutsideFidelity": ("generic", "classification"),
    "EndogenousFidelityGenerator": ("generic", "classification"),
    # Classified on arrival rather than added to KNOWN_UNCLASSIFIED.
    # That list pins a debt of 24 legacy namespaces whose classification
    # is real work; this namespace has seven theorems written in the same
    # change, so declaring them is cheap and deferring would grow the
    # debt for no reason.  Every one is also overridden individually
    # below, so the default is a fallback, not the operative label.
    "Breaking": ("generic", "countermodel"),
}

KIND_ROLE_OVERRIDES: dict[str, tuple[str, str]] = {
    # genesis / inertia / erasure
    "Derivation.supply_no_op": ("generic", "preservation"),
    "Derivation.genesis_underivable": ("concrete", "countermodel"),
    "Derivation.underivable_of_empty": ("generic", "countermodel"),
    "Derivation.collapsed_of_no_insts": ("generic", "classification"),
    "Derivation.R2L_collapsed": ("concrete", "classification"),
    "Derivation.R2F_collapsed": ("concrete", "classification"),
    "Derivation.historyL_replays": ("concrete", "example"),
    "Derivation.historyF_replays": ("concrete", "example"),
    "Derivation.admission_without_expressive_increase":
        ("concrete", "countermodel"),
    "Derivation.separable_not_collapsed": ("generic", "classification"),
    "Derivation.quotient_barrier": ("generic", "classification"),
    "Derivation.quot_barrier": ("generic", "classification"),
    "Derivation.barrier_R2L": ("concrete", "classification"),
    "Derivation.index_le_strict_mono": ("generic", "termination"),
    "Derivation.strict_bounded_length": ("generic", "termination"),
    "Derivation.no_supply_round_bound": ("bounded", "termination"),
    "Derivation.allPairs_length": ("generic", "termination"),
    "Derivation.cost1_insufficient_general": ("generic", "minimality"),
    "Derivation.cost1_insufficient": ("concrete", "minimality"),
    "Derivation.cost1_insufficient_F": ("concrete", "minimality"),
    "Derivation.mu1_minimum_not_unique": ("concrete", "uniqueness"),
    "Derivation.mu2_unique": ("bounded", "uniqueness"),
    "Derivation.markK_pairwise_noniso": ("generic", "uniqueness"),
    "Derivation.mark_progress": ("generic", "existence"),
    "Derivation.erase_step": ("generic", "simulation"),
    "Derivation.erase_replay": ("generic", "simulation"),
    # primitive difference highlights
    "PrimDiff.D2_initial_pointed": ("generic", "uniqueness"),
    "PrimDiff.D2_not_pointed_iso_S2": ("concrete", "uniqueness"),
    "PrimDiff.bool_irrefl_witness_classification":
        ("concrete", "classification"),
    "PrimDiff.swap_carries_D2_to_D2rev": ("concrete", "classification"),
    "PrimDiff.swap_twice_restores_D2": ("concrete", "classification"),
    "PrimDiff.swap_twice_restores_D2rev": ("concrete", "classification"),
    "PrimDiff.sym_D2_eq_S2": ("concrete", "classification"),
    "PrimDiff.sym_D2rev_eq_S2": ("concrete", "classification"),
    "PrimDiff.swap_auto_of_S2_not_of_D2": ("concrete", "classification"),
    "PrimDiff.bool_irrefl_nonempty_classification":
        ("concrete", "classification"),
    "ObserverInventory.bool_irrefl_full_classification":
        ("concrete", "classification"),
    "ObserverInventory.witnesses_are_data":
        ("concrete", "existence"),
    "ObserverInventory.transpose_D2_eq_D2rev":
        ("concrete", "classification"),
    "ObserverInventory.transpose_ne_pushNot":
        ("concrete", "countermodel"),
    "ObserverInventory.collision_is_not_obstruction":
        ("generic", "countermodel"),
    "ObserverInventory.residuals_not_unique":
        ("concrete", "uniqueness"),
    "ObserverInventory.empty_ne_D2":
        ("concrete", "uniqueness"),
    "PrimDiff.symmetric_no_equivariant_classifier":
        ("concrete", "countermodel"),
    "PrimDiff.collapse_unobstructed_without_fidelity":
        ("generic", "countermodel"),
    "PrimDiff.witnessed_irrefl_on_every_larger_carrier":
        ("generic", "existence"),
    # bridge provenance
    "Bridge.second_token_required": ("generic", "countermodel"),
    "Bridge.irrefl_law_not_entailed": ("generic", "countermodel"),
    "Bridge.single_token_carrier_bound": ("horizon-free", "termination"),
    # refusal frontier highlights
    "RefusalFrontier.silent_repetition_inert":
        ("horizon-free", "preservation"),
    "RefusalFrontier.judgment_carrier_bound":
        ("horizon-free", "preservation"),
    "RefusalFrontier.equivariant_output_invariant":
        ("generic", "preservation"),
    "RefusalFrontier.reflective_chain_growth":
        ("horizon-free", "existence"),
    "RefusalFrontier.reflective_chain_is_initial_segment":
        ("horizon-free", "classification"),
    "RefusalFrontier.reflective_chain_successor_relation":
        ("horizon-free", "classification"),
    "RefusalFrontier.reflective_chain_irreflexive_facts":
        ("horizon-free", "classification"),
    "RefusalFrontier.min_witnessed_route_closes":
        ("concrete", "minimality"),
    "RefusalFrontier.histories_collapse": ("concrete", "countermodel"),
    # generator highlights
    "Generator.generation_never_dries": ("horizon-free", "existence"),
    "Generator.finite_marks_outrun": ("horizon-free", "countermodel"),
    "Generator.valued_marks_collapse_generation":
        ("horizon-free", "countermodel"),
    "Generator.depth2_separates_near_ends_n4": ("concrete", "example"),
    "Generator.depth2_obstruction_n5": ("concrete", "countermodel"),
    "Generator.middle_swap_not_relation_preserving":
        ("generic", "countermodel"),
    # difference interface highlights
    "DiffInterface.zeroRel_equivalence": ("generic", "equivalence"),
    "DiffInterface.bare_reflection_certifies_active_obstruction":
        ("generic", "existence"),
    "DiffInterface.drive_terminates": ("generic", "termination"),
    "DiffInterface.tower_fuel_terminates": ("generic", "termination"),
    "DiffInterface.bool_view_pigeonhole": ("generic", "countermodel"),
    "DiffInterface.no_bool_view_is_closed": ("generic", "countermodel"),
    "DiffInterface.cm_freshness": ("concrete", "countermodel"),
    "DiffInterface.cm_tagging": ("concrete", "countermodel"),
    "DiffInterface.cm_edge": ("concrete", "countermodel"),
    "DiffInterface.cm_hash": ("concrete", "countermodel"),
    "DiffInterface.cm_repetition": ("concrete", "countermodel"),
    # represented kernel highlights
    "Represented.represented_progress": ("generic", "existence"),
    "Represented.support_determines": ("generic", "preservation"),
    "Represented.worldAt_data": ("horizon-free", "classification"),
    "Represented.productive_run": ("horizon-free", "termination"),
    "Represented.wit_no_infinite": ("generic", "countermodel"),
    "Represented.scheduler_hidden": ("concrete", "countermodel"),
    "Represented.gensym_hidden": ("concrete", "countermodel"),
    "Represented.oracle_hidden": ("concrete", "countermodel"),
    "Represented.incomplete_search_false_alarm":
        ("concrete", "countermodel"),
    "Represented.augmentation_destroys_old_replay":
        ("concrete", "countermodel"),
    "Represented.repetition_not_progress": ("concrete", "countermodel"),
    "Represented.order_sensitivity_splits_equivalents":
        ("concrete", "countermodel"),
    "Represented.cert_not_correspondence": ("concrete", "countermodel"),
    "Represented.cert_panel_relative": ("concrete", "countermodel"),
    "Represented.worldAt_three_quiescent": ("concrete", "example"),
    "Represented.notes_inert": ("concrete", "example"),
    # choice-free counting and coloured separation capacity
    "Pigeonhole.nodup_length_le": ("generic", "termination"),
    "Pigeonhole.pigeonhole": ("generic", "existence"),
    "CapacityBound.encode_lt": ("generic", "classification"),
    "CapacityBound.encode_inj": ("generic", "uniqueness"),
    "CapacityBound.colourBall_length": ("generic", "classification"),
    "CapacityBound.capacity_bound": ("horizon-free", "countermodel"),
    "CapacityBound.capacity_at_one_colour": ("horizon-free", "example"),
    "CapacityBound.local_view_can_separate": ("concrete", "countermodel"),
    # general radius-one bridge and local finite-alphabet G1 class
    "SeparationCapacity.filter_range_decide_eq":
        ("generic", "classification"),
    "SeparationCapacity.filter_range_succ_eq":
        ("generic", "classification"),
    "SeparationCapacity.filter_range_eq": ("generic", "classification"),
    "SeparationCapacity.incoming_edges_interior":
        ("generic", "classification"),
    "SeparationCapacity.outgoing_edges_interior":
        ("generic", "classification"),
    "SeparationCapacity.profile2_interior":
        ("generic", "classification"),
    "SeparationCapacity.profileD_radius_one":
        ("generic", "classification"),
    "SeparationCapacity.radius_one_agrees_with_sealed_depth2":
        ("horizon-free", "equivalence"),
    "LocalFiniteAlphabet.profileCode_lt_eight":
        ("generic", "classification"),
    "LocalFiniteAlphabet.fires_every_strategy":
        ("horizon-free", "existence"),
    "LocalFiniteAlphabet.identityGrade_implies_clears":
        ("generic", "preservation"),
    "LocalFiniteAlphabet.strategy_capacity_collision":
        ("horizon-free", "countermodel"),
    "LocalFiniteAlphabet.finite_local_not_clears":
        ("horizon-free", "countermodel"),
    "LocalFiniteAlphabet.finite_local_not_identityGrade":
        ("horizon-free", "countermodel"),
    "LocalFiniteAlphabet.g1_local_finite_alphabet_class":
        ("horizon-free", "countermodel"),
    "LocalFiniteAlphabet.bare_finite": ("concrete", "classification"),
    "LocalFiniteAlphabet.presence_finite":
        ("concrete", "classification"),
    "LocalFiniteAlphabet.presence_eq_bare": ("concrete", "equivalence"),
    "LocalFiniteAlphabet.depthTwo_finite":
        ("concrete", "classification"),
    "LocalFiniteAlphabet.depthTwo_clears_n4": ("concrete", "example"),
    "LocalFiniteAlphabet.perPair_recurring":
        ("concrete", "classification"),
    "LocalFiniteAlphabet.perPair_identityGrade":
        ("horizon-free", "classification"),
    "LocalFiniteAlphabet.perPair_not_finite":
        ("horizon-free", "countermodel"),
    "LocalFiniteAlphabet.valued_oneTimeIdentity":
        ("horizon-free", "classification"),
    "LocalFiniteAlphabet.valued_not_finite":
        ("horizon-free", "countermodel"),
    "LocalFiniteAlphabet.valued_clears":
        ("horizon-free", "classification"),
    "LocalFiniteAlphabet.class_nonvacuity":
        ("horizon-free", "existence"),
    "LocalFiniteAlphabet.bare_not_identityGrade":
        ("concrete", "countermodel"),
    "LocalFiniteAlphabet.bare_classification":
        ("horizon-free", "classification"),
    "LocalFiniteAlphabet.presence_classification":
        ("horizon-free", "classification"),
    "LocalFiniteAlphabet.depthTwo_classification":
        ("horizon-free", "classification"),
    "G1Class.local_strategy_cycle_impossible":
        ("horizon-free", "countermodel"),
    "G1Class.g1_class_exclusion": ("horizon-free", "countermodel"),
    "G1Class.clears_does_not_imply_not_fires":
        ("horizon-free", "countermodel"),
    # presentation-relative identity and comparison-forced refinement
    "PresentationRelativity.presentationIdentity_iff_fiberIdentity":
        ("generic", "equivalence"),
    "PresentationRelativity.directionalResidual_refutes_identity":
        ("generic", "classification"),
    "PresentationRelativity.presentationIdentity_iff_residualEmpty":
        ("generic", "equivalence"),
    "PresentationRelativity.presentationIdentity_equivalence":
        ("generic", "equivalence"),
    "PresentationRelativity.self_comparison_has_empty_residual":
        ("generic", "preservation"),
    "PresentationRelativity.identityRelativeToQuestions_iff":
        ("generic", "equivalence"),
    "PresentationRelativity.splitsAt_iff_directionalResidualAt":
        ("generic", "equivalence"),
    "PresentationRelativity.family_enlargement_refines":
        ("generic", "preservation"),
    "PresentationRelativity.family_split_refuses_relative_identity":
        ("generic", "classification"),
    "PresentationRelativity.family_enlargement_split_is_strict":
        ("generic", "classification"),
    "PresentationRelativity.classCount_lt_of_refinement_split":
        ("generic", "minimality"),
    "PresentationRelativity.forced_split_of_factorization_failure":
        ("generic", "existence"),
    "PresentationRelativity.jointPresentation_factors_left":
        ("generic", "preservation"),
    "PresentationRelativity.jointPresentation_factors_right":
        ("generic", "preservation"),
    "PresentationRelativity.jointPresentation_strict_of_factorization_failure":
        ("generic", "existence"),
    "PresentationRelativity.directionalResidual_of_factorization_failure":
        ("generic", "existence"),
    "PresentationRelativity.Metatheory."
    "attempted_absolute_identification_collapses_to_equality":
        ("generic", "equivalence"),
    "PresentationRelativity.Metatheory."
    "attempted_absolute_polarities_are_refuted":
        ("generic", "countermodel"),
    "PresentationRelativity.world_eq_iff_support_eq_and_notes_eq":
        ("generic", "equivalence"),
    "PresentationRelativity.supportNotesView_injective":
        ("generic", "uniqueness"),
    "PresentationRelativity.support_identifies_while_supportNotes_separates":
        ("generic", "classification"),
    "PresentationRelativity.notes_update_kernel_results_agree":
        ("generic", "preservation"),
    "PresentationRelativity.panelEquiv_antitone":
        ("generic", "preservation"),
    "PresentationRelativity.panel_members_preserved_by_extension":
        ("generic", "preservation"),
    "PresentationRelativity.panel_extension_refines_equivalence":
        ("generic", "preservation"),
    "PresentationRelativity.certNeg_extension_implies_source":
        ("generic", "preservation"),
    "PresentationRelativity.panel_extension_changes_verdict_not_world":
        ("concrete", "countermodel"),
    "PresentationRelativity.encodeDepthOneProfile_injective":
        ("concrete", "uniqueness"),
    "PresentationRelativity.depthOnePresentation_eq_iff":
        ("generic", "equivalence"),
    "PresentationRelativity."
    "declared_generator_index_comparison_does_not_factor":
        ("horizon-free", "countermodel"),
    "PresentationRelativity."
    "declared_generator_index_comparison_forces_refinement":
        ("horizon-free", "existence"),
    "PresentationRelativity.declared_generator_profiles_disagree_at_pair":
        ("horizon-free", "countermodel"),
    # closure failure as loss of invariance under an internal symmetry
    "ClosureSymmetry.transpose_left": ("generic", "classification"),
    "ClosureSymmetry.transpose_right": ("generic", "classification"),
    "ClosureSymmetry.transpose_fixed": ("generic", "classification"),
    "ClosureSymmetry.transpose_involutive": ("generic", "equivalence"),
    "ClosureSymmetry.residual_nonempty_iff_internal_symmetry_break_nonempty":
        ("generic", "equivalence"),
    "ClosureSymmetry.residual_refutes_factorization":
        ("generic", "countermodel"),
    "ClosureSymmetry.closure_failure_iff_internal_symmetry_break":
        ("generic", "equivalence"),
    # current closure and loss of generating symmetry
    "ResidualClosure.factorization_preserves_invariance":
        ("generic", "preservation"),
    "ResidualClosure.carrying_right_face_loses_generating_invariance":
        ("generic", "classification"),
    "ResidualClosure.carrying_right_face_splits_generating_pair":
        ("generic", "classification"),
    "ResidualClosure.common_refinement_strictly_splits_left_face":
        ("generic", "minimality"),
    "ResidualClosure.current_directional_residual_is_empty":
        ("generic", "classification"),
    "ResidualClosure.current_internal_symmetry_break_is_empty":
        ("generic", "classification"),
    "ResidualClosure.common_refinement_closes_current_obstruction":
        ("generic", "preservation"),
    # heterogeneous descent and faithful index erasure
    "PresentationDescent.translation_gap_refuses_totalization":
        ("generic", "countermodel"),
    "PresentationDescent.coherence_residual_refutes_round_trip":
        ("generic", "classification"),
    "PresentationDescent.faithful_common_descent_has_coincident_images":
        ("generic", "preservation"),
    "PresentationDescent.faithful_descent_to_coherent":
        ("generic", "preservation"),
    "PresentationDescent.faithful_descent_iff_round_trip_coherent":
        ("generic", "equivalence"),
    "PresentationDescent.incoherence_forces_index_retention":
        ("generic", "classification"),
    "PresentationDescent.residual_forces_index_retention":
        ("generic", "classification"),
    # quotient retention
    "QuotientRetention.RelationRefinement.refl":
        ("generic", "preservation"),
    "QuotientRetention.RelationRefinement.trans":
        ("generic", "preservation"),
    "QuotientRetention.collapseMap_mk": ("generic", "preservation"),
    "QuotientRetention.collapseMap_surjective": ("generic", "existence"),
    "QuotientRetention.failed_identification_retains_two_classes":
        ("generic", "countermodel"),
    "QuotientRetention.failed_identification_makes_collapse_noninjective":
        ("generic", "countermodel"),
    "QuotientRetention.collapseMap_injective_iff_reverse_refinement":
        ("generic", "equivalence"),
    "QuotientRetention.symmetry_failure_retains_multiplicity":
        ("generic", "classification"),
    "QuotientRetention.collapseMap_compose": ("generic", "preservation"),
    # fidelity closure, loop transport, and presentation-relative labels
    "FidelityClosure.fidelity_refl": ("generic", "preservation"),
    "FidelityClosure.fidelity_symm": ("generic", "preservation"),
    "FidelityClosure.fidelity_trans": ("generic", "preservation"),
    "FidelityClosure.class_eq_iff_coherent_path": ("generic", "equivalence"),
    "FidelityClosure.no_coherent_path_retains_indices":
        ("generic", "classification"),
    "FidelityClosure.failed_endomorphism_does_not_refute_self_fidelity":
        ("generic", "countermodel"),
    "FidelityClosure.holonomy_residual_refuses_faithful_network_descent":
        ("generic", "countermodel"),
    "FidelityClosure.faithful_network_descent_forces_trivial_loops":
        ("generic", "preservation"),
    "FidelityClosure.label_descends_iff_fidelity_invariant":
        ("generic", "equivalence"),
    "FidelityClosure.coherent_disagreement_refuses_label_descent":
        ("generic", "classification"),
    "FidelityClosure.polarity_flip_is_presentation_relative":
        ("generic", "classification"),
    # operational no-outside witness
    "NoOutsideFidelity.support_fiber_contains_distinct_notes":
        ("concrete", "countermodel"),
    "NoOutsideFidelity.support_projection_not_injective":
        ("concrete", "countermodel"),
    "NoOutsideFidelity.support_translation_never_round_trip_coherent":
        ("generic", "countermodel"),
    "NoOutsideFidelity.support_translation_never_faithfully_erases_index":
        ("generic", "classification"),
    "NoOutsideFidelity.no_support_inverse_faithfully_erases_index":
        ("generic", "countermodel"),
    "NoOutsideFidelity.notes_fiber_has_no_operational_authority":
        ("generic", "preservation"),
    # least coherent closure as endogenous generator
    "EndogenousFidelityGenerator.admitted_step_has_fidelity_path":
        ("generic", "existence"),
    "EndogenousFidelityGenerator.fidelity_is_least_equivalence_containing_admitted_steps":
        ("generic", "minimality"),
    "EndogenousFidelityGenerator.fidelity_refines_indiscrete":
        ("generic", "preservation"),
    "EndogenousFidelityGenerator.universalCollapse_surjective":
        ("generic", "existence"),
    "EndogenousFidelityGenerator.no_coherent_path_retains_multiplicity":
        ("generic", "classification"),
    "EndogenousFidelityGenerator.generated_structure_is_failed_erasure":
        ("generic", "classification"),
    # equivariance obstruction
    "Breaking.no_orbit_constant_equivariant_endomap":
        ("generic", "countermodel"),
    "Breaking.no_orbit_constant_equivariant_selector":
        ("generic", "countermodel"),
    "Breaking.no_selector_of_no_common_fixed_point":
        ("generic", "countermodel"),
    "Breaking.no_common_fixed_point": ("generic", "classification"),
    "Breaking.no_fixed_point_free_involution_on_Tri":
        ("concrete", "countermodel"),
    "Breaking.selector_exists_at_common_fixed_point":
        ("generic", "existence"),
    "Breaking.selector_iff_common_fixed_point": ("generic", "equivalence"),
}


#: Modules whose theorems have never been classified, but which declare into
#: a namespace that HAS a default.  Without this, joining such a module to
#: `DERIVATION_FILES` silently stamps every theorem in it with that namespace's
#: role -- and the namespace pin cannot see it, because the pin compares
#: NAMESPACE_FILES keys against NAMESPACE_DEFAULTS keys and no new key appears.
#:
#: That happened here.  Adding the five parked modules below routed 31 of the
#: 48 newly reported theorems into `Derivation`'s ("generic", "preservation"),
#: which is the exact false-role shape deleted on 2026-08-18 and re-labelled
#: `Derivation.sortPair_comm` (a commutativity) and `Derivation.plug_args_lt`
#: (a strict bound) as preservation results.  A role is a positive assertion
#: about what a theorem DOES; none of these was ever asserted by anyone.
#:
#: Pinned by `test_unclassified_modules_are_pinned`, so this set may shrink but
#: not grow unnoticed.
UNCLASSIFIED_MODULES: frozenset[str] = frozenset({
    "FormRenaming.lean",
    "FormTransport.lean",
    "IsoBridge.lean",
    "IsoCanon.lean",
    "IsoCollapse.lean",
})


def classify(qualified: str, module: str | None = None) -> tuple[str, str]:
    if qualified in KIND_ROLE_OVERRIDES:
        return KIND_ROLE_OVERRIDES[qualified]
    if module in UNCLASSIFIED_MODULES:
        return ("generic", "undeclared")
    ns = qualified.rpartition(".")[0]
    # No silent default role.  An undeclared namespace previously came
    # back ("generic", "preservation") -- a positive assertion about what
    # the theorem DOES, applied to 912 of the 1417 exported theorems,
    # none of which had ever been classified.  "generic" is the honest
    # weakest kind and is kept; the role is now the explicit absence, and
    # test_every_namespace_declares_a_default fails while any namespace
    # is unclassified.  This deletes a false label; it does not invent a
    # true one.
    return NAMESPACE_DEFAULTS.get(ns, ("generic", "undeclared"))


def inventory() -> list[dict[str, object]]:
    out = []
    for rec in parse_axiom_reports():
        name = str(rec["name"])
        module = source_module(name)
        kind, role = classify(name, module)
        out.append(
            {
                "name": name,
                "module": module,
                "statement": extract_statement(name, module),
                "axioms": rec["axioms"],
                "kind": kind,
                "role": role,
                "consumers": consuming_modules(name, module),
                "citing_claims": citing_claims(name),
            }
        )
    return out


# --------------------------------------------------------------------------
# The dependency graph: notion nodes and classified bridges.
# Statuses reflect the state of the estate at the END of this run;
# every evidence reference is resolved by the tests.
# --------------------------------------------------------------------------

NODES = [
    "seed", "supply", "admission", "retention", "two-ness",
    "witnessed relation", "irreflexivity fact", "irreflexivity law",
    "orientation", "observer/difference map", "Zero/ZeroRel",
    "protected requirement", "active obstruction", "response menu",
    "exhaustion certificate", "same-level repair", "extension proposal",
    "extension execution", "replay", "support", "budget", "license",
    "refusal", "terminal", "certification panel", "next-event source",
    "kernel constitution",
]

# Each bridge: source, relation, target, status, evidence (Lean theorem
# names, artifact keys, or DECLARED:<where>), boundary note.
BRIDGES: list[dict[str, object]] = [
    {
        "source": "seed", "relation": "forces successor state",
        "target": "admission", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Derivation.genesis_underivable",
                     "Derivation.supply_no_op"],
        "boundary": "nothing follows from the seed alone; admission is "
                    "a separate represented event",
    },
    {
        "source": "supply", "relation": "is",
        "target": "admission", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Derivation.supply_no_op"],
        "boundary": "supply never mutates admitted state",
    },
    {
        "source": "admission", "relation": "changes state via event",
        "target": "retention", "status": "PROVED",
        "evidence": ["Derivation.historyL_replays",
                     "Derivation.historyF_replays"],
        "boundary": "event-indexed, replayable",
    },
    {
        "source": "seed", "relation": "yields",
        "target": "two-ness", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Bridge.single_token_carrier_bound",
                     "Bridge.second_token_required"],
        "boundary": "one deduplicated token bounds the carrier at one",
    },
    {
        "source": "admission", "relation": "priced routes to",
        "target": "two-ness", "status": "PROVED",
        "evidence": ["RefusalFrontier.min_witnessed_route_closes",
                     "Refusal.reifyUntagged_eq_occurrence"],
        "boundary": "three tied purchases: second token / occurrence / "
                    "reification (order-dependent winners)",
    },
    {
        "source": "two-ness", "relation": "yields",
        "target": "witnessed relation", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Bridge.no_forms_no_witness"],
        "boundary": "the relation channel is a separate purchase",
    },
    {
        "source": "admission", "relation": "priced relation route to",
        "target": "witnessed relation", "status": "PROVED",
        "evidence": ["RefusalFrontier.min_witnessed_route_closes"],
        "boundary": "unique minimum in the 44-protocol class under both "
                    "declared cost orders",
    },
    {
        "source": "witnessed relation", "relation": "born off-diagonal",
        "target": "irreflexivity fact", "status": "PROVED",
        "evidence": ["RefusalFrontier.reflective_chain_irreflexive_facts"],
        "boundary": "horizon-free on the chain; class-general form is "
                    "bounded computation",
    },
    {
        "source": "irreflexivity fact", "relation": "entails",
        "target": "irreflexivity law", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Bridge.irrefl_law_not_entailed",
                     "RefusalFrontier.bridge_facts_not_law"],
        "boundary": "the law is always a separate declaration",
    },
    {
        "source": "irreflexivity law", "relation": "declared as",
        "target": "protected requirement", "status": "DECLARED",
        "evidence": ["DECLARED:DiffInterface.Stage.guarded",
                     "DECLARED:Represented.World.reqs"],
        "boundary": "protection is a fidelity commitment, never entailed",
    },
    {
        "source": "two-ness", "relation": "equivariantly yields",
        "target": "orientation", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["PrimDiff.symmetric_no_equivariant_classifier",
                     "RefusalFrontier.equivariant_output_invariant"],
        "boundary": "the invariance ceiling; bypass requires a priced "
                    "asymmetry (tag/relation/position)",
    },
    {
        "source": "admission", "relation": "priced asymmetry yields",
        "target": "orientation", "status": "PROVED",
        "evidence": ["RefusalFrontier.priced_bridge_oriented"],
        "boundary": "orientation cost relocated to the declaration, "
                    "never eliminated",
    },
    {
        "source": "observer/difference map", "relation": "declared with laws",
        "target": "Zero/ZeroRel", "status": "PROVED",
        "evidence": ["DiffInterface.zeroRel_equivalence"],
        "boundary": "equivalence proved before any quotient; kernel "
                    "observers inherit the laws",
    },
    {
        "source": "Zero/ZeroRel", "relation": "with retention+protection is",
        "target": "active obstruction", "status": "PROVED",
        "evidence":
            ["DiffInterface.bare_reflection_certifies_active_obstruction",
             "DiffInterface.no_guard_no_obstruction"],
        "boundary": "conjunction of three separated conditions; every "
                    "proper subset realized without it",
    },
    {
        "source": "protected requirement", "relation": "necessary for",
        "target": "active obstruction", "status": "PROVED",
        "evidence": ["DiffInterface.no_guard_no_obstruction",
                     "PrimDiff.collapse_unobstructed_without_fidelity"],
        "boundary": "no fidelity, no obstruction: collapse alone is "
                    "admissible",
    },
    {
        "source": "active obstruction", "relation": "checked against",
        "target": "response menu", "status": "DECLARED",
        "evidence": ["DECLARED:Represented.responseMenu"],
        "boundary": "the menu is part of the fixed kernel constitution",
    },
    {
        "source": "response menu", "relation": "exhaustive failure gives",
        "target": "exhaustion certificate", "status": "PROVED",
        "evidence": ["Represented.incomplete_search_false_alarm"],
        "boundary": "obstruction requires exhaustive failure by "
                    "definition; truncated search falsely certifies",
    },
    {
        "source": "active obstruction", "relation": "dichotomy (refusal parallel)",
        "target": "same-level repair", "status": "PROVED",
        "evidence": ["Represented.represented_progress",
                     "Completion.rule1_repair_or_extension"],
        "boundary": "repair family nonempty, or certificate + accepted "
                    "augmentation, or recordable refusal; conditional on "
                    "WF and the fixed constitution",
    },
    {
        "source": "exhaustion certificate", "relation": "forces",
        "target": "extension proposal", "status": "PROVED",
        "evidence": ["Represented.represented_progress",
                     "DiffInterface.no_bool_view_is_closed"],
        "boundary": "canonical augmentation accepted; in bounded "
                    "grammars only a proposal is possible",
    },
    {
        "source": "extension proposal", "relation": "executes without authorization",
        "target": "extension execution", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Represented.progress_needs_license",
                     "Represented.progress_needs_budget"],
        "boundary": "authorization and budget are represented gates; "
                    "proposals never self-execute",
    },
    {
        "source": "same-level repair", "relation": "preserves satisfied",
        "target": "replay", "status": "PROVED",
        "evidence": ["Represented.step_mark_sound",
                     "Represented.aug_preserves_satisfied"],
        "boundary": "positive-satisfaction preservation, not full "
                    "observational conservativity",
    },
    {
        "source": "replay", "relation": "factors through",
        "target": "support", "status": "PROVED",
        "evidence": ["Represented.support_determines",
                     "NoOutside.support_replay"],
        "boundary": "operational-support factorization, extended to "
                    "histories, families, verdicts this run",
    },
    {
        "source": "budget", "relation": "gates",
        "target": "same-level repair", "status": "PROVED",
        "evidence": ["Represented.progress_needs_budget"],
        "boundary": "represented fuel; setBudget is a history event",
    },
    {
        "source": "license", "relation": "gates",
        "target": "extension execution", "status": "PROVED",
        "evidence": ["Represented.progress_needs_license"],
        "boundary": "represented authorization",
    },
    {
        "source": "exhaustion certificate", "relation": "recordable as",
        "target": "refusal", "status": "PROVED",
        "evidence": ["Represented.refusal_needs_certificate",
                     "Represented.refusals_are_represented"],
        "boundary": "refusal only with a verified certificate",
    },
    {
        "source": "refusal", "relation": "terminalizes the run",
        "target": "terminal", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Completion.refusal_non_absorbing"],
        "boundary": "refusal is a status record, non-absorbing; run "
                    "termination belongs to the history producer",
    },
    {
        "source": "certification panel", "relation": "certifies up to",
        "target": "Zero/ZeroRel", "status": "PROVED",
        "evidence": ["Represented.cert_scope",
                     "Represented.cert_not_correspondence",
                     "NoOutside.panel_equiv"],
        "boundary": "panel-relative warrant = joint quotient closure; "
                    "never correspondence; panel now replay-integrable",
    },
    {
        "source": "next-event source", "relation": "internalized as policy",
        "target": "replay", "status": "PROVED",
        "evidence": ["Constitution.driver_reproduces_tower",
                     "Constitution.nextFamily_complete"],
        "boundary": "relative to a fixed interpreter; the policy and its "
                    "outputs are represented, the interpreter is "
                    "constitution",
    },
    {
        "source": "kernel constitution", "relation": "represented as data",
        "target": "next-event source", "status": "PROVED",
        "evidence": ["Constitution.interp_describe"],
        "boundary": "a declared constitution family is describable and "
                    "executable relative to the fixed family "
                    "interpreter; the outermost interpreter remains "
                    "metatheory",
    },
    {
        "source": "kernel constitution", "relation": "interprets itself absolutely",
        "target": "kernel constitution", "status": "OPEN",
        "evidence": ["DECLARED:Constitution stratification boundary"],
        "boundary": "the named irreducible obligation: the family "
                    "interpreter is not a member of its own described "
                    "family; absolute self-interpretation unformulated",
    },
]

VALID_STATUSES = (
    "PROVED", "DECLARED", "COMPUTED_WITHIN_BOUNDS",
    "FALSE_WITH_COUNTERMODEL", "OPEN",
)


def dependency_graph() -> dict[str, object]:
    return {
        "nodes": NODES,
        "bridges": BRIDGES,
        "statuses": {
            s: sum(1 for b in BRIDGES if b["status"] == s)
            for s in VALID_STATUSES
        },
    }


# --------------------------------------------------------------------------
# Stage V mirror: represented scheduler, driver, constitution family
# --------------------------------------------------------------------------

from dataclasses import replace as _replace  # noqa: E402

from derivation.represented import (  # noqa: E402
    GENESIS,
    Event,
    World,
    aug_apply,
    aug_ok,
    hist_up_to,
    mark_apply,
    mark_ok,
    obstructed,
    quiescent,
    repair_family,
    replay,
    req_ok,
    step,
    viol,
    wf,
)


def fresh_name(w: World) -> int:
    """Canonical numeral: a priced import of arithmetic and ordering."""
    return len(w.data)


def tower_block(w: World) -> list[Event]:
    k = fresh_name(w)
    return [("setBudget", 1), ("admit", k), ("require", 0, k),
            ("addView", (k,))]


def aug_family(w: World, r: tuple[int, int]) -> list[tuple[int, ...]]:
    return [c for c in [(r[0],), (r[1],)] if aug_ok(w, c)]


def close_blocks(w: World) -> list[list[Event]]:
    out: list[list[Event]] = []
    for r in w.reqs:
        if viol(w, r):
            for (v, p) in repair_family(w, r):
                out.append([("mark", v, p)])
            for c in aug_family(w, r):
                out.append([("addView", c)])
    return out


def next_family(w: World, policy: str) -> list[list[Event]]:
    if policy == "idle":
        return []
    if policy == "tower":
        return [tower_block(w)]
    assert policy == "close"
    return close_blocks(w)


def tower_gen(k: int) -> list[Event]:
    h: list[Event] = [("admit", 0)]
    for _ in range(k):
        h.extend(tower_block(replay(h)))
    return h


PIGEON: list[Event] = [
    ("setBudget", 9), ("admit", 10), ("admit", 20), ("admit", 30),
    ("require", 0, 1), ("require", 0, 2), ("require", 1, 2),
    ("addView", (0,)),
]


def protocols_report(rounds: int = 15) -> dict[str, object]:
    """G0-G2: the driver reproduces the previously supplied stream;
    families are complete and tie-retained; the stop outcome is the
    empty family."""
    reproduces = all(
        tower_gen(k) == hist_up_to(k) for k in range(rounds + 1)
    )
    accepted = []
    for k in range(rounds + 1):
        w = GENESIS
        ok = True
        for e in tower_gen(k):
            w2 = step(w, e)
            if w2 == w:
                ok = False
            w = w2
        accepted.append(ok and quiescent(w) and wf(w))
    pigeon = replay(PIGEON)
    blocks = close_blocks(pigeon)
    both_orientations = (
        [("addView", (1,))] in blocks and [("addView", (2,))] in blocks
    )
    quiet = replay(hist_up_to(4))
    return {
        "G0_supplied_stream": "hist_up_to (metatheoretic producer)",
        "G1_family_singleton_per_stage": True,
        "G2_driver_reproduces_supplied_stream": reproduces,
        "G2_all_stages_accepted_quiescent_wf": all(accepted),
        "close_family_retains_both_orientations": both_orientations,
        "close_family_size_on_pigeonhole": len(blocks),
        "stop_outcome_empty_family": next_family(quiet, "close") == [],
        "fresh_name_source": "canonical numeral (arithmetic/ordering "
                             "import, recorded)",
        "fresh_name_fresh_along_run": all(
            fresh_name(replay(tower_gen(k)))
            not in replay(tower_gen(k)).data
            for k in range(rounds + 1)
        ),
        "generation_scope": "state-derived, prefix-compatible "
                            "generation under metatheoretic iteration "
                            "and a fixed interpreter",
    }


# --------------------------------------------------------------------------
# Constitution family and the fixed family interpreter (mirror)
# --------------------------------------------------------------------------

Desc = tuple[bool, bool, bool, bool, bool, bool]
KERNEL_DESC: Desc = (True, True, True, True, True, True)
DESC_FIELDS = ("dedupAdmit", "guardRequire", "guardAccept",
               "gateBudget", "gateLicense", "certRefusal")


def all_descs() -> list[Desc]:
    out: list[Desc] = []
    for n in range(64):
        bits = (bool(n & 1), bool(n & 2), bool(n & 4),
                bool(n & 8), bool(n & 16), bool(n & 32))
        out.append(bits)
    return out


def interp_step(d: Desc, w: World, e: Event) -> World:
    """Nat-domain guards are unconditional: a disabled guard toggle
    never licenses a negative state, matching the Lean carrier (where
    negatives are unrepresentable) for every constitution descriptor.
    Budget decrements saturate at zero (``max(0, budget - 1)``),
    matching Lean ``Nat`` subtraction exactly — the gateBudget toggle
    only controls whether a zero budget blocks the event, never
    whether the decrement may underflow (PR #12 correction C10)."""
    dedup, greq, gacc, gbud, glic, gcert = d
    kind = e[0]
    if kind == "admit":
        t = e[1]
        assert isinstance(t, int)
        if t < 0 or (dedup and t in w.data):
            return w
        return _replace(w, data=w.data + (t,))
    if kind == "require":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        if i < 0 or j < 0:
            return w
        if (not greq) or req_ok(w, i, j):
            return _replace(w, reqs=w.reqs + ((i, j),))
        return w
    if kind == "mark":
        v, p = e[1], e[2]
        assert isinstance(v, tuple) and isinstance(p, int)
        if p < 0 or any(x < 0 for x in v):
            return w
        if ((not gacc) or mark_ok(w, v, p)) and (
                (not gbud) or w.budget > 0):
            return _replace(mark_apply(w, v, p),
                            budget=max(0, w.budget - 1))
        return w
    if kind == "addView":
        c = e[1]
        assert isinstance(c, tuple)
        if any(x < 0 for x in c):
            return w
        if (((not gacc) or aug_ok(w, c))
                and ((not glic) or w.aug_licensed)
                and ((not gbud) or w.budget > 0)):
            return _replace(aug_apply(w, c),
                            budget=max(0, w.budget - 1))
        return w
    if kind == "refuse":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        if i < 0 or j < 0:
            return w
        if ((not gcert) or obstructed(w, (i, j))) and (
                (i, j) not in w.refusals):
            return _replace(w, refusals=w.refusals + ((i, j),))
        return w
    return step(w, e)


DUP_WORLD = World(data=(5,), budget=9)
SAT_WORLD = World(data=(10, 20), views=((0,),), reqs=((0, 1),), budget=9)
BROKE_WORLD = World(data=(10, 20), views=((),), reqs=((0, 1),), budget=0)
UNLIC_WORLD = World(data=(10, 20), views=((),), reqs=((0, 1),),
                    budget=9, aug_licensed=False)

PROBES: list[tuple[str, World, Event]] = [
    ("dedup", DUP_WORLD, ("admit", 5)),
    ("require_guard", DUP_WORLD, ("require", 0, 0)),
    ("accept_guard", SAT_WORLD, ("mark", (0,), 1)),
    ("budget_gate", BROKE_WORLD, ("mark", (), 0)),
    ("license_gate", UNLIC_WORLD, ("addView", (0,))),
    ("refusal_certificate", SAT_WORLD, ("refuse", 0, 1)),
]


def probe_results(d: Desc) -> dict[str, bool]:
    return {
        name: interp_step(d, w, e) == w for (name, w, e) in PROBES
    }


def compliant(d: Desc) -> bool:
    return all(probe_results(d).values())


def cost_capabilities(d: Desc) -> int:
    return sum(1 for b in d if b)


def cost_lex(d: Desc) -> tuple[int, int]:
    return (sum(1 for b in d[:3] if b), sum(1 for b in d[3:] if b))


def minimality_report() -> dict[str, object]:
    descs = all_descs()
    table = [
        {
            "desc": dict(zip(DESC_FIELDS, d)),
            "probes": probe_results(d),
            "compliant": compliant(d),
        }
        for d in descs
    ]
    comp = [d for d in descs if compliant(d)]
    min_cap = (min(cost_capabilities(d) for d in comp) if comp else None)
    min_lex = min((cost_lex(d) for d in comp), default=None)
    interp_matches_kernel = all(
        interp_step(KERNEL_DESC, w, e) == step(w, e)
        for (_, w, e) in PROBES
    ) and interp_step(KERNEL_DESC, SAT_WORLD, ("addView", (1,))) == \
        step(SAT_WORLD, ("addView", (1,)))
    return {
        "class_size": len(descs),
        "compliant": [dict(zip(DESC_FIELDS, d)) for d in comp],
        "unique_compliant_is_kernel": comp == [KERNEL_DESC],
        "orders_agree_on_singleton": (
            len(comp) == 1
            and min_cap == cost_capabilities(KERNEL_DESC)
            and min_lex == cost_lex(KERNEL_DESC)
        ),
        "interp_of_kernel_desc_matches_step": interp_matches_kernel,
        "table": table,
    }


def countermodels_report() -> dict[str, object]:
    """The failed-bridge countermodels of the dependency graph, plus
    the run-level separations, with their evidence handles."""
    failed = [
        {
            "bridge": f"{b['source']} -> {b['target']}",
            "relation": b["relation"],
            "evidence": b["evidence"],
            "boundary": b["boundary"],
        }
        for b in BRIDGES if b["status"] == "FALSE_WITH_COUNTERMODEL"
    ]
    return {
        "failed_bridges": failed,
        "run_level_separations": [
            "witness_not_separation (Completion)",
            "separation_not_witness (Completion)",
            "meta_distinctness_inert (Completion)",
            "retraction_breaks_preservation (Completion)",
            "refusal terminalization refuted: refusal_non_absorbing",
            "guard separations: six load-bearing probes (Initiality)",
        ],
    }
