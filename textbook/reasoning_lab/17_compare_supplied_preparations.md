# 17. Compare a supplied list of preparations

Supply four preparations with target pairs
(0,0), (0,0), (1,1), (2,2). Repeating (0,0) gives it two rows in this
list. These are invented inputs, not four observations of a device.

Read both targets with the copying probe. Then run a second version:
advance A in each preparation before reading both targets. Do not relay
anything through M.

**Predict:** how many pairs of records agree in each version? Does B's
list of recorded marks change?

<details><summary>Count agreement and B's marks separately</summary>

| Comparison | Original preparations | After advancing A only |
|---|---|---|
| Matching record pairs | 4 of 4 | 0 of 4 |
| B's marks, in row order | 0, 0, 1, 2 | 0, 0, 1, 2 |

B still gives two zeros, one 1 and one 2. Their shares are 2/4=1/2,
1/4 and 1/4. Agreement between the two records changed, while B's own
list stayed fixed. These are different questions about the same rows.

</details>

**Try a change:** use the always-zero probe. Both observers now always
store 0, so agreement is 4 of 4 even after the local advance. The marks
have hidden every target distinction. This does not restore equal targets.

## From calculation to evidence

If each row's B record is unchanged, counting that finite list preserves
the same shares. The source proves the pointwise record equality; the
book also checks equality of whole finite record lists. This is not a
proof about unspecified probability spaces or measured populations.

An empty list supplies no preparations or observations. A calculation
returning no difference there is not experimental support. Recording a
real trial would additionally require a declared procedure, timing,
reading rule, conditions, and retained raw results.

Try the [new protocol practice](PROTOCOL_PRACTICE.md) before its
[answers](PROTOCOL_ANSWERS.md). The [protocol desk](protocols.html) selects
these supplied calculations. Unit conversions belong to the separate
calibration model; they are not inferred from matching records here.

AuthorityEffect: None. Finite shares use exact rational counting. No
physical observations, novice performance or general measurement bridge
is established by this continuation.
