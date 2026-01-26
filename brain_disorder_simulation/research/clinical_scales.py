"""
임상 스케일 통합 모듈

우울증 연구를 위한 표준 임상 평가 도구 매핑
- HAM-D (Hamilton Depression Rating Scale)
- BDI (Beck Depression Inventory)
- PHQ-9 (Patient Health Questionnaire-9)

시뮬레이션 결과를 실제 임상 평가 도구 점수로 변환

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class HAMDScore:
    """HAM-D 점수"""
    total_score: int
    severity: str
    item_scores: Dict[str, int]
    interpretation: str


@dataclass
class BDIScore:
    """BDI 점수"""
    total_score: int
    severity: str
    item_scores: Dict[str, int]
    interpretation: str


@dataclass
class PHQ9Score:
    """PHQ-9 점수"""
    total_score: int
    severity: str
    item_scores: Dict[str, int]
    interpretation: str


class HAMDMapper:
    """
    HAM-D (Hamilton Depression Rating Scale) 매핑
    
    연구 근거:
    - 표준 우울증 평가 도구 (Hamilton, 1960)
    - 17-21 항목 평가
    - 각 항목 0-4점 또는 0-2점
    - 총점 0-52점 (17항목 기준)
    
    심각도 해석:
    - 0-7: 정상
    - 8-13: 경미한 우울증
    - 14-18: 중등도 우울증
    - 19-22: 중증 우울증
    - 23+: 매우 중증 우울증
    
    참고 문헌:
    - Hamilton (1960) - A rating scale for depression
    - Williams (1988) - A structured interview guide for the HAM-D
    """
    
    def __init__(self):
        """HAM-D 매퍼 초기화"""
        pass
    
    def map_to_hamd(self, simulation_results: Dict[str, any]) -> HAMDScore:
        """
        시뮬레이션 결과를 HAM-D 점수로 매핑
        
        ⚠️ 주의: 본 결과는 시뮬레이션 기반 연구용 결과이며 임상 진단이 아닙니다.
        
        연구 근거:
        - 시뮬레이션 결과의 각 지표를 HAM-D 항목에 매핑
        - 실제 임상 평가와 유사한 점수 체계 사용
        
        Args:
            simulation_results: 시뮬레이션 결과 딕셔너리
                - energy: 에너지 수준 (0-100)
                - motivation: 동기 수준 (0-1)
                - negative_bias: 부정적 편향 (0-1)
                - rumination: 반추 수준 (0-1)
                - sleep_quality: 수면 질 (0-1)
                - cognitive_control: 인지 제어 (0-1)
                - final_energy: 최종 에너지 (0-100)
                - final_motivation: 최종 동기 (0-1)
        
        Returns:
            HAM-D 점수 (시뮬레이션 기반)
        """
        item_scores = {}
        
        # 입력값 범위 방어
        negative_bias = np.clip(simulation_results.get('negative_bias', 0.0), 0.0, 1.0)
        rumination = np.clip(simulation_results.get('rumination', 0.0), 0.0, 1.0)
        energy = np.clip(simulation_results.get('final_energy', 100.0) / 100.0, 0.0, 1.0)
        motivation = np.clip(simulation_results.get('final_motivation', 1.0), 0.0, 1.0)
        sleep_quality = np.clip(simulation_results.get('sleep_quality', 1.0), 0.0, 1.0)
        cognitive_control = np.clip(simulation_results.get('cognitive_control', 1.0), 0.0, 1.0)
        stress_level = np.clip(simulation_results.get('stress_level', 0.0), 0.0, 1.0)
        
        # 항목 1: 우울한 기분 (Depressed Mood) - 0-4점
        if negative_bias > 0.8:
            item_scores['depressed_mood'] = 4
        elif negative_bias > 0.6:
            item_scores['depressed_mood'] = 3
        elif negative_bias > 0.4:
            item_scores['depressed_mood'] = 2
        elif negative_bias > 0.2:
            item_scores['depressed_mood'] = 1
        else:
            item_scores['depressed_mood'] = 0
        
        # 항목 2: 죄책감 (Feelings of Guilt) - 0-4점
        # 부정적 편향과 반추가 높으면 죄책감 증가
        guilt_score = (negative_bias * 0.6 + rumination * 0.4)
        if guilt_score > 0.8:
            item_scores['guilt'] = 4
        elif guilt_score > 0.6:
            item_scores['guilt'] = 3
        elif guilt_score > 0.4:
            item_scores['guilt'] = 2
        elif guilt_score > 0.2:
            item_scores['guilt'] = 1
        else:
            item_scores['guilt'] = 0
        
        # 항목 3: 자살 (Suicide) - 0-4점
        # 매우 심각한 경우만 점수 부여 (보수적 접근)
        suicide_risk = (1.0 - energy) * 0.5 + (1.0 - motivation) * 0.5
        if suicide_risk > 0.9:
            item_scores['suicide'] = 4
        elif suicide_risk > 0.7:
            item_scores['suicide'] = 3
        elif suicide_risk > 0.5:
            item_scores['suicide'] = 2
        elif suicide_risk > 0.3:
            item_scores['suicide'] = 1
        else:
            item_scores['suicide'] = 0
        
        # 항목 4: 불면증 초기 (Insomnia Early) - 0-2점
        if sleep_quality < 0.3:
            item_scores['insomnia_early'] = 2
        elif sleep_quality < 0.6:
            item_scores['insomnia_early'] = 1
        else:
            item_scores['insomnia_early'] = 0
        
        # 항목 5: 불면증 중기 (Insomnia Middle) - 0-2점
        if sleep_quality < 0.3:
            item_scores['insomnia_middle'] = 2
        elif sleep_quality < 0.6:
            item_scores['insomnia_middle'] = 1
        else:
            item_scores['insomnia_middle'] = 0
        
        # 항목 6: 불면증 말기 (Insomnia Late) - 0-2점
        if sleep_quality < 0.3:
            item_scores['insomnia_late'] = 2
        elif sleep_quality < 0.6:
            item_scores['insomnia_late'] = 1
        else:
            item_scores['insomnia_late'] = 0
        
        # 항목 7: 일과성 업무 및 활동 (Work and Activities) - 0-4점
        # 에너지 고갈과 동기 감소 반영
        work_impairment = np.clip((1.0 - energy) * 0.6 + (1.0 - motivation) * 0.4, 0.0, 1.0)
        if work_impairment > 0.8:
            item_scores['work_activities'] = 4
        elif work_impairment > 0.6:
            item_scores['work_activities'] = 3
        elif work_impairment > 0.4:
            item_scores['work_activities'] = 2
        elif work_impairment > 0.2:
            item_scores['work_activities'] = 1
        else:
            item_scores['work_activities'] = 0
        
        # 항목 8: 정신 운동 지연 (Retardation) - 0-4점
        # 동기 감소와 인지 제어 저하 반영
        retardation = np.clip((1.0 - motivation) * 0.6 + (1.0 - cognitive_control) * 0.4, 0.0, 1.0)
        if retardation > 0.8:
            item_scores['retardation'] = 4
        elif retardation > 0.6:
            item_scores['retardation'] = 3
        elif retardation > 0.4:
            item_scores['retardation'] = 2
        elif retardation > 0.2:
            item_scores['retardation'] = 1
        else:
            item_scores['retardation'] = 0
        
        # 항목 9: 초조 (Agitation) - 0-4점
        # 불안과 스트레스 반영 (우울증에서는 보통 낮음)
        if stress_level > 0.7:
            item_scores['agitation'] = 3
        elif stress_level > 0.4:
            item_scores['agitation'] = 2
        elif stress_level > 0.2:
            item_scores['agitation'] = 1
        else:
            item_scores['agitation'] = 0
        
        # 항목 10: 정신적 불안 (Anxiety Psychic) - 0-4점
        anxiety = stress_level * 0.7 + negative_bias * 0.3
        if anxiety > 0.8:
            item_scores['anxiety_psychic'] = 4
        elif anxiety > 0.6:
            item_scores['anxiety_psychic'] = 3
        elif anxiety > 0.4:
            item_scores['anxiety_psychic'] = 2
        elif anxiety > 0.2:
            item_scores['anxiety_psychic'] = 1
        else:
            item_scores['anxiety_psychic'] = 0
        
        # 항목 11: 신체적 불안 (Anxiety Somatic) - 0-4점
        if stress_level > 0.7:
            item_scores['anxiety_somatic'] = 3
        elif stress_level > 0.4:
            item_scores['anxiety_somatic'] = 2
        elif stress_level > 0.2:
            item_scores['anxiety_somatic'] = 1
        else:
            item_scores['anxiety_somatic'] = 0
        
        # 항목 12: 소화기 증상 (Somatic Symptoms Gastrointestinal) - 0-2점
        # 스트레스와 에너지 고갈 반영
        gi_symptoms = (1.0 - energy) * 0.5 + stress_level * 0.5
        if gi_symptoms > 0.6:
            item_scores['somatic_gi'] = 2
        elif gi_symptoms > 0.3:
            item_scores['somatic_gi'] = 1
        else:
            item_scores['somatic_gi'] = 0
        
        # 항목 13: 일반적인 신체 증상 (General Somatic Symptoms) - 0-2점
        if energy < 0.5:
            item_scores['somatic_general'] = 2
        elif energy < 0.7:
            item_scores['somatic_general'] = 1
        else:
            item_scores['somatic_general'] = 0
        
        # 항목 14: 성적 증상 (Genital Symptoms) - 0-2점
        # 동기 감소 반영
        if motivation < 0.3:
            item_scores['genital'] = 2
        elif motivation < 0.6:
            item_scores['genital'] = 1
        else:
            item_scores['genital'] = 0
        
        # 항목 15: 건강염려증 (Hypochondriasis) - 0-4점
        # 부정적 편향과 반추 반영
        hypochondria = np.clip(negative_bias * 0.6 + rumination * 0.4, 0.0, 1.0)
        if hypochondria > 0.7:
            item_scores['hypochondriasis'] = 3
        elif hypochondria > 0.4:
            item_scores['hypochondriasis'] = 2
        elif hypochondria > 0.2:
            item_scores['hypochondriasis'] = 1
        else:
            item_scores['hypochondriasis'] = 0
        
        # 항목 16: 체중 감소 (Loss of Weight) - 0-2점
        # 에너지 고갈 반영
        if energy < 0.4:
            item_scores['weight_loss'] = 2
        elif energy < 0.6:
            item_scores['weight_loss'] = 1
        else:
            item_scores['weight_loss'] = 0
        
        # 항목 17: 통찰력 (Insight) - 0-2점
        # 인지 제어 저하 반영
        if cognitive_control < 0.3:
            item_scores['insight'] = 2
        elif cognitive_control < 0.6:
            item_scores['insight'] = 1
        else:
            item_scores['insight'] = 0
        
        # 총점 계산
        total_score = sum(item_scores.values())
        
        # 심각도 해석
        if total_score <= 7:
            severity = "정상"
            interpretation = "우울증 증상 없음 (시뮬레이션 기반)"
        elif total_score <= 13:
            severity = "경미한 우울증"
            interpretation = "경미한 우울증 증상 (시뮬레이션 기반)"
        elif total_score <= 18:
            severity = "중등도 우울증"
            interpretation = "중등도 우울증 증상 (시뮬레이션 기반)"
        elif total_score <= 22:
            severity = "중증 우울증"
            interpretation = "중증 우울증 증상 (시뮬레이션 기반)"
        else:
            severity = "매우 중증 우울증"
            interpretation = "매우 중증 우울증 증상 (시뮬레이션 기반)"
        
        return HAMDScore(
            total_score=total_score,
            severity=severity,
            item_scores=item_scores,
            interpretation=interpretation
        )


class BDIMapper:
    """
    BDI (Beck Depression Inventory) 매핑
    
    연구 근거:
    - 자가 보고식 우울증 평가 도구 (Beck et al., 1961)
    - 21 항목, 각 0-3점
    - 총점 0-63점
    
    심각도 해석:
    - 0-9: 최소 우울증
    - 10-18: 경미한 우울증
    - 19-29: 중등도 우울증
    - 30-63: 중증 우울증
    
    참고 문헌:
    - Beck et al. (1961) - An inventory for measuring depression
    - Beck et al. (1996) - Manual for the BDI-II
    """
    
    def __init__(self):
        """BDI 매퍼 초기화"""
        pass
    
    def map_to_bdi(self, simulation_results: Dict[str, any]) -> BDIScore:
        """
        시뮬레이션 결과를 BDI 점수로 매핑
        
        ⚠️ 주의: 본 결과는 시뮬레이션 기반 연구용 결과이며 임상 진단이 아닙니다.
        
        Args:
            simulation_results: 시뮬레이션 결과 딕셔너리
        
        Returns:
            BDI 점수 (시뮬레이션 기반)
        """
        item_scores = {}
        
        # 입력값 범위 방어
        negative_bias = np.clip(simulation_results.get('negative_bias', 0.0), 0.0, 1.0)
        rumination = np.clip(simulation_results.get('rumination', 0.0), 0.0, 1.0)
        motivation = np.clip(simulation_results.get('final_motivation', 1.0), 0.0, 1.0)
        energy = np.clip(simulation_results.get('final_energy', 100.0) / 100.0, 0.0, 1.0)
        sleep_quality = np.clip(simulation_results.get('sleep_quality', 1.0), 0.0, 1.0)
        cognitive_control = np.clip(simulation_results.get('cognitive_control', 1.0), 0.0, 1.0)
        stress_level = np.clip(simulation_results.get('stress_level', 0.0), 0.0, 1.0)
        
        # 항목 1: 슬픔 (Sadness) - 0-3점
        if negative_bias > 0.75:
            item_scores['sadness'] = 3
        elif negative_bias > 0.5:
            item_scores['sadness'] = 2
        elif negative_bias > 0.25:
            item_scores['sadness'] = 1
        else:
            item_scores['sadness'] = 0
        
        # 항목 2: 비관주의 (Pessimism) - 0-3점
        if negative_bias > 0.75:
            item_scores['pessimism'] = 3
        elif negative_bias > 0.5:
            item_scores['pessimism'] = 2
        elif negative_bias > 0.25:
            item_scores['pessimism'] = 1
        else:
            item_scores['pessimism'] = 0
        
        # 항목 3: 과거의 실패 (Past Failure) - 0-3점
        if rumination > 0.75:
            item_scores['past_failure'] = 3
        elif rumination > 0.5:
            item_scores['past_failure'] = 2
        elif rumination > 0.25:
            item_scores['past_failure'] = 1
        else:
            item_scores['past_failure'] = 0
        
        # 항목 4: 즐거움 상실 (Loss of Pleasure) - 0-3점
        if motivation < 0.25:
            item_scores['loss_of_pleasure'] = 3
        elif motivation < 0.5:
            item_scores['loss_of_pleasure'] = 2
        elif motivation < 0.75:
            item_scores['loss_of_pleasure'] = 1
        else:
            item_scores['loss_of_pleasure'] = 0
        
        # 항목 5: 죄책감 (Guilty Feelings) - 0-3점
        guilt = (negative_bias * 0.6 + rumination * 0.4)
        if guilt > 0.75:
            item_scores['guilty_feelings'] = 3
        elif guilt > 0.5:
            item_scores['guilty_feelings'] = 2
        elif guilt > 0.25:
            item_scores['guilty_feelings'] = 1
        else:
            item_scores['guilty_feelings'] = 0
        
        # 항목 6: 처벌에 대한 느낌 (Punishment Feelings) - 0-3점
        if guilt > 0.75:
            item_scores['punishment_feelings'] = 3
        elif guilt > 0.5:
            item_scores['punishment_feelings'] = 2
        elif guilt > 0.25:
            item_scores['punishment_feelings'] = 1
        else:
            item_scores['punishment_feelings'] = 0
        
        # 항목 7: 자기 혐오 (Self-Dislike) - 0-3점
        if negative_bias > 0.75:
            item_scores['self_dislike'] = 3
        elif negative_bias > 0.5:
            item_scores['self_dislike'] = 2
        elif negative_bias > 0.25:
            item_scores['self_dislike'] = 1
        else:
            item_scores['self_dislike'] = 0
        
        # 항목 8: 자기 비난 (Self-Criticalness) - 0-3점
        if negative_bias > 0.75:
            item_scores['self_criticalness'] = 3
        elif negative_bias > 0.5:
            item_scores['self_criticalness'] = 2
        elif negative_bias > 0.25:
            item_scores['self_criticalness'] = 1
        else:
            item_scores['self_criticalness'] = 0
        
        # 항목 9: 자살 사고 또는 소망 (Suicidal Thoughts or Wishes) - 0-3점
        suicide_risk = np.clip((1.0 - energy) * 0.5 + (1.0 - motivation) * 0.5, 0.0, 1.0)
        if suicide_risk > 0.8:
            item_scores['suicidal_thoughts'] = 3
        elif suicide_risk > 0.6:
            item_scores['suicidal_thoughts'] = 2
        elif suicide_risk > 0.4:
            item_scores['suicidal_thoughts'] = 1
        else:
            item_scores['suicidal_thoughts'] = 0
        
        # 항목 10: 울음 (Crying) - 0-3점
        if negative_bias > 0.7:
            item_scores['crying'] = 3
        elif negative_bias > 0.5:
            item_scores['crying'] = 2
        elif negative_bias > 0.3:
            item_scores['crying'] = 1
        else:
            item_scores['crying'] = 0
        
        # 항목 11: 초조 (Agitation) - 0-3점
        if stress_level > 0.7:
            item_scores['agitation'] = 3
        elif stress_level > 0.5:
            item_scores['agitation'] = 2
        elif stress_level > 0.3:
            item_scores['agitation'] = 1
        else:
            item_scores['agitation'] = 0
        
        # 항목 12: 관심 상실 (Loss of Interest) - 0-3점
        if motivation < 0.25:
            item_scores['loss_of_interest'] = 3
        elif motivation < 0.5:
            item_scores['loss_of_interest'] = 2
        elif motivation < 0.75:
            item_scores['loss_of_interest'] = 1
        else:
            item_scores['loss_of_interest'] = 0
        
        # 항목 13: 결정력 부족 (Indecisiveness) - 0-3점
        if cognitive_control < 0.3:
            item_scores['indecisiveness'] = 3
        elif cognitive_control < 0.5:
            item_scores['indecisiveness'] = 2
        elif cognitive_control < 0.7:
            item_scores['indecisiveness'] = 1
        else:
            item_scores['indecisiveness'] = 0
        
        # 항목 14: 무가치감 (Worthlessness) - 0-3점
        if negative_bias > 0.75:
            item_scores['worthlessness'] = 3
        elif negative_bias > 0.5:
            item_scores['worthlessness'] = 2
        elif negative_bias > 0.25:
            item_scores['worthlessness'] = 1
        else:
            item_scores['worthlessness'] = 0
        
        # 항목 15: 에너지 상실 (Loss of Energy) - 0-3점
        if energy < 0.3:
            item_scores['loss_of_energy'] = 3
        elif energy < 0.5:
            item_scores['loss_of_energy'] = 2
        elif energy < 0.7:
            item_scores['loss_of_energy'] = 1
        else:
            item_scores['loss_of_energy'] = 0
        
        # 항목 16: 수면 패턴 변화 (Changes in Sleeping Pattern) - 0-3점
        if sleep_quality < 0.3:
            item_scores['sleep_changes'] = 3
        elif sleep_quality < 0.5:
            item_scores['sleep_changes'] = 2
        elif sleep_quality < 0.7:
            item_scores['sleep_changes'] = 1
        else:
            item_scores['sleep_changes'] = 0
        
        # 항목 17: 짜증 (Irritability) - 0-3점
        if stress_level > 0.7:
            item_scores['irritability'] = 3
        elif stress_level > 0.5:
            item_scores['irritability'] = 2
        elif stress_level > 0.3:
            item_scores['irritability'] = 1
        else:
            item_scores['irritability'] = 0
        
        # 항목 18: 식욕 변화 (Changes in Appetite) - 0-3점
        if energy < 0.4:
            item_scores['appetite_changes'] = 3
        elif energy < 0.6:
            item_scores['appetite_changes'] = 2
        elif energy < 0.8:
            item_scores['appetite_changes'] = 1
        else:
            item_scores['appetite_changes'] = 0
        
        # 항목 19: 집중력 부족 (Concentration Difficulty) - 0-3점
        if cognitive_control < 0.3:
            item_scores['concentration_difficulty'] = 3
        elif cognitive_control < 0.5:
            item_scores['concentration_difficulty'] = 2
        elif cognitive_control < 0.7:
            item_scores['concentration_difficulty'] = 1
        else:
            item_scores['concentration_difficulty'] = 0
        
        # 항목 20: 피로 또는 무기력 (Tiredness or Fatigue) - 0-3점
        if energy < 0.3:
            item_scores['tiredness'] = 3
        elif energy < 0.5:
            item_scores['tiredness'] = 2
        elif energy < 0.7:
            item_scores['tiredness'] = 1
        else:
            item_scores['tiredness'] = 0
        
        # 항목 21: 성적 관심 상실 (Loss of Interest in Sex) - 0-3점
        if motivation < 0.3:
            item_scores['loss_of_sex_interest'] = 3
        elif motivation < 0.5:
            item_scores['loss_of_sex_interest'] = 2
        elif motivation < 0.7:
            item_scores['loss_of_sex_interest'] = 1
        else:
            item_scores['loss_of_sex_interest'] = 0
        
        # 총점 계산
        total_score = sum(item_scores.values())
        
        # 심각도 해석
        if total_score <= 9:
            severity = "최소 우울증"
            interpretation = "최소한의 우울증 증상 (시뮬레이션 기반)"
        elif total_score <= 18:
            severity = "경미한 우울증"
            interpretation = "경미한 우울증 증상 (시뮬레이션 기반)"
        elif total_score <= 29:
            severity = "중등도 우울증"
            interpretation = "중등도 우울증 증상 (시뮬레이션 기반)"
        else:
            severity = "중증 우울증"
            interpretation = "중증 우울증 증상 (시뮬레이션 기반)"
        
        return BDIScore(
            total_score=total_score,
            severity=severity,
            item_scores=item_scores,
            interpretation=interpretation
        )


class PHQ9Mapper:
    """
    PHQ-9 (Patient Health Questionnaire-9) 매핑
    
    연구 근거:
    - 자가 보고식 우울증 선별 도구 (Kroenke et al., 2001)
    - 9 항목, 각 0-3점
    - 총점 0-27점
    
    심각도 해석:
    - 0-4: 최소 우울증
    - 5-9: 경미한 우울증
    - 10-14: 중등도 우울증
    - 15-19: 중등도-중증 우울증
    - 20-27: 중증 우울증
    
    참고 문헌:
    - Kroenke et al. (2001) - The PHQ-9: validity of a brief depression severity measure
    - Spitzer et al. (1999) - Validation and utility of a self-report version of PRIME-MD
    """
    
    def __init__(self):
        """PHQ-9 매퍼 초기화"""
        pass
    
    def map_to_phq9(self, simulation_results: Dict[str, any]) -> PHQ9Score:
        """
        시뮬레이션 결과를 PHQ-9 점수로 매핑
        
        ⚠️ 주의: 본 결과는 시뮬레이션 기반 연구용 결과이며 임상 진단이 아닙니다.
        
        Args:
            simulation_results: 시뮬레이션 결과 딕셔너리
        
        Returns:
            PHQ-9 점수 (시뮬레이션 기반)
        """
        item_scores = {}
        
        # 입력값 범위 방어
        negative_bias = np.clip(simulation_results.get('negative_bias', 0.0), 0.0, 1.0)
        motivation = np.clip(simulation_results.get('final_motivation', 1.0), 0.0, 1.0)
        energy = np.clip(simulation_results.get('final_energy', 100.0) / 100.0, 0.0, 1.0)
        sleep_quality = np.clip(simulation_results.get('sleep_quality', 1.0), 0.0, 1.0)
        cognitive_control = np.clip(simulation_results.get('cognitive_control', 1.0), 0.0, 1.0)
        stress_level = np.clip(simulation_results.get('stress_level', 0.0), 0.0, 1.0)
        
        # 항목 1: 관심이나 즐거움의 상실 (Loss of Interest or Pleasure) - 0-3점
        if motivation < 0.25:
            item_scores['loss_of_interest'] = 3
        elif motivation < 0.5:
            item_scores['loss_of_interest'] = 2
        elif motivation < 0.75:
            item_scores['loss_of_interest'] = 1
        else:
            item_scores['loss_of_interest'] = 0
        
        # 항목 2: 우울하거나 절망적인 기분 (Feeling Down or Hopeless) - 0-3점
        if negative_bias > 0.75:
            item_scores['feeling_down'] = 3
        elif negative_bias > 0.5:
            item_scores['feeling_down'] = 2
        elif negative_bias > 0.25:
            item_scores['feeling_down'] = 1
        else:
            item_scores['feeling_down'] = 0
        
        # 항목 3: 잠들기 어렵거나 잠을 너무 많이 자는 문제 (Sleep Problems) - 0-3점
        if sleep_quality < 0.3:
            item_scores['sleep_problems'] = 3
        elif sleep_quality < 0.5:
            item_scores['sleep_problems'] = 2
        elif sleep_quality < 0.7:
            item_scores['sleep_problems'] = 1
        else:
            item_scores['sleep_problems'] = 0
        
        # 항목 4: 피로하거나 에너지 부족 (Feeling Tired or Having Little Energy) - 0-3점
        if energy < 0.3:
            item_scores['tiredness'] = 3
        elif energy < 0.5:
            item_scores['tiredness'] = 2
        elif energy < 0.7:
            item_scores['tiredness'] = 1
        else:
            item_scores['tiredness'] = 0
        
        # 항목 5: 식욕 부진 또는 과식 (Poor Appetite or Overeating) - 0-3점
        if energy < 0.4:
            item_scores['appetite_problems'] = 3
        elif energy < 0.6:
            item_scores['appetite_problems'] = 2
        elif energy < 0.8:
            item_scores['appetite_problems'] = 1
        else:
            item_scores['appetite_problems'] = 0
        
        # 항목 6: 자신에 대한 나쁜 느낌 (Feeling Bad About Yourself) - 0-3점
        if negative_bias > 0.75:
            item_scores['self_worth'] = 3
        elif negative_bias > 0.5:
            item_scores['self_worth'] = 2
        elif negative_bias > 0.25:
            item_scores['self_worth'] = 1
        else:
            item_scores['self_worth'] = 0
        
        # 항목 7: 집중하거나 결정하는 데 어려움 (Trouble Concentrating or Making Decisions) - 0-3점
        if cognitive_control < 0.3:
            item_scores['concentration_trouble'] = 3
        elif cognitive_control < 0.5:
            item_scores['concentration_trouble'] = 2
        elif cognitive_control < 0.7:
            item_scores['concentration_trouble'] = 1
        else:
            item_scores['concentration_trouble'] = 0
        
        # 항목 8: 느리게 움직이거나 너무 안절부절함 (Moving or Speaking Slowly or Being Restless) - 0-3점
        # 정신 운동 지연 또는 초조
        retardation = np.clip((1.0 - motivation) * 0.6 + (1.0 - cognitive_control) * 0.4, 0.0, 1.0)
        agitation = np.clip(max(retardation, stress_level * 0.7), 0.0, 1.0)
        if agitation > 0.75:
            item_scores['psychomotor'] = 3
        elif agitation > 0.5:
            item_scores['psychomotor'] = 2
        elif agitation > 0.25:
            item_scores['psychomotor'] = 1
        else:
            item_scores['psychomotor'] = 0
        
        # 항목 9: 자해 사고 (Thoughts of Hurting Yourself) - 0-3점
        suicide_risk = np.clip((1.0 - energy) * 0.5 + (1.0 - motivation) * 0.5, 0.0, 1.0)
        if suicide_risk > 0.8:
            item_scores['self_harm_thoughts'] = 3
        elif suicide_risk > 0.6:
            item_scores['self_harm_thoughts'] = 2
        elif suicide_risk > 0.4:
            item_scores['self_harm_thoughts'] = 1
        else:
            item_scores['self_harm_thoughts'] = 0
        
        # 총점 계산
        total_score = sum(item_scores.values())
        
        # 심각도 해석
        if total_score <= 4:
            severity = "최소 우울증"
            interpretation = "최소한의 우울증 증상 (시뮬레이션 기반)"
        elif total_score <= 9:
            severity = "경미한 우울증"
            interpretation = "경미한 우울증 증상 (시뮬레이션 기반)"
        elif total_score <= 14:
            severity = "중등도 우울증"
            interpretation = "중등도 우울증 증상 (시뮬레이션 기반)"
        elif total_score <= 19:
            severity = "중등도-중증 우울증"
            interpretation = "중등도-중증 우울증 증상 (시뮬레이션 기반)"
        else:
            severity = "중증 우울증"
            interpretation = "중증 우울증 증상 (시뮬레이션 기반)"
        
        return PHQ9Score(
            total_score=total_score,
            severity=severity,
            item_scores=item_scores,
            interpretation=interpretation
        )


class ClinicalScaleMapper:
    """
    통합 임상 스케일 매퍼
    
    모든 임상 스케일을 통합하여 매핑
    """
    
    def __init__(self):
        """임상 스케일 매퍼 초기화"""
        self.hamd_mapper = HAMDMapper()
        self.bdi_mapper = BDIMapper()
        self.phq9_mapper = PHQ9Mapper()
    
    def map_all_scales(self, simulation_results: Dict[str, any]) -> Dict[str, any]:
        """
        모든 임상 스케일로 매핑
        
        Args:
            simulation_results: 시뮬레이션 결과 딕셔너리
        
        Returns:
            모든 임상 스케일 점수
        """
        return {
            'hamd': self.hamd_mapper.map_to_hamd(simulation_results),
            'bdi': self.bdi_mapper.map_to_bdi(simulation_results),
            'phq9': self.phq9_mapper.map_to_phq9(simulation_results)
        }
    
    def generate_clinical_report(self, simulation_results: Dict[str, any]) -> str:
        """
        임상 리포트 생성
        
        ⚠️ 주의: 본 결과는 시뮬레이션 기반 연구용 결과이며 임상 진단이 아닙니다.
        
        Args:
            simulation_results: 시뮬레이션 결과 딕셔너리
        
        Returns:
            임상 리포트 문자열
        """
        scales = self.map_all_scales(simulation_results)
        
        report = f"""
{'=' * 70}
임상 평가 결과 (시뮬레이션 기반)
{'=' * 70}

⚠️  중요 안내
본 결과는 시뮬레이션 기반 연구용 결과이며 임상 진단이 아닙니다.
실제 임상 진단은 전문의의 면담 및 평가가 필요합니다.

{'=' * 70}

HAM-D (Hamilton Depression Rating Scale):
  - 총점: {scales['hamd'].total_score} / 52
  - 심각도: {scales['hamd'].severity}
  - 해석: {scales['hamd'].interpretation}

BDI (Beck Depression Inventory):
  - 총점: {scales['bdi'].total_score} / 63
  - 심각도: {scales['bdi'].severity}
  - 해석: {scales['bdi'].interpretation}

PHQ-9 (Patient Health Questionnaire-9):
  - 총점: {scales['phq9'].total_score} / 27
  - 심각도: {scales['phq9'].severity}
  - 해석: {scales['phq9'].interpretation}

{'=' * 70}
"""
        return report

