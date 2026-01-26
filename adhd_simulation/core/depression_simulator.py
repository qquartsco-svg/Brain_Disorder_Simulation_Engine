"""
우울증 시뮬레이터

Cookiie Brain Engine을 사용한 우울증 메커니즘 시뮬레이션
목적: "왜 이런 상황이 발생할 수 있는가?" 원인 분석

⚠️ 주의: 이 시뮬레이터는 치료 도구가 아닙니다.
- 진단 도구 아님
- 치료 솔루션 제시 아님
- 패턴 관측 및 메커니즘 분석 목적

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
                                str(Path(__file__).parent.parent.parent.parent / 'Cookiie_Brain_Engine'))
sys.path.insert(0, str(Path(cookiie_brain_path) / 'package'))

from cookiie_brain import (
    CookiieBrainEngine, CookiieBrainConfig,
    BrainInput, BrainOutput, BrainState
)

from .depression_engines import (
    NegativeBiasEngine,
    CognitiveControlEngine,
    EnergyDepletionEngine,
    MotivationEngine
)

from ..utils.reproducibility import ReproducibleRNG, ExperimentMetadata
from ..utils.statistics import StatisticalValidator
from ..utils.report_generator import ReportGenerator


class DepressionSimulator:
    """
    우울증 시뮬레이터
    
    Cookiie Brain Engine과 우울증 특화 엔진을 통합한 시뮬레이션 시스템
    목적: 우울증 메커니즘의 원인 분석 및 패턴 관측
    """
    
    def __init__(self, 
                 config: Optional[CookiieBrainConfig] = None,
                 seed: Optional[int] = None,
                 negative_bias_strength: float = 0.5,
                 control_impairment: float = 0.5,
                 energy_depletion_rate: float = 0.5,
                 motivation_deficit: float = 0.5):
        """
        우울증 시뮬레이터 초기화
        
        Args:
            config: Cookiie Brain Engine 설정
            seed: 재현성을 위한 시드 값
            negative_bias_strength: 부정적 편향 강도 (0.0 ~ 1.0)
            control_impairment: 인지 제어 약화 정도 (0.0 ~ 1.0)
            energy_depletion_rate: 에너지 고갈 속도 (0.0 ~ 1.0)
            motivation_deficit: 동기 결핍 정도 (0.0 ~ 1.0)
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
        
        # 우울증 특화 엔진 초기화
        self.depression_engines = {
            'negative_bias': NegativeBiasEngine(
                negative_bias_strength=negative_bias_strength,
                rng=self.rng.get_rng('negative_bias')
            ),
            'cognitive_control': CognitiveControlEngine(
                control_impairment=control_impairment,
                rng=self.rng.get_rng('cognitive_control')
            ),
            'energy_depletion': EnergyDepletionEngine(
                depletion_rate=energy_depletion_rate,
                rng=self.rng.get_rng('energy_depletion')
            ),
            'motivation': MotivationEngine(
                motivation_deficit=motivation_deficit,
                rng=self.rng.get_rng('motivation')
            )
        }
        
        # 시뮬레이션 데이터
        self.simulation_data = {
            'timestamps': [],
            'negative_bias_scores': [],
            'cognitive_control_scores': [],
            'energy_scores': [],
            'motivation_scores': [],
            'brain_states': [],
            'stimulus_events': [],
            'pattern_observations': []
        }
        
        # 통계적 검증 시스템
        self.statistical_validator = StatisticalValidator()
        
        # 리포트 생성기
        self.report_generator = ReportGenerator()
        
        # 실험 메타데이터
        self.experiment_metadata = None
        
        # 시뮬레이션 시작 시간
        self.start_time = None
    
    def simulate_negative_bias_task(self,
                                   duration: float = 60.0,
                                   stimulus_sequence: Optional[List[Dict]] = None) -> Dict:
        """
        부정적 편향 테스트 시뮬레이션
        
        핵심 질문: "왜 부정적 편향이 발생하는가?"
        
        Args:
            duration: 시뮬레이션 지속 시간 (초)
            stimulus_sequence: 자극 시퀀스 (None이면 자동 생성)
        
        Returns:
            시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🔬 우울증 부정적 편향 메커니즘 시뮬레이션")
        print(f"{'='*70}")
        print(f"지속 시간: {duration}초")
        print(f"목적: 부정적 편향 발생 메커니즘 탐색")
        print(f"{'='*70}\n")
        
        self.start_time = time.time()
        dt = 0.1
        steps = int(duration / dt)
        
        # 자극 시퀀스 생성 (없으면 자동 생성)
        if stimulus_sequence is None:
            stimulus_sequence = self._generate_stimulus_sequence(duration, dt)
        
        # 시뮬레이션 루프
        for step in range(steps):
            t = step * dt
            
            # 현재 시점의 자극 찾기
            current_stimuli = [s for s in stimulus_sequence 
                             if s['start_time'] <= t <= s['end_time']]
            
            # 각 자극 처리
            for stimulus in current_stimuli:
                result = self.depression_engines['negative_bias'].process_stimulus(
                    stimulus_valence=stimulus['valence'],
                    stimulus_intensity=stimulus['intensity'],
                    time_elapsed=t
                )
                
                # Brain Engine에 입력
                brain_input = BrainInput(
                    sensory={
                        'stimulus': {
                            'valence': result['perceived_valence'],
                            'intensity': result['perceived_intensity'],
                            'threat_detected': result['threat_detected']
                        }
                    }
                )
                
                brain_output = self.brain.process(brain_input)
                
                # 데이터 기록
                self.simulation_data['timestamps'].append(t)
                self.simulation_data['negative_bias_scores'].append(
                    self.depression_engines['negative_bias'].get_bias_score()
                )
                self.simulation_data['stimulus_events'].append({
                    'time': t,
                    'original_valence': stimulus['valence'],
                    'perceived_valence': result['perceived_valence'],
                    'bias_applied': result['bias_applied']
                })
            
            # 반추 업데이트
            self.depression_engines['negative_bias'].update_rumination(dt)
        
        # 결과 분석
        results = self._analyze_negative_bias_patterns()
        
        print(f"\n✅ 부정적 편향 메커니즘 시뮬레이션 완료!")
        print(f"   관측된 패턴: {results['pattern_type']}")
        print(f"   부정적 편향 점수: {results['bias_score']:.3f}")
        
        return results
    
    def simulate_cognitive_control_task(self,
                                       duration: float = 60.0,
                                       cognitive_tasks: Optional[List[Dict]] = None) -> Dict:
        """
        인지 제어 약화 테스트 시뮬레이션
        
        핵심 질문: "왜 인지 제어가 약화되는가?"
        
        Args:
            duration: 시뮬레이션 지속 시간 (초)
            cognitive_tasks: 인지 작업 리스트 (None이면 자동 생성)
        
        Returns:
            시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🔬 우울증 인지 제어 약화 메커니즘 시뮬레이션")
        print(f"{'='*70}")
        print(f"지속 시간: {duration}초")
        print(f"목적: 인지 제어 약화 메커니즘 탐색")
        print(f"{'='*70}\n")
        
        self.start_time = time.time()
        dt = 0.1
        steps = int(duration / dt)
        
        # 인지 작업 생성 (없으면 자동 생성)
        if cognitive_tasks is None:
            cognitive_tasks = self._generate_cognitive_tasks(duration, dt)
        
        # 시뮬레이션 루프
        for step in range(steps):
            t = step * dt
            
            # 현재 시점의 작업 찾기
            current_tasks = [task for task in cognitive_tasks
                           if task['start_time'] <= t <= task['end_time']]
            
            for task in current_tasks:
                # 부정적 사고 처리
                if task.get('negative_thought', False):
                    thought_result = self.depression_engines['cognitive_control'].process_negative_thought(
                        thought_intensity=task.get('thought_intensity', 0.5),
                        time_elapsed=t
                    )
                    
                    # 억제 실패 시 부정적 루프 강화
                    if not thought_result['inhibition_success']:
                        # Brain Engine에 부정적 상태 전달
                        brain_input = BrainInput(
                            sensory={
                                'cognitive_state': {
                                    'negative_loop': thought_result['negative_loop_strength'],
                                    'control_impaired': thought_result['control_impaired']
                                }
                            }
                        )
                        self.brain.process(brain_input)
                
                # 인지 제어 작업
                if task.get('requires_control', False):
                    control_result = self.depression_engines['cognitive_control'].attempt_cognitive_control(
                        task_difficulty=task.get('difficulty', 0.5)
                    )
                    
                    # 데이터 기록
                    self.simulation_data['timestamps'].append(t)
                    self.simulation_data['cognitive_control_scores'].append(
                        self.depression_engines['cognitive_control'].get_control_score()
                    )
            
            # 부정적 루프 업데이트
            self.depression_engines['cognitive_control'].update_negative_loop(dt)
        
        # 결과 분석
        results = self._analyze_cognitive_control_patterns()
        
        print(f"\n✅ 인지 제어 약화 메커니즘 시뮬레이션 완료!")
        print(f"   관측된 패턴: {results['pattern_type']}")
        print(f"   인지 제어 점수: {results['control_score']:.3f}")
        
        return results
    
    def simulate_energy_depletion_task(self,
                                      duration: float = 120.0,
                                      stress_events: Optional[List[Dict]] = None) -> Dict:
        """
        에너지 고갈 테스트 시뮬레이션
        
        핵심 질문: "왜 에너지가 고갈되는가?"
        
        Args:
            duration: 시뮬레이션 지속 시간 (초)
            stress_events: 스트레스 이벤트 리스트 (None이면 자동 생성)
        
        Returns:
            시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🔬 우울증 에너지 고갈 메커니즘 시뮬레이션")
        print(f"{'='*70}")
        print(f"지속 시간: {duration}초")
        print(f"목적: 에너지 고갈 메커니즘 탐색")
        print(f"{'='*70}\n")
        
        self.start_time = time.time()
        dt = 0.1
        steps = int(duration / dt)
        
        # 스트레스 이벤트 생성 (없으면 자동 생성)
        if stress_events is None:
            stress_events = self._generate_stress_events(duration, dt)
        
        # 시뮬레이션 루프
        for step in range(steps):
            t = step * dt
            
            # 현재 시점의 스트레스 이벤트 찾기
            current_stress = [e for e in stress_events
                            if e['start_time'] <= t <= e['end_time']]
            
            # 인지 부하 계산
            cognitive_load = sum(e.get('cognitive_load', 0.5) for e in current_stress)
            cognitive_load = min(1.0, cognitive_load)
            
            # 스트레스 수준 계산
            stress_level = sum(e.get('stress_intensity', 0.5) for e in current_stress)
            stress_level = min(1.0, stress_level)
            
            # 에너지 업데이트
            energy_result = self.depression_engines['energy_depletion'].update_energy(
                cognitive_load=cognitive_load,
                stress_level=stress_level,
                dt=dt
            )
            
            # 데이터 기록
            self.simulation_data['timestamps'].append(t)
            self.simulation_data['energy_scores'].append(
                self.depression_engines['energy_depletion'].get_energy_score()
            )
            
            # Brain Engine에 에너지 상태 전달
            brain_input = BrainInput(
                sensory={
                    'energy_state': {
                        'current_energy': energy_result['current_energy'],
                        'depletion_rate': energy_result['depletion_rate']
                    }
                }
            )
            self.brain.process(brain_input)
        
        # 결과 분석
        results = self._analyze_energy_depletion_patterns()
        
        print(f"\n✅ 에너지 고갈 메커니즘 시뮬레이션 완료!")
        print(f"   관측된 패턴: {results['pattern_type']}")
        print(f"   에너지 점수: {results['energy_score']:.3f}")
        
        return results
    
    def simulate_motivation_task(self,
                                duration: float = 60.0,
                                reward_opportunities: Optional[List[Dict]] = None) -> Dict:
        """
        동기 감소 테스트 시뮬레이션
        
        핵심 질문: "왜 동기가 사라지는가?"
        
        Args:
            duration: 시뮬레이션 지속 시간 (초)
            reward_opportunities: 보상 기회 리스트 (None이면 자동 생성)
        
        Returns:
            시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🔬 우울증 동기 감소 메커니즘 시뮬레이션")
        print(f"{'='*70}")
        print(f"지속 시간: {duration}초")
        print(f"목적: 동기 감소 메커니즘 탐색")
        print(f"{'='*70}\n")
        
        self.start_time = time.time()
        dt = 0.1
        steps = int(duration / dt)
        
        # 보상 기회 생성 (없으면 자동 생성)
        if reward_opportunities is None:
            reward_opportunities = self._generate_reward_opportunities(duration, dt)
        
        # 시뮬레이션 루프
        for step in range(steps):
            t = step * dt
            
            # 현재 시점의 보상 기회 찾기
            current_rewards = [r for r in reward_opportunities
                             if r['start_time'] <= t <= r['end_time']]
            
            for reward in current_rewards:
                # 보상 처리
                reward_result = self.depression_engines['motivation'].process_reward(
                    reward_value=reward.get('value', 0.5),
                    effort_required=reward.get('effort', 0.5)
                )
                
                # 행동 평가
                action_result = self.depression_engines['motivation'].evaluate_action(
                    expected_reward=reward.get('value', 0.5),
                    effort_required=reward.get('effort', 0.5),
                    delay=reward.get('delay', 0.0)
                )
                
                # 데이터 기록
                self.simulation_data['timestamps'].append(t)
                self.simulation_data['motivation_scores'].append(
                    self.depression_engines['motivation'].get_motivation_score()
                )
                
                # Brain Engine에 동기 상태 전달
                brain_input = BrainInput(
                    sensory={
                        'motivation_state': {
                            'motivation_level': self.depression_engines['motivation'].state.motivation_level,
                            'should_act': action_result['should_act']
                        }
                    }
                )
                self.brain.process(brain_input)
        
        # 결과 분석
        results = self._analyze_motivation_patterns()
        
        print(f"\n✅ 동기 감소 메커니즘 시뮬레이션 완료!")
        print(f"   관측된 패턴: {results['pattern_type']}")
        print(f"   동기 점수: {results['motivation_score']:.3f}")
        
        return results
    
    def simulate_full_depression_assessment(self,
                                           duration: float = 300.0) -> Dict:
        """
        전체 우울증 메커니즘 시뮬레이션
        
        모든 메커니즘을 통합하여 우울증 패턴 관측
        
        Args:
            duration: 시뮬레이션 지속 시간 (초)
        
        Returns:
            통합 시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🔬 우울증 통합 메커니즘 시뮬레이션")
        print(f"{'='*70}")
        print(f"지속 시간: {duration}초")
        print(f"목적: 우울증 패턴의 종합적 관측 및 메커니즘 분석")
        print(f"{'='*70}\n")
        
        # 데이터 초기화
        self.simulation_data = {
            'timestamps': [],
            'negative_bias_scores': [],
            'cognitive_control_scores': [],
            'energy_scores': [],
            'motivation_scores': [],
            'brain_states': [],
            'stimulus_events': [],
            'pattern_observations': []
        }
        
        self.start_time = time.time()
        dt = 0.1
        steps = int(duration / dt)
        
        # 통합 시뮬레이션 루프
        for step in range(steps):
            t = step * dt
            
            # 각 엔진 업데이트
            # 1. 부정적 편향 (자극 처리)
            if step % 10 == 0:  # 1초마다 자극
                stimulus = self._generate_random_stimulus()
                bias_result = self.depression_engines['negative_bias'].process_stimulus(
                    stimulus_valence=stimulus['valence'],
                    stimulus_intensity=stimulus['intensity'],
                    time_elapsed=t
                )
            
            # 2. 인지 제어 (부정적 사고 처리)
            if step % 20 == 0:  # 2초마다 부정적 사고
                thought_rng = self.rng.get_rng('thought')
                thought_result = self.depression_engines['cognitive_control'].process_negative_thought(
                    thought_intensity=0.3 + thought_rng.random() * 0.4,
                    time_elapsed=t
                )
            
            # 3. 에너지 고갈
            energy_rng = self.rng.get_rng('energy')
            energy_result = self.depression_engines['energy_depletion'].update_energy(
                cognitive_load=0.3 + energy_rng.random() * 0.4,
                stress_level=0.2 + energy_rng.random() * 0.3,
                dt=dt
            )
            
            # 4. 동기 (보상 기회 평가)
            if step % 30 == 0:  # 3초마다 보상 기회
                reward = self._generate_random_reward()
                motivation_result = self.depression_engines['motivation'].process_reward(
                    reward_value=reward['value'],
                    effort_required=reward['effort']
                )
            
            # 상태 업데이트
            self.depression_engines['negative_bias'].update_rumination(dt)
            self.depression_engines['cognitive_control'].update_negative_loop(dt)
            
            # 데이터 기록
            if step % 10 == 0:  # 1초마다 기록
                self.simulation_data['timestamps'].append(t)
                self.simulation_data['negative_bias_scores'].append(
                    self.depression_engines['negative_bias'].get_bias_score()
                )
                self.simulation_data['cognitive_control_scores'].append(
                    self.depression_engines['cognitive_control'].get_control_score()
                )
                self.simulation_data['energy_scores'].append(
                    self.depression_engines['energy_depletion'].get_energy_score()
                )
                self.simulation_data['motivation_scores'].append(
                    self.depression_engines['motivation'].get_motivation_score()
                )
        
        # 통합 결과 분석
        results = self._analyze_integrated_patterns()
        
        print(f"\n✅ 통합 우울증 메커니즘 시뮬레이션 완료!")
        print(f"\n📊 관측된 패턴 요약:")
        print(f"   부정적 편향: {results['negative_bias_score']:.3f}")
        print(f"   인지 제어: {results['cognitive_control_score']:.3f}")
        print(f"   에너지: {results['energy_score']:.3f}")
        print(f"   동기: {results['motivation_score']:.3f}")
        print(f"\n   종합 패턴: {results['overall_pattern']}")
        
        return results
    
    # ======================================================================
    # 헬퍼 메서드
    # ======================================================================
    
    def _generate_stimulus_sequence(self, duration: float, dt: float) -> List[Dict]:
        """자극 시퀀스 생성"""
        stimuli = []
        num_stimuli = int(duration / 5.0)  # 5초마다 자극
        
        rng = self.rng.get_rng('stimulus_sequence')
        for i in range(num_stimuli):
            start_time = i * 5.0
            end_time = start_time + 1.0
            
            # 부정적/긍정적/중립 자극 랜덤 생성
            valence = rng.choice([-0.8, -0.4, 0.0, 0.4, 0.8], 
                                p=[0.3, 0.2, 0.2, 0.15, 0.15])
            intensity = 0.5 + rng.random() * 0.5
            
            stimuli.append({
                'start_time': start_time,
                'end_time': end_time,
                'valence': valence,
                'intensity': intensity
            })
        
        return stimuli
    
    def _generate_cognitive_tasks(self, duration: float, dt: float) -> List[Dict]:
        """인지 작업 생성"""
        tasks = []
        num_tasks = int(duration / 10.0)  # 10초마다 작업
        
        for i in range(num_tasks):
            start_time = i * 10.0
            end_time = start_time + 2.0
            
            # 부정적 사고 또는 인지 제어 작업
            rng = self.rng.get_rng('cognitive_tasks')
            if rng.random() < 0.5:
                tasks.append({
                    'start_time': start_time,
                    'end_time': end_time,
                    'negative_thought': True,
                    'thought_intensity': 0.3 + rng.random() * 0.5
                })
            else:
                tasks.append({
                    'start_time': start_time,
                    'end_time': end_time,
                    'requires_control': True,
                    'difficulty': 0.3 + rng.random() * 0.5
                })
        
        return tasks
    
    def _generate_stress_events(self, duration: float, dt: float) -> List[Dict]:
        """스트레스 이벤트 생성"""
        events = []
        num_events = int(duration / 15.0)  # 15초마다 이벤트
        
        for i in range(num_events):
            start_time = i * 15.0
            end_time = start_time + 3.0
            
            rng = self.rng.get_rng('stress_events')
            events.append({
                'start_time': start_time,
                'end_time': end_time,
                'stress_intensity': 0.3 + rng.random() * 0.5,
                'cognitive_load': 0.2 + rng.random() * 0.4
            })
        
        return events
    
    def _generate_reward_opportunities(self, duration: float, dt: float) -> List[Dict]:
        """보상 기회 생성"""
        opportunities = []
        num_opportunities = int(duration / 8.0)  # 8초마다 기회
        
        for i in range(num_opportunities):
            start_time = i * 8.0
            end_time = start_time + 1.0
            
            rng = self.rng.get_rng('reward_opportunities')
            opportunities.append({
                'start_time': start_time,
                'end_time': end_time,
                'value': 0.3 + rng.random() * 0.5,
                'effort': 0.2 + rng.random() * 0.6,
                'delay': rng.random() * 2.0
            })
        
        return opportunities
    
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
    
    # ======================================================================
    # 분석 메서드
    # ======================================================================
    
    def _analyze_negative_bias_patterns(self) -> Dict:
        """부정적 편향 패턴 분석"""
        if not self.simulation_data['negative_bias_scores']:
            return {'pattern_type': 'insufficient_data', 'bias_score': 0.0}
        
        scores = np.array(self.simulation_data['negative_bias_scores'])
        mean_score = float(np.mean(scores))
        std_score = float(np.std(scores))
        
        # 패턴 분류
        if mean_score > 0.7:
            pattern_type = 'strong_negative_bias'
        elif mean_score > 0.4:
            pattern_type = 'moderate_negative_bias'
        else:
            pattern_type = 'mild_negative_bias'
        
        return {
            'pattern_type': pattern_type,
            'bias_score': mean_score,
            'bias_std': std_score,
            'mechanism': 'negative_amplification_and_positive_dampening'
        }
    
    def _analyze_cognitive_control_patterns(self) -> Dict:
        """인지 제어 패턴 분석"""
        if not self.simulation_data['cognitive_control_scores']:
            return {'pattern_type': 'insufficient_data', 'control_score': 0.0}
        
        scores = np.array(self.simulation_data['cognitive_control_scores'])
        mean_score = float(np.mean(scores))
        std_score = float(np.std(scores))
        
        # 패턴 분류
        if mean_score < 0.4:
            pattern_type = 'severe_control_impairment'
        elif mean_score < 0.6:
            pattern_type = 'moderate_control_impairment'
        else:
            pattern_type = 'mild_control_impairment'
        
        return {
            'pattern_type': pattern_type,
            'control_score': mean_score,
            'control_std': std_score,
            'mechanism': 'inhibition_failure_and_negative_loop'
        }
    
    def _analyze_energy_depletion_patterns(self) -> Dict:
        """에너지 고갈 패턴 분석"""
        if not self.simulation_data['energy_scores']:
            return {'pattern_type': 'insufficient_data', 'energy_score': 0.0}
        
        scores = np.array(self.simulation_data['energy_scores'])
        mean_score = float(np.mean(scores))
        std_score = float(np.std(scores))
        
        # 패턴 분류
        if mean_score < 0.3:
            pattern_type = 'severe_energy_depletion'
        elif mean_score < 0.5:
            pattern_type = 'moderate_energy_depletion'
        else:
            pattern_type = 'mild_energy_depletion'
        
        return {
            'pattern_type': pattern_type,
            'energy_score': mean_score,
            'energy_std': std_score,
            'mechanism': 'increased_consumption_and_reduced_recovery'
        }
    
    def _analyze_motivation_patterns(self) -> Dict:
        """동기 패턴 분석"""
        if not self.simulation_data['motivation_scores']:
            return {'pattern_type': 'insufficient_data', 'motivation_score': 0.0}
        
        scores = np.array(self.simulation_data['motivation_scores'])
        mean_score = float(np.mean(scores))
        std_score = float(np.std(scores))
        
        # 패턴 분류
        if mean_score < 0.3:
            pattern_type = 'severe_motivation_deficit'
        elif mean_score < 0.5:
            pattern_type = 'moderate_motivation_deficit'
        else:
            pattern_type = 'mild_motivation_deficit'
        
        return {
            'pattern_type': pattern_type,
            'motivation_score': mean_score,
            'motivation_std': std_score,
            'mechanism': 'reduced_reward_sensitivity_and_anhedonia'
        }
    
    def _analyze_integrated_patterns(self) -> Dict:
        """통합 패턴 분석"""
        bias_result = self._analyze_negative_bias_patterns()
        control_result = self._analyze_cognitive_control_patterns()
        energy_result = self._analyze_energy_depletion_patterns()
        motivation_result = self._analyze_motivation_patterns()
        
        # 종합 패턴 판단
        scores = [
            bias_result.get('bias_score', 0.0),
            1.0 - control_result.get('control_score', 1.0),  # 역변환
            1.0 - energy_result.get('energy_score', 1.0),   # 역변환
            1.0 - motivation_result.get('motivation_score', 1.0)  # 역변환
        ]
        mean_depression_score = np.mean(scores)
        
        if mean_depression_score > 0.7:
            overall_pattern = 'severe_depression_like_pattern'
        elif mean_depression_score > 0.5:
            overall_pattern = 'moderate_depression_like_pattern'
        elif mean_depression_score > 0.3:
            overall_pattern = 'mild_depression_like_pattern'
        else:
            overall_pattern = 'minimal_depression_like_pattern'
        
        return {
            'overall_pattern': overall_pattern,
            'mean_depression_score': float(mean_depression_score),
            'negative_bias_score': bias_result.get('bias_score', 0.0),
            'cognitive_control_score': control_result.get('control_score', 0.0),
            'energy_score': energy_result.get('energy_score', 0.0),
            'motivation_score': motivation_result.get('motivation_score', 0.0),
            'mechanisms': {
                'negative_bias': bias_result.get('mechanism', ''),
                'cognitive_control': control_result.get('mechanism', ''),
                'energy': energy_result.get('mechanism', ''),
                'motivation': motivation_result.get('mechanism', '')
            }
        }
    
    def visualize_results(self, output_path: Optional[str] = None):
        """결과 시각화"""
        if not self.simulation_data['timestamps']:
            print("⚠️ 시각화할 데이터가 없습니다.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('우울증 메커니즘 시뮬레이션 결과\n(패턴 관측 및 원인 분석)', 
                     fontsize=16, fontweight='bold')
        
        timestamps = np.array(self.simulation_data['timestamps'])
        
        # 1. 부정적 편향
        if self.simulation_data['negative_bias_scores']:
            ax1 = axes[0, 0]
            ax1.plot(timestamps, self.simulation_data['negative_bias_scores'], 
                     'r-', linewidth=2, label='부정적 편향 점수')
            ax1.set_xlabel('시간 (초)')
            ax1.set_ylabel('편향 점수')
            ax1.set_title('부정적 편향 메커니즘')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
        
        # 2. 인지 제어
        if self.simulation_data['cognitive_control_scores']:
            ax2 = axes[0, 1]
            ax2.plot(timestamps, self.simulation_data['cognitive_control_scores'],
                     'b-', linewidth=2, label='인지 제어 점수')
            ax2.set_xlabel('시간 (초)')
            ax2.set_ylabel('제어 점수')
            ax2.set_title('인지 제어 약화 메커니즘')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
        
        # 3. 에너지
        if self.simulation_data['energy_scores']:
            ax3 = axes[1, 0]
            ax3.plot(timestamps, self.simulation_data['energy_scores'],
                     'g-', linewidth=2, label='에너지 점수')
            ax3.set_xlabel('시간 (초)')
            ax3.set_ylabel('에너지 점수')
            ax3.set_title('에너지 고갈 메커니즘')
            ax3.grid(True, alpha=0.3)
            ax3.legend()
        
        # 4. 동기
        if self.simulation_data['motivation_scores']:
            ax4 = axes[1, 1]
            ax4.plot(timestamps, self.simulation_data['motivation_scores'],
                     'm-', linewidth=2, label='동기 점수')
            ax4.set_xlabel('시간 (초)')
            ax4.set_ylabel('동기 점수')
            ax4.set_title('동기 감소 메커니즘')
            ax4.grid(True, alpha=0.3)
            ax4.legend()
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            print(f"\n💾 시각화 저장: {output_path}")
        else:
            plt.savefig('depression_simulation_results.png', dpi=150, bbox_inches='tight')
            print(f"\n💾 시각화 저장: depression_simulation_results.png")
        
        plt.close()


def main():
    """메인 실행 함수"""
    print("\n" + "="*70)
    print("🔬 우울증 메커니즘 시뮬레이터")
    print("="*70)
    print("목적: 우울증 패턴의 원인 분석 및 메커니즘 탐색")
    print("⚠️  주의: 이 시뮬레이터는 치료 도구가 아닙니다.")
    print("="*70 + "\n")
    
    # 시뮬레이터 생성
    simulator = DepressionSimulator(
        seed=42,
        negative_bias_strength=0.6,
        control_impairment=0.5,
        energy_depletion_rate=0.5,
        motivation_deficit=0.6
    )
    
    # 통합 시뮬레이션 실행
    results = simulator.simulate_full_depression_assessment(duration=300.0)
    
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
    main()

