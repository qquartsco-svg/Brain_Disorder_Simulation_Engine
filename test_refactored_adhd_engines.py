"""리팩터링된 ADHD 엔진 테스트

AttentionControlEngine / ImpulseControlEngine이 루프를 가지며 동작하는지 확인
"""

from brain_disorder_simulation.disorders.adhd.adhd_engines import AttentionControlEngine, ImpulseControlEngine


def main():
    print('='*60)
    print('리팩터링된 ADHD 엔진 테스트')
    print('='*60)

    att = AttentionControlEngine()
    res = att.maintain_attention(
        task={'importance': 0.6},
        distractions=[{'intensity': 0.9, 'relevance': 0.8}],
        time_elapsed=10.0
    )
    print('attention_score:', res['attention_score'])
    print('attention_loop_strength:', att.loop.get_strength())

    imp = ImpulseControlEngine()
    r = imp.control_impulse(
        immediate_reward=0.4,
        delayed_reward=1.0,
        delay_time=30.0,
        goal_context={'strength': 0.3}
    )
    print('impulse_score:', r['impulse_score'])
    print('rpe_loop_strength:', imp.loop.get_strength())

    print('\n✅ ADHD 엔진 테스트 완료')


if __name__ == '__main__':
    main()
