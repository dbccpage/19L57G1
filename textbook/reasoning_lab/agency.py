"""Isolated read-only X303 teaching controls; AuthorityEffect: None."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def verify_sources():
    expected = json.loads(Path(__file__).with_name('agency_sources.json').read_text(encoding='utf-8'))
    actual = {name: hashlib.sha256((ROOT / name).read_text(encoding='utf-8').encode()).hexdigest()
              for name in expected}
    assert actual == expected, 'Review changed source dependencies before updating book pins'
    return actual


def check_examples():
    # Native X301 imports use bare module names and X303 adjusts sys.path.
    # Keep those effects inside a fresh process, away from other book routes.
    verify_sources()
    result = subprocess.run([sys.executable, '-I', str(Path(__file__).resolve()), '--worker'],
                            cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        raise RuntimeError('Isolated agency control failed:\n' + result.stderr)
    return json.loads(result.stdout)


def worker():
    from dataclasses import replace
    from itertools import product

    verify_sources()
    sys.path.insert(0, str(ROOT))
    from research.x303_bounded_agency import agency as a
    from research.x301_formal_semantics import semantics as s
    import model
    assert Path(a.__file__).resolve() == ROOT / 'research/x303_bounded_agency/agency.py'
    assert Path(model.__file__).resolve() == ROOT / 'research/x301_formal_semantics/model.py'

    def notebook(marked=(0,)):
        return s.RelationalModel(data=('A', 'B'), forms=(1,),
                                 insts=frozenset((0, (i,)) for i in marked))

    def envelope(ceiling=2):
        return a.ViabilityEnvelope(max_data=2, max_forms=1, max_arity=1, max_insts=ceiling)

    def controller(state=None, ceiling=2, fuel=3, horizon=2, authorizer=None, abilities=None):
        return a.AgentController(state if state is not None else notebook(), envelope(ceiling),
                                 total_fuel=fuel, memory_horizon=horizon,
                                 authorizer=authorizer, abilities=abilities)

    def snapshot(c):
        return c.state, c.state.insts, c.memory, c.fuel, c.step_count

    def retained(c, before, result):
        state, insts, memory, fuel, count = before
        assert result.is_refusal and result.state is state and c.state is state
        assert c.state.insts == insts and c.memory is memory
        assert c.fuel == fuel and c.step_count == count

    # Horizon-2 lifecycle, then a refused fourth attempt.
    c = controller()
    actions = [a.add_instance_action(0, (1,), name='mark B'),
               a.remove_instance_action(0, (0,), name='erase A'),
               a.remove_instance_action(0, (1,), name='erase B')]
    expected_marks = [frozenset({(0, (0,)), (0, (1,))}), frozenset({(0, (1,))}), frozenset()]
    for index, (action, marks) in enumerate(zip(actions, expected_marks)):
        result = c.step([action])
        assert result.is_success and c.state.insts == marks and c.fuel == 2 - index
        assert [r.action_repr for r in c.memory.records] == [x.name for x in actions[max(0, index - 1):index + 1]]
    before = snapshot(c)
    retained(c, before, c.step([a.add_instance_action(0, (0,))]))
    assert c.step_count == 3 and [r.step_index for r in c.memory.records] == [1, 2]

    # FIFO independent oracle, including initialization beyond capacity.
    memory_checks = 0
    for horizon, length in product(range(1, 5), range(9)):
        records = tuple(a.MemoryRecord(i, 'pre', str(i), s.RationalValuation(1), 'post', 1)
                        for i in range(length))
        memory = a.BoundedMemory(horizon)
        for rec in records:
            memory = memory.append(rec)
        assert memory.records == records[max(0, length - horizon):]
        assert a.BoundedMemory(horizon, records).records == memory.records
        memory_checks += 1
    try:
        a.BoundedMemory(0)
    except ValueError:
        pass
    else:
        raise AssertionError('Python horizon zero unexpectedly accepted')

    # Licenses for computed projections, without caller-supplied cached keys.
    state = notebook()
    action = a.add_instance_action(0, (1,))
    projected = action.apply(state)
    key = action.get_canon_key(projected)
    issuer, driver = a.ActionAuthorizer(), a.LicensedDriver()
    assert key != a.compute_canon_key(state)
    for license in (issuer.issue_license([]), issuer.issue_license([a.compute_canon_key(state)])):
        try:
            driver.apply_licensed(state, action, license)
        except a.UnlicensedActionError:
            pass
        else:
            raise AssertionError('Unlisted computed projected key unexpectedly accepted')
    assert driver.apply_licensed(state, action, issuer.issue_license([key])).insts == projected.insts
    assert state.insts == frozenset({(0, (0,))})
    other_position = notebook((1,))
    assert a.compute_canon_key(state) == a.compute_canon_key(other_position)
    assert a.canonical_model_digest(state) != a.canonical_model_digest(other_position)

    # A supplied cached key is trusted in a different native API branch.
    cached = replace(action, canon_key=a.compute_canon_key(state))
    returned = driver.apply_licensed(state, cached, issuer.issue_license([cached.canon_key]))
    assert a.compute_canon_key(returned) != cached.canon_key

    # No-change acceptance, zero-cost repetition, and the zero-budget precheck.
    c = controller(fuel=1)
    unchanged = a.add_instance_action(0, (0,), name='mark A again')
    evaluation = c.evaluator.evaluate_candidate(c.state, unchanged, c.envelope, 1, 1)
    assert not evaluation.has_empirical_reference and evaluation.viable
    assert c.step([unchanged]).is_success and c.fuel == 0 and len(c.memory) == 1
    free = replace(unchanged, fuel_cost=0)
    c = controller(fuel=1)
    for _ in range(5):
        assert c.step([free]).is_success and c.fuel == 1
    assert len(c.memory) == 2 and c.step_count == 5
    c = controller(fuel=0)
    retained(c, snapshot(c), c.step([free]))

    # No eligible candidates and the controller's unlicensed-apply refusal.
    c = controller(abilities=a.AbilitySet(()))
    retained(c, snapshot(c), c.step([action]))
    c = controller()
    retained(c, snapshot(c), c.step([]))

    class EmptyLicense(a.ActionAuthorizer):
        def authorize_evaluation(self, evaluation):
            return self.issue_license([])

    c = controller(authorizer=EmptyLicense())
    retained(c, snapshot(c), c.step([action]))

    # Digests omit custom meanings; a flag is neither a complete-state check nor a trial.
    custom = a.CandidateAction('custom field', 1,
                              lambda m: replace(m, custom_domains={'extra': (0,)}))
    assert custom.apply(state).custom_domains != state.custom_domains
    assert a.canonical_model_digest(custom.apply(state)) == a.canonical_model_digest(state)
    assert not c.evaluator.check_empirical_reference(state, custom)

    # Deliberate contract violation in a disposable notebook: identity is not content preservation.
    mutable = replace(notebook(), custom_domains={})
    def mutate_input(m):
        m.custom_domains['changed'] = (0,)
        return m
    c = controller(state=mutable, authorizer=a.ActionAuthorizer(policy=lambda e: False))
    bad = a.CandidateAction('violates purity', 1, mutate_input)
    result = c.step([bad])
    assert result.is_refusal and c.state is mutable and mutable.custom_domains == {'changed': (0,)}

    # Exhaust the small valid mark states with an independent one-step set calculation.
    population = successes = refusals = 0
    for mask, ceiling in product(range(4), range(3)):
        marked = {i for i in range(2) if mask & (1 << i)}
        if len(marked) > ceiling:
            continue
        for fuel, cost, add, index, allow, horizon in product(range(4), range(3),
                (False, True), range(2), (False, True), range(1, 4)):
            action = (a.add_instance_action if add else a.remove_instance_action)(0, (index,), fuel_cost=cost)
            target = marked | {index} if add else marked - {index}
            expected = fuel > 0 and cost <= fuel and len(target) <= ceiling and allow
            c = controller(state=notebook(marked), ceiling=ceiling, fuel=fuel, horizon=horizon,
                           authorizer=a.ActionAuthorizer(policy=lambda e, permit=allow: permit))
            before = snapshot(c)
            result = c.step([action])
            assert result.is_success == expected
            if expected:
                assert c.state.insts == frozenset((0, (i,)) for i in target)
                assert c.fuel == fuel - cost and c.step_count == 1 and len(c.memory) == 1
                assert before[0].insts == frozenset((0, (i,)) for i in marked)
                assert c.evaluator.check_empirical_reference(before[0], action) == (marked != target)
                successes += 1
            else:
                retained(c, before, result)
                refusals += 1
            population += 1
    assert population == 2304 and population == successes + refusals
    return {'memory_cases': memory_checks, 'controller_cases': population,
            'successes': successes, 'refusals': refusals, 'computational_practice_questions': 9,
            'computed_key_refusals': 2, 'cached_key_trust_control': True,
            'purity_violation_control': True, 'physical_observations': 0,
            'learner_results': 0}


if __name__ == '__main__':
    print(json.dumps(worker() if sys.argv[1:] == ['--worker'] else check_examples(), sort_keys=True))
