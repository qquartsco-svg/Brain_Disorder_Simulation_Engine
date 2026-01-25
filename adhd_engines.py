"""
ADHD 특화 엔진

주의력 제어, 충동성 제어 등 ADHD 관련 특화 엔진
"""

import numpy as np
import time
from typing import Dict, List, Optional, Tuple


class AttentionControlEngine:
    """
    주의력 제어 엔진
    
    ADHD의 주의력 결핍을 시뮬레이션하고 측정
    """
    
    def __init__(self):
        self.attention_level = 1.0  # 기본 주의력 레벨
        self.distraction_threshold = 0.5
        self.sustained_attention_time = 0.0
        self.attention_history: List[float] = []
        self.distraction_history: List[float] = []
        self.last_update_time = time.time()
        
        # ADHD 특성 파라미터
        self.attention_decay_rate = 0.02  # 주의력 감소율
        self.distraction_sensitivity = 1.5  # 주의 분산 민감도
        self.recovery_rate = 0.01  # 주의력 회복율
    
    def calculate_attention(self, task_importance: float, 
                          distractions: List[Dict], 
                          time_elapsed: float) -> float:
        """
        주의력 점수 계산
        
        Args:
            task_importance: 작업 중요도 (0.0 ~ 1.0)
            distractions: 주의 분산 요인 리스트
            time_elapsed: 경과 시간 (초)
        
        Returns:
            attention_score: 주의력 점수 (0.0 ~ 1.0)
        """
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
        attention_score = max(0.0, base_attention - distraction_penalty)
        
        # 주의력 회복 (약간)
        if attention_score < self.attention_level:
            attention_score += self.recovery_rate * (1.0 - attention_score)
        
        return min(1.0, attention_score)
    
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
        
        # 히스토리 저장
        self.attention_history.append(attention_score)
        if len(self.attention_history) > 1000:
            self.attention_history.pop(0)
        
        total_distraction = sum(d.get('intensity', 0.0) for d in distractions)
        self.distraction_history.append(total_distraction)
        if len(self.distraction_history) > 1000:
            self.distraction_history.pop(0)
        
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
        
        recent = self.attention_history[-10:]
        earlier = self.attention_history[-20:-10] if len(self.attention_history) >= 20 else recent[:10]
        
        recent_avg = np.mean(recent)
        earlier_avg = np.mean(earlier)
        
        trend = recent_avg - earlier_avg
        
        if trend < -0.2:
            return {'trend': 'declining', 'rate': trend}
        elif trend > 0.1:
            return {'trend': 'improving', 'rate': trend}
        else:
            return {'trend': 'stable', 'rate': trend}


class ImpulseControlEngine:
    """
    충동성 제어 엔진
    
    ADHD의 충동성을 시뮬레이션하고 측정
    """
    
    def __init__(self):
        self.impulse_threshold = 0.7
        self.delay_tolerance = 0.5
        self.impulse_history: List[float] = []
        self.choice_history: List[str] = []
        
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
        
        # 히스토리 저장
        self.impulse_history.append(impulse_score)
        if len(self.impulse_history) > 1000:
            self.impulse_history.pop(0)
        
        self.choice_history.append(choice)
        if len(self.choice_history) > 100:
            self.choice_history.pop(0)
        
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
        
        recent_choices = self.choice_history[-10:]
        immediate_count = sum(1 for c in recent_choices if c == 'immediate_reward')
        impulsivity_rate = immediate_count / len(recent_choices)
        
        return {
            'trend': 'high_impulsivity' if impulsivity_rate > 0.7 else 'normal',
            'impulsivity_rate': impulsivity_rate
        }


class HyperactivityEngine:
    """
    과잉행동 엔진
    
    ADHD의 과잉행동을 시뮬레이션하고 측정
    """
    
    def __init__(self):
        self.energy_variance_threshold = 100.0
        self.energy_history: List[float] = []
        self.movement_history: List[float] = []
        
        # ADHD 특성 파라미터
        self.energy_volatility = 1.5  # 에너지 변동성
        self.restlessness_factor = 0.3  # 안절부절함
    
    def calculate_hyperactivity(self, current_energy: float,
                               task_demand: float,
                               time_elapsed: float) -> Dict:
        """
        과잉행동 측정
        
        Args:
            current_energy: 현재 에너지 레벨
            task_demand: 작업 요구도
            time_elapsed: 경과 시간
        
        Returns:
            result: 과잉행동 상태 딕셔너리
        """
        # 에너지 히스토리 저장
        self.energy_history.append(current_energy)
        if len(self.energy_history) > 1000:
            self.energy_history.pop(0)
        
        # 에너지 변동성 계산
        if len(self.energy_history) >= 10:
            energy_variance = np.var(self.energy_history[-10:])
        else:
            energy_variance = 0.0
        
        # 작업 요구도와 에너지 불일치
        energy_mismatch = abs(current_energy - task_demand)
        
        # 안절부절함 (에너지가 높지만 작업 요구도가 낮을 때)
        restlessness = 0.0
        if current_energy > task_demand * 1.5:
            restlessness = (current_energy - task_demand * 1.5) * self.restlessness_factor
        
        # 과잉행동 점수
        hyperactivity_score = min(1.0, (
            energy_variance / self.energy_variance_threshold * 0.5 +
            energy_mismatch * 0.3 +
            restlessness * 0.2
        ))
        
        is_hyperactive = hyperactivity_score > 0.6
        
        return {
            'hyperactivity_score': hyperactivity_score,
            'is_hyperactive': is_hyperactive,
            'energy_variance': energy_variance,
            'energy_mismatch': energy_mismatch,
            'restlessness': restlessness,
            'pattern': 'adhd' if is_hyperactive else 'normal'
        }
    
    def get_energy_trend(self) -> Dict:
        """에너지 추세 분석"""
        if len(self.energy_history) < 10:
            return {'trend': 'insufficient_data'}
        
        recent = self.energy_history[-10:]
        variance = np.var(recent)
        mean_energy = np.mean(recent)
        
        return {
            'trend': 'high_variance' if variance > 50 else 'stable',
            'variance': variance,
            'mean_energy': mean_energy
        }

