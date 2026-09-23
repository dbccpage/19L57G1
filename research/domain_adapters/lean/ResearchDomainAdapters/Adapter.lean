import ResearchNativeBridge.Sim

/-!
# Domain adapters: declared maps into the passage, and what they must satisfy

AuthorityEffect: None.  An adapter declares four things about an imported
domain:

* its carrier, events and step;
* its observation;
* a commuting translation of its step into the sealed passage step;
* an observation map with a commuting observation square.

Nothing an adapter declares is attributed to the sealed seed.  Its laws are
fields, and every field must be supplied with a proof.

Proved here:

* `Sim.comp`, `comp_enc`: commuting translations compose.
* `Adapter.replay_obs`: for every source path, the lifted native path
  ends at the encoded end state, and the native observation of that state
  is the mapped source observation.  This is the replay square together
  with the observation square.
* `swap_core`: a source step that returns to its start in two steps
  (`g (g s e) e = s`) forces every translation into the passage to give
  both states the same core.  A reversible domain can be carried only by
  budget and license, whatever its encoding.
-/

namespace ResearchDomainAdapters

open PrimitivePassage ResearchNativeBridge

/-- Commuting translations compose. -/
def Sim.comp {S E σ ε τ δ : Type} {g : S → E → S} {f : σ → ε → σ} {h : τ → δ → τ}
    (m₁ : Sim g f) (m₂ : Sim f h) : Sim g h where
  enc := fun s => m₂.enc (m₁.enc s)
  tr := fun s e => m₂.trHist (m₁.enc s) (m₁.tr s e)
  comm := fun s e => by
    show run h (m₂.trHist (m₁.enc s) (m₁.tr s e)) (m₂.enc (m₁.enc s)) = m₂.enc (m₁.enc (g s e))
    rw [Sim.run_trHist, m₁.comm]

theorem comp_enc {S E σ ε τ δ : Type} {g : S → E → S} {f : σ → ε → σ} {h : τ → δ → τ}
    (m₁ : Sim g f) (m₂ : Sim f h) (s : S) : (Sim.comp m₁ m₂).enc s = m₂.enc (m₁.enc s) := rfl

/-- A domain adapter into the passage. -/
structure Adapter {S E O O' : Type} (g : S → E → S) (obsA : S → O) (obsN : PState → O') where
  sim : Sim g step
  obsMap : O → O'
  obs_comm : ∀ s, obsN (sim.enc s) = obsMap (obsA s)

theorem Adapter.replay_obs {S E O O' : Type} {g : S → E → S} {obsA : S → O}
    {obsN : PState → O'} (A : Adapter g obsA obsN) {s t : S} (τ : Path g s t) :
    replayP (Path.events (A.sim.lift τ)) (A.sim.enc s) = A.sim.enc t ∧
      obsN (A.sim.enc t) = A.obsMap (obsA t) :=
  ⟨Path.run_events _, A.obs_comm t⟩

/-- **Reversible steps collapse to budget and license.** -/
theorem swap_core {S E : Type} {g : S → E → S} (m : Sim g step) (s : S) (e : E)
    (hback : g (g s e) e = s) : core (m.enc (g s e)) = core (m.enc s) :=
  passage_sim_cycle m (Path.cons e (Path.nil _)) (Path.ofSub ⟨[e], hback⟩)

end ResearchDomainAdapters
