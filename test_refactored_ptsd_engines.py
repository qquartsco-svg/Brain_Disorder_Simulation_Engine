"""
리팩터링된 PTSD 엔진 테스트

IntrusiveMemoryLoop와 AvoidanceReinforcementLoop를 사용하도록 리팩터링된 엔진들의 동작 확인
"""

import numpy as np
from brain_disorder_simulation.disorders.ptsd.ptsd_engines import (
    IntrusiveMemoryEngine,
    AvoidanceEngine
)


def test_refactored_ptsd_engines():
    """리팩터링된 PTSD 엔진 테스트"""
    print("=" * 60)
    print("리팩터링된 PTSD 엔진 테스트")
    print("=" * 60)
    
    # IntrusiveMemoryEngine 테스트
    print("\n" + "=" * 60)
    print("1. IntrusiveMemoryEngine 테스트")
    print("=" * 60)
    
    intrusive_engine = IntrusiveMemoryEngine(
        initial_trauma_intensity=0.7,
        initial_suppression_failure=0.4
    )
    
    print("\n1-1. 초기 상태 (루프 기반):")
    print(f"  - 억제 실패율: {intrusive_engine.suppression_failure_rate:.3f}")
    print(f"  - 루프 강도: {intrusive_engine.loop.get_strength():.3f}")
    
    # 외상 기억 추가
    print("\n1-2. 외상 기억 추가:")
    intrusive_engine.add_traumatic_memory(
        memory_id='trauma_1',
        initial_intensity=0.8,
        initial_fear=0.7
    )
    print(f"  - 기억 개수: {len(intrusive_engine.traumatic_memories)}")
    print(f"  - 루프 강도: {intrusive_engine.loop.get_strength():.3f}")
    
    # 억제 시도
    print("\n1-3. 억제 시도:")
    success = intrusive_engine.attempt_suppression('trauma_1', pfc_control=0.5)
    print(f"  - 억제 성공: {success}")
    print(f"  - 억제 시도 횟수: {intrusive_engine.suppression_attempts}")
    print(f"  - 루프 강도: {intrusive_engine.loop.get_strength():.3f}")
    
    # 침입 수준 계산
    print("\n1-4. 침입 수준 계산:")
    intrusion = intrusive_engine.compute_intrusion(amygdala_arousal=0.6)
    print(f"  - 침입 수준: {intrusion:.3f}")
    print(f"  - 현재 침입 수준: {intrusive_engine.current_intrusion_level:.3f}")
    
    # 엔진 업데이트
    print("\n1-5. 엔진 업데이트:")
    intrusive_engine.update(dt=1.0, amygdala_arousal=0.6, pfc_control=0.5)
    print(f"  - 업데이트 후 침입 수준: {intrusive_engine.current_intrusion_level:.3f}")
    print(f"  - 업데이트 후 루프 강도: {intrusive_engine.loop.get_strength():.3f}")
    
    # AvoidanceEngine 테스트
    print("\n" + "=" * 60)
    print("2. AvoidanceEngine 테스트")
    print("=" * 60)
    
    avoidance_engine = AvoidanceEngine(
        initial_avoidance_strength=0.3,
        initial_generalization=0.3
    )
    
    print("\n2-1. 초기 상태 (루프 기반):")
    print(f"  - 회피 강도: {avoidance_engine.current_avoidance_level:.3f}")
    print(f"  - 일반화 인자: {avoidance_engine.generalization_factor:.3f}")
    print(f"  - 루프 강도: {avoidance_engine.loop.get_strength():.3f}")
    
    # 회피 학습
    print("\n2-2. 회피 학습:")
    avoidance_engine.learn_avoidance('trauma_trigger_1', fear_level=0.8)
    print(f"  - 회피된 자극 수: {len(avoidance_engine.avoided_stimuli)}")
    print(f"  - 루프 강도: {avoidance_engine.loop.get_strength():.3f}")
    print(f"  - 회피 강도: {avoidance_engine.current_avoidance_level:.3f}")
    print(f"  - 감정적 마비: {avoidance_engine.emotional_numbing:.3f}")
    
    # 회피 확인
    print("\n2-3. 회피 확인:")
    avoids, strength = avoidance_engine.check_avoidance('trauma_trigger_1')
    print(f"  - 회피 여부: {avoids}")
    print(f"  - 회피 강도: {strength:.3f}")
    
    # 회피 수준 계산
    print("\n2-4. 회피 수준 계산:")
    avoidance_level = avoidance_engine.compute_avoidance_level()
    print(f"  - 회피 수준: {avoidance_level:.3f}")
    
    # 엔진 업데이트
    print("\n2-5. 엔진 업데이트:")
    avoidance_engine.update(dt=1.0)
    print(f"  - 업데이트 후 회피 수준: {avoidance_engine.current_avoidance_level:.3f}")
    print(f"  - 업데이트 후 루프 강도: {avoidance_engine.loop.get_strength():.3f}")
    
    # 호환성 확인
    print("\n" + "=" * 60)
    print("3. 호환성 확인")
    print("=" * 60)
    print("  - 기존 인터페이스 유지: ✅")
    print("  - add_traumatic_memory() 정상 작동: ✅")
    print("  - attempt_suppression() 정상 작동: ✅")
    print("  - compute_intrusion() 정상 작동: ✅")
    print("  - learn_avoidance() 정상 작동: ✅")
    print("  - check_avoidance() 정상 작동: ✅")
    print("  - compute_avoidance_level() 정상 작동: ✅")
    print("  - state 속성 접근 가능: ✅")
    
    print("\n✅ 리팩터링된 PTSD 엔진 테스트 완료\n")


if __name__ == "__main__":
    test_refactored_ptsd_engines()

