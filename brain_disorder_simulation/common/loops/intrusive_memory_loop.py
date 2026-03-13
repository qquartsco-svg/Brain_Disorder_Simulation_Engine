"""
침입 기억 루프 (Intrusive Memory Loop)

PTSD, 우울증, 불안장애에서 공통적으로 나타나는 침입 기억 메커니즘

핵심 메커니즘:
외상 기억 강화 → 억제 실패 → 침입 발생 → 공포 반응 → 기억 더 강화 → 억제 더 실패 (폐루프)

연구 근거:
- Brewin et al. (2000) - Dual representation theory
- Ehlers & Clark (2000) - Cognitive model of PTSD
- Rauch et al. (2006) - Neurocircuitry of PTSD

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional, List
from dataclasses import dataclass, field

from .base_loop import BaseLoop, LoopState, LoopParameters


@dataclass
class TraumaticMemory:
    """외상 기억 데이터 구조"""
    memory_id: str
    intensity: float = 0.0  # 0.0 ~ 1.0
    frequency: float = 0.0  # 침입 빈도
    associated_fear: float = 0.0  # 연관된 공포 수준
    suppression_attempts: int = 0  # 억제 시도 횟수
    suppression_success: float = 0.5  # 억제 성공률


@dataclass
class IntrusiveMemoryLoopState(LoopState):
    """침입 기억 루프 상태"""
    memory_intensity: float = 0.0  # 기억 강도 (0.0 ~ 1.0)
    intrusion_frequency: float = 0.0  # 침입 빈도 (0.0 ~ 1.0)
    suppression_failure: float = 0.3  # 억제 실패율 (0.0 ~ 1.0)
    associated_fear: float = 0.0  # 연관된 공포 수준 (0.0 ~ 1.0)
    current_intrusion_level: float = 0.0  # 현재 침입 수준 (0.0 ~ 1.0)
    suppression_attempts: int = 0  # 억제 시도 횟수
    traumatic_memories: List[TraumaticMemory] = field(default_factory=list)  # 외상 기억 목록


class IntrusiveMemoryLoop(BaseLoop):
    """
    침입 기억 루프
    
    PTSD, 우울증, 불안장애에서 공통적으로 나타나는 침입 기억 메커니즘
    
    루프 메커니즘:
    1. 외상 기억 접촉 또는 억제 실패
    2. 기억 강화
    3. 억제 실패율 증가
    4. 침입 발생
    5. 공포 반응
    6. 기억 더 강화 → 억제 더 실패
    7. 루프 강화 (폐루프)
    """
    
    def __init__(self,
                 initial_trauma_intensity: float = 0.0,
                 initial_suppression_failure: float = 0.3,
                 parameters: Optional[LoopParameters] = None,
                 rng: Optional[np.random.Generator] = None):
        """
        침입 기억 루프 초기화
        
        Args:
            initial_trauma_intensity: 초기 외상 강도 (0.0 ~ 1.0)
            initial_suppression_failure: 초기 억제 실패율 (0.0 ~ 1.0)
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
            name="IntrusiveMemoryLoop",
            parameters=parameters,
            rng=rng
        )
        
        # 초기 상태 설정
        self.intrusion_state = IntrusiveMemoryLoopState()
        self.intrusion_state.suppression_failure = np.clip(initial_suppression_failure, 0.0, 1.0)
        
        # 동역학 파라미터
        self.memory_consolidation_rate = 0.1  # 기억 강화율
        self.intrusion_threshold = 0.5  # 침입 임계값
        self.fear_amplification = 1.5  # 공포 증폭 인자
        
        # 초기 외상 강도 적용
        if initial_trauma_intensity > 0.0:
            self._apply_trauma(initial_trauma_intensity)
    
    def _apply_trauma(self, intensity: float):
        """외상 강도에 따라 상태 업데이트"""
        intensity = np.clip(intensity, 0.0, 1.0)
        
        # 기억 강도 설정
        self.intrusion_state.memory_intensity = intensity
        
        # 공포 수준 설정
        self.intrusion_state.associated_fear = intensity * 0.9
        
        # 루프 강도 설정
        self.state.loop_strength = intensity
    
    def add_traumatic_memory(self,
                            memory_id: str,
                            initial_intensity: float = 0.8,
                            initial_fear: float = 0.7):
        """
        외상 기억 추가
        
        Args:
            memory_id: 기억 식별자
            initial_intensity: 초기 강도
            initial_fear: 초기 공포 수준
        """
        memory = TraumaticMemory(
            memory_id=memory_id,
            intensity=np.clip(initial_intensity, 0.0, 1.0),
            frequency=0.0,
            associated_fear=np.clip(initial_fear, 0.0, 1.0),
            suppression_attempts=0,
            suppression_success=0.5
        )
        self.intrusion_state.traumatic_memories.append(memory)
        
        # 기억 강도 업데이트
        if initial_intensity > self.intrusion_state.memory_intensity:
            self.intrusion_state.memory_intensity = initial_intensity
            self.state.loop_strength = initial_intensity
    
    def _trigger_condition(self, context: Optional[Dict] = None) -> bool:
        """
        트리거 조건 확인
        
        Args:
            context: 컨텍스트 정보
                - memory_id: 기억 식별자
                - pfc_control: PFC 제어 능력 (0.0 ~ 1.0)
                - amygdala_arousal: Amygdala 각성 수준 (0.0 ~ 1.0)
                - suppression_attempted: 억제 시도 여부
        
        Returns:
            트리거 여부
        """
        if context is None:
            return False
        
        # 억제 시도 실패
        if context.get('suppression_attempted', False):
            pfc_control = context.get('pfc_control', 1.0)
            suppression_prob = pfc_control * (1.0 - self.intrusion_state.suppression_failure)
            if self.rng.random() >= suppression_prob:
                return True
        
        # Amygdala 각성이 높고 기억 강도가 임계값 이상
        amygdala_arousal = context.get('amygdala_arousal', 0.0)
        if (amygdala_arousal > 0.5 and 
            self.intrusion_state.memory_intensity > self.intrusion_threshold):
            return True
        
        # 침입 빈도가 높음
        if self.intrusion_state.intrusion_frequency > 0.4:
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
        
        # 기억 강화 (시간에 따른)
        memory_consolidation = 0.01 * loop_effect * dt
        self.intrusion_state.memory_intensity = min(
            1.0,
            self.intrusion_state.memory_intensity + memory_consolidation
        )
        
        # 억제 실패율 증가
        failure_increase = 0.01 * loop_effect * dt
        self.intrusion_state.suppression_failure = min(
            0.9,
            self.intrusion_state.suppression_failure + failure_increase
        )
        
        # 침입 빈도 증가
        frequency_increase = 0.02 * loop_effect * dt
        self.intrusion_state.intrusion_frequency = min(
            1.0,
            self.intrusion_state.intrusion_frequency + frequency_increase
        )
        
        # 공포 수준 증가
        fear_increase = 0.015 * loop_effect * dt
        self.intrusion_state.associated_fear = min(
            1.0,
            self.intrusion_state.associated_fear + fear_increase
        )
        
        # 자연적 감쇠 (매우 느림)
        self.state.loop_strength *= (self.parameters.loop_decay ** (dt * 0.1))
    
    def attempt_suppression(self, memory_id: str, pfc_control: float) -> bool:
        """
        기억 억제 시도 (PFC 역할)
        
        Args:
            memory_id: 기억 식별자
            pfc_control: PFC 제어 능력 (0.0 ~ 1.0)
        
        Returns:
            억제 성공 여부
        """
        # 억제 시도 횟수 증가
        self.intrusion_state.suppression_attempts += 1
        
        # PFC 제어 능력에 따른 억제 성공률
        suppression_prob = pfc_control * (1.0 - self.intrusion_state.suppression_failure)
        
        success = self.rng.random() < suppression_prob
        
        if success:
            # 억제 성공 시 루프 약화
            self.state.loop_strength = max(
                0.0,
                self.state.loop_strength - 0.05
            )
        else:
            # 억제 실패 시 루프 트리거
            self.trigger(
                intensity=0.3,
                context={
                    'memory_id': memory_id,
                    'pfc_control': pfc_control,
                    'suppression_attempted': True
                }
            )
            # 침입 빈도 증가
            self.intrusion_state.intrusion_frequency = min(
                1.0,
                self.intrusion_state.intrusion_frequency + 0.2
            )
        
        return success
    
    def compute_intrusion(self, amygdala_arousal: float) -> float:
        """
        침입 수준 계산
        
        Args:
            amygdala_arousal: Amygdala 각성 수준 (0.0 ~ 1.0)
        
        Returns:
            침입 수준 (0.0 ~ 1.0)
        """
        if not self.intrusion_state.traumatic_memories:
            # 기억이 없으면 기억 강도 기반으로 계산
            contribution = (
                self.intrusion_state.memory_intensity *
                self.intrusion_state.intrusion_frequency *
                self.intrusion_state.associated_fear *
                amygdala_arousal *
                self.fear_amplification
            )
        else:
            # 각 기억의 침입 기여도 계산
            intrusion_contributions = []
            for memory in self.intrusion_state.traumatic_memories:
                contribution = (
                    memory.intensity *
                    memory.frequency *
                    memory.associated_fear *
                    amygdala_arousal *
                    self.fear_amplification
                )
                intrusion_contributions.append(contribution)
            
            contribution = np.mean(intrusion_contributions) if intrusion_contributions else 0.0
        
        # 전체 침입 수준
        total_intrusion = np.clip(contribution, 0.0, 1.0)
        
        self.intrusion_state.current_intrusion_level = total_intrusion
        
        # 침입이 발생하면 루프 트리거
        if total_intrusion > self.intrusion_threshold:
            self.trigger(
                intensity=total_intrusion,
                context={
                    'amygdala_arousal': amygdala_arousal,
                    'intrusion_level': total_intrusion
                }
            )
        
        return total_intrusion
    
    def _apply_loop_effect(self, intensity: float, context: Optional[Dict] = None) -> Dict:
        """
        루프 효과 적용
        
        Args:
            intensity: 효과 강도
            context: 컨텍스트 정보
        
        Returns:
            적용된 효과 정보
        """
        # 루프 강도에 따라 침입 상태 업데이트
        self._update_intrusion_from_strength(self.state.loop_strength)
        
        return {
            'memory_intensity': self.intrusion_state.memory_intensity,
            'intrusion_frequency': self.intrusion_state.intrusion_frequency,
            'suppression_failure': self.intrusion_state.suppression_failure,
            'associated_fear': self.intrusion_state.associated_fear,
            'current_intrusion_level': self.intrusion_state.current_intrusion_level,
            'loop_strength': self.state.loop_strength
        }
    
    def _update_intrusion_from_strength(self, strength: float):
        """
        루프 강도에 따라 침입 상태 업데이트
        
        Args:
            strength: 루프 강도 (0.0 ~ 1.0)
        """
        # 기억 강도 업데이트
        if strength > self.intrusion_state.memory_intensity:
            self.intrusion_state.memory_intensity = strength
        
        # 억제 실패율 업데이트
        self.intrusion_state.suppression_failure = max(
            self.intrusion_state.suppression_failure,
            strength * 0.7
        )
    
    def _calculate_score(self) -> float:
        """
        루프 점수 계산 (0.0 ~ 1.0)
        
        Returns:
            루프 점수 (높을수록 침입 심각)
        """
        # 침입 심각도 계산
        intrusion_severity = (
            self.intrusion_state.memory_intensity * 0.4 +
            self.intrusion_state.intrusion_frequency * 0.3 +
            self.intrusion_state.associated_fear * 0.2 +
            self.intrusion_state.suppression_failure * 0.1
        )
        
        return np.clip(intrusion_severity, 0.0, 1.0)
    
    def _analyze_patterns(self) -> Dict:
        """
        패턴 분석
        
        Returns:
            패턴 분석 결과
        """
        return {
            'memory_intensity': self.intrusion_state.memory_intensity,
            'intrusion_frequency': self.intrusion_state.intrusion_frequency,
            'suppression_failure': self.intrusion_state.suppression_failure,
            'associated_fear': self.intrusion_state.associated_fear,
            'current_intrusion_level': self.intrusion_state.current_intrusion_level,
            'suppression_attempts': self.intrusion_state.suppression_attempts,
            'loop_strength': self.state.loop_strength,
            'intrusion_severity': self._calculate_score()
        }
    
    def get_strength(self) -> float:
        """루프 강도 반환"""
        return self.state.loop_strength
    
    def get_state(self) -> IntrusiveMemoryLoopState:
        """루프 상태 반환"""
        return self.intrusion_state

