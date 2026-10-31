# Unit 61: Compressing a presentation against a question list

**Claim.** On a supplied finite domain, compression may merge data only when they agree on the declared questions. A first-match representative preserves exactly those answer signatures.

**Status:** Admitted definitions; derived theorems under their stated
hypotheses; finite examples and refuted general uniqueness claims are
distinguished below. **Lean:** `Derivation.Compression`.

Use the [Map lab](../map_lab/README.md) for the worked pictures and the
[reading guide](../reading_formal_statements.md) for one formula at a time.

## First pass

A **presentation** assigns a stored label to each input. A **fiber** is
the group of inputs sharing one label. Supply this three-item example:

| Input | Kept question's answer | Stored representative |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 0 | 0 |
| 2 | 1 | 2 |

The recorder groups inputs 0 and 1 because their kept answers agree.
Input 2 stays separate. From stored label 0 we can return answer 0;
from label 2 we can return answer 1. The kept answer is recoverable.

If a different requested question gives inputs 0 and 1 different answers,
it is not recoverable from these labels. A lookup receives the same
stored input 0 in both cases and cannot assign it two different outputs.

An **adequate** presentation preserves the questions we declared. Keeping
all three inputs separate would also be adequate; it would keep more
distinctions than this example needs. The first-match rule below chooses
representatives using the supplied order of the domain list.

**Predict.** If the domain order changes from `[0, 1, 2]` to `[1, 0, 2]`,
with the same kept answers, must the stored labels stay the same?

<details>
<summary>Check your prediction</summary>

No. In the second order, input 1 is the first member of the shared
answer class, so both 0 and 1 receive label 1 instead of label 0.
The grouping and recoverability are preserved; these representative
labels depend on the supplied order. `first_match_order_changes_labels`
checks the example with the question that returns 1 exactly at input 2.

</details>

<details>
<summary>Formal source record and theorem summary</summary>

| field | value |
|---|---|
| **Mark** | `FROZEN` for `sigEq_iff_sigList`, `factors_iff_fiberConstant`, `factor_unique_on_image`, `pQ_exact`, `pQ_adequate`, `pQ_unique_on_image`, `enlarge_refines`, `splits_iff_new_separator`, `absolute_adequacy_iff_injective`, `dup_no_refine`, `postcompose_no_refine`, `refine_bounded`, and the 16 list/counting helper lemmas; `CONDITIONAL` for `pQ_coarsest` (on `Adequate D Q p`), `descent_witness` (on `p x = p x'` and `¬ SigEq Q x x'`), `refine_requires_separator` (on `SplitsAt D Q Q' x`), `classCount_pos`, `chain_bounded`, and `strict_steps_lt` (on `D ≠ []`), and `strict_split_increases` (on `Q ⊆ Q'`, `x ∈ D`, `SplitsAt D Q Q' x`); `REFUTED` for off-image factoring uniqueness (`factor_not_unique_off_image`), refinement uniqueness (`refinement_not_unique`), and minimum-length refinement uniqueness (`refinement_tie`). |
| **Role** | Target-relative presentation compression (`lean4/Derivation/Compression.lean`, `code/derivation/compression.py`), imported downstream by `ObsDescent`, `ContactKernel`, `ClosureSymmetry`, `PresentationRelativity`, and `ResidualClosure`. |
| **AuthorityEffect** | `None`. Neither `PrimitiveCore.Step` nor `DiffObs` appears in `Compression.lean`; the connection between presentations `p : Nat → Nat` and observer projections is established later in `ObsDescent` (Unit 67). |
| **Source** | `lean4/Derivation/Compression.lean` (787 lines; 14 definitions, 38 theorems, 22 in `artifacts/lean_axioms.txt`); `code/derivation/compression.py` (509 lines); `code/run_compression.py` (117 lines); `artifacts/compression.json`; `textbook/audit/modules/Compression.md`. |
| **Axioms** | 12 of the 22 artifact theorems use no axioms (`sigEq_iff_sigList`, `factor_unique_on_image`, `factor_not_unique_off_image`, `pQ_unique_on_image`, `descent_witness`, `enlarge_refines`, `splits_iff_new_separator`, `absolute_adequacy_iff_injective`, `refine_requires_separator`, `refinement_not_unique`, `refinement_tie`, `classCount_pos`; separately, all 4 book theorems in `Textbook.U61` use no axioms); 4 use `[Quot.sound]` (`factors_iff_fiberConstant`, `pQ_exact`, `pQ_adequate`, `pQ_coarsest`); 2 use `[propext]` (`dup_no_refine`, `postcompose_no_refine`); 4 use `[propext, Quot.sound]` (`refine_bounded`, `strict_split_increases`, `chain_bounded`, `strict_steps_lt`). |


## Detailed claim and formal anchors

Over a represented finite domain `D : List Nat` and a declared question family `Q : List (Nat → Nat)`, a question `q` factors through a presentation `p : Nat → Nat` on `D` if and only if the fibers of `p` over `D` are `q`-constant (`factors_iff_fiberConstant`), with the factoring map unique on the `p`-image of `D` (`factor_unique_on_image`) and not unique off it (`factor_not_unique_off_image`).

The first-match signature quotient `pQ D Q` has fibers on `D` equal to the `Q`-signature classes (`pQ_exact`), is `Q`-adequate (`pQ_adequate`), and factors through every `Q`-adequate presentation on `D` (`pQ_coarsest`).

Every adequacy failure on `D` is witnessed by an explicit question in `Q` (`descent_witness`).

A class splits under a new family `Q'` if and only if `Q'` contains a separator across an old `Q`-agreement (`splits_iff_new_separator`), which cannot be a function of the old signature (`refine_requires_separator`), whereas duplicating `Q` (`dup_no_refine`) or appending a function of `sigList Q` (`postcompose_no_refine`) refines nothing.

Adequacy for all families `Q` is equivalent to injectivity on `D` (`absolute_adequacy_iff_injective`).

Splitting enlargements are neither unique (`refinement_not_unique`) nor unique among equal-length families (`refinement_tie`), and every strict split under a subfamily enlargement strictly increases `classCount D Q ≤ D.length` (`strict_split_increases`, `refine_bounded`), bounding any strict refinement chain on a nonempty domain `D` to fewer than `D.length` steps (`strict_steps_lt`).

</details>

## Question

Suppose we have a finite list of natural-number labels $D = [d_0, d_1, \dots, d_{n-1}]$ and a finite list of numerical questions $Q = [q_0, q_1, \dots, q_{k-1}]$ that we plan to ask about items in $D$. A **presentation** is a map $p : \mathbb{N} \to \mathbb{N}$ that assigns a label $p(x)$ to each item $x \in D$, potentially merging distinct items $x \neq x'$ onto the same label $p(x) = p(x')$.

1. When is merging two items $x, x' \in D$ harmless relative to $Q$, and when does a question $q$ factor through $p$ on $D$ as $q(x) = g(p(x))$?
2. Is there a coarsest presentation selected by the declared list order $p_Q$ on $D$ that preserves all answers in $Q$ without invoking a choice principle, and what happens if we ask for a presentation that is adequate for *every* possible question list at once?
3. When we enlarge the question list from $Q$ to $Q'$, what must $Q'$ contain to split a merged class, is there a unique one-question refinement, and how many times can classes strictly split on a finite domain $D$?

---

## What we already possess

From standard list arithmetic in Lean 4 (and `Derivation.PrimitiveCore`, which `Compression.lean` imports at line 1 only for build-order placement without referencing any `PrimitiveCore` symbol):

- A represented finite domain is given explicitly as a list `D : List Nat`, where membership `x ∈ D` defines the domain of interest.
  The list order selects first representatives. Repeated entries are allowed by the native type; list length counts entries, while membership specifies which inputs are under consideration.
- Questions and presentations are functions `Nat → Nat`, and a declared question family is an explicit list `Q : List (Nat → Nat)`.
- Equality on `Nat` and on `List Nat` is decidable (`DecidableEq Nat`, `DecidableEq (List Nat)`), allowing boolean tests `decide (p z = y)` and `decide (sigList Q z = sigList Q x)` inside list recursion without invoking classical choice.

---

## New concept

### 1. Answer signatures, adequacy, fiber-constancy, and factorization (Lines 64–196)

#### Answer signatures

For an input `x`, `sigList Q x` lists the answers to Q's questions in
their declared order. It is an answer pattern. `SigEq Q x x'` means the
two inputs agree on every question in Q. The theorem `sigEq_iff_sigList`
shows this is equivalent to equality of their full answer lists.

#### Adequacy for the declared questions

`Adequate D Q p` says that whenever p merges two inputs in D, those inputs
agree on Q. It is a condition to check for the supplied D, Q, and p.
It allows p to keep additional distinctions; it does not require every
pair with the same answers to be merged.

#### One requested question

`FiberConstant D p q` says q has the same value on all members of each
p-fiber within D. Different fibers may have different q values.

`FactorsOn D p q` says there is a lookup g with `g(p(x)) = q(x)` for
every x in D. The same g must work for the whole declared domain. This
is the equation worked out in the [reading guide](../reading_formal_statements.md).

The theorem `factors_iff_fiberConstant` proves these last two conditions
equivalent. One direction checks that equal lookup inputs give equal
outputs. The other constructs a lookup from each fiber's common answer.

#### Constructing the lookup

To construct a factoring map `g` from `FiberConstant D p q` without any axiom of choice, `Compression.lean` defines first-match selection `pick (D : List Nat) (P : Nat → Bool) : Option Nat`, which returns the first entry `a` of `D` with `P a = true` (or `none` if none exists). Setting
$$g(y) = q\bigl((\mathrm{pick}\;D\;(\lambda z \Rightarrow \mathrm{decide}(p(z) = y))).\mathrm{getD}\;0\bigr)$$
evaluates `q` at the first point `r ∈ D` in the fiber $p^{-1}(y) \cap D$. By `FiberConstant D p q`, $q(r) = q(x)$ for every $x \in D$ with $p(x) = y$, proving `factors_iff_fiberConstant`.

Any two factoring maps `g, g'` for `q` through `p` on `D` satisfy $g(p(x)) = q(x) = g'(p(x))$ for all $x \in D$ (`factor_unique_on_image`). Outside the image $p(D)$, however, the factoring equations impose no constraint: on $D = [0]$ with $p = q = \mathrm{id}$, the maps $g = \mathrm{id}$ and $g'(n) = (\text{if } n = 5 \text{ then } 6 \text{ else } n)$ both factor $q$ through $p$ on $D$ yet disagree at $5 \notin p(D)$ (`factor_not_unique_off_image`).

### 2. The signature quotient `pQ` and witnessed descent failure (Lines 215–334)

Using `pick`, the **signature quotient presentation** `pQ D Q : Nat → Nat` sends each `x` to the first element of `D` carrying the same `Q`-signature as `x` (defaulting to `0` if none exists):
$$p_Q(x) = \bigl(\mathrm{pick}\;D\;(\lambda z \Rightarrow \mathrm{decide}(\mathrm{sigList}(Q, z) = \mathrm{sigList}(Q, x)))\bigr).\mathrm{getD}\;0.$$
On `D`, `pQ D Q` satisfies four properties:

1. **Representative specification (`pQ_spec`):** For $x \in D$, $p_Q(x) \in D$ and $\mathrm{sigList}(Q, p_Q(x)) = \mathrm{sigList}(Q, x)$.
2. **Exactness (`pQ_exact`):** For $x, x' \in D$, $p_Q(x) = p_Q(x') \iff \mathrm{SigEq}(Q, x, x')$.
3. **Adequacy (`pQ_adequate`):** `Adequate D Q (pQ D Q)`.
4. **Coarsest factorization (`pQ_coarsest` and `pQ_unique_on_image`):** For every presentation `p` satisfying `Adequate D Q p`, `FactorsOn D p (pQ D Q)` holds, and any two maps factoring `pQ D Q` through `p` on `D` agree on $p(D)$.

**Scope note on "coarsest" and idle hypothesis `_hp`:** As audited in `textbook/audit/modules/Compression.md` (§4 and §11.3), `pQ_coarsest` proves that `pQ D Q` factors through every `Q`-adequate presentation `p` on `D`, and the docstring explicitly notes that this is the only sense of "coarsest" claimed (no image-isomorphism uniqueness theorem between arbitrary coarsest adequate presentations is stated). Moreover, `pQ_unique_on_image` carries the hypothesis `(_hp : Adequate D Q p)` with a leading underscore: its proof is a direct specialization of `factor_unique_on_image D p (pQ D Q) g g' hg hg'` and never uses `_hp`.

When a presentation `p` is *not* `Q`-adequate on `D`—merging $x, x' \in D$ ($p(x) = p(x')$) while $\neg\,\mathrm{SigEq}(Q, x, x')$—list recursion over `Q` via `sigEq_decompose` finds the first question $q \in Q$ with $q(x) \neq q(x')$, which immediately refutes `FiberConstant D p q` (`descent_witness`).

### 3. Enlargement, no absolute adequacy, and non-signature-determined splits (Lines 337–443)

When a question family `Q` is replaced by `Q'`:

- If $Q \subseteq Q'$ (`∀ q, q ∈ Q → q ∈ Q'`), then agreement on `Q'` implies agreement on `Q` (`enlarge_refines`).
- The `Q`-class of $x$ **splits under `Q'`** (`SplitsAt D Q Q' x`) when $\exists x' \in D,\; \mathrm{SigEq}(Q, x, x') \land \neg\,\mathrm{SigEq}(Q', x, x')$.
- Theorem `splits_iff_new_separator` proves that `SplitsAt D Q Q' x` holds if and only if there exist $x' \in D$ and $q' \in Q'$ with $\mathrm{SigEq}(Q, x, x')$ and $q'(x) \neq q'(x')$. Notice that `splits_iff_new_separator` also carries an unused hypothesis `(_hsub : ∀ q, q ∈ Q → q ∈ Q')`; in `Textbook.U61.splits_iff_without_sub` we verify the identical equivalence without `_hsub`.
- **No absolute adequacy (`absolute_adequacy_iff_injective`):** A presentation `p` is adequate for *all* question lists `Q : List (Nat → Nat)` if and only if `p` is injective on `D` ($\forall x, x' \in D,\; p(x) = p(x') \implies x = x'$). The forward direction tests `p` against the one-question indicator list `[fun z => if z = x then 1 else 0]`. Thus any presentation that merges at least two points of `D` is adequate only relative to a specific family of questions that agree on those merged points.
- **Repetition and signature digests (`dup_no_refine`, `postcompose_no_refine`, `refine_requires_separator`):** Repeating `Q` (`Q ++ Q`) or appending a function $z \mapsto f(\mathrm{sigList}(Q, z))$ of the existing signature list leaves `SigEq` unchanged. Consequently, if `SplitsAt D Q Q' x` holds, then `Q'` must contain some question $q' \in Q'$ that is not signature-determined (`¬ ∃ f : List Nat → Nat, ∀ z, q' z = f (sigList Q z)`).

**Interpretation audit on "replay", "evidential", and "equal-cost" (`textbook/audit/modules/Compression.md` §11.1, §11.4):** The docstrings of `postcompose_no_refine` and `refine_requires_separator` gloss `f (sigList Q z)` as "a hash or a replay record" and state that "replay is evidential only when it carries a new represented separator." In `Compression.lean`, the terms *replay*, *evidential*, *hash*, and *record* have no formal definitions; the proved mathematical statement is strictly that a function of the old signature `f ∘ sigList Q` preserves `SigEq Q`, so any split requires a question not of the form `f ∘ sigList Q`. Similarly, `refinement_tie` describes `Q1.length = Q2.length` as "equal-cost", where `List.length` is an admitted count of questions in the list rather than a derived cost functional.

### 4. Non-unique refinement and the class-count chain bound (Lines 446–786)

On $D = [0, 1, 2]$ starting from the empty family $Q = []$, the two one-question enlargements $Q_1 = [\mathrm{ind}\;0]$ and $Q_2 = [\mathrm{ind}\;1]$ (where $\mathrm{ind}\;a\;(z) = 1$ if $z = a$ else $0$) both split the class of $0$, both have length $1$, and induce distinct partitions of $D$: $Q_1$ merges $\{1, 2\}$ into `[0], [1, 2]` while $Q_2$ separates $1$ from $2$ into `[0, 2], [1]` (`refinement_not_unique`, `refinement_tie`).

To bound the length of any sequence of strict splits on a finite domain $D$, `Compression.lean` defines:

- `memB s l : Bool` and `dedupL : List (List Nat) → List (List Nat)` (deduplicating a list of signatures by keeping the last occurrence of each distinct signature), and
- `classCount D Q : Nat := (dedupL (D.map (sigList Q))).length`, the number of distinct `Q`-signatures realized on `D`.

Two list-induction lemmas (`count_le_of_determines` and `count_lt_of_split`) show that whenever a fine label $F(a)$ determines a coarse label $G(a)$ on $D$, the number of distinct $G$-values on $D$ is at most the number of distinct $F$-values (`count_le_of_determines`), and is strictly smaller whenever some pair $x, y \in D$ shares its $G$-value ($G(x) = G(y)$) while differing in $F$ ($F(x) \neq F(y)$) (`count_lt_of_split`). Applying this to $F = \mathrm{sigList}\;Q'$ and $G = \mathrm{sigList}\;Q$ when $Q \subseteq Q'$ yields:

- $1 \le \mathrm{classCount}(D, Q) \le |D|$ for every nonempty $D$ (`classCount_pos`, `refine_bounded`),
- $\mathrm{classCount}(D, Q) < \mathrm{classCount}(D, Q')$ whenever $Q \subseteq Q'$, $x \in D$, and $\mathrm{SplitsAt}(D, Q, Q', x)$ (`strict_split_increases`), and
- for any `StrictChain D (Q :: t)` of consecutive subfamily splits on a nonempty $D$, $\mathrm{classCount}(D, Q) + |t| \le |D|$ (`chain_count`), so the total number of families in the chain is at most $|D|$ (`chain_bounded`) and the number of strict split steps $|t|$ is strictly less than $|D|$ (`strict_steps_lt`).

Unlike `splits_iff_new_separator`, the subfamily hypothesis `hsub : ∀ q, q ∈ Q → q ∈ Q'` in `strict_split_increases` is load-bearing: in `Textbook.U61.non_sub_split_preserves_count` we show that on $D = [0, 1, 2]$, switching from $Q = [\mathrm{ind}\;0]$ to $Q' = [\mathrm{ind}\;1]$ (where $Q \not\subseteq Q'$) splits $x = 1$ (since $1$ and $2$ agree on $\mathrm{ind}\;0$ and disagree on $\mathrm{ind}\;1$) while merging $0$ and $2$, leaving $\mathrm{classCount}$ unchanged at $2$.

---

## Plain-language interpretation

Think of $D$ as a table of rows and $Q$ as the columns we have chosen to inspect. A presentation $p$ assigns a group ID $p(x)$ to each row $x \in D$.

- **Factorization (`factors_iff_fiberConstant`):** We can compute a column $q(x)$ purely from the group ID $p(x)$ if and only if no two rows with the same group ID have different values in column $q$. The lookup table $g$ from group IDs to answers is completely fixed on the group IDs that actually appear in $D$ (`factor_unique_on_image`), and completely arbitrary on group IDs that never appear in $D$ (`factor_not_unique_off_image`).
- **Signature quotient (`pQ`):** If we label every row $x \in D$ by the first row in $D$ that has the exact same tuple of answers across all columns of $Q$, we get the coarsest grouping on $D$ that loses no information about $Q$ (`pQ_exact`, `pQ_adequate`, `pQ_coarsest`).
- **Relative vs. absolute adequacy (`absolute_adequacy_iff_injective`):** If someone demands a grouping $p$ that preserves the answers to *every conceivable column* without declaring which columns matter, the only safe grouping is to never merge any two distinct rows of $D$ ($p$ must be injective on $D$). Compression is only possible relative to a declared list of questions.
- **Adding derived columns vs. new separators (`postcompose_no_refine`, `refine_requires_separator`):** Adding a column that is computed purely as a formula of existing columns (or duplicating existing columns) never splits any group. To split an existing group, a new column must disagree on two rows that had identical tuples under the old columns.
- **Refinement choices and finite depth (`refinement_not_unique`, `strict_steps_lt`):** Starting from a single unsplit group on $D = [0, 1, 2]$, asking "is the row equal to $0$?" gives groups $\{0\}, \{1, 2\}$, whereas asking "is the row equal to $1$?" gives groups $\{0, 2\}, \{1\}$. Both use a single question and split the initial group, so there is no canonical "next question." However, whenever we *keep* all old questions ($Q \subseteq Q'$) and add a question that splits at least one group, the number of groups increases by at least $1$ and can never exceed $|D|$, so at most $|D| - 1$ strict split steps can occur along any enlarging chain.

---

## Pseudocode

```text
function SIG_LIST(Q, x):
    return [q(x) for q in Q]

function PICK(D, pred):
    for a in D:
        if pred(a):
            return Some(a)
    return None

function P_QUOTIENT(D, Q, x):
    match PICK(D, z -> SIG_LIST(Q, z) == SIG_LIST(Q, x)):
        case Some(r): return r
        case None:    return 0

function FACTOR_MAP(D, p, q, y):
    match PICK(D, z -> p(z) == y):
        case Some(r): return q(r)
        case None:    return q(0)

function DESCENT_WITNESS(Q, x, x_prime):
    # Precondition: p(x) == p(x_prime) and SIG_LIST(Q, x) != SIG_LIST(Q, x_prime)
    for q in Q:
        if q(x) != q(x_prime):
            return q   # witnesses q(x) != q(x_prime) and not FiberConstant(D, p, q)

function CLASS_COUNT(D, Q):
    # Number of distinct answer signatures realized on D
    return length(DEDUP_LAST([SIG_LIST(Q, x) for x in D]))
```

---

## Python

From `code/derivation/compression.py` (with `D = list(range(n))` and functions on `D` represented as tuples `Fn = tuple[int, ...]`) and `textbook/checks/u61_compression.py`:

```python
from itertools import product

Fn = tuple[int, ...]
Family = tuple[Fn, ...]


def sig_list(Q: Family, x: int) -> Fn:
    """The answer signature of x under Q, in family order."""
    return tuple(q[x] for q in Q)


def sig_eq(Q: Family, x: int, xp: int) -> bool:
    """Agreement of x and xp on every question of Q."""
    return all(q[x] == q[xp] for q in Q)


def adequate(D: list[int], Q: Family, p: Fn) -> bool:
    """Points of D merged by p agree on every question."""
    return all(
        sig_eq(Q, x, xp)
        for x in D for xp in D if p[x] == p[xp])


def fiber_constant(D: list[int], p: Fn, q: Fn) -> bool:
    """The fibers of p over D are q-constant."""
    return all(
        q[x] == q[xp]
        for x in D for xp in D if p[x] == p[xp])


def valid_factor_maps(
    D: list[int], p: Fn, q: Fn, m: int
) -> list[dict[int, int]]:
    """All maps on the p-image of D (into range(m)) factoring q through p."""
    image = sorted({p[x] for x in D})
    out: list[dict[int, int]] = []
    for values in product(range(m), repeat=len(image)):
        g = dict(zip(image, values))
        if all(g[p[x]] == q[x] for x in D):
            out.append(g)
    return out


def first_with_sig(D: list[int], Q: Family, s: Fn) -> int:
    """First element of D with signature s (0 if none, mirroring getD 0)."""
    for d in D:
        if sig_list(Q, d) == s:
            return d
    return 0


def p_quotient(D: list[int], Q: Family) -> Fn:
    """The signature quotient presentation on D."""
    return tuple(first_with_sig(D, Q, sig_list(Q, x)) for x in D)


def splits_at(D: list[int], Q: Family, Qp: Family, x: int) -> bool:
    """The class of x splits under the enlargement Qp."""
    return any(
        sig_eq(Q, x, xp) and not sig_eq(Qp, x, xp) for xp in D)


def sig_determined(D: list[int], Q: Family, q: Fn) -> bool:
    """q is a function of the Q-signature on D."""
    return all(
        q[x] == q[xp]
        for x in D for xp in D
        if sig_list(Q, x) == sig_list(Q, xp))


def class_count(D: list[int], Q: Family) -> int:
    """The number of distinct signatures on D."""
    return len({sig_list(Q, x) for x in D})
```

---

## Line-by-line Python explanation

- **`Fn = tuple[int, ...]` and `Family = tuple[Fn, ...]`:** In `code/derivation/compression.py`, a function on `D = list(range(n))` into `range(m)` is represented by its value tuple `(f(0), ..., f(n - 1))`, and a question family is an ordered tuple of such functions.
- **`sig_list(Q, x)` and `sig_eq(Q, x, xp)`:** Mirror `Compression.sigList` and `Compression.SigEq`. `sig_iff_exhaustive(3, 3, 2)` verifies `sig_eq(Q, x, xp) == (sig_list(Q, x) == sig_list(Q, xp))` across all $n \in \{1, 2, 3\}$, $m \in \{1, 2, 3\}$, and families of size $\le 2$.
- **`adequate(D, Q, p)` and `fiber_constant(D, p, q)`:** Mirror `Compression.Adequate` and `Compression.FiberConstant` by universally quantifying over all pairs `x, xp in D` with `p[x] == p[xp]`.
- **`valid_factor_maps(D, p, q, m)`:** Collects the sorted image `image = sorted({p[x] for x in D})` and searches all maps `g : image -> range(m)` satisfying `g[p[x]] == q[x]` for all `x in D`. When `fiber_constant(D, p, q)` holds, `len(valid_factor_maps(D, p, q, m)) == 1` (confirming `factor_unique_on_image`); when it fails, the list is empty (confirming `factors_iff_fiberConstant`).
- **`first_with_sig(D, Q, s)` and `p_quotient(D, Q)`:** Mirror `Compression.pick` and `Compression.pQ D Q`. For each `x in D`, `first_with_sig` scans `D` in list order and returns the first `d in D` whose signature matches `sig_list(Q, x)`.
- **`splits_at(D, Q, Qp, x)` and `sig_determined(D, Q, q)`:** Mirror `Compression.SplitsAt` and the negand `∃ f, ∀ z, q' z = f (sigList Q z)` of `Compression.refine_requires_separator` restricted to `D`.
- **`class_count(D, Q)`:** Computes the number of distinct signature tuples `{sig_list(Q, x) for x in D}` realized on `D`, matching `Compression.classCount D Q`.

---

## Lean 4

From `lean4/Derivation/Compression.lean` and `textbook/checks/u61_lean.py`:

```lean
namespace Compression

def sigList (Q : List (Nat → Nat)) (x : Nat) : List Nat :=
  Q.map (fun q => q x)

def SigEq (Q : List (Nat → Nat)) (x x' : Nat) : Prop :=
  ∀ q, q ∈ Q → q x = q x'

def Adequate (D : List Nat) (Q : List (Nat → Nat))
    (p : Nat → Nat) : Prop :=
  ∀ x, x ∈ D → ∀ x', x' ∈ D → p x = p x' → SigEq Q x x'

def FiberConstant (D : List Nat) (p q : Nat → Nat) : Prop :=
  ∀ x, x ∈ D → ∀ x', x' ∈ D → p x = p x' → q x = q x'

def FactorsOn (D : List Nat) (p q : Nat → Nat) : Prop :=
  ∃ g : Nat → Nat, ∀ x, x ∈ D → g (p x) = q x

def pick (D : List Nat) (P : Nat → Bool) : Option Nat :=
  match D with
  | [] => none
  | a :: t => if P a then some a else pick t P

theorem factors_iff_fiberConstant (D : List Nat) (p q : Nat → Nat) :
    FactorsOn D p q ↔ FiberConstant D p q := by
  constructor
  · intro hf x hx x' hx' hp
    obtain ⟨g, hg⟩ := hf
    rw [← hg x hx, ← hg x' hx', hp]
  · intro hfc
    refine ⟨fun y => q ((pick D (fun z => decide (p z = y))).getD 0),
      ?_⟩
    intro x hx
    obtain ⟨r, hr⟩ :=
      pick_some_of_mem D (fun z => decide (p z = p x)) x hx
        (decide_eq_true rfl)
    have hrD := pick_mem D (fun z => decide (p z = p x)) r hr
    have hpr : p r = p x :=
      of_decide_eq_true (pick_holds D _ r hr)
    show q ((pick D (fun z => decide (p z = p x))).getD 0) = q x
    rw [hr]
    exact hfc r hrD x hx hpr

theorem factor_unique_on_image (D : List Nat) (p q g g' : Nat → Nat)
    (h : ∀ x, x ∈ D → g (p x) = q x)
    (h' : ∀ x, x ∈ D → g' (p x) = q x) :
    ∀ x, x ∈ D → g (p x) = g' (p x) :=
  fun x hx => (h x hx).trans (h' x hx).symm

theorem factor_not_unique_off_image :
    ∃ (D : List Nat) (p q g g' : Nat → Nat),
      (∀ x, x ∈ D → g (p x) = q x) ∧
      (∀ x, x ∈ D → g' (p x) = q x) ∧ g ≠ g' := by
  refine ⟨[0], id, id, id, fun n => if n = 5 then 6 else n,
    fun x _ => rfl, ?_, ?_⟩
  · intro x hx
    cases hx with
    | head => decide
    | tail _ hm => cases hm
  · intro h
    exact absurd (congrFun h 5) (by decide)

def pQ (D : List Nat) (Q : List (Nat → Nat)) : Nat → Nat :=
  fun x =>
    (pick D (fun z => decide (sigList Q z = sigList Q x))).getD 0

theorem pQ_exact (D : List Nat) (Q : List (Nat → Nat)) :
    ∀ x, x ∈ D → ∀ x', x' ∈ D →
      (pQ D Q x = pQ D Q x' ↔ SigEq Q x x') := by
  intro x hx x' hx'
  constructor
  · intro h
    apply (sigEq_iff_sigList Q x x').mpr
    have s1 := (pQ_spec D Q x hx).2
    have s2 := (pQ_spec D Q x' hx').2
    rw [← s1, ← s2, h]
  · intro h
    have hs := (sigEq_iff_sigList Q x x').mp h
    show (pick D
        (fun z => decide (sigList Q z = sigList Q x))).getD 0 =
      (pick D
        (fun z => decide (sigList Q z = sigList Q x'))).getD 0
    rw [hs]

theorem pQ_coarsest (D : List Nat) (Q : List (Nat → Nat))
    (p : Nat → Nat) (hp : Adequate D Q p) :
    FactorsOn D p (pQ D Q) := by
  apply (factors_iff_fiberConstant D p (pQ D Q)).mpr
  intro x hx x' hx' hpx
  exact (pQ_exact D Q x hx x' hx').mpr (hp x hx x' hx' hpx)

theorem descent_witness (D : List Nat) (Q : List (Nat → Nat))
    (p : Nat → Nat) (x x' : Nat) (hx : x ∈ D) (hx' : x' ∈ D)
    (hp : p x = p x') (hne : ¬ SigEq Q x x') :
    ∃ q, q ∈ Q ∧ q x ≠ q x' ∧ ¬ FiberConstant D p q := by
  obtain ⟨q, hm, hqne⟩ := exists_separator_of_not_sigEq Q x x' hne
  exact ⟨q, hm, hqne, fun hfc => hqne (hfc x hx x' hx' hp)⟩

def SplitsAt (D : List Nat) (Q Q' : List (Nat → Nat))
    (x : Nat) : Prop :=
  ∃ x', x' ∈ D ∧ SigEq Q x x' ∧ ¬ SigEq Q' x x'

theorem splits_iff_new_separator (D : List Nat)
    (Q Q' : List (Nat → Nat)) (x : Nat)
    (_hsub : ∀ q, q ∈ Q → q ∈ Q') :
    SplitsAt D Q Q' x ↔
      ∃ x', x' ∈ D ∧ SigEq Q x x' ∧
        ∃ q', q' ∈ Q' ∧ q' x ≠ q' x' := by
  constructor
  · intro h
    obtain ⟨x', hx', hsig, hnot⟩ := h
    obtain ⟨q', hm, hne⟩ := exists_separator_of_not_sigEq Q' x x' hnot
    exact ⟨x', hx', hsig, q', hm, hne⟩
  · intro h
    obtain ⟨x', hx', hsig, q', hm, hne⟩ := h
    exact ⟨x', hx', hsig, fun hs => hne (hs q' hm)⟩

theorem absolute_adequacy_iff_injective (D : List Nat)
    (p : Nat → Nat) :
    (∀ Q : List (Nat → Nat), Adequate D Q p) ↔
      (∀ x, x ∈ D → ∀ x', x' ∈ D → p x = p x' → x = x') := by
  constructor
  · intro h x hx x' hx' hp
    have hsig := h [fun z => if z = x then 1 else 0] x hx x' hx' hp
    have h1 : (if x = x then (1 : Nat) else 0) =
        (if x' = x then (1 : Nat) else 0) :=
      hsig (fun z => if z = x then (1 : Nat) else 0)
        List.mem_cons_self
    rw [if_pos rfl] at h1
    cases hd : decide (x' = x) with
    | true => exact (of_decide_eq_true hd).symm
    | false =>
      rw [if_neg (of_decide_eq_false hd)] at h1
      exact absurd h1 (by decide)
  · intro h Q x hx x' hx' hp q _
    rw [h x hx x' hx' hp]

theorem postcompose_no_refine (Q : List (Nat → Nat))
    (f : List Nat → Nat) (x x' : Nat) :
    SigEq (Q ++ [fun z => f (sigList Q z)]) x x' ↔
      SigEq Q x x' := by
  constructor
  · intro h q hq
    exact h q (List.mem_append.mpr (Or.inl hq))
  · intro h q hq
    cases List.mem_append.mp hq with
    | inl h1 => exact h q h1
    | inr h2 =>
      cases h2 with
      | head =>
        show f (sigList Q x) = f (sigList Q x')
        rw [(sigEq_iff_sigList Q x x').mp h]
      | tail _ h3 => cases h3

theorem refine_requires_separator (D : List Nat)
    (Q Q' : List (Nat → Nat)) (x : Nat) (h : SplitsAt D Q Q' x) :
    ∃ q', q' ∈ Q' ∧
      ¬ (∃ f : List Nat → Nat, ∀ z, q' z = f (sigList Q z)) := by
  obtain ⟨x', hx', hsig, hnot⟩ := h
  obtain ⟨q', hm, hne⟩ := exists_separator_of_not_sigEq Q' x x' hnot
  refine ⟨q', hm, ?_⟩
  intro hdet
  obtain ⟨f, hf⟩ := hdet
  apply hne
  rw [hf x, hf x', (sigEq_iff_sigList Q x x').mp hsig]

def classCount (D : List Nat) (Q : List (Nat → Nat)) : Nat :=
  (dedupL (D.map (sigList Q))).length

theorem strict_split_increases (D : List Nat)
    (Q Q' : List (Nat → Nat)) (hsub : ∀ q, q ∈ Q → q ∈ Q')
    (x : Nat) (hx : x ∈ D) (hs : SplitsAt D Q Q' x) :
    classCount D Q < classCount D Q' := by
  obtain ⟨x', hx', hsig, hnot⟩ := hs
  have hdet : ∀ a, a ∈ D → ∀ b, b ∈ D →
      sigList Q' a = sigList Q' b → sigList Q a = sigList Q b :=
    fun a _ b _ hab =>
      (sigEq_iff_sigList Q a b).mp
        (enlarge_refines Q Q' hsub a b
          ((sigEq_iff_sigList Q' a b).mpr hab))
  exact count_lt_of_split (sigList Q') (sigList Q) D hdet x x' hx hx'
    ((sigEq_iff_sigList Q x x').mp hsig)
    (fun he => hnot ((sigEq_iff_sigList Q' x x').mpr he))

theorem strict_steps_lt (D : List Nat) (hD : D ≠ [])
    (Q : List (Nat → Nat)) (t : List (List (Nat → Nat)))
    (hc : StrictChain D (Q :: t)) : t.length < D.length := by
  have h1 := chain_count D t Q hc
  have h2 := classCount_pos D Q hD
  omega

end Compression
```

And the book-Lean additions in `textbook/checks/u61_lean.py` (`namespace Textbook.U61`):

```lean
namespace Textbook.U61

open Compression

theorem splits_iff_without_sub (D : List Nat)
    (Q Q' : List (Nat → Nat)) (x : Nat) :
    SplitsAt D Q Q' x ↔
      ∃ x', x' ∈ D ∧ SigEq Q x x' ∧
        ∃ q', q' ∈ Q' ∧ q' x ≠ q' x' := by
  constructor
  · intro h
    obtain ⟨x', hx', hsig, hnot⟩ := h
    obtain ⟨q', hm, hne⟩ := exists_separator_of_not_sigEq Q' x x' hnot
    exact ⟨x', hx', hsig, q', hm, hne⟩
  · intro h
    obtain ⟨x', hx', hsig, q', hm, hne⟩ := h
    exact ⟨x', hx', hsig, fun hs => hne (hs q' hm)⟩

theorem non_sub_split_preserves_count :
    SplitsAt [0, 1, 2] [ind 0] [ind 1] 1 ∧
      classCount [0, 1, 2] [ind 0] = 2 ∧
      classCount [0, 1, 2] [ind 1] = 2 := by
  refine ⟨⟨2, ?_, ?_, ?_⟩, rfl, rfl⟩
  · exact List.mem_cons_of_mem _ (List.mem_cons_of_mem _ List.mem_cons_self)
  · intro q hq
    cases hq with
    | head => decide
    | tail _ hm => cases hm
  · intro hs
    exact absurd (hs (ind 1) List.mem_cons_self) (by decide)

end Textbook.U61
```

---

## Line-by-line Lean explanation

- **`factors_iff_fiberConstant`:** Forward (`mp`): if $g(p(z)) = q(z)$ on $D$ and $p(x) = p(x')$, rewriting $q(x) \leftarrow g(p(x))$ and $q(x') \leftarrow g(p(x'))$ yields $q(x) = q(x')$. Reverse (`mpr`): defines $g(y) = q((\mathrm{pick}\;D\;(\lambda z \Rightarrow \mathrm{decide}(p(z) = y))).\mathrm{getD}\;0)$. For $x \in D$, `pick_some_of_mem` produces the first $r \in D$ with $p(r) = p(x)$ (using `pick_mem` and `pick_holds`), and `hfc r hrD x hx hpr` concludes $q(r) = q(x)$. Note that `decide (p z = y)` uses `Nat.decEq`, which touches `[Quot.sound]` in Lean 4's kernel axiom tracker through standard library machinery.
- **`factor_unique_on_image` and `factor_not_unique_off_image`:** Both are axiom-free (`does not depend on any axioms`). `factor_unique_on_image` chains `(h x hx).trans (h' x hx).symm`. `factor_not_unique_off_image` exhibits $D = [0]$, $p = q = g = \mathrm{id}$, and $g'(n) = (\text{if } n = 5 \text{ then } 6 \text{ else } n)$, using `congrFun h 5` to refute $g = g'$.
- **`pQ`, `pQ_exact`, and `pQ_coarsest`:** `pQ D Q x` picks the first element of $D$ whose `sigList Q` equals `sigList Q x`. `pQ_exact` uses `pQ_spec` (the chosen representative lies in $D$ and has the same `sigList Q` as $x$) for the forward direction and rewrites by `sigList Q x = sigList Q x'` for the reverse direction. `pQ_coarsest` applies `(factors_iff_fiberConstant D p (pQ D Q)).mpr` and uses `hp : Adequate D Q p` together with `pQ_exact`.
- **`descent_witness`:** Calls `exists_separator_of_not_sigEq Q x x' hne` (which walks `Q` by list recursion using `sigEq_decompose` and `decide (q x = q x')`) to obtain $q \in Q$ with $q(x) \neq q(x')$; if `hfc : FiberConstant D p q` held, $p(x) = p(x')$ would force $q(x) = q(x')$, contradicting `hqne`.
- **`splits_iff_new_separator` and `Textbook.U61.splits_iff_without_sub`:** Unpack `SplitsAt D Q Q' x` and apply `exists_separator_of_not_sigEq Q' x x'` in the forward direction and `fun hs => hne (hs q' hm)` in the reverse direction. Neither direction touches `_hsub`.
- **`absolute_adequacy_iff_injective`:** In the forward direction, specializes `h : ∀ Q, Adequate D Q p` to the one-question indicator family `[fun z => if z = x then 1 else 0]`. Evaluating at $x$ gives $1$; if $x' \neq x$, evaluating at $x'$ gives $0$, contradicting $1 = 0$.
- **`postcompose_no_refine` and `refine_requires_separator`:** `postcompose_no_refine` splits membership in `Q ++ [fun z => f (sigList Q z)]` via `List.mem_append` and rewrites `f (sigList Q x) = f (sigList Q x')` using `(sigEq_iff_sigList Q x x').mp h` (`List.mem_append` pulls in `[propext]`). `refine_requires_separator` takes the separating question $q' \in Q'$ with $q'(x) \neq q'(x')$ across $\mathrm{SigEq}(Q, x, x')$; if $q'(z) = f(\mathrm{sigList}(Q, z))$ held for all $z$, then $\mathrm{sigList}(Q, x) = \mathrm{sigList}(Q, x')$ would force $q'(x) = q'(x')$.
- **`strict_split_increases`, `strict_steps_lt`, and `Textbook.U61.non_sub_split_preserves_count`:** `strict_split_increases` uses `enlarge_refines Q Q' hsub` to establish that `sigList Q'` determines `sigList Q` on $D$, then invokes `count_lt_of_split` on the pair $(x, x')$ that agrees on $Q$ and disagrees on $Q'$. `strict_steps_lt` combines `chain_count D t Q hc` ($\mathrm{classCount}(D, Q) + |t| \le |D|$) with `classCount_pos D Q hD` ($1 \le \mathrm{classCount}(D, Q)$) via `omega`. Finally, `non_sub_split_preserves_count` shows that when `hsub` is dropped ($Q = [\mathrm{ind}\;0]$, $Q' = [\mathrm{ind}\;1]$ on $D = [0, 1, 2]$), `SplitsAt` holds at $x = 1$ while `classCount` remains $2$.

---

## What has been proved

1. **Factorization equivalence and image-scoped uniqueness (`factors_iff_fiberConstant`, `factor_unique_on_image`, `factor_not_unique_off_image`):** Over any represented domain `D : List Nat`, a question `q` factors through a presentation `p` on `D` if and only if `p`'s fibers over `D` are `q`-constant; the factoring map is constructed by first-match selection (`pick`), is unique on $p(D)$, and is not unique off $p(D)$.
2. **Signature quotient (`pQ_spec`, `pQ_exact`, `pQ_adequate`, `pQ_coarsest`, `pQ_unique_on_image`):** The first-match quotient `pQ D Q` has fibers over `D` equal to the `Q`-signature classes, is `Q`-adequate, and factors through every `Q`-adequate presentation `p` on `D`, uniquely on $p(D)$.
3. **Constructive descent failure witness (`descent_witness`):** Whenever $x, x' \in D$ satisfy $p(x) = p(x')$ and $\neg\,\mathrm{SigEq}(Q, x, x')$, list recursion over `Q` constructs a question $q \in Q$ with $q(x) \neq q(x')$ and $\neg\,\mathrm{FiberConstant}(D, p, q)$.
4. **Enlargement, splits, and non-signature-determination (`enlarge_refines`, `splits_iff_new_separator`, `dup_no_refine`, `postcompose_no_refine`, `refine_requires_separator`):** Subfamily enlargement refines `SigEq`; a class splits at $x$ if and only if the new family contains a separator $q'$ across an old `Q`-agreement; duplicating `Q` or appending $f \circ \mathrm{sigList}\;Q$ refines nothing; and every split requires some $q' \in Q'$ not of the form $f \circ \mathrm{sigList}\;Q$.
5. **No absolute adequacy (`absolute_adequacy_iff_injective`):** `∀ Q, Adequate D Q p` is equivalent to injectivity of `p` on `D`.
6. **Non-uniqueness of splits and strict chain bound (`refinement_not_unique`, `refinement_tie`, `refine_bounded`, `classCount_pos`, `strict_split_increases`, `chain_bounded`, `strict_steps_lt`):** On $D = [0, 1, 2]$, $[\mathrm{ind}\;0]$ and $[\mathrm{ind}\;1]$ both split the empty-family class at $0$ with length $1$ and distinct resulting partitions; under subfamily enlargements ($Q \subseteq Q'$), every split on $D$ strictly increases `classCount D Q`, bounding any strict chain on a nonempty $D$ to length at most $|D|$ and fewer than $|D|$ split steps.

---

## What has not been proved

1. **Off-domain behavior or undeclared question families:** Every theorem is scoped to membership in the list `D : List Nat` and to questions in the list `Q : List (Nat → Nat)`. Nothing is claimed for points outside `D`.
2. **Image-isomorphism uniqueness of coarsest adequate presentations:** `pQ_coarsest` proves one-way factorization `FactorsOn D p (pQ D Q)` for every `Q`-adequate `p`; `Compression.lean` does not formulate or prove a theorem that any two presentations sharing this universal property have isomorphic images on `D`.
3. **Formal semantics for "replay", "evidential", "hash", "record", or "cost":** As noted in the audit (`textbook/audit/modules/Compression.md` §11.1, §11.4), these words appear only in docstrings/comments of `postcompose_no_refine`, `refine_requires_separator`, and `refinement_tie`. What is proved is strictly about functions of the form `f ∘ sigList Q` and list length `Q.length`.
4. **Termination of any machine execution from `chain_bounded`:** `chain_bounded` and `strict_steps_lt` bound the length of a Lean list `L : List (List (Nat → Nat))` satisfying the predicate `StrictChain D L`; they do not prove termination of a state-machine transition relation (`Step` does not appear in `Compression.lean`).

---

## Outside the system

- **Functions `Nat → Nat` and metatheoretic universal quantification in `absolute_adequacy_iff_injective`:** Questions and presentations are typed as total Lean functions `Nat → Nat`. Within the individual adequacy and quotient theorems, values of $p$ and $q$ are inspected only on elements of the finite list `D`. In `absolute_adequacy_iff_injective`, the left-hand side `∀ Q : List (Nat → Nat), Adequate D Q p` quantifies over the metatheoretic totality of all finite lists of functions `Nat → Nat`; the module uses that quantifier negatively (instantiating it at the indicator family `[fun z => if z = x then 1 else 0]`) to show that demanding adequacy across all families forces injectivity on `D`.
- **Decidability of `Nat` and `List Nat` equality:** Both `pick` and `sigEq_decompose` rely on `DecidableEq Nat` (`decide (p z = y)`, `decide (sigList Q z = sigList Q x)`, `decide (q x = q x')`) so that factoring maps, quotient representatives, and separating witnesses are computed by structural recursion on `D` and `Q` without classical choice.
- **Exhaustive Python bounds (`MAX_N = 3`, `MAX_M = 3`, `MAX_FAMILY = 2`):** The Python mirror `code/derivation/compression.py` enumerates functions $D \to \{0, \dots, m-1\}$ for $|D| \le 3$, $m \le 3$, and families of length $\le 2$ (covering $37{,}736$ merged-but-separated descent instances and $10{,}006$ split instances). The unconditional statements for arbitrary finite lists `D` and `Q` are the Lean theorems.

---

## Student exercise

Let $D = [0, 1, 2, 3]$ and consider two questions on $D$:
$$q_{\mathrm{parity}}(x) = x \bmod 2, \qquad q_{\mathrm{half}}(x) = \lfloor x / 2 \rfloor.$$

1. Compute the signature quotient presentations $p_{Q^{(0)}}, p_{Q^{(1)}}, p_{Q^{(2)}}$ on $D$ (as 4-tuples of values on $(0, 1, 2, 3)$) and their class counts $\mathrm{classCount}(D, Q^{(i)})$ along the enlarging chain
   $$Q^{(0)} = [], \qquad Q^{(1)} = [q_{\mathrm{parity}}], \qquad Q^{(2)} = [q_{\mathrm{parity}}, q_{\mathrm{half}}].$$
2. Consider the presentation $p_{\mathrm{fine}} = (2, 1, 2, 3)$ on $D = [0, 1, 2, 3]$. Is $p_{\mathrm{fine}}$ adequate for $Q^{(1)} = [q_{\mathrm{parity}}]$ on $D$? If so, find the unique values of a factoring map $g$ for $p_{Q^{(1)}}$ through $p_{\mathrm{fine}}$ on the image $p_{\mathrm{fine}}(D) = \{1, 2, 3\}$, and exhibit two distinct extensions $g_a, g_b : \{0, 1, 2, 3\} \to \{0, 1, 2, 3\}$ that both satisfy $g(p_{\mathrm{fine}}(x)) = p_{Q^{(1)}}(x)$ for all $x \in D$.
3. On $D_3 = [0, 1, 2]$, let $Q = [\mathrm{ind}\;0]$ and $Q' = [\mathrm{ind}\;1]$ (note $Q \not\subseteq Q'$). Show that $\mathrm{SplitsAt}(D_3, Q, Q', 1)$ holds and find the witnessing pair $(x', q')$, yet verify that $\mathrm{classCount}(D_3, Q) = \mathrm{classCount}(D_3, Q') = 2$. Why does this not contradict `strict_split_increases`?

---

## Answer

1. **Quotient presentations and class counts along $Q^{(0)} \subset Q^{(1)} \subset Q^{(2)}$ on $D = [0, 1, 2, 3]$:**
   - For $Q^{(0)} = []$: every $x \in D$ has empty signature `[]`, whose first match in $D = [0, 1, 2, 3]$ is $0$. Thus
     $$p_{Q^{(0)}} = (0, 0, 0, 0), \qquad \mathrm{classCount}(D, Q^{(0)}) = 1, \qquad \text{partition } [[0, 1, 2, 3]].$$
   - For $Q^{(1)} = [q_{\mathrm{parity}}]$: the signatures on $(0, 1, 2, 3)$ are `[0], [1], [0], [1]`. The first match in $D$ with signature `[0]` is $0$, and the first match with signature `[1]` is $1$. Thus
     $$p_{Q^{(1)}} = (0, 1, 0, 1), \qquad \mathrm{classCount}(D, Q^{(1)}) = 2, \qquad \text{partition } [[0, 2], [1, 3]].$$
     Appending the signature-determined digest $q_{\neg\mathrm{parity}}(x) = 1 - (x \bmod 2)$ gives signatures `[0, 1], [1, 0], [0, 1], [1, 0]`, leaving both $p_Q = (0, 1, 0, 1)$ and $\mathrm{classCount} = 2$ unchanged (`postcompose_no_refine`).
   - For $Q^{(2)} = [q_{\mathrm{parity}}, q_{\mathrm{half}}]$: the signatures on $(0, 1, 2, 3)$ are `[0, 0], [1, 0], [0, 1], [1, 1]`, all distinct. Thus
     $$p_{Q^{(2)}} = (0, 1, 2, 3), \qquad \mathrm{classCount}(D, Q^{(2)}) = 4, \qquad \text{partition } [[0], [1], [2], [3]].$$
     This 2-step strict chain on $|D| = 4$ satisfies $|t| = 2 < 4 = |D|$ (`strict_steps_lt`).

2. **Factoring $p_{Q^{(1)}} = (0, 1, 0, 1)$ through $p_{\mathrm{fine}} = (2, 1, 2, 3)$ on $D = [0, 1, 2, 3]$:**
   - The fibers of $p_{\mathrm{fine}}$ on $D$ are $\{0, 2\}$ (mapped to $2$), $\{1\}$ (mapped to $1$), and $\{3\}$ (mapped to $3$). Since $0$ and $2$ have the same parity $q_{\mathrm{parity}}(0) = q_{\mathrm{parity}}(2) = 0$, `Adequate D Q1 p_fine` holds.
   - By `pQ_coarsest` and `factor_unique_on_image`, any factoring map $g$ satisfying $g(p_{\mathrm{fine}}(x)) = p_{Q^{(1)}}(x)$ for all $x \in D$ is uniquely determined on $p_{\mathrm{fine}}(D) = \{1, 2, 3\}$ by:
     $$g(2) = p_{Q^{(1)}}(0) = 0, \qquad g(1) = p_{Q^{(1)}}(1) = 1, \qquad g(3) = p_{Q^{(1)}}(3) = 1.$$
   - Because $0 \notin p_{\mathrm{fine}}(D)$, the value $g(0)$ is unconstrained by $D$: both $g_a = \{0 \mapsto 0, 1 \mapsto 1, 2 \mapsto 0, 3 \mapsto 1\}$ and $g_b = \{0 \mapsto 3, 1 \mapsto 1, 2 \mapsto 0, 3 \mapsto 1\}$ satisfy $g(p_{\mathrm{fine}}(x)) = p_{Q^{(1)}}(x)$ for every $x \in D$ while $g_a(0) \neq g_b(0)$.

3. **Non-subfamily split on $D_3 = [0, 1, 2]$ ($Q = [\mathrm{ind}\;0]$, $Q' = [\mathrm{ind}\;1]$):**
   - Under $Q = [\mathrm{ind}\;0]$, points $1$ and $2$ have equal signature `[0]`, so $\mathrm{SigEq}(Q, 1, 2)$ holds. Under $Q' = [\mathrm{ind}\;1]$, $\mathrm{ind}\;1\;(1) = 1 \neq 0 = \mathrm{ind}\;1\;(2)$, so $\neg\,\mathrm{SigEq}(Q', 1, 2)$ holds. Thus $\mathrm{SplitsAt}(D_3, Q, Q', 1)$ holds with witness $x' = 2 \in D_3$ and separator $q' = \mathrm{ind}\;1 \in Q'$ (`splits_iff_without_sub`).
   - However, $\mathrm{classCount}(D_3, Q) = 2$ (classes $\{0\}$ and $\{1, 2\}$) and $\mathrm{classCount}(D_3, Q') = 2$ (classes $\{0, 2\}$ and $\{1\}$). This does not contradict `strict_split_increases` because `strict_split_increases` requires the subfamily hypothesis `hsub : ∀ q, q ∈ Q → q ∈ Q'`, which fails here ($\mathrm{ind}\;0 \notin [\mathrm{ind}\;1]$): dropping $\mathrm{ind}\;0$ allows $0$ and $2$ to merge at the same time $1$ and $2$ split.

---

## Verification

Run both standalone verification scripts from the repository root:

```text
$ python textbook/checks/u61_compression.py
Unit 61 Compression check: factorization_iff=True; quotient_exact_adequate_coarsest=True/True/True; descent_instances=37736; splits=10006; D4_counts=[1, 2, 2, 4]; failures=[]

$ python textbook/checks/u61_lean.py
Unit 61 Lean check: exit=0; axiom reports as expected: 26 of 26; failures: []
```

**Count correction, 2026-10-28.** The artifact contains 12 axiom-free Compression reports, not 13. The book theorems are a separate population; four are checked after the
2026-10-31 domain-order example was added.
