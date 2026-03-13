"""Inference/Emergence report smoke test."""

from brain_disorder_simulation.unified import UnifiedDisorderSimulator


def main():
    sim = UnifiedDisorderSimulator(seed=1)
    # ADHD quick run
    results = sim.simulate_adhd(duration=5.0, task_importance=0.6)
    text = sim.explain_patterns(results)
    assert 'INFERENCE STATE' in text
    assert 'EMERGENCE/COMPENSATION' in text
    print('✅ inference/emergence report present')


if __name__ == '__main__':
    main()
