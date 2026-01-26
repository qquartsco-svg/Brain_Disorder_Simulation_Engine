"""
우울증 특화 엔진

Cookiie Brain Engine 기반 우울증 메커니즘 시뮬레이션
목적: "왜 이런 상황이 발생할 수 있는가?" 원인 분석

⚠️ 주의: 이 엔진은 치료 도구가 아닙니다.
- 진단 도구 아님
- 치료 솔루션 제시 아님
- 패턴 관측 및 메커니즘 분석 목적

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass


@dataclass
class NegativeBiasState:
    """부정적 편향 상태"""
    negative_amplification: float = 1.0  # 부정적 자극 증폭 배수
    positive_dampening: float = 1.0      # 긍정적 자극 감쇠 배수
    threat_sensitivity: float = 1.0       # 위협 민감도
    memory_bias: float = 0.0             # 부정적 기억 편향
    rumination_strength: float = 0.0     # 반추 강도


@dataclass
class CognitiveControlState:
    """인지 제어 상태"""
    inhibition_strength: float = 1.0      # 억제 제어 강도
    cognitive_flexibility: float = 1.0    # 인지적 유연성
    working_memory_capacity: float = 1.0 # 작업 기억 용량
    negative_thought_loop: float = 0.0   # 부정적 사고 루프 강도
    executive_function: float = 1.0       # 실행 기능


@dataclass
class EnergyDepletionState:
    """에너지 고갈 상태"""
    current_energy: float = 100.0         # 현재 에너지 수준
    energy_depletion_rate: float = 0.0    # 에너지 고갈 속도
    recovery_rate: float = 0.0           # 회복 속도
    sleep_quality: float = 1.0            # 수면 질
    circadian_rhythm: float = 1.0         # 일주기 리듬


@dataclass
class MotivationState:
    """동기 상태"""
    reward_sensitivity: float = 1.0       # 보상 민감도
    motivation_level: float = 1.0         # 동기 수준
    goal_directed_behavior: float = 1.0   # 목표 지향 행동
    anhedonia: float = 0.0                # 무쾌감증 (anhedonia)
    effort_cost: float = 1.0              # 노력 비용


class NegativeBiasEngine:
    """
    부정적 편향 엔진 (Amygdala 기반)
    
    핵심 질문: "왜 부정적 편향이 발생하는가?"
    
    메커니즘:
    1. 부정적 자극에 대한 과민 반응
    2. 긍정적 자극에 대한 둔감 반응
    3. 위협 감지 과민화
    4. 부정적 기억 편향
    5. 반추 (rumination) 강화
    """
    
    def __init__(self, 
                 negative_bias_strength: float = 0.0,
                 rng: Optional[np.random.Generator] = None):
        """
        부정적 편향 엔진 초기화
        
        Args:
            negative_bias_strength: 부정적 편향 강도 (0.0 ~ 1.0)
            rng: 난수 생성기
        """
        self.negative_bias_strength = np.clip(negative_bias_strength, 0.0, 1.0)
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 상태 초기화
        self.state = NegativeBiasState()
        
        # 파라미터
        self.negative_amplification_base = 1.0
        self.positive_dampening_base = 1.0
        self.threat_threshold_base = 0.5
        
        # 동역학 파라미터
        self.rumination_decay = 0.95  # 반추 감쇠율
        self.memory_bias_decay = 0.98  # 기억 편향 감쇠율
        
        # 초기 상태 설정
        self._update_state_from_strength()
    
    def _update_state_from_strength(self):
        """편향 강도에 따라 상태 업데이트"""
        strength = self.negative_bias_strength
        
        # 부정적 자극 증폭 (1.0 ~ 2.5)
        self.state.negative_amplification = 1.0 + (strength * 1.5)
        
        # 긍정적 자극 감쇠 (1.0 ~ 0.3)
        self.state.positive_dampening = 1.0 - (strength * 0.7)
        
        # 위협 민감도 증가 (1.0 ~ 2.0)
        self.state.threat_sensitivity = 1.0 + (strength * 1.0)
        
        # 기억 편향 (0.0 ~ 0.8)
        self.state.memory_bias = strength * 0.8
    
    def process_stimulus(self, 
                        stimulus_valence: float,
                        stimulus_intensity: float = 1.0,
                        time_elapsed: float = 0.0) -> Dict:
        """
        자극 처리 (부정적 편향 적용)
        
        Args:
            stimulus_valence: 자극의 정서가 (-1.0: 매우 부정적, 0.0: 중립, 1.0: 매우 긍정적)
            stimulus_intensity: 자극 강도
            time_elapsed: 경과 시간
        
        Returns:
            처리된 자극 정보
        """
        # 변수 초기화
        amplified_intensity = stimulus_intensity
        dampened_intensity = stimulus_intensity
        perceived_valence = stimulus_valence
        
        # 부정적 자극 처리
        if stimulus_valence < 0:
            # 부정적 자극 증폭
            amplified_intensity = stimulus_intensity * self.state.negative_amplification
            perceived_valence = stimulus_valence * self.state.negative_amplification
            
            # 반추 강화 (부정적 자극에 대한 반복적 사고)
            self.state.rumination_strength = min(1.0, 
                self.state.rumination_strength + 0.1 * amplified_intensity)
            
            # 기억 편향 업데이트
            self.state.memory_bias = min(1.0,
                self.state.memory_bias + 0.05 * amplified_intensity)
        
        # 긍정적 자극 처리
        elif stimulus_valence > 0:
            # 긍정적 자극 감쇠
            dampened_intensity = stimulus_intensity * self.state.positive_dampening
            perceived_valence = stimulus_valence * self.state.positive_dampening
            
            # 반추 약화 (긍정적 자극은 빠르게 사라짐)
            self.state.rumination_strength *= self.rumination_decay
        
        # 중립 자극 처리
        else:
            # 중립 자극도 약간 부정적으로 해석될 수 있음
            if self.state.rumination_strength > 0.3:
                perceived_valence = -0.1 * self.state.rumination_strength
                dampened_intensity = stimulus_intensity
                amplified_intensity = stimulus_intensity
            else:
                perceived_valence = 0.0
                dampened_intensity = stimulus_intensity
                amplified_intensity = stimulus_intensity
        
        # 위협 감지 (부정적 자극에 대한 과민 반응)
        threat_detected = False
        if stimulus_valence < -0.3:
            threat_probability = (abs(stimulus_valence) * 
                               self.state.threat_sensitivity * 
                               stimulus_intensity)
            if threat_probability > self.threat_threshold_base:
                threat_detected = True
        
        # 최종 강도 결정
        if stimulus_valence < 0:
            final_intensity = amplified_intensity
        elif stimulus_valence > 0:
            final_intensity = dampened_intensity
        else:
            final_intensity = stimulus_intensity
        
        return {
            'perceived_valence': np.clip(perceived_valence, -1.0, 1.0),
            'perceived_intensity': final_intensity,
            'threat_detected': threat_detected,
            'rumination_triggered': stimulus_valence < 0,
            'bias_applied': True
        }
    
    def update_rumination(self, dt: float = 0.1):
        """
        반추 업데이트 (시간에 따른 자연적 감쇠)
        
        Args:
            dt: 시간 간격
        """
        # 반추는 시간이 지나면서 점차 감쇠하지만, 완전히 사라지지 않음
        self.state.rumination_strength *= (self.rumination_decay ** (dt * 10))
        
        # 기억 편향도 점차 감쇠
        self.state.memory_bias *= (self.memory_bias_decay ** (dt * 10))
    
    def get_bias_score(self) -> float:
        """
        부정적 편향 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            편향 점수 (높을수록 부정적 편향 강함)
        """
        score = (
            (self.state.negative_amplification - 1.0) / 1.5 * 0.3 +
            (1.0 - self.state.positive_dampening) / 0.7 * 0.3 +
            (self.state.threat_sensitivity - 1.0) / 1.0 * 0.2 +
            self.state.rumination_strength * 0.1 +
            self.state.memory_bias * 0.1
        )
        return np.clip(score, 0.0, 1.0)


class CognitiveControlEngine:
    """
    인지 제어 엔진 (Prefrontal Cortex 기반)
    
    핵심 질문: "왜 인지 제어가 약화되는가?"
    
    메커니즘:
    1. 억제 제어 약화
    2. 인지적 유연성 감소
    3. 작업 기억 용량 감소
    4. 부정적 사고 루프 형성
    5. 실행 기능 저하
    """
    
    def __init__(self,
                 control_impairment: float = 0.0,
                 rng: Optional[np.random.Generator] = None):
        """
        인지 제어 엔진 초기화
        
        Args:
            control_impairment: 제어 약화 정도 (0.0 ~ 1.0)
            rng: 난수 생성기
        """
        self.control_impairment = np.clip(control_impairment, 0.0, 1.0)
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 상태 초기화
        self.state = CognitiveControlState()
        
        # 동역학 파라미터
        self.negative_loop_gain = 0.05  # 부정적 루프 강화율
        self.negative_loop_decay = 0.98  # 부정적 루프 감쇠율
        
        # 초기 상태 설정
        self._update_state_from_impairment()
    
    def _update_state_from_impairment(self):
        """약화 정도에 따라 상태 업데이트"""
        impairment = self.control_impairment
        
        # 억제 제어 약화 (1.0 ~ 0.3)
        self.state.inhibition_strength = 1.0 - (impairment * 0.7)
        
        # 인지적 유연성 감소 (1.0 ~ 0.4)
        self.state.cognitive_flexibility = 1.0 - (impairment * 0.6)
        
        # 작업 기억 용량 감소 (1.0 ~ 0.5)
        self.state.working_memory_capacity = 1.0 - (impairment * 0.5)
        
        # 실행 기능 저하 (1.0 ~ 0.4)
        self.state.executive_function = 1.0 - (impairment * 0.6)
    
    def process_negative_thought(self,
                               thought_intensity: float,
                               time_elapsed: float = 0.0) -> Dict:
        """
        부정적 사고 처리
        
        Args:
            thought_intensity: 사고 강도
            time_elapsed: 경과 시간
        
        Returns:
            처리 결과
        """
        # 억제 제어 시도
        inhibition_success = False
        if self.state.inhibition_strength > 0.5:
            # 억제 성공 확률
            inhibition_prob = self.state.inhibition_strength
            if self.rng.random() < inhibition_prob:
                inhibition_success = True
                # 억제 성공 시 루프 약화
                self.state.negative_thought_loop *= 0.9
        else:
            # 억제 제어가 약하면 실패
            inhibition_success = False
        
        # 억제 실패 시 부정적 루프 강화
        if not inhibition_success:
            self.state.negative_thought_loop = min(1.0,
                self.state.negative_thought_loop + 
                self.negative_loop_gain * thought_intensity)
        
        # 인지적 유연성에 따른 대안 사고 생성 능력
        alternative_thinking = self.state.cognitive_flexibility
        
        return {
            'inhibition_success': inhibition_success,
            'negative_loop_strength': self.state.negative_thought_loop,
            'alternative_thinking': alternative_thinking,
            'control_impaired': self.control_impairment > 0.3
        }
    
    def attempt_cognitive_control(self, task_difficulty: float = 0.5) -> Dict:
        """
        인지 제어 시도
        
        Args:
            task_difficulty: 작업 난이도 (0.0 ~ 1.0)
        
        Returns:
            제어 결과
        """
        # 실행 기능에 따른 성공 확률
        base_success = self.state.executive_function
        difficulty_factor = 1.0 - (task_difficulty * 0.5)
        success_probability = base_success * difficulty_factor
        
        # 작업 기억 용량에 따른 처리 능력
        processing_capacity = self.state.working_memory_capacity
        
        # 실제 성공 여부
        success = self.rng.random() < success_probability
        
        # 실패 시 부정적 루프 약간 강화
        if not success:
            self.state.negative_thought_loop = min(1.0,
                self.state.negative_thought_loop + 0.05)
        
        return {
            'success': success,
            'success_probability': success_probability,
            'processing_capacity': processing_capacity,
            'executive_function': self.state.executive_function
        }
    
    def update_negative_loop(self, dt: float = 0.1):
        """
        부정적 사고 루프 업데이트
        
        Args:
            dt: 시간 간격
        """
        # 자연적 감쇠 (하지만 완전히 사라지지 않음)
        self.state.negative_thought_loop *= (self.negative_loop_decay ** (dt * 10))
        
        # 억제 제어가 약하면 루프가 더 오래 지속됨
        if self.state.inhibition_strength < 0.5:
            self.state.negative_thought_loop *= 1.01  # 약간 증가
    
    def get_control_score(self) -> float:
        """
        인지 제어 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            제어 점수 (낮을수록 제어 약화)
        """
        score = (
            self.state.inhibition_strength * 0.3 +
            self.state.cognitive_flexibility * 0.2 +
            self.state.working_memory_capacity * 0.2 +
            self.state.executive_function * 0.2 +
            (1.0 - self.state.negative_thought_loop) * 0.1
        )
        return np.clip(score, 0.0, 1.0)


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


class MotivationEngine:
    """
    동기 엔진 (Basal Ganglia 기반)
    
    핵심 질문: "왜 동기가 사라지는가?"
    
    메커니즘:
    1. 보상 민감도 감소
    2. 동기 수준 저하
    3. 목표 지향 행동 감소
    4. 무쾌감증 (anhedonia)
    5. 노력 비용 증가
    """
    
    def __init__(self,
                 motivation_deficit: float = 0.0,
                 rng: Optional[np.random.Generator] = None):
        """
        동기 엔진 초기화
        
        Args:
            motivation_deficit: 동기 결핍 정도 (0.0 ~ 1.0)
            rng: 난수 생성기
        """
        self.motivation_deficit = np.clip(motivation_deficit, 0.0, 1.0)
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 상태 초기화
        self.state = MotivationState()
        
        # 파라미터
        self.base_reward_sensitivity = 1.0
        
        # 초기 상태 설정
        self._update_state_from_deficit()
    
    def _update_state_from_deficit(self):
        """결핍 정도에 따라 상태 업데이트"""
        deficit = self.motivation_deficit
        
        # 보상 민감도 감소 (1.0 ~ 0.3)
        self.state.reward_sensitivity = 1.0 - (deficit * 0.7)
        
        # 동기 수준 저하 (1.0 ~ 0.2)
        self.state.motivation_level = 1.0 - (deficit * 0.8)
        
        # 목표 지향 행동 감소 (1.0 ~ 0.3)
        self.state.goal_directed_behavior = 1.0 - (deficit * 0.7)
        
        # 무쾌감증 (0.0 ~ 0.8)
        self.state.anhedonia = deficit * 0.8
        
        # 노력 비용 증가 (1.0 ~ 2.5)
        self.state.effort_cost = 1.0 + (deficit * 1.5)
    
    def process_reward(self,
                      reward_value: float,
                      effort_required: float = 0.5) -> Dict:
        """
        보상 처리
        
        Args:
            reward_value: 보상 가치 (0.0 ~ 1.0)
            effort_required: 필요한 노력 (0.0 ~ 1.0)
        
        Returns:
            보상 처리 결과
        """
        # 보상 민감도 적용
        perceived_reward = reward_value * self.state.reward_sensitivity
        
        # 무쾌감증 적용 (보상에 대한 즐거움 감소)
        pleasure = perceived_reward * (1.0 - self.state.anhedonia)
        
        # 노력 비용 계산
        effort_cost = effort_required * self.state.effort_cost
        
        # 동기 계산 (보상 - 비용)
        motivation_gain = pleasure - effort_cost
        
        # 동기 업데이트
        if motivation_gain > 0:
            self.state.motivation_level = min(1.0,
                self.state.motivation_level + motivation_gain * 0.1)
        else:
            # 비용이 더 크면 동기 감소
            self.state.motivation_level = max(0.0,
                self.state.motivation_level + motivation_gain * 0.1)
        
        # 목표 지향 행동 가능 여부
        can_engage = (self.state.motivation_level > 0.3 and 
                     motivation_gain > -0.2)
        
        return {
            'perceived_reward': perceived_reward,
            'pleasure': pleasure,
            'effort_cost': effort_cost,
            'motivation_gain': motivation_gain,
            'can_engage': can_engage,
            'anhedonia_effect': self.state.anhedonia
        }
    
    def evaluate_action(self,
                       expected_reward: float,
                       effort_required: float = 0.5,
                       delay: float = 0.0) -> Dict:
        """
        행동 평가 (할 가치가 있는가?)
        
        Args:
            expected_reward: 예상 보상
            effort_required: 필요한 노력
            delay: 지연 시간
        
        Returns:
            행동 평가 결과
        """
        # 보상 민감도 적용
        perceived_reward = expected_reward * self.state.reward_sensitivity
        
        # 무쾌감증 적용
        pleasure = perceived_reward * (1.0 - self.state.anhedonia)
        
        # 노력 비용
        effort_cost = effort_required * self.state.effort_cost
        
        # 지연 할인 (시간이 지날수록 보상 가치 감소)
        delay_discount = np.exp(-delay * 0.5)
        discounted_pleasure = pleasure * delay_discount
        
        # 총 가치
        total_value = discounted_pleasure - effort_cost
        
        # 행동 결정
        should_act = total_value > 0.0 and self.state.motivation_level > 0.2
        
        return {
            'total_value': total_value,
            'should_act': should_act,
            'motivation_sufficient': self.state.motivation_level > 0.3,
            'goal_directed': self.state.goal_directed_behavior > 0.5
        }
    
    def get_motivation_score(self) -> float:
        """
        동기 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            동기 점수 (낮을수록 동기 결핍)
        """
        score = (
            self.state.reward_sensitivity * 0.3 +
            self.state.motivation_level * 0.3 +
            self.state.goal_directed_behavior * 0.2 +
            (1.0 - self.state.anhedonia) * 0.1 +
            (2.0 - self.state.effort_cost) / 1.5 * 0.1
        )
        return np.clip(score, 0.0, 1.0)

