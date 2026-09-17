# Boundary source custody: explicit policy amendment

AuthorityEffect: None. This file records the author's authorization; it does
not grant authority of its own and makes no object-language claim.

The author explicitly authorized a separate custody-policy repair after the
review of PRs #193 and #194 found a pre-existing local-gate failure. The
original `research/boundary_seed/FREEZE.md` remains unchanged. Its historical
claim of an unbroken post-marker source freeze is not restored or asserted.

The custody-ratchet changes added `SOURCE_MANIFEST.json` and `verify_sources.py`
after the marker despite its comparison-only rule. The four affected source
snapshots, including their integration snapshot, are listed by exact commit,
path and Git blob in `boundary_custody_policy.json`. This is a retrospective
acceptance of those apparatus bytes, not a claim they complied at the time.
No derivation, prediction, theorem, receipt or source-isolation history is
changed. The added source verifier is not promoted into evidence of blind
discovery; it is post-freeze apparatus.

Going forward, the amendment approves exactly those two apparatus files and
the amended `verify_freeze.py`, at the listed nonexecutable Git blobs. Every
other frozen file and the original marker retain their exact original bytes.
Only `comparison.md` retains its original open content permission. A new
path, deletion, mode change or different blob is not authorized by this policy.
Historical revisions and reversions remain checked. Missing or edited policy
data cannot silently fall back to a successful original-freeze result.

The amended checker reads committed policy and checks index and working
copies independently, without trusting dirty-path flags. The exception census
is nonempty and fully visited. Commit ancestry and exact object types are
checked; identifiers are never inferred from current working bytes. The
current checker is itself pinned in the policy, outside the frozen write root,
avoiding a self-hashing source manifest. A future checker change requires an
explicit policy update and review, not an automatic repin.

`verify_freeze.py --require-frozen` prints every acknowledged historical
exception as AMENDED CUSTODY, not an unbroken original freeze. Its `frozen`
flag now means the original custody conditions plus this explicit amendment
are satisfied; it does not erase the historical breach or certify mathematics.
`verify_pins.py` consumes that same audit. Tests exercise both the unchanged
original policy on temporary repositories and the amended policy's refusal
and recovery paths. Neither the checker nor this JSON authenticates the
operator, executable environment, or author; repository review remains the
authority for policy changes.
