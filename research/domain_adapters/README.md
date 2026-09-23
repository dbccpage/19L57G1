# domain_adapters

AuthorityEffect: None.  Plan F of the foundations roadmap.  An adapter
declares, for an imported domain:

- its carrier, events, step and observation;
- a commuting translation of its step into the sealed passage step;
- an observation map with a commuting observation square.

Every law is a field that must be proved.  Nothing is attributed to the
sealed seed.

## What it establishes

- **Adapters compose**, and satisfy the replay square and the
  observation square for every source path.
- **Reversible domains collapse.**  If a source step returns to its start
  in two steps, every translation gives both states the same core.  The
  passage's core only grows (`native_bridge`), so a reversible domain can
  be carried by budget and license alone.
- **Four domains, each with a proof:**

  | Domain | Status | Result |
  | --- | --- | --- |
  | A monotone counter | faithful | its value is the native occurrence count; the encoding is injective on the core |
  | P209b's matrix `matH` | refused as a core-faithful adapter | it swaps the basis vectors; a budget-only adapter with an injective encoding exists |
  | The conservation ladder's integer step at coefficient 2 | refused | it has period four, so a state and its successor share their core under every translation |
  | Proposal and license | mapped | a proposal maps to no native event; application is gated by the sealed license and budget theorems |

Open: a non-thin cell semantics, the smooth tier, and operator families
outside this repository (`CLAIMS.md`).

## Checks

```text
python verify.py --check   # pins, tests, strict typing, Lean build, named axiom reports
python run.py --check      # the finite receipt regenerates byte-identically
```
