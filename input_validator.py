"""
입력 검증 모듈

의료 소프트웨어 기준에 따른 엄격한 입력 검증
ISO 14971 위험 완화를 위한 필수 컴포넌트
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
import logging

logger = logging.getLogger(__name__)


class InputValidator:
    """
    입력 데이터 검증 클래스
    
    의료 소프트웨어 기준에 따른 엄격한 검증 수행
    """
    
    def __init__(self):
        """검증기 초기화"""
        self.validation_errors = []
        self.validation_warnings = []
    
    def validate_simulation_input(self, data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        시뮬레이션 입력 데이터 검증
        
        Args:
            data: 입력 데이터 딕셔너리
            
        Returns:
            (is_valid, errors, warnings): 검증 결과
        """
        self.validation_errors = []
        self.validation_warnings = []
        
        # 1. 기본 구조 검증
        if not isinstance(data, dict):
            self.validation_errors.append("입력 데이터는 딕셔너리여야 합니다")
            return False, self.validation_errors, self.validation_warnings
        
        # 2. 필수 필드 검증
        required_fields = ['duration', 'task_importance']
        for field in required_fields:
            if field not in data:
                self.validation_errors.append(f"필수 필드 누락: {field}")
        
        # 3. 타입 검증
        if 'duration' in data:
            if not isinstance(data['duration'], (int, float)):
                self.validation_errors.append("duration은 숫자여야 합니다")
            elif np.isnan(data['duration']) or np.isinf(data['duration']):
                self.validation_errors.append("duration은 유효한 숫자여야 합니다")
            elif data['duration'] <= 0:
                self.validation_errors.append("duration은 0보다 커야 합니다")
            elif data['duration'] > 3600:  # 1시간 제한
                self.validation_warnings.append("duration이 1시간을 초과합니다 (3600초)")
        
        if 'task_importance' in data:
            if not isinstance(data['task_importance'], (int, float)):
                self.validation_errors.append("task_importance는 숫자여야 합니다")
            elif np.isnan(data['task_importance']) or np.isinf(data['task_importance']):
                self.validation_errors.append("task_importance는 유효한 숫자여야 합니다")
            elif not (0.0 <= data['task_importance'] <= 1.0):
                self.validation_errors.append("task_importance는 0.0과 1.0 사이여야 합니다")
        
        # 4. 선택적 필드 검증
        if 'distractions' in data:
            if not isinstance(data['distractions'], list):
                self.validation_errors.append("distractions는 리스트여야 합니다")
            else:
                for i, dist in enumerate(data['distractions']):
                    if not isinstance(dist, dict):
                        self.validation_errors.append(f"distractions[{i}]는 딕셔너리여야 합니다")
                    else:
                        if 'intensity' in dist:
                            if not isinstance(dist['intensity'], (int, float)):
                                self.validation_errors.append(f"distractions[{i}].intensity는 숫자여야 합니다")
                            elif np.isnan(dist['intensity']) or np.isinf(dist['intensity']):
                                self.validation_errors.append(f"distractions[{i}].intensity는 유효한 숫자여야 합니다")
                            elif not (0.0 <= dist['intensity'] <= 1.0):
                                self.validation_errors.append(f"distractions[{i}].intensity는 0.0과 1.0 사이여야 합니다")
        
        # 5. 이상치 감지
        if 'task_importance' in data and isinstance(data['task_importance'], (int, float)):
            if data['task_importance'] < 0.1:
                self.validation_warnings.append("task_importance가 매우 낮습니다 (< 0.1)")
            if data['task_importance'] > 0.95:
                self.validation_warnings.append("task_importance가 매우 높습니다 (> 0.95)")
        
        is_valid = len(self.validation_errors) == 0
        
        if not is_valid:
            logger.error(f"입력 검증 실패: {self.validation_errors}")
        if self.validation_warnings:
            logger.warning(f"입력 검증 경고: {self.validation_warnings}")
        
        return is_valid, self.validation_errors, self.validation_warnings
    
    def validate_impulsivity_input(self, data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        충동성 테스트 입력 검증
        
        Args:
            data: 충동성 테스트 입력 데이터
            
        Returns:
            (is_valid, errors, warnings): 검증 결과
        """
        self.validation_errors = []
        self.validation_warnings = []
        
        if not isinstance(data, dict):
            self.validation_errors.append("입력 데이터는 딕셔너리여야 합니다")
            return False, self.validation_errors, self.validation_warnings
        
        if 'scenarios' not in data:
            self.validation_errors.append("필수 필드 누락: scenarios")
            return False, self.validation_errors, self.validation_warnings
        
        if not isinstance(data['scenarios'], list):
            self.validation_errors.append("scenarios는 리스트여야 합니다")
            return False, self.validation_errors, self.validation_warnings
        
        if len(data['scenarios']) == 0:
            self.validation_errors.append("scenarios는 최소 1개 이상이어야 합니다")
            return False, self.validation_errors, self.validation_warnings
        
        # 각 시나리오 검증
        for i, scenario in enumerate(data['scenarios']):
            if not isinstance(scenario, dict):
                self.validation_errors.append(f"scenarios[{i}]는 딕셔너리여야 합니다")
                continue
            
            required = ['immediate_reward', 'delayed_reward', 'delay_time']
            for field in required:
                if field not in scenario:
                    self.validation_errors.append(f"scenarios[{i}].{field} 필수 필드 누락")
                elif not isinstance(scenario[field], (int, float)):
                    self.validation_errors.append(f"scenarios[{i}].{field}는 숫자여야 합니다")
                elif np.isnan(scenario[field]) or np.isinf(scenario[field]):
                    self.validation_errors.append(f"scenarios[{i}].{field}는 유효한 숫자여야 합니다")
            
            # 값 범위 검증
            if 'immediate_reward' in scenario and isinstance(scenario['immediate_reward'], (int, float)):
                if scenario['immediate_reward'] < 0:
                    self.validation_errors.append(f"scenarios[{i}].immediate_reward는 0 이상이어야 합니다")
            
            if 'delayed_reward' in scenario and isinstance(scenario['delayed_reward'], (int, float)):
                if scenario['delayed_reward'] < 0:
                    self.validation_errors.append(f"scenarios[{i}].delayed_reward는 0 이상이어야 합니다")
            
            if 'delay_time' in scenario and isinstance(scenario['delay_time'], (int, float)):
                if scenario['delay_time'] < 0:
                    self.validation_errors.append(f"scenarios[{i}].delay_time는 0 이상이어야 합니다")
                elif scenario['delay_time'] > 3600:  # 1시간 제한
                    self.validation_warnings.append(f"scenarios[{i}].delay_time가 1시간을 초과합니다")
        
        is_valid = len(self.validation_errors) == 0
        
        if not is_valid:
            logger.error(f"충동성 입력 검증 실패: {self.validation_errors}")
        if self.validation_warnings:
            logger.warning(f"충동성 입력 검증 경고: {self.validation_warnings}")
        
        return is_valid, self.validation_errors, self.validation_warnings
    
    def validate_hyperactivity_input(self, data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        과잉행동 테스트 입력 검증
        
        Args:
            data: 과잉행동 테스트 입력 데이터
            
        Returns:
            (is_valid, errors, warnings): 검증 결과
        """
        self.validation_errors = []
        self.validation_warnings = []
        
        if not isinstance(data, dict):
            self.validation_errors.append("입력 데이터는 딕셔너리여야 합니다")
            return False, self.validation_errors, self.validation_warnings
        
        if 'duration' in data:
            if not isinstance(data['duration'], (int, float)):
                self.validation_errors.append("duration은 숫자여야 합니다")
            elif np.isnan(data['duration']) or np.isinf(data['duration']):
                self.validation_errors.append("duration은 유효한 숫자여야 합니다")
            elif data['duration'] <= 0:
                self.validation_errors.append("duration은 0보다 커야 합니다")
            elif data['duration'] > 3600:
                self.validation_warnings.append("duration이 1시간을 초과합니다")
        
        if 'task_demand' in data:
            if not isinstance(data['task_demand'], (int, float)):
                self.validation_errors.append("task_demand는 숫자여야 합니다")
            elif np.isnan(data['task_demand']) or np.isinf(data['task_demand']):
                self.validation_errors.append("task_demand는 유효한 숫자여야 합니다")
            elif not (0.0 <= data['task_demand'] <= 1.0):
                self.validation_errors.append("task_demand는 0.0과 1.0 사이여야 합니다")
        
        is_valid = len(self.validation_errors) == 0
        
        if not is_valid:
            logger.error(f"과잉행동 입력 검증 실패: {self.validation_errors}")
        if self.validation_warnings:
            logger.warning(f"과잉행동 입력 검증 경고: {self.validation_warnings}")
        
        return is_valid, self.validation_errors, self.validation_warnings
    
    def sanitize_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        입력 데이터 정제 (NaN, Inf 제거)
        
        Args:
            data: 원본 입력 데이터
            
        Returns:
            정제된 데이터
        """
        sanitized = {}
        
        for key, value in data.items():
            if isinstance(value, (int, float)):
                if np.isnan(value) or np.isinf(value):
                    # NaN/Inf를 안전한 기본값으로 대체
                    if key in ['duration', 'delay_time']:
                        sanitized[key] = 10.0  # 기본 10초
                    elif key in ['task_importance', 'task_demand']:
                        sanitized[key] = 0.5  # 기본 0.5
                    else:
                        sanitized[key] = 0.0
                else:
                    sanitized[key] = value
            elif isinstance(value, list):
                sanitized[key] = [self._sanitize_item(item) for item in value]
            elif isinstance(value, dict):
                sanitized[key] = self.sanitize_input(value)
            else:
                sanitized[key] = value
        
        return sanitized
    
    def _sanitize_item(self, item: Any) -> Any:
        """단일 항목 정제"""
        if isinstance(item, (int, float)):
            if np.isnan(item) or np.isinf(item):
                return 0.0
            return item
        elif isinstance(item, dict):
            return self.sanitize_input(item)
        else:
            return item
    
    def get_validation_report(self) -> Dict[str, Any]:
        """
        검증 결과 리포트
        
        Returns:
            검증 리포트 딕셔너리
        """
        return {
            'errors': self.validation_errors.copy(),
            'warnings': self.validation_warnings.copy(),
            'error_count': len(self.validation_errors),
            'warning_count': len(self.validation_warnings),
            'is_valid': len(self.validation_errors) == 0
        }

