# Cost Cohomology & Obstruction Witness

## Target 7 Deliverable

This directory computes the 1-cohomology group of additive costs modulo exact costs on the depth-3 move graph ($|V|=262$, $|E|=638$), exhibits pure commuting squares spanning the non-self cycle space, computes the cellular homology group of the 2-complex $X$, and exhibits native cost cocycles detecting commitment growth.

### Core Mathematical Invariants

1. **Move Graph & 1-Skeleton Topology:**
   - Vertices (reachable regimes): $|V| = 262$.
   - Directed edges (valid moves): $|E| = 638$.
   - Connected components: $c = 2$.
   - Space of 1-chains / additive edge costs: $C^1(G; \mathbb{R}) = \mathbb{R}^{638}$.
   - Space of exact costs (coboundaries $\operatorname{im}(d_0)$): $B^1(G; \mathbb{R}) = \mathbb{R}^{|V| - c} = \mathbb{R}^{260}$.
   - Cycle rank / 1-cohomology quotient:
     $$H^1(G; \mathbb{R}) = C^1(G; \mathbb{R}) / B^1(G; \mathbb{R}) \cong \operatorname{Hom}(H_1(G; \mathbb{R}), \mathbb{R}) \cong \mathbb{R}^{378}$$
   - Direct-sum decomposition:
     $$\mathbb{R}^{378} \cong \mathbb{R}^{232}_{\text{waste}} \oplus \mathbb{R}^{146}_{\text{order}}$$
     where $\mathbb{R}^{232}_{\text{waste}}$ corresponds to repeated instance admissions (self-loops) and $\mathbb{R}^{146}_{\text{order}}$ corresponds to non-self fundamental cycles.

2. **Commuting Squares & Cellular 2-Complex $X$:**
   - 770 total commuting squares (length-2 path pairs $u \rightrightarrows w$).
   - 146 **pure commuting squares** (squares with zero self-loop edges).
   - **Order Spanning Theorem**: The boundary operator restricted to the 146 pure commuting squares has rank **exactly 146**. Hence, the pure commuting squares linearly span the entire 146-dimensional non-self cycle space!
   - 2-Complex Homology: Attaching all 770 squares as 2-cells yields $\operatorname{rank}(d_2) = 324$.
     $$H_1(X; \mathbb{R}) = Z_1(G; \mathbb{R}) / \operatorname{im}(d_2) \cong \mathbb{R}^{378 - 324} = \mathbb{R}^{54}$$
     All 146 non-self cycle directions are null-homologous in $X$; the remaining 54 degrees of freedom are uncancelled self-loops.

3. **Obstruction Detection in Native Vocabulary:**
   - `rule_span(S, it)` charges $(|S|)^{\text{arity}}$ for `NewRuleAll` and 0 elsewhere.
   - It is strictly 0 on all 232 self-loop edges (waste-free).
   - On commuting squares exchanging `NewRuleAll` and `NewDatum`, it yields circulation $+1$ (witnessing the commitment-growth obstruction: committing to a rule before vs after enlarging the state base).
   - The 4 native order candidates (`width_at_admission`, `rule_span`, `empty_admission`, `mention_deficit`) have rank **exactly 4** on the pure commuting squares, spanning the 4 pairwise commutators of native items.
