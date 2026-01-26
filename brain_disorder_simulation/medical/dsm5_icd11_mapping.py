"""
DSM-5 및 ICD-11 기준 매핑 모듈

의료 표준에 따른 ADHD 평가 기준 매핑
임상 연구용 표준화된 평가 시스템
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
import numpy as np


class ADHDSubtype(Enum):
    """ADHD 하위 타입 (DSM-5 기준)"""
    PREDOMINANTLY_INATTENTIVE = "predominantly_inattentive"  # 주의력 결핍 우세형
    PREDOMINANTLY_HYPERACTIVE_IMPULSIVE = "predominantly_hyperactive_impulsive"  # 과잉행동/충동성 우세형
    COMBINED = "combined"  # 혼합형
    UNSPECIFIED = "unspecified"  # 명시되지 않음


class ICD11Code(Enum):
    """ICD-11 ADHD 코드"""
    ADHD_6A05_0 = "6A05.0"  # 주의력 결핍 우세형
    ADHD_6A05_1 = "6A05.1"  # 과잉행동/충동성 우세형
    ADHD_6A05_2 = "6A05.2"  # 혼합형
    ADHD_6A05_Y = "6A05.Y"  # 기타 명시된 ADHD
    ADHD_6A05_Z = "6A05.Z"  # ADHD, 명시되지 않음


class DSM5Mapper:
    """
    DSM-5 기준 매핑 클래스
    
    Diagnostic and Statistical Manual of Mental Disorders, 5th Edition
    """
    
    def __init__(self):
        """DSM-5 매퍼 초기화"""
        # DSM-5 A1: 주의력 결핍 증상 (9개 항목)
        self.attention_symptoms = [
            "세부사항을 놓치거나, 학업, 직업, 또는 다른 활동에서 부주의한 실수를 함",
            "과제나 활동에 집중을 유지하는 데 어려움이 있음",
            "직접 대화를 나눌 때 듣지 않는 것처럼 보임",
            "지시를 따르지 못하고 학업이나 집안일을 끝내지 못함",
            "과제와 활동을 체계화하는 데 어려움이 있음",
            "지속적인 정신적 노력이 필요한 과제를 피하거나 싫어함",
            "과제나 활동에 필요한 물건을 잃어버림",
            "외부 자극에 쉽게 산만해짐",
            "일상 활동에서 건망증이 있음"
        ]
        
        # DSM-5 A2: 과잉행동 및 충동성 증상 (9개 항목)
        self.hyperactivity_impulsivity_symptoms = [
            "손발을 가만히 두지 못하거나 의자에 앉아서도 꿈틀거림",
            "앉아 있어야 하는 상황에서 자리를 떠남",
            "부적절한 상황에서 뛰어다니거나 기어오름",
            "조용히 여가 활동에 참여하지 못함",
            "끊임없이 움직이거나 마치 '모터에 달린 것처럼' 행동함",
            "과도하게 말함",
            "질문이 끝나기 전에 성급하게 대답함",
            "차례를 기다리기 어려움",
            "다른 사람을 방해하거나 끼어듦"
        ]
        
        # DSM-5 진단 기준
        self.min_symptoms_required = 6  # 12세 이상: 5개 이상
        self.min_age_for_diagnosis = 12  # 12세 이상 기준
        self.symptom_duration_months = 6  # 최소 6개월 지속
    
    def map_attention_deficit(self, attention_score: float, 
                             decline_rate: float,
                             sustained_attention_time: float) -> Dict:
        """
        주의력 결핍 증상 매핑 (DSM-5 A1)
        
        Args:
            attention_score: 주의력 점수 (0.0 ~ 1.0)
            decline_rate: 주의력 감소율
            sustained_attention_time: 지속 주의력 시간 (초)
        
        Returns:
            DSM-5 A1 항목 매핑 결과
        """
        # 주의력 결핍 증상 개수 추정 (시뮬레이션 기반)
        symptom_count = 0
        
        # 세부사항 놓침 (부주의한 실수)
        if attention_score < 0.3:
            symptom_count += 1
        
        # 집중 유지 어려움
        if sustained_attention_time < 5.0:  # 5초 미만
            symptom_count += 1
        
        # 지시 따르지 못함
        if decline_rate > 0.5:
            symptom_count += 1
        
        # 체계화 어려움
        if attention_score < 0.4:
            symptom_count += 1
        
        # 정신적 노력 필요한 과제 회피
        if attention_score < 0.5:
            symptom_count += 1
        
        # 물건 잃어버림 (시뮬레이션에서는 주의력 점수로 추정)
        if attention_score < 0.35:
            symptom_count += 1
        
        # 외부 자극에 산만함
        if decline_rate > 0.3:
            symptom_count += 1
        
        # 건망증
        if attention_score < 0.4:
            symptom_count += 1
        
        # 지속성 (시간에 따른 일관성)
        if decline_rate > 0.4:
            symptom_count += 1
        
        # DSM-5 A1 기준: 6개 이상 (12세 이상)
        meets_criterion_a1 = symptom_count >= self.min_symptoms_required
        
        return {
            'criterion': 'A1',
            'description': '주의력 결핍 증상',
            'symptom_count': symptom_count,
            'symptoms_required': self.min_symptoms_required,
            'meets_criterion': meets_criterion_a1,
            'attention_score': attention_score,
            'decline_rate': decline_rate,
            'sustained_attention_time': sustained_attention_time,
            'mapped_symptoms': self._map_attention_symptoms(attention_score, decline_rate)
        }
    
    def map_hyperactivity_impulsivity(self, impulsivity_score: float,
                                     hyperactivity_score: float,
                                     impulsivity_rate: float) -> Dict:
        """
        과잉행동 및 충동성 증상 매핑 (DSM-5 A2)
        
        Args:
            impulsivity_score: 충동성 점수 (0.0 ~ 1.0)
            hyperactivity_score: 과잉행동 점수 (0.0 ~ 1.0)
            impulsivity_rate: 충동적 선택 비율
        
        Returns:
            DSM-5 A2 항목 매핑 결과
        """
        symptom_count = 0
        
        # 과잉행동 증상 (6개)
        if hyperactivity_score > 0.6:
            # 손발 가만히 두지 못함
            symptom_count += 1
            # 자리 떠남
            symptom_count += 1
            # 뛰어다니거나 기어오름
            if hyperactivity_score > 0.7:
                symptom_count += 1
            # 조용히 여가 활동 참여 못함
            symptom_count += 1
            # 끊임없이 움직임
            if hyperactivity_score > 0.8:
                symptom_count += 1
        
        # 충동성 증상 (3개)
        if impulsivity_score > 0.6:
            # 과도하게 말함
            symptom_count += 1
            # 질문 끝나기 전에 대답
            if impulsivity_rate > 0.7:
                symptom_count += 1
            # 차례 기다리기 어려움
            symptom_count += 1
            # 방해하거나 끼어듦
            if impulsivity_rate > 0.75:
                symptom_count += 1
        
        # DSM-5 A2 기준: 6개 이상 (12세 이상)
        meets_criterion_a2 = symptom_count >= self.min_symptoms_required
        
        return {
            'criterion': 'A2',
            'description': '과잉행동 및 충동성 증상',
            'symptom_count': symptom_count,
            'symptoms_required': self.min_symptoms_required,
            'meets_criterion': meets_criterion_a2,
            'impulsivity_score': impulsivity_score,
            'hyperactivity_score': hyperactivity_score,
            'impulsivity_rate': impulsivity_rate,
            'mapped_symptoms': self._map_hyperactivity_symptoms(hyperactivity_score, impulsivity_score)
        }
    
    def classify_subtype(self, a1_result: Dict, a2_result: Dict) -> ADHDSubtype:
        """
        ADHD 하위 타입 분류 (DSM-5)
        
        Args:
            a1_result: A1 (주의력 결핍) 결과
            a2_result: A2 (과잉행동/충동성) 결과
        
        Returns:
            ADHD 하위 타입
        """
        meets_a1 = a1_result['meets_criterion']
        meets_a2 = a2_result['meets_criterion']
        
        if meets_a1 and meets_a2:
            return ADHDSubtype.COMBINED
        elif meets_a1:
            return ADHDSubtype.PREDOMINANTLY_INATTENTIVE
        elif meets_a2:
            return ADHDSubtype.PREDOMINANTLY_HYPERACTIVE_IMPULSIVE
        else:
            return ADHDSubtype.UNSPECIFIED
    
    def _map_attention_symptoms(self, attention_score: float, 
                               decline_rate: float) -> List[str]:
        """주의력 증상 세부 매핑"""
        symptoms = []
        if attention_score < 0.3:
            symptoms.append("세부사항 놓침")
        if decline_rate > 0.5:
            symptoms.append("집중 유지 어려움")
        if attention_score < 0.4:
            symptoms.append("체계화 어려움")
        return symptoms
    
    def _map_hyperactivity_symptoms(self, hyperactivity_score: float,
                                   impulsivity_score: float) -> List[str]:
        """과잉행동/충동성 증상 세부 매핑"""
        symptoms = []
        if hyperactivity_score > 0.6:
            symptoms.append("손발 가만히 두지 못함")
        if impulsivity_score > 0.6:
            symptoms.append("과도하게 말함")
        return symptoms


class ICD11Mapper:
    """
    ICD-11 기준 매핑 클래스
    
    International Classification of Diseases, 11th Revision
    """
    
    def __init__(self):
        """ICD-11 매퍼 초기화"""
        self.code_mapping = {
            ADHDSubtype.PREDOMINANTLY_INATTENTIVE: ICD11Code.ADHD_6A05_0,
            ADHDSubtype.PREDOMINANTLY_HYPERACTIVE_IMPULSIVE: ICD11Code.ADHD_6A05_1,
            ADHDSubtype.COMBINED: ICD11Code.ADHD_6A05_2,
            ADHDSubtype.UNSPECIFIED: ICD11Code.ADHD_6A05_Z
        }
    
    def map_to_icd11(self, dsm5_subtype: ADHDSubtype) -> ICD11Code:
        """
        DSM-5 하위 타입을 ICD-11 코드로 매핑
        
        Args:
            dsm5_subtype: DSM-5 하위 타입
        
        Returns:
            ICD-11 코드
        """
        return self.code_mapping.get(dsm5_subtype, ICD11Code.ADHD_6A05_Z)
    
    def get_code_description(self, code: ICD11Code) -> str:
        """
        ICD-11 코드 설명
        
        Args:
            code: ICD-11 코드
        
        Returns:
            코드 설명
        """
        descriptions = {
            ICD11Code.ADHD_6A05_0: "주의력 결핍 과다행동 장애, 주의력 결핍 우세형",
            ICD11Code.ADHD_6A05_1: "주의력 결핍 과다행동 장애, 과잉행동/충동성 우세형",
            ICD11Code.ADHD_6A05_2: "주의력 결핍 과다행동 장애, 혼합형",
            ICD11Code.ADHD_6A05_Y: "주의력 결핍 과다행동 장애, 기타 명시된 ADHD",
            ICD11Code.ADHD_6A05_Z: "주의력 결핍 과다행동 장애, 명시되지 않음"
        }
        return descriptions.get(code, "알 수 없음")


class ClinicalAssessmentMapper:
    """
    임상 평가 매핑 통합 클래스
    
    DSM-5 및 ICD-11 매핑을 통합하여 임상 평가 결과 생성
    """
    
    def __init__(self):
        """임상 평가 매퍼 초기화"""
        self.dsm5_mapper = DSM5Mapper()
        self.icd11_mapper = ICD11Mapper()
    
    def assess_from_simulation_results(self,
                                      attention_results: Dict,
                                      impulsivity_results: Dict,
                                      hyperactivity_results: Dict) -> Dict:
        """
        시뮬레이션 결과를 임상 평가로 변환
        
        Args:
            attention_results: 주의력 테스트 결과
            impulsivity_results: 충동성 테스트 결과
            hyperactivity_results: 과잉행동 테스트 결과
        
        Returns:
            임상 평가 결과 (DSM-5 + ICD-11)
        """
        # DSM-5 A1 매핑
        a1_result = self.dsm5_mapper.map_attention_deficit(
            attention_score=attention_results.get('mean_attention', 0.0),
            decline_rate=attention_results.get('decline_rate', 0.0),
            sustained_attention_time=attention_results.get('sustained_attention_time', 0.0)
        )
        
        # DSM-5 A2 매핑
        a2_result = self.dsm5_mapper.map_hyperactivity_impulsivity(
            impulsivity_score=impulsivity_results.get('mean_impulse_score', 0.0),
            hyperactivity_score=hyperactivity_results.get('mean_hyperactivity', 0.0),
            impulsivity_rate=impulsivity_results.get('impulsivity_rate', 0.0)
        )
        
        # 하위 타입 분류
        subtype = self.dsm5_mapper.classify_subtype(a1_result, a2_result)
        
        # ICD-11 코드 매핑
        icd11_code = self.icd11_mapper.map_to_icd11(subtype)
        
        return {
            'dsm5': {
                'criterion_a1': a1_result,
                'criterion_a2': a2_result,
                'subtype': subtype.value,
                'meets_dsm5_criteria': a1_result['meets_criterion'] or a2_result['meets_criterion']
            },
            'icd11': {
                'code': icd11_code.value,
                'description': self.icd11_mapper.get_code_description(icd11_code)
            },
            'assessment_note': '⚠️ 이 결과는 시뮬레이션 기반 패턴 평가이며, 의학적 진단이 아닙니다.',
            'clinical_recommendation': '전문의 상담 권장'
        }
    
    def format_clinical_report(self, assessment: Dict) -> str:
        """
        임상 리포트 포맷팅
        
        Args:
            assessment: 임상 평가 결과
        
        Returns:
            포맷된 리포트 문자열
        """
        report = []
        report.append("=" * 70)
        report.append("임상 평가 리포트 (시뮬레이션 기반)")
        report.append("=" * 70)
        report.append("")
        
        # DSM-5 결과
        report.append("DSM-5 평가:")
        dsm5 = assessment['dsm5']
        report.append(f"  A1 (주의력 결핍): {dsm5['criterion_a1']['symptom_count']}/{dsm5['criterion_a1']['symptoms_required']} 증상")
        report.append(f"    기준 충족: {'예' if dsm5['criterion_a1']['meets_criterion'] else '아니오'}")
        report.append(f"  A2 (과잉행동/충동성): {dsm5['criterion_a2']['symptom_count']}/{dsm5['criterion_a2']['symptoms_required']} 증상")
        report.append(f"    기준 충족: {'예' if dsm5['criterion_a2']['meets_criterion'] else '아니오'}")
        report.append(f"  하위 타입: {dsm5['subtype']}")
        report.append("")
        
        # ICD-11 결과
        report.append("ICD-11 분류:")
        icd11 = assessment['icd11']
        report.append(f"  코드: {icd11['code']}")
        report.append(f"  설명: {icd11['description']}")
        report.append("")
        
        # 주의사항
        report.append(assessment['assessment_note'])
        report.append(assessment['clinical_recommendation'])
        report.append("=" * 70)
        
        return "\n".join(report)

