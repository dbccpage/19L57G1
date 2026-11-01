# Practice: read the exact claim

[Reading guide](reading_formal_statements.md) · [Answers after your attempt](reading_formal_answers.md)

Supply this new table:

| Item | Stored code p | Requested answer q |
|---|---|---|
| K | 7 | red |
| L | 7 | red |
| M | 9 | green |

1. Name the domain and give a successful lookup g on the stored codes.
2. Replace L's requested answer by green. What pair now blocks a lookup
   on all three items? State the two incompatible equations.
3. With that changed table, restrict the domain to K and M. Does the
   successful lookup establish recovery for the excluded item L?
4. Return to the original three-item table. Allow the lookup to accept
   any code 0, 1, 2, and so on, returning either red or green. Code 12
   never occurs. Must all successful rules agree at 12?
5. Translate “there exists one g that works for every x in D” into words
   describing who receives which input. Explain why a separate g for
   each original item would be a different claim.
6. An observer record gives `Zero : R → Prop` and equivalence-law proofs.
   Someone says “we can therefore run a program deciding Zero on any R.”
   What additional ingredient has that person assumed?
7. A theorem requires a fresh arrival and no observation views. A worked
   example supplies an arrival but already has views. Does the theorem
   give its numerical conclusion for that example?
8. A finite toy table and its formal theorem agree. Name an empirical
   question still needed before using it to describe a real recorder.
9. A generic driver returns `closed` when its supplied next-step function
   returns `none`. Does the tag by itself establish that no active demand remains?

This completes the core practice. Check the [answers](reading_formal_answers.md),
then continue to [Unit 00](units/00_mark_and_constructor.md).

<details>
<summary>Optional: institution exercises after the named later Units</summary>

## Institution foundations I00–I03

Use a new four-input example, after reading
[I03](institutions/units/03_information_counts_classes.md). Explain your
answers without inspecting the answer page.

| Input | Table p | Table r | Requested answer q |
|---|---|---|---|
| J | 4 | 8 | 5 |
| K | 6 | 8 | 7 |
| L | 4 | 9 | 5 |
| M | 6 | 9 | 7 |

10. With family `[p]` and carrier order J,K,L,M, give the four
    representative inputs. Scan M,L,K,J instead: which labels change,
    and which groups change? Does relabelling p's values 4→40 and 6→60
    change those first-input representatives?
11. Recover q from p using one lookup. Change L's requested answer to 12.
    Give a pair that now blocks the lookup. Could choosing a different
    lookup separately for J and L meet the original one-lookup requirement?
12. Write J's and L's signatures under `[p,r]` and under `[r,p]`.
    Which inputs does `[p,r]` still merge? Does appending p again change
    any merged pair? Explain the difference between changing a signature
    list and changing the groups defined by equal signatures.
13. Count classes for `[p]`, `[r]`, `[p,r]`, and `[p,q]` using the original
    q. Does the equal count for `[p]` and `[r]` make either table recoverable
    from the other? Name a blocking pair in each direction. Explain why
    this does not contradict the theorem about appending a known table.
14. An empty family uses the four-input carrier. How many signatures and
    how many distinct signatures are there? What if the carrier is empty?
    What if its list is J,J,K,L,M? Distinguish list length from class count.
15. A software desk shows these invented rows and reports a successful
    lookup. A school proposes using the same labels for actual sensor
    readings. What additional correspondence must be specified and tested
    before the table calculation supports a claim about that sensor?

## Combined reports and loss I04–I07

Use this different supplied table after
[I07](institutions/units/07_long_chains_go_stationary.md). Work through
the questions before opening the answers.

| Input | Member p | Member r | Requested q |
|---|---|---|---|
| J | 0 | 0 | 0 |
| K | 0 | 1 | 1 |
| L | 1 | 0 | 1 |
| M | 1 | 1 | 0 |

16. Can the combined family `[p,r]` recover q? Give its lookup. Give a
    failure pair for p alone and one for r alone. Explain why “some member
    separates each required pair” does not mean “one member separates them all.”
17. Swap only r's entries for K and L. Can the changed family recover q?
    Name a blocking pair. Compare this with moving the two complete rows,
    including p, r and q, together.
18. Use p as a correspondence to later labels 0 and 1. A later view says
    yes exactly on label 1. Which original inputs pass it? Is this observer
    sharp for p, for q, or for original input identity? Is the correspondence
    faithful? What changes if the later observer has no views?
19. For the original family, compare appending constant `[7,7,7,7]`,
    replacing the family by that constant, replacing it by its full
    first-input representative, and removing r. Give each class count and
    whether q remains recoverable. Which operation retains the original
    member tables?
20. Given the full p and q tables, name a conflicting pair. Can a lookup
    receiving only p's value distinguish its two inputs? Now append
    h=`[0,1,0,0]`: it separates J/K. Does that make all of q recoverable,
    or can you find another conflict?
21. On this fixed four-input carrier, consider five stages: no tables;
    constant c alone; c and p; c,p,r; c,p,r,q. List their counts, the number
    of adjacent comparisons, and the stationary comparisons. Does the first
    stationary comparison prevent later growth? Would replacing `[p]`
    by `[r]` with equal counts meet the same extension hypothesis?

## Targets, policies and identity I08–I11

Use these new examples after
[I11](institutions/units/11_same_and_apart_outcomes.md). Give reasons
before checking the separate answers.

22. On inputs 0,1,2, the held table is `[0,1,0]`, report q is `[2,4,2]`,
    and target t is `[2,4,9]`. Is q recoverable? Write the agreement table.
    Is that table recoverable before adding t? After adding t, does the
    newly recoverable agreement table mean that q has become correct everywhere?
23. Three tables on J,K,L,M are `[5,5,5,8]`, `[20,20,20,30]` and
    `[40,40,40,50]`. Supply decoders mapping each first code to 0 and
    each last code to 1. Count reports, different individual groupings,
    and combined signature groups. For target `[0,0,1,1]`, where does
    the common decoded assessment fail? Does a three-report count alone
    establish statistical independence or reliability?
24. The held table on J,K,L,M is `[0,0,1,1]`; the requested report is
    `[0,3,0,0]`. Which inputs are settled? Write the encoded fallback,
    using 0 for demurral and n+1 for a settled answer n. Is the fallback
    defined at all four inputs? Is the original report recoverable?
    Now add `[1,0,0,0]`: write the new fallback and decode its answers.
25. On four inputs, hold no tables and supply target `[0,0,0,0]`.
    Compare rules “refuse all,” “approve known reports,” and “approve only
    known reports matching this target.” Give their decisions on constant
    reports 0 and 1 and on `[0,1,2,3]`. Does scoped soundness require
    every known report to be approved? Does approval by the largest rule
    establish agreement with this target?
26. With `[0,1,0,1]` held, give the same/apart policy outcomes for pair
    J/L. Append `[1,0,0,0]`, then remove it: give the new outcomes each
    time and identify which change is an extension. What outcomes does
    the policy give J/J, although ordinary equality J=J holds?
27. A team says “three differently encoded reports guarantee correctness,”
    “authorization proves empirical accuracy,” and “unresolved sameness
    proves literal identity.” Choose one assertion. Use a changed example
    to explain the missing implication, and name what additional
    correspondence or evidence would be needed for a claim about a real device.

## Acquisition, changing views and interpreters I12–I17

Use these changed examples after
[I17](institutions/units/17_the_interpreter_boundary_at_verdict_level.md).
Predict the result, name the assumptions, then consult the separate answers.

28. A protocol asks 0/1; next it asks 1/2 if Equal, otherwise 0/2;
    third it asks 2/3 if the second answer was Equal, otherwise 1/3;
    then it stops. Run it on `[4,8,4,9]` and `[20,30,20,40]` for two
    and five steps. Can the final record distinguish the first actor
    from `[4,8,4,8]`? Which unasked pair distinguishes them? Now store
    the first actor only on D=`[0,1]`. What happens to a probe of 0/2
    after decoding with default 0? Did those pair answers supply its
    original numeric labels?
29. On four inputs the identity actor answers Different to 0/1, 1/2
    and 2/3. Give a different actor merging the unasked pair 0/2 with
    the same record. Explain why Different is not transitive. Contrast
    a fixed actor answering Equal on 0/1 and 1/2: what is known about
    0/2 without asking it? Which example supports the worst-case bound?
30. On 0,1,2,3, let p=`[7,7,9,12]`. Write the six complete pair answers
    and the four row views. Supply two Yes/No views that sharply encode
    its three classes. Compare the numbers of probes and stored views.
    For the partial record `(0,1,true),(1,2,true)` on three inputs,
    does `sameT` directly report 0/2 equal? Would its `tableE` be sharp
    for a constant actor? Compare with equivalence closure.
31. With no promise, does the empty record fix a three-input partition?
    With exactly three classes promised, how many probes are needed?
    Evaluate the proposed formula there. Does unrestricted `Fixes`
    change when you merely say the promise aloud? Now inspect
    `(0,1,true),(1,2,true),(0,2,false)`: can any actor supply it, and why
    is the formal `Fixes` condition alone not evidence of discovery?
32. A regime with three admitted inputs has one unary view `{2}`.
    Its protected pair is 0/2. Admit the instance making its same view
    contain 0 as well. Compare 0/2 and new target 1/2 afterward. Could
    this be a valid response protecting 0/2? Compare appending `{0,2}`
    while retaining `{2}`. Separately rename the original regime by
    swapping 0 and 2: compare raw 0/1 with the correctly mapped pair.
33. A world has tokens `[10,20]`, view `{0}`, requirement 0/1, one unit
    of budget and licence enabled. A mark adds position 1 to the view.
    Compare codes differing only in the acceptance guard. Give the
    resulting view, quiescence and `WF` result. At the world carrying
    the guarded code, do that fixed coded role and the reflective role
    differ? At a world carrying the relaxed code, why can they differ?
34. A catalogue contains the kernel step, possibly with different notes
    but identical support. Can a `Lawful` function escape every entry
    on support? Does a well-formed output alone prove Lawful agreement
    at every input? Explain the quantifier difference between “for each
    fixed step, choose a differing guard code” and “one code differs
    from every fixed step.”
35. A device team argues that “six invented equality answers establish
    the physical grouping,” “a two-view code proves two probes suffice,”
    or “a relaxed guard’s well-formed output preserves every protected
    distinction.” Choose one claim, construct a changed counterexample
    or identify the missing evidence, and state what would need to be
    observed or specified for a conclusion about the actual device.

</details>

AuthorityEffect: None. Labels, codes, requested values, and domain choices
are supplied. Explain every answer from the stated task and assumptions.
