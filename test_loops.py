"""
루프 라이브러리 테스트

구현된 루프 모듈들의 기본 동작 테스트
"""

import numpy as np
from brain_disorder_simulation.common.loops import (
    NegativeBiasLoop,
    HyperarousalLoop,
    ControlFailureLoop,
    EnergyCollapseLoop
)


def test_negative_bias_loop():
    """부정적 편향 루프 테스트"""
    print("=" * 60)
    print("테스트 1: NegativeBiasLoop (부정적 편향 루프)")
    print("=" * 60)
    
    loop = NegativeBiasLoop(initial_bias_strength=0.3)
    
    # 부정적 자극 처리
    print("\n1. 부정적 자극 처리:")
    result = loop.process_stimulus(stimulus_valence=-0.8, stimulus_intensity=1.0)
    print(f"   루프 강도: {loop.get_strength():.3f}")
    print(f"   활성화 여부: {loop.is_active()}")
    print(f"   편향 점수: {loop.get_bias_score():.3f}")
    
    # 긍정적 자극 처리
    print("\n2. 긍정적 자극 처리:")
    result = loop.process_stimulus(stimulus_valence=0.8, stimulus_intensity=1.0)
    print(f"   루프 강도: {loop.get_strength():.3f}")
    
    # 시간 경과
    print("\n3. 시간 경과 (10 스텝):")
    for i in range(10):
        loop.update(dt=0.1)
        if i % 2 == 0:
            print(f"   스텝 {i}: 루프 강도 = {loop.get_strength():.3f}, 편향 점수 = {loop.get_bias_score():.3f}")
    
    stats = loop.get_statistics()
    print(f"\n통계: {stats}")
    print("✅ NegativeBiasLoop 테스트 완료\n")


def test_hyperarousal_loop():
    """과각성 루프 테스트"""
    print("=" * 60)
    print("테스트 2: HyperarousalLoop (과각성 루프)")
    print("=" * 60)
    
    loop = HyperarousalLoop(initial_arousal=0.2)
    
    # 위협 감지
    print("\n1. 위협 감지:")
    result = loop.detect_threat(threat_intensity=0.7)
    print(f"   루프 강도: {loop.get_strength():.3f}")
    print(f"   각성 수준: {result['arousal_level']:.3f}")
    print(f"   수면 질: {result['sleep_quality']:.3f}")
    
    # 시간 경과
    print("\n2. 시간 경과 (10 스텝):")
    for i in range(10):
        loop.update(dt=0.1)
        if i % 2 == 0:
            arousal_score = loop.get_arousal_score()
            print(f"   스텝 {i}: 루프 강도 = {loop.get_strength():.3f}, 과각성 점수 = {arousal_score:.3f}")
    
    stats = loop.get_statistics()
    print(f"\n통계: {stats}")
    print("✅ HyperarousalLoop 테스트 완료\n")


def test_control_failure_loop():
    """제어 실패 루프 테스트"""
    print("=" * 60)
    print("테스트 3: ControlFailureLoop (제어 실패 루프)")
    print("=" * 60)
    
    loop = ControlFailureLoop(initial_impairment=0.4)
    
    # 부정적 사고 처리
    print("\n1. 부정적 사고 처리:")
    result = loop.process_negative_thought(thought_intensity=0.8)
    print(f"   억제 성공: {result['inhibition_success']}")
    print(f"   루프 강도: {loop.get_strength():.3f}")
    print(f"   제어 점수: {loop.get_control_score():.3f}")
    
    # 인지 제어 시도
    print("\n2. 인지 제어 시도:")
    result = loop.attempt_cognitive_control(task_difficulty=0.7)
    print(f"   제어 성공: {result['success']}")
    print(f"   성공 확률: {result['success_probability']:.3f}")
    print(f"   루프 강도: {loop.get_strength():.3f}")
    
    # 시간 경과
    print("\n3. 시간 경과 (10 스텝):")
    for i in range(10):
        loop.update(dt=0.1)
        if i % 2 == 0:
            control_score = loop.get_control_score()
            print(f"   스텝 {i}: 루프 강도 = {loop.get_strength():.3f}, 제어 점수 = {control_score:.3f}")
    
    stats = loop.get_statistics()
    print(f"\n통계: {stats}")
    print("✅ ControlFailureLoop 테스트 완료\n")


def test_energy_collapse_loop():
    """에너지 붕괴 루프 테스트"""
    print("=" * 60)
    print("테스트 4: EnergyCollapseLoop (에너지 붕괴 루프)")
    print("=" * 60)
    
    loop = EnergyCollapseLoop(initial_energy=80.0, initial_depletion_rate=0.3)
    
    # 에너지 소비
    print("\n1. 에너지 소비:")
    result = loop.consume_energy(cognitive_load=0.6, stress_level=0.5)
    print(f"   에너지: {result['energy_after']:.1f}")
    print(f"   소비량: {result['consumption']:.3f}")
    
    # 에너지 업데이트
    print("\n2. 에너지 업데이트 (10 스텝):")
    for i in range(10):
        result = loop.update_energy(cognitive_load=0.3, stress_level=0.2, dt=0.1)
        if i % 2 == 0:
            energy_score = loop.get_energy_score()
            print(f"   스텝 {i}: 에너지 = {result['current_energy']:.1f}, "
                  f"루프 강도 = {loop.get_strength():.3f}, 에너지 점수 = {energy_score:.3f}")
    
    stats = loop.get_statistics()
    print(f"\n통계: {stats}")
    print("✅ EnergyCollapseLoop 테스트 완료\n")


def main():
    """모든 루프 테스트 실행"""
    print("\n" + "=" * 60)
    print("루프 라이브러리 통합 테스트")
    print("=" * 60 + "\n")
    
    try:
        test_negative_bias_loop()
        test_hyperarousal_loop()
        test_control_failure_loop()
        test_energy_collapse_loop()
        
        print("=" * 60)
        print("✅ 모든 루프 테스트 성공!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

