"""
Normative Data 모듈

정상 참조군 데이터 정의
연령별, 성별, 발달 단계별 정상 범위
"""

from typing import Dict, Optional, Tuple
import numpy as np
from enum import Enum


class AgeGroup(Enum):
    """연령 그룹"""
    CHILD_6_12 = "6-12"  # 아동기
    ADOLESCENT_13_17 = "13-17"  # 청소년기
    ADULT_18_64 = "18-64"  # 성인기
    ELDERLY_65_PLUS = "65+"  # 노년기


class Gender(Enum):
    """성별"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class NormativeData:
    """
    정상 참조군 데이터 클래스
    
    문헌 기반 정상 범위 정의
    """
    
    def __init__(self):
        """정상 참조군 데이터 초기화"""
        # 문헌 기반 정상 범위 (예시 데이터)
        # 실제 사용 시 공개 데이터셋 또는 메타 분석 결과 사용 필요
        
        # 주의력 점수 정상 범위 (평균 ± 1SD)
        self.attention_norms = {
            AgeGroup.CHILD_6_12: {
                Gender.MALE: {'mean': 0.75, 'std': 0.15, 'min': 0.60, 'max': 0.90},
                Gender.FEMALE: {'mean': 0.78, 'std': 0.13, 'min': 0.65, 'max': 0.91}
            },
            AgeGroup.ADOLESCENT_13_17: {
                Gender.MALE: {'mean': 0.80, 'std': 0.12, 'min': 0.68, 'max': 0.92},
                Gender.FEMALE: {'mean': 0.82, 'std': 0.11, 'min': 0.71, 'max': 0.93}
            },
            AgeGroup.ADULT_18_64: {
                Gender.MALE: {'mean': 0.82, 'std': 0.10, 'min': 0.72, 'max': 0.92},
                Gender.FEMALE: {'mean': 0.84, 'std': 0.09, 'min': 0.75, 'max': 0.93}
            },
            AgeGroup.ELDERLY_65_PLUS: {
                Gender.MALE: {'mean': 0.75, 'std': 0.12, 'min': 0.63, 'max': 0.87},
                Gender.FEMALE: {'mean': 0.77, 'std': 0.11, 'min': 0.66, 'max': 0.88}
            }
        }
        
        # 충동성 점수 정상 범위
        self.impulsivity_norms = {
            AgeGroup.CHILD_6_12: {
                Gender.MALE: {'mean': 0.35, 'std': 0.15, 'min': 0.20, 'max': 0.50},
                Gender.FEMALE: {'mean': 0.30, 'std': 0.12, 'min': 0.18, 'max': 0.42}
            },
            AgeGroup.ADOLESCENT_13_17: {
                Gender.MALE: {'mean': 0.40, 'std': 0.14, 'min': 0.26, 'max': 0.54},
                Gender.FEMALE: {'mean': 0.32, 'std': 0.13, 'min': 0.19, 'max': 0.45}
            },
            AgeGroup.ADULT_18_64: {
                Gender.MALE: {'mean': 0.30, 'std': 0.12, 'min': 0.18, 'max': 0.42},
                Gender.FEMALE: {'mean': 0.25, 'std': 0.10, 'min': 0.15, 'max': 0.35}
            },
            AgeGroup.ELDERLY_65_PLUS: {
                Gender.MALE: {'mean': 0.25, 'std': 0.10, 'min': 0.15, 'max': 0.35},
                Gender.FEMALE: {'mean': 0.22, 'std': 0.09, 'min': 0.13, 'max': 0.31}
            }
        }
        
        # 과잉행동 점수 정상 범위
        self.hyperactivity_norms = {
            AgeGroup.CHILD_6_12: {
                Gender.MALE: {'mean': 0.40, 'std': 0.18, 'min': 0.22, 'max': 0.58},
                Gender.FEMALE: {'mean': 0.30, 'std': 0.15, 'min': 0.15, 'max': 0.45}
            },
            AgeGroup.ADOLESCENT_13_17: {
                Gender.MALE: {'mean': 0.35, 'std': 0.16, 'min': 0.19, 'max': 0.51},
                Gender.FEMALE: {'mean': 0.25, 'std': 0.14, 'min': 0.11, 'max': 0.39}
            },
            AgeGroup.ADULT_18_64: {
                Gender.MALE: {'mean': 0.25, 'std': 0.12, 'min': 0.13, 'max': 0.37},
                Gender.FEMALE: {'mean': 0.20, 'std': 0.10, 'min': 0.10, 'max': 0.30}
            },
            AgeGroup.ELDERLY_65_PLUS: {
                Gender.MALE: {'mean': 0.20, 'std': 0.10, 'min': 0.10, 'max': 0.30},
                Gender.FEMALE: {'mean': 0.18, 'std': 0.09, 'min': 0.09, 'max': 0.27}
            }
        }
    
    def get_age_group(self, age: int) -> AgeGroup:
        """
        연령으로부터 연령 그룹 결정
        
        Args:
            age: 나이 (세)
        
        Returns:
            연령 그룹
        """
        if 6 <= age <= 12:
            return AgeGroup.CHILD_6_12
        elif 13 <= age <= 17:
            return AgeGroup.ADOLESCENT_13_17
        elif 18 <= age <= 64:
            return AgeGroup.ADULT_18_64
        else:
            return AgeGroup.ELDERLY_65_PLUS
    
    def get_normal_range(self, 
                        metric: str,
                        age: int,
                        gender: Gender = Gender.MALE) -> Dict:
        """
        정상 범위 조회
        
        Args:
            metric: 지표 ('attention', 'impulsivity', 'hyperactivity')
            age: 나이 (세)
            gender: 성별
        
        Returns:
            정상 범위 딕셔너리
        """
        age_group = self.get_age_group(age)
        
        if metric == 'attention':
            norms = self.attention_norms.get(age_group, {}).get(gender, {})
        elif metric == 'impulsivity':
            norms = self.impulsivity_norms.get(age_group, {}).get(gender, {})
        elif metric == 'hyperactivity':
            norms = self.hyperactivity_norms.get(age_group, {}).get(gender, {})
        else:
            return {'mean': 0.5, 'std': 0.2, 'min': 0.3, 'max': 0.7}
        
        return norms if norms else {'mean': 0.5, 'std': 0.2, 'min': 0.3, 'max': 0.7}
    
    def calculate_z_score(self,
                         value: float,
                         metric: str,
                         age: int,
                         gender: Gender = Gender.MALE) -> float:
        """
        Z-score 계산 (정상 참조군 대비)
        
        Args:
            value: 측정값
            metric: 지표
            age: 나이
            gender: 성별
        
        Returns:
            Z-score
        """
        norms = self.get_normal_range(metric, age, gender)
        mean = norms.get('mean', 0.5)
        std = norms.get('std', 0.2)
        
        if std == 0:
            return 0.0
        
        z_score = (value - mean) / std
        return float(z_score)
    
    def is_within_normal_range(self,
                              value: float,
                              metric: str,
                              age: int,
                              gender: Gender = Gender.MALE,
                              threshold_sd: float = 1.5) -> Tuple[bool, Dict]:
        """
        정상 범위 내 여부 판단
        
        Args:
            value: 측정값
            metric: 지표
            age: 나이
            gender: 성별
            threshold_sd: 임계값 (표준편차 단위, 기본값 1.5)
        
        Returns:
            (정상 범위 내 여부, 상세 정보)
        """
        norms = self.get_normal_range(metric, age, gender)
        mean = norms.get('mean', 0.5)
        std = norms.get('std', 0.2)
        
        z_score = self.calculate_z_score(value, metric, age, gender)
        
        # 정상 범위: 평균 ± threshold_sd * SD
        lower_bound = mean - threshold_sd * std
        upper_bound = mean + threshold_sd * std
        
        is_normal = lower_bound <= value <= upper_bound
        
        return is_normal, {
            'value': value,
            'mean': mean,
            'std': std,
            'z_score': z_score,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'is_normal': is_normal,
            'percentile': self._z_to_percentile(z_score)
        }
    
    def _z_to_percentile(self, z_score: float) -> float:
        """
        Z-score를 백분위수로 변환
        
        Args:
            z_score: Z-score
        
        Returns:
            백분위수 (0-100)
        """
        # 정규분포 가정
        from scipy import stats
        try:
            percentile = stats.norm.cdf(z_score) * 100
            return float(percentile)
        except:
            # scipy가 없으면 근사값
            if z_score <= -2:
                return 2.3
            elif z_score <= -1.5:
                return 6.7
            elif z_score <= -1:
                return 15.9
            elif z_score <= 0:
                return 50.0
            elif z_score <= 1:
                return 84.1
            elif z_score <= 1.5:
                return 93.3
            elif z_score <= 2:
                return 97.7
            else:
                return 99.9
    
    def compare_to_normative(self,
                           attention_score: float,
                           impulsivity_score: float,
                           hyperactivity_score: float,
                           age: int,
                           gender: Gender = Gender.MALE) -> Dict:
        """
        시뮬레이션 결과를 정상 참조군과 비교
        
        Args:
            attention_score: 주의력 점수
            impulsivity_score: 충동성 점수
            hyperactivity_score: 과잉행동 점수
            age: 나이
            gender: 성별
        
        Returns:
            비교 결과
        """
        attention_info = self.is_within_normal_range(
            attention_score, 'attention', age, gender
        )
        impulsivity_info = self.is_within_normal_range(
            impulsivity_score, 'impulsivity', age, gender
        )
        hyperactivity_info = self.is_within_normal_range(
            hyperactivity_score, 'hyperactivity', age, gender
        )
        
        return {
            'age_group': self.get_age_group(age).value,
            'gender': gender.value,
            'attention': attention_info[1],
            'impulsivity': impulsivity_info[1],
            'hyperactivity': hyperactivity_info[1],
            'overall_assessment': {
                'all_normal': (attention_info[0] and 
                              impulsivity_info[0] and 
                              hyperactivity_info[0]),
                'abnormal_count': sum([
                    0 if attention_info[0] else 1,
                    0 if impulsivity_info[0] else 1,
                    0 if hyperactivity_info[0] else 1
                ])
            }
        }

