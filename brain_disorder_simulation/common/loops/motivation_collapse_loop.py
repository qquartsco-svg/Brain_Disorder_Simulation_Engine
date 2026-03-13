"""
동기 붕괴 루프 (Motivation Collapse Loop)

우울증, ADHD, PTSD에서 공통적으로 나타나는 동기 시스템 붕괴 메커니즘

핵심 메커니즘:
보상 민감도 감소 → 무쾌감증 → 동기 수준 저하 → 목표 지향 행동 감소 → 보상 기회 감소 → 보상 민감도 더 감소 (폐루프)

연구 근거:
- Treadway & Zald (2011) - Reward processing in depression
- Der-Avakian & Markou (2012) - Anhedonia in depression
- Pizzagalli (2014) - Reward dysfunction in depression

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass

from .base_loop import BaseLoop, LoopState, LoopParameters


@dataclass
class MotivationCollapseLoopState(LoopState):
    """동기 붕괴 루프 상태"""
    reward_sensitivity: float = 1.0       # 보상 민감도 (0.0 ~ 1.0)
    motivation_level: float = 1.0         # 동기 수준 (0.0 ~ 1.0)
    goal_directed_behavior: float = 1.0   # 목표 지향 행동 (0.0 ~ 1.0)
    anhedonia: float = 0.0                # 무쾌감증 (0.0 ~ 1.0)
    effort_cost: float = 1.0              # 노력 비용 (1.0 ~ 2.5)
    reward_failures: int = 0              # 보상 실패 횟수
    goal_failures: int = 0                # 목표 달성 실패 횟수


class MotivationCollapseLoop(BaseLoop):
    """
    동기 붕괴 루프
    
    우울증, ADHD, PTSD에서 공통적으로 나타나는 동기 시스템 붕괴 메커니즘
    
    루프 메커니즘:
    1. 보상 실패 또는 노력 비용 증가
    2. 보상 민감도 감소
    3. 무쾌감증 증가
    4. 동기 수준 저하
    5. 목표 지향 행동 감소
    6. 보상 기회 감소 → 더 많은 보상 실패
    7. 루프 강화 (폐루프)
    """
    
    def __init__(self,
                 initial_motivation_deficit: float = 0.0,
                 parameters: Optional[LoopParameters] = None,
                 rng: Optional[np.random.Generator] = None):
        """
        동기 붕괴 루프 초기화
        
        Args:
            initial_motivation_deficit: 초기 동기 결핍 정도 (0.0 ~ 1.0)
            parameters: 루프 파라미터
            rng: 난수 생성기
        """
        super().__init__(
            name="MotivationCollapseLoop",
            parameters=parameters,
            rng=rng
        )
        
        # 초기 상태 설정
        self.motivation_state = MotivationCollapseLoopState()
        
        # 초기 결핍 정도 적용
        if initial_motivation_deficit > 0.0:
            self._apply_deficit(initial_motivation_deficit)
    
    def _apply_deficit(self, deficit: float):
        """결핍 정도에 따라 상태 업데이트"""
        deficit = np.clip(deficit, 0.0, 1.0)
        
        # 보상 민감도 감소 (1.0 ~ 0.3)
        self.motivation_state.reward_sensitivity = 1.0 - (deficit * 0.7)
        
        # 동기 수준 저하 (1.0 ~ 0.2)
        self.motivation_state.motivation_level = 1.0 - (deficit * 0.8)
        
        # 목표 지향 행동 감소 (1.0 ~ 0.3)
        self.motivation_state.goal_directed_behavior = 1.0 - (deficit * 0.7)
        
        # 무쾌감증 (0.0 ~ 0.8)
        self.motivation_state.anhedonia = deficit * 0.8
        
        # 노력 비용 증가 (1.0 ~ 2.5)
        self.motivation_state.effort_cost = 1.0 + (deficit * 1.5)
        
        # 루프 강도 설정
        self.state.loop_strength = deficit
    
    def _trigger_condition(self, context: Optional[Dict] = None) -> bool:
        """
        트리거 조건 확인
        
        Args:
            context: 컨텍스트 정보
                - reward_value: 보상 가치 (0.0 ~ 1.0)
                - effort_required: 필요한 노력 (0.0 ~ 1.0)
                - goal_achieved: 목표 달성 여부 (bool)
                - reward_threshold: 보상 임계값 (기본 0.3)
        
        Returns:
            트리거 여부
        """
        if context is None:
            return False
        
        # 보상 실패
        reward_value = context.get('reward_value', 1.0)
        reward_threshold = context.get('reward_threshold', 0.3)
        if reward_value < reward_threshold:
            return True
        
        # 노력 비용이 너무 높음
        effort_required = context.get('effort_required', 0.0)
        if effort_required > 0.7 and self.motivation_state.motivation_level < 0.5:
            return True
        
        # 목표 달성 실패
        goal_achieved = context.get('goal_achieved', True)
        if not goal_achieved and self.motivation_state.goal_directed_behavior < 0.5:
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
        
        # 보상 민감도 감소
        sensitivity_decay = 0.01 * loop_effect * dt
        self.motivation_state.reward_sensitivity = max(
            0.3,
            self.motivation_state.reward_sensitivity - sensitivity_decay
        )
        
        # 무쾌감증 증가
        anhedonia_increase = 0.02 * loop_effect * dt
        self.motivation_state.anhedonia = min(
            0.9,
            self.motivation_state.anhedonia + anhedonia_increase
        )
        
        # 동기 수준 저하
        motivation_decay = 0.015 * loop_effect * dt
        self.motivation_state.motivation_level = max(
            0.1,
            self.motivation_state.motivation_level - motivation_decay
        )
        
        # 목표 지향 행동 감소
        goal_decay = 0.01 * loop_effect * dt
        self.motivation_state.goal_directed_behavior = max(
            0.2,
            self.motivation_state.goal_directed_behavior - goal_decay
        )
        
        # 노력 비용 증가
        effort_increase = 0.01 * loop_effect * dt
        self.motivation_state.effort_cost = min(
            2.5,
            self.motivation_state.effort_cost + effort_increase
        )
        
        # 자연적 감쇠 (매우 느림)
        self.state.loop_strength *= (self.parameters.loop_decay ** (dt * 0.1))
    
    def _apply_loop_effect(self, intensity: float, context: Optional[Dict] = None) -> Dict:
        """
        루프 효과 적용
        
        Args:
            intensity: 효과 강도
            context: 컨텍스트 정보
        
        Returns:
            적용된 효과 정보
        """
        # 루프 강도에 따라 동기 상태 업데이트
        self._update_motivation_from_strength(self.state.loop_strength)
        
        return {
            'reward_sensitivity': self.motivation_state.reward_sensitivity,
            'motivation_level': self.motivation_state.motivation_level,
            'goal_directed_behavior': self.motivation_state.goal_directed_behavior,
            'anhedonia': self.motivation_state.anhedonia,
            'effort_cost': self.motivation_state.effort_cost,
            'loop_strength': self.state.loop_strength
        }
    
    def _update_motivation_from_strength(self, strength: float):
        """
        루프 강도에 따라 동기 상태 업데이트
        
        Args:
            strength: 루프 강도 (0.0 ~ 1.0)
        """
        # 루프 강도에 비례하여 동기 결핍 적용
        self._apply_deficit(strength)
    
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
        perceived_reward = reward_value * self.motivation_state.reward_sensitivity
        
        # 무쾌감증 적용 (보상에 대한 즐거움 감소)
        pleasure = perceived_reward * (1.0 - self.motivation_state.anhedonia)
        
        # 노력 비용 계산
        effort_cost = effort_required * self.motivation_state.effort_cost
        
        # 동기 계산 (보상 - 비용)
        motivation_gain = pleasure - effort_cost
        
        # 동기 업데이트
        if motivation_gain > 0:
            self.motivation_state.motivation_level = min(
                1.0,
                self.motivation_state.motivation_level + motivation_gain * 0.1
            )
        else:
            # 비용이 더 크면 동기 감소 및 루프 트리거
            self.motivation_state.motivation_level = max(
                0.0,
                self.motivation_state.motivation_level + motivation_gain * 0.1
            )
            
            # 보상 실패로 루프 트리거
            self.trigger(
                intensity=abs(motivation_gain),
                context={
                    'reward_value': reward_value,
                    'effort_required': effort_required,
                    'reward_threshold': 0.3
                }
            )
            self.motivation_state.reward_failures += 1
        
        # 목표 지향 행동 가능 여부
        can_engage = (self.motivation_state.motivation_level > 0.3 and 
                     motivation_gain > -0.2)
        
        return {
            'perceived_reward': perceived_reward,
            'pleasure': pleasure,
            'effort_cost': effort_cost,
            'motivation_gain': motivation_gain,
            'can_engage': can_engage,
            'anhedonia_effect': self.motivation_state.anhedonia,
            'motivation_level': self.motivation_state.motivation_level
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
        perceived_reward = expected_reward * self.motivation_state.reward_sensitivity
        
        # 무쾌감증 적용
        pleasure = perceived_reward * (1.0 - self.motivation_state.anhedonia)
        
        # 노력 비용
        effort_cost = effort_required * self.motivation_state.effort_cost
        
        # 지연 할인 (시간이 지날수록 보상 가치 감소)
        delay_discount = np.exp(-delay * 0.5)
        discounted_pleasure = pleasure * delay_discount
        
        # 총 가치
        total_value = discounted_pleasure - effort_cost
        
        # 행동 결정
        should_act = (total_value > 0.0 and 
                     self.motivation_state.motivation_level > 0.2)
        
        return {
            'total_value': total_value,
            'should_act': should_act,
            'motivation_sufficient': self.motivation_state.motivation_level > 0.3,
            'goal_directed': self.motivation_state.goal_directed_behavior > 0.5
        }
    
    def _calculate_score(self) -> float:
        """
        루프 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            루프 점수 (높을수록 동기 붕괴 심각)
        """
        # 동기 결핍 정도를 점수로 변환
        motivation_deficit = 1.0 - self.motivation_state.motivation_level
        reward_deficit = 1.0 - self.motivation_state.reward_sensitivity
        goal_deficit = 1.0 - self.motivation_state.goal_directed_behavior
        
        # 가중 평균
        score = (
            motivation_deficit * 0.4 +
            reward_deficit * 0.3 +
            goal_deficit * 0.2 +
            self.motivation_state.anhedonia * 0.1
        )
        
        return np.clip(score, 0.0, 1.0)
    
    def _analyze_patterns(self) -> Dict:
        """
        패턴 분석
        
        Returns:
            패턴 분석 결과
        """
        return {
            'reward_sensitivity': self.motivation_state.reward_sensitivity,
            'motivation_level': self.motivation_state.motivation_level,
            'goal_directed_behavior': self.motivation_state.goal_directed_behavior,
            'anhedonia': self.motivation_state.anhedonia,
            'effort_cost': self.motivation_state.effort_cost,
            'reward_failures': self.motivation_state.reward_failures,
            'goal_failures': self.motivation_state.goal_failures,
            'loop_strength': self.state.loop_strength,
            'collapse_severity': self._calculate_score()
        }
    
    def get_motivation_score(self) -> float:
        """
        동기 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            동기 점수 (낮을수록 동기 결핍)
        """
        score = (
            self.motivation_state.reward_sensitivity * 0.3 +
            self.motivation_state.motivation_level * 0.3 +
            self.motivation_state.goal_directed_behavior * 0.2 +
            (1.0 - self.motivation_state.anhedonia) * 0.1 +
            (2.5 - self.motivation_state.effort_cost) / 1.5 * 0.1
        )
        return np.clip(score, 0.0, 1.0)
    
    def get_strength(self) -> float:
        """루프 강도 반환"""
        return self.state.loop_strength
    
    def get_state(self) -> MotivationCollapseLoopState:
        """루프 상태 반환"""
        return self.motivation_state

