# 루프 모듈화 로드맵 (Loop Modularization Roadmap)

**작성일**: 2025-01-28  
**목표**: 모든 엔진을 루프 라이브러리로 승격하여 "유니버설 루프 조합 시스템" 구축

---

## 📊 현재 상태

### ✅ 완료된 루프 (4개)
- `NegativeBiasLoop` - 부정적 편향 루프
- `HyperarousalLoop` - 과각성 루프
- `ControlFailureLoop` - 제어 실패 루프
- `EnergyCollapseLoop` - 에너지 붕괴 루프

### ⚠️ 아직 엔진 단위에 머물러 있는 것들

1. **MotivationEngine** → `MotivationCollapseLoop` ❌
2. **IntrusiveMemoryEngine** → `IntrusiveMemoryLoop` ❌
3. **AvoidanceEngine** → `AvoidanceReinforcementLoop` ❌
4. **ADHD 엔진 3종** → `AttentionInstabilityLoop`, `RewardPredictionErrorLoop` ❌

---

## 🎯 우선순위 제안

### Phase 1: 우울증 핵심 루프 (1주)
**우선순위: ⭐⭐⭐⭐⭐**

1. **MotivationCollapseLoop** (1순위)
   - **이유**: 
     - 우울증의 핵심 메커니즘
     - 이미 `EnergyCollapseLoop`, `NegativeBiasLoop` 완성 → 조합 가능
     - ADHD 보상 실패, PTSD 회피와도 연결 가능
   - **영향 범위**: 우울증, ADHD, PTSD
   - **예상 작업량**: 2-3일

### Phase 2: PTSD 핵심 루프 (1주)
**우선순위: ⭐⭐⭐⭐**

2. **IntrusiveMemoryLoop** (2순위)
   - **이유**:
     - PTSD의 핵심 메커니즘
     - 이미 `HyperarousalLoop` 완성 → 조합 가능
     - 우울증 반추, 불안장애 걱정과도 연결 가능
   - **영향 범위**: PTSD, 우울증, 불안장애
   - **예상 작업량**: 2-3일

3. **AvoidanceReinforcementLoop** (3순위)
   - **이유**:
     - `IntrusiveMemoryLoop`와 밀접하게 연관
     - 불안장애, OCD 회피와도 연결 가능
   - **영향 범위**: PTSD, 불안장애, OCD
   - **예상 작업량**: 2-3일

### Phase 3: ADHD 루프 (2주)
**우선순위: ⭐⭐⭐**

4. **AttentionInstabilityLoop** (4순위)
   - **이유**:
     - ADHD의 핵심 메커니즘
     - 복잡도가 높아서 나중에 처리
   - **영향 범위**: ADHD
   - **예상 작업량**: 3-4일

5. **RewardPredictionErrorLoop** (5순위)
   - **이유**:
     - `MotivationCollapseLoop`와 연결 가능
     - 복잡도가 높아서 나중에 처리
   - **영향 범위**: ADHD, 우울증
   - **예상 작업량**: 3-4일

---

## 📋 상세 설계

### 1. MotivationCollapseLoop 설계

**위치**: `brain_disorder_simulation/common/loops/motivation_collapse_loop.py`

**기존 엔진**: `brain_disorder_simulation/disorders/depression/motivation_engine.py`

**핵심 메커니즘**:
```
보상 민감도 감소 → 무쾌감증 → 동기 수준 저하 → 목표 지향 행동 감소 → 보상 기회 감소 → 보상 민감도 더 감소 (폐루프)
```

**상태 변수**:
- `reward_sensitivity`: 보상 민감도 (0.0 ~ 1.0)
- `motivation_level`: 동기 수준 (0.0 ~ 1.0)
- `anhedonia`: 무쾌감증 (0.0 ~ 1.0)
- `effort_cost`: 노력 비용 (1.0 ~ 2.5)
- `goal_directed_behavior`: 목표 지향 행동 (0.0 ~ 1.0)

**트리거 조건**:
- 보상 실패 (reward_value < threshold)
- 노력 비용 증가 (effort_required > threshold)
- 목표 달성 실패

**동역학**:
- 보상 민감도 감소 → 무쾌감증 증가 → 동기 수준 저하 → 목표 지향 행동 감소
- 루프 강도가 높을수록 보상 민감도가 더 빠르게 감소

**연결 가능한 루프**:
- `EnergyCollapseLoop`: 에너지 고갈 → 동기 저하
- `NegativeBiasLoop`: 부정적 편향 → 보상 기대 감소
- `ControlFailureLoop`: 제어 실패 → 목표 달성 실패

**사용 시나리오**:
- 우울증: 동기 붕괴
- ADHD: 보상 실패 → 동기 저하
- PTSD: 회피 → 보상 기회 감소 → 동기 저하

---

### 2. IntrusiveMemoryLoop 설계

**위치**: `brain_disorder_simulation/common/loops/intrusive_memory_loop.py`

**기존 엔진**: `brain_disorder_simulation/disorders/ptsd/ptsd_engines.py` (IntrusiveMemoryEngine)

**핵심 메커니즘**:
```
외상 기억 강화 → 억제 실패 → 침입 발생 → 공포 반응 → 기억 더 강화 → 억제 더 실패 (폐루프)
```

**상태 변수**:
- `memory_intensity`: 기억 강도 (0.0 ~ 1.0)
- `intrusion_frequency`: 침입 빈도 (0.0 ~ 1.0)
- `suppression_failure`: 억제 실패율 (0.0 ~ 1.0)
- `associated_fear`: 연관된 공포 수준 (0.0 ~ 1.0)

**트리거 조건**:
- 외상 기억 접촉
- 억제 시도 실패
- 유사 자극 노출

**동역학**:
- 기억 강화 → 억제 실패 → 침입 발생 → 공포 반응 → 기억 더 강화
- 루프 강도가 높을수록 억제 실패율이 증가

**연결 가능한 루프**:
- `HyperarousalLoop`: 침입 → 각성 증가
- `NegativeBiasLoop`: 침입 → 부정적 편향 강화
- `AvoidanceReinforcementLoop`: 침입 → 회피 강화

**사용 시나리오**:
- PTSD: 외상 기억 침입
- 우울증: 반추 (rumination)
- 불안장애: 걱정 (worry)

---

### 3. AvoidanceReinforcementLoop 설계

**위치**: `brain_disorder_simulation/common/loops/avoidance_reinforcement_loop.py`

**기존 엔진**: `brain_disorder_simulation/disorders/ptsd/ptsd_engines.py` (AvoidanceEngine)

**핵심 메커니즘**:
```
회피 학습 → 단기 불안 감소 → 회피 강화 → 노출 기회 감소 → 회피 더 강화 (폐루프)
```

**상태 변수**:
- `avoidance_strength`: 회피 강도 (0.0 ~ 1.0)
- `emotional_numbing`: 감정적 마비 (0.0 ~ 1.0)
- `generalization_factor`: 일반화 인자 (0.0 ~ 1.0)
- `avoided_stimuli_count`: 회피된 자극 수

**트리거 조건**:
- 공포 자극 접촉
- 회피 성공 (단기 불안 감소)
- 유사 자극 감지

**동역학**:
- 회피 학습 → 단기 불안 감소 → 회피 강화 → 노출 기회 감소 → 회피 더 강화
- 루프 강도가 높을수록 일반화 인자가 증가 (유사 자극도 회피)

**연결 가능한 루프**:
- `IntrusiveMemoryLoop`: 침입 → 회피 강화
- `HyperarousalLoop`: 각성 증가 → 회피 강화
- `MotivationCollapseLoop`: 회피 → 보상 기회 감소 → 동기 저하

**사용 시나리오**:
- PTSD: 외상 관련 자극 회피
- 불안장애: 위협 자극 회피
- OCD: 강박 자극 회피

---

## 🚀 구현 순서

### Step 1: MotivationCollapseLoop 구현
1. `base_loop.py` 기반으로 `MotivationCollapseLoop` 클래스 생성
2. `MotivationState` dataclass 정의
3. `_trigger_condition()`, `_update_dynamics()`, `_calculate_score()` 구현
4. `MotivationEngine` 리팩터링 (내부적으로 루프 사용)
5. `UnifiedDisorderSimulator`에 통합
6. 테스트 작성

### Step 2: IntrusiveMemoryLoop 구현
1. `base_loop.py` 기반으로 `IntrusiveMemoryLoop` 클래스 생성
2. `IntrusiveMemoryState` dataclass 정의
3. `_trigger_condition()`, `_update_dynamics()`, `_calculate_score()` 구현
4. `IntrusiveMemoryEngine` 리팩터링
5. `UnifiedDisorderSimulator`에 통합
6. 테스트 작성

### Step 3: AvoidanceReinforcementLoop 구현
1. `base_loop.py` 기반으로 `AvoidanceReinforcementLoop` 클래스 생성
2. `AvoidanceState` dataclass 정의
3. `_trigger_condition()`, `_update_dynamics()`, `_calculate_score()` 구현
4. `AvoidanceEngine` 리팩터링
5. `UnifiedDisorderSimulator`에 통합
6. 테스트 작성

---

## 📈 예상 효과

### 완료 후 상태
- **루프 라이브러리**: 7개 루프 (현재 4개 + 3개)
- **질환별 엔진**: 거의 사라지고 루프 조합으로 대체
- **통합 시뮬레이터**: 모든 질환을 루프 조합으로 시뮬레이션 가능

### 장점
1. **재사용성**: 한 루프를 여러 질환에서 사용
2. **조합 가능성**: 루프 간 상호작용 분석 가능
3. **확장성**: 새로운 질환 추가 시 기존 루프 조합으로 가능
4. **일관성**: 모든 질환이 동일한 루프 기반으로 시뮬레이션

---

## 📝 참고사항

- 각 루프는 `BaseLoop`를 상속받아 구현
- 기존 엔진은 호환성을 위해 유지하되, 내부적으로 루프 사용
- `UnifiedDisorderSimulator`에서 루프 조합 분석 가능
- 루프 간 상호작용은 `explain_patterns()`에서 분석

---

**작성자**: GNJz (Qquarts)  
**최종 업데이트**: 2025-01-28

