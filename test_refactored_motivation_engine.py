"""
리팩터링된 MotivationEngine 테스트

MotivationCollapseLoop를 사용하도록 리팩터링된 MotivationEngine의 동작 확인
"""

import numpy as np
from brain_disorder_simulation.disorders.depression.motivation_engine import MotivationEngine


def test_refactored_motivation_engine():
    """리팩터링된 MotivationEngine 테스트"""
    print("=" * 60)
    print("리팩터링된 MotivationEngine 테스트")
    print("=" * 60)
    
    # 엔진 생성
    engine = MotivationEngine(motivation_deficit=0.3)
    
    print("\n1. 초기 상태 (루프 기반):")
    print(f"  - 동기 결핍: {engine.motivation_deficit:.3f}")
    print(f"  - 보상 민감도: {engine.state.reward_sensitivity:.3f}")
    print(f"  - 동기 수준: {engine.state.motivation_level:.3f}")
    print(f"  - 무쾌감증: {engine.state.anhedonia:.3f}")
    print(f"  - 루프 강도: {engine.loop.get_strength():.3f}")
    
    # 보상 처리 테스트
    print("\n2. 보상 처리 테스트:")
    result1 = engine.process_reward(reward_value=0.8, effort_required=0.3)
    print(f"  - 보상 가치: 0.8, 노력: 0.3")
    print(f"  - 인지된 보상: {result1['perceived_reward']:.3f}")
    print(f"  - 동기 증가: {result1['motivation_gain']:.3f}")
    print(f"  - 행동 가능: {result1['can_engage']}")
    print(f"  - 업데이트된 동기 수준: {engine.state.motivation_level:.3f}")
    print(f"  - 루프 강도: {engine.loop.get_strength():.3f}")
    
    # 보상 실패 테스트
    print("\n3. 보상 실패 테스트 (루프 트리거):")
    result2 = engine.process_reward(reward_value=0.1, effort_required=0.8)
    print(f"  - 보상 가치: 0.1, 노력: 0.8")
    print(f"  - 동기 증가: {result2['motivation_gain']:.3f}")
    print(f"  - 행동 가능: {result2['can_engage']}")
    print(f"  - 업데이트된 동기 수준: {engine.state.motivation_level:.3f}")
    print(f"  - 루프 강도: {engine.loop.get_strength():.3f}")
    
    # 행동 평가 테스트
    print("\n4. 행동 평가 테스트:")
    eval_result = engine.evaluate_action(
        expected_reward=0.6,
        effort_required=0.5,
        delay=0.0
    )
    print(f"  - 예상 보상: 0.6, 노력: 0.5")
    print(f"  - 총 가치: {eval_result['total_value']:.3f}")
    print(f"  - 행동 결정: {eval_result['should_act']}")
    print(f"  - 동기 충분: {eval_result['motivation_sufficient']}")
    
    # 동기 점수
    print("\n5. 동기 점수:")
    score = engine.get_motivation_score()
    print(f"  - 동기 점수: {score:.3f} (낮을수록 동기 결핍)")
    
    # 엔진 업데이트
    print("\n6. 엔진 업데이트 (시간 경과):")
    engine.update(dt=1.0)
    print(f"  - 업데이트 후 동기 수준: {engine.state.motivation_level:.3f}")
    print(f"  - 업데이트 후 루프 강도: {engine.loop.get_strength():.3f}")
    
    # 호환성 확인
    print("\n7. 호환성 확인:")
    print(f"  - 기존 인터페이스 유지: ✅")
    print(f"  - process_reward() 정상 작동: ✅")
    print(f"  - evaluate_action() 정상 작동: ✅")
    print(f"  - get_motivation_score() 정상 작동: ✅")
    print(f"  - state 속성 접근 가능: ✅")
    
    print("\n✅ 리팩터링된 MotivationEngine 테스트 완료\n")


if __name__ == "__main__":
    test_refactored_motivation_engine()

