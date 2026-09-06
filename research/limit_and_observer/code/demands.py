"""The eight demands, as total decidable predicates of one signature.

Classification: imposed challenge (each demand); derived definition (the
combination set); deterministic computation (every decision below).

Because the demand is a parameter of the pricing routine and never a branch
inside it, no demand can acquire its own enumerator, bound or measure.

Evidence arity is carried with each demand and preserved into the report: the
observer ladder is decided **at a single state**, LIM-R over a **chain** at a
fixed state, LIM-G and LIM-F on a **run**.  A candidate answering demands of
different arity is answering different kinds of question.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Callable

from .grammar import contexts, sealed_relation
from .items import (
    AddContext,
    Delta,
    NewDatum,
    NewReader,
    StatedState,
    is_sealed_item,
    item_shape_valid,
)
from .quotient import automorphisms, transport_context
from .readers import Reader, induced_relation, reading_class
from .regime import Pair, Regime

Relation = frozenset[Pair]

SINGLE_STATE = "single state"
CHAIN = "chain at a fixed state"
RUN = "run"


@dataclass(frozen=True)
class Situation:
    """Everything a demand may read.  Nothing else is available to it."""

    base: Regime
    delta: Delta
    state: StatedState
    designated: Pair | None
    w_max: int


Predicate = Callable[[Situation], bool]


def reader_relations(sit: Situation) -> list[Relation]:
    return [
        induced_relation(sit.state.regime, rho) for rho in sit.state.readers
    ]


# --------------------------------------------------------------------------
# The observer ladder
# --------------------------------------------------------------------------


def obs1_existence(sit: Situation) -> bool:
    """At least one admitted reader whose induced relation differs from the
    sealed observer's.  Distinctness is decided by the **induced relation**,
    never by syntax."""
    sealed = sealed_relation(sit.state.regime)
    return any(rel != sealed for rel in reader_relations(sit))


def obs2_sub_reader(sit: Situation) -> bool:
    """OBS-1 with the reader strictly coarser: it identifies a pair the
    sealed observer separates and separates none it identifies."""
    sealed = sealed_relation(sit.state.regime)
    return any(
        rel != sealed and rel <= sealed for rel in reader_relations(sit)
    )


def obs3_rival(sit: Situation) -> bool:
    """An admitted reader that **separates a pair the sealed observer
    identifies**.  The rung that carries the question."""
    sealed = sealed_relation(sit.state.regime)
    return any(rel - sealed for rel in reader_relations(sit))


def obs4_coexistence(sit: Situation) -> bool:
    """Two admitted readers, each separating at least one pair, giving
    opposite verdicts at the designated pair, neither an automorphism image
    of the other.

    The last clause bars the answer bought by a reader that sees nothing:
    the estate already exhibits that reader (``natural_sections`` NS-05,
    ``blindObs``), so it must be priced rather than excluded by taste."""
    if sit.designated is None or len(sit.state.readers) != 2:
        return False
    rels = reader_relations(sit)
    if not rels[0] or not rels[1]:
        return False
    if (sit.designated in rels[0]) == (sit.designated in rels[1]):
        return False
    return not renaming_of_each_other(
        sit.state.regime, sit.state.readers[0], sit.state.readers[1]
    )


def renaming_of_each_other(r: Regime, a: Reader, b: Reader) -> bool:
    """Transport the frozen reading class, aggregation and selected contexts."""
    if reading_class(a.reading) != reading_class(b.reading) or a.aggregation != b.aggregation:
        return False
    for pi, phi in automorphisms(r):
        moved = sorted(transport_context(c, pi, phi) for c in a.selection)
        if moved == sorted(b.selection):
            return True
    return False


#: The declared finite combination set of OBS-5.
COMBINATIONS: tuple[str, ...] = (
    "identity",
    "complement",
    "intersection",
    "union",
    "symmetric_difference",
    "left_projection",
    "right_projection",
)


def combination_values(
    universe: Relation, sealed: Relation, other: Relation | None
) -> dict[str, Relation]:
    out: dict[str, Relation] = {
        "identity": sealed,
        "complement": universe - sealed,
    }
    if other is not None:
        out["intersection"] = sealed & other
        out["union"] = sealed | other
        out["symmetric_difference"] = (sealed | other) - (sealed & other)
        out["left_projection"] = sealed
        out["right_projection"] = other
    return out


def obs5_derivability(sit: Situation) -> bool:
    """Whether every admitted reader's relation is a value of the declared
    combination set applied to the sealed relation and the other admitted
    reader.  Inside the set: **derived**.  Outside for every combination:
    **admitted**.  The enumeration says which; nothing is argued."""
    if not sit.state.readers:
        return False
    r = sit.state.regime
    from .grammar import data_pairs

    universe = frozenset(data_pairs(r.n_data()))
    sealed = sealed_relation(r)
    rels = reader_relations(sit)
    for idx, rel in enumerate(rels):
        other = rels[1 - idx] if len(rels) == 2 else None
        if rel not in set(combination_values(universe, sealed, other).values()):
            return False
    return True


# --------------------------------------------------------------------------
# The limit
# --------------------------------------------------------------------------


def strict_split_chain_length(r: Regime, rho: Reader) -> int:
    """The longest chain of strictly splitting selections built from this
    reader's selection, over every order in which its contexts could have
    been bought."""
    from .readers import induced_blocks

    best = 0
    for order in itertools.permutations(rho.selection):
        blocks = induced_blocks(r, Reader((), rho.reading, rho.aggregation))
        steps = 0
        for k in range(len(order)):
            nxt = induced_blocks(
                r, Reader(order[: k + 1], rho.reading, rho.aggregation)
            )
            if nxt > blocks:
                steps += 1
                blocks = nxt
        best = max(best, steps)
    return best


def limr_refinement(sit: Situation) -> bool:
    """Refinement without end: a chain of strictly splitting selections
    longer than the carrier, with **no** ``NewDatum`` item anywhere in the
    delta.  The absence of a growth item is what keeps this direction apart
    from the other, and it is an assertion of the predicate, not a
    convention of the prose."""
    if any(isinstance(it, NewDatum) for it in sit.delta):
        return False
    n = sit.state.regime.n_data()
    for rho in sit.state.readers:
        # A chain of strict splits built from a selection has at most one step
        # per context, so its length is at most the reader's width.  A chain
        # longer than the carrier therefore needs a width above the carrier,
        # and the search below is skipped when no reader has one.  This is an
        # equivalence, not a heuristic; ``tests/test_obstructions.py`` checks
        # it against the unabridged computation.
        if rho.width() <= n:
            continue
        if strict_split_chain_length(sit.state.regime, rho) > n:
            return True
    return False


def selection_is_fixed(delta: Delta) -> bool:
    """Whether every reader's selection is fixed at stage 0.

    In a one-step delta every ``AddContext`` is at stage 0 by construction;
    the check exists so that a multi-stage candidate cannot smuggle a repair
    round, and it is asserted rather than assumed."""
    return all(
        is_sealed_item(it) or isinstance(it, (NewReader, AddContext))
        for it in delta
    )


def limg_growth(sit: Situation) -> bool:
    """Growth without end: a fixed-selection admitted reader separating every
    pair of admitted data at a carrier exceeding ``2 ** w_max``.

    Equal signatures force ``s = 0`` and ``a(0) = false``, so the
    non-separation relation of any fixed-selection reader is coarser than
    signature equality and has at most ``2 ** w`` blocks.  The demand is
    therefore stated at the state level, which is equivalent to the run-level
    statement for every run by that argument."""
    if not selection_is_fixed(sit.delta):
        return False
    r = sit.state.regime
    if r.n_data() <= 2 ** sit.w_max:
        return False
    from .grammar import data_pairs

    universe = frozenset(data_pairs(r.n_data()))
    return any(
        induced_relation(r, rho) == universe for rho in sit.state.readers
    )


def reads_only_the_stage(delta: Delta) -> bool:
    """The exhaustiveness check behind LIM-F.

    No item of the declared alphabet carries a stage index, an earlier
    regime, or its own earlier verdict: ``NewReader`` carries a reading and an
    aggregation, ``AddContext`` carries a reader position and a context, and
    the four sealed items carry admission data.  This is a real property of
    the enumeration and it can fail — if an item kind grows a field, it fails
    here."""
    return all(item_shape_valid(it) for it in delta)


def limf_family_verdict(sit: Situation) -> bool:
    """The family-determined verdict: an admitted object realising a total
    function of the finite verdict sequence that is stable and novel.

    No item of the alphabet admits a function of a verdict sequence, so this
    is false for every candidate.  The **content** is
    ``reads_only_the_stage``, which is the checkable half; the implication
    that stage-local readers agreeing at every stage have equal family
    verdicts is true by unfolding and carries no content by itself."""
    return not reads_only_the_stage(sit.delta)


@dataclass(frozen=True)
class Demand:
    """A demand, its predicate, its evidence arity, and — for a demand that
    imposes a requirement — the pair imposed before the quotient is taken.

    The imposed pair is part of the child state's structure and so constrains
    which bijections preserve it, exactly as in the sealed ``_quotient``.
    Carrying it as a field of the demand keeps the pricing routine
    demand-parameterised rather than branched."""

    name: str
    predicate: Predicate
    evidence_arity: str
    statement: str
    impose: Pair | None = None


DEMANDS: tuple[Demand, ...] = (
    Demand("OBS-1", obs1_existence, SINGLE_STATE,
           "an admitted reader whose induced relation differs from the "
           "sealed observer's"),
    Demand("OBS-2", obs2_sub_reader, SINGLE_STATE,
           "an admitted reader strictly coarser than the sealed observer"),
    Demand("OBS-3", obs3_rival, SINGLE_STATE,
           "an admitted reader separating a pair the sealed observer "
           "identifies"),
    Demand("OBS-4", obs4_coexistence, SINGLE_STATE,
           "two admitted readers, each separating, disagreeing at the "
           "designated pair, neither a renaming of the other"),
    Demand("OBS-5", obs5_derivability, SINGLE_STATE,
           "every admitted reader's relation lies in the declared "
           "combination set over the sealed relation and the other reader"),
    Demand("LIM-R", limr_refinement, CHAIN,
           "a chain of strictly splitting selections longer than the "
           "carrier, with no growth item"),
    Demand("LIM-G", limg_growth, RUN,
           "a fixed-selection reader separating every pair at a carrier "
           "above two to the width"),
    Demand("LIM-F", limf_family_verdict, RUN,
           "an admitted object realising a stable and novel function of the "
           "finite verdict sequence"),
)

DEMANDS_BY_NAME: dict[str, Demand] = {d.name: d for d in DEMANDS}
