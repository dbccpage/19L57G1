# Worked practice answers

[Practice](PRACTICE.md) · [Map lab](README.md)

1. Yes. U → Yes and V → No recovers striped on all four packets.
2. No. K/L share U but disagree on large. M/N share V but also disagree.
3. No. The names of representatives change; the two merged pairs and
   their conflicting large values remain.
4. No. Striped is recoverable but large is not. Reading a recovered pair's
   second component would recover large, contradicting either blocking pair.
5. Duplicating the bucket leaves K/L and M/N merged. Adding large gives
   each conflicting pair different complete records, so it resolves the task.
6. No. The new constant target is recoverable even without a bucket.
   It is a different requested question.
7. Two. Both send U to Yes and V to No. At unused Z, either No or Yes
   works. These are all maps for the stated three-label Boolean task;
   they are not a count of every possible function on natural numbers.
8. On L and N, large is always Yes, so a constant-Yes lookup works.
   Adding K or M introduces the earlier conflicts. An empty domain checks
   no packet and constrains none of the lookup's inputs; it establishes
   no successful answer for an unlisted packet.
9. K and L agree on striped. L and N agree on large. K and N agree on
   neither. This proposed match relation is not transitive and does not
   justify one equivalence class containing all three.
10. Specify what produces the bucket, which procedures determine striped
    and large, which packets and conditions are allowed, and how missing
    or inconsistent readings are handled. The printed table supplies none
    of those measurements. A same-record pair with different requested
    measured answers would challenge the proposed recovery correspondence.

AuthorityEffect: None. Success and failure retain their exact task and domain.
