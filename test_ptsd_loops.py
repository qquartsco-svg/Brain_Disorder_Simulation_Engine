"""
PTSD 루프 테스트

IntrusiveMemoryLoop와 AvoidanceReinforcementLoop의 기본 동작 확인
"""

import numpy as np
from brain_disorder_simulation.common.loops import (
    IntrusiveMemoryLoop,
    AvoidanceReinforcementLoop
)


def test_intrusive_memory_loop():
    """침입 기억 루프 기본 테스트"""
    print("=" * 60)
    print("IntrusiveMemoryLoop 테스트")
    print("=" * 60)
    
    # 루프 생성
    loop = IntrusiveMemoryLoop(
        initial_trauma_intensity=0.7,
        initial_suppression_failure=0.4
    )
    
    print("\n1. 초기 상태:")
    print(f"  - 루프 강도: {loop.get_strength():.3f}")
    print(f"  - 기억 강도: {loop.get_state().memory_intensity:.3f}")
    print(f"  - 억제 실패율: {loop.get_state().suppression_failure:.3f}")
    print(f"  - 공포 수준: {loop.get_state().associated_fear:.3f}")
    
    # 외상 기억 추가
    print("\n2. 외상 기억 추가:")
    loop.add_traumatic_memory(
        memory_id='trauma_1',
        initial_intensity=0.8,
        initial_fear=0.7
    )
    print(f"  - 기억 개수: {len(loop.get_state().traumatic_memories)}")
    print(f"  - 루프 강도: {loop.get_strength():.3f}")
    
    # 억제 시도 실패 (루프 트리거)
    print("\n3. 억제 시도 실패 (루프 트리거):")
    success = loop.attempt_suppression('trauma_1', pfc_control=0.3)
    print(f"  - 억제 성공: {success}")
    print(f"  - 루프 강도: {loop.get_strength():.3f}")
    print(f"  - 침입 빈도: {loop.get_state().intrusion_frequency:.3f}")
    print(f"  - 억제 시도 횟수: {loop.get_state().suppression_attempts}")
    
    # 침입 수준 계산
    print("\n4. 침입 수준 계산:")
    intrusion = loop.compute_intrusion(amygdala_arousal=0.7)
    print(f"  - 침입 수준: {intrusion:.3f}")
    print(f"  - 루프 강도: {loop.get_strength():.3f}")
    
    # 동역학 업데이트
    print("\n5. 동역학 업데이트:")
    loop._update_dynamics(dt=1.0)
    print(f"  - 루프 강도: {loop.get_strength():.3f}")
    print(f"  - 기억 강도: {loop.get_state().memory_intensity:.3f}")
    print(f"  - 억제 실패율: {loop.get_state().suppression_failure:.3f}")
    
    # 패턴 분석
    print("\n6. 패턴 분석:")
    patterns = loop._analyze_patterns()
    print(f"  - 침입 심각도: {patterns['intrusion_severity']:.3f}")
    print(f"  - 기억 강도: {patterns['memory_intensity']:.3f}")
    print(f"  - 침입 빈도: {patterns['intrusion_frequency']:.3f}")
    
    print("\n✅ IntrusiveMemoryLoop 테스트 완료\n")


def test_avoidance_reinforcement_loop():
    """회피 강화 루프 기본 테스트"""
    print("=" * 60)
    print("AvoidanceReinforcementLoop 테스트")
    print("=" * 60)
    
    # 루프 생성
    loop = AvoidanceReinforcementLoop(
        initial_avoidance_strength=0.3,
        initial_generalization=0.3
    )
    
    print("\n1. 초기 상태:")
    print(f"  - 루프 강도: {loop.get_strength():.3f}")
    print(f"  - 회피 강도: {loop.get_state().avoidance_strength:.3f}")
    print(f"  - 일반화 인자: {loop.get_state().generalization_factor:.3f}")
    print(f"  - 감정적 마비: {loop.get_state().emotional_numbing:.3f}")
    
    # 회피 학습
    print("\n2. 회피 학습 (루프 트리거):")
    loop.learn_avoidance('trauma_trigger_1', fear_level=0.8)
    print(f"  - 회피된 자극 수: {loop.get_state().avoided_stimuli_count}")
    print(f"  - 루프 강도: {loop.get_strength():.3f}")
    print(f"  - 회피 강도: {loop.get_state().avoidance_strength:.3f}")
    print(f"  - 감정적 마비: {loop.get_state().emotional_numbing:.3f}")
    
    # 회피 확인
    print("\n3. 회피 확인:")
    avoids, strength = loop.check_avoidance('trauma_trigger_1')
    print(f"  - 회피 여부: {avoids}")
    print(f"  - 회피 강도: {strength:.3f}")
    
    # 일반화된 회피 확인
    print("\n4. 일반화된 회피 확인:")
    avoids2, strength2 = loop.check_avoidance('trauma_trigger_similar')
    print(f"  - 유사 자극 회피 여부: {avoids2}")
    print(f"  - 회피 강도: {strength2:.3f}")
    
    # 회피 수준 계산
    print("\n5. 회피 수준 계산:")
    avoidance_level = loop.compute_avoidance_level()
    print(f"  - 회피 수준: {avoidance_level:.3f}")
    
    # 동역학 업데이트
    print("\n6. 동역학 업데이트:")
    loop._update_dynamics(dt=1.0)
    print(f"  - 루프 강도: {loop.get_strength():.3f}")
    print(f"  - 회피 강도: {loop.get_state().avoidance_strength:.3f}")
    print(f"  - 일반화 인자: {loop.get_state().generalization_factor:.3f}")
    
    # 패턴 분석
    print("\n7. 패턴 분석:")
    patterns = loop._analyze_patterns()
    print(f"  - 회피 심각도: {patterns['avoidance_severity']:.3f}")
    print(f"  - 회피 강도: {patterns['avoidance_strength']:.3f}")
    print(f"  - 감정적 마비: {patterns['emotional_numbing']:.3f}")
    
    print("\n✅ AvoidanceReinforcementLoop 테스트 완료\n")


if __name__ == "__main__":
    test_intrusive_memory_loop()
    test_avoidance_reinforcement_loop()

