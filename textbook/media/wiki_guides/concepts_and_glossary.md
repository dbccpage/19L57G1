# Concepts and glossary

These are repository-local meanings, not automatic identifications with similarly named objects elsewhere. Read a term with its carrier and classification.

## Start with four terms

An **admission** adds something to the system's record under its declared
rules. A **datum** is one admitted item. Its **index** is its position in
that record. A **form** specifies a kind of statement and how many items
it takes. That number is its **arity**: a unary form takes one item, and a
binary form takes two.

An **instance** fills the form's slots with admitted data. If the form is
“marked,” then “datum 0 is marked” is an instance. Admitting a form does
not automatically admit any instance of it.

## Follow one observation

1. Leave a slot empty: “___ is marked.” This is a **context**.
2. Plug in datum 0 and check whether the resulting instance is derivable.
3. Repeat with datum 1. If the answers differ, the context is a **separation witness**.

A datum's **profile** collects all contexts that succeed for it. Equal
profiles mean **observational collapse** at that stage. The two datum
indices can still be distinct.

## Terms used in later lessons

A **carrier** is the declared collection of items under discussion. A
**presentation** assigns a label to each item. A **fiber** groups items
with the same label. A **quotient** treats the members of each declared
equivalence class as one class; always check which equivalence relation
the lesson uses.

A claim **factors through** a presentation when its answer can be
recovered from that presentation's label alone. For labels `[0, 0, 1]`,
answers `[7, 7, 9]` are recoverable. Answers `[7, 8, 9]` are not: label 0
would need two answers. See [the factoring lesson](textbook_i02_knowing_is_factoring).

## Compact reference

Use this table after the examples above. The quotient row concerns search
branches; other lessons use observation or signature equivalences.

| Term | Working meaning | Important boundary |
| --- | --- | --- |
| Opaque seed | Supplied presentation used as a read-only derivational input | Its glyphs do not themselves specify a preferred internal interpretation |
| Metatheory apparatus | Declared machinery used to define and study the object language | It is not thereby derived inside the language |
| Regime | Admitted data, form arities, instances, uniform rules, and separation requirements | It is not an arbitrary consumer's domain state |
| Presentation token | External string recorded on datum admission | Token identity is not observational separation |
| Datum index | Position identifying admitted data internally | Two indices can have identical observable profiles |
| Supply | Presentation event with no admitted-state effect | Not datum admission or authorization |
| Form | Admitted judgment shape with positive arity | A form alone supplies no particular positive instance |
| Instance | A form index with a tuple of admitted datum indices | Must respect arity and range |
| Uniform rule | An admitted form's all-tuples rule | Not an arbitrary inference engine |
| Requirement | Persistent imposed obligation to separate a pair | A collapsed pair is not automatically an active demand |
| Context | Form with a slot tuple containing at least one hole | Plugging fills every hole with the same datum |
| Profile | Contexts whose plugging is derivable for a datum | Equality of profiles is a declared observation relation |
| Separation | Different profiles, witnessed by a context | Not external semantic identity or inequality |
| Delta | Canonically ordered tuple of candidate admission items | A proposal is not executed merely because it is valid |
| `mu1` | Item-count cost | Ties are retained |
| `mu2` | Item count followed by new-form arity sum, lexicographically | An additional declared preference, not a derivation of the preference |
| Canonical key | Serialization minimum under the implemented datum/form isomorphisms | Not a universal canonicalization across carriers |
| Quotient | Identification under the stated isomorphism relation | Needs edge witnesses and replay, not only merged node counts |
| Frontier | Explicit unresolved/bound/guard portion of a bounded run | Not a proof that no continuation exists |
| Receipt | Recorded command outcome or deterministic artifact | Not proof of an unchecked payload |
| Pin | Source identity binding to files/blobs/snapshots | Not freshness or semantic correctness |
| License | Alpha host-built authorization record, bound to a declaration | Not authentication, a proposal, or a seventh sealed event |
| Obstruction | A development-specific failure relative to its observation/protection/response hypotheses | A bare collision is not automatically an obstruction |
| Bridge | Explicit correspondence with proved laws between carriers | Shared names, imports, or an index edge are insufficient |
| OPEN | A named obligation not discharged at the stated scope | Not false, passed, or silently resolved |

## Classifications

The source contract distinguishes apparatus, supplied data, imposed challenge, admitted primitive, derived definition, proved theorem, deterministic computation, countermodel, optional realization, conjecture, open obstruction, and refuted claim. The paper uses its own explicit tag vocabulary, including bounded theorem and unresolved. Do not collapse every green item to “proved.”

## Example of a distinction that matters

Admitting two different tokens creates two datum indices. With no judgment forms, both profiles are empty. They are two admitted data but not internally separable. A later unary form plus one positive instance can separate them. The point is the change in available observations, not the visual difference between token strings.

Source: [model](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/code/derivation/model.py), [observation](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/code/derivation/observe.py), and [source contract](source_contract).
