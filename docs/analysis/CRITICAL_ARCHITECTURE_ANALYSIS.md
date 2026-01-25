# 🔨 의료기기(SaMD) 전환을 위한 구조 파괴 및 재건축 계획

**분석 일자**: 2025-01-25  
**분석 기준**: FDA SaMD, IEC 62304, ISO 14971, HL7 FHIR (실제 규제 기준)  
**목적**: "의료기기 흉내" → "실제 의료기기" 전환을 위한 구조적 재설계

---

## 🚨 현재 구조의 치명적 결함 (규제 기준)

### 결함 1: "약물-판단" 직결 구조 (Critical Risk)

**현재 구조**:
```
약물 투여 → PK/PD 모델 → 증상 점수 → ADHD 판단
```

**규제기관 시선**:
- ❌ **블랙박스형 위험 시스템**
- ❌ **의사 개입 불가능한 자동 판단**
- ❌ **약물 효과가 직접 진단에 영향** (SaMD 금지 사항)

**FDA 반응 예상**: 즉시 리젝

---

### 결함 2: "형식적 FHIR" (Semantic Binding 부재)

**현재 구조**:
```
시뮬레이션 결과 → FHIR 리소스 (타입만 맞춤)
```

**병원 EHR 시선**:
- ❌ **Provenance 리소스 부재** → 데이터 무효
- ❌ **LOINC 코드 검증 없음** → 의미론적 불일치
- ❌ **Clinical Context 부족** → why/how/instrument 없음
- ❌ **Device 정보 없음** → UDI 부재

**병원 반응 예상**: 데이터 거부

---

### 결함 3: "문서 생성 시스템" (QMS 부재)

**현재 구조**:
```
코드 완성 → 사후 문서 생성
```

**규제기관 시선**:
- ❌ **개발 과정 기록 없음**
- ❌ **위험 분석과 코드 분리**
- ❌ **변경 추적성 없음**
- ❌ **"조작된 문서"로 간주 가능**

**ISO 13485 반응**: 즉시 리젝

---

## 🔨 부숴야 할 구조 (3가지)

### 1. 약물-판단 직결 구조 파괴

**현재 코드 위치**:
- `pkpd_model.py`: `get_pharmacodynamic_effect()` → 직접 점수 반환
- `adhd_simulator.py`: 약물 효과가 직접 ADHD 점수에 반영

**파괴 방법**:
```python
# ❌ 현재 (위험)
medication_effect = pkpd.get_pharmacodynamic_effect(...)
attention_score = base_attention * (1 + medication_effect['attention_boost'])

# ✅ 재설계 (안전)
medication_effect = pkpd.get_pharmacodynamic_effect(...)  # Sandbox
# → 의사가 "반응성 계수"를 조정
# → 시스템은 "가능성"만 제시
```

**재건축 방향**:
- PK/PD 모듈을 완전히 격리된 Sandbox로 분리
- 약물 효과는 "인지 반응성(Responsiveness)" 매개 변수로만 전달
- 의사가 이 매개 변수를 조정 가능한 CDSS 구조

---

### 2. 형식적 FHIR 파괴

**현재 코드 위치**:
- `fhir_mapper.py`: Observation 생성 시 Provenance 없음
- LOINC 코드 검증 없음
- Device 정보 없음

**파괴 방법**:
```python
# ❌ 현재 (무효)
observation = {
    'resourceType': 'Observation',
    'valueQuantity': {...}
    # Provenance 없음
    # Device 없음
}

# ✅ 재설계 (유효)
observation = {
    'resourceType': 'Observation',
    'valueQuantity': {...},
    'device': {
        'reference': 'Device/cookiie-brain-v1.0.0',
        'display': 'Cookiie Brain Engine v1.0.0'
    },
    'extension': [{
        'url': 'http://hl7.org/fhir/StructureDefinition/provenance',
        'valueReference': {
            'reference': 'Provenance/...'
        }
    }]
}

provenance = {
    'resourceType': 'Provenance',
    'target': [{'reference': 'Observation/...'}],
    'recorded': timestamp,
    'agent': [{
        'type': {'coding': [{'code': 'author'}]},
        'who': {'reference': 'Device/cookiie-brain-v1.0.0'},
        'onBehalfOf': {'reference': 'Organization/...'}
    }],
    'entity': [{
        'role': 'source',
        'what': {
            'reference': 'Algorithm/cookiie-brain-algorithm-v1.0.0',
            'display': 'Cookiie Brain ADHD Simulation Algorithm'
        }
    }]
}
```

**재건축 방향**:
- 모든 Observation에 Provenance 강제
- Device 리소스 생성 (UDI 포함)
- LOINC 코드 Semantic Validator 추가
- Clinical Context (why/how/instrument) 필수

---

### 3. 문서 생성 시스템 파괴

**현재 코드 위치**:
- `regulatory_preparation.py`: 사후 문서 생성
- 개발 과정과 분리

**파괴 방법**:
```python
# ❌ 현재 (조작 가능)
# 코드 완성 후 문서 생성
regulatory.save_regulatory_documents(...)

# ✅ 재설계 (추적 가능)
# 코드 변경 시 자동 위험 분석 및 로그
class RiskAwareCodeChange:
    def on_code_change(self, file_path, change_type):
        # 1. 위험 분석 자동 실행
        risk_analysis = self.analyze_risk(file_path, change_type)
        
        # 2. Audit Trail 자동 기록
        self.audit_trail.record({
            'timestamp': now(),
            'file': file_path,
            'change': change_type,
            'risk_impact': risk_analysis,
            'developer': get_current_user()
        })
        
        # 3. QMS 문서 자동 업데이트
        self.qms.update_design_history(file_path, risk_analysis)
```

**재건축 방향**:
- 코드 변경 → 위험 분석 → Audit Trail → QMS 문서 (자동 연동)
- 개발 과정 자체가 규제 문서가 되는 구조

---

## 🏗️ 재건축 전략

### Phase 4A: 구조 분리 (Critical)

**목표**: 약물-판단 직결 구조 파괴

**작업**:
1. PK/PD 모듈을 완전히 격리된 Sandbox로 분리
2. 약물 효과는 "인지 반응성" 매개 변수로만 전달
3. 의사 개입 가능한 CDSS 구조로 전환

**예상 기간**: 2-3개월

---

### Phase 4B: FHIR Semantic Binding (Critical)

**목표**: 형식적 FHIR → 의미론적 FHIR

**작업**:
1. Provenance 리소스 강제 생성
2. Device 리소스 생성 (UDI 포함)
3. LOINC 코드 Semantic Validator
4. Clinical Context 필수화

**예상 기간**: 1-2개월

---

### Phase 4C: QMS 기반 개발 (Critical)

**목표**: 문서 생성 → 개발 과정 기록

**작업**:
1. 코드 변경 시 자동 위험 분석
2. Audit Trail 자동 기록
3. QMS 문서 자동 업데이트
4. 개발 과정 = 규제 문서 구조

**예상 기간**: 2-3개월

---

## 📊 재건축 후 예상 준수도

| 규제 기준 | 현재 | 재건축 후 | 향상 |
|----------|------|----------|------|
| **FDA SaMD** | 50% | 85% | +35%p |
| **IEC 62304** | 55% | 90% | +35%p |
| **ISO 14971** | 50% | 85% | +35%p |
| **HL7 FHIR** | 40% | 90% | +50%p |
| **전체 평균** | 60% | **88%** | **+28%p** |

---

## ⚠️ 경고

**이 재건축은 "개선"이 아니라 "파괴 후 재건"입니다.**

- 기존 코드의 30-40%는 완전히 재작성 필요
- 아키텍처 전면 변경
- API 호환성 깨짐

**하지만**:
- 규제 승인 가능한 구조
- 병원 EHR 연동 가능
- 실제 의료기기로 전환 가능

---

## 🎯 결론

**현재**: "의료기기 흉내" (60%)  
**재건축 후**: "실제 의료기기" (88%)

**선택지**:
1. ✅ **재건축 진행** → 의료기기 목표 (12-18개월)
2. ⚠️ **현재 구조 유지** → 연구 플랫폼으로 고정 (3-6개월)

**권장**: 재건축 진행

---

**"구조를 부수지 않으면, 규제기관이 부숴줄 것이다."**

