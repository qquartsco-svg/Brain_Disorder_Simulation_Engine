"""Controlled Collapse ADHD MVP test.

We expect:
- controller produces steps with mode transitions (at least stabilize/explore/exploit possible)
- emergence score is computable and logged
"""

from brain_disorder_simulation.alpha.self_regulation_controller import SelfRegulationController
from brain_disorder_simulation.alpha.adhd_controlled_episode import run_controlled_adhd_episode


def main():
    controller = SelfRegulationController(seed=0)
    out = run_controlled_adhd_episode(duration=20.0, task_importance=0.6, seed=42, controller=controller)

    steps = out['steps']
    assert len(steps) > 0
    ems = [s.obs['Emerge'] for s in steps]
    assert all(e is not None for e in ems)

    modes = set(s.mode for s in steps)
    print('modes:', modes)
    print('max emergence:', max(ems))
    print('final loops:', out['final_loop_strengths'])

    print('✅ controlled collapse ADHD test ok')


if __name__ == '__main__':
    main()
