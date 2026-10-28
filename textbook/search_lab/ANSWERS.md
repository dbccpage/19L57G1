# Worked practice answers

[Questions](PRACTICE.md) · [Search lab](README.md)

1. U gives Yes, V and W give No. Recording a requirement changes the
   requirement list; it supplies no new recorded instance or observation.
2. The answers become Yes, Yes, No. U/V collapses, so the response fails
   an old requirement. The instance is well-formed: P exists and V is an
   admitted entry. The response-validity condition rejects this repair.
3. A new entry gives no new successful judgment about V or W. A new form
   alone has no recorded instance. The only new instances on the old form
   are P(V) and P(W); each loses a protected separation. Re-recording P(U)
   changes nothing. The uniform rule makes all P answers Yes and loses both
   old distinctions. An instance or rule on a new form needs that form too,
   which would take two items.
4. Admit Q and record Q(V). The answer patterns in P, Q order are U:
   Yes, No; V: No, Yes; W: No, No. Q(_) separates V/W. P(_) still separates
   U from each of V and W. Q(W) would give another valid two-item plan.
5. Each plan costs two under mu1. Under mu2 the Q plan costs `(2,1)` and
   the R plan costs `(2,2)`. The R plan works: R(_,V) succeeds on V and
   fails on W, while the original P test keeps both old requirements.
6. The three-class count is for at most two items and form arity at most
   two in reading L. Allowing arity three gives fourteen minimum raw plans
   in seven classes under mu1. A three-slot form with one instance still
   costs two items. It cannot be isomorphic to a one-slot or two-slot form
   because the isomorphism preserves arities. No arity bound permits an
   unqualified claim that this finite list exhausts the grammar-wide ties.
7. Replay checks reconstructed states and edge maps. Recompute prices and
   compare every allowed candidate against the minimum for a price claim.
   State item/arity bounds, supply and demand policies, round limit, and
   guard. A depth-limited explored graph does not establish exhaustive
   coverage of every future history. Reading L versus F also matters.

An example investigation asks whether a parcel recorder can distinguish
the destination classes required by a sorting task after one sensor is
replaced. Measure recorder outputs on cases from each required class,
check errors and repeatability, and look for two differently destined
cases receiving the same recorded pattern. Such a pair would challenge
the proposed correspondence. No result about actual parcels follows
merely from declaring this test.

AuthorityEffect: None. These answers are scoped to the supplied exercises.
