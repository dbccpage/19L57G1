# Worked practice answers

[Practice](PRACTICE.md) · [Path lab](README.md)

1. K → L → N is a walk: KL and LN are present. K → N → M is not:
   KN is absent, although NM uses the present edge MN in reverse.
2. The boundary is −K +N. L's arrival +1 cancels its departure −1.
3. The triangle walk is closed and its endpoint counts are all zero.
   The out-and-back and zero-step examples also have all-zero counts.
   The endpoint tally does not retain the full route.
4. Neither. The facet guard permits a face step; it does not perform it.
5. LMN succeeds: LM, LN, MN remain. KLM fails because KM is missing.
6. No. LM has coefficient +1 in each default boundary, so the combined
   coefficient is +2. A shared edge cancels only when its contributions
   have opposite signs; adjacency alone does not ensure this.
7. The second boundary becomes −MN +LN −LM. Adding the first gives
   +KL −KM +LN −MN. The LM coefficients cancel. This follows the outer
   route K → L → N → M → K.
8. No. Membership of the edge register and its coefficient in this
   boundary sum are different facts.
9. The repeated vertex violates strict increase. The boundary formula's
   unrestricted cancellation theorem does not assert valid cell admission.
10. We need an interpretation of edges as usable connections, relevant
    measured durations and conditions, and a rule for combining them.
    The diagram supplies neither such measurements nor a travel-time law.

AuthorityEffect: None. These conclusions concern the supplied transfer case.
