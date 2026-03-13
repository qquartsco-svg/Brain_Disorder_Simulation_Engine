"""Alpha vNext controller MVP smoke test.

- baseline(plant) is untouched.
- controller runs on top and outputs an action.
"""

from brain_disorder_simulation.unified import UnifiedDisorderSimulator
from brain_disorder_simulation.alpha.self_regulation_controller import SelfRegulationController
from brain_disorder_simulation.alpha.alpha_brain_runner import AlphaBrainRunner


def main():
    plant = UnifiedDisorderSimulator(seed=42)
    controller = SelfRegulationController(seed=0)
    runner = AlphaBrainRunner(plant=plant, controller=controller)

    out = runner.run_episode_adhd(duration=5.0, task_importance=0.6)
    assert out['controller_action'] is not None
    assert len(out['logs']) == 1
    print('✅ alpha controller MVP smoke ok')


if __name__ == '__main__':
    main()
