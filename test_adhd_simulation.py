"""UnifiedDisorderSimulator ADHD 통합 테스트"""

from brain_disorder_simulation.unified import UnifiedDisorderSimulator


def main():
    sim = UnifiedDisorderSimulator(seed=42)
    results = sim.simulate_adhd(duration=10.0, task_importance=0.6)
    print('pattern:', results['overall_pattern'])
    print('mean_attention:', results['mean_attention'])
    print('mean_impulsivity:', results['mean_impulsivity'])
    print('loop keys:', list(results.get('loop_analysis', {}).get('active_loops', {}).keys()))


if __name__ == '__main__':
    main()
