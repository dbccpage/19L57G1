"""Independent finite model of B2(i)-(iii).  AuthorityEffect: None.

Nothing here is imported from the Lean library, from model.py or from
another tree.  Outcomes are bits (0 for +1, 1 for -1); a context's product
is -1 exactly when the sum of its bits is odd.  By exhaustive search:

* the 3 x 3 parity square (rows even, columns even, even, odd) has no
  global assignment among all 2**9 bit assignments;
* dropping any one of its six contexts leaves exactly 2**4 assignments;
* on the 3 x 3 grid every one of the 2**6 parity targets has a global
  assignment exactly when its six targets sum to an even number;
* on every grid with 2 to GRID_MAX rows and columns and every target, the
  same holds, and an odd target becomes satisfiable when any one context
  is dropped;
* a context-indexed table (each context with its own bits) meets the
  square, and every such table breaks a shared entry.

A passing check is a finite receipt on these bounds, not a proof.
"""
from __future__ import annotations

from itertools import product

GRID_MAX = 3

Context = tuple[tuple[int, int], ...]


def grid_contexts(rows: int, cols: int) -> list[Context]:
    """Rows first, then columns; an entry is (row, column)."""
    by_row = [tuple((r, c) for c in range(cols)) for r in range(rows)]
    by_col = [tuple((r, c) for r in range(rows)) for c in range(cols)]
    return by_row + by_col


SQUARE_TARGET = (0, 0, 0, 0, 0, 1)


def meets(assignment: dict[tuple[int, int], int], contexts: list[Context],
          target: tuple[int, ...], skip: int | None = None) -> bool:
    return all(sum(assignment[e] for e in ctx) % 2 == target[k]
               for k, ctx in enumerate(contexts) if k != skip)


def global_count(rows: int, cols: int, target: tuple[int, ...], skip: int | None = None) -> int:
    contexts = grid_contexts(rows, cols)
    entries = [(r, c) for r in range(rows) for c in range(cols)]
    count = 0
    for bits in product((0, 1), repeat=len(entries)):
        if meets(dict(zip(entries, bits)), contexts, target, skip):
            count += 1
    return count


def grid_failures(max_side: int) -> list[str]:
    """Every grid and target where the even-sum criterion or minimality fails."""
    failures: list[str] = []
    for rows in range(2, max_side + 1):
        for cols in range(2, max_side + 1):
            n_ctx = rows + cols
            for target in product((0, 1), repeat=n_ctx):
                exists = global_count(rows, cols, target) > 0
                if exists != (sum(target) % 2 == 0):
                    failures.append(f"criterion {rows}x{cols} {target}")
                if not exists:
                    for k in range(n_ctx):
                        if global_count(rows, cols, target, skip=k) == 0:
                            failures.append(f"minimality {rows}x{cols} {target} drop {k}")
    return failures


def context_indexed_witness() -> list[tuple[int, ...]]:
    """One bit triple per context of the square: all 0 but the first entry
    of the last column."""
    zero: tuple[int, ...] = (0, 0, 0)
    first: tuple[int, ...] = (1, 0, 0)
    return [zero] * 5 + [first]


def context_indexed_meets(table: list[tuple[int, ...]]) -> bool:
    return all(sum(bits) % 2 == SQUARE_TARGET[k] for k, bits in enumerate(table))


def broken_entries(table: list[tuple[int, ...]]) -> list[tuple[int, int]]:
    """Entries whose row copy and column copy differ."""
    contexts = grid_contexts(3, 3)
    copies: dict[tuple[int, int], list[int]] = {}
    for ctx, bits in zip(contexts, table):
        for entry, bit in zip(ctx, bits):
            copies.setdefault(entry, []).append(bit)
    return sorted(e for e, values in copies.items() if len(set(values)) > 1)


def every_meeting_table_breaks() -> bool:
    """All 2**18 context-indexed bit tables that meet the square break some entry."""
    for flat in product((0, 1), repeat=18):
        table = [tuple(flat[3 * k:3 * k + 3]) for k in range(6)]
        if context_indexed_meets(table) and not broken_entries(table):
            return False
    return True
