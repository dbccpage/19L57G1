"""Independent prefix certificate through four sealed items at both bases.

Classification: metatheory apparatus; deterministic computation.

Completeness of the direct construction follows from the declared canonical
order. Every delta has a unique count of data, forms, rules and instances.
New forms are a multiset of the declared arities. Data and forms precede all
rules and instances, so their counts and arities fix the entire coordinate
domain before the latter items are chosen. Rules occur at most once and may
not already be present; instances may repeat, including existing instances.

The rule and instance pools start wider than that domain: form indices and
datum indices extend one below and one above their valid ranges, and instance
argument lengths extend from zero through one above the largest arity. Only
naive replay filters those coordinates. This filtering before taking products
is complete: neither a rule nor an instance changes data, forms or arities,
so another such admission cannot repair a refused coordinate. All products
are then replayed as whole deltas. No one-item generator, breadth population,
or production shape predicate is used to construct the independent side.

This certifies the enumerator against the shared admission semantics, not the
mathematical correspondence of those semantics to the frozen requirements.
"""

from __future__ import annotations

import itertools
import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

from code.enumerate_space import (  # noqa: E402
    DEFAULT_BOUNDS, Bounds, sealed_prefixes,
)
from code.items import (  # noqa: E402
    Delta, NewDatum, NewForm, NewInst, NewRuleAll, StatedState, apply_delta,
)
from code.regime import AdmissionRefused, Regime, genesis  # noqa: E402


def direct_prefixes(base: Regime, count: int, bounds: Bounds) -> dict[Delta, Regime]:
    """Construct canonical multisets by item-kind counts, not move histories."""
    out: dict[Delta, Regime] = {}
    for data_count in range(count + 1):
        for form_count in range(count - data_count + 1):
            for arities in itertools.combinations_with_replacement(
                range(1, bounds.max_arity + 1), form_count
            ):
                stem = (NewDatum(),) * data_count + tuple(
                    NewForm(arity) for arity in arities
                )
                after_stem = apply_delta(
                    StatedState(base, ()), stem, bounds.w_max, bounds.max_readers
                ).regime
                remaining = count - data_count - form_count
                if remaining == 0:
                    out[stem] = after_stem
                    continue

                rules: list[NewRuleAll] = []
                instances: list[NewInst] = []
                wide_forms = range(-1, len(after_stem.forms) + 1)
                wide_data = range(-1, after_stem.n_data() + 1)
                wide_lengths = range(
                    max((bounds.max_arity, *after_stem.forms)) + 2
                )
                for form in wide_forms:
                    rule = NewRuleAll(form)
                    try:
                        apply_delta(
                            StatedState(after_stem, ()), (rule,),
                            bounds.w_max, bounds.max_readers,
                        )
                    except AdmissionRefused:
                        pass
                    else:
                        if form not in base.rules:
                            rules.append(rule)
                    for length in wide_lengths:
                        for args in itertools.product(wide_data, repeat=length):
                            instance = NewInst(form, args)
                            try:
                                apply_delta(
                                    StatedState(after_stem, ()), (instance,),
                                    bounds.w_max, bounds.max_readers,
                                )
                            except AdmissionRefused:
                                continue
                            instances.append(instance)

                # The loops above sort by length before arguments. Canonical
                # instances sort only by form and arguments after replay has
                # fixed each form's one valid length.
                instances.sort(key=lambda item: (item.form, item.args))
                for rule_count in range(remaining + 1):
                    for chosen_rules in itertools.combinations(rules, rule_count):
                        for chosen_instances in itertools.combinations_with_replacement(
                            instances, remaining - rule_count
                        ):
                            delta = stem + chosen_rules + chosen_instances
                            child = apply_delta(
                                StatedState(base, ()), delta,
                                bounds.w_max, bounds.max_readers,
                            ).regime
                            out[delta] = child
    return out


class FourItemPrefixCertificate(unittest.TestCase):
    def test_exact_delta_and_child_equality_through_four_items(self) -> None:
        """Compare every delta and its child, without quotienting or sampling."""
        for reading in ("L", "F"):
            base = genesis(reading)
            for count in range(5):
                with self.subTest(reading=reading, count=count):
                    independent = direct_prefixes(base, count, DEFAULT_BOUNDS)
                    breadth = sealed_prefixes(base, count, DEFAULT_BOUNDS)
                    self.assertEqual(set(independent), set(breadth))
                    self.assertEqual(independent, breadth)
                    self.assertTrue(independent)
                    self.assertTrue(all(len(delta) == count for delta in independent))

    def test_repeated_instances_and_distinct_rules_are_retained(self) -> None:
        """No idempotence quotient silently removes paid-for instance items."""
        base = genesis("L")
        prefixes = direct_prefixes(base, 4, DEFAULT_BOUNDS)
        repeated_instance = (
            NewForm(1), NewRuleAll(0), NewInst(0, (0,)), NewInst(0, (0,)),
        )
        distinct_rules = (
            NewForm(1), NewForm(1), NewRuleAll(0), NewRuleAll(1),
        )
        repeated_rule = (
            NewForm(1), NewRuleAll(0), NewRuleAll(0), NewInst(0, (0,)),
        )
        self.assertIn(repeated_instance, prefixes)
        self.assertIn(distinct_rules, prefixes)
        self.assertNotIn(repeated_rule, prefixes)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
