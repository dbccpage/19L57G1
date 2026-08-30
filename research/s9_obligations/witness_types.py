"""P3 -- S9.3, proof-relevant witness types below function spaces.

PROMPT.md steps 21-25 (step 26's statements are proposed here and proved
by the Lean stage).  AuthorityEffect: None.  This module computes over a
declared finite space and proposes; it amends nothing sealed.

Declarations, in the order the prompt asks for them.  Every one of them
is also written into the receipt under a named key, and none of them is
changed by a computation.

Step 21, the witness-type layer against A2's bill (S1).  A2 supplies
``W : X -> X -> Nat`` with ``0 < W a b``.  This layer replaces the count
by a finite token domain ``T = {t0, ..., t(k-1)}`` with identity across
pairs: a *witness assignment* is a map from ordered pairs ``(x, y)`` of
the carrier to finite SUBSETS of ``T``.  Sets, not multisets, because
the layer replaces the count rather than adding to it: the A2 count is
recovered as the derived cardinality ``|S(x, y)|`` and is not admitted a
second time, and with token equality the only admitted judgement on
tokens, two occurrences of one token at one pair would be inseparable by
every expressible question -- a within-pair multiplicity would be A2's
count re-entering under a new name.

Admitted beyond A2, in one line:

    TOKEN_DOMAIN (a second finite sort T, distinct from the carrier) and
    TOKEN_EQ (a decidable equality judgement on T, admitted as a
    primitive, not derived); the named variant of V2 admits in addition
    TOKEN_NAMES (one object-language constant per element of T).

Pricing TOKEN_EQ against S1's bills: A1's bill is a type, one binary
relation symbol, and one asserted instance -- no axioms, no identity
relation of the object language.  TOKEN_EQ is an identity judgement, so
it is OUTSIDE A1's bill; it is an identity on the token sort, never on
the carrier, so it is strictly LESS than A3's bill, which imports the
metatheory's identity on the carrier itself through function types,
composition, and the one-point carrier -- none of which TOKEN_EQ uses.

Step 22, the vocabularies, each an explicit finite list of questions
with no function types (see ``vocabulary``):

    V0        presence(p)                    is the store at p nonempty
    V1        V0 + count_eq(p, q), count_lt(p, q)   cardinality comparisons
    V2_ANON   V0 + share(p, q)               do the stores at p and q share
                                              a token (uses TOKEN_EQ)
    V2_NAMED  V0 + token_at(t, p)            does the named token t occur
                                              at p (TOKEN_EQ + TOKEN_NAMES)
    V1_V2_ANON, V1_V2_NAMED                  the joins with V1

"Below function spaces" forbids, and ``refuse`` refuses by name: maps as
data (no question ranges over maps of any type, so family isomorphism is
not a question), composition (no witness at ``(x, z)`` is formed from
witnesses at ``(x, y)`` and ``(y, z)``, and no maps are composed), and
quotients (no quotient carrier by presence and no quotient token domain
by sharing is formed or asked about).

Enumeration order: ordered pairs are listed row-major, ``(0,0), (0,1),
...``; a store is a bit mask over T (bit i = token ti present); an
assignment is the tuple of masks; the order is lexicographic on that
tuple.  "First pair" always means the lexicographically least ``(A, B)``
with ``A < B`` among the pairs the key describes.  Every ``first_*``
value is the MINIMUM over all groups that hold such a pair, never the
pair of the first group visited (round-1 repair: two keys used to take
the first bucket in insertion order, whose least qualifying pair need
not be the least overall; an independent scan in the tests now checks
every ``first_*`` key).  Bucketing by answer vector IS the enumeration:
every assignment of the space is generated and keyed; the counts are
exact.

Bounds (PREFLIGHT.md step 4, P3): the numbers N = 2 required, N = 3
attempted, N = 4 refused; T = 2 required, T = 3 attempted, T = 4
refused; at most 2^20 assignments enumerated per (N, T) cell, applied
PER CELL as PREFLIGHT states it -- a cell whose declared assignment
space exceeds 2^20 is not enumerated in any of its spaces.  The declared
assignment space of a cell is A2's object over that cell (the
``witnessed`` space); the ``witnessed_irreflexive`` space is a sub-space
of it.  Cell (3, 3) therefore is not enumerated: its witnessed space has
117440512 assignments.  Its irreflexive sub-space (229376) is inside the
number and outside the rule; an earlier version of this part enumerated
it under a per-space reading, which departed from PREFLIGHT and is
withdrawn.  A per-space rule would be an amendment of PREFLIGHT, which
this part cannot make; it is proposed, not applied.

Wording rule (round-2 repair): a result seen in one cell is stated for
that cell by name, never by a phrase reaching past the bound (the
round-1 wording read the (2, 3) result as holding at every T from 3
up); the step-37 scanner in the tests now lists such phrases.  The
count-equal non-isomorphic invisible pairs are split by the invariant
they differ in (``non_isomorphic_count_equal_pairs_by_differing_
invariant``), so the sentence "every such pair differs in how many
tokens two pairs share" is a receipt value, not a reading of one pair.

The isomorphism of witness families used to classify invisible pairs is
metatheoretic apparatus (a bijection on the carrier fixing the
designated points plus a bijection on tokens transporting the
assignment); it is computed for step 24's characterization and step 26's
targets and is in no vocabulary.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations, product
from typing import Iterator, Sequence

import common

Assignment = tuple[int, ...]
Pair = tuple[int, int]

PART = "P3"
DESIGNATED: Pair = (0, 1)

# PREFLIGHT.md step 4, P3.  The numbers are copied from there; the rule
# when the assignment bound is hit is applied per CELL, as PREFLIGHT
# states it (see DECLARED_BOUNDS below and the module docstring).
CARRIER_REQUIRED = 2
CARRIER_ATTEMPTED = 3
CARRIER_REFUSED = 4
TOKENS_REQUIRED = 2
TOKENS_ATTEMPTED = 3
TOKENS_REFUSED = 4
ASSIGNMENT_BOUND = 1 << 20

CELLS: tuple[tuple[int, int], ...] = ((2, 2), (2, 3), (3, 2), (3, 3))
SPACES: tuple[str, ...] = ("witnessed", "witnessed_irreflexive")
VOCABULARIES: tuple[str, ...] = (
    "V0",
    "V1",
    "V2_ANON",
    "V2_NAMED",
    "V1_V2_ANON",
    "V1_V2_NAMED",
)

SPACE_DEFINITIONS: dict[str, str] = {
    "witnessed": (
        "A2's object: every map from ordered pairs to subsets of T whose "
        "store at the designated pair (0, 1) is nonempty; no other axiom"
    ),
    "witnessed_irreflexive": (
        "S7's object: witnessed, and every diagonal store (x, x) is empty, "
        "so the induced presence relation is irreflexive"
    ),
}

DECLARED_BOUNDS: dict[str, object] = {
    "carrier": {
        "required": CARRIER_REQUIRED,
        "attempted": CARRIER_ATTEMPTED,
        "refused_by_name": CARRIER_REFUSED,
    },
    "token_domain": {
        "required": TOKENS_REQUIRED,
        "attempted": TOKENS_ATTEMPTED,
        "refused_by_name": TOKENS_REFUSED,
    },
    "assignments_enumerated_per_cell_at_most": ASSIGNMENT_BOUND,
    "rule_when_hit": (
        "PREFLIGHT, verbatim: a cell whose declared assignment space "
        "exceeds 2^20 is not enumerated; it is reported as bounded with "
        "the cells that finished, each named by its (N, T)"
    ),
    "rule_unit": "cell",
    "cell_assignment_space": (
        "the declared assignment space of a cell (N, T) is A2's object over "
        "it, the witnessed space: every map from ordered pairs to subsets "
        "of T with the designated store nonempty; the witnessed_irreflexive "
        "space is a sub-space of it, so the union of the declared spaces of "
        "a cell is the witnessed space and its count is the cell's count"
    ),
    "application": (
        "a cell whose witnessed count exceeds the bound is not enumerated "
        "in any of its spaces; enumerate_space refuses every space of such "
        "a cell by name; nothing is extrapolated from the cells that "
        "finished"
    ),
    "withdrawn_application": (
        "an earlier version of this part applied the rule per SPACE and "
        "enumerated the witnessed_irreflexive sub-space of cell (3, 3), "
        "229376 assignments, while its witnessed space (117440512) was "
        "refused; that reading departed from PREFLIGHT's per-cell rule "
        "without saying so and is withdrawn in round 1; the numbers it "
        "produced are not part of this receipt"
    ),
    "proposed_amendment_not_made": (
        "a per-space rule (a space whose declared count exceeds 2^20 is not "
        "enumerated; a cell is reported bounded with the spaces that "
        "finished) would let the (3, 3) irreflexive sub-space be "
        "enumerated inside the same number; that is an amendment of "
        "PREFLIGHT.md, which this part does not own and does not make"
    ),
    "source": "research/s9_obligations/PREFLIGHT.md, step 4, P3",
}

ADMISSION: dict[str, object] = {
    "a2_bill": (
        "S1, A2: as A1, plus witness multiplicity; object "
        "(X, W : X -> X -> Nat, a, b) with 0 < W a b"
    ),
    "layer": (
        "a finite token domain T and a witness assignment "
        "S : (X x X) -> finite subsets of T, with S(a, b) nonempty"
    ),
    "store": "set",
    "why_sets": [
        "the layer replaces A2's count; the count is recovered as the "
        "derived cardinality |S(x, y)| and is not admitted a second time",
        "TOKEN_EQ is the only admitted judgement on tokens, so two "
        "occurrences of one token at one pair are inseparable by every "
        "expressible question; within-pair multiplicity would be A2's "
        "count re-entering under a new name",
        "it keeps the (N=3, T=2) cell inside the 2^20 bound: with sets the "
        "cell's declared assignment space (the witnessed space, the number "
        "the per-cell rule reads) has 196608 assignments, of a full space of "
        "4^9 = 262144; with multisets of multiplicity at most 2 the full "
        "space alone would be 3^18 = 387420489, over the bound",
    ],
    "admitted_beyond_a2": (
        "TOKEN_DOMAIN (a second finite sort T, distinct from the carrier) "
        "and TOKEN_EQ (a decidable equality judgement on T, admitted as a "
        "primitive, not derived); V2_NAMED admits in addition TOKEN_NAMES "
        "(one object-language constant per element of T)"
    ),
    "TOKEN_EQ": {
        "definition": "for tokens s, t of T: a decidable judgement s = t",
        "used_by": ["share(p, q)", "token_at(t, p)"],
        "price_vs_A1": (
            "outside A1's bill: A1 admits no identity relation of the "
            "object language, and TOKEN_EQ is one, on the token sort"
        ),
        "price_vs_A3": (
            "not contained in A3's bill, which it does not contain either: "
            "A3 imports the metatheory's identity on the CARRIER through "
            "function types, composition, and the one-point carrier; "
            "TOKEN_EQ is an identity on T only, says nothing about carrier "
            "points, and uses no function type, no composition, and no "
            "one-point carrier; the two bills are incomparable under "
            "inclusion of their listed items, and no ranking between them "
            "is claimed (no order on metatheory bills is declared in this "
            "tree)"
        ),
    },
    "TOKEN_NAMES": {
        "definition": "one object-language constant for each element of T",
        "used_by": ["token_at(t, p)"],
        "price": (
            "beyond TOKEN_EQ: a question may address a token by its "
            "metatheoretic name; the answers are then not invariant under "
            "token bijections (computed per enumerated space: the receipt "
            "key cells.<cell>.spaces.<space>.invariant_under_token_"
            "bijections.V2_NAMED is false in every enumerated space)"
        ),
    },
    "not_admitted": [
        "identity on the carrier",
        "function types, composition, quotients",
        "an order or a successor on T",
        "any axiom on the induced presence relation (the witnessed_"
        "irreflexive sub-space imposes irreflexivity as a filter on the "
        "same space, not as an admission)",
    ],
}

BELOW_FUNCTION_SPACES_FORBIDS: dict[str, str] = {
    "maps_as_data": (
        "no question takes, returns, or ranges over a map of any type "
        "(carrier maps, token maps, assignments as arguments); in "
        "particular 'is there a bijection carrying A onto B' is not a "
        "question"
    ),
    "composition": (
        "no question forms a witness at (x, z) from witnesses at (x, y) "
        "and (y, z), and no question composes maps"
    ),
    "quotients": (
        "no question is asked of a quotient carrier (points identified by "
        "presence) or a quotient token domain (tokens identified by "
        "sharing), and no assignment is formed by quotienting"
    ),
}

# (construction, which forbidden device it needs, why)
REFUSED_CONSTRUCTIONS: tuple[tuple[str, str, str], ...] = (
    (
        "family_isomorphism_as_question",
        "maps_as_data",
        "asks whether a carrier bijection and a token bijection carry one "
        "assignment onto another; it quantifies over maps",
    ),
    (
        "witness_composition",
        "composition",
        "forms a witness at (x, z) from witnesses at (x, y) and (y, z)",
    ),
    (
        "presence_quotient_of_carrier",
        "quotients",
        "identifies carrier points related by presence",
    ),
    (
        "sharing_quotient_of_tokens",
        "quotients",
        "identifies tokens that share a pair",
    ),
)


class BelowFunctionSpaces(Exception):
    """Raised, by name, when a construction needs a forbidden device."""


def refuse_map_as_datum(construction: str) -> None:
    raise BelowFunctionSpaces(
        f"refused by name: {construction} needs maps as data; below function "
        "spaces no question ranges over maps"
    )


def refuse_composition(construction: str) -> None:
    raise BelowFunctionSpaces(
        f"refused by name: {construction} needs composition; below function "
        "spaces no witnesses and no maps are composed"
    )


def refuse_quotient(construction: str) -> None:
    raise BelowFunctionSpaces(
        f"refused by name: {construction} needs a quotient; below function "
        "spaces no quotient carrier and no quotient token domain is formed"
    )


def refuse(construction: str) -> None:
    """Refuse a named construction from ``REFUSED_CONSTRUCTIONS``.

    Always raises: ``BelowFunctionSpaces`` for a listed construction,
    ``KeyError`` for an unlisted name (an unlisted construction is not
    refused silently; it is not known)."""

    for name, device, _why in REFUSED_CONSTRUCTIONS:
        if name == construction:
            if device == "maps_as_data":
                refuse_map_as_datum(name)
            if device == "composition":
                refuse_composition(name)
            refuse_quotient(name)
    raise KeyError(f"not a declared construction: {construction}")


# ---------------------------------------------------------------------------
# Carrier, pairs, stores
# ---------------------------------------------------------------------------


def ordered_pairs(n: int) -> list[Pair]:
    return [(x, y) for x in range(n) for y in range(n)]


def pair_index(n: int, x: int, y: int) -> int:
    return x * n + y


def token_names(t: int) -> list[str]:
    return [f"t{i}" for i in range(t)]


def store_tokens(mask: int, t: int) -> list[str]:
    return [f"t{i}" for i in range(t) if mask >> i & 1]


def render_assignment(a: Assignment, n: int, t: int) -> dict[str, object]:
    return {
        "masks": list(a),
        "stores": [
            {"pair": [x, y], "tokens": store_tokens(a[pair_index(n, x, y)], t)}
            for (x, y) in ordered_pairs(n)
        ],
    }


def enumeration_choices(n: int, t: int, space: str) -> list[range]:
    if space not in SPACES:
        raise KeyError(f"not a declared space: {space}")
    full = range(1 << t)
    nonempty = range(1, 1 << t)
    empty = range(0, 1)
    choices: list[range] = []
    for x, y in ordered_pairs(n):
        if (x, y) == DESIGNATED:
            choices.append(nonempty)
        elif space == "witnessed_irreflexive" and x == y:
            choices.append(empty)
        else:
            choices.append(full)
    return choices


def declared_assignment_count(n: int, t: int, space: str) -> int:
    count = 1
    for choice in enumeration_choices(n, t, space):
        count *= len(choice)
    return count


def full_space_count(n: int, t: int) -> int:
    """(2^t)^(n^2): every map from ordered pairs to subsets of T."""

    return 1 << (t * n * n)


def declared_cell_assignment_count(n: int, t: int) -> int:
    """The count of the cell's declared assignment space: the witnessed
    space (A2's object), of which every other declared space is a
    sub-space.  This is the number PREFLIGHT's per-cell rule reads."""

    return max(declared_assignment_count(n, t, space) for space in SPACES)


def cell_is_enumerated(n: int, t: int) -> bool:
    """PREFLIGHT's rule, per cell: enumerated iff the cell's declared
    assignment space is within the bound."""

    return declared_cell_assignment_count(n, t) <= ASSIGNMENT_BOUND


def enumerate_space(n: int, t: int, space: str) -> Iterator[Assignment]:
    """Every assignment of the space, in the declared (lexicographic)
    order.  Refuses by name a carrier or token domain beyond the declared
    bounds, and every space of a cell whose declared assignment space
    exceeds the per-cell assignment bound (PREFLIGHT.md step 4, P3)."""

    if n >= CARRIER_REFUSED:
        raise ValueError(f"carrier N = {n} is refused by name (bound N = {CARRIER_ATTEMPTED})")
    if t >= TOKENS_REFUSED:
        raise ValueError(f"token domain T = {t} is refused by name (bound T = {TOKENS_ATTEMPTED})")
    if space not in SPACES:
        raise KeyError(f"not a declared space: {space}")
    if not cell_is_enumerated(n, t):
        raise ValueError(
            f"cell (N={n}, T={t}) is refused by name: its declared assignment "
            f"space (witnessed) has {declared_cell_assignment_count(n, t)} "
            f"assignments, over the per-cell bound {ASSIGNMENT_BOUND}; no space "
            f"of the cell is enumerated (space {space} has "
            f"{declared_assignment_count(n, t, space)}; PREFLIGHT's rule is "
            "per cell, not per space)"
        )
    for a in product(*enumeration_choices(n, t, space)):
        yield tuple(a)


def is_witnessed(a: Assignment, n: int) -> bool:
    return a[pair_index(n, *DESIGNATED)] != 0


def is_irreflexive(a: Assignment, n: int) -> bool:
    return all(a[pair_index(n, x, x)] == 0 for x in range(n))


# ---------------------------------------------------------------------------
# Questions and vocabularies (step 22)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Question:
    """One expressible question.  ``args`` are carrier points and token
    indices only; no argument is a map."""

    kind: str
    args: tuple[int, ...]

    def text(self) -> str:
        if self.kind == "presence":
            x, y = self.args
            return f"presence({x},{y})"
        if self.kind == "token_at":
            tok, x, y = self.args
            return f"token_at(t{tok},({x},{y}))"
        x, y, u, v = self.args
        return f"{self.kind}(({x},{y}),({u},{v}))"


def presence_questions(n: int) -> list[Question]:
    return [Question("presence", (x, y)) for (x, y) in ordered_pairs(n)]


def count_questions(n: int) -> list[Question]:
    pairs = ordered_pairs(n)
    eq = [Question("count_eq", p + q) for p, q in combinations(pairs, 2)]
    lt = [Question("count_lt", p + q) for p, q in permutations(pairs, 2)]
    return eq + lt


def share_questions(n: int) -> list[Question]:
    return [Question("share", p + q) for p, q in combinations(ordered_pairs(n), 2)]


def token_questions(n: int, t: int) -> list[Question]:
    return [
        Question("token_at", (tok, x, y))
        for (x, y) in ordered_pairs(n)
        for tok in range(t)
    ]


def vocabulary(name: str, n: int, t: int) -> list[Question]:
    """The declared question list, in the declared order."""

    v0 = presence_questions(n)
    if name == "V0":
        return v0
    if name == "V1":
        return v0 + count_questions(n)
    if name == "V2_ANON":
        return v0 + share_questions(n)
    if name == "V2_NAMED":
        return v0 + token_questions(n, t)
    if name == "V1_V2_ANON":
        return v0 + count_questions(n) + share_questions(n)
    if name == "V1_V2_NAMED":
        return v0 + count_questions(n) + token_questions(n, t)
    raise KeyError(f"not a declared vocabulary: {name}")


def vocabulary_size_formula(name: str, n: int, t: int) -> int:
    """Arithmetic size of the declared question list (checked by test
    against the enumerated list)."""

    m = n * n
    pres = m
    cnt = m * (m - 1) // 2 + m * (m - 1)
    share = m * (m - 1) // 2
    tok = t * m
    return {
        "V0": pres,
        "V1": pres + cnt,
        "V2_ANON": pres + share,
        "V2_NAMED": pres + tok,
        "V1_V2_ANON": pres + cnt + share,
        "V1_V2_NAMED": pres + cnt + tok,
    }[name]


def evaluate(q: Question, a: Assignment, n: int) -> bool:
    """Generic evaluation of one question on one assignment."""

    if q.kind == "presence":
        x, y = q.args
        return a[pair_index(n, x, y)] != 0
    if q.kind == "token_at":
        tok, x, y = q.args
        return (a[pair_index(n, x, y)] >> tok) & 1 == 1
    x, y, u, v = q.args
    left = a[pair_index(n, x, y)]
    right = a[pair_index(n, u, v)]
    if q.kind == "count_eq":
        return left.bit_count() == right.bit_count()
    if q.kind == "count_lt":
        return left.bit_count() < right.bit_count()
    if q.kind == "share":
        return left & right != 0
    raise KeyError(f"not a declared question kind: {q.kind}")


def answer_vector(questions: Sequence[Question], a: Assignment, n: int) -> int:
    """The answers packed as bits: bit i is the answer to question i."""

    bits = 0
    for i, q in enumerate(questions):
        if evaluate(q, a, n):
            bits |= 1 << i
    return bits


def differing_questions(
    questions: Sequence[Question], a: Assignment, b: Assignment, n: int
) -> list[Question]:
    return [q for q in questions if evaluate(q, a, n) != evaluate(q, b, n)]


class Keyer:
    """Answer vectors for all six vocabularies, computed directly from the
    masks and packed in the same bit order as ``answer_vector``.  A test
    checks the two agree on whole cells."""

    def __init__(self, n: int, t: int) -> None:
        self.n = n
        self.t = t
        m = n * n
        self.pairs_eq = list(combinations(range(m), 2))
        self.pairs_lt = [(p, q) for p in range(m) for q in range(m) if p != q]
        self.len_pres = m
        self.len_cnt = len(self.pairs_eq) + len(self.pairs_lt)
        self._cnt_memo: dict[tuple[int, ...], int] = {}

    def parts(self, a: Assignment) -> tuple[int, int, int, int]:
        counts = tuple(mask.bit_count() for mask in a)
        pres = 0
        for i, c in enumerate(counts):
            if c:
                pres |= 1 << i
        cnt = self._cnt_memo.get(counts)
        if cnt is None:
            cnt = 0
            bit = 0
            for p, q in self.pairs_eq:
                if counts[p] == counts[q]:
                    cnt |= 1 << bit
                bit += 1
            for p, q in self.pairs_lt:
                if counts[p] < counts[q]:
                    cnt |= 1 << bit
                bit += 1
            self._cnt_memo[counts] = cnt
        share = 0
        for bit, (p, q) in enumerate(self.pairs_eq):
            if a[p] & a[q]:
                share |= 1 << bit
        tok = 0
        for p, mask in enumerate(a):
            tok |= mask << (p * self.t)
        return pres, cnt, share, tok

    def keys(self, a: Assignment) -> dict[str, int]:
        pres, cnt, share, tok = self.parts(a)
        lp = self.len_pres
        lpc = self.len_pres + self.len_cnt
        return {
            "V0": pres,
            "V1": pres | cnt << lp,
            "V2_ANON": pres | share << lp,
            "V2_NAMED": pres | tok << lp,
            "V1_V2_ANON": pres | cnt << lp | share << lpc,
            "V1_V2_NAMED": pres | cnt << lp | tok << lpc,
        }


# ---------------------------------------------------------------------------
# Metatheoretic apparatus: isomorphism of witness families (step 26's
# definition), token-bijection action, classifying invariants.  None of
# this is a question of any vocabulary.
# ---------------------------------------------------------------------------


def carrier_bijections_fixing_designated(n: int) -> list[tuple[int, ...]]:
    a, b = DESIGNATED
    return [f for f in permutations(range(n)) if f[a] == a and f[b] == b]


def token_bijections(t: int) -> list[tuple[int, ...]]:
    return [tuple(p) for p in permutations(range(t))]


def act_mask(mask: int, tau: tuple[int, ...]) -> int:
    out = 0
    for i, target in enumerate(tau):
        if mask >> i & 1:
            out |= 1 << target
    return out


def transport(
    a: Assignment, n: int, f: tuple[int, ...], tau: tuple[int, ...]
) -> Assignment:
    """B(f x, f y) = tau[S(x, y)]: the transported assignment."""

    out = [0] * (n * n)
    for x, y in ordered_pairs(n):
        out[pair_index(n, f[x], f[y])] = act_mask(a[pair_index(n, x, y)], tau)
    return tuple(out)


class Transporter:
    """All transports of an assignment, with the token action tabulated
    once per bijection.  Same function as ``transport``; checked equal by
    test."""

    def __init__(self, n: int, t: int) -> None:
        self.n = n
        self.carrier = carrier_bijections_fixing_designated(n)
        self.tokens = token_bijections(t)
        self.tables = [[act_mask(m, tau) for m in range(1 << t)] for tau in self.tokens]
        self.identity = tuple(range(n))
        self.pair_targets = [
            [pair_index(n, f[x], f[y]) for (x, y) in ordered_pairs(n)] for f in self.carrier
        ]

    def transports(self, a: Assignment) -> Iterator[Assignment]:
        for f, targets in zip(self.carrier, self.pair_targets):
            for table in self.tables:
                if f == self.identity:
                    yield tuple(table[m] for m in a)
                else:
                    out = [0] * (self.n * self.n)
                    for src, dst in enumerate(targets):
                        out[dst] = table[a[src]]
                    yield tuple(out)

    def token_transports(self, a: Assignment) -> Iterator[Assignment]:
        for table in self.tables:
            yield tuple(table[m] for m in a)

    def least_transport(self, a: Assignment) -> Assignment:
        return min(self.transports(a))


def least_transport(a: Assignment, n: int, t: int) -> Assignment:
    """Least transport over all (f, tau); two assignments have the same
    least transport exactly when they are isomorphic as witness families
    (checked against ``family_isomorphic_metatheory`` by test)."""

    best = a
    for f in carrier_bijections_fixing_designated(n):
        for tau in token_bijections(t):
            candidate = transport(a, n, f, tau)
            if candidate < best:
                best = candidate
    return best


def family_isomorphic_metatheory(a: Assignment, b: Assignment, n: int, t: int) -> bool:
    """Metatheoretic classification, by exhaustive search over the
    bijections; never a question."""

    return any(
        transport(a, n, f, tau) == b
        for f in carrier_bijections_fixing_designated(n)
        for tau in token_bijections(t)
    )


def token_degree_multiset(a: Assignment, t: int) -> list[int]:
    """For each token, the number of ordered pairs whose store holds it;
    sorted, so it is a token-bijection invariant."""

    return sorted(sum(mask >> i & 1 for mask in a) for i in range(t))


def intersection_profile(a: Assignment) -> list[int]:
    """|S(p) & S(q)| for p < q in the declared pair order."""

    return [(a[p] & a[q]).bit_count() for p, q in combinations(range(len(a)), 2)]


def common_token_count(a: Assignment) -> int:
    """Tokens held by every nonempty store."""

    nonempty = [mask for mask in a if mask]
    acc = -1
    for mask in nonempty:
        acc &= mask
    return acc.bit_count() if nonempty else 0


def count_vector(a: Assignment) -> list[int]:
    """A2's W recovered: |S(p)| per ordered pair."""

    return [mask.bit_count() for mask in a]


INVARIANTS: tuple[str, ...] = (
    "count_vector",
    "intersection_profile",
    "token_degree_multiset",
    "common_token_count",
)


def invariants(a: Assignment, t: int) -> dict[str, object]:
    """Token-bijection (and point-fixing carrier-bijection) invariants used
    only to say what an invisible non-isomorphic pair differs by."""

    return {
        "count_vector": count_vector(a),
        "intersection_profile": intersection_profile(a),
        "token_degree_multiset": token_degree_multiset(a, t),
        "common_token_count": common_token_count(a),
    }


def invariant_tuple(a: Assignment, t: int) -> tuple[tuple[int, ...], ...]:
    """The same invariants as hashable tuples, in ``INVARIANTS`` order."""

    return (
        tuple(count_vector(a)),
        tuple(intersection_profile(a)),
        tuple(token_degree_multiset(a, t)),
        (common_token_count(a),),
    )


# ---------------------------------------------------------------------------
# Bucketing (the enumeration) and the two directions (steps 23, 24)
# ---------------------------------------------------------------------------


def group_by_key(keys: Sequence[int]) -> dict[int, list[int]]:
    groups: dict[int, list[int]] = {}
    for i, k in enumerate(keys):
        groups.setdefault(k, []).append(i)
    return groups


def refines(groups_p: dict[int, list[int]], keys_q: Sequence[int]) -> bool:
    """P refines Q: every P-bucket lies inside one Q-bucket, i.e. P sees
    every separation Q sees."""

    for members in groups_p.values():
        k0 = keys_q[members[0]]
        if any(keys_q[i] != k0 for i in members):
            return False
    return True


def separating_pairs(
    groups_p: dict[int, list[int]], keys_q: Sequence[int]
) -> tuple[int, tuple[int, int] | None]:
    """Pairs equal under P and different under Q: their count and the
    lexicographically first."""

    pair_count = 0
    first: tuple[int, int] | None = None
    for members in groups_p.values():
        if len(members) < 2:
            continue
        sub: dict[int, int] = {}
        for i in members:
            sub[keys_q[i]] = sub.get(keys_q[i], 0) + 1
        if len(sub) < 2:
            continue
        s = len(members)
        pair_count += (s * s - sum(c * c for c in sub.values())) // 2
        if first is None:
            i0 = members[0]
            j = next(i for i in members if keys_q[i] != keys_q[i0])
            first = (i0, j)
    return pair_count, first


@dataclass
class Invisible:
    pair_count: int
    isomorphic_pair_count: int
    non_isomorphic_pair_count: int
    first_pair: tuple[int, int] | None
    first_non_isomorphic_pair: tuple[int, int] | None
    invariant_counts: dict[str, int]
    first_pair_no_invariant_differs: tuple[int, int] | None
    non_isomorphic_count_equal_pair_count: int
    first_non_isomorphic_count_equal_pair: tuple[int, int] | None
    count_equal_invariant_counts: dict[str, int]


COUNT_EQUAL_INVARIANTS: tuple[str, ...] = tuple(
    name for name in INVARIANTS if name != "count_vector"
)


def pairs_within(sizes: Sequence[int]) -> int:
    return sum(c * (c - 1) // 2 for c in sizes)


def first_split(members: Sequence[int], canon: Sequence[Assignment]) -> tuple[int, int] | None:
    """The lexicographically first pair of ``members`` (given in
    increasing order) in different isomorphism classes, if any."""

    i0 = members[0]
    for j in members:
        if canon[j] != canon[i0]:
            return (i0, j)
    return None


def least_pair(
    current: tuple[int, int] | None, candidate: tuple[int, int] | None
) -> tuple[int, int] | None:
    """The lexicographically least of two optional index pairs.  Indices
    follow enumeration order, so the least index pair is the least
    ``(A, B)`` as assignments."""

    if current is None:
        return candidate
    if candidate is None:
        return current
    return min(current, candidate)


def invisible_pairs(
    groups_q: dict[int, list[int]],
    canon: Sequence[Assignment],
    inv: Sequence[tuple[tuple[int, ...], ...]],
) -> Invisible:
    """Distinct assignments with identical Q answers: count, first pair,
    the split into isomorphic (a renaming) and non-isomorphic families,
    and for the latter the computed invariants that tell them apart --
    all from class sizes inside each bucket, never from a pair loop.

    Every ``first_*`` value is the least qualifying pair over ALL groups.
    For ``first`` and ``first_noniso`` the least pair's left member is
    the first member of the first qualifying bucket in insertion order
    (buckets are inserted in order of their first member, and a bucket's
    first member is always a left member of a qualifying pair when the
    bucket holds one), so the first bucket visited suffices; for the
    count-equal and joint-invariant groups inside a bucket it does not --
    a later bucket with an earlier first member can hold a smaller pair
    -- so those two are taken as the minimum over every group (round-1
    repair; the old code took the first bucket visited and reported a
    non-least pair in two spaces).  An independent scan in the tests
    checks every ``first_*`` key."""

    pair_count = 0
    iso_pairs = 0
    first: tuple[int, int] | None = None
    first_noniso: tuple[int, int] | None = None
    first_none: tuple[int, int] | None = None
    first_count_equal: tuple[int, int] | None = None
    count_equal_noniso = 0
    counts = {name: 0 for name in INVARIANTS}
    counts["none_of_the_computed_invariants"] = 0
    # Round-2 addition: among the count-equal non-isomorphic pairs, how many
    # differ in each of the remaining invariants (count_vector is equal on
    # every such pair by definition of the group).
    ce_counts = {name: 0 for name in COUNT_EQUAL_INVARIANTS}
    ce_counts["none_of_the_computed_invariants"] = 0
    count_index = INVARIANTS.index("count_vector")
    for members in groups_q.values():
        s = len(members)
        if s < 2:
            continue
        bucket_pairs = s * (s - 1) // 2
        pair_count += bucket_pairs
        first = least_pair(first, (members[0], members[1]))
        classes: dict[Assignment, int] = {}
        for i in members:
            classes[canon[i]] = classes.get(canon[i], 0) + 1
        iso_pairs += pairs_within(list(classes.values()))
        if len(classes) < 2:
            continue
        first_noniso = least_pair(first_noniso, first_split(members, canon))
        # Every invariant is constant on an isomorphism class (checked by
        # test), so pairs differing in an invariant are non-isomorphic and
        # number the bucket's pairs minus the pairs inside one value.
        per_invariant: list[dict[tuple[int, ...], int]] = [{} for _ in INVARIANTS]
        joint: dict[tuple[tuple[int, ...], ...], list[int]] = {}
        by_count: dict[tuple[int, ...], list[int]] = {}
        for i in members:
            values = inv[i]
            for k, value in enumerate(values):
                per_invariant[k][value] = per_invariant[k].get(value, 0) + 1
            joint.setdefault(values, []).append(i)
            by_count.setdefault(values[count_index], []).append(i)
        for k, name in enumerate(INVARIANTS):
            counts[name] += bucket_pairs - pairs_within(list(per_invariant[k].values()))
        for same_counts in by_count.values():
            inner: dict[Assignment, int] = {}
            ce_per_invariant: list[dict[tuple[int, ...], int]] = [{} for _ in INVARIANTS]
            ce_joint: dict[tuple[tuple[int, ...], ...], list[int]] = {}
            for i in same_counts:
                inner[canon[i]] = inner.get(canon[i], 0) + 1
                values = inv[i]
                for k, value in enumerate(values):
                    ce_per_invariant[k][value] = ce_per_invariant[k].get(value, 0) + 1
                ce_joint.setdefault(values, []).append(i)
            group_pairs = pairs_within([len(same_counts)])
            hidden = group_pairs - pairs_within(list(inner.values()))
            count_equal_noniso += hidden
            if hidden:
                first_count_equal = least_pair(first_count_equal, first_split(same_counts, canon))
            for k, name in enumerate(INVARIANTS):
                if name in ce_counts:
                    ce_counts[name] += group_pairs - pairs_within(list(ce_per_invariant[k].values()))
            for same_invariants_ce in ce_joint.values():
                inner_ce: dict[Assignment, int] = {}
                for i in same_invariants_ce:
                    inner_ce[canon[i]] = inner_ce.get(canon[i], 0) + 1
                ce_counts["none_of_the_computed_invariants"] += pairs_within(
                    [len(same_invariants_ce)]
                ) - pairs_within(list(inner_ce.values()))
        for same_invariants in joint.values():
            inner = {}
            for i in same_invariants:
                inner[canon[i]] = inner.get(canon[i], 0) + 1
            hidden = pairs_within([len(same_invariants)]) - pairs_within(list(inner.values()))
            counts["none_of_the_computed_invariants"] += hidden
            if hidden:
                first_none = least_pair(first_none, first_split(same_invariants, canon))
    return Invisible(
        pair_count=pair_count,
        isomorphic_pair_count=iso_pairs,
        non_isomorphic_pair_count=pair_count - iso_pairs,
        first_pair=first,
        first_non_isomorphic_pair=first_noniso,
        invariant_counts=counts,
        first_pair_no_invariant_differs=first_none,
        non_isomorphic_count_equal_pair_count=count_equal_noniso,
        first_non_isomorphic_count_equal_pair=first_count_equal,
        count_equal_invariant_counts=ce_counts,
    )


SEPARATIONS: tuple[tuple[str, str], ...] = (
    ("V0", "V1"),
    ("V1", "V2_ANON"),
    ("V1", "V2_NAMED"),
    ("V2_ANON", "V1"),
    ("V2_ANON", "V2_NAMED"),
    ("V1_V2_ANON", "V1_V2_NAMED"),
)

INVISIBLE_IN: tuple[str, ...] = ("V2_ANON", "V2_NAMED", "V1_V2_ANON", "V1_V2_NAMED")


def render_pair(
    pair: tuple[int, int] | None,
    assignments: Sequence[Assignment],
    n: int,
    t: int,
) -> dict[str, object] | None:
    if pair is None:
        return None
    i, j = pair
    return {
        "left_index": i,
        "right_index": j,
        "left": render_assignment(assignments[i], n, t),
        "right": render_assignment(assignments[j], n, t),
    }


def analyze_space(n: int, t: int, space: str) -> dict[str, object]:
    """Steps 23 and 24 over one enumerated space."""

    assignments = list(enumerate_space(n, t, space))
    if len(assignments) != declared_assignment_count(n, t, space):
        raise AssertionError("enumeration count differs from the declared count")
    keyer = Keyer(n, t)
    keys: dict[str, list[int]] = {name: [] for name in VOCABULARIES}
    for a in assignments:
        for name, k in keyer.keys(a).items():
            keys[name].append(k)
    groups = {name: group_by_key(keys[name]) for name in VOCABULARIES}
    transporter = Transporter(n, t)
    canon = [transporter.least_transport(a) for a in assignments]
    inv = [invariant_tuple(a, t) for a in assignments]
    index_of = {a: i for i, a in enumerate(assignments)}

    # Computed invariance of each vocabulary under token bijections.
    invariant: dict[str, bool] = {}
    for name in VOCABULARIES:
        ok = True
        for i, a in enumerate(assignments):
            for image in transporter.token_transports(a):
                if keys[name][index_of[image]] != keys[name][i]:
                    ok = False
                    break
            if not ok:
                break
        invariant[name] = ok

    refinement: dict[str, bool] = {}
    for p in VOCABULARIES:
        for q in VOCABULARIES:
            if p != q:
                refinement[f"{p} refines {q}"] = refines(groups[p], keys[q])

    separating: dict[str, object] = {}
    for p, q in SEPARATIONS:
        count, first = separating_pairs(groups[p], keys[q])
        entry: dict[str, object] = {
            "coarse": p,
            "fine": q,
            "meaning": f"pairs with identical {p} answers and some differing {q} answer",
            "pair_count": count,
            "exists": count > 0,
            "first_pair": render_pair(first, assignments, n, t),
        }
        if first is not None:
            i, j = first
            diff_q = differing_questions(vocabulary(q, n, t), assignments[i], assignments[j], n)
            diff_p = differing_questions(vocabulary(p, n, t), assignments[i], assignments[j], n)
            entry["coarse_differing_question_count"] = len(diff_p)
            entry["fine_differing_question_count"] = len(diff_q)
            entry["first_fine_differing_question"] = diff_q[0].text()
        separating[f"{p}_vs_{q}"] = entry

    def characterize(pair: tuple[int, int]) -> dict[str, object]:
        i, j = pair
        left = invariants(assignments[i], t)
        right = invariants(assignments[j], t)
        return {
            "differing_pairs": [
                [x, y]
                for (x, y) in ordered_pairs(n)
                if assignments[i][pair_index(n, x, y)] != assignments[j][pair_index(n, x, y)]
            ],
            "isomorphic_as_families": family_isomorphic_metatheory(
                assignments[i], assignments[j], n, t
            ),
            "left_invariants": left,
            "right_invariants": right,
            "invariants_that_differ": [
                name for name in INVARIANTS if left[name] != right[name]
            ],
        }

    invisible: dict[str, object] = {}
    for q in INVISIBLE_IN:
        found = invisible_pairs(groups[q], canon, inv)
        entry = {
            "vocabulary": q,
            "meaning": f"distinct assignments with identical answers to every {q} question",
            "pair_count": found.pair_count,
            "exists": found.pair_count > 0,
            "isomorphic_pair_count": found.isomorphic_pair_count,
            "non_isomorphic_pair_count": found.non_isomorphic_pair_count,
            "first_pair": render_pair(found.first_pair, assignments, n, t),
            "first_non_isomorphic_pair": render_pair(
                found.first_non_isomorphic_pair, assignments, n, t
            ),
            "non_isomorphic_pairs_by_differing_invariant": found.invariant_counts,
            "first_non_isomorphic_pair_no_invariant_differs": render_pair(
                found.first_pair_no_invariant_differs, assignments, n, t
            ),
            "non_isomorphic_count_equal_pair_count": found.non_isomorphic_count_equal_pair_count,
            "first_non_isomorphic_count_equal_pair": render_pair(
                found.first_non_isomorphic_count_equal_pair, assignments, n, t
            ),
            "non_isomorphic_count_equal_pairs_by_differing_invariant": found.count_equal_invariant_counts,
            "every_non_isomorphic_count_equal_pair_differs_in_intersection_profile": (
                found.count_equal_invariant_counts["intersection_profile"]
                == found.non_isomorphic_count_equal_pair_count
            ),
        }
        if found.first_pair is not None:
            entry["first_pair_characterization"] = characterize(found.first_pair)
        if found.first_non_isomorphic_pair is not None:
            entry["first_non_isomorphic_pair_characterization"] = characterize(
                found.first_non_isomorphic_pair
            )
        if found.first_non_isomorphic_count_equal_pair is not None:
            entry["first_non_isomorphic_count_equal_pair_characterization"] = characterize(
                found.first_non_isomorphic_count_equal_pair
            )
        if found.first_pair_no_invariant_differs is not None:
            entry["first_non_isomorphic_pair_no_invariant_differs_characterization"] = (
                characterize(found.first_pair_no_invariant_differs)
            )
        invisible[q] = entry

    class_sizes: dict[Assignment, int] = {}
    for c in canon:
        class_sizes[c] = class_sizes.get(c, 0) + 1

    return {
        "space": space,
        "definition": SPACE_DEFINITIONS[space],
        "enumerated": True,
        "bounded": False,
        "bound_reached": "none: the whole declared space was enumerated",
        "assignment_count": len(assignments),
        "first_assignment": render_assignment(assignments[0], n, t),
        "partition_class_counts": {name: len(groups[name]) for name in VOCABULARIES},
        "isomorphism_class_count": len(class_sizes),
        "isomorphic_pair_count_total": sum(c * (c - 1) // 2 for c in class_sizes.values()),
        "invariant_under_token_bijections": invariant,
        "refinement": refinement,
        "separating": separating,
        "invisible": invisible,
    }


def analyze_cell(n: int, t: int) -> dict[str, object]:
    """One cell under PREFLIGHT's per-cell rule: every declared space is
    enumerated, or none is."""

    spaces: dict[str, object] = {}
    notes: list[str] = []
    cell_count = declared_cell_assignment_count(n, t)
    enumerated = cell_is_enumerated(n, t)
    if not enumerated:
        notes.append(
            f"cell not enumerated: its declared assignment space (witnessed) "
            f"has {cell_count} assignments, over the per-cell bound "
            f"{ASSIGNMENT_BOUND} (PREFLIGHT.md step 4, P3, rule applied per "
            "cell)"
        )
    for space in SPACES:
        declared = declared_assignment_count(n, t, space)
        if not enumerated:
            notes.append(f"space {space}: {declared} assignments, not enumerated")
            spaces[space] = {
                "space": space,
                "definition": SPACE_DEFINITIONS[space],
                "enumerated": False,
                "bounded": True,
                "bound_reached": (
                    f"per-cell assignment-count bound {ASSIGNMENT_BOUND}: the "
                    f"cell's declared assignment space has {cell_count} "
                    f"assignments; this space alone has {declared}, which is "
                    "not the number the rule reads"
                ),
                "declared_assignment_count": declared,
            }
        else:
            notes.append(f"space {space}: {declared} assignments enumerated")
            spaces[space] = analyze_space(n, t, space)
    return {
        "cell": f"N{n}_T{t}",
        "n": n,
        "t": t,
        "full_space_count": full_space_count(n, t),
        "declared_assignment_counts": {
            space: declared_assignment_count(n, t, space) for space in SPACES
        },
        "declared_cell_assignment_count": cell_count,
        "vocabulary_sizes": {
            name: len(vocabulary(name, n, t)) for name in VOCABULARIES
        },
        "enumerated": enumerated,
        "bounded": not enumerated,
        "bound_reached": "; ".join(notes),
        "spaces": spaces,
    }


# ---------------------------------------------------------------------------
# Lean targets (step 26, proposed only) rendered from the computed pairs
# ---------------------------------------------------------------------------


def lean_definition(name: str, a: Assignment, n: int, t: int) -> str:
    """A concrete finite definition of an assignment over carrier Bool
    (n = 2) as ``Bool -> Bool -> Fin t -> Bool``; ASCII only."""

    if n != 2:
        raise ValueError("Lean targets are rendered for carrier Bool only")
    arms: list[str] = []
    for x, y in ordered_pairs(n):
        for tok in range(t):
            if a[pair_index(n, x, y)] >> tok & 1:
                bx = "true" if x else "false"
                by = "true" if y else "false"
                arms.append(f"| {bx}, {by}, {tok} => true")
    body = " ".join(arms + ["| _, _, _ => false"])
    return f"def {name} : Bool -> Bool -> Fin {t} -> Bool := fun x y t => match x, y, t.val with {body}"


def _pair_from(entry: object, side: str) -> Assignment:
    if not isinstance(entry, dict):
        raise ValueError("no computed pair to render")
    side_obj = entry[side]
    if not isinstance(side_obj, dict):
        raise ValueError("no computed pair to render")
    masks = side_obj["masks"]
    if not isinstance(masks, list):
        raise ValueError("no computed pair to render")
    return tuple(int(m) for m in masks)


def lean_targets(cells: dict[str, object]) -> list[dict[str, object]]:
    """The step-26 proposals, with the pairs taken from the computation
    (the witnessed_irreflexive space, S7's object), never hand-picked."""

    def space(cell: str) -> dict[str, object]:
        c = cells[cell]
        assert isinstance(c, dict)
        s = c["spaces"]
        assert isinstance(s, dict)
        w = s["witnessed_irreflexive"]
        assert isinstance(w, dict)
        return w

    sep = space("N2_T2")["separating"]
    assert isinstance(sep, dict)
    sep_entry = sep["V1_vs_V2_ANON"]
    assert isinstance(sep_entry, dict)
    sep_pair = sep_entry["first_pair"]
    w1 = _pair_from(sep_pair, "left")
    w2 = _pair_from(sep_pair, "right")

    inv = space("N2_T3")["invisible"]
    assert isinstance(inv, dict)
    inv_entry = inv["V1_V2_ANON"]
    assert isinstance(inv_entry, dict)
    inv_pair = inv_entry["first_non_isomorphic_count_equal_pair"]
    targets: list[dict[str, object]] = [
        {
            "name": "S9_3_sep_W1_W2_definitions",
            "cell": "N2_T2",
            "space": "witnessed_irreflexive",
            "definitions": [lean_definition("W1", w1, 2, 2), lean_definition("W2", w2, 2, 2)],
            "encoding": (
                "carrier Bool with designated (false, true); token domain Fin 2; "
                "an assignment is W : Bool -> Bool -> Fin 2 -> Bool, W x y t = true "
                "meaning token t occurs at (x, y); the function type is the "
                "metatheory's encoding of a finite table, not an object-language "
                "device"
            ),
        },
        {
            "name": "S9_3_sep_presence_equal",
            "statement": (
                "forall x y : Bool, (exists t : Fin 2, W1 x y t = true) <-> "
                "(exists t : Fin 2, W2 x y t = true)"
            ),
            "proof_route": "decide (finite quantifiers over Bool and Fin 2)",
        },
        {
            "name": "S9_3_sep_count_equal",
            "statement": (
                "forall x y : Bool, card (W1 x y) = card (W2 x y), where "
                "card w := (if w 0 then 1 else 0) + (if w 1 then 1 else 0)"
            ),
            "proof_route": "decide",
        },
        {
            "name": "S9_3_sep_V1_indistinguishable",
            "statement": (
                "forall q in V1_list, evalV1 q W1 = evalV1 q W2, with V1_list "
                "the explicit list of the 4 presence, 6 count_eq, and 12 count_lt "
                "questions (22 questions) as an inductive Q and evalV1 : Q -> "
                "(Bool -> Bool -> Fin 2 -> Bool) -> Bool"
            ),
            "proof_route": "decide over the explicit list",
            "formalizable": True,
            "residual": (
                "the list is written by hand in Lean; that it equals the "
                "Python vocabulary V1 at (N=2, T=2) is checked by no gate -- the "
                "encoding (a hand-written finite list of decidable questions) is "
                "the named residual, not an obstacle to the proof"
            ),
        },
        {
            "name": "S9_3_sep_V2_ANON_separates",
            "statement": (
                "(exists t : Fin 2, W1 false true t = true /\\ W1 true false t = true) "
                "/\\ not (exists t : Fin 2, W2 false true t = true /\\ W2 true false t = true)"
            ),
            "proof_route": "decide",
        },
        {
            "name": "S9_3_sep_not_isomorphic",
            "definition_of_isomorphism": (
                "WitnessIso W W' := exists (s : Bool -> Bool) (r : Fin 2 -> Fin 2), "
                "s false = false /\\ s true = true /\\ Function.Bijective s /\\ "
                "Function.Bijective r /\\ forall x y t, W x y t = W' (s x) (s y) (r t)"
            ),
            "statement": "not (WitnessIso W1 W2)",
            "proof_route": (
                "not decide: the quantifiers range over function types. Route: "
                "from a transport at (false, true, t0) and (true, false, t0) with "
                "s point-fixing, obtain W2 false true (r t0) = true and W2 true "
                "false (r t0) = true, then case on r t0 : Fin 2 and close by "
                "decide; constructive, no choice"
            ),
            "formalizable": True,
            "obstacle_named": (
                "quantification over bijections of a function type is not "
                "decidable in core without a finite enumeration of the function "
                "type; the invariant route avoids it"
            ),
        },
        {
            "name": "S9_3_inv_W3_W4_definitions",
            "cell": "N2_T3",
            "space": "witnessed_irreflexive",
            "definitions": (
                [
                    lean_definition("W3", _pair_from(inv_pair, "left"), 2, 3),
                    lean_definition("W4", _pair_from(inv_pair, "right"), 2, 3),
                ]
                if inv_pair is not None
                else []
            ),
            "statements": [
                "S9_3_inv_V1_V2_ANON_indistinguishable: forall q in V1_V2_ANON_list "
                "(4 + 18 + 6 = 28 questions), eval q W3 = eval q W4 -- decide over "
                "the explicit list",
                "S9_3_inv_count_equal: forall x y, card3 (W3 x y) = card3 (W4 x y) "
                "-- decide; this pair is chosen as the first V1_V2_ANON-invisible "
                "non-isomorphic pair with equal count vectors, so what it hides "
                "is token-level, not count magnitude",
                "S9_3_inv_not_isomorphic: not (WitnessIso W3 W4) over Fin 3 -- by "
                "the invariant that differs in the receipt "
                "(first_non_isomorphic_count_equal_pair_characterization), "
                "transported by any (s, r); not decide",
            ],
            "present": inv_pair is not None,
        },
    ]
    return targets


# ---------------------------------------------------------------------------
# Step 25's sentence, the terminals with scopes, and the revision record.
# Declarations, written into the receipt so the prose can cite them.
# ---------------------------------------------------------------------------

BOUND_SCOPE = (
    "finite computation, bounded by N = 3 (reached at T = 2) and T = 3 "
    "(reached at N = 2); cells (2, 2), (2, 3), (3, 2) enumerated whole in "
    "both declared spaces; cell (3, 3) not enumerated under PREFLIGHT's "
    "per-cell assignment bound 2^20 (its declared assignment space has "
    "117440512 assignments); N = 4 and T = 4 refused by name"
)

STEP25_ANSWER: dict[str, object] = {
    "sentence": (
        "Within the declared vocabularies V0, V1, V2_ANON, V2_NAMED and their "
        "joins, and the declared finite space (cells (2, 2), (2, 3), (3, 2) "
        "enumerated whole in both spaces; cell (3, 3) not enumerated), "
        "witness-level structure becomes observable below function spaces "
        "exactly when TOKEN_EQ is admitted on top of TOKEN_DOMAIN (together, "
        "the admission named in step 21): the vocabularies expressible over "
        "TOKEN_DOMAIN without TOKEN_EQ, V0 and V1, leave {t0},{t0} versus "
        "{t0},{t1} unseparated in every enumerated space, the one question "
        "that separates that pair, share((0,1),(1,0)), uses TOKEN_EQ and "
        "nothing else, and TOKEN_EQ does not make all witness-level structure "
        "observable: V1 with V2_ANON still hides token renamings, count "
        "magnitudes, and, at T = 3 (cell (2, 3), the only T = 3 cell "
        "enumerated; 0 such pairs in every enumerated T = 2 space), the "
        "number of tokens two pairs share, while V2_NAMED hides nothing only "
        "because TOKEN_NAMES lets it address tokens by metatheoretic name, "
        "which also makes it separate renamings that are not witness-level "
        "structure"
    ),
    "when_half": (
        "computed: in every enumerated space there exist pairs identical "
        "under every V1 question and separated by a V2_ANON question "
        "(summary.<cell>/<space>.V1_equal_V2_ANON_different > 0); a finding "
        "of the enumeration; every enumerated space has T = 2 or T = 3, and "
        "T = 1 is not a declared cell, so nothing is said about it"
    ),
    "only_when_half": (
        "definitional within the declared vocabularies, not a finding: "
        "every V0 and V1 question reads only the count vector (presence is "
        "|S(p)| > 0, count_eq and count_lt compare |S(p)| and |S(q)|), and "
        "the count vector is invariant under token bijections by "
        "construction, so V0 and V1 could not separate an assignment from "
        "a token renaming of it; the computed invariance "
        "(invariant_under_token_bijections.V0, .V1 = true in every "
        "enumerated space) confirms this and could not have come out "
        "otherwise; the sentence says nothing about vocabularies that were "
        "not declared"
    ),
    "scope": BOUND_SCOPE,
}

LEAN_STAGE_MODULE = "S9Obligations.WitnessTypes"
# The Lean stage's theorems that the strings below cite by name.  Each must
# be listed, under LEAN_STAGE_MODULE, in verify_lean.AXIOM_REPORT_DECLARATIONS
# (test_terminal_strings_cite_only_audited_lean_theorems), so a cited name is
# an audited report and not a promise.
LEAN_STAGE_CITED: tuple[str, ...] = (
    "S9_3_sep_V1_indistinguishable",
    "S9_3_sep_V2_ANON_separates",
    "S9_3_sep_not_isomorphic",
    "S9_3_inv_V1_V2_ANON_indistinguishable",
    "S9_3_inv_not_isomorphic",
)

TERMINALS: list[dict[str, str]] = [
    {
        "terminal": "S9_3_ADMISSION_NAMED",
        "scope": (
            "the admission beyond A2 is TOKEN_DOMAIN plus TOKEN_EQ (a "
            "decidable equality on the token sort, admitted as a primitive), "
            "with TOKEN_NAMES a separately labelled further admission for "
            "V2_NAMED only; priced outside A1's bill and not contained in "
            "A3's bill, which it does not contain either -- the two bills "
            "are incomparable under inclusion of their listed items and no "
            "ranking between them is claimed; a declaration, not a theorem "
            "(step21_admission)"
        ),
    },
    {
        "terminal": "S9_3_WITNESS_OBSERVABLE",
        "scope": (
            BOUND_SCOPE + "; in every enumerated space there are pairs of "
            "witness assignments identical under every V1 question and "
            "separated by some V2_ANON question "
            "(summary.<cell>/<space>.V1_equal_V2_ANON_different), the first "
            "on the two-element irreflexive object being {t0},{t0} versus "
            "{t0},{t1}, separated by share((0,1),(1,0)), which uses TOKEN_EQ "
            "(on top of TOKEN_DOMAIN, the admission of step 21) and nothing "
            "else; no carrier-general claim; the Lean half for that pair is "
            + ", ".join(LEAN_STAGE_CITED[:3])
            + " in "
            + LEAN_STAGE_MODULE
            + " (each with a #print axioms report listed in verify_lean.py's "
            "AXIOM_REPORT_DECLARATIONS, a manual receipt read by no CI gate)"
        ),
    },
    {
        "terminal": "S9_3_WITNESS_INVISIBLE",
        "scope": (
            BOUND_SCOPE + "; in every enumerated space V1 with V2_ANON leaves "
            "invisible pairs unequal as raw data "
            "(summary.<cell>/<space>.invisible_in_V1_V2_ANON): token "
            "renamings, count magnitudes, and, at T = 3 (cell (2, 3), the "
            "only T = 3 cell enumerated; none in any enumerated T = 2 space), "
            "non-isomorphic families with equal count vectors, every one of "
            "which differs in how many tokens two pairs share "
            "(invisible.V1_V2_ANON.non_isomorphic_count_equal_pairs_by_"
            "differing_invariant.intersection_profile equals "
            "non_isomorphic_count_equal_pair_count in every enumerated "
            "space); under V2_NAMED no pair is invisible in any enumerated "
            "space, at the cost of separating every token renaming; no "
            "equality is claimed"
        ),
    },
    {
        "terminal": "PYTHON_ONLY_SCOPE_DECLARED",
        "scope": (
            "the exhaustiveness of this part's enumeration (the first-pair "
            "rule, every pair count, the split by invariant, the "
            "isomorphism-class counts) lives in Python only, "
            + BOUND_SCOPE
            + "; the Lean theorems of "
            + LEAN_STAGE_MODULE
            + " ("
            + ", ".join(LEAN_STAGE_CITED)
            + " and the list lemmas) concern the two computed pairs and the "
            "carrier-size-2 lists, and none of them reads the enumeration "
            "or its counts"
        ),
    },
    {
        "terminal": "REFUSED",
        "scope": (
            "N = 4 and T = 4 refused by name; cell (3, 3) refused under the "
            "per-cell assignment bound (bounds_reached.refused_by_name); the "
            "constructions family_isomorphism_as_question, "
            "witness_composition, presence_quotient_of_carrier, "
            "sharing_quotient_of_tokens refused by name in code and prose "
            "(step22_vocabularies.refused_constructions)"
        ),
    },
    {
        "terminal": "OB1_UNCHANGED",
        "scope": "this part makes no claim about OB-1; it is not closed, narrowed, or priced here",
    },
    {
        "terminal": "S66_UNCHANGED",
        "scope": "this part makes no claim about S6.6; it is not closed, narrowed, or priced here",
    },
    {
        "terminal": "S9_LAST_UNCHANGED",
        "scope": (
            "this part makes no claim about the inscription bridge (the S9 "
            "last bullet); it is not closed, narrowed, or priced here"
        ),
    },
]

REVISION: dict[str, object] = {
    "rounds_completed": 3,
    "round_3": {
        "occasion": (
            "repair after full-run audit 1 of the tree (recorded in "
            "STATUS.md): strings that described this part's own files and "
            "had lagged the Lean stage, and one ranking no declared order "
            "supported"
        ),
        "reworded": [
            {
                "keys": [
                    "step21_admission.TOKEN_EQ.price_vs_A3",
                    "terminals[0].scope (S9_3_ADMISSION_NAMED)",
                ],
                "was": "strictly less than A3's bill",
                "now": (
                    "not contained in A3's bill, which it does not contain "
                    "either; incomparable under inclusion of the listed "
                    "items, no ranking claimed"
                ),
                "why": (
                    "no order on metatheory bills is declared anywhere in "
                    "this tree, so 'strictly less' ranked what nothing ranks"
                ),
            },
            {
                "keys": ["terminals[1].scope (S9_3_WITNESS_OBSERVABLE)"],
                "was": "Lean statements proposed, not proved",
                "now": (
                    "the Lean half for that pair is named by theorem "
                    "(LEAN_STAGE_CITED, each in AXIOM_REPORT_DECLARATIONS)"
                ),
                "why": (
                    "the Lean stage ran after this part and proved the "
                    "proposed statements; the string described this part's "
                    "own files and lagged the tree"
                ),
            },
            {
                "keys": [
                    "terminals[3].scope (PYTHON_ONLY_SCOPE_DECLARED)",
                    "lean_stage_note",
                ],
                "was": "no Lean theorem of this part exists",
                "now": (
                    "the Lean theorems concern the two computed pairs and the "
                    "carrier-size-2 lists, and none reads the enumeration"
                ),
                "why": (
                    "the same lag; the terminal now says what the theorems "
                    "carry and what they do not, with the bound in the same "
                    "sentence"
                ),
            },
        ],
        "unchanged_by_the_repair": [
            "every pair count and every first_* value in every enumerated space",
            "the Lean targets",
            "the bound rule and the cells enumerated",
        ],
    },
    "round_2": {
        "reworded": [
            {
                "keys": [
                    "step25_answer.sentence",
                    "terminals[2].scope (S9_3_WITNESS_INVISIBLE)",
                ],
                "was": (
                    "the words 'from T = 3' followed by 'on', read as: at "
                    "every T from 3 up"
                ),
                "now": (
                    "at T = 3 (cell (2, 3), the only T = 3 cell enumerated; "
                    "none in any enumerated T = 2 space)"
                ),
                "why": (
                    "'on' read as T >= 3, past the bound reached; cell (3, 3) "
                    "and T = 4 are refused, so nothing is known beyond (2, 3)"
                ),
            },
            {
                "keys": ["step25_answer.sentence", "terminals[1].scope (S9_3_WITNESS_OBSERVABLE)"],
                "was": "exactly when TOKEN_EQ is admitted",
                "now": "exactly when TOKEN_EQ is admitted on top of TOKEN_DOMAIN",
                "why": (
                    "step 21's named admission is TOKEN_DOMAIN and TOKEN_EQ; "
                    "V0 and V1 already presuppose TOKEN_DOMAIN, so the "
                    "admission step 25 names must be the one step 21 names"
                ),
            },
            {
                "keys": ["step25_answer.when_half"],
                "was": "this depends on T >= 2",
                "now": "every enumerated space has T = 2 or T = 3; T = 1 is not a declared cell",
                "why": "T = 1 was never enumerated; the old phrase was a claim about it",
            },
            {
                "keys": ["step21_admission.why_sets[2]"],
                "was": "4^9 = 262144 maps in the full space",
                "now": "the witnessed space, 196608, is the number the per-cell rule reads",
                "why": (
                    "declared_bounds.cell_assignment_space reads the bound against "
                    "the witnessed space; one receipt declared two units"
                ),
            },
        ],
        "added_keys": [
            "cells.<cell>.spaces.<space>.invisible.<V>.non_isomorphic_count_equal_pairs_by_differing_invariant",
            "cells.<cell>.spaces.<space>.invisible.<V>.every_non_isomorphic_count_equal_pair_differs_in_intersection_profile",
        ],
        "why_added": (
            "the prose said every count-equal non-isomorphic invisible pair "
            "differs in how many tokens two pairs share, and no receipt key "
            "carried that aggregate; only the first such pair was characterized"
        ),
        "unchanged_by_the_repair": [
            "every pair count and every first_* value in every enumerated space",
            "the Lean targets",
            "the bound rule and the cells enumerated",
        ],
    },
    "round_1": {
    "withdrawn_values": [
        {
            "key": "cells.N2_T3.spaces.witnessed.invisible.V1_V2_ANON.first_non_isomorphic_count_equal_pair",
            "was": {"left_masks": [0, 3, 0, 3], "right_masks": [0, 3, 0, 5]},
            "why": (
                "not the least qualifying pair; the old code took the first "
                "bucket visited (see enumeration.first_pair_rule)"
            ),
        },
        {
            "key": "cells.N3_T3.spaces.witnessed_irreflexive.*",
            "was": "an enumeration of the (3, 3) witnessed_irreflexive sub-space, 229376 assignments",
            "why": (
                "cell (3, 3) is not enumerated under PREFLIGHT's per-cell "
                "rule (declared_bounds.withdrawn_application); its first "
                "count-equal non-isomorphic invisible pair as reported was "
                "also not the least"
            ),
        },
    ],
    "unchanged_by_the_repair": [
        "every pair count in every enumerated space",
        "the step-23 separating pair W1/W2 (N2_T2, witnessed_irreflexive)",
        "the step-24 pair W3/W4 (N2_T3, witnessed_irreflexive), where the reported pair was already the least",
        "every first_pair and first_non_isomorphic_pair value",
    ],
    },
}


# ---------------------------------------------------------------------------
# The receipt
# ---------------------------------------------------------------------------


def numbering_note() -> str:
    return (
        "S9.1, S9.2, S9.3 are the first, second, third bullets of section S9 "
        "of paper/primitive_difference.md in the order they appear; the "
        "numbering is the prompt's, not the paper's"
    )


def build_receipt() -> dict[str, object]:
    cells: dict[str, object] = {}
    for n, t in CELLS:
        cell = analyze_cell(n, t)
        cells[str(cell["cell"])] = cell

    reached: list[str] = []
    for key, cell_obj in cells.items():
        assert isinstance(cell_obj, dict)
        reached.append(f"{key}: {cell_obj['bound_reached']}")

    def space_of(cell: str, space: str) -> dict[str, object] | None:
        c = cells[cell]
        assert isinstance(c, dict)
        s = c["spaces"]
        assert isinstance(s, dict)
        w = s[space]
        assert isinstance(w, dict)
        if not w["enumerated"]:
            return None
        return w

    # The two Lean-target cells must be enumerated cells: the targets are
    # rendered from computed pairs, never hand-picked.
    for cell_key in ("N2_T2", "N2_T3"):
        if space_of(cell_key, "witnessed_irreflexive") is None:
            raise AssertionError(f"Lean targets need the enumerated cell {cell_key}")

    def count_of(block: dict[str, object], key: str) -> int:
        e = block[key]
        assert isinstance(e, dict)
        v = e["pair_count"]
        assert isinstance(v, int)
        return v

    def noniso_of(block: dict[str, object], key: str) -> int:
        e = block[key]
        assert isinstance(e, dict)
        v = e["non_isomorphic_pair_count"]
        assert isinstance(v, int)
        return v

    def noniso_count_equal_of(block: dict[str, object], key: str) -> int:
        e = block[key]
        assert isinstance(e, dict)
        v = e["non_isomorphic_count_equal_pair_count"]
        assert isinstance(v, int)
        return v

    summary: dict[str, object] = {}
    for cell_name in cells:
        for space in SPACES:
            w = space_of(cell_name, space)
            if w is None:
                summary[f"{cell_name}/{space}"] = {"enumerated": False}
                continue
            sep = w["separating"]
            inv = w["invisible"]
            assert isinstance(sep, dict) and isinstance(inv, dict)
            summary[f"{cell_name}/{space}"] = {
                "enumerated": True,
                "assignment_count": w["assignment_count"],
                "V1_equal_V2_ANON_different": count_of(sep, "V1_vs_V2_ANON"),
                "V1_equal_V2_NAMED_different": count_of(sep, "V1_vs_V2_NAMED"),
                "V2_ANON_equal_V1_different": count_of(sep, "V2_ANON_vs_V1"),
                "invisible_in_V2_ANON": count_of(inv, "V2_ANON"),
                "invisible_in_V2_NAMED": count_of(inv, "V2_NAMED"),
                "invisible_in_V1_V2_ANON": count_of(inv, "V1_V2_ANON"),
                "invisible_in_V1_V2_ANON_non_isomorphic": noniso_of(inv, "V1_V2_ANON"),
                "invisible_in_V1_V2_ANON_non_isomorphic_count_equal": noniso_count_equal_of(
                    inv, "V1_V2_ANON"
                ),
                "invisible_in_V1_V2_NAMED": count_of(inv, "V1_V2_NAMED"),
                "isomorphism_class_count": w["isomorphism_class_count"],
            }

    receipt: dict[str, object] = {
        **common.receipt_header(),
        "part": PART,
        "subject": "S9.3, proof-relevant witness types (PROMPT.md steps 21-26)",
        "authority_effect": "None",
        "numbering_note": numbering_note(),
        "declared_bounds": DECLARED_BOUNDS,
        "bounds_reached": {
            "carrier_reached": CARRIER_ATTEMPTED,
            "carrier_reached_at": [
                f"T = {t}" for n, t in CELLS if n == CARRIER_ATTEMPTED and cell_is_enumerated(n, t)
            ],
            "token_domain_reached": TOKENS_ATTEMPTED,
            "token_domain_reached_at": [
                f"N = {n}" for n, t in CELLS if t == TOKENS_ATTEMPTED and cell_is_enumerated(n, t)
            ],
            "cells_enumerated": [f"N{n}_T{t}" for n, t in CELLS if cell_is_enumerated(n, t)],
            "cells_not_enumerated": [f"N{n}_T{t}" for n, t in CELLS if not cell_is_enumerated(n, t)],
            "cells": reached,
            "refused_by_name": [
                f"N = {CARRIER_REFUSED}",
                f"T = {TOKENS_REFUSED}",
                *[
                    f"cell N{n}_T{t}: {declared_cell_assignment_count(n, t)} "
                    f"assignments in its declared assignment space (witnessed) "
                    f"over the per-cell bound {ASSIGNMENT_BOUND}; no space of "
                    f"the cell enumerated (witnessed_irreflexive would have "
                    f"{declared_assignment_count(n, t, 'witnessed_irreflexive')}, "
                    "inside the number and outside the rule)"
                    for n, t in CELLS
                    if not cell_is_enumerated(n, t)
                ],
            ],
        },
        "step21_admission": ADMISSION,
        "step22_vocabularies": {
            "designated_pair": list(DESIGNATED),
            "pair_order": "row-major (x, y) over the carrier",
            "questions": {
                "presence(p)": "is the store at p nonempty (V0)",
                "count_eq(p, q)": "|S(p)| = |S(q)| for p < q (V1)",
                "count_lt(p, q)": "|S(p)| < |S(q)| for p != q (V1)",
                "share(p, q)": "do S(p) and S(q) hold a common token, p < q (V2_ANON; TOKEN_EQ)",
                "token_at(t, p)": "does the named token t occur at p (V2_NAMED; TOKEN_EQ + TOKEN_NAMES)",
            },
            "vocabularies": {
                "V0": "presence",
                "V1": "presence + count_eq + count_lt",
                "V2_ANON": "presence + share",
                "V2_NAMED": "presence + token_at",
                "V1_V2_ANON": "presence + count_eq + count_lt + share",
                "V1_V2_NAMED": "presence + count_eq + count_lt + token_at",
            },
            "named_versus_anonymous": (
                "both computed and labelled separately; step 24's answer "
                "depends on the choice and the dependence is reported, not hidden"
            ),
            "sizes_by_cell": {
                f"N{n}_T{t}": {name: len(vocabulary(name, n, t)) for name in VOCABULARIES}
                for n, t in CELLS
            },
            "size_formulas": {
                "V0": "n^2",
                "V1": "n^2 + C(n^2, 2) + n^2 (n^2 - 1)",
                "V2_ANON": "n^2 + C(n^2, 2)",
                "V2_NAMED": "n^2 + t n^2",
                "V1_V2_ANON": "n^2 + C(n^2, 2) + n^2 (n^2 - 1) + C(n^2, 2)",
                "V1_V2_NAMED": "n^2 + C(n^2, 2) + n^2 (n^2 - 1) + t n^2",
            },
            "below_function_spaces_forbids": BELOW_FUNCTION_SPACES_FORBIDS,
            "refused_constructions": [
                {"construction": name, "needs": device, "why": why}
                for name, device, why in REFUSED_CONSTRUCTIONS
            ],
            "refusal_functions": [
                "refuse_map_as_datum",
                "refuse_composition",
                "refuse_quotient",
                "refuse",
            ],
            "metatheoretic_apparatus_not_in_any_vocabulary": [
                "family_isomorphic_metatheory",
                "least_transport",
                "intersection_profile",
                "token_degree_multiset",
                "common_token_count",
            ],
        },
        "enumeration": {
            "order": (
                "lexicographic on the tuple of per-pair token masks, pairs "
                "row-major, bit i of a mask = token ti present; first pair = "
                "lexicographically least (A, B) with A < B"
            ),
            "first_pair_rule": (
                "every key named first_* holds the lexicographically least "
                "(A, B) with A < B among the pairs the key describes, taken as "
                "the minimum over all groups holding such a pair, never the "
                "pair of the first group visited; checked by an independent "
                "scan in enumeration order (test "
                "test_every_first_pair_is_the_least_by_independent_scan) and "
                "by a full pair loop on the small spaces (test "
                "test_counts_and_first_pairs_by_full_pair_loop_on_small_spaces)"
            ),
            "bucketing_is_the_enumeration": (
                "every assignment of a space is generated and keyed by its "
                "answer vector under each vocabulary; pair counts are exact "
                "sums over buckets, not samples"
            ),
            "spaces": SPACE_DEFINITIONS,
        },
        "cells": cells,
        "summary": summary,
        "step25_answer": STEP25_ANSWER,
        "lean_targets": lean_targets(cells),
        "lean_stage_note": (
            "step 26's proofs belong to the Lean stage; this part proposes "
            "the statements (lean_targets) and proves nothing itself; the "
            "Lean stage ran after this part and carries them in "
            + LEAN_STAGE_MODULE
            + " ("
            + ", ".join(LEAN_STAGE_CITED)
            + "), whose #print axioms reports verify_lean.py audits by hand; "
            "what stays LEAN_NOT_CARRIED for S9.3 is the enumeration and its "
            "counts (the PYTHON_ONLY_SCOPE_DECLARED terminal) and the "
            "transcription of the carrier-size-2 vocabulary lists "
            "(lean_targets[3].residual); had no Lean stage run, "
            "LEAN_NOT_CARRIED would have been emitted by the synthesis pass "
            "with the obstacle 'no Lean stage ran', and S9.3 would have "
            "ended narrowed with the residual (the proofs) written, not "
            "discharged"
        ),
        "terminals": TERMINALS,
        "revision": REVISION,
    }
    return receipt


def write(out_dir: str) -> str:
    target = common.assert_inside_tree(out_dir) / "witness_types.json"
    common.write_receipt(target, build_receipt())
    return str(target.relative_to(common.REPO)).replace("\\", "/")
