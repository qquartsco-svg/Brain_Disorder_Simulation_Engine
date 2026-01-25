"""
HL7 FHIR 매핑 모듈

의료 데이터 표준 (HL7 FHIR) 연동
Observation, Patient, Encounter 리소스 생성
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
import json


class FHIRMapper:
    """
    HL7 FHIR 매핑 클래스
    
    시뮬레이션 결과를 FHIR 리소스로 변환
    """
    
    def __init__(self):
        """FHIR 매퍼 초기화"""
        # SNOMED CT 코드 (예시)
        self.snomed_codes = {
            'adhd_assessment': {
                'system': 'http://snomed.info/sct',
                'code': '33747003',
                'display': 'Attention deficit hyperactivity disorder assessment'
            },
            'attention_deficit': {
                'system': 'http://snomed.info/sct',
                'code': '422587007',
                'display': 'Attention deficit'
            },
            'impulsivity': {
                'system': 'http://snomed.info/sct',
                'code': '422587007',
                'display': 'Impulsivity'
            },
            'hyperactivity': {
                'system': 'http://snomed.info/sct',
                'code': '422587007',
                'display': 'Hyperactivity'
            }
        }
        
        # LOINC 코드 (예시)
        self.loinc_codes = {
            'adhd_screening': {
                'system': 'http://loinc.org',
                'code': '69737-8',
                'display': 'ADHD screening assessment'
            }
        }
    
    def create_observation(self,
                          assessment_result: Dict,
                          patient_id: Optional[str] = None,
                          encounter_id: Optional[str] = None) -> Dict:
        """
        Observation 리소스 생성
        
        Args:
            assessment_result: 평가 결과
            patient_id: 환자 ID (익명화된 UUID)
            encounter_id: 방문 ID (선택)
        
        Returns:
            FHIR Observation 리소스
        """
        observation_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # 주의력 결핍 Observation
        attention_obs = {
            'resourceType': 'Observation',
            'id': f"{observation_id}-attention",
            'status': 'final',
            'category': [{
                'coding': [{
                    'system': 'http://terminology.hl7.org/CodeSystem/observation-category',
                    'code': 'survey',
                    'display': 'Survey'
                }]
            }],
            'code': {
                'coding': [self.snomed_codes['attention_deficit']],
                'text': 'Attention Deficit Score'
            },
            'subject': {
                'reference': f"Patient/{patient_id}" if patient_id else None
            },
            'encounter': {
                'reference': f"Encounter/{encounter_id}" if encounter_id else None
            },
            'effectiveDateTime': timestamp,
            'valueQuantity': {
                'value': assessment_result.get('scores', {}).get('attention_deficit', 0.0),
                'unit': 'score',
                'system': 'http://unitsofmeasure.org',
                'code': '{score}'
            },
            'interpretation': [{
                'coding': [{
                    'system': 'http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation',
                    'code': 'H' if assessment_result.get('scores', {}).get('attention_deficit', 0.0) > 0.7 else 'N',
                    'display': 'High' if assessment_result.get('scores', {}).get('attention_deficit', 0.0) > 0.7 else 'Normal'
                }]
            }],
            'note': [{
                'text': '⚠️ 시뮬레이션 기반 평가, 의학적 진단 아님'
            }]
        }
        
        # 충동성 Observation
        impulsivity_obs = {
            'resourceType': 'Observation',
            'id': f"{observation_id}-impulsivity",
            'status': 'final',
            'category': [{
                'coding': [{
                    'system': 'http://terminology.hl7.org/CodeSystem/observation-category',
                    'code': 'survey',
                    'display': 'Survey'
                }]
            }],
            'code': {
                'coding': [self.snomed_codes['impulsivity']],
                'text': 'Impulsivity Score'
            },
            'subject': {
                'reference': f"Patient/{patient_id}" if patient_id else None
            },
            'encounter': {
                'reference': f"Encounter/{encounter_id}" if encounter_id else None
            },
            'effectiveDateTime': timestamp,
            'valueQuantity': {
                'value': assessment_result.get('scores', {}).get('impulsivity', 0.0),
                'unit': 'score',
                'system': 'http://unitsofmeasure.org',
                'code': '{score}'
            },
            'interpretation': [{
                'coding': [{
                    'system': 'http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation',
                    'code': 'H' if assessment_result.get('scores', {}).get('impulsivity', 0.0) > 0.6 else 'N',
                    'display': 'High' if assessment_result.get('scores', {}).get('impulsivity', 0.0) > 0.6 else 'Normal'
                }]
            }],
            'note': [{
                'text': '⚠️ 시뮬레이션 기반 평가, 의학적 진단 아님'
            }]
        }
        
        # 과잉행동 Observation
        hyperactivity_obs = {
            'resourceType': 'Observation',
            'id': f"{observation_id}-hyperactivity",
            'status': 'final',
            'category': [{
                'coding': [{
                    'system': 'http://terminology.hl7.org/CodeSystem/observation-category',
                    'code': 'survey',
                    'display': 'Survey'
                }]
            }],
            'code': {
                'coding': [self.snomed_codes['hyperactivity']],
                'text': 'Hyperactivity Score'
            },
            'subject': {
                'reference': f"Patient/{patient_id}" if patient_id else None
            },
            'encounter': {
                'reference': f"Encounter/{encounter_id}" if encounter_id else None
            },
            'effectiveDateTime': timestamp,
            'valueQuantity': {
                'value': assessment_result.get('scores', {}).get('hyperactivity', 0.0),
                'unit': 'score',
                'system': 'http://unitsofmeasure.org',
                'code': '{score}'
            },
            'interpretation': [{
                'coding': [{
                    'system': 'http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation',
                    'code': 'H' if assessment_result.get('scores', {}).get('hyperactivity', 0.0) > 0.6 else 'N',
                    'display': 'High' if assessment_result.get('scores', {}).get('hyperactivity', 0.0) > 0.6 else 'Normal'
                }]
            }],
            'note': [{
                'text': '⚠️ 시뮬레이션 기반 평가, 의학적 진단 아님'
            }]
        }
        
        return {
            'observations': [attention_obs, impulsivity_obs, hyperactivity_obs],
            'bundle': self._create_bundle([attention_obs, impulsivity_obs, hyperactivity_obs])
        }
    
    def create_patient(self,
                      age: int,
                      gender: str,
                      patient_id: Optional[str] = None) -> Dict:
        """
        Patient 리소스 생성 (익명화)
        
        Args:
            age: 나이
            gender: 성별 ('male', 'female', 'other')
            patient_id: 환자 ID (없으면 생성)
        
        Returns:
            FHIR Patient 리소스
        """
        if patient_id is None:
            patient_id = str(uuid.uuid4())
        
        # 성별 코드 매핑
        gender_code = {
            'male': 'male',
            'female': 'female',
            'other': 'other'
        }.get(gender.lower(), 'unknown')
        
        # 출생일 계산 (나이 기반, 정확한 날짜는 익명화)
        birth_year = datetime.now().year - age
        
        patient = {
            'resourceType': 'Patient',
            'id': patient_id,
            'meta': {
                'security': [{
                    'system': 'http://terminology.hl7.org/CodeSystem/v3-Confidentiality',
                    'code': 'R',
                    'display': 'Restricted'
                }]
            },
            'gender': gender_code,
            'birthDate': f"{birth_year}-01-01",  # 익명화: 정확한 날짜 제거
            'extension': [{
                'url': 'http://hl7.org/fhir/StructureDefinition/patient-age',
                'valueAge': {
                    'value': age,
                    'unit': 'years',
                    'system': 'http://unitsofmeasure.org',
                    'code': 'a'
                }
            }],
            'identifier': [{
                'system': 'http://hospital.example.org/patients',
                'value': patient_id,
                'type': {
                    'coding': [{
                        'system': 'http://terminology.hl7.org/CodeSystem/v2-0203',
                        'code': 'MR',
                        'display': 'Medical Record Number'
                    }]
                }
            }]
        }
        
        return patient
    
    def create_encounter(self,
                        patient_id: str,
                        encounter_type: str = 'outpatient',
                        encounter_id: Optional[str] = None) -> Dict:
        """
        Encounter 리소스 생성
        
        Args:
            patient_id: 환자 ID
            encounter_type: 방문 유형 ('outpatient', 'inpatient', 'emergency')
            encounter_id: 방문 ID (없으면 생성)
        
        Returns:
            FHIR Encounter 리소스
        """
        if encounter_id is None:
            encounter_id = str(uuid.uuid4())
        
        encounter = {
            'resourceType': 'Encounter',
            'id': encounter_id,
            'status': 'finished',
            'class': {
                'system': 'http://terminology.hl7.org/CodeSystem/v3-ActCode',
                'code': 'AMB' if encounter_type == 'outpatient' else 'IMP',
                'display': 'Ambulatory' if encounter_type == 'outpatient' else 'Inpatient'
            },
            'type': [{
                'coding': [{
                    'system': 'http://www.snomed.org/sct',
                    'code': '390906007',
                    'display': 'Follow-up encounter'
                }]
            }],
            'subject': {
                'reference': f"Patient/{patient_id}"
            },
            'period': {
                'start': datetime.now().isoformat(),
                'end': datetime.now().isoformat()
            },
            'reasonCode': [{
                'coding': [{
                    'system': 'http://snomed.info/sct',
                    'code': '33747003',
                    'display': 'ADHD assessment'
                }]
            }]
        }
        
        return encounter
    
    def create_diagnostic_report(self,
                                assessment_result: Dict,
                                patient_id: str,
                                encounter_id: str) -> Dict:
        """
        DiagnosticReport 리소스 생성
        
        Args:
            assessment_result: 평가 결과
            patient_id: 환자 ID
            encounter_id: 방문 ID
        
        Returns:
            FHIR DiagnosticReport 리소스
        """
        report_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # DSM-5/ICD-11 결과
        dsm5 = assessment_result.get('clinical_assessment', {}).get('dsm5', {})
        icd11 = assessment_result.get('clinical_assessment', {}).get('icd11', {})
        
        report = {
            'resourceType': 'DiagnosticReport',
            'id': report_id,
            'status': 'final',
            'category': [{
                'coding': [{
                    'system': 'http://terminology.hl7.org/CodeSystem/v2-0074',
                    'code': 'LAB',
                    'display': 'Laboratory'
                }]
            }],
            'code': {
                'coding': [self.loinc_codes['adhd_screening']],
                'text': 'ADHD Simulation Assessment'
            },
            'subject': {
                'reference': f"Patient/{patient_id}"
            },
            'encounter': {
                'reference': f"Encounter/{encounter_id}"
            },
            'effectiveDateTime': timestamp,
            'issued': timestamp,
            'conclusion': f"시뮬레이션 기반 ADHD 패턴 평가 (DSM-5: {dsm5.get('subtype', 'N/A')}, ICD-11: {icd11.get('code', 'N/A')})",
            'conclusionCode': [{
                'coding': [{
                    'system': 'http://hl7.org/fhir/sid/icd-11',
                    'code': icd11.get('code', ''),
                    'display': icd11.get('description', '')
                }]
            }],
            'note': [{
                'text': '⚠️ 이 리포트는 시뮬레이션 기반 평가이며, 의학적 진단이 아닙니다. 전문의 상담이 필요합니다.'
            }]
        }
        
        return report
    
    def _create_bundle(self, resources: List[Dict]) -> Dict:
        """
        FHIR Bundle 생성
        
        Args:
            resources: FHIR 리소스 목록
        
        Returns:
            FHIR Bundle 리소스
        """
        bundle_id = str(uuid.uuid4())
        
        bundle = {
            'resourceType': 'Bundle',
            'id': bundle_id,
            'type': 'collection',
            'timestamp': datetime.now().isoformat(),
            'entry': [
                {
                    'fullUrl': f"urn:uuid:{resource.get('id', '')}",
                    'resource': resource
                }
                for resource in resources
            ]
        }
        
        return bundle
    
    def export_to_fhir_json(self, resources: Dict, output_path: str):
        """
        FHIR 리소스를 JSON 파일로 내보내기
        
        Args:
            resources: FHIR 리소스 딕셔너리
            output_path: 출력 파일 경로
        """
        from pathlib import Path
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resources, f, indent=2, ensure_ascii=False)
    
    def create_complete_fhir_bundle(self,
                                   assessment_result: Dict,
                                   age: int,
                                   gender: str) -> Dict:
        """
        완전한 FHIR Bundle 생성 (Patient + Encounter + Observations + Report)
        
        Args:
            assessment_result: 평가 결과
            age: 나이
            gender: 성별
        
        Returns:
            완전한 FHIR Bundle
        """
        # Patient 생성
        patient = self.create_patient(age, gender)
        patient_id = patient['id']
        
        # Encounter 생성
        encounter = self.create_encounter(patient_id)
        encounter_id = encounter['id']
        
        # Observations 생성
        observations_result = self.create_observation(
            assessment_result,
            patient_id,
            encounter_id
        )
        observations = observations_result['observations']
        
        # DiagnosticReport 생성
        diagnostic_report = self.create_diagnostic_report(
            assessment_result,
            patient_id,
            encounter_id
        )
        
        # Bundle 생성
        all_resources = [patient, encounter] + observations + [diagnostic_report]
        bundle = self._create_bundle(all_resources)
        
        return {
            'bundle': bundle,
            'patient': patient,
            'encounter': encounter,
            'observations': observations,
            'diagnostic_report': diagnostic_report
        }

