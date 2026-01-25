# ADHD Simulation Engine

**Cookiie Brain Engine 기반 ADHD 전용 시뮬레이션 시스템**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📋 개요

ADHD Simulation Engine은 Cookiie Brain Engine의 동역학적 상호작용을 활용하여 ADHD의 주요 특성(주의력 결핍, 충동성, 과잉행동)을 시뮬레이션하는 전용 엔진입니다.

**⚠️ 중요 안내**:
- 이 프로젝트는 인지 동역학의 계산적 시뮬레이션입니다.
- **진단, 예측, 또는 치료 권고를 제공하지 않습니다.**
- 연구 및 교육 목적으로만 사용되어야 합니다.
- 실제 의학적 진단 도구가 아닙니다.
- 실제 ADHD 진단은 전문의와 상담해야 합니다.

---

## 🎯 사용 목적별 구분

### 공학용 / 연구용 (현재 버전)

**용도**:
- 연구 및 교육 목적
- 알고리즘 개발 및 테스트
- 시뮬레이션 실험
- 개념 검증

**특징**:
- ✅ 빠른 프로토타이핑
- ✅ 유연한 파라미터 조정
- ✅ 교육 및 연구 목적
- ✅ 오픈루프 측정 구조

**대상 사용자**:
- 연구자
- 교육자
- 알고리즘 개발자
- 시뮬레이션 실험자

---

### 의료용 / 임상용 (확장 계획)

**용도**:
- 대학 병원 연구소
- 종합 병원 연구
- 임상 연구 지원
- 정밀 시뮬레이션

**특징** (계획 중):
- 🔄 폐루프 동역학 구조
- 🔄 재현성 보장 (Seed 관리)
- 🔄 상태공간 좌표 출력
- 🔄 의료 표준 준수 (HL7/FHIR)
- 🔄 생체 데이터 통합 (fMRI, EEG 등)
- 🔄 약물 효과 시뮬레이션 (PK/PD)

**대상 사용자**:
- 의료 연구자
- 임상 연구소
- 대학 병원 연구팀

**확장 로드맵**: [Cookiie Brain Engine - Clinical Roadmap](https://github.com/qquartsco-svg/cookiieBrain_alpha/blob/main/docs/medical/CLINICAL_ENGINE_ROADMAP.md)

---

**현재 버전**: 공학용/연구용  
**의료용 확장**: 계획 중 (Phase 1-4)

---

## 🎯 주요 기능

### 1. ADHD 특화 엔진

- **AttentionControlEngine**: 주의력 제어 및 측정
  - 주의력 지속 능력 측정
  - 주의 분산 감지
  - ADHD 패턴 분석

- **ImpulseControlEngine**: 충동성 제어 및 측정
  - 즉각적 vs 지연된 보상 선택
  - 할인율(discount rate) 모델링
  - 충동성 점수 계산

- **HyperactivityEngine**: 과잉행동 측정
  - 에너지 변동성 분석
  - 에너지 불일치 감지
  - 과잉행동 점수 계산

### 2. 시뮬레이션 시나리오

- **주의력 지속 테스트**: 30초간 주의력 유지 능력 측정
  - 작업 중요도 기반 주의력 계산
  - 시간에 따른 주의력 감소 모델링
  - ADHD 패턴 감지
  
- **충동성 테스트**: 4가지 시나리오에서 즉각적 vs 지연된 보상 선택
  - 할인율(discount rate) 기반 선택 모델
  - 충동성 점수 계산
  - ADHD 패턴 감지
  
- **과잉행동 테스트**: 10초간 에너지 변동성 측정
  - 에너지 불일치 분석
  - 에너지 변동성 계산
  - ADHD 패턴 감지

### 3. 동역학적 상호작용

- Cookiie Brain Engine의 엔진 간 상호작용 활용
- Thalamus → PFC → Basal Ganglia 흐름
- Hypothalamus 에너지 관리
- 실시간 상태 추적

---

## 🚀 빠른 시작

### 사전 요구사항

1. **Cookiie Brain Engine 설치**:
   ```bash
   git clone https://github.com/qquartsco-svg/cookiieBrain_alpha.git
   cd cookiieBrain_alpha
   # Cookiie Brain Engine 설치 방법 참조
   ```

2. **ADHD Simulation Engine 설치**:
   ```bash
   # 저장소 클론
   git clone https://github.com/qquartsco-svg/adhd_simulation_engine.git
   cd adhd_simulation_engine

   # 의존성 설치
   pip install -r requirements.txt
   ```

### 기본 실행

```bash
# Cookiie Brain Engine이 상위 디렉토리에 있는 경우
python3 adhd_simulator.py

# 또는 환경 변수로 경로 지정
export COOKIIE_BRAIN_PATH=/path/to/Cookiie_Brain_Engine
python3 adhd_simulator.py
```

### 코드에서 사용

```python
from adhd_simulator import ADHDSimulator

# 시뮬레이터 초기화
simulator = ADHDSimulator()

# 전체 평가 실행
results = simulator.simulate_full_adhd_assessment()

# 개별 테스트
attention_results = simulator.simulate_attention_task(duration=30.0)
impulsivity_results = simulator.simulate_impulsivity_task(scenarios)
hyperactivity_results = simulator.simulate_hyperactivity_task(duration=10.0)

# 결과 시각화
simulator.visualize_results('results.png')
```

---

## 📊 시뮬레이션 결과

### 주의력 테스트

- **평균 주의력 점수**: 0.0 ~ 1.0
- **주의력 감소율**: 시간에 따른 주의력 감소 비율
- **ADHD 패턴 감지**: True/False

### 충동성 테스트

- **충동적 선택 비율**: 즉각적 보상을 선택한 비율
- **평균 충동성 점수**: 0.0 ~ 1.0
- **ADHD 패턴 감지**: True/False

### 과잉행동 테스트

- **평균 과잉행동 점수**: 0.0 ~ 1.0
- **에너지 변동성**: 에너지 레벨의 변동성
- **ADHD 패턴 감지**: True/False

### 종합 평가 결과 (Assessment Summary)

- **ADHD-like dynamics strongly observed**: 3가지 특성 모두에서 ADHD 유사 패턴 관측
- **Attention deficit pattern observed**: 주의력 결핍 패턴만 관측
- **Impulsivity/Hyperactivity pattern observed**: 충동성 또는 과잉행동 패턴만 관측
- **Normal range dynamics**: ADHD 유사 패턴 미관측

**참고**: 이 결과는 시뮬레이션 기반 동역학적 패턴 관측이며, 의학적 진단이 아닙니다.

---

## 🧠 동역학적 상호작용

### 엔진 간 상호작용

1. **Thalamus**: 주의력 필터링
   - 주의 분산 요인 필터링
   - 중요한 정보만 통과

2. **PFC**: 인지 제어
   - 목표 관리
   - 충동성 억제

3. **Basal Ganglia**: 행동 선택
   - 즉각적 vs 지연된 보상 선택
   - 행동 억제

4. **Hypothalamus**: 에너지 관리
   - 에너지 레벨 조절
   - 과잉행동 제어

### 실시간 상태 추적

- 에너지 레벨
- 각성도
- 패턴 신뢰도 (시뮬레이션 기반)
- 주의력 점수

---

## 📁 프로젝트 구조

```
ADHD_Simulation_Engine/
├── adhd_engines.py          # ADHD 특화 엔진
├── adhd_simulator.py        # 메인 시뮬레이터
├── __init__.py              # 모듈 초기화
├── README.md                # 이 파일
├── requirements.txt         # 의존성 목록
├── LICENSE                  # MIT 라이선스
├── .gitignore              # Git 무시 파일
└── PHAM_BLOCKCHAIN_SIGNATURE.md  # PHAM 서명
```

---

## 📦 의존성

### 필수 의존성

- **Python 3.8+**
- **numpy** >= 1.20.0
- **matplotlib** >= 3.3.0
- **Cookiie Brain Engine**: 별도 설치 필요
  - 설치 방법: [Cookiie Brain Engine](https://github.com/qquartsco-svg/cookiieBrain_alpha)

### 선택적 의존성

- **scipy** >= 1.7.0 (고급 수치 계산)
- **pandas** >= 1.3.0 (데이터 분석)

### Cookiie Brain Engine 경로 설정

ADHD Simulation Engine은 Cookiie Brain Engine에 의존합니다. 다음 방법 중 하나로 경로를 설정할 수 있습니다:

1. **기본 경로** (자동 감지):
   - 상위 디렉토리의 `Cookiie_Brain_Engine` 폴더를 자동으로 찾습니다
   - 예: `ADHD_Simulation_Engine/../Cookiie_Brain_Engine/`

2. **환경 변수로 지정**:
   ```bash
   export COOKIIE_BRAIN_PATH=/path/to/Cookiie_Brain_Engine
   python3 adhd_simulator.py
   ```

3. **코드에서 직접 수정**:
   `adhd_simulator.py` 파일의 경로 설정 부분을 수정하세요.

---

## 📝 사용 예시

### 전체 평가 실행

```python
from adhd_simulator import ADHDSimulator

simulator = ADHDSimulator()
results = simulator.simulate_full_adhd_assessment()

print(f"Assessment summary: {results['assessment']}")
print(f"Pattern confidence (simulation-based): {results['confidence']:.2f}")
print(f"Attention deficit score: {results['attention_deficit']:.3f}")
print(f"Impulsivity score: {results['impulsivity']:.3f}")
print(f"Hyperactivity score: {results['hyperactivity']:.3f}")
```

**참고**: `assessment`는 시뮬레이션 기반 동역학적 패턴 평가 결과이며, 의학적 진단이 아닙니다.

### 개별 테스트 실행

```python
# 주의력 테스트
attention_results = simulator.simulate_attention_task(
    duration=30.0,
    task_importance=0.8
)

# 충동성 테스트
scenarios = [
    {'immediate': 5, 'delayed': 50, 'delay': 10},
    {'immediate': 10, 'delayed': 100, 'delay': 20},
]
impulsivity_results = simulator.simulate_impulsivity_task(scenarios)

# 과잉행동 테스트
hyperactivity_results = simulator.simulate_hyperactivity_task(
    duration=10.0,
    task_demand=0.5
)
```

---

## ⚠️ 주의사항

### 공학용/연구용 버전

**이 시뮬레이션은 연구 및 교육 목적으로만 사용되어야 합니다.**

- ❌ 실제 의학적 진단 도구가 아닙니다
- ❌ 실제 ADHD 진단은 전문의와 상담해야 합니다
- ✅ 시뮬레이션 결과는 참고용입니다
- ✅ 연구 및 교육 목적으로 사용 가능합니다
- ✅ 알고리즘 개발 및 테스트 목적

### 의료용 버전 (확장 계획)

의료용 버전은 현재 개발 계획 중이며, 다음 기능을 포함할 예정입니다:

- 🔄 의료 표준 준수 (HL7/FHIR)
- 🔄 재현성 보장 시스템
- 🔄 정밀 생체 데이터 통합
- 🔄 임상 연구 지원 기능

**의료용 버전은 실제 의학적 진단 도구가 아닙니다.**  
임상 연구 지원 및 시뮬레이션 목적으로만 사용되어야 합니다.

---

## 🔬 확장 가능성

### 공학용/연구용 확장

1. **개인화된 시뮬레이션**
   - 개인별 ADHD 특성 파라미터 조정
   - 맞춤형 테스트 시나리오

2. **다양한 시나리오**
   - 학습 환경 시뮬레이션
   - 작업 환경 시뮬레이션
   - 사회적 상호작용 시뮬레이션

3. **알고리즘 개선**
   - 성능 최적화
   - 새로운 모델 통합
   - 실험 기능 추가

### 의료용 확장 (계획 중)

1. **폐루프 동역학**
   - 엔진 간 피드백 루프
   - 상태 벡터 기반 동역학
   - 시간축 전이 모델링

2. **재현성 시스템**
   - Seed 관리
   - 실험 메타데이터
   - 재현 가능한 결과

3. **의료 표준 준수**
   - HL7/FHIR 호환
   - 생체 데이터 통합 (fMRI, EEG, HRV)
   - 의료 리포트 생성

4. **약물 효과 시뮬레이션**
   - PK/PD 모델링
   - 치료 효과 예측
   - 개입 전후 비교

5. **장기 추적**
   - 장기간 ADHD 패턴 추적
   - 변화 추이 분석
   - 예측 모델링

**의료용 확장 로드맵**: [Clinical Engine Roadmap](https://github.com/qquartsco-svg/cookiieBrain_alpha/blob/main/docs/medical/CLINICAL_ENGINE_ROADMAP.md)

---

## 📚 참고 자료

- **[Cookiie Brain Engine](https://github.com/qquartsco-svg/cookiieBrain_alpha)**: 기본 엔진 (필수 의존성)
- **Cookiie Brain Engine 문서**:
  - [ADHD 적용 분석](https://github.com/qquartsco-svg/cookiieBrain_alpha/blob/main/docs/concepts/ADHD_APPLICATION_ANALYSIS.md)
  - [의료용 확장 로드맵](https://github.com/qquartsco-svg/cookiieBrain_alpha/blob/main/docs/medical/CLINICAL_ENGINE_ROADMAP.md)

---

## 📄 라이선스

MIT License

---

## 👤 작성자

**GNJz (Qquarts)**

- GitHub: [@qquartsco-svg](https://github.com/qquartsco-svg)
- 작성일: 2025-01-25

---

## 🤝 기여

기여를 환영합니다! 이슈를 열거나 Pull Request를 보내주세요.

---

## 📧 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 열어주세요.

---

**⚠️ 면책 조항**: 이 시뮬레이션은 연구 및 교육 목적으로만 사용되어야 하며, 실제 의학적 진단 도구가 아닙니다. 실제 ADHD 진단은 전문의와 상담해야 합니다.
