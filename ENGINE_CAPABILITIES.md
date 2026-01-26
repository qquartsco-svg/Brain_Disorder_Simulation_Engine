# Brain Disorder Simulation Engine - 활용 가능한 기능

**작성일**: 2025-01-26  
**버전**: 1.0.0  
**작성자**: GNJz (Qquarts)

---

## 🎯 현재 엔진으로 할 수 있는 것들

### 1️⃣ 뇌 질환 메커니즘 시뮬레이션

#### 우울증 시뮬레이션
- **에너지 시스템 붕괴 과정 관측**
  - 초기 에너지 고갈 → 동기 루프 단절 → 완전한 붕괴
  - 시간에 따른 에너지 변화 추적
  - 회복 메커니즘 억제 시뮬레이션

- **부정적 편향과 반추 패턴 재현**
  - 부정적 편향 강화 과정
  - 반추 루프 지속 메커니즘
  - 인지 제어 실패 과정

- **동기 시스템 붕괴**
  - 무쾌감증 (Anhedonia) 시뮬레이션
  - 보상 민감도 감소
  - 행동 억제 및 지연

#### ADHD 시뮬레이션
- **주의력 결핍 패턴 관측**
  - 주의력 변동성 분석
  - 방해 자극에 대한 취약성
  - 주의력 회복 메커니즘

- **충동성 및 과잉행동 분석**
  - 즉시 보상 선호 패턴
  - 행동 억제 실패
  - 에너지 과다 소비

#### 질환 간 비교
- 우울증 vs ADHD vs 정상 상태
- 공존 질환 (Comorbidity) 시뮬레이션
- 질환별 뇌 영역 활성화 패턴 비교

---

### 2️⃣ 생체지표 예측 및 매핑

#### fMRI 활성화 패턴 예측
- **뇌 영역별 활성화 수준**
  - PFC (전전두엽 피질) 활성화
  - Amygdala (편도체) 활성화
  - Hypothalamus (시상하부) 활성화
  - Basal Ganglia (선조체) 활성화

- **뇌 네트워크 활성화**
  - Default Mode Network (DMN)
  - Salience Network
  - Executive Network

#### EEG 파워 스펙트럼 예측
- **주파수 대역별 파워**
  - Alpha 파 (8-13 Hz)
  - Beta 파 (13-30 Hz)
  - Theta 파 (4-8 Hz)
  - Delta 파 (0.5-4 Hz)
  - Gamma 파 (30-100 Hz)

- **EEG 지표**
  - Theta/Beta 비율
  - Alpha 비대칭 (좌-우)

#### HRV (심박 변이도) 예측
- **HRV 지표**
  - RMSSD (부교감 신경 활성)
  - SDNN (전체 변이도)
  - LF/HF 비율
  - HF 파워, LF 파워

---

### 3️⃣ 임상 스케일 점수 생성

#### HAM-D (Hamilton Depression Rating Scale)
- 17개 항목 평가
- 총점 0-52점
- 심각도 해석 (정상, 경미, 중등도, 중증, 매우 중증)

#### BDI (Beck Depression Inventory)
- 21개 항목 평가
- 총점 0-63점
- 자가 보고식 특성 반영

#### PHQ-9 (Patient Health Questionnaire-9)
- 9개 항목 평가
- 총점 0-27점
- 선별 도구 특성 반영

**⚠️ 중요**: 모든 점수는 시뮬레이션 기반이며 임상 진단이 아닙니다.

---

### 4️⃣ 신경전달물질 시스템 분석

#### 도파민 시스템
- **Tonic Dopamine** (기본 도파민 수준)
- **Phasic Dopamine** (보상 반응)
- **Reward Sensitivity** (보상 민감도)
- 우울증 수준에 따른 변화 추적

#### 세로토닌 시스템
- **Serotonin Level** (세로토닌 수준)
- **SSRI 효과 시뮬레이션** (재흡수 억제)
- 우울증 수준에 따른 변화 추적

#### 노르에피네프린 시스템
- **Norepinephrine Level** (노르에피네프린 수준)
- **Arousal Level** (각성 수준)
- 스트레스 반응 모델링

---

### 5️⃣ 통계 분석 및 연구

#### Seed Sweep (다중 시뮬레이션)
- 100회 이상 반복 시뮬레이션
- 결과 분포 분석
- 통계적 신뢰도 확보
- 평균, 표준편차, 신뢰구간 계산

#### 그룹 비교 연구
- **t-test** (독립 표본)
- **ANOVA** (다중 그룹)
- **Cohen's d** (효과 크기)
- **95% 신뢰구간** 계산

#### 논문용 데이터 생성
- **Table 1, Table 2** (표 형식)
- **Figure 1, Figure 2** (그래프)
- **LaTeX 형식** 출력
- **CSV 형식** 출력

---

### 6️⃣ 검증 및 품질 관리

#### 생물학적 타당성 검증
- 뇌 영역 매핑 정확성
- 시간 스케일 일치 여부
- 에너지 대사 모델 검증
- 신경전달물질 시스템 검증

#### 임상적 관련성 검증
- DSM-5/ICD-11 기준 매핑
- 임상 스케일 통합 검증
- 증상 패턴 재현 검증
- 개인차 모델링 검증

#### 연구 재현성 검증
- Seed 관리 시스템
- 실험 메타데이터 추적
- 파라미터 문서화
- 결과 추적성 검증

---

## 💡 실제 활용 시나리오

### 시나리오 1: 우울증 연구 논문 작성

```python
# 1. 우울증 시뮬레이션 실행
from brain_disorder_simulation.disorders.depression.depression_simulator import DepressionSimulator

simulator = DepressionSimulator(initial_energy=30.0, recovery_inhibition=0.8)
results = simulator.simulate_full_depression_assessment()

# 2. 생체지표 추출
from research.depression.biomarkers import BiomarkerExtractor
extractor = BiomarkerExtractor()
biomarkers = extractor.extract_all_biomarkers(
    brain_state=results['brain_state'],
    energy_state=results['energy_state']
)

# 3. 임상 스케일 점수 생성
from research.clinical_scales import ClinicalScaleMapper
mapper = ClinicalScaleMapper()
scales = mapper.map_all_scales(results)

# 4. 통계 분석
from research.utils.statistical import StatisticalAnalyzer
analyzer = StatisticalAnalyzer()
# Seed Sweep 실행
sweep_results = analyzer.seed_sweep(DepressionSimulator, n_seeds=100)

# 5. 논문용 리포트 생성
from research.utils.reporting import ResearchReportGenerator
generator = ResearchReportGenerator()
report = generator.generate_full_report(
    normal_group=normal_results,
    depression_group=depression_results,
    comparison_results=comparison_results,
    metric_keys=['energy', 'motivation', 'negative_bias']
)
```

### 시나리오 2: 약물 효과 예측

```python
# 1. 우울증 상태 시뮬레이션
simulator = DepressionSimulator()
baseline_results = simulator.simulate_full_depression_assessment()

# 2. SSRI 투여 효과 시뮬레이션
from research.depression.neurotransmitters import NeurotransmitterSystem
nt_system = NeurotransmitterSystem()
nt_system.serotonin.apply_ssri(dose=0.5)  # SSRI 투여

# 3. 약물 투여 후 시뮬레이션
# (신경전달물질 시스템이 업데이트된 상태에서 재시뮬레이션)

# 4. 전후 비교
# 생체지표, 임상 스케일 점수, 통계 분석
```

### 시나리오 3: 질환 간 비교 연구

```python
# 1. 우울증 시뮬레이션
depression_results = depression_simulator.simulate()

# 2. ADHD 시뮬레이션
adhd_results = adhd_simulator.simulate()

# 3. 정상 상태 시뮬레이션
normal_results = normal_simulator.simulate()

# 4. 그룹 간 통계 비교
comparison = analyzer.compare_groups(
    normal_results, 
    depression_results, 
    'energy'
)

# 5. 뇌 영역 활성화 패턴 차이 분석
# fMRI, EEG, HRV 비교
```

### 시나리오 4: 교육 및 훈련

- 의과대학/심리학과 교육 자료
- 뇌 질환 메커니즘 시각화
- 연구자 훈련 시뮬레이션
- 임상 의사 결정 지원 (참고용)

---

## 📁 실행 가능한 파일들

### 주요 실행 파일

1. **연구 모듈 테스트**
   ```
   /Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/test_research_modules.py
   ```
   - 모든 연구 모듈 통합 테스트
   - 신경전달물질, 생체지표, 임상 스케일, 통계 분석, 검증

2. **우울증 시뮬레이션**
   ```
   /Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/run_depression_simulation.py
   ```
   - 우울증 메커니즘 시뮬레이션
   - 우울증 특화 태스크 실행
   - 결과 시각화

3. **통합 시뮬레이터**
   ```
   /Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/run_simulation.py
   ```
   - 다중 질환 시뮬레이션
   - 공존 질환 시뮬레이션

---

## ⚠️ 제한사항 및 주의사항

### ❌ 할 수 없는 것

- **실제 환자 진단**
  - 이 엔진은 진단 도구가 아닙니다
  - 실제 환자의 상태를 평가할 수 없습니다

- **실제 치료 계획 수립**
  - 치료 계획은 전문의의 판단이 필요합니다
  - 시뮬레이션 결과만으로 치료를 결정할 수 없습니다

- **실제 약물 처방 결정**
  - 약물 처방은 전문의의 판단이 필요합니다
  - 시뮬레이션은 참고용입니다

- **실제 생체지표 측정 대체**
  - fMRI, EEG, HRV는 실제 측정이 필요합니다
  - 시뮬레이션은 예측/추정일 뿐입니다

### ✅ 할 수 있는 것

- **연구용 시뮬레이션**
  - 메커니즘 분석
  - 가설 검증
  - 교육 및 훈련

- **논문 데이터 생성**
  - 통계 분석
  - 표/그래프 생성
  - 재현 가능한 실험

- **임상 연구 지원**
  - 생체지표 예측
  - 임상 스케일 점수 생성
  - 약물 효과 시뮬레이션

---

## 🎯 핵심 가치

이 엔진의 핵심 가치는:

1. **"왜 이런 상황이 발생하는가?" 원인 분석**
   - 단순 측정이 아닌 메커니즘 이해
   - 동역학적 과정 관측

2. **뇌 동역학 → 임상 언어로 번역**
   - 시뮬레이션 결과를 임상 전문가가 이해할 수 있는 언어로 변환
   - 생체지표, 임상 스케일 점수로 표현

3. **연구 재현성 확보**
   - Seed 관리
   - 메타데이터 추적
   - 완전한 문서화

4. **확장 가능한 플랫폼**
   - 새로운 질환 추가 용이
   - 새로운 분석 도구 추가 용이
   - 모듈화된 구조

---

## 📊 현재 구현 상태

### ✅ 완료된 기능 (100%)

- Phase 1: 구조 분리
- Phase 2-1: 신경전달물질 시스템
- Phase 2-2: 생체지표 매핑
- Phase 2-3: 통계 분석 도구
- Phase 3: 임상 스케일 통합
- Phase 4-1: 연구 논문용 데이터 생성
- Phase 4-2: 검증 및 문서화

### 📦 구현된 모듈

- `research/depression/neurotransmitters.py` - 신경전달물질 시스템
- `research/depression/biomarkers.py` - 생체지표 매핑
- `research/utils/statistical.py` - 통계 분석
- `research/clinical_scales.py` - 임상 스케일
- `research/utils/reporting.py` - 리포트 생성
- `research/depression/validation.py` - 검증 시스템

---

## 🚀 다음 단계 제안

1. **실제 우울증 시뮬레이터와 통합**
   - 연구 모듈을 실제 시뮬레이터에 통합
   - 전체 파이프라인 테스트

2. **다른 뇌 질환 확장**
   - 불안 장애
   - 강박 장애
   - 양극성 장애

3. **고급 분석 도구 추가**
   - 머신러닝 기반 패턴 분석
   - 시간 시리즈 분석
   - 네트워크 분석

---

**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0  
**최종 업데이트**: 2025-01-26

