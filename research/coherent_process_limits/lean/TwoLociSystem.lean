import Limits
import TwoLoci

/-!
# TwoLociSystem: two-locus thread space as an inverse system

The observation space of the sealed system is initially formulated over a
single carrier. Extending to two independent loci equips the observation
space with a product inverse system.

This module establishes three core structures:
1. **Factorization of bonding maps.** An observation at scale `n` over two
   loci with capacities `c₁` and `c₂` is an element of `Stage (c₁ * c₂) n`.
   The bonding map `bond (c₁ * c₂) n` projects under `stageFst` and `stageSnd`
   to `bond c₁ n` and `bond c₂ n`.
2. **The two-locus thread space as a product.** A thread of the composite
   system corresponds to a pair of threads of the individual loci via the
   explicit mutual inverses `threadPack` and `⟨threadFst, threadSnd⟩`.
3. **Locus-wise observation compatibility of runs.** For any two-locus run,
   the observed tapes at finite scales satisfy prefix compatibility when
   projected to each locus.

AuthorityEffect: None.
-/

namespace TwoLociSystem

open Derivation Translation Execution Control Product Schedule Runner Observe Limits

/-! ## 1. Two-locus observations at finite scales -/

/-- The first-locus projection of a two-locus observation at scale `n`.
AuthorityEffect: None. -/
def stageFst (c₁ c₂ n : Nat) (t : Stage (c₁ * c₂) n) : Stage c₁ n :=
  fun i => ⟨fstOf c₂ (t i).val, fst_lt (t i).isLt⟩

/-- The second-locus projection of a two-locus observation at scale `n`.
AuthorityEffect: None. -/
def stageSnd (c₁ c₂ n : Nat) (hc₂ : 0 < c₂) (t : Stage (c₁ * c₂) n) : Stage c₂ n :=
  fun i => ⟨sndOf c₂ (t i).val, snd_lt hc₂⟩

/-- Pack two single-locus observations at scale `n` into a two-locus observation.
AuthorityEffect: None. -/
def stagePack (c₁ c₂ n : Nat) (t₁ : Stage c₁ n) (t₂ : Stage c₂ n) : Stage (c₁ * c₂) n :=
  fun i => ⟨pack c₂ (t₁ i).val (t₂ i).val, pack_lt (t₁ i).isLt (t₂ i).isLt⟩

/-- Projecting a packed stage to the first locus recovers the first component.
AuthorityEffect: None. -/
theorem stageFst_stagePack (c₁ c₂ n : Nat) (hc₂ : 0 < c₂)
    (t₁ : Stage c₁ n) (t₂ : Stage c₂ n) :
    stageFst c₁ c₂ n (stagePack c₁ c₂ n t₁ t₂) = t₁ := by
  funext i
  apply Fin.ext
  exact fst_pack hc₂ (t₂ i).isLt

/-- Projecting a packed stage to the second locus recovers the second component.
AuthorityEffect: None. -/
theorem stageSnd_stagePack (c₁ c₂ n : Nat) (hc₂ : 0 < c₂)
    (t₁ : Stage c₁ n) (t₂ : Stage c₂ n) :
    stageSnd c₁ c₂ n hc₂ (stagePack c₁ c₂ n t₁ t₂) = t₂ := by
  funext i
  apply Fin.ext
  exact snd_pack (t₂ i).isLt

/-- Packing the two coordinate projections of a stage recovers the stage.
AuthorityEffect: None. -/
theorem stagePack_stageFst_stageSnd (c₁ c₂ n : Nat) (hc₂ : 0 < c₂)
    (t : Stage (c₁ * c₂) n) :
    stagePack c₁ c₂ n (stageFst c₁ c₂ n t) (stageSnd c₁ c₂ n hc₂ t) = t := by
  funext i
  apply Fin.ext
  show pack c₂ (fstOf c₂ (t i).val) (sndOf c₂ (t i).val) = (t i).val
  show c₂ * ((t i).val / c₂) + (t i).val % c₂ = (t i).val
  exact Nat.div_add_mod (t i).val c₂

/-! ## 2. Factorization of bonding maps -/

/-- The bonding map of a two-locus system projects under `stageFst` to the
bonding map of the first locus.
AuthorityEffect: None. -/
theorem stageFst_bond (c₁ c₂ n : Nat) (t : Stage (c₁ * c₂) (n + 1)) :
    stageFst c₁ c₂ n (bond (c₁ * c₂) n t) = bond c₁ n (stageFst c₁ c₂ (n + 1) t) := rfl

/-- The bonding map of a two-locus system projects under `stageSnd` to the
bonding map of the second locus.
AuthorityEffect: None. -/
theorem stageSnd_bond (c₁ c₂ n : Nat) (hc₂ : 0 < c₂) (t : Stage (c₁ * c₂) (n + 1)) :
    stageSnd c₁ c₂ n hc₂ (bond (c₁ * c₂) n t) = bond c₂ n (stageSnd c₁ c₂ (n + 1) hc₂ t) := rfl

/-- Packing preserves bonding: the bonding map of packed stages is the packing
of the component bonding maps.
AuthorityEffect: None. -/
theorem stagePack_bond (c₁ c₂ n : Nat) (t₁ : Stage c₁ (n + 1)) (t₂ : Stage c₂ (n + 1)) :
    stagePack c₁ c₂ n (bond c₁ n t₁) (bond c₂ n t₂) =
      bond (c₁ * c₂) n (stagePack c₁ c₂ (n + 1) t₁ t₂) := rfl

/-- **Factorization of bonding maps.** The bonding map of the two-locus product
factors through the bonding maps of the individual loci.
AuthorityEffect: None. -/
theorem bond_factors_two_loci (c₁ c₂ n : Nat) (hc₂ : 0 < c₂)
    (t : Stage (c₁ * c₂) (n + 1)) :
    bond (c₁ * c₂) n t =
      stagePack c₁ c₂ n (bond c₁ n (stageFst c₁ c₂ (n + 1) t))
        (bond c₂ n (stageSnd c₁ c₂ (n + 1) hc₂ t)) := by
  exact (stagePack_stageFst_stageSnd c₁ c₂ n hc₂ (bond (c₁ * c₂) n t)).symm

/-- Factorization of the bonding map on a product of finite settings.
AuthorityEffect: None. -/
theorem bond_prodSetting_factors (F G : FiniteSetting) (n : Nat)
    (t : Stage (prodSetting F G).n (n + 1)) :
    bond (prodSetting F G).n n t =
      stagePack F.n G.n n (bond F.n n (stageFst F.n G.n (n + 1) t))
        (bond G.n n (stageSnd F.n G.n (n + 1) (Nat.lt_of_le_of_lt (Nat.zero_le _) G.a_lt) t)) :=
  bond_factors_two_loci F.n G.n n (Nat.lt_of_le_of_lt (Nat.zero_le _) G.a_lt) t

/-! ## 3. Two-locus thread space as a product inverse system -/

/-- A two-locus thread projects to a compatible family (thread) at the first locus.
AuthorityEffect: None. -/
def threadFst (c₁ c₂ : Nat) (t : Thread (c₁ * c₂)) : Thread c₁ :=
  ⟨fun n => stageFst c₁ c₂ n (t.val n), fun n => by
    change stageFst c₁ c₂ n (bond (c₁ * c₂) n (t.val (n + 1))) = stageFst c₁ c₂ n (t.val n)
    rw [t.property n]⟩

/-- A two-locus thread projects to a compatible family (thread) at the second locus.
AuthorityEffect: None. -/
def threadSnd (c₁ c₂ : Nat) (hc₂ : 0 < c₂) (t : Thread (c₁ * c₂)) : Thread c₂ :=
  ⟨fun n => stageSnd c₁ c₂ n hc₂ (t.val n), fun n => by
    change stageSnd c₁ c₂ n hc₂ (bond (c₁ * c₂) n (t.val (n + 1))) = stageSnd c₁ c₂ n hc₂ (t.val n)
    rw [t.property n]⟩

/-- Two single-locus threads pack into a two-locus thread.
AuthorityEffect: None. -/
def threadPack (c₁ c₂ : Nat) (t₁ : Thread c₁) (t₂ : Thread c₂) : Thread (c₁ * c₂) :=
  ⟨fun n => stagePack c₁ c₂ n (t₁.val n) (t₂.val n), fun n => by
    change stagePack c₁ c₂ n (bond c₁ n (t₁.val (n + 1))) (bond c₂ n (t₂.val (n + 1))) =
      stagePack c₁ c₂ n (t₁.val n) (t₂.val n)
    rw [t₁.property n, t₂.property n]⟩

/-- Unpacking a packed pair of threads recovers the first thread.
AuthorityEffect: None. -/
theorem threadFst_threadPack (c₁ c₂ : Nat) (hc₂ : 0 < c₂)
    (t₁ : Thread c₁) (t₂ : Thread c₂) :
    threadFst c₁ c₂ (threadPack c₁ c₂ t₁ t₂) = t₁ := by
  apply Subtype.ext
  funext n
  exact stageFst_stagePack c₁ c₂ n hc₂ (t₁.val n) (t₂.val n)

/-- Unpacking a packed pair of threads recovers the second thread.
AuthorityEffect: None. -/
theorem threadSnd_threadPack (c₁ c₂ : Nat) (hc₂ : 0 < c₂)
    (t₁ : Thread c₁) (t₂ : Thread c₂) :
    threadSnd c₁ c₂ hc₂ (threadPack c₁ c₂ t₁ t₂) = t₂ := by
  apply Subtype.ext
  funext n
  exact stageSnd_stagePack c₁ c₂ n hc₂ (t₁.val n) (t₂.val n)

/-- Packing the two coordinate projections of a thread recovers the thread.
AuthorityEffect: None. -/
theorem threadPack_threadFst_threadSnd (c₁ c₂ : Nat) (hc₂ : 0 < c₂)
    (t : Thread (c₁ * c₂)) :
    threadPack c₁ c₂ (threadFst c₁ c₂ t) (threadSnd c₁ c₂ hc₂ t) = t := by
  apply Subtype.ext
  funext n
  exact stagePack_stageFst_stageSnd c₁ c₂ n hc₂ (t.val n)

/-- A thread over `prodSetting F G` projects to a thread over `F`.
AuthorityEffect: None. -/
def threadProdFst (F G : FiniteSetting) (t : Thread (prodSetting F G).n) : Thread F.n :=
  threadFst F.n G.n t

/-- A thread over `prodSetting F G` projects to a thread over `G`.
AuthorityEffect: None. -/
def threadProdSnd (F G : FiniteSetting) (t : Thread (prodSetting F G).n) : Thread G.n :=
  threadSnd F.n G.n (Nat.lt_of_le_of_lt (Nat.zero_le _) G.a_lt) t

/-- Threads over `F` and `G` pack into a thread over `prodSetting F G`.
AuthorityEffect: None. -/
def threadProdPack (F G : FiniteSetting) (t₁ : Thread F.n) (t₂ : Thread G.n) :
    Thread (prodSetting F G).n :=
  threadPack F.n G.n t₁ t₂

/-- Two-locus thread correspondence: projecting a packed thread recovers the first component.
AuthorityEffect: None. -/
theorem threadProdFst_pack (F G : FiniteSetting) (t₁ : Thread F.n) (t₂ : Thread G.n) :
    threadProdFst F G (threadProdPack F G t₁ t₂) = t₁ :=
  threadFst_threadPack F.n G.n (Nat.lt_of_le_of_lt (Nat.zero_le _) G.a_lt) t₁ t₂

/-- Two-locus thread correspondence: projecting a packed thread recovers the second component.
AuthorityEffect: None. -/
theorem threadProdSnd_pack (F G : FiniteSetting) (t₁ : Thread F.n) (t₂ : Thread G.n) :
    threadProdSnd F G (threadProdPack F G t₁ t₂) = t₂ :=
  threadSnd_threadPack F.n G.n (Nat.lt_of_le_of_lt (Nat.zero_le _) G.a_lt) t₁ t₂

/-- Two-locus thread correspondence: packing the two locus projections of a thread recovers the thread.
AuthorityEffect: None. -/
theorem threadProdPack_proj (F G : FiniteSetting) (t : Thread (prodSetting F G).n) :
    threadProdPack F G (threadProdFst F G t) (threadProdSnd F G t) = t :=
  threadPack_threadFst_threadSnd F.n G.n (Nat.lt_of_le_of_lt (Nat.zero_le _) G.a_lt) t

/-! ## 4. Connection to sequence space -/

/-- Pack two coordinate sequences into a sequence over the product carrier.
AuthorityEffect: None. -/
def seqPack (c₁ c₂ : Nat) (s₁ : Nat → Fin c₁) (s₂ : Nat → Fin c₂) : Nat → Fin (c₁ * c₂) :=
  fun i => ⟨pack c₂ (s₁ i).val (s₂ i).val, pack_lt (s₁ i).isLt (s₂ i).isLt⟩

/-- The sequence of a packed thread is the coordinate-wise pack of the sequences.
AuthorityEffect: None. -/
theorem thread_toSeq_pack (c₁ c₂ : Nat) (t₁ : Thread c₁) (t₂ : Thread c₂) :
    toSeq (c₁ * c₂) (threadPack c₁ c₂ t₁ t₂) =
      seqPack c₁ c₂ (toSeq c₁ t₁) (toSeq c₂ t₂) := rfl

/-- The thread of a packed sequence is the packing of the component threads.
AuthorityEffect: None. -/
theorem thread_ofSeq_pack (c₁ c₂ : Nat) (s₁ : Nat → Fin c₁) (s₂ : Nat → Fin c₂) :
    ofSeq (c₁ * c₂) (seqPack c₁ c₂ s₁ s₂) =
      threadPack c₁ c₂ (ofSeq c₁ s₁) (ofSeq c₂ s₂) := rfl

/-- Project a sequence over a product carrier to its first coordinate sequence.
AuthorityEffect: None. -/
def seqFst (c₁ c₂ : Nat) (s : Nat → Fin (c₁ * c₂)) : Nat → Fin c₁ :=
  fun i => ⟨fstOf c₂ (s i).val, fst_lt (s i).isLt⟩

/-- Project a sequence over a product carrier to its second coordinate sequence.
AuthorityEffect: None. -/
def seqSnd (c₁ c₂ : Nat) (hc₂ : 0 < c₂) (s : Nat → Fin (c₁ * c₂)) : Nat → Fin c₂ :=
  fun i => ⟨sndOf c₂ (s i).val, snd_lt hc₂⟩

/-- Projecting a packed sequence to the first coordinate recovers the first sequence.
AuthorityEffect: None. -/
theorem seqFst_seqPack (c₁ c₂ : Nat) (hc₂ : 0 < c₂)
    (s₁ : Nat → Fin c₁) (s₂ : Nat → Fin c₂) :
    seqFst c₁ c₂ (seqPack c₁ c₂ s₁ s₂) = s₁ := by
  funext i
  apply Fin.ext
  exact fst_pack hc₂ (s₂ i).isLt

/-- Projecting a packed sequence to the second coordinate recovers the second sequence.
AuthorityEffect: None. -/
theorem seqSnd_seqPack (c₁ c₂ : Nat) (hc₂ : 0 < c₂)
    (s₁ : Nat → Fin c₁) (s₂ : Nat → Fin c₂) :
    seqSnd c₁ c₂ hc₂ (seqPack c₁ c₂ s₁ s₂) = s₂ := by
  funext i
  apply Fin.ext
  exact snd_pack (s₂ i).isLt

/-- Packing the two coordinate projections of a sequence recovers the sequence.
AuthorityEffect: None. -/
theorem seqPack_seqFst_seqSnd (c₁ c₂ : Nat) (hc₂ : 0 < c₂)
    (s : Nat → Fin (c₁ * c₂)) :
    seqPack c₁ c₂ (seqFst c₁ c₂ s) (seqSnd c₁ c₂ hc₂ s) = s := by
  funext i
  apply Fin.ext
  exact Nat.div_add_mod (s i).val c₂

/-! ## 5. Locus-wise observation compatibility of runs -/

/-- The first-locus projection of an observation prefix-bonds to the next scale.
AuthorityEffect: None. -/
theorem obs_locus1_prefix (m n : Nat) (s : State) :
    locus1 m (obs n s) <+: locus1 m (obs (n + 1) s) :=
  (obs_prefix n s).map (fstOf m)

/-- The second-locus projection of an observation prefix-bonds to the next scale.
AuthorityEffect: None. -/
theorem obs_locus2_prefix (m n : Nat) (s : State) :
    locus2 m (obs n s) <+: locus2 m (obs (n + 1) s) :=
  (obs_prefix n s).map (sndOf m)

/-- The first-locus projection of an observation prefix-bonds across any scale difference.
AuthorityEffect: None. -/
theorem obs_locus1_prefix_add (m n k : Nat) (s : State) :
    locus1 m (obs n s) <+: locus1 m (obs (n + k) s) :=
  (obs_prefix_add n s k).map (fstOf m)

/-- The second-locus projection of an observation prefix-bonds across any scale difference.
AuthorityEffect: None. -/
theorem obs_locus2_prefix_add (m n k : Nat) (s : State) :
    locus2 m (obs n s) <+: locus2 m (obs (n + k) s) :=
  (obs_prefix_add n s k).map (sndOf m)

/-- Locus-wise observation compatibility: along any two-locus run, the observed
tape at scale `n` projects at locus 1 to a prefix of the projection at scale `n + k`.
AuthorityEffect: None. -/
theorem two_locus_run_obs_compat_locus1 (F G : FiniteSetting) (sched : Nat → Nat)
    (x fuel n k : Nat) :
    locus1 G.n (obs n (Control.init (twoLocus F G sched) x fuel)) <+:
      locus1 G.n (obs (n + k) (Control.init (twoLocus F G sched) x fuel)) :=
  obs_locus1_prefix_add G.n n k (Control.init (twoLocus F G sched) x fuel)

/-- Locus-wise observation compatibility: along any two-locus run, the observed
tape at scale `n` projects at locus 2 to a prefix of the projection at scale `n + k`.
AuthorityEffect: None. -/
theorem two_locus_run_obs_compat_locus2 (F G : FiniteSetting) (sched : Nat → Nat)
    (x fuel n k : Nat) :
    locus2 G.n (obs n (Control.init (twoLocus F G sched) x fuel)) <+:
      locus2 G.n (obs (n + k) (Control.init (twoLocus F G sched) x fuel)) :=
  obs_locus2_prefix_add G.n n k (Control.init (twoLocus F G sched) x fuel)

end TwoLociSystem

#print axioms TwoLociSystem.stageFst_stagePack
#print axioms TwoLociSystem.stageSnd_stagePack
#print axioms TwoLociSystem.stagePack_stageFst_stageSnd
#print axioms TwoLociSystem.stageFst_bond
#print axioms TwoLociSystem.stageSnd_bond
#print axioms TwoLociSystem.stagePack_bond
#print axioms TwoLociSystem.bond_factors_two_loci
#print axioms TwoLociSystem.bond_prodSetting_factors
#print axioms TwoLociSystem.threadFst_threadPack
#print axioms TwoLociSystem.threadSnd_threadPack
#print axioms TwoLociSystem.threadPack_threadFst_threadSnd
#print axioms TwoLociSystem.threadProdFst_pack
#print axioms TwoLociSystem.threadProdSnd_pack
#print axioms TwoLociSystem.threadProdPack_proj
#print axioms TwoLociSystem.thread_toSeq_pack
#print axioms TwoLociSystem.thread_ofSeq_pack
#print axioms TwoLociSystem.seqFst_seqPack
#print axioms TwoLociSystem.seqSnd_seqPack
#print axioms TwoLociSystem.seqPack_seqFst_seqSnd
#print axioms TwoLociSystem.obs_locus1_prefix
#print axioms TwoLociSystem.obs_locus2_prefix
#print axioms TwoLociSystem.obs_locus1_prefix_add
#print axioms TwoLociSystem.obs_locus2_prefix_add
#print axioms TwoLociSystem.two_locus_run_obs_compat_locus1
#print axioms TwoLociSystem.two_locus_run_obs_compat_locus2
