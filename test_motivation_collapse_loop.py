"""
MotivationCollapseLoop 테스트

동기 붕괴 루프의 기본 동작 확인
"""

import numpy as np
from brain_disorder_simulation.common.loops import MotivationCollapseLoop


def test_motivation_collapse_loop():
    """동기 붕괴 루프 기본 테스트"""
    print("=" * 60)
    print("MotivationCollapseLoop 테스트")
    print("=" * 60)
    
    # 루프 생성
    loop = MotivationCollapseLoop(initial_motivation_deficit=0.3)
    
    print("\n1. 초기 상태:")
    print(f"  - 루프 강도: {loop.get_strength():.3f}")
    print(f"  - 보상 민감도: {loop.get_state().reward_sensitivity:.3f}")
    print(f"  - 동기 수준: {loop.get_state().motivation_level:.3f}")
    print(f"  - 무쾌감증: {loop.get_state().anhedonia:.3f}")
    
    # 보상 처리 테스트
    print("\n2. 보상 처리 테스트:")
    result1 = loop.process_reward(reward_value=0.8, effort_required=0.3)
    print(f"  - 보상 가치: 0.8, 노력: 0.3")
    print(f"  - 인지된 보상: {result1['perceived_reward']:.3f}")
    print(f"  - 즐거움: {result1['pleasure']:.3f}")
    print(f"  - 동기 증가: {result1['motivation_gain']:.3f}")
    print(f"  - 행동 가능: {result1['can_engage']}")
    
    # 보상 실패 테스트 (루프 트리거)
    print("\n3. 보상 실패 테스트 (루프 트리거):")
    result2 = loop.process_reward(reward_value=0.1, effort_required=0.8)
    print(f"  - 보상 가치: 0.1, 노력: 0.8")
    print(f"  - 동기 증가: {result2['motivation_gain']:.3f}")
    print(f"  - 행동 가능: {result2['can_engage']}")
    print(f"  - 루프 강도: {loop.get_strength():.3f}")
    print(f"  - 보상 실패 횟수: {loop.get_state().reward_failures}")
    
    # 동역학 업데이트
    print("\n4. 동역학 업데이트:")
    loop._update_dynamics(dt=1.0)
    print(f"  - 루프 강도: {loop.get_strength():.3f}")
    print(f"  - 보상 민감도: {loop.get_state().reward_sensitivity:.3f}")
    print(f"  - 동기 수준: {loop.get_state().motivation_level:.3f}")
    print(f"  - 무쾌감증: {loop.get_state().anhedonia:.3f}")
    
    # 행동 평가 테스트
    print("\n5. 행동 평가 테스트:")
    eval_result = loop.evaluate_action(
        expected_reward=0.6,
        effort_required=0.5,
        delay=0.0
    )
    print(f"  - 예상 보상: 0.6, 노력: 0.5")
    print(f"  - 총 가치: {eval_result['total_value']:.3f}")
    print(f"  - 행동 결정: {eval_result['should_act']}")
    print(f"  - 동기 충분: {eval_result['motivation_sufficient']}")
    
    # 패턴 분석
    print("\n6. 패턴 분석:")
    patterns = loop._analyze_patterns()
    print(f"  - 동기 붕괴 심각도: {patterns['collapse_severity']:.3f}")
    print(f"  - 보상 민감도: {patterns['reward_sensitivity']:.3f}")
    print(f"  - 동기 수준: {patterns['motivation_level']:.3f}")
    print(f"  - 목표 지향 행동: {patterns['goal_directed_behavior']:.3f}")
    print(f"  - 무쾌감증: {patterns['anhedonia']:.3f}")
    print(f"  - 노력 비용: {patterns['effort_cost']:.3f}")
    
    # 동기 점수
    print("\n7. 동기 점수:")
    score = loop.get_motivation_score()
    print(f"  - 동기 점수: {score:.3f} (낮을수록 동기 결핍)")
    
    print("\n✅ MotivationCollapseLoop 테스트 완료\n")


if __name__ == "__main__":
    test_motivation_collapse_loop()

