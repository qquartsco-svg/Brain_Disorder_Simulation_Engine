"""
PK/PD 모델 (약물동태학/약력학)

의료 기준에 따른 정밀한 약물 효과 시뮬레이션
1-compartment, 2-compartment 모델 지원
"""

import numpy as np
from typing import Dict, Optional, List, Tuple
from collections import deque
from scipy import optimize


class PKModel:
    """
    약물동태학 (Pharmacokinetics) 모델
    
    약물의 흡수, 분포, 대사, 배설 (ADME) 모델링
    """
    
    def __init__(self, model_type: str = 'one_compartment'):
        """
        PK 모델 초기화
        
        Args:
            model_type: 모델 타입 ('one_compartment', 'two_compartment')
        """
        self.model_type = model_type
        self.concentration_history = deque(maxlen=10000)
        self.time_history = deque(maxlen=10000)
    
    def one_compartment_oral(self,
                           dose: float,
                           ka: float,  # 흡수 속도 상수
                           ke: float,  # 제거 속도 상수
                           vd: float,  # 분포 용적
                           time: float) -> float:
        """
        1-compartment 경구 투여 모델
        
        C(t) = (ka * F * D) / (vd * (ka - ke)) * (e^(-ke*t) - e^(-ka*t))
        
        Args:
            dose: 투여량 (mg)
            ka: 흡수 속도 상수 (1/h)
            ke: 제거 속도 상수 (1/h)
            vd: 분포 용적 (L)
            time: 경과 시간 (h)
        
        Returns:
            concentration: 혈장 농도 (mg/L)
        """
        F = 1.0  # 생체이용률 (기본값 100%)
        
        if ka == ke:
            # 특수 케이스: ka = ke
            concentration = (ka * F * dose) / vd * time * np.exp(-ka * time)
        else:
            concentration = (ka * F * dose) / (vd * (ka - ke)) * (
                np.exp(-ke * time) - np.exp(-ka * time)
            )
        
        return max(0.0, float(concentration))
    
    def two_compartment_iv(self,
                          dose: float,
                          alpha: float,  # 빠른 상 (분포)
                          beta: float,   # 느린 상 (제거)
                          A: float,      # 계수 A
                          B: float,      # 계수 B
                          time: float) -> float:
        """
        2-compartment 정맥 투여 모델
        
        C(t) = A * e^(-alpha*t) + B * e^(-beta*t)
        
        Args:
            dose: 투여량 (mg)
            alpha: 빠른 상 (1/h)
            beta: 느린 상 (1/h)
            A: 계수 A
            B: 계수 B
            time: 경과 시간 (h)
        
        Returns:
            concentration: 혈장 농도 (mg/L)
        """
        concentration = A * np.exp(-alpha * time) + B * np.exp(-beta * time)
        return max(0.0, float(concentration))
    
    def calculate_auc(self, time_points: List[float], 
                     concentrations: List[float]) -> float:
        """
        AUC (Area Under Curve) 계산
        
        Args:
            time_points: 시간 점 목록
            concentrations: 농도 목록
        
        Returns:
            AUC 값
        """
        if len(time_points) < 2:
            return 0.0
        
        auc = 0.0
        for i in range(len(time_points) - 1):
            dt = time_points[i+1] - time_points[i]
            avg_conc = (concentrations[i] + concentrations[i+1]) / 2.0
            auc += avg_conc * dt
        
        return float(auc)
    
    def calculate_clearance(self, dose: float, auc: float) -> float:
        """
        Clearance (CL) 계산
        
        CL = Dose / AUC
        
        Args:
            dose: 투여량
            auc: AUC 값
        
        Returns:
            clearance: 청소율 (L/h)
        """
        if auc == 0:
            return 0.0
        return float(dose / auc)
    
    def calculate_half_life(self, ke: float) -> float:
        """
        반감기 (Half-life) 계산
        
        t1/2 = ln(2) / ke
        
        Args:
            ke: 제거 속도 상수
        
        Returns:
            half_life: 반감기 (h)
        """
        if ke == 0:
            return float('inf')
        return float(np.log(2) / ke)


class PDModel:
    """
    약력학 (Pharmacodynamics) 모델
    
    약물 농도와 효과의 관계 모델링
    """
    
    def __init__(self):
        """PD 모델 초기화"""
        self.effect_history = deque(maxlen=10000)
    
    def emax_model(self,
                  concentration: float,
                  emax: float,      # 최대 효과
                  ec50: float,     # 50% 효과 농도
                  hill_coefficient: float = 1.0) -> float:
        """
        Emax 모델 (Hill equation)
        
        E = (Emax * C^n) / (EC50^n + C^n)
        
        Args:
            concentration: 약물 농도
            emax: 최대 효과
            ec50: 50% 효과 농도
            hill_coefficient: Hill 계수 (기본값 1.0)
        
        Returns:
            effect: 효과 (0.0 ~ emax)
        """
        if concentration <= 0:
            return 0.0
        
        numerator = emax * (concentration ** hill_coefficient)
        denominator = (ec50 ** hill_coefficient) + (concentration ** hill_coefficient)
        
        effect = numerator / denominator if denominator > 0 else 0.0
        return float(np.clip(effect, 0.0, emax))
    
    def linear_model(self,
                    concentration: float,
                    slope: float,
                    baseline: float = 0.0) -> float:
        """
        선형 모델
        
        E = baseline + slope * C
        
        Args:
            concentration: 약물 농도
            slope: 기울기
            baseline: 기저 효과
        
        Returns:
            effect: 효과
        """
        effect = baseline + slope * concentration
        return float(max(0.0, effect))
    
    def sigmoid_model(self,
                     concentration: float,
                     emax: float,
                     ec50: float,
                     gamma: float = 1.0) -> float:
        """
        시그모이드 모델
        
        E = Emax / (1 + (EC50 / C)^gamma)
        
        Args:
            concentration: 약물 농도
            emax: 최대 효과
            ec50: 50% 효과 농도
            gamma: 시그모이드 계수
        
        Returns:
            effect: 효과
        """
        if concentration <= 0:
            return 0.0
        
        ratio = ec50 / concentration
        effect = emax / (1.0 + (ratio ** gamma))
        return float(np.clip(effect, 0.0, emax))


class MedicationPKPD:
    """
    약물 PK/PD 통합 모델
    
    의료 기준에 따른 정밀한 약물 효과 시뮬레이션
    """
    
    def __init__(self, rng: Optional[np.random.Generator] = None):
        """
        PK/PD 모델 초기화
        
        Args:
            rng: 재현 가능한 랜덤 생성기
        """
        self.rng = rng if rng is not None else np.random.default_rng()
        
        self.pk_model = PKModel()
        self.pd_model = PDModel()
        
        # 약물 데이터베이스 (문헌 기반 파라미터)
        self.medication_db = {
            'methylphenidate': {
                'pk': {
                    'model': 'one_compartment',
                    'ka': 2.5,      # 흡수 속도 (1/h)
                    'ke': 0.23,     # 제거 속도 (1/h) - 반감기 약 3시간
                    'vd': 2.1,      # 분포 용적 (L/kg, 체중 70kg 기준 147L)
                    'bioavailability': 0.9  # 생체이용률
                },
                'pd': {
                    'model': 'emax',
                    'emax_dopamine': 0.4,    # 최대 도파민 증가
                    'ec50_dopamine': 10.0,   # 50% 효과 농도 (ng/mL)
                    'emax_attention': 0.5,   # 최대 주의력 개선
                    'ec50_attention': 12.0,
                    'hill_coefficient': 1.2
                },
                'dosing': {
                    'standard_dose': 10.0,   # 표준 용량 (mg)
                    'max_dose': 60.0,        # 최대 용량 (mg)
                    'dosing_interval': 4.0   # 투여 간격 (h)
                }
            },
            'atomoxetine': {
                'pk': {
                    'model': 'one_compartment',
                    'ka': 0.8,      # 흡수 속도 (1/h) - 더 느림
                    'ke': 0.14,     # 제거 속도 (1/h) - 반감기 약 5시간
                    'vd': 0.85,     # 분포 용적 (L/kg)
                    'bioavailability': 0.63  # 생체이용률
                },
                'pd': {
                    'model': 'emax',
                    'emax_dopamine': 0.25,   # 더 약한 효과
                    'ec50_dopamine': 15.0,
                    'emax_attention': 0.35,
                    'ec50_attention': 18.0,
                    'hill_coefficient': 1.0
                },
                'dosing': {
                    'standard_dose': 40.0,
                    'max_dose': 100.0,
                    'dosing_interval': 24.0  # 1일 1회
                }
            },
            'amphetamine': {
                'pk': {
                    'model': 'one_compartment',
                    'ka': 3.0,
                    'ke': 0.35,     # 반감기 약 2시간
                    'vd': 3.5,
                    'bioavailability': 0.75
                },
                'pd': {
                    'model': 'emax',
                    'emax_dopamine': 0.5,
                    'ec50_dopamine': 8.0,
                    'emax_attention': 0.6,
                    'ec50_attention': 10.0,
                    'hill_coefficient': 1.5
                },
                'dosing': {
                    'standard_dose': 5.0,
                    'max_dose': 40.0,
                    'dosing_interval': 4.0
                }
            }
        }
        
        # 현재 약물 상태
        self.active_medications = {}  # {medication_type: {dose, time, ...}}
    
    def administer_medication(self,
                            medication_type: str,
                            dose: float,
                            time: float,
                            route: str = 'oral'):
        """
        약물 투여
        
        Args:
            medication_type: 약물 종류
            dose: 투여량 (mg)
            time: 투여 시간 (초)
            route: 투여 경로 ('oral', 'iv')
        """
        if medication_type not in self.medication_db:
            raise ValueError(f"Unknown medication: {medication_type}")
        
        med_data = self.medication_db[medication_type]
        
        # 용량 검증
        if dose > med_data['dosing']['max_dose']:
            raise ValueError(f"Dose exceeds maximum: {dose} > {med_data['dosing']['max_dose']}")
        
        if medication_type not in self.active_medications:
            self.active_medications[medication_type] = []
        
        self.active_medications[medication_type].append({
            'dose': dose,
            'time': time,
            'route': route
        })
    
    def get_concentration(self,
                        medication_type: str,
                        current_time: float) -> float:
        """
        현재 약물 농도 계산
        
        Args:
            medication_type: 약물 종류
            current_time: 현재 시간 (초)
        
        Returns:
            concentration: 혈장 농도 (ng/mL)
        """
        if medication_type not in self.active_medications:
            return 0.0
        
        med_data = self.medication_db[medication_type]
        pk_params = med_data['pk']
        
        total_concentration = 0.0
        
        for administration in self.active_medications[medication_type]:
            dose = administration['dose']
            admin_time = administration['time']
            elapsed_hours = (current_time - admin_time) / 3600.0
            
            if elapsed_hours < 0:
                continue
            
            if pk_params['model'] == 'one_compartment':
                # 농도 단위 변환: mg → ng/mL (1 mg/L = 1000 ng/mL)
                # 분포 용적을 L/kg에서 L로 변환 (70kg 기준)
                vd_liters = pk_params['vd'] * 70.0
                concentration_mg_l = self.pk_model.one_compartment_oral(
                    dose=dose,
                    ka=pk_params['ka'],
                    ke=pk_params['ke'],
                    vd=vd_liters,
                    time=elapsed_hours
                )
                # mg/L → ng/mL 변환
                concentration_ng_ml = concentration_mg_l * 1000.0
                total_concentration += concentration_ng_ml
        
        return float(total_concentration)
    
    def get_pharmacodynamic_effect(self,
                                  medication_type: str,
                                  current_time: float) -> Dict:
        """
        약력학 효과 계산
        
        Args:
            medication_type: 약물 종류
            current_time: 현재 시간 (초)
        
        Returns:
            effect: 도파민 증가, 주의력 개선 등
        """
        if medication_type not in self.active_medications:
            return {
                'dopamine_boost': 0.0,
                'attention_boost': 0.0,
                'concentration': 0.0
            }
        
        med_data = self.medication_db[medication_type]
        pd_params = med_data['pd']
        
        # 현재 농도
        concentration = self.get_concentration(medication_type, current_time)
        
        # 약력학 효과 (Emax 모델)
        dopamine_boost = self.pd_model.emax_model(
            concentration=concentration,
            emax=pd_params['emax_dopamine'],
            ec50=pd_params['ec50_dopamine'],
            hill_coefficient=pd_params['hill_coefficient']
        )
        
        attention_boost = self.pd_model.emax_model(
            concentration=concentration,
            emax=pd_params['emax_attention'],
            ec50=pd_params['ec50_attention'],
            hill_coefficient=pd_params['hill_coefficient']
        )
        
        return {
            'dopamine_boost': float(dopamine_boost),
            'attention_boost': float(attention_boost),
            'concentration': float(concentration),
            'medication_type': medication_type
        }
    
    def get_all_medication_effects(self, current_time: float) -> Dict:
        """
        모든 활성 약물의 효과 합산
        
        Args:
            current_time: 현재 시간 (초)
        
        Returns:
            total_effect: 총 효과
        """
        total_dopamine_boost = 0.0
        total_attention_boost = 0.0
        concentrations = {}
        
        for medication_type in self.active_medications.keys():
            effect = self.get_pharmacodynamic_effect(medication_type, current_time)
            total_dopamine_boost += effect['dopamine_boost']
            total_attention_boost += effect['attention_boost']
            concentrations[medication_type] = effect['concentration']
        
        # 효과 상한 (과다 복용 방지)
        total_dopamine_boost = min(0.8, total_dopamine_boost)
        total_attention_boost = min(0.9, total_attention_boost)
        
        return {
            'dopamine_boost': float(total_dopamine_boost),
            'attention_boost': float(total_attention_boost),
            'concentrations': concentrations,
            'n_active_medications': len(self.active_medications)
        }
    
    def clear_medications(self):
        """모든 약물 제거"""
        self.active_medications = {}
    
    def get_medication_summary(self, current_time: float) -> Dict:
        """
        약물 상태 요약
        
        Args:
            current_time: 현재 시간 (초)
        
        Returns:
            summary: 약물 상태 요약
        """
        summary = {
            'active_medications': list(self.active_medications.keys()),
            'total_effects': self.get_all_medication_effects(current_time),
            'individual_effects': {}
        }
        
        for medication_type in self.active_medications.keys():
            summary['individual_effects'][medication_type] = {
                'concentration': self.get_concentration(medication_type, current_time),
                'effect': self.get_pharmacodynamic_effect(medication_type, current_time)
            }
        
        return summary

