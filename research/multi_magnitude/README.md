# Multi-Magnitude Carrier & Repair Channel Separation

## Target 4 Deliverable

This directory resolves and unblocks roadmap leftover **LP4** by:
1. Constructing a carrier supporting $\ge 2$ operational magnitudes from cyclotomic reduction (carrier V6 in `fresh_characters`).
2. Programmatically demonstrating the separation of repair channels across `fresh_characters`, `convention_price`, and `balance_carrier`.
3. Emitting byte-pinned verification receipts in `receipts/carrier.json`.

### Background: The Single-Magnitude Degeneracy Bottleneck

Across previous research trees:
- In `convention_price`, arrow weights were restricted to $\{-1, +1\}$, so every closed walk had magnitude 1. Under magnitude 1, the pairing certificate criterion `certificate_iff_dominated` reduces to $\min(\text{count}(-1), \text{count}(+1)) \le \max(\text{count}(-1), \text{count}(+1))$, which is unconditionally true. Hence, Channel (b) could not refuse any row, and all 10 decided rows evaluated to cell `both` (`CHANNELS_AGREE_ON_DECIDED_ROWS`).
- In `balance_carrier`, every term in the candidate walk families at $N \in \{6, 7, 12\}$ had magnitude 1 (`DEGENERACY_PERSISTS`).

### Resolution via Cyclotomic Reduction

1. **Cyclotomic Row-Level Diversity:**
   - In `cyclotomic.py`, Carrier V6 (reduction modulo the layer's fresh part $\Phi_n(x)$) produces row families carrying $\ge 2$ operational magnitudes.
   - At part count $n = 3$, the row family has terms $[2, -1, -1]$ (total 0, magnitudes 1 and 2).
   - At magnitude 1: $\text{count}(-1) = 2, \text{count}(+1) = 0 \implies \text{neg\_dominated is False}$.
   - At magnitude 2: $\text{count}(+2) = 1, \text{count}(-2) = 0 \implies \text{pos\_dominated is False}$.
   - Channel (b) refuses a cancellation certificate (`certificate_exists: False`). Across $n \le 60$, 54 row families are diverse, exhibiting 25 distinct magnitudes, with 29 refusals.

2. **Multi-Magnitude Generator Presentations:**
   - In `carrier.py`, finite presentations are equipped with arrow weights drawn from cyclotomic rows.
   - Closed walks on these presentations generate multiple operational magnitudes (e.g. $[1, 2, 4, 8, 16]$).
   - On presentations with curable transport structures (e.g. two-label slot relabeling), Channel (a) succeeds (`a_yes = True`), while Channel (b) on the multi-magnitude walk weights refuses (`b_yes = False`).
   - This produces **`a_only`** cells!
   - Together with **`b_only`**, **`both`**, and **`neither`** cells, the channel table achieves:
     - `separated = True`
     - `terminal = "CHANNELS_SEPARATED"`
     - `single_magnitude_degeneracy = False`

LP4 is programmatically resolved in this setting: the cyclotomic row toy exhibits channel separation. No Lean formalization exists for this result.
