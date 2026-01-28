"""
PTSD 시뮬레이터 (독립 클래스)

Cookiie Brain Engine을 사용한 PTSD 메커니즘 시뮬레이션
목적: "왜 이런 상황이 발생할 수 있는가?" 원인 분석

⚠️ 주의: 이 시뮬레이터는 치료 도구가 아닙니다.
- 진단 도구 아님
- 치료 솔루션 제시 아님
- 패턴 관측 및 메커니즘 분석 목적

핵심 정체성: "PTSD 메커니즘 엔진"
- 외상 기억 침입 → 회피 → 과각성 → 부정적 인지 변화
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

# PTSD 특화 엔진
from .ptsd_engines import (
    IntrusiveMemoryEngine,
    AvoidanceEngine,
    HyperarousalEngine,
    NegativeCognitionEngine
)

# 유틸리티
from ...utils.reproducibility import ReproducibleRNG, ExperimentMetadata
from ...utils.statistics import StatisticalValidator
from ...utils.report_generator import ReportGenerator


class PTSDSimulator:
    """
    PTSD 시뮬레이터 (독립 클래스)
    
    Cookiie Brain Engine과 PTSD 특화 엔진을 통합한 시뮬레이션 시스템
    목적: PTSD 메커니즘의 원인 분석 및 패턴 관측
    
    핵심 특징:
    - 외상 기억 침입
    - 회피 패턴 강화
    - 과각성 상태
    - 부정적 인지 변화
    - Cookiie Brain Engine과 실시간 동적 연결
    """
    
    def __init__(self, 
                 config: Optional[CookiieBrainConfig] = None,
                 seed: Optional[int] = None,
                 trauma_intensity: float = 0.8,
                 suppression_failure: float = 0.6,
                 avoidance_strength: float = 0.7,
                 hyperarousal_level: float = 0.7,
                 negative_bias_strength: float = 0.6):
        """
        PTSD 시뮬레이터 초기화
        
        Args:
            config: Cookiie Brain Engine 설정
            seed: 재현성을 위한 시드 값
            trauma_intensity: 외상 강도 (0.0 ~ 1.0)
            suppression_failure: 억제 실패율 (0.0 ~ 1.0)
            avoidance_strength: 회피 강도 (0.0 ~ 1.0)
            hyperarousal_level: 과각성 수준 (0.0 ~ 1.0)
            negative_bias_strength: 부정적 편향 강도 (0.0 ~ 1.0)
        """
        # 재현성 시스템 초기화
        self.rng = ReproducibleRNG(seed=seed)
        self.seed = self.rng.seed
        
        # PTSD 특성 파라미터
        self.trauma_intensity = np.clip(trauma_intensity, 0.0, 1.0)
        self.suppression_failure = np.clip(suppression_failure, 0.0, 1.0)
        self.avoidance_strength = np.clip(avoidance_strength, 0.0, 1.0)
        self.hyperarousal_level = np.clip(hyperarousal_level, 0.0, 1.0)
        self.negative_bias_strength = np.clip(negative_bias_strength, 0.0, 1.0)
        
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
        
        # PTSD 엔진 초기화
        self.common_engines = {}
        self.disorder_engines = {}
        
        # 공통 엔진
        self.common_engines['negative_bias'] = NegativeBiasEngine(
            negative_bias_strength=self.negative_bias_strength,
            rng=self.rng.get_rng('negative_bias')
        )
        
        self.common_engines['cognitive_control'] = CognitiveControlEngine(
            control_impairment=self.suppression_failure,
            rng=self.rng.get_rng('cognitive_control')
        )
        
        # PTSD 특화 엔진
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
            initial_intensity=self.trauma_intensity,
            initial_fear=self.trauma_intensity * 0.9
        )
        
        # 억제 실패율 설정
        self.disorder_engines['intrusive_memory'].suppression_failure_rate = self.suppression_failure
        
        # 시뮬레이션 데이터
        self.simulation_data = {
            'timestamps': [],
            'intrusion_scores': [],
            'avoidance_scores': [],
            'arousal_scores': [],
            'negative_cognition_scores': [],
            'brain_states': [],
            'pattern_observations': []
        }
        
        # 통계적 검증 시스템
        self.statistical_validator = StatisticalValidator()
        
        # 리포트 생성기
        self.report_generator = ReportGenerator()
        
        # 시뮬레이션 시작 시간
        self.start_time = None
    
    def simulate_full_ptsd_assessment(self,
                                     duration: float = 300.0,
                                     enable_brain_integration: bool = True) -> Dict:
        """
        PTSD 전체 평가 시뮬레이션
        
        Args:
            duration: 시뮬레이션 지속 시간 (초)
            enable_brain_integration: Cookiie Brain Engine 통합 활성화
        
        Returns:
            시뮬레이션 결과
        """
        print(f"\n{'='*70}")
        print(f"🔬 PTSD 메커니즘 시뮬레이션")
        print(f"{'='*70}")
        print(f"목적: PTSD 패턴의 원인 분석")
        print(f"지속 시간: {duration}초")
        print(f"외상 강도: {self.trauma_intensity:.1f}")
        print(f"억제 실패율: {self.suppression_failure:.1f}")
        print(f"{'='*70}\n")
        
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
            # 1. 외상 기억 침입 처리
            # ============================================================
            if step % 50 == 0:  # 5초마다
                # Amygdala 각성 수준 가져오기
                amygdala_arousal = self._get_amygdala_arousal()
                
                # PFC 제어 능력 가져오기
                pfc_control = 1.0 - self.common_engines['cognitive_control'].control_impairment
                
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
            
            # ============================================================
            # 2. 회피 패턴 업데이트
            # ============================================================
            if step % 30 == 0:  # 3초마다
                avoidance_level = self.disorder_engines['avoidance'].compute_avoidance_level()
            
            # ============================================================
            # 3. 과각성 업데이트
            # ============================================================
            stress_level = self._compute_stress_level()
            threat_detected = self._check_threat_detection()
            thalamus_filtering = self._get_thalamus_filtering()
            
            arousal = self.disorder_engines['hyperarousal'].update_arousal(
                stress_level=stress_level,
                threat_detected=threat_detected,
                thalamus_filtering=thalamus_filtering
            )
            
            # ============================================================
            # 4. 부정적 인지 변화 업데이트
            # ============================================================
            if step % 100 == 0:  # 10초마다
                # 침입 발생 시 부정적 신념 강화
                intrusion = self.disorder_engines['intrusive_memory'].current_intrusion_level
                if intrusion > 0.3:
                    self.disorder_engines['negative_cognition'].strengthen_negative_belief(
                        'self_blame', evidence=intrusion * 0.5
                    )
                    self.disorder_engines['negative_cognition'].strengthen_negative_belief(
                        'guilt', evidence=intrusion * 0.4
                    )
                
                negative_bias = self.disorder_engines['negative_cognition'].compute_negative_bias()
            
            # ============================================================
            # 5. Cookiie Brain Engine 통합
            # ============================================================
            if enable_brain_integration and self.brain:
                # 뇌 상태 가져오기
                brain_state = self._get_brain_state()
                
                # 뇌 상태를 엔진에 피드백
                self._update_engines_from_brain(brain_state)
            
            # ============================================================
            # 6. 데이터 수집
            # ============================================================
            if step % 10 == 0:  # 1초마다
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
                
                if enable_brain_integration and self.brain:
                    self.simulation_data['brain_states'].append(self._get_brain_state())
        
        # 최종 결과 계산
        results = self._compute_final_results()
        
        # 패턴 관측
        patterns = self._analyze_patterns()
        results['pattern_observations'] = patterns
        
        # 시뮬레이션 완료
        elapsed_time = time.time() - self.start_time
        print(f"\n✅ 시뮬레이션 완료 (소요 시간: {elapsed_time:.2f}초)")
        print(f"\n📊 최종 결과:")
        print(f"   침입 수준: {results['final_intrusion']:.3f}")
        print(f"   회피 수준: {results['final_avoidance']:.3f}")
        print(f"   과각성 수준: {results['final_arousal']:.3f}")
        print(f"   부정적 인지: {results['final_negative_cognition']:.3f}")
        
        return results
    
    def _get_amygdala_arousal(self) -> float:
        """Amygdala 각성 수준 가져오기"""
        if self.brain:
            brain_state = self._get_brain_state()
            # Amygdala 활성화 수준 추정
            return brain_state.get('amygdala_activation', 0.5)
        return 0.5
    
    def _get_thalamus_filtering(self) -> float:
        """Thalamus 필터링 능력 가져오기"""
        if self.brain:
            brain_state = self._get_brain_state()
            # Thalamus 필터링 능력 추정
            return brain_state.get('thalamus_filtering', 0.5)
        return 0.5
    
    def _compute_stress_level(self) -> float:
        """스트레스 수준 계산"""
        intrusion = self.disorder_engines['intrusive_memory'].current_intrusion_level
        arousal = self.disorder_engines['hyperarousal'].current_arousal
        return np.clip((intrusion + arousal) / 2.0, 0.0, 1.0)
    
    def _check_threat_detection(self) -> bool:
        """위협 감지 확인"""
        # 침입이 높거나 각성이 높으면 위협으로 인식
        intrusion = self.disorder_engines['intrusive_memory'].current_intrusion_level
        arousal = self.disorder_engines['hyperarousal'].current_arousal
        return (intrusion > 0.4) or (arousal > 0.6)
    
    def _create_brain_input(self, intrusion: float, arousal: float, avoidance: float):
        """Cookiie Brain Engine 입력 생성"""
        if not COOKIIE_BRAIN_AVAILABLE:
            return None
        
        # PTSD 특성 반영
        # BrainInput은 실제 Cookiie Brain Engine의 구조에 맞게 조정 필요
        # 현재는 기본 모드로 실행 (BrainInput 없이)
        return None
    
    def _get_brain_state(self) -> Dict:
        """Cookiie Brain Engine 상태 가져오기"""
        if not self.brain:
            return {}
        
        try:
            state = self.brain.get_state()
            return {
                'amygdala_activation': getattr(state, 'amygdala_activation', 0.5),
                'pfc_control': getattr(state, 'pfc_control', 0.5),
                'thalamus_filtering': getattr(state, 'thalamus_filtering', 0.5),
                'hypothalamus_arousal': getattr(state, 'hypothalamus_arousal', 0.5)
            }
        except:
            return {
                'amygdala_activation': 0.5,
                'pfc_control': 0.5,
                'thalamus_filtering': 0.5,
                'hypothalamus_arousal': 0.5
            }
    
    def _update_engines_from_brain(self, brain_state: Dict):
        """뇌 상태를 엔진에 피드백"""
        # Amygdala 각성 → 침입 엔진 업데이트
        amygdala_arousal = brain_state.get('amygdala_activation', 0.5)
        pfc_control = brain_state.get('pfc_control', 0.5)
        
        self.disorder_engines['intrusive_memory'].update(
            dt=0.1,
            amygdala_arousal=amygdala_arousal,
            pfc_control=pfc_control
        )
    
    def _compute_final_results(self) -> Dict:
        """최종 결과 계산"""
        return {
            'final_intrusion': np.mean(self.simulation_data['intrusion_scores'][-100:]) if self.simulation_data['intrusion_scores'] else 0.0,
            'final_avoidance': np.mean(self.simulation_data['avoidance_scores'][-100:]) if self.simulation_data['avoidance_scores'] else 0.0,
            'final_arousal': np.mean(self.simulation_data['arousal_scores'][-100:]) if self.simulation_data['arousal_scores'] else 0.0,
            'final_negative_cognition': np.mean(self.simulation_data['negative_cognition_scores'][-100:]) if self.simulation_data['negative_cognition_scores'] else 0.0,
            'intrusion_scores': self.simulation_data['intrusion_scores'],
            'avoidance_scores': self.simulation_data['avoidance_scores'],
            'arousal_scores': self.simulation_data['arousal_scores'],
            'negative_cognition_scores': self.simulation_data['negative_cognition_scores'],
            'timestamps': self.simulation_data['timestamps'],
            'brain_states': self.simulation_data['brain_states']
        }
    
    def _analyze_patterns(self) -> Dict:
        """패턴 분석"""
        patterns = {
            'intrusion_pattern': 'high' if np.mean(self.simulation_data['intrusion_scores']) > 0.5 else 'moderate',
            'avoidance_pattern': 'high' if np.mean(self.simulation_data['avoidance_scores']) > 0.5 else 'moderate',
            'hyperarousal_pattern': 'high' if np.mean(self.simulation_data['arousal_scores']) > 0.7 else 'moderate',
            'ptsd_likelihood': 'high' if (
                np.mean(self.simulation_data['intrusion_scores']) > 0.5 and
                np.mean(self.simulation_data['avoidance_scores']) > 0.4 and
                np.mean(self.simulation_data['arousal_scores']) > 0.6
            ) else 'moderate'
        }
        return patterns


def main():
    """메인 실행 함수"""
    print("=" * 70)
    print("🧠 PTSD 시뮬레이터")
    print("=" * 70)
    
    # 시뮬레이터 생성
    simulator = PTSDSimulator(
        seed=42,
        trauma_intensity=0.8,
        suppression_failure=0.6,
        avoidance_strength=0.7,
        hyperarousal_level=0.7
    )
    
    # 시뮬레이션 실행
    results = simulator.simulate_full_ptsd_assessment(duration=300.0)
    
    print("\n" + "=" * 70)
    print("✅ 시뮬레이션 완료")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    main()

