"""
부정적 편향 엔진 (공통)

우울증과 불안장애에서 공통으로 사용되는 부정적 편향 메커니즘
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class NegativeBiasState:
    """부정적 편향 상태"""
    negative_amplification: float = 1.0  # 부정적 자극 증폭 배수
    positive_dampening: float = 1.0      # 긍정적 자극 감쇠 배수
    threat_sensitivity: float = 1.0       # 위협 민감도
    memory_bias: float = 0.0             # 부정적 기억 편향
    rumination_strength: float = 0.0     # 반추 강도


class NegativeBiasEngine:
    """
    부정적 편향 엔진 (Amygdala 기반)
    
    핵심 질문: "왜 부정적 편향이 발생하는가?"
    
    메커니즘:
    1. 부정적 자극에 대한 과민 반응
    2. 긍정적 자극에 대한 둔감 반응
    3. 위협 감지 과민화
    4. 부정적 기억 편향
    5. 반추 (rumination) 강화
    """
    
    def __init__(self, 
                 negative_bias_strength: float = 0.0,
                 rng: Optional[np.random.Generator] = None):
        """
        부정적 편향 엔진 초기화
        
        Args:
            negative_bias_strength: 부정적 편향 강도 (0.0 ~ 1.0)
            rng: 난수 생성기
        """
        self.negative_bias_strength = np.clip(negative_bias_strength, 0.0, 1.0)
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 상태 초기화
        self.state = NegativeBiasState()
        
        # 파라미터
        self.negative_amplification_base = 1.0
        self.positive_dampening_base = 1.0
        self.threat_threshold_base = 0.5
        
        # 동역학 파라미터
        self.rumination_decay = 0.95  # 반추 감쇠율
        self.memory_bias_decay = 0.98  # 기억 편향 감쇠율
        
        # 초기 상태 설정
        self._update_state_from_strength()
    
    def _update_state_from_strength(self):
        """편향 강도에 따라 상태 업데이트"""
        strength = self.negative_bias_strength
        
        # 부정적 자극 증폭 (1.0 ~ 2.5)
        self.state.negative_amplification = 1.0 + (strength * 1.5)
        
        # 긍정적 자극 감쇠 (1.0 ~ 0.3)
        self.state.positive_dampening = 1.0 - (strength * 0.7)
        
        # 위협 민감도 증가 (1.0 ~ 2.0)
        self.state.threat_sensitivity = 1.0 + (strength * 1.0)
        
        # 기억 편향 (0.0 ~ 0.8)
        self.state.memory_bias = strength * 0.8
    
    def process_stimulus(self, 
                        stimulus_valence: float,
                        stimulus_intensity: float = 1.0,
                        time_elapsed: float = 0.0) -> Dict:
        """
        자극 처리 (부정적 편향 적용)
        
        Args:
            stimulus_valence: 자극의 정서가 (-1.0: 매우 부정적, 0.0: 중립, 1.0: 매우 긍정적)
            stimulus_intensity: 자극 강도
            time_elapsed: 경과 시간
        
        Returns:
            처리된 자극 정보
        """
        # 변수 초기화
        amplified_intensity = stimulus_intensity
        dampened_intensity = stimulus_intensity
        perceived_valence = stimulus_valence
        
        # 부정적 자극 처리
        if stimulus_valence < 0:
            # 부정적 자극 증폭
            amplified_intensity = stimulus_intensity * self.state.negative_amplification
            perceived_valence = stimulus_valence * self.state.negative_amplification
            
            # 반추 강화 (부정적 자극에 대한 반복적 사고)
            self.state.rumination_strength = min(1.0, 
                self.state.rumination_strength + 0.1 * amplified_intensity)
            
            # 기억 편향 업데이트
            self.state.memory_bias = min(1.0,
                self.state.memory_bias + 0.05 * amplified_intensity)
        
        # 긍정적 자극 처리
        elif stimulus_valence > 0:
            # 긍정적 자극 감쇠
            dampened_intensity = stimulus_intensity * self.state.positive_dampening
            perceived_valence = stimulus_valence * self.state.positive_dampening
            
            # 반추 약화 (긍정적 자극은 빠르게 사라짐)
            self.state.rumination_strength *= self.rumination_decay
        
        # 중립 자극 처리
        else:
            # 중립 자극도 약간 부정적으로 해석될 수 있음
            if self.state.rumination_strength > 0.3:
                perceived_valence = -0.1 * self.state.rumination_strength
                dampened_intensity = stimulus_intensity
                amplified_intensity = stimulus_intensity
            else:
                perceived_valence = 0.0
                dampened_intensity = stimulus_intensity
                amplified_intensity = stimulus_intensity
        
        # 위협 감지 (부정적 자극에 대한 과민 반응)
        threat_detected = False
        if stimulus_valence < -0.3:
            threat_probability = (abs(stimulus_valence) * 
                               self.state.threat_sensitivity * 
                               stimulus_intensity)
            if threat_probability > self.threat_threshold_base:
                threat_detected = True
        
        # 최종 강도 결정
        if stimulus_valence < 0:
            final_intensity = amplified_intensity
        elif stimulus_valence > 0:
            final_intensity = dampened_intensity
        else:
            final_intensity = stimulus_intensity
        
        return {
            'perceived_valence': np.clip(perceived_valence, -1.0, 1.0),
            'perceived_intensity': final_intensity,
            'threat_detected': threat_detected,
            'rumination_triggered': stimulus_valence < 0,
            'bias_applied': True
        }
    
    def update_rumination(self, dt: float = 0.1):
        """
        반추 업데이트 (시간에 따른 자연적 감쇠)
        
        Args:
            dt: 시간 간격
        """
        # 반추는 시간이 지나면서 점차 감쇠하지만, 완전히 사라지지 않음
        self.state.rumination_strength *= (self.rumination_decay ** (dt * 10))
        
        # 기억 편향도 점차 감쇠
        self.state.memory_bias *= (self.memory_bias_decay ** (dt * 10))
    
    def get_bias_score(self) -> float:
        """
        부정적 편향 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            편향 점수 (높을수록 부정적 편향 강함)
        """
        score = (
            (self.state.negative_amplification - 1.0) / 1.5 * 0.3 +
            (1.0 - self.state.positive_dampening) / 0.7 * 0.3 +
            (self.state.threat_sensitivity - 1.0) / 1.0 * 0.2 +
            self.state.rumination_strength * 0.1 +
            self.state.memory_bias * 0.1
        )
        return np.clip(score, 0.0, 1.0)

