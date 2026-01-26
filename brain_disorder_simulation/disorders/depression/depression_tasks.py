"""
우울증 특화 태스크

우울증 메커니즘을 정량적으로 측정하는 전용 태스크들
목적: "왜 이런 상황이 발생할 수 있는가?" 원인 분석

⚠️ 주의: 이 태스크들은 치료 도구가 아닙니다.
"""

import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class TaskResult:
    """태스크 결과"""
    task_name: str
    success: bool
    metrics: Dict
    pattern_observation: str


class MotivationCollapseTask:
    """
    동기 붕괴 태스크
    
    핵심 질문: "왜 동기가 사라지는가?"
    
    측정:
    - 보상 민감도 감소
    - 노력 비용 증가
    - 동기 루프 단절 지점
    """
    
    def __init__(self, motivation_engine, rng: Optional[np.random.Generator] = None):
        """
        동기 붕괴 태스크 초기화
        
        Args:
            motivation_engine: MotivationEngine 인스턴스
            rng: 난수 생성기
        """
        self.motivation_engine = motivation_engine
        self.rng = rng if rng is not None else np.random.default_rng()
    
    def run(self, num_trials: int = 20) -> TaskResult:
        """
        동기 붕괴 태스크 실행
        
        Args:
            num_trials: 시행 횟수
        
        Returns:
            태스크 결과
        """
        results = {
            'trials': [],
            'motivation_history': [],
            'reward_sensitivity_history': [],
            'effort_cost_history': [],
            'collapse_point': None
        }
        
        initial_motivation = self.motivation_engine.state.motivation_level
        
        for trial in range(num_trials):
            # 보상 기회 제시
            reward_value = 0.3 + self.rng.random() * 0.5
            effort_required = 0.3 + self.rng.random() * 0.5
            
            # 동기 평가
            evaluation = self.motivation_engine.evaluate_action(
                expected_reward=reward_value,
                effort_required=effort_required,
                delay=0.0
            )
            
            # 행동 결정
            if evaluation['should_act']:
                # 행동 실행
                reward_result = self.motivation_engine.process_reward(
                    reward_value=reward_value,
                    effort_required=effort_required
                )
                action_taken = True
            else:
                action_taken = False
                reward_result = {
                    'perceived_reward': 0.0,
                    'pleasure': 0.0,
                    'effort_cost': effort_required * self.motivation_engine.state.effort_cost,
                    'motivation_gain': 0.0,
                    'can_engage': False
                }
            
            # 데이터 기록
            results['trials'].append({
                'trial': trial,
                'action_taken': action_taken,
                'motivation_level': self.motivation_engine.state.motivation_level,
                'reward_sensitivity': self.motivation_engine.state.reward_sensitivity,
                'effort_cost': self.motivation_engine.state.effort_cost,
                'anhedonia': self.motivation_engine.state.anhedonia
            })
            
            results['motivation_history'].append(self.motivation_engine.state.motivation_level)
            results['reward_sensitivity_history'].append(self.motivation_engine.state.reward_sensitivity)
            results['effort_cost_history'].append(self.motivation_engine.state.effort_cost)
            
            # 붕괴 지점 감지 (동기가 0.2 이하로 떨어지고 회복 불가)
            if (self.motivation_engine.state.motivation_level < 0.2 and 
                results['collapse_point'] is None):
                results['collapse_point'] = trial
        
        # 결과 분석
        final_motivation = self.motivation_engine.state.motivation_level
        motivation_decrease = initial_motivation - final_motivation
        
        if results['collapse_point'] is not None:
            pattern = f"동기 붕괴 (시행 {results['collapse_point']}에서 발생)"
        elif final_motivation < 0.3:
            pattern = "동기 저하 (붕괴 직전)"
        else:
            pattern = "동기 유지"
        
        metrics = {
            'initial_motivation': initial_motivation,
            'final_motivation': final_motivation,
            'motivation_decrease': motivation_decrease,
            'collapse_point': results['collapse_point'],
            'average_reward_sensitivity': np.mean(results['reward_sensitivity_history']),
            'average_effort_cost': np.mean(results['effort_cost_history']),
            'action_rate': sum(1 for t in results['trials'] if t['action_taken']) / num_trials
        }
        
        return TaskResult(
            task_name='Motivation Collapse Task',
            success=True,
            metrics=metrics,
            pattern_observation=pattern
        )


class RuminationPersistenceTask:
    """
    반추 지속 태스크
    
    핵심 질문: "왜 부정적 사고가 지속되는가?"
    
    측정:
    - 반추 강도
    - 억제 제어 실패율
    - 부정적 루프 지속 시간
    """
    
    def __init__(self, negative_bias_engine, cognitive_control_engine, 
                 rng: Optional[np.random.Generator] = None):
        """
        반추 지속 태스크 초기화
        
        Args:
            negative_bias_engine: NegativeBiasEngine 인스턴스
            cognitive_control_engine: CognitiveControlEngine 인스턴스
            rng: 난수 생성기
        """
        self.negative_bias_engine = negative_bias_engine
        self.cognitive_control_engine = cognitive_control_engine
        self.rng = rng if rng is not None else np.random.default_rng()
    
    def run(self, duration: float = 60.0, dt: float = 0.1) -> TaskResult:
        """
        반추 지속 태스크 실행
        
        Args:
            duration: 시뮬레이션 지속 시간 (초)
            dt: 시간 간격
        
        Returns:
            태스크 결과
        """
        steps = int(duration / dt)
        
        results = {
            'rumination_history': [],
            'inhibition_success_history': [],
            'negative_loop_history': [],
            'stimulus_events': []
        }
        
        for step in range(steps):
            t = step * dt
            
            # 부정적 자극 제시 (5초마다)
            if step % 50 == 0:
                stimulus_valence = -0.6 - self.rng.random() * 0.3  # 부정적 자극
                stimulus_intensity = 0.6 + self.rng.random() * 0.4
                
                bias_result = self.negative_bias_engine.process_stimulus(
                    stimulus_valence=stimulus_valence,
                    stimulus_intensity=stimulus_intensity,
                    time_elapsed=t
                )
                
                results['stimulus_events'].append({
                    'time': t,
                    'valence': stimulus_valence,
                    'rumination_triggered': bias_result.get('rumination_triggered', False)
                })
            
            # 부정적 사고 처리 (2초마다)
            if step % 20 == 0:
                thought_intensity = 0.4 + self.rng.random() * 0.4
                thought_result = self.cognitive_control_engine.process_negative_thought(
                    thought_intensity=thought_intensity,
                    time_elapsed=t
                )
                
                results['inhibition_success_history'].append(
                    thought_result.get('inhibition_success', False)
                )
            
            # 상태 업데이트
            self.negative_bias_engine.update_rumination(dt)
            self.cognitive_control_engine.update_negative_loop(dt)
            
            # 데이터 기록 (1초마다)
            if step % 10 == 0:
                results['rumination_history'].append(
                    self.negative_bias_engine.state.rumination_strength
                )
                results['negative_loop_history'].append(
                    self.cognitive_control_engine.state.negative_thought_loop
                )
        
        # 결과 분석
        avg_rumination = np.mean(results['rumination_history'])
        max_rumination = np.max(results['rumination_history'])
        inhibition_success_rate = np.mean(results['inhibition_success_history']) if results['inhibition_success_history'] else 0.0
        avg_negative_loop = np.mean(results['negative_loop_history'])
        
        if avg_rumination > 0.6:
            pattern = "강한 반추 지속"
        elif avg_rumination > 0.3:
            pattern = "중간 반추 지속"
        else:
            pattern = "약한 반추"
        
        metrics = {
            'average_rumination': avg_rumination,
            'max_rumination': max_rumination,
            'inhibition_success_rate': inhibition_success_rate,
            'average_negative_loop': avg_negative_loop,
            'rumination_persistence': avg_rumination * (1.0 - inhibition_success_rate)
        }
        
        return TaskResult(
            task_name='Rumination Persistence Task',
            success=True,
            metrics=metrics,
            pattern_observation=pattern
        )


class EffortBasedDecisionMakingTask:
    """
    노력 기반 의사결정 태스크
    
    핵심 질문: "왜 노력 대비 포기하는가?"
    
    측정:
    - 보상-노력 비율
    - 포기 임계점
    - 에너지 소비 패턴
    """
    
    def __init__(self, motivation_engine, energy_engine,
                 rng: Optional[np.random.Generator] = None):
        """
        노력 기반 의사결정 태스크 초기화
        
        Args:
            motivation_engine: MotivationEngine 인스턴스
            energy_engine: EnergyDepletionEngine 인스턴스
            rng: 난수 생성기
        """
        self.motivation_engine = motivation_engine
        self.energy_engine = energy_engine
        self.rng = rng if rng is not None else np.random.default_rng()
    
    def run(self, num_tasks: int = 15, dt: float = 0.1) -> TaskResult:
        """
        노력 기반 의사결정 태스크 실행
        
        Args:
            num_tasks: 작업 수
            dt: 시간 간격
        
        Returns:
            태스크 결과
        """
        results = {
            'tasks': [],
            'acceptance_rate': 0.0,
            'rejection_rate': 0.0,
            'energy_history': [],
            'motivation_history': []
        }
        
        accepted = 0
        rejected = 0
        
        for task_idx in range(num_tasks):
            # 작업 제시 (보상과 노력)
            reward_value = 0.4 + self.rng.random() * 0.4
            effort_required = 0.2 + self.rng.random() * 0.6
            
            # 현재 에너지 확인
            current_energy = self.energy_engine.state.current_energy / 100.0
            
            # 동기 평가
            evaluation = self.motivation_engine.evaluate_action(
                expected_reward=reward_value,
                effort_required=effort_required,
                delay=0.0
            )
            
            # 의사결정
            if evaluation['should_act'] and current_energy > 0.2:
                # 작업 수락
                accepted += 1
                
                # 에너지 소비
                energy_result = self.energy_engine.update_energy(
                    cognitive_load=effort_required,
                    stress_level=0.3,
                    dt=dt * 10  # 작업 시간
                )
                
                # 보상 처리
                reward_result = self.motivation_engine.process_reward(
                    reward_value=reward_value,
                    effort_required=effort_required
                )
                
                task_result = 'accepted'
            else:
                # 작업 거부
                rejected += 1
                task_result = 'rejected'
            
            # 데이터 기록
            results['tasks'].append({
                'task': task_idx,
                'reward': reward_value,
                'effort': effort_required,
                'decision': task_result,
                'energy': self.energy_engine.state.current_energy / 100.0,
                'motivation': self.motivation_engine.state.motivation_level
            })
            
            results['energy_history'].append(self.energy_engine.state.current_energy / 100.0)
            results['motivation_history'].append(self.motivation_engine.state.motivation_level)
        
        results['acceptance_rate'] = accepted / num_tasks
        results['rejection_rate'] = rejected / num_tasks
        
        # 결과 분석
        if results['acceptance_rate'] < 0.3:
            pattern = "높은 포기율 (에너지/동기 부족)"
        elif results['acceptance_rate'] < 0.6:
            pattern = "중간 포기율"
        else:
            pattern = "낮은 포기율"
        
        metrics = {
            'acceptance_rate': results['acceptance_rate'],
            'rejection_rate': results['rejection_rate'],
            'final_energy': results['energy_history'][-1] if results['energy_history'] else 0.0,
            'final_motivation': results['motivation_history'][-1] if results['motivation_history'] else 0.0,
            'energy_decrease': results['energy_history'][0] - results['energy_history'][-1] if len(results['energy_history']) > 1 else 0.0
        }
        
        return TaskResult(
            task_name='Effort-Based Decision Making Task',
            success=True,
            metrics=metrics,
            pattern_observation=pattern
        )

