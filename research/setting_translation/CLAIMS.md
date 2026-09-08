# Claims: a setting as a regime of the sealed grammar

AuthorityEffect: None.  Every claim names its hypotheses, its novelty against
the reused results, its evidence, its falsifier and its remaining obligation.
The words forced, minimal, free, canonical, equivalent, universal and complete
appear only where a proof is named.  Lean names are in `lean/` under the
namespaces `Translation`, `Chains`, `Visible` and `Transcription`; every
report lies within `{propext, Quot.sound}` (`evidence/lean.json`).  "Finite
setting" means the Lean `FiniteSetting`: carrier `{0, …, n-1}`, boolean-valued
(hence decidable) stores, two endpoints in the carrier, finitely many
operations closed on the carrier.  The encoding does not carry the designated
pair; every reading is decided on the encoding *together with* the pair.

### CL-ST-01 — every finite setting is a well-formed regime

- **Statement**: `encode F` is a regime of the sealed grammar with `n` data,
  `3 + k` binary forms (the three stores, then the `k` operations), the
  asserted pairs and graphs as instances, no rule and no requirement; it is
  well-formed.
- **Hypotheses**: none beyond the finite-setting signature.
- **Novelty**: the sealed `PrimitiveCore.Setting` had no regime image; the
  merged `Magnification.induced` was a declared constant map.
- **Evidence**: `Translation.encode_wf`, `encode_forms_two`, `encode_rules`,
  `encode_reqs`, `mem_encode_insts`; computed: `translation.faithful` on all
  56 088 settings of the sealed universe and on the thirteen sealed concrete
  settings, three of which (full retention and protection stores) lie
  outside that universe (`evidence/census.json:universe`, `sealed_settings`).
- **Falsifier**: a finite setting whose encoding is ill-formed.
- **Obligation**: none.

### CL-ST-02 — the encoding is faithful instance by instance

- **Statement**: for admitted data, `(0, [x, y])` is derivable exactly when
  the difference relation asserts `(x, y)`; likewise form 1 for retention,
  form 2 for protection; `(3 + k, [x, y])` is derivable exactly when `y` is
  the value of the `k`-th operation at `x`.
- **Hypotheses**: `x < n`, `y < n`, `k` below the operation count.
- **Novelty**: the translation of the three stores and of the admitted
  operations into the sealed grammar, which PR #149 had left OPEN.
- **Evidence**: `Translation.derivable_rel`, `derivable_ret`,
  `derivable_prot`, `derivable_op`; `Chains.follow_derivable`,
  `follow_unique`.
- **Falsifier**: an admitted pair whose instance is underivable, or a
  derivable instance the setting does not assert.
- **Obligation**: none.

### CL-ST-03 — eight readings decide on the encoding beside the pair

- **Statement**: `W`, `A`, `Bs`, `Bc`, `Bl`, `C`, `D`, `F` of the presented
  setting are each equivalent to a decidable statement about derivable
  instances of the encoding at the designated pair (the witnessed link, no
  derivable self-instance, every link reversed, every link splitting every
  datum, the retention and protection links) or about the pair itself
  (`D` is endpoint inequality).  `Bl` coincides with `A` because a finite
  setting is located (the sealed `located_of_decidable`, which uses the
  decidability of the stores).
- **Hypotheses**: none.
- **Novelty**: the sealed matrix theorems are about the abstract signature;
  these are their regime-level forms.
- **Evidence**: `Translation.W_iff`, `A_iff`, `Bs_iff`, `Bc_iff`, `Bl_iff`,
  `C_iff`, `D_iff`, `F_iff`.  The thirteen sealed concrete settings are
  transcribed as finite settings (`Transcription.unitBare` … `boolEmptyMerged`)
  and their 42 sealed verdicts re-proved on the transcriptions by deciding
  these statements (`Transcription.unitBare_w` … `boolEmptyMerged_not_e`,
  named as the sealed theorems are).  Computed: `translation.readings` agrees
  with the sealed `primitive_core.evaluate` on all 56 088 settings, and the
  42-row verdict table is resolved by name, reading and sign against both the
  sealed `PrimitiveCore.lean` and `lean/Transcription.lean`
  (`evidence/census.json:verdict_sources`).  For `Bl` the Python agreement
  is not independent evidence: the sealed evaluator identifies `Bl` with `A`
  as the mirror does; `Bl_iff` is the evidence.
- **Falsifier**: a setting where a reading and its regime-level statement
  disagree; a verdict row that no theorem of that name states.
- **Obligation**: no Lean isomorphism between a sealed setting on `Unit`,
  `Bool` or `Fin 3` and its transcription is proved; the transcription is
  checked by the 42 verdicts and the sealed evaluator.

### CL-ST-04 — irreducibility is the chain criterion, and it is decidable

- **Statement**: `E` (no member of the closure of the admitted family
  identifies the endpoints) holds exactly when no word over the operation
  forms runs the endpoints to the same datum (`E_iff`), and exactly when no
  such word of length at most `n * n` does (`E_iff_noChain`), a decidable
  statement.
- **Hypotheses**: none.
- **Novelty**: the closure `Clos` is matched with words in both directions
  (`word_in_clos`, `clos_word`); the bound uses the sealed
  `Pigeonhole.pigeonhole` on coded position pairs (`shorten`, `cut`).
- **Evidence**: `Chains.E_iff`, `E_iff_noChain`, `noChain_iff`,
  `bounded_shorten`, `shorten`, `cut`, `code_inj`, `mem_words`; computed:
  the bounded criterion (`translation.no_chain`, exponential in the
  operation count) agrees with the unbounded one decided by reachability
  (`no_chain_reach`, the readings path) and with the sealed
  closure-of-tables evaluator on every setting of the universe.
- **Falsifier**: an operation family and a pair identified by a composite
  but by no word, or by a word but by no word of length at most `n * n`.
- **Obligation**: none.

### CL-ST-05 — separability of a binary regime is internal visibility

- **Statement**: in a regime all of whose forms are binary, two data are
  separable (the declared sense: a well-formed context whose pluggings differ
  in derivability) exactly when some form's self-instance, row or column
  differs at them (`Visible`, decidable); collapse is the negation.  For
  admitted data the self-instance clause is never the only witness.
- **Hypotheses**: every form of arity two; for the last sentence, both data
  admitted.  A state with a unary form (the seed's own mark response) is
  outside the statement.
- **Novelty**: the well-formed contexts of a binary regime have three shapes
  (`wfCtx_binary`); the sealed `one_unary_form_ctx_char` covered one unary
  form.
- **Evidence**: `Visible.separable_iff_visible`,
  `collapsed_iff_not_visible`, `wfCtx_binary`, `visible_iff_rows_columns`;
  computed: `translation.visible` equals the sealed collapse verdict on
  every pair of every encoded setting of the universe and the sealed
  `separable` on the thirteen concrete settings, and its row-column form
  equals it too.
- **Falsifier**: a binary regime and a pair that the sealed `separable`
  and `visible` grade differently.
- **Obligation**: none.

### CL-ST-06 — a witnessed irreflexive pair is internal; a bare witness is not

- **Statement**: `A` of the presented setting makes the encoded pair
  separable in either order, by the row context at the second endpoint; the
  constant relation on two points with empty stores and no operation is `W`
  and leaves the pair collapsed.
- **Hypotheses**: none.
- **Novelty**: the regime-level content of the readings: what a reading
  makes *internal*.
- **Evidence**: `Visible.A_separable`, `A_separable_rev`,
  `witness_alone_invisible`, `bothLinks_A`; the six two-point exhibits
  `selfOnly_visible`, `linkOnly_visible`, `selfAndLink_visible`,
  `bothLinks_visible`, `everyPair_collapsed`, `noPair_collapsed`; computed:
  over the 37 248 universe settings with distinct endpoints, every `A`
  setting (2 352) has a visible pair, 66 `W` settings have a collapsed pair,
  132 pairs are collapsed in all (`evidence/census.json:universe.by_reading`).
  The universe's zero collapsed count for `C` is an artifact of how it
  decorates protection (empty, or exactly the designated pair, which the
  protection form then exhibits); it is not a theorem, and the 66 `C`
  settings visible only through that form are the 66 collapsed `W` pairs.
- **Falsifier**: an `A` setting with a collapsed encoded pair.
- **Obligation**: none.

### CL-ST-07 — what the sealed engine does at an encoded pair

- **Statement**: the encoding is `Good`; at the encoded pair of a setting
  with distinct endpoints the seed's three fresh-form responses are valid
  (`seed_embeds`); at a separable pair there is no firing in either order of
  the endpoints (`A_no_fire`); at a collapsed pair of a binary regime with
  no standing requirement, every absent link and every absent self-instance
  on any form is a valid response and a minimum under both measures
  (`link_valid`, `self_valid`, `one_inst_min`, `link_min`, `self_min`,
  `encode_link_min`, `encode_self_min`); on the two-point setting with no
  assertion the self-instance and the link on the difference form are such
  minima and each a rooted seed step (`noPair_fires_self`,
  `noPair_fires_link`, `noPair_rooted_*`); on the constant relation a
  self-instance on the empty retention form is (`everyPair_fires`).
- **Hypotheses**: distinct endpoints throughout; for the minima, an absent
  instance to add.  When every instance of every form is present no
  one-instance response exists: the setting with all three stores complete
  on two points is collapsed and its minimum costs two items
  (`tests/test_translation.py`).
- **Novelty**: assembles the merged `EngineClass`/`Magnification`
  relation with the encoding; the minima theorems generalize the merged
  `ctx_min1`.
- **Evidence**: the named theorems; computed: the sealed `build_tree` from
  the encoding of each of the eleven concrete settings with distinct
  endpoints and of the six two-point exhibits, certified by the sealed
  `verify_full_export`, and refused by the receipt if it deviates: at every
  visible pair the root round's minimum is the empty response; at the
  collapsed pairs the root round has exactly the self-instance class and the
  link class at one item (`evidence/census.json:sealed_settings.*.restart`,
  `two_point.*.restart`).
- **Falsifier**: a certified restart whose root round differs from the
  stated minima; the receipt (`run.py`) refuses to record one.
- **Obligation**: the restart trees are recorded at bounded depth (4 rounds
  for the concrete settings, 3 for the exhibits); nothing about deeper
  rounds is claimed.  That the two classes are *all* the minima at a
  collapsed pair is computed, not proved.

### CL-ST-08 — the answer to the OPEN item of PR #149

- **Statement**: a finite setting carrying admitted operations *does*
  translate into the sealed grammar: the operations are binary forms whose
  instances are their graphs, and every reading of the setting, `E`
  included, is decided on the translation beside the designated pair.  The
  scope is the three hypotheses the Lean theorems carry: a finite carrier,
  decidable stores, and finitely many operations.
- **Hypotheses**: as stated.
- **Novelty**: closes the item PR #149 recorded as "A translation of a
  setting's operations, retention or protection into the sealed grammar"
  under *Not claimed*.
- **Evidence**: CL-ST-01 … CL-ST-04.
- **Falsifier**: a finite setting with a reading the encoding beside the
  pair cannot decide.
- **Obligation**: infinite carriers, undecidable stores and infinite
  operation families are outside the statements; no claim is made about
  them.  Protection is presented as a form, not enforced: the engine's
  demand at the designated pair is the seed imposition, made whether or not
  the pair is protected, and no other protected pair is ever imposed.  An
  encoding that places protected pairs into the regime's requirements
  instead is a possible variant, not built here.
