"""P1 -- S9.1, the axiom lattice (PROMPT.md steps 5-12).

Finite computation only.  Nothing here is a theorem; the carrier-general
statements the sweep suggests are proposed as Lean targets in
``P1_FINDINGS.md`` and proved by nobody in this module.  AuthorityEffect:
None.

Declarations, in the order the prompt asks for them.  Every one of them is
fixed here before anything is enumerated, and the receipt copies them.
Repair round 1 revised the step-7 paragraph below (it stated possibility
where necessity holds) and the one-variable count of step 5; repair round
2 bounded the pure-fragment lemma wherever a receipt string states it,
recomputed W from the raw relation census, and recorded the restriction
of the N = 4 closure onto the N = 3 closure; both rounds are recorded in
``P1_FINDINGS.md`` sections 11 and 12.

Step 5 -- the axiom space.  Universally quantified Horn clauses over one
binary relation ``r`` in at most two variables ``x``, ``y``.  The atoms are
``r x x``, ``r x y``, ``r y x``, ``r y y`` (indices 0..3).  A clause has a
head that is one atom or falsum and a body that is any subset of the
atoms.  An axiom is a finite set of clauses; its extent is the
intersection of its clauses' extents.  The raw clause count is 5 heads
times 16 bodies = 80.  Clauses are quotiented by the swap ``x <-> y``
(the swap fixes every extent: checked by computation at N = 3 in
``test_swap_fixes_every_extent`` over all 192 raw clauses; no general
statement is claimed here); the count before and after the quotient
is printed and both are in the receipt.  Clauses whose head lies in their
own body are KEPT in the enumeration and counted, and DROPPED from the
generating set: their extent is the top of the lattice, which is present
anyway as the extent of the empty axiom.  The count used downstream is
the number of non-trivial swap orbits.  A clause is ONE-VARIABLE when the
atoms it mentions, in body and head together, use at most one of ``x``,
``y`` (``-> falsum`` mentions none and is counted among them); ``x = y``
mentions both, so no EQ_BEARING clause is one-variable.  Both the raw
count and the swap-orbit count of one-variable clauses are reported.

Step 6 -- the EQ_BEARING fragment.  Atom index 4 is ``x = y``, the
metatheory's own identity (A3's bill, not A1's).  A clause mentioning it
in body or head belongs to the EQ_BEARING fragment, enumerated separately
under the same bounds; its results are never merged into the pure
fragment's without the label ``MERGED_PURE_AND_EQ_BEARING`` in the same
object.

Step 7 -- soundness transfer, two definitions, computed side by side.

    TRANSFER_ALL_CARRIERS (the default):  phi transfers iff for every
    pointed structure (X, r, a, b) with |X| in 1..N, r a b and phi(r),
    the metatheory has a != b.

    TRANSFER_ABOVE_POINT:  phi transfers iff for every pointed structure
    (X, r, a, b) with |X| in 2..N, r a b and phi(r), the metatheory has
    a != b.

"phi entails irreflexivity" is fixed once, independently of either
definition: every relation in ext(phi), over carriers 1..N, is
irreflexive, i.e. ext(phi) is contained in the extent of ``r x x ->
falsum``.  Under EITHER definition "phi transfers" unfolds to a
containment ``ext(phi) <= W`` in one fixed extent W: under
TRANSFER_ALL_CARRIERS W is irreflexivity's extent, so the transfer test
and the entailment test are the same containment and the step-11 set is
empty by construction (F3 cannot fail; that is why the second definition
exists); under TRANSFER_ABOVE_POINT W is the extent of ``r x x -> x =
y``, which exceeds irreflexivity's extent by the one-point full relation
alone.  The step-11 set under the second definition is therefore decided
by argument before the sweep in every fragment: NONEMPTY wherever the
lattice contains an extent between the one-point full relation and W --
in the EQ_BEARING fragment ``r x x -> x = y`` is itself a generator, so
its extent is a member -- and EMPTY in the pure fragment, because no pure
clause separates the one-point full relation from the two-point full
relation (their realized r-atom patterns coincide), so every pure extent
admitting the former admits the latter and fails above the point; that
lemma is checked at N and bounded by N = 4, and its general form is Lean
target T7, not proved here.  The sweep confirms both at N and lists the
members; it discovers neither.  The receipt carries this per cell under
``f3_set.decided_before_the_sweep``.

Step 8 -- extents are over all relations on carriers 1..N (unpointed; the
pointing enters only in the transfer test).  N = 3 is required, N = 4 is
attempted, N = 5 is refused by name (``RefusedCarrier``).

Step 9 -- the lattice is a lattice of extents.  An extent is stored as the
set of realized pattern classes it contains: two relations are in the same
class when they have the same carrier size and realize the same set of
atom patterns, and clause truth depends only on that set.  Classes are
nonempty and pairwise disjoint sets of relations, so equality and
inclusion of class sets coincide with equality and inclusion of the
underlying relation sets; ``RelationTable.expand`` recovers the relations
and the tests compare it against the sealed enumerator at N = 3.  The meet
closure of the single-clause extents stops at ``CLOSURE_BOUND`` distinct
extents and is then marked truncated.

Step 10 -- the order is extent inclusion; a SMALLER extent is a STRONGER
axiom, so "stronger" points DOWN in the inclusion order and "upward closed
in the strength direction" is ``closed_under_strengthening`` below.
Because transfer is containment in a fixed W, the transferring set is the
principal down-set of W within the lattice: closure under strengthening
and under meet are then automatic, and W is the unique weakest
transferring extent whenever the lattice realizes it.  The three step-10
findings are still computed and reported separately, with witnesses, and
the receipt says next to them what is automatic; the non-definitional
content of step 10 in each cell is which extent W is and whether the
lattice realizes it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Sequence

import common
from derivation.primdiff import Pointed, enumerate_pointed

# ---------------------------------------------------------------------------
# Declarations
# ---------------------------------------------------------------------------

ATOM_TEXT: tuple[str, ...] = ("r x x", "r x y", "r y x", "r y y", "x = y")
R_ATOMS: tuple[int, ...] = (0, 1, 2, 3)
EQ_ATOM = 4
FALSUM = 5
HEAD_TEXT: dict[int, str] = {i: ATOM_TEXT[i] for i in range(5)}
HEAD_TEXT[FALSUM] = "falsum"
SWAP_ATOM: dict[int, int] = {0: 3, 1: 2, 2: 1, 3: 0, 4: 4}
ATOM_VARIABLES: dict[int, frozenset[str]] = {
    0: frozenset({"x"}),
    1: frozenset({"x", "y"}),
    2: frozenset({"x", "y"}),
    3: frozenset({"y"}),
    4: frozenset({"x", "y"}),
}
ONE_VARIABLE_MEANING = (
    "a clause is one-variable when the atoms it mentions, in body and head "
    "together, use at most one of x, y (-> falsum mentions none and is "
    "counted among them); x = y mentions both variables, so no EQ_BEARING "
    "clause is one-variable; counted over the raw clauses before the swap "
    "quotient and over the swap orbits after it; not used downstream"
)

PURE = "PURE"
EQ_BEARING = "EQ_BEARING"
MERGED = "MERGED_PURE_AND_EQ_BEARING"
FRAGMENTS: tuple[str, ...] = (PURE, EQ_BEARING, MERGED)
MERGE_SENTENCE = (
    "This object MERGES the pure fragment's generators with the EQ_BEARING "
    "fragment's generators; every count in it mixes A1's bill with A3's "
    "identity atom and must be cited with this sentence."
)
MERGE_CLAUSE = (
    "; this cell is MERGED_PURE_AND_EQ_BEARING, which merges the pure "
    "generators with the EQ_BEARING generators and mixes A1's bill with "
    "A3's identity atom (merge_sentence applies)"
)

REQUIRED_CARRIER = 3
ATTEMPTED_CARRIER = 4
REFUSED_CARRIER = 5
CLOSURE_BOUND = 65536

# The reflexive pattern: r x x, r x y, r y x, r y y all true and x = y.
REFLEXIVE_PATTERN = 0b11111

DECLARED_BOUNDS: dict[str, object] = {
    "carrier_required": REQUIRED_CARRIER,
    "carrier_attempted": ATTEMPTED_CARRIER,
    "carrier_refused_by_name": REFUSED_CARRIER,
    "relation_census_required": 2 + 16 + 512,
    "relation_census_attempted": 2 + 16 + 512 + 65536,
    "closure_bound_distinct_extents": CLOSURE_BOUND,
    "raw_clause_count_arithmetic": 5 * 16,
    "source": "research/s9_obligations/PREFLIGHT.md, step 4, P1",
    "on_bound_hit": (
        "report the bounded terminal with the partial, mark the closure "
        "truncated, never extrapolate, never promote to a carrier-general "
        "claim without a Lean theorem naming the general case"
    ),
}


@dataclass(frozen=True)
class TransferDefinition:
    name: str
    displayed: str
    min_carrier: int
    # True when the definition's W is irreflexivity's extent by definition,
    # so the step-11 set is empty by definitional identity; the fragment-level
    # verdict under f3_set.decided_before_the_sweep uses the same vocabulary
    # and analyze_transfer raises if the two disagree.
    f3_set_empty_by_definitional_identity: bool
    why: str


TRANSFER_ALL_CARRIERS = TransferDefinition(
    name="TRANSFER_ALL_CARRIERS",
    displayed=(
        "phi transfers iff for every pointed structure (X, r, a, b) with |X| "
        "in 1..N, r a b and phi(r), the metatheory has a != b"
    ),
    min_carrier=1,
    f3_set_empty_by_definitional_identity=True,
    why=(
        "the prompt's default (step 7); under this encoding it is the "
        "statement that ext(phi) lies inside the extent of r x x -> falsum, "
        "which is also the fixed meaning of 'entails irreflexivity', so the "
        "step-11 set is empty by construction and F3 cannot fail here"
    ),
)

TRANSFER_ABOVE_POINT = TransferDefinition(
    name="TRANSFER_ABOVE_POINT",
    displayed=(
        "phi transfers iff for every pointed structure (X, r, a, b) with |X| "
        "in 2..N, r a b and phi(r), the metatheory has a != b"
    ),
    min_carrier=2,
    f3_set_empty_by_definitional_identity=False,
    why=(
        "the second definition step 7 permits; it separates the two "
        "consequences of irreflexivity that S7 lists separately, "
        "metatheoretic distinctness (irrefl_witness_ne) and the forced "
        "two-element carrier (no_witness_on_subsingleton), by asking for "
        "the first without the second; under it 'transfers' unfolds to "
        "containment in the extent of r x x -> x = y, which exceeds "
        "irreflexivity's extent by the one-point full relation alone, so "
        "the step-11 set is decided before the sweep: NONEMPTY wherever "
        "the lattice realizes an extent between the one-point full relation "
        "and that extent (in the EQ_BEARING fragment r x x -> x = y is a "
        "generator, so F3 fails there by construction), EMPTY in the pure "
        "fragment (no pure clause separates the one-point full relation "
        f"from the two-point full relation: checked at N, bounded by N = "
        f"{ATTEMPTED_CARRIER}; the general lemma is Lean target T7, not "
        "proved); the sweep confirms this at N and lists the members, it "
        "discovers neither; it is a weaker notion of soundness than the "
        "paper's, because it discounts the one-point self-difference of "
        "selfdiff_consistent"
    ),
)

DEFINITIONS: tuple[TransferDefinition, ...] = (
    TRANSFER_ALL_CARRIERS,
    TRANSFER_ABOVE_POINT,
)

ENTAILS_IRREFLEXIVITY_DISPLAYED = (
    "phi entails irreflexivity iff every relation in ext(phi), over carriers "
    "1..N, is irreflexive, i.e. ext(phi) is contained in the extent of "
    "r x x -> falsum; fixed once, independent of the transfer definition"
)

ORDER_DECLARATION: dict[str, str] = {
    "order": "extent inclusion: e1 <= e2 iff e1 is a subset of e2",
    "stronger": (
        "a SMALLER extent is a STRONGER axiom; stronger points DOWN in the "
        "inclusion order"
    ),
    "meet": "intersection of extents = conjunction of axioms",
    "upward_closed_in_strength": (
        "closed_under_strengthening: every lattice extent contained in a "
        "transferring extent transfers (down in inclusion); checked at N over "
        "the closure's elements"
    ),
    "closed_under_weakening": (
        "every lattice extent containing a transferring extent transfers "
        "(up in inclusion); checked at N over the closure's elements; "
        "reported for contrast, expected to fail at the empty axiom"
    ),
    "unique_weakest": (
        "the transferring extent that contains every other transferring "
        "extent, when one exists; it is the unique minimum in the strength "
        "direction"
    ),
    "principal_downset": (
        "under either definition transfer is containment in one fixed extent "
        "W, so the transferring set is the principal down-set of W within "
        "the lattice; closure under strengthening and under meet are then "
        "automatic, and W is the unique weakest transferring extent whenever "
        "the lattice realizes it; the three findings are computed anyway and "
        "the non-definitional content is which extent W is and whether the "
        "lattice realizes it"
    ),
}

F3_DECISION_MEANING = (
    "what the step-11 set must be by argument, before the sweep runs: "
    "empty_by_definitional_identity when the transfer test and the "
    "entailment test are the same containment; empty_by_lemma when every "
    "lattice extent admitting the one-point full relation admits the "
    "two-point full relation and so fails above the point (that premise is "
    "checked at N and bounded by N; its general form is Lean target T7, not "
    "proved); nonempty_by_named_generator when a generator realizes W, the "
    "extent transfer is containment in, and W admits the one-point full "
    "relation; undecided otherwise.  The sweep's count is checked against "
    "the verdict and a disagreement raises."
)


class RefusedCarrier(ValueError):
    """Raised when a carrier at or above the refused bound is requested."""


def refusal_record(max_n: int) -> dict[str, object]:
    """The refusal record for a carrier the declared bounds forbid."""

    return {
        "terminal": "REFUSED",
        "carrier": max_n,
        "reason": (
            f"carrier N = {max_n} is refused by name in PREFLIGHT.md step 4 "
            f"(P1); no relation, extent, or closure at that size was computed"
        ),
        "relations_that_would_be_added": 1 << (max_n * max_n),
    }


def check_carrier_bound(max_n: int) -> None:
    if max_n >= REFUSED_CARRIER:
        raise RefusedCarrier(str(refusal_record(max_n)["reason"]))
    if max_n < 1:
        raise ValueError("the carrier bound must be at least 1")


# ---------------------------------------------------------------------------
# Clauses (step 5, step 6)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, order=True)
class Clause:
    """A universally quantified Horn clause ``body -> head``.

    ``head`` is an atom index 0..4 or ``FALSUM``; ``body`` is a bitmask over
    atom indices 0..4.  The derived order (head, then body) is the
    enumeration order.
    """

    head: int
    body: int

    def body_atoms(self) -> tuple[int, ...]:
        return tuple(i for i in range(5) if self.body >> i & 1)

    def atoms(self) -> tuple[int, ...]:
        """Every atom mentioned, in body or head."""

        return self.body_atoms() + (() if self.head == FALSUM else (self.head,))

    def variables(self) -> frozenset[str]:
        out: frozenset[str] = frozenset()
        for atom in self.atoms():
            out |= ATOM_VARIABLES[atom]
        return out

    def one_variable(self) -> bool:
        return len(self.variables()) <= 1

    def mentions_eq(self) -> bool:
        return self.head == EQ_ATOM or bool(self.body >> EQ_ATOM & 1)

    def head_in_body(self) -> bool:
        return self.head != FALSUM and bool(self.body >> self.head & 1)

    def falsum_headed(self) -> bool:
        return self.head == FALSUM

    def swap(self) -> Clause:
        body = 0
        for i in self.body_atoms():
            body |= 1 << SWAP_ATOM[i]
        head = FALSUM if self.head == FALSUM else SWAP_ATOM[self.head]
        return Clause(head, body)

    def text(self) -> str:
        body = ", ".join(ATOM_TEXT[i] for i in self.body_atoms())
        return f"{body} -> {HEAD_TEXT[self.head]}".lstrip()

    def bad_patterns(self) -> int:
        """Bitmask over the 32 atom patterns on which the clause fails.

        A pattern is the truth vector of the five atoms at one pair
        ``(x, y)``; the clause fails there iff the body holds and the head
        does not.  Bit 4 (``x = y``) is simply never in the body or head of
        a pure clause, so pure clauses ignore it.
        """

        bad = 0
        for pattern in range(32):
            if pattern & self.body != self.body:
                continue
            if self.head == FALSUM or not pattern >> self.head & 1:
                bad |= 1 << pattern
        return bad


def enumerate_clauses(fragment: str) -> list[Clause]:
    """The raw clause list of a fragment, in enumeration order.

    PURE: heads 0..3 or falsum, bodies over atoms 0..3 (80 clauses).
    EQ_BEARING: heads 0..4 or falsum, bodies over atoms 0..4, keeping the
    clauses that mention ``x = y`` (112 clauses).
    """

    if fragment == PURE:
        heads = [0, 1, 2, 3, FALSUM]
        bodies = range(16)
        return [Clause(h, b) for h in heads for b in bodies]
    if fragment == EQ_BEARING:
        heads = [0, 1, 2, 3, 4, FALSUM]
        return [
            Clause(h, b)
            for h in heads
            for b in range(32)
            if Clause(h, b).mentions_eq()
        ]
    raise ValueError(f"unknown clause fragment {fragment!r}")


def swap_orbits(clauses: Sequence[Clause]) -> list[tuple[Clause, ...]]:
    """Orbits under ``x <-> y``, each sorted, listed by their least member."""

    seen: set[Clause] = set()
    orbits: list[tuple[Clause, ...]] = []
    for clause in sorted(clauses):
        if clause in seen:
            continue
        orbit = tuple(sorted({clause, clause.swap()}))
        seen.update(orbit)
        orbits.append(orbit)
    return orbits


def generating_clauses(fragment: str) -> list[Clause]:
    """The clauses used downstream: one representative per non-trivial
    swap orbit, in enumeration order.  MERGED concatenates PURE then
    EQ_BEARING."""

    if fragment == MERGED:
        return generating_clauses(PURE) + generating_clauses(EQ_BEARING)
    return [
        orbit[0]
        for orbit in swap_orbits(enumerate_clauses(fragment))
        if not orbit[0].head_in_body()
    ]


def clause_space_report(fragment: str) -> dict[str, object]:
    """Step 5's counts: before and after the swap quotient, with and without
    the head-in-body clauses, one- and two-variable, and which count is
    used downstream."""

    if fragment == MERGED:
        pure = clause_space_report(PURE)
        eq = clause_space_report(EQ_BEARING)
        keys = (
            "raw_clause_count",
            "swap_orbit_count",
            "head_in_body_count",
            "nontrivial_clause_count",
            "nontrivial_swap_orbit_count",
            "one_variable_clause_count_raw",
            "one_variable_swap_orbit_count",
            "two_variable_clause_count_raw",
        )
        merged: dict[str, object] = {
            key: int(str(pure[key])) + int(str(eq[key])) for key in keys
        }
        merged["fragment"] = MERGED
        merged["merge_sentence"] = MERGE_SENTENCE
        merged["used_downstream"] = "nontrivial_swap_orbit_count"
        return merged
    raw = enumerate_clauses(fragment)
    orbits = swap_orbits(raw)
    trivial = [c for c in raw if c.head_in_body()]
    nontrivial = [c for c in raw if not c.head_in_body()]
    nontrivial_orbits = [o for o in orbits if not o[0].head_in_body()]
    one_variable = [c for c in raw if c.one_variable()]
    return {
        "fragment": fragment,
        "atoms": list(ATOM_TEXT[:4]) + ([ATOM_TEXT[4]] if fragment == EQ_BEARING else []),
        "heads": "one atom or falsum",
        "bodies": "any subset of the atoms",
        "raw_clause_count": len(raw),
        "swap_orbit_count": len(orbits),
        "swap_fixed_clause_count": sum(1 for o in orbits if len(o) == 1),
        "head_in_body_count": len(trivial),
        "head_in_body_policy": (
            "kept in the enumeration and counted; dropped from the generating "
            "set because their extent is the top, present anyway as the empty "
            "axiom"
        ),
        "nontrivial_clause_count": len(nontrivial),
        "nontrivial_swap_orbit_count": len(nontrivial_orbits),
        "used_downstream": "nontrivial_swap_orbit_count",
        "one_variable_meaning": ONE_VARIABLE_MEANING,
        "one_variable_clause_count_raw": len(one_variable),
        "one_variable_clauses_raw": [c.text() for c in one_variable],
        "one_variable_swap_orbit_count": len(swap_orbits(one_variable)),
        "two_variable_clause_count_raw": len(raw) - len(one_variable),
    }


# ---------------------------------------------------------------------------
# Relations and pattern classes (step 8, step 9)
# ---------------------------------------------------------------------------

Rel = frozenset[tuple[int, int]]


def relation_from_mask(n: int, mask: int) -> Rel:
    return frozenset((u, v) for u in range(n) for v in range(n) if mask >> (u * n + v) & 1)


@dataclass(frozen=True)
class RelationTable:
    """Every relation on carriers 1..max_n, grouped into pattern classes.

    Class ``i`` is the set of relations on carrier ``class_n[i]`` whose
    realized atom-pattern set is ``class_pattern[i]``; ``class_count[i]``
    is its size and ``class_first[i]`` the bitmask of its first relation.
    """

    max_n: int
    class_n: tuple[int, ...]
    class_pattern: tuple[int, ...]
    class_count: tuple[int, ...]
    class_first: tuple[int, ...]
    census: dict[int, int]

    @property
    def class_total(self) -> int:
        return len(self.class_n)

    @property
    def top(self) -> int:
        return (1 << self.class_total) - 1

    def classes(self, extent: int) -> Iterator[int]:
        i = 0
        while extent:
            if extent & 1:
                yield i
            extent >>= 1
            i += 1

    def class_mask(self, predicate: Sequence[bool]) -> int:
        out = 0
        for i, flag in enumerate(predicate):
            if flag:
                out |= 1 << i
        return out

    def reflexive_classes(self) -> int:
        return self.class_mask(
            [bool(p >> REFLEXIVE_PATTERN & 1) for p in self.class_pattern]
        )

    def carrier_classes(self, min_n: int) -> int:
        return self.class_mask([n >= min_n for n in self.class_n])

    def size_by_carrier(self, extent: int) -> dict[str, int]:
        sizes = {str(n): 0 for n in range(1, self.max_n + 1)}
        for i in self.classes(extent):
            sizes[str(self.class_n[i])] += self.class_count[i]
        return sizes

    def total_size(self, extent: int) -> int:
        return sum(self.size_by_carrier(extent).values())

    def first_relation(self, class_index: int) -> tuple[int, Rel]:
        n = self.class_n[class_index]
        return n, relation_from_mask(n, self.class_first[class_index])

    def expand(self, extent: int) -> set[tuple[int, Rel]]:
        """Every relation in the extent, recomputed from the raw census."""

        wanted = {
            (self.class_n[i], self.class_pattern[i]) for i in self.classes(extent)
        }
        out: set[tuple[int, Rel]] = set()
        for n in range(1, self.max_n + 1):
            for mask in range(1 << (n * n)):
                if (n, pattern_set(n, mask)) in wanted:
                    out.add((n, relation_from_mask(n, mask)))
        return out


def pattern_set(n: int, mask: int) -> int:
    """The set of atom patterns realized by a relation, as a 32-bit mask."""

    patterns = 0
    for x in range(n):
        xx = mask >> (x * n + x) & 1
        for y in range(n):
            pattern = (
                xx
                | (mask >> (x * n + y) & 1) << 1
                | (mask >> (y * n + x) & 1) << 2
                | (mask >> (y * n + y) & 1) << 3
                | (16 if x == y else 0)
            )
            patterns |= 1 << pattern
    return patterns


def build_table(max_n: int) -> RelationTable:
    """Enumerate every relation on carriers 1..max_n and group by pattern
    class.  Refuses the declared bound by name."""

    check_carrier_bound(max_n)
    groups: dict[tuple[int, int], list[int]] = {}
    census: dict[int, int] = {}
    for n in range(1, max_n + 1):
        total = 1 << (n * n)
        census[n] = total
        for mask in range(total):
            key = (n, pattern_set(n, mask))
            group = groups.get(key)
            if group is None:
                groups[key] = [1, mask]
            else:
                group[0] += 1
    keys = sorted(groups)
    return RelationTable(
        max_n=max_n,
        class_n=tuple(k[0] for k in keys),
        class_pattern=tuple(k[1] for k in keys),
        class_count=tuple(groups[k][0] for k in keys),
        class_first=tuple(groups[k][1] for k in keys),
        census=census,
    )


def clause_extent(clause: Clause, table: RelationTable) -> int:
    """The classes on which the clause holds: no realized pattern is bad."""

    bad = clause.bad_patterns()
    return table.class_mask([p & bad == 0 for p in table.class_pattern])


def clause_holds(clause: Clause, n: int, rel: Rel) -> bool:
    """The clause evaluated literally by quantifying over x and y."""

    for x in range(n):
        for y in range(n):
            truth = ((x, x) in rel, (x, y) in rel, (y, x) in rel, (y, y) in rel, x == y)
            if all(truth[i] for i in clause.body_atoms()) and (
                clause.head == FALSUM or not truth[clause.head]
            ):
                return False
    return True


def literal_extent(clause: Clause, max_n: int) -> set[tuple[int, Rel]]:
    """The extent by direct evaluation over every relation (cross-check)."""

    check_carrier_bound(max_n)
    out: set[tuple[int, Rel]] = set()
    for n in range(1, max_n + 1):
        for mask in range(1 << (n * n)):
            rel = relation_from_mask(n, mask)
            if clause_holds(clause, n, rel):
                out.add((n, rel))
    return out


# ---------------------------------------------------------------------------
# Transfer (step 7, step 10, step 11, step 12)
# ---------------------------------------------------------------------------


def render_pointed(n: int, rel: Rel, a: int, b: int) -> dict[str, object]:
    return {
        "carrier": n,
        "relation": common.render_relation(rel),
        "a": a,
        "b": b,
        "asserted": (a, b) in rel,
        "a_equals_b": a == b,
    }


@dataclass(frozen=True)
class TransferVerdict:
    transfers: bool
    witness: dict[str, object] | None


def transfer_extent(defn: TransferDefinition, table: RelationTable) -> int:
    """The extent W that transfer under ``defn`` is containment in: every
    class with no reflexive relation on a carrier the definition ranges
    over.

    This and ``transfer_verdict`` read the SAME two class masks, so the
    check ``e & W == e`` on every lattice element in ``analyze_transfer`` is
    a consistency check of the bitset encoding and cannot fail.  The
    evidence that the verdicts match the displayed definition is
    ``test_bitset_verdicts_match_the_literal_definition_at_n3`` (the sealed
    enumerator, N = 3) and ``transfer_extent_from_raw_census`` below, which
    recomputes W from the raw relation census and is compared with this
    value in the receipt.
    """

    return table.top & ~(table.reflexive_classes() & table.carrier_classes(defn.min_carrier))


def reflexive_classes_from_raw_census(table: RelationTable) -> int:
    """The classes containing a relation with a reflexive point, recomputed
    from the raw relation census.

    Every relation on carriers 1..max_n is re-enumerated; whether it has a
    pair ``(a, a)`` is evaluated on the relation itself, not read from the
    stored pattern bit; the class is found by carrier and realized pattern
    set.  Raises if a class is not homogeneous -- if two relations of one
    class disagree on having a reflexive point -- which is the check that
    makes this an independent path to W rather than a copy of
    ``RelationTable.reflexive_classes``.
    """

    index = {
        (table.class_n[i], table.class_pattern[i]): i for i in range(table.class_total)
    }
    marked: dict[int, bool] = {}
    for n in range(1, table.max_n + 1):
        for mask in range(1 << (n * n)):
            i = index[(n, pattern_set(n, mask))]
            reflexive = any(mask >> (a * n + a) & 1 for a in range(n))
            seen = marked.get(i)
            if seen is None:
                marked[i] = reflexive
            elif seen != reflexive:
                raise AssertionError(
                    f"pattern class {i} mixes relations with and without a reflexive point"
                )
    return table.class_mask([marked[i] for i in range(table.class_total)])


def transfer_extent_from_raw_census(
    defn: TransferDefinition, table: RelationTable, raw_reflexive: int
) -> int:
    """W under ``defn`` from ``reflexive_classes_from_raw_census``."""

    return table.top & ~(raw_reflexive & table.carrier_classes(defn.min_carrier))


def transfer_verdict(
    extent: int, defn: TransferDefinition, table: RelationTable
) -> TransferVerdict:
    """Decide the definition on an extent.

    A failure is a pointed structure (X, r, a, a) with r a a and r in the
    extent, on a carrier the definition ranges over; the witness is the
    first such structure in class order.
    """

    failing = extent & table.reflexive_classes() & table.carrier_classes(defn.min_carrier)
    if failing == 0:
        return TransferVerdict(True, None)
    class_index = next(table.classes(failing))
    n, rel = table.first_relation(class_index)
    point = next(a for a in range(n) if (a, a) in rel)
    return TransferVerdict(False, render_pointed(n, rel, point, point))


def literal_transfer(
    clause: Clause, defn: TransferDefinition, max_n: int
) -> tuple[bool, Pointed | None]:
    """The definition evaluated literally with the sealed enumerator."""

    check_carrier_bound(max_n)
    for n in range(defn.min_carrier, max_n + 1):
        for s in enumerate_pointed(n):
            if (s.a, s.b) in s.rel and clause_holds(clause, n, s.rel) and s.a == s.b:
                return False, s
    return True, None


def entails_irreflexivity(extent: int, table: RelationTable) -> bool:
    return extent & table.reflexive_classes() == 0


def witnessed_model(extent: int, table: RelationTable) -> dict[str, object] | None:
    """A structure in the extent with an asserted pair a != b, if any."""

    for i in table.classes(extent):
        n, rel = table.first_relation(i)
        for x, y in sorted(rel):
            if x != y:
                return render_pointed(n, rel, x, y)
    return None


@dataclass(frozen=True)
class Lattice:
    elements: tuple[int, ...]
    representative: dict[int, tuple[int, ...]]
    bound: int
    truncated: bool


def meet_closure(generators: Sequence[int], top: int, bound: int) -> Lattice:
    """All meets of subsets of the generators, the empty meet being ``top``.

    Each element remembers the first generator subset that produced it, as
    a syntactic representative.  Stops, marked truncated, when ``bound``
    distinct extents have been produced.
    """

    representative: dict[int, tuple[int, ...]] = {top: ()}
    order: list[int] = [top]
    truncated = False
    for gi, g in enumerate(generators):
        for e in list(order):
            m = e & g
            if m in representative:
                continue
            if len(order) >= bound:
                truncated = True
                break
            representative[m] = representative[e] + (gi,)
            order.append(m)
        if truncated:
            break
    return Lattice(tuple(order), representative, bound, truncated)


def describe_extent(
    extent: int,
    lattice: Lattice,
    generators: Sequence[Clause],
    table: RelationTable,
) -> dict[str, object]:
    rep = lattice.representative[extent]
    return {
        "representative_axiom": [generators[i].text() for i in rep],
        "representative_is_unique": False,
        "extent_size_by_carrier": table.size_by_carrier(extent),
        "extent_size_total": table.total_size(extent),
    }


def full_relation_classes(table: RelationTable) -> int:
    """The classes of the full relation on each carrier 1..N (one class
    per carrier; the full relation is alone in its class)."""

    out = 0
    for n in range(1, table.max_n + 1):
        key = (n, pattern_set(n, (1 << (n * n)) - 1))
        for i in range(table.class_total):
            if (table.class_n[i], table.class_pattern[i]) == key:
                out |= 1 << i
    return out


def one_point_full_class(table: RelationTable) -> int:
    return full_relation_classes(table) & table.carrier_classes(1) & ~table.carrier_classes(2)


def two_point_full_class(table: RelationTable) -> int:
    return full_relation_classes(table) & table.carrier_classes(2) & ~table.carrier_classes(3)


def render_extent_relations(extent: int, table: RelationTable) -> list[dict[str, object]]:
    """Every relation of a (small) extent, rendered; used for W minus
    irreflexivity's extent, which has at most one relation."""

    if all(table.class_count[i] == 1 for i in table.classes(extent)):
        found = [table.first_relation(i) for i in table.classes(extent)]
    else:
        found = list(table.expand(extent))
    return [
        {"carrier": n, "relation": common.render_relation(rel)}
        for n, rel in sorted(found, key=lambda t: (t[0], sorted(t[1])))
    ]


def f3_decision(
    defn: TransferDefinition,
    lattice: Lattice,
    generators: Sequence[Clause],
    extents: Sequence[int],
    table: RelationTable,
    w: int,
    irrefl_extent: int,
) -> dict[str, object]:
    """What the step-11 set must be by argument, before the sweep.

    Every premise used is itself checked by computation at N and reported;
    the verdict is then compared with the sweep's count by the caller.
    """

    point = one_point_full_class(table)
    two_point = two_point_full_class(table)
    same_containment = w == irrefl_extent
    lemma_holds = all(e & two_point == two_point for e in lattice.elements if e & point)
    realizing = [c.text() for c, e in zip(generators, extents) if e == w]
    w_transfers = transfer_verdict(w, defn, table).transfers
    w_admits_point = bool(w & point)
    if same_containment:
        verdict = "empty_by_definitional_identity"
        reason = (
            "transfer is containment in irreflexivity's extent, which is "
            "the entailment test; identical predicates, so the set is empty "
            "whatever the sweep finds"
        )
    elif realizing and w in lattice.representative and w_admits_point and w_transfers:
        verdict = "nonempty_by_named_generator"
        reason = (
            f"the generator {realizing[0]} realizes W, the extent transfer "
            f"is containment in, so it transfers, and W admits the one-point "
            f"full relation (the clause's head is x = y), so it does not "
            f"entail irreflexivity; it is a member before any sweep"
        )
    elif lemma_holds:
        verdict = "empty_by_lemma"
        reason = (
            "every lattice extent admitting the one-point full relation "
            "admits the two-point full relation (no clause of this fragment "
            "separates them: their realized r-atom patterns coincide), and "
            "the two-point full relation fails above the point, so no "
            "transferring extent admits a reflexive relation; the set is "
            f"empty whatever the sweep finds; the lemma is checked at N = "
            f"{table.max_n} and bounded by it, and its general form is Lean "
            "target T7, not proved"
        )
    else:
        verdict = "undecided_before_the_sweep"
        reason = "no argument above applies; the sweep's count decides"
    return {
        "meaning": F3_DECISION_MEANING,
        "verdict": verdict,
        "reason": reason,
        "named_generator": realizing[0] if verdict == "nonempty_by_named_generator" else None,
        "premises_checked_at_N": {
            "bounded": True,
            "bound_reached": table.max_n,
            "W_equals_irreflexivity_extent": same_containment,
            "W_realized_by_generators": realizing,
            "W_in_lattice": w in lattice.representative,
            "W_admits_one_point_full": w_admits_point,
            "W_transfers": w_transfers,
            "one_point_full_implies_two_point_full_on_lattice": lemma_holds,
        },
    }


def analyze_transfer(
    lattice: Lattice,
    defn: TransferDefinition,
    table: RelationTable,
    generators: Sequence[Clause],
    extents: Sequence[int],
    irrefl_extent: int,
    raw_reflexive: int,
) -> dict[str, object]:
    """Step 10's three findings, separately, plus step 11's set, plus the
    containment W that makes the findings automatic.  ``raw_reflexive`` is
    ``reflexive_classes_from_raw_census(table)``, the independent path to
    W."""

    verdicts = {e: transfer_verdict(e, defn, table) for e in lattice.elements}
    transferring = [e for e in lattice.elements if verdicts[e].transfers]
    non_transferring = [e for e in lattice.elements if not verdicts[e].transfers]

    def pair_witness(t: int, e: int) -> dict[str, object]:
        return {
            "transferring": describe_extent(t, lattice, generators, table),
            "not_transferring": describe_extent(e, lattice, generators, table),
            "failure": verdicts[e].witness,
        }

    strengthening_witness: dict[str, object] | None = None
    for t in transferring:
        for e in non_transferring:
            if e & t == e:
                strengthening_witness = pair_witness(t, e)
                break
        if strengthening_witness is not None:
            break

    weakening_witness: dict[str, object] | None = None
    for t in transferring:
        for e in non_transferring:
            if t & e == t:
                weakening_witness = pair_witness(t, e)
                break
        if weakening_witness is not None:
            break

    meet_witness: dict[str, object] | None = None
    for i, t1 in enumerate(transferring):
        for t2 in transferring[i:]:
            m = t1 & t2
            if m not in verdicts:
                raise AssertionError("meet closure is not closed under meet")
            if not verdicts[m].transfers:
                meet_witness = {
                    "left": describe_extent(t1, lattice, generators, table),
                    "right": describe_extent(t2, lattice, generators, table),
                    "meet": describe_extent(m, lattice, generators, table),
                    "failure": verdicts[m].witness,
                }
                break
        if meet_witness is not None:
            break

    weakest: int | None = None
    for t in transferring:
        if all(u & t == u for u in transferring):
            weakest = t
            break

    w = transfer_extent(defn, table)
    downset = [e for e in lattice.elements if e & w == e]
    transferring_is_downset = sorted(downset) == sorted(transferring)
    if not transferring_is_downset:
        raise AssertionError("transfer verdicts disagree with containment in W")
    w_raw = transfer_extent_from_raw_census(defn, table, raw_reflexive)
    if w_raw != w:
        raise AssertionError("W from the raw relation census disagrees with W from the pattern bits")
    w_in_lattice = w in lattice.representative
    containment: dict[str, object] = {
        "meaning": (
            "under this definition an extent transfers iff it is contained in "
            "W, the extent of every relation with no reflexive point on a "
            "carrier the definition ranges over.  "
            "transferring_equals_lattice_extents_contained_in_W is checked on "
            "every lattice element but is a consistency check of the bitset "
            "encoding: the verdict and W read the same two class masks, so it "
            "cannot be false.  The evidence that the verdicts match the "
            "displayed definition is "
            "test_bitset_verdicts_match_the_literal_definition_at_n3 (the "
            "sealed enumerator, N = 3) and "
            "W_recomputed_from_raw_census_equals_W here, which re-enumerates "
            "every relation of the census, evaluates 'has a reflexive point' "
            "on the relation itself, checks each pattern class is homogeneous, "
            "and compares the resulting W with this one; a disagreement raises, "
            "so the key records that the cross-check ran"
        ),
        "W_recomputed_from_raw_census_equals_W": w_raw == w,
        "W_size_by_carrier": table.size_by_carrier(w),
        "W_equals_irreflexivity_extent": w == irrefl_extent,
        "W_minus_irreflexivity_extent": {
            "size_by_carrier": table.size_by_carrier(w & ~irrefl_extent),
            "relations": render_extent_relations(w & ~irrefl_extent, table),
        },
        "W_realized_by_generators": [
            c.text() for c, e in zip(generators, extents) if e == w
        ],
        "W_in_lattice": w_in_lattice,
        "W_description_in_lattice": (
            describe_extent(w, lattice, generators, table) if w_in_lattice else None
        ),
        "transferring_equals_lattice_extents_contained_in_W": transferring_is_downset,
        "automatic_once_W_is_fixed": (
            "closed_under_strengthening and closed_under_meet hold for every "
            "principal down-set; unique_weakest equals W whenever W_in_lattice; "
            "when W is not in the lattice the unique weakest, if any, is the "
            "largest lattice extent below W and is a computed fact bounded by N"
        ),
    }

    f3_members = [e for e in transferring if not entails_irreflexivity(e, table)]
    f3_rows: list[dict[str, object]] = []
    for e in f3_members:
        row = describe_extent(e, lattice, generators, table)
        row["not_entailing_witness"] = transfer_verdict(
            e, TRANSFER_ALL_CARRIERS, table
        ).witness
        row["uses_eq_atom"] = any(
            generators[i].mentions_eq() for i in lattice.representative[e]
        )
        f3_rows.append(row)
    decision = f3_decision(defn, lattice, generators, extents, table, w, irrefl_extent)
    verdict_name = str(decision["verdict"])
    if verdict_name.startswith("empty") and f3_members:
        raise AssertionError(f"{verdict_name} but the sweep found {len(f3_members)} members")
    if verdict_name == "nonempty_by_named_generator" and not f3_members:
        raise AssertionError("nonempty_by_named_generator but the sweep found no member")
    if defn.f3_set_empty_by_definitional_identity != (
        verdict_name == "empty_by_definitional_identity"
    ):
        raise AssertionError(
            "the definition-level empty_by_definitional_identity flag disagrees "
            "with the fragment-level verdict"
        )

    generated = (
        strengthening_witness is None
        and meet_witness is None
        and weakest is not None
        and weakest == irrefl_extent
    )
    return {
        "definition": defn.name,
        "displayed": defn.displayed,
        "lattice_size": len(lattice.elements),
        "transferring_count": len(transferring),
        "non_transferring_count": len(non_transferring),
        "transfer_as_containment": containment,
        "closed_under_strengthening": strengthening_witness is None,
        "closed_under_strengthening_witness": strengthening_witness,
        "closed_under_weakening": weakening_witness is None,
        "closed_under_weakening_witness": weakening_witness,
        "closed_under_meet": meet_witness is None,
        "closed_under_meet_witness": meet_witness,
        "unique_weakest_exists": weakest is not None,
        "unique_weakest": (
            None if weakest is None else describe_extent(weakest, lattice, generators, table)
        ),
        "unique_weakest_equals_irreflexivity_extent": weakest == irrefl_extent,
        "unique_weakest_equals_W": weakest == w,
        "generated_by_irreflexivity": generated,
        "f3_set": {
            "meaning": "extents that transfer but do not entail irreflexivity",
            "flags_meaning": (
                "empty_by_definitional_identity is the definition-level flag "
                "(W is irreflexivity's extent by the definition) and equals "
                "decided_before_the_sweep.verdict == empty_by_definitional_identity; "
                "nonempty_by_construction equals decided_before_the_sweep.verdict "
                "== nonempty_by_named_generator; a lemma-decided emptiness is "
                "neither flag and is read from the verdict"
            ),
            "empty_by_definitional_identity": defn.f3_set_empty_by_definitional_identity,
            "nonempty_by_construction": verdict_name == "nonempty_by_named_generator",
            "decided_before_the_sweep": decision,
            "count": len(f3_members),
            "members": f3_rows,
        },
    }


def audit_classifier(
    rows: Sequence[tuple[str, bool, dict[str, object] | None]],
    table: RelationTable,
) -> dict[str, object]:
    """Step 12: an all-transfer or none-transfer table is a defect.

    ``rows`` are (name, transfers, failure witness).  The defect witness
    for "all transfer" is the one-point full relation, which lies in the
    extent of the empty axiom and hosts r a a with a = a; for "none
    transfer" it is the row carrying irreflexivity's clause, whose
    reported failure witness is re-checked against the definition of
    irreflexivity directly.
    """

    transferring = [name for name, ok, _ in rows if ok]
    failing = [name for name, ok, _ in rows if not ok]
    one_point_full = render_pointed(1, frozenset({(0, 0)}), 0, 0)
    if not rows:
        return {"defect": True, "kind": "empty table", "witness": None}
    if not failing:
        return {
            "defect": True,
            "kind": "all transfer",
            "witness": one_point_full,
            "reason": (
                "the empty axiom admits the one-point full relation, which "
                "hosts r a a with a = a, so at least one row must fail"
            ),
        }
    if not transferring:
        irrefl_text = IRREFLEXIVITY.text()
        reported = next((w for name, _, w in rows if name == irrefl_text), None)
        return {
            "defect": True,
            "kind": "none transfer",
            "witness": {"clause": irrefl_text, "reported_failure": reported},
            "reason": (
                "r x x -> falsum must transfer: any reported failure has r a a "
                "and so violates the clause it is claimed to satisfy"
            ),
        }
    return {
        "defect": False,
        "kind": "mixed",
        "transferring_count": len(transferring),
        "non_transferring_count": len(failing),
        "row_count": len(rows),
        "rows_are": (
            "the single-clause extent classes of the fragment, one row per "
            "class; not the pattern classes of the relation table, whose "
            "count is sweeps.N<n>.pattern_class_total"
        ),
    }


# Named clauses for hand-checked cases (tests) and for the receipt.
IRREFLEXIVITY = Clause(FALSUM, 1 << 0)
SYMMETRY = Clause(2, 1 << 1)
FULL_FORCING = Clause(1, 0)
REFLEXIVITY = Clause(0, 0)
ASYMMETRY = Clause(FALSUM, (1 << 1) | (1 << 2))
EMPTY_FORCING = Clause(FALSUM, 1 << 1)
UNSATISFIABLE = Clause(FALSUM, 0)
REFLEXIVE_POINT_FORCES_SINGLETON = Clause(EQ_ATOM, 1 << 0)
SINGLETON = Clause(EQ_ATOM, 0)


# ---------------------------------------------------------------------------
# Finite evidence for the proposed Lean targets (step 13, proposal only)
# ---------------------------------------------------------------------------


def lean_target_evidence(
    fragment: str,
    generators: Sequence[Clause],
    extents: Sequence[int],
    lattice: Lattice,
    table: RelationTable,
) -> dict[str, object]:
    """Each key is the finite fact a proposed Lean target would generalize.
    True here is evidence bounded by the table's carrier, never a proof."""

    full = full_relation_classes(table)
    point = one_point_full_class(table)
    atom_headed = [e for c, e in zip(generators, extents) if c.head in R_ATOMS]
    non_falsum = [e for c, e in zip(generators, extents) if not c.falsum_headed()]
    falsum_headed = [e for c, e in zip(generators, extents) if c.falsum_headed()]
    admitting = [
        e
        for e in lattice.elements
        if e & point
        and transfer_verdict(e, TRANSFER_ABOVE_POINT, table).transfers
    ]
    evidence: dict[str, object] = {
        "bounded": True,
        "bound_reached": table.max_n,
        "T1_atom_headed_generators_admit_full_relation_on_carriers_1_to_N": all(
            e & full == full for e in atom_headed
        ),
        "T2_non_falsum_generators_admit_one_point_full": all(
            e & point == point for e in non_falsum
        ),
        "T3_falsum_headed_generators_entail_irreflexivity": all(
            entails_irreflexivity(e, table) for e in falsum_headed
        ),
        "T4_lattice_transfers_iff_representative_has_falsum_head": all(
            transfer_verdict(e, TRANSFER_ALL_CARRIERS, table).transfers
            == any(generators[i].falsum_headed() for i in lattice.representative[e])
            for e in lattice.elements
        ),
        "T7_lattice_extents_admitting_one_point_full_and_transferring_above_point": len(
            admitting
        ),
        "atom_headed_generator_count": len(atom_headed),
        "non_falsum_generator_count": len(non_falsum),
        "falsum_headed_generator_count": len(falsum_headed),
    }
    if fragment != PURE:
        extent = clause_extent(REFLEXIVE_POINT_FORCES_SINGLETON, table)
        evidence["T6_reflexive_point_forces_singleton"] = {
            "clause": REFLEXIVE_POINT_FORCES_SINGLETON.text(),
            "transfers_above_point": transfer_verdict(
                extent, TRANSFER_ABOVE_POINT, table
            ).transfers,
            "admits_one_point_full": extent & point == point,
            "entails_irreflexivity": entails_irreflexivity(extent, table),
            "extent_size_by_carrier": table.size_by_carrier(extent),
        }
    return evidence


# ---------------------------------------------------------------------------
# Fragment analysis
# ---------------------------------------------------------------------------


def analyze_fragment(
    fragment: str,
    table: RelationTable,
    closure_bound: int = CLOSURE_BOUND,
    raw_reflexive: int | None = None,
) -> dict[str, object]:
    """The whole analysis of one fragment at one carrier bound.
    ``raw_reflexive`` is ``reflexive_classes_from_raw_census(table)``,
    computed here when not supplied (``build_receipt`` computes it once per
    table and shares it across the three fragments)."""

    generators = generating_clauses(fragment)
    extents = [clause_extent(c, table) for c in generators]
    irrefl_extent = clause_extent(IRREFLEXIVITY, table)
    top = table.top
    if raw_reflexive is None:
        raw_reflexive = reflexive_classes_from_raw_census(table)

    by_extent: dict[int, list[int]] = {}
    for gi, e in enumerate(extents):
        by_extent.setdefault(e, []).append(gi)
    classes: list[dict[str, object]] = []
    rows_for_audit: dict[str, list[tuple[str, bool, dict[str, object] | None]]] = {
        defn.name: [] for defn in DEFINITIONS
    }
    for e, members in sorted(by_extent.items(), key=lambda kv: kv[1][0]):
        head = generators[members[0]]
        transfer: dict[str, object] = {}
        for defn in DEFINITIONS:
            verdict = transfer_verdict(e, defn, table)
            transfer[defn.name] = {
                "transfers": verdict.transfers,
                "failure_witness": verdict.witness,
            }
            rows_for_audit[defn.name].append((head.text(), verdict.transfers, verdict.witness))
        classes.append(
            {
                "representative": head.text(),
                "members": [generators[i].text() for i in members],
                "member_count": len(members),
                "extent_size_by_carrier": table.size_by_carrier(e),
                "extent_size_total": table.total_size(e),
                "is_top": e == top,
                "is_bottom": e == 0,
                "falsum_headed": head.falsum_headed(),
                "entails_irreflexivity": entails_irreflexivity(e, table),
                "equals_irreflexivity_extent": e == irrefl_extent,
                "witnessed_model": witnessed_model(e, table),
                "transfer": transfer,
            }
        )

    lattice = meet_closure(extents, top, closure_bound)
    transfer_analysis = {
        defn.name: analyze_transfer(
            lattice, defn, table, generators, extents, irrefl_extent, raw_reflexive
        )
        for defn in DEFINITIONS
    }
    falsum_vs_transfer = all(
        transfer_verdict(e, TRANSFER_ALL_CARRIERS, table).transfers
        == any(generators[i].falsum_headed() for i in lattice.representative[e])
        for e in lattice.elements
    )
    result: dict[str, object] = {
        "fragment": fragment,
        "bounded": True,
        "bound_reached": {
            "carrier": table.max_n,
            "closure_bound": closure_bound,
            "closure_bound_hit": lattice.truncated,
        },
        "clause_space": clause_space_report(fragment),
        "generators": {
            "count": len(generators),
            "clauses": [c.text() for c in generators],
            "valid_by_extent_count": sum(1 for e in extents if e == top),
            "valid_by_extent_clauses": [
                generators[i].text() for i, e in enumerate(extents) if e == top
            ],
        },
        "single_clause_extents": {
            "syntax_class_count": len(generators),
            "extent_class_count": len(by_extent),
            "classes": classes,
        },
        "lattice": {
            "of": "extents, not syntax",
            "closure_size": len(lattice.elements),
            "closure_bound": closure_bound,
            "closure_bound_hit": lattice.truncated,
            "truncated": lattice.truncated,
            "syntax_axiom_count": 1 << len(generators),
            "syntax_axiom_count_note": (
                "subsets of the generating set, arithmetic; the extent count "
                "is closure_size"
            ),
            "top_is_empty_axiom": True,
            "bottom_is_empty_extent": 0 in lattice.representative,
            "irreflexivity_extent_in_lattice": irrefl_extent in lattice.representative,
            "irreflexivity_extent_size_by_carrier": table.size_by_carrier(irrefl_extent),
            "transferring_iff_representative_has_falsum_head": falsum_vs_transfer,
        },
        "transfer": transfer_analysis,
        "classifier_audit": {
            defn.name: audit_classifier(rows_for_audit[defn.name], table)
            for defn in DEFINITIONS
        },
        "lean_target_evidence": lean_target_evidence(
            fragment, generators, extents, lattice, table
        ),
    }
    if fragment == MERGED:
        result["merge_sentence"] = MERGE_SENTENCE
    return result


# ---------------------------------------------------------------------------
# Restriction of the closure at one carrier bound onto a lower one (step 9)
# ---------------------------------------------------------------------------


def extent_keys(table: RelationTable, extent: int, max_carrier: int) -> frozenset[tuple[int, int]]:
    """The (carrier, pattern set) keys of an extent's classes on carriers
    <= ``max_carrier``; comparable across tables of different bounds."""

    return frozenset(
        (table.class_n[i], table.class_pattern[i])
        for i in table.classes(extent)
        if table.class_n[i] <= max_carrier
    )


def closure_restriction(
    fragment: str,
    upper: RelationTable,
    lower: RelationTable,
    closure_bound: int = CLOSURE_BOUND,
) -> dict[str, object]:
    """Restrict every element of the meet closure at ``upper.max_n`` to the
    relations on carriers 1..``lower.max_n`` and compare with the closure
    computed at ``lower.max_n``.

    ``injective`` means no two upper extents restrict to one set;
    ``image_equals_lower_closure`` means the restrictions are exactly the
    lower closure's elements.  Both are computed facts about the two bounds
    and say nothing about any larger carrier.
    """

    if lower.max_n >= upper.max_n:
        raise ValueError("the lower bound must be below the upper bound")
    generators = generating_clauses(fragment)
    up = meet_closure([clause_extent(c, upper) for c in generators], upper.top, closure_bound)
    low = meet_closure([clause_extent(c, lower) for c in generators], lower.top, closure_bound)
    restricted = {extent_keys(upper, e, lower.max_n) for e in up.elements}
    lower_keys = {extent_keys(lower, e, lower.max_n) for e in low.elements}
    out: dict[str, object] = {
        "meaning": (
            "each extent of the closure at from_carrier restricted to the "
            "relations on carriers 1..to_carrier, compared with the closure "
            "computed at to_carrier; injective means no two extents at "
            "from_carrier restrict to one set, image_equals_lower_closure "
            "means the restrictions are exactly the lower closure's elements; "
            "a fact about these two bounds only"
        ),
        "fragment": fragment,
        "from_carrier": upper.max_n,
        "to_carrier": lower.max_n,
        "upper_closure_size": len(up.elements),
        "lower_closure_size": len(low.elements),
        "distinct_restrictions": len(restricted),
        "injective": len(restricted) == len(up.elements),
        "image_equals_lower_closure": restricted == lower_keys,
        "bounded": True,
        "bound_reached": upper.max_n,
        "truncated": up.truncated or low.truncated,
    }
    if fragment == MERGED:
        out["merge_sentence"] = MERGE_SENTENCE
    return out


# ---------------------------------------------------------------------------
# Receipt
# ---------------------------------------------------------------------------


def f3_terminal(
    fragment: str, defn: TransferDefinition, analysis: dict[str, object], max_n: int
) -> str:
    f3 = analysis["f3_set"]
    assert isinstance(f3, dict)
    decision = f3["decided_before_the_sweep"]
    assert isinstance(decision, dict)
    verdict = str(decision["verdict"])
    count = int(str(f3["count"]))
    merge = MERGE_CLAUSE if fragment == MERGED else ""
    where = f"under {defn.name} in {fragment}"
    if verdict == "empty_by_definitional_identity":
        return (
            f"F3_UNTESTED -- {where}: the set of axioms that transfer but do "
            f"not entail irreflexivity is empty by construction, because the "
            f"transfer test and the entailment test are the same containment "
            f"(in irreflexivity's extent), so the conjecture could not fail and "
            f"was not tested; carriers 1..{max_n}{merge}"
        )
    if verdict == "empty_by_lemma":
        return (
            f"F3_SUPPORTED_BOUNDED -- {where}: the set of axioms that transfer "
            f"but do not entail irreflexivity is empty by computation, bounded "
            f"by N = {max_n}, and could not have come out otherwise: transfer "
            f"here is containment in the extent of r x x -> x = y, which "
            f"exceeds irreflexivity's extent by the one-point full relation "
            f"alone, and no clause of this fragment separates that relation "
            f"from the two-point full relation, so every lattice extent "
            f"admitting it fails above the point; the sweep confirms that "
            f"lemma at N = {max_n} (Lean target T7) rather than discovering "
            f"it; no carrier-general claim{merge}"
        )
    if verdict == "nonempty_by_named_generator":
        members = f3["members"]
        assert isinstance(members, list)
        eq_count = sum(1 for m in members if isinstance(m, dict) and bool(m["uses_eq_atom"]))
        if eq_count == count:
            bill = (
                f"F3 as written ranges over one-relation axioms under A1's bill "
                f"(S1: no identity relation of the object language), and S7 "
                f"names selfdiff_consistent as the soundness countermodel this "
                f"definition discounts; every one of the {count} members uses "
                f"A3's identity atom (uses_eq_atom = true), so this refutes F3 "
                f"extended to A3's bill under a soundness weaker than S7's, "
                f"not F3 as written"
            )
        else:
            bill = (
                f"F3 as written ranges over one-relation axioms under A1's bill "
                f"(S1: no identity relation of the object language), and S7 "
                f"names selfdiff_consistent as the soundness countermodel this "
                f"definition discounts; {count - eq_count} of the {count} "
                f"members use no identity atom (uses_eq_atom = false), so the "
                f"refutation reaches A1's bill under this weaker soundness"
            )
        return (
            f"F3_REFUTED -- {where}: the set has {count} member(s), each "
            f"admitting the one-point self-difference, and is nonempty by "
            f"construction: the generator {decision['named_generator']} "
            f"realizes W, the extent that transfer above the point is "
            f"containment in, so it transfers, and it admits the one-point full "
            f"relation because its head is x = y, so it does not entail "
            f"irreflexivity; it is a member before any sweep; the sweep's contribution is "
            f"the listing of all {count} members, bounded by N = {max_n} (the "
            f"transfer half of each witness is checked on carriers 2..{max_n}; "
            f"Lean target T6); the refutation is exactly as strong as "
            f"discounting the one-point carrier and does not touch F3 under "
            f"TRANSFER_ALL_CARRIERS, where the same axioms do not transfer; "
            f"{bill}{merge}"
        )
    if count == 0:
        return (
            f"F3_SUPPORTED_BOUNDED -- {where}: the set is empty by computation, "
            f"bounded by N = {max_n}; not decided by argument before the sweep; "
            f"no carrier-general claim{merge}"
        )
    return (
        f"F3_REFUTED -- {where}: the set has {count} member(s), each admitting "
        f"the one-point self-difference; not decided by argument before the "
        f"sweep; the transfer half of each witness is bounded by N = {max_n}{merge}"
    )


def transfer_terminal(
    fragment: str, defn: TransferDefinition, analysis: dict[str, object], max_n: int
) -> str:
    weakest = analysis["unique_weakest"]
    containment = analysis["transfer_as_containment"]
    assert isinstance(containment, dict)
    characterized = (
        bool(analysis["unique_weakest_exists"])
        and bool(analysis["closed_under_strengthening"])
        and bool(analysis["closed_under_meet"])
    )
    merge = MERGE_CLAUSE if fragment == MERGED else ""
    if not characterized:
        return (
            f"S9_1_TRANSFER_OPEN -- under {defn.name} in {fragment} the "
            f"transferring set has no unique weakest extent or is not closed "
            f"under strengthening or meet at N = {max_n}; bounded by N = {max_n}{merge}"
        )
    assert isinstance(weakest, dict)
    rep = weakest["representative_axiom"]
    assert isinstance(rep, list)
    axiom = " ; ".join(str(t) for t in rep)
    generated = bool(analysis["generated_by_irreflexivity"])
    tail = (
        "generated by irreflexivity (unique weakest extent equals the extent "
        "of r x x -> falsum)"
        if generated
        else f"NOT generated by irreflexivity: the unique weakest extent is that of [{axiom}]"
    )
    if bool(containment["W_in_lattice"]):
        realized = containment["W_realized_by_generators"]
        assert isinstance(realized, list)
        w_clause = (
            f"W is realized in the lattice (by the generator {realized[0]})"
            if realized
            else "W is realized in the lattice by a conjunction"
        )
    else:
        w_clause = (
            "W is NOT in the lattice, so the unique weakest is the largest "
            "lattice extent below W, a computed fact"
        )
    return (
        f"S9_1_TRANSFER_CHARACTERIZED -- under {defn.name} in {fragment}, "
        f"bounded by N = {max_n}: transfer is containment in the fixed extent W "
        f"(every relation without a reflexive point on carriers {defn.min_carrier}..{max_n}), "
        f"so the transferring extents are exactly the lattice extents contained "
        f"in W, closure under strengthening and meet is automatic, and the "
        f"non-definitional content is that {w_clause}; {tail}; finite "
        f"computation, no Lean theorem carries it{merge}"
    )


def _fragment_hit(result: dict[str, object]) -> bool:
    lattice = result["lattice"]
    assert isinstance(lattice, dict)
    return bool(lattice["closure_bound_hit"])


def _fragment_transfer(result: dict[str, object], name: str) -> dict[str, object]:
    transfer = result["transfer"]
    assert isinstance(transfer, dict)
    analysis = transfer[name]
    assert isinstance(analysis, dict)
    return analysis


LEAN_MODULE = "S9Obligations.AxiomLattice"
# The Lean stage's theorems the LEAN_CARRIED terminal names, in the order the
# string names them.  Each must be listed, under LEAN_MODULE, in
# verify_lean.AXIOM_REPORT_DECLARATIONS (test_terminals), so a cited name is
# an audited report and not a promise.
LEAN_CARRIED_THEOREMS: tuple[str, ...] = (
    "transfers_iff_has_falsum_clause",
    "transfers_iff_entails_irrefl",
    "atom_head_clause_does_not_transfer",
    "non_falsum_clause_set_admits_selfdiff",
    "pure_transfer_above_point_iff_has_falsum_clause",
    "pure_transfers_above_point_iff_entails_irrefl",
    "reflexive_point_forces_singleton_f3_countermodel_above_point",
    "transfers_above_point_iff",
    "transfers_above_point_of_entails_reflexive_point_forces_singleton",
    "transfers_above_point_imp_entails_reflexive_point_forces_singleton",
)

# The Lean terminal pair.  Until the Lean stage ran this key held one
# LEAN_NOT_CARRIED string naming the part split as the blocker; that string
# was superseded by the stage's 23 theorems and is replaced here (receipt
# key `revision`), with what the theorems carry and what stays finite
# computation stated separately.
LEAN_TERMINALS: dict[str, str] = {
    "LEAN_CARRIED": (
        "LEAN_CARRIED -- S9.1: the seven step-13 targets proposed in "
        f"P1_FINDINGS.md section 8 are proved in {LEAN_MODULE} of this tree's "
        "research Lake package, whose #print axioms reports verify_lean.py "
        f"audits by hand: {LEAN_CARRIED_THEOREMS[0]} and "
        f"{LEAN_CARRIED_THEOREMS[1]} (every fragment under "
        f"TRANSFER_ALL_CARRIERS), {LEAN_CARRIED_THEOREMS[2]} and "
        f"{LEAN_CARRIED_THEOREMS[3]} (the step-13 question: a clause whose "
        "head is an atom does not transfer, the one-point full relation "
        "satisfying every clause set without a falsum head), "
        f"{LEAN_CARRIED_THEOREMS[4]} and {LEAN_CARRIED_THEOREMS[5]} (PURE "
        f"under TRANSFER_ABOVE_POINT), {LEAN_CARRIED_THEOREMS[6]} (r x x -> "
        "x = y, the F3 countermodel once the identity atom is admitted), "
        f"{LEAN_CARRIED_THEOREMS[7]} with {LEAN_CARRIED_THEOREMS[8]} and "
        f"{LEAN_CARRIED_THEOREMS[9]} (the above-the-point W identification, "
        "the latter under decidable identity on the carrier); the theorems "
        "quantify over every type and carry the transfer characterization "
        "and the three F3 terminals with no carrier bound, as the targets "
        "proposed"
    ),
    "LEAN_NOT_CARRIED": (
        "LEAN_NOT_CARRIED -- S9.1: the lattice of extents as an object (the "
        "closure sizes, closure_restriction, the classifier rows, "
        "W_in_lattice, unique_weakest, every lattice membership fact) is "
        f"finite computation bounded by N = {ATTEMPTED_CARRIER}, and no Lean "
        "theorem describes it; a syntactic characterization of transfer "
        "above the point with the identity atom admitted was neither "
        "proposed nor attempted; the converse of the above-the-point W "
        "identification without decidable identity is not attempted, the "
        "transfer hypothesis yielding only 'no y differs from x'"
    ),
}


def build_receipt(
    required: int = REQUIRED_CARRIER,
    attempted: int = ATTEMPTED_CARRIER,
    closure_bound: int = CLOSURE_BOUND,
) -> dict[str, object]:
    """The whole P1 receipt.  Deterministic; no timestamps, no paths."""

    check_carrier_bound(attempted)
    sweeps: dict[str, object] = {}
    completed: dict[str, bool] = {}
    results: dict[int, dict[str, dict[str, object]]] = {}
    tables: dict[int, RelationTable] = {}
    for max_n in sorted({required, attempted}):
        table = build_table(max_n)
        tables[max_n] = table
        raw_reflexive = reflexive_classes_from_raw_census(table)
        fragments = {
            f: analyze_fragment(f, table, closure_bound, raw_reflexive) for f in FRAGMENTS
        }
        results[max_n] = fragments
        hit = any(_fragment_hit(fragments[f]) for f in FRAGMENTS)
        completed[str(max_n)] = not hit
        sweeps[f"N{max_n}"] = {
            "carrier": max_n,
            "relation_census": {str(n): c for n, c in table.census.items()},
            "relation_total": sum(table.census.values()),
            "pattern_class_total": table.class_total,
            "closure_bound_hit_in_any_fragment": hit,
            "completed_inside_bound": not hit,
            "fragments": fragments,
        }
    lattice_terminal = (
        f"S9_1_LATTICE_COMPLETE -- the meet closure terminated below the "
        f"closure bound {closure_bound} for every fragment at N = {attempted}, "
        f"bounded by N = {attempted}: complete only as the lattice of extents "
        f"over carriers <= {attempted}, and an extent equality there is not an "
        f"equality at larger carriers"
        if completed[str(attempted)]
        else f"S9_1_LATTICE_BOUNDED -- the closure hit the bound {closure_bound} "
        f"at N = {attempted}, bounded by N = {attempted}; the partial closure is "
        f"reported truncated and the N = {required} result stands"
    )
    restriction: dict[str, object] = {
        "meaning": (
            f"the closure at N = {attempted} restricted onto carriers "
            f"1..{required}, per fragment; computed only when the two bounds "
            f"differ"
        )
    }
    if required != attempted:
        lower, upper = sorted((required, attempted))
        for fragment in FRAGMENTS:
            restriction[fragment] = closure_restriction(
                fragment, tables[upper], tables[lower], closure_bound
            )
    f3_terminals: dict[str, object] = {}
    transfer_terminals: dict[str, object] = {}
    for fragment in FRAGMENTS:
        f3_terminals[fragment] = {
            defn.name: f3_terminal(
                fragment,
                defn,
                _fragment_transfer(results[attempted][fragment], defn.name),
                attempted,
            )
            for defn in DEFINITIONS
        }
        transfer_terminals[fragment] = {
            defn.name: transfer_terminal(
                fragment,
                defn,
                _fragment_transfer(results[attempted][fragment], defn.name),
                attempted,
            )
            for defn in DEFINITIONS
        }
    return {
        "header": common.receipt_header(),
        "part": "P1",
        "subject": "S9.1, the axiom lattice",
        "revision": (
            "repair round 2: the reviewer defects recorded in P1_FINDINGS.md "
            "sections 11 and 12 are addressed in this receipt; repair after "
            "full-run audit 1 (STATUS.md): terminals.lean is the "
            "LEAN_CARRIED / LEAN_NOT_CARRIED pair naming the Lean stage's "
            "theorems, in place of the Python part's LEAN_NOT_CARRIED string "
            "that the stage had superseded; no count changed"
        ),
        "numbering_note": (
            "S9.1 is the first bullet of section S9 of "
            "paper/primitive_difference.md; the numbering is the prompt's, "
            "not the paper's"
        ),
        "authority_effect": "None",
        "declared_bounds": DECLARED_BOUNDS,
        "bounds_reached": {
            "carrier_required": required,
            "carrier_attempted": attempted,
            "carrier_completed_inside_bound": {k: v for k, v in completed.items()},
            "carrier_refused": refusal_record(REFUSED_CARRIER),
            "closure_bound": closure_bound,
        },
        "axiom_space": {
            "declaration": (
                "universally quantified Horn clauses over one binary relation "
                "r in at most two variables x, y; atoms r x x, r x y, r y x, "
                "r y y; head one atom or falsum; body any subset of atoms; an "
                "axiom is a finite set of clauses"
            ),
            "swap_quotient": (
                "clauses are quotiented by x <-> y; the swap fixes every "
                "extent, checked by computation"
            ),
            "one_variable_meaning": ONE_VARIABLE_MEANING,
            PURE: clause_space_report(PURE),
            EQ_BEARING: clause_space_report(EQ_BEARING),
            MERGED: clause_space_report(MERGED),
        },
        "eq_fragment": {
            "terminal": (
                "EQ_FRAGMENT_SEPARATED -- clauses mentioning x = y are "
                "enumerated as EQ_BEARING under their own key, with their own "
                "lattice and transfer analysis; the only object mixing them "
                "with the pure fragment is labelled MERGED_PURE_AND_EQ_BEARING "
                "and carries the merge sentence"
            ),
            "bill": "A3's (the metatheory's identity), not A1's, per S1",
        },
        "transfer_definitions": {
            defn.name: {
                "displayed": defn.displayed,
                "min_carrier": defn.min_carrier,
                "f3_set_empty_by_definitional_identity": (
                    defn.f3_set_empty_by_definitional_identity
                ),
                "why": defn.why,
            }
            for defn in DEFINITIONS
        },
        "entails_irreflexivity": ENTAILS_IRREFLEXIVITY_DISPLAYED,
        "f3_sweep_scope": (
            "the sweep decides nothing about F3 that a one-line argument per "
            "cell does not already decide: under TRANSFER_ALL_CARRIERS the "
            "conjecture is a tautology of the encoding, and under "
            "TRANSFER_ABOVE_POINT it fails exactly where the identity atom is "
            "admitted (by the generator r x x -> x = y) and holds in the pure "
            "fragment (no pure clause separates the one-point full relation "
            f"from the two-point full relation: checked at N = {attempted} and "
            "bounded by it; the general lemma is Lean target T7, not proved); "
            "so F3's truth value is set by whether the one-point carrier "
            "counts, and what the sweep adds is the bounded confirmation at N "
            "and the exact member listings"
        ),
        "order": ORDER_DECLARATION,
        "sweeps": sweeps,
        "closure_restriction": restriction,
        "terminals": {
            "lattice": lattice_terminal,
            "transfer": transfer_terminals,
            "f3": f3_terminals,
            "eq_fragment": "EQ_FRAGMENT_SEPARATED -- see eq_fragment.terminal",
            "refused": (
                f"REFUSED -- carrier N = {REFUSED_CARRIER} refused by name; see "
                f"bounds_reached.carrier_refused"
            ),
            "lean": LEAN_TERMINALS,
        },
    }
