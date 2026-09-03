# Predictions and declarations frozen before computation

AuthorityEffect: None.

This file is one pre-computation freeze. Results and missed predictions are
recorded in `STATUS.md`; this file is not edited after its hash is committed.

## First freeze: shared finite class

- `DECLARED_POLICY`: Class identifier: `DR-C-2-1-3`.
- `DECLARED_POLICY`: Every member has base regime `EMPTY`.
- `DECLARED_POLICY`: Datum token alphabet: `a`, `b`.
- `DECLARED_POLICY`: Form arity alphabet: unary only; arity bound 1.
- `DECLARED_POLICY`: Event-symbol alphabet, in order: `Supply(a)`,
  `Supply(b)`, `AdmitDatum(a)`, `AdmitDatum(b)`, `AdmitForm(1)`,
  `AdmitInst(0,(0,))`, `AdmitInst(0,(1,))`, `AdmitRuleAll(0)`, and
  `Impose(0,1)`.
- `DECLARED_POLICY`: History length bound: 3 events, including the empty
  history. Membership requires one-event well-formedness from `EMPTY` at
  every prefix.
- `DECLARED_POLICY`: The class contains all and only histories meeting those
  declarations. Its size is recorded, not predicted.

## First freeze: description and decoder

- `DECLARED_POLICY`: Event symbol `e` at zero-based position `p` is encoded
  by the datum token `p<decimal p>e<decimal e>`.
- `DECLARED_POLICY`: A description regime starts at `EMPTY` and admits those
  tokens in position order using only `AdmitDatum` events.
- `DECLARED_POLICY`: Description-token alphabet: the 27 position-symbol
  tokens for three positions and nine event symbols.
- `DECLARED_POLICY`: Description price is its number of admission events.
- `DECLARED_POLICY`: The decoder returns a member exactly when every token
  has the expected position, names an event symbol, the length is at most 3,
  the description regime has no forms, instances, rules, or impositions,
  and the decoded history is well formed from `EMPTY`. It returns no member
  otherwise.
- `PREDICTION`: `decode_encode_id`, `encode_injective`,
  `encode_admission_only`, and `decoder_domain_iff` are provable in core
  Lean and reproduced by Python enumeration.
- `PREDICTION`: The empty history and the one-event `Supply(a)` history are
  distinct members with distinct descriptions and the same endpoint.

## First freeze: one-event stepper

- `DECLARED_POLICY`: A described state contains a description, pointer, and
  current regime. `Step` consumes exactly one event and advances the pointer
  once; `Done` means the pointer equals the decoded length; `Invalid` means
  decoding fails, the pointer is beyond the decoded length, or the recorded
  current regime does not equal the prefix fold.
- `PREDICTION`: `stepper_one`, `stepper_iterate`, and `stepper_total` are
  provable in core Lean.
- `PREDICTION`: A source-body check can establish `stepper_no_replay`; the
  proof of agreement may mention whole-history replay, but the stepper body
  will not.

## First freeze: class-wide reproduction

- `DECLARED_POLICY`: A candidate is a member of `DR-C-2-1-3`.
- `DECLARED_POLICY`: Giving a description validates and decodes it, then the
  candidate executes its own fixed history. No class event reads or branches
  on the description.
- `DECLARED_POLICY`: The complete matrix has one row per candidate and one
  column per target; every cell stores the candidate key, target key,
  reproduced regime hash, target regime hash, and local `certify` result.
- `PREDICTION`: Both result branches are retained. The run records either
  every successful candidate with a class-and-bound terminal, or the scoped
  no-member terminal. No branch is favored here.

## First freeze: self-description and bounded reporting

- `DECLARED_POLICY`: A description lies in the class when its admission
  history itself satisfies `DR-C-2-1-3`; this property is checked rather than
  assumed.
- `DECLARED_POLICY`: A target reaches the declared terminal exactly when its
  final regime has at least one admitted datum.
- `DECLARED_POLICY`: A candidate's report is true exactly when its own fixed
  final regime contains datum token `b`.
- `DECLARED_POLICY`: The within-cost bound is 6: at most three stepper
  applications plus at most three description admission events.
- `DECLARED_POLICY`: The outside-class reporter decodes a supplied
  description, takes one step per described event, and reports the declared
  terminal. Its per-target cost uses the same rule and is at most 6.
- `PREDICTION`: Self-description and in-class reporting outcomes are
  recorded, not predicted.
- `PREDICTION`: If no in-class reporter succeeds, a diagonal member selected
  from the empty member and `AdmitDatum(a)` member disagrees with each fixed
  candidate on that selected member's description; the bounded statement is
  expected to be provable in core Lean.
- `OPEN`: The unbounded question is `OPEN_UNBOUNDED` regardless of the
  bounded result.

## First freeze: cost ledger

- `DECLARED_POLICY`: The only cost of a described run is
  `stepper_applications + description_admission_events`.
- `DECLARED_POLICY`: The separation base admits `a` and `b`, then imposes
  `(0,1)`. It has no forms, instances, or rules before the response.
- `DECLARED_POLICY`: Candidate bounds are at most one new datum, at most one
  new form, arity at most 1, and at most two response items.
- `DECLARED_POLICY`: Item order is new datum, new forms by arity, new rules
  by form index, then new instances by form and argument tuple.
- `DECLARED_POLICY`: Measure `mu1` is response-item count. Measure `mu2` is
  the lexicographic pair of response-item count and admitted fresh-form arity
  sum.
- `DECLARED_POLICY`: A supplied response is checked by applying its
  admission-event list and testing the imposed pair with the local profile
  predicate. Its declared cost counts one description admission plus one
  stepper application per response event; the final predicate evaluation is
  outside this cost by declaration.
- `DECLARED_POLICY`: Finding enumerates complete cost levels in the declared
  order and stops after the first successful level has been completely
  checked, so all tied responses are retained. Finding cost is the sum of the
  declared checking costs for every candidate checked through that level.
- `PREDICTION`: The check costs, finding costs, tied counts, ratios, and
  largest completed row are recorded, not predicted.
- `OPEN`: Enlarged response bounds and the unbounded cost comparison remain
  `OPEN_UNBOUNDED`.

## First freeze: protected opens

- `OPEN`: `OB1_UNCHANGED`.
- `OPEN`: `S66_UNCHANGED`.
- `OPEN`: `S9_LAST_UNCHANGED`.
- `OPEN`: The all-policy quotient-tree frontier is named and not started.
