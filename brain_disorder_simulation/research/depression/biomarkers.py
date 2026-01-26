"""
생체지표 매핑 모듈

우울증 연구를 위한 생체지표 추출 및 매핑
fMRI, EEG, HRV 등 실제 연구에서 사용되는 생체지표

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class FMRIBiomarkers:
    """fMRI 활성화 패턴"""
    pfc_activation: float = 1.0          # 전전두엽 피질 활성화
    amygdala_activation: float = 1.0    # 편도체 활성화
    hypothalamus_activation: float = 1.0 # 시상하부 활성화
    basal_ganglia_activation: float = 1.0 # 선조체 활성화
    default_mode_network: float = 1.0    # Default Mode Network
    salience_network: float = 1.0        # Salience Network
    executive_network: float = 1.0       # Executive Network


@dataclass
class EEGBiomarkers:
    """EEG 패턴"""
    alpha_power: float = 1.0             # Alpha 파 (8-13 Hz)
    beta_power: float = 1.0             # Beta 파 (13-30 Hz)
    theta_power: float = 1.0            # Theta 파 (4-8 Hz)
    delta_power: float = 1.0            # Delta 파 (0.5-4 Hz)
    gamma_power: float = 1.0            # Gamma 파 (30-100 Hz)
    theta_beta_ratio: float = 1.0       # Theta/Beta 비율
    alpha_asymmetry: float = 0.0         # Alpha 비대칭 (좌-우)


@dataclass
class HRVBiomarkers:
    """HRV (Heart Rate Variability) 생체지표"""
    rmssd: float = 1.0                   # RMSSD (부교감 신경 활성)
    sdnn: float = 1.0                   # SDNN (전체 변이도)
    lf_hf_ratio: float = 1.0            # LF/HF 비율
    hf_power: float = 1.0               # HF 파워 (부교감 신경)
    lf_power: float = 1.0               # LF 파워 (교감 신경)


class FMRIBiomarkerExtractor:
    """
    fMRI 활성화 패턴 추출
    
    연구 근거:
    - 우울증에서 PFC 활성화 감소
    - Amygdala 활성화 증가
    - Default Mode Network 과활성화
    - Executive Network 활성화 감소
    
    참고 문헌:
    - Drevets et al. (2008) - Neuroimaging and depression
    - Hamilton et al. (2012) - Default mode network in depression
    """
    
    def __init__(self):
        """fMRI 생체지표 추출기 초기화"""
        pass
    
    def extract_fmri_pattern(self, brain_state: Dict) -> FMRIBiomarkers:
        """
        뇌 상태에서 fMRI 패턴 추출
        
        연구 근거:
        - PFC 활성화: 인지 제어, 부정적 편향, 반추와 관련
        - Amygdala 활성화: 부정적 감정 처리, 위협 감지
        - Hypothalamus 활성화: 에너지 대사, 스트레스 반응
        - Basal Ganglia 활성화: 동기, 보상 처리
        
        Args:
            brain_state: 뇌 상태 딕셔너리
                - pfc_activity: PFC 활동 수준
                - amygdala_activity: Amygdala 활동 수준
                - hypothalamus_activity: Hypothalamus 활동 수준
                - basal_ganglia_activity: Basal Ganglia 활동 수준
                - negative_bias: 부정적 편향 수준
                - energy_level: 에너지 수준
        
        Returns:
            fMRI 생체지표
        """
        # PFC 활성화 (인지 제어, 부정적 편향, 반추)
        # 우울증에서는 PFC 활성화 감소
        pfc_base = brain_state.get('pfc_activity', 1.0)
        negative_bias = brain_state.get('negative_bias', 0.0)
        rumination = brain_state.get('rumination', 0.0)
        
        # 부정적 편향과 반추가 높으면 PFC 활성화 감소
        pfc_activation = pfc_base * (1.0 - negative_bias * 0.3 - rumination * 0.2)
        pfc_activation = np.clip(pfc_activation, 0.0, 1.0)
        
        # Amygdala 활성화 (부정적 감정 처리, 위협 감지)
        # 우울증에서는 Amygdala 활성화 증가
        amygdala_base = brain_state.get('amygdala_activity', 1.0)
        amygdala_activation = amygdala_base * (1.0 + negative_bias * 0.5)
        amygdala_activation = np.clip(amygdala_activation, 0.0, 2.0)
        
        # Hypothalamus 활성화 (에너지 대사, 스트레스 반응)
        energy_level = brain_state.get('energy_level', 1.0)
        stress_level = brain_state.get('stress_level', 0.0)
        hypothalamus_activation = (energy_level * 0.6 + stress_level * 0.4)
        hypothalamus_activation = np.clip(hypothalamus_activation, 0.0, 1.0)
        
        # Basal Ganglia 활성화 (동기, 보상 처리)
        # 우울증에서는 Basal Ganglia 활성화 감소
        basal_ganglia_base = brain_state.get('basal_ganglia_activity', 1.0)
        motivation = brain_state.get('motivation', 1.0)
        basal_ganglia_activation = basal_ganglia_base * motivation
        basal_ganglia_activation = np.clip(basal_ganglia_activation, 0.0, 1.0)
        
        # Default Mode Network (DMN)
        # 우울증에서는 DMN 과활성화
        dmn_base = 1.0
        dmn_activation = dmn_base * (1.0 + rumination * 0.4 + negative_bias * 0.3)
        dmn_activation = np.clip(dmn_activation, 0.0, 2.0)
        
        # Salience Network
        # 우울증에서는 Salience Network 활성화 변화
        salience_base = 1.0
        salience_activation = salience_base * (1.0 + negative_bias * 0.2)
        salience_activation = np.clip(salience_activation, 0.0, 1.5)
        
        # Executive Network
        # 우울증에서는 Executive Network 활성화 감소
        executive_base = brain_state.get('executive_control', 1.0)
        executive_activation = executive_base * (1.0 - negative_bias * 0.3)
        executive_activation = np.clip(executive_activation, 0.0, 1.0)
        
        return FMRIBiomarkers(
            pfc_activation=pfc_activation,
            amygdala_activation=amygdala_activation,
            hypothalamus_activation=hypothalamus_activation,
            basal_ganglia_activation=basal_ganglia_activation,
            default_mode_network=dmn_activation,
            salience_network=salience_activation,
            executive_network=executive_activation
        )


class EEGBiomarkerExtractor:
    """
    EEG 패턴 추출
    
    연구 근거:
    - 우울증에서 Alpha 파 감소
    - Beta 파 증가
    - Theta/Beta 비율 변화
    - Alpha 비대칭 (좌측 감소)
    
    참고 문헌:
    - Thibodeau et al. (2006) - EEG and depression
    - Bruder et al. (2017) - Alpha asymmetry in depression
    """
    
    def __init__(self):
        """EEG 생체지표 추출기 초기화"""
        pass
    
    def extract_eeg_pattern(self, brain_state: Dict) -> EEGBiomarkers:
        """
        뇌 상태에서 EEG 패턴 추출
        
        연구 근거:
        - Alpha 파 (8-13 Hz): 휴식 상태, 우울증에서는 감소
        - Beta 파 (13-30 Hz): 각성, 인지 활동, 우울증에서는 증가
        - Theta 파 (4-8 Hz): 수면, 우울증에서는 증가
        - Delta 파 (0.5-4 Hz): 깊은 수면
        - Gamma 파 (30-100 Hz): 인지 결합
        
        Args:
            brain_state: 뇌 상태 딕셔너리
                - arousal_level: 각성 수준
                - energy_level: 에너지 수준
                - negative_bias: 부정적 편향
                - sleep_quality: 수면 질
        
        Returns:
            EEG 생체지표
        """
        arousal = brain_state.get('arousal_level', 1.0)
        energy = brain_state.get('energy_level', 1.0)
        negative_bias = brain_state.get('negative_bias', 0.0)
        sleep_quality = brain_state.get('sleep_quality', 1.0)
        
        # Alpha 파 (8-13 Hz)
        # 우울증에서는 Alpha 파 감소
        alpha_base = 1.0
        alpha_power = alpha_base * (1.0 - negative_bias * 0.4 - (1.0 - energy) * 0.3)
        alpha_power = np.clip(alpha_power, 0.0, 1.0)
        
        # Beta 파 (13-30 Hz)
        # 우울증에서는 Beta 파 증가 (불안, 각성)
        beta_base = 1.0
        beta_power = beta_base * (1.0 + negative_bias * 0.3 + (1.0 - sleep_quality) * 0.2)
        beta_power = np.clip(beta_power, 0.0, 2.0)
        
        # Theta 파 (4-8 Hz)
        # 우울증에서는 Theta 파 증가 (피로, 수면 장애)
        theta_base = 1.0
        theta_power = theta_base * (1.0 + (1.0 - energy) * 0.4 + (1.0 - sleep_quality) * 0.3)
        theta_power = np.clip(theta_power, 0.0, 2.0)
        
        # Delta 파 (0.5-4 Hz)
        # 수면 질과 관련
        delta_base = 1.0
        delta_power = delta_base * sleep_quality
        delta_power = np.clip(delta_power, 0.0, 1.0)
        
        # Gamma 파 (30-100 Hz)
        # 인지 결합, 우울증에서는 감소
        gamma_base = 1.0
        gamma_power = gamma_base * (1.0 - negative_bias * 0.2)
        gamma_power = np.clip(gamma_power, 0.0, 1.0)
        
        # Theta/Beta 비율
        # 우울증에서는 Theta/Beta 비율 증가
        theta_beta_ratio = theta_power / (beta_power + 0.001)
        
        # Alpha 비대칭 (좌측 - 우측)
        # 우울증에서는 좌측 Alpha 감소 (부정적 감정)
        alpha_asymmetry = -negative_bias * 0.5  # 좌측 감소
        
        return EEGBiomarkers(
            alpha_power=alpha_power,
            beta_power=beta_power,
            theta_power=theta_power,
            delta_power=delta_power,
            gamma_power=gamma_power,
            theta_beta_ratio=theta_beta_ratio,
            alpha_asymmetry=alpha_asymmetry
        )


class HRVBiomarkerExtractor:
    """
    HRV (Heart Rate Variability) 생체지표 추출
    
    연구 근거:
    - 우울증에서 RMSSD 감소 (부교감 신경 활성 감소)
    - LF/HF 비율 변화
    - 전체 변이도 감소
    
    참고 문헌:
    - Kemp et al. (2010) - HRV and depression
    - Carney et al. (2005) - HRV in depression
    """
    
    def __init__(self):
        """HRV 생체지표 추출기 초기화"""
        pass
    
    def extract_hrv(self, 
                    energy_state: Dict,
                    stress_level: float,
                    sleep_quality: float = 1.0) -> HRVBiomarkers:
        """
        에너지 상태에서 HRV 추출
        
        연구 근거:
        - RMSSD: 부교감 신경 활성 지표, 우울증에서는 감소
        - SDNN: 전체 변이도, 우울증에서는 감소
        - LF/HF 비율: 교감/부교감 신경 균형
        - HF 파워: 부교감 신경 활성
        - LF 파워: 교감 신경 활성
        
        Args:
            energy_state: 에너지 상태 딕셔너리
                - current_energy: 현재 에너지 수준
                - recovery_rate: 회복 속도
            stress_level: 스트레스 수준 (0.0 ~ 1.0)
            sleep_quality: 수면 질 (0.0 ~ 1.0)
        
        Returns:
            HRV 생체지표
        """
        energy = energy_state.get('current_energy', 100.0) / 100.0
        recovery_rate = energy_state.get('recovery_rate', 0.05) / 0.05
        
        # RMSSD (Root Mean Square of Successive Differences)
        # 부교감 신경 활성 지표, 우울증에서는 감소
        rmssd_base = 1.0
        rmssd = rmssd_base * energy * sleep_quality * recovery_rate
        rmssd = np.clip(rmssd, 0.0, 1.0)
        
        # SDNN (Standard Deviation of NN intervals)
        # 전체 변이도, 우울증에서는 감소
        sdnn_base = 1.0
        sdnn = sdnn_base * energy * (1.0 - stress_level * 0.3)
        sdnn = np.clip(sdnn, 0.0, 1.0)
        
        # HF 파워 (High Frequency, 0.15-0.4 Hz)
        # 부교감 신경 활성, 우울증에서는 감소
        hf_power = rmssd * 1.2  # RMSSD와 유사
        hf_power = np.clip(hf_power, 0.0, 1.5)
        
        # LF 파워 (Low Frequency, 0.04-0.15 Hz)
        # 교감 신경 활성, 우울증에서는 변화
        lf_power = 1.0 + stress_level * 0.3
        lf_power = np.clip(lf_power, 0.0, 2.0)
        
        # LF/HF 비율
        # 교감/부교감 신경 균형, 우울증에서는 증가
        lf_hf_ratio = lf_power / (hf_power + 0.001)
        
        return HRVBiomarkers(
            rmssd=rmssd,
            sdnn=sdnn,
            lf_hf_ratio=lf_hf_ratio,
            hf_power=hf_power,
            lf_power=lf_power
        )


class BiomarkerExtractor:
    """
    통합 생체지표 추출기
    
    fMRI, EEG, HRV 생체지표를 통합 추출
    """
    
    def __init__(self):
        """생체지표 추출기 초기화"""
        self.fmri_extractor = FMRIBiomarkerExtractor()
        self.eeg_extractor = EEGBiomarkerExtractor()
        self.hrv_extractor = HRVBiomarkerExtractor()
    
    def extract_all_biomarkers(self,
                              brain_state: Dict,
                              energy_state: Dict,
                              stress_level: float = 0.0,
                              sleep_quality: float = 1.0) -> Dict:
        """
        모든 생체지표 추출
        
        Args:
            brain_state: 뇌 상태 딕셔너리
            energy_state: 에너지 상태 딕셔너리
            stress_level: 스트레스 수준
            sleep_quality: 수면 질
        
        Returns:
            모든 생체지표 딕셔너리
        """
        fmri = self.fmri_extractor.extract_fmri_pattern(brain_state)
        eeg = self.eeg_extractor.extract_eeg_pattern(brain_state)
        hrv = self.hrv_extractor.extract_hrv(energy_state, stress_level, sleep_quality)
        
        return {
            'fmri': {
                'pfc_activation': fmri.pfc_activation,
                'amygdala_activation': fmri.amygdala_activation,
                'hypothalamus_activation': fmri.hypothalamus_activation,
                'basal_ganglia_activation': fmri.basal_ganglia_activation,
                'default_mode_network': fmri.default_mode_network,
                'salience_network': fmri.salience_network,
                'executive_network': fmri.executive_network
            },
            'eeg': {
                'alpha_power': eeg.alpha_power,
                'beta_power': eeg.beta_power,
                'theta_power': eeg.theta_power,
                'delta_power': eeg.delta_power,
                'gamma_power': eeg.gamma_power,
                'theta_beta_ratio': eeg.theta_beta_ratio,
                'alpha_asymmetry': eeg.alpha_asymmetry
            },
            'hrv': {
                'rmssd': hrv.rmssd,
                'sdnn': hrv.sdnn,
                'lf_hf_ratio': hrv.lf_hf_ratio,
                'hf_power': hrv.hf_power,
                'lf_power': hrv.lf_power
            }
        }
