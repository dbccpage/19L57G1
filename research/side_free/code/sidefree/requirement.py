"""The imposed requirement, its second reading, and the one shared verdict.

Classification (assumption discipline):

* ``REQUIREMENT`` and ``REQUIREMENT_SECOND_READING`` are an IMPOSED
  CHALLENGE.  They are inherited from the pinned receipt by one declared
  textual deletion each and by nothing else; gate ``G2`` asserts both
  deletions byte for byte against the vendored bytes, and also scans the two
  control strings for the words the deletion removes.
* ``RETAINED_MARKS`` is the pinned pair, inherited.
* ``separates`` is a DERIVED DEFINITION and is the ONE verdict function of
  this tree.  Both carriers define their own separability by calling it, and
  the replay against the pinned receipt calls it too, so a translation error
  cannot hide in a second implementation.

This module imports nothing.  It is the bottom of the tree so that every
carrier can call it without a cycle.
"""

from __future__ import annotations

from typing import Iterable, Sequence

# The pinned `requirement.declared` with the phrase " under a reading"
# deleted.  The pinned world indexes the requirement by its two readings; this
# world has one carrier and does not.  (The judged design called that phrase
# "four bytes"; it is sixteen.  The gate asserts the phrase, not a count.)
REQUIREMENT = (
    "the two retained marks are internally separable exactly "
    "when no permitted automorphism of the regime carries one of them to the "
    "other"
)

# The pinned `requirement.second_reading` with the phrase " of the reading"
# deleted, for the same reason.
REQUIREMENT_SECOND_READING = (
    "some property of a mark that forgets whatever the candidate's declared "
    "serialization forgets, and that is invariant under every permitted "
    "renaming, holds of one retained mark and not of the other"
)

# The exact phrases deleted from the pinned strings, carried here so the gate
# reconstructs the pinned text from the control text rather than the reverse.
DELETED_FROM_DECLARED = " under a reading"
DELETED_FROM_SECOND_READING = " of the reading"

# Words the deletion removes from the object language.  Neither control string
# may contain any of them as a whole word, and a test asserts it.
DELETED_WORDS: tuple[str, ...] = (
    "side",
    "sides",
    "boundary",
    "placement",
    "reflection",
    "near",
    "far",
)

RETAINED_MARKS: tuple[int, int] = (0, 1)


def separates(
    automorphism_permutations: Iterable[Sequence[int]], i: int, j: int
) -> bool:
    """The one verdict function: no permitted automorphism carries ``i`` to ``j``.

    Every separability judgment in this tree is this function applied to some
    automorphism set.  The two carriers hand it their own sets; the gate that
    replays the pinned receipt hands it the pinned world's own recorded sets.
    """
    return not any(pi[i] == j for pi in automorphism_permutations)
