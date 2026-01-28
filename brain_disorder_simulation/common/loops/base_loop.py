"""
기본 루프 클래스 (Base Loop Class)

모든 동역학 루프의 기본 클래스
폐루프 동역학 메커니즘을 추상화하여 재사용 가능한 구조 제공

핵심 개념:
- 루프 강도 (loop_strength): 루프의 활성화 정도
- 루프 게인 (loop_gain): 루프 강화 속도
- 루프 감쇠 (loop_decay): 루프 자연 감쇠율
- 루프 임계값 (loop_threshold): 루프 활성화 임계값

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional, List, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class LoopState:
    """루프 상태"""
    loop_strength: float = 0.0  # 루프 강도 (0.0 ~ 1.0)
    activation_count: int = 0  # 활성화 횟수
    last_activation_time: float = 0.0  # 마지막 활성화 시간
    cumulative_effect: float = 0.0  # 누적 효과


@dataclass
class LoopParameters:
    """루프 파라미터"""
    loop_gain: float = 0.05  # 루프 강화 속도
    loop_decay: float = 0.98  # 루프 자연 감쇠율
    loop_threshold: float = 0.3  # 루프 활성화 임계값
    max_strength: float = 1.0  # 최대 루프 강도
    min_strength: float = 0.0  # 최소 루프 강도


class BaseLoop(ABC):
    """
    기본 루프 클래스
    
    모든 동역학 루프의 기본 구조를 제공하는 추상 클래스
    
    루프 메커니즘:
    1. 트리거 이벤트 발생
    2. 루프 강도 증가
    3. 루프 효과 적용
    4. 자연적 감쇠
    5. 폐루프 형성 (강도가 임계값 이상이면 자가 강화)
    """
    
    def __init__(self,
                 name: str,
                 parameters: Optional[LoopParameters] = None,
                 rng: Optional[np.random.Generator] = None):
        """
        기본 루프 초기화
        
        Args:
            name: 루프 이름
            parameters: 루프 파라미터
            rng: 난수 생성기
        """
        self.name = name
        self.parameters = parameters if parameters is not None else LoopParameters()
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 상태 초기화
        self.state = LoopState()
        
        # 히스토리 (디버깅 및 분석용)
        self.history: List[Dict] = []
        self.max_history_length = 1000
    
    def trigger(self, intensity: float = 1.0, context: Optional[Dict] = None) -> Dict:
        """
        루프 트리거 (활성화)
        
        Args:
            intensity: 트리거 강도 (0.0 ~ 1.0)
            context: 추가 컨텍스트 정보
        
        Returns:
            트리거 결과
        """
        # 트리거 전 상태
        prev_strength = self.state.loop_strength
        
        # 루프 강도 증가
        strength_increase = intensity * self.parameters.loop_gain
        self.state.loop_strength = min(
            self.parameters.max_strength,
            self.state.loop_strength + strength_increase
        )
        
        # 활성화 여부 확인
        is_active = self.state.loop_strength >= self.parameters.loop_threshold
        
        # 활성화된 경우
        if is_active:
            self.state.activation_count += 1
            self.state.last_activation_time = 0.0  # 시간은 외부에서 업데이트
        
        # 루프 효과 적용
        effect = self._apply_loop_effect(intensity, context)
        
        # 폐루프 형성 (자가 강화)
        if is_active:
            self._reinforce_loop(effect)
        
        # 히스토리 저장
        self._add_to_history({
            'time': self.state.last_activation_time,
            'trigger_intensity': intensity,
            'prev_strength': prev_strength,
            'new_strength': self.state.loop_strength,
            'is_active': is_active,
            'effect': effect
        })
        
        return {
            'loop_name': self.name,
            'prev_strength': prev_strength,
            'new_strength': self.state.loop_strength,
            'strength_increase': strength_increase,
            'is_active': is_active,
            'activation_count': self.state.activation_count,
            'effect': effect
        }
    
    def update(self, dt: float = 0.1, external_factors: Optional[Dict] = None) -> Dict:
        """
        루프 업데이트 (시간 경과에 따른 자연적 감쇠)
        
        Args:
            dt: 시간 간격
            external_factors: 외부 요인 (예: 치료 개입)
        
        Returns:
            업데이트 결과
        """
        # 시간 업데이트
        self.state.last_activation_time += dt
        
        # 자연적 감쇠
        decay_factor = self.parameters.loop_decay ** (dt * 10)
        self.state.loop_strength *= decay_factor
        
        # 외부 요인 적용 (예: 치료 개입)
        if external_factors:
            self._apply_external_factors(external_factors)
        
        # 최소값 보장
        self.state.loop_strength = max(
            self.parameters.min_strength,
            self.state.loop_strength
        )
        
        # 누적 효과 업데이트
        self.state.cumulative_effect = (
            self.state.cumulative_effect * 0.99 + 
            self.state.loop_strength * 0.01
        )
        
        # 활성화 여부
        is_active = self.state.loop_strength >= self.parameters.loop_threshold
        
        return {
            'loop_name': self.name,
            'loop_strength': self.state.loop_strength,
            'is_active': is_active,
            'cumulative_effect': self.state.cumulative_effect,
            'time': self.state.last_activation_time
        }
    
    def reset(self):
        """루프 상태 초기화"""
        self.state = LoopState()
        self.history = []
    
    def get_strength(self) -> float:
        """현재 루프 강도 반환"""
        return self.state.loop_strength
    
    def is_active(self) -> bool:
        """루프 활성화 여부 확인"""
        return self.state.loop_strength >= self.parameters.loop_threshold
    
    def get_statistics(self) -> Dict:
        """루프 통계 정보 반환"""
        if not self.history:
            return {
                'loop_name': self.name,
                'current_strength': self.state.loop_strength,
                'activation_count': self.state.activation_count,
                'is_active': self.is_active(),
                'cumulative_effect': self.state.cumulative_effect
            }
        
        strengths = [h['new_strength'] for h in self.history]
        return {
            'loop_name': self.name,
            'current_strength': self.state.loop_strength,
            'activation_count': self.state.activation_count,
            'is_active': self.is_active(),
            'cumulative_effect': self.state.cumulative_effect,
            'mean_strength': np.mean(strengths),
            'max_strength': np.max(strengths),
            'min_strength': np.min(strengths),
            'std_strength': np.std(strengths)
        }
    
    @abstractmethod
    def _apply_loop_effect(self, intensity: float, context: Optional[Dict] = None) -> Dict:
        """
        루프 효과 적용 (서브클래스에서 구현)
        
        Args:
            intensity: 효과 강도
            context: 컨텍스트 정보
        
        Returns:
            적용된 효과 정보
        """
        pass
    
    def _reinforce_loop(self, effect: Dict):
        """
        루프 자가 강화 (폐루프 형성)
        
        Args:
            effect: 루프 효과 정보
        """
        # 기본 자가 강화 메커니즘
        # 서브클래스에서 오버라이드 가능
        if self.state.loop_strength > self.parameters.loop_threshold:
            # 루프가 활성화되면 추가 강화
            reinforcement = self.parameters.loop_gain * 0.1
            self.state.loop_strength = min(
                self.parameters.max_strength,
                self.state.loop_strength + reinforcement
            )
    
    def _apply_external_factors(self, factors: Dict):
        """
        외부 요인 적용 (예: 치료 개입)
        
        Args:
            factors: 외부 요인 딕셔너리
        """
        # 치료 효과 등 외부 개입
        if 'intervention_strength' in factors:
            intervention = factors['intervention_strength']
            self.state.loop_strength = max(
                self.parameters.min_strength,
                self.state.loop_strength - intervention
            )
    
    def _add_to_history(self, entry: Dict):
        """히스토리에 항목 추가"""
        self.history.append(entry)
        if len(self.history) > self.max_history_length:
            self.history.pop(0)

