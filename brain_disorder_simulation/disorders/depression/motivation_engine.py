"""
동기 엔진 (우울증 전용)

우울증 특화: 동기 감소 및 무쾌감증 메커니즘
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class MotivationState:
    """동기 상태"""
    reward_sensitivity: float = 1.0       # 보상 민감도
    motivation_level: float = 1.0         # 동기 수준
    goal_directed_behavior: float = 1.0   # 목표 지향 행동
    anhedonia: float = 0.0                # 무쾌감증 (anhedonia)
    effort_cost: float = 1.0              # 노력 비용


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

