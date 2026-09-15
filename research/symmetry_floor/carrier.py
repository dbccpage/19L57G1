"""The glyph carrier, its renamings, and what each inscription holds still.

An inscription is ``"<" region ("|" region)* ">"`` where a region is a possibly
empty run of data glyphs.  Two renamings are declared on it:

``relabel``
    exchange every ``a`` with every ``b``.  Presentation glyphs are forgettable,
    so this is not a new inscription.

``reflect``
    reverse the order of the regions and reverse each region.  On the flat run of
    tokens between the brackets this is exactly reversal.

They commute and each is its own inverse, so with the identity and their
composite there are four renamings.  Nothing below uses that structure, and the
proof in ``lean/SymmetryFloor.lean`` uses even less: four named maps suffice.

The **held set** of an inscription is which of the four leave it exactly as it
was.  It is the only quantity in this tree; everything else is read off it.
"""

from __future__ import annotations

import itertools
from typing import Iterator, Sequence

Region = tuple[str, ...]
Form = tuple[Region, ...]

DATA: tuple[str, ...] = ("a", "b")
RENAMINGS: tuple[str, ...] = ("id", "relabel", "reflect", "relabel.reflect")

_EXCHANGE = {"a": "b", "b": "a"}


def relabel(form: Form) -> Form:
    """Exchange every ``a`` with every ``b``."""
    return tuple(tuple(_EXCHANGE[s] for s in region) for region in form)


def reflect(form: Form) -> Form:
    """Reverse the region order, and reverse within each region."""
    return tuple(tuple(reversed(region)) for region in reversed(form))


def apply(name: str, form: Form) -> Form:
    """Apply one named renaming."""
    if name == "id":
        return form
    if name == "relabel":
        return relabel(form)
    if name == "reflect":
        return reflect(form)
    if name == "relabel.reflect":
        return relabel(reflect(form))
    raise ValueError("unknown renaming: " + name)


def held(form: Form) -> frozenset[str]:
    """Which renamings leave this inscription exactly as it was."""
    return frozenset(n for n in RENAMINGS if apply(n, form) == form)


def ways(form: Form) -> frozenset[Form]:
    """Every inscription the renamings carry this one to.

    These are one object.  Nothing admitted separates them, so the count is how
    many indistinguishable ways the object can be presented, and when a step
    produces it, how many ways it could have happened with no fact about which.
    """
    return frozenset(apply(n, form) for n in RENAMINGS)


def name_of(form: Form) -> Form:
    """One chosen presentation per object, so that objects can be counted."""
    return min(ways(form))


def render(form: Form) -> str:
    return "<" + "|".join("".join(region) for region in form) + ">"


def parse(text: str) -> Form:
    if not (text.startswith("<") and text.endswith(">")):
        raise ValueError("not an inscription: " + text)
    body = text[1:-1]
    for glyph in body:
        if glyph not in DATA and glyph != "|":
            raise ValueError("glyph outside the carrier: " + glyph)
    return tuple(tuple(part) for part in body.split("|"))


def data_count(form: Form) -> int:
    """How many data glyphs the inscription holds."""
    return sum(len(region) for region in form)


def divider_count(form: Form) -> int:
    return len(form) - 1


def size(form: Form) -> int:
    """Total glyphs, data plus dividers.  One step raises this by exactly one."""
    return data_count(form) + divider_count(form)


def _splits(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in _splits(total - first, parts - 1):
            yield (first,) + rest


def with_shape(dividers: int, data: int) -> Iterator[Form]:
    """Every inscription with exactly this many dividers and data glyphs."""
    for split in _splits(data, dividers + 1):
        pools = [list(itertools.product(DATA, repeat=k)) for k in split]
        for regions in itertools.product(*pools):
            yield tuple(regions)


def generation(k: int) -> list[Form]:
    """Every inscription of exactly ``k`` glyphs.

    Every inscription of size ``k`` is reached from one of size ``k - 1`` by one
    glyph appearing, so this is the whole of what the step relation can have
    produced by step ``k``.  Nothing here is sampled and no search is cut short.
    """
    out: list[Form] = []
    for dividers in range(k + 1):
        out.extend(with_shape(dividers, k - dividers))
    return sorted(out)


def objects(k: int) -> list[Form]:
    """One chosen presentation per object at generation ``k``, sorted."""
    return sorted({name_of(form) for form in generation(k)})


def still_everywhere(forms: Sequence[Form]) -> list[Form]:
    """Those inscriptions every renaming leaves exactly as they were."""
    return [form for form in forms if len(held(form)) == len(RENAMINGS)]
