"""
부정적 편향 엔진 (공통)

우울증과 불안장애에서 공통으로 사용되는 부정적 편향 메커니즘

⚠️ 리팩터링: 이 엔진은 내부적으로 NegativeBiasLoop를 사용합니다.
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass

# 루프 라이브러리 import
from .loops.negative_bias_loop import NegativeBiasLoop


@dataclass
class NegativeBiasState:
    """부정적 편향 상태 (호환성 유지)"""
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
        
        # 루프 라이브러리 사용
        self.loop = NegativeBiasLoop(
            initial_bias_strength=negative_bias_strength,
            rng=rng
        )
        
        # 상태 초기화 (호환성 유지)
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
        """편향 강도에 따라 상태 업데이트 (루프에서 상태 동기화)"""
        # 루프 강도 업데이트
        loop_strength = self.loop.get_strength()
        if loop_strength > 0:
            self.negative_bias_strength = loop_strength
        
        # 루프 상태에서 동기화
        bias_state = self.loop.bias_state
        self.state.negative_amplification = bias_state.negative_amplification
        self.state.positive_dampening = bias_state.positive_dampening
        self.state.threat_sensitivity = bias_state.threat_sensitivity
        self.state.memory_bias = bias_state.memory_bias
        self.state.rumination_strength = bias_state.rumination_strength
    
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
        # 루프를 사용하여 자극 처리
        result = self.loop.process_stimulus(stimulus_valence, stimulus_intensity)
        
        # 상태 동기화
        self._update_state_from_strength()
        
        # 위협 감지 (부정적 자극에 대한 과민 반응)
        threat_detected = False
        if stimulus_valence < -0.3:
            threat_probability = (abs(stimulus_valence) * 
                               self.state.threat_sensitivity * 
                               stimulus_intensity)
            if threat_probability > self.threat_threshold_base:
                threat_detected = True
        
        # 결과 반환 (호환성 유지)
        return {
            'perceived_valence': result['perceived_valence'],
            'perceived_intensity': result['perceived_intensity'],
            'threat_detected': threat_detected,
            'rumination_triggered': result.get('rumination_triggered', False),
            'bias_applied': result.get('bias_applied', True),
            'loop_triggered': result.get('loop_triggered', False)
        }
    
    def update_rumination(self, dt: float = 0.1):
        """
        반추 업데이트 (시간에 따른 자연적 감쇠)
        
        Args:
            dt: 시간 간격
        """
        # 루프 업데이트
        self.loop.update(dt)
        
        # 상태 동기화
        self._update_state_from_strength()
    
    def get_bias_score(self) -> float:
        """
        부정적 편향 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            편향 점수 (높을수록 부정적 편향 강함)
        """
        # 루프에서 점수 가져오기
        return self.loop.get_bias_score()

