"""
PTSD 특화 엔진

외상 후 스트레스 장애 (PTSD) 메커니즘 시뮬레이션을 위한 특화 엔진

핵심 메커니즘:
1. 외상 기억 침입 (Intrusive Memory Engine)
2. 회피 패턴 (Avoidance Engine)
3. 과각성 (Hyperarousal Engine)
4. 부정적 인지 변화 (Negative Cognition Engine)

연구 근거:
- Brewin et al. (2000) - Dual representation theory
- Ehlers & Clark (2000) - Cognitive model of PTSD
- Rauch et al. (2006) - Neurocircuitry of PTSD

참고 문헌:
- Brewin, C. R., et al. (2000). Meta-analysis of risk factors for posttraumatic stress disorder
- Ehlers, A., & Clark, D. M. (2000). A cognitive model of posttraumatic stress disorder
- Rauch, S. L., et al. (2006). Neurocircuitry models of posttraumatic stress disorder

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass


@dataclass
class TraumaticMemory:
    """외상 기억 데이터 구조"""
    memory_id: str
    intensity: float  # 0.0 ~ 1.0
    frequency: float  # 침입 빈도
    associated_fear: float  # 연관된 공포 수준
    suppression_attempts: int  # 억제 시도 횟수
    suppression_success: float  # 억제 성공률


class IntrusiveMemoryEngine:
    """
    외상 기억 침입 엔진
    
    메커니즘:
    - Hippocampus: 외상 기억 강화 저장
    - PFC: 기억 억제 실패
    - Amygdala: 공포 반응 강화
    """
    
    def __init__(self, rng: Optional[np.random.Generator] = None):
        """
        외상 기억 침입 엔진 초기화
        
        Args:
            rng: 난수 생성기
        """
        self.rng = rng if rng is not None else np.random.default_rng()
        self.traumatic_memories: List[TraumaticMemory] = []
        
        # 동역학 파라미터
        self.memory_consolidation_rate = 0.1  # 기억 강화율
        self.suppression_failure_rate = 0.3  # 억제 실패율
        self.intrusion_threshold = 0.5  # 침입 임계값
        self.fear_amplification = 1.5  # 공포 증폭 인자
        
        # 상태
        self.current_intrusion_level = 0.0
        self.suppression_attempts = 0
        self.suppression_success_rate = 0.5
        
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
        self.traumatic_memories.append(memory)
    
    def consolidate_memory(self, memory_id: str, factor: float = 0.1):
        """
        기억 강화 (Hippocampus 역할)
        
        연구 근거:
        - PTSD에서 외상 기억이 과도하게 강화됨
        - 정상적인 기억 소거 과정이 실패
        
        Args:
            memory_id: 기억 식별자
            factor: 강화 인자
        """
        for memory in self.traumatic_memories:
            if memory.memory_id == memory_id:
                # 기억 강도 증가
                memory.intensity = np.clip(
                    memory.intensity + factor * (1.0 - memory.intensity),
                    0.0, 1.0
                )
                # 공포 수준도 함께 증가
                memory.associated_fear = np.clip(
                    memory.associated_fear + factor * 0.5,
                    0.0, 1.0
                )
                break
    
    def attempt_suppression(self, memory_id: str, pfc_control: float) -> bool:
        """
        기억 억제 시도 (PFC 역할)
        
        연구 근거:
        - PTSD에서 PFC의 억제 기능이 약화됨
        - 억제 실패 시 침입 발생
        
        Args:
            memory_id: 기억 식별자
            pfc_control: PFC 제어 능력 (0.0 ~ 1.0)
            
        Returns:
            억제 성공 여부
        """
        for memory in self.traumatic_memories:
            if memory.memory_id == memory_id:
                memory.suppression_attempts += 1
                
                # PFC 제어 능력에 따른 억제 성공률
                suppression_prob = pfc_control * (1.0 - self.suppression_failure_rate)
                
                success = self.rng.random() < suppression_prob
                
                if success:
                    memory.suppression_success = np.clip(
                        memory.suppression_success + 0.1,
                        0.0, 1.0
                    )
                else:
                    # 억제 실패 시 침입 발생
                    memory.frequency += 0.2
                    memory.suppression_success = np.clip(
                        memory.suppression_success - 0.1,
                        0.0, 1.0
                    )
                
                return success
        return False
    
    def compute_intrusion(self, amygdala_arousal: float) -> float:
        """
        침입 수준 계산
        
        연구 근거:
        - Amygdala 각성 수준이 높을수록 침입 빈도 증가
        - 억제 실패 시 침입 발생
        
        Args:
            amygdala_arousal: Amygdala 각성 수준 (0.0 ~ 1.0)
            
        Returns:
            침입 수준 (0.0 ~ 1.0)
        """
        if not self.traumatic_memories:
            return 0.0
        
        # 각 기억의 침입 기여도 계산
        intrusion_contributions = []
        for memory in self.traumatic_memories:
            # 기억 강도 × 빈도 × 공포 수준 × Amygdala 각성
            contribution = (
                memory.intensity *
                memory.frequency *
                memory.associated_fear *
                amygdala_arousal *
                self.fear_amplification
            )
            intrusion_contributions.append(contribution)
        
        # 전체 침입 수준
        total_intrusion = np.clip(
            np.mean(intrusion_contributions) if intrusion_contributions else 0.0,
            0.0, 1.0
        )
        
        self.current_intrusion_level = total_intrusion
        return total_intrusion
    
    def update(self, dt: float, amygdala_arousal: float, pfc_control: float):
        """
        엔진 업데이트
        
        Args:
            dt: 시간 간격
            amygdala_arousal: Amygdala 각성 수준
            pfc_control: PFC 제어 능력
        """
        # 자동 기억 강화 (시간에 따른)
        for memory in self.traumatic_memories:
            if memory.intensity > self.intrusion_threshold:
                self.consolidate_memory(memory.memory_id, factor=0.01 * dt)
        
        # 침입 수준 계산
        self.compute_intrusion(amygdala_arousal)


class AvoidanceEngine:
    """
    회피 패턴 엔진
    
    메커니즘:
    - Basal Ganglia: 회피 행동 선택
    - PFC: 인지 회피
    """
    
    def __init__(self, rng: Optional[np.random.Generator] = None):
        """
        회피 패턴 엔진 초기화
        
        Args:
            rng: 난수 생성기
        """
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 회피 패턴
        self.avoided_stimuli: List[str] = []  # 회피된 자극 목록
        self.avoidance_strength: Dict[str, float] = {}  # 자극별 회피 강도
        
        # 동역학 파라미터
        self.avoidance_learning_rate = 0.2  # 회피 학습률
        self.generalization_factor = 0.3  # 일반화 인자 (유사 자극도 회피)
        
        # 상태
        self.current_avoidance_level = 0.0
        self.emotional_numbing = 0.0  # 감정적 마비
        
    def learn_avoidance(self, stimulus: str, fear_level: float):
        """
        회피 학습 (Basal Ganglia 역할)
        
        연구 근거:
        - PTSD에서 외상 관련 자극에 대한 회피가 강화됨
        - 회피가 단기적으로는 불안 감소시키지만 장기적으로는 문제 유지
        
        Args:
            stimulus: 자극 식별자
            fear_level: 공포 수준
        """
        if stimulus not in self.avoided_stimuli:
            self.avoided_stimuli.append(stimulus)
        
        # 회피 강도 업데이트
        current_strength = self.avoidance_strength.get(stimulus, 0.0)
        new_strength = np.clip(
            current_strength + self.avoidance_learning_rate * fear_level,
            0.0, 1.0
        )
        self.avoidance_strength[stimulus] = new_strength
        
        # 감정적 마비 증가 (회피가 지속될수록)
        self.emotional_numbing = np.clip(
            self.emotional_numbing + 0.05 * fear_level,
            0.0, 1.0
        )
    
    def check_avoidance(self, stimulus: str) -> Tuple[bool, float]:
        """
        회피 여부 확인
        
        Args:
            stimulus: 자극 식별자
            
        Returns:
            (회피 여부, 회피 강도)
        """
        # 직접 회피
        if stimulus in self.avoided_stimuli:
            strength = self.avoidance_strength.get(stimulus, 0.0)
            return True, strength
        
        # 일반화된 회피 (유사 자극)
        for avoided in self.avoided_stimuli:
            similarity = self._compute_similarity(stimulus, avoided)
            if similarity > (1.0 - self.generalization_factor):
                strength = self.avoidance_strength.get(avoided, 0.0) * similarity
                return True, strength
        
        return False, 0.0
    
    def _compute_similarity(self, s1: str, s2: str) -> float:
        """
        자극 유사도 계산 (간단한 구현)
        
        Args:
            s1, s2: 자극 식별자
            
        Returns:
            유사도 (0.0 ~ 1.0)
        """
        # 간단한 문자열 유사도 (실제로는 의미적 유사도 사용)
        if s1 == s2:
            return 1.0
        
        # 공통 부분 기반
        common_chars = sum(1 for c in s1 if c in s2)
        max_len = max(len(s1), len(s2))
        return common_chars / max_len if max_len > 0 else 0.0
    
    def compute_avoidance_level(self) -> float:
        """
        전체 회피 수준 계산
        
        Returns:
            회피 수준 (0.0 ~ 1.0)
        """
        if not self.avoidance_strength:
            return 0.0
        
        avg_strength = np.mean(list(self.avoidance_strength.values()))
        self.current_avoidance_level = avg_strength
        return avg_strength


class HyperarousalEngine:
    """
    과각성 엔진
    
    메커니즘:
    - Hypothalamus: 스트레스 반응 과다
    - Thalamus: 필터링 실패
    - Amygdala: 경계 상태 유지
    """
    
    def __init__(self, rng: Optional[np.random.Generator] = None):
        """
        과각성 엔진 초기화
        
        Args:
            rng: 난수 생성기
        """
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 동역학 파라미터
        self.baseline_arousal = 0.3  # 기본 각성 수준
        self.hyperarousal_threshold = 0.7  # 과각성 임계값
        self.stress_amplification = 2.0  # 스트레스 증폭 인자
        self.filtering_failure_rate = 0.4  # 필터링 실패율
        
        # 상태
        self.current_arousal = self.baseline_arousal
        self.hypervigilance = 0.0  # 과도한 경계 상태
        self.sleep_disturbance = 0.0  # 수면 장애
        self.concentration_impairment = 0.0  # 집중력 저하
        
    def update_arousal(self, 
                      stress_level: float,
                      threat_detected: bool,
                      thalamus_filtering: float) -> float:
        """
        각성 수준 업데이트
        
        연구 근거:
        - PTSD에서 Hypothalamus의 스트레스 반응이 과도함
        - Thalamus 필터링 실패로 모든 자극이 위협으로 인식됨
        
        Args:
            stress_level: 스트레스 수준
            threat_detected: 위협 감지 여부
            thalamus_filtering: Thalamus 필터링 능력 (0.0 ~ 1.0)
            
        Returns:
            각성 수준 (0.0 ~ 1.0)
        """
        # 기본 각성
        arousal = self.baseline_arousal
        
        # 스트레스에 의한 각성 증가
        arousal += stress_level * self.stress_amplification * 0.3
        
        # 위협 감지 시 급격한 각성 증가
        if threat_detected:
            arousal += 0.4
        
        # Thalamus 필터링 실패 시 각성 증가
        filtering_failure = 1.0 - thalamus_filtering
        arousal += filtering_failure * 0.3
        
        # 각성 수준 제한
        self.current_arousal = np.clip(arousal, 0.0, 1.0)
        
        # 과각성 상태 확인
        if self.current_arousal > self.hyperarousal_threshold:
            self.hypervigilance = np.clip(
                self.hypervigilance + 0.1,
                0.0, 1.0
            )
            self.sleep_disturbance = np.clip(
                self.sleep_disturbance + 0.05,
                0.0, 1.0
            )
            self.concentration_impairment = np.clip(
                self.concentration_impairment + 0.08,
                0.0, 1.0
            )
        else:
            # 서서히 감소
            self.hypervigilance = np.clip(self.hypervigilance - 0.02, 0.0, 1.0)
            self.sleep_disturbance = np.clip(self.sleep_disturbance - 0.01, 0.0, 1.0)
            self.concentration_impairment = np.clip(
                self.concentration_impairment - 0.02, 0.0, 1.0
            )
        
        return self.current_arousal
    
    def get_hyperarousal_symptoms(self) -> Dict[str, float]:
        """
        과각성 증상 반환
        
        Returns:
            과각성 증상 딕셔너리
        """
        return {
            'arousal_level': self.current_arousal,
            'hypervigilance': self.hypervigilance,
            'sleep_disturbance': self.sleep_disturbance,
            'concentration_impairment': self.concentration_impairment
        }


class NegativeCognitionEngine:
    """
    부정적 인지 변화 엔진
    
    메커니즘:
    - PFC: 부정적 편향 (우울증 엔진 재사용 가능)
    - 기억 왜곡
    """
    
    def __init__(self, rng: Optional[np.random.Generator] = None):
        """
        부정적 인지 변화 엔진 초기화
        
        Args:
            rng: 난수 생성기
        """
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # 부정적 신념
        self.negative_beliefs: Dict[str, float] = {
            'self_blame': 0.0,  # 자기 비난
            'guilt': 0.0,  # 죄책감
            'shame': 0.0,  # 수치심
            'world_dangerous': 0.0,  # 세계는 위험하다
            'self_incompetent': 0.0  # 자신은 무능하다
        }
        
        # 동역학 파라미터
        self.belief_strengthening_rate = 0.15  # 신념 강화율
        self.memory_distortion_rate = 0.1  # 기억 왜곡율
        
        # 상태
        self.current_negative_bias = 0.0
        self.memory_gaps = 0.0  # 기억 공백
        
    def strengthen_negative_belief(self, belief_type: str, evidence: float):
        """
        부정적 신념 강화
        
        연구 근거:
        - PTSD에서 부정적 신념이 강화됨
        - 자기 비난, 죄책감, 수치심 증가
        
        Args:
            belief_type: 신념 유형
            evidence: 증거 강도
        """
        if belief_type in self.negative_beliefs:
            current = self.negative_beliefs[belief_type]
            self.negative_beliefs[belief_type] = np.clip(
                current + self.belief_strengthening_rate * evidence,
                0.0, 1.0
            )
    
    def distort_memory(self, memory_id: str, distortion_type: str) -> float:
        """
        기억 왜곡
        
        연구 근거:
        - PTSD에서 외상 관련 기억이 왜곡됨
        - 기억 공백 발생
        
        Args:
            memory_id: 기억 식별자
            distortion_type: 왜곡 유형
            
        Returns:
            왜곡 정도
        """
        # 기억 공백 증가
        self.memory_gaps = np.clip(
            self.memory_gaps + self.memory_distortion_rate,
            0.0, 1.0
        )
        
        # 왜곡 정도 반환
        return self.memory_distortion_rate
    
    def compute_negative_bias(self) -> float:
        """
        부정적 편향 수준 계산
        
        Returns:
            부정적 편향 수준 (0.0 ~ 1.0)
        """
        avg_belief = np.mean(list(self.negative_beliefs.values()))
        self.current_negative_bias = avg_belief
        return avg_belief
    
    def get_negative_cognitions(self) -> Dict[str, float]:
        """
        부정적 인지 반환
        
        Returns:
            부정적 인지 딕셔너리
        """
        return {
            **self.negative_beliefs,
            'negative_bias': self.current_negative_bias,
            'memory_gaps': self.memory_gaps
        }

