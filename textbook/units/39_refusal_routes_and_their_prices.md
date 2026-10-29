# Unit 39. Comparing refusal protocols under declared prices

**Claim.** The search compares 44 declared protocols within six events and
a four-position cap. Its cheapest protocol depends on the chosen
milestone and cost order. Lean separately proves facts about particular
routes; it does not prove universal optimality over every protocol.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Unit 38 compared five ways of recording a refused repeat. This
module widens the comparison to a declared space of 44 *protocols*
(result algebra, retention rule, tag, reflection, relation rule, one or
two tokens) and asks which reach a witnessed, oriented pair at what
declared price. Two-token protocols are controls in the same search.
Lean proves the cores: silent refusal is inert over histories whose
admissions all name already-present tokens (`silent_repetition_inert`); the
traced runner's results never feed back into the state (`trace_erasure`,
`histories_collapse`); the judgment variant never grows its carrier
(`judgment_carrier_bound`); a priced route with tag and relation closes
and is oriented (`priced_bridge_closes`, `priced_bridge_oriented`); the
cheaper route with a receipt and a relation rule and no tag closes
(`min_witnessed_route_closes`); the bridge's irreflexive *facts* do not
entail the irreflexivity *law* (`bridge_facts_not_law`); an equivariant
construction sends fixed points to fixed points
(`equivariant_output_invariant`); and a declared reflective rule realizes
the successor chain for every `n` (`reflective_chain_is_initial_segment`).
That the receipt-and-relation route is the *unique minimum* under both
cost orders is a finite search over the 44 protocols at a 6-event
horizon and carrier cap 4, not a general minimality theorem.

**Status:** derived (the cores); bounded
computation, exhaustive in class (minimality and uniqueness); declared
(the protocol space and the cost orders). **Lean:**
`lean4/Derivation/RefusalFrontier.lean` lines 29-47, 60-84, 94-116,
124-162, 179-252, 261-282, 292-370. **Axioms:** within
`{propext, Quot.sound}`; `equivariant_output_invariant` and the T3 and
`Bool` facts use none. **Depends on:** `stepR`, `replayR`, `emptyR` (Unit
38); `Bridge.irrefl_law_not_entailed` (Unit 26); `Irrefl` (Unit 24);
`List.range`.

</details>

## First pass

Compare two ways to retain a receipt for a repeated token:

| Route | What is added | Separated pair? | Written directed link? |
|---|---|---|---|
| Tag | Receipt and a tag on it | Yes | No |
| Relation | Receipt and a link from the subject | Yes | Yes |

The two routes reach different milestones. Asking only for a separated
pair is a weaker task than also asking for a written relation witness.

The declared cost order A charges both routes 2 imports, so they tie for
separation. Order B compares three counts in sequence: first external
token acts, then sorts and constructors, then rules. Their prices are
`(0,1,2)` and `(0,1,3)`, so the tag route wins for separation under B.
For the written-link milestone, the relation route is the unique minimum
under both orders in this search.

**Predict:** has agreement between these two prices proved the route
cheapest under every possible price system?

<details>
<summary>Check your prediction</summary>

No. The conclusion names two chosen orders, 44 protocols, six events,
and a four-position cap. Changing the task, menu, or prices asks a new
question.

</details>

## Question

Unit 38 ended with a price: the tag discipline reaches a witnessed pair
in two admissions by declaring a unary observable. Is that the cheapest
way? Is it the only way? And is "cheapest" even well defined, or does it
depend on how imports are counted? The module answers by enumerating
every protocol in a declared class, running each to a horizon, and
proving in Lean the facts that do not depend on the horizon.

## What we already possess

- `RState`, `REvent`, `stepR`, `replayR` and the five modes (Unit 38).
- `single_token_carrier_bound` (Unit 11) and the carrier bound for the
  non-reifying modes (Unit 38).
- The fact/law boundary: `irrefl_law_not_entailed` (Unit 26).
- The equivariance obstruction on `Bool` (`Bridge.equivariant_witness_is_S2`,
  `equivariant_not_D2`, cited by name in Units 37 and 38).

## New concept: a protocol space, milestones, and two cost orders

A protocol is a six-tuple: a result algebra with one constructor (`New`)
or two (`New`, `Refused`); a retention rule for refusals, one of `none`,
`judgment` (a separate store), `occurrence` (re-append the token itself)
or `datum` (reify a fresh receipt into the carrier); and, only with
`datum`, an optional tag, optional reflection (receipts can be presented
again) and an optional relation rule (reifying also asserts a link from
the refused subject to the receipt); plus one token or a second token as
a control. Forty-four tuples survive the constraints.

Each protocol is run to a horizon of six events and asked when it first
reaches each *milestone*: two carrier elements; a separable pair; an
oriented pair; a witnessed relation; a witnessed irreflexive fact. Two
cost orders rank protocols: A counts declared imports; B is
lexicographic in (external token acts, sorts and constructors, rules).

The Lean module then takes the cores out of the search and proves them
without a horizon, as eight theorem groups T1 to T8, on small state
types written for each: `RState` for T1 and T2, pairs of codes for T3,
`JState` for T4, `PState` and `MState` for T5, and `PState` again for T8.

## Plain-language interpretation

Imagine many door policies for the second knock, each built from a short
menu: do you note the knock in a ledger, hand out a receipt, pin a badge
on the receipt, let receipts knock too, and write down "this receipt
belongs to that knock"? For each policy, ask how many knocks it takes
before someone inside can point at two different things, say which is
which, and show a written link between them. Then ask which policy buys
that with the fewest menu items.

The answer has three parts. Ignoring the knock buys nothing, however
many times it happens. Several policies get two things in the room for
one menu item, and which is "cheapest" among them depends on how you
price the menu. But only one policy gets a *written link* for two menu
items under order A, and is the same unique minimum under the declared
order B: hand out a receipt, and write "this
receipt belongs to that knock". The badge is not needed for the link; it
was needed in Unit 38 only because that unit's menu had no link rule.

In these models, the extra receipt, tag, and link follow from the
declared menu rules. The search does not derive that menu from repetition.

## Pseudocode

```
# Gloss
protocol := (algebra ∈ {1,2}, retention ∈ {none, judgment, occurrence, datum},
             tag?, reflection?, autorel?, tokens ∈ {1,2})
             with tag/reflection/autorel only under datum       -- 44 of them

-- T1: silent refusal over a whole history
if every admitTok in h names a token already in s.data
   then foldl (stepR silent) s h = s

-- T5: the two closing routes, from one token presented twice
stepP s t := if t in s.data then append t; tag (len); link (0, len)   -- tag + relation
             else append t
stepM s t := if tok t in s.data then append receipt(len); link (0, len) -- relation only
             else append tok t
bridgeState = stepP (stepP empty 0) 0 = ⟨[0,0], [1], [(0,1)]⟩
minState    = stepM (stepM empty 0) 0 = ⟨[tok 0, receipt 1], [(0,1)]⟩

-- T7: an equivariant F sends fixed points of the symmetry to fixed points
F (act s) = act' (F s)  and  act s = s   ==>  act' (F s) = F s

-- T8: a declared reflective step, iterated
stepRefl s := append (len s); tag (len s); link (len s - 1, len s)
reflState n = ⟨range (n+1), [1..n], successor links⟩
```

## Python

```python
from derivation.refusal_frontier import Proto, cost_a, cost_b, minimum_table, protocol_report

routes = {"silent": Proto(1, "none", False, False, False, 1),
          "tag": Proto(1, "datum", True, False, False, 1),
          "relation": Proto(1, "datum", False, False, True, 1)}
for name, p in routes.items():
    m = protocol_report(p, 6)["min_events_to"]
    print(name, m["two_carrier"], m["oriented_pair"], m["witnessed_relation"], cost_a(p), cost_b(p))
mt = minimum_table(6)
for order in ("A_total_imports", "B_lex"):
    print(order, [len(mt[order][ms]["tied_minima"]) for ms in
                  ("two_carrier", "separable_pair", "witnessed_relation")])
```

Output:

```text
silent None None None 0 (0, 0, 0)
tag 2 2 None 2 (0, 1, 2)
relation 2 2 2 2 (0, 1, 3)
A_total_imports [3, 2, 1]
B_lex [1, 1, 1]
```

The check script's table, every row compared with
`artifacts/refusal_frontier.json`:

```text
declared protocols: 44 (artifact 44)
route: min events to two_carrier / separable / oriented / witnessed / witnessed_irrefl; dynamics; cost A; cost B
  silent                     None / None / None / None / None; fixpoint; 0; (0, 0, 0)
  judgment                   None / None / None / None / None; bounded; 1; (0, 0, 1)
  tag route                  2 / 2 / 2 / None / None; growth_to_cap; 2; (0, 1, 2)
  relation route (minimum)   2 / 2 / 2 / 2 / 2; growth_to_cap; 2; (0, 1, 3)
  tag + relation (stepP)     2 / 2 / 2 / 2 / 2; growth_to_cap; 3; (0, 1, 4)
  reflection                 2 / None / None / None / None; growth_to_cap; 2; (0, 1, 2)
  A_total_imports  two_carrier           cost 1, 3 minimum protocol(s): ret=none tag=False rel=False tok=2; ret=occurrence tag=False rel=False tok=1; ret=datum tag=False rel=False tok=1
  A_total_imports  separable_pair        cost 2, 2 minimum protocol(s): ret=datum tag=False rel=True tok=1; ret=datum tag=True rel=False tok=1
  A_total_imports  oriented_pair         cost 2, 2 minimum protocol(s): ret=datum tag=False rel=True tok=1; ret=datum tag=True rel=False tok=1
  A_total_imports  witnessed_relation    cost 2, 1 minimum protocol(s): ret=datum tag=False rel=True tok=1
  A_total_imports  witnessed_irreflexive cost 2, 1 minimum protocol(s): ret=datum tag=False rel=True tok=1
  B_lex            two_carrier           cost (0, 0, 1), 1 minimum protocol(s): ret=occurrence tag=False rel=False tok=1
  B_lex            separable_pair        cost (0, 1, 2), 1 minimum protocol(s): ret=datum tag=True rel=False tok=1
  B_lex            oriented_pair         cost (0, 1, 2), 1 minimum protocol(s): ret=datum tag=True rel=False tok=1
  B_lex            witnessed_relation    cost (0, 1, 3), 1 minimum protocol(s): ret=datum tag=False rel=True tok=1
  B_lex            witnessed_irreflexive cost (0, 1, 3), 1 minimum protocol(s): ret=datum tag=False rel=True tok=1
normal form in class: holds True, every reacher made a purchase True, witnessed_irreflexive reachers 16, witnessed without a relation rule [], separable without tag or relation []
imports of the minimum route: ['receipt reification rule (coproduct into carrier)', 'relation symbol + witness rule']
failures: []
```

## Line-by-line Python explanation

`Proto(algebra, retention, tagging, reflection, autorel, tokens)` is the
six-tuple; `enumerate_protocols()` builds all of them and keeps the 44
that pass `valid()`. `protocol_report(p, 6)` runs the protocol over every
enabled event sequence of length at most six from the empty state,
discarding steps that exceed carrier cap 4, and records,
per milestone, the least depth at which a reached state satisfies it,
or `None`. `cost_a` is the length of `p.imports()`; `cost_b` is the
triple.

The silent protocol admits its first token and then reaches a fixed state
under the available repeats. None of the five listed two-element or
relational milestones is reached; “nothing” here is not an empty state.
The tag route
reaches two carrier elements, a separable pair and an oriented pair at
two events and never a witnessed relation: it has no relation rule to
write one. The relation route reaches all five at two events. The
`stepP` route of T5 reaches the same five at a higher price (3 under A).
Reflection alone reaches two carrier elements and nothing else: receipts
knock, but nothing tells them apart.

`minimum_table(6)` collects, per order and milestone, the least cost and
every protocol attaining it. Under A, three protocols tie for two carrier
elements (the three purchases Unit 13 named: a second token, occurrence
identity, reification), two tie for a separable or oriented pair (tag
route, relation route), and one protocol attains a witnessed relation.
Under B the weaker ties are broken differently (occurrence; tag route),
and the witnessed minimum is the same single protocol. That agreement is
the computed content of "unique minimum witnessed bridge": a fact about
44 protocols at horizon 6 under two declared orders.

`normal_form_check` is the in-class dependency audit: no protocol
reaches a witnessed relation without the relation rule, none reaches a
separable pair without a tag or a relation, none reaches two carrier
elements without reification, occurrence or a second token, and every
protocol that reaches anything imported something. These are the
exhaustive-in-class halves of the paper's FR8; the class-general Lean
form is listed as unresolved there.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/RefusalFrontier.lean lines 29-47
theorem silent_repetition_inert (h : List REvent) :
    ∀ s : RState,
      (∀ e ∈ h, ∀ tok, e = REvent.admitTok tok → tok ∈ s.data) →
      h.foldl (stepR .silent) s = s := by
  induction h with
  | nil => intro s _; rfl
  | cons e rest ih =>
      intro s hall
      have hstep : stepR .silent s e = s := by
        cases e with
        | supply tok => rfl
        | marker tok => rfl
        | admitTok tok =>
            have hmem := hall _ List.mem_cons_self tok rfl
            simp only [stepR]
            rw [if_pos hmem]
      simp only [List.foldl]
      rw [hstep]
      exact ih s (fun e' he' => hall e' (List.mem_cons_of_mem _ he'))
```

```lean
-- Lean (Genesis), lean4/Derivation/RefusalFrontier.lean lines 179-199, 223-252, 261-264, 276-282
structure PState where
  data : List Nat
  tags : List Nat
  rel : List (Nat × Nat)
deriving Repr, DecidableEq

def stepP (s : PState) (tok : Nat) : PState :=
  if tok ∈ s.data then
    { data := s.data ++ [tok],
      tags := s.tags ++ [s.data.length],
      rel := s.rel ++ [(0, s.data.length)] }
  else { s with data := s.data ++ [tok] }

def bridgeState : PState := stepP (stepP ⟨[], [], []⟩ 0) 0

theorem priced_bridge_closes :
    bridgeState.data.length = 2 ∧
    bridgeState.rel = [(0, 1)] ∧
    (∀ p ∈ bridgeState.rel, p.1 ≠ p.2) ∧
    bridgeState.tags = [1] := by decide

inductive MItem where
  | tok (n : Nat)
  | receipt (n : Nat)
deriving Repr, DecidableEq

structure MState where
  data : List MItem
  rel : List (Nat × Nat)
deriving Repr, DecidableEq

def stepM (s : MState) (t : Nat) : MState :=
  if MItem.tok t ∈ s.data then
    { data := s.data ++ [MItem.receipt s.data.length],
      rel := s.rel ++ [(0, s.data.length)] }
  else { s with data := s.data ++ [MItem.tok t] }

def minState : MState := stepM (stepM ⟨[], []⟩ 0) 0

theorem min_witnessed_route_closes :
    minState.data = [MItem.tok 0, MItem.receipt 1] ∧
    minState.rel = [(0, 1)] ∧
    (∀ p ∈ minState.rel, p.1 ≠ p.2) := by decide

theorem bridge_facts_not_law :
    ∃ r' : Nat → Nat → Prop,
      (∀ x y, (x, y) ∈ bridgeState.rel → r' x y) ∧
      ¬ PrimDiff.Irrefl r' :=
  ⟨fun _ _ => True, fun _ _ _ => trivial, fun hi => hi 0 trivial⟩

theorem equivariant_output_invariant {S R : Type} (actS : S → S)
    (actR : R → R) (F : S → R)
    (hequiv : ∀ s, F (actS s) = actR (F s)) :
    ∀ s, actS s = s → actR (F s) = F s := by
  intro s hfix
  calc actR (F s) = F (actS s) := (hequiv s).symm
    _ = F s := by rw [hfix]
```

```lean
-- Lean (Genesis), lean4/Derivation/RefusalFrontier.lean lines 304-345
def stepRefl (s : PState) : PState :=
  ⟨s.data ++ [s.data.length],
   s.tags ++ [s.data.length],
   s.rel ++ [(s.data.length - 1, s.data.length)]⟩

def reflState : Nat → PState
  | 0 => ⟨[0], [], []⟩
  | n + 1 => stepRefl (reflState n)

theorem reflective_chain_growth :
    ∀ n, (reflState n).data.length = n + 1 := by
  intro n
  induction n with
  | zero => rfl
  | succ m ih =>
      show (stepRefl (reflState m)).data.length = m + 2
      simp only [stepRefl, List.length_append]
      rw [ih]
      rfl

theorem reflective_chain_is_initial_segment :
    ∀ n, (reflState n).data = List.range (n + 1) := by
  intro n
  induction n with
  | zero => rfl
  | succ m ih =>
      show (stepRefl (reflState m)).data = List.range (m + 2)
      have hr : List.range (m + 2) = List.range (m + 1) ++ [m + 1] :=
        List.range_succ
      simp only [stepRefl]
      rw [reflective_chain_growth m, ih, hr]
```

The book's Lean instantiates the horizon-free theorems at concrete
histories, writes the two closing states out in full, shows that a third
presentation under the minimum route makes a star while reflection
makes a chain, gives a non-trivial witness for the fact/law gap, and
shows what the invariance ceiling says on `Bool`.

```lean
-- Lean (book), textbook/checks/u39_lean.py
theorem silent_inert_here :
    [REvent.admitTok 0, .marker 3, .admitTok 0].foldl (stepR .silent) ⟨[0], [], 0⟩ = ⟨[0], [], 0⟩ :=
  silent_repetition_inert _ _ (by
    intro e he tok htok
    subst htok
    simp at he
    simp [he])

theorem traced_results :
    (stepTraced emptyR (.admitTok 0)).1 = .isNew ∧
    (stepTraced (stepTraced emptyR (.admitTok 0)).2 (.admitTok 0)).1 = .existing := by
  decide

theorem judgment_bound_three :
    (([0, 0, 0] : List Nat).foldl stepJ ⟨[], []⟩).data = [] ∨
    (([0, 0, 0] : List Nat).foldl stepJ ⟨[], []⟩).data = [0] :=
  judgment_carrier_bound _ _ (Or.inl rfl) (by intro t ht; simp at ht; omega)

theorem bridge_state_value : bridgeState = ⟨[0, 0], [1], [(0, 1)]⟩ := by decide
theorem min_state_value : minState = ⟨[.tok 0, .receipt 1], [(0, 1)]⟩ := by decide

theorem min_third_presentation :
    stepM minState 0 = ⟨[.tok 0, .receipt 1, .receipt 2], [(0, 1), (0, 2)]⟩ := by
  decide

theorem refl_two : reflState 2 = ⟨[0, 1, 2], [1, 2], [(0, 1), (1, 2)]⟩ := by decide

def bridgePlusLoop : Nat → Nat → Prop :=
  fun x y => (x, y) ∈ bridgeState.rel ∨ (x = 0 ∧ y = 0)

theorem bridge_plus_loop_extends :
    (∀ x y, (x, y) ∈ bridgeState.rel → bridgePlusLoop x y) ∧
    ¬ PrimDiff.Irrefl bridgePlusLoop ∧ ¬ bridgePlusLoop 1 0 := by
  refine ⟨fun x y h => Or.inl h, fun hi => hi 0 (Or.inr ⟨rfl, rfl⟩), ?_⟩
  intro h
  rcases h with h | h
  · rw [bridge_state_value] at h
    simp at h
  · exact absurd h.1 (by decide)

theorem not_has_no_fixed_point : ∀ b : Bool, (!b) ≠ b := by decide

theorem ceiling_on_bool (F : Bool → Bool) (h : ∀ s, F (!s) = !(F s)) :
    ∀ s, (!s) = s → (!(F s)) = F s :=
  equivariant_output_invariant (fun s => !s) (fun r => !r) F h

theorem chain_three_facts :
    (reflState 3).data = [0, 1, 2, 3] ∧ (reflState 3).rel = [(0, 1), (1, 2), (2, 3)] :=
  ⟨reflective_chain_is_initial_segment 3, reflective_chain_successor_relation 3⟩
```

## Line-by-line Lean explanation

**T1, `silent_repetition_inert`.** Induction on the history, with the
start state generalized. The hypothesis says every `admitTok` in the
history names a token already in `s.data`. For the first event: a
`supply` or `marker` is an identity; an `admitTok tok` has `tok ∈ s.data`
by the hypothesis at the head, so the `if` takes its first branch and the
silent mode returns `s`. Then the fold continues from the same `s`, and
the induction hypothesis applies to the tail with the hypothesis
restricted. No horizon: `h` is any list. The book's `silent_inert_here`
applies it to a three-event history with a marker in the middle; the
side condition is discharged by simplifying membership in the concrete
list to `tok = 0`.

**T2, `stepTraced`, `trace_erasure`, `histories_collapse`.** The traced
runner returns a pair: a host-visible result (`isNew` or `existing`) and
the next state. Its state projection equals the silent stepper, event by
event (four cases, two by `rfl`, two by `simp` on the membership test).
So the result stream is never consumed by the state, and two histories
with different result streams (one presentation; two) end in one state.
The book's `traced_results` reads the two results off the probe; its
`histories_collapse_three` extends the collapse to three presentations.
The ledger narrowed this on 2026-08-18: `histories_collapse` is that one
witness pair, not a universal over histories.

**T3, the code quartet.** A retained two-receipt store is modelled by a
pair of constructor codes. `storeSwap` exchanges them. Equal codes are
swap-invariant (`rfl`); distinct codes are not; a singleton algebra
forces equal codes; and `distinction_needs_two_constructors` concludes
from `p.1 ≠ p.2` that two distinct codes occur in `{p.1, p.2}`, which is
its hypothesis restated. The audit records that the last theorem's
docstring ("the distinction was purchased with the result algebra") is
carried by the Python `normal_form_check`, not by this statement. The
lesson therefore teaches T3 as a vocabulary fixture, and does not put it
in the book Lean.

**T4, `JState`, `judgment_carrier_bound`.** The judgment variant appends
a refused token to a separate `judgments` list and never to `data`. The
bound is the same induction as T1 with the same case split as Unit 38's
`nonreify_carrier_bound`, now over a whole history of one token:
`data` stays `[]` or `[0]`. The book's `judgment_bound_three` applies it
to three presentations. Its companion `judgment_variant_second_judgment_not_datum`
reads the probe: `data = [0]`, `judgments = [0, 0]`.

**T5, `stepP` and `stepM`.** `stepP` re-appends the token itself, tags
the new position and links `0` to it: occurrence-style reification plus
tag plus relation. `bridgeState` after two presentations is
`⟨[0, 0], [1], [(0, 1)]⟩` (the book writes it out). `priced_bridge_closes`
reads four facts off it by `decide`; `priced_bridge_oriented` shows the
protocol swap moves it. `stepM` does strictly less: its carrier is a list
of `MItem`, a token or a receipt, and a repeat appends a *receipt* and
links `0` to it; there is no tag field and no result store in `MState`
at all. `min_witnessed_route_closes` reads three facts off `minState`:
the carrier is `[tok 0, receipt 1]`, the relation is `[(0, 1)]`, every
link is off-diagonal. That is *closure* of one declared protocol. The
words "unique minimum" in the paper's FR6 tag belong to the finite
search: the Lean statement contains no other protocol and no cost. The
audit records this as an interpretation defect in the tag, and the paper's
own "computed only within bounds" sentence agrees. The book's
`min_third_presentation` shows what a third presentation does under
`stepM`: a second receipt, linked again to subject `0`, so repeated
refusal under this route makes a star, where reflection (T8) makes a
chain.

**T6, `bridge_facts_not_law`.** The bridge's relation is `[(0, 1)]`,
every link off-diagonal: irreflexive *facts*. The law is still not
entailed: a relation extending those facts can have a self-edge. The
Genesis witness is the constantly true relation, which extends every
list of facts and so does not look at `bridgeState` at all (the audit
calls it correct and trivial; the general form is Unit 26's). The book's
`bridgePlusLoop` is the bridge's facts plus the single self-edge
`(0, 0)`: it extends the facts, breaks the law at `0`, and still denies
`(1, 0)`, so it is a genuine extension of *this* bridge rather than of
everything. The proof: the first conjunct by `Or.inl`; the second by
applying irreflexivity at `0` to the self-edge; the third by cases,
`(1, 0) ∉ [(0, 1)]` after rewriting the state, and `1 ≠ 0`.

**T7, `equivariant_output_invariant`.** Fully general and one `calc`:
if `F` commutes with the two actions and `s` is fixed by `actS`, then
`F s` is fixed by `actR`. Its content in any instance is in identifying
the fixed points. On `Bool` with the swap `!`, there are none
(`not_has_no_fixed_point`), so `ceiling_on_bool` is a true statement with
nothing to apply to in this Boolean instance. The separate tagged bridge
is a particular two-position state moved by `swapP`
(`priced_bridge_oriented`); that does not prove every earlier state or
every relation-route state is moved. The two-element case with content is
`Bridge.equivariant_witness_is_S2`.

**T8, the reflective chain.** `stepRefl` appends the current length as a
new carrier element, tags it, and links the previous element to it.
`reflState 0` is the one-element state `⟨[0], [], []⟩`; no token event
occurs, the start is given. `reflective_chain_growth`: by induction, the
carrier after `n` steps has `n + 1` elements (`List.length_append`, the
induction hypothesis, arithmetic). `reflective_chain_is_initial_segment`:
the carrier *is* `List.range (n + 1)`, using `List.range_succ` to peel the
last element and the growth theorem to identify the appended value.
`reflective_chain_successor_relation` and `reflective_chain_irreflexive_facts`
do the same for the links. The paper says, and the lesson repeats:
*realization, not derivation*. The successor shape is written into
`stepRefl`; what the theorems add is that the realization is exact for
every `n`, not merely to the tested depth. The audit adds a finitude flag:
`reflState : Nat → PState` is a `Nat`-indexed family in the metatheory,
and "one token generates a chain" (the docstring) is a declared
constructor iterated from a given one-element start. The book's
`refl_two` and `chain_three_facts` read depths 2 and 3; `untyped_from_false`
instantiates the one-step fixpoint of the untyped reflection.

**Axioms.** The `decide` theorems on `RState` and `PState` report
`propext, Quot.sound`; on `MState` and for `reflState 2`, where the
derived instance reduces differently, `propext` or none. The general
T7 theorem and the `Bool` facts use no axioms.

## What has been proved

- Silent refusal is inert over any history of already-present tokens
  (Genesis, horizon-free).
- The traced result stream never changes the state; one and two
  presentations erase to one state (Genesis).
- The judgment variant never grows its carrier, over any history of one
  token (Genesis, horizon-free).
- Two presentations of one token close the `stepP` route (carrier 2,
  link `(0, 1)`, off-diagonal, tag `[1]`, not swap-invariant) and the
  `stepM` route (carrier `[tok 0, receipt 1]`, link `(0, 1)`,
  off-diagonal, with no tag and no result store) (Genesis).
- The bridge's positive relation facts have an extension that violates
  irreflexivity, with a constant witness (Genesis) and an extension adding
  one self-edge (book). This is the unrestricted positive-extension
  question of Unit 26, not a prohibition on explicit negative constraints.
- Equivariant constructions preserve fixed points (Genesis, general).
- The declared reflective rule realizes `range (n + 1)` with the successor
  relation for every `n` (Genesis).
- Within the declared class and horizon: the minimum table, the three
  terminal lines, and the normal-form dependencies (computation,
  exhaustive in class).

## What has not been proved

- That the receipt-and-relation route is minimal, or unique, among all
  protocols. It is minimal and unique among the 44 declared ones at
  horizon 6 under the two declared orders. Lean verifies only that it
  closes.
- That the two cost orders are the right ones, or that "import" is well
  defined outside the declared list `Proto.imports`.
- The class-general form of the normal-form dependencies ("no witnessed
  relation without a relation rule" for every protocol whatever): listed
  as unresolved in FR8.
- That any numerals, successor structure or chain are *derived* from
  refusal. FR10 disclaims it; the chain is the content of `stepRefl`.
- Initiality of the chain (whether every realization admits a unique
  structure map from it): frontier conjecture F4, OPEN.
- Anything about the irreflexivity law being reached: it is not, and the
  terminal says so.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| the six-tuple protocol space | the search | declared metatheory, "a search space, not a curated list" |
| `cost_a`, `cost_b` | the minimum table | declared orders |
| horizon 6, carrier cap 4 | every `min_events_to` | declared bounds |
| `Nat × Nat` as a two-receipt store | T3 | metatheory model |
| `s.data.length` as tag, receipt index and link target | T5, T8 | metatheoretic positions admitted as data by each declaration |
| `reflState : Nat → PState` | T8 | a `Nat`-indexed family in the metatheory (finitude flag) |
| `List.range`, `List.range_succ` | T8 | metatheory |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** Under each protocol, exactly what its
declaration lets it hold: one token under the silent and judgment
routes; the token and a receipt, with a link, under the minimum route;
the chain, under reflection. The token contributes one admission, once
(FR11). Everything else is declared.

**Phrases to read with care.**

- "Unique minimum bridge, now also verified in Lean" is two claims. The
  bridge closes: Lean. It is the unique minimum: a search in class.
- "One token generates a chain" means a declared rule, applied `n` times
  to a given one-element state, yields the chain.
- "The dependency theorem" (T3's last member) restates its hypothesis;
  the dependency is the Python `normal_form_check`.
- "Horizon-free" applies to T1, T4 and T8 as stated, and to T2's
  per-event lemma; `histories_collapse` is one pair of histories.

## Student exercise

Under `stepM`, write the state after *three* presentations of token `0`
and say whether it is swap-invariant under the exchange of positions `1`
and `2`. Under `stepRefl` from `reflState 0`, write the state after two
steps and answer the same question. What does the comparison say about
the two routes' relation to orientation?

## Answer

<details>
<summary>Worked answer</summary>

`stepM` three times gives `⟨[tok 0, receipt 1, receipt 2], [(0, 1), (0, 2)]⟩`
(the book's `min_third_presentation`). First specify what the exchange
acts on. As literal `MItem` values, `receipt 1 ≠ receipt 2`: exchanging
the two list entries changes the data list. No general renaming action
on `MState` is defined here, so literal swap-invariance does not follow.

If the observation forgets receipt-number payloads and reads only the
directed links as a set, exchanging vertex names 1 and 2 keeps the star
`{(0,1),(0,2)}`. Both receipts have incoming but no outgoing links. This
coarser relation view does not distinguish them. The book checks the
literal inequality and this declared link observation separately.

`reflState 2` is
`⟨[0, 1, 2], [1, 2], [(0, 1), (1, 2)]⟩` (the book's `refl_two`); the
exchange sends `(0, 1), (1, 2)` to `(0, 2), (2, 1)`, a different relation,
so that exchange does not preserve its directed relation: one is linked from the subject,
the other from a receipt. The minimum route orients subject against
receipt in the two-position example. Its later star has repeated
link profiles, while this chain's link profiles differ. These statements
depend on the declared observation; raw receipt payloads retain more
information. Both constructions are declarations: `stepM` always links from
`0`, `stepRefl` always links from the last element.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/RefusalFrontier.lean` lines 29-47 (T1), 56-84 (T2), 94-116 (T3), 124-162 (T4), 179-252 (T5), 261-264 (T6), 276-282 (T7), 292-370 (T8) |
| Axiom report | `artifacts/lean_axioms.txt` lines 140-159: all within `{propext, Quot.sound}`; `mono_code_swap_invariant`, `distinct_code_not_swap_invariant`, `distinction_needs_two_constructors`, `equivariant_output_invariant`, `untyped_reflect_fixpoint`, `toggle_two_cycle` none |
| Paper | `paper/refusal_as_difference.md` TERMINAL (three lines), FR1 (the space), FR3-FR10 (T1-T8), FR8 (normal form; class-general Lean form unresolved), FR11; ledger `CL-FR6-TERMINAL`, `CL-FR6-T1-INERTIA`, `CL-FR6-T2-TRACE` (narrowed 2026-08-18), `CL-FR6-T3-CONSTRUCTORS` and the other `CL-FR6-T*` entries |
| Python | `code/derivation/refusal_frontier.py`; `artifacts/refusal_frontier.json` (`protocols`, `minimum_table`, `normal_form`, `notion_matrix`); `tests/test_refusal_frontier.py` (`test_witnessed_minimum_unique_under_both_orders`, `test_minimum_table_ties_and_disagreement`, `test_normal_form_holds`) |
| Check (Python) | `python textbook/checks/u39_refusal_frontier.py`: 44 protocols; six named routes' milestones, dynamics and costs; the minimum table under both orders with the witnessed minimum unique and the weaker ties as stated; the normal-form checks; all against the artifact |
| Check (book Lean) | `python textbook/checks/u39_lean.py`: fifteen book theorems plus seven Genesis theorems kernel-checked, Lean 4.33.0 |
