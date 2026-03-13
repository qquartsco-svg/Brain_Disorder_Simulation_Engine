"""
회피 강화 루프 (Avoidance Reinforcement Loop)

PTSD, 불안장애, OCD에서 공통적으로 나타나는 회피 패턴 강화 메커니즘

핵심 메커니즘:
회피 학습 → 단기 불안 감소 → 회피 강화 → 노출 기회 감소 → 회피 더 강화 (폐루프)

연구 근거:
- Mowrer (1960) - Two-factor theory of avoidance
- Foa & Kozak (1986) - Emotional processing theory
- Craske et al. (2008) - Avoidance in anxiety disorders

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional, List
from dataclasses import dataclass, field

from .base_loop import BaseLoop, LoopState, LoopParameters


@dataclass
class AvoidanceReinforcementLoopState(LoopState):
    """회피 강화 루프 상태"""
    avoidance_strength: float = 0.0  # 회피 강도 (0.0 ~ 1.0)
    emotional_numbing: float = 0.0  # 감정적 마비 (0.0 ~ 1.0)
    generalization_factor: float = 0.3  # 일반화 인자 (0.0 ~ 1.0)
    avoided_stimuli_count: int = 0  # 회피된 자극 수
    current_avoidance_level: float = 0.0  # 현재 회피 수준 (0.0 ~ 1.0)
    avoided_stimuli: List[str] = field(default_factory=list)  # 회피된 자극 목록
    avoidance_strength_map: Dict[str, float] = field(default_factory=dict)  # 자극별 회피 강도


class AvoidanceReinforcementLoop(BaseLoop):
    """
    회피 강화 루프
    
    PTSD, 불안장애, OCD에서 공통적으로 나타나는 회피 패턴 강화 메커니즘
    
    루프 메커니즘:
    1. 공포 자극 접촉
    2. 회피 학습
    3. 단기 불안 감소
    4. 회피 강화
    5. 노출 기회 감소
    6. 회피 더 강화
    7. 루프 강화 (폐루프)
    """
    
    def __init__(self,
                 initial_avoidance_strength: float = 0.0,
                 initial_generalization: float = 0.3,
                 parameters: Optional[LoopParameters] = None,
                 rng: Optional[np.random.Generator] = None):
        """
        회피 강화 루프 초기화
        
        Args:
            initial_avoidance_strength: 초기 회피 강도 (0.0 ~ 1.0)
            initial_generalization: 초기 일반화 인자 (0.0 ~ 1.0)
            parameters: 루프 파라미터
            rng: 난수 생성기
        """
        # 기본 파라미터 설정
        if parameters is None:
            parameters = LoopParameters(
                loop_gain=0.04,
                loop_decay=0.99,
                loop_threshold=0.3,
                max_strength=1.0,
                min_strength=0.0
            )
        
        super().__init__(
            name="AvoidanceReinforcementLoop",
            parameters=parameters,
            rng=rng
        )
        
        # 초기 상태 설정
        self.avoidance_state = AvoidanceReinforcementLoopState()
        self.avoidance_state.generalization_factor = np.clip(initial_generalization, 0.0, 1.0)
        
        # 동역학 파라미터
        self.avoidance_learning_rate = 0.2  # 회피 학습률
        
        # 초기 회피 강도 적용
        if initial_avoidance_strength > 0.0:
            self._apply_avoidance(initial_avoidance_strength)
    
    def _apply_avoidance(self, strength: float):
        """회피 강도에 따라 상태 업데이트"""
        strength = np.clip(strength, 0.0, 1.0)
        
        # 회피 강도 설정
        self.avoidance_state.avoidance_strength = strength
        self.avoidance_state.current_avoidance_level = strength
        
        # 일반화 인자 증가
        self.avoidance_state.generalization_factor = min(
            1.0,
            0.3 + (strength * 0.7)
        )
        
        # 루프 강도 설정
        self.state.loop_strength = strength
    
    def _trigger_condition(self, context: Optional[Dict] = None) -> bool:
        """
        트리거 조건 확인
        
        Args:
            context: 컨텍스트 정보
                - stimulus: 자극 식별자
                - fear_level: 공포 수준 (0.0 ~ 1.0)
                - avoidance_successful: 회피 성공 여부
        
        Returns:
            트리거 여부
        """
        if context is None:
            return False
        
        # 공포 자극 접촉
        fear_level = context.get('fear_level', 0.0)
        if fear_level > 0.5:
            return True
        
        # 회피 성공 (단기 불안 감소)
        if context.get('avoidance_successful', False):
            return True
        
        # 유사 자극 감지
        stimulus = context.get('stimulus', '')
        if stimulus and self._check_generalized_avoidance(stimulus)[0]:
            return True
        
        return False
    
    def _update_dynamics(self, dt: float, context: Optional[Dict] = None):
        """
        동역학 업데이트
        
        Args:
            dt: 시간 간격
            context: 컨텍스트 정보
        """
        # 루프 강도에 따른 영향
        loop_effect = self.state.loop_strength
        
        # 회피 강도 증가
        strength_increase = 0.01 * loop_effect * dt
        self.avoidance_state.avoidance_strength = min(
            1.0,
            self.avoidance_state.avoidance_strength + strength_increase
        )
        
        # 감정적 마비 증가
        numbing_increase = 0.015 * loop_effect * dt
        self.avoidance_state.emotional_numbing = min(
            1.0,
            self.avoidance_state.emotional_numbing + numbing_increase
        )
        
        # 일반화 인자 증가 (회피가 강화될수록 유사 자극도 회피)
        generalization_increase = 0.01 * loop_effect * dt
        self.avoidance_state.generalization_factor = min(
            1.0,
            self.avoidance_state.generalization_factor + generalization_increase
        )
        
        # 자연적 감쇠 (매우 느림)
        self.state.loop_strength *= (self.parameters.loop_decay ** (dt * 0.1))
    
    def learn_avoidance(self, stimulus: str, fear_level: float):
        """
        회피 학습 (Basal Ganglia 역할)
        
        Args:
            stimulus: 자극 식별자
            fear_level: 공포 수준 (0.0 ~ 1.0)
        """
        # 새로운 자극이면 목록에 추가
        if stimulus not in self.avoidance_state.avoided_stimuli:
            self.avoidance_state.avoided_stimuli.append(stimulus)
            self.avoidance_state.avoided_stimuli_count += 1
        
        # 회피 강도 업데이트
        current_strength = self.avoidance_state.avoidance_strength_map.get(stimulus, 0.0)
        new_strength = np.clip(
            current_strength + self.avoidance_learning_rate * fear_level,
            0.0, 1.0
        )
        self.avoidance_state.avoidance_strength_map[stimulus] = new_strength
        
        # 감정적 마비 증가
        self.avoidance_state.emotional_numbing = np.clip(
            self.avoidance_state.emotional_numbing + 0.05 * fear_level,
            0.0, 1.0
        )
        
        # 회피 학습 시 루프 트리거
        self.trigger(
            intensity=fear_level,
            context={
                'stimulus': stimulus,
                'fear_level': fear_level,
                'avoidance_successful': True
            }
        )
        
        # 전체 회피 수준 업데이트
        self.compute_avoidance_level()
    
    def check_avoidance(self, stimulus: str) -> tuple[bool, float]:
        """
        회피 여부 확인
        
        Args:
            stimulus: 자극 식별자
        
        Returns:
            (회피 여부, 회피 강도)
        """
        return self._check_generalized_avoidance(stimulus)
    
    def _check_generalized_avoidance(self, stimulus: str) -> tuple[bool, float]:
        """
        일반화된 회피 확인 (유사 자극도 회피)
        
        Args:
            stimulus: 자극 식별자
        
        Returns:
            (회피 여부, 회피 강도)
        """
        # 직접 회피
        if stimulus in self.avoidance_state.avoided_stimuli:
            strength = self.avoidance_state.avoidance_strength_map.get(stimulus, 0.0)
            return True, strength
        
        # 일반화된 회피 (유사 자극)
        for avoided in self.avoidance_state.avoided_stimuli:
            similarity = self._compute_similarity(stimulus, avoided)
            if similarity > (1.0 - self.avoidance_state.generalization_factor):
                strength = self.avoidance_state.avoidance_strength_map.get(avoided, 0.0) * similarity
                return True, strength
        
        return False, 0.0
    
    def _compute_similarity(self, s1: str, s2: str) -> float:
        """
        자극 유사도 계산 (간단한 구현)
        
        Args:
            s1, s2: 자극 식별자
        
        Returns:
            유사도 (0.0 ~ 1.0)
        """
        if s1 == s2:
            return 1.0
        
        # 공통 부분 기반
        common_chars = sum(1 for c in s1 if c in s2)
        max_len = max(len(s1), len(s2))
        return common_chars / max_len if max_len > 0 else 0.0
    
    def compute_avoidance_level(self) -> float:
        """
        전체 회피 수준 계산
        
        Returns:
            회피 수준 (0.0 ~ 1.0)
        """
        if not self.avoidance_state.avoidance_strength_map:
            self.avoidance_state.current_avoidance_level = 0.0
            return 0.0
        
        avg_strength = np.mean(list(self.avoidance_state.avoidance_strength_map.values()))
        self.avoidance_state.current_avoidance_level = avg_strength
        self.avoidance_state.avoidance_strength = avg_strength
        
        return avg_strength
    
    def _apply_loop_effect(self, intensity: float, context: Optional[Dict] = None) -> Dict:
        """
        루프 효과 적용
        
        Args:
            intensity: 효과 강도
            context: 컨텍스트 정보
        
        Returns:
            적용된 효과 정보
        """
        # 루프 강도에 따라 회피 상태 업데이트
        self._update_avoidance_from_strength(self.state.loop_strength)
        
        return {
            'avoidance_strength': self.avoidance_state.avoidance_strength,
            'emotional_numbing': self.avoidance_state.emotional_numbing,
            'generalization_factor': self.avoidance_state.generalization_factor,
            'current_avoidance_level': self.avoidance_state.current_avoidance_level,
            'avoided_stimuli_count': self.avoidance_state.avoided_stimuli_count,
            'loop_strength': self.state.loop_strength
        }
    
    def _update_avoidance_from_strength(self, strength: float):
        """
        루프 강도에 따라 회피 상태 업데이트
        
        Args:
            strength: 루프 강도 (0.0 ~ 1.0)
        """
        # 회피 강도 업데이트
        self.avoidance_state.avoidance_strength = max(
            self.avoidance_state.avoidance_strength,
            strength
        )
        
        # 일반화 인자 업데이트
        self.avoidance_state.generalization_factor = min(
            1.0,
            0.3 + (strength * 0.7)
        )
    
    def _calculate_score(self) -> float:
        """
        루프 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            루프 점수 (높을수록 회피 심각)
        """
        # 회피 심각도 계산
        avoidance_severity = (
            self.avoidance_state.avoidance_strength * 0.4 +
            self.avoidance_state.emotional_numbing * 0.3 +
            self.avoidance_state.generalization_factor * 0.2 +
            (self.avoidance_state.avoided_stimuli_count / 10.0) * 0.1
        )
        
        return np.clip(avoidance_severity, 0.0, 1.0)
    
    def _analyze_patterns(self) -> Dict:
        """
        패턴 분석
        
        Returns:
            패턴 분석 결과
        """
        return {
            'avoidance_strength': self.avoidance_state.avoidance_strength,
            'emotional_numbing': self.avoidance_state.emotional_numbing,
            'generalization_factor': self.avoidance_state.generalization_factor,
            'current_avoidance_level': self.avoidance_state.current_avoidance_level,
            'avoided_stimuli_count': self.avoidance_state.avoided_stimuli_count,
            'loop_strength': self.state.loop_strength,
            'avoidance_severity': self._calculate_score()
        }
    
    def get_strength(self) -> float:
        """루프 강도 반환"""
        return self.state.loop_strength
    
    def get_state(self) -> AvoidanceReinforcementLoopState:
        """루프 상태 반환"""
        return self.avoidance_state

