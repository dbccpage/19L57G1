# Unit 59. Growing the carrier by one, and renaming the supply

**Claim.** On the passage state `PState` (Unit 54), a one-edge supply block `upBlock s p` admits the canonical fresh token `freshTok s` (one past the maximum token in `s.occ`, fresh on every occurrence list by `freshTok_fresh`, whereas `s.occ.length` collides on non-initial lists by `length_not_fresh_countermodel`) and then asserts, retains and protects the directed pair `(p, s.occ.length)` from parent position `p` to the new position. The complete proposal family `upFamily s` lists one block per existing position, and membership in `upFamily s` coincides with the declared one-edge grammar (`up_iff_legal`). On a live, store-bounded state (`WFStores s`, `s.halted = false`, `p < s.occ.length`), replaying `upBlock s p` reaches the closed form `upS4 s p` (`up_exec_eq`), extends the occurrence, asserted, retained and protected stores by one each, and preserves `WFStores` (`up_executes`); on a halted state every block is inert (`halted_up_inert`); an out-of-range parent meets a typed refusal (`attachChecked_refuses`) rather than silent clamping (`clamp_rewrote_input`). Iterating along any `LawfulPolicy` (a parent selector bounded by `choose (k + 1) ≤ k`) from genesis produces the closed-form state `treeState π n` (`treeAt_spec`) with `V − E = 1` (`attach_residue`), ascending edges (`parent_lt`), a unique parent per non-root position (`parent_unique`, `parent_exists`), and root reachability (`all_reach`); yet equal block cost does not force the resulting graph shape (`path4_star4_not_isomorphic`, `equal_cost_non_isomorphic_extensions`). A positional `Renaming n` (a bijection below `n`, identity at or above `n`) satisfies the six group laws under `idRen`, `invRen` and `compRen` (`comp_id`, `id_comp`, `comp_assoc`, `inv_comp`, `comp_inv`, `inv_inv`), acts on states (`act_id` unconditionally; `act_comp` and `act_inv` on `n ≤ s.occ.length`), preserves `WFStores` at `n = s.occ.length` (`wf_act`), transports blocks and the family (`upBlock_transport`, `upFamily_transport`, `upFamily_orbit_closed`), and commutes with block replay coherently under composition (`act_up_comm`, `act_up_comm_comp`, `act_up_comm_twostep`, packaged in `equivariance_summary`). A collapsing map is not a renaming (`collapse_not_a_renaming`), its raw pair pushforward produces ill-formed self-pairs (`collapse_pushforward_ill_formed`), and equal carrier size does not make two states renaming-related (`equal_size_not_renaming_related`). **Status:** FROZEN (general theorems); CONDITIONAL (`up_exec_eq`, `up_executes`, `act_up_comm`, `act_comp`, `act_inv`, `wf_act`, `equivariance_summary`, under their stated store-bound, liveness and scope hypotheses); VERIFIED_FINITE / REFUTED (the countermodels on clamp, length-as-token, 4-vertex shape, non-bijective collapse, equal size and equal cost). **Lean:** `lean4/Derivation/Attachment.lean` lines 61-1172 and `lean4/Derivation/RenamingStructure.lean` lines 48-482. **Axioms:** 54 reports for `Attachment` (`propext, Quot.sound` for 43, `propext` for 7, none for 4) and 28 reports for `RenamingStructure` (`propext, Quot.sound` for 23, `propext` for 1, none for 4). **Depends on:** Unit 54 (`PState`, `PEvent`, `step`, `replayP`, `genesisP`, `step_halted`), Unit 55 (`HigherStructure`).

## Question

When the passage kernel is driven to grow its carrier one occurrence at a time by attaching a new position to an existing parent position, what does the kernel guarantee (freshness, store growth, parent uniqueness, root reachability), what does block cost fail to determine (global graph shape), and in what exact sense does relabelling existing positions commute with proposing and executing the one-edge supply family?

## What we already possess

- `PState` with occurrence token list `occ`, pair stores `asserted`, `wit`, `prot` indexed by positions below `occ.length`, observation `obs`, `budget`, `licensed`, `refusals` and `halted`; the eleven `PEvent` constructors; `step`; `replayP`; `genesisP`; and `step_halted` (Unit 54).
- The distinction between tokens stored in `s.occ` and their list indices (positions `0 .. s.occ.length - 1`), which relational stores and observation columns reference (Unit 54, Unit 55).

## New concept: one-edge supply blocks, lawful tree policies, and positional renamings

`natMax l` folds `max` over `l` with base `0`. `freshTok s` is `0` when `s.occ` is empty and `natMax s.occ + 1` otherwise. For a parent position `p`, the four-event supply block is:

$$\text{upBlock}(s, p) = [\text{admitOcc}(\text{freshTok}(s)),\ \text{assertWit}(p, |s.\text{occ}|),\ \text{admitWit}(p, |s.\text{occ}|),\ \text{protect}(p, |s.\text{occ}|)].$$

`upFamily s` maps `upBlock s` over `List.range s.occ.length`. `LegalOneEdgeExtension s b` says `∃ p < s.occ.length, b = upBlock s p`. `WFStores s` says every pair `(a, b)` in `s.asserted`, `s.wit` and `s.prot` satisfies `a < s.occ.length ∧ b < s.occ.length`. `attachChecked s p` returns `.attached (replayP (upBlock s p) s)` when `p < s.occ.length` and `s.halted = false`, and `.refusedParent p s.occ.length` otherwise.

A `LawfulPolicy` pairs a function `choose : Nat → Nat` with a proof `lawful : ∀ k, choose (k + 1) ≤ k`. Writing `par π k = π.choose (k + 1)`, `attachBlock π k` attaches position `k + 1` to parent `par π k`, `attachHist π n` concatenates `[.admitOcc 0]` with the first `n` blocks, `treeAt π n` replays that history from `genesisP`, and `treeState π n` is the explicit record with `occ = List.range (n + 1)` and `asserted = wit = prot = (List.range n).map (fun k => (par π k, k + 1))`. `Reaches E v` is the inductive root-reachability predicate generated by `Reaches E 0` and `Reaches E p → (p, c) ∈ E → Reaches E c`.

A positional `Renaming n` consists of maps `f g : Nat → Nat` that are mutual inverses (`fg`, `gf`), map positions below `n` below `n` (`fbound`), and fix every position `x ≥ n` (`ffix`). `idRen n`, `invRen σ` and `compRen σ τ` define identity, inverse and composition. `act σ s` re-indexes `s.occ` so position `j` receives `s.occ.getD (σ.g j) 0` (putting the old token at position `i` into new position `σ.f i`), maps `renPair σ` (`(a, b) ↦ (σ.f a, σ.f b)`) over `asserted`, `wit`, `prot` and `refusals`, maps `σ.f` over any declared observation columns, and leaves `budget`, `licensed` and `halted` unchanged.

## Plain-language interpretation

To grow a graph one vertex and one edge at a time inside `PState`, two confusions have to be avoided up front.

First, tokens are not positions. `s.occ` is a list of token numbers in admission order; the stores `asserted`, `wit` and `prot` record pairs of list indices (positions). If `s.occ` is `[0, 1, 2]`, the length `3` happens to be an unused token. But if `s.occ` is `[1, 2]` (`s12`), its length is `2`, which is already in `s.occ`. Admitting `2` is deduplicated away by `step`, so the carrier stays of length `2`, position `2` never comes into existence, and the subsequent edge events `(0, 2)` fail their position-bound guard (`length_not_fresh_countermodel`). `freshTok s` takes one past the maximum token in `s.occ` (`3` on `[1, 2]`), which is guaranteed absent from `s.occ` (`freshTok_fresh`).

Second, an out-of-range parent choice must not be silently rewritten. An earlier draft clamped `c (k + 1)` to `min (c (k + 1)) k`, turning `badChoice` (`i ↦ i + 7`) into `0` at stage `0` (`clamp_rewrote_input`) and hiding the invalid input behind the star policy's output. Here a `LawfulPolicy` carries a proof that `choose (k + 1) ≤ k`, while `attachChecked` returns `.refusedParent p s.occ.length` whenever `p ≥ s.occ.length` (`attachChecked_refuses`).

With those two repairs in place, `upBlock s p` is the four-event recipe that admits `freshTok s` (creating position `s.occ.length`) and asserts, retains and protects the edge `(p, s.occ.length)`. `upFamily s` collects one such block for each existing position `p < s.occ.length`. When `s` is live and its existing stores only mention existing positions (`WFStores s`), replaying `upBlock s p` succeeds at all four steps (`up_exec_eq`, `up_executes`): the new pair `(p, s.occ.length)` cannot already be in `s.asserted`, `s.wit` or `s.prot` because every existing pair has second coordinate strictly below `s.occ.length`. Iterating along any `LawfulPolicy` from genesis produces a pre-observational tree at every stage `n` (`treeAt_spec`): `n + 1` occurrences, `n` edges in each of the three stores (`attach_residue`), every edge pointing from an older position to a newer one (`parent_lt`), a unique parent for every non-root position (`parent_unique`, `parent_exists`), and a directed path from `0` to every position (`all_reach`).

Does paying the same event cost force the same tree? No. The path policy (`choose (k + 1) = k`) and the star policy (`choose (k + 1) = 0`) both run three 4-event blocks to reach 4 vertices, yet no bijection of the 4 positions maps the undirected edges of the 4-path onto those of the 4-star (`path4_star4_not_isomorphic`), and even from the same 3-vertex path state, the two legal blocks at parents `1` and `2` have equal length `4` and execute to non-isomorphic 4-vertex trees (`equal_cost_non_isomorphic_extensions`).

Finally, what happens when we permute the existing positions `0 .. n - 1`? `Renaming n` packages a permutation of `{0, ..., n - 1}` extended by the identity on `{n, n + 1, ...}`. In `RenamingStructure`, identity, inverse and composition of renamings are shown to obey the group laws, and `act` is shown to obey the action laws on any state with at least `n` occurrences (`n ≤ s.occ.length`). Because a renaming at scale `n = s.occ.length` permutes the existing positions below `n` while fixing the new child position `n`, renaming a state and then running the block for `σ.f p` produces the exact same state as running the block for `p` and then renaming (`act_up_comm`), and this commutation composes across two renamings (`act_up_comm_comp`, `act_up_comm_twostep`). Because `upFamily` lists a block for every position, it carries the entire renaming orbit of every parent without selecting a representative (`upFamily_orbit_closed`). None of this holds for a non-bijective map such as `collapseMap` (`_ ↦ 0`), which has no left inverse (`collapse_not_a_renaming`) and pushes a valid store forward into self-loops `(0, 0)` (`collapse_pushforward_ill_formed`).

## Pseudocode

```
freshTok(s)          := 0 if s.occ == [] else max(s.occ) + 1
upBlock(s, p)        := [admitOcc(freshTok(s)), assertWit(p, |s.occ|),
                         admitWit(p, |s.occ|), protect(p, |s.occ|)]
upFamily(s)          := [upBlock(s, p) for p in 0 .. |s.occ| - 1]

if WFStores(s) and not s.halted and p < |s.occ|:
    replayP(upBlock(s, p), s) == upS4(s, p)   -- all four stores grow by 1

treeAt(pi, n)        := replayP([admitOcc 0] ++ concat_{k < n} attachBlock(pi, k), genesisP)
                     == treeState(pi, n)      -- V = n+1, E = n, unique parent, all reach 0

Renaming(n)          := (f, g, fg: g(f(x))=x, gf: f(g(x))=x,
                         fbound: x<n -> f(x)<n, ffix: x>=n -> f(x)=x)
act(sigma, s).occ[j] := s.occ[sigma.g(j)]
act(sigma, s).stores := map (a, b) |-> (sigma.f(a), sigma.f(b))

if n == |s.occ| and WFStores(s) and not s.halted and p < |s.occ|:
    act(sigma, replayP(upBlock(s, p), s))
      == replayP(upBlock(act(sigma, s), sigma.f(p)), act(sigma, s))
```

## Python

Genesis's mirrors, `code/derivation/attachment_ladder.py` and `code/derivation/renaming_structure.py`:

```python
def fresh_tok(s: PS) -> int:
    return 0 if not s.occ else max(s.occ) + 1


def up_block(s: PS, p: int) -> list[PEvent]:
    n = len(s.occ)
    return [("admitOcc", fresh_tok(s)), ("assertWit", p, n),
            ("admitWit", p, n), ("protect", p, n)]


def up_family(s: PS) -> list[list[PEvent]]:
    return [up_block(s, p) for p in range(len(s.occ))]


def act(perm: tuple[int, ...], s: PS) -> PS:
    n = len(perm)
    inv = [0] * n
    for i, fi in enumerate(perm):
        inv[fi] = i

    def f(x: int) -> int:
        return perm[x] if x < n else x

    def g(j: int) -> int:
        return inv[j] if j < n else j

    def rp(pr: Pair) -> Pair:
        return (f(pr[0]), f(pr[1]))

    obs: Optional[tuple[tuple[int, ...], ...]] = None
    if s.obs is not None:
        obs = tuple(tuple(f(x) for x in col) for col in s.obs)
    return PS(occ=tuple(s.occ[g(j)] for j in range(len(s.occ))),
              asserted=tuple(rp(pr) for pr in s.asserted),
              wit=tuple(rp(pr) for pr in s.wit),
              prot=tuple(rp(pr) for pr in s.prot),
              obs=obs, budget=s.budget, licensed=s.licensed,
              refusals=tuple(rp(pr) for pr in s.refusals),
              halted=s.halted)


def comp_ren(sigma: Perm, tau: Perm) -> Perm:
    return tuple(sigma[tau[i]] for i in range(len(tau)))
```

The book's check, `textbook/checks/u59_attachment.py`, adds Python (book):

```python
    s_ill = PS(occ=(1, 2), asserted=((0, 2),), wit=((0, 2),), prot=((0, 2),))
    ill_out = attach_checked(s_ill, 0)
    s_halted = PS(occ=(1, 2), halted=True)
    halted_out = attach_checked(s_halted, 0)
```

## Line-by-line Python explanation

- `fresh_tok`: returns `0` on an empty occurrence tuple and `max(s.occ) + 1` otherwise, matching `Attachment.freshTok`.
- `up_block`: reads `n = len(s.occ)` as the new child position, admits `fresh_tok(s)`, and emits the three edge events on `(p, n)`.
- `up_family`: builds the list of `up_block(s, p)` for `p` from `0` to `len(s.occ) - 1`.
- `act`: constructs the inverse table `inv` of `perm`, extends both `f` and `g` by the identity on indices `>= n`, re-indexes `s.occ` by `s.occ[g(j)]` so the token at old index `i` lands at new index `f(i)`, and maps `rp` across `asserted`, `wit`, `prot` and `refusals` and `f` across `s.obs`.
- `comp_ren`: composes two permutation tuples of length `n` as `sigma[tau[i]]`.
- Python (book) `s_ill`: a live 2-occurrence state whose stores already contain `(0, 2)` (violating `WFStores`). `attach_checked(s_ill, 0)` checks only `p < len(s.occ)` and `not s.halted`, so it returns `"outcome": "attached"` with `occ_len == 3`, while the duplicate-pair guards reject all three edge events and `wit_len` stays `1`. This shows concretely why `up_executes` requires `WFStores s`.

## Lean 4

From `lean4/Derivation/Attachment.lean` (lines 61-1170, abridged):

```lean
structure LawfulPolicy where
  choose : Nat → Nat
  lawful : ∀ k, choose (k + 1) ≤ k

def freshTok (s : PState) : Nat :=
  if s.occ.isEmpty then 0 else natMax s.occ + 1

theorem freshTok_fresh (s : PState) : ¬ (freshTok s ∈ s.occ) := by ...

def upBlock (s : PState) (p : Nat) : List PEvent :=
  [.admitOcc (freshTok s), .assertWit p s.occ.length,
   .admitWit p s.occ.length, .protect p s.occ.length]

def upFamily (s : PState) : List (List PEvent) :=
  (List.range s.occ.length).map (upBlock s)

def LegalOneEdgeExtension (s : PState) (b : List PEvent) : Prop :=
  ∃ p, p < s.occ.length ∧ b = upBlock s p

theorem up_iff_legal (s : PState) (b : List PEvent) :
    b ∈ upFamily s ↔ LegalOneEdgeExtension s b := by
  constructor
  · intro hb
    obtain ⟨p, hp, heq⟩ := List.mem_map.mp hb
    exact ⟨p, List.mem_range.mp hp, heq.symm⟩
  · intro ⟨p, hp, heq⟩
    subst heq
    exact List.mem_map.mpr ⟨p, List.mem_range.mpr hp, rfl⟩

theorem up_executes (s : PState) (hwf : WFStores s)
    (hh : s.halted = false) (p : Nat) (hp : p < s.occ.length) :
    (replayP (upBlock s p) s).occ.length = s.occ.length + 1 ∧
    (replayP (upBlock s p) s).asserted.length = s.asserted.length + 1 ∧
    (replayP (upBlock s p) s).wit.length = s.wit.length + 1 ∧
    (replayP (upBlock s p) s).prot.length = s.prot.length + 1 ∧
    WFStores (replayP (upBlock s p) s) := by ...

theorem halted_up_inert (s : PState) (h : s.halted = true)
    (p : Nat) : replayP (upBlock s p) s = s := by
  show step (step (step (step s (.admitOcc (freshTok s)))
    (.assertWit p s.occ.length)) (.admitWit p s.occ.length))
    (.protect p s.occ.length) = s
  rw [step_halted s _ h, step_halted s _ h, step_halted s _ h,
      step_halted s _ h]

structure Renaming (n : Nat) where
  f : Nat → Nat
  g : Nat → Nat
  fg : ∀ x, g (f x) = x
  gf : ∀ x, f (g x) = x
  fbound : ∀ x, x < n → f x < n
  ffix : ∀ x, n ≤ x → f x = x

theorem act_up_comm {n : Nat} (σ : Renaming n) (s : PState)
    (hn : n = s.occ.length) (hwf : WFStores s)
    (hh : s.halted = false) (p : Nat) (hp : p < s.occ.length) :
    act σ (replayP (upBlock s p) s)
      = replayP (upBlock (act σ s) (σ.f p)) (act σ s) := by ...

theorem treeAt_spec (π : LawfulPolicy) (n : Nat) :
    treeAt π n = treeState π n := by ...

theorem path4_star4_not_isomorphic :
    (tuples4.all fun t => !(isoMatch t path4E star4E)) = true := by
  decide

theorem equal_cost_non_isomorphic_extensions :
    (upBlock (treeAt pathPolL 2) 1 ∈ upFamily (treeAt pathPolL 2)) ∧
    (upBlock (treeAt pathPolL 2) 2 ∈ upFamily (treeAt pathPolL 2)) ∧
    ((upBlock (treeAt pathPolL 2) 1).length
      = (upBlock (treeAt pathPolL 2) 2).length) ∧
    ((tuples4.all fun t => !(isoMatch t
        (replayP (upBlock (treeAt pathPolL 2) 1)
          (treeAt pathPolL 2)).wit
        (replayP (upBlock (treeAt pathPolL 2) 2)
          (treeAt pathPolL 2)).wit)) = true) := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> decide
```

From `lean4/Derivation/RenamingStructure.lean` (lines 48-480, abridged):

```lean
theorem Renaming.ext {n : Nat} (σ τ : Renaming n)
    (hf : σ.f = τ.f) (hg : σ.g = τ.g) : σ = τ := by
  cases σ; cases τ; cases hf; cases hg; rfl

theorem comp_id {n : Nat} (σ : Renaming n) : compRen σ (idRen n) = σ :=
  Renaming.ext _ _ rfl rfl
theorem id_comp {n : Nat} (σ : Renaming n) : compRen (idRen n) σ = σ :=
  Renaming.ext _ _ rfl rfl
theorem comp_assoc {n : Nat} (σ τ ρ : Renaming n) :
    compRen (compRen σ τ) ρ = compRen σ (compRen τ ρ) :=
  Renaming.ext _ _ rfl rfl
theorem inv_comp {n : Nat} (σ : Renaming n) :
    compRen (invRen σ) σ = idRen n :=
  Renaming.ext _ _ (funext (fun x => σ.fg x)) (funext (fun x => σ.fg x))
theorem comp_inv {n : Nat} (σ : Renaming n) :
    compRen σ (invRen σ) = idRen n :=
  Renaming.ext _ _ (funext (fun x => σ.gf x)) (funext (fun x => σ.gf x))

theorem act_id (n : Nat) (s : PState) : act (idRen n) s = s := by ...
theorem act_comp {n : Nat} (σ τ : Renaming n) (s : PState)
    (hn : n ≤ s.occ.length) :
    act (compRen σ τ) s = act σ (act τ s) := by ...
theorem act_inv {n : Nat} (σ : Renaming n) (s : PState)
    (hn : n ≤ s.occ.length) : act (invRen σ) (act σ s) = s := by
  rw [← act_comp (invRen σ) σ s hn, inv_comp, act_id]

theorem wf_act {n : Nat} (σ : Renaming n) (s : PState)
    (hn : n = s.occ.length) (hwf : WFStores s) :
    WFStores (act σ s) := by ...

theorem upFamily_orbit_closed {n : Nat} (σ : Renaming n) (s : PState)
    (hn : n = s.occ.length) (b : List PEvent) (hb : b ∈ upFamily s) :
    ∃ p, p < s.occ.length ∧ b = upBlock s p ∧
      upBlock (act σ s) (σ.f p) ∈ upFamily (act σ s) := by ...

theorem collapse_not_a_renaming :
    ¬ ∃ g : Nat → Nat, ∀ x, g (collapseMap x) = x := by
  intro ⟨g, hg⟩
  have h0 : g 0 = 0 := hg 0
  have h1 : g 0 = 1 := hg 1
  omega

theorem equivariance_summary {n : Nat} (σ τ : Renaming n)
    (s : PState) (hn : n = s.occ.length) (hwf : WFStores s)
    (hh : s.halted = false) (p : Nat) (hp : p < s.occ.length) :
    compRen σ (idRen n) = σ ∧
    compRen (invRen σ) σ = idRen n ∧
    act (idRen n) s = s ∧
    act (compRen σ τ) s = act σ (act τ s) ∧
    upFamily (act (idRen n) s) = upFamily s ∧
    upFamily (act (compRen σ τ) s) = upFamily (act σ (act τ s)) ∧
    act (compRen σ τ) (replayP (upBlock s p) s)
      = replayP (upBlock (act σ (act τ s)) (σ.f (τ.f p)))
          (act σ (act τ s)) := ...
```

Lean (book), from `textbook/checks/u59_lean.py`:

```lean
def sIll : PState :=
  { s12 with asserted := [(0, 2)], wit := [(0, 2)], prot := [(0, 2)] }

theorem sIll_not_wf : ¬ WFStores sIll := by
  intro ⟨hwa, _, _⟩
  have h := (hwa (0, 2) List.mem_cons_self).2
  revert h
  decide

theorem sIll_attach_partial :
    attachChecked sIll 0 = .attached (replayP (upBlock sIll 0) sIll) ∧
    (replayP (upBlock sIll 0) sIll).occ.length = 3 ∧
    (replayP (upBlock sIll 0) sIll).asserted.length = sIll.asserted.length ∧
    (replayP (upBlock sIll 0) sIll).wit.length = sIll.wit.length ∧
    (replayP (upBlock sIll 0) sIll).prot.length = sIll.prot.length := by
  refine ⟨by decide, by decide, by decide, by decide, by decide⟩

theorem act_inv_out_of_scope :
    (act swap12Ren3 s12).occ = [1, 0] ∧
    act (invRen swap12Ren3) (act swap12Ren3 s12) ≠ s12 := by
  refine ⟨by decide, ?_⟩
  intro h
  have hocc := congrArg PState.occ h
  revert hocc
  decide
```

## Line-by-line Lean explanation

- `freshTok_fresh`: splits on `s.occ`. On `nil`, membership in `[]` is impossible; on `a :: t`, `freshTok s = natMax (a :: t) + 1`, and `le_natMax_of_mem` shows any member is `≤ natMax (a :: t)`, which `omega` refutes.
- `up_iff_legal`: unfolds membership in `(List.range s.occ.length).map (upBlock s)` via `List.mem_map` and `List.mem_range`. Both directions are definitional renamings of `LegalOneEdgeExtension`.
- `up_exec_eq` and `up_executes`: step through the four events of `upBlock s p` using `pstep_admit`, `pstep_assert`, `pstep_wit` and `pstep_prot`. At step 1, `freshTok_fresh` guarantees the token is admitted so `occ` becomes `s.occ ++ [freshTok s]` of length `s.occ.length + 1`. At steps 2-4, `p < s.occ.length` gives `p ≠ s.occ.length` and both coordinates `< s.occ.length + 1`, while `WFStores s` guarantees `(p, s.occ.length)` is not already in `s.asserted`, `s.wit` or `s.prot`.
- `halted_up_inert`: rewrites all four `step` calls by `step_halted`.
- `Renaming`: stores both `f` and `g` as `Nat → Nat` functions with inverse proofs `fg` and `gf`, the bound `fbound` below `n`, and the fixpoint law `ffix` at or above `n`. From these, `Renaming.gbound`, `Renaming.gfix` and `Renaming.fbound_iff` derive the matching properties for `g`.
- `act_up_comm`: proves `WFStores (act σ s)` from `hwf` and `hn : n = s.occ.length`, rewrites both sides by `up_exec_eq` into `act σ (upS4 s p)` and `upS4 (act σ s) (σ.f p)`, and checks field by field that they coincide: on `occ`, positions `j < n` come from `s.occ` via `getD_append_lt` and position `n` is fixed by `σ.gfix` and carries `freshTok s = freshTok (act σ s)`; on the pair stores, `renPair σ (p, s.occ.length) = (σ.f p, (act σ s).occ.length)` because `σ.ffix` fixes `s.occ.length`.
- `treeAt_spec`: induction on `n`. At `0`, `[.admitOcc 0]` on `genesisP` gives `treeState π 0`. At `m + 1`, `replay_append` and the induction hypothesis reduce the goal to four steps from `treeState π m`, discharged by `attach_fresh`, `attach_wf_guard`, `attach_wit_guard` and `attach_prot_guard`.
- `attach_residue`, `parent_lt`, `parent_unique`, `parent_exists`, `all_reach`: rewrite `treeAt π n` to `treeState π n` by `treeAt_spec`; the edge list is `(List.range n).map (fun k => (par π k, k + 1))`, where `par π k ≤ k < k + 1` gives strict ascent, the second coordinate `k + 1` uniquely determines `k`, every `c` in `1 .. n` arises at `k = c - 1`, and strong induction on the vertex index (`all_reach_aux`) walks back to `0`.
- `Renaming.ext` and the six laws: because the four proof fields of `Renaming n` live in `Prop`, two renamings with the same `f` and `g` are equal (`Renaming.ext`). `comp_id`, `id_comp`, `comp_assoc` and `inv_inv` then hold by `rfl` on both functions, while `inv_comp` and `comp_inv` use `funext` with `σ.fg` and `σ.gf`.
- `act_id`, `act_comp`, `act_inv`: `act_id` uses `map_getD_range` (`(List.range l.length).map (l.getD · 0) = l`) and needs no bound on `n`. `act_comp` requires `n ≤ s.occ.length` so that for every `j < s.occ.length`, `σ.g j < s.occ.length` (by `σ.gbound` below `n` and `σ.gfix` at or above `n`), allowing `getD_lt` to compose the two `occ` re-indexings. `act_inv` follows in one line from `act_comp`, `inv_comp` and `act_id`.
- Book `sIll_not_wf` and `sIll_attach_partial`: demonstrate that `attachChecked` only tests `p < s.occ.length` and `!s.halted`; without `WFStores`, `.attached` is returned even though none of the three edge stores grows.
- Book `act_inv_out_of_scope`: with `n = 3 > s12.occ.length = 2`, `swap12Ren3` maps index `1` to `2`, so `(act swap12Ren3 s12).occ` reads `s12.occ.getD 2 0 = 0`, losing token `2` and refuting `act (invRen σ) (act σ s12) = s12`.

## What has been proved

- In `Attachment`: `par_le` (69), `clamp_rewrote_input` (84), `le_natMax_of_mem` (101), `freshTok_fresh` (119), `up_iff_legal` (153), `up_exec_eq` (187), `up_executes` (252), `attachChecked_refuses` (312), `unlawful_refused` (325), `length_not_fresh_countermodel` (345), `halted_up_inert` (354), `Renaming.f_inj` (375), `Renaming.gbound` (381), `Renaming.gfix` (391), `Renaming.fbound_iff` (403), `getD_lt` (414), `getD_append_lt` (419), `act_occ_length` (444), `act_occ_mem` (451), `freshTok_act` (472), `upBlock_transport` (513), `upBlock_parent_inj` (525), `upFamily_transport` (533), `act_up_comm` (561), `upFamily_grammar_uniform` (663), `attach_fresh` (699), `attach_pair_not_mem` (703), `attach_len` (726), `attach_wf_guard` (730), `attach_wit_guard` (747), `attach_prot_guard` (768), `range_map_succ` (781), `treeAt_spec` (791), `natMax_append_singleton` (837), `natMax_range_le` (848), `tree_occ_len` (855), `freshTok_treeState` (862), `attachBlock_is_upBlock` (879), `treeState_wf` (886), `attach_residue` (903), `parent_lt` (915), `parent_unique` (925), `parent_exists` (940), `all_reach_aux` (959), `all_reach` (984), `path_edges` (1011), `star_edges` (1023), `tree4_concrete` (1034), `path4_star4_not_isomorphic` (1063), `star_orbit_swap` (1085), `path_oriented_rigid` (1102), `path_center_separate` (1110), `equal_size_not_renaming_related` (1130), `equal_cost_non_isomorphic_extensions` (1160).
- In `RenamingStructure`: `Renaming.ext` (48), `comp_id` (90), `id_comp` (94), `comp_assoc` (98), `inv_comp` (102), `comp_inv` (107), `inv_inv` (112), `map_getD_range` (118), `act_id` (129), `act_comp` (168), `act_inv` (233), `upBlock_id` (239), `upBlock_comp` (244), `upFamily_id` (251), `upFamily_comp` (255), `upFamily_transport_comp` (262), `upFamily_transport_id` (270), `wf_act` (280), `act_up_comm_comp` (312), `act_up_comm_twostep` (323), `upFamily_orbit_closed` (342), `star_orbit_both_present` (353), `upFamily_length` (362), `collapse_not_a_renaming` (379), `collapse_pushforward_ill_formed` (397), `equal_size_supplies_no_law` (411), `equal_cost_supplies_no_law` (420), `equivariance_summary` (461).

## What has not been proved

- That `up_iff_legal` characterizes every possible one-edge extension of `PState`. Audit finding (`Attachment` §11): `LegalOneEdgeExtension` is defined using the same `upBlock` (`∃ p < s.occ.length, b = upBlock s p`), so completeness is registry-relative to the declared 4-event grammar and the canonical `freshTok` policy. It says nothing about other fresh-token conventions, multi-edge blocks, or observation events.
- That `attachChecked s p = .attached t` implies all four stores of `t` grew. Audit finding (`Attachment` §6, §11): `attachChecked` checks `p < s.occ.length` and `!s.halted`, but does not check `WFStores s`. As `sIll_attach_partial` (Lean (book)) shows, on an ill-formed live state `attachChecked` returns `.attached` even when the edge stores fail to grow.
- A single bundled `IsTree` predicate in Lean. The tree properties are proved as five separate theorems (`attach_residue`, `parent_lt`, `parent_unique`, `parent_exists`, `all_reach`); the bundled `is_tree` boolean exists only in Python.
- That `act` is a global group action on all of `PState` without the scope condition `n ≤ s.occ.length`. As `act_inv_out_of_scope` (Lean (book)) shows, when `n > s.occ.length` a renaming can move an in-range position to an out-of-range index, causing `getD` to substitute `0` and breaking invertibility.
- That `upFamily_orbit_closed` establishes a non-trivial symmetry-selection theorem beyond the fact that `upFamily` already lists a block for every position `p < s.occ.length` (`RenamingStructure` audit §6, §11). Nor is equivariance claimed for the observation calculus (`refineCol`, `addCol`).

## Outside the system

- `LawfulPolicy.choose : Nat → Nat`, `treeAt : LawfulPolicy → Nat → PState`, and `Renaming.f, g : Nat → Nat` are functions on all of `Nat` in the metatheory. At any stage `n`, the system holds a single finite state `treeAt π n` with `n + 1` occurrences and `n` edges; no infinite tree and no infinite permutation object exists inside `PState`.
- "Cost" in `equal_cost_non_isomorphic_extensions` is the list length of a proposal block (`4` events), an admitted count of events in the declared grammar, not a derived measure.
- `store_automorphisms` and `parent_orbits` in `code/derivation/attachment_ladder.py` are finite Python enumerations over `permutations(range(n))` at `n = 3`; Lean proves concrete orbit instances (`star_orbit_swap`, `path_oriented_rigid`, `path_center_separate`, `star_orbit_both_present`) rather than defining an orbit-partition function.

## Student exercise

In `Attachment`, `act_occ_mem` and `freshTok_act` assume `hn : n = s.occ.length`, whereas in `RenamingStructure`, `act_comp` and `act_inv` assume the weaker inequality `hn : n ≤ s.occ.length`. Explain why `act_up_comm_twostep` needs `act_comp` under `n ≤ s.occ.length` rather than `n = s.occ.length`, even though `act_up_comm_twostep` itself assumes `hn : n = s.occ.length`.

## Answer

In `act_up_comm_twostep`, the starting state `s` has `s.occ.length = n`, so at the source of the square `n = s.occ.length` holds. However, the left-hand side of `act_up_comm_twostep` applies `act σ (act τ (replayP (upBlock s p) s))` to the *extended* state `t = replayP (upBlock s p) s`. By `(up_executes s hwf hh p hp).1`, the extended state has `t.occ.length = s.occ.length + 1 = n + 1`. At `t`, the equality `n = t.occ.length` is false (`n ≠ n + 1`), while the inequality `n ≤ t.occ.length` (`n ≤ n + 1`) holds! Because `act_comp` was proved under `n ≤ s.occ.length`, line 331 of `RenamingStructure.lean` can rewrite `act σ (act τ t)` to `act (compRen σ τ) t` and reduce `act_up_comm_twostep` to `act_up_comm_comp`.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Attachment.lean` lines 61-95 (policies, refusal), 99-131 (`freshTok`), 138-360 (`upBlock`, `upFamily`, `up_executes`, countermodels), 367-666 (`Renaming`, `act`, `act_up_comm`), 675-987 (`treeAt_spec`, tree theorems), 990-1172 (path vs star, orbits, equal-size and equal-cost countermodels); `lean4/Derivation/RenamingStructure.lean` lines 48-115 (`Renaming.ext`, group laws), 118-236 (`act_id`, `act_comp`, `act_inv`), 239-276 (transport composition), 280-335 (`wf_act`, coherence), 342-367 (orbit closure), 371-431 (countermodels), 461-482 (`equivariance_summary`) |
| Axiom report | `artifacts/lean_axioms.txt` lines 656-709 (`Attachment`, 54 reports) and lines 765-792 (`RenamingStructure`, 28 reports) |
| Paper | `paper/primitive_difference_map.md` §8; `paper/paper_claim_ledger.md` `CL-PD2-ATTACHMENT`, `CL-PD2-RENAMING-STRUCTURE` |
| Python | `code/derivation/attachment_ladder.py` (sections 1-4), `code/derivation/renaming_structure.py`, `code/run_attachment_ladder.py`, `code/run_renaming_structure.py`, `tests/test_attachment_ladder.py`, `tests/test_renaming_structure.py`, `artifacts/attachment_ladder.json`, `artifacts/renaming_structure.json` |
| Audit | `textbook/audit/modules/Attachment.md`, `textbook/audit/modules/RenamingStructure.md` |
| Check (Python) | `python textbook/checks/u59_attachment.py`: clamp and length-as-token countermodels, `up_report`, Python (book) `WFStores` load-bearing check on `s_ill`, `tree_report(15)` on path/star/zigzag, `shape_report`, `Renaming(3)` group/action/transport/coherence/orbit laws and countermodels, artifact comparison |
| Check (book Lean) | `python textbook/checks/u59_lean.py`: nine book theorems (`sIll_not_wf`, `sIll_attach_partial`, `act_inv_out_of_scope`, etc.) plus thirty-seven Genesis theorems kernel-checked, Lean 4.33.0 |
