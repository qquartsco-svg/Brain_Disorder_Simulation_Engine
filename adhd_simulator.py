"""
ADHD 시뮬레이터

Cookiie Brain Engine을 사용한 ADHD 전용 시뮬레이션
동역학적 상호작용을 고려한 실제 시뮬레이션
"""

import sys
import os
from pathlib import Path
import numpy as np
import time
from typing import Dict, List, Optional, Tuple
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정
try:
    # macOS에서 사용 가능한 한글 폰트 찾기
    font_list = [f.name for f in fm.fontManager.ttflist]
    korean_fonts = ['AppleGothic', 'NanumGothic', 'Malgun Gothic', 'Gulim']
    korean_font = None
    for font in korean_fonts:
        if font in font_list:
            korean_font = font
            break
    
    if korean_font:
        plt.rcParams['font.family'] = korean_font
    else:
        # 한글 폰트를 찾을 수 없으면 경고 없이 진행
        plt.rcParams['font.family'] = 'DejaVu Sans'
except:
    plt.rcParams['font.family'] = 'DejaVu Sans'

# Cookiie Brain Engine 경로 추가
# Cookiie Brain Engine이 설치된 경로를 지정하세요
# 기본값: 상위 디렉토리의 Cookiie_Brain_Engine
cookiie_brain_path = os.getenv('COOKIIE_BRAIN_PATH', 
                                str(Path(__file__).parent.parent.parent / 'Cookiie_Brain_Engine'))
sys.path.insert(0, str(Path(cookiie_brain_path) / 'package'))

from cookiie_brain import (
    CookiieBrainEngine, CookiieBrainConfig,
    BrainInput, BrainOutput, BrainState
)

from adhd_engines import (
    AttentionControlEngine,
    ImpulseControlEngine,
    HyperactivityEngine
)


class ADHDSimulator:
    """
    ADHD 시뮬레이터
    
    Cookiie Brain Engine과 ADHD 특화 엔진을 통합한 시뮬레이션 시스템
    """
    
    def __init__(self, config: Optional[CookiieBrainConfig] = None):
        """
        ADHD 시뮬레이터 초기화
        
        Args:
            config: Cookiie Brain Engine 설정
        """
        # Cookiie Brain Engine 초기화
        if config is None:
            config = CookiieBrainConfig(
                enable_dynamics=True,
                enable_dynamics_integration=True,
                log_level='ERROR'
            )
        
        self.brain = CookiieBrainEngine(config)
        
        # ADHD 특화 엔진 초기화
        self.adhd_engines = {
            'attention': AttentionControlEngine(),
            'impulse': ImpulseControlEngine(),
            'hyperactivity': HyperactivityEngine()
        }
        
        # 시뮬레이션 데이터
        self.simulation_data = {
            'timestamps': [],
            'attention_scores': [],
            'impulse_scores': [],
            'hyperactivity_scores': [],
            'brain_states': [],
            'adhd_patterns': []
        }
        
        # 시뮬레이션 시작 시간
        self.start_time = None
    
    def simulate_attention_task(self, duration: float = 30.0, 
                               task_importance: float = 0.8,
                               distraction_events: Optional[List[Dict]] = None) -> Dict:
        """
        주의력 지속 테스트 시뮬레이션
        
        Args:
            duration: 시뮬레이션 지속 시간 (초)
            task_importance: 작업 중요도
            distraction_events: 주의 분산 이벤트 리스트
        
        Returns:
            results: 시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🧠 ADHD 주의력 지속 테스트 시뮬레이션")
        print(f"{'='*70}")
        print(f"지속 시간: {duration}초")
        print(f"작업 중요도: {task_importance}")
        print(f"{'='*70}\n")
        
        self.start_time = time.time()
        dt = 0.1  # 시간 간격 (초)
        steps = int(duration / dt)
        
        # 주의 분산 이벤트 처리
        if distraction_events is None:
            distraction_events = []
        
        # 시뮬레이션 루프
        for step in range(steps):
            t = step * dt
            
            # 현재 주의 분산 계산
            current_distractions = []
            for event in distraction_events:
                if event['start_time'] <= t <= event['end_time']:
                    current_distractions.append({
                        'intensity': event['intensity'],
                        'relevance': event.get('relevance', 0.5)
                    })
            
            # Cookiie Brain Engine 처리
            brain_input = BrainInput(
                sensory={
                    'task': {
                        'name': '지속적 작업',
                        'importance': task_importance,
                        'time_elapsed': t
                    },
                    'distractions': current_distractions,
                    'attention_demand': task_importance
                },
                query='작업 지속',
                context={'goal': '작업 완료'}
            )
            
            brain_output = self.brain.process(brain_input)
            brain_state = self.brain.get_state()
            
            # ADHD 특화 엔진 처리
            attention_result = self.adhd_engines['attention'].maintain_attention(
                task={'importance': task_importance},
                distractions=current_distractions,
                time_elapsed=t
            )
            
            # 데이터 저장
            self.simulation_data['timestamps'].append(t)
            self.simulation_data['attention_scores'].append(attention_result['attention_score'])
            self.simulation_data['brain_states'].append({
                'energy': brain_state.energy,
                'confidence': brain_output.confidence,
                'arousal': brain_state.get('arousal', 0.5) if hasattr(brain_state, 'get') else 0.5
            })
            self.simulation_data['adhd_patterns'].append(attention_result['pattern'])
            
            # 진행 상황 출력
            if step % 50 == 0:
                progress = (step / steps) * 100
                print(f"진행: {progress:.1f}% | 주의력: {attention_result['attention_score']:.2f} | "
                      f"패턴: {attention_result['pattern']}")
        
        # 결과 분석
        results = self._analyze_attention_results()
        
        print(f"\n{'='*70}")
        print(f"✅ 주의력 테스트 완료")
        print(f"{'='*70}")
        print(f"평균 주의력: {results['mean_attention']:.3f}")
        print(f"주의력 감소율: {results['decline_rate']:.3f}")
        print(f"ADHD 패턴 감지: {results['adhd_detected']}")
        print(f"{'='*70}\n")
        
        return results
    
    def simulate_impulsivity_task(self, scenarios: List[Dict]) -> Dict:
        """
        충동성 테스트 시뮬레이션
        
        Args:
            scenarios: 충동성 테스트 시나리오 리스트
        
        Returns:
            results: 시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🧠 ADHD 충동성 테스트 시뮬레이션")
        print(f"{'='*70}")
        print(f"시나리오 수: {len(scenarios)}")
        print(f"{'='*70}\n")
        
        choices = []
        impulse_scores = []
        
        for i, scenario in enumerate(scenarios):
            print(f"시나리오 {i+1}/{len(scenarios)}:")
            print(f"  즉각적 보상: {scenario['immediate']}")
            print(f"  지연된 보상: {scenario['delayed']} (지연: {scenario['delay']}초)")
            
            # Cookiie Brain Engine 처리
            brain_input = BrainInput(
                sensory={
                    'immediate_reward': scenario['immediate'],
                    'delayed_reward': scenario['delayed'],
                    'delay_time': scenario['delay']
                },
                query='보상 선택',
                context={'goal': {'strength': 0.7, 'type': '장기적 목표'}}
            )
            
            brain_output = self.brain.process(brain_input)
            brain_state = self.brain.get_state()
            
            # ADHD 특화 엔진 처리
            impulse_result = self.adhd_engines['impulse'].control_impulse(
                immediate_reward=scenario['immediate'],
                delayed_reward=scenario['delayed'],
                delay_time=scenario['delay'],
                goal_context={'strength': 0.7}
            )
            
            # 선택 예측
            choice = impulse_result['predicted_choice']
            choices.append(choice)
            impulse_scores.append(impulse_result['impulse_score'])
            
            print(f"  충동성 점수: {impulse_result['impulse_score']:.3f}")
            print(f"  예상 선택: {choice}")
            print(f"  패턴: {impulse_result['pattern']}\n")
        
        # 결과 분석
        impulsive_count = sum(1 for c in choices if c == 'immediate_reward')
        impulsivity_rate = impulsive_count / len(choices)
        
        results = {
            'choices': choices,
            'impulse_scores': impulse_scores,
            'impulsivity_rate': impulsivity_rate,
            'adhd_detected': impulsivity_rate > 0.7,
            'mean_impulse_score': np.mean(impulse_scores)
        }
        
        print(f"{'='*70}")
        print(f"✅ 충동성 테스트 완료")
        print(f"{'='*70}")
        print(f"충동적 선택 비율: {impulsivity_rate:.1%}")
        print(f"평균 충동성 점수: {results['mean_impulse_score']:.3f}")
        print(f"ADHD 패턴 감지: {results['adhd_detected']}")
        print(f"{'='*70}\n")
        
        return results
    
    def simulate_hyperactivity_task(self, duration: float = 10.0,
                                   task_demand: float = 0.5) -> Dict:
        """
        과잉행동 테스트 시뮬레이션
        
        Args:
            duration: 시뮬레이션 지속 시간 (초)
            task_demand: 작업 요구도
        
        Returns:
            results: 시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🧠 ADHD 과잉행동 테스트 시뮬레이션")
        print(f"{'='*70}")
        print(f"지속 시간: {duration}초")
        print(f"작업 요구도: {task_demand}")
        print(f"{'='*70}\n")
        
        dt = 0.1
        steps = int(duration / dt)
        
        hyperactivity_scores = []
        energy_levels = []
        
        for step in range(steps):
            t = step * dt
            
            # Cookiie Brain Engine 처리
            brain_input = BrainInput(
                sensory={
                    'task_demand': task_demand,
                    'time_elapsed': t
                },
                query='에너지 관리',
                context={}
            )
            
            brain_output = self.brain.process(brain_input)
            brain_state = self.brain.get_state()
            
            # 에너지 레벨 추출
            current_energy = brain_state.energy if hasattr(brain_state, 'energy') else 0.5
            
            # ADHD 특화 엔진 처리
            hyperactivity_result = self.adhd_engines['hyperactivity'].calculate_hyperactivity(
                current_energy=current_energy,
                task_demand=task_demand,
                time_elapsed=t
            )
            
            hyperactivity_scores.append(hyperactivity_result['hyperactivity_score'])
            energy_levels.append(current_energy)
            
            # 진행 상황 출력
            if step % 20 == 0:
                print(f"시간: {t:.1f}초 | 과잉행동 점수: {hyperactivity_result['hyperactivity_score']:.3f} | "
                      f"에너지: {current_energy:.2f}")
        
        # 결과 분석
        energy_variance = np.var(energy_levels)
        mean_hyperactivity = np.mean(hyperactivity_scores)
        mean_energy = np.mean(energy_levels)
        
        # 에너지 불일치도 고려 (에너지가 높은데 작업 요구도가 낮으면 과잉행동)
        energy_mismatch = abs(mean_energy - task_demand * 100)  # 에너지는 0-100 스케일
        
        # ADHD 감지: 에너지 변동성이 높거나, 에너지 불일치가 크거나, 과잉행동 점수가 높으면
        adhd_detected = (energy_variance > 50.0 or 
                        energy_mismatch > 30.0 or 
                        mean_hyperactivity > 0.6)
        
        results = {
            'hyperactivity_scores': hyperactivity_scores,
            'energy_levels': energy_levels,
            'energy_variance': energy_variance,
            'mean_hyperactivity': mean_hyperactivity,
            'energy_mismatch': energy_mismatch,
            'mean_energy': mean_energy,
            'adhd_detected': adhd_detected
        }
        
        print(f"\n{'='*70}")
        print(f"✅ 과잉행동 테스트 완료")
        print(f"{'='*70}")
        print(f"평균 과잉행동 점수: {mean_hyperactivity:.3f}")
        print(f"에너지 변동성: {energy_variance:.2f}")
        print(f"에너지 불일치: {results.get('energy_mismatch', 0.0):.2f}")
        print(f"평균 에너지: {results.get('mean_energy', 0.0):.2f}")
        print(f"ADHD 패턴 감지: {results['adhd_detected']}")
        print(f"{'='*70}\n")
        
        return results
    
    def simulate_full_adhd_assessment(self) -> Dict:
        """
        전체 ADHD 평가 시뮬레이션
        
        주의력, 충동성, 과잉행동을 모두 테스트
        """
        print(f"\n{'='*70}")
        print(f"🧠 ADHD 전체 평가 시뮬레이션")
        print(f"{'='*70}\n")
        
        # 1. 주의력 테스트
        print("📋 1단계: 주의력 지속 테스트")
        distraction_events = [
            {'start_time': 5.0, 'end_time': 7.0, 'intensity': 0.6, 'relevance': 0.7},
            {'start_time': 15.0, 'end_time': 17.0, 'intensity': 0.5, 'relevance': 0.6},
            {'start_time': 25.0, 'end_time': 27.0, 'intensity': 0.7, 'relevance': 0.8}
        ]
        attention_results = self.simulate_attention_task(
            duration=30.0,
            task_importance=0.8,
            distraction_events=distraction_events
        )
        
        # 2. 충동성 테스트
        print("📋 2단계: 충동성 테스트")
        scenarios = [
            {'immediate': 5, 'delayed': 50, 'delay': 10},
            {'immediate': 10, 'delayed': 100, 'delay': 20},
            {'immediate': 20, 'delayed': 200, 'delay': 30},
            {'immediate': 15, 'delayed': 150, 'delay': 25}
        ]
        impulsivity_results = self.simulate_impulsivity_task(scenarios)
        
        # 3. 과잉행동 테스트
        print("📋 3단계: 과잉행동 테스트")
        hyperactivity_results = self.simulate_hyperactivity_task(
            duration=10.0,
            task_demand=0.5
        )
        
        # 종합 평가
        assessment = self._assess_adhd_patterns(
            attention_results,
            impulsivity_results,
            hyperactivity_results
        )
        
        print(f"\n{'='*70}")
        print(f"🏆 ADHD 동역학 패턴 평가 결과")
        print(f"{'='*70}")
        print(f"평가 요약: {assessment['assessment']}")
        print(f"패턴 신뢰도 (시뮬레이션 기반): {assessment['confidence']:.2f}")
        print(f"\n세부 점수:")
        print(f"  주의력 결핍 점수: {assessment['scores']['attention_deficit']:.3f}")
        print(f"  충동성 점수: {assessment['scores']['impulsivity']:.3f}")
        print(f"  과잉행동 점수: {assessment['scores']['hyperactivity']:.3f}")
        print(f"\n⚠️  참고: 이 결과는 시뮬레이션 기반 동역학적 패턴 평가이며, 의학적 진단이 아닙니다.")
        print(f"{'='*70}\n")
        
        return {
            'attention': attention_results,
            'impulsivity': impulsivity_results,
            'hyperactivity': hyperactivity_results,
            'assessment': assessment
        }
    
    def _analyze_attention_results(self) -> Dict:
        """주의력 결과 분석"""
        if len(self.simulation_data['attention_scores']) < 10:
            return {'mean_attention': 0.0, 'decline_rate': 0.0, 'adhd_detected': False}
        
        scores = self.simulation_data['attention_scores']
        
        # 평균 주의력
        mean_attention = np.mean(scores)
        
        # 주의력 감소율 (초반 vs 후반)
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        first_avg = np.mean(first_half)
        second_avg = np.mean(second_half)
        
        decline_rate = (first_avg - second_avg) / first_avg if first_avg > 0 else 0.0
        
        # ADHD 패턴 감지
        adhd_detected = decline_rate > 0.3 or mean_attention < 0.5
        
        return {
            'mean_attention': mean_attention,
            'decline_rate': decline_rate,
            'adhd_detected': adhd_detected,
            'first_half_avg': first_avg,
            'second_half_avg': second_avg
        }
    
    def _diagnose_adhd(self, attention_results: Dict,
                       impulsivity_results: Dict,
                       hyperactivity_results: Dict) -> Dict:
        """ADHD 종합 진단"""
        # 점수 정규화
        attention_score = attention_results.get('decline_rate', 0.0)
        if attention_score > 0.3:
            attention_deficit = min(1.0, attention_score * 2.0)
        else:
            attention_deficit = attention_score / 0.3
        
        impulsivity_score = impulsivity_results.get('impulsivity_rate', 0.0)
        # 과잉행동 점수: 에너지 변동성과 불일치 모두 고려
        energy_variance = hyperactivity_results.get('energy_variance', 0.0)
        energy_mismatch = hyperactivity_results.get('energy_mismatch', 0.0)
        hyperactivity_score = min(1.0, (
            energy_variance / 100.0 * 0.5 +  # 변동성 기여도 50%
            energy_mismatch / 50.0 * 0.5     # 불일치 기여도 50%
        ))
        
        # 진단 기준
        if (attention_deficit > 0.7 and
            (impulsivity_score > 0.6 or hyperactivity_score > 0.6)):
            diagnosis = 'ADHD 가능성 높음'
            confidence = 0.8
        elif attention_deficit > 0.7:
            diagnosis = '주의력 결핍 가능성'
            confidence = 0.6
        elif impulsivity_score > 0.7 or hyperactivity_score > 0.7:
            diagnosis = '충동성/과잉행동 가능성'
            confidence = 0.5
        else:
            diagnosis = '정상 범위'
            confidence = 0.9
        
        return {
            'diagnosis': diagnosis,
            'confidence': confidence,
            'scores': {
                'attention_deficit': attention_deficit,
                'impulsivity': impulsivity_score,
                'hyperactivity': hyperactivity_score
            }
        }
    
    def visualize_results(self, output_path: str = 'adhd_simulation_results.png'):
        """시뮬레이션 결과 시각화"""
        if len(self.simulation_data['timestamps']) == 0:
            print("시각화할 데이터가 없습니다.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. 주의력 추이
        ax1 = axes[0, 0]
        ax1.plot(self.simulation_data['timestamps'], 
                self.simulation_data['attention_scores'],
                'b-', linewidth=2, label='주의력 점수')
        ax1.axhline(y=0.5, color='r', linestyle='--', label='ADHD 임계값')
        ax1.set_xlabel('시간 (초)', fontsize=10)
        ax1.set_ylabel('주의력 점수', fontsize=10)
        ax1.set_title('주의력 지속 테스트', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 뇌 상태 (에너지)
        ax2 = axes[0, 1]
        if self.simulation_data['brain_states']:
            energies = [s['energy'] for s in self.simulation_data['brain_states']]
            ax2.plot(self.simulation_data['timestamps'], energies,
                    'g-', linewidth=2, label='에너지 레벨')
            ax2.set_xlabel('시간 (초)', fontsize=10)
            ax2.set_ylabel('에너지 레벨', fontsize=10)
            ax2.set_title('에너지 변동성', fontsize=12, fontweight='bold')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        # 3. ADHD 패턴 분포
        ax3 = axes[1, 0]
        if self.simulation_data['adhd_patterns']:
            adhd_count = sum(1 for p in self.simulation_data['adhd_patterns'] if p == 'adhd')
            normal_count = len(self.simulation_data['adhd_patterns']) - adhd_count
            
            ax3.bar(['정상', 'ADHD 패턴'], [normal_count, adhd_count],
                   color=['green', 'red'], alpha=0.7, edgecolor='black', linewidth=2)
            ax3.set_ylabel('빈도', fontsize=10)
            ax3.set_title('ADHD 패턴 분포', fontsize=12, fontweight='bold')
            ax3.grid(axis='y', alpha=0.3)
        
        # 4. 주의력 히스토그램
        ax4 = axes[1, 1]
        ax4.hist(self.simulation_data['attention_scores'], bins=20,
                color='blue', alpha=0.7, edgecolor='black')
        ax4.axvline(x=0.5, color='r', linestyle='--', label='ADHD 임계값')
        ax4.set_xlabel('주의력 점수', fontsize=10)
        ax4.set_ylabel('빈도', fontsize=10)
        ax4.set_title('주의력 분포', fontsize=12, fontweight='bold')
        ax4.legend()
        ax4.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✅ 시각화 결과 저장: {output_path}")
        plt.close()


def main():
    """메인 실행 함수"""
    print("\n" + "="*70)
    print("🧠 ADHD 시뮬레이터 시작")
    print("="*70)
    
    # 시뮬레이터 초기화
    simulator = ADHDSimulator()
    
    # 전체 평가 실행
    results = simulator.simulate_full_adhd_assessment()
    
    # 결과 시각화
    output_dir = Path(__file__).parent
    output_path = output_dir / 'adhd_simulation_results.png'
    simulator.visualize_results(str(output_path))
    
    print("\n" + "="*70)
    print("✅ ADHD 시뮬레이션 완료")
    print("="*70)
    print(f"\n결과 파일: {output_path}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

