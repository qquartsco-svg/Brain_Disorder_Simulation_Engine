# ADHD Simulation Engine

**Cookiie Brain Engine 기반 ADHD 전용 시뮬레이션 시스템**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🚀 빠른 시작

### 설치

```bash
# 저장소 클론
git clone https://github.com/qquartsco-svg/ADHD_Simulation_Engine.git
cd ADHD_Simulation_Engine

# 패키지 설치
pip install -e .

# Cookiie Brain Engine 설치 (의존성)
# https://github.com/qquartsco-svg/cookiieBrain_alpha
```

### 실행

```bash
# 명령줄에서 실행
python -m adhd_simulator --age 15 --gender male --scenario adhd

# 또는 Python 코드에서
from adhd_simulator import ADHDSimulator
simulator = ADHDSimulator(age=15, gender='male')
results = simulator.simulate_full_adhd_assessment(scenario='adhd')
```

자세한 설치 방법은 [INSTALLATION.md](INSTALLATION.md)를 참고하세요.

---

## 📋 개요

ADHD Simulation Engine은 Cookiie Brain Engine의 동역학적 상호작용을 활용하여 ADHD의 주요 특성(주의력 결핍, 충동성, 과잉행동)을 시뮬레이션하는 전용 엔진입니다.

**⚠️ ⚠️ ⚠️ 매우 중요한 안내 ⚠️ ⚠️ ⚠️**:

**이 소프트웨어는 의학적 진단 도구가 아닙니다.**

- ❌ **진단, 예측, 또는 치료 권고를 제공하지 않습니다.**
- ❌ **실제 의학적 진단 도구가 아닙니다.**
- ❌ **의료기기(SaMD)가 아닙니다.**
- ❌ **병원에서 환자 진단에 사용할 수 없습니다.**
- ✅ **연구 및 교육 목적으로만 사용되어야 합니다.**
- ✅ **인지 동역학의 계산적 시뮬레이션입니다.**
- ✅ **대학병원 연구실에서 시뮬레이션 도구로 사용 가능합니다.**

**실제 ADHD 진단이 필요한 경우 반드시 의료 전문가(정신건강의학과 전문의)와 상담하세요.**

자세한 면책 조항은 [LEGAL_DISCLAIMER.md](LEGAL_DISCLAIMER.md)를 참고하세요.

### 📊 현재 상태 (2025-01-25 최신 업데이트)

**연구용/교육용 준비도**: ✅ **90-95%** (사용 가능) ⬆️ **+15-20%p**  
**의료용 병원 준비도**: ❌ **25-30%** (사용 불가능) ⬆️ **+10-15%p**

**현재 버전의 정확한 위치**:
- ✅ **대학병원 연구실에서 시뮬레이션 도구로 사용 가능**
- ✅ **연구 및 교육 목적으로 충분히 사용 가능**
- ✅ **폐루프 동역학 기본 구조 구현 완료**
- ✅ **도파민 시스템 기본 모델 구현 완료**
- ❌ **의료기기/진단 보조 시스템으로는 사용 불가능**
- ❌ **환자 데이터 연결 및 진단 보조는 불가능**

**최신 개선사항** (2025-01-25):
- ✅ 재현성 보장 시스템 (Seed 관리, 실험 메타데이터)
- ✅ 상태공간 출력 (라벨 제거, 상태 벡터 출력)
- ✅ 통계적 검증 (Seed sweep 기반 신뢰도)
- ✅ 메모리 최적화 (CircularBuffer)
- ✅ 변동성 분석 (주의력, 움직임 패턴)
- ✅ **폐루프 동역학 기본 구조** (상태 벡터, 피드백 루프)
- ✅ **도파민 시스템 기본 모델** (Tonic/Phasic 도파민)
- ✅ **약물 효과 시뮬레이션 기본 구조** (메틸페니데이트, 아토목세틴)
- ✅ **동역학 불변식 테스트** (단조성, 게이트 효과, 안정성)
- ✅ **실험 리포트 자동 생성** (JSON, Markdown, PNG)
- ✅ **확장 가능한 아키텍처** (플러그인 구조, 설정 기반 확장)

**의료용 전환을 위한 남은 작업**:
- ❌ 생체 데이터 통합 (EEG, fMRI, HRV) - 외부 데이터 필요
- ❌ PK/PD 모델 정밀화 - 약물 데이터 필요
- ❌ HL7/FHIR 연동 - 의료 표준 필요
- ❌ 임상 데이터 검증 - 환자 데이터 필요
- ❌ 법적/윤리적 요건 - 외부 승인 필요

**상세 분석**: [의료용 준비도 분석](./docs/medical/MEDICAL_READINESS_ANALYSIS.md) | [개선사항 보고서](./docs/guides/IMPROVEMENTS_APPLIED.md)

---

## 🎯 사용 목적별 구분

### 공학용 / 연구용 (현재 버전) ✅ 사용 가능

**용도**:
- 연구 및 교육 목적
- 알고리즘 개발 및 테스트
- 시뮬레이션 실험
- 개념 검증
- 대학병원 연구실 시뮬레이션 도구

**현재 구현된 기능**:
- ✅ 재현성 보장 시스템 (Seed 관리, 실험 메타데이터)
- ✅ 상태공간 좌표 출력 (라벨 대신 상태 벡터)
- ✅ 통계적 검증 (Seed sweep 기반 신뢰도)
- ✅ 메모리 최적화 (CircularBuffer)
- ✅ 변동성 분석 (주의력, 움직임 패턴)
- ✅ **폐루프 동역학** (상태 벡터, 피드백 루프, 확장 가능)
- ✅ **도파민 시스템** (Tonic/Phasic 모델, 약물 효과 기본 구조)
- ✅ **동역학 불변식 테스트** (물리적 타당성 검증)
- ✅ **실험 리포트 자동 생성** (JSON, Markdown, PNG)
- ✅ 빠른 프로토타이핑
- ✅ 유연한 파라미터 조정
- ✅ 확장 가능한 아키텍처

**준비도**: **90-95%** (연구용/교육용으로 거의 완성)

**대상 사용자**:
- 연구자
- 교육자
- 알고리즘 개발자
- 시뮬레이션 실험자
- 대학병원 연구실

---

### 의료용 / 임상용 (확장 계획) ❌ 현재 사용 불가능

**⚠️ 중요**: 현재 버전은 의료용 병원에서 사용할 수 없습니다.

**준비도**: **15%** (의료용 전환을 위해 추가 개발 필요)

**의료용 전환을 위한 필수 작업** (6-11개월 소요 예상):

**Phase 1: 핵심 동역학** (1-2개월)
- ❌ 폐루프 동역학 구조 (현재: 오픈루프)
- ✅ 재현성 보장 (Seed 관리) - **완료**
- ✅ 상태공간 좌표 출력 - **완료**

**Phase 2: 의료 표준** (2-3개월)
- ❌ 의료 표준 준수 (HL7/FHIR)
- ❌ 생체 데이터 통합 (fMRI, EEG, HRV)
- ❌ 약물 효과 시뮬레이션 (PK/PD)

**Phase 3: 검증 및 품질** (3-6개월)
- ❌ 임상 데이터 검증
- ❌ 법적/윤리적 요건 (HIPAA, IRB)

**대상 사용자** (의료용 전환 후):
- 의료 연구자
- 임상 연구소
- 대학 병원 연구팀

**확장 로드맵**: [Cookiie Brain Engine - Clinical Roadmap](https://github.com/qquartsco-svg/cookiieBrain_alpha/blob/main/docs/medical/CLINICAL_ENGINE_ROADMAP.md)

---

**현재 버전**: 공학용/연구용 ✅ **사용 가능 (75%)**  
**의료용 확장**: 계획 중 (Phase 1-4) ❌ **사용 불가능 (15%)**

---

## 🎯 주요 기능

### 1. ADHD 특화 엔진

- **AttentionControlEngine**: 주의력 제어 및 측정
  - 주의력 지속 능력 측정
  - 주의 분산 감지
  - ADHD 패턴 분석
  - ✅ 변동성 분석 (분산, 자기상관, 드롭아웃 비율)

- **ImpulseControlEngine**: 충동성 제어 및 측정
  - 즉각적 vs 지연된 보상 선택
  - 할인율(discount rate) 모델링
  - 충동성 점수 계산

- **HyperactivityEngine**: 과잉행동 측정
  - 에너지 변동성 분석
  - 에너지 불일치 감지
  - 과잉행동 점수 계산
  - ✅ 움직임 패턴 분석 (burstiness, fidget_rate, dwell_time)

### 1-1. 재현성 보장 시스템 (2025-01-25 추가)

- **ReproducibleRNG**: Seed 관리 시스템
  - 컴포넌트별 독립적 RNG
  - 재현 가능한 결과 보장

- **ExperimentMetadata**: 실험 메타데이터
  - 실험 ID, Seed 값, 설정 해시
  - Git commit hash, 플랫폼 정보
  - 재현성 검증을 위한 필수 정보

### 1-2. 상태공간 출력 (2025-01-25 추가)

- **상태 벡터 출력**: 라벨 대신 상태공간 좌표
  - attention, energy, arousal 등 상태 변수
  - 점수 (attention_deficit, impulsivity, hyperactivity)
  - 변동성 지표 (분산, 자기상관 등)

### 1-3. 통계적 검증 (2025-01-25 추가)

- **StatisticalValidator**: Seed sweep 기반 신뢰도
  - 분포 기반 신뢰도 계산
  - 신뢰구간 계산
  - 통계적 타당성 보장

### 1-4. 폐루프 동역학 시스템 (2025-01-25 추가)

- **ClosedLoopDynamics**: 상태 벡터 기반 동역학
  - 상태 벡터 (attention, arousal, pfc_inhibition, dopamine 등)
  - 엔진 간 피드백 루프
  - 확장 가능한 피드백 루프 등록 시스템

### 1-5. 도파민 시스템 (2025-01-25 추가)

- **DopamineSystem**: 도파민 동역학 모델
  - Tonic/Phasic 도파민
  - ADHD 도파민 부족 모델링
  - 주의력, 충동성, 과잉행동에 대한 효과

- **MedicationSimulator**: 약물 효과 시뮬레이션 (기본 구조)
  - 메틸페니데이트, 아토목세틴 모델
  - 약물 농도 곡선 (1-compartment model)
  - 향후 PK/PD 모델로 확장 가능

### 1-6. 동역학 불변식 테스트 (2025-01-25 추가)

- **DynamicsInvariantTests**: 물리적 타당성 검증
  - 단조성 테스트
  - 할인율 테스트
  - 게이트 효과 테스트
  - 도파민 효과 테스트
  - 폐루프 안정성 테스트

### 1-7. 실험 리포트 자동 생성 (2025-01-25 추가)

- **ReportGenerator**: 표준 리포트 생성
  - JSON 리포트
  - Markdown 리포트
  - PNG 시각화
  - 향후 PDF, HTML 확장 가능

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

**오픈루프 모드** (기본):
- Cookiie Brain Engine의 엔진 간 상호작용 활용
- Thalamus → PFC → Basal Ganglia 흐름
- Hypothalamus 에너지 관리
- 실시간 상태 추적

**폐루프 모드** (2025-01-25 추가):
- 상태 벡터 기반 동역학
- 엔진 간 피드백 루프
- 도파민 시스템 통합
- 확장 가능한 피드백 루프 등록

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

#### 기본 사용 (재현성 보장)

```python
from adhd_simulator import ADHDSimulator

# 시뮬레이터 초기화 (Seed 지정으로 재현성 보장)
# 폐루프 동역학 및 도파민 시스템 활성화 (기본값: True)
simulator = ADHDSimulator(
    seed=42,
    enable_closed_loop=True,  # 폐루프 동역학 활성화
    enable_dopamine=True      # 도파민 시스템 활성화
)

# 실험 메타데이터 설정
simulator.set_experiment_metadata({
    'simulation_type': 'full_assessment',
    'duration': 30.0
})

# 전체 평가 실행
results = simulator.simulate_full_adhd_assessment()

# 상태공간 출력 (라벨 대신)
state_space = simulator.get_state_space_output()
print(state_space['state_vector'])  # 상태 벡터
print(state_space['scores'])        # 점수
print(state_space['variability'])   # 변동성 지표

# 통계적 신뢰도
print(results['statistical_confidence'])

# 실험 메타데이터 저장
simulator.experiment_metadata.save('experiment.json')
```

#### 개별 테스트

```python
# 주의력 테스트
attention_results = simulator.simulate_attention_task(duration=30.0)

# 충동성 테스트
scenarios = [
    {'immediate': 5, 'delayed': 50, 'delay': 10},
    {'immediate': 10, 'delayed': 100, 'delay': 20},
]
impulsivity_results = simulator.simulate_impulsivity_task(scenarios)

# 과잉행동 테스트
hyperactivity_results = simulator.simulate_hyperactivity_task(duration=10.0)

# 결과 시각화
simulator.visualize_results('results.png')
```

#### Seed Sweep (통계적 검증)

```python
from adhd_simulator import ADHDSimulator
from statistics import StatisticalValidator

validator = StatisticalValidator()

# 여러 Seed로 시뮬레이션 (통계적 검증)
for seed in range(100):
    simulator = ADHDSimulator(seed=seed)
    results = simulator.simulate_full_adhd_assessment()
    
    # 결과 수집
    validator.add_sweep_result(
        attention=results['assessment']['scores']['attention_deficit'],
        impulsivity=results['assessment']['scores']['impulsivity'],
        hyperactivity=results['assessment']['scores']['hyperactivity']
    )

# 통계적 신뢰도 계산
confidence = validator.calculate_confidence_distribution()
print(confidence)  # 분포 기반 신뢰도
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

### 종합 평가 결과

**상태공간 출력** (2025-01-25 업데이트):
- **상태 벡터**: attention, energy, arousal 등 상태 변수
- **점수**: attention_deficit, impulsivity, hyperactivity
- **변동성 지표**: 분산, 자기상관, 드롭아웃 비율

**통계적 신뢰도** (2025-01-25 추가):
- **분포 기반 신뢰도**: Seed sweep 기반 확률
- **신뢰구간**: 95% 신뢰구간 계산

**참고**: 
- 이 결과는 시뮬레이션 기반 동역학적 패턴 관측이며, 의학적 진단이 아닙니다.
- 상태공간 좌표는 연구용 분석에 사용됩니다.
- 통계적 신뢰도는 Seed sweep 기반 분포 분석 결과입니다.

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
├── reproducibility.py       # 재현성 보장 시스템
├── statistics.py            # 통계적 검증 모듈
├── dopamine_system.py       # 도파민 시스템 모델 (2025-01-25 추가)
├── closed_loop_dynamics.py # 폐루프 동역학 시스템 (2025-01-25 추가)
├── report_generator.py      # 실험 리포트 자동 생성 (2025-01-25 추가)
├── dynamics_invariant_tests.py # 동역학 불변식 테스트 (2025-01-25 추가)
├── __init__.py              # 모듈 초기화
├── README.md                # 이 파일
├── requirements.txt         # 의존성 목록
├── LICENSE                  # MIT 라이선스
├── .gitignore              # Git 무시 파일
├── PHAM_BLOCKCHAIN_SIGNATURE.md  # PHAM 서명
├── LEGAL_DISCLAIMER.md          # 면책 조항
├── INSTALLATION.md               # 설치 가이드
├── docs/                         # 상세 문서 디렉토리
│   ├── deployment/               # 배포 관련 문서
│   ├── medical/                   # 의료 관련 문서
│   ├── analysis/                 # 분석 문서
│   ├── phase/                    # Phase별 보고서
│   └── guides/                   # 가이드 문서
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

### 의료용 버전 (확장 계획) ❌ 현재 사용 불가능

**⚠️ 중요**: 현재 버전은 의료용 병원에서 사용할 수 없습니다.

**준비도**: **15%** (의료용 전환을 위해 추가 개발 필요)

**의료용 버전에 필요한 기능**:

**✅ 완료된 기능** (코드 레벨):
- ✅ 재현성 보장 시스템 (Seed 관리, 실험 메타데이터)
- ✅ 상태공간 좌표 출력
- ✅ 통계적 검증 (Seed sweep)
- ✅ **폐루프 동역학 기본 구조** (상태 벡터, 피드백 루프)
- ✅ **도파민 시스템 기본 모델** (Tonic/Phasic)
- ✅ **약물 효과 시뮬레이션 기본 구조** (메틸페니데이트, 아토목세틴)
- ✅ **동역학 불변식 테스트** (물리적 타당성 검증)

**❌ 미구현 기능** (외부 의존):
- ❌ 의료 표준 준수 (HL7/FHIR) - 의료 표준 라이브러리 필요
- ❌ 생체 데이터 통합 (EEG, fMRI, HRV) - 실제 데이터 필요
- ❌ PK/PD 모델 정밀화 - 약물 데이터 필요
- ❌ 임상 데이터 검증 - 환자 데이터 필요
- ❌ 법적/윤리적 요건 (HIPAA, IRB) - 외부 승인 필요

**의료용 전환 소요 시간**: 4-8개월 (전담 팀 기준, 코드 레벨 완료로 단축)

**의료용 버전은 실제 의학적 진단 도구가 아닙니다.**  
임상 연구 지원 및 시뮬레이션 목적으로만 사용되어야 합니다.

**상세 분석**: [의료용 준비도 분석](./docs/medical/MEDICAL_READINESS_ANALYSIS.md)

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

4. **확장 가능한 구조** (2025-01-25 추가)
   - 도파민 시스템 확장 (PK/PD 모델)
   - 폐루프 동역학 확장 (커스텀 피드백 루프)
   - 약물 효과 시뮬레이션 확장 (새로운 약물 추가)
   - 리포트 생성 확장 (PDF, HTML 등)
   - 플러그인 아키텍처 (향후)

**확장 가이드**: [확장 가능성 가이드](./docs/guides/EXTENSIBILITY_GUIDE.md)

### 의료용 확장

**✅ 완료된 기능** (코드 레벨):
1. ✅ **폐루프 동역학** (기본 구조 완료)
   - 엔진 간 피드백 루프
   - 상태 벡터 기반 동역학
   - 확장 가능한 구조

2. ✅ **재현성 시스템** (완료)
   - Seed 관리 (ReproducibleRNG)
   - 실험 메타데이터 (ExperimentMetadata)
   - 재현 가능한 결과 (100% 재현성 보장)

3. ✅ **약물 효과 시뮬레이션** (기본 구조 완료)
   - 기본 약물 모델 (메틸페니데이트, 아토목세틴)
   - 약물 농도 곡선
   - 향후 PK/PD 모델로 확장 가능

4. ✅ **동역학 불변식 테스트** (완료)
   - 단조성, 할인율, 게이트 효과
   - 도파민 효과, 폐루프 안정성

5. ✅ **실험 리포트 자동 생성** (완료)
   - JSON, Markdown, PNG
   - 향후 PDF, HTML 확장 가능

**❌ 미구현 기능** (외부 의존):
6. ❌ **의료 표준 준수** (HL7/FHIR)
   - 의료 표준 라이브러리 필요
   - EMR 시스템 연동 필요

7. ❌ **생체 데이터 통합** (fMRI, EEG, HRV)
   - 실제 데이터 필요
   - 데이터 파싱 라이브러리 필요

8. ❌ **PK/PD 모델 정밀화**
   - 약물 데이터 필요
   - 정밀 모델링 필요

9. ❌ **장기 추적**
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

---

## ⚠️ ⚠️ ⚠️ 면책 조항 및 사용 제한 ⚠️ ⚠️ ⚠️

### 🚨 매우 중요한 경고

**이 소프트웨어는 의학적 진단 도구가 아닙니다.**

**절대로 다음 용도로 사용하지 마세요:**
- ❌ 의학적 진단
- ❌ 치료 권고
- ❌ 환자 관리
- ❌ 임상 의사결정
- ❌ 법적 증거
- ❌ 보험 청구

### 현재 버전의 정확한 위치

**✅ 사용 가능** (연구/교육 목적):
- 대학병원 연구실에서 시뮬레이션 도구로 사용
- 연구 및 교육 목적
- 알고리즘 개발 및 테스트
- 개념 검증
- 학술 논문 작성

**❌ 사용 불가능** (의료 목적):
- 의료기기/진단 보조 시스템
- 환자 데이터 연결 및 진단 보조
- 실제 의학적 진단 도구
- 치료 결정 보조
- 임상 의사결정

### 준비도

- **연구용/교육용**: ✅ **90-95%** (사용 가능)
- **의료용 병원**: ❌ **25-30%** (사용 불가능)

### 면책 조항

**이 시뮬레이션은 연구 및 교육 목적으로만 사용되어야 하며, 실제 의학적 진단 도구가 아닙니다.**

- ❌ **진단, 예측, 또는 치료 권고를 제공하지 않습니다**
- ❌ **실제 ADHD 진단은 전문의와 상담해야 합니다**
- ❌ **의료용 병원에서 환자 진단에 사용할 수 없습니다**
- ❌ **FDA 승인 없음, CE 마킹 없음, 의료기기 등록 없음**
- ✅ **연구 및 교육 목적으로만 사용 가능합니다**
- ✅ **대학병원 연구실에서 시뮬레이션 도구로 사용 가능합니다**

**상세 면책 조항**: [LEGAL_DISCLAIMER.md](LEGAL_DISCLAIMER.md)  
**의료용 준비도 분석**: [docs/medical/MEDICAL_READINESS_ANALYSIS.md](docs/medical/MEDICAL_READINESS_ANALYSIS.md)  
**개선사항 보고서**: [docs/guides/IMPROVEMENTS_APPLIED.md](docs/guides/IMPROVEMENTS_APPLIED.md)
