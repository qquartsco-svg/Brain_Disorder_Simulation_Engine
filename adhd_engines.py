"""
ADHD 특화 엔진

주의력 제어, 충동성 제어 등 ADHD 관련 특화 엔진
"""

import numpy as np
import time
from typing import Dict, List, Optional, Tuple
from collections import deque

# 순환 버퍼 (메모리 효율적 히스토리 관리)
class CircularBuffer:
    """순환 버퍼 - O(1) 삽입/삭제"""
    def __init__(self, maxsize: int):
        self.buffer = deque(maxlen=maxsize)
        self.maxsize = maxsize
    
    def append(self, value: float):
        self.buffer.append(value)
    
    def get_window(self, window_size: int) -> np.ndarray:
        if len(self.buffer) < window_size:
            return np.array(list(self.buffer))
        return np.array(list(self.buffer)[-window_size:])
    
    def get_all(self) -> np.ndarray:
        return np.array(list(self.buffer))
    
    def get_variance(self, window_size: Optional[int] = None) -> float:
        if window_size is None:
            data = self.get_all()
        else:
            data = self.get_window(window_size)
        if len(data) == 0:
            return 0.0
        return float(np.var(data))
    
    def get_mean(self, window_size: Optional[int] = None) -> float:
        if window_size is None:
            data = self.get_all()
        else:
            data = self.get_window(window_size)
        if len(data) == 0:
            return 0.0
        return float(np.mean(data))
    
    def __len__(self) -> int:
        return len(self.buffer)


class AttentionControlEngine:
    """
    주의력 제어 엔진
    
    ADHD의 주의력 결핍을 시뮬레이션하고 측정
    """
    
    def __init__(self, rng: Optional[np.random.Generator] = None):
        """
        주의력 제어 엔진 초기화
        
        Args:
            rng: 재현 가능한 랜덤 생성기 (None이면 전역 RNG 사용)
        """
        self.attention_level = 1.0  # 기본 주의력 레벨
        self.distraction_threshold = 0.5
        self.sustained_attention_time = 0.0
        
        # CircularBuffer로 메모리 효율적 히스토리 관리
        self.attention_history = CircularBuffer(maxsize=1000)
        self.distraction_history = CircularBuffer(maxsize=1000)
        self.last_update_time = time.time()
        
        # RNG (재현성 보장)
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # ADHD 특성 파라미터
        self.attention_decay_rate = 0.02  # 주의력 감소율
        self.distraction_sensitivity = 1.5  # 주의 분산 민감도
        self.recovery_rate = 0.01  # 주의력 회복율
    
    def calculate_attention(self, task_importance: float, 
                          distractions: List[Dict], 
                          time_elapsed: float) -> float:
        """
        주의력 점수 계산 (의료 기준: 포화 방지)
        
        Args:
            task_importance: 작업 중요도 (0.0 ~ 1.0)
            distractions: 주의 분산 요인 리스트
            time_elapsed: 경과 시간 (초)
        
        Returns:
            attention_score: 주의력 점수 (0.0 ~ 1.0)
        """
        # 이전 주의력 (관성 효과)
        previous_attention = self.attention_history[-1] if len(self.attention_history) > 0 else self.attention_level
        
        # 기본 주의력 (작업 중요도 기반)
        base_attention = self.attention_level * task_importance
        
        # 시간에 따른 주의력 감소 (ADHD 특성)
        time_decay = np.exp(-self.attention_decay_rate * time_elapsed)
        base_attention *= time_decay
        
        # 주의 분산 효과
        distraction_penalty = 0.0
        for dist in distractions:
            intensity = dist.get('intensity', 0.0)
            relevance = dist.get('relevance', 0.5)
            distraction_penalty += intensity * relevance * self.distraction_sensitivity
        
        # 주의력 점수 계산
        attention_score = max(self.min_attention, base_attention - distraction_penalty)
        
        # 의료 기준: 관성 효과 (이전 값 영향)
        attention_score = (self.attention_inertia * previous_attention + 
                          (1.0 - self.attention_inertia) * attention_score)
        
        # 의료 기준: 강화된 회복 메커니즘 (포화 탈출)
        if attention_score < self.distraction_threshold:
            # 포화 상태에서 강제 회복
            recovery_boost = self.recovery_strength * (1.0 - attention_score / self.min_attention)
            attention_score = min(1.0, attention_score + recovery_boost)
        
        # 의료 기준: 무작위 각성 스파이크 (인지적 진동)
        arousal_spike = self.rng.normal(0.0, self.arousal_noise_scale)
        attention_score = np.clip(attention_score + arousal_spike, self.min_attention, 1.0)
        
        return float(attention_score)
    
    def maintain_attention(self, task: Dict, distractions: List[Dict], 
                          time_elapsed: float) -> Dict:
        """
        주의력 유지 및 측정
        
        Returns:
            result: 주의력 상태 딕셔너리
        """
        task_importance = task.get('importance', 0.5)
        
        attention_score = self.calculate_attention(
            task_importance, distractions, time_elapsed
        )
        
        # 주의력 결핍 감지
        is_attention_deficit = attention_score < self.distraction_threshold
        
        # 지속 주의력 시간 업데이트
        if attention_score > self.distraction_threshold:
            self.sustained_attention_time += 0.1
        else:
            self.sustained_attention_time = max(0.0, self.sustained_attention_time - 0.2)
        
        # 히스토리 저장 (CircularBuffer는 자동으로 크기 제한)
        self.attention_history.append(attention_score)
        
        total_distraction = sum(d.get('intensity', 0.0) for d in distractions)
        self.distraction_history.append(total_distraction)
        
        return {
            'attention_score': attention_score,
            'is_attention_deficit': is_attention_deficit,
            'sustained_attention_time': self.sustained_attention_time,
            'distraction_level': total_distraction,
            'pattern': 'adhd' if is_attention_deficit else 'normal'
        }
    
    def get_attention_trend(self) -> Dict:
        """주의력 추세 분석"""
        if len(self.attention_history) < 10:
            return {'trend': 'insufficient_data'}
        
        recent = self.attention_history.get_window(10)
        earlier = self.attention_history.get_window(20)[:10] if len(self.attention_history) >= 20 else recent[:10]
        
        recent_avg = np.mean(recent)
        earlier_avg = np.mean(earlier)
        
        trend = recent_avg - earlier_avg
        
        if trend < -0.2:
            return {'trend': 'declining', 'rate': float(trend)}
        elif trend > 0.1:
            return {'trend': 'improving', 'rate': float(trend)}
        else:
            return {'trend': 'stable', 'rate': float(trend)}
    
    def get_attention_variability(self, window_size: int = 10) -> Dict:
        """
        주의력 변동성 분석 (ADHD 특성)
        
        Args:
            window_size: 분석 윈도우 크기
        
        Returns:
            변동성 지표 (분산, 자기상관, 드롭아웃 비율)
        """
        if len(self.attention_history) < window_size:
            return {'variance': 0.0, 'autocorr': 0.0, 'dropout_rate': 0.0}
        
        window = self.attention_history.get_window(window_size)
        
        # 분산
        variance = float(np.var(window))
        
        # 자기상관 (지속성)
        if len(window) > 1:
            autocorr = float(np.corrcoef(window[:-1], window[1:])[0, 1])
            if np.isnan(autocorr):
                autocorr = 0.0
        else:
            autocorr = 0.0
        
        # 드롭아웃 비율 (임계값 이하)
        dropout_count = np.sum(window < self.distraction_threshold)
        dropout_rate = float(dropout_count / len(window))
        
        return {
            'variance': variance,
            'autocorr': autocorr,
            'dropout_rate': dropout_rate
        }


class ImpulseControlEngine:
    """
    충동성 제어 엔진
    
    ADHD의 충동성을 시뮬레이션하고 측정
    """
    
    def __init__(self, rng: Optional[np.random.Generator] = None):
        """
        충동성 제어 엔진 초기화
        
        Args:
            rng: 재현 가능한 랜덤 생성기
        """
        self.impulse_threshold = 0.7
        self.delay_tolerance = 0.5
        
        # CircularBuffer 사용
        self.impulse_history = CircularBuffer(maxsize=1000)
        self.choice_history = deque(maxlen=100)
        
        # RNG (재현성 보장)
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # ADHD 특성 파라미터
        self.discount_rate = 0.5  # 시간 할인율 (ADHD는 높음 - 0.5로 증가)
        self.impulse_sensitivity = 1.5  # 충동성 민감도 (1.5로 증가)
    
    def calculate_impulse_preference(self, immediate_reward: float,
                                   delayed_reward: float,
                                   delay_time: float) -> float:
        """
        충동성 선호도 계산
        
        Args:
            immediate_reward: 즉각적 보상
            delayed_reward: 지연된 보상
            delay_time: 지연 시간 (초)
        
        Returns:
            impulse_score: 충동성 점수 (0.0 ~ 1.0)
        """
        # 시간 할인 (ADHD는 높은 할인율)
        # delay_time을 분 단위로 변환하여 더 현실적인 할인 적용
        delay_minutes = delay_time / 60.0
        discount_factor = 1.0 / (1.0 + self.discount_rate * delay_minutes)
        discounted_delayed = delayed_reward * discount_factor
        
        # 즉각적 보상 선호도 계산
        if immediate_reward > 0:
            # 할인된 지연 보상과 즉각 보상 비교
            if discounted_delayed > immediate_reward:
                # 지연된 보상이 여전히 더 크지만, ADHD는 높은 할인율로 인해
                # 즉각 보상을 선호할 가능성이 높음
                # 비율이 작을수록 (즉각 보상이 상대적으로 작을수록) 충동성은 낮지만
                # ADHD는 여전히 즉각 보상을 선호할 수 있음
                ratio = immediate_reward / discounted_delayed
                # ADHD 특성: 비율이 낮아도 지연 시간이 길면 충동성 증가
                base_impulse = (1.0 - ratio) * 0.3
                # 지연 시간이 길수록 충동성 증가
                time_boost = min(0.4, delay_minutes * 0.1)
                impulse_score = base_impulse + time_boost
            else:
                # 즉각적 보상이 더 크면 높은 충동성
                ratio = discounted_delayed / immediate_reward
                impulse_score = 1.0 - ratio
        else:
            impulse_score = 0.0
        
        # ADHD 특성: 지연 시간이 길수록 충동성 증가
        if delay_time > 10:  # 10초 이상 지연
            time_impulse_boost = min(0.5, (delay_time - 10) / 50.0)
            impulse_score = min(1.0, impulse_score + time_impulse_boost)
        
        return min(1.0, impulse_score * self.impulse_sensitivity)
    
    def control_impulse(self, immediate_reward: float,
                       delayed_reward: float,
                       delay_time: float,
                       goal_context: Optional[Dict] = None) -> Dict:
        """
        충동성 제어 및 측정
        
        Returns:
            result: 충동성 상태 딕셔너리
        """
        impulse_score = self.calculate_impulse_preference(
            immediate_reward, delayed_reward, delay_time
        )
        
        # 목표 맥락 고려 (PFC의 목표 관리)
        goal_strength = 0.0
        if goal_context:
            goal_strength = goal_context.get('strength', 0.0)
            # 목표가 강하면 충동성 감소
            impulse_score *= (1.0 - goal_strength * 0.5)
        
        # 충동성 판단
        is_high_impulsivity = impulse_score > self.impulse_threshold
        
        # 선택 예측 (충동성 점수가 높으면 즉각적 보상 선호)
        # ADHD는 높은 충동성을 가지므로, 점수가 0.3 이상이면 즉각적 보상 선호
        if impulse_score > 0.3:
            choice = 'immediate_reward'
        else:
            choice = 'delayed_reward'
        
        # 히스토리 저장 (CircularBuffer는 자동으로 크기 제한)
        self.impulse_history.append(impulse_score)
        self.choice_history.append(choice)
        
        return {
            'impulse_score': impulse_score,
            'is_high_impulsivity': is_high_impulsivity,
            'predicted_choice': choice,
            'delay_tolerance': self.delay_tolerance,
            'pattern': 'adhd' if is_high_impulsivity else 'normal'
        }
    
    def get_impulse_trend(self) -> Dict:
        """충동성 추세 분석"""
        if len(self.impulse_history) < 10:
            return {'trend': 'insufficient_data'}
        
        recent_choices = list(self.choice_history)[-10:]
        if len(recent_choices) == 0:
            return {'trend': 'insufficient_data', 'impulsivity_rate': 0.0}
        
        immediate_count = sum(1 for c in recent_choices if c == 'immediate_reward')
        impulsivity_rate = immediate_count / len(recent_choices)
        
        return {
            'trend': 'high_impulsivity' if impulsivity_rate > 0.7 else 'normal',
            'impulsivity_rate': float(impulsivity_rate)
        }


class HyperactivityEngine:
    """
    과잉행동 엔진
    
    ADHD의 과잉행동을 시뮬레이션하고 측정
    """
    
    def __init__(self, rng: Optional[np.random.Generator] = None):
        """
        과잉행동 엔진 초기화
        
        Args:
            rng: 재현 가능한 랜덤 생성기
        """
        self.energy_variance_threshold = 100.0
        
        # CircularBuffer 사용
        self.energy_history = CircularBuffer(maxsize=1000)
        self.movement_history = CircularBuffer(maxsize=1000)
        
        # RNG (재현성 보장)
        self.rng = rng if rng is not None else np.random.default_rng()
        
        # ADHD 특성 파라미터
        self.energy_volatility = 1.5  # 에너지 변동성
        self.restlessness_factor = 0.3  # 안절부절함
        
        # 의료 기준: 에너지 소비 파라미터
        self.energy_consumption_rate = 0.5  # 과잉행동 시 에너지 소비율
        self.energy_recovery_rate = 0.1  # 에너지 회복율
        self.energy_min = 20.0  # 최소 에너지 (고갈 방지)
        self.energy_max = 100.0  # 최대 에너지
    
    def calculate_hyperactivity(self, current_energy: float,
                               task_demand: float,
                               time_elapsed: float) -> Dict:
        """
        과잉행동 측정 (의료 기준: 에너지 동역학 연결)
        
        Args:
            current_energy: 현재 에너지 레벨
            task_demand: 작업 요구도
            time_elapsed: 경과 시간
        
        Returns:
            result: 과잉행동 상태 딕셔너리 (에너지 소비 포함)
        """
        # 의료 기준: 에너지 동역학 (에너지가 실제로 변동)
        # 이전 에너지
        previous_energy = self.energy_history[-1] if len(self.energy_history) > 0 else current_energy
        
        # 에너지 변화율 (dE/dt)
        energy_change_rate = (current_energy - previous_energy) / 0.1 if len(self.energy_history) > 0 else 0.0
        
        # 에너지 히스토리 저장
        self.energy_history.append(current_energy)
        
        # 에너지 변동성 계산
        if len(self.energy_history) >= 10:
            energy_variance = self.energy_history.get_variance(window_size=10)
        else:
            energy_variance = 0.0
        
        # 작업 요구도와 에너지 불일치
        energy_mismatch = abs(current_energy - task_demand * 100.0) / 100.0  # 정규화
        
        # 안절부절함 (에너지가 높지만 작업 요구도가 낮을 때)
        restlessness = 0.0
        if current_energy > task_demand * 100.0 * 1.5:
            restlessness = min(1.0, (current_energy - task_demand * 100.0 * 1.5) / 100.0 * self.restlessness_factor)
        
        # 의료 기준: 과잉행동 점수 (에너지 변화율 포함)
        hyperactivity_score = min(1.0, (
            energy_variance / self.energy_variance_threshold * 0.3 +  # 변동성 기여도 감소
            energy_mismatch * 0.3 +
            restlessness * 0.2 +
            abs(energy_change_rate) / 10.0 * 0.2  # 에너지 변화율 기여도 추가
        ))
        
        is_hyperactive = hyperactivity_score > 0.6
        
        # 의료 기준: 에너지 소비 계산 (과잉행동 시 에너지 소모)
        energy_consumed = 0.0
        if is_hyperactive:
            energy_consumed = hyperactivity_score * self.energy_consumption_rate * 0.1  # dt=0.1 고려
        
        # 다음 에너지 예측 (소비 반영)
        next_energy = max(self.energy_min, 
                         min(self.energy_max, 
                             current_energy - energy_consumed + self.energy_recovery_rate * 0.1))
        
        return {
            'hyperactivity_score': float(hyperactivity_score),
            'is_hyperactive': is_hyperactive,
            'energy_variance': float(energy_variance),
            'energy_mismatch': float(energy_mismatch),
            'restlessness': float(restlessness),
            'energy_change_rate': float(energy_change_rate),
            'energy_consumed': float(energy_consumed),
            'next_energy': float(next_energy),  # 다음 스텝 예측 에너지
            'pattern': 'adhd' if is_hyperactive else 'normal'
        }
    
    def get_energy_trend(self) -> Dict:
        """에너지 추세 분석"""
        if len(self.energy_history) < 10:
            return {'trend': 'insufficient_data'}
        
        recent = self.energy_history.get_window(10)
        variance = float(np.var(recent))
        mean_energy = float(np.mean(recent))
        
        return {
            'trend': 'high_variance' if variance > 50 else 'stable',
            'variance': variance,
            'mean_energy': mean_energy
        }
    
    def analyze_movement_patterns(self, window_size: int = 10) -> Dict:
        """
        움직임 패턴 분석
        
        Args:
            window_size: 분석 윈도우 크기
        
        Returns:
            움직임 패턴 지표 (burstiness, fidget_rate, dwell_time)
        """
        if len(self.energy_history) < window_size:
            return {'burstiness': 0.0, 'fidget_rate': 0.0, 'dwell_time': 0.0}
        
        window = self.energy_history.get_window(window_size)
        
        # Burstiness (군집성) - 높은 값이 연속으로 나오는 패턴
        bursts = 0
        for i in range(1, len(window)):
            if window[i] > 0.7 and window[i-1] > 0.7:
                bursts += 1
        burstiness = float(bursts / len(window)) if len(window) > 0 else 0.0
        
        # Fidget rate (작은 움직임 빈도)
        fidget_threshold = 0.3
        fidget_count = np.sum((window > 0.1) & (window < fidget_threshold))
        fidget_rate = float(fidget_count / len(window)) if len(window) > 0 else 0.0
        
        # Dwell time (지속 시간) - 높은 값이 지속되는 구간의 평균 길이
        high_periods = []
        current_period = 0
        for val in window:
            if val > 0.7:
                current_period += 1
            else:
                if current_period > 0:
                    high_periods.append(current_period)
                current_period = 0
        if current_period > 0:
            high_periods.append(current_period)
        
        dwell_time = float(np.mean(high_periods)) if len(high_periods) > 0 else 0.0
        
        return {
            'burstiness': burstiness,
            'fidget_rate': fidget_rate,
            'dwell_time': dwell_time
        }

