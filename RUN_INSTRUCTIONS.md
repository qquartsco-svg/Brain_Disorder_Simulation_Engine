# 🚀 ADHD Simulation Engine 실행 가이드

## 📍 실행 파일 위치

```
/Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine/
├── adhd_simulator.py          # 메인 실행 파일
├── run_adhd_simulation.sh     # 실행 스크립트 (Unix/Mac)
└── ...
```

## 🎯 실행 방법

### 방법 1: Python 직접 실행

```bash
cd /Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine
python3 adhd_simulator.py
```

### 방법 2: 실행 스크립트 사용 (권장)

```bash
cd /Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine
./run_adhd_simulation.sh
```

### 방법 3: 환경 변수 설정 후 실행

```bash
export COOKIIE_BRAIN_PATH="/Users/jazzin/Desktop/00_BRAIN/Cookiie_Brain_Engine"
cd /Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine
python3 adhd_simulator.py
```

## 📋 실행 전 확인 사항

1. **Cookiie Brain Engine 경로 확인**
   - 기본 경로: `/Users/jazzin/Desktop/00_BRAIN/Cookiie_Brain_Engine`
   - 다른 위치에 있다면 `COOKIIE_BRAIN_PATH` 환경 변수 설정

2. **필수 패키지 설치**
   ```bash
   pip install numpy scipy matplotlib
   ```

3. **Python 버전**
   - Python 3.7 이상 필요

## 🔧 실행 옵션

현재 버전은 기본 설정으로 실행됩니다:
- Seed: 42 (고정)
- 폐루프 동역학: 활성화
- 도파민 시스템: 활성화
- 실험 메타데이터: 자동 생성

## 📊 실행 결과

실행 후 다음 파일들이 생성됩니다:

```
ADHD_Simulation_Engine/
├── results/
│   ├── adhd_simulation_results.png      # 시각화 결과
│   ├── experiment_report.json           # JSON 리포트
│   ├── experiment_report.md             # Markdown 리포트
│   └── experiment_report_visualization.png  # 리포트 시각화
└── ...
```

## 🐛 문제 해결

### ModuleNotFoundError: No module named 'cookiie_brain'

**해결 방법:**
```bash
# Cookiie Brain Engine 경로 확인
ls /Users/jazzin/Desktop/00_BRAIN/Cookiie_Brain_Engine/package

# 환경 변수 설정
export COOKIIE_BRAIN_PATH="/Users/jazzin/Desktop/00_BRAIN/Cookiie_Brain_Engine"
```

### 한글 폰트 경고

기능상 문제 없음. macOS에서는 AppleGothic이 자동으로 사용됩니다.

## 📝 예제 실행

```bash
# 기본 실행
./run_adhd_simulation.sh

# 또는 Python 직접 실행
python3 adhd_simulator.py
```

## ✅ 테스트 실행

```bash
# 동역학 불변식 테스트
python3 dynamics_invariant_tests.py

# 통합 테스트
python3 -c "from adhd_simulator import ADHDSimulator; print('✅ Import 성공')"
```

