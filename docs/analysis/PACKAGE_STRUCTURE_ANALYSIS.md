# 뇌 질환 시뮬레이션 패키지 구조 분석

**작성일**: 2025-01-XX  
**목적**: 뇌 질환 시뮬레이션 패키지 구조 최적화

---

## 🤔 현재 상황 분석

### 현재 구조

```
ADHD_Simulation_Engine/
  ├── adhd_simulation/
  │   ├── core/
  │   │   ├── adhd_engines.py          # ADHD 전용
  │   │   ├── adhd_simulator.py        # ADHD 전용
  │   │   ├── depression_engines.py   # 우울증 전용
  │   │   └── depression_simulator.py # 우울증 전용
  │   ├── medical/
  │   └── utils/
```

**문제점:**
- ADHD와 우울증이 같은 패키지에 섞여 있음
- 패키지 이름이 "adhd_simulation"인데 우울증도 포함
- 확장 시 구조가 복잡해질 수 있음

---

## 💡 제안된 구조 분석

### 옵션 1: 별도 패키지 분리

```
00_BRAIN/
  ├── ADHD_Simulation_Engine/          # ADHD 전용
  │   └── adhd_simulation/
  │
  ├── Depression_Simulation_Engine/    # 우울증 전용
  │   └── depression_simulation/
  │
  ├── Anxiety_Simulation_Engine/       # 불안장애 전용
  │   └── anxiety_simulation/
  │
  └── Brain_Disorder_Simulation/       # 통합 패키지
      └── brain_disorder_simulation/
          ├── common/                  # 공통 엔진
          ├── disorders/               # 질환별 특화
          │   ├── adhd/
          │   ├── depression/
          │   └── anxiety/
          └── unified/                 # 통합 시뮬레이터
```

**장점:**
- ✅ 명확한 분리
- ✅ 독립적 관리 가능

**단점:**
- ❌ 코드 중복 (공통 엔진 반복)
- ❌ 공존 시뮬레이션 어려움
- ❌ 유지보수 복잡

---

### 옵션 2: 통합 패키지 (권장) ⭐

```
00_BRAIN/
  └── Brain_Disorder_Simulation_Engine/
      └── brain_disorder_simulation/
          ├── __init__.py
          │
          ├── common/                  # 공통 엔진 (재사용)
          │   ├── __init__.py
          │   ├── negative_bias_engine.py
          │   ├── cognitive_control_engine.py
          │   ├── energy_depletion_engine.py
          │   └── base_simulator.py
          │
          ├── disorders/               # 질환별 특화
          │   ├── __init__.py
          │   ├── adhd/
          │   │   ├── __init__.py
          │   │   ├── attention_engine.py
          │   │   ├── impulse_engine.py
          │   │   └── hyperactivity_engine.py
          │   ├── depression/
          │   │   ├── __init__.py
          │   │   └── motivation_engine.py
          │   └── anxiety/
          │       ├── __init__.py
          │       ├── threat_detection_engine.py
          │       └── worry_loop_engine.py
          │
          ├── unified/                 # 통합 시뮬레이터
          │   ├── __init__.py
          │   ├── unified_simulator.py
          │   └── comorbidity_simulator.py
          │
          ├── utils/                   # 유틸리티
          │   ├── reproducibility.py
          │   ├── statistics.py
          │   └── report_generator.py
          │
          └── medical/                 # 의료 관련
              ├── input_validator.py
              └── audit_trail.py
```

**장점:**
- ✅ 공통 엔진 재사용
- ✅ 공존 시뮬레이션 용이
- ✅ 확장성 높음
- ✅ 명확한 구조
- ✅ Cookiie Brain Engine과 일관성

**단점:**
- ⚠️ 초기 마이그레이션 필요

---

### 옵션 3: 하이브리드 (현재 + 확장)

```
ADHD_Simulation_Engine/                # 기존 유지
  └── adhd_simulation/
      └── core/
          ├── adhd_engines.py
          └── adhd_simulator.py

Brain_Disorder_Simulation_Engine/      # 새로 생성
  └── brain_disorder_simulation/
      ├── common/                      # 공통 엔진
      ├── disorders/                   # 질환별
      │   ├── adhd/                    # ADHD는 기존 참조
      │   ├── depression/
      │   └── anxiety/
      └── unified/                     # 통합
```

**장점:**
- ✅ 기존 코드 유지
- ✅ 점진적 확장

**단점:**
- ❌ 구조 일관성 부족
- ❌ 중복 가능성

---

## 🎯 최종 권장: 통합 패키지 (옵션 2)

### 이유

1. **실제 상황 반영**
   - 공존(co-morbidity) 시뮬레이션 필수
   - 통합 패키지가 자연스러움

2. **코드 효율성**
   - 공통 엔진 재사용
   - 중복 최소화

3. **확장성**
   - 새 질환 추가 용이
   - 모듈화 구조

4. **일관성**
   - Cookiie Brain Engine과 구조 일치
   - 명확한 네이밍

---

## 📁 권장 폴더 구조 (상세)

```
Brain_Disorder_Simulation_Engine/
  ├── README.md
  ├── LICENSE
  ├── requirements.txt
  ├── setup.py
  │
  ├── brain_disorder_simulation/
  │   ├── __init__.py
  │   │
  │   ├── common/                      # 공통 엔진
  │   │   ├── __init__.py
  │   │   ├── negative_bias_engine.py
  │   │   ├── cognitive_control_engine.py
  │   │   ├── energy_depletion_engine.py
  │   │   └── base_simulator.py
  │   │
  │   ├── disorders/                   # 질환별 특화
  │   │   ├── __init__.py
  │   │   │
  │   │   ├── adhd/
  │   │   │   ├── __init__.py
  │   │   │   ├── attention_engine.py
  │   │   │   ├── impulse_engine.py
  │   │   │   ├── hyperactivity_engine.py
  │   │   │   └── adhd_simulator.py
  │   │   │
  │   │   ├── depression/
  │   │   │   ├── __init__.py
  │   │   │   ├── motivation_engine.py
  │   │   │   └── depression_simulator.py
  │   │   │
  │   │   └── anxiety/
  │   │       ├── __init__.py
  │   │       ├── threat_detection_engine.py
  │   │       ├── worry_loop_engine.py
  │   │       └── anxiety_simulator.py
  │   │
  │   ├── unified/                     # 통합 시뮬레이터
  │   │   ├── __init__.py
  │   │   ├── unified_simulator.py     # 메인 통합 시뮬레이터
  │   │   └── comorbidity_simulator.py # 공존 시뮬레이터
  │   │
  │   ├── utils/                       # 유틸리티
  │   │   ├── __init__.py
  │   │   ├── reproducibility.py
  │   │   ├── statistics.py
  │   │   └── report_generator.py
  │   │
  │   └── medical/                     # 의료 관련
  │       ├── __init__.py
  │       ├── input_validator.py
  │       └── audit_trail.py
  │
  ├── docs/
  │   ├── analysis/
  │   ├── guides/
  │   └── medical/
  │
  └── tests/
      ├── test_common_engines.py
      ├── test_unified_simulator.py
      └── test_comorbidity.py
```

---

## 🔄 마이그레이션 전략

### Phase 1: 새 패키지 생성
1. `Brain_Disorder_Simulation_Engine/` 폴더 생성
2. 기본 구조 설정
3. 공통 엔진 이동/재구성

### Phase 2: 질환별 엔진 정리
1. ADHD 엔진 → `disorders/adhd/`
2. 우울증 엔진 → `disorders/depression/`
3. 불안장애 엔진 → `disorders/anxiety/`

### Phase 3: 통합 시뮬레이터 구현
1. `UnifiedSimulator` 구현
2. 공존 시뮬레이터 구현
3. 테스트 작성

### Phase 4: 기존 패키지 처리
- 옵션 A: 기존 `ADHD_Simulation_Engine` 유지 (레거시)
- 옵션 B: 기존 패키지를 새 패키지로 리다이렉트
- 옵션 C: 기존 패키지 제거 (완전 마이그레이션)

---

## ✅ 최종 결론

### 제안된 구조가 맞는가?

**네, 맞습니다!** ✅

**이유:**
1. ✅ 모듈화 통합 접근법과 일치
2. ✅ 공존 시뮬레이션 가능
3. ✅ 확장성 높음
4. ✅ 명확한 구조
5. ✅ Cookiie Brain Engine과 일관성

### 구현 순서

1. **새 패키지 생성**: `Brain_Disorder_Simulation_Engine/`
2. **공통 엔진 배치**: `common/` 폴더
3. **질환별 엔진 배치**: `disorders/` 폴더
4. **통합 시뮬레이터 구현**: `unified/` 폴더
5. **테스트 및 검증**

---

**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0  
**최종 업데이트**: 2025-01-XX

