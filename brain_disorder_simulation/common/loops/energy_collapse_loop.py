"""
에너지 붕괴 루프 (Energy Collapse Loop)

우울증에서 나타나는 에너지 시스템 붕괴 루프

루프 메커니즘:
1. 에너지 고갈
2. 회복 속도 감소
3. 수면 질 저하
4. 더 많은 에너지 고갈 (폐루프)

연구 근거:
- Nutt et al. (2007) - Sleep and depression
- Treadway et al. (2012) - Effort-based decision making in depression

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass

from .base_loop import BaseLoop, LoopParameters, LoopState


@dataclass
class EnergyCollapseLoopState(LoopState):
    """에너지 붕괴 루프 상태"""
    current_energy: float = 100.0  # 현재 에너지 수준 (0.0 ~ 100.0)
    energy_depletion_rate: float = 0.1  # 에너지 고갈 속도
    recovery_rate: float = 0.05  # 회복 속도
    sleep_quality: float = 1.0  # 수면 질 (0.0 ~ 1.0)
    circadian_rhythm: float = 1.0  # 일주기 리듬 (0.0 ~ 1.0)


class EnergyCollapseLoop(BaseLoop):
    """
    에너지 붕괴 루프
    
    에너지 고갈 → 회복 속도 감소 → 수면 저하 → 더 많은 고갈
    
    사용 질환:
    - 우울증 (Depression)
    """
    
    def __init__(self,
                 initial_energy: float = 100.0,
                 initial_depletion_rate: float = 0.0,
                 parameters: Optional[LoopParameters] = None,
                 rng: Optional[np.random.Generator] = None):
        """
        에너지 붕괴 루프 초기화
        
        Args:
            initial_energy: 초기 에너지 수준 (0.0 ~ 100.0)
            initial_depletion_rate: 초기 고갈 속도 (0.0 ~ 1.0)
            parameters: 루프 파라미터
            rng: 난수 생성기
        """
        # 기본 파라미터 설정
        if parameters is None:
            parameters = LoopParameters(
                loop_gain=0.04,
                loop_decay=0.99,
                loop_threshold=0.2,
                max_strength=1.0,
                min_strength=0.0
            )
        
        super().__init__(
            name="EnergyCollapseLoop",
            parameters=parameters,
            rng=rng
        )
        
        # 에너지 붕괴 특화 상태
        self.energy_state = EnergyCollapseLoopState()
        self.energy_state.current_energy = np.clip(initial_energy, 0.0, 100.0)
        
        # 초기 고갈 속도 설정
        if initial_depletion_rate > 0:
            self._update_energy_from_depletion(initial_depletion_rate)
    
    def _update_energy_from_depletion(self, depletion_rate: float):
        """고갈 속도에 따라 에너지 상태 업데이트"""
        depletion_rate = np.clip(depletion_rate, 0.0, 1.0)
        
        # 에너지 고갈 속도 증가 (0.1 ~ 0.5)
        self.energy_state.energy_depletion_rate = 0.1 + (depletion_rate * 0.4)
        
        # 회복 속도 감소 (0.05 ~ 0.01)
        self.energy_state.recovery_rate = 0.05 - (depletion_rate * 0.04)
        self.energy_state.recovery_rate = max(0.01, self.energy_state.recovery_rate)
        
        # 수면 질 저하 (1.0 ~ 0.3)
        self.energy_state.sleep_quality = 1.0 - (depletion_rate * 0.7)
        
        # 일주기 리듬 혼란 (1.0 ~ 0.4)
        self.energy_state.circadian_rhythm = 1.0 - (depletion_rate * 0.6)
    
    def consume_energy(self,
                      cognitive_load: float = 0.0,
                      stress_level: float = 0.0) -> Dict:
        """
        에너지 소비 (루프 트리거)
        
        Args:
            cognitive_load: 인지 부하 (0.0 ~ 1.0)
            stress_level: 스트레스 수준 (0.0 ~ 1.0)
        
        Returns:
            에너지 소비 결과
        """
        # 에너지 소비량 계산
        consumption = (self.energy_state.energy_depletion_rate *
                      (1.0 + cognitive_load * 0.5 + stress_level * 0.5))
        
        # 에너지 감소
        energy_before = self.energy_state.current_energy
        self.energy_state.current_energy = max(0.0,
            self.energy_state.current_energy - consumption)
        
        # 에너지가 낮으면 루프 트리거
        energy_ratio = self.energy_state.current_energy / 100.0
        if energy_ratio < 0.5:
            trigger_intensity = 1.0 - energy_ratio
            trigger_result = self.trigger(trigger_intensity, {
                'cognitive_load': cognitive_load,
                'stress_level': stress_level,
                'energy_before': energy_before,
                'energy_after': self.energy_state.current_energy
            })
        else:
            trigger_result = {'loop_triggered': False}
        
        return {
            'energy_before': energy_before,
            'energy_after': self.energy_state.current_energy,
            'consumption': consumption,
            'energy_ratio': energy_ratio,
            **trigger_result
        }
    
    def update_energy(self,
                     cognitive_load: float = 0.0,
                     stress_level: float = 0.0,
                     dt: float = 0.1) -> Dict:
        """
        에너지 업데이트 (시간 경과)
        
        Args:
            cognitive_load: 인지 부하 (0.0 ~ 1.0)
            stress_level: 스트레스 수준 (0.0 ~ 1.0)
            dt: 시간 간격
        
        Returns:
            에너지 상태 정보
        """
        # 에너지 소비
        consumption = (self.energy_state.energy_depletion_rate *
                      (1.0 + cognitive_load * 0.5 + stress_level * 0.5) * dt)
        
        # 회복 (수면 질과 일주기 리듬에 영향받음)
        recovery = (self.energy_state.recovery_rate *
                   self.energy_state.sleep_quality *
                   self.energy_state.circadian_rhythm * dt)
        
        # 에너지가 낮으면 회복 속도도 더 느려짐 (악순환)
        if self.energy_state.current_energy < 30.0:
            effective_recovery = recovery * 0.5
        else:
            effective_recovery = recovery
        
        # 에너지 변화
        energy_change = effective_recovery - consumption
        
        # 에너지 업데이트
        self.energy_state.current_energy = np.clip(
            self.energy_state.current_energy + energy_change,
            0.0, 100.0
        )
        
        # 에너지가 낮으면 루프 강화
        energy_ratio = self.energy_state.current_energy / 100.0
        if energy_ratio < 0.3:
            self.state.loop_strength = min(1.0,
                self.state.loop_strength + 0.05 * (1.0 - energy_ratio))
        
        # 기본 루프 업데이트
        loop_result = self.update(dt)
        
        return {
            'current_energy': self.energy_state.current_energy,
            'energy_change': energy_change,
            'consumption': consumption,
            'recovery': effective_recovery,
            'depletion_rate': self.energy_state.energy_depletion_rate,
            'recovery_rate': self.energy_state.recovery_rate,
            'energy_ratio': energy_ratio,
            **loop_result
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
        # 루프 강도에 따라 고갈 속도 업데이트
        self._update_energy_from_depletion(self.state.loop_strength)
        
        return {
            'current_energy': self.energy_state.current_energy,
            'energy_depletion_rate': self.energy_state.energy_depletion_rate,
            'recovery_rate': self.energy_state.recovery_rate,
            'sleep_quality': self.energy_state.sleep_quality,
            'circadian_rhythm': self.energy_state.circadian_rhythm
        }
    
    def _reinforce_loop(self, effect: Dict):
        """
        루프 자가 강화 (폐루프 형성)
        
        에너지가 낮을수록 회복이 어려워져 더 많은 고갈 발생
        """
        # 기본 자가 강화
        super()._reinforce_loop(effect)
        
        # 에너지가 낮으면 루프가 더 강화됨
        energy_ratio = self.energy_state.current_energy / 100.0
        if energy_ratio < 0.3:
            reinforcement = self.parameters.loop_gain * 0.3
            self.state.loop_strength = min(
                self.parameters.max_strength,
                self.state.loop_strength + reinforcement
            )
        
        # 수면 질이 낮으면 루프가 더 강화됨
        if self.energy_state.sleep_quality < 0.5:
            reinforcement = self.parameters.loop_gain * 0.2
            self.state.loop_strength = min(
                self.parameters.max_strength,
                self.state.loop_strength + reinforcement
            )
    
    def get_energy_score(self) -> float:
        """
        에너지 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            에너지 점수 (낮을수록 에너지 고갈)
        """
        energy_ratio = self.energy_state.current_energy / 100.0
        recovery_ratio = self.energy_state.recovery_rate / 0.05
        
        score = (
            energy_ratio * 0.5 +
            recovery_ratio * 0.2 +
            self.energy_state.sleep_quality * 0.2 +
            self.energy_state.circadian_rhythm * 0.1
        )
        return np.clip(score, 0.0, 1.0)

