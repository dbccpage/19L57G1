# Unit 63. Where new occurrences come from

**Claim.** The declared internal response fragment leaves the graph stores fixed. The separately supplied attachment block grows those stores under its execution hypotheses.

<details>
<summary>Sources and classification (optional)</summary>

**Status:** FROZEN (the field-invariance theorems, the `nextFamilyP` graph-fixing theorem, the `ProposalRecord` packaging of `upBlock`, the renaming transport theorem, the tie witness on `tri`, and the separation of carrier growth from internal obstruction); ADMITTED (the predicates `MentionsOnlyExisting`, `IsInternal`, `IsResponseEvent`, `GraphStoresFixed`, and the structure `ProposalRecord` with its unconstrained `.cost : Nat` field); VERIFIED_FINITE (`artifacts/graph_genesis.json`); NOT CLAIMED (a carrier-growth restriction on every differently declared response family). A separately supplied admission can grow the carrier; it lies outside `IsResponseEvent`.
**Lean:** `lean4/Derivation/GraphGenesis.lean` lines 59–720.
**Axioms:** `propext`, `Quot.sound` on 26 of 28 public theorem reports; `none` on `GraphGenesis.IsInternal_exact` and `GraphGenesis.internal_is_response` (`artifacts/lean_axioms.txt` lines 793–820).
**Depends on:** Unit 54 (`PrimitivePassage.PState`, `PEvent`, `step`, `replayP`, `obstP`, `sepP`, `nextFamilyP`, `extensionProposals`, `repairFamily`, `nextFamilyP_nonempty`, `extension_always_available`, `extension_resolves`, `obst_requires_observation`), Unit 55 (`HigherStructure.pstep_budget`), Unit 59 (`Attachment.upFamily`, `upBlock`, `up_iff_legal`, `up_executes`, `halted_up_inert`, `act_up_comm`, `treeAt`, `WFStores`).

---

</details>

## First pass

Use [Unit 59](59_growing_the_carrier_by_one_and_renaming_the_supply.md)
for the attachment recipe.

Begin with occurrences `[0, 1]`, the pair `(0, 1)` retained and protected,
and a declared observation with no columns. The required distinction is
missing. Two supplied continuations do different jobs:

| Continuation | Occurrences afterward | Observation columns afterward |
|---|---|---|
| Fund one update, add column `[0]` | `[0, 1]` | `[[0]]` |
| Attach one fresh occurrence at parent 0 | `[0, 1, 2]` | `[]` |

The first separates 0 from 1 without growing the carrier. The second
grows it while leaving the view unchanged. Here **carrier growth** means
adding an occurrence to the represented list, with a new position for it.
No physical space is inferred from that representation. The internal response family supplies observation repairs; the
attachment block is a separate supplied recipe.

**Predict.** Does executing the attachment alone make the original
pair visible as different?

<details>
<summary>Check your prediction</summary>

No. Its observation still has no columns. Growth and resolving this
observation demand are different changes. Recording either recipe as a
proposal also does not execute it or grant permission.

</details>

<details>
<summary>Detailed statement and formal anchors (optional)</summary>

## Detailed claim and formal anchors

On the nine-field primitive-passage ledger `PState`, every block emitted by the internal controller `nextFamilyP` is either a single same-level repair `[.refineCol v p]` or a funded column creation `[.setBudget 1, .addCol c]` whose newly mentioned positions lie strictly below `s.occ.length`, and replaying any finite trace over the internal fragment `IsInternal` (or over `IsResponseEvent`) leaves the four graph stores (`occ`, `asserted`, `wit`, `prot`) untouched; by contrast, the attached-continuation block `Attachment.upBlock s p` grows `occ`, `asserted`, `wit`, and `prot` by one entry each when replayed from a live store-bounded state with `p < s.occ.length`, packaged as an inert `ProposalRecord` whose family transports under renaming, retains equal-cost non-isomorphic branches on `tri`, and whose carrier-growth demand is not forced by internal pair obstruction (`GraphGenesis.graph_growth_is_supplied`, `GraphGenesis.nextFamilyP_block_fixes_graph`, `GraphGenesis.internal_family_cannot_grow_carrier`, `GraphGenesis.proposal_confers_no_execution`, `GraphGenesis.upProposal_executes`, `GraphGenesis.proposal_transports`, `GraphGenesis.proposal_family_retains_ties`, `GraphGenesis.obstruction_resolved_in_carrier`, `GraphGenesis.family_never_grows_carrier`, `GraphGenesis.growth_demand_not_obstruction_consequence`).

</details>

## Question

Unit 54 gave the nine-field primitive-passage ledger `PState` and its internal response family `nextFamilyP : PState → List (List PEvent)`, while Unit 59 gave the attached-continuation block `Attachment.upBlock s p : List PEvent` that admits one fresh occurrence `freshTok s` attached to an existing parent position `p < s.occ.length`. Can the internal controller `nextFamilyP`—or any finite trace over the internal observation-and-refusal fragment—ever admit a new occurrence, a new asserted pair, a new retained pair, or a new protected pair on its own? When `upBlock s p` is packaged as a typed proposal record before execution, does holding that record confer any license or execution on the ledger, does one parent win when several parents are legal, and does an active pair obstruction (`obstP s i j = true`) ever require growing the occurrence carrier `s.occ`?

---

## What we already possess

From Unit 54 (`lean4/Derivation/PrimitivePassage.lean`), we have the nine-field ledger `PState` with fields:

- four graph stores: `occ : List Nat`, `asserted : List (Nat × Nat)`, `wit : List (Nat × Nat)`, and `prot : List (Nat × Nat)`;
- two observer/refusal stores: `obs : Option (List (List Nat))` and `refusals : List (Nat × Nat)`;
- three control fields: `budget : Nat`, `licensed : Bool`, and `halted : Bool`.

We also have the eleven-constructor event grammar `PEvent` (`admitOcc`, `assertWit`, `admitWit`, `protect`, `declareObs`, `refineCol`, `addCol`, `refuse`, `setBudget`, `setLicense`, `halt`), the transition function `step : PState → PEvent → PState`, left-to-right replay `replayP : List PEvent → PState → PState`, pair separation `sepP`, pair obstruction `obstP`, the same-level repair list `repairFamily s i j`, the created-column list `extensionProposals s i j`, and the represented response family `nextFamilyP s`.

From Unit 55 (`lean4/Derivation/HigherStructure.lean`), we have `HigherStructure.pstep_budget : s.halted = false → step s (.setBudget n) = { s with budget := n }`.

From Unit 59 (`lean4/Derivation/Attachment.lean`), we have the four-event block `upBlock s p`, the complete one-edge family `upFamily s`, the store-bound predicate `WFStores s`, the legality equivalence `up_iff_legal`, the execution theorems `up_executes` and `up_exec_eq`, the halted inertia theorem `halted_up_inert`, the renaming commutation theorem `act_up_comm`, the canonical rooted tree chain `treeAt pathPolL n`, and the non-isomorphic branch theorem `equal_cost_non_isomorphic_extensions`.

Notice what is **not** imported here: `GraphGenesis.lean` imports `Derivation.Attachment` (and through it `HigherStructure`, `PrimitivePassage`, `PrimDiff`, and `PrimitiveCore`), and does not import `Derivation.Basic`. Nothing in this unit touches `Basic.Regime`, `Basic.Event`, or `Basic.replayE`; the word "graph" in `GraphGenesis` refers strictly to the four stores `(s.occ, s.asserted, s.wit, s.prot)` of `PState`.

---

## New concept: the internal/supply partition, `ProposalRecord`, and carrier-growth independence

`GraphGenesis` organizes its results into three parts corresponding to three structural questions about `PState`:

1. **Part 1 — Where new occurrences come from (internal vs. response vs. supply events).**
   - `MentionsOnlyExisting s e` checks that the newly added point `p` of `.refineCol v p` and every point `x ∈ c` of `.addCol c` satisfy `p < s.occ.length` and `x < s.occ.length` (`True` for all other constructors).
   - `IsInternal : PEvent → Bool` returns `true` on the four observation-and-refusal constructors `.refineCol`, `.addCol`, `.declareObs`, `.refuse`, and `false` on the four graph-supply constructors (`.admitOcc`, `.assertWit`, `.admitWit`, `.protect`) and the three control constructors (`.setBudget`, `.setLicense`, `.halt`).
   - `IsResponseEvent : PEvent → Bool` extends `IsInternal` by adding `.setBudget`, which `nextFamilyP` prefixes to each created column (`internal_is_response : IsInternal e = true → IsResponseEvent e = true`).
   - `GraphStoresFixed s t` states that `t.occ = s.occ ∧ t.asserted = s.asserted ∧ t.wit = s.wit ∧ t.prot = s.prot`.
   - `graph_growth_is_supplied` combines the negative statement (every block `b ∈ nextFamilyP s` preserves all four graph stores) with the positive statement (under `WFStores s`, `s.halted = false`, and `p < s.occ.length`, replaying `Attachment.upBlock s p` increases `.occ.length`, `.asserted.length`, `.wit.length`, and `.prot.length` by `1`).

2. **Part 2 — `ProposalRecord`: packaging `upBlock` as an inert record.**
   - `ProposalRecord (s : PState)` is a seventeen-field dependent structure holding `block : List PEvent`, `block_complete : block ∈ upFamily s`, `embed : Nat → Nat`, `retract : Nat → Nat`, `retract_embed : ∀ x, x < s.occ.length → retract (embed x) = x`, `token_fresh`, `preserves_asserted`, `preserves_wit`, `preserves_prot`, `preserves_separated`, `newPair : Nat × Nat`, `parentPos : Nat`, `freshPos : Nat`, `newPair_provenance : newPair = (parentPos, freshPos)`, `parent_represented : parentPos < s.occ.length`, `freshPos_is_new : freshPos = s.occ.length`, and `cost : Nat`.
   - `ProposalRecord` has no license, execution, or activation field. In addition, `proposal_confers_no_execution` shows that on a halted ledger (`s.halted = true`), replaying `P.block` returns `s`.
   - `upProposal s hwf hh p hp` constructs the canonical `ProposalRecord s` for a legal parent `p < s.occ.length` under `WFStores s` and `s.halted = false`, with `embed := fun x => x`, `retract := fun x => x`, `newPair := (p, s.occ.length)`, and `cost := (upBlock s p).length` (`4`).
   - `proposal_transports` lifts `Attachment.act_up_comm` to `ProposalRecord s`.
   - On the three-occurrence oriented path `tri := treeAt pathPolL 2`, `triProp1` (attaching at parent `1`) and `triProp2` (attaching at parent `2`) both have `.cost = 4`, both belong to `upFamily tri`, and their resulting `.wit` graphs are not carried onto each other by any 4-point bijection (`proposal_family_retains_ties`).

3. **Part 3 — Carrier growth is not forced by internal pair obstruction.**
   - Under `obstP s i j = true`, `i ≠ j`, `i < s.occ.length`, `(i, j) ∈ s.prot`, `s.licensed = true`, and `s.halted = false`, `obstruction_resolved_in_carrier` establishes that `[.setBudget 1, .addCol [i]] ∈ nextFamilyP s`, replaying it clears `obstP ... i j` to `false`, and `GraphStoresFixed s (replayP [.setBudget 1, .addCol [i]] s)` holds.
   - `FamilyGrowsCarrier s := ∃ b ∈ nextFamilyP s, s.occ.length < (replayP b s).occ.length` is refuted for every `s : PState` (`family_never_grows_carrier : ¬ FamilyGrowsCarrier s`).
   - On the explicit two-occurrence ledger `blindPair` (`occ = [0, 1]`, `asserted = wit = prot = [(0, 1)]`, `obs = some []`, `budget = 0`, `licensed = true`, `halted = false`), `growth_demand_not_obstruction_consequence` establishes that `obstP blindPair 0 1 = true`, `nextFamilyP blindPair` has two funded blocks `[[.setBudget 1, .addCol [0]], [.setBudget 1, .addCol [1]]]`, every block in `nextFamilyP blindPair` resolves `obstP` to `false` while fixing all four graph stores, and `∀ s, ¬ FamilyGrowsCarrier s`.

---

## Plain-language interpretation

Think of the ledger `PState` as having four columns that record the objects in the room and their declared links (`occ`, `asserted`, `wit`, `prot`), alongside two columns that record how the room currently groups those objects into observation buckets or logs refusals (`obs`, `refusals`) and three control switches (`budget`, `licensed`, `halted`).

When a protected pair `(i, j)` is not yet separated by any observation column in `obs`, the internal controller `nextFamilyP` proposes blocks of events to resolve the obstruction. Every block it proposes is either a single column refinement `[.refineCol v p]` or a funded column creation `[.setBudget 1, .addCol c]`. Neither `.refineCol`, `.addCol`, `.declareObs`, `.refuse`, nor `.setBudget` ever writes to the four object-and-link columns (`occ`, `asserted`, `wit`, `prot`), and every position `p` or `x ∈ c` that `nextFamilyP` adds was already below `s.occ.length` before the block ran. Consequently, running the internal controller can reorganize `obs` and adjust `budget`, but it can never bring a new occurrence into `s.occ` or add a new link to `asserted`, `wit`, or `prot`.

New occurrences and new links can enter only through the four supply events `.admitOcc`, `.assertWit`, `.admitWit`, and `.protect`, such as the four-event package `upBlock s p` from Unit 59. Packaging `upBlock s p` into a `ProposalRecord s` writes down the four-event block, its membership proof in `upFamily s`, the identity embedding and retraction, the freshness and preservation proofs, the provenance `(p, s.occ.length)`, and the declared cost `4`. This value belongs to the canonical constructor; the general record type does not require `cost = block.length`. Changing only that field preserves the other obligations (`proposal_cost_is_declared` in the book). Holding that record does not execute the block, and when two parents `p = 1` and `p = 2` are both legal (as on `tri`), their two proposal records tie at cost `4` while producing non-isomorphic link graphs (a 4-vertex path vs. a 3-leaf star) when executed.

---

## Pseudocode

```text
PARTITION(e : PEvent):
  IsInternal(e)      := e in { refineCol(_, _), addCol(_), declareObs, refuse(_, _) }
  IsResponseEvent(e) := IsInternal(e) or e == setBudget(_)
  IsSupply(e)        := e in { admitOcc(_), assertWit(_, _), admitWit(_, _), protect(_, _) }

CHECK_NEXT_FAMILY_BLOCKS(s : PState):
  for each b in nextFamilyP(s):
    -- b is either [refineCol v p] or [setBudget 1, addCol c]
    assert all e in b satisfy IsResponseEvent(e) and MentionsOnlyExisting(s, e)
    t := replayP(b, s)
    assert (t.occ, t.asserted, t.wit, t.prot) == (s.occ, s.asserted, s.wit, s.prot)

BUILD_UP_PROPOSAL(s : PState, p : Nat) requires WFStores(s), not s.halted, p < len(s.occ):
  return ProposalRecord(
    block      = upBlock(s, p),
    embed      = (x -> x),
    retract    = (x -> x),
    newPair    = (p, len(s.occ)),
    parentPos  = p,
    freshPos   = len(s.occ),
    cost       = len(upBlock(s, p))   -- 4
  )
```

---

## Python

From `code/derivation/graph_genesis.py` (lines 75–122, 318–338, 376–420):

```python
STATE_FIELDS: tuple[str, ...] = (
    "occ", "asserted", "wit", "prot", "obs", "budget", "licensed",
    "refusals", "halted")

GRAPH_FIELDS: tuple[str, ...] = ("occ", "asserted", "wit", "prot")

OBSERVATION_FIELDS: tuple[str, ...] = ("obs", "budget")

INTERNAL_KINDS: tuple[str, ...] = (
    "refineCol", "addCol", "declareObs", "refuse")

FUNDING_KINDS: tuple[str, ...] = ("setBudget",)

SUPPLY_KINDS: tuple[str, ...] = (
    "admitOcc", "assertWit", "admitWit", "protect")

CONTROL_KINDS: tuple[str, ...] = ("setBudget", "setLicense", "halt")


def is_internal(e: PEvent) -> bool:
    """True exactly on the internal fragment (Lean ``IsInternal``)."""
    return kind(e) in INTERNAL_KINDS


def is_funding(e: PEvent) -> bool:
    return kind(e) in FUNDING_KINDS


def is_response_event(e: PEvent) -> bool:
    """The internal fragment plus the funding event the represented
    family prefixes to a created column (Lean ``IsResponseEvent``)."""
    return is_internal(e) or is_funding(e)


def graph_stores_fixed(s: PS, t: PS) -> bool:
    """Lean ``GraphStoresFixed``: the four graph stores agree."""
    return all(getattr(s, f) == getattr(t, f) for f in GRAPH_FIELDS)


def mentions_only_existing(s: PS, e: PEvent) -> bool:
    """Lean ``MentionsOnlyExisting``: the point a refinement adds and
    every point of a created column is already represented."""
    if kind(e) == "refineCol":
        return int_arg(e, 2) < len(s.occ)
    if kind(e) == "addCol":
        return all(x < len(s.occ) for x in col_arg(e, 1))
    return True


@dataclass(frozen=True)
class ProposalRecord:
    block: tuple[PEvent, ...]
    embed: tuple[int, ...]
    retract: tuple[int, ...]
    new_pair: Pair
    parent_pos: int
    fresh_pos: int
    cost: int


def up_proposal(s: PS, p: int) -> ProposalRecord:
    n = len(s.occ)
    block = tuple(up_block(s, p))
    return ProposalRecord(block=block, embed=tuple(range(n)),
                          retract=tuple(range(n + 1)),
                          new_pair=(p, n), parent_pos=p, fresh_pos=n,
                          cost=len(block))
```

---

## Line-by-line Python explanation

- **`GRAPH_FIELDS`, `INTERNAL_KINDS`, `FUNDING_KINDS`, `SUPPLY_KINDS`, `CONTROL_KINDS` (lines 79–92):** Names the four graph stores (`occ`, `asserted`, `wit`, `prot`) and splits the 11 `PEvent` kinds into 4 supply kinds (`admitOcc`, `assertWit`, `admitWit`, `protect`), 4 internal kinds (`refineCol`, `addCol`, `declareObs`, `refuse`), and 3 control kinds (`setBudget`, `setLicense`, `halt`).
- **`is_internal`, `is_funding`, `is_response_event` (lines 109–121):** Mirrors Lean's `IsInternal` and `IsResponseEvent` (`IsInternal` union `setBudget`).
- **`graph_stores_fixed(s, t)` (lines 232–234):** Checks that `occ`, `asserted`, `wit`, and `prot` match between `s` and `t`.
- **`mentions_only_existing(s, e)` (lines 318–325):** Checks `p < len(s.occ)` on `("refineCol", v, p)` and `all(x < len(s.occ) for x in c)` on `("addCol", c)`.
- **`ProposalRecord` and `up_proposal(s, p)` (lines 376–420):** Mirrors Lean's `ProposalRecord` data fields, setting `block = tuple(up_block(s, p))`, `embed = tuple(range(n))`, `retract = tuple(range(n + 1))`, `new_pair = (p, n)`, `parent_pos = p`, `fresh_pos = n`, and `cost = len(block)` (`4`). `carries_no_authority()` (lines 402–407) checks that no field name contains `"licen"`, `"execut"`, `"activ"`, `"authorit"`, `"budget"`, or `"gate"`.

---

## Lean 4

From `lean4/Derivation/GraphGenesis.lean` (selected declarations and theorems across Parts 1–3, lines 59–720):

```lean
namespace GraphGenesis

open PrimitivePassage Attachment

def MentionsOnlyExisting (s : PState) : PEvent → Prop
  | .refineCol _ p => p < s.occ.length
  | .addCol c => ∀ x ∈ c, x < s.occ.length
  | _ => True

def IsInternal : PEvent → Bool
  | .refineCol _ _ => true
  | .addCol _ => true
  | .declareObs => true
  | .refuse _ _ => true
  | .admitOcc _ => false
  | .assertWit _ _ => false
  | .admitWit _ _ => false
  | .protect _ _ => false
  | .setBudget _ => false
  | .setLicense _ => false
  | .halt => false

def IsResponseEvent : PEvent → Bool
  | .refineCol _ _ => true
  | .addCol _ => true
  | .declareObs => true
  | .refuse _ _ => true
  | .setBudget _ => true
  | .admitOcc _ => false
  | .assertWit _ _ => false
  | .admitWit _ _ => false
  | .protect _ _ => false
  | .setLicense _ => false
  | .halt => false

def GraphStoresFixed (s t : PState) : Prop :=
  t.occ = s.occ ∧ t.asserted = s.asserted ∧ t.wit = s.wit
    ∧ t.prot = s.prot

theorem internal_family_cannot_grow_carrier (h : List PEvent)
    (s : PState) (hint : ∀ e ∈ h, IsInternal e = true) :
    GraphStoresFixed s (replayP h s) :=
  replay_fixes_graph_of_all IsInternal internal_step_fixes_graph h s
    hint

theorem nextFamilyP_block_fixes_graph (s : PState) (b : List PEvent)
    (hb : b ∈ nextFamilyP s) : GraphStoresFixed s (replayP b s) :=
  response_replay_fixes_graph b s
    (nextFamilyP_blocks_are_responses s b hb)

theorem graph_growth_is_supplied (s : PState) (hwf : WFStores s)
    (hh : s.halted = false) (p : Nat) (hp : p < s.occ.length) :
    (∀ b ∈ nextFamilyP s, GraphStoresFixed s (replayP b s)) ∧
    (replayP (upBlock s p) s).occ.length = s.occ.length + 1 ∧
    (replayP (upBlock s p) s).asserted.length = s.asserted.length + 1 ∧
    (replayP (upBlock s p) s).wit.length = s.wit.length + 1 ∧
    (replayP (upBlock s p) s).prot.length = s.prot.length + 1 := by
  obtain ⟨e1, e2, e3, e4, _⟩ := up_executes s hwf hh p hp
  exact ⟨fun b hb => nextFamilyP_block_fixes_graph s b hb,
    e1, e2, e3, e4⟩

structure ProposalRecord (s : PState) where
  block : List PEvent
  block_complete : block ∈ upFamily s
  embed : Nat → Nat
  retract : Nat → Nat
  retract_embed : ∀ x, x < s.occ.length → retract (embed x) = x
  token_fresh : ∀ t : Nat, (PEvent.admitOcc t) ∈ block → ¬ (t ∈ s.occ)
  preserves_asserted : ∀ pr ∈ s.asserted,
    (embed pr.1, embed pr.2) ∈ (replayP block s).asserted
  preserves_wit : ∀ pr ∈ s.wit,
    (embed pr.1, embed pr.2) ∈ (replayP block s).wit
  preserves_prot : ∀ pr ∈ s.prot,
    (embed pr.1, embed pr.2) ∈ (replayP block s).prot
  preserves_separated : ∀ cols, s.obs = some cols →
    ∀ cols', (replayP block s).obs = some cols' →
      ∀ i j, sepP cols i j = true →
        sepP cols' (embed i) (embed j) = true
  newPair : Nat × Nat
  parentPos : Nat
  freshPos : Nat
  newPair_provenance : newPair = (parentPos, freshPos)
  parent_represented : parentPos < s.occ.length
  freshPos_is_new : freshPos = s.occ.length
  cost : Nat

theorem proposal_confers_no_execution (s : PState)
    (P : ProposalRecord s) (h : s.halted = true) :
    replayP P.block s = s := by
  obtain ⟨p, _, heq⟩ := (up_iff_legal s P.block).mp P.block_complete
  rw [heq]
  exact halted_up_inert s h p

theorem proposal_family_retains_ties :
    triProp1.cost = triProp2.cost ∧
    triProp1.block ≠ triProp2.block ∧
    triProp1.block ∈ upFamily tri ∧
    triProp2.block ∈ upFamily tri ∧
    (tuples4.all fun t => !(isoMatch t
        (replayP triProp1.block tri).wit
        (replayP triProp2.block tri).wit)) = true

theorem obstruction_resolved_in_carrier (s : PState) (i j : Nat)
    (hobst : obstP s i j = true) (hij : i ≠ j)
    (hi : i < s.occ.length) (hprot : (i, j) ∈ s.prot)
    (hlic : s.licensed = true) (hh : s.halted = false) :
    [PEvent.setBudget 1, PEvent.addCol [i]] ∈ nextFamilyP s ∧
    obstP (replayP [PEvent.setBudget 1, PEvent.addCol [i]] s) i j
      = false ∧
    GraphStoresFixed s
      (replayP [PEvent.setBudget 1, PEvent.addCol [i]] s)

def FamilyGrowsCarrier (s : PState) : Prop :=
  ∃ b ∈ nextFamilyP s, s.occ.length < (replayP b s).occ.length

theorem family_never_grows_carrier (s : PState) :
    ¬ FamilyGrowsCarrier s

theorem growth_demand_not_obstruction_consequence :
    obstP blindPair 0 1 = true ∧
    nextFamilyP blindPair
      = [[PEvent.setBudget 1, PEvent.addCol [0]],
         [PEvent.setBudget 1, PEvent.addCol [1]]] ∧
    (∀ b ∈ nextFamilyP blindPair,
      obstP (replayP b blindPair) 0 1 = false) ∧
    (∀ b ∈ nextFamilyP blindPair,
      GraphStoresFixed blindPair (replayP b blindPair)) ∧
    (∀ s : PState, ¬ FamilyGrowsCarrier s)
```

---

## Line-by-line Lean explanation

1. **Observer-only effects and existing-position bounds (lines 59–183):**
   - `refineCol_only_obs` (line 59) and `addCol_only_obs` (line 75) unfold `step` on `.refineCol v p` and `.addCol c` to show that the seven fields `occ`, `asserted`, `wit`, `prot`, `refusals`, `licensed`, and `halted` are unchanged (`obs` and `budget` are the only two fields omitted from the conjunction).
   - `extensionProposals_range_over_existing` (line 99) unpacks `List.mem_filter`, `List.mem_map`, and `List.mem_range` to prove `∀ c ∈ extensionProposals s i j, ∀ x ∈ c, x < s.occ.length`.
   - `repairFamily_range_over_existing` (line 116) unpacks `responseMenu` to prove `∀ m ∈ repairFamily s i j, m.2 < s.occ.length`.
   - `MentionsOnlyExisting` (line 137), `nextFamilyP_block_shape` (line 146), and `nextFamilyP_range_over_existing` (line 165) show that every block `b ∈ nextFamilyP s` is either `[.refineCol m.1 m.2]` or `[.setBudget 1, .addCol c]`, and every event inside `b` satisfies `MentionsOnlyExisting s e`.

2. **Internal vs. response events and fixed graph stores (lines 190–350):**
   - `IsInternal` (line 190) and `IsInternal_exact` (line 204) classify `.refineCol`, `.addCol`, `.declareObs`, `.refuse`; `IsResponseEvent` (line 224) and `internal_is_response` (line 237) adjoin `.setBudget`.
   - `GraphStoresFixed` (line 244), `response_step_fixes_graph` (line 250), and `internal_step_fixes_graph` (line 259) show that any `IsResponseEvent` (and hence any `IsInternal` event) leaves `occ`, `asserted`, `wit`, and `prot` unchanged.
   - `replay_fixes_graph_of_all` (line 264) inducts on `h : List PEvent` to yield `internal_family_cannot_grow_carrier` (line 283), `response_replay_fixes_graph` (line 291), `nextFamilyP_blocks_are_responses` (line 299), `nextFamilyP_block_fixes_graph` (line 317), and `graph_growth_is_supplied` (line 340).

3. **Proposal records, renaming transport, and tie retention (lines 381–591):**
   - `ProposalRecord` (line 381) packages `block ∈ upFamily s`, `embed`, `retract`, freshness and preservation proofs, `newPair = (parentPos, freshPos)`, and `cost : Nat`.
   - `proposal_confers_no_execution` (line 441) uses `up_iff_legal` to write `P.block = upBlock s p` and applies `halted_up_inert` when `s.halted = true`.
   - `upProposal` (line 452) and `upProposal_executes` (line 507) discharge all 17 fields for `upBlock s p` using `up_exec_eq` and `up_executes`.
   - `proposal_transports` (line 533) combines `up_iff_legal`, `upFamily_transport`, and `act_up_comm` to show that any `ProposalRecord s` commutes with a carrier renaming `σ : Renaming n` (`n = s.occ.length`).
   - `tri := treeAt pathPolL 2` (line 552) has `triProp1` (parent `1`) and `triProp2` (parent `2`); `proposal_family_retains_ties` (line 576) shows `triProp1.cost = triProp2.cost` (`4 = 4`), `triProp1.block ≠ triProp2.block`, both blocks belong to `upFamily tri`, and `tuples4.all` confirms no 4-tuple bijection carries `(replayP triProp1.block tri).wit` onto `(replayP triProp2.block tri).wit`.

4. **Demand separation: internal obstruction vs. carrier growth (lines 606–720):**
   - `funded` (line 606) sets `budget := 1`.
   - `obstruction_resolved_in_carrier` (line 614) uses `nextFamilyP_nonempty`, `HigherStructure.pstep_budget`, `extension_always_available`, `obst_requires_observation`, and `extension_resolves` to prove that `[.setBudget 1, .addCol [i]] ∈ nextFamilyP s` resolves `obstP` on `(i, j)` while fixing all four graph stores.
   - `FamilyGrowsCarrier` (line 651) and `family_never_grows_carrier` (line 655) show `¬ ∃ b ∈ nextFamilyP s, s.occ.length < (replayP b s).occ.length`.
   - `blindPair` (line 666), `growth_demand_not_obstruction_consequence` (line 693), and `blindPair_resolution_keeps_carrier` (line 711) check the concrete witness by `decide`.

---

## What has been proved

- **Exact internal and response event classifications (`IsInternal_exact`, `internal_is_response`):** `IsInternal` holds on `.refineCol`, `.addCol`, `.declareObs`, `.refuse` and is `false` on the other 7 constructors; `IsResponseEvent` adds `.setBudget`.
- **`nextFamilyP` emits only response blocks over represented positions (`nextFamilyP_block_shape`, `nextFamilyP_range_over_existing`, `nextFamilyP_blocks_are_responses`):** Every block in `nextFamilyP s` is either `[.refineCol v p]` (`p < s.occ.length`) or `[.setBudget 1, .addCol c]` (`∀ x ∈ c, x < s.occ.length`).
- **Internal and response traces fix the four graph stores (`internal_family_cannot_grow_carrier`, `response_replay_fixes_graph`, `nextFamilyP_block_fixes_graph`, `graph_growth_is_supplied`):** Replaying any trace of `IsResponseEvent` (or `IsInternal`) events fixes `occ`, `asserted`, `wit`, and `prot`, whereas `upBlock s p` grows all four lengths by `1` on a live `WFStores s` state with `p < s.occ.length`.
- **Inert proposal packaging, renaming transport, and tie retention (`proposal_confers_no_execution`, `upProposal_executes`, `proposal_transports`, `proposal_family_retains_ties`):** `upProposal` discharges all `ProposalRecord` obligations, is inert when `s.halted = true`, commutes with `Renaming n`, and retains tied cost-`4` non-isomorphic branches (`triProp1` vs. `triProp2`) on `tri`.
- **Internal obstruction resolves inside the current carrier (`obstruction_resolved_in_carrier`, `family_never_grows_carrier`, `growth_demand_not_obstruction_consequence`, `blindPair_resolution_keeps_carrier`):** Every active protected obstruction `(i, j)` with `i ≠ j` and `i < s.occ.length` on a live licensed state is resolved inside `s.occ` by `[.setBudget 1, .addCol [i]] ∈ nextFamilyP s`.

---

## What has not been proved

- **No link to `Basic.lean` (`Regime`, `Event`, `replayE`):** `GraphGenesis.lean` works exclusively on `PrimitivePassage.PState` and `PEvent`.
- **`obs` and `budget` movement is not asserted by `refineCol_only_obs` or `addCol_only_obs`:** Those theorems prove that the other seven fields do not move; whether `obs` and `budget` actually change on a step depends on whether the step's guard succeeds.
- **Points already inside a refined column:** `repairFamily_range_over_existing` establishes `m.2 < s.occ.length` for the newly added point `m.2`, without asserting a bound on points already stored in the column `m.1`.
- **No classification of every differently declared family:** The negative theorems cover `nextFamilyP` and traces over `IsInternal` / `IsResponseEvent`. A separately declared block `[.admitOcc 7]` grows the empty occurrence list; it lies outside `IsResponseEvent` (`separately_declared_supply_grows` in the book). Thus the unqualified existence of a different growing family is not an open result. A new response grammar would require its own definitions and scope checks. The fixed-family theorem supplies no general prohibition on it.
- **`ProposalRecord` fields and `.cost` are admitted, not canonical:** `ProposalRecord.cost : Nat` has no constraint inside the structure declaration (`upProposal` sets `cost := (upBlock s p).length = 4`), and `ProposalRecord` is presented as one sufficient schema without any minimality or uniqueness claim.
- **Hypotheses of `obstruction_resolved_in_carrier`:** In-carrier resolution requires `i ≠ j`, `i < s.occ.length`, `(i, j) ∈ s.prot`, `s.licensed = true`, and `s.halted = false`.

---

## Outside the system

1. **Metatheory types and quantifiers:**
   - Lean's `Nat`, `Bool`, `List`, `Option`, `Prop`, quantifiers (`∀ s b`, `∀ h : List PEvent`), and total function types `Nat → Nat` in `ProposalRecord.embed` and `ProposalRecord.retract` belong to the declared metatheory (Unit 00).
2. **What the system itself holds:**
   - At any state `s : PState`, the ledger holds nine finite fields (`occ`, `asserted`, `wit`, `prot`, `obs`, `budget`, `licensed`, `refusals`, `halted`), and `nextFamilyP s` or `upFamily s` is a finite list of finite event blocks.
3. **Admissions and their prices:**
   - `MentionsOnlyExisting`, `IsInternal`, `IsResponseEvent`, `GraphStoresFixed`, and `ProposalRecord` (including its unconstrained `.cost : Nat` field) are admitted definitions in `GraphGenesis.lean`.
   - Clearing an internal obstruction via `[.setBudget 1, .addCol [i]]` uses `.setBudget 1` (one funding event) and requires `s.licensed = true`.
4. **Phrases to read without importing an outside agent or container:**
   - Calling `admitOcc`, `assertWit`, `admitWit`, and `protect` "supplied" means `IsResponseEvent e = false` and `e ∉ b` for every `b ∈ nextFamilyP s`; it does not posit an external agent object inside Lean.
   - Saying "`ProposalRecord` carries no authority" means `ProposalRecord` declares no license, execution, or activation field and `proposal_confers_no_execution` holds on halted states.

---

## Student exercise

Consider the concrete witness state `blindPair` (`occ = [0, 1]`, `asserted = [(0, 1)]`, `wit = [(0, 1)]`, `prot = [(0, 1)]`, `obs = some []`, `budget = 0`, `licensed = true`, `refusals = []`, `halted = false`).

1. Verify that all four obstruction conditions hold for `(0, 1)` at `blindPair` (`obstP blindPair 0 1 = true`).
2. List the blocks in `nextFamilyP blindPair`. For the first block `b₀ = [.setBudget 1, .addCol [0]]`, compute `(replayP b₀ blindPair).occ`, `(replayP b₀ blindPair).obs`, and `obstP (replayP b₀ blindPair) 0 1`.
3. Compare `replayP b₀ blindPair` with `replayP (upBlock blindPair 0) blindPair`. Which stores change in each case?

---

<details>
<summary>Student exercise answer</summary>

1. **Four obstruction conditions at `blindPair`:**
   - `(0, 1) ∈ blindPair.wit` is `true`, `(0, 1) ∈ blindPair.prot` is `true`, `blindPair.obs = some []` is declared, and `sepP [] 0 1 = false`. Hence `obstP blindPair 0 1 = true`.
2. **Blocks in `nextFamilyP blindPair` and replay of `b₀`:**
   - Since `blindPair.obs = some []`, there are no existing columns to refine (`repairFamily blindPair 0 1 = []`), and `extensionProposals blindPair 0 1 = [[0], [1]]`.
   - Thus `nextFamilyP blindPair = [[.setBudget 1, .addCol [0]], [.setBudget 1, .addCol [1]]]`.
   - Replaying `b₀ = [.setBudget 1, .addCol [0]]` sets `budget` to `1` and then appends column `[0]` while spending `1` budget, giving `(replayP b₀ blindPair).occ = [0, 1]`, `(replayP b₀ blindPair).obs = some [[0]]`, and `obstP (replayP b₀ blindPair) 0 1 = false` (`blindPair_resolution_keeps_carrier`). All four graph stores (`occ`, `asserted`, `wit`, `prot`) are unchanged.
3. **Comparison with `upBlock blindPair 0`:**
   - Replaying `b₀` changes only `obs` (from `some []` to `some [[0]]`) and keeps `occ = [0, 1]`.
   - Replaying `upBlock blindPair 0` leaves `obs = some []` and `budget = 0` untouched, while growing `occ` from `[0, 1]` to `[0, 1, 2]` and appending `(0, 2)` to `asserted`, `wit`, and `prot`.

---

</details>

## Verification

| Check | Source |
|---|---|
| Lean | `lean4/Derivation/GraphGenesis.lean` lines 59–720 (`lake build Derivation.GraphGenesis`) |
| Axiom report | `artifacts/lean_axioms.txt` lines 793–820 (26 `[propext, Quot.sound]`, 2 `none`) |
| Paper | `paper/paper_claim_ledger.md` `CL-PD2-GRAPH-GENESIS` (Goal 5); `paper/paper_change_log.md` line 833 |
| Python | `code/derivation/graph_genesis.py`, `code/run_graph_genesis.py`, `tests/test_graph_genesis.py`, `artifacts/graph_genesis.json` |
| Audit | `textbook/audit/modules/GraphGenesis.md` (zero semantic gaps; scope notes on `ProposalRecord.cost` and `obstruction_resolved_in_carrier` recorded above) |
| Check (Python) | `python textbook/checks/u63_graph_genesis.py` |
| Check (book Lean) | `python textbook/checks/u63_lean.py` |
