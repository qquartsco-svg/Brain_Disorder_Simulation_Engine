"""
인지 제어 엔진 (공통)

대부분의 뇌 질환에서 공통으로 나타나는 인지 제어 약화 메커니즘

⚠️ 리팩터링: 이 엔진은 내부적으로 ControlFailureLoop를 사용합니다.
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass

# 루프 라이브러리 import
from .loops.control_failure_loop import ControlFailureLoop


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
        
        # 루프 라이브러리 사용
        self.loop = ControlFailureLoop(
            initial_impairment=control_impairment,
            rng=rng
        )
        
        # 상태 초기화 (호환성 유지)
        self.state = CognitiveControlState()
        
        # 초기 상태 설정
        self._update_state_from_impairment()
    
    def _update_state_from_impairment(self):
        """약화 정도에 따라 상태 업데이트 (루프에서 상태 동기화)"""
        # 루프 강도 업데이트
        loop_strength = self.loop.get_strength()
        if loop_strength > 0:
            self.control_impairment = loop_strength
        
        # 루프 상태에서 동기화
        control_state = self.loop.control_state
        self.state.inhibition_strength = control_state.inhibition_strength
        self.state.cognitive_flexibility = control_state.cognitive_flexibility
        self.state.working_memory_capacity = control_state.working_memory_capacity
        self.state.executive_function = control_state.executive_function
        self.state.negative_thought_loop = control_state.negative_thought_frequency
    
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
        # 루프를 사용하여 부정적 사고 처리
        result = self.loop.process_negative_thought(thought_intensity)
        
        # 상태 동기화
        self._update_state_from_impairment()
        
        # 결과 반환 (호환성 유지)
        return {
            'inhibition_success': result['inhibition_success'],
            'negative_loop_strength': result['negative_loop_strength'],
            'alternative_thinking': self.state.cognitive_flexibility,
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
        # 루프를 사용하여 인지 제어 시도
        result = self.loop.attempt_cognitive_control(task_difficulty)
        
        # 상태 동기화
        self._update_state_from_impairment()
        
        # 결과 반환 (호환성 유지)
        return {
            'success': result['success'],
            'success_probability': result['success_probability'],
            'processing_capacity': result['processing_capacity'],
            'executive_function': result['executive_function']
        }
    
    def update_negative_loop(self, dt: float = 0.1):
        """
        부정적 사고 루프 업데이트
        
        Args:
            dt: 시간 간격
        """
        # 루프 업데이트
        self.loop.update(dt)
        
        # 상태 동기화
        self._update_state_from_impairment()
    
    def get_control_score(self) -> float:
        """
        인지 제어 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            제어 점수 (낮을수록 제어 약화)
        """
        # 루프에서 점수 가져오기
        return self.loop.get_control_score()

