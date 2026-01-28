"""
부정적 편향 루프 (Negative Bias Loop)

우울증과 PTSD에서 공통으로 나타나는 부정적 편향 강화 루프

루프 메커니즘:
1. 부정적 자극 감지
2. 부정적 편향 강화
3. 긍정적 자극 감쇠
4. 기억 편향 형성
5. 반추 (rumination) 강화
6. 더 많은 부정적 자극 감지 (폐루프)

연구 근거:
- Beck (1967) - Cognitive model of depression
- Disner et al. (2011) - Neural mechanisms of negative bias

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass

from .base_loop import BaseLoop, LoopParameters, LoopState


@dataclass
class NegativeBiasLoopState(LoopState):
    """부정적 편향 루프 상태"""
    negative_amplification: float = 1.0  # 부정적 자극 증폭 배수
    positive_dampening: float = 1.0  # 긍정적 자극 감쇠 배수
    memory_bias: float = 0.0  # 부정적 기억 편향
    rumination_strength: float = 0.0  # 반추 강도
    threat_sensitivity: float = 1.0  # 위협 민감도


class NegativeBiasLoop(BaseLoop):
    """
    부정적 편향 루프
    
    부정적 자극 → 편향 강화 → 기억 편향 → 반추 → 더 많은 부정적 자극 감지
    
    사용 질환:
    - 우울증 (Depression)
    - PTSD
    - 불안장애 (Anxiety)
    """
    
    def __init__(self,
                 initial_bias_strength: float = 0.0,
                 parameters: Optional[LoopParameters] = None,
                 rng: Optional[np.random.Generator] = None):
        """
        부정적 편향 루프 초기화
        
        Args:
            initial_bias_strength: 초기 편향 강도 (0.0 ~ 1.0)
            parameters: 루프 파라미터
            rng: 난수 생성기
        """
        # 기본 파라미터 설정
        if parameters is None:
            parameters = LoopParameters(
                loop_gain=0.05,
                loop_decay=0.98,
                loop_threshold=0.3,
                max_strength=1.0,
                min_strength=0.0
            )
        
        super().__init__(
            name="NegativeBiasLoop",
            parameters=parameters,
            rng=rng
        )
        
        # 부정적 편향 특화 상태
        self.bias_state = NegativeBiasLoopState()
        
        # 초기 편향 강도 설정
        if initial_bias_strength > 0:
            self._update_bias_from_strength(initial_bias_strength)
    
    def _update_bias_from_strength(self, strength: float):
        """편향 강도에 따라 상태 업데이트"""
        strength = np.clip(strength, 0.0, 1.0)
        
        # 부정적 자극 증폭 (1.0 ~ 2.5)
        self.bias_state.negative_amplification = 1.0 + (strength * 1.5)
        
        # 긍정적 자극 감쇠 (1.0 ~ 0.3)
        self.bias_state.positive_dampening = 1.0 - (strength * 0.7)
        
        # 위협 민감도 증가 (1.0 ~ 2.0)
        self.bias_state.threat_sensitivity = 1.0 + (strength * 1.0)
        
        # 기억 편향 (0.0 ~ 0.8)
        self.bias_state.memory_bias = strength * 0.8
    
    def process_stimulus(self,
                        stimulus_valence: float,
                        stimulus_intensity: float = 1.0) -> Dict:
        """
        자극 처리 (부정적 편향 적용)
        
        Args:
            stimulus_valence: 자극의 정서가 (-1.0: 매우 부정적, 0.0: 중립, 1.0: 매우 긍정적)
            stimulus_intensity: 자극 강도
        
        Returns:
            처리된 자극 정보
        """
        # 부정적 자극인 경우 루프 트리거
        if stimulus_valence < 0:
            trigger_intensity = abs(stimulus_valence) * stimulus_intensity
            trigger_result = self.trigger(trigger_intensity, {
                'stimulus_valence': stimulus_valence,
                'stimulus_intensity': stimulus_intensity
            })
            
            # 반추 강화
            self.bias_state.rumination_strength = min(1.0,
                self.bias_state.rumination_strength + 0.1 * trigger_intensity)
            
            # 기억 편향 업데이트
            self.bias_state.memory_bias = min(1.0,
                self.bias_state.memory_bias + 0.05 * trigger_intensity)
            
            # 부정적 자극 증폭 적용
            amplified_intensity = stimulus_intensity * self.bias_state.negative_amplification
            perceived_valence = stimulus_valence * self.bias_state.negative_amplification
            
            return {
                'perceived_valence': np.clip(perceived_valence, -1.0, 1.0),
                'perceived_intensity': amplified_intensity,
                'bias_applied': True,
                'rumination_triggered': True,
                'loop_triggered': True,
                **trigger_result
            }
        
        # 긍정적 자극인 경우
        elif stimulus_valence > 0:
            # 긍정적 자극 감쇠 적용
            dampened_intensity = stimulus_intensity * self.bias_state.positive_dampening
            perceived_valence = stimulus_valence * self.bias_state.positive_dampening
            
            # 반추 약화
            self.bias_state.rumination_strength *= 0.95
            
            return {
                'perceived_valence': np.clip(perceived_valence, -1.0, 1.0),
                'perceived_intensity': dampened_intensity,
                'bias_applied': True,
                'rumination_triggered': False,
                'loop_triggered': False
            }
        
        # 중립 자극
        else:
            # 반추가 강하면 중립도 부정적으로 해석
            if self.bias_state.rumination_strength > 0.3:
                perceived_valence = -0.1 * self.bias_state.rumination_strength
                return {
                    'perceived_valence': perceived_valence,
                    'perceived_intensity': stimulus_intensity,
                    'bias_applied': True,
                    'rumination_triggered': False,
                    'loop_triggered': False
                }
            else:
                return {
                    'perceived_valence': 0.0,
                    'perceived_intensity': stimulus_intensity,
                    'bias_applied': False,
                    'rumination_triggered': False,
                    'loop_triggered': False
                }
    
    def _apply_loop_effect(self, intensity: float, context: Optional[Dict] = None) -> Dict:
        """
        루프 효과 적용
        
        Args:
            intensity: 효과 강도
            context: 컨텍스트 정보
        
        Returns:
            적용된 효과 정보
        """
        # 루프 강도에 따라 편향 상태 업데이트
        self._update_bias_from_strength(self.state.loop_strength)
        
        return {
            'negative_amplification': self.bias_state.negative_amplification,
            'positive_dampening': self.bias_state.positive_dampening,
            'memory_bias': self.bias_state.memory_bias,
            'rumination_strength': self.bias_state.rumination_strength,
            'threat_sensitivity': self.bias_state.threat_sensitivity
        }
    
    def _reinforce_loop(self, effect: Dict):
        """
        루프 자가 강화 (폐루프 형성)
        
        부정적 편향이 강해질수록 더 많은 부정적 자극을 감지하게 됨
        """
        # 기본 자가 강화
        super()._reinforce_loop(effect)
        
        # 반추가 강하면 루프가 더 강화됨
        if self.bias_state.rumination_strength > 0.5:
            reinforcement = self.parameters.loop_gain * 0.2
            self.state.loop_strength = min(
                self.parameters.max_strength,
                self.state.loop_strength + reinforcement
            )
        
        # 기억 편향이 강하면 루프가 더 강화됨
        if self.bias_state.memory_bias > 0.5:
            reinforcement = self.parameters.loop_gain * 0.15
            self.state.loop_strength = min(
                self.parameters.max_strength,
                self.state.loop_strength + reinforcement
            )
    
    def update(self, dt: float = 0.1, external_factors: Optional[Dict] = None) -> Dict:
        """
        루프 업데이트 (시간 경과에 따른 자연적 감쇠)
        
        Args:
            dt: 시간 간격
            external_factors: 외부 요인
        """
        # 기본 업데이트
        result = super().update(dt, external_factors)
        
        # 반추 자연적 감쇠
        self.bias_state.rumination_strength *= (0.95 ** (dt * 10))
        
        # 기억 편향 자연적 감쇠
        self.bias_state.memory_bias *= (0.98 ** (dt * 10))
        
        # 루프 강도에 따라 편향 상태 업데이트
        self._update_bias_from_strength(self.state.loop_strength)
        
        result['bias_state'] = {
            'negative_amplification': self.bias_state.negative_amplification,
            'positive_dampening': self.bias_state.positive_dampening,
            'memory_bias': self.bias_state.memory_bias,
            'rumination_strength': self.bias_state.rumination_strength,
            'threat_sensitivity': self.bias_state.threat_sensitivity
        }
        
        return result
    
    def get_bias_score(self) -> float:
        """
        부정적 편향 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            편향 점수 (높을수록 부정적 편향 강함)
        """
        score = (
            (self.bias_state.negative_amplification - 1.0) / 1.5 * 0.3 +
            (1.0 - self.bias_state.positive_dampening) / 0.7 * 0.3 +
            (self.bias_state.threat_sensitivity - 1.0) / 1.0 * 0.2 +
            self.bias_state.rumination_strength * 0.1 +
            self.bias_state.memory_bias * 0.1
        )
        return np.clip(score, 0.0, 1.0)

