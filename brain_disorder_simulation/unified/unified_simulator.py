"""
통합 뇌 질환 시뮬레이터

모든 뇌 질환을 통합하여 시뮬레이션하는 메인 클래스
목적: "왜 이런 상황이 발생할 수 있는가?" 원인 분석

⚠️ 주의: 이 시뮬레이터는 치료 도구가 아닙니다.
"""

import sys
import os
from pathlib import Path
import numpy as np
import time
from typing import Dict, List, Optional, Tuple, Union
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정
try:
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
        plt.rcParams['font.family'] = 'DejaVu Sans'
except:
    plt.rcParams['font.family'] = 'DejaVu Sans'

# Cookiie Brain Engine 경로 추가
cookiie_brain_path = os.getenv('COOKIIE_BRAIN_PATH', 
                                str(Path(__file__).parent.parent.parent.parent / 'Cookiie_Brain_Engine'))
sys.path.insert(0, str(Path(cookiie_brain_path) / 'package'))

from cookiie_brain import (
    CookiieBrainEngine, CookiieBrainConfig,
    BrainInput, BrainOutput, BrainState
)

# 공통 엔진
from ..common.negative_bias_engine import NegativeBiasEngine
from ..common.cognitive_control_engine import CognitiveControlEngine
from ..common.energy_depletion_engine import EnergyDepletionEngine

# 질환별 특화 엔진
from ..disorders.depression.motivation_engine import MotivationEngine
from ..disorders.adhd.adhd_engines import (
    AttentionControlEngine,
    ImpulseControlEngine,
    HyperactivityEngine
)

# 유틸리티
from ..utils.reproducibility import ReproducibleRNG, ExperimentMetadata
from ..utils.statistics import StatisticalValidator
from ..utils.report_generator import ReportGenerator


class UnifiedDisorderSimulator:
    """
    통합 뇌 질환 시뮬레이터
    
    여러 뇌 질환을 통합하여 시뮬레이션하는 메인 클래스
    - 단일 질환 시뮬레이션
    - 공존(co-morbidity) 시뮬레이션
    - 커스텀 조합 시뮬레이션
    """
    
    def __init__(self,
                 config: Optional[CookiieBrainConfig] = None,
                 seed: Optional[int] = None):
        """
        통합 시뮬레이터 초기화
        
        Args:
            config: Cookiie Brain Engine 설정
            seed: 재현성을 위한 시드 값
        """
        # 재현성 시스템 초기화
        self.rng = ReproducibleRNG(seed=seed)
        self.seed = self.rng.seed
        
        # Cookiie Brain Engine 초기화
        if config is None:
            config = CookiieBrainConfig(
                enable_dynamics=True,
                enable_dynamics_integration=True,
                log_level='ERROR'
            )
        
        self.brain = CookiieBrainEngine(config)
        
        # 공통 엔진 (필요시 초기화)
        self.common_engines = {}
        
        # 질환별 특화 엔진 (필요시 초기화)
        self.disorder_engines = {}
        
        # 시뮬레이션 데이터
        self.simulation_data = {
            'timestamps': [],
            'pattern_observations': []
        }
        
        # 통계적 검증 시스템
        self.statistical_validator = StatisticalValidator()
        
        # 리포트 생성기
        self.report_generator = ReportGenerator()
        
        # 시뮬레이션 시작 시간
        self.start_time = None
    
    def simulate_depression(self,
                           negative_bias_strength: float = 0.5,
                           control_impairment: float = 0.5,
                           energy_depletion_rate: float = 0.5,
                           motivation_deficit: float = 0.5,
                           duration: float = 300.0) -> Dict:
        """
        우울증 시뮬레이션
        
        Args:
            negative_bias_strength: 부정적 편향 강도
            control_impairment: 인지 제어 약화 정도
            energy_depletion_rate: 에너지 고갈 속도
            motivation_deficit: 동기 결핍 정도
            duration: 시뮬레이션 지속 시간
        
        Returns:
            시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🔬 우울증 메커니즘 시뮬레이션")
        print(f"{'='*70}")
        print(f"목적: 우울증 패턴의 원인 분석")
        print(f"지속 시간: {duration}초")
        print(f"{'='*70}\n")
        
        # 우울증 엔진 초기화
        self.common_engines['negative_bias'] = NegativeBiasEngine(
            negative_bias_strength=negative_bias_strength,
            rng=self.rng.get_rng('negative_bias')
        )
        
        self.common_engines['cognitive_control'] = CognitiveControlEngine(
            control_impairment=control_impairment,
            rng=self.rng.get_rng('cognitive_control')
        )
        
        self.common_engines['energy_depletion'] = EnergyDepletionEngine(
            depletion_rate=energy_depletion_rate,
            rng=self.rng.get_rng('energy_depletion')
        )
        
        self.disorder_engines['motivation'] = MotivationEngine(
            motivation_deficit=motivation_deficit,
            rng=self.rng.get_rng('motivation')
        )
        
        # 시뮬레이션 실행
        self.start_time = time.time()
        dt = 0.1
        steps = int(duration / dt)
        
        # 데이터 초기화
        self.simulation_data = {
            'timestamps': [],
            'negative_bias_scores': [],
            'cognitive_control_scores': [],
            'energy_scores': [],
            'motivation_scores': [],
            'pattern_observations': []
        }
        
        for step in range(steps):
            t = step * dt
            
            # 각 엔진 업데이트
            if step % 10 == 0:  # 1초마다
                # 부정적 편향 (자극 처리)
                stimulus = self._generate_random_stimulus()
                bias_result = self.common_engines['negative_bias'].process_stimulus(
                    stimulus_valence=stimulus['valence'],
                    stimulus_intensity=stimulus['intensity'],
                    time_elapsed=t
                )
            
            if step % 20 == 0:  # 2초마다
                # 인지 제어 (부정적 사고)
                thought_result = self.common_engines['cognitive_control'].process_negative_thought(
                    thought_intensity=0.3 + self.rng.get_rng('thought').random() * 0.4,
                    time_elapsed=t
                )
            
            # 에너지 고갈
            energy_rng = self.rng.get_rng('energy')
            energy_result = self.common_engines['energy_depletion'].update_energy(
                cognitive_load=0.3 + energy_rng.random() * 0.4,
                stress_level=0.2 + energy_rng.random() * 0.3,
                dt=dt
            )
            
            if step % 30 == 0:  # 3초마다
                # 동기 (보상 기회)
                reward = self._generate_random_reward()
                motivation_result = self.disorder_engines['motivation'].process_reward(
                    reward_value=reward['value'],
                    effort_required=reward['effort']
                )
            
            # 상태 업데이트
            self.common_engines['negative_bias'].update_rumination(dt)
            self.common_engines['cognitive_control'].update_negative_loop(dt)
            
            # 데이터 기록
            if step % 10 == 0:
                self.simulation_data['timestamps'].append(t)
                self.simulation_data['negative_bias_scores'].append(
                    self.common_engines['negative_bias'].get_bias_score()
                )
                self.simulation_data['cognitive_control_scores'].append(
                    self.common_engines['cognitive_control'].get_control_score()
                )
                self.simulation_data['energy_scores'].append(
                    self.common_engines['energy_depletion'].get_energy_score()
                )
                self.simulation_data['motivation_scores'].append(
                    self.disorder_engines['motivation'].get_motivation_score()
                )
        
        # 결과 분석
        results = self._analyze_depression_patterns()
        
        print(f"\n✅ 우울증 시뮬레이션 완료!")
        print(f"   종합 패턴: {results['overall_pattern']}")
        print(f"   종합 점수: {results['mean_depression_score']:.3f}")
        
        return results
    
    def simulate_anxiety(self,
                        threat_sensitivity: float = 0.6,
                        filtering_impairment: float = 0.5,
                        worry_loop_strength: float = 0.5,
                        stress_response: float = 0.6,
                        duration: float = 300.0) -> Dict:
        """
        불안장애 시뮬레이션
        
        Args:
            threat_sensitivity: 위협 민감도
            filtering_impairment: 필터링 약화 정도
            worry_loop_strength: 걱정 루프 강도
            stress_response: 스트레스 반응 강도
            duration: 시뮬레이션 지속 시간
        
        Returns:
            시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🔬 불안장애 메커니즘 시뮬레이션")
        print(f"{'='*70}")
        print(f"목적: 불안장애 패턴의 원인 분석")
        print(f"지속 시간: {duration}초")
        print(f"{'='*70}\n")
        
        # 불안장애는 향후 구현 예정
        # 현재는 플레이스홀더
        print("⚠️  불안장애 엔진은 아직 구현 중입니다.")
        print("   현재는 공통 엔진만 사용 가능합니다.")
        
        return {
            'status': 'not_implemented',
            'message': '불안장애 엔진 구현 예정'
        }
    
    def simulate_comorbidity(self,
                            disorders: List[str],
                            duration: float = 300.0,
                            **kwargs) -> Dict:
        """
        공존(co-morbidity) 시뮬레이션
        
        여러 질환이 동시에 나타나는 실제 상황 시뮬레이션
        
        Args:
            disorders: 질환 리스트 (예: ['depression', 'anxiety'])
            duration: 시뮬레이션 지속 시간
            **kwargs: 질환별 파라미터
        
        Returns:
            통합 시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🔬 공존(co-morbidity) 메커니즘 시뮬레이션")
        print(f"{'='*70}")
        print(f"질환: {', '.join(disorders)}")
        print(f"목적: 공존 패턴의 원인 분석")
        print(f"지속 시간: {duration}초")
        print(f"{'='*70}\n")
        
        # 공존 시뮬레이션은 향후 구현 예정
        # 현재는 단일 질환 시뮬레이션만 가능
        if 'depression' in disorders:
            return self.simulate_depression(
                duration=duration,
                **kwargs.get('depression_params', {})
            )
        else:
            return {
                'status': 'not_implemented',
                'message': '공존 시뮬레이션 구현 예정'
            }
    
    def simulate_custom(self,
                       active_engines: Dict[str, Dict],
                       duration: float = 300.0) -> Dict:
        """
        커스텀 조합 시뮬레이션
        
        사용자가 직접 엔진을 조합하여 시뮬레이션
        
        Args:
            active_engines: 활성화할 엔진과 파라미터
            duration: 시뮬레이션 지속 시간
        
        Returns:
            커스텀 시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🔬 커스텀 메커니즘 시뮬레이션")
        print(f"{'='*70}")
        print(f"활성 엔진: {list(active_engines.keys())}")
        print(f"목적: 커스텀 조합 패턴의 원인 분석")
        print(f"지속 시간: {duration}초")
        print(f"{'='*70}\n")
        
        # 커스텀 시뮬레이션은 향후 구현 예정
        return {
            'status': 'not_implemented',
            'message': '커스텀 시뮬레이션 구현 예정'
        }
    
    # ======================================================================
    # 헬퍼 메서드
    # ======================================================================
    
    def _generate_random_stimulus(self) -> Dict:
        """랜덤 자극 생성"""
        rng = self.rng.get_rng('stimulus')
        valence = rng.choice([-0.8, -0.4, 0.0, 0.4, 0.8],
                            p=[0.3, 0.2, 0.2, 0.15, 0.15])
        intensity = 0.5 + rng.random() * 0.5
        return {'valence': valence, 'intensity': intensity}
    
    def _generate_random_reward(self) -> Dict:
        """랜덤 보상 생성"""
        rng = self.rng.get_rng('reward')
        return {
            'value': 0.3 + rng.random() * 0.5,
            'effort': 0.2 + rng.random() * 0.6
        }
    
    def _analyze_depression_patterns(self) -> Dict:
        """우울증 패턴 분석"""
        if not self.simulation_data['negative_bias_scores']:
            return {'overall_pattern': 'insufficient_data', 'mean_depression_score': 0.0}
        
        bias_scores = np.array(self.simulation_data['negative_bias_scores'])
        control_scores = np.array(self.simulation_data['cognitive_control_scores'])
        energy_scores = np.array(self.simulation_data['energy_scores'])
        motivation_scores = np.array(self.simulation_data['motivation_scores'])
        
        # 역변환 (낮을수록 우울증 강함)
        depression_scores = [
            np.mean(bias_scores),
            1.0 - np.mean(control_scores),
            1.0 - np.mean(energy_scores),
            1.0 - np.mean(motivation_scores)
        ]
        
        mean_score = np.mean(depression_scores)
        
        if mean_score > 0.7:
            pattern = 'severe_depression_like_pattern'
        elif mean_score > 0.5:
            pattern = 'moderate_depression_like_pattern'
        elif mean_score > 0.3:
            pattern = 'mild_depression_like_pattern'
        else:
            pattern = 'minimal_depression_like_pattern'
        
        return {
            'overall_pattern': pattern,
            'mean_depression_score': float(mean_score),
            'negative_bias_score': float(np.mean(bias_scores)),
            'cognitive_control_score': float(np.mean(control_scores)),
            'energy_score': float(np.mean(energy_scores)),
            'motivation_score': float(np.mean(motivation_scores))
        }
    
    def visualize_results(self, output_path: Optional[str] = None):
        """결과 시각화"""
        if not self.simulation_data['timestamps']:
            print("⚠️ 시각화할 데이터가 없습니다.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('뇌 질환 메커니즘 시뮬레이션 결과\n(패턴 관측 및 원인 분석)', 
                     fontsize=16, fontweight='bold')
        
        timestamps = np.array(self.simulation_data['timestamps'])
        
        # 1. 부정적 편향
        if 'negative_bias_scores' in self.simulation_data and self.simulation_data['negative_bias_scores']:
            ax1 = axes[0, 0]
            ax1.plot(timestamps, self.simulation_data['negative_bias_scores'], 
                     'r-', linewidth=2, label='부정적 편향 점수')
            ax1.set_xlabel('시간 (초)')
            ax1.set_ylabel('편향 점수')
            ax1.set_title('부정적 편향 메커니즘')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
        
        # 2. 인지 제어
        if 'cognitive_control_scores' in self.simulation_data and self.simulation_data['cognitive_control_scores']:
            ax2 = axes[0, 1]
            ax2.plot(timestamps, self.simulation_data['cognitive_control_scores'],
                     'b-', linewidth=2, label='인지 제어 점수')
            ax2.set_xlabel('시간 (초)')
            ax2.set_ylabel('제어 점수')
            ax2.set_title('인지 제어 약화 메커니즘')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
        
        # 3. 에너지
        if 'energy_scores' in self.simulation_data and self.simulation_data['energy_scores']:
            ax3 = axes[1, 0]
            ax3.plot(timestamps, self.simulation_data['energy_scores'],
                     'g-', linewidth=2, label='에너지 점수')
            ax3.set_xlabel('시간 (초)')
            ax3.set_ylabel('에너지 점수')
            ax3.set_title('에너지 고갈 메커니즘')
            ax3.grid(True, alpha=0.3)
            ax3.legend()
        
        # 4. 동기
        if 'motivation_scores' in self.simulation_data and self.simulation_data['motivation_scores']:
            ax4 = axes[1, 1]
            ax4.plot(timestamps, self.simulation_data['motivation_scores'],
                     'm-', linewidth=2, label='동기 점수')
            ax4.set_xlabel('시간 (초)')
            ax4.set_ylabel('동기 점수')
            ax4.set_title('동기 감소 메커니즘')
            ax4.grid(True, alpha=0.3)
            ax4.legend()
        
        plt.tight_layout()
        
        # 저장 경로 결정
        if output_path:
            save_path = output_path
        else:
            # 현재 작업 디렉토리에 저장
            import os
            save_path = os.path.join(os.getcwd(), 'unified_simulation_results.png')
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"\n💾 시각화 저장: {save_path}")
        print(f"   절대 경로: {os.path.abspath(save_path)}")
        
        plt.close()


def main():
    """메인 실행 함수"""
    print("\n" + "="*70)
    print("🔬 통합 뇌 질환 시뮬레이터")
    print("="*70)
    print("목적: 뇌 질환 패턴의 원인 분석 및 메커니즘 탐색")
    print("⚠️  주의: 이 시뮬레이터는 치료 도구가 아닙니다.")
    print("="*70 + "\n")
    
    # 통합 시뮬레이터 생성
    simulator = UnifiedDisorderSimulator(seed=42)
    
    # 우울증 시뮬레이션 실행
    results = simulator.simulate_depression(
        negative_bias_strength=0.6,
        control_impairment=0.5,
        energy_depletion_rate=0.5,
        motivation_deficit=0.6,
        duration=300.0
    )
    
    # 결과 시각화
    simulator.visualize_results()
    
    print("\n" + "="*70)
    print("✅ 시뮬레이션 완료!")
    print("="*70)
    print(f"\n관측된 패턴: {results['overall_pattern']}")
    print(f"종합 점수: {results['mean_depression_score']:.3f}")
    print("\n⚠️  이 결과는 패턴 관측 및 메커니즘 분석 목적입니다.")
    print("   진단 도구나 치료 솔루션이 아닙니다.")
    print("="*70 + "\n")


if __name__ == "__main__":
    import sys
    # 모듈이 이미 로드된 경우를 대비한 처리
    if 'brain_disorder_simulation.unified.unified_simulator' in sys.modules:
        # 직접 실행 시 main 함수 호출
        if sys.argv[0].endswith('unified_simulator.py'):
            main()
    else:
        main()

