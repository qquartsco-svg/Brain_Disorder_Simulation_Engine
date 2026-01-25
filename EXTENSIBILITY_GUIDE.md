# 확장 가능성 가이드

**작성일**: 2025-01-25  
**목적**: ADHD Simulation Engine의 확장 가능한 구조 설명

---

## 🎯 확장 가능한 아키텍처

### 현재 구조

```
ADHDSimulator
├── ReproducibleRNG (재현성)
├── DopamineSystem (도파민 모델) - 확장 가능
├── ClosedLoopDynamics (폐루프 동역학) - 확장 가능
├── MedicationSimulator (약물 효과) - 확장 가능
├── ADHD Engines (주의력, 충동성, 과잉행동)
└── ReportGenerator (리포트 생성) - 확장 가능
```

---

## 🔧 확장 포인트

### 1. 도파민 시스템 확장

**현재**: 기본 도파민 모델  
**확장 가능**: PK/PD 모델, 약물 효과 정밀화

```python
from dopamine_system import DopamineSystem

# 기본 사용
dopamine = DopamineSystem(rng=rng, adhd_deficit=0.3)

# 확장: 커스텀 도파민 모델
class CustomDopamineSystem(DopamineSystem):
    def update(self, reward_prediction_error, time_elapsed, external_boost):
        # 커스텀 로직
        return super().update(rpe, time, boost)
```

### 2. 폐루프 동역학 확장

**현재**: 기본 피드백 루프  
**확장 가능**: 커스텀 피드백 루프 등록

```python
from closed_loop_dynamics import ClosedLoopDynamics

# 기본 사용
dynamics = ClosedLoopDynamics(rng=rng)

# 확장: 커스텀 피드백 루프 등록
def custom_feedback_loop(state, dt):
    # 커스텀 로직
    state.attention += custom_calculation(state, dt)
    return state

dynamics.register_feedback_loop(custom_feedback_loop)
```

### 3. 약물 효과 시뮬레이션 확장

**현재**: 기본 약물 모델  
**확장 가능**: 새로운 약물 추가, PK/PD 정밀화

```python
from dopamine_system import MedicationSimulator

med_sim = MedicationSimulator(rng=rng)

# 새로운 약물 추가
med_sim.medications['new_medication'] = {
    'peak_time': 2.0,
    'half_life': 4.0,
    'dopamine_boost': 0.25,
    'attention_improvement': 0.35
}

# 약물 투여
med_sim.administer('new_medication', dose=10.0, time=0.0)
```

### 4. 리포트 생성 확장

**현재**: JSON, Markdown, PNG  
**확장 가능**: PDF, HTML, 커스텀 형식

```python
from report_generator import ReportGenerator

report_gen = ReportGenerator(output_dir='./reports')

# 기본 리포트
files = report_generator.generate_report(results, metadata)

# 확장: 커스텀 리포트
class CustomReportGenerator(ReportGenerator):
    def _generate_custom_format(self, results, filepath):
        # 커스텀 로직
        pass
```

### 5. ADHD 엔진 확장

**현재**: Attention, Impulse, Hyperactivity  
**확장 가능**: 새로운 엔진 추가

```python
from adhd_engines import AttentionControlEngine

# 기본 사용
attention_engine = AttentionControlEngine(rng=rng)

# 확장: 커스텀 엔진
class CustomAttentionEngine(AttentionControlEngine):
    def calculate_attention(self, task_importance, distractions, time_elapsed):
        # 커스텀 로직
        return super().calculate_attention(...)
```

---

## 📋 설정 기반 확장

### 시뮬레이터 초기화 옵션

```python
simulator = ADHDSimulator(
    config=config,
    seed=42,
    enable_closed_loop=True,  # 폐루프 동역학 활성화
    enable_dopamine=True      # 도파민 시스템 활성화
)
```

### 확장 가능한 설정

```python
# 향후 확장 가능한 설정 구조
simulator_config = {
    'dopamine': {
        'adhd_deficit': 0.3,
        'volatility': 0.2,
        'enable_medication': True
    },
    'closed_loop': {
        'enable_feedback': True,
        'feedback_strength': 0.5
    },
    'engines': {
        'attention': {'decay_rate': 0.02},
        'impulse': {'discount_rate': 0.5},
        'hyperactivity': {'volatility': 1.5}
    }
}
```

---

## 🔌 플러그인 아키텍처 (향후 확장)

### 플러그인 인터페이스

```python
from abc import ABC, abstractmethod

class ADHDPlugin(ABC):
    """ADHD 엔진 플러그인 인터페이스"""
    
    @abstractmethod
    def process(self, state: StateVector, input_data: Dict) -> Dict:
        """플러그인 처리"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """플러그인 이름"""
        pass

# 플러그인 등록
simulator.register_plugin(CustomPlugin())
```

---

## 📊 확장 가능성 체크리스트

### 현재 구현됨

- ✅ 도파민 시스템 (기본 모델)
- ✅ 폐루프 동역학 (기본 구조)
- ✅ 약물 효과 시뮬레이션 (기본 구조)
- ✅ 리포트 생성 (JSON, Markdown, PNG)
- ✅ 재현성 보장 (Seed 관리)
- ✅ 상태공간 출력

### 향후 확장 가능

- 🔄 PK/PD 모델 (약물 효과 정밀화)
- 🔄 생체 데이터 통합 (EEG, fMRI, HRV)
- 🔄 HL7/FHIR 연동 (의료 표준)
- 🔄 플러그인 아키텍처 (커스텀 엔진)
- 🔄 웹 API (RESTful API)
- 🔄 실시간 모니터링 (대시보드)

---

## 🎯 확장 예시

### 예시 1: 커스텀 도파민 모델

```python
from dopamine_system import DopamineSystem
import numpy as np

class AdvancedDopamineSystem(DopamineSystem):
    """고급 도파민 모델 (PK/PD 포함)"""
    
    def __init__(self, rng, adhd_deficit=0.3):
        super().__init__(rng, adhd_deficit)
        self.pharmacokinetics = {}  # PK 모델
    
    def update_with_pkpd(self, medication_concentration, time):
        """PK/PD 모델 기반 업데이트"""
        # 정밀한 약물 효과 계산
        pass
```

### 예시 2: 생체 데이터 통합

```python
class BiometricDataAdapter:
    """생체 데이터 어댑터 (향후 확장)"""
    
    def load_eeg(self, eeg_file):
        """EEG 데이터 로드"""
        pass
    
    def convert_to_state(self, eeg_data):
        """EEG → 상태 벡터 변환"""
        pass
```

### 예시 3: 커스텀 리포트

```python
from report_generator import ReportGenerator

class ClinicalReportGenerator(ReportGenerator):
    """임상 리포트 생성기 (향후 확장)"""
    
    def _generate_fhir_report(self, results, filepath):
        """FHIR 형식 리포트"""
        pass
```

---

## 📝 확장 가이드라인

### 1. 인터페이스 준수

- 기존 인터페이스를 유지하면서 확장
- 호환성 보장

### 2. 설정 기반 확장

- 하드코딩 지양
- 설정 파일로 제어

### 3. 테스트 가능성

- 확장 기능도 테스트 가능하도록
- 모킹 지원

### 4. 문서화

- 확장 기능 문서화
- 사용 예시 제공

---

**작성일**: 2025-01-25  
**작성자**: GNJz (Qquarts)

