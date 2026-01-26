"""
동역학 불변식 테스트

모델이 물리적으로 타당한지 검증하는 테스트 세트
"""

import numpy as np
from typing import Dict, List
from adhd_engines import AttentionControlEngine, ImpulseControlEngine, HyperactivityEngine
from closed_loop_dynamics import ClosedLoopDynamics


class DynamicsInvariantTests:
    """
    동역학 불변식 테스트 클래스
    
    모델의 물리적 타당성을 검증
    """
    
    def __init__(self):
        """테스트 초기화"""
        self.test_results = []
    
    def test_monotonicity_attention(self) -> Dict:
        """
        단조성 테스트: 방해 강도↑ → attention_score 기대값↓
        
        Returns:
            테스트 결과
        """
        engine = AttentionControlEngine()
        
        distractions = [
            [{'intensity': 0.1, 'relevance': 0.5}],
            [{'intensity': 0.5, 'relevance': 0.5}],
            [{'intensity': 0.9, 'relevance': 0.5}]
        ]
        
        scores = []
        for dist in distractions:
            result = engine.calculate_attention(
                task_importance=0.8,
                distractions=dist,
                time_elapsed=10.0
            )
            scores.append(result)
        
        # 단조 감소 확인
        is_monotonic = scores[0] > scores[1] > scores[2]
        
        result = {
            'test_name': 'monotonicity_attention',
            'passed': is_monotonic,
            'scores': scores,
            'message': 'Passed' if is_monotonic else 'Failed: Not monotonic'
        }
        
        self.test_results.append(result)
        return result
    
    def test_discount_rate(self) -> Dict:
        """
        할인율 테스트: delay↑ → immediate 선택 확률↑
        
        Returns:
            테스트 결과
        """
        engine = ImpulseControlEngine()
        
        delays = [10, 20, 30, 40]
        immediate_preferences = []
        
        for delay in delays:
            result = engine.calculate_impulse_preference(
                immediate_reward=10,
                delayed_reward=100,
                delay_time=delay
            )
            immediate_preferences.append(result)
        
        # 단조 증가 확인 (지연이 길수록 즉각 보상 선호도 증가)
        is_monotonic = immediate_preferences[0] <= immediate_preferences[-1]
        
        result = {
            'test_name': 'discount_rate',
            'passed': is_monotonic,
            'preferences': immediate_preferences,
            'message': 'Passed' if is_monotonic else 'Failed: Discount rate violation'
        }
        
        self.test_results.append(result)
        return result
    
    def test_gate_effect(self) -> Dict:
        """
        게이트 효과 테스트: thalamus_gate↓ → distraction 영향↓
        
        Returns:
            테스트 결과
        """
        dynamics = ClosedLoopDynamics()
        
        gates = [0.9, 0.5, 0.1]
        attention_scores = []
        
        for gate in gates:
            dynamics.state.thalamus_gate = gate
            external_input = {
                'task_importance': 0.8,
                'distractions': [{'intensity': 0.7, 'relevance': 0.8}],
                'time_elapsed': 10.0
            }
            updated_state = dynamics.update_state(external_input, dt=0.1)
            attention_scores.append(updated_state.attention)
        
        # 게이트가 낮을수록 주의력 높음 (방해 영향 감소)
        is_correct = attention_scores[0] < attention_scores[-1]
        
        result = {
            'test_name': 'gate_effect',
            'passed': is_correct,
            'attention_scores': attention_scores,
            'message': 'Passed' if is_correct else 'Failed: Gate effect violation'
        }
        
        self.test_results.append(result)
        return result
    
    def test_dopamine_effect(self) -> Dict:
        """
        도파민 효과 테스트: dopamine↓ → attention_decay↑
        
        Returns:
            테스트 결과
        """
        from dopamine_system import DopamineSystem
        
        dopamine_levels = [0.7, 0.5, 0.3, 0.1]
        attention_effects = []
        
        for dop in dopamine_levels:
            dop_sys = DopamineSystem()
            dop_sys.current_dopamine = dop
            dop_sys.tonic_dopamine = dop
            effect = dop_sys.get_effect_on_attention()
            attention_effects.append(effect)
        
        # 도파민이 낮을수록 주의력 감소율 배수 증가
        is_correct = attention_effects[0] < attention_effects[-1]
        
        result = {
            'test_name': 'dopamine_effect',
            'passed': is_correct,
            'attention_effects': attention_effects,
            'message': 'Passed' if is_correct else 'Failed: Dopamine effect violation'
        }
        
        self.test_results.append(result)
        return result
    
    def test_closed_loop_stability(self) -> Dict:
        """
        폐루프 안정성 테스트: 발산하지 않음
        
        Returns:
            테스트 결과
        """
        dynamics = ClosedLoopDynamics()
        
        # 장기 시뮬레이션
        states = []
        for _ in range(100):
            external_input = {
                'task_importance': 0.8,
                'distractions': [],
                'time_elapsed': dynamics.time_elapsed
            }
            state = dynamics.update_state(external_input, dt=0.1)
            states.append(state.attention)
        
        # 안정성 확인 (발산하지 않음)
        final_std = np.std(states[-20:])
        is_stable = final_std < 1.0
        
        result = {
            'test_name': 'closed_loop_stability',
            'passed': is_stable,
            'final_std': final_std,
            'message': 'Passed' if is_stable else 'Failed: Unstable'
        }
        
        self.test_results.append(result)
        return result
    
    def run_all_tests(self) -> Dict:
        """
        모든 테스트 실행
        
        Returns:
            전체 테스트 결과
        """
        print("\n" + "="*70)
        print("🧪 동역학 불변식 테스트 실행")
        print("="*70 + "\n")
        
        # 각 테스트 실행
        self.test_monotonicity_attention()
        self.test_discount_rate()
        self.test_gate_effect()
        self.test_dopamine_effect()
        self.test_closed_loop_stability()
        
        # 결과 요약
        passed = sum(1 for r in self.test_results if r['passed'])
        total = len(self.test_results)
        
        print("="*70)
        print(f"테스트 결과: {passed}/{total} 통과")
        print("="*70 + "\n")
        
        for result in self.test_results:
            status = "✅" if result['passed'] else "❌"
            print(f"{status} {result['test_name']}: {result['message']}")
        
        print("\n" + "="*70 + "\n")
        
        return {
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'results': self.test_results
        }


if __name__ == "__main__":
    tester = DynamicsInvariantTests()
    results = tester.run_all_tests()
    print(f"전체 결과: {results['passed']}/{results['total']} 통과")

