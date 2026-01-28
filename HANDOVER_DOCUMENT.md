# Brain Disorder Simulation Engine - 인수인계 문서

**작성일**: 2025-01-27  
**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0  
**상태**: 작업 중단 (컴퓨터 재부팅 전 인수인계)

---

## 📋 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [프로젝트 구조](#프로젝트-구조)
3. [구현된 기능](#구현된-기능)
4. [주요 파일 위치](#주요-파일-위치)
5. [실행 방법](#실행-방법)
6. [다음 작업 계획](#다음-작업-계획)
7. [주의사항 및 제한사항](#주의사항-및-제한사항)
8. [의존성 및 환경](#의존성-및-환경)

---

## 프로젝트 개요

### 프로젝트명
**Brain Disorder Simulation Engine** (뇌 질환 시뮬레이션 통합 엔진)

### 목적
Cookiie Brain Engine의 동역학적 상호작용을 활용하여 다양한 뇌 질환의 메커니즘을 시뮬레이션하는 통합 시스템

### 핵심 철학
- **"왜 이런 상황이 발생하는가?"** 원인 분석 중심
- 치료 도구가 아닌 **메커니즘 이해 도구**
- 연구 및 교육 목적 (의학적 진단 도구 아님)

### 지원하는 뇌 질환
- ✅ **ADHD** (주의력 결핍 과잉행동 장애)
- ✅ **우울증** (Depression)
- ✅ **불안장애** (Anxiety)
- ✅ **PTSD** (외상 후 스트레스 장애)
- ⏳ **강박장애** (OCD) - 구현 예정

### 현재 준비도
- **연구용/교육용**: ✅ 90-95% (사용 가능)
- **의료용 병원**: ❌ 25-30% (사용 불가능)

---

## 프로젝트 구조

### 디렉토리 구조

```
ADHD_Simulation_Engine/                    # 프로젝트 루트
├── brain_disorder_simulation/              # 메인 패키지
│   ├── __init__.py
│   ├── common/                            # 공통 엔진
│   │   ├── negative_bias_engine.py        # 부정적 편향 엔진
│   │   ├── cognitive_control_engine.py   # 인지 제어 엔진
│   │   ├── energy_depletion_engine.py     # 에너지 고갈 엔진
│   │   └── loops/                         # 루프 라이브러리 (작업 예정)
│   ├── disorders/                         # 질환별 모듈
│   │   ├── adhd/                          # ADHD 시뮬레이션
│   │   │   ├── __init__.py
│   │   │   └── adhd_engines.py            # ADHD 특화 엔진
│   │   ├── depression/                    # 우울증 시뮬레이션
│   │   │   ├── __init__.py
│   │   │   ├── depression_simulator.py    # 우울증 시뮬레이터
│   │   │   ├── depression_tasks.py       # 우울증 특화 태스크
│   │   │   └── motivation_engine.py      # 동기 엔진
│   │   ├── anxiety/                       # 불안장애 시뮬레이션
│   │   ├── ptsd/                          # PTSD 시뮬레이션
│   │   │   ├── __init__.py
│   │   │   ├── ptsd_engines.py            # PTSD 특화 엔진
│   │   │   └── ptsd_simulator.py          # PTSD 시뮬레이터
│   │   └── ocd/                           # 강박장애 (구현 예정)
│   ├── research/                          # 연구 모듈
│   │   ├── __init__.py
│   │   ├── clinical_scales.py            # 임상 스케일 (HAM-D, BDI, PHQ-9)
│   │   ├── depression/                    # 우울증 연구 도구
│   │   │   ├── neurotransmitters.py       # 신경전달물질 시스템
│   │   │   ├── biomarkers.py              # 생체지표 매핑
│   │   │   └── validation.py              # 검증 시스템
│   │   └── utils/
│   │       ├── statistical.py             # 통계 분석
│   │       └── reporting.py               # 리포트 생성
│   ├── unified/                           # 통합 시뮬레이터
│   │   ├── __init__.py
│   │   └── unified_simulator.py           # 통합 시뮬레이터 메인 클래스
│   ├── utils/                             # 유틸리티
│   │   ├── reproducibility.py             # 재현성 시스템
│   │   ├── statistics.py                  # 통계 검증
│   │   ├── report_generator.py           # 리포트 생성
│   │   └── dynamics_invariant_tests.py    # 동역학 불변식 테스트
│   ├── medical/                           # 의료용 모듈 (Phase 1-3)
│   │   ├── input_validator.py             # 입력 검증
│   │   ├── audit_trail.py                 # 감사 추적
│   │   ├── dsm5_icd11_mapping.py          # DSM-5/ICD-11 매핑
│   │   ├── normative_data.py             # 규준 데이터
│   │   ├── fhir_mapper.py                # HL7 FHIR 매퍼
│   │   ├── pkpd_model.py                 # PK/PD 모델
│   │   ├── validation_study.py           # 검증 연구
│   │   ├── irb_templates.py              # IRB 템플릿
│   │   └── regulatory_preparation.py     # 규제 준비
│   └── engineering/                       # 엔지니어링 모듈
│       ├── architecture/                 # 아키텍처 분석
│       ├── dynamics/                     # 동역학 분석
│       └── optimization/                 # 최적화 분석
├── adhd_simulation/                       # 기존 ADHD 모듈 (호환성 유지)
│   ├── core/
│   │   ├── adhd_engines.py
│   │   ├── adhd_simulator.py
│   │   ├── depression_engines.py
│   │   ├── depression_simulator.py
│   │   ├── closed_loop_dynamics.py
│   │   └── dopamine_system.py
│   ├── medical/                          # 의료용 모듈 (중복)
│   └── utils/                            # 유틸리티 (중복)
├── docs/                                  # 문서 디렉토리
│   ├── analysis/                         # 분석 문서
│   ├── deployment/                       # 배포 문서
│   ├── guides/                           # 가이드 문서
│   ├── medical/                          # 의료 관련 문서
│   └── phase/                            # Phase별 보고서
├── README.md                             # 메인 README
├── CHANGELOG.md                          # 변경 이력
├── ENGINE_CAPABILITIES.md               # 엔진 기능 설명
├── PHAM_BLOCKCHAIN_SIGNATURE.md         # PHAM 블록체인 서명
├── HANDOVER_DOCUMENT.md                  # 이 파일 (인수인계 문서)
├── setup.py                              # 패키지 설정
├── requirements.txt                      # 의존성 목록
├── run_ptsd_simulation.py               # PTSD 시뮬레이션 실행 파일
└── test_research_modules.py              # 연구 모듈 테스트 파일
```

---

## 구현된 기능

### 1. 질환별 시뮬레이터

#### ADHD 시뮬레이터
- **위치**: `brain_disorder_simulation/disorders/adhd/`
- **주요 엔진**:
  - `AttentionControlEngine`: 주의력 제어 및 측정
  - `ImpulseControlEngine`: 충동성 제어 및 측정
  - `HyperactivityEngine`: 과잉행동 측정
- **기능**:
  - 주의력 지속 테스트
  - 충동성 테스트 (즉각적 vs 지연된 보상)
  - 과잉행동 테스트
  - 변동성 분석 (분산, 자기상관, 드롭아웃 비율)

#### 우울증 시뮬레이터
- **위치**: `brain_disorder_simulation/disorders/depression/`
- **주요 엔진**:
  - `NegativeBiasEngine`: 부정적 편향
  - `CognitiveControlEngine`: 인지 제어 실패
  - `EnergyDepletionEngine`: 에너지 고갈
  - `MotivationEngine`: 동기 시스템 붕괴
- **특화 태스크**:
  - `MotivationCollapseTask`: 동기 붕괴 태스크
  - `RuminationPersistenceTask`: 반추 지속 태스크
  - `EffortBasedDecisionMakingTask`: 노력 기반 의사결정 태스크
- **기능**:
  - 에너지 시스템 붕괴 과정 관측
  - 부정적 편향과 반추 패턴 재현
  - 동기 시스템 붕괴 시뮬레이션

#### PTSD 시뮬레이터
- **위치**: `brain_disorder_simulation/disorders/ptsd/`
- **주요 엔진**:
  - `IntrusiveMemoryEngine`: 침입 기억 엔진
  - `AvoidanceEngine`: 회피 엔진
  - `HyperarousalEngine`: 과각성 엔진
  - `NegativeCognitionEngine`: 부정적 인지 엔진
- **기능**:
  - 외상 기억 침입 시뮬레이션
  - 회피 행동 패턴 분석
  - 과각성 상태 모델링
  - 부정적 인지 변화 추적

### 2. 통합 시뮬레이터

#### UnifiedDisorderSimulator
- **위치**: `brain_disorder_simulation/unified/unified_simulator.py`
- **기능**:
  - 단일 질환 시뮬레이션
  - 공존 질환 (Comorbidity) 시뮬레이션
  - 커스텀 조합 시뮬레이션
  - 질환 간 비교 분석

### 3. 연구 모듈

#### 신경전달물질 시스템
- **위치**: `brain_disorder_simulation/research/depression/neurotransmitters.py`
- **구현된 시스템**:
  - `DopamineSystem`: 도파민 시스템 (Tonic/Phasic)
  - `SerotoninSystem`: 세로토닌 시스템 (SSRI 효과 포함)
  - `NorepinephrineSystem`: 노르에피네프린 시스템
  - `NeurotransmitterSystem`: 통합 시스템

#### 생체지표 매핑
- **위치**: `brain_disorder_simulation/research/depression/biomarkers.py`
- **구현된 추출기**:
  - `FMRIBiomarkerExtractor`: fMRI 활성화 패턴 추출
  - `EEGBiomarkerExtractor`: EEG 파워 스펙트럼 추출
  - `HRVBiomarkerExtractor`: HRV 지표 추출
  - `BiomarkerExtractor`: 통합 생체지표 추출기

#### 통계 분석 도구
- **위치**: `brain_disorder_simulation/research/utils/statistical.py`
- **주요 기능**:
  - `seed_sweep()`: 다중 시뮬레이션 실행
  - `compare_groups()`: 두 그룹 비교 (t-test, Cohen's d)
  - `compare_multiple_groups()`: 다중 그룹 비교 (ANOVA)
  - `generate_statistical_report()`: 통계 리포트 생성
  - `CircularBuffer`: 효율적인 히스토리 관리

#### 임상 스케일 매핑
- **위치**: `brain_disorder_simulation/research/clinical_scales.py`
- **구현된 매퍼**:
  - `HAMDMapper`: HAM-D (17항목) 매핑
  - `BDIMapper`: BDI (21항목) 매핑
  - `PHQ9Mapper`: PHQ-9 (9항목) 매핑
  - `ClinicalScaleMapper`: 통합 매퍼

#### 연구 리포트 생성
- **위치**: `brain_disorder_simulation/research/utils/reporting.py`
- **주요 기능**:
  - `generate_table1()`: 그룹별 평균 및 표준편차
  - `generate_table2()`: 통계 분석 결과
  - `generate_figure1()`: 그룹별 비교 그래프
  - `generate_figure2()`: 시간에 따른 변화 그래프
  - LaTeX, CSV 형식 출력 지원

#### 검증 시스템
- **위치**: `brain_disorder_simulation/research/depression/validation.py`
- **구현된 검증기**:
  - `BiologicalValidityValidator`: 생물학적 타당성 검증
  - `ClinicalRelevanceValidator`: 임상적 관련성 검증
  - `ReproducibilityValidator`: 연구 재현성 검증
  - `ComprehensiveValidator`: 통합 검증기

### 4. 유틸리티 모듈

#### 재현성 시스템
- **위치**: `brain_disorder_simulation/utils/reproducibility.py`
- **주요 클래스**:
  - `ReproducibleRNG`: Seed 관리 시스템
  - `ExperimentMetadata`: 실험 메타데이터

#### 통계 검증
- **위치**: `brain_disorder_simulation/utils/statistics.py`
- **주요 클래스**:
  - `StatisticalValidator`: Seed sweep 기반 신뢰도 계산

#### 리포트 생성
- **위치**: `brain_disorder_simulation/utils/report_generator.py`
- **주요 클래스**:
  - `ReportGenerator`: 표준 리포트 생성 (JSON, Markdown, PNG)

#### 동역학 불변식 테스트
- **위치**: `brain_disorder_simulation/utils/dynamics_invariant_tests.py`
- **주요 기능**:
  - 단조성 테스트
  - 할인율 테스트
  - 게이트 효과 테스트
  - 도파민 효과 테스트
  - 폐루프 안정성 테스트

### 5. 의료용 모듈 (Phase 1-3)

#### Phase 1: 기본 안전성
- **위치**: `brain_disorder_simulation/medical/`
- **구현된 모듈**:
  - `input_validator.py`: 입력 검증 (NaN, Inf, 범위, 타입)
  - `audit_trail.py`: 감사 추적 (PHI 보호 포함)

#### Phase 2: 의료 표준 준비
- **구현된 모듈**:
  - `dsm5_icd11_mapping.py`: DSM-5/ICD-11 매핑
  - `normative_data.py`: 규준 데이터 관리
  - `irb_templates.py`: IRB 제출 문서 템플릿
  - `validation_study.py`: 검증 연구 설계

#### Phase 3: 의료 표준 통합
- **구현된 모듈**:
  - `fhir_mapper.py`: HL7 FHIR 매퍼
  - `pkpd_model.py`: PK/PD 모델 (기본 구조)
  - `regulatory_preparation.py`: 규제 준비 문서

---

## 주요 파일 위치

### 실행 파일

1. **PTSD 시뮬레이션 실행**
   ```
   /Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine/run_ptsd_simulation.py
   ```
   - 실행 방법: `python run_ptsd_simulation.py`
   - 또는: `python -m brain_disorder_simulation.disorders.ptsd.ptsd_simulator`

2. **연구 모듈 테스트**
   ```
   /Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine/test_research_modules.py
   ```
   - 실행 방법: `python test_research_modules.py`

3. **통합 시뮬레이터**
   ```
   /Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine/brain_disorder_simulation/unified/unified_simulator.py
   ```
   - Python 코드에서 import하여 사용

### 핵심 클래스 파일

1. **통합 시뮬레이터**
   - `brain_disorder_simulation/unified/unified_simulator.py`
   - 클래스: `UnifiedDisorderSimulator`

2. **우울증 시뮬레이터**
   - `brain_disorder_simulation/disorders/depression/depression_simulator.py`
   - 클래스: `DepressionSimulator`

3. **PTSD 시뮬레이터**
   - `brain_disorder_simulation/disorders/ptsd/ptsd_simulator.py`
   - 클래스: `PTSDSimulator`

4. **ADHD 엔진**
   - `brain_disorder_simulation/disorders/adhd/adhd_engines.py`
   - 클래스: `AttentionControlEngine`, `ImpulseControlEngine`, `HyperactivityEngine`

### 공통 엔진 파일

1. **부정적 편향 엔진**
   - `brain_disorder_simulation/common/negative_bias_engine.py`
   - 클래스: `NegativeBiasEngine`

2. **인지 제어 엔진**
   - `brain_disorder_simulation/common/cognitive_control_engine.py`
   - 클래스: `CognitiveControlEngine`

3. **에너지 고갈 엔진**
   - `brain_disorder_simulation/common/energy_depletion_engine.py`
   - 클래스: `EnergyDepletionEngine`

### 연구 모듈 파일

1. **신경전달물질 시스템**
   - `brain_disorder_simulation/research/depression/neurotransmitters.py`

2. **생체지표 매핑**
   - `brain_disorder_simulation/research/depression/biomarkers.py`

3. **통계 분석**
   - `brain_disorder_simulation/research/utils/statistical.py`

4. **임상 스케일**
   - `brain_disorder_simulation/research/clinical_scales.py`

5. **리포트 생성**
   - `brain_disorder_simulation/research/utils/reporting.py`

6. **검증 시스템**
   - `brain_disorder_simulation/research/depression/validation.py`

### 설정 파일

1. **패키지 설정**
   - `setup.py`

2. **의존성 목록**
   - `requirements.txt`

3. **블록체인 서명**
   - `PHAM_BLOCKCHAIN_SIGNATURE.md`

---

## 실행 방법

### 1. 환경 설정

```bash
# 프로젝트 디렉토리로 이동
cd /Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine

# 가상환경 생성 (선택사항)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows

# 패키지 설치
pip install -e .

# 의존성 설치
pip install -r requirements.txt
```

### 2. Cookiie Brain Engine 경로 설정

**방법 1: 환경 변수 설정**
```bash
export COOKIIE_BRAIN_PATH=/path/to/Cookiie_Brain_Engine
```

**방법 2: 기본 경로 사용**
- 상위 디렉토리의 `Cookiie_Brain_Engine` 폴더를 자동으로 찾습니다
- 예: `ADHD_Simulation_Engine/../Cookiie_Brain_Engine/`

### 3. 실행 예시

#### PTSD 시뮬레이션 실행
```bash
# 방법 1: 직접 실행
python run_ptsd_simulation.py

# 방법 2: 모듈로 실행
python -m brain_disorder_simulation.disorders.ptsd.ptsd_simulator
```

#### 연구 모듈 테스트
```bash
python test_research_modules.py
```

#### Python 코드에서 사용
```python
# PTSD 시뮬레이션
from brain_disorder_simulation.disorders.ptsd import PTSDSimulator
simulator = PTSDSimulator(trauma_intensity=0.8, suppression_failure=0.6)
results = simulator.simulate_full_ptsd_assessment()

# 우울증 시뮬레이션
from brain_disorder_simulation.disorders.depression import DepressionSimulator
simulator = DepressionSimulator(initial_energy=30.0)
results = simulator.simulate_full_depression_assessment()

# 통합 시뮬레이터
from brain_disorder_simulation.unified import UnifiedDisorderSimulator
simulator = UnifiedDisorderSimulator(seed=42)
results = simulator.simulate_depression(...)
results = simulator.simulate_ptsd(...)
```

---

## 다음 작업 계획

### 우선순위 1: 루프 라이브러리 정식 모듈화 ⚠️ **현재 작업 중단 지점**

#### 작업 내용
- **위치**: `brain_disorder_simulation/common/loops/`
- **목적**: 공통 동역학 루프를 추상화하여 재사용 가능한 모듈로 만들기

#### 구현할 루프 모듈
1. **NegativeBiasLoop** (부정적 편향 루프)
   - 우울증, PTSD에서 공통 사용
   - 부정적 편향 강화 메커니즘

2. **HyperarousalLoop** (과각성 루프)
   - PTSD, 불안장애에서 공통 사용
   - 과각성 상태 유지 메커니즘

3. **ControlFailureLoop** (제어 실패 루프)
   - 우울증, ADHD에서 공통 사용
   - 인지 제어 실패 메커니즘

4. **EnergyCollapseLoop** (에너지 붕괴 루프)
   - 우울증에서 사용
   - 에너지 시스템 붕괴 메커니즘

#### 작업 단계
1. `common/loops/` 디렉토리 구조 설계
2. 각 루프를 독립적인 클래스로 구현
3. 기존 엔진을 루프 라이브러리 기반으로 리팩터링
4. `UnifiedDisorderSimulator`에 루프 조합 기능 추가
5. 루프 다이어그램 자동 생성 기능 추가

#### 예상 파일 구조
```
brain_disorder_simulation/common/loops/
├── __init__.py
├── base_loop.py              # 기본 루프 클래스
├── negative_bias_loop.py     # 부정적 편향 루프
├── hyperarousal_loop.py      # 과각성 루프
├── control_failure_loop.py    # 제어 실패 루프
└── energy_collapse_loop.py    # 에너지 붕괴 루프
```

### 우선순위 2: UnifiedDisorderSimulator 리포트 강화

#### 작업 내용
- `simulate_depression`, `simulate_ptsd` 결과에 대한 **"원인 루프 해석"** 리포트 추가
- 숫자 대신 **"어떤 루프들이 얼마나 활성화되었는지"** 텍스트 설명
- `explain_patterns()` 메서드 추가

### 우선순위 3: OCD 모듈 구현

#### 작업 내용
- **위치**: `brain_disorder_simulation/disorders/ocd/`
- 강박 사고 루프 + 강박 행동 루프 구현
- `OCDSimulator` 클래스 추가
- `UnifiedSimulator`에 `simulate_ocd()` 메서드 추가

### 우선순위 4: 문서 정리

#### 작업 내용
- `docs/` 디렉토리 내 문서들을 카테고리별로 정리
- 중복 문서 제거
- 핵심 문서만 메인 디렉토리에 유지

---

## 주의사항 및 제한사항

### ⚠️ 매우 중요한 안내

**이 소프트웨어는 의학적 진단 도구가 아닙니다.**

- ❌ **진단, 예측, 또는 치료 권고를 제공하지 않습니다.**
- ❌ **실제 의학적 진단 도구가 아닙니다.**
- ❌ **의료기기(SaMD)가 아닙니다.**
- ❌ **병원에서 환자 진단에 사용할 수 없습니다.**
- ✅ **연구 및 교육 목적으로만 사용되어야 합니다.**
- ✅ **인지 동역학의 계산적 시뮬레이션입니다.**
- ✅ **대학병원 연구실에서 시뮬레이션 도구로 사용 가능합니다.**

### 현재 버전의 정확한 위치

#### ✅ 사용 가능 (연구/교육 목적)
- 대학병원 연구실에서 시뮬레이션 도구로 사용
- 연구 및 교육 목적
- 알고리즘 개발 및 테스트
- 개념 검증
- 학술 논문 작성

#### ❌ 사용 불가능 (의료 목적)
- 의료기기/진단 보조 시스템
- 환자 데이터 연결 및 진단 보조
- 실제 의학적 진단 도구
- 치료 결정 보조
- 임상 의사결정

### 준비도
- **연구용/교육용**: ✅ 90-95% (사용 가능)
- **의료용 병원**: ❌ 25-30% (사용 불가능)

### 알려진 제한사항

1. **폐루프 동역학**
   - 기본 폐루프 동역학 구조는 구현됨 (연구용)
   - **임상급 폐루프 (실제 데이터 피드백)는 미구현**

2. **생체 데이터 통합**
   - fMRI, EEG, HRV 데이터는 **예측/매핑**만 가능
   - 실제 측정 데이터 통합은 미구현

3. **약물 효과 시뮬레이션**
   - 기본 PK/PD 모델 구조는 구현됨
   - 정밀한 약물 데이터 기반 모델은 미구현

4. **의료 표준 준수**
   - HL7 FHIR 매퍼는 구현됨 (기본 구조)
   - 실제 EMR 시스템 연동은 미구현

---

## 의존성 및 환경

### 필수 의존성

- **Python**: 3.8 이상
- **numpy**: >= 1.20.0
- **matplotlib**: >= 3.3.0
- **Cookiie Brain Engine**: 별도 설치 필요
  - 저장소: https://github.com/qquartsco-svg/cookiieBrain_alpha

### 선택적 의존성

- **scipy**: >= 1.7.0 (고급 수치 계산)
- **pandas**: >= 1.3.0 (데이터 분석)

### 환경 변수

- `COOKIIE_BRAIN_PATH`: Cookiie Brain Engine 경로 (선택사항)

### 설치 방법

```bash
# 저장소 클론
git clone https://github.com/qquartsco-svg/Brain_Disorder_Simulation_Engine.git
cd Brain_Disorder_Simulation_Engine

# 패키지 설치
pip install -e .

# 의존성 설치
pip install -r requirements.txt

# Cookiie Brain Engine 설치 (의존성)
# https://github.com/qquartsco-svg/cookiieBrain_alpha
```

---

## Git 및 버전 관리

### 저장소 정보
- **GitHub URL**: https://github.com/qquartsco-svg/Brain_Disorder_Simulation_Engine
- **현재 버전**: 1.0.0
- **라이선스**: MIT

### 블록체인 서명
- **PHAM 서명 파일**: `PHAM_BLOCKCHAIN_SIGNATURE.md`
- **작성자**: GNJz (Qquarts)
- **기여도**: 100% (초기 개발)
- **PHAM 규칙**: GNJz 기여도 제한 6% (향후 기여)

---

## 문제 해결 가이드

### 일반적인 문제

1. **Cookiie Brain Engine 경로 오류**
   - 환경 변수 `COOKIIE_BRAIN_PATH` 설정 확인
   - 또는 상위 디렉토리에 `Cookiie_Brain_Engine` 폴더 존재 확인

2. **Import 오류**
   - `pip install -e .` 실행 확인
   - Python 경로 확인

3. **한글 폰트 오류 (matplotlib)**
   - 시스템에 한글 폰트 설치 확인
   - 또는 `matplotlib` 설정에서 폰트 변경

### 디버깅 팁

1. **시뮬레이션 결과가 예상과 다를 때**
   - Seed 값 확인 (재현성)
   - 파라미터 설정 확인
   - 로그 출력 확인

2. **성능 문제**
   - Seed sweep 시 반복 횟수 줄이기
   - 메모리 사용량 확인

---

## 연락처 및 참고 자료

### 작성자
- **GNJz (Qquarts)**
- **GitHub**: @qquartsco-svg

### 참고 문서
- `README.md`: 프로젝트 개요 및 사용법
- `ENGINE_CAPABILITIES.md`: 엔진 활용 가능한 기능 설명
- `CHANGELOG.md`: 변경 이력
- `PHAM_BLOCKCHAIN_SIGNATURE.md`: 블록체인 서명
- `docs/`: 상세 문서 디렉토리

### Cookiie Brain Engine
- **저장소**: https://github.com/qquartsco-svg/cookiieBrain_alpha
- **문서**: Cookiie Brain Engine 문서 참조

---

## 작업 재개 시 체크리스트

### 즉시 확인할 사항
- [ ] 프로젝트 디렉토리 위치 확인
- [ ] Cookiie Brain Engine 경로 확인
- [ ] 가상환경 활성화 (사용하는 경우)
- [ ] 의존성 설치 확인 (`pip list`)

### 다음 작업 시작 전
- [ ] `common/loops/` 디렉토리 확인
- [ ] 기존 공통 엔진 파일 확인
- [ ] `UnifiedDisorderSimulator` 코드 리뷰
- [ ] 루프 라이브러리 설계 문서 작성 (선택사항)

### 작업 진행 순서
1. `common/loops/base_loop.py` 구현
2. 각 루프 모듈 구현 (NegativeBiasLoop, HyperarousalLoop 등)
3. 기존 엔진 리팩터링
4. `UnifiedDisorderSimulator` 통합
5. 테스트 및 검증

---

**작성 완료일**: 2025-01-27  
**작성자**: GNJz (Qquarts)  
**상태**: 작업 중단 (컴퓨터 재부팅 전 인수인계 완료)

---

**Qquarts co Present**


