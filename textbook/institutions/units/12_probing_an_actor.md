# Unit 12. Probing an actor, and finite question tables

**Claim.** A probe asks only whether two actor values are equal. A transcript
records the asked pairs and answers. Finite encoding preserves the
specified carrier behavior; it does not reveal arbitrary numeric labels.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** When an adaptive protocol `π : Transcript → Option (Nat × Nat)`
probes an actor `p : Nat → Nat` by asking whether `p x = p y`, the resulting
transcript `run π p k` has at most `k` entries, is consistent with `p`, and is
identical for any two actors `p, p'` that give the same boolean answer
`decide (p x = p y)` on every asked pair (`run_congr`). Moreover, on any finite
carrier `D`, tabulating every member of an institution `Q` into a finite list of
pairs `encode D Q : List (List (Nat × Nat))` and decoding back via `decode`
preserves signatures, the canonical representative `pQ D Q`, knowledge of every
question, and information (`encoding_faithful`); and knowing any `q : Nat → Nat`
is equivalent to knowing its canonical representative `pQ D [q] : Nat → Nat`, read on `D`
(`knows_iff_knows_pQ`).

**Status:** derived (probe grammar admitted; `run_congr` and table fidelity
derived). **Lean:** `Acquisition.Transcript`, `Acquisition.Protocol`,
`Acquisition.entry`, `Acquisition.run`, `Acquisition.run_length_le`,
`Acquisition.Consistent`, `Acquisition.run_consistent`, `Acquisition.run_congr`
(`actor_institution`); `Reading.knows_congr`, `Reading.knows_iff_knows_pQ`,
`FiniteQuestions.Table`, `FiniteQuestions.tabulate`, `FiniteQuestions.ofTable`,
`FiniteQuestions.ofTable_tabulate`, `FiniteQuestions.encode`,
`FiniteQuestions.decode`, `FiniteQuestions.knows_tabulated`,
`FiniteQuestions.encoding_faithful` (`two_theorems`). **Sources:**
`research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean`
lines 62–150; `research/two_theorems/lean/ResearchTwoTheorems/Reading.lean`
lines 303–347;
`research/two_theorems/lean/ResearchTwoTheorems/FiniteQuestions.lean` lines
38–164.

Units 00 through 11 took an institution's member presentations as already
given. Units 12 through 15 ask how a presentation's partition on `D` can be
*acquired* from pairwise equality probes `decide (p x = p y)`. This unit sets up
two pieces of foundation:
1. The probe grammar (`Transcript`, `Protocol`, `run`): an adaptive protocol
   chooses the next pair `(x, y)` to probe from the transcript accumulated so
   far, or stops (`none`). Because the protocol sees `p` only through the
   boolean answers recorded by `entry p`, any two actors `p` and `p'` that
   answer every asked pair alike produce the exact same transcript
   (`run_congr`).
2. The finite-table discipline (`FiniteQuestions.lean`): although Lean types a
   presentation as `Nat → Nat`, every relation in the textbook (`SigEq`, `pQ`,
   `Knows`, `information`) reads `p` only at points of the finite carrier `D`,
   so tabulating `Q` on `D` and reading the tables back changes nothing
   (`encoding_faithful`), and the entire question space on `D` reduces to the
   finitely many canonical tables `pQ D [q]` from `D` into `D`
   (`knows_iff_knows_pQ`).

</details>

## First pass

An unknown table reports [7,9,7] on inputs 0,1,2. A probe cannot ask
for a stored number. It asks whether two entries are equal:

| Probe | Answer |
|---|---|
| 0/1 | Different |
| 0/2 | Equal |

The table [20,30,20] gives the same answers. The prober can learn the
grouping without learning the actual labels 7 and 9. A transcript is
the ordered record of such pair questions and answers. An adaptive
protocol chooses its next pair from that record.

**Predict:** if two actors agree on every pair actually asked along
the run, can this deterministic protocol secretly distinguish them?

<details><summary>Check your prediction</summary>

No. The next question depends on the same transcript. The theorem
tracks this agreement inductively. Its grammar and finite encoding
conditions are supplied assumptions, not all possible ways of learning.

</details>

## What you need first

Unit 00 (`SigEq`), Unit 01 (`pQ`, `pQ_spec`, `pQ_exact`), Unit 02 (`Knows`,
`knows_iff_determined`, `knows_iff_sigList`), and Unit 03 (`sigList`,
`sigEq_iff_sigList`, `information`, `classCount`).

### 1. Transcripts, adaptive protocols, and `run`

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean lines 62–77, 106–107
/-- A transcript: the probed pairs with their answers. -/
abbrev Transcript := List (Nat × Nat × Bool)

/-- A protocol: from the transcript so far, the next pair to probe, or stop. -/
abbrev Protocol := Transcript → Option (Nat × Nat)

/-- The transcript entry recording the actor's answer on a pair. -/
def entry (p : Nat → Nat) (pr : Nat × Nat) : Nat × Nat × Bool :=
  (pr.1, pr.2, decide (p pr.1 = p pr.2))

/-- Run a protocol against an actor for at most `k` steps. -/
def run (π : Protocol) (p : Nat → Nat) : Nat → Transcript
  | 0 => []
  | k + 1 =>
    match π (run π p k) with
    | none => run π p k
    | some pr => run π p k ++ [entry p pr]

/-- The actor `p` answers every entry of `T` as recorded. -/
def Consistent (T : Transcript) (p : Nat → Nat) : Prop :=
  ∀ e, e ∈ T → decide (p e.1 = p e.2.1) = e.2.2
```

At step `0`, `run π p 0` is `[]`. At step `k + 1`, the protocol inspects the
transcript `run π p k` and either stops (`none`), leaving the transcript
unchanged, or names a pair `pr = (x, y)` (`some pr`), appending
`(x, y, decide (p x = p y))`.

### 2. Finite tables for presentations and families

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/FiniteQuestions.lean lines 38–58, 89–96
abbrev Table := List (Nat × Nat)

def tabulate (D : List Nat) (q : Nat → Nat) : Table :=
  D.map (fun x => (x, q x))

def find : Table → Nat → Option Nat
  | [], _ => none
  | (k, v) :: t, x => if k = x then some v else find t x

def ofTable (t : Table) : Nat → Nat := fun x => (find t x).getD 0

theorem ofTable_tabulate (D : List Nat) (q : Nat → Nat) {x : Nat}
    (hx : x ∈ D) : ofTable (tabulate D q) x = q x := by ...

abbrev FinInstitution := List Table
def encode (D : List Nat) (Q : Institution) : FinInstitution := Q.map (tabulate D)
def decode (T : FinInstitution) : Institution := T.map ofTable
```

`tabulate D q` stores `(x, q x)` for each `x ∈ D`, and `ofTable` looks up the
first matching entry (defaulting to `0` outside `D`). On `D`,
`ofTable (tabulate D q) x = q x` (`ofTable_tabulate`).

## The theorems

First, the transcript invariants of `run`:

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean lines 94–150
theorem run_length_le (π : Protocol) (p : Nat → Nat) : ∀ k, (run π p k).length ≤ k := by ...

theorem run_consistent (π : Protocol) (p : Nat → Nat) : ∀ k, Consistent (run π p k) p := by ...

/-- **Two actors that answer alike on every asked pair have the same
transcript.**  The protocol cannot see anything else. -/
theorem run_congr (π : Protocol) (p p' : Nat → Nat) :
    ∀ k, (∀ e, e ∈ run π p k → decide (p' e.1 = p' e.2.1) = decide (p e.1 = p e.2.1)) →
      run π p' k = run π p k := by
  intro k
  induction k with
  | zero => intro _; rfl
  | succ k ih =>
    intro h
    have h' : ∀ e, e ∈ run π p k → decide (p' e.1 = p' e.2.1) = decide (p e.1 = p e.2.1) :=
      fun e he => h e (run_mono π p k e he)
    have ih' := ih h'
    cases hπ : π (run π p k) with
    | none =>
      rw [run_succ_none hπ]
      rw [← ih'] at hπ
      rw [run_succ_none hπ, ih']
    | some pr =>
      have hmem : entry p pr ∈ run π p (k + 1) := by
        rw [run_succ_some hπ]; exact List.mem_append_right _ List.mem_cons_self
      have hdec : decide (p' pr.1 = p' pr.2) = decide (p pr.1 = p pr.2) := h _ hmem
      rw [run_succ_some hπ]
      rw [← ih'] at hπ
      rw [run_succ_some hπ, ih']
      show run π p k ++ [(pr.1, pr.2, decide (p' pr.1 = p' pr.2))] =
        run π p k ++ [(pr.1, pr.2, decide (p pr.1 = p pr.2))]
      rw [hdec]
```

Second, finite-table fidelity and the finite question space:

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Reading.lean lines 338–347
theorem knows_iff_knows_pQ (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q q ↔ Knows D Q (pQ D [q]) := by
  rw [knows_iff_determined, knows_iff_determined]
  constructor
  · intro h x hx y hy hs
    exact (pQ_exact D [q] x hx y hy).mpr
      (fun r hr => by rw [List.mem_singleton.mp hr]; exact h x hx y hy hs)
  · intro h x hx y hy hs
    exact (pQ_exact D [q] x hx y hy).mp (h x hx y hy hs) q
      (List.mem_singleton_self q)
```

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/FiniteQuestions.lean lines 147–164
theorem knows_tabulated (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q (ofTable (tabulate D q)) ↔ Knows D Q q :=
  knows_congr (fun _ hx => ofTable_tabulate D q hx)

theorem encoding_faithful (D : List Nat) (Q : Institution) :
    (∀ q, Knows D (decode (encode D Q)) q ↔ Knows D Q q) ∧
    information D (decode (encode D Q)) = information D Q ∧
    (∀ x, x ∈ D → actor D (decode (encode D Q)) x = actor D Q x) :=
  ⟨knows_decode_encode D Q, information_decode_encode D Q,
    fun _ hx => actor_decode_encode D Q hx⟩
```

## The proof, step by step

**Step 1. `run_length_le` and `run_consistent` by induction on `k`.**
At `k = 0`, `run π p 0 = []` has length `0 ≤ 0` and vacuously satisfies
`Consistent`. At `k + 1`, either `π (run π p k) = none` (length and entries
unchanged) or `π (run π p k) = some pr`, which appends one entry `entry p pr`
whose third field is `decide (p pr.1 = p pr.2)` by definition.

**Step 2. `run_congr` by induction on `k`.**
Assume `p'` agrees with `p` on every entry of `run π p (k + 1)`. Because
`run_mono` says every entry of `run π p k` remains in `run π p (k + 1)`, the
induction hypothesis gives `ih' : run π p' k = run π p k`. Therefore, at step
`k + 1`, the protocol `π` sees the exact same input transcript `run π p' k =
run π p k` and makes the exact same choice (`none` or `some pr`). In the
`some pr` branch, `entry p pr ∈ run π p (k + 1)`, so the hypothesis gives
`decide (p' pr.1 = p' pr.2) = decide (p pr.1 = p pr.2)`, making the appended
entries equal as well.

**Step 3. `knows_iff_knows_pQ` and `encoding_faithful`.**
By Unit 01's `pQ_exact`, `pQ D [q]` merges `x, y ∈ D` iff `q x = q y`, and by
`pQ_mem` (`Reading.lean` lines 331–333), `pQ D [q] x ∈ D` for every `x ∈ D`.
Thus `Knows D Q q ↔ Knows D Q (pQ D [q])` (`knows_iff_knows_pQ`). And because
`ofTable (tabulate D p) x = p x` for every `x ∈ D`, replacing `Q` by
`decode (encode D Q)` leaves `sigList` unchanged on `D`
(`sigList_decode_encode`), which preserves `Knows`, `information`, and `actor`
(`pQ`) on `D` (`encoding_faithful`).

## The same fact in Python

The check verifies:

1. On `range(4)`, running an adaptive protocol against all partitions `p, p'`
   shows that whenever `p` and `p'` give the same equality answers on the pairs
   probed in `run(π, p, k)`, their transcripts are identical (`run_congr`, `0`
   violations), and every transcript has length `≤ k` and is `consistent` with
   `p`.
2. `finite_question_space` and `encoding_checks` from `two_theorems/model.py` on
   `D = (0, 1, 2, 3)` and `D = (0, 1, 2)`: `knows(D, Q, q)` matches
   `knows(D, Q, pQ(D, [q]))` with `0` mismatches, and `decode_family(
   encode_family(D, Q))` preserves `information`, `pQ`, and `knows` across all
   `55` cases (`0` violations).

```
python textbook/institutions/checks/i12_probing.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `Protocol` (`Transcript → Option (Nat × Nat)`) | `run` | metatheory function choosing the next probe from the transcript |
| Induction on `k : Nat` and `D : List Nat` | `run_length_le`, `run_consistent`, `run_congr`, `ofTable_tabulate` | structural induction in the metatheory |
| `by_cases hax : a = x` | `ofTable_tabulate` | decidable equality on `Nat` keys during table lookup |

**What the system holds.** A finite `Transcript : List (Nat × Nat × Bool)`, a
finite `Table : List (Nat × Nat)`, and a finite list of tables
`FinInstitution : List Table`.

**Admissions relied on, and their price.** Unit 00's three admissions, plus the
probe cost model (`AI-16`): a probe asks `decide (p x = p y)` on two data `x, y`
and costs `1` step; the protocol sees `p` only through the transcript `T`.
Meanwhile, `FiniteQuestions.lean` discharges the finitude obligation (`TT-41`):
typing presentations as `Nat → Nat` is proved to be notation for their finite
tables on `D`.

**Phrases to read with care.**

- "Protocol." A `Protocol` is not an observer (`Evaluator`) inside the system;
  it is an external caller that sequentially queries `decide (p x = p y)` to
  accumulate a `Transcript`.
- "The question space is finite." There are infinitely many functions
  `Nat → Nat`, and on a carrier `D` of size `n` there are at most `n^n`
  canonical representatives `pQ D [q] : D → D` (and `B_n` partitions of `D`),
  which determine `Knows D Q q` for every `q : Nat → Nat` (`knows_iff_knows_pQ`).

## What it shows, and what it does not

It shows that an adaptive protocol `π` running for `k` steps produces a
consistent transcript of length at most `k`, and cannot distinguish two actors
`p` and `p'` that agree on every pair asked during the run (`run_congr`).

It shows that encoding an institution `Q` as a list of finite tables over `D`
and decoding back preserves `Knows`, `information`, and `pQ` on `D`
(`encoding_faithful`), and that `Knows D Q q` depends only on the finite table
of `pQ D [q]` (`knows_iff_knows_pQ`).

It does not yet bound how many probes `k` are needed to acquire an unknown
actor's partition; Units 13 and 14 prove the lower and upper bounds.

## Sources

| Item | Where |
|---|---|
| `Transcript`, `Protocol`, `entry`, `run`, `run_length_le`, `Consistent`, `run_consistent`, `run_congr` | `research/actor_institution/lean/ResearchActorInstitution/Acquisition.lean` lines 62–150 |
| `knows_congr`, `knows_member_congr`, `pQ_mem`, `knows_iff_knows_pQ` | `research/two_theorems/lean/ResearchTwoTheorems/Reading.lean` lines 303–347 |
| `Table`, `tabulate`, `find`, `ofTable`, `ofTable_tabulate`, `tabulate_pQ_mem`, `FinInstitution`, `encode`, `decode`, `knows_tabulated`, `encoding_faithful` | `research/two_theorems/lean/ResearchTwoTheorems/FiniteQuestions.lean` lines 38–164 |
| Python mirrors | `research/actor_institution/model.py` lines 269–277 (`transcripts`, `consistent`); `research/two_theorems/model.py` lines 821–831, 887–931 (`finite_question_space`, `tabulate`, `of_table`, `encode_family`, `decode_family`, `encoding_checks`) |
| Check | `textbook/institutions/checks/i12_probing.py` |
| Ledger | `research/actor_institution/CLAIMS.md` AI-16; `research/two_theorems/CLAIMS.md` TT-30, TT-41, TT-41c |
