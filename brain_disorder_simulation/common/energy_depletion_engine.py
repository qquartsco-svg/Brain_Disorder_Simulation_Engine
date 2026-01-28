"""
에너지 고갈 엔진 (공통)

우울증과 불안장애에서 공통으로 나타나는 에너지 고갈 메커니즘

⚠️ 리팩터링: 이 엔진은 내부적으로 EnergyCollapseLoop를 사용합니다.
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass

# 루프 라이브러리 import
from .loops.energy_collapse_loop import EnergyCollapseLoop


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
        
        # 루프 라이브러리 사용
        self.loop = EnergyCollapseLoop(
            initial_energy=100.0,
            initial_depletion_rate=depletion_rate,
            rng=rng
        )
        
        # 상태 초기화 (호환성 유지)
        self.state = EnergyDepletionState()
        
        # 파라미터
        self.base_energy = 100.0
        self.base_depletion = 0.1  # 기본 고갈 속도 (단위 시간당)
        self.base_recovery = 0.05  # 기본 회복 속도
        
        # 초기 상태 설정
        self._update_state_from_rate()
    
    def _update_state_from_rate(self):
        """고갈 속도에 따라 상태 업데이트 (루프에서 상태 동기화)"""
        # 루프 강도 업데이트
        loop_strength = self.loop.get_strength()
        if loop_strength > 0:
            self.depletion_rate = loop_strength
        
        # 루프 상태에서 동기화
        energy_state = self.loop.energy_state
        self.state.current_energy = energy_state.current_energy
        self.state.energy_depletion_rate = energy_state.energy_depletion_rate
        self.state.recovery_rate = energy_state.recovery_rate
        self.state.sleep_quality = energy_state.sleep_quality
        self.state.circadian_rhythm = energy_state.circadian_rhythm
    
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
        # 루프를 사용하여 에너지 업데이트
        result = self.loop.update_energy(cognitive_load, stress_level, dt)
        
        # 상태 동기화
        self._update_state_from_rate()
        
        # 결과 반환 (호환성 유지)
        return {
            'current_energy': result['current_energy'],
            'energy_change': result['energy_change'],
            'consumption': result['consumption'],
            'recovery': result['recovery'],
            'depletion_rate': result['depletion_rate'],
            'recovery_rate': result['recovery_rate']
        }
    
    def get_energy_score(self) -> float:
        """
        에너지 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            에너지 점수 (낮을수록 에너지 고갈)
        """
        # 루프에서 점수 가져오기
        return self.loop.get_energy_score()

