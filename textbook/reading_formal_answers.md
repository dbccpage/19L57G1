# Worked reading-practice answers

[Practice](reading_formal_practice.md) · [Reading guide](reading_formal_statements.md)

1. D consists of K, L, M. Set g(7)=red and g(9)=green.
2. K and L share code 7. They require g(7)=red and g(7)=green, which
   cannot both hold for distinct requested values.
3. No. On K and M the earlier lookup works, but the excluded L would
   still require a different answer at the same stored code 7.
4. No. Correctness on D constrains only codes 7 and 9. The lookup's
   declared input type includes 12, and either red or green is allowed there.
5. One lookup receives each stored code, rather than the original item.
   The same lookup must return the requested answer for every listed item.
   Choosing different lookups using original identity would give access
   to information this task did not make available.
6. A decision procedure for the specified condition. The abstract
   structure fields do not require one. That absence is not a proof
   that no particular observer can have such a procedure.
7. No. Its no-views hypothesis is missing. Inspect the actual observations
   and the statement that applies to them; do not discard the condition.
8. For example: does the proposed real observation procedure produce the
   recorded codes for every allowed input under the claimed conditions?
   Identify what measurement would challenge that correspondence.
9. No. That conclusion needs a property connecting this particular
   next-step function to the demand conditions. The generic tag's
   definition alone supplies only the stated stopping condition.

## Institution foundations I00–I03

10. In J,K,L,M order, the representatives are J,K,J,K. In M,L,K,J scan
    order, the group {J,L} chooses L and {K,M} chooses M, so the values on
    J,K,L,M become L,M,L,M. The groups do not change. Renaming the two
    p-values injectively keeps their equalities and the representatives.
11. Set g(4)=5 and g(6)=7. After changing L's answer, J and L require
    g(4)=5 and g(4)=12, which are incompatible. Choosing the lookup using
    original input identity gives it information the stated task withholds.
12. Under `[p,r]`, J has [4,8] and L has [4,9]. Under `[r,p]` they have
    [8,4] and [9,4]. All four combined signatures differ, so no two
    distinct inputs merge. Repeating p lengthens each signature without
    changing which pairs agree.
13. The counts are 2,2,4,2. Table p cannot recover r: J/L share p=4 but
    differ in r. Table r cannot recover p: J/K share r=8 but differ in p.
    The two equal counts describe different groups. Appending q preserves
    p's groups because q is recoverable from p; appending r splits them.
    The theorem retains the old family and adds the specified new table.
14. Four empty signatures give one distinct signature. An empty carrier
    gives no signatures and zero classes. For J,J,K,L,M with the empty
    family, five empty signatures still give one class. With `[p]`, that
    repeated-input carrier has five entries and two classes.
15. Specify which physical inputs, measurement procedure and conditions
    correspond to these rows, and how readings receive the declared
    labels. Collect results that could reveal a disagreement with the
    proposed correspondence. Calculating the invented table supplies no
    such observations by itself.

## Combined reports and loss I04–I07

16. Send [0,0]→0, [0,1]→1, [1,0]→1 and [1,1]→0. For p alone, J/K
    have the same available value and different requested values. For r,
    J/L do. The separating member may depend on the pair; the full lookup
    uses both answers, while each member has a failure pair of its own.
17. The changed r is `[0,0,1,1]`, the same table as p. J/K now share
    signature [0,0] but require different q-values. Moving the entire rows
    together instead preserves their answer associations and recoverability.
18. L and M pass the pulled-back view. It merges exactly p's groups, so
    it is sharp for p. It fails for q on J/K, and for identity on J/K too.
    The correspondence is not faithful because it merges distinct inputs.
    With no later views all inputs merge; even sharpness for p fails.
19. Appending c gives count 4 and still recovers q, retaining the original
    members. Replacing by c gives count 1 and loses q. Replacing by the
    full representative `[J,K,L,M]` gives count 4 and preserves q, but
    that table alone does not record the original members. Removing r
    leaves p, with count 2 and no recovery of q. A separate copy of the
    original family could retain it; the replacement table does not supply one.
20. J/K conflict. A lookup receiving only their shared p-value 0 cannot
    distinguish them, while the reader given both full tables can name
    the pair. After adding h, L/M still share p=1 and h=0 but require
    q=1 and q=0. Resolving the first pair does not resolve every conflict.
21. Counts are 1,1,2,4,4 across five stages and four comparisons. The
    first and fourth comparisons are stationary; the first is followed
    by growth. All four comparisons retain the previous members.
    Replacing `[p]` by `[r]` drops p and does not meet that hypothesis.
    Both counts are 2, but r cannot recover p on J/L, while p knows itself.

## Targets, policies and identity I08–I11

22. q is recoverable with 0→2 and 1→4. The agreement table `[1,1,0]`
    conflicts on 0/2 under the old presentation. Adding t separates that
    pair, making the agreement table recoverable. It still has a 0 at
    input 2, so q still disagrees there.
23. The three supplied decoders each give `[0,0,0,1]`. There are three
    reports, one individual grouping, and two combined groups. The decoded
    assessment disagrees with the target at L. No probability, sampling
    or reliability model has been supplied, so the report count establishes
    none of those statistical conclusions.
24. J/K conflict; L/M are settled with original answer 0. The fallback
    is `[0,0,1,1]`, defined everywhere and recoverable, while the original
    report is not. After adding the indicator, every group is settled and
    the fallback is `[1,4,1,1]`. Subtract 1 from each positive mark to
    decode `[0,3,0,0]`. Before that change, the zero marks supplied no answer.
25. Refuse-all returns No/No/No. Known-only returns Yes/Yes/No. Requiring
    both known and target agreement returns Yes/No/No. Scoped soundness
    forbids approval of unknown reports; it does not require approval of
    every known one. The largest rule approves constant 1, which disagrees
    everywhere with the supplied zero target.
26. Initially both questions are unresolved. Appending the indicator is
    an extension: same is refuted and apart supported. Removing it gives
    unresolved/unresolved and is not an extension. J/J gives unresolved
    for both questions under this declared mapping; equality J=J remains true.
27. For example, differently encoded copies of `[0,0,1,1]` all recover
    the same assessment but can disagree with target `[0,1,1,1]` at K.
    Repetition does not establish correctness. Specify how actual device
    inputs, reading conditions, output labels and target readings correspond
    to the tables, then retain observations capable of challenging that
    correspondence. Likewise, recoverable-report approval supplies no
    physical validation, and current test agreement supplies no proof of
    literal identity. Other reasoned counterexamples can answer the task.

AuthorityEffect: None. Passing these written tasks would be reader evidence;
software validation of the examples alone is not a comprehension result.
