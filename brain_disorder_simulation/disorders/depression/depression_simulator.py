"""
우울증 시뮬레이터 (독립 클래스)

Cookiie Brain Engine을 사용한 우울증 메커니즘 시뮬레이션
목적: "왜 이런 상황이 발생할 수 있는가?" 원인 분석

⚠️ 주의: 이 시뮬레이터는 치료 도구가 아닙니다.
- 진단 도구 아님
- 치료 솔루션 제시 아님
- 패턴 관측 및 메커니즘 분석 목적

핵심 정체성: "우울증 붕괴 메커니즘 엔진"
- 에너지 시스템 붕괴 이후 동기 루프가 끊어진 상태를 재현
- 질환이 만들어지는 과정을 관측

Author: GNJz (Qquarts)
Version: 1.0.0
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
                                str(Path(__file__).parent.parent.parent.parent.parent / 'Cookiie_Brain_Engine'))
sys.path.insert(0, str(Path(cookiie_brain_path) / 'package'))

try:
    from cookiie_brain import (
        CookiieBrainEngine, CookiieBrainConfig,
        BrainInput, BrainOutput, BrainState
    )
    COOKIIE_BRAIN_AVAILABLE = True
except ImportError:
    COOKIIE_BRAIN_AVAILABLE = False
    print("⚠️  Cookiie Brain Engine을 찾을 수 없습니다. 기본 모드로 실행합니다.")

# 공통 엔진
from ...common.negative_bias_engine import NegativeBiasEngine
from ...common.cognitive_control_engine import CognitiveControlEngine
from ...common.energy_depletion_engine import EnergyDepletionEngine

# 우울증 특화 엔진
from .motivation_engine import MotivationEngine

# 유틸리티
from ...utils.reproducibility import ReproducibleRNG, ExperimentMetadata
from ...utils.statistics import StatisticalValidator
from ...utils.report_generator import ReportGenerator

# 우울증 특화 태스크
try:
    from .depression_tasks import (
        MotivationCollapseTask,
        RuminationPersistenceTask,
        EffortBasedDecisionMakingTask
    )
    DEPRESSION_TASKS_AVAILABLE = True
except ImportError:
    DEPRESSION_TASKS_AVAILABLE = False


class DepressionSimulator:
    """
    우울증 시뮬레이터 (독립 클래스)
    
    Cookiie Brain Engine과 우울증 특화 엔진을 통합한 시뮬레이션 시스템
    목적: 우울증 메커니즘의 원인 분석 및 패턴 관측
    
    핵심 특징:
    - 초기 에너지 낮음
    - 보상 민감도 낮음
    - 회복 루프 억제
    - Cookiie Brain Engine과 실시간 동적 연결
    """
    
    def __init__(self, 
                 config: Optional[CookiieBrainConfig] = None,
                 seed: Optional[int] = None,
                 negative_bias_strength: float = 0.6,
                 control_impairment: float = 0.5,
                 energy_depletion_rate: float = 0.5,
                 motivation_deficit: float = 0.6,
                 initial_energy: float = 60.0,  # 우울증: 초기 에너지 낮음
                 recovery_inhibition: float = 0.7):  # 회복 루프 억제
        """
        우울증 시뮬레이터 초기화
        
        Args:
            config: Cookiie Brain Engine 설정
            seed: 재현성을 위한 시드 값
            negative_bias_strength: 부정적 편향 강도 (0.0 ~ 1.0)
            control_impairment: 인지 제어 약화 정도 (0.0 ~ 1.0)
            energy_depletion_rate: 에너지 고갈 속도 (0.0 ~ 1.0)
            motivation_deficit: 동기 결핍 정도 (0.0 ~ 1.0)
            initial_energy: 초기 에너지 수준 (우울증: 낮음, 기본 60.0)
            recovery_inhibition: 회복 루프 억제 강도 (0.0 ~ 1.0)
        """
        # 재현성 시스템 초기화
        self.rng = ReproducibleRNG(seed=seed)
        self.seed = self.rng.seed
        
        # 우울증 특성 파라미터
        self.negative_bias_strength = np.clip(negative_bias_strength, 0.0, 1.0)
        self.control_impairment = np.clip(control_impairment, 0.0, 1.0)
        self.energy_depletion_rate = np.clip(energy_depletion_rate, 0.0, 1.0)
        self.motivation_deficit = np.clip(motivation_deficit, 0.0, 1.0)
        self.initial_energy = initial_energy  # 우울증: 초기 에너지 낮음
        self.recovery_inhibition = np.clip(recovery_inhibition, 0.0, 1.0)
        
        # Cookiie Brain Engine 초기화
        self.brain = None
        if COOKIIE_BRAIN_AVAILABLE:
            if config is None:
                config = CookiieBrainConfig(
                    enable_dynamics=True,
                    enable_dynamics_integration=True,
                    log_level='ERROR'
                )
            self.brain = CookiieBrainEngine(config)
        
        # 우울증 엔진 초기화
        self.common_engines = {}
        self.disorder_engines = {}
        
        # 공통 엔진
        self.common_engines['negative_bias'] = NegativeBiasEngine(
            negative_bias_strength=self.negative_bias_strength,
            rng=self.rng.get_rng('negative_bias')
        )
        
        self.common_engines['cognitive_control'] = CognitiveControlEngine(
            control_impairment=self.control_impairment,
            rng=self.rng.get_rng('cognitive_control')
        )
        
        self.common_engines['energy_depletion'] = EnergyDepletionEngine(
            depletion_rate=self.energy_depletion_rate,
            rng=self.rng.get_rng('energy_depletion')
        )
        
        # 우울증 특화: 초기 에너지 낮게 설정
        self.common_engines['energy_depletion'].state.current_energy = self.initial_energy
        
        # 우울증 특화 엔진
        self.disorder_engines['motivation'] = MotivationEngine(
            motivation_deficit=self.motivation_deficit,
            rng=self.rng.get_rng('motivation')
        )
        
        # 시뮬레이션 데이터
        self.simulation_data = {
            'timestamps': [],
            'negative_bias_scores': [],
            'cognitive_control_scores': [],
            'energy_scores': [],
            'motivation_scores': [],
            'brain_states': [],  # Cookiie Brain Engine 상태
            'pattern_observations': []
        }
        
        # 통계적 검증 시스템
        self.statistical_validator = StatisticalValidator()
        
        # 리포트 생성기
        self.report_generator = ReportGenerator()
        
        # 시뮬레이션 시작 시간
        self.start_time = None
    
    def simulate_full_depression_assessment(self,
                                           duration: float = 300.0,
                                           enable_brain_integration: bool = True) -> Dict:
        """
        우울증 전체 평가 시뮬레이션
        
        Args:
            duration: 시뮬레이션 지속 시간 (초)
            enable_brain_integration: Cookiie Brain Engine 통합 활성화
        
        Returns:
            시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🔬 우울증 붕괴 메커니즘 시뮬레이션")
        print(f"{'='*70}")
        print(f"목적: 우울증 패턴의 원인 분석 (에너지 시스템 붕괴 → 동기 루프 단절)")
        print(f"지속 시간: {duration}초")
        print(f"초기 에너지: {self.initial_energy:.1f} (우울증: 낮음)")
        print(f"회복 억제: {self.recovery_inhibition:.1f}")
        print(f"{'='*70}\n")
        
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
            'brain_states': [],
            'pattern_observations': []
        }
        
        # Cookiie Brain Engine 초기 상태
        if enable_brain_integration and self.brain:
            initial_brain_state = self._get_brain_state()
            self.simulation_data['brain_states'].append(initial_brain_state)
        
        for step in range(steps):
            t = step * dt
            
            # ============================================================
            # 1. 부정적 편향 처리 (1초마다)
            # ============================================================
            if step % 10 == 0:
                stimulus = self._generate_random_stimulus()
                bias_result = self.common_engines['negative_bias'].process_stimulus(
                    stimulus_valence=stimulus['valence'],
                    stimulus_intensity=stimulus['intensity'],
                    time_elapsed=t
                )
                
                # Cookiie Brain Engine 통합: Amygdala에 부정적 편향 반영
                if enable_brain_integration and self.brain:
                    self._update_brain_from_bias(bias_result, t)
            
            # ============================================================
            # 2. 인지 제어 처리 (2초마다)
            # ============================================================
            if step % 20 == 0:
                thought_intensity = 0.3 + self.rng.get_rng('thought').random() * 0.4
                thought_result = self.common_engines['cognitive_control'].process_negative_thought(
                    thought_intensity=thought_intensity,
                    time_elapsed=t
                )
                
                # Cookiie Brain Engine 통합: PFC에 인지 제어 상태 반영
                if enable_brain_integration and self.brain:
                    self._update_brain_from_cognitive_control(thought_result, t)
            
            # ============================================================
            # 3. 에너지 고갈 (매 스텝)
            # ============================================================
            energy_rng = self.rng.get_rng('energy')
            cognitive_load = 0.3 + energy_rng.random() * 0.4
            stress_level = 0.2 + energy_rng.random() * 0.3
            
            # 우울증 특성: 회복 억제 적용
            energy_result = self.common_engines['energy_depletion'].update_energy(
                cognitive_load=cognitive_load,
                stress_level=stress_level,
                dt=dt
            )
            
            # 회복 억제: 회복 속도를 감소시킴
            if energy_result['recovery'] > 0:
                energy_result['recovery'] *= (1.0 - self.recovery_inhibition)
                # 에너지 재계산
                energy_change = energy_result['recovery'] - energy_result['consumption']
                self.common_engines['energy_depletion'].state.current_energy = np.clip(
                    self.common_engines['energy_depletion'].state.current_energy + energy_change,
                    0.0, 100.0
                )
            
            # Cookiie Brain Engine 통합: Hypothalamus에 에너지 상태 반영
            if enable_brain_integration and self.brain:
                self._update_brain_from_energy(energy_result, t)
            
            # ============================================================
            # 4. 동기 처리 (3초마다)
            # ============================================================
            if step % 30 == 0:
                reward = self._generate_random_reward()
                motivation_result = self.disorder_engines['motivation'].process_reward(
                    reward_value=reward['value'],
                    effort_required=reward['effort']
                )
                
                # Cookiie Brain Engine 통합: Basal Ganglia에 동기 상태 반영
                if enable_brain_integration and self.brain:
                    self._update_brain_from_motivation(motivation_result, t)
            
            # ============================================================
            # 5. 상태 업데이트
            # ============================================================
            self.common_engines['negative_bias'].update_rumination(dt)
            self.common_engines['cognitive_control'].update_negative_loop(dt)
            
            # ============================================================
            # 6. 데이터 기록 (1초마다)
            # ============================================================
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
                
                # Cookiie Brain Engine 상태 기록
                if enable_brain_integration and self.brain:
                    brain_state = self._get_brain_state()
                    self.simulation_data['brain_states'].append(brain_state)
        
        # 결과 분석
        results = self._analyze_depression_patterns()
        
        print(f"\n✅ 우울증 시뮬레이션 완료!")
        print(f"   종합 패턴: {results['overall_pattern']}")
        print(f"   종합 점수: {results['mean_depression_score']:.3f}")
        print(f"   에너지 최종: {self.common_engines['energy_depletion'].state.current_energy:.1f}")
        print(f"   동기 최종: {self.disorder_engines['motivation'].state.motivation_level:.3f}")
        
        return results
    
    # ======================================================================
    # 우울증 특화 태스크 메서드
    # ======================================================================
    
    def run_motivation_collapse_task(self, num_trials: int = 20) -> Dict:
        """
        동기 붕괴 태스크 실행
        
        Args:
            num_trials: 시행 횟수
        
        Returns:
            태스크 결과
        """
        if not DEPRESSION_TASKS_AVAILABLE:
            return {'status': 'not_available', 'message': 'Depression tasks module not available'}
        
        print(f"\n{'='*70}")
        print(f"🔬 동기 붕괴 태스크")
        print(f"{'='*70}")
        print(f"목적: 동기 루프 단절 지점 관측")
        print(f"시행 횟수: {num_trials}")
        print(f"{'='*70}\n")
        
        task = MotivationCollapseTask(
            motivation_engine=self.disorder_engines['motivation'],
            rng=self.rng.get_rng('motivation_task')
        )
        
        result = task.run(num_trials=num_trials)
        
        print(f"✅ 동기 붕괴 태스크 완료!")
        print(f"   패턴: {result.pattern_observation}")
        print(f"   초기 동기: {result.metrics['initial_motivation']:.3f}")
        print(f"   최종 동기: {result.metrics['final_motivation']:.3f}")
        if result.metrics['collapse_point'] is not None:
            print(f"   붕괴 지점: 시행 {result.metrics['collapse_point']}")
        print(f"   행동 비율: {result.metrics['action_rate']:.2%}")
        
        return {
            'task_name': result.task_name,
            'success': result.success,
            'metrics': result.metrics,
            'pattern': result.pattern_observation
        }
    
    def run_rumination_persistence_task(self, duration: float = 60.0) -> Dict:
        """
        반추 지속 태스크 실행
        
        Args:
            duration: 시뮬레이션 지속 시간 (초)
        
        Returns:
            태스크 결과
        """
        if not DEPRESSION_TASKS_AVAILABLE:
            return {'status': 'not_available', 'message': 'Depression tasks module not available'}
        
        print(f"\n{'='*70}")
        print(f"🔬 반추 지속 태스크")
        print(f"{'='*70}")
        print(f"목적: 부정적 사고 지속 메커니즘 관측")
        print(f"지속 시간: {duration}초")
        print(f"{'='*70}\n")
        
        task = RuminationPersistenceTask(
            negative_bias_engine=self.common_engines['negative_bias'],
            cognitive_control_engine=self.common_engines['cognitive_control'],
            rng=self.rng.get_rng('rumination_task')
        )
        
        result = task.run(duration=duration)
        
        print(f"✅ 반추 지속 태스크 완료!")
        print(f"   패턴: {result.pattern_observation}")
        print(f"   평균 반추 강도: {result.metrics['average_rumination']:.3f}")
        print(f"   억제 성공률: {result.metrics['inhibition_success_rate']:.2%}")
        print(f"   반추 지속도: {result.metrics['rumination_persistence']:.3f}")
        
        return {
            'task_name': result.task_name,
            'success': result.success,
            'metrics': result.metrics,
            'pattern': result.pattern_observation
        }
    
    def run_effort_based_decision_task(self, num_tasks: int = 15) -> Dict:
        """
        노력 기반 의사결정 태스크 실행
        
        Args:
            num_tasks: 작업 수
        
        Returns:
            태스크 결과
        """
        if not DEPRESSION_TASKS_AVAILABLE:
            return {'status': 'not_available', 'message': 'Depression tasks module not available'}
        
        print(f"\n{'='*70}")
        print(f"🔬 노력 기반 의사결정 태스크")
        print(f"{'='*70}")
        print(f"목적: 노력 대비 포기 임계점 관측")
        print(f"작업 수: {num_tasks}")
        print(f"{'='*70}\n")
        
        task = EffortBasedDecisionMakingTask(
            motivation_engine=self.disorder_engines['motivation'],
            energy_engine=self.common_engines['energy_depletion'],
            rng=self.rng.get_rng('effort_task')
        )
        
        result = task.run(num_tasks=num_tasks)
        
        print(f"✅ 노력 기반 의사결정 태스크 완료!")
        print(f"   패턴: {result.pattern_observation}")
        print(f"   수락률: {result.metrics['acceptance_rate']:.2%}")
        print(f"   거부률: {result.metrics['rejection_rate']:.2%}")
        print(f"   최종 에너지: {result.metrics['final_energy']:.2f}")
        print(f"   최종 동기: {result.metrics['final_motivation']:.3f}")
        
        return {
            'task_name': result.task_name,
            'success': result.success,
            'metrics': result.metrics,
            'pattern': result.pattern_observation
        }
    
    def run_all_depression_tasks(self) -> Dict:
        """
        모든 우울증 특화 태스크 실행
        
        Returns:
            통합 태스크 결과
        """
        print(f"\n{'='*70}")
        print(f"🔬 우울증 특화 태스크 전체 실행")
        print(f"{'='*70}\n")
        
        results = {}
        
        # 1. 동기 붕괴 태스크
        results['motivation_collapse'] = self.run_motivation_collapse_task()
        
        # 2. 반추 지속 태스크
        results['rumination_persistence'] = self.run_rumination_persistence_task()
        
        # 3. 노력 기반 의사결정 태스크
        results['effort_decision'] = self.run_effort_based_decision_task()
        
        # 종합 분석
        print(f"\n{'='*70}")
        print(f"📊 우울증 특화 태스크 종합 결과")
        print(f"{'='*70}")
        print(f"1. 동기 붕괴: {results['motivation_collapse']['pattern']}")
        print(f"2. 반추 지속: {results['rumination_persistence']['pattern']}")
        print(f"3. 노력 의사결정: {results['effort_decision']['pattern']}")
        print(f"{'='*70}\n")
        
        return results
    
    # ======================================================================
    # Cookiie Brain Engine 통합 메서드
    # ======================================================================
    
    def _get_brain_state(self) -> Dict:
        """Cookiie Brain Engine 현재 상태 가져오기"""
        if not self.brain:
            return {}
        
        try:
            state = self.brain.get_state()
            return {
                'energy': state.get('energy', 0.0),
                'arousal': state.get('arousal', 0.0),
                'emotion': state.get('emotion', {}),
                'attention': state.get('attention', 0.0)
            }
        except:
            return {}
    
    def _update_brain_from_bias(self, bias_result: Dict, t: float):
        """부정적 편향 결과를 Cookiie Brain Engine에 반영"""
        if not self.brain:
            return
        
        try:
            # Amygdala에 부정적 편향 반영
            sensory_input = {
                'valence': bias_result.get('perceived_valence', 0.0),
                'intensity': bias_result.get('perceived_intensity', 0.0),
                'threat_detected': bias_result.get('threat_detected', False)
            }
            
            brain_input = BrainInput(
                sensory=sensory_input,
                context={'time': t, 'source': 'negative_bias'}
            )
            
            self.brain.process(brain_input)
        except Exception as e:
            pass  # 통합 실패 시 무시
    
    def _update_brain_from_cognitive_control(self, thought_result: Dict, t: float):
        """인지 제어 결과를 Cookiie Brain Engine에 반영"""
        if not self.brain:
            return
        
        try:
            # PFC에 인지 제어 상태 반영
            sensory_input = {
                'cognitive_load': 1.0 - thought_result.get('alternative_thinking', 0.5),
                'inhibition_success': thought_result.get('inhibition_success', False),
                'negative_loop': thought_result.get('negative_loop_strength', 0.0)
            }
            
            brain_input = BrainInput(
                sensory=sensory_input,
                context={'time': t, 'source': 'cognitive_control'}
            )
            
            self.brain.process(brain_input)
        except Exception as e:
            pass
    
    def _update_brain_from_energy(self, energy_result: Dict, t: float):
        """에너지 결과를 Cookiie Brain Engine에 반영"""
        if not self.brain:
            return
        
        try:
            # Hypothalamus에 에너지 상태 반영
            sensory_input = {
                'energy_level': energy_result.get('current_energy', 0.0) / 100.0,
                'energy_change': energy_result.get('energy_change', 0.0),
                'stress': energy_result.get('consumption', 0.0) * 10.0
            }
            
            brain_input = BrainInput(
                sensory=sensory_input,
                context={'time': t, 'source': 'energy_depletion'}
            )
            
            self.brain.process(brain_input)
        except Exception as e:
            pass
    
    def _update_brain_from_motivation(self, motivation_result: Dict, t: float):
        """동기 결과를 Cookiie Brain Engine에 반영"""
        if not self.brain:
            return
        
        try:
            # Basal Ganglia에 동기 상태 반영
            sensory_input = {
                'reward_value': motivation_result.get('perceived_reward', 0.0),
                'effort_cost': motivation_result.get('effort_cost', 0.0),
                'can_engage': motivation_result.get('can_engage', False)
            }
            
            brain_input = BrainInput(
                sensory=sensory_input,
                context={'time': t, 'source': 'motivation'}
            )
            
            self.brain.process(brain_input)
        except Exception as e:
            pass
    
    # ======================================================================
    # 헬퍼 메서드
    # ======================================================================
    
    def _generate_random_stimulus(self) -> Dict:
        """랜덤 자극 생성"""
        rng = self.rng.get_rng('stimulus')
        # 우울증: 부정적 자극 비중 높음
        valence = rng.choice([-0.8, -0.6, -0.4, 0.0, 0.2, 0.4],
                            p=[0.25, 0.20, 0.15, 0.15, 0.15, 0.10])
        intensity = 0.5 + rng.random() * 0.5
        return {'valence': valence, 'intensity': intensity}
    
    def _generate_random_reward(self) -> Dict:
        """랜덤 보상 생성"""
        rng = self.rng.get_rng('reward')
        # 우울증: 보상 가치 낮게 인식
        return {
            'value': 0.2 + rng.random() * 0.4,  # 낮은 보상
            'effort': 0.4 + rng.random() * 0.4  # 높은 노력
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
            'motivation_score': float(np.mean(motivation_scores)),
            'final_energy': float(self.common_engines['energy_depletion'].state.current_energy),
            'final_motivation': float(self.disorder_engines['motivation'].state.motivation_level)
        }
    
    def visualize_results(self, output_path: Optional[str] = None):
        """결과 시각화"""
        if not self.simulation_data['timestamps']:
            print("⚠️ 시각화할 데이터가 없습니다.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('우울증 붕괴 메커니즘 시뮬레이션 결과\n(에너지 시스템 붕괴 → 동기 루프 단절)', 
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
            ax3.set_title('에너지 고갈 메커니즘 (회복 억제)')
            ax3.grid(True, alpha=0.3)
            ax3.legend()
        
        # 4. 동기
        if 'motivation_scores' in self.simulation_data and self.simulation_data['motivation_scores']:
            ax4 = axes[1, 1]
            ax4.plot(timestamps, self.simulation_data['motivation_scores'],
                     'm-', linewidth=2, label='동기 점수')
            ax4.set_xlabel('시간 (초)')
            ax4.set_ylabel('동기 점수')
            ax4.set_title('동기 감소 메커니즘 (루프 단절)')
            ax4.grid(True, alpha=0.3)
            ax4.legend()
        
        plt.tight_layout()
        
        # 저장 경로 결정
        if output_path:
            save_path = output_path
        else:
            save_path = os.path.join(os.getcwd(), 'depression_simulation_results.png')
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"\n💾 시각화 저장: {save_path}")
        print(f"   절대 경로: {os.path.abspath(save_path)}")
        
        plt.close()


def main():
    """메인 실행 함수"""
    print("\n" + "="*70)
    print("🔬 우울증 붕괴 메커니즘 시뮬레이터")
    print("="*70)
    print("목적: 우울증 패턴의 원인 분석 (에너지 시스템 붕괴 → 동기 루프 단절)")
    print("⚠️  주의: 이 시뮬레이터는 치료 도구가 아닙니다.")
    print("="*70 + "\n")
    
    # 우울증 시뮬레이터 생성
    simulator = DepressionSimulator(
        seed=42,
        negative_bias_strength=0.6,
        control_impairment=0.5,
        energy_depletion_rate=0.5,
        motivation_deficit=0.6,
        initial_energy=60.0,  # 우울증: 초기 에너지 낮음
        recovery_inhibition=0.7  # 회복 루프 억제
    )
    
    # 우울증 시뮬레이션 실행
    results = simulator.simulate_full_depression_assessment(
        duration=300.0,
        enable_brain_integration=True
    )
    
    # 우울증 특화 태스크 실행
    task_results = simulator.run_all_depression_tasks()
    
    # 결과 시각화
    simulator.visualize_results()
    
    print("\n" + "="*70)
    print("✅ 시뮬레이션 완료!")
    print("="*70)
    print(f"\n관측된 패턴: {results['overall_pattern']}")
    print(f"종합 점수: {results['mean_depression_score']:.3f}")
    print(f"최종 에너지: {results['final_energy']:.1f}")
    print(f"최종 동기: {results['final_motivation']:.3f}")
    print("\n⚠️  이 결과는 패턴 관측 및 메커니즘 분석 목적입니다.")
    print("   진단 도구나 치료 솔루션이 아닙니다.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

