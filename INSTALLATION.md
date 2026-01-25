# 📦 설치 가이드

ADHD Simulation Engine 설치 방법

---

## 🔧 사전 요구사항

- Python 3.8 이상
- Cookiie Brain Engine (의존성)

---

## 📥 설치 방법

### 방법 1: pip로 설치 (권장)

```bash
# 저장소 클론
git clone https://github.com/qquartsco-svg/ADHD_Simulation_Engine.git
cd ADHD_Simulation_Engine

# 패키지 설치
pip install -e .
```

### 방법 2: 개발 모드 설치

```bash
# 저장소 클론
git clone https://github.com/qquartsco-svg/ADHD_Simulation_Engine.git
cd ADHD_Simulation_Engine

# 개발 의존성 포함 설치
pip install -e ".[dev]"
```

### 방법 3: 전체 기능 포함 설치

```bash
# 저장소 클론
git clone https://github.com/qquartsco-svg/ADHD_Simulation_Engine.git
cd ADHD_Simulation_Engine

# 모든 선택적 의존성 포함 설치
pip install -e ".[full]"
```

---

## 🚀 Cookiie Brain Engine 설치

ADHD Simulation Engine은 Cookiie Brain Engine에 의존합니다.

### Cookiie Brain Engine 설치

```bash
# Cookiie Brain Engine 저장소 클론
git clone https://github.com/qquartsco-svg/cookiieBrain_alpha.git
cd cookiieBrain_alpha

# Cookiie Brain Engine 설치
pip install -e .
```

또는 Cookiie Brain Engine이 이미 설치되어 있다면, 경로를 환경 변수로 지정:

```bash
export COOKIIE_BRAIN_PATH="/path/to/cookiieBrain_alpha"
```

---

## ✅ 설치 확인

설치가 완료되었는지 확인:

```bash
# Python에서 import 테스트
python -c "from adhd_simulator import ADHDSimulator; print('✅ 설치 성공!')"
```

---

## 🎯 빠른 시작

### 명령줄에서 실행

```bash
# 기본 시뮬레이션
python -m adhd_simulator

# 옵션 지정
python -m adhd_simulator --age 15 --gender male --scenario adhd --seed 42
```

### Python 코드에서 사용

```python
from adhd_simulator import ADHDSimulator

# 시뮬레이터 초기화
simulator = ADHDSimulator(age=15, gender='male', seed=42)

# 시뮬레이션 실행
results = simulator.simulate_full_adhd_assessment(scenario='adhd')

# 결과 확인
print(results['scores'])
```

---

## 🐛 트러블슈팅

### 오류: "ModuleNotFoundError: No module named 'cookiie_brain'"

**원인**: Cookiie Brain Engine이 설치되지 않았거나 경로가 설정되지 않음

**해결**:
1. Cookiie Brain Engine 설치 확인
2. 환경 변수 `COOKIIE_BRAIN_PATH` 설정
3. Python 경로에 Cookiie Brain Engine 추가

### 오류: "ImportError: cannot import name 'ADHDSimulator'"

**원인**: 패키지가 제대로 설치되지 않음

**해결**:
```bash
pip install -e . --force-reinstall
```

### 오류: "matplotlib 한글 폰트 오류"

**원인**: 시스템에 한글 폰트가 없음

**해결**:
- macOS: 기본 폰트 사용 (AppleGothic)
- Linux: 한글 폰트 설치 필요
- Windows: 기본 폰트 사용

---

## 📚 추가 정보

- [README.md](README.md) - 프로젝트 개요
- [RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md) - 실행 가이드
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API 문서

---

## 💬 지원

문제가 발생하면 GitHub Issues에 문의하세요:
https://github.com/qquartsco-svg/ADHD_Simulation_Engine/issues

