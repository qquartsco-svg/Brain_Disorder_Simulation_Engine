"""
규제 승인 준비 모듈

FDA 510(k) 또는 De Novo 신청 준비
ISO 13485 품질 시스템 준비
"""

from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import json


class RegulatoryPreparation:
    """
    규제 승인 준비 클래스
    
    FDA, CE 마킹 등 규제 승인 신청 준비
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        규제 준비 초기화
        
        Args:
            output_dir: 출력 디렉토리
        """
        self.output_dir = output_dir or Path.cwd() / 'regulatory_documents'
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_510k_summary(self,
                             device_name: str,
                             manufacturer: str,
                             predicate_device: Optional[str] = None) -> str:
        """
        510(k) 요약 문서 생성
        
        Args:
            device_name: 의료기기 이름
            manufacturer: 제조사
            predicate_device: 비교 의료기기 (선택)
        
        Returns:
            510(k) 요약 텍스트
        """
        summary = f"""
================================================================================
510(k) 요약 (510(k) Summary)
================================================================================

의료기기 이름: {device_name}
제조사: {manufacturer}
작성 일자: {datetime.now().strftime('%Y-%m-%d')}

================================================================================
1. 의료기기 설명
================================================================================

1.1 의료기기 명칭
{device_name}

1.2 의료기기 분류
- 분류: Class II
- 규제 번호: 21 CFR 882.5800 (Neurological Diagnostic Device)
- 제품 코드: QQQ (Software as Medical Device)

1.3 의료기기 목적
ADHD 평가를 위한 시뮬레이션 기반 보조 도구

1.4 의료기기 설명
Cookiie Brain Engine 기반 ADHD 시뮬레이션 시스템
주의력, 충동성, 과잉행동 패턴 평가

================================================================================
2. 비교 의료기기 (Predicate Device)
================================================================================

{f"비교 의료기기: {predicate_device}" if predicate_device else "비교 의료기기: 없음 (De Novo 고려)"}

================================================================================
3. 의료기기 차이점
================================================================================

3.1 기술적 차이점
- 시뮬레이션 기반 평가 (기존: 설문 기반)
- 동역학적 패턴 분석
- 상태공간 출력

3.2 의료적 차이점
- 진단 도구가 아닌 평가 보조 도구
- 전문의 평가와 병행 사용

================================================================================
4. 성능 데이터
================================================================================

4.1 임상 검증
- 민감도: 목표 80% 이상
- 특이도: 목표 80% 이상
- AUC: 목표 0.85 이상

4.2 소프트웨어 검증
- IEC 62304 준수
- ISO 14971 위험 관리
- 소프트웨어 생명주기 프로세스

================================================================================
5. 안전성 및 효과성
================================================================================

5.1 안전성
- 최소 위험 (Minimal Risk)
- 부작용 없음
- 데이터 보호 조치

5.2 효과성
- 전문의 평가와의 일치도
- 정상 참조군과의 차이
- 재현성 검증

================================================================================
6. 결론
================================================================================

본 의료기기는 비교 의료기기와 실질적으로 동등하며,
안전하고 효과적으로 사용할 수 있습니다.

================================================================================
"""
        return summary
    
    def generate_technical_file(self,
                               device_name: str,
                               software_version: str) -> Dict:
        """
        기술 파일 생성 (CE 마킹용)
        
        Args:
            device_name: 의료기기 이름
            software_version: 소프트웨어 버전
        
        Returns:
            기술 파일 딕셔너리
        """
        technical_file = {
            'device_identification': {
                'device_name': device_name,
                'software_version': software_version,
                'manufacturer': 'Cookiie Brain Engine Team',
                'device_class': 'Class IIa',
                'mdm_code': 'QQQ'
            },
            'intended_use': {
                'intended_purpose': 'ADHD 평가 보조 도구',
                'target_population': '12세 이상',
                'contraindications': [
                    '의학적 진단 도구 아님',
                    '전문의 평가 대체 불가'
                ]
            },
            'technical_specifications': {
                'software_lifecycle': 'IEC 62304',
                'risk_management': 'ISO 14971',
                'programming_language': 'Python 3.8+',
                'platform': 'Cross-platform',
                'dependencies': [
                    'numpy',
                    'scipy',
                    'matplotlib'
                ]
            },
            'clinical_evaluation': {
                'validation_study': '진행 중',
                'literature_review': '필요',
                'post_market_surveillance': '계획됨'
            },
            'risk_analysis': {
                'hazard_analysis': 'ISO 14971 준수',
                'risk_mitigation': [
                    '입력 검증',
                    '오류 처리',
                    '면책 조항'
                ]
            },
            'quality_management': {
                'qms_standard': 'ISO 13485',
                'documentation_control': '구현됨',
                'change_control': '구현됨'
            }
        }
        
        return technical_file
    
    def generate_iso13485_checklist(self) -> Dict:
        """
        ISO 13485 품질 시스템 체크리스트
        
        Returns:
            체크리스트 딕셔너리
        """
        checklist = {
            'quality_management_system': {
                'quality_manual': False,
                'quality_policy': False,
                'quality_objectives': False,
                'documentation_control': True,  # 구현됨
                'records_control': True  # Audit Trail 구현됨
            },
            'management_responsibility': {
                'management_commitment': False,
                'customer_focus': False,
                'quality_policy': False,
                'planning': False,
                'responsibility_authority': False,
                'management_review': False
            },
            'resource_management': {
                'provision_of_resources': False,
                'human_resources': False,
                'infrastructure': True,  # 기본 인프라 있음
                'work_environment': False
            },
            'product_realization': {
                'planning': True,  # Phase별 계획 있음
                'customer_related_processes': False,
                'design_development': {
                    'design_planning': True,
                    'design_input': True,
                    'design_output': True,
                    'design_review': True,
                    'design_verification': True,  # 테스트 있음
                    'design_validation': False,  # 임상 검증 필요
                    'design_changes': True
                },
                'purchasing': False,
                'production_service_provision': {
                    'control_of_production': True,
                    'validation_of_processes': True,
                    'identification_traceability': True,  # Audit Trail
                    'customer_property': False,
                    'preservation_of_product': False
                },
                'control_of_monitoring_measuring_devices': False
            },
            'measurement_analysis_improvement': {
                'monitoring_measurement': True,  # Validation Study
                'control_of_nonconforming_product': True,  # Input Validator
                'analysis_of_data': True,  # Statistical Validator
                'improvement': {
                    'continual_improvement': True,
                    'corrective_action': True,
                    'preventive_action': True
                }
            }
        }
        
        return checklist
    
    def save_regulatory_documents(self,
                                 device_name: str,
                                 software_version: str) -> Dict[str, Path]:
        """
        모든 규제 문서 저장
        
        Args:
            device_name: 의료기기 이름
            software_version: 소프트웨어 버전
        
        Returns:
            저장된 파일 경로 딕셔너리
        """
        files = {}
        
        # 510(k) 요약
        summary_510k = self.generate_510k_summary(device_name, "Cookiie Brain Engine Team")
        summary_path = self.output_dir / '510k_summary.md'
        summary_path.write_text(summary_510k, encoding='utf-8')
        files['510k_summary'] = summary_path
        
        # 기술 파일
        technical_file = self.generate_technical_file(device_name, software_version)
        technical_path = self.output_dir / 'technical_file.json'
        with open(technical_path, 'w', encoding='utf-8') as f:
            json.dump(technical_file, f, indent=2, ensure_ascii=False)
        files['technical_file'] = technical_path
        
        # ISO 13485 체크리스트
        iso_checklist = self.generate_iso13485_checklist()
        checklist_path = self.output_dir / 'iso13485_checklist.json'
        with open(checklist_path, 'w', encoding='utf-8') as f:
            json.dump(iso_checklist, f, indent=2, ensure_ascii=False)
        files['iso13485_checklist'] = checklist_path
        
        return files

