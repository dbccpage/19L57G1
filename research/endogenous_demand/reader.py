"""Never-selects reader of admitted instances.

Classification: metatheory apparatus.  The reader is a fixed scan of
``Regime.insts``.  It consults no requirement store, no profile, no host
predicate, and no Python control that picks a pair.  It is the represented-
execution analogue used to *classify* candidates, never a generator.

AuthorityEffect: None.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import FrozenSet

from derivation.model import Inst, Pair, Regime

READER_SOURCE = Path(__file__).resolve()

# Names the reader must not consult.  A branch on any of these is a host
# choice, not a scan of admitted instances.
FORBIDDEN_READER_NAMES: FrozenSet[str] = frozenset(
    {
        "reqs",
        "collapsed",
        "collapsed_pairs",
        "profiles",
        "separable",
        "Impose",
        "next_demand",
        "holds",
        "labeler",
    }
)


def lookup_binary(insts: FrozenSet[Inst], form: int, src: int) -> int | None:
    """The unique second argument of an instance ``(form, [src, y])``, if any.

    The scan is deterministic (sorted instances).  Multiple matches return
    ``None`` rather than choosing.
    """
    found: list[int] = []
    for form_index, args in sorted(insts):
        if form_index == form and len(args) == 2 and args[0] == src:
            found.append(args[1])
    if len(found) == 1:
        return found[0]
    return None


def read_pairs(insts: FrozenSet[Inst], form: int) -> tuple[Pair, ...]:
    """Every arity-two instance of ``form``, as ordered pairs ``i < j``.

    Unordered or reflexive arguments are dropped, not rewritten.  The
    result is sorted.  Nothing but ``insts`` is read.
    """
    pairs: list[Pair] = []
    for form_index, args in sorted(insts):
        if form_index != form or len(args) != 2:
            continue
        left, right = args
        if left < right:
            pairs.append((left, right))
    return tuple(pairs)


def read_pairs_of_regime(regime: Regime, form: int) -> tuple[Pair, ...]:
    """Read ``form`` from the admitted instances of ``regime`` only."""
    return read_pairs(regime.insts, form)


def reader_source_violations(source: str | None = None) -> tuple[str, ...]:
    """Names in this module's function bodies that the never-selects guard forbids.

    The scan is an AST walk of this file.  It does not execute the reader.
    """
    text = READER_SOURCE.read_text(encoding="utf-8") if source is None else source
    tree = ast.parse(text)
    hits: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in FORBIDDEN_READER_NAMES:
            hits.append(f"{node.lineno}:{node.id}")
        if isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_READER_NAMES:
            hits.append(f"{node.lineno}:{node.attr}")
    return tuple(hits)
