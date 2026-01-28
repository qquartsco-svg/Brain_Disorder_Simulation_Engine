# 릴리스 노트 v1.0.0

**릴리스 일자**: 2025-01-28  
**버전**: 1.0.0  
**코드명**: "Research-Ready Release"  
**작성자**: GNJz (Qquarts)

---

## 🎉 첫 공식 릴리스

Brain Disorder Simulation Engine의 첫 공식 릴리스입니다. 이 버전은 연구 및 교육 목적으로 사용할 수 있는 안정적인 시뮬레이션 플랫폼을 제공합니다.

---

## ✨ 주요 기능

### 1. 통합 시뮬레이터
- **UnifiedDisorderSimulator**: 모든 뇌 질환을 통합하여 시뮬레이션하는 메인 클래스
- 단일 질환 시뮬레이션 (우울증, PTSD 등)
- 공존 질환(co-morbidity) 시뮬레이션
- 커스텀 조합 시뮬레이션

### 2. 루프 라이브러리 (신규)
- **모듈화된 동역학 루프 시스템**
- `NegativeBiasLoop`: 부정적 편향 루프
- `HyperarousalLoop`: 과각성 루프
- `ControlFailureLoop`: 제어 실패 루프
- `EnergyCollapseLoop`: 에너지 붕괴 루프
- 재사용 가능한 구조로 설계

### 3. 질환별 시뮬레이터
- ✅ **ADHD**: 주의력 결핍, 충동성, 과잉행동
- ✅ **우울증**: 에너지 붕괴, 동기 루프 단절, 부정적 편향
- ✅ **PTSD**: 외상 기억 침입, 회피, 과각성, 부정적 인지 변화
- ⏳ **불안장애**: 구현 예정
- ⏳ **강박장애**: 구현 예정

### 4. 연구 모듈
- 임상 스케일 매핑 (HAM-D, BDI, PHQ-9)
- 신경전달물질 시스템 (도파민, 세로토닌, 노르에피네프린)
- 생체지표 매핑 (fMRI, EEG, HRV)
- 통계 분석 도구
- 리포트 생성 기능

### 5. 루프 기반 패턴 해석
- `explain_patterns()`: 루프 기반 패턴 해석 리포트
- 활성화된 루프 분석
- 루프 간 상호작용 설명
- 패턴별 메커니즘 해석

---

## 🔧 기술적 개선사항

### 아키텍처 개선
- **루프 라이브러리 모듈화**: 공통 동역학 루프를 재사용 가능한 모듈로 추상화
- **엔진 리팩터링**: 기존 엔진을 루프 라이브러리 기반으로 리팩터링
- **호환성 유지**: 기존 인터페이스 유지하면서 내부 구조 개선

### 코드 품질
- 53개 Python 파일, 문법 오류 없음
- 모든 핵심 모듈 정상 import 확인
- 통합 테스트 통과

---

## 📚 문서

### 완비된 문서
- **README.md** (31KB): 프로젝트 개요, 설치 방법, 사용 예시
- **HANDOVER_DOCUMENT.md** (24KB): 상세 인수인계 문서
- **ENGINE_CAPABILITIES.md**: 엔진 기능 설명
- **PROJECT_STRUCTURE_GUIDE.md**: 프로젝트 구조 가이드
- **DEPLOYMENT_READINESS_CHECK.md**: 배포 가능성 체크리스트
- **LEGAL_DISCLAIMER.md**: 법적 고지사항

---

## ⚠️ 중요 안내

### 사용 목적
- ✅ **연구 및 교육 목적으로만 사용**
- ❌ **의학적 진단 도구 아님**
- ❌ **의료기기(SaMD) 아님**
- ❌ **병원 진단에 사용 불가**

### 의존성
- **Cookiie Brain Engine** 필수 설치 필요
- 별도의 연구용 계산 모델 (본 패키지의 일부 아님)
- 설치 방법: [Cookiie Brain Engine 저장소](https://github.com/qquartsco-svg/cookiieBrain_alpha)

---

## 📊 통계

- **Python 파일**: 53개
- **총 코드 라인**: 약 15,000줄 이상
- **문서**: 8개 주요 문서
- **테스트**: 기본 기능 테스트 포함

---

## 🚀 시작하기

### 설치
```bash
# 1. Cookiie Brain Engine 설치 (필수)
# https://github.com/qquartsco-svg/cookiieBrain_alpha

# 2. 저장소 클론
git clone https://github.com/qquartsco-svg/Brain_Disorder_Simulation_Engine.git
cd Brain_Disorder_Simulation_Engine

# 3. 패키지 설치
pip install -e .
pip install -r requirements.txt
```

### 사용 예시
```python
from brain_disorder_simulation.unified import UnifiedDisorderSimulator

simulator = UnifiedDisorderSimulator(seed=42)
results = simulator.simulate_depression(
    negative_bias_strength=0.6,
    control_impairment=0.5,
    energy_depletion_rate=0.5,
    duration=300.0
)

# 루프 기반 패턴 해석
report = simulator.explain_patterns(results)
print(report)
```

---

## 🔮 향후 계획

### v1.1.0 (예정)
- 불안장애 모듈 구현
- 강박장애 모듈 구현
- 루프 다이어그램 자동 생성

### v1.2.0 (예정)
- 더 많은 질환 모듈 추가
- 치료 개입 시뮬레이션
- 고급 통계 분석 도구

---

## 🙏 감사의 말

이 프로젝트는 Cookiie Brain Engine의 동역학적 상호작용을 활용하여 구현되었습니다.

---

## 📝 변경 이력

자세한 변경 이력은 [CHANGELOG.md](CHANGELOG.md)를 참고하세요.

---

**Qquarts co Present**

