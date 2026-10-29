# Practice: a packet recorder

[Map lab](README.md) · [Answers, after your attempt](ANSWERS.md)

Supply this complete table. The recorder keeps only the bucket label.

| Packet | Bucket | striped? | large? |
|---|---|---|---|
| K | U | Yes | No |
| L | U | Yes | Yes |
| M | V | No | No |
| N | V | No | Yes |

1. Can striped be recovered from the bucket? Give the lookup values.
2. Can large be recovered? Name every conflicting pair within a bucket.
3. Could choosing L and N rather than K and M as bucket representatives
   fix the large-answer task? Explain what did and did not change.
4. Is the requested pair (striped, large) recoverable? Explain each component.
5. Compare recording the bucket twice with adding the large answer to
   the record. Which changes the blocked task, and why?
6. Replace the requested answer by “always Yes.” Does successful recovery
   now establish the original large answer?
7. A total lookup accepts labels U, V, Z and outputs Yes or No. Z is
   never recorded. How many such lookups recover striped? Where must
   they agree, and where may they differ?
8. Restrict the packet domain to L and N. Is large now recoverable? Does
   that establish recovery on K, L, M, N? What does an empty-domain test prove?
9. Define a match as agreeing on at least one of striped or large.
   Use K, L, N to test whether this relation is transitive.
10. If these were device records, name the measurements and domain
    assumptions needed before interpreting a successful lookup physically.

AuthorityEffect: None. Buckets, questions, answers, and allowable lookup
labels are supplied. Explain each answer using this table and its domain.
