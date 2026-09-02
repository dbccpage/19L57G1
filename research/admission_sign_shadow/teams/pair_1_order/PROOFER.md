# Pair 1 proofer: two admission orders

AuthorityEffect: None.

## Proposed lane

The proposal reconstructs exactly two named order classes, equips them with
an exchange, and treats the exchange bit as a two-element action.  The local
proof targets are a free involution, action composition, and a unique bit
carrying either class to the other.

A declared `ExchangeCharacter` maps that bit action into the two values of
`Polarity`.  Both the constant character and the sign character satisfy the
character laws.  Therefore the laws alone do not select the sign character.
The additional predicate `OperationalNontrivial` is an imported premise.
With that premise, the exchange value is negative and its declared integer
encoding is `-1`.

The relative labels are normalized at a declared base order.  Two labelings
survive, related by global negation.  Once the base order is declared positive,
the relative labeling is unique.

## Source classification

- PROVED: free local exchange, action laws, unique transporter, character
  classification, relative-label classification, and uniqueness after a
  declared base value.
- DECLARED: the two local constructors, their exchange, `Polarity`, and the
  base-value normalization.
- IMPORTED: correspondence between the local constructors and the two frozen
  replay endpoints; operational nontriviality.
- OPEN: deriving either imported premise from the frozen admission calculus.

## Proposed ceiling

The local two-order object supports both characters.  Nontriviality selects
the sign character only after the nontriviality premise is supplied.  Absolute
sign remains a base-order convention.

Manager verdict: **IMPORT ISOLATED BUT NOT REMOVED**.
