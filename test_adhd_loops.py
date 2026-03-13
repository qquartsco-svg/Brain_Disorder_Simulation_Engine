"""ADHD 루프 테스트

AttentionInstabilityLoop / RewardPredictionErrorLoop 기본 동작 확인
"""

from brain_disorder_simulation.common.loops import AttentionInstabilityLoop, RewardPredictionErrorLoop


def main():
    print('='*60)
    print('AttentionInstabilityLoop 테스트')
    print('='*60)
    loop = AttentionInstabilityLoop(initial_instability=0.2)
    for t in range(20):
        att = 0.8 if t < 5 else 0.3
        dist = 0.1 if t < 5 else 0.9
        loop.observe(attention_score=att, distraction_level=dist, dt=0.1, threshold=0.5)
    print('loop_strength:', f"{loop.get_strength():.3f}")
    print('modifiers:', loop.get_modifiers())

    print('\n' + '='*60)
    print('RewardPredictionErrorLoop 테스트')
    print('='*60)
    rpe = RewardPredictionErrorLoop(initial_rpe_instability=0.1)
    for i in range(20):
        expected = 0.6
        received = 0.9 if i % 2 == 0 else 0.2
        rpe.observe(expected_reward=expected, received_reward=received, dt=0.1)
    print('loop_strength:', f"{rpe.get_strength():.3f}")
    print('modifiers:', rpe.get_modifiers())

    print('\n✅ ADHD 루프 테스트 완료')


if __name__ == '__main__':
    main()
