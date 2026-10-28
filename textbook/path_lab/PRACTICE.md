# Practice with two different faces

[Path lab](README.md) · [Answers, after your attempt](ANSWERS.md)

Supply vertices K, L, M, N in that order and edges KL, KM, LM, LN, MN.
The candidate faces are KLM and LMN. The reference direction of an edge
goes from the earlier to the later named vertex. These are declared inputs.

1. Is K → L → N a walk? Is K → N → M a walk? Identify every missing step.
2. Compute the endpoint boundary of K → L → N, with departures −1 and
   arrivals +1. Which intermediate contribution cancels?
3. Is K → L → M → K closed? Does its endpoint boundary distinguish it
   from K → L → K or the zero-step walk at K?
4. Keep all edges but issue no face requests. Is either face admitted?
5. Remove KM and request both faces. Which request succeeds? State the
   exact failed facet condition for the other.
6. Restore all edges and admit both faces. Their default boundaries are
   +LM −KM +KL and +MN −LN +LM. Does LM cancel when we add these two
   lists with coefficient +1 on each face?
7. Instead give LMN coefficient −1, reversing all its boundary signs.
   Compute the combined boundary. Which shared contribution now cancels?
8. Does the zero coefficient on a shared edge erase that stored edge?
9. Someone evaluates the raw repeated list K, K, L and obtains a zero
   double boundary. Explain why this does not pass the face guard.
10. A map uses vertices for stations and edges for reported connections.
    Which extra information would be needed to estimate actual travel
    time? Does the number of drawn edges by itself provide it?

AuthorityEffect: None. This transfer exercise changes the shared facet's
orientation role; use the rules instead of memorizing the original diagram.
