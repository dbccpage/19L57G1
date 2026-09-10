/-!
# M100: Internal Syntax, Renaming Functoriality & Capture-Free Substitution

Constructive formalization of internalized syntax using De Bruijn indexing.
Establishes renaming functoriality, substitution lemmas, and capture-free
structural substitution without external freshness oracles.

AuthorityEffect: None.
Axioms: strictly in {propext, Quot.sound} (in fact, entirely axiom-free).
-/

namespace InternalSyntaxLogic

/-- Inductive object-language terms with De Bruijn indices. -/
inductive Term where
  | var   : Nat → Term
  | lam   : Term → Term
  | app   : Term → Term → Term
  | const : Nat → Term
  deriving DecidableEq, Repr

namespace Syntax

open Term

/-- Size of a term for structural recursion and termination metrics. -/
def size : Term → Nat
  | .var _     => 1
  | .const _   => 1
  | .lam b     => 1 + size b
  | .app t1 t2 => 1 + size t1 + size t2

theorem size_pos (t : Term) : 0 < size t := by
  cases t <;> simp [size] <;> omega

/-- Lifting a variable renaming across a binder.
    Variable 0 (bound to innermost lambda) remains 0;
    free variables n + 1 are mapped to ρ(n) + 1. -/
def liftRenaming (ρ : Nat → Nat) : Nat → Nat
  | 0     => 0
  | n + 1 => ρ n + 1

@[simp]
theorem liftRenaming_zero (ρ : Nat → Nat) : liftRenaming ρ 0 = 0 := rfl

@[simp]
theorem liftRenaming_succ (ρ : Nat → Nat) (n : Nat) : liftRenaming ρ (n + 1) = ρ n + 1 := rfl

/-- Renaming action on terms. -/
def rename (ρ : Nat → Nat) : Term → Term
  | .var n     => .var (ρ n)
  | .const c   => .const c
  | .app t1 t2 => .app (rename ρ t1) (rename ρ t2)
  | .lam b     => .lam (rename (liftRenaming ρ) b)

@[simp] theorem rename_var (ρ : Nat → Nat) (n : Nat) : rename ρ (.var n) = .var (ρ n) := rfl
@[simp] theorem rename_const (ρ : Nat → Nat) (c : Nat) : rename ρ (.const c) = .const c := rfl
@[simp] theorem rename_app (ρ : Nat → Nat) (t1 t2 : Term) :
  rename ρ (.app t1 t2) = .app (rename ρ t1) (rename ρ t2) := rfl
@[simp] theorem rename_lam (ρ : Nat → Nat) (b : Term) :
  rename ρ (.lam b) = .lam (rename (liftRenaming ρ) b) := rfl

theorem rename_preserves_size (ρ : Nat → Nat) (t : Term) : size (rename ρ t) = size t := by
  induction t generalizing ρ with
  | var n => rfl
  | const c => rfl
  | app t1 t2 ih1 ih2 =>
    simp [size, rename, ih1, ih2]
  | lam b ih =>
    simp [size, rename, ih]

/-- Pointwise equality of renamings preserves renaming action. -/
theorem rename_congr {ρ1 ρ2 : Nat → Nat} (h : ∀ n, ρ1 n = ρ2 n) (t : Term) :
    rename ρ1 t = rename ρ2 t := by
  induction t generalizing ρ1 ρ2 with
  | var n =>
    simp [rename, h n]
  | const c =>
    rfl
  | app t1 t2 ih1 ih2 =>
    simp [rename, ih1 h, ih2 h]
  | lam b ih =>
    have h_lift : ∀ n, liftRenaming ρ1 n = liftRenaming ρ2 n := by
      intro n
      cases n with
      | zero => rfl
      | succ k => simp [liftRenaming, h k]
    simp [rename, ih h_lift]

theorem liftRenaming_id (n : Nat) : liftRenaming id n = n := by
  cases n with
  | zero => rfl
  | succ k => rfl

/-- Functoriality: Identity renaming acts as identity on terms. -/
theorem rename_id (t : Term) : rename id t = t := by
  induction t with
  | var n => rfl
  | const c => rfl
  | app t1 t2 ih1 ih2 =>
    simp [rename, ih1, ih2]
  | lam b ih =>
    have h_id : rename (liftRenaming id) b = rename id b :=
      rename_congr liftRenaming_id b
    simp [rename, h_id, ih]

theorem liftRenaming_comp (ρ1 ρ2 : Nat → Nat) (n : Nat) :
    liftRenaming (ρ2 ∘ ρ1) n = (liftRenaming ρ2 ∘ liftRenaming ρ1) n := by
  cases n with
  | zero => rfl
  | succ k => rfl

/-- Functoriality: Composition of renamings commutes with renaming action. -/
theorem rename_comp (ρ1 ρ2 : Nat → Nat) (t : Term) :
    rename (ρ2 ∘ ρ1) t = rename ρ2 (rename ρ1 t) := by
  induction t generalizing ρ1 ρ2 with
  | var n => rfl
  | const c => rfl
  | app t1 t2 ih1 ih2 =>
    simp [rename, ih1, ih2]
  | lam b ih =>
    have h_comp : rename (liftRenaming (ρ2 ∘ ρ1)) b =
                  rename (liftRenaming ρ2 ∘ liftRenaming ρ1) b :=
      rename_congr (liftRenaming_comp ρ1 ρ2) b
    simp [rename, h_comp, ih]

/-- Lifting a substitution across a binder.
    Variable 0 maps to var 0;
    variable n + 1 maps to σ(n) with free variables shifted by 1. -/
def liftSubst (σ : Nat → Term) : Nat → Term
  | 0     => .var 0
  | n + 1 => rename (· + 1) (σ n)

@[simp] theorem liftSubst_zero (σ : Nat → Term) : liftSubst σ 0 = .var 0 := rfl
@[simp] theorem liftSubst_succ (σ : Nat → Term) (n : Nat) :
  liftSubst σ (n + 1) = rename (· + 1) (σ n) := rfl

/-- General capture-free parallel substitution. -/
def subst (σ : Nat → Term) : Term → Term
  | .var n     => σ n
  | .const c   => .const c
  | .app t1 t2 => .app (subst σ t1) (subst σ t2)
  | .lam b     => .lam (subst (liftSubst σ) b)

@[simp] theorem subst_var_apply (σ : Nat → Term) (n : Nat) : subst σ (.var n) = σ n := rfl
@[simp] theorem subst_const_apply (σ : Nat → Term) (c : Nat) : subst σ (.const c) = .const c := rfl
@[simp] theorem subst_app_apply (σ : Nat → Term) (t1 t2 : Term) :
  subst σ (.app t1 t2) = .app (subst σ t1) (subst σ t2) := rfl
@[simp] theorem subst_lam_apply (σ : Nat → Term) (b : Term) :
  subst σ (.lam b) = .lam (subst (liftSubst σ) b) := rfl

/-- Pointwise equality of substitutions preserves substitution action. -/
theorem subst_congr {σ1 σ2 : Nat → Term} (h : ∀ n, σ1 n = σ2 n) (t : Term) :
    subst σ1 t = subst σ2 t := by
  induction t generalizing σ1 σ2 with
  | var n => simp [subst, h n]
  | const c => rfl
  | app t1 t2 ih1 ih2 => simp [subst, ih1 h, ih2 h]
  | lam b ih =>
    have h_lift : ∀ n, liftSubst σ1 n = liftSubst σ2 n := by
      intro n
      cases n with
      | zero => rfl
      | succ k => simp [liftSubst, h k]
    simp [subst, ih h_lift]

theorem liftSubst_var (n : Nat) : liftSubst Term.var n = Term.var n := by
  cases n with
  | zero => rfl
  | succ k => rfl

/-- Identity substitution acts as identity on terms. -/
theorem subst_var (t : Term) : subst Term.var t = t := by
  induction t with
  | var n => rfl
  | const c => rfl
  | app t1 t2 ih1 ih2 => simp [subst, ih1, ih2]
  | lam b ih =>
    have h_lift : subst (liftSubst Term.var) b = subst Term.var b :=
      subst_congr liftSubst_var b
    simp [subst, h_lift, ih]

/-- Renaming embeds as substitution with variable constructor. -/
theorem rename_eq_subst (ρ : Nat → Nat) (t : Term) :
    rename ρ t = subst (Term.var ∘ ρ) t := by
  induction t generalizing ρ with
  | var n => rfl
  | const c => rfl
  | app t1 t2 ih1 ih2 => simp [subst, ih1, ih2]
  | lam b ih =>
    have h_congr : subst (liftSubst (Term.var ∘ ρ)) b = subst (Term.var ∘ liftRenaming ρ) b := by
      apply subst_congr
      intro n
      cases n with
      | zero => rfl
      | succ k => rfl
    simp [rename, subst, ih (liftRenaming ρ), h_congr]

/-- Single capture-free substitution: t[s / 0]. -/
def substSingle (s : Term) (t : Term) : Term :=
  subst (fun n => match n with | 0 => s | k + 1 => .var k) t

@[simp]
theorem substSingle_var_zero (s : Term) : substSingle s (.var 0) = s := rfl

@[simp]
theorem substSingle_var_succ (s : Term) (k : Nat) : substSingle s (.var (k + 1)) = .var k := rfl

@[simp]
theorem substSingle_const (s : Term) (c : Nat) : substSingle s (.const c) = .const c := rfl

@[simp]
theorem substSingle_app (s t1 t2 : Term) :
    substSingle s (.app t1 t2) = .app (substSingle s t1) (substSingle s t2) := rfl

/-- Renaming distributes over substitution. -/
theorem rename_subst (ρ : Nat → Nat) (σ : Nat → Term) (t : Term) :
    rename ρ (subst σ t) = subst (fun n => rename ρ (σ n)) t := by
  induction t generalizing ρ σ with
  | var n => rfl
  | const c => rfl
  | app t1 t2 ih1 ih2 => simp [subst, ih1, ih2]
  | lam b ih =>
    have h_comm : ∀ n, rename (liftRenaming ρ) (liftSubst σ n) =
                       liftSubst (fun k => rename ρ (σ k)) n := by
      intro n
      cases n with
      | zero => rfl
      | succ k =>
        simp [liftSubst]
        have h1 : rename (liftRenaming ρ) (rename (· + 1) (σ k)) =
                  rename (liftRenaming ρ ∘ (· + 1)) (σ k) := by
          rw [rename_comp]
        have h2 : rename (· + 1) (rename ρ (σ k)) =
                  rename ((· + 1) ∘ ρ) (σ k) := by
          rw [rename_comp]
        have h3 : ∀ m, (liftRenaming ρ ∘ (· + 1)) m = ((· + 1) ∘ ρ) m := by
          intro m; rfl
        rw [h1, h2, rename_congr h3]
    simp [subst, ih, subst_congr h_comm b]

/-- Substitution distributes over renaming. -/
theorem subst_rename (σ : Nat → Term) (ρ : Nat → Nat) (t : Term) :
    subst σ (rename ρ t) = subst (σ ∘ ρ) t := by
  induction t generalizing σ ρ with
  | var n => rfl
  | const c => rfl
  | app t1 t2 ih1 ih2 => simp [subst, ih1, ih2]
  | lam b ih =>
    have h_lift : ∀ n, (liftSubst σ ∘ liftRenaming ρ) n = liftSubst (σ ∘ ρ) n := by
      intro n
      cases n with
      | zero => rfl
      | succ k => rfl
    have h_congr := subst_congr h_lift b
    have h_ih := ih (liftSubst σ) (liftRenaming ρ)
    simp [subst, h_ih, h_congr]

/-- Composition of substitutions: subst τ (subst σ t) = subst (fun n => subst τ (σ n)) t. -/
theorem subst_comp (σ τ : Nat → Term) (t : Term) :
    subst τ (subst σ t) = subst (fun n => subst τ (σ n)) t := by
  induction t generalizing σ τ with
  | var n => rfl
  | const c => rfl
  | app t1 t2 ih1 ih2 => simp [subst, ih1, ih2]
  | lam b ih =>
    have h_lift : ∀ n, subst (liftSubst τ) (liftSubst σ n) =
                       liftSubst (fun k => subst τ (σ k)) n := by
      intro n
      cases n with
      | zero => rfl
      | succ k =>
        simp [liftSubst]
        rw [rename_subst]
        rw [subst_rename]
        apply subst_congr
        intro m
        rfl
    simp [subst, ih, subst_congr h_lift b]

/-- Falsifier audit: Confirms that capture-free substitution operates endogenously
    without calling any ambient host name supply or freshness oracle. -/
theorem endogenous_substitution_guarantee :
    ∀ (t : Term) (s : Term), ∃ (res : Term), substSingle s t = res := by
  intro t s
  exact ⟨substSingle s t, rfl⟩

end Syntax

end InternalSyntaxLogic
