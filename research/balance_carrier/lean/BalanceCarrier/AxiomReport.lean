/-
AxiomReport: one report per exported theorem.  The build log's reports
are checked against the whitelist {propext, Quot.sound} by
`verify_lean.py`.  The `Receiver` and `Balance` theorems are verbatim
reconstructions of pinned sources (CONDITIONAL_THEOREM); the `Observer`
and `Walk` theorems originate here.
-/

import BalanceCarrier

#print axioms BalanceCarrier.Receiver.R_refl
#print axioms BalanceCarrier.Receiver.R_symm
#print axioms BalanceCarrier.Receiver.int_left_cancel
#print axioms BalanceCarrier.Receiver.den_int_ne_zero
#print axioms BalanceCarrier.Receiver.R_trans
#print axioms BalanceCarrier.Receiver.layer_mul_compat
#print axioms BalanceCarrier.Receiver.receiver_is_union
#print axioms BalanceCarrier.Balance.natCast_dvd_down
#print axioms BalanceCarrier.Balance.lt_of_mul_left
#print axioms BalanceCarrier.Balance.layer_inj
#print axioms BalanceCarrier.Balance.fresh_not_below
#print axioms BalanceCarrier.Balance.reduce_below
#print axioms BalanceCarrier.Balance.fresh_descend
#print axioms BalanceCarrier.Balance.fresh_rep_exists
#print axioms BalanceCarrier.Balance.fresh_rep_unique
#print axioms BalanceCarrier.Balance.mem_divisorsBelow
#print axioms BalanceCarrier.Balance.map_congr_mem
#print axioms BalanceCarrier.Balance.balanceFuel_stable
#print axioms BalanceCarrier.Balance.balance_eq_fuel
#print axioms BalanceCarrier.Balance.balance_one
#print axioms BalanceCarrier.Balance.sumI_append_single
#print axioms BalanceCarrier.Balance.balance_divisor_sum
#print axioms BalanceCarrier.Balance.balance_unique
#print axioms BalanceCarrier.Balance.balance_values
#print axioms BalanceCarrier.Balance.freshCount_values
#print axioms BalanceCarrier.Balance.partition_instances
#print axioms BalanceCarrier.Balance.inversion_instances
#print axioms BalanceCarrier.Balance.runningBalance_checkpoints
#print axioms BalanceCarrier.Observer.gcd_den_pos
#print axioms BalanceCarrier.Observer.rawObs_pos
#print axioms BalanceCarrier.Observer.redPart_lt
#print axioms BalanceCarrier.Observer.den_rawObs
#print axioms BalanceCarrier.Observer.red_fresh
#print axioms BalanceCarrier.Observer.red_same_nat
#print axioms BalanceCarrier.Observer.red_same
#print axioms BalanceCarrier.Observer.layer_observer_wf
#print axioms BalanceCarrier.Observer.layer_observer_constant
#print axioms BalanceCarrier.Observer.layer_observer_separates
#print axioms BalanceCarrier.Observer.layer_observer_separates'
#print axioms BalanceCarrier.Observer.layer_observer_grades
#print axioms BalanceCarrier.Observer.partCount_layer_image
#print axioms BalanceCarrier.Observer.observer_value_divides
#print axioms BalanceCarrier.Walk.flatMap_congr_mem
#print axioms BalanceCarrier.Walk.chainsFuel_stable
#print axioms BalanceCarrier.Walk.chainsFuel_head
#print axioms BalanceCarrier.Walk.chains_head
#print axioms BalanceCarrier.Walk.chains_succ_succ
#print axioms BalanceCarrier.Walk.sumI_append
#print axioms BalanceCarrier.Walk.sumI_flatMap
#print axioms BalanceCarrier.Walk.sumI_map_mul_left
#print axioms BalanceCarrier.Walk.sumI_map_neg
#print axioms BalanceCarrier.Walk.walkSum_one
#print axioms BalanceCarrier.Walk.walkSum_succ_succ
#print axioms BalanceCarrier.Walk.walkSum_neg_one_eq_balance
#print axioms BalanceCarrier.Walk.totalWalkSum_neg_one_eq_runningBalance
#print axioms BalanceCarrier.Walk.arrangements_four
#print axioms BalanceCarrier.Walk.unit_table_matches_to_7
#print axioms BalanceCarrier.Walk.balance_table_matches_to_7
