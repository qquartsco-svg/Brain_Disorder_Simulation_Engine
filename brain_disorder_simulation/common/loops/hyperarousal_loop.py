"""
과각성 루프 (Hyperarousal Loop)

PTSD와 불안장애에서 나타나는 과각성 상태 유지 루프

루프 메커니즘:
1. 위협 감지
2. 각성 수준 증가
3. 수면 저하
4. 더 많은 위협 감지 (폐루프)

연구 근거:
- Rauch et al. (2006) - Neurocircuitry of PTSD
- Bremner (2006) - Stress and brain atrophy

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass

from .base_loop import BaseLoop, LoopParameters, LoopState


@dataclass
class HyperarousalLoopState(LoopState):
    """과각성 루프 상태"""
    arousal_level: float = 0.0  # 각성 수준 (0.0 ~ 1.0)
    sleep_quality: float = 1.0  # 수면 질 (0.0 ~ 1.0)
    threat_vigilance: float = 1.0  # 위협 경계 수준
    startle_response: float = 1.0  # 깜짝 반응 강도


class HyperarousalLoop(BaseLoop):
    """
    과각성 루프
    
    위협 감지 → 각성 증가 → 수면 저하 → 더 많은 위협 감지
    
    사용 질환:
    - PTSD
    - 불안장애 (Anxiety)
    """
    
    def __init__(self,
                 initial_arousal: float = 0.0,
                 parameters: Optional[LoopParameters] = None,
                 rng: Optional[np.random.Generator] = None):
        """
        과각성 루프 초기화
        
        Args:
            initial_arousal: 초기 각성 수준 (0.0 ~ 1.0)
            parameters: 루프 파라미터
            rng: 난수 생성기
        """
        # 기본 파라미터 설정
        if parameters is None:
            parameters = LoopParameters(
                loop_gain=0.06,
                loop_decay=0.97,
                loop_threshold=0.4,
                max_strength=1.0,
                min_strength=0.0
            )
        
        super().__init__(
            name="HyperarousalLoop",
            parameters=parameters,
            rng=rng
        )
        
        # 과각성 특화 상태
        self.arousal_state = HyperarousalLoopState()
        
        # 초기 각성 수준 설정
        if initial_arousal > 0:
            self._update_arousal_from_strength(initial_arousal)
    
    def _update_arousal_from_strength(self, strength: float):
        """루프 강도에 따라 각성 상태 업데이트"""
        strength = np.clip(strength, 0.0, 1.0)
        
        # 각성 수준 증가 (0.0 ~ 1.0)
        self.arousal_state.arousal_level = strength
        
        # 수면 질 저하 (1.0 ~ 0.2)
        self.arousal_state.sleep_quality = 1.0 - (strength * 0.8)
        
        # 위협 경계 수준 증가 (1.0 ~ 2.5)
        self.arousal_state.threat_vigilance = 1.0 + (strength * 1.5)
        
        # 깜짝 반응 강도 증가 (1.0 ~ 3.0)
        self.arousal_state.startle_response = 1.0 + (strength * 2.0)
    
    def detect_threat(self, threat_intensity: float = 1.0) -> Dict:
        """
        위협 감지 (루프 트리거)
        
        Args:
            threat_intensity: 위협 강도 (0.0 ~ 1.0)
        
        Returns:
            위협 감지 결과
        """
        # 위협 감지 시 루프 트리거
        trigger_result = self.trigger(threat_intensity, {
            'threat_intensity': threat_intensity
        })
        
        # 각성 수준 증가
        arousal_increase = threat_intensity * 0.2
        self.arousal_state.arousal_level = min(1.0,
            self.arousal_state.arousal_level + arousal_increase)
        
        # 수면 질 즉시 저하
        sleep_degradation = threat_intensity * 0.1
        self.arousal_state.sleep_quality = max(0.0,
            self.arousal_state.sleep_quality - sleep_degradation)
        
        # 위협 경계 수준 증가
        self.arousal_state.threat_vigilance = min(2.5,
            self.arousal_state.threat_vigilance + threat_intensity * 0.1)
        
        return {
            'threat_detected': True,
            'arousal_level': self.arousal_state.arousal_level,
            'sleep_quality': self.arousal_state.sleep_quality,
            'threat_vigilance': self.arousal_state.threat_vigilance,
            **trigger_result
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
        # 루프 강도에 따라 각성 상태 업데이트
        self._update_arousal_from_strength(self.state.loop_strength)
        
        return {
            'arousal_level': self.arousal_state.arousal_level,
            'sleep_quality': self.arousal_state.sleep_quality,
            'threat_vigilance': self.arousal_state.threat_vigilance,
            'startle_response': self.arousal_state.startle_response
        }
    
    def _reinforce_loop(self, effect: Dict):
        """
        루프 자가 강화 (폐루프 형성)
        
        각성이 높을수록 더 많은 위협을 감지하게 됨
        """
        # 기본 자가 강화
        super()._reinforce_loop(effect)
        
        # 수면 질이 낮으면 루프가 더 강화됨
        if self.arousal_state.sleep_quality < 0.5:
            reinforcement = self.parameters.loop_gain * 0.25
            self.state.loop_strength = min(
                self.parameters.max_strength,
                self.state.loop_strength + reinforcement
            )
        
        # 각성 수준이 높으면 루프가 더 강화됨
        if self.arousal_state.arousal_level > 0.6:
            reinforcement = self.parameters.loop_gain * 0.2
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
        
        # 각성 수준 자연적 감쇠 (하지만 수면이 나쁘면 느림)
        arousal_decay = 0.98 if self.arousal_state.sleep_quality > 0.5 else 0.99
        self.arousal_state.arousal_level *= (arousal_decay ** (dt * 10))
        
        # 수면 질 회복 (하지만 각성이 높으면 느림)
        if self.arousal_state.arousal_level < 0.3:
            sleep_recovery = 0.02 * dt
            self.arousal_state.sleep_quality = min(1.0,
                self.arousal_state.sleep_quality + sleep_recovery)
        
        # 위협 경계 수준 자연적 감쇠
        self.arousal_state.threat_vigilance = max(1.0,
            self.arousal_state.threat_vigilance * (0.99 ** (dt * 10)))
        
        # 루프 강도에 따라 각성 상태 업데이트
        self._update_arousal_from_strength(self.state.loop_strength)
        
        result['arousal_state'] = {
            'arousal_level': self.arousal_state.arousal_level,
            'sleep_quality': self.arousal_state.sleep_quality,
            'threat_vigilance': self.arousal_state.threat_vigilance,
            'startle_response': self.arousal_state.startle_response
        }
        
        return result
    
    def get_arousal_score(self) -> float:
        """
        과각성 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            과각성 점수 (높을수록 과각성 강함)
        """
        score = (
            self.arousal_state.arousal_level * 0.4 +
            (1.0 - self.arousal_state.sleep_quality) * 0.3 +
            (self.arousal_state.threat_vigilance - 1.0) / 1.5 * 0.2 +
            (self.arousal_state.startle_response - 1.0) / 2.0 * 0.1
        )
        return np.clip(score, 0.0, 1.0)

