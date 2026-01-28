"""
리팩터링된 엔진 통합 테스트

루프 라이브러리 기반으로 리팩터링된 엔진들의 동작 확인
"""

import numpy as np
from brain_disorder_simulation.common.negative_bias_engine import NegativeBiasEngine
from brain_disorder_simulation.common.cognitive_control_engine import CognitiveControlEngine
from brain_disorder_simulation.common.energy_depletion_engine import EnergyDepletionEngine


def test_negative_bias_engine():
    """부정적 편향 엔진 테스트"""
    print("=" * 60)
    print("테스트 1: NegativeBiasEngine (루프 기반 리팩터링)")
    print("=" * 60)
    
    engine = NegativeBiasEngine(negative_bias_strength=0.4)
    
    # 부정적 자극 처리
    print("\n1. 부정적 자극 처리:")
    result = engine.process_stimulus(stimulus_valence=-0.7, stimulus_intensity=1.0)
    print(f"   인지된 정서가: {result['perceived_valence']:.3f}")
    print(f"   인지된 강도: {result['perceived_intensity']:.3f}")
    print(f"   위협 감지: {result['threat_detected']}")
    print(f"   루프 트리거: {result.get('loop_triggered', False)}")
    print(f"   편향 점수: {engine.get_bias_score():.3f}")
    print(f"   루프 강도: {engine.loop.get_strength():.3f}")
    
    # 긍정적 자극 처리
    print("\n2. 긍정적 자극 처리:")
    result = engine.process_stimulus(stimulus_valence=0.8, stimulus_intensity=1.0)
    print(f"   인지된 정서가: {result['perceived_valence']:.3f}")
    print(f"   인지된 강도: {result['perceived_intensity']:.3f}")
    
    # 시간 경과
    print("\n3. 시간 경과 (5 스텝):")
    for i in range(5):
        engine.update_rumination(dt=0.1)
        if i % 2 == 0:
            print(f"   스텝 {i}: 편향 점수 = {engine.get_bias_score():.3f}, "
                  f"루프 강도 = {engine.loop.get_strength():.3f}")
    
    print("✅ NegativeBiasEngine 테스트 완료\n")


def test_cognitive_control_engine():
    """인지 제어 엔진 테스트"""
    print("=" * 60)
    print("테스트 2: CognitiveControlEngine (루프 기반 리팩터링)")
    print("=" * 60)
    
    engine = CognitiveControlEngine(control_impairment=0.5)
    
    # 부정적 사고 처리
    print("\n1. 부정적 사고 처리:")
    result = engine.process_negative_thought(thought_intensity=0.8)
    print(f"   억제 성공: {result['inhibition_success']}")
    print(f"   부정적 루프 강도: {result['negative_loop_strength']:.3f}")
    print(f"   제어 점수: {engine.get_control_score():.3f}")
    print(f"   루프 강도: {engine.loop.get_strength():.3f}")
    
    # 인지 제어 시도
    print("\n2. 인지 제어 시도:")
    result = engine.attempt_cognitive_control(task_difficulty=0.6)
    print(f"   제어 성공: {result['success']}")
    print(f"   성공 확률: {result['success_probability']:.3f}")
    print(f"   처리 용량: {result['processing_capacity']:.3f}")
    
    # 시간 경과
    print("\n3. 시간 경과 (5 스텝):")
    for i in range(5):
        engine.update_negative_loop(dt=0.1)
        if i % 2 == 0:
            print(f"   스텝 {i}: 제어 점수 = {engine.get_control_score():.3f}, "
                  f"루프 강도 = {engine.loop.get_strength():.3f}")
    
    print("✅ CognitiveControlEngine 테스트 완료\n")


def test_energy_depletion_engine():
    """에너지 고갈 엔진 테스트"""
    print("=" * 60)
    print("테스트 3: EnergyDepletionEngine (루프 기반 리팩터링)")
    print("=" * 60)
    
    engine = EnergyDepletionEngine(depletion_rate=0.4)
    
    # 에너지 업데이트
    print("\n1. 에너지 업데이트 (10 스텝):")
    for i in range(10):
        result = engine.update_energy(cognitive_load=0.3, stress_level=0.2, dt=0.1)
        if i % 3 == 0:
            energy_score = engine.get_energy_score()
            print(f"   스텝 {i}: 에너지 = {result['current_energy']:.1f}, "
                  f"에너지 점수 = {energy_score:.3f}, "
                  f"루프 강도 = {engine.loop.get_strength():.3f}")
    
    # 에너지 소비
    print("\n2. 에너지 소비:")
    engine.loop.consume_energy(cognitive_load=0.7, stress_level=0.5)
    result = engine.update_energy(cognitive_load=0.0, stress_level=0.0, dt=0.1)
    print(f"   에너지: {result['current_energy']:.1f}")
    print(f"   소비량: {result['consumption']:.3f}")
    print(f"   회복량: {result['recovery']:.3f}")
    
    print("✅ EnergyDepletionEngine 테스트 완료\n")


def main():
    """모든 엔진 테스트 실행"""
    print("\n" + "=" * 60)
    print("리팩터링된 엔진 통합 테스트")
    print("=" * 60 + "\n")
    
    try:
        test_negative_bias_engine()
        test_cognitive_control_engine()
        test_energy_depletion_engine()
        
        print("=" * 60)
        print("✅ 모든 엔진 리팩터링 테스트 성공!")
        print("=" * 60)
        print("\n리팩터링 완료:")
        print("  - NegativeBiasEngine → NegativeBiasLoop 사용")
        print("  - CognitiveControlEngine → ControlFailureLoop 사용")
        print("  - EnergyDepletionEngine → EnergyCollapseLoop 사용")
        print("\n호환성: 기존 인터페이스 유지, 내부적으로 루프 라이브러리 사용")
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

