# 시뮬레이션 아키텍처 설계 분석

**작성일**: 2025-01-XX  
**목적**: 질환별 시뮬레이션 구조 결정 (분리 vs 통합)

---

## 🤔 핵심 질문

1. **우울증과 불안장애를 분리해야 하는가, 통합해야 하는가?**
2. **각 질환을 따로 만들어야 하는가, 통합 시뮬레이션으로 가야 하는가?**
3. **다른 질환들도 같은 방식으로 시뮬레이션 가능한가?**

---

## 📊 접근법 비교

### 1️⃣ 완전 분리 접근법 (Separate Simulators)

```
ADHD_Simulator
Depression_Simulator
Anxiety_Simulator
OCD_Simulator
...
```

**장점:**
- ✅ 각 질환의 특정 메커니즘에 집중
- ✅ 명확한 경계
- ✅ 독립적 테스트 가능
- ✅ 단순한 구조

**단점:**
- ❌ 코드 중복 (공통 메커니즘 반복)
- ❌ 공존(co-morbidity) 시뮬레이션 불가
- ❌ 확장성 낮음 (새 질환마다 새 시뮬레이터)
- ❌ 실제 상황과 거리감

---

### 2️⃣ 완전 통합 접근법 (Unified Simulator)

```
UnifiedDisorderSimulator
  - disorder_type: 'depression' | 'anxiety' | 'adhd' | ...
  - 모든 메커니즘을 하나의 시뮬레이터에 통합
```

**장점:**
- ✅ 공존 시뮬레이션 가능
- ✅ 코드 중복 최소화
- ✅ 실제 상황 반영

**단점:**
- ❌ 복잡한 구조
- ❌ 질환별 특화 어려움
- ❌ 유지보수 어려움

---

### 3️⃣ 모듈화 통합 접근법 (Modular Unified) ⭐ **권장**

```
BaseDisorderSimulator (공통 기반)
  ├── 공통 엔진 (재사용 가능)
  │   ├── NegativeBiasEngine (우울증, 불안장애 공통)
  │   ├── CognitiveControlEngine (대부분 질환 공통)
  │   └── EnergyDepletionEngine (우울증, 불안장애 공통)
  │
  ├── 질환별 특화 엔진
  │   ├── AnxietyThreatEngine (불안장애 전용)
  │   ├── OCDLoopEngine (강박장애 전용)
  │   └── ADHDAttentionEngine (ADHD 전용)
  │
  └── 통합 시뮬레이터
      ├── simulate_depression()
      ├── simulate_anxiety()
      ├── simulate_comorbidity() (공존 시뮬레이션)
      └── simulate_custom() (사용자 정의 조합)
```

**장점:**
- ✅ **코드 재사용**: 공통 메커니즘 공유
- ✅ **공존 시뮬레이션**: 실제 상황 반영
- ✅ **확장성**: 새 질환 추가 용이
- ✅ **유연성**: 질환별 특화 + 통합 가능
- ✅ **Cookiie Brain Engine 구조와 일치**: 모듈화 철학

**단점:**
- ⚠️ 초기 설계 복잡도 (하지만 장기적으로 유리)

---

## 🔬 실제 상황 분석

### 공존(Co-morbidity) 현실

**우울증 + 불안장애 공존률:**
- 약 50-60%의 우울증 환자가 불안장애도 경험
- 약 50%의 불안장애 환자가 우울증도 경험

**공통 메커니즘:**
- **Amygdala**: 둘 다 과활성화
- **Prefrontal Cortex**: 둘 다 억제 제어 약화
- **Hypothalamus**: 둘 다 스트레스 반응 이상
- **Thalamus**: 불안장애는 필터링 실패, 우울증은 간접적 영향

**차이점:**
- **불안장애**: 위협 감지 과민, 걱정 루프, 과각성
- **우울증**: 부정적 편향, 에너지 고갈, 동기 감소

---

## 🏗️ 권장 아키텍처: 모듈화 통합 접근법

### 구조 설계

```
adhd_simulation/
  ├── core/
  │   ├── base_simulator.py          # 공통 기반 시뮬레이터
  │   ├── common_engines.py          # 공통 엔진 (재사용)
  │   │   ├── NegativeBiasEngine
  │   │   ├── CognitiveControlEngine
  │   │   └── EnergyDepletionEngine
  │   │
  │   ├── disorder_specific/         # 질환별 특화
  │   │   ├── depression_engines.py
  │   │   │   └── MotivationEngine (우울증 전용)
  │   │   ├── anxiety_engines.py
  │   │   │   ├── ThreatDetectionEngine (불안장애 전용)
  │   │   │   └── WorryLoopEngine (불안장애 전용)
  │   │   └── adhd_engines.py
  │   │       └── AttentionControlEngine (ADHD 전용)
  │   │
  │   └── unified_simulator.py      # 통합 시뮬레이터
  │       ├── simulate_depression()
  │       ├── simulate_anxiety()
  │       ├── simulate_comorbidity()
  │       └── simulate_custom()
```

### 사용 예시

```python
from adhd_simulation.core.unified_simulator import UnifiedDisorderSimulator

# 1. 단일 질환 시뮬레이션
simulator = UnifiedDisorderSimulator()

# 우울증만
results_depression = simulator.simulate_depression(
    negative_bias_strength=0.6,
    duration=300.0
)

# 불안장애만
results_anxiety = simulator.simulate_anxiety(
    threat_sensitivity=0.7,
    duration=300.0
)

# 2. 공존 시뮬레이션 (실제 상황)
results_comorbidity = simulator.simulate_comorbidity(
    disorders=['depression', 'anxiety'],
    depression_params={'negative_bias_strength': 0.5},
    anxiety_params={'threat_sensitivity': 0.6},
    duration=300.0
)

# 3. 사용자 정의 조합
results_custom = simulator.simulate_custom(
    active_engines={
        'negative_bias': {'strength': 0.4},
        'threat_detection': {'sensitivity': 0.5},
        'cognitive_control': {'impairment': 0.3}
    },
    duration=300.0
)
```

---

## ✅ 결론 및 권장사항

### 1. 아키텍처 선택: **모듈화 통합 접근법**

**이유:**
1. **실제 상황 반영**: 공존 시뮬레이션 가능
2. **코드 효율성**: 공통 메커니즘 재사용
3. **확장성**: 새 질환 추가 용이
4. **Cookiie Brain Engine 철학과 일치**: 모듈화 구조

### 2. 구현 전략

**Phase 1: 공통 엔진 추출**
- `NegativeBiasEngine` → `common_engines.py`
- `CognitiveControlEngine` → `common_engines.py`
- `EnergyDepletionEngine` → `common_engines.py`

**Phase 2: 질환별 특화 엔진**
- 우울증: `MotivationEngine` (depression_engines.py)
- 불안장애: `ThreatDetectionEngine`, `WorryLoopEngine` (anxiety_engines.py)

**Phase 3: 통합 시뮬레이터**
- `UnifiedDisorderSimulator` 구현
- 단일/공존/커스텀 시뮬레이션 지원

### 3. 질문에 대한 답변

**Q: 우울증과 불안장애를 나눠야 하는가?**
- **A**: 엔진은 분리, 시뮬레이터는 통합
  - 공통 엔진: 재사용
  - 특화 엔진: 질환별 분리
  - 시뮬레이터: 통합하여 공존 시뮬레이션 가능

**Q: 다른 질환도 같은 방식으로 시뮬레이션 가능한가?**
- **A**: 네, 모듈화 구조 덕분에 가능
  - 공통 엔진 재사용
  - 질환별 특화 엔진 추가
  - 통합 시뮬레이터에서 조합

**Q: 따로따로 만들어야 하는가?**
- **A**: 아니요, 통합 구조 권장
  - 공통 기반 시뮬레이터
  - 질환별 특화 엔진 추가
  - 통합 시뮬레이터로 조합

---

## 🎯 최종 권장 구조

```
UnifiedDisorderSimulator (통합 시뮬레이터)
  ├── 공통 엔진 (재사용)
  │   ├── NegativeBiasEngine
  │   ├── CognitiveControlEngine
  │   └── EnergyDepletionEngine
  │
  ├── 질환별 특화 엔진 (필요시 추가)
  │   ├── MotivationEngine (우울증)
  │   ├── ThreatDetectionEngine (불안장애)
  │   └── WorryLoopEngine (불안장애)
  │
  └── 시뮬레이션 메서드
      ├── simulate_depression()      # 단일 질환
      ├── simulate_anxiety()         # 단일 질환
      ├── simulate_comorbidity()     # 공존
      └── simulate_custom()          # 커스텀 조합
```

**핵심 철학:**
> "공통은 공유하고, 특화는 분리하며, 시뮬레이션은 통합한다"

---

**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0  
**최종 업데이트**: 2025-01-XX

