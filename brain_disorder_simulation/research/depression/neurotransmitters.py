"""
신경전달물질 시스템 모델링

우울증 연구를 위한 신경전달물질 시스템 구현
연구 근거: 실제 우울증 연구 자료 기반

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class DopamineState:
    """도파민 시스템 상태"""
    tonic_dopamine: float = 1.0      # 기본 도파민 수준 (0.0 ~ 1.0)
    phasic_dopamine: float = 1.0     # 반응성 도파민 (0.0 ~ 1.0)
    reward_sensitivity: float = 1.0   # 보상 민감도 (0.0 ~ 1.0)
    reward_prediction_error: float = 0.0  # 보상 예측 오차


@dataclass
class SerotoninState:
    """세로토닌 시스템 상태"""
    serotonin_level: float = 1.0           # 세로토닌 수준 (0.0 ~ 1.0)
    reuptake_inhibition: float = 0.0       # 재흡수 억제 (SSRI 효과, 0.0 ~ 1.0)
    mood_regulation: float = 1.0           # 기분 조절 능력 (0.0 ~ 1.0)
    sleep_quality_factor: float = 1.0      # 수면 질 영향 인자


@dataclass
class NorepinephrineState:
    """노르에피네프린 시스템 상태"""
    norepinephrine_level: float = 1.0      # 노르에피네프린 수준 (0.0 ~ 1.0)
    arousal_level: float = 1.0             # 각성 수준 (0.0 ~ 1.0)
    stress_response: float = 1.0           # 스트레스 반응 (0.0 ~ 1.0)
    attention_focus: float = 1.0           # 주의 집중 (0.0 ~ 1.0)


class DopamineSystem:
    """
    도파민 시스템 모델링
    
    연구 근거:
    - 우울증에서 도파민 보상 경로의 기능 저하
    - Tonic dopamine 감소 (기본 도파민 수준)
    - Phasic dopamine 반응 약화 (보상 반응)
    - 보상 민감도 감소 (무쾌감증)
    
    참고 문헌:
    - Nestler & Carlezon (2006) - Dopamine and depression
    - Treadway & Zald (2011) - Reconsidering anhedonia in depression
    """
    
    def __init__(self, 
                 initial_tonic: float = 1.0,
                 initial_phasic: float = 1.0,
                 rng: Optional[np.random.Generator] = None):
        """
        도파민 시스템 초기화
        
        Args:
            initial_tonic: 초기 Tonic dopamine 수준
            initial_phasic: 초기 Phasic dopamine 수준
            rng: 난수 생성기
        """
        self.state = DopamineState(
            tonic_dopamine=np.clip(initial_tonic, 0.0, 1.0),
            phasic_dopamine=np.clip(initial_phasic, 0.0, 1.0),
            reward_sensitivity=1.0
        )
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 동역학 파라미터
        self.tonic_decay_rate = 0.99      # Tonic dopamine 감쇠율
        self.phasic_decay_rate = 0.95      # Phasic dopamine 감쇠율
        self.reward_learning_rate = 0.1    # 보상 학습률
        
    def update_from_depression(self, depression_level: float):
        """
        우울증 수준에 따른 도파민 변화
        
        연구 근거:
        - 우울증 수준이 높을수록 도파민 시스템 기능 저하
        - Tonic dopamine: 1.0 → 0.5 (50% 감소)
        - Phasic dopamine: 1.0 → 0.4 (60% 감소)
        - 보상 민감도: 1.0 → 0.3 (70% 감소)
        
        Args:
            depression_level: 우울증 수준 (0.0 ~ 1.0)
        """
        depression_level = np.clip(depression_level, 0.0, 1.0)
        
        # Tonic dopamine 감소 (1.0 → 0.5)
        target_tonic = 1.0 - (depression_level * 0.5)
        self.state.tonic_dopamine = np.clip(
            self.state.tonic_dopamine * 0.9 + target_tonic * 0.1,
            0.0, 1.0
        )
        
        # Phasic dopamine 반응 약화 (1.0 → 0.4)
        target_phasic = 1.0 - (depression_level * 0.6)
        self.state.phasic_dopamine = np.clip(
            self.state.phasic_dopamine * 0.9 + target_phasic * 0.1,
            0.0, 1.0
        )
        
        # 보상 민감도 감소 (1.0 → 0.3)
        target_sensitivity = 1.0 - (depression_level * 0.7)
        self.state.reward_sensitivity = np.clip(
            self.state.reward_sensitivity * 0.9 + target_sensitivity * 0.1,
            0.0, 1.0
        )
    
    def process_reward(self, reward_value: float, expected_reward: float = 0.0):
        """
        보상 처리 및 보상 예측 오차 계산
        
        연구 근거:
        - Phasic dopamine은 보상 예측 오차(RPE)에 반응
        - RPE = 실제 보상 - 예상 보상
        - 우울증에서는 RPE 반응이 약화됨
        
        Args:
            reward_value: 실제 보상 값 (0.0 ~ 1.0)
            expected_reward: 예상 보상 값 (0.0 ~ 1.0)
        
        Returns:
            보상 처리 결과
        """
        # 보상 예측 오차 (Reward Prediction Error)
        rpe = reward_value - expected_reward
        
        # Phasic dopamine 반응 (RPE에 비례, 우울증에서는 약화)
        phasic_response = rpe * self.state.phasic_dopamine
        
        # 보상 민감도 적용
        perceived_reward = reward_value * self.state.reward_sensitivity
        
        # 상태 업데이트
        self.state.reward_prediction_error = rpe
        
        # Phasic dopamine 업데이트 (RPE 반응)
        if rpe > 0:
            # 긍정적 RPE → Phasic dopamine 증가
            self.state.phasic_dopamine = min(1.0,
                self.state.phasic_dopamine + phasic_response * 0.1)
        else:
            # 부정적 RPE → Phasic dopamine 감소
            self.state.phasic_dopamine = max(0.0,
                self.state.phasic_dopamine + phasic_response * 0.1)
        
        return {
            'rpe': rpe,
            'phasic_response': phasic_response,
            'perceived_reward': perceived_reward,
            'reward_sensitivity': self.state.reward_sensitivity
        }
    
    def update_temporal(self, dt: float = 0.1):
        """
        시간에 따른 도파민 시스템 업데이트
        
        Args:
            dt: 시간 간격
        """
        # Tonic dopamine 자연 감쇠
        self.state.tonic_dopamine *= (self.tonic_decay_rate ** dt)
        
        # Phasic dopamine 자연 감쇠 (더 빠름)
        self.state.phasic_dopamine *= (self.phasic_decay_rate ** dt)
        
        # 보상 예측 오차 감쇠
        self.state.reward_prediction_error *= 0.9
    
    def get_dopamine_level(self) -> float:
        """
        전체 도파민 수준 계산
        
        Returns:
            도파민 수준 (0.0 ~ 1.0)
        """
        # Tonic과 Phasic의 가중 평균
        return (self.state.tonic_dopamine * 0.7 + 
                self.state.phasic_dopamine * 0.3)


class SerotoninSystem:
    """
    세로토닌 시스템 모델링
    
    연구 근거:
    - 우울증에서 세로토닌 전달 감소
    - SSRI (Selective Serotonin Reuptake Inhibitor) 효과
    - 기분 조절 및 수면 질에 영향
    
    참고 문헌:
    - Cowen & Browning (2015) - Serotonin and depression
    - Harmer et al. (2017) - SSRI mechanisms
    """
    
    def __init__(self,
                 initial_level: float = 1.0,
                 rng: Optional[np.random.Generator] = None):
        """
        세로토닌 시스템 초기화
        
        Args:
            initial_level: 초기 세로토닌 수준
            rng: 난수 생성기
        """
        self.state = SerotoninState(
            serotonin_level=np.clip(initial_level, 0.0, 1.0)
        )
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 동역학 파라미터
        self.serotonin_decay_rate = 0.98
        self.reuptake_rate = 0.1  # 재흡수 속도
        
    def update_from_depression(self, depression_level: float):
        """
        우울증 수준에 따른 세로토닌 변화
        
        연구 근거:
        - 우울증 수준이 높을수록 세로토닌 수준 감소
        - 세로토닌: 1.0 → 0.6 (40% 감소)
        - 기분 조절 능력 감소
        
        Args:
            depression_level: 우울증 수준 (0.0 ~ 1.0)
        """
        depression_level = np.clip(depression_level, 0.0, 1.0)
        
        # 세로토닌 수준 감소 (1.0 → 0.6)
        target_level = 1.0 - (depression_level * 0.4)
        self.state.serotonin_level = np.clip(
            self.state.serotonin_level * 0.9 + target_level * 0.1,
            0.0, 1.0
        )
        
        # 기분 조절 능력 감소
        target_mood = 1.0 - (depression_level * 0.5)
        self.state.mood_regulation = np.clip(
            self.state.mood_regulation * 0.9 + target_mood * 0.1,
            0.0, 1.0
        )
        
        # 수면 질 영향
        target_sleep = 1.0 - (depression_level * 0.4)
        self.state.sleep_quality_factor = np.clip(
            self.state.sleep_quality_factor * 0.9 + target_sleep * 0.1,
            0.0, 1.0
        )
    
    def apply_ssri(self, dose: float):
        """
        SSRI 투여 효과
        
        연구 근거:
        - SSRI는 세로토닌 재흡수를 억제하여 시냅스 간 세로토닌 증가
        - 투여량에 비례하여 효과 증가
        
        Args:
            dose: SSRI 투여량 (0.0 ~ 1.0)
        
        Returns:
            SSRI 효과 정보
        """
        dose = np.clip(dose, 0.0, 1.0)
        
        # 재흡수 억제 증가
        self.state.reuptake_inhibition = np.clip(
            self.state.reuptake_inhibition * 0.8 + dose * 0.2,
            0.0, 1.0
        )
        
        # 세로토닌 수준 증가 (재흡수 억제로 인한)
        serotonin_increase = dose * 0.3 * (1.0 - self.state.reuptake_inhibition)
        self.state.serotonin_level = min(1.0,
            self.state.serotonin_level + serotonin_increase)
        
        return {
            'reuptake_inhibition': self.state.reuptake_inhibition,
            'serotonin_increase': serotonin_increase,
            'current_serotonin': self.state.serotonin_level
        }
    
    def update_temporal(self, dt: float = 0.1):
        """
        시간에 따른 세로토닌 시스템 업데이트
        
        Args:
            dt: 시간 간격
        """
        # 재흡수로 인한 세로토닌 감소 (SSRI 효과가 있으면 감소율 낮음)
        reuptake_effect = self.reuptake_rate * (1.0 - self.state.reuptake_inhibition)
        self.state.serotonin_level = max(0.0,
            self.state.serotonin_level - reuptake_effect * dt)
        
        # 자연 감쇠
        self.state.serotonin_level *= (self.serotonin_decay_rate ** dt)
        
        # 재흡수 억제 감쇠 (SSRI 효과 지속 시간)
        self.state.reuptake_inhibition *= 0.999


class NorepinephrineSystem:
    """
    노르에피네프린 시스템 모델링
    
    연구 근거:
    - 각성 및 에너지 조절
    - 스트레스 반응
    - 주의 집중에 영향
    
    참고 문헌:
    - Moret & Briley (2011) - Norepinephrine and depression
    - Delgado (2004) - Norepinephrine and stress
    """
    
    def __init__(self,
                 initial_level: float = 1.0,
                 rng: Optional[np.random.Generator] = None):
        """
        노르에피네프린 시스템 초기화
        
        Args:
            initial_level: 초기 노르에피네프린 수준
            rng: 난수 생성기
        """
        self.state = NorepinephrineState(
            norepinephrine_level=np.clip(initial_level, 0.0, 1.0)
        )
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 동역학 파라미터
        self.norepinephrine_decay_rate = 0.97
        self.stress_response_rate = 0.2
        
    def update_from_depression(self, depression_level: float):
        """
        우울증 수준에 따른 노르에피네프린 변화
        
        연구 근거:
        - 우울증 수준이 높을수록 노르에피네프린 수준 감소
        - 노르에피네프린: 1.0 → 0.7 (30% 감소)
        - 각성 수준 감소
        - 주의 집중 감소
        
        Args:
            depression_level: 우울증 수준 (0.0 ~ 1.0)
        """
        depression_level = np.clip(depression_level, 0.0, 1.0)
        
        # 노르에피네프린 수준 감소 (1.0 → 0.7)
        target_level = 1.0 - (depression_level * 0.3)
        self.state.norepinephrine_level = np.clip(
            self.state.norepinephrine_level * 0.9 + target_level * 0.1,
            0.0, 1.0
        )
        
        # 각성 수준 감소 (1.0 → 0.6)
        target_arousal = 1.0 - (depression_level * 0.4)
        self.state.arousal_level = np.clip(
            self.state.arousal_level * 0.9 + target_arousal * 0.1,
            0.0, 1.0
        )
        
        # 주의 집중 감소
        target_attention = 1.0 - (depression_level * 0.5)
        self.state.attention_focus = np.clip(
            self.state.attention_focus * 0.9 + target_attention * 0.1,
            0.0, 1.0
        )
    
    def respond_to_stress(self, stress_level: float):
        """
        스트레스에 대한 노르에피네프린 반응
        
        연구 근거:
        - 스트레스에 대한 노르에피네프린 반응
        - 우울증에서는 스트레스 반응이 과도하거나 부족할 수 있음
        
        Args:
            stress_level: 스트레스 수준 (0.0 ~ 1.0)
        
        Returns:
            스트레스 반응 정보
        """
        stress_level = np.clip(stress_level, 0.0, 1.0)
        
        # 노르에피네프린 증가 (스트레스 반응)
        norepinephrine_increase = stress_level * self.stress_response_rate
        self.state.norepinephrine_level = min(1.0,
            self.state.norepinephrine_level + norepinephrine_increase)
        
        # 각성 수준 증가
        arousal_increase = stress_level * 0.3
        self.state.arousal_level = min(1.0,
            self.state.arousal_level + arousal_increase)
        
        # 스트레스 반응 능력
        self.state.stress_response = min(1.0,
            self.state.stress_response + stress_level * 0.1)
        
        return {
            'norepinephrine_increase': norepinephrine_increase,
            'arousal_increase': arousal_increase,
            'current_norepinephrine': self.state.norepinephrine_level
        }
    
    def update_temporal(self, dt: float = 0.1):
        """
        시간에 따른 노르에피네프린 시스템 업데이트
        
        Args:
            dt: 시간 간격
        """
        # 자연 감쇠
        self.state.norepinephrine_level *= (self.norepinephrine_decay_rate ** dt)
        self.state.arousal_level *= 0.99
        self.state.stress_response *= 0.995


class NeurotransmitterSystem:
    """
    통합 신경전달물질 시스템
    
    도파민, 세로토닌, 노르에피네프린 시스템을 통합 관리
    """
    
    def __init__(self, rng: Optional[np.random.Generator] = None):
        """
        신경전달물질 시스템 초기화
        
        Args:
            rng: 난수 생성기
        """
        self.dopamine = DopamineSystem(rng=rng)
        self.serotonin = SerotoninSystem(rng=rng)
        self.norepinephrine = NorepinephrineSystem(rng=rng)
    
    def update_from_depression(self, depression_level: float):
        """
        우울증 수준에 따른 모든 신경전달물질 시스템 업데이트
        
        Args:
            depression_level: 우울증 수준 (0.0 ~ 1.0)
        """
        self.dopamine.update_from_depression(depression_level)
        self.serotonin.update_from_depression(depression_level)
        self.norepinephrine.update_from_depression(depression_level)
    
    def update_temporal(self, dt: float = 0.1):
        """
        시간에 따른 모든 신경전달물질 시스템 업데이트
        
        Args:
            dt: 시간 간격
        """
        self.dopamine.update_temporal(dt)
        self.serotonin.update_temporal(dt)
        self.norepinephrine.update_temporal(dt)
    
    def get_system_state(self) -> Dict:
        """
        전체 신경전달물질 시스템 상태 반환
        
        Returns:
            시스템 상태 딕셔너리
        """
        return {
            'dopamine': {
                'tonic': self.dopamine.state.tonic_dopamine,
                'phasic': self.dopamine.state.phasic_dopamine,
                'reward_sensitivity': self.dopamine.state.reward_sensitivity,
                'rpe': self.dopamine.state.reward_prediction_error
            },
            'serotonin': {
                'level': self.serotonin.state.serotonin_level,
                'reuptake_inhibition': self.serotonin.state.reuptake_inhibition,
                'mood_regulation': self.serotonin.state.mood_regulation,
                'sleep_quality_factor': self.serotonin.state.sleep_quality_factor
            },
            'norepinephrine': {
                'level': self.norepinephrine.state.norepinephrine_level,
                'arousal': self.norepinephrine.state.arousal_level,
                'stress_response': self.norepinephrine.state.stress_response,
                'attention_focus': self.norepinephrine.state.attention_focus
            }
        }

