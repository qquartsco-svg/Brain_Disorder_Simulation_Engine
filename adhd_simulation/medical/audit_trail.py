"""
Audit Trail 시스템

의료 소프트웨어 규제 준수를 위한 실행 기록 시스템
모든 입력, 출력, 실행 정보를 추적 가능하게 기록
"""

import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
import uuid

logger = logging.getLogger(__name__)


class AuditTrail:
    """
    Audit Trail 관리 클래스
    
    모든 실행 기록을 저장하고 추적
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Audit Trail 초기화
        
        Args:
            output_dir: 기록 저장 디렉토리
        """
        self.output_dir = output_dir or Path.cwd() / 'audit_logs'
        self.output_dir.mkdir(exist_ok=True)
        
        self.current_session_id = str(uuid.uuid4())
        self.session_start_time = datetime.now().isoformat()
        
        self.entries: List[Dict[str, Any]] = []
        
        logger.info(f"Audit Trail 초기화: Session ID = {self.current_session_id}")
    
    def log_execution(self,
                     operation: str,
                     input_data: Dict[str, Any],
                     output_data: Optional[Dict[str, Any]] = None,
                     execution_time: Optional[float] = None,
                     errors: Optional[List[str]] = None,
                     warnings: Optional[List[str]] = None) -> str:
        """
        실행 기록 추가
        
        Args:
            operation: 수행된 작업 이름
            input_data: 입력 데이터
            output_data: 출력 데이터 (선택)
            execution_time: 실행 시간 (초)
            errors: 오류 목록 (선택)
            warnings: 경고 목록 (선택)
            
        Returns:
            entry_id: 기록 ID
        """
        entry_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # 입력 데이터 해시 (민감 정보 제외)
        input_hash = self._hash_data(input_data)
        
        # 출력 데이터 해시
        output_hash = None
        if output_data:
            output_hash = self._hash_data(output_data)
        
        entry = {
            'entry_id': entry_id,
            'session_id': self.current_session_id,
            'timestamp': timestamp,
            'operation': operation,
            'input_hash': input_hash,
            'output_hash': output_hash,
            'execution_time_seconds': execution_time,
            'error_count': len(errors) if errors else 0,
            'warning_count': len(warnings) if warnings else 0,
            'has_errors': bool(errors),
            'has_warnings': bool(warnings)
        }
        
        # 민감 정보 제외한 입력/출력 요약
        entry['input_summary'] = self._create_summary(input_data)
        if output_data:
            entry['output_summary'] = self._create_summary(output_data)
        
        self.entries.append(entry)
        
        # 즉시 파일에 저장 (데이터 손실 방지)
        self._save_entry(entry)
        
        logger.info(f"Audit Trail 기록: {operation} (ID: {entry_id})")
        
        return entry_id
    
    def log_input_validation(self,
                           input_data: Dict[str, Any],
                           is_valid: bool,
                           errors: List[str],
                           warnings: List[str]) -> str:
        """
        입력 검증 기록
        
        Args:
            input_data: 검증된 입력 데이터
            is_valid: 검증 통과 여부
            errors: 검증 오류 목록
            warnings: 검증 경고 목록
            
        Returns:
            entry_id: 기록 ID
        """
        return self.log_execution(
            operation='input_validation',
            input_data=input_data,
            errors=errors if not is_valid else None,
            warnings=warnings if warnings else None
        )
    
    def log_simulation_run(self,
                          simulation_type: str,
                          input_data: Dict[str, Any],
                          output_data: Dict[str, Any],
                          execution_time: float) -> str:
        """
        시뮬레이션 실행 기록
        
        Args:
            simulation_type: 시뮬레이션 타입 (attention, impulsivity, hyperactivity)
            input_data: 입력 데이터
            output_data: 출력 데이터
            execution_time: 실행 시간
            
        Returns:
            entry_id: 기록 ID
        """
        return self.log_execution(
            operation=f'simulation_{simulation_type}',
            input_data=input_data,
            output_data=output_data,
            execution_time=execution_time
        )
    
    def log_error(self,
                 operation: str,
                 input_data: Dict[str, Any],
                 error_message: str,
                 error_type: Optional[str] = None) -> str:
        """
        오류 기록
        
        Args:
            operation: 수행 중이었던 작업
            input_data: 입력 데이터
            error_message: 오류 메시지
            error_type: 오류 타입 (선택)
            
        Returns:
            entry_id: 기록 ID
        """
        entry_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        entry = {
            'entry_id': entry_id,
            'session_id': self.current_session_id,
            'timestamp': timestamp,
            'operation': operation,
            'error_type': error_type,
            'error_message': error_message,
            'input_hash': self._hash_data(input_data),
            'input_summary': self._create_summary(input_data),
            'is_error': True
        }
        
        self.entries.append(entry)
        self._save_entry(entry)
        
        logger.error(f"Audit Trail 오류 기록: {operation} - {error_message}")
        
        return entry_id
    
    def _hash_data(self, data: Dict[str, Any]) -> str:
        """
        데이터 해시 생성 (민감 정보 제외)
        
        Args:
            data: 해시할 데이터
            
        Returns:
            해시 문자열
        """
        # 민감 정보 제외한 복사본 생성
        safe_data = self._remove_sensitive_info(data.copy())
        
        # JSON 직렬화 후 해시
        json_str = json.dumps(safe_data, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    def _remove_sensitive_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        민감 정보 제거 (PHI 보호)
        
        Args:
            data: 원본 데이터
            
        Returns:
            민감 정보가 제거된 데이터
        """
        sensitive_keys = [
            'patient_id', 'patient_name', 'name', 'id',
            'email', 'phone', 'address', 'ssn', 'social_security_number'
        ]
        
        safe_data = {}
        for key, value in data.items():
            if any(sk in key.lower() for sk in sensitive_keys):
                safe_data[key] = '[REDACTED]'
            elif isinstance(value, dict):
                safe_data[key] = self._remove_sensitive_info(value)
            elif isinstance(value, list):
                safe_data[key] = [
                    self._remove_sensitive_info(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                safe_data[key] = value
        
        return safe_data
    
    def _create_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        데이터 요약 생성 (전체 데이터 대신 요약만 저장)
        
        Args:
            data: 원본 데이터
            
        Returns:
            요약 딕셔너리
        """
        summary = {}
        
        for key, value in data.items():
            if isinstance(value, (int, float)):
                summary[key] = value
            elif isinstance(value, str):
                summary[key] = value[:100] if len(value) > 100 else value
            elif isinstance(value, list):
                summary[key] = {
                    'type': 'list',
                    'length': len(value),
                    'first_item': self._create_summary(value[0]) if value and isinstance(value[0], dict) else None
                }
            elif isinstance(value, dict):
                summary[key] = self._create_summary(value)
            else:
                summary[key] = str(type(value).__name__)
        
        return summary
    
    def _save_entry(self, entry: Dict[str, Any]):
        """
        개별 기록 저장
        
        Args:
            entry: 기록 딕셔너리
        """
        # 세션별 파일에 저장
        session_file = self.output_dir / f"session_{self.current_session_id}.jsonl"
        
        with open(session_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, default=str) + '\n')
    
    def finalize_session(self) -> Dict[str, Any]:
        """
        세션 종료 및 최종 리포트 생성
        
        Returns:
            세션 리포트
        """
        session_end_time = datetime.now().isoformat()
        
        # 세션 요약
        session_report = {
            'session_id': self.current_session_id,
            'start_time': self.session_start_time,
            'end_time': session_end_time,
            'total_entries': len(self.entries),
            'error_count': sum(1 for e in self.entries if e.get('is_error', False)),
            'operations': list(set(e['operation'] for e in self.entries)),
            'entries': self.entries
        }
        
        # 세션 리포트 저장
        report_file = self.output_dir / f"session_{self.current_session_id}_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(session_report, f, indent=2, default=str)
        
        logger.info(f"Audit Trail 세션 종료: {self.current_session_id} ({len(self.entries)} entries)")
        
        return session_report
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        현재 세션 요약
        
        Returns:
            세션 요약 딕셔너리
        """
        return {
            'session_id': self.current_session_id,
            'start_time': self.session_start_time,
            'entry_count': len(self.entries),
            'error_count': sum(1 for e in self.entries if e.get('is_error', False)),
            'operations': list(set(e['operation'] for e in self.entries))
        }

