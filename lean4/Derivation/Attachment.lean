import Derivation.HigherStructure

/-!
# One-edge attachment: trees from arbitrary policies

The growth driver of `HigherStructure` fixes one policy (attach to
the latest occurrence).  This module studies attachment as such:

1. **One-edge attachment** (`attachBlock`): glue a fresh walking
   edge — one new occurrence plus one asserted, retained, protected
   difference — along a *represented* parent chosen by an arbitrary
   policy.
2. **Every attachment policy produces a tree** (`treeAt_spec`,
   `parent_lt`, `parent_unique`, `parent_exists`, `all_reach`) and
   **preserves the connectivity residue** `V − E = 1`
   (`attach_residue`).
3. **Global shape is not forced**: the path and star policies yield
   non-isomorphic trees on four occurrences
   (`path4_star4_not_isomorphic`) — attachment forces tree-ness
   locally, never a global shape.
4. **`Up` is the complete family of legal extensions**
   (`attachMoves`): one block per represented parent, no selection
   (`attachMoves_complete`, `attachMoves_length`); the family
   depends only on the presentation size
   (`attachMoves_presentation_invariant`), and where the state has a
   symmetry the choices fall into orbits, demonstrated on the star
   and path instances (`star_orbit_swap`, `path_oriented_rigid`,
   `path_center_separate`).

Imported (declared, not derived) inputs, per the standing
discipline: fresh occurrence supply (the canonical next numeral),
protection, observer transport (none is used here — the attachment
driver is pre-observational), budget and activation (no funded
events occur in the supply blocks), and the metatheoretic iteration
of the driver.
-/

namespace Attachment

open PrimitivePassage HigherStructure

/-- The clamped parent: any policy value is forced onto a
represented parent of the child `k + 1`. -/
def par (π : Nat → Nat) (k : Nat) : Nat := min (π (k + 1)) k

/-- One-edge attachment: glue a fresh walking edge along the
represented parent — supply side only (assert, retain, protect). -/
def attachBlock (π : Nat → Nat) (k : Nat) : List PEvent :=
  [.admitOcc (k + 1), .assertWit (par π k) (k + 1),
   .admitWit (par π k) (k + 1), .protect (par π k) (k + 1)]

def attachHist (π : Nat → Nat) : Nat → List PEvent
  | 0 => [.admitOcc 0]
  | n + 1 => attachHist π n ++ attachBlock π n

/-- The grown state of an arbitrary attachment policy. -/
def treeAt (π : Nat → Nat) (n : Nat) : PState :=
  replayP (attachHist π n) genesisP

/-- The characterized record: `n + 1` occurrences and one
parent-edge per non-root occurrence, pre-observational. -/
def treeState (π : Nat → Nat) (n : Nat) : PState :=
  { occ := List.range (n + 1),
    asserted := (List.range n).map (fun k => (par π k, k + 1)),
    wit := (List.range n).map (fun k => (par π k, k + 1)),
    prot := (List.range n).map (fun k => (par π k, k + 1)),
    obs := none, budget := 0, licensed := true, refusals := [],
    halted := false }

/-! ### Guard facts, uniform in the policy -/

theorem par_le (π : Nat → Nat) (k : Nat) : par π k ≤ k :=
  Nat.min_le_right _ _

theorem attach_fresh (n : Nat) : ¬ (n + 1 ∈ List.range (n + 1)) := by
  intro h
  exact absurd (List.mem_range.mp h) (by omega)

theorem attach_pair_not_mem (π : Nat → Nat) (n : Nat) :
    ¬ ((par π n, n + 1) ∈ (List.range n).map
      (fun k => (par π k, k + 1))) := by
  intro h
  obtain ⟨k, hk, heq⟩ := List.mem_map.mp h
  have h2 : k + 1 = n + 1 := congrArg Prod.snd heq
  have h3 : k < n := List.mem_range.mp hk
  omega

/-- Intermediate states of one attachment round. -/
def t1 (π : Nat → Nat) (n : Nat) : PState :=
  { treeState π n with occ := List.range (n + 1) ++ [n + 1] }

def t2 (π : Nat → Nat) (n : Nat) : PState :=
  { t1 π n with
    asserted := (List.range n).map (fun k => (par π k, k + 1))
      ++ [(par π n, n + 1)] }

def t3 (π : Nat → Nat) (n : Nat) : PState :=
  { t2 π n with
    wit := (List.range n).map (fun k => (par π k, k + 1))
      ++ [(par π n, n + 1)] }

theorem attach_len (n : Nat) :
    (List.range (n + 1) ++ [n + 1]).length = n + 2 := by
  simp [List.length_append, List.length_range]

theorem attach_wf_guard (π : Nat → Nat) (n : Nat) :
    (wfPair (t1 π n) (par π n) (n + 1)
      && !(decide ((par π n, n + 1) ∈ (t1 π n).asserted)))
      = true := by
  show ((par π n != n + 1)
      && decide (par π n < (List.range (n + 1) ++ [n + 1]).length)
      && decide (n + 1 < (List.range (n + 1) ++ [n + 1]).length)
      && !(decide ((par π n, n + 1) ∈ (List.range n).map
            (fun k => (par π k, k + 1))))) = true
  rw [attach_len]
  have hle := par_le π n
  simp only [Bool.and_eq_true, Bool.not_eq_true',
    decide_eq_false_iff_not]
  exact ⟨⟨⟨bne_iff_ne.mpr (by omega),
    decide_eq_true (by omega)⟩, decide_eq_true (by omega)⟩,
    attach_pair_not_mem π n⟩

theorem attach_wit_guard (π : Nat → Nat) (n : Nat) :
    (wfPair (t2 π n) (par π n) (n + 1)
      && (decide ((par π n, n + 1) ∈ (t2 π n).asserted))
      && !(decide ((par π n, n + 1) ∈ (t2 π n).wit))) = true := by
  show ((par π n != n + 1)
      && decide (par π n < (List.range (n + 1) ++ [n + 1]).length)
      && decide (n + 1 < (List.range (n + 1) ++ [n + 1]).length)
      && (decide ((par π n, n + 1) ∈ (List.range n).map
            (fun k => (par π k, k + 1)) ++ [(par π n, n + 1)]))
      && !(decide ((par π n, n + 1) ∈ (List.range n).map
            (fun k => (par π k, k + 1))))) = true
  rw [attach_len]
  have hle := par_le π n
  simp only [Bool.and_eq_true, Bool.not_eq_true',
    decide_eq_false_iff_not]
  exact ⟨⟨⟨⟨bne_iff_ne.mpr (by omega),
    decide_eq_true (by omega)⟩, decide_eq_true (by omega)⟩,
    decide_eq_true
      (List.mem_append.mpr (Or.inr List.mem_cons_self))⟩,
    attach_pair_not_mem π n⟩

theorem attach_prot_guard (π : Nat → Nat) (n : Nat) :
    ((decide ((par π n, n + 1) ∈ (t3 π n).wit))
      && !(decide ((par π n, n + 1) ∈ (t3 π n).prot))) = true := by
  show ((decide ((par π n, n + 1) ∈ (List.range n).map
        (fun k => (par π k, k + 1)) ++ [(par π n, n + 1)]))
    && !(decide ((par π n, n + 1) ∈ (List.range n).map
        (fun k => (par π k, k + 1))))) = true
  simp only [Bool.and_eq_true, Bool.not_eq_true',
    decide_eq_false_iff_not]
  exact ⟨decide_eq_true
    (List.mem_append.mpr (Or.inr List.mem_cons_self)),
    attach_pair_not_mem π n⟩

theorem range_map_succ (π : Nat → Nat) (n : Nat) :
    (List.range (n + 1)).map (fun k => (par π k, k + 1))
      = (List.range n).map (fun k => (par π k, k + 1))
        ++ [(par π n, n + 1)] := by
  rw [List.range_succ, List.map_append]
  rfl

/-- **Every attachment policy is lawful at every stage**: the grown
state is exactly the characterized tree record, by induction —
whatever the policy chooses. -/
theorem treeAt_spec (π : Nat → Nat) (n : Nat) :
    treeAt π n = treeState π n := by
  induction n with
  | zero =>
      show replayP [.admitOcc 0] genesisP = treeState π 0
      have h : step genesisP (.admitOcc 0) =
          { genesisP with occ := [0] } := by
        rw [pstep_admit rfl (by intro h; cases h)]
        rfl
      show step genesisP (.admitOcc 0) = treeState π 0
      rw [h]
      rfl
  | succ m ih =>
      show replayP (attachHist π m ++ attachBlock π m) genesisP
        = treeState π (m + 1)
      rw [replay_append]
      show replayP (attachBlock π m) (treeAt π m)
        = treeState π (m + 1)
      rw [ih]
      show step (step (step (step (treeState π m)
        (.admitOcc (m + 1))) (.assertWit (par π m) (m + 1)))
        (.admitWit (par π m) (m + 1)))
        (.protect (par π m) (m + 1)) = treeState π (m + 1)
      rw [show step (treeState π m) (.admitOcc (m + 1)) = t1 π m
        from by
          rw [pstep_admit rfl (by exact attach_fresh m)]
          rfl]
      rw [show step (t1 π m) (.assertWit (par π m) (m + 1)) = t2 π m
        from by
          rw [pstep_assert rfl (attach_wf_guard π m)]
          rfl]
      rw [show step (t2 π m) (.admitWit (par π m) (m + 1)) = t3 π m
        from by
          rw [pstep_wit rfl (attach_wit_guard π m)]
          rfl]
      rw [pstep_prot rfl (attach_prot_guard π m)]
      show ({ t3 π m with
        prot := (List.range m).map (fun k => (par π k, k + 1))
          ++ [(par π m, m + 1)] } : PState) = treeState π (m + 1)
      unfold t3 t2 t1 treeState
      rw [show List.range (m + 1) ++ [m + 1] = List.range (m + 2)
        from (List.range_succ).symm,
        ← range_map_succ π m]

/-! ### The tree theorems, policy-uniform -/

/-- The connectivity residue `V − E = 1` at every stage, for every
policy. -/
theorem attach_residue (π : Nat → Nat) (n : Nat) :
    (treeAt π n).occ.length = n + 1 ∧
      (treeAt π n).wit.length = n := by
  rw [treeAt_spec]
  constructor
  · show (List.range (n + 1)).length = n + 1
    exact List.length_range
  · show ((List.range n).map (fun k => (par π k, k + 1))).length = n
    rw [List.length_map]
    exact List.length_range

/-- Edges ascend: every parent strictly precedes its child. -/
theorem parent_lt (π : Nat → Nat) (n : Nat) :
    ∀ p ∈ (treeAt π n).wit, p.1 < p.2 := by
  rw [treeAt_spec]
  intro p hp
  obtain ⟨k, _, heq⟩ := List.mem_map.mp hp
  subst heq
  have := par_le π k
  omega

/-- Unique parent: two edges into the same child coincide. -/
theorem parent_unique (π : Nat → Nat) (n : Nat) :
    ∀ p q, p ∈ (treeAt π n).wit → q ∈ (treeAt π n).wit →
      p.2 = q.2 → p = q := by
  rw [treeAt_spec]
  intro p q hp hq h2
  obtain ⟨k1, _, he1⟩ := List.mem_map.mp hp
  obtain ⟨k2, _, he2⟩ := List.mem_map.mp hq
  subst he1
  subst he2
  simp only at h2
  have : k1 = k2 := by omega
  subst this
  rfl

/-- Every non-root occurrence has a parent edge. -/
theorem parent_exists (π : Nat → Nat) (n : Nat) :
    ∀ c, 1 ≤ c → c < n + 1 →
      ∃ p, (p, c) ∈ (treeAt π n).wit := by
  rw [treeAt_spec]
  intro c h1 h2
  refine ⟨par π (c - 1), ?_⟩
  have hc : c - 1 < n := by omega
  have : (par π (c - 1), (c - 1) + 1) ∈
      (List.range n).map (fun k => (par π k, k + 1)) :=
    List.mem_map.mpr ⟨c - 1, List.mem_range.mpr hc, rfl⟩
  have hcc : c - 1 + 1 = c := by omega
  rw [hcc] at this
  exact this

/-- Reachability along parent edges. -/
inductive Reaches (E : List (Nat × Nat)) : Nat → Prop where
  | root : Reaches E 0
  | step {p c : Nat} : Reaches E p → (p, c) ∈ E → Reaches E c

theorem all_reach_aux (π : Nat → Nat) (n : Nat) :
    ∀ (bound v : Nat), v ≤ bound → v < n + 1 →
      Reaches ((treeState π n).wit) v := by
  intro bound
  induction bound with
  | zero =>
      intro v hv _
      have : v = 0 := by omega
      subst this
      exact .root
  | succ b ih =>
      intro v hv hn
      match v with
      | 0 => exact .root
      | Nat.succ k =>
          have hk : k < n := by omega
          have hmem : (par π k, k + 1) ∈ (treeState π n).wit := by
            show _ ∈ (List.range n).map (fun j => (par π j, j + 1))
            exact List.mem_map.mpr ⟨k, List.mem_range.mpr hk, rfl⟩
          have hple := par_le π k
          exact .step (ih (par π k) (by omega) (by omega)) hmem

/-- **Every attachment policy produces a tree**: unique ascending
parent per non-root occurrence, and every occurrence reaches the
root along parent edges. -/
theorem all_reach (π : Nat → Nat) (n : Nat) :
    ∀ v, v < n + 1 → Reaches ((treeState π n).wit) v :=
  fun v hv => all_reach_aux π n v v (Nat.le_refl v) hv

/-! ### Global shape is not forced: path versus star -/

def pathPol : Nat → Nat := fun i => i - 1

def starPol : Nat → Nat := fun _ => 0

theorem path_edges (n : Nat) :
    (treeAt pathPol n).wit
      = (List.range n).map (fun k => (k, k + 1)) := by
  rw [treeAt_spec]
  show (List.range n).map (fun k => (par pathPol k, k + 1)) = _
  have h : (fun k => (par pathPol k, k + 1))
      = (fun k : Nat => (k, k + 1)) := by
    funext k
    show (min ((k + 1) - 1) k, k + 1) = (k, k + 1)
    rw [show (k + 1) - 1 = k from rfl, Nat.min_self]
  rw [h]

theorem star_edges (n : Nat) :
    (treeAt starPol n).wit
      = (List.range n).map (fun k => (0, k + 1)) := by
  rw [treeAt_spec]
  show (List.range n).map (fun k => (par starPol k, k + 1)) = _
  have h : (fun k => (par starPol k, k + 1))
      = (fun k : Nat => (0, k + 1)) := by
    funext k
    show (min 0 k, k + 1) = (0, k + 1)
    rw [Nat.zero_min]
  rw [h]

def path4E : List (Nat × Nat) := [(0, 1), (1, 2), (2, 3)]

def star4E : List (Nat × Nat) := [(0, 1), (0, 2), (0, 3)]

theorem tree4_concrete :
    (treeAt pathPol 3).wit = path4E ∧
      (treeAt starPol 3).wit = star4E := by
  constructor <;> decide

/-- All injective 4-tuples: the candidate carrier bijections. -/
def tuples4 : List (Nat × Nat × Nat × Nat) :=
  ((List.range 4).flatMap fun a => (List.range 4).flatMap fun b =>
    (List.range 4).flatMap fun c => (List.range 4).map fun d =>
      (a, b, c, d)).filter fun t =>
    (t.1 != t.2.1) && (t.1 != t.2.2.1) && (t.1 != t.2.2.2)
      && (t.2.1 != t.2.2.1) && (t.2.1 != t.2.2.2)
      && (t.2.2.1 != t.2.2.2)

def app4 (t : Nat × Nat × Nat × Nat) (x : Nat) : Nat :=
  if x = 0 then t.1 else if x = 1 then t.2.1
  else if x = 2 then t.2.2.1 else t.2.2.2

def edgeInU (E : List (Nat × Nat)) (a b : Nat) : Bool :=
  (decide ((a, b) ∈ E)) || (decide ((b, a) ∈ E))

def isoMatch (t : Nat × Nat × Nat × Nat)
    (E1 E2 : List (Nat × Nat)) : Bool :=
  E1.all fun e => edgeInU E2 (app4 t e.1) (app4 t e.2)

/-- **Global shape is not forced**: no carrier bijection carries the
path tree onto the star tree on four occurrences (undirected edge
reading; both have three edges, so forward preservation under an
injective map decides isomorphism). -/
theorem path4_star4_not_isomorphic :
    (tuples4.all fun t => !(isoMatch t path4E star4E)) = true := by
  decide

/-! ### `Up`: the complete family of legal extensions -/

/-- `Up` of a state: ONE attachment block per represented parent —
the complete family, never a selected extension.  The fresh
occurrence is the canonical next numeral (imported supply). -/
def attachMoves (s : PState) : List (List PEvent) :=
  (List.range s.occ.length).map fun p =>
    [PEvent.admitOcc s.occ.length,
     PEvent.assertWit p s.occ.length,
     PEvent.admitWit p s.occ.length,
     PEvent.protect p s.occ.length]

/-- One block per parent: the family carries every choice. -/
theorem attachMoves_length (s : PState) :
    (attachMoves s).length = s.occ.length := by
  unfold attachMoves
  rw [List.length_map]
  exact List.length_range

/-- Completeness: every represented parent's block is in the
family. -/
theorem attachMoves_complete (s : PState) (p : Nat)
    (hp : p < s.occ.length) :
    [PEvent.admitOcc s.occ.length,
     PEvent.assertWit p s.occ.length,
     PEvent.admitWit p s.occ.length,
     PEvent.protect p s.occ.length] ∈ attachMoves s := by
  unfold attachMoves
  exact List.mem_map.mpr ⟨p, List.mem_range.mpr hp, rfl⟩

/-- The family is nonempty on every inhabited presentation. -/
theorem attachMoves_nonempty (s : PState)
    (h : 0 < s.occ.length) : attachMoves s ≠ [] := by
  intro he
  have := attachMoves_length s
  rw [he] at this
  simp at this
  omega

/-- **`Up` respects presentation isomorphisms** — in the strongest
form available at the family level: the family is invariant under
EVERY carrier-size-preserving re-presentation (renamings included),
because a legal parent is exactly a represented position. -/
theorem attachMoves_presentation_invariant (s t : PState)
    (h : s.occ.length = t.occ.length) :
    attachMoves s = attachMoves t := by
  unfold attachMoves
  rw [h]

/-! Orbit-valued choices where symmetry remains: on the star, the
two leaves are one orbit — attaching to either yields
rename-identical stores; on the path, the two ends are one orbit and
the center is its own.  (Concrete instances, decided; the general
orbit computation is the Python mirror's business, reusing the
sealed automorphism machinery.) -/

def swap12 : Nat → Nat := fun x =>
  if x = 1 then 2 else if x = 2 then 1 else x

def flip02 : Nat → Nat := fun x =>
  if x = 0 then 2 else if x = 2 then 0 else x

def renamePair (σ : Nat → Nat) (p : Nat × Nat) : Nat × Nat :=
  (σ p.1, σ p.2)

def blockAt (p n : Nat) : List PEvent :=
  [PEvent.admitOcc n, PEvent.assertWit p n, PEvent.admitWit p n,
   PEvent.protect p n]

/-- Star instance: attaching to leaf 1 and to leaf 2 are one orbit —
the leaf swap carries each store of the one extension exactly onto
the other's. -/
theorem star_orbit_swap :
    (((replayP (blockAt 1 3) (treeAt starPol 2)).wit.map
        (renamePair swap12)).all
      (fun p => decide (p ∈ (replayP (blockAt 2 3)
        (treeAt starPol 2)).wit)) = true) ∧
    (((replayP (blockAt 2 3) (treeAt starPol 2)).wit.map
        (renamePair swap12)).all
      (fun p => decide (p ∈ (replayP (blockAt 1 3)
        (treeAt starPol 2)).wit)) = true) := by
  constructor <;> decide

/-- Path instance: the ORIENTED path is rigid — the undirected flip
does NOT carry the end-attachment onto the other end's attachment,
because the oriented stores refuse the undirected symmetry (the
orientation residue at work: `Apartness.orientations_differ` one
level up).  So on the oriented path every parent is its own orbit,
while the star's leaves genuinely form one (`star_orbit_swap`). -/
theorem path_oriented_rigid :
    (((replayP (blockAt 0 3) (treeAt pathPol 2)).wit.map
        (renamePair flip02)).all
      (fun p => decide (p ∈ (replayP (blockAt 2 3)
        (treeAt pathPol 2)).wit)) = false) := by decide

/-- And the center is a separate orbit: neither the identity nor the
flip carries the end-attachment onto the center-attachment. -/
theorem path_center_separate :
    (((replayP (blockAt 0 3) (treeAt pathPol 2)).wit.map
        (renamePair flip02)).all
      (fun p => decide (p ∈ (replayP (blockAt 1 3)
        (treeAt pathPol 2)).wit)) = false) ∧
    (((replayP (blockAt 0 3) (treeAt pathPol 2)).wit.map
        (renamePair id)).all
      (fun p => decide (p ∈ (replayP (blockAt 1 3)
        (treeAt pathPol 2)).wit)) = false) := by
  constructor <;> decide

end Attachment
