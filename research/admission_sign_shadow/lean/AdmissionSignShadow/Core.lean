import Std

namespace AdmissionSignShadow

inductive HistoryClass where
  | forward
  | reversed
deriving DecidableEq, Repr

def exchange : HistoryClass → HistoryClass
  | .forward => .reversed
  | .reversed => .forward

def erasedEndpoint : HistoryClass → Unit := fun _ => ()

theorem histories_distinct : HistoryClass.forward ≠ HistoryClass.reversed := by
  decide

theorem same_erased_endpoint :
    erasedEndpoint HistoryClass.forward = erasedEndpoint HistoryClass.reversed := by
  rfl

theorem exchange_involutive (h : HistoryClass) : exchange (exchange h) = h := by
  cases h <;> rfl

theorem exchange_has_no_fixed_point (h : HistoryClass) : exchange h ≠ h := by
  cases h <;> decide

def act (bit : Bool) (h : HistoryClass) : HistoryClass :=
  if bit then exchange h else h

theorem act_identity (h : HistoryClass) : act false h = h := by
  rfl

theorem act_composition (a b : Bool) (h : HistoryClass) :
    act (xor a b) h = act a (act b h) := by
  cases a <;> cases b <;> cases h <;> rfl

theorem unique_transporter (left right : HistoryClass) :
    ∃ bit : Bool, act bit left = right ∧
      ∀ other : Bool, act other left = right → other = bit := by
  cases left <;> cases right
  · exact ⟨false, rfl, by intro bit h; cases bit <;> simp [act, exchange] at h ⊢⟩
  · exact ⟨true, rfl, by intro bit h; cases bit <;> simp [act, exchange] at h ⊢⟩
  · exact ⟨true, rfl, by intro bit h; cases bit <;> simp [act, exchange] at h ⊢⟩
  · exact ⟨false, rfl, by intro bit h; cases bit <;> simp [act, exchange] at h ⊢⟩

inductive Polarity where
  | positive
  | negative
deriving DecidableEq, Repr

namespace Polarity

def mul : Polarity → Polarity → Polarity
  | .positive, value => value
  | .negative, .positive => .negative
  | .negative, .negative => .positive

def neg : Polarity → Polarity
  | .positive => .negative
  | .negative => .positive

def toInt : Polarity → Int
  | .positive => 1
  | .negative => -1

theorem toInt_mul (a b : Polarity) : toInt (mul a b) = toInt a * toInt b := by
  cases a <;> cases b <;> decide

end Polarity

structure ExchangeCharacter where
  map : Bool → Polarity
  identity : map false = .positive
  multiplicative : ∀ a b, map (xor a b) = Polarity.mul (map a) (map b)

def trivialCharacter : ExchangeCharacter where
  map := fun _ => .positive
  identity := rfl
  multiplicative := by intro a b; cases a <;> cases b <;> rfl

def signCharacter : ExchangeCharacter where
  map := fun bit => if bit then .negative else .positive
  identity := rfl
  multiplicative := by intro a b; cases a <;> cases b <;> rfl

def OperationalNontrivial (c : ExchangeCharacter) : Prop := c.map true ≠ .positive

theorem character_classification (c : ExchangeCharacter) :
    (∀ bit, c.map bit = trivialCharacter.map bit) ∨
      (∀ bit, c.map bit = signCharacter.map bit) := by
  cases h : c.map true with
  | positive =>
      left
      intro bit
      cases bit
      · simpa [trivialCharacter] using c.identity
      · simpa [trivialCharacter] using h
  | negative =>
      right
      intro bit
      cases bit
      · simpa [signCharacter] using c.identity
      · simpa [signCharacter] using h

theorem trivial_and_sign_are_characters :
    trivialCharacter.map false = .positive ∧
      trivialCharacter.map true = .positive ∧
      signCharacter.map false = .positive ∧ signCharacter.map true = .negative := by
  decide

theorem character_laws_do_not_force_nontrivial : ¬ OperationalNontrivial trivialCharacter := by
  simp [OperationalNontrivial, trivialCharacter]

theorem nontrivial_exchange_is_negative (c : ExchangeCharacter)
    (h : OperationalNontrivial c) : c.map true = .negative := by
  cases hc : c.map true with
  | positive => exact False.elim (h hc)
  | negative => rfl

theorem nontrivial_character_unique (c : ExchangeCharacter)
    (h : OperationalNontrivial c) : ∀ bit, c.map bit = signCharacter.map bit := by
  intro bit
  cases bit
  · simpa [signCharacter] using c.identity
  · simpa [signCharacter] using nontrivial_exchange_is_negative c h

theorem nontrivial_exchange_toInt (c : ExchangeCharacter)
    (h : OperationalNontrivial c) : Polarity.toInt (c.map true) = -1 := by
  rw [nontrivial_exchange_is_negative c h]
  rfl

def transporter : HistoryClass → HistoryClass → Bool
  | .forward, .forward => false
  | .forward, .reversed => true
  | .reversed, .forward => true
  | .reversed, .reversed => false

def relativeValue (c : ExchangeCharacter) (base h : HistoryClass) : Polarity :=
  c.map (transporter base h)

theorem operational_nontrivial_iff_labels_separate (c : ExchangeCharacter)
    (base : HistoryClass) :
    OperationalNontrivial c ↔
      relativeValue c base (exchange base) ≠ relativeValue c base base := by
  cases base <;> simp [OperationalNontrivial, relativeValue, transporter, exchange, c.identity]

theorem sign_exchange_relative (base h : HistoryClass) :
    relativeValue signCharacter base (exchange h) =
      Polarity.neg (relativeValue signCharacter base h) := by
  cases base <;> cases h <;> rfl

theorem sign_global_basepoint_flip (h : HistoryClass) :
    relativeValue signCharacter HistoryClass.forward h =
      Polarity.neg (relativeValue signCharacter HistoryClass.reversed h) := by
  cases h <;> rfl

def IsRelativeLabel (label : HistoryClass → Polarity) : Prop :=
  ∀ h, label (exchange h) = Polarity.neg (label h)

def forwardPositive : HistoryClass → Polarity
  | .forward => .positive
  | .reversed => .negative

def forwardNegative : HistoryClass → Polarity
  | .forward => .negative
  | .reversed => .positive

theorem relative_label_classification (label : HistoryClass → Polarity)
    (hrel : IsRelativeLabel label) :
    (∀ h, label h = forwardPositive h) ∨
      (∀ h, label h = forwardNegative h) := by
  cases hf : label .forward with
  | positive =>
      left
      intro h
      cases h
      · exact hf
      · have hs := hrel .forward
        simpa [exchange, Polarity.neg, forwardPositive, hf] using hs
  | negative =>
      right
      intro h
      cases h
      · exact hf
      · have hs := hrel .forward
        simpa [exchange, Polarity.neg, forwardNegative, hf] using hs

theorem relative_label_unique_after_basepoint (label : HistoryClass → Polarity)
    (hrel : IsRelativeLabel label) (hbase : label .forward = .positive) :
    ∀ h, label h = forwardPositive h := by
  rcases relative_label_classification label hrel with h | h
  · exact h
  · have contradiction : Polarity.negative = Polarity.positive := by
      exact (h .forward).symm.trans hbase
    exact False.elim (by cases contradiction)

theorem global_neg_preserves_relative (label : HistoryClass → Polarity)
    (hrel : IsRelativeLabel label) :
    IsRelativeLabel (fun h => Polarity.neg (label h)) := by
  intro h
  have step := hrel h
  cases hv : label h <;> simp [Polarity.neg, hv] at step ⊢ <;>
    cases hw : label (exchange h) <;> simp [hw] at step ⊢

structure Occurrence where
  id : Nat
  token : Nat
deriving DecidableEq, Repr

def ids (h : List Occurrence) : List Nat := h.map Occurrence.id
def OccurrenceValid (h : List Occurrence) : Prop := (ids h).Nodup

def IdsDisjoint (left right : List Occurrence) : Prop :=
  ∀ identifier ∈ ids left, identifier ∉ ids right

theorem nodup_append_of_disjoint {α : Type} {left right : List α}
    (hleft : left.Nodup) (hright : right.Nodup)
    (hdisjoint : ∀ value ∈ left, value ∉ right) : (left ++ right).Nodup := by
  induction left with
  | nil => exact hright
  | cons value rest ih =>
      have hhead : value ∉ rest := by
        intro hmem
        exact (List.nodup_cons.mp hleft).1 hmem
      have htail : rest.Nodup := (List.nodup_cons.mp hleft).2
      refine List.nodup_cons.mpr ⟨?_, ih htail (fun item hmem =>
        hdisjoint item (List.mem_cons_of_mem value hmem))⟩
      intro hmem
      rcases List.mem_append.mp hmem with hrest | hrightMem
      · exact hhead hrest
      · exact hdisjoint value (List.mem_cons_self) hrightMem

theorem occurrence_valid_append {left right : List Occurrence}
    (hleft : OccurrenceValid left) (hright : OccurrenceValid right)
    (hdisjoint : IdsDisjoint left right) : OccurrenceValid (left ++ right) := by
  unfold OccurrenceValid ids at hleft hright ⊢
  rw [List.map_append]
  exact nodup_append_of_disjoint hleft hright hdisjoint

def countToken (token : Nat) : List Occurrence → Nat
  | [] => 0
  | item :: rest => (if item.token = token then 1 else 0) + countToken token rest

theorem countToken_nil (token : Nat) : countToken token [] = 0 := rfl

theorem countToken_append (token : Nat) (left right : List Occurrence) :
    countToken token (left ++ right) =
      countToken token left + countToken token right := by
  induction left with
  | nil => simp [countToken]
  | cons item rest ih =>
      simp [countToken, ih, Nat.add_assoc]

theorem countToken_perm (token : Nat) {left right : List Occurrence}
    (h : left.Perm right) : countToken token left = countToken token right := by
  induction h with
  | nil => rfl
  | cons item _ ih => simp [countToken, ih]
  | swap first second rest =>
      simp [countToken, Nat.add_comm, Nat.add_left_comm]
  | trans _ _ ihLeft ihRight => exact ihLeft.trans ihRight

def OccurrenceEquivalent (left right : List Occurrence) : Prop :=
  ∀ token, countToken token left = countToken token right

theorem occurrence_equivalent_refl (h : List Occurrence) : OccurrenceEquivalent h h := by
  intro token
  rfl

theorem occurrence_equivalent_symm {left right : List Occurrence}
    (h : OccurrenceEquivalent left right) : OccurrenceEquivalent right left := by
  intro token
  exact (h token).symm

theorem occurrence_equivalent_trans {first second third : List Occurrence}
    (h₁ : OccurrenceEquivalent first second)
    (h₂ : OccurrenceEquivalent second third) : OccurrenceEquivalent first third := by
  intro token
  exact (h₁ token).trans (h₂ token)

theorem perm_occurrence_equivalent {left right : List Occurrence}
    (h : left.Perm right) : OccurrenceEquivalent left right := by
  intro token
  exact countToken_perm token h

def insertToken (tokens : List Nat) (token : Nat) : List Nat :=
  if token ∈ tokens then tokens else tokens ++ [token]

def forgetOccurrences (h : List Occurrence) : List Nat :=
  h.foldl (fun tokens item => insertToken tokens item.token) []

def once : List Occurrence := [⟨0, 7⟩]
def twice : List Occurrence := [⟨0, 7⟩, ⟨1, 7⟩]
def orderedA : List Occurrence := [⟨0, 7⟩, ⟨1, 8⟩]
def orderedB : List Occurrence := [⟨1, 8⟩, ⟨0, 7⟩]

theorem once_valid : OccurrenceValid once := by
  simp [OccurrenceValid, ids, once]

theorem twice_valid : OccurrenceValid twice := by
  simp [OccurrenceValid, ids, twice]

theorem canonical_forget_same_count_differs :
    forgetOccurrences once = forgetOccurrences twice ∧
      countToken 7 once ≠ countToken 7 twice := by
  decide

theorem count_equivalent_but_ordered_forget_differs :
    OccurrenceEquivalent orderedA orderedB ∧
      forgetOccurrences orderedA ≠ forgetOccurrences orderedB := by
  constructor
  · intro token
    simp [orderedA, orderedB, countToken, Nat.add_comm]
  · decide

theorem canonical_data_does_not_determine_count :
    ¬ ∃ f : List Nat → Nat,
      ∀ h : List Occurrence, OccurrenceValid h → f (forgetOccurrences h) = countToken 7 h := by
  rintro ⟨f, hf⟩
  have hOne : f [7] = 1 := by
    simpa [once, forgetOccurrences, insertToken, countToken] using hf once once_valid
  have hTwo : f [7] = 2 := by
    simpa [twice, forgetOccurrences, insertToken, countToken] using hf twice twice_valid
  have impossible : (1 : Nat) = 2 := hOne.symm.trans hTwo
  have hne : (1 : Nat) ≠ 2 := by decide
  exact hne impossible

def occurrenceWeight (suppliedMap : Nat → Int) (token : Nat)
    (h : List Occurrence) : Int := suppliedMap (countToken token h)

structure CountCalibration where
  encode : Nat → Int
  zero : encode 0 = 0
  additive : ∀ left right, encode (left + right) = encode left + encode right
  unit : encode 1 = 1

theorem count_calibration_unique (calibration : CountCalibration) :
    ∀ count, calibration.encode count = Int.ofNat count := by
  intro count
  induction count with
  | zero => exact calibration.zero
  | succ previous ih =>
      calc
        calibration.encode (previous + 1) =
            calibration.encode previous + calibration.encode 1 :=
          calibration.additive previous 1
        _ = Int.ofNat previous + 1 := by rw [ih, calibration.unit]
        _ = Int.ofNat (previous + 1) := by simp

theorem calibrated_occurrence_weight (calibration : CountCalibration)
    (token : Nat) (h : List Occurrence) :
    occurrenceWeight calibration.encode token h = Int.ofNat (countToken token h) := by
  exact count_calibration_unique calibration (countToken token h)

theorem occurrenceWeight_zero (suppliedMap : Nat → Int) (hZero : suppliedMap 0 = 0)
    (token : Nat) : occurrenceWeight suppliedMap token [] = 0 := by
  exact hZero

theorem occurrenceWeight_append (suppliedMap : Nat → Int)
    (hAdd : ∀ a b, suppliedMap (a + b) = suppliedMap a + suppliedMap b)
    (token : Nat) (left right : List Occurrence) :
    occurrenceWeight suppliedMap token (left ++ right) =
      occurrenceWeight suppliedMap token left + occurrenceWeight suppliedMap token right := by
  simp [occurrenceWeight, countToken_append, hAdd]

theorem separating_weight_does_not_factor (suppliedMap : Nat → Int)
    (hseparates : suppliedMap 1 ≠ suppliedMap 2) :
    ¬ ∃ factor : List Nat → Int,
      ∀ h : List Occurrence, OccurrenceValid h →
        factor (forgetOccurrences h) = occurrenceWeight suppliedMap 7 h := by
  rintro ⟨factor, hfactor⟩
  have hOne : factor [7] = suppliedMap 1 := by
    simpa [once, forgetOccurrences, insertToken, occurrenceWeight, countToken] using
      hfactor once once_valid
  have hTwo : factor [7] = suppliedMap 2 := by
    simpa [twice, forgetOccurrences, insertToken, occurrenceWeight, countToken] using
      hfactor twice twice_valid
  exact hseparates (hOne.symm.trans hTwo)

theorem zero_weight_factors_through_forget :
    ∃ factor : List Nat → Int,
      ∀ h : List Occurrence, OccurrenceValid h →
        factor (forgetOccurrences h) = occurrenceWeight (fun _ => 0) 7 h := by
  refine ⟨fun _ => 0, ?_⟩
  intro h _
  rfl

def PairAdmissible {α β : Type} (erase : α → β) (left right : α) : Prop :=
  left ≠ right ∧ erase left = erase right

theorem collapsed_pair_rejected {α β : Type} (erase : α → β) (h : α) :
    ¬ PairAdmissible erase h h := by
  simp [PairAdmissible]

theorem unequal_endpoints_rejected {α β : Type} (erase : α → β) (left right : α)
    (h : erase left ≠ erase right) : ¬ PairAdmissible erase left right := by
  intro valid
  exact h valid.2

structure ImportedPairCorrespondence where
  left : HistoryClass
  right : HistoryClass
  rightIsExchange : right = exchange left
  eligible : PairAdmissible erasedEndpoint left right

structure IntegerCalibration where
  encode : Polarity → Int
  positiveOne : encode .positive = 1
  negativeNegOne : encode .negative = -1

def standardIntegerCalibration : IntegerCalibration where
  encode := Polarity.toInt
  positiveOne := rfl
  negativeNegOne := rfl

def plusPair : Int × Int := (1, 1)
def inducedPair (calibration : IntegerCalibration) (c : ExchangeCharacter) : Int × Int :=
  (calibration.encode .positive, calibration.encode (c.map true))
def coordinateSquares (p : Int × Int) : Int × Int :=
  (p.1 * p.1, p.2 * p.2)

theorem induced_coordinate_squares_equal (calibration : IntegerCalibration)
    (c : ExchangeCharacter) :
    coordinateSquares plusPair = coordinateSquares (inducedPair calibration c) := by
  cases hc : c.map true with
  | positive =>
      simp [coordinateSquares, plusPair, inducedPair, hc, calibration.positiveOne]
  | negative =>
      simp [coordinateSquares, plusPair, inducedPair, hc, calibration.positiveOne,
        calibration.negativeNegOne]

theorem conditional_mixing_separation
    (pair : ImportedPairCorrespondence)
    (calibration : IntegerCalibration)
    (c : ExchangeCharacter) (hn : OperationalNontrivial c)
    (mixing : Int → Int → Int)
    (hmix : mixing 1 1 ≠ mixing 1 (-1)) :
    pair.right = exchange pair.left ∧
      PairAdmissible erasedEndpoint pair.left pair.right ∧
      coordinateSquares plusPair = coordinateSquares (inducedPair calibration c) ∧
      mixing plusPair.1 plusPair.2 ≠
        mixing (inducedPair calibration c).1 (inducedPair calibration c).2 := by
  have hc := nontrivial_exchange_is_negative c hn
  refine ⟨pair.rightIsExchange, pair.eligible,
    induced_coordinate_squares_equal calibration c, ?_⟩
  simpa [plusPair, inducedPair, hc, calibration.positiveOne,
    calibration.negativeNegOne] using hmix

theorem trivial_character_rejected : ¬ OperationalNontrivial trivialCharacter := by
  exact character_laws_do_not_force_nontrivial

theorem trivial_character_no_pair_change (calibration : IntegerCalibration) :
    inducedPair calibration trivialCharacter = plusPair := by
  simp [inducedPair, trivialCharacter, plusPair, calibration.positiveOne]

def flatMixing (_ _ : Int) : Int := 0

def squareMixing (left right : Int) : Int := (left + right) * (left + right)

theorem square_mixing_separates : squareMixing 1 1 ≠ squareMixing 1 (-1) := by
  decide

theorem square_mixing_contact
    (pair : ImportedPairCorrespondence)
    (calibration : IntegerCalibration)
    (c : ExchangeCharacter) (hn : OperationalNontrivial c) :
    pair.right = exchange pair.left ∧
      PairAdmissible erasedEndpoint pair.left pair.right ∧
      coordinateSquares plusPair = coordinateSquares (inducedPair calibration c) ∧
      squareMixing plusPair.1 plusPair.2 ≠
        squareMixing (inducedPair calibration c).1 (inducedPair calibration c).2 := by
  exact conditional_mixing_separation pair calibration c hn squareMixing
    square_mixing_separates

theorem coordinate_data_does_not_force_mixing :
    coordinateSquares plusPair =
        coordinateSquares (inducedPair standardIntegerCalibration signCharacter) ∧
      flatMixing plusPair.1 plusPair.2 =
        flatMixing (inducedPair standardIntegerCalibration signCharacter).1
          (inducedPair standardIntegerCalibration signCharacter).2 := by
  decide

inductive ThreeHistory where
  | first
  | second
  | third
deriving DecidableEq, Repr

def rotateThree : ThreeHistory → ThreeHistory
  | .first => .second
  | .second => .third
  | .third => .first

theorem three_cycle_is_not_involution :
    ∃ h : ThreeHistory, rotateThree (rotateThree h) ≠ h := by
  exact ⟨.first, by decide⟩

theorem three_involution_has_fixed_point (f : ThreeHistory → ThreeHistory)
    (hinv : ∀ h, f (f h) = h) : ∃ h, f h = h := by
  cases hFirst : f .first with
  | first => exact ⟨.first, hFirst⟩
  | second =>
      have hSecond : f .second = .first := by
        simpa [hFirst] using hinv .first
      cases hThird : f .third with
      | first =>
          have impossible := hinv .third
          simp [hThird, hFirst] at impossible
      | second =>
          have impossible := hinv .third
          simp [hThird, hSecond] at impossible
      | third => exact ⟨.third, hThird⟩
  | third =>
      have hThird : f .third = .first := by
        simpa [hFirst] using hinv .first
      cases hSecond : f .second with
      | first =>
          have impossible := hinv .second
          simp [hSecond, hFirst] at impossible
      | second => exact ⟨.second, hSecond⟩
      | third =>
          have impossible := hinv .second
          simp [hSecond, hThird] at impossible

theorem no_free_three_involution :
    ¬ ∃ f : ThreeHistory → ThreeHistory,
      (∀ h, f (f h) = h) ∧ (∀ h, f h ≠ h) := by
  rintro ⟨f, hinv, hfree⟩
  rcases three_involution_has_fixed_point f hinv with ⟨h, hh⟩
  exact hfree h hh

structure TriplePresentation where
  first : Int
  second : Int
  third : Int
deriving DecidableEq, Repr

def extensionPositive : TriplePresentation := ⟨1, -1, 1⟩
def extensionNegative : TriplePresentation := ⟨1, -1, -1⟩

def tripleSquares (value : TriplePresentation) : Int × Int × Int :=
  (value.first * value.first, value.second * value.second,
    value.third * value.third)

theorem two_coordinates_do_not_determine_third :
    extensionPositive.first = extensionNegative.first ∧
      extensionPositive.second = extensionNegative.second ∧
      extensionPositive.third ≠ extensionNegative.third ∧
      tripleSquares extensionPositive = tripleSquares extensionNegative := by
  decide

structure ReportSection (X Q : Type) (report : X → Q) where
  choose : Q → X
  rightInverse : ∀ q, report (choose q) = q

structure ObserverFamily where
  Obj : Type
  Pair : Obj → Type
  Arrow : Type
  src : Arrow → Obj
  tgt : Arrow → Obj
  transport : (a : Arrow) → Pair (src a) → Pair (tgt a)

structure NaturalChoice (F : ObserverFamily) where
  choose : (o : F.Obj) → F.Pair o
  natural : ∀ a : F.Arrow, F.transport a (choose (F.src a)) = choose (F.tgt a)

structure AdapterKernel (X Q : Type) (report : X → Q) (F : ObserverFamily) where
  query : F.Obj → Q
  pairOf : (object : F.Obj) → X → F.Pair object
  commutes : ∀ (reportSection : ReportSection X Q report) (arrow : F.Arrow),
    F.transport arrow
        (pairOf (F.src arrow) (reportSection.choose (query (F.src arrow)))) =
      pairOf (F.tgt arrow) (reportSection.choose (query (F.tgt arrow)))

def adapter_yields_natural_choice {X Q : Type} {report : X → Q} {F : ObserverFamily}
    (kernel : AdapterKernel X Q report F)
    (reportSection : ReportSection X Q report) :
    NaturalChoice F where
  choose := fun object =>
    kernel.pairOf object (reportSection.choose (kernel.query object))
  natural := kernel.commutes reportSection

def unitReport : Unit → Unit := id

def unitReportSection : ReportSection Unit Unit unitReport where
  choose := id
  rightInverse := by intro q; cases q; rfl

def flipFamily : ObserverFamily where
  Obj := Unit
  Pair := fun _ => Bool
  Arrow := Unit
  src := fun _ => ()
  tgt := fun _ => ()
  transport := fun _ value => !value

theorem flip_family_has_no_natural_choice : ¬ Nonempty (NaturalChoice flipFamily) := by
  rintro ⟨choice⟩
  have h := choice.natural ()
  cases hv : choice.choose () <;> simp [flipFamily, hv] at h

theorem report_section_does_not_determine_natural_choice :
    ¬ (ReportSection Unit Unit unitReport → Nonempty (NaturalChoice flipFamily)) := by
  intro adapter
  exact flip_family_has_no_natural_choice (adapter unitReportSection)

theorem flip_family_has_no_adapter_kernel :
    ¬ Nonempty (AdapterKernel Unit Unit unitReport flipFamily) := by
  rintro ⟨kernel⟩
  exact flip_family_has_no_natural_choice
    ⟨adapter_yields_natural_choice kernel unitReportSection⟩

def unitFamily : ObserverFamily where
  Obj := Unit
  Pair := fun _ => Unit
  Arrow := Unit
  src := fun _ => ()
  tgt := fun _ => ()
  transport := fun _ value => value

def unitNaturalChoice : NaturalChoice unitFamily where
  choose := fun _ => ()
  natural := by intro a; cases a; rfl

def emptyReport : Empty → Unit := fun value => nomatch value

theorem empty_report_has_no_section : ¬ Nonempty (ReportSection Empty Unit emptyReport) := by
  rintro ⟨s⟩
  exact nomatch s.choose ()

theorem natural_choice_does_not_determine_report_section :
    ¬ (Nonempty (NaturalChoice unitFamily) →
      Nonempty (ReportSection Empty Unit emptyReport)) := by
  intro adapter
  exact empty_report_has_no_section (adapter ⟨unitNaturalChoice⟩)

end AdmissionSignShadow
