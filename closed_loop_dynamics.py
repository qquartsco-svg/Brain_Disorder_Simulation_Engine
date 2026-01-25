"""
폐루프 동역학 시스템

오픈루프 → 폐루프 전환을 위한 기본 구조
확장 가능한 아키텍처
"""

import numpy as np
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from collections import deque


@dataclass
class StateVector:
    """
    상태 벡터
    
    ADHD 시뮬레이션의 핵심 상태 변수들
    """
    attention: float = 0.5
    arousal: float = 0.5
    pfc_inhibition: float = 0.5
    dopamine_level: float = 0.5
    discount_rate: float = 0.5
    thalamus_gate: float = 0.5
    bg_drive: float = 0.5
    energy: float = 0.5
    noise_level: float = 0.1
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'attention': self.attention,
            'arousal': self.arousal,
            'pfc_inhibition': self.pfc_inhibition,
            'dopamine_level': self.dopamine_level,
            'discount_rate': self.discount_rate,
            'thalamus_gate': self.thalamus_gate,
            'bg_drive': self.bg_drive,
            'energy': self.energy,
            'noise_level': self.noise_level
        }
    
    def from_dict(self, data: Dict):
        """딕셔너리에서 로드"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)


class ClosedLoopDynamics:
    """
    폐루프 동역학 시스템
    
    상태 벡터 기반 동역학 방정식
    엔진 간 피드백 루프 관리
    """
    
    def __init__(self, rng: Optional[np.random.Generator] = None):
        """
        폐루프 동역학 초기화
        
        Args:
            rng: 재현 가능한 랜덤 생성기
        """
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 상태 벡터
        self.state = StateVector()
        
        # 히스토리
        self.state_history = deque(maxlen=1000)
        
        # 피드백 루프 등록 (확장 가능)
        self.feedback_loops: List[Callable] = []
        
        # 시간 추적
        self.time_elapsed = 0.0
        self.dt = 0.1  # 시간 간격 (초)
    
    def register_feedback_loop(self, feedback_func: Callable):
        """
        피드백 루프 등록 (확장 가능)
        
        Args:
            feedback_func: 피드백 함수 (state, dt) -> state
        """
        self.feedback_loops.append(feedback_func)
    
    def update_state(self, external_input: Dict, dt: Optional[float] = None) -> StateVector:
        """
        상태 벡터 업데이트 (동역학 방정식)
        
        Args:
            external_input: 외부 입력 (작업 요구도, 보상 구조, 방해 자극 등)
            dt: 시간 간격 (None이면 기본값 사용)
        
        Returns:
            업데이트된 상태 벡터
        """
        if dt is None:
            dt = self.dt
        
        self.time_elapsed += dt
        
        # 기본 동역학 (확장 가능)
        self._update_basic_dynamics(external_input, dt)
        
        # 등록된 피드백 루프 실행
        for feedback_func in self.feedback_loops:
            self.state = feedback_func(self.state, dt)
        
        # 노이즈 추가 (ADHD 특성)
        self._add_noise(dt)
        
        # 범위 제한
        self._clamp_state()
        
        # 히스토리 저장
        self.state_history.append(self.state.to_dict())
        
        return self.state
    
    def _update_basic_dynamics(self, external_input: Dict, dt: float):
        """기본 동역학 업데이트"""
        # 도파민 효과
        dopamine = self.state.dopamine_level
        
        # 주의력 동역학
        task_importance = external_input.get('task_importance', 0.5)
        distractions = external_input.get('distractions', [])
        
        # 도파민이 낮으면 주의력 감소율 증가
        attention_decay = 0.02 * (2.0 if dopamine < 0.4 else 1.0)
        attention_decay *= dt
        
        # 기본 주의력
        base_attention = task_importance * (1.0 - attention_decay)
        
        # 방해 자극 효과
        distraction_penalty = sum(
            d.get('intensity', 0.0) * d.get('relevance', 0.5)
            for d in distractions
        ) * 0.3
        
        # Thalamus 게이트 효과
        # 게이트가 높을수록 방해 자극 통과 (낮을수록 차단)
        effective_distraction = distraction_penalty * self.state.thalamus_gate
        
        self.state.attention = max(0.0, base_attention - effective_distraction)
        
        # PFC 억제력 동역학
        # 도파민이 낮으면 억제력 감소
        inhibition_decay = 0.01 * (1.5 if dopamine < 0.4 else 1.0) * dt
        self.state.pfc_inhibition = max(0.0, self.state.pfc_inhibition - inhibition_decay)
        
        # Basal Ganglia 구동력
        # 도파민이 낮으면 구동력 증가 (충동성)
        bg_base = 0.5
        bg_boost = (0.4 - dopamine) * 0.5 if dopamine < 0.4 else 0.0
        self.state.bg_drive = np.clip(bg_base + bg_boost, 0.0, 1.0)
        
        # Thalamus 게이트
        # 에너지와 각성도에 따라 조절
        energy_factor = self.state.energy / 100.0 if self.state.energy > 0 else 0.5
        arousal_factor = self.state.arousal
        self.state.thalamus_gate = np.clip((energy_factor + arousal_factor) / 2.0, 0.0, 1.0)
        
        # 할인율 (충동성)
        # 도파민이 낮으면 할인율 증가
        base_discount = 0.3
        discount_boost = (0.4 - dopamine) * 0.4 if dopamine < 0.4 else 0.0
        self.state.discount_rate = np.clip(base_discount + discount_boost, 0.0, 1.0)
    
    def _add_noise(self, dt: float):
        """노이즈 추가 (ADHD 특성)"""
        noise_scale = self.state.noise_level * dt
        
        # 각 상태 변수에 노이즈 추가
        self.state.attention += self.rng.normal(0, noise_scale * 0.1)
        self.state.arousal += self.rng.normal(0, noise_scale * 0.1)
        self.state.pfc_inhibition += self.rng.normal(0, noise_scale * 0.05)
        self.state.dopamine_level += self.rng.normal(0, noise_scale * 0.05)
    
    def _clamp_state(self):
        """상태 변수 범위 제한"""
        self.state.attention = np.clip(self.state.attention, 0.0, 1.0)
        self.state.arousal = np.clip(self.state.arousal, 0.0, 1.0)
        self.state.pfc_inhibition = np.clip(self.state.pfc_inhibition, 0.0, 1.0)
        self.state.dopamine_level = np.clip(self.state.dopamine_level, 0.0, 1.0)
        self.state.discount_rate = np.clip(self.state.discount_rate, 0.0, 1.0)
        self.state.thalamus_gate = np.clip(self.state.thalamus_gate, 0.0, 1.0)
        self.state.bg_drive = np.clip(self.state.bg_drive, 0.0, 1.0)
        self.state.energy = np.clip(self.state.energy, 0.0, 100.0)
        self.state.noise_level = np.clip(self.state.noise_level, 0.0, 1.0)
    
    def apply_feedback(self, attention_score: float, impulse_score: float,
                      hyperactivity_score: float):
        """
        ADHD 엔진 출력을 상태 벡터에 피드백
        
        Args:
            attention_score: 주의력 점수
            impulse_score: 충동성 점수
            hyperactivity_score: 과잉행동 점수
        """
        # 주의력 → Thalamus 게이트
        # 주의력이 낮으면 게이트 약화
        gate_adjustment = (attention_score - 0.5) * 0.2
        self.state.thalamus_gate = np.clip(
            self.state.thalamus_gate + gate_adjustment, 0.0, 1.0
        )
        
        # 충동성 → PFC 억제력
        # 충동성이 높으면 억제력 감소
        inhibition_adjustment = -(impulse_score - 0.5) * 0.2
        self.state.pfc_inhibition = np.clip(
            self.state.pfc_inhibition + inhibition_adjustment, 0.0, 1.0
        )
        
        # 과잉행동 → 각성도
        # 과잉행동이 높으면 각성도 증가
        arousal_adjustment = (hyperactivity_score - 0.5) * 0.3
        self.state.arousal = np.clip(
            self.state.arousal + arousal_adjustment, 0.0, 1.0
        )
    
    def get_state(self) -> StateVector:
        """현재 상태 벡터 반환"""
        return self.state
    
    def reset(self):
        """상태 리셋"""
        self.state = StateVector()
        self.time_elapsed = 0.0
        self.state_history.clear()

