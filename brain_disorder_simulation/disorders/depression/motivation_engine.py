"""
동기 엔진 (우울증 전용)

우울증 특화: 동기 감소 및 무쾌감증 메커니즘

⚠️ 리팩터링: 이 엔진은 내부적으로 MotivationCollapseLoop를 사용합니다.
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass

# 루프 라이브러리 import
from ...common.loops import MotivationCollapseLoop


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
        
        # 루프 라이브러리 사용
        self.loop = MotivationCollapseLoop(
            initial_motivation_deficit=motivation_deficit,
            rng=rng
        )
        
        # 상태 초기화 (호환성 유지)
        self.state = MotivationState()
        
        # 파라미터
        self.base_reward_sensitivity = 1.0
        
        # 초기 상태 설정
        self._update_state_from_loop()
    
    def _update_state_from_loop(self):
        """루프에서 상태 동기화 (호환성 유지)"""
        loop_state = self.loop.get_state()
        
        # 루프 상태를 엔진 상태로 동기화
        self.state.reward_sensitivity = loop_state.reward_sensitivity
        self.state.motivation_level = loop_state.motivation_level
        self.state.goal_directed_behavior = loop_state.goal_directed_behavior
        self.state.anhedonia = loop_state.anhedonia
        self.state.effort_cost = loop_state.effort_cost
        
        # 루프 강도 업데이트
        loop_strength = self.loop.get_strength()
        if loop_strength > 0:
            self.motivation_deficit = loop_strength
    
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
        # 루프를 통해 보상 처리
        result = self.loop.process_reward(
            reward_value=reward_value,
            effort_required=effort_required
        )
        
        # 상태 동기화
        self._update_state_from_loop()
        
        return result
    
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
        # 루프를 통해 행동 평가
        result = self.loop.evaluate_action(
            expected_reward=expected_reward,
            effort_required=effort_required,
            delay=delay
        )
        
        # 상태 동기화
        self._update_state_from_loop()
        
        return result
    
    def get_motivation_score(self) -> float:
        """
        동기 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            동기 점수 (낮을수록 동기 결핍)
        """
        # 상태 동기화
        self._update_state_from_loop()
        
        # 루프를 통해 동기 점수 계산
        return self.loop.get_motivation_score()
    
    def update(self, dt: float):
        """
        엔진 업데이트 (시간 경과에 따른 동역학)
        
        Args:
            dt: 시간 간격
        """
        # 루프 동역학 업데이트
        self.loop._update_dynamics(dt=dt)
        
        # 상태 동기화
        self._update_state_from_loop()

