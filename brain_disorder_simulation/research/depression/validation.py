"""
검증 도구 모듈

의료 연구를 위한 검증 기능
- 생물학적 타당성 검증
- 임상적 관련성 검증
- 연구 재현성 검증

연구 근거:
- O'Reilly et al. (2012) - Computational models of cognitive control
- Poldrack et al. (2011) - Decoding the large-scale structure of brain function
- Ioannidis (2005) - Why most published research findings are false

참고 문헌:
- O'Reilly, R. C., et al. (2012). Computational models of cognitive control. Current Opinion in Neurobiology
- Poldrack, R. A., et al. (2011). Decoding the large-scale structure of brain function. Nature Reviews Neuroscience
- Ioannidis, J. P. (2005). Why most published research findings are false. PLoS Medicine

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class ValidationResult:
    """검증 결과"""
    category: str
    passed: bool
    score: float  # 0.0 ~ 1.0
    details: Dict[str, Any]
    recommendations: List[str]


@dataclass
class BiologicalValidityResult:
    """생물학적 타당성 검증 결과"""
    brain_region_mapping: ValidationResult
    time_scale: ValidationResult
    energy_metabolism: ValidationResult
    neurotransmitter_systems: ValidationResult
    overall_score: float


@dataclass
class ClinicalRelevanceResult:
    """임상적 관련성 검증 결과"""
    dsm5_mapping: ValidationResult
    clinical_scales: ValidationResult
    symptom_patterns: ValidationResult
    individual_differences: ValidationResult
    overall_score: float


@dataclass
class ReproducibilityResult:
    """연구 재현성 검증 결과"""
    seed_management: ValidationResult
    experiment_metadata: ValidationResult
    parameter_documentation: ValidationResult
    result_traceability: ValidationResult
    overall_score: float


class BiologicalValidityValidator:
    """
    생물학적 타당성 검증기
    
    연구 근거:
    - 뇌 영역 매핑 정확성
    - 시간 스케일 일치
    - 에너지 대사 모델 정확성
    - 신경전달물질 시스템 정확성
    """
    
    def __init__(self):
        """생물학적 타당성 검증기 초기화"""
        pass
    
    def validate_brain_region_mapping(self, simulation_results: Dict[str, Any]) -> ValidationResult:
        """
        뇌 영역 매핑 정확성 검증
        
        연구 근거:
        - PFC, Amygdala, Hypothalamus, Basal Ganglia 등
        - 실제 뇌 영역 기능과 일치 여부 확인
        
        Args:
            simulation_results: 시뮬레이션 결과
        
        Returns:
            검증 결과
        """
        required_regions = ['pfc_activity', 'amygdala_activity', 
                           'hypothalamus_activity', 'basal_ganglia_activity']
        
        found_regions = []
        missing_regions = []
        
        for region in required_regions:
            if region in simulation_results or self._has_nested_key(simulation_results, region):
                found_regions.append(region)
            else:
                missing_regions.append(region)
        
        score = len(found_regions) / len(required_regions)
        passed = score >= 0.75
        
        recommendations = []
        if missing_regions:
            recommendations.append(f"누락된 뇌 영역: {', '.join(missing_regions)}")
        
        return ValidationResult(
            category="뇌 영역 매핑",
            passed=passed,
            score=score,
            details={
                'found_regions': found_regions,
                'missing_regions': missing_regions,
                'total_regions': len(required_regions)
            },
            recommendations=recommendations
        )
    
    def validate_time_scale(self, simulation_results: Dict[str, Any]) -> ValidationResult:
        """
        시간 스케일 일치 검증
        
        연구 근거:
        - 시뮬레이션 시간 스케일이 생물학적 시간과 일치하는지 확인
        - 예: 반응 시간, 학습 시간, 회복 시간 등
        
        Args:
            simulation_results: 시뮬레이션 결과
        
        Returns:
            검증 결과
        """
        # 시간 관련 파라미터 확인
        time_params = ['time_scale', 'dt', 'simulation_duration', 'recovery_time']
        
        found_params = []
        for param in time_params:
            if param in simulation_results or self._has_nested_key(simulation_results, param):
                found_params.append(param)
        
        score = len(found_params) / len(time_params) if time_params else 0.5
        passed = score >= 0.5
        
        recommendations = []
        if not found_params:
            recommendations.append("시간 스케일 파라미터가 명시되지 않았습니다")
        
        return ValidationResult(
            category="시간 스케일",
            passed=passed,
            score=score,
            details={
                'found_params': found_params,
                'total_params': len(time_params)
            },
            recommendations=recommendations
        )
    
    def validate_energy_metabolism(self, simulation_results: Dict[str, Any]) -> ValidationResult:
        """
        에너지 대사 모델 정확성 검증
        
        연구 근거:
        - 에너지 소비와 회복 메커니즘이 생물학적으로 타당한지 확인
        - ATP, 포도당 대사 등
        
        Args:
            simulation_results: 시뮬레이션 결과
        
        Returns:
            검증 결과
        """
        energy_keys = ['energy', 'current_energy', 'energy_level', 'energy_consumption', 
                      'energy_recovery', 'recovery_rate']
        
        found_keys = []
        for key in energy_keys:
            if key in simulation_results or self._has_nested_key(simulation_results, key):
                found_keys.append(key)
        
        # 에너지 값의 범위 검증 (0-100 또는 0-1)
        energy_values = []
        for key in found_keys:
            value = self._get_nested_value(simulation_results, key)
            if value is not None:
                energy_values.append(value)
        
        score = len(found_keys) / len(energy_keys) if energy_keys else 0.5
        
        # 에너지 값이 합리적인 범위인지 확인
        if energy_values:
            valid_range = all(0 <= v <= 100 or 0 <= v <= 1 for v in energy_values)
            if not valid_range:
                score *= 0.8  # 범위 벗어나면 점수 감소
        
        passed = score >= 0.6
        
        recommendations = []
        if not found_keys:
            recommendations.append("에너지 관련 파라미터가 명시되지 않았습니다")
        if energy_values and not all(0 <= v <= 100 or 0 <= v <= 1 for v in energy_values):
            recommendations.append("에너지 값이 합리적인 범위를 벗어났습니다 (0-100 또는 0-1)")
        
        return ValidationResult(
            category="에너지 대사",
            passed=passed,
            score=score,
            details={
                'found_keys': found_keys,
                'energy_values': energy_values[:5] if energy_values else [],  # 처음 5개만
                'valid_range': valid_range if energy_values else None
            },
            recommendations=recommendations
        )
    
    def validate_neurotransmitter_systems(self, simulation_results: Dict[str, Any]) -> ValidationResult:
        """
        신경전달물질 시스템 정확성 검증
        
        연구 근거:
        - 도파민, 세로토닌, 노르에피네프린 시스템
        - 실제 신경전달물질 동작과 일치 여부 확인
        
        Args:
            simulation_results: 시뮬레이션 결과
        
        Returns:
            검증 결과
        """
        neurotransmitter_keys = ['dopamine', 'serotonin', 'norepinephrine',
                                'tonic_dopamine', 'phasic_dopamine', 'serotonin_level']
        
        found_keys = []
        for key in neurotransmitter_keys:
            if key in simulation_results or self._has_nested_key(simulation_results, key):
                found_keys.append(key)
        
        score = len(found_keys) / len(neurotransmitter_keys) if neurotransmitter_keys else 0.5
        passed = score >= 0.5
        
        recommendations = []
        if not found_keys:
            recommendations.append("신경전달물질 시스템이 구현되지 않았습니다")
        elif len(found_keys) < len(neurotransmitter_keys) * 0.5:
            recommendations.append("신경전달물질 시스템이 부분적으로만 구현되었습니다")
        
        return ValidationResult(
            category="신경전달물질 시스템",
            passed=passed,
            score=score,
            details={
                'found_keys': found_keys,
                'total_keys': len(neurotransmitter_keys)
            },
            recommendations=recommendations
        )
    
    def validate_all(self, simulation_results: Dict[str, Any]) -> BiologicalValidityResult:
        """
        전체 생물학적 타당성 검증
        
        Args:
            simulation_results: 시뮬레이션 결과
        
        Returns:
            생물학적 타당성 검증 결과
        """
        brain_region = self.validate_brain_region_mapping(simulation_results)
        time_scale = self.validate_time_scale(simulation_results)
        energy = self.validate_energy_metabolism(simulation_results)
        neurotransmitters = self.validate_neurotransmitter_systems(simulation_results)
        
        overall_score = np.mean([
            brain_region.score,
            time_scale.score,
            energy.score,
            neurotransmitters.score
        ])
        
        return BiologicalValidityResult(
            brain_region_mapping=brain_region,
            time_scale=time_scale,
            energy_metabolism=energy,
            neurotransmitter_systems=neurotransmitters,
            overall_score=overall_score
        )
    
    def _has_nested_key(self, data: Dict[str, Any], key: str) -> bool:
        """중첩된 딕셔너리에서 키 존재 확인"""
        keys = key.split('.')
        value = data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return False
        
        return True
    
    def _get_nested_value(self, data: Dict[str, Any], key: str) -> Optional[Any]:
        """중첩된 딕셔너리에서 값 추출"""
        keys = key.split('.')
        value = data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        
        return value


class ClinicalRelevanceValidator:
    """
    임상적 관련성 검증기
    
    연구 근거:
    - DSM-5/ICD-11 기준 매핑
    - 임상 스케일 통합
    - 증상 패턴 재현
    - 개인차 모델링
    """
    
    def __init__(self):
        """임상적 관련성 검증기 초기화"""
        pass
    
    def validate_dsm5_mapping(self, simulation_results: Dict[str, Any]) -> ValidationResult:
        """
        DSM-5 기준 매핑 검증
        
        연구 근거:
        - DSM-5 우울증 진단 기준과 일치 여부 확인
        
        Args:
            simulation_results: 시뮬레이션 결과
        
        Returns:
            검증 결과
        """
        # DSM-5 주요 증상 확인
        dsm5_symptoms = ['depressed_mood', 'loss_of_interest', 'weight_change',
                        'sleep_disturbance', 'fatigue', 'worthlessness', 'concentration']
        
        found_symptoms = []
        for symptom in dsm5_symptoms:
            if symptom in simulation_results or self._has_nested_key(simulation_results, symptom):
                found_symptoms.append(symptom)
        
        score = len(found_symptoms) / len(dsm5_symptoms) if dsm5_symptoms else 0.5
        passed = score >= 0.6
        
        recommendations = []
        if not found_symptoms:
            recommendations.append("DSM-5 증상이 매핑되지 않았습니다")
        elif len(found_symptoms) < len(dsm5_symptoms) * 0.6:
            recommendations.append("DSM-5 증상이 부분적으로만 매핑되었습니다")
        
        return ValidationResult(
            category="DSM-5 매핑",
            passed=passed,
            score=score,
            details={
                'found_symptoms': found_symptoms,
                'total_symptoms': len(dsm5_symptoms)
            },
            recommendations=recommendations
        )
    
    def validate_clinical_scales(self, simulation_results: Dict[str, Any]) -> ValidationResult:
        """
        임상 스케일 통합 검증
        
        연구 근거:
        - HAM-D, BDI, PHQ-9 등 임상 스케일과의 일치 여부 확인
        
        Args:
            simulation_results: 시뮬레이션 결과
        
        Returns:
            검증 결과
        """
        clinical_scales = ['hamd', 'bdi', 'phq9', 'hamd_score', 'bdi_score', 'phq9_score']
        
        found_scales = []
        for scale in clinical_scales:
            if scale in simulation_results or self._has_nested_key(simulation_results, scale):
                found_scales.append(scale)
        
        score = len(found_scales) / len(clinical_scales) if clinical_scales else 0.5
        passed = score >= 0.5
        
        recommendations = []
        if not found_scales:
            recommendations.append("임상 스케일이 통합되지 않았습니다")
        elif len(found_scales) < len(clinical_scales) * 0.5:
            recommendations.append("임상 스케일이 부분적으로만 통합되었습니다")
        
        return ValidationResult(
            category="임상 스케일",
            passed=passed,
            score=score,
            details={
                'found_scales': found_scales,
                'total_scales': len(clinical_scales)
            },
            recommendations=recommendations
        )
    
    def validate_symptom_patterns(self, simulation_results: Dict[str, Any]) -> ValidationResult:
        """
        증상 패턴 재현 검증
        
        연구 근거:
        - 실제 우울증 증상 패턴과 일치 여부 확인
        
        Args:
            simulation_results: 시뮬레이션 결과
        
        Returns:
            검증 결과
        """
        symptom_patterns = ['negative_bias', 'rumination', 'energy_depletion',
                           'motivation_loss', 'cognitive_impairment']
        
        found_patterns = []
        for pattern in symptom_patterns:
            if pattern in simulation_results or self._has_nested_key(simulation_results, pattern):
                found_patterns.append(pattern)
        
        score = len(found_patterns) / len(symptom_patterns) if symptom_patterns else 0.5
        passed = score >= 0.7
        
        recommendations = []
        if not found_patterns:
            recommendations.append("증상 패턴이 재현되지 않았습니다")
        elif len(found_patterns) < len(symptom_patterns) * 0.7:
            recommendations.append("증상 패턴이 부분적으로만 재현되었습니다")
        
        return ValidationResult(
            category="증상 패턴",
            passed=passed,
            score=score,
            details={
                'found_patterns': found_patterns,
                'total_patterns': len(symptom_patterns)
            },
            recommendations=recommendations
        )
    
    def validate_individual_differences(self, simulation_results: Dict[str, Any]) -> ValidationResult:
        """
        개인차 모델링 검증
        
        연구 근거:
        - 개인차를 반영하는 파라미터 존재 여부 확인
        
        Args:
            simulation_results: 시뮬레이션 결과
        
        Returns:
            검증 결과
        """
        individual_params = ['individual_variability', 'personality_traits',
                           'baseline_differences', 'response_variability']
        
        found_params = []
        for param in individual_params:
            if param in simulation_results or self._has_nested_key(simulation_results, param):
                found_params.append(param)
        
        score = len(found_params) / len(individual_params) if individual_params else 0.3
        passed = score >= 0.3  # 개인차는 선택적이므로 낮은 기준
        
        recommendations = []
        if not found_params:
            recommendations.append("개인차 모델링이 구현되지 않았습니다 (선택사항)")
        
        return ValidationResult(
            category="개인차 모델링",
            passed=passed,
            score=score,
            details={
                'found_params': found_params,
                'total_params': len(individual_params)
            },
            recommendations=recommendations
        )
    
    def validate_all(self, simulation_results: Dict[str, Any]) -> ClinicalRelevanceResult:
        """
        전체 임상적 관련성 검증
        
        Args:
            simulation_results: 시뮬레이션 결과
        
        Returns:
            임상적 관련성 검증 결과
        """
        dsm5 = self.validate_dsm5_mapping(simulation_results)
        clinical_scales = self.validate_clinical_scales(simulation_results)
        symptom_patterns = self.validate_symptom_patterns(simulation_results)
        individual_differences = self.validate_individual_differences(simulation_results)
        
        overall_score = np.mean([
            dsm5.score,
            clinical_scales.score,
            symptom_patterns.score,
            individual_differences.score
        ])
        
        return ClinicalRelevanceResult(
            dsm5_mapping=dsm5,
            clinical_scales=clinical_scales,
            symptom_patterns=symptom_patterns,
            individual_differences=individual_differences,
            overall_score=overall_score
        )
    
    def _has_nested_key(self, data: Dict[str, Any], key: str) -> bool:
        """중첩된 딕셔너리에서 키 존재 확인"""
        keys = key.split('.')
        value = data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return False
        
        return True


class ReproducibilityValidator:
    """
    연구 재현성 검증기
    
    연구 근거:
    - Seed 관리 시스템
    - 실험 메타데이터
    - 파라미터 문서화
    - 결과 추적성
    """
    
    def __init__(self):
        """연구 재현성 검증기 초기화"""
        pass
    
    def validate_seed_management(self, experiment_config: Dict[str, Any]) -> ValidationResult:
        """
        Seed 관리 시스템 검증
        
        연구 근거:
        - 재현 가능한 실험을 위한 Seed 관리
        
        Args:
            experiment_config: 실험 설정
        
        Returns:
            검증 결과
        """
        seed_keys = ['seed', 'random_seed', 'numpy_seed', 'rng_seed']
        
        found_seeds = []
        for key in seed_keys:
            if key in experiment_config:
                found_seeds.append(key)
        
        score = 1.0 if found_seeds else 0.0
        passed = score >= 0.5
        
        recommendations = []
        if not found_seeds:
            recommendations.append("Seed가 명시되지 않았습니다. 재현성을 위해 Seed를 설정해야 합니다")
        
        return ValidationResult(
            category="Seed 관리",
            passed=passed,
            score=score,
            details={
                'found_seeds': found_seeds,
                'seed_value': experiment_config.get('seed') if found_seeds else None
            },
            recommendations=recommendations
        )
    
    def validate_experiment_metadata(self, experiment_config: Dict[str, Any]) -> ValidationResult:
        """
        실험 메타데이터 검증
        
        연구 근거:
        - 실험 재현을 위한 메타데이터 존재 여부
        
        Args:
            experiment_config: 실험 설정
        
        Returns:
            검증 결과
        """
        metadata_keys = ['experiment_id', 'date', 'version', 'author', 'description']
        
        found_metadata = []
        for key in metadata_keys:
            if key in experiment_config:
                found_metadata.append(key)
        
        score = len(found_metadata) / len(metadata_keys) if metadata_keys else 0.5
        passed = score >= 0.6
        
        recommendations = []
        if not found_metadata:
            recommendations.append("실험 메타데이터가 없습니다")
        elif len(found_metadata) < len(metadata_keys) * 0.6:
            recommendations.append("실험 메타데이터가 부분적으로만 있습니다")
        
        return ValidationResult(
            category="실험 메타데이터",
            passed=passed,
            score=score,
            details={
                'found_metadata': found_metadata,
                'total_metadata': len(metadata_keys)
            },
            recommendations=recommendations
        )
    
    def validate_parameter_documentation(self, experiment_config: Dict[str, Any]) -> ValidationResult:
        """
        파라미터 문서화 검증
        
        연구 근거:
        - 모든 파라미터가 문서화되어 있는지 확인
        
        Args:
            experiment_config: 실험 설정
        
        Returns:
            검증 결과
        """
        # 필수 파라미터 확인
        essential_params = ['n_steps', 'dt', 'initial_conditions', 'parameters']
        
        found_params = []
        for param in essential_params:
            if param in experiment_config:
                found_params.append(param)
        
        score = len(found_params) / len(essential_params) if essential_params else 0.5
        passed = score >= 0.5
        
        recommendations = []
        if not found_params:
            recommendations.append("필수 파라미터가 문서화되지 않았습니다")
        elif len(found_params) < len(essential_params) * 0.5:
            recommendations.append("필수 파라미터가 부분적으로만 문서화되었습니다")
        
        return ValidationResult(
            category="파라미터 문서화",
            passed=passed,
            score=score,
            details={
                'found_params': found_params,
                'total_params': len(essential_params)
            },
            recommendations=recommendations
        )
    
    def validate_result_traceability(self, results: Dict[str, Any]) -> ValidationResult:
        """
        결과 추적성 검증
        
        연구 근거:
        - 결과가 실험 설정과 연결되어 있는지 확인
        
        Args:
            results: 실험 결과
        
        Returns:
            검증 결과
        """
        traceability_keys = ['experiment_id', 'config_hash', 'timestamp', 'version']
        
        found_keys = []
        for key in traceability_keys:
            if key in results or self._has_nested_key(results, key):
                found_keys.append(key)
        
        score = len(found_keys) / len(traceability_keys) if traceability_keys else 0.5
        passed = score >= 0.5
        
        recommendations = []
        if not found_keys:
            recommendations.append("결과 추적 정보가 없습니다")
        elif len(found_keys) < len(traceability_keys) * 0.5:
            recommendations.append("결과 추적 정보가 부분적으로만 있습니다")
        
        return ValidationResult(
            category="결과 추적성",
            passed=passed,
            score=score,
            details={
                'found_keys': found_keys,
                'total_keys': len(traceability_keys)
            },
            recommendations=recommendations
        )
    
    def validate_all(self, 
                    experiment_config: Dict[str, Any],
                    results: Dict[str, Any]) -> ReproducibilityResult:
        """
        전체 연구 재현성 검증
        
        Args:
            experiment_config: 실험 설정
            results: 실험 결과
        
        Returns:
            연구 재현성 검증 결과
        """
        seed = self.validate_seed_management(experiment_config)
        metadata = self.validate_experiment_metadata(experiment_config)
        parameters = self.validate_parameter_documentation(experiment_config)
        traceability = self.validate_result_traceability(results)
        
        overall_score = np.mean([
            seed.score,
            metadata.score,
            parameters.score,
            traceability.score
        ])
        
        return ReproducibilityResult(
            seed_management=seed,
            experiment_metadata=metadata,
            parameter_documentation=parameters,
            result_traceability=traceability,
            overall_score=overall_score
        )
    
    def _has_nested_key(self, data: Dict[str, Any], key: str) -> bool:
        """중첩된 딕셔너리에서 키 존재 확인"""
        keys = key.split('.')
        value = data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return False
        
        return True


class ComprehensiveValidator:
    """
    통합 검증기
    
    모든 검증을 통합하여 실행
    """
    
    def __init__(self):
        """통합 검증기 초기화"""
        self.biological_validator = BiologicalValidityValidator()
        self.clinical_validator = ClinicalRelevanceValidator()
        self.reproducibility_validator = ReproducibilityValidator()
    
    def validate_all(self,
                    simulation_results: Dict[str, Any],
                    experiment_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        전체 검증 실행
        
        Args:
            simulation_results: 시뮬레이션 결과
            experiment_config: 실험 설정
        
        Returns:
            전체 검증 결과
        """
        biological = self.biological_validator.validate_all(simulation_results)
        clinical = self.clinical_validator.validate_all(simulation_results)
        reproducibility = self.reproducibility_validator.validate_all(
            experiment_config, simulation_results
        )
        
        overall_score = np.mean([
            biological.overall_score,
            clinical.overall_score,
            reproducibility.overall_score
        ])
        
        return {
            'biological_validity': biological,
            'clinical_relevance': clinical,
            'reproducibility': reproducibility,
            'overall_score': overall_score,
            'overall_passed': overall_score >= 0.7
        }
    
    def generate_validation_report(self, validation_results: Dict[str, Any]) -> str:
        """
        검증 리포트 생성
        
        Args:
            validation_results: 검증 결과
        
        Returns:
            리포트 문자열
        """
        report = f"""
{'=' * 70}
종합 검증 리포트
{'=' * 70}

전체 점수: {validation_results['overall_score']:.2%}
전체 통과: {'✅ 통과' if validation_results['overall_passed'] else '❌ 미통과'}

{'=' * 70}
1. 생물학적 타당성
{'=' * 70}
점수: {validation_results['biological_validity'].overall_score:.2%}

- 뇌 영역 매핑: {'✅' if validation_results['biological_validity'].brain_region_mapping.passed else '❌'} 
  ({validation_results['biological_validity'].brain_region_mapping.score:.2%})
- 시간 스케일: {'✅' if validation_results['biological_validity'].time_scale.passed else '❌'} 
  ({validation_results['biological_validity'].time_scale.score:.2%})
- 에너지 대사: {'✅' if validation_results['biological_validity'].energy_metabolism.passed else '❌'} 
  ({validation_results['biological_validity'].energy_metabolism.score:.2%})
- 신경전달물질 시스템: {'✅' if validation_results['biological_validity'].neurotransmitter_systems.passed else '❌'} 
  ({validation_results['biological_validity'].neurotransmitter_systems.score:.2%})

{'=' * 70}
2. 임상적 관련성
{'=' * 70}
점수: {validation_results['clinical_relevance'].overall_score:.2%}

- DSM-5 매핑: {'✅' if validation_results['clinical_relevance'].dsm5_mapping.passed else '❌'} 
  ({validation_results['clinical_relevance'].dsm5_mapping.score:.2%})
- 임상 스케일: {'✅' if validation_results['clinical_relevance'].clinical_scales.passed else '❌'} 
  ({validation_results['clinical_relevance'].clinical_scales.score:.2%})
- 증상 패턴: {'✅' if validation_results['clinical_relevance'].symptom_patterns.passed else '❌'} 
  ({validation_results['clinical_relevance'].symptom_patterns.score:.2%})
- 개인차 모델링: {'✅' if validation_results['clinical_relevance'].individual_differences.passed else '❌'} 
  ({validation_results['clinical_relevance'].individual_differences.score:.2%})

{'=' * 70}
3. 연구 재현성
{'=' * 70}
점수: {validation_results['reproducibility'].overall_score:.2%}

- Seed 관리: {'✅' if validation_results['reproducibility'].seed_management.passed else '❌'} 
  ({validation_results['reproducibility'].seed_management.score:.2%})
- 실험 메타데이터: {'✅' if validation_results['reproducibility'].experiment_metadata.passed else '❌'} 
  ({validation_results['reproducibility'].experiment_metadata.score:.2%})
- 파라미터 문서화: {'✅' if validation_results['reproducibility'].parameter_documentation.passed else '❌'} 
  ({validation_results['reproducibility'].parameter_documentation.score:.2%})
- 결과 추적성: {'✅' if validation_results['reproducibility'].result_traceability.passed else '❌'} 
  ({validation_results['reproducibility'].result_traceability.score:.2%})

{'=' * 70}
"""
        return report

