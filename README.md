# ADHD Simulation Engine

**Cookiie Brain Engine 기반 ADHD 전용 시뮬레이션 시스템**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📋 개요

ADHD Simulation Engine은 Cookiie Brain Engine의 동역학적 상호작용을 활용하여 ADHD의 주요 특성(주의력 결핍, 충동성, 과잉행동)을 시뮬레이션하는 전용 엔진입니다.

**⚠️ 중요**: 이 시뮬레이션은 연구 및 교육 목적으로만 사용되어야 합니다. 실제 의학적 진단 도구가 아닙니다.

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
- **충동성 테스트**: 4가지 시나리오에서 즉각적 vs 지연된 보상 선택
- **과잉행동 테스트**: 10초간 에너지 변동성 측정

### 3. 동역학적 상호작용

- Cookiie Brain Engine의 엔진 간 상호작용 활용
- Thalamus → PFC → Basal Ganglia 흐름
- Hypothalamus 에너지 관리
- 실시간 상태 추적

---

## 🚀 빠른 시작

### 설치

```bash
# 저장소 클론
git clone https://github.com/qquartsco-svg/adhd_simulation_engine.git
cd adhd_simulation_engine

# 의존성 설치
pip install -r requirements.txt
```

### 기본 실행

```bash
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

### 종합 진단

- **ADHD 가능성 높음**: 3가지 특성 모두에서 ADHD 패턴 감지
- **주의력 결핍 가능성**: 주의력 결핍만 감지
- **충동성/과잉행동 가능성**: 충동성 또는 과잉행동만 감지
- **정상 범위**: ADHD 패턴 미감지

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
- 신뢰도
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
├── LICENSE                  # 라이선스
└── .gitignore              # Git 무시 파일
```

---

## 📦 의존성

- Python 3.8+
- numpy
- matplotlib
- Cookiie Brain Engine (의존성)

---

## 📝 사용 예시

### 전체 평가 실행

```python
from adhd_simulator import ADHDSimulator

simulator = ADHDSimulator()
results = simulator.simulate_full_adhd_assessment()

print(f"진단: {results['diagnosis']}")
print(f"신뢰도: {results['confidence']:.1f}%")
print(f"주의력 결핍: {results['attention_deficit']:.3f}")
print(f"충동성: {results['impulsivity']:.3f}")
print(f"과잉행동: {results['hyperactivity']:.3f}")
```

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

**이 시뮬레이션은 연구 및 교육 목적으로만 사용되어야 합니다.**

- ❌ 실제 의학적 진단 도구가 아닙니다
- ❌ 실제 ADHD 진단은 전문의와 상담해야 합니다
- ✅ 시뮬레이션 결과는 참고용입니다
- ✅ 연구 및 교육 목적으로 사용 가능합니다

---

## 🔬 확장 가능성

### 추가 가능한 기능

1. **개인화된 시뮬레이션**
   - 개인별 ADHD 특성 파라미터 조정
   - 맞춤형 테스트 시나리오

2. **개입 시뮬레이션**
   - 치료 효과 시뮬레이션
   - 개입 전후 비교

3. **장기 추적**
   - 장기간 ADHD 패턴 추적
   - 변화 추이 분석

4. **다양한 시나리오**
   - 학습 환경 시뮬레이션
   - 작업 환경 시뮬레이션
   - 사회적 상호작용 시뮬레이션

---

## 📚 참고 자료

- [Cookiie Brain Engine](https://github.com/qquartsco-svg/cookiieBrain_alpha): 기본 엔진
- ADHD 적용 분석 문서
- ADHD 확장 구조 문서

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
