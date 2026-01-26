"""
에너지 고갈 엔진 (공통)

우울증과 불안장애에서 공통으로 나타나는 에너지 고갈 메커니즘
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class EnergyDepletionState:
    """에너지 고갈 상태"""
    current_energy: float = 100.0         # 현재 에너지 수준
    energy_depletion_rate: float = 0.0    # 에너지 고갈 속도
    recovery_rate: float = 0.0           # 회복 속도
    sleep_quality: float = 1.0            # 수면 질
    circadian_rhythm: float = 1.0         # 일주기 리듬


class EnergyDepletionEngine:
    """
    에너지 고갈 엔진 (Hypothalamus 기반)
    
    핵심 질문: "왜 에너지가 고갈되는가?"
    
    메커니즘:
    1. 에너지 고갈 속도 증가
    2. 회복 속도 감소
    3. 수면 질 저하
    4. 일주기 리듬 혼란
    5. 항상성 붕괴
    """
    
    def __init__(self,
                 depletion_rate: float = 0.0,
                 rng: Optional[np.random.Generator] = None):
        """
        에너지 고갈 엔진 초기화
        
        Args:
            depletion_rate: 고갈 속도 (0.0 ~ 1.0)
            rng: 난수 생성기
        """
        self.depletion_rate = np.clip(depletion_rate, 0.0, 1.0)
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 상태 초기화
        self.state = EnergyDepletionState()
        
        # 파라미터
        self.base_energy = 100.0
        self.base_depletion = 0.1  # 기본 고갈 속도 (단위 시간당)
        self.base_recovery = 0.05  # 기본 회복 속도
        
        # 초기 상태 설정
        self._update_state_from_rate()
    
    def _update_state_from_rate(self):
        """고갈 속도에 따라 상태 업데이트"""
        rate = self.depletion_rate
        
        # 에너지 고갈 속도 증가 (0.1 ~ 0.5)
        self.state.energy_depletion_rate = self.base_depletion + (rate * 0.4)
        
        # 회복 속도 감소 (0.05 ~ 0.01)
        self.state.recovery_rate = self.base_recovery - (rate * 0.04)
        self.state.recovery_rate = max(0.01, self.state.recovery_rate)
        
        # 수면 질 저하 (1.0 ~ 0.3)
        self.state.sleep_quality = 1.0 - (rate * 0.7)
        
        # 일주기 리듬 혼란 (1.0 ~ 0.4)
        self.state.circadian_rhythm = 1.0 - (rate * 0.6)
    
    def update_energy(self, 
                     cognitive_load: float = 0.0,
                     stress_level: float = 0.0,
                     dt: float = 0.1) -> Dict:
        """
        에너지 업데이트
        
        Args:
            cognitive_load: 인지 부하 (0.0 ~ 1.0)
            stress_level: 스트레스 수준 (0.0 ~ 1.0)
            dt: 시간 간격
        
        Returns:
            에너지 상태 정보
        """
        # 에너지 소비 (인지 부하와 스트레스에 비례)
        consumption = (self.state.energy_depletion_rate * 
                      (1.0 + cognitive_load * 0.5 + stress_level * 0.5) * dt)
        
        # 회복 (수면 질과 일주기 리듬에 영향받음)
        recovery = (self.state.recovery_rate * 
                   self.state.sleep_quality * 
                   self.state.circadian_rhythm * dt)
        
        # 에너지 변화
        energy_change = recovery - consumption
        
        # 에너지 업데이트
        self.state.current_energy = np.clip(
            self.state.current_energy + energy_change,
            0.0, self.base_energy
        )
        
        # 에너지가 낮으면 회복 속도도 더 느려짐 (악순환)
        if self.state.current_energy < 30.0:
            effective_recovery = recovery * 0.5
        else:
            effective_recovery = recovery
        
        return {
            'current_energy': self.state.current_energy,
            'energy_change': energy_change,
            'consumption': consumption,
            'recovery': effective_recovery,
            'depletion_rate': self.state.energy_depletion_rate,
            'recovery_rate': self.state.recovery_rate
        }
    
    def get_energy_score(self) -> float:
        """
        에너지 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            에너지 점수 (낮을수록 에너지 고갈)
        """
        energy_ratio = self.state.current_energy / self.base_energy
        recovery_ratio = self.state.recovery_rate / self.base_recovery
        
        score = (
            energy_ratio * 0.5 +
            recovery_ratio * 0.2 +
            self.state.sleep_quality * 0.2 +
            self.state.circadian_rhythm * 0.1
        )
        return np.clip(score, 0.0, 1.0)

