# 프로젝트 구조 가이드

**작성일**: 2025-01-28  
**프로젝트**: Brain Disorder Simulation Engine

---

## 📁 메인 폴더 구조

### 1. **프로젝트 루트** (`/Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine/`)

프로젝트의 최상위 디렉토리입니다.

#### 주요 폴더

1. **`brain_disorder_simulation/`** ⭐ **핵심 메인 패키지**
   - 모든 시뮬레이션 엔진과 모듈이 들어있는 메인 패키지
   - 이 폴더가 프로젝트의 핵심입니다

2. **`adhd_simulation/`** (레거시/호환성)
   - 기존 ADHD 모듈 (호환성 유지용)
   - 새로운 코드는 `brain_disorder_simulation/` 사용 권장

3. **`docs/`**
   - 분석 문서, 배포 문서, 가이드 등

4. **`test_output/`**
   - 테스트 결과 파일들

---

## 🎯 핵심 메인 패키지: `brain_disorder_simulation/`

이 폴더가 **프로젝트의 핵심**입니다.

### 구조

```
brain_disorder_simulation/
├── __init__.py                    # 패키지 초기화
├── common/                        # 공통 엔진 (모든 질환에서 사용)
│   ├── negative_bias_engine.py   # 부정적 편향 엔진
│   ├── cognitive_control_engine.py # 인지 제어 엔진
│   ├── energy_depletion_engine.py  # 에너지 고갈 엔진
│   └── loops/                     # ⭐ 루프 라이브러리 (최신 추가)
│       ├── base_loop.py
│       ├── negative_bias_loop.py
│       ├── hyperarousal_loop.py
│       ├── control_failure_loop.py
│       └── energy_collapse_loop.py
│
├── disorders/                     # 질환별 시뮬레이터
│   ├── adhd/                      # ADHD 시뮬레이션
│   ├── depression/                # 우울증 시뮬레이션
│   ├── ptsd/                      # PTSD 시뮬레이션
│   ├── anxiety/                   # 불안장애 (구현 예정)
│   └── ocd/                       # 강박장애 (구현 예정)
│
├── unified/                       # ⭐ 통합 시뮬레이터 (메인 진입점)
│   └── unified_simulator.py       # UnifiedDisorderSimulator 클래스
│
├── research/                      # 연구 모듈
│   ├── clinical_scales.py         # 임상 스케일 매핑
│   ├── depression/                # 우울증 연구 도구
│   └── utils/                     # 통계 분석, 리포트 생성
│
├── medical/                       # 의료용 모듈 (Phase 1-3)
│   ├── input_validator.py
│   ├── audit_trail.py
│   └── ...
│
└── utils/                         # 유틸리티
    ├── reproducibility.py
    ├── statistics.py
    └── report_generator.py
```

---

## 📄 메인 파일 설명

### 1. **`brain_disorder_simulation/unified/unified_simulator.py`** ⭐⭐⭐
**가장 중요한 메인 파일**

- **역할**: 모든 뇌 질환을 통합하여 시뮬레이션하는 메인 클래스
- **클래스**: `UnifiedDisorderSimulator`
- **기능**:
  - 단일 질환 시뮬레이션 (우울증, PTSD 등)
  - 공존 질환 시뮬레이션
  - 루프 조합 분석
  - 패턴 해석 리포트 생성

**사용 예시**:
```python
from brain_disorder_simulation.unified import UnifiedDisorderSimulator

simulator = UnifiedDisorderSimulator(seed=42)
results = simulator.simulate_depression(...)
report = simulator.explain_patterns(results)
```

---

### 2. **`brain_disorder_simulation/common/loops/`** ⭐⭐
**최신 추가된 루프 라이브러리**

- **역할**: 공통 동역학 루프를 모듈화한 라이브러리
- **주요 파일**:
  - `base_loop.py`: 기본 루프 클래스
  - `negative_bias_loop.py`: 부정적 편향 루프
  - `control_failure_loop.py`: 제어 실패 루프
  - `energy_collapse_loop.py`: 에너지 붕괴 루프
  - `hyperarousal_loop.py`: 과각성 루프

**특징**: 
- 기존 엔진들이 내부적으로 이 루프를 사용하도록 리팩터링됨
- 재사용 가능한 모듈화된 구조

---

### 3. **`brain_disorder_simulation/common/`** ⭐⭐
**공통 엔진 (모든 질환에서 공통 사용)**

- `negative_bias_engine.py`: 부정적 편향 엔진 (우울증, PTSD에서 사용)
- `cognitive_control_engine.py`: 인지 제어 엔진 (우울증, ADHD에서 사용)
- `energy_depletion_engine.py`: 에너지 고갈 엔진 (우울증에서 사용)

**특징**: 
- 내부적으로 루프 라이브러리를 사용하도록 리팩터링됨
- 호환성 유지 (기존 인터페이스 그대로 사용 가능)

---

### 4. **`brain_disorder_simulation/disorders/`** ⭐
**질환별 시뮬레이터**

각 질환별로 독립적인 시뮬레이터가 있습니다:

- **`adhd/`**: ADHD 시뮬레이터
- **`depression/`**: 우울증 시뮬레이터
  - `depression_simulator.py`: 메인 시뮬레이터
  - `depression_tasks.py`: 특화 태스크
  - `motivation_engine.py`: 동기 엔진
- **`ptsd/`**: PTSD 시뮬레이터
  - `ptsd_simulator.py`: 메인 시뮬레이터
  - `ptsd_engines.py`: PTSD 특화 엔진들

---

### 5. **루트 디렉토리의 주요 파일**

#### 문서 파일
- **`README.md`**: 프로젝트 개요 및 사용법
- **`HANDOVER_DOCUMENT.md`**: 인수인계 문서 (24KB)
- **`ENGINE_CAPABILITIES.md`**: 엔진 기능 설명
- **`CHANGELOG.md`**: 변경 이력
- **`PROJECT_STATUS_REPORT.md`**: 프로젝트 상태 리포트

#### 설정 파일
- **`setup.py`**: 패키지 설정
- **`requirements.txt`**: 의존성 목록
- **`pyproject.toml`**: Python 프로젝트 설정

#### 실행 파일
- **`run_ptsd_simulation.py`**: PTSD 시뮬레이션 실행 스크립트
- **`cli.py`**: CLI 인터페이스
- **`test_loops.py`**: 루프 라이브러리 테스트
- **`test_refactored_engines.py`**: 리팩터링된 엔진 테스트

---

## 🚀 시작하기

### 가장 빠른 시작 방법

1. **통합 시뮬레이터 사용** (권장):
```python
from brain_disorder_simulation.unified import UnifiedDisorderSimulator

simulator = UnifiedDisorderSimulator(seed=42)
results = simulator.simulate_depression(
    negative_bias_strength=0.6,
    control_impairment=0.5,
    energy_depletion_rate=0.5,
    duration=300.0
)
```

2. **개별 질환 시뮬레이터 사용**:
```python
from brain_disorder_simulation.disorders.depression import DepressionSimulator

simulator = DepressionSimulator(initial_energy=30.0)
results = simulator.simulate_full_depression_assessment()
```

3. **루프 라이브러리 직접 사용**:
```python
from brain_disorder_simulation.common.loops import NegativeBiasLoop

loop = NegativeBiasLoop(initial_bias_strength=0.5)
result = loop.process_stimulus(stimulus_valence=-0.8, stimulus_intensity=1.0)
```

---

## 📊 파일 크기 및 중요도

### 매우 중요한 파일 (⭐⭐⭐)
- `brain_disorder_simulation/unified/unified_simulator.py` (28KB)
  - 통합 시뮬레이터 메인 클래스

### 중요한 파일 (⭐⭐)
- `brain_disorder_simulation/common/loops/` (전체 약 50KB)
  - 루프 라이브러리
- `brain_disorder_simulation/common/*_engine.py` (각 4-7KB)
  - 공통 엔진들

### 참고 파일 (⭐)
- `HANDOVER_DOCUMENT.md` (24KB) - 인수인계 문서
- `README.md` - 프로젝트 개요
- `docs/` - 상세 문서들

---

## 🔍 현재 작업 상태

### 완료된 작업 ✅
1. 루프 라이브러리 모듈화
2. 기존 엔진 리팩터링 (루프 기반)
3. UnifiedDisorderSimulator 루프 통합
4. 루프 기반 패턴 해석 기능

### 다음 작업 예정
1. 루프 다이어그램 자동 생성
2. 더 많은 질환에 루프 통합
3. 문서 정리

---

## 💡 핵심 개념

### 메인 진입점
- **`UnifiedDisorderSimulator`**: 모든 시뮬레이션의 통합 진입점

### 핵심 아키텍처
- **루프 라이브러리**: 공통 동역학 루프 모듈화
- **공통 엔진**: 루프를 사용하는 엔진들
- **질환별 시뮬레이터**: 각 질환 특화 시뮬레이터

### 데이터 흐름
```
UnifiedDisorderSimulator
  ↓
질환별 시뮬레이터 (depression, ptsd, etc.)
  ↓
공통 엔진 (negative_bias, cognitive_control, etc.)
  ↓
루프 라이브러리 (loops/)
```

---

**작성 완료일**: 2025-01-28

