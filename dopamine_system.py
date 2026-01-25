"""
도파민 시스템 모델

ADHD의 핵심인 도파민 부족/불균형을 모델링
"""

import numpy as np
from typing import Dict, Optional, List
from collections import deque


class DopamineSystem:
    """
    도파민 시스템 모델
    
    ADHD는 도파민 부족/불균형이 핵심
    """
    
    def __init__(self, rng: Optional[np.random.Generator] = None,
                 adhd_deficit: float = 0.3):
        """
        도파민 시스템 초기화
        
        Args:
            rng: 재현 가능한 랜덤 생성기
            adhd_deficit: ADHD 도파민 부족 비율 (기본값: 0.3 = 30%)
        """
        # RNG (재현성 보장)
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 도파민 레벨
        self.tonic_dopamine = 0.5  # 기저 도파민 (정상: 0.5-0.7)
        self.phasic_dopamine = 0.0  # 순간 도파민
        self.current_dopamine = 0.5  # 현재 도파민 농도
        
        # ADHD 특성
        self.adhd_dopamine_deficit = adhd_deficit  # ADHD는 30% 부족 (기본값)
        self.dopamine_volatility = 0.2  # 변동성 증가
        
        # 히스토리 (CircularBuffer)
        self.dopamine_history = deque(maxlen=1000)
        self.tonic_history = deque(maxlen=1000)
        self.phasic_history = deque(maxlen=1000)
        
        # 시간 추적
        self.time_elapsed = 0.0
        self.last_update_time = 0.0
    
    def update(self, reward_prediction_error: float = 0.0,
               time_elapsed: float = 0.0,
               external_boost: float = 0.0) -> float:
        """
        도파민 업데이트
        
        Args:
            reward_prediction_error: 보상 예측 오차 (RPE)
            time_elapsed: 경과 시간 (초)
            external_boost: 외부 부스트 (약물 등)
        
        Returns:
            current_dopamine: 현재 도파민 농도 (0.0 ~ 1.0)
        """
        self.time_elapsed = time_elapsed
        dt = time_elapsed - self.last_update_time if self.last_update_time > 0 else 0.1
        self.last_update_time = time_elapsed
        
        # 순간 도파민 (RPE 기반)
        phasic = reward_prediction_error * 0.5
        phasic = np.clip(phasic, -0.5, 0.5)  # 범위 제한
        
        # 기저 도파민 (시간에 따른 감소 - ADHD 특성)
        # ADHD는 기저 도파민이 더 빠르게 감소
        decay_rate = 0.01 if self.adhd_dopamine_deficit > 0 else 0.005
        tonic_decay = np.exp(-decay_rate * dt)
        self.tonic_dopamine = self.tonic_dopamine * tonic_decay
        
        # 기저 도파민 회복 (정상 범위로)
        if self.tonic_dopamine < 0.3:
            self.tonic_dopamine += 0.001 * dt  # 느린 회복
        
        # 기저 도파민 상한
        self.tonic_dopamine = min(0.7, self.tonic_dopamine)
        
        # ADHD 특성: 도파민 부족 + 변동성
        base_dopamine = (self.tonic_dopamine + phasic) * (1.0 - self.adhd_dopamine_deficit)
        
        # 변동성 추가 (ADHD 특성)
        volatility_noise = self.rng.normal(0, self.dopamine_volatility)
        
        # 외부 부스트 (약물 등)
        dopamine = base_dopamine + volatility_noise + external_boost
        
        # 범위 제한
        self.current_dopamine = np.clip(dopamine, 0.0, 1.0)
        self.phasic_dopamine = phasic
        
        # 히스토리 저장
        self.dopamine_history.append(self.current_dopamine)
        self.tonic_history.append(self.tonic_dopamine)
        self.phasic_history.append(self.phasic_dopamine)
        
        return self.current_dopamine
    
    def get_effect_on_attention(self) -> float:
        """
        도파민이 주의력에 미치는 효과
        
        Returns:
            attention_decay_multiplier: 주의력 감소율 배수
        """
        # 도파민이 낮으면 주의력 감소율 증가
        if self.current_dopamine < 0.4:
            # 도파민이 매우 낮으면 감소율 크게 증가
            multiplier = 1.0 + (0.4 - self.current_dopamine) * 2.5
            return min(2.5, multiplier)
        else:
            return 1.0
    
    def get_effect_on_impulse(self) -> float:
        """
        도파민이 충동성에 미치는 효과
        
        Returns:
            inhibition_multiplier: 억제력 배수
        """
        # 도파민이 낮으면 억제력 감소
        if self.current_dopamine < 0.4:
            # 도파민이 매우 낮으면 억제력 크게 감소
            multiplier = self.current_dopamine / 0.4
            return max(0.3, multiplier)
        else:
            return 1.0
    
    def get_effect_on_hyperactivity(self) -> float:
        """
        도파민이 과잉행동에 미치는 효과
        
        Returns:
            hyperactivity_multiplier: 과잉행동 배수
        """
        # 도파민이 낮으면 과잉행동 증가 (에너지 불일치)
        if self.current_dopamine < 0.4:
            multiplier = 1.0 + (0.4 - self.current_dopamine) * 1.5
            return min(2.0, multiplier)
        else:
            return 1.0
    
    def get_state(self) -> Dict:
        """
        현재 도파민 상태 반환
        
        Returns:
            상태 딕셔너리
        """
        return {
            'current_dopamine': self.current_dopamine,
            'tonic_dopamine': self.tonic_dopamine,
            'phasic_dopamine': self.phasic_dopamine,
            'adhd_deficit': self.adhd_dopamine_deficit,
            'attention_effect': self.get_effect_on_attention(),
            'impulse_effect': self.get_effect_on_impulse(),
            'hyperactivity_effect': self.get_effect_on_hyperactivity()
        }
    
    def reset(self):
        """도파민 시스템 리셋"""
        self.tonic_dopamine = 0.5
        self.phasic_dopamine = 0.0
        self.current_dopamine = 0.5
        self.time_elapsed = 0.0
        self.last_update_time = 0.0
        self.dopamine_history.clear()
        self.tonic_history.clear()
        self.phasic_history.clear()


class MedicationSimulator:
    """
    약물 효과 시뮬레이터 (기본 구조)
    
    향후 PK/PD 모델로 확장 가능
    """
    
    def __init__(self, rng: Optional[np.random.Generator] = None):
        """
        약물 시뮬레이터 초기화
        
        Args:
            rng: 재현 가능한 랜덤 생성기
        """
        self.rng = rng if rng is not None else np.random.default_rng()
        self.medication_active = False
        self.medication_type = None
        self.dose = 0.0
        self.time_since_dose = 0.0
        
        # 약물 특성 (기본값, 향후 확장 가능)
        self.medications = {
            'methylphenidate': {
                'peak_time': 1.5,  # 최고 농도 시간 (시간)
                'half_life': 3.0,  # 반감기 (시간)
                'dopamine_boost': 0.3,  # 도파민 증가량
                'attention_improvement': 0.4  # 주의력 개선
            },
            'atomoxetine': {
                'peak_time': 2.0,
                'half_life': 5.0,
                'dopamine_boost': 0.2,
                'attention_improvement': 0.3
            }
        }
    
    def administer(self, medication_type: str, dose: float, time: float):
        """
        약물 투여
        
        Args:
            medication_type: 약물 종류
            dose: 투여량
            time: 투여 시간
        """
        if medication_type not in self.medications:
            raise ValueError(f"Unknown medication type: {medication_type}")
        
        self.medication_active = True
        self.medication_type = medication_type
        self.dose = dose
        self.time_since_dose = time
    
    def get_current_effect(self, current_time: float) -> Dict:
        """
        현재 약물 효과 계산
        
        Args:
            current_time: 현재 시간
        
        Returns:
            effect: 도파민 증가, 주의력 개선 등
        """
        if not self.medication_active:
            return {'dopamine_boost': 0.0, 'attention_boost': 0.0, 'concentration': 0.0}
        
        med = self.medications[self.medication_type]
        elapsed = (current_time - self.time_since_dose) / 3600.0  # 초 → 시간 변환
        
        if elapsed < 0:
            return {'dopamine_boost': 0.0, 'attention_boost': 0.0, 'concentration': 0.0}
        
        # 약물 농도 곡선 (1-compartment model)
        if elapsed < med['peak_time']:
            # 상승기
            concentration = (elapsed / med['peak_time']) * (self.dose / 10.0)
        else:
            # 감소기 (지수 감쇠)
            decay = np.exp(-0.693 * (elapsed - med['peak_time']) / med['half_life'])
            concentration = (self.dose / 10.0) * decay
        
        # 농도 범위 제한
        concentration = np.clip(concentration, 0.0, 1.0)
        
        # 효과 계산
        dopamine_boost = med['dopamine_boost'] * concentration
        attention_boost = med['attention_improvement'] * concentration
        
        return {
            'dopamine_boost': dopamine_boost,
            'attention_boost': attention_boost,
            'concentration': concentration
        }
    
    def stop(self):
        """약물 중단"""
        self.medication_active = False
        self.medication_type = None
        self.dose = 0.0
        self.time_since_dose = 0.0

