"""
인지 제어 엔진 (공통)

대부분의 뇌 질환에서 공통으로 나타나는 인지 제어 약화 메커니즘
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class CognitiveControlState:
    """인지 제어 상태"""
    inhibition_strength: float = 1.0      # 억제 제어 강도
    cognitive_flexibility: float = 1.0    # 인지적 유연성
    working_memory_capacity: float = 1.0 # 작업 기억 용량
    negative_thought_loop: float = 0.0   # 부정적 사고 루프 강도
    executive_function: float = 1.0       # 실행 기능


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

