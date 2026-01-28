"""
제어 실패 루프 (Control Failure Loop)

우울증과 ADHD에서 공통으로 나타나는 인지 제어 실패 루프

루프 메커니즘:
1. 부정적 사고 발생
2. 억제 제어 시도
3. 억제 실패
4. 부정적 루프 강화
5. 더 많은 부정적 사고 (폐루프)

연구 근거:
- Joormann & Gotlib (2010) - Emotion regulation in depression
- Barkley (1997) - ADHD and executive functions

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass

from .base_loop import BaseLoop, LoopParameters, LoopState


@dataclass
class ControlFailureLoopState(LoopState):
    """제어 실패 루프 상태"""
    inhibition_strength: float = 1.0  # 억제 제어 강도 (0.0 ~ 1.0)
    cognitive_flexibility: float = 1.0  # 인지적 유연성 (0.0 ~ 1.0)
    working_memory_capacity: float = 1.0  # 작업 기억 용량 (0.0 ~ 1.0)
    executive_function: float = 1.0  # 실행 기능 (0.0 ~ 1.0)
    negative_thought_frequency: float = 0.0  # 부정적 사고 빈도


class ControlFailureLoop(BaseLoop):
    """
    제어 실패 루프
    
    부정적 사고 → 억제 실패 → 루프 강화 → 더 많은 부정적 사고
    
    사용 질환:
    - 우울증 (Depression)
    - ADHD
    """
    
    def __init__(self,
                 initial_impairment: float = 0.0,
                 parameters: Optional[LoopParameters] = None,
                 rng: Optional[np.random.Generator] = None):
        """
        제어 실패 루프 초기화
        
        Args:
            initial_impairment: 초기 제어 약화 정도 (0.0 ~ 1.0)
            parameters: 루프 파라미터
            rng: 난수 생성기
        """
        # 기본 파라미터 설정
        if parameters is None:
            parameters = LoopParameters(
                loop_gain=0.05,
                loop_decay=0.98,
                loop_threshold=0.3,
                max_strength=1.0,
                min_strength=0.0
            )
        
        super().__init__(
            name="ControlFailureLoop",
            parameters=parameters,
            rng=rng
        )
        
        # 제어 실패 특화 상태
        self.control_state = ControlFailureLoopState()
        
        # 초기 약화 정도 설정
        if initial_impairment > 0:
            self._update_control_from_impairment(initial_impairment)
    
    def _update_control_from_impairment(self, impairment: float):
        """약화 정도에 따라 제어 상태 업데이트"""
        impairment = np.clip(impairment, 0.0, 1.0)
        
        # 억제 제어 약화 (1.0 ~ 0.3)
        self.control_state.inhibition_strength = 1.0 - (impairment * 0.7)
        
        # 인지적 유연성 감소 (1.0 ~ 0.4)
        self.control_state.cognitive_flexibility = 1.0 - (impairment * 0.6)
        
        # 작업 기억 용량 감소 (1.0 ~ 0.5)
        self.control_state.working_memory_capacity = 1.0 - (impairment * 0.5)
        
        # 실행 기능 저하 (1.0 ~ 0.4)
        self.control_state.executive_function = 1.0 - (impairment * 0.6)
    
    def process_negative_thought(self,
                                  thought_intensity: float = 1.0) -> Dict:
        """
        부정적 사고 처리 (루프 트리거)
        
        Args:
            thought_intensity: 사고 강도 (0.0 ~ 1.0)
        
        Returns:
            처리 결과
        """
        # 억제 제어 시도
        inhibition_success = False
        if self.control_state.inhibition_strength > 0.5:
            # 억제 성공 확률
            inhibition_prob = self.control_state.inhibition_strength
            if self.rng.random() < inhibition_prob:
                inhibition_success = True
                # 억제 성공 시 루프 약화
                self.state.loop_strength *= 0.9
        else:
            # 억제 제어가 약하면 실패
            inhibition_success = False
        
        # 억제 실패 시 루프 트리거
        if not inhibition_success:
            trigger_intensity = thought_intensity
            trigger_result = self.trigger(trigger_intensity, {
                'thought_intensity': thought_intensity,
                'inhibition_failed': True
            })
            
            # 부정적 사고 빈도 증가
            self.control_state.negative_thought_frequency = min(1.0,
                self.control_state.negative_thought_frequency + 0.1 * thought_intensity)
            
            return {
                'inhibition_success': False,
                'negative_loop_strength': self.state.loop_strength,
                'negative_thought_frequency': self.control_state.negative_thought_frequency,
                'control_impaired': True,
                **trigger_result
            }
        else:
            return {
                'inhibition_success': True,
                'negative_loop_strength': self.state.loop_strength,
                'negative_thought_frequency': self.control_state.negative_thought_frequency,
                'control_impaired': False
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
        base_success = self.control_state.executive_function
        difficulty_factor = 1.0 - (task_difficulty * 0.5)
        success_probability = base_success * difficulty_factor
        
        # 작업 기억 용량에 따른 처리 능력
        processing_capacity = self.control_state.working_memory_capacity
        
        # 실제 성공 여부
        success = self.rng.random() < success_probability
        
        # 실패 시 루프 트리거
        if not success:
            trigger_intensity = task_difficulty * (1.0 - success_probability)
            self.trigger(trigger_intensity, {
                'task_difficulty': task_difficulty,
                'control_failed': True
            })
        
        return {
            'success': success,
            'success_probability': success_probability,
            'processing_capacity': processing_capacity,
            'executive_function': self.control_state.executive_function,
            'loop_strength': self.state.loop_strength
        }
    
    def _apply_loop_effect(self, intensity: float, context: Optional[Dict] = None) -> Dict:
        """
        루프 효과 적용
        
        Args:
            intensity: 효과 강도
            context: 컨텍스트 정보
        
        Returns:
            적용된 효과 정보
        """
        # 루프 강도에 따라 제어 상태 업데이트
        self._update_control_from_impairment(self.state.loop_strength)
        
        return {
            'inhibition_strength': self.control_state.inhibition_strength,
            'cognitive_flexibility': self.control_state.cognitive_flexibility,
            'working_memory_capacity': self.control_state.working_memory_capacity,
            'executive_function': self.control_state.executive_function,
            'negative_thought_frequency': self.control_state.negative_thought_frequency
        }
    
    def _reinforce_loop(self, effect: Dict):
        """
        루프 자가 강화 (폐루프 형성)
        
        제어가 약해질수록 더 많은 부정적 사고가 발생함
        """
        # 기본 자가 강화
        super()._reinforce_loop(effect)
        
        # 억제 제어가 약하면 루프가 더 강화됨
        if self.control_state.inhibition_strength < 0.5:
            reinforcement = self.parameters.loop_gain * 0.2
            self.state.loop_strength = min(
                self.parameters.max_strength,
                self.state.loop_strength + reinforcement
            )
        
        # 부정적 사고 빈도가 높으면 루프가 더 강화됨
        if self.control_state.negative_thought_frequency > 0.5:
            reinforcement = self.parameters.loop_gain * 0.15
            self.state.loop_strength = min(
                self.parameters.max_strength,
                self.state.loop_strength + reinforcement
            )
    
    def update(self, dt: float = 0.1, external_factors: Optional[Dict] = None) -> Dict:
        """
        루프 업데이트 (시간 경과에 따른 자연적 감쇠)
        
        Args:
            dt: 시간 간격
            external_factors: 외부 요인
        """
        # 기본 업데이트
        result = super().update(dt, external_factors)
        
        # 부정적 사고 빈도 자연적 감쇠
        self.control_state.negative_thought_frequency *= (0.99 ** (dt * 10))
        
        # 루프 강도에 따라 제어 상태 업데이트
        self._update_control_from_impairment(self.state.loop_strength)
        
        result['control_state'] = {
            'inhibition_strength': self.control_state.inhibition_strength,
            'cognitive_flexibility': self.control_state.cognitive_flexibility,
            'working_memory_capacity': self.control_state.working_memory_capacity,
            'executive_function': self.control_state.executive_function,
            'negative_thought_frequency': self.control_state.negative_thought_frequency
        }
        
        return result
    
    def get_control_score(self) -> float:
        """
        인지 제어 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            제어 점수 (낮을수록 제어 약화)
        """
        score = (
            self.control_state.inhibition_strength * 0.3 +
            self.control_state.cognitive_flexibility * 0.2 +
            self.control_state.working_memory_capacity * 0.2 +
            self.control_state.executive_function * 0.2 +
            (1.0 - self.control_state.negative_thought_frequency) * 0.1
        )
        return np.clip(score, 0.0, 1.0)

