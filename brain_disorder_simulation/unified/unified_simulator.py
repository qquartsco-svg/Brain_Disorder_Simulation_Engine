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

# 루프 라이브러리
from ..common.loops import (
    NegativeBiasLoop,
    HyperarousalLoop,
    ControlFailureLoop,
    EnergyCollapseLoop
)

# 질환별 특화 엔진
from ..disorders.depression.motivation_engine import MotivationEngine
from ..disorders.adhd.adhd_engines import (
    AttentionControlEngine,
    ImpulseControlEngine,
    HyperactivityEngine
)
from ..disorders.ptsd.ptsd_engines import (
    IntrusiveMemoryEngine,
    AvoidanceEngine,
    HyperarousalEngine,
    NegativeCognitionEngine
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
        
        # 루프 추적 (루프 조합 분석용)
        self.active_loops = {}
        self.loop_history = []
        
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
        
        # 루프 추적 초기화
        self.active_loops = {
            'negative_bias': self.common_engines['negative_bias'].loop,
            'control_failure': self.common_engines['cognitive_control'].loop,
            'energy_collapse': self.common_engines['energy_depletion'].loop
        }
        self.loop_history = []
        
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
                
                # 루프 상태 기록
                loop_state = {
                    'time': t,
                    'negative_bias_loop': self.active_loops['negative_bias'].get_strength(),
                    'control_failure_loop': self.active_loops['control_failure'].get_strength(),
                    'energy_collapse_loop': self.active_loops['energy_collapse'].get_strength()
                }
                self.loop_history.append(loop_state)
        
        # 결과 분석
        results = self._analyze_depression_patterns()
        
        # 루프 기반 패턴 해석 추가
        loop_analysis = self._analyze_loop_combinations()
        results['loop_analysis'] = loop_analysis
        
        # 최근 결과 저장 (explain_patterns에서 사용)
        self.last_results = results
        
        print(f"\n✅ 우울증 시뮬레이션 완료!")
        print(f"   종합 패턴: {results['overall_pattern']}")
        print(f"   종합 점수: {results['mean_depression_score']:.3f}")
        
        # 루프 기반 해석 출력
        print("\n" + self.explain_patterns(results))
        
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
    
    def simulate_ptsd(self,
                      trauma_intensity: float = 0.8,
                      suppression_failure: float = 0.6,
                      avoidance_strength: float = 0.7,
                      hyperarousal_level: float = 0.7,
                      duration: float = 300.0) -> Dict:
        """
        PTSD 시뮬레이션
        
        Args:
            trauma_intensity: 외상 강도 (0.0 ~ 1.0)
            suppression_failure: 억제 실패율 (0.0 ~ 1.0)
            avoidance_strength: 회피 강도 (0.0 ~ 1.0)
            hyperarousal_level: 과각성 수준 (0.0 ~ 1.0)
            duration: 시뮬레이션 지속 시간
        
        Returns:
            시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🔬 PTSD 메커니즘 시뮬레이션")
        print(f"{'='*70}")
        print(f"목적: PTSD 패턴의 원인 분석")
        print(f"지속 시간: {duration}초")
        print(f"{'='*70}\n")
        
        # PTSD 엔진 초기화
        self.disorder_engines['intrusive_memory'] = IntrusiveMemoryEngine(
            rng=self.rng.get_rng('intrusive_memory')
        )
        
        self.disorder_engines['avoidance'] = AvoidanceEngine(
            rng=self.rng.get_rng('avoidance')
        )
        
        self.disorder_engines['hyperarousal'] = HyperarousalEngine(
            rng=self.rng.get_rng('hyperarousal')
        )
        
        self.disorder_engines['negative_cognition'] = NegativeCognitionEngine(
            rng=self.rng.get_rng('negative_cognition')
        )
        
        # 초기 외상 기억 추가
        self.disorder_engines['intrusive_memory'].add_traumatic_memory(
            memory_id='trauma_1',
            initial_intensity=trauma_intensity,
            initial_fear=trauma_intensity * 0.9
        )
        
        # 억제 실패율 설정
        self.disorder_engines['intrusive_memory'].suppression_failure_rate = suppression_failure
        
        # 시뮬레이션 실행
        self.start_time = time.time()
        dt = 0.1
        steps = int(duration / dt)
        
        # 데이터 초기화
        self.simulation_data = {
            'timestamps': [],
            'intrusion_scores': [],
            'avoidance_scores': [],
            'arousal_scores': [],
            'negative_cognition_scores': [],
            'pattern_observations': []
        }
        
        for step in range(steps):
            t = step * dt
            
            # 외상 기억 침입 처리 (5초마다)
            if step % 50 == 0:
                # Amygdala 각성 수준 추정
                amygdala_arousal = 0.5 + self.disorder_engines['hyperarousal'].current_arousal * 0.5
                
                # PFC 제어 능력 추정
                pfc_control = 1.0 - suppression_failure
                
                # 기억 억제 시도
                for memory in self.disorder_engines['intrusive_memory'].traumatic_memories:
                    self.disorder_engines['intrusive_memory'].attempt_suppression(
                        memory.memory_id, pfc_control
                    )
                
                # 침입 수준 계산
                intrusion = self.disorder_engines['intrusive_memory'].compute_intrusion(
                    amygdala_arousal
                )
                
                # 침입 발생 시 회피 학습
                if intrusion > 0.5:
                    stimulus = f"trauma_trigger_{step}"
                    self.disorder_engines['avoidance'].learn_avoidance(
                        stimulus, fear_level=intrusion
                    )
            
            # 회피 패턴 업데이트 (3초마다)
            if step % 30 == 0:
                avoidance_level = self.disorder_engines['avoidance'].compute_avoidance_level()
            
            # 과각성 업데이트
            stress_level = (self.disorder_engines['intrusive_memory'].current_intrusion_level +
                          self.disorder_engines['hyperarousal'].current_arousal) / 2.0
            threat_detected = (self.disorder_engines['intrusive_memory'].current_intrusion_level > 0.4)
            thalamus_filtering = 1.0 - suppression_failure * 0.5
            
            arousal = self.disorder_engines['hyperarousal'].update_arousal(
                stress_level=stress_level,
                threat_detected=threat_detected,
                thalamus_filtering=thalamus_filtering
            )
            
            # 부정적 인지 변화 업데이트 (10초마다)
            if step % 100 == 0:
                intrusion = self.disorder_engines['intrusive_memory'].current_intrusion_level
                if intrusion > 0.3:
                    self.disorder_engines['negative_cognition'].strengthen_negative_belief(
                        'self_blame', evidence=intrusion * 0.5
                    )
                    self.disorder_engines['negative_cognition'].strengthen_negative_belief(
                        'guilt', evidence=intrusion * 0.4
                    )
                
                negative_bias = self.disorder_engines['negative_cognition'].compute_negative_bias()
            
            # 엔진 업데이트
            self.disorder_engines['intrusive_memory'].update(
                dt=dt,
                amygdala_arousal=arousal,
                pfc_control=1.0 - suppression_failure
            )
            
            # 데이터 기록 (1초마다)
            if step % 10 == 0:
                self.simulation_data['timestamps'].append(t)
                self.simulation_data['intrusion_scores'].append(
                    self.disorder_engines['intrusive_memory'].current_intrusion_level
                )
                self.simulation_data['avoidance_scores'].append(
                    self.disorder_engines['avoidance'].current_avoidance_level
                )
                self.simulation_data['arousal_scores'].append(
                    self.disorder_engines['hyperarousal'].current_arousal
                )
                self.simulation_data['negative_cognition_scores'].append(
                    self.disorder_engines['negative_cognition'].current_negative_bias
                )
        
        # 결과 분석
        results = self._analyze_ptsd_patterns()
        
        print(f"\n✅ PTSD 시뮬레이션 완료!")
        print(f"   종합 패턴: {results['overall_pattern']}")
        print(f"   침입 수준: {results['mean_intrusion']:.3f}")
        print(f"   회피 수준: {results['mean_avoidance']:.3f}")
        print(f"   과각성 수준: {results['mean_arousal']:.3f}")
        
        return results
    
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
        
        # 공존 시뮬레이션
        if 'depression' in disorders:
            return self.simulate_depression(
                duration=duration,
                **kwargs.get('depression_params', {})
            )
        elif 'ptsd' in disorders:
            return self.simulate_ptsd(
                duration=duration,
                **kwargs.get('ptsd_params', {})
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
    
    def _analyze_ptsd_patterns(self) -> Dict:
        """PTSD 패턴 분석"""
        if not self.simulation_data['intrusion_scores']:
            return {
                'overall_pattern': 'insufficient_data',
                'mean_intrusion': 0.0,
                'mean_avoidance': 0.0,
                'mean_arousal': 0.0
            }
        
        intrusion_scores = np.array(self.simulation_data['intrusion_scores'])
        avoidance_scores = np.array(self.simulation_data['avoidance_scores'])
        arousal_scores = np.array(self.simulation_data['arousal_scores'])
        negative_cognition_scores = np.array(self.simulation_data['negative_cognition_scores'])
        
        mean_intrusion = np.mean(intrusion_scores)
        mean_avoidance = np.mean(avoidance_scores)
        mean_arousal = np.mean(arousal_scores)
        mean_negative_cognition = np.mean(negative_cognition_scores)
        
        # PTSD 패턴 판단 (DSM-5 기준)
        if (mean_intrusion > 0.5 and mean_avoidance > 0.4 and 
            mean_arousal > 0.6 and mean_negative_cognition > 0.4):
            pattern = 'severe_ptsd_like_pattern'
        elif (mean_intrusion > 0.4 and mean_avoidance > 0.3 and 
              mean_arousal > 0.5):
            pattern = 'moderate_ptsd_like_pattern'
        elif (mean_intrusion > 0.3 or mean_arousal > 0.4):
            pattern = 'mild_ptsd_like_pattern'
        else:
            pattern = 'minimal_ptsd_like_pattern'
        
        return {
            'overall_pattern': pattern,
            'mean_intrusion': float(mean_intrusion),
            'mean_avoidance': float(mean_avoidance),
            'mean_arousal': float(mean_arousal),
            'mean_negative_cognition': float(mean_negative_cognition)
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
    
    def explain_patterns(self, results: Optional[Dict] = None) -> str:
        """
        루프 기반 패턴 해석 리포트 생성
        
        Args:
            results: 시뮬레이션 결과 (없으면 최근 결과 사용)
        
        Returns:
            패턴 해석 리포트 (텍스트)
        """
        if results is None:
            # 최근 결과 사용
            if not hasattr(self, 'last_results'):
                return "⚠️ 시뮬레이션 결과가 없습니다."
            results = self.last_results
        
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("🔍 루프 기반 패턴 해석 리포트")
        report_lines.append("=" * 70)
        report_lines.append("")
        
        # 루프 분석이 있는 경우
        if 'loop_analysis' in results:
            loop_analysis = results['loop_analysis']
            
            report_lines.append("📊 활성화된 루프 분석:")
            report_lines.append("")
            
            for loop_name, loop_info in loop_analysis['active_loops'].items():
                strength = loop_info['mean_strength']
                is_active = loop_info['is_active']
                activation_count = loop_info['activation_count']
                
                status = "🟢 활성화" if is_active else "⚪ 비활성화"
                report_lines.append(f"  • {loop_name}:")
                report_lines.append(f"    - 상태: {status}")
                report_lines.append(f"    - 평균 강도: {strength:.3f}")
                report_lines.append(f"    - 활성화 횟수: {activation_count}")
                report_lines.append("")
            
            # 루프 조합 분석
            if loop_analysis.get('loop_interactions'):
                report_lines.append("🔗 루프 간 상호작용:")
                report_lines.append("")
                for interaction in loop_analysis['loop_interactions']:
                    report_lines.append(f"  • {interaction['description']}")
                report_lines.append("")
        
        # 패턴 해석
        if 'overall_pattern' in results:
            pattern = results['overall_pattern']
            report_lines.append("📋 관측된 패턴:")
            report_lines.append(f"  • {pattern}")
            report_lines.append("")
            
            # 패턴별 루프 해석
            if 'depression' in pattern.lower():
                report_lines.append("💡 우울증 패턴의 루프 메커니즘:")
                report_lines.append("")
                report_lines.append("  1. 부정적 편향 루프:")
                report_lines.append("     - 부정적 자극 → 반추 강화 → 기억 편향 → 더 많은 부정적 자극 감지")
                report_lines.append("     - 이 루프가 활성화되면 부정적 사고가 지속적으로 강화됩니다.")
                report_lines.append("")
                report_lines.append("  2. 제어 실패 루프:")
                report_lines.append("     - 부정적 사고 → 억제 실패 → 루프 강화 → 더 많은 부정적 사고")
                report_lines.append("     - 인지 제어가 약해지면 부정적 사고를 억제하기 어려워집니다.")
                report_lines.append("")
                report_lines.append("  3. 에너지 붕괴 루프:")
                report_lines.append("     - 에너지 고갈 → 회복 속도 감소 → 수면 저하 → 더 많은 고갈")
                report_lines.append("     - 에너지가 낮아지면 회복이 더 어려워지는 악순환이 형성됩니다.")
                report_lines.append("")
            
            elif 'ptsd' in pattern.lower():
                report_lines.append("💡 PTSD 패턴의 루프 메커니즘:")
                report_lines.append("")
                report_lines.append("  1. 과각성 루프:")
                report_lines.append("     - 위협 감지 → 각성 증가 → 수면 저하 → 더 많은 위협 감지")
                report_lines.append("     - 과각성 상태가 지속되면 수면이 방해받고 더 예민해집니다.")
                report_lines.append("")
                report_lines.append("  2. 부정적 편향 루프:")
                report_lines.append("     - 외상 기억 → 부정적 해석 → 기억 강화 → 더 많은 침입")
                report_lines.append("     - 부정적 편향이 강해지면 외상 기억이 더 자주 침입합니다.")
                report_lines.append("")
        
        # 종합 해석
        report_lines.append("=" * 70)
        report_lines.append("⚠️  중요 안내:")
        report_lines.append("   이 해석은 시뮬레이션 기반 패턴 분석입니다.")
        report_lines.append("   실제 의학적 진단이나 치료 권고가 아닙니다.")
        report_lines.append("=" * 70)
        
        report = "\n".join(report_lines)
        return report
    
    def _analyze_loop_combinations(self) -> Dict:
        """
        루프 조합 분석
        
        Returns:
            루프 조합 분석 결과
        """
        if not self.loop_history:
            return {
                'active_loops': {},
                'loop_interactions': []
            }
        
        # 각 루프의 통계 계산
        active_loops = {}
        for loop_name, loop in self.active_loops.items():
            stats = loop.get_statistics()
            active_loops[loop_name] = {
                'mean_strength': stats.get('mean_strength', 0.0),
                'max_strength': stats.get('max_strength', 0.0),
                'is_active': stats.get('is_active', False),
                'activation_count': stats.get('activation_count', 0)
            }
        
        # 루프 간 상호작용 분석
        loop_interactions = []
        
        # 부정적 편향 루프와 제어 실패 루프의 상호작용
        if 'negative_bias' in active_loops and 'control_failure' in active_loops:
            nb_strength = active_loops['negative_bias']['mean_strength']
            cf_strength = active_loops['control_failure']['mean_strength']
            
            if nb_strength > 0.3 and cf_strength > 0.3:
                loop_interactions.append({
                    'type': 'reinforcement',
                    'loops': ['negative_bias', 'control_failure'],
                    'description': '부정적 편향 루프와 제어 실패 루프가 서로 강화하는 패턴 관측'
                })
        
        # 에너지 붕괴 루프와 제어 실패 루프의 상호작용
        if 'energy_collapse' in active_loops and 'control_failure' in active_loops:
            ec_strength = active_loops['energy_collapse']['mean_strength']
            cf_strength = active_loops['control_failure']['mean_strength']
            
            if ec_strength > 0.2 and cf_strength > 0.3:
                loop_interactions.append({
                    'type': 'reinforcement',
                    'loops': ['energy_collapse', 'control_failure'],
                    'description': '에너지 붕괴로 인한 인지 제어 약화 패턴 관측'
                })
        
        return {
            'active_loops': active_loops,
            'loop_interactions': loop_interactions
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

