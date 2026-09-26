/-!
# The capability census of the declared engine class

Native to continuation one.

The declared class of `PROMPT.md`, as a finite object: nine rules (rung
two's E-one to E-nine, with the observables rung two says each reads),
two measures, two validity members and the four subsets of the two
continuation rules.  A member's CAPABILITIES are the three skeleton
capabilities every engine declares, each observable its rule reads, its
measure, each clause of its validity member, and each continuation rule
it holds.  Its COUNT is the length of that list; `count2` reads growth as
two capabilities, a trigger and an admission.

Every theorem here is about DECLARATIONS.  A count says nothing of what
an engine does; the probe in the Python of this tree does that, to level
two, and this module does not mirror it.

* `class_size`, `literal_size`: one hundred and forty-four members, one
  hundred and eight holding at least one continuation rule.
* `count_ge_six`, `count_six_members`: every count is at least six, and
  sixteen members have six.
* `literal_count_ge_seven`, `literal_count_seven_members`,
  `literal_count2_seven_members`: in the seed-literal subclass every
  count is at least seven, thirty-two have seven, and sixteen have seven
  when growth counts two.
* `no_one_declaration`: no member's count is one, so no member is one
  declaration.
* `same_caps_e3_e4`: the members reading E-three and E-four, alike
  elsewhere, declare one capability list -- a count cannot tell two
  rules reading one observable apart.
* `no_initial`: no member's capabilities lie inside every member's.
* `no_initial_of_two_measures`: in any list of members holding members
  of both measures, no member's capabilities lie inside every member's.

The morphisms of this reading are inclusions of declarations and nothing
else; the refusal of an initial member is scoped to it.

AuthorityEffect: None.
-/

namespace SecondEngine
namespace Census

/-- Rung two's nine rules. -/
inductive Rule
  | e1 | e2 | e3 | e4 | e5 | e6 | e7 | e8 | e9
  deriving DecidableEq, Repr

/-- Rung two's six observables. -/
inductive Obs
  | o1 | o2 | o3 | o4 | o5 | o6
  deriving DecidableEq, Repr

/-- The observables each rule reads, as rung two counts them. -/
def Rule.obs : Rule → List Obs
  | .e1 => [.o1]
  | .e2 => [.o2]
  | .e3 => [.o4]
  | .e4 => [.o4]
  | .e5 => [.o3]
  | .e6 => [.o3, .o4]
  | .e7 => [.o2]
  | .e8 => [.o6]
  | .e9 => [.o5]

/-- The capabilities a declaration can name. -/
inductive Cap
  | demandRead | leastResponse | replay
  | obs (o : Obs)
  | mu1 | mu2
  | noRegress | introducedHonoured
  | growth | switch
  deriving DecidableEq, Repr

/-- A member of the class: its rule, whether its measure is the second,
whether its validity is member two, and which continuation rules it
holds. -/
structure Decl where
  rule : Rule
  mu2 : Bool
  strict : Bool
  growth : Bool
  switch : Bool
  deriving DecidableEq, Repr

/-- The capability list of a declaration. -/
def Decl.caps (e : Decl) : List Cap :=
  [.demandRead, .leastResponse, .replay] ++ e.rule.obs.map Cap.obs ++
    [if e.mu2 then .mu2 else .mu1] ++
    (if e.strict then [.noRegress, .introducedHonoured] else [.noRegress]) ++
    (if e.growth then [.growth] else []) ++
    (if e.switch then [.switch] else [])

/-- The count of a declaration. -/
def Decl.count (e : Decl) : Nat := e.caps.length

/-- The count with growth read as two capabilities. -/
def Decl.count2 (e : Decl) : Nat := e.count + (if e.growth then 1 else 0)

/-- A member of the seed-literal subclass holds a continuation rule. -/
def Decl.literal (e : Decl) : Bool := e.growth || e.switch

def allRules : List Rule := [.e1, .e2, .e3, .e4, .e5, .e6, .e7, .e8, .e9]

def bools : List Bool := [false, true]

/-- The declared class. -/
def classList : List Decl :=
  allRules.flatMap fun r => bools.flatMap fun m => bools.flatMap fun v =>
    bools.flatMap fun g => bools.map fun w => ⟨r, m, v, g, w⟩

/-- The seed-literal subclass. -/
def literalList : List Decl := classList.filter Decl.literal

theorem class_size : classList.length = 144 := by decide +kernel

theorem literal_size : literalList.length = 108 := by decide +kernel

theorem count_ge_six (e : Decl) : 6 ≤ e.count := by
  obtain ⟨r, m, v, g, w⟩ := e
  cases r <;> cases m <;> cases v <;> cases g <;> cases w <;> decide

theorem count_six_members : (classList.filter fun e => e.count == 6).length = 16 := by
  decide +kernel

theorem literal_count_ge_seven (e : Decl) (h : e.literal = true) : 7 ≤ e.count := by
  revert h
  obtain ⟨r, m, v, g, w⟩ := e
  cases r <;> cases m <;> cases v <;> cases g <;> cases w <;> decide

theorem literal_count_seven_members :
    (literalList.filter fun e => e.count == 7).length = 32 := by
  decide +kernel

theorem literal_count2_seven_members :
    (literalList.filter fun e => e.count2 == 7).length = 16 := by
  decide +kernel

/-- No member of the class is one declaration. -/
theorem no_one_declaration (e : Decl) : e.count ≠ 1 := by
  intro h
  have h6 := count_ge_six e
  rw [h] at h6
  exact absurd h6 (by decide)

/-- Two members alike but for reading E-three or E-four declare one
capability list. -/
theorem same_caps_e3_e4 (m v g w : Bool) :
    (Decl.mk .e3 m v g w).caps = (Decl.mk .e4 m v g w).caps := by
  cases m <;> cases v <;> cases g <;> cases w <;> rfl

/-- No member's capabilities lie inside every member's: the one reading
E-one and the one reading E-two, alike elsewhere, share no observable,
and every member reads one. -/
theorem no_initial : ¬ ∃ e : Decl, ∀ e' : Decl, ∀ c ∈ e.caps, c ∈ e'.caps := by
  rintro ⟨e, he⟩
  have hmem : ∀ d : Decl, Cap.obs (d.rule.obs.headD .o1) ∈ d.caps := by
    intro d
    obtain ⟨r, m, v, g, w⟩ := d
    cases r <;> cases m <;> cases v <;> cases g <;> cases w <;> decide
  have hboth : ∀ o : Obs, Cap.obs o ∈ (Decl.mk .e1 false false false false).caps →
      Cap.obs o ∈ (Decl.mk .e2 false false false false).caps → False := by
    intro o
    cases o <;> decide
  exact hboth _ (he _ _ (hmem e)) (he _ _ (hmem e))

/-- In any list of members holding members of both measures, no member's
capabilities lie inside every member's: its measure is missing from the
members of the other. -/
theorem no_initial_of_two_measures (P : List Decl) (e₁ e₂ : Decl) (h₁ : e₁ ∈ P)
    (h₂ : e₂ ∈ P) (hm : e₁.mu2 ≠ e₂.mu2) :
    ¬ ∃ e ∈ P, ∀ e' ∈ P, ∀ c ∈ e.caps, c ∈ e'.caps := by
  rintro ⟨e, _, he⟩
  have hmeas : ∀ d : Decl, (if d.mu2 then Cap.mu2 else Cap.mu1) ∈ d.caps := by
    intro d
    obtain ⟨r, m, v, g, w⟩ := d
    cases r <;> cases m <;> cases v <;> cases g <;> cases w <;> decide
  have hone : ∀ (b : Bool) (d' : Decl), (if b then Cap.mu2 else Cap.mu1) ∈ d'.caps →
      d'.mu2 = b := by
    intro b d'
    obtain ⟨r', m', v', g', w'⟩ := d'
    cases b <;> cases m' <;> cases r' <;> cases v' <;> cases g' <;> cases w' <;> decide
  have e1m := hone e.mu2 e₁ (he e₁ h₁ _ (hmeas e))
  have e2m := hone e.mu2 e₂ (he e₂ h₂ _ (hmeas e))
  exact hm (e1m.trans e2m.symm)

end Census
end SecondEngine
